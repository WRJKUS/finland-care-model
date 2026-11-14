"""Build the tidy signal table: one row per (signal, county, period) with numerator/denominator and availability date.
Every signal names its pathway step, endpoint definition and source. No patient-level data: all inputs are public aggregates."""
import pandas as pd, numpy as np, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]; T = ROOT / "data/tidy"
THL_LAG_DAYS = 45      # THL publishes queue snapshots ~1-1.5 months after the reference date (cube updated 19.10.2026 holds 30.09.2026)
ANNUAL_LAG_DAYS = 365  # registry/Sotkanet annual figures: year Y treated as available on 31.12.(Y+1)

d = pd.read_csv(T / "thl_queue.csv", parse_dates=["date"], dtype={"specialty": str})
d["producer"] = d.producer.str.strip()
NAT = "Kaikki hyvinvointialueet"
d = d[d.producer != "Helsingin sosiaali-, terveys- ja pelastustoimi"]
geo = json.load(open(ROOT / "data/raw/geo/hva.geojson"))
name2code = {f["properties"]["nimi"]: f["properties"]["hyvinvointialue"] for f in geo["features"]}
def code(p):
    if p == NAT: return "FI"
    if p == "HUS": return "HUS"
    return name2code[p]
d["county"] = d.producer.map(code)

def wide(specs, measures):
    x = d[d.specialty.isin(specs) & d.measure.isin(measures)]
    # require all requested specialties? no: sum what is reported, but record how many specialties reported
    w = x.pivot_table(index=["county", "date"], columns="measure", values="value", aggfunc="sum")
    return w

def ytd_to_flow(w, col):
    """Year-to-date cumulative -> flow in the period since the previous reported date of the same year. NaN if not derivable."""
    out = []
    for c, g in w[col].dropna().groupby(level=0):
        g = g.droplevel(0).sort_index()
        prev_date, prev_val = None, None
        for dt, v in g.items():
            if prev_date is None or prev_date.year != dt.year:
                start = pd.Timestamp(dt.year, 1, 1); flow = v
                # first report of the year must be the first period (Jan monthly-era, Apr tertile-era) else unknown span
                ok = (dt.month == 1) or (dt.year <= 2020 and dt.month == 4)
            else:
                start = prev_date; flow = v - prev_val; ok = flow >= 0
            days = (dt - start).days
            out.append((c, dt, flow if ok else np.nan, days))
            prev_date, prev_val = dt, v
    return pd.DataFrame(out, columns=["county", "date", col + "_flow", "days"]).set_index(["county", "date"])

rows = []
def add_share(sig, specs, num, den, min_den=1):
    w = wide(specs, [num, den]).dropna(subset=[den])
    w[num] = w[num].fillna(0)
    for (c, dt), r in w.iterrows():
        if r[den] >= min_den:
            rows.append(dict(signal=sig, county=c, period=dt, num=float(r[num]), den=float(r[den]), kind="share"))

# --- Treatment initiation (Goal 3 proxies) ---
add_share("treat_onc_over90", ["65"], "Yli 90 vrk hoitoa odottaneet", "Hoitoa odottaneet")
add_share("treat_surg_over90", ["20G", "20U"], "Yli 90 vrk hoitoa odottaneet", "Hoitoa odottaneet")
# oncology queue index: patients waiting for treatment / referral inflow per day  (days of inflow held in the queue)
w = wide(["65"], ["Hoitoa odottaneet", "Lähetteet yhteensä"])
f = ytd_to_flow(w, "Lähetteet yhteensä")
w = w.join(f)
for (c, dt), r in w.iterrows():
    if pd.notna(r["Hoitoa odottaneet"]) and pd.notna(r["Lähetteet yhteensä_flow"]) and r["Lähetteet yhteensä_flow"] > 0:
        rows.append(dict(signal="treat_onc_wait", county=c, period=dt, num=float(r["Hoitoa odottaneet"]),
                         den=float(r["Lähetteet yhteensä_flow"]) / r["days"], kind="ratio", den_count=float(r["Lähetteet yhteensä_flow"])))
# --- Diagnosis ---
add_share("dx_endo_over90", ["proc27"], "Yli 90 vrk toimenpidettä odottaneet", "Toimenpidettä odottaneet yhteensä")
# --- Referral (primary -> specialist handover) ---
add_share("ref_assess_over90", ["80", "10G", "20U", "20G", "30"], "Yli 90 vrk hoidon tarpeen arviointia odottaneet", "Hoidon tarpeen arviointia odottaneet")
w = wide(["ALL"], ["Lähete käsitelty yli 21 vrk:ssa", "Lähetteitä käsitelty yhteensä", "Lähetteet yhteensä", "Asukasluku"])
fa = ytd_to_flow(w, "Lähete käsitelty yli 21 vrk:ssa"); fb = ytd_to_flow(w, "Lähetteitä käsitelty yhteensä"); fc = ytd_to_flow(w, "Lähetteet yhteensä")
x = fa.join(fb, lsuffix="_a").join(fc, rsuffix="_c")
for (c, dt), r in x.iterrows():
    if pd.notna(r.iloc[0]) and pd.notna(r["Lähetteitä käsitelty yhteensä_flow"]) and r["Lähetteitä käsitelty yhteensä_flow"] > 0:
        rows.append(dict(signal="ref_over21", county=c, period=dt, num=float(r.iloc[0]), den=float(r["Lähetteitä käsitelty yhteensä_flow"]), kind="share"))
# referral volume, year-on-year (Model 2 flow; positive control 2020)
vol = fc.rename(columns={"Lähetteet yhteensä_flow": "flow"}).dropna().reset_index()
vol["key"] = list(zip(vol.county, vol.date.dt.month, vol.date.dt.day > 0))
prev = vol.assign(date=vol.date + pd.offsets.DateOffset(years=1))
prev["date"] = prev.date + pd.offsets.MonthEnd(0)
m = vol.merge(prev[["county", "date", "flow", "days"]], on=["county", "date"], suffixes=("", "_prev"))
for _, r in m.iterrows():
    if r.flow > 0 and r.flow_prev > 0 and abs(r.days - r.days_prev) <= 3:
        rows.append(dict(signal="ref_volume_yoy", county=r.county, period=r.date, num=float(r.flow), den=float(r.flow_prev), kind="ratio", den_count=float(r.flow_prev)))
# negative control: resident population reported in the same cube (should not move with care disruptions)
pop = w["Asukasluku"].dropna().reset_index()
pp = pop.assign(date=(pop.date + pd.offsets.DateOffset(years=1)) + pd.offsets.MonthEnd(0)).merge(pop, on=["county", "date"], suffixes=("_prev", ""))
for _, r in pp.iterrows():
    rows.append(dict(signal="ctrl_population_yoy", county=r.county, period=r.date, num=float(r.Asukasluku), den=float(r.Asukasluku_prev), kind="ratio", den_count=float(r.Asukasluku_prev)))
s = pd.DataFrame(rows)
s["available"] = s.period + pd.Timedelta(days=THL_LAG_DAYS)
s["source"] = "THL eshjono"
# --- Detection: organised screening participation (annual; Finnish Cancer Registry via Sotkanet) ---
k = pd.read_csv(T / "sotkanet.csv", dtype={"region_code": str})
k = k[k.gender.isin(["total", "female"])]
out = []
for ind, sig, g in [(3621, "det_screen_breast", "female"), (3620, "det_screen_cervix", "female"), (6103, "det_screen_colorectal", "total"),
                    (3625, "out_surv_breast", "total"), (3627, "out_surv_colon", "total"), (4404, "risk_smoking", "total"),
                    (4408, "risk_smoking_lowedu", "total"), (4410, "risk_smoking_highedu", "total"), (5502, "pc_continuity_coci", "total")]:
    x = k[(k.indicator == ind)]
    gg = g if (x.gender == g).any() else x.gender.iloc[0]
    x = x[x.gender == gg]
    for _, r in x.iterrows():
        c = "FI" if r["cat"] == "MAA" else str(r.region_code).zfill(2)
        out.append(dict(signal=sig, county=c, period=pd.Timestamp(int(r.year), 12, 31), num=r.value, den=np.nan, kind="pct",
                        available=pd.Timestamp(int(r.year), 12, 31) + pd.Timedelta(days=ANNUAL_LAG_DAYS), source=f"Sotkanet {ind}"))
s = pd.concat([s, pd.DataFrame(out)], ignore_index=True)
s.to_csv(T / "signals.csv", index=False)
print(s.groupby("signal").agg(n=("num", "count"), counties=("county", "nunique"), first=("period", "min"), last=("period", "max")).to_string())
