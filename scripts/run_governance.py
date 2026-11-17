"""Governance suggestions on the replay (rules: GOVERNANCE.md, thresholds: twin/governance.json).
Reads only stored runs (Model 1 records, Model 2 alarms, the policy scorecard's hindsight truth); never recomputes a model and never looks ahead.
Writes runs/governance/replay/<timestamp>/{records.csv, metrics.json, meta.json} and LATEST.

One code per (signal, unit, replay month):
  1-4  ladder rung (1 unit, 2 county management, 3 collaborative area, 4 national), only while the unit is in gap
  H    hold: a gap that reached rung 2+ has closed, for fewer than closed_months
  X    stop: closed closed_months in a row after reaching rung 2+ (release the slot, record the outcome)
  D    data request (cannot be judged)      S  stale data (no new figure for over 6 months)
  w    watch (no decision asked)             -  nothing
"""
import json, pathlib, subprocess, datetime as dt
import numpy as np, pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
L = lambda p: (ROOT / p / "LATEST").read_text().strip()
G = json.load(open(ROOT / "twin/governance.json")); R = G["rules"]
PERSIST, MIN_ACT, NAT_N, ALARM_W, CLOSED = R["persist_months"], R["min_action_months"], R["national_counties"], R["alarm_window_months"], R["closed_months"]
STEPSIG = {"detection": ["det_screen_breast", "det_screen_cervix", "det_screen_colorectal"], "referral": ["ref_assess_over90", "ref_over21"],
           "diagnosis": ["dx_endo_over90"], "treatment": ["treat_onc_wait", "treat_onc_over90", "treat_surg_over90"]}
STEP = {s: k for k, v in STEPSIG.items() for s in v}
YTA = {u: k for k, v in G["yta"].items() for u in v["members"]}

r1 = ROOT / "runs/model1/replay" / L("runs/model1/replay"); r2 = ROOT / "runs/model2/replay" / L("runs/model2/replay")
pc = ROOT / "runs/compare/policy" / L("runs/compare/policy")
rec = pd.read_csv(r1 / "records.csv", dtype={"county": str}); rec = rec[rec.signal.isin(STEP) & (rec.county != "FI")]
rec["status"] = rec.status.fillna("n/a")
months = sorted(rec.t.unique()); mi = {m: i for i, m in enumerate(months)}; N = len(months)
card = json.load(open(pc / "scorecard.json"))

# Model 2 national alarms, known from the first replay month at least 45 days after the period (publication lag of the THL queue figures)
alarm = {s: np.zeros(N, bool) for s in STEP}
for a in json.load(open(r2 / "alarms.json")):
    if a["signal"] not in alarm: continue
    known = pd.Timestamp(a["period"]) + pd.Timedelta(days=45)
    k = next((i for i, m in enumerate(months) if pd.Timestamp(m) >= known), None)
    if k is not None: alarm[a["signal"]][k:k + ALARM_W] = True

ST = {}   # (signal, unit) -> array of statuses
for (s, u), g in rec.groupby(["signal", "county"]):
    a = np.array(["n/a"] * N, dtype=object)
    for x in g.itertuples(): a[mi[x.t]] = x.status
    ST[s, u] = a
ngap = {s: np.array([sum(ST[k][i] == "gap" for k in ST if k[0] == s) for i in range(N)]) for s in STEP}
national = {s: (ngap[s] >= NAT_N) | alarm[s] for s in STEP}

rows, CODES = [], {}
for (s, u), st in sorted(ST.items()):
    codes = ["-"] * N; ep = False; ep_start = decision = None; run = closed = 0
    for i in range(N):
        x = st[i]
        if x == "gap":
            if not ep: ep, ep_start, decision = True, i, None
            run += 1; closed = 0
            if decision is None and run >= PERSIST: decision = i
            rung = 1 if decision is None else (3 if i - decision >= MIN_ACT else 2)
            if national[s][i]: rung = 4
            codes[i] = str(rung)
        else:
            run = 0
            if ep and decision is not None:
                if x in ("unidentifiable", "stale", "n/a"): codes[i] = "D" if x == "unidentifiable" else "S" if x == "stale" else "H"   # cannot tell whether it closed: the episode stays open
                else:
                    closed += 1
                    if closed >= CLOSED: codes[i] = "X"; ep, decision, closed = False, None, 0
                    else: codes[i] = "H"
            else:
                ep, decision = False, None
                codes[i] = {"watch": "w", "unidentifiable": "D", "stale": "S"}.get(x, "-")
        rows.append(dict(t=months[i], signal=s, step=STEP[s], unit=u, yta=YTA.get(u, ""), status=x, code=codes[i],
                         episode_start=months[ep_start] if ep and ep_start is not None else "", decision=months[decision] if ep and decision is not None else "",
                         counties_in_gap=int(ngap[s][i]), national_alarm=bool(alarm[s][i])))
    CODES[s, u] = "".join(codes)

# ---- scoring on the three policy signals against the hindsight truth (2021-01 .. 2026-10)
cm = card["months"]; ci = [mi[m] for m in cm]; years = len(cm) / 12
def runs_of(b):
    out, i = [], 0
    while i < len(b):
        if b[i]:
            j = i
            while j < len(b) and b[j]: j += 1
            out.append((i, j)); i = j
        else: i += 1
    return out
M = {}
for s, cs in card["signals"].items():
    eps = esc3 = esc3_false = gm = gm_none = dmon = dmon_true = 0; lead_dec, lead_any, reached = [], [], 0; per_yta = {}
    for u, tr in cs["truth"].items():
        code = "".join(CODES.get((s, u), "-" * N)[i] for i in ci); tr = tr["gap"]
        for a, b in runs_of([v == 1 for v in tr]):
            if b - a < 3: continue
            eps += 1; seg = code[a:b]
            d = next((k for k, c in enumerate(seg) if c in "234"), None); f = next((k for k, c in enumerate(seg) if c in "1234"), None)
            if d is not None: reached += 1; lead_dec.append(d)
            if f is not None: lead_any.append(f)
        for k in range(len(cm)):
            if tr[k] == 1:
                gm += 1; gm_none += code[k] not in "1234H"
            if code[k] in "DS": dmon += 1; dmon_true += tr[k] == 1
            if code[k] == "3" and (k == 0 or code[k - 1] not in "34"):
                esc3 += 1; esc3_false += tr[k] == 0; per_yta[YTA.get(u, "?")] = per_yta.get(YTA.get(u, "?"), 0) + 1
    nat = [national[s][i] for i in ci]; tru_n = [sum(cs["truth"][u]["gap"][k] for u in cs["truth"]) for k in range(len(cm))]
    nat_eps = runs_of(nat)
    M[s] = dict(episodes=eps, episodes_decided=reached, median_months_to_decision=float(np.median(lead_dec)) if lead_dec else None,
                median_months_to_first_suggestion=float(np.median(lead_any)) if lead_any else None,
                true_gap_months=gm, true_gap_months_no_suggestion=gm_none, data_track_months=dmon, data_track_months_true_gap=dmon_true,
                yta_escalations=esc3, yta_escalations_not_confirmed=esc3_false, yta_escalations_by_area=per_yta,
                national_episodes=len(nat_eps), national_episodes_not_confirmed=sum(tru_n[a] < NAT_N for a, b in nat_eps), national_months=int(sum(nat)))
# ---- load on the collaborative areas, every judged signal, 2021-01 .. 2026-10
load = {k: 0 for k in G["yta"]}; load_sig = {}
for (s, u), code in CODES.items():
    c = "".join(code[i] for i in ci)
    n = sum(1 for k in range(len(c)) if c[k] == "3" and (k == 0 or c[k - 1] not in "34"))
    if n: load[YTA.get(u, "?")] = load.get(YTA.get(u, "?"), 0) + n; load_sig[s] = load_sig.get(s, 0) + n
M["_load"] = dict(years=round(years, 2), yta_escalations_by_area=load, yta_escalations_by_signal=load_sig,
                  national_months_by_signal={s: int(sum(national[s][i] for i in ci)) for s in STEP})

ts = dt.datetime.now().strftime("%Y%m%dT%H%M%S"); out = ROOT / "runs/governance/replay" / ts; out.mkdir(parents=True)
pd.DataFrame(rows).to_csv(out / "records.csv", index=False)
json.dump(M, open(out / "metrics.json", "w"), indent=1)
git = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip()
json.dump(dict(produced_by="scripts/run_governance.py", timestamp=ts, git=git, rules="GOVERNANCE.md", thresholds=R,
               inputs=dict(model1=str(r1.relative_to(ROOT)), model2=str(r2.relative_to(ROOT)), truth=str(pc.relative_to(ROOT)))), open(out / "meta.json", "w"), indent=1)
(ROOT / "runs/governance/replay/LATEST").write_text(ts)
print("runs/governance/replay/" + ts)
for s, m in M.items(): print(s, json.dumps(m))
