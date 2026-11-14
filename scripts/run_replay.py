"""Replay history in order. At each replay date the twin may use only observations already published (available <= T).
Writes runs/model1 (equality twin: county vs national gaps) and runs/model2 (pathway twin: national levels, change alarms),
plus baselines and controls. Nothing downstream recomputes."""
import pandas as pd, numpy as np, json, pathlib, datetime, sys, subprocess
from scipy.stats import norm
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
from twin.core import Q_GRID, PHI_GRID, PARAMS, transform, inverse, kfilter, smooth
SIG = json.load(open(ROOT / "twin/signals.json"))
s = pd.read_csv(ROOT / "data/tidy/signals.csv", parse_dates=["period", "available"], dtype={"county": str})
bad = (s.kind == "share") & (s.num > s.den)   # qc: impossible rows (numerator above denominator) are dropped and counted
print("dropped impossible share rows:", int(bad.sum()), s[bad].groupby("signal").size().to_dict()); s = s[~bad]
REPLAY = pd.date_range("2016-01-31", "2026-10-31", freq="ME")
t0 = pd.Timestamp("2000-01-01")
mon = lambda d: (d - t0).days / 30.4375
Z80 = 1.2816
records, fc_rows, series_out, alarms = [], [], {}, []
qstar_log = {}
for sig, cfg in SIG.items():
    g = s[s.signal == sig].sort_values("period")
    if g.empty: continue
    kind = cfg["kind"]; filt = {}
    for c, x in g.groupby("county"):
        yr = [transform(kind, a, b, dc) for a, b, dc in zip(x.num, x.den, x.get("den_count", pd.Series(np.nan, index=x.index)))]
        y = np.array([v[0] for v in yr]); r = np.array([v[1] for v in yr]); tm = np.array([mon(d) for d in x.period])
        filt[c] = dict(x=x.reset_index(drop=True), y=y, r=r, tm=tm, av=x.available.values, f=[kfilter(tm, y, r * phi, q) for q, phi in PARAMS])
    # expanding-window choice of q: cumulative predictive log-likelihood of everything published by T, pooled over counties
    def qidx_at(T):
        tot = np.zeros(len(PARAMS))
        for c, d in filt.items():
            n = int((d["av"] <= np.datetime64(T)).sum())
            if n > 1: tot += np.array([d["f"][k]["ll"][:n].sum() for k in range(len(PARAMS))])
        return int(np.argmax(tot)) if tot.any() else 8
    qi_T = {T: qidx_at(T) for T in REPLAY}
    qstar_log[sig] = {str(T.date()): list(PARAMS[k]) for T, k in qi_T.items() if T.month == 12 or T == REPLAY[-1]}
    qi_final = qi_T[REPLAY[-1]]
    # hindsight ("judged") series: two-sided smoother with the final q. Used only for scoring, never for decisions.
    for c, d in filt.items():
        ms, Ps = smooth(d["tm"], d["f"][qi_final], PARAMS[qi_final][0])
        d["ms"], d["Ps"] = ms, Ps
        series_out[f"{sig}|{c}"] = dict(period=[str(p.date()) for p in d["x"].period], obs=[round(float(v), 4) for v in inverse(kind, d["y"])],
                                        num=[float(v) for v in d["x"].num], den=[round(float(v), 3) for v in d["x"].den],
                                        smooth=[round(float(v), 4) for v in inverse(kind, ms)], smooth_x=[round(float(v), 4) for v in ms],
                                        smooth_sd=[round(float(v), 4) for v in np.sqrt(Ps)])
    def state(c, T, k):
        d = filt.get(c)
        if d is None: return None
        n = int((d["av"] <= np.datetime64(T)).sum())
        if n == 0: return None
        f = d["f"][k]; last_p = d["x"].period[n - 1]
        gap_m = max(mon(T) - d["tm"][n - 1], 0.0)
        return dict(m=f["m"][n - 1], P=f["P"][n - 1], n=n, last=last_p, stale_m=gap_m, y=d["y"][n - 1],
                    num=float(d["x"].num[n - 1]), den=float(d["x"].den[n - 1]),
                    m_prev=f["m"][max(n - 1 - cfg["trend_lag"], 0)] if n > cfg["trend_lag"] else np.nan)
    sgn = cfg["bad_direction"]   # +1: higher is worse, -1: lower is worse, 0: no judgement
    for T in REPLAY:
        k = qi_T[T]; ref = state("FI", T, k)
        for c in filt:
            st = state(c, T, k)
            if st is None: continue
            sd = np.sqrt(st["P"]); lvl = float(inverse(kind, st["m"])); lo = float(inverse(kind, st["m"] - Z80 * sd)); hi = float(inverse(kind, st["m"] + Z80 * sd))
            width = (hi - lo) if kind != "ratio" else hi / max(lo, 1e-9)
            stale = st["stale_m"] > cfg["stale_months"]
            small = (st["den"] < cfg.get("min_den", 0)) or (st["num"] < cfg.get("min_num", 0))
            ident = (width <= cfg["ident_width"]) and not stale and not small
            rec = dict(t=str(T.date()), signal=sig, step=cfg["step"], county=c, data_through=str(st["last"].date()), n_obs=st["n"],
                       obs=round(float(inverse(kind, st["y"])), 4), num=st["num"], den=round(st["den"], 3), level=round(lvl, 4), lo=round(lo, 4), hi=round(hi, 4),
                       identifiable=bool(ident), small_numbers=bool(small), q=float(PARAMS[k][0]), phi=float(PARAMS[k][1]),
                       q_at_bound=bool(PARAMS[k][0] in (Q_GRID[0], Q_GRID[-1])), phi_at_bound=bool(PARAMS[k][1] == PHI_GRID[-1]))
            if not np.isnan(st["m_prev"]): rec["trend"] = round(lvl - float(inverse(kind, st["m_prev"])), 4)
            p_gap = None
            if c != "FI" and ref is not None and sgn != 0:
                refl = float(inverse(kind, ref["m"])); rec["ref"] = round(refl, 4)
                thr_nat = refl + sgn * cfg["delta"] if cfg["delta_type"] == "abs" else refl * (cfg["delta"] if sgn > 0 else 1 / cfg["delta"])
                thr_nat = min(max(thr_nat, 1e-4), 0.9999) if kind != "ratio" else thr_nat
                thr_x = np.log(thr_nat / (1 - thr_nat)) if kind != "ratio" else np.log(thr_nat)
                p_gap = float(norm.cdf(sgn * (st["m"] - thr_x) / np.sqrt(st["P"] + ref["P"])))
                rec["gap"] = round(lvl - refl, 4); rec["p_gap"] = round(p_gap, 3); rec["thr"] = round(float(thr_nat), 4)
            if "target" in cfg and sgn != 0:
                tx = np.log(cfg["target"] / (1 - cfg["target"]))
                rec["p_miss_target"] = round(float(norm.cdf(sgn * (st["m"] - tx) / sd)), 3)
            rec["status"] = ("stale" if stale else "unidentifiable" if not ident else "n/a" if p_gap is None else
                             "gap" if p_gap >= 0.9 else "watch" if p_gap >= 0.7 else "ok")
            records.append(rec)
    # one-step-ahead forecasts on periods the estimator had not seen: twin vs persistence vs linear trend
    if cfg.get("score_forecast", True):
        for c, d in filt.items():
            n = len(d["y"])
            for i in range(6, n):
                Tprev = pd.Timestamp(d["x"].period[i]) - pd.Timedelta(days=1)   # information set: everything up to the previous period
                Tq = REPLAY[REPLAY <= Tprev]
                k = qi_T[Tq[-1]] if len(Tq) else 8
                tw = d["f"][k]["m0"][i]
                pe = d["y"][i - 1]
                xs = d["tm"][i - 6:i]; b = np.polyfit(xs, d["y"][i - 6:i], 1); tr = b[0] * d["tm"][i] + b[1]
                tr = float(np.clip(tr, d["y"][i - 6:i].min() - 3, d["y"][i - 6:i].max() + 3))
                act = float(inverse(kind, d["y"][i]))
                fc_rows.append(dict(signal=sig, county=c, period=str(d["x"].period[i].date()), actual=act, den=float(d["x"].den[i]),
                                    twin=float(inverse(kind, tw)), persistence=float(inverse(kind, pe)), trend=float(inverse(kind, tr)),
                                    z=float((d["y"][i] - tw) / np.sqrt(d["f"][k]["P0"][i] + d["r"][i] * PARAMS[k][1]))))
rec = pd.DataFrame(records); fc = pd.DataFrame(fc_rows)
# ---- Model 2 change alarms: national one-step-ahead surprise |z| >= 3 (model threshold), on the publication date of that period
for sig in fc.signal.unique():
    x = fc[(fc.signal == sig) & (fc.county == "FI")]
    for _, r in x[abs(x.z) >= 3].iterrows():
        alarms.append(dict(signal=sig, period=r.period, z=round(r.z, 2), actual=round(r.actual, 4), expected=round(r.twin, 4)))
# ---- baselines scorecard
def mae(x, col): return float(np.mean(np.abs(x[col] - x.actual)))
def mdae(x, col): return float(np.median(np.abs(x[col] - x.actual)))
base = []
for sig, x in fc[fc.county != "FI"].groupby("signal"):
    base.append(dict(signal=sig, n=len(x), twin=mae(x, "twin"), persistence=mae(x, "persistence"), trend=mae(x, "trend"), twin_md=mdae(x, "twin"), persistence_md=mdae(x, "persistence"), trend_md=mdae(x, "trend"),
                     coverage80=float(np.mean(np.abs(x.z) <= Z80))))
base = pd.DataFrame(base)
base["beats_persistence"] = base.twin < base.persistence; base["beats_trend"] = base.twin < base.trend
ts = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
git = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip()
for model, sel in [("model1", rec[rec.county != "FI"]), ("model2", rec[rec.county == "FI"])]:
    out = ROOT / f"runs/{model}/replay/{ts}"; out.mkdir(parents=True)
    sel.to_csv(out / "records.csv", index=False)
    json.dump(dict(model=model, produced_by="scripts/run_replay.py", timestamp=ts, git=git, replay=[str(REPLAY[0].date()), str(REPLAY[-1].date())],
                   q_grid=Q_GRID.tolist(), phi_grid=PHI_GRID.tolist(), q_selected=qstar_log, signals=SIG, n_records=len(sel)), open(out / "meta.json", "w"), indent=1)
    if model == "model1":
        fc.to_csv(out / "forecasts.csv", index=False); base.to_csv(out / "baselines.csv", index=False)
        json.dump(series_out, open(out / "series.json", "w"))
    else:
        json.dump(alarms, open(out / "alarms.json", "w"), indent=1)
    (ROOT / f"runs/{model}/replay/LATEST").write_text(ts)
pd.set_option("display.width", 200)
print(base.round(4).to_string())
print("q selected (final):", {k: list(v.values())[-1] for k, v in qstar_log.items()})
last = rec[(rec.t == str(REPLAY[-1].date())) & (rec.county != "FI")]
print(last.groupby(["signal", "status"]).size().unstack(fill_value=0).to_string())
print([a for a in alarms if a["period"].startswith("2020") or a["period"].startswith("2021-0")])
x = fc[(fc.county == "FI") & fc.signal.isin(["ref_volume_yoy", "ctrl_population_yoy", "det_screen_breast", "det_screen_cervix"]) & fc.period.between("2019-12-01", "2021-12-31")]
print(x[["signal", "period", "actual", "twin", "z"]].round(3).to_string())
