"""Models 3 and 4: the same lever (county pathway pilot slot) and the same budget, different monitoring.
Counterfactual on history ("had this been in place over these years"), never a forecast. Definitions: SCORECARD.md."""
import pandas as pd, numpy as np, json, pathlib, datetime, subprocess
ROOT = pathlib.Path(__file__).resolve().parents[1]
SIG = json.load(open(ROOT / "twin/signals.json"))
ts1 = (ROOT / "runs/model1/replay/LATEST").read_text()
rec = pd.read_csv(ROOT / f"runs/model1/replay/{ts1}/records.csv", dtype={"county": str}, parse_dates=["t"])
ser = json.load(open(ROOT / f"runs/model1/replay/{ts1}/series.json"))
raw = pd.read_csv(ROOT / "data/tidy/signals.csv", parse_dates=["period", "available"], dtype={"county": str})
raw = raw[~((raw.kind == "share") & (raw.num > raw.den))]
K = 3; MIN_RUN = 6
MONTHS = pd.date_range("2021-01-31", "2026-10-31", freq="ME")
POLICY = ["treat_onc_wait", "dx_endo_over90", "ref_assess_over90"]
EFFECTS = {"zero (E05)": 0.0, "conservative (half of E04)": 0.1625, "high (E04: 53.2 -> 35.9 days)": 0.325}
rng = np.random.default_rng(20261114)

def thr(cfg, nat):
    return nat * cfg["delta"] if cfg["delta_type"] == "rel" else nat + cfg["delta"]

def truth(sig):
    cfg = SIG[sig]; kind = cfg["kind"]
    inv = (lambda x: np.exp(x)) if kind == "ratio" else (lambda x: 1 / (1 + np.exp(-x)))
    fi = ser[f"{sig}|FI"]; fip = pd.to_datetime(fi["period"]); out = {}
    for key, s in ser.items():
        g, c = key.split("|")
        if g != sig or c == "FI": continue
        p = pd.to_datetime(s["period"]); rows = []
        for T in MONTHS:
            i = np.searchsorted(p.values, np.datetime64(T), side="right") - 1
            j = np.searchsorted(fip.values, np.datetime64(T), side="right") - 1
            if i < 0 or j < 0 or (T - p[i]).days > 186: rows.append((False, np.nan, np.nan, False)); continue
            lvl = float(inv(s["smooth_x"][i])); nat = float(inv(fi["smooth_x"][j])); th = thr(cfg, nat)
            small = s["den"][i] < cfg.get("min_den", 0) or s["num"][i] < cfg.get("min_num", 0)
            rows.append((bool(lvl > th and not small), lvl, th, True))
        out[c] = pd.DataFrame(rows, index=MONTHS, columns=["gap", "level", "thr", "observed"])
    return out

def model3(sig, lag_years):
    cfg = SIG[sig]; g = raw[raw.signal == sig].assign(y=lambda d: d.period.dt.year)
    active = {c: np.zeros(len(MONTHS), bool) for c in g.county.unique() if c != "FI"}; log = []
    for Y in range(2021, 2027):
        yy = Y - lag_years; a = g[g.y == yy].groupby("county").agg(num=("num", "sum"), den=("den", "sum"), n=("num", "size"))
        if "FI" not in a.index: continue
        a["val"] = a.num / a.den; nat = a.loc["FI", "val"]; th = thr(cfg, nat)
        a = a.drop("FI"); a = a[(a.den / a.n >= cfg.get("min_den", 0)) & (a.num / a.n >= cfg.get("min_num", 0))]
        a["excess"] = a.val - th; pick = a[a.excess > 0].sort_values("excess", ascending=False).head(K)
        start = pd.Timestamp(Y, 2, 28) + pd.offsets.MonthEnd(0); end = pd.Timestamp(Y + 1, 1, 31)
        for c, r in pick.iterrows():
            active[c] |= (MONTHS >= start) & (MONTHS <= end)
            log.append(dict(signal=sig, county=c, start=str(start.date()), end=str(min(end, MONTHS[-1]).date()), decided=f"{Y}-01-31", evidence=f"annual value {yy}: {r.val:.3g} vs national {nat:.3g} (threshold {th:.3g})"))
    return active, log

def model4(sig):
    r = rec[rec.signal == sig]; counties = [c for c in r.county.unique()]
    active = {c: np.zeros(len(MONTHS), bool) for c in counties}; running = {}; log = []
    for i, T in enumerate(MONTHS[:-1]):
        now = r[r.t == T].set_index("county")
        for c in list(running):
            st = now.status.get(c, "none")
            if running[c]["n"] >= MIN_RUN and st != "gap":
                running[c]["rec"]["end"] = str(T.date()); del running[c]
        cand = now[(now.status == "gap") & ~now.index.isin(list(running))].copy()
        cand["score"] = cand.p_gap * (cand.level - cand.thr) / cand.thr.clip(lower=1e-6)
        for c, x in cand.sort_values("score", ascending=False).iterrows():
            if len(running) >= K: break
            e = dict(signal=sig, county=c, start=str(MONTHS[i + 1].date()), end=str(MONTHS[-1].date()), decided=str(T.date()),
                     evidence=f"level {x.level:.3g} [{x.lo:.3g}, {x.hi:.3g}] vs threshold {x.thr:.3g}, P(gap)={x.p_gap:.2f}, data through {x.data_through}")
            running[c] = dict(n=0, rec=e); log.append(e)
        for c in running:
            active[c][i + 1] = True; running[c]["n"] += 1
    return active, log

def score(tr, active, counties=None):
    cs = counties if counties is not None else list(tr)
    gm = cov = used = hit = wsum = wcov = 0.0
    for c in cs:
        g = tr[c].gap.values; a = active.get(c, np.zeros(len(MONTHS), bool)); w = np.where(g, (tr[c].level - tr[c].thr).fillna(0).values, 0)
        gm += g.sum(); cov += (g & a).sum(); used += a.sum(); hit += (g & a).sum(); wsum += w.sum(); wcov += (w * a).sum()
    return dict(true_gap_months=int(gm), covered=int(cov), coverage=cov / gm if gm else np.nan, slot_months_used=int(used),
                precision=hit / used if used else np.nan, weighted_coverage=wcov / wsum if wsum else np.nan)

def episodes(tr, active):
    out = []
    for c in tr:
        g = tr[c].gap.values; i = 0
        while i < len(g):
            if g[i]:
                j = i
                while j < len(g) and g[j]: j += 1
                if j - i >= 3:
                    a = active.get(c, np.zeros(len(g), bool))[i:j]
                    out.append(dict(county=c, start=str(MONTHS[i].date()), months=int(j - i), lead=int(np.argmax(a)) if a.any() else None))
                i = j
            else: i += 1
    return out

card = {"budget": dict(K=K, months=len(MONTHS), cap_slot_months=K * len(MONTHS)), "signals": {}}
ts = datetime.datetime.now().strftime("%Y%m%dT%H%M%S"); slots = {"model3": [], "model3fast": [], "model4": []}
for sig in POLICY:
    tr = truth(sig); runs = {"model3": model3(sig, 2), "model3fast": model3(sig, 1), "model4": model4(sig)}
    res = {}
    for m, (act, log) in runs.items():
        slots[m] += log; sc = score(tr, act); ep = episodes(tr, act)
        leads = [e["lead"] for e in ep if e["lead"] is not None]
        sc.update(episodes=len(ep), episodes_reached=len(leads), median_lead_months=float(np.median(leads)) if leads else None,
                  missed=[f'{e["county"]} from {e["start"]} ({e["months"]} mo)' for e in ep if e["lead"] is None], episode_list=ep)
        if sig == "treat_onc_wait":
            tot = sum(np.where(tr[c].gap, tr[c].level - tr[c].thr, 0).sum() for c in tr)
            sc["scenario_excess_queue_days_removed"] = {k: float(sum(np.where(tr[c].gap & act.get(c, False), np.minimum(e * tr[c].level, tr[c].level - tr[c].thr), 0).sum() for c in tr)) for k, e in EFFECTS.items()}
            sc["scenario_total_excess"] = float(tot)
        res[m] = sc
    cs = list(tr); boots = {"model3": [], "model3fast": []}
    for _ in range(2000):
        b = list(rng.choice(cs, len(cs)))
        c4 = score(tr, runs["model4"][0], b)["coverage"]
        for m in boots: boots[m].append(c4 - score(tr, runs[m][0], b)["coverage"])
    for m in boots:
        v = np.array(boots[m]); v = v[~np.isnan(v)]
        res[f"model4_minus_{m}_coverage"] = dict(point=res["model4"]["coverage"] - res[m]["coverage"], lo80=float(np.quantile(v, .1)), hi80=float(np.quantile(v, .9)))
    res["truth"] = {c: dict(gap=[int(x) for x in tr[c].gap], level=[None if np.isnan(x) else round(float(x), 4) for x in tr[c].level], thr=[None if np.isnan(x) else round(float(x), 4) for x in tr[c].thr]) for c in tr}
    res["active"] = {m: {c: [int(x) for x in a] for c, a in runs[m][0].items() if a.any()} for m in runs}
    card["signals"][sig] = res
git = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip()
for m, log in slots.items():
    out = ROOT / f"runs/{m}/policy/{ts}"; out.mkdir(parents=True); pd.DataFrame(log).to_csv(out / "slots.csv", index=False)
    json.dump(dict(model=m, produced_by="scripts/run_policy.py", timestamp=ts, git=git, inputs=f"runs/model1/replay/{ts1}", K=K, min_run=MIN_RUN, effects=EFFECTS), open(out / "meta.json", "w"), indent=1)
    (ROOT / f"runs/{m}/policy/LATEST").write_text(ts)
out = ROOT / f"runs/compare/policy/{ts}"; out.mkdir(parents=True)
card["months"] = [str(m.date()) for m in MONTHS]
json.dump(card, open(out / "scorecard.json", "w"), indent=1); json.dump(dict(produced_by="scripts/run_policy.py", timestamp=ts, git=git), open(out / "meta.json", "w"))
(ROOT / "runs/compare/policy/LATEST").write_text(ts)
for sig, res in card["signals"].items():
    print("\n==", sig)
    for m in ["model3", "model3fast", "model4"]:
        s = res[m]; print(f'{m:11s} gap-months {s["true_gap_months"]:4d} coverage {s["coverage"]:.2f} wcov {s["weighted_coverage"]:.2f} precision {s["precision"]:.2f} used {s["slot_months_used"]:3d} episodes {s["episodes_reached"]}/{s["episodes"]} lead {s["median_lead_months"]}', s.get("scenario_excess_queue_days_removed", ""))
    print({k: {a: round(b, 2) for a, b in v.items()} for k, v in res.items() if k.startswith("model4_minus")})
