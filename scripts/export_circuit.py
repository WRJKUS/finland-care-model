"""Export the small data file the Typst circuit document reads (visuals/circuit/data.json).
Reads runs/ and twin/ registries. The step combiner below mirrors demo/template.html (stepStatus): a step takes the
worst status of its signals; a step that has a cancer-specific signal is 'ok' only if that signal is ok.
One exception to "never recompute": Model 3's yearly view of a single county is not stored in runs/, so it is rebuilt
here with run_policy.model3's exact rule from data/tidy/signals.csv, and checked against the stored Model 3 slots."""
import pandas as pd, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
L = lambda p: (ROOT / p / "LATEST").read_text().strip()
SIG = json.load(open(ROOT / "twin/signals.json")); CT = json.load(open(ROOT / "twin/counties.json"))
r1 = ROOT / "runs/model1/replay" / L("runs/model1/replay")
rec = pd.read_csv(r1 / "records.csv", dtype={"county": str})
rec["status"] = rec.status.fillna("n/a")
card = json.load(open(ROOT / "runs/compare/policy" / L("runs/compare/policy") / "scorecard.json"))
ST = {"gap": "g", "watch": "w", "ok": "o", "unidentifiable": "u", "stale": "s", "n/a": "n"}
RANK = {"g": 5, "w": 4, "o": 3, "u": 2, "s": 1, "n": 0, "x": 0}
STEPSIG = {"detection": ["det_screen_breast", "det_screen_cervix", "det_screen_colorectal"],
           "referral": ["ref_assess_over90", "ref_over21"], "diagnosis": ["dx_endo_over90"],
           "treatment": ["treat_onc_wait", "treat_onc_over90", "treat_surg_over90"]}
months = sorted(rec.t.unique())
st = {(r.signal, r.county, r.t): ST[r.status] for r in rec[["signal", "county", "t", "status"]].itertuples(index=False)}

def step_status(step, c, t):
    best, cs, csok = "x", False, False
    for s in STEPSIG[step]:
        x = st.get((s, c, t), "x")
        if RANK[x] > RANK[best]: best = x
        if SIG[s]["cancer_specific"]:
            cs = True; csok = csok or x == "o"
    return "u" if best == "o" and cs and not csok else best

steps = {}
for step, sigs in STEPSIG.items():
    units = sorted(rec[rec.signal.isin(sigs)].county.unique())
    counts = {k: [] for k in "gwousx"}
    for t in months:
        v = [step_status(step, c, t) for c in units]
        for k in counts: counts[k].append(sum(1 for z in v if (z if z != "n" else "x") == k))
    steps[step] = dict(units=len(units), counts=counts)

# timing traces for the three policy channels (policy window only)
pm = card["months"]; timing = {}
for sig, res in card["signals"].items():
    rows = []
    for c, tr in res["truth"].items():
        a3 = res["active"]["model3"].get(c, [0] * len(pm)); a4 = res["active"]["model4"].get(c, [0] * len(pm))
        if not (any(tr["gap"]) or any(a3) or any(a4)): continue
        m1 = "".join(st.get((sig, c, t), "x") for t in pm)
        rows.append(dict(county=c, name=CT[c]["en"], truth=tr["gap"], m1=m1, m3=a3, m4=a4,
                         gap_months=sum(tr["gap"]), m3_hit=sum(g & a for g, a in zip(tr["gap"], a3)), m4_hit=sum(g & a for g, a in zip(tr["gap"], a4))))
    rows.sort(key=lambda r: -r["gap_months"])
    keep = {k: res[k] for k in ("model3", "model3fast", "model4")}
    summ = {m: {k: keep[m][k] for k in ("true_gap_months", "covered", "coverage", "slot_months_used", "precision", "episodes", "episodes_reached", "median_lead_months")} for m in keep}
    timing[sig] = dict(rows=rows, summary=summ, diff={k: res[k] for k in res if k.startswith("model4_minus")})

ex = rec[(rec.signal == "dx_endo_over90") & (rec.county == "19") & (rec.t == "2021-06-30")].iloc[0]
example = {k: (None if pd.isna(ex[k]) else (float(ex[k]) if isinstance(ex[k], (int, float)) else str(ex[k]))) for k in ["t", "data_through", "num", "den", "obs", "level", "lo", "hi", "ref", "thr", "gap", "p_gap", "q", "phi", "status", "identifiable"]}
xs = rec[(rec.signal == "dx_endo_over90") & (rec.county == "19")].set_index("t")
nz = lambda v: None if pd.isna(v) else round(float(v), 4)
example_series = dict(t=list(xs.index), level=[nz(v) for v in xs.level], lo=[nz(v) for v in xs.lo], hi=[nz(v) for v in xs.hi],
                      ref=[nz(v) for v in xs.ref], thr=[nz(v) for v in xs.thr], den=[nz(v) for v in xs.den], status=[ST[v] for v in xs.status],
                      m3=card["signals"]["dx_endo_over90"]["active"]["model3"].get("19"), m4=card["signals"]["dx_endo_over90"]["active"]["model4"].get("19"),
                      truth=card["signals"]["dx_endo_over90"]["truth"]["19"]["gap"])
# --- one channel over the whole replay: need (hindsight) against what each model saw and did --------------------------
SIGNAL, C = "dx_endo_over90", "19"
cfg = SIG[SIGNAL]
mk = lambda d: (pd.Timestamp(d).year - 2016) * 12 + pd.Timestamp(d).month - 1      # month index, 0 = Jan 2016
SER = json.load(open(r1 / "series.json"))
sc, sf = SER[f"{SIGNAL}|{C}"], SER[f"{SIGNAL}|FI"]
fper = pd.to_datetime(sf["period"])
hind = []
for i, p in enumerate(pd.to_datetime(sc["period"])):
    j = fper.searchsorted(p, side="right") - 1                                       # same alignment as run_policy.truth
    nat = sf["smooth"][j]; thr = nat + cfg["delta"]
    hind.append(dict(k=mk(p), period=str(p.date()), num=sc["num"][i], den=sc["den"][i], share=round(sc["num"][i] / sc["den"][i], 4),
                     level=sc["smooth"][i], nat=nat, thr=round(thr, 4), need=bool(sc["smooth"][i] > thr and sc["den"][i] >= cfg["min_den"])))
runs, cur = [], []
for h in hind:
    if h["need"]: cur.append([h["k"], h["level"], h["thr"]])
    elif cur: runs.append(cur); cur = []
if cur: runs.append(cur)
nat_line = [[mk(p), v, round(v + cfg["delta"], 4)] for p, v in zip(fper, sf["smooth"])]
rt = [dict(k=mk(t), level=nz(r.level), lo=nz(r.lo), hi=nz(r.hi), thr=nz(r.thr), ref=nz(r.ref), p=nz(r.p_gap), status=ST[r.status], through=r.data_through)
      for t, r in xs.iterrows()]
pol = card["signals"][SIGNAL]
use = {m: [sum(v[i] for v in pol["active"][m].values()) for i in range(len(pm))] for m in ("model3", "model4")}
slots = {}
for m in ("model3", "model4"):
    s = pd.read_csv(ROOT / f"runs/{m}/policy" / L(f"runs/{m}/policy") / "slots.csv", dtype={"county": str})
    s = s[(s.signal == SIGNAL) & (s.county == C)]
    slots[m] = [dict(decided=r.decided, k_decided=mk(r.decided), k_start=mk(r.start), k_end=mk(r.end), evidence=r.evidence) for r in s.itertuples()]
# Model 3's yearly view (rebuilt with run_policy.model3's rule; see docstring)
raw = pd.read_csv(ROOT / "data/tidy/signals.csv", parse_dates=["period"], dtype={"county": str})
raw = raw[~((raw.kind == "share") & (raw.num > raw.den))]
g = raw[raw.signal == SIGNAL].assign(y=lambda d: d.period.dt.year)
m3view = []
for Y in range(2021, 2027):
    a = g[g.y == Y - 2].groupby("county").agg(num=("num", "sum"), den=("den", "sum"), n=("num", "size"))
    a["val"] = a.num / a.den; nat = float(a.loc["FI", "val"]); th = nat + cfg["delta"]
    b = a.drop("FI"); el = b[(b.den / b.n >= cfg.get("min_den", 0)) & (b.num / b.n >= cfg.get("min_num", 0))].copy()
    el["excess"] = el.val - th; picks = list(el[el.excess > 0].sort_values("excess", ascending=False).head(3).index)
    stored = sorted(s.county for s in pd.read_csv(ROOT / "runs/model3/policy" / L("runs/model3/policy") / "slots.csv", dtype={"county": str}).itertuples()
                    if s.signal == SIGNAL and s.decided == f"{Y}-01-31")
    assert sorted(picks) == stored, (Y, picks, stored)                                # rebuilt view must reproduce the stored decisions
    r = a.loc[C]
    m3view.append(dict(year=Y, data_year=Y - 2, val=round(float(r.val), 4), nat=round(nat, 4), thr=round(th, 4), mean_den=round(float(r.den / r.n), 1),
                       eligible=bool(C in el.index), picked=bool(C in picks), k_from=mk(f"{Y}-01-31"), k_to=min(mk(f"{Y + 1}-01-31"), mk("2026-10-31"))))
truth = pol["truth"][C]["gap"]; a3 = pol["active"]["model3"].get(C, [0] * len(pm)); a4 = pol["active"]["model4"].get(C, [0] * len(pm))
channel = dict(signal=SIGNAL, county=C, name=CT[C]["en"], delta=cfg["delta"], min_den=cfg["min_den"], k_policy0=mk(pm[0]), hind=hind, need_runs=runs,
               nat_line=nat_line, rt=rt, m3view=m3view, truth=truth, m3=a3, m4=a4, use3=use["model3"], use4=use["model4"], slots3=slots["model3"], slots4=slots["model4"],
               need_months=sum(truth), m3_hit=sum(x & y for x, y in zip(truth, a3)), m4_hit=sum(x & y for x, y in zip(truth, a4)),
               all_cov=dict(m3=pol["model3"]["coverage"], m4=pol["model4"]["coverage"]))
sigs = {k: dict(step=v["step"], kind=v["kind"], delta=v["delta"], delta_type=v["delta_type"], origin=v["delta_origin"], cancer_specific=v["cancer_specific"], label=v["label_en"], source=v["source"]) for k, v in SIG.items()}
out = ROOT / "visuals/circuit"; out.mkdir(parents=True, exist_ok=True)
json.dump(dict(produced_by="scripts/export_circuit.py", model1_run=str(r1.relative_to(ROOT)), policy_run=L("runs/compare/policy"),
               replay_months=months, policy_months=pm, steps=steps, timing=timing, example=example, example_series=example_series, channel=channel, signals=sigs), open(out / "data.json", "w"), indent=1)
print("wrote", out / "data.json", {s: len(t["rows"]) for s, t in timing.items()})
