"""Assemble the offline demo: reads only from runs/ and registries, inlines everything into demo/index.html. Never recomputes models."""
import pandas as pd, numpy as np, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
L = lambda p: (ROOT / p / "LATEST").read_text().strip()
SIG = json.load(open(ROOT / "twin/signals.json")); ACT = json.load(open(ROOT / "twin/actions.json")); SRC = json.load(open(ROOT / "twin/sources.json")); CT = json.load(open(ROOT / "twin/counties.json"))
r1 = ROOT / "runs/model1/replay" / L("runs/model1/replay"); r2 = ROOT / "runs/model2/replay" / L("runs/model2/replay")
rec = pd.concat([pd.read_csv(r1 / "records.csv", dtype={"county": str}), pd.read_csv(r2 / "records.csv", dtype={"county": str})])
rec["status"] = rec.status.fillna("n/a"); months = sorted(rec.t.unique()); mi = {m: i for i, m in enumerate(months)}
ST = {"gap": "g", "watch": "w", "ok": "o", "unidentifiable": "u", "stale": "s", "n/a": "n"}
R = {}
def rnd(v, k=4): return None if v is None or (isinstance(v, float) and np.isnan(v)) else round(float(v), k)
for (sig, c), g in rec.groupby(["signal", "county"]):
    n = len(months); d = {k: [None] * n for k in ("lv", "lo", "hi", "rf", "th", "p", "num", "den", "dt")}; st = ["-"] * n
    for x in g.itertuples():
        i = mi[x.t]; d["lv"][i] = rnd(x.level); d["lo"][i] = rnd(x.lo); d["hi"][i] = rnd(x.hi); d["rf"][i] = rnd(getattr(x, "ref", None)); d["th"][i] = rnd(getattr(x, "thr", None))
        d["p"][i] = rnd(getattr(x, "p_gap", None), 3); d["num"][i] = rnd(x.num, 1); d["den"][i] = rnd(x.den, 2); d["dt"][i] = x.data_through; st[i] = ST[x.status]
    d["st"] = "".join(st); R.setdefault(sig, {})[c] = d
fc = pd.read_csv(r1 / "forecasts.csv", dtype={"county": str}); F = {}
for (sig, c), g in fc.groupby(["signal", "county"]):
    F.setdefault(sig, {})[c] = dict(period=list(g.period), pred=[rnd(v) for v in g.twin], actual=[rnd(v) for v in g.actual], hit=[int(abs(z) <= 1.2816) for z in g.z])
ser = json.load(open(r1 / "series.json")); S = {}
for k, v in ser.items():
    sig, c = k.split("|"); S.setdefault(sig, {})[c] = dict(period=v["period"], obs=v["obs"])
base = pd.read_csv(r1 / "baselines.csv").to_dict("records")
alarms = json.load(open(r2 / "alarms.json")); meta1 = json.load(open(r1 / "meta.json"))
card = json.load(open(ROOT / "runs/compare/policy" / L("runs/compare/policy") / "scorecard.json"))
slots = {m: pd.read_csv(ROOT / f"runs/{m}/policy" / L(f"runs/{m}/policy") / "slots.csv", dtype={"county": str}).to_dict("records") for m in ("model3", "model3fast", "model4")}
for s in card["signals"].values():
    for m in ("model3", "model3fast", "model4"): s[m].pop("episode_list", None)
bp = ROOT / "runs/briefings/llm"; B = {}; bmeta = {}
if (bp / "LATEST").exists():
    B = json.load(open(bp / L("runs/briefings/llm") / "briefings.json")); bmeta = json.load(open(bp / L("runs/briefings/llm") / "meta.json")); bmeta = dict(llm=bmeta["llm"], timestamp=bmeta["timestamp"])
# map
geo = json.load(open(ROOT / "data/raw/geo/hva.geojson")); X0, Y1, sc = 60000, 7780000, 600 / 1180000; paths = {}
def ring_area(r): return abs(sum(r[i][0] * r[i + 1][1] - r[i + 1][0] * r[i][1] for i in range(len(r) - 1))) / 2
for f in geo["features"]:
    polys = f["geometry"]["coordinates"] if f["geometry"]["type"] == "MultiPolygon" else [f["geometry"]["coordinates"]]
    d = ""; cx = cy = aa = 0
    for poly in polys:
        ring = poly[0]; a = ring_area(ring)
        if a < 3e7: continue
        pts = [((x - X0) * sc, (Y1 - y) * sc) for x, y in ring]
        d += "M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + "Z"
        cx += a * np.mean([p[0] for p in pts]); cy += a * np.mean([p[1] for p in pts]); aa += a
    paths[f["properties"]["hyvinvointialue"]] = dict(d=d, cx=round(cx / aa, 1), cy=round(cy / aa, 1))
# context: latest annual figures per county
sk = pd.read_csv(ROOT / "data/tidy/signals.csv", dtype={"county": str}); ctx = {}
for sig in ["risk_smoking_lowedu", "risk_smoking_highedu", "risk_smoking", "pc_continuity_coci", "out_surv_breast", "out_surv_colon"]:
    g = sk[sk.signal == sig]; y = g.period.max(); ctx[sig] = dict(period=y, v={x.county: rnd(x.num, 2) for x in g[g.period == y].itertuples()})
last = months[-1]; scr = {}
for sig in ["det_screen_breast", "det_screen_cervix", "det_screen_colorectal"]:
    x = rec[(rec.signal == sig) & (rec.t == last) & (rec.county != "FI")]
    scr[sig] = dict(n=int(len(x)), at_target=int((x.obs >= 0.8).sum()), min=rnd(x.obs.min()), max=rnd(x.obs.max()), min_county=x.loc[x.obs.idxmin(), "county"], data_through=x.data_through.max())
# governance suggestions on the replay (scripts/run_governance.py; rules GOVERNANCE.md, texts twin/governance.json)
gp = ROOT / "runs/governance/replay"; GV = None
if (gp / "LATEST").exists():
    gr = gp / L("runs/governance/replay"); gv = pd.read_csv(gr / "records.csv", dtype={"unit": str}).fillna(""); codes, eps = {}, {}
    for (sig, u), g in gv.groupby(["signal", "unit"]):
        g = g.sort_values("t"); c = ["-"] * len(months); e = []
        for x in g.itertuples():
            i = mi[x.t]; c[i] = x.code
            if x.episode_start:
                a, d = mi[x.episode_start], (mi[x.decision] if x.decision else -1)
                if e and e[-1][0] == a: e[-1][1], e[-1][2] = d, i
                else: e.append([a, d, i])
        codes.setdefault(sig, {})[u] = "".join(c); eps.setdefault(sig, {})[u] = e
    GV = dict(codes=codes, episodes=eps, metrics=json.load(open(gr / "metrics.json")), map=json.load(open(ROOT / "twin/governance.json")), run=str(gr.relative_to(ROOT)))
else: print("warning: no governance run; the demo will have no governance layer (python scripts/run_governance.py)")
# page 1 of the circuit document, shown in the About panel (typst compile --format svg --pages 1 ... circuit-p1.svg)
cp = ROOT / "visuals/circuit/circuit-p1.svg"; circuit = cp.read_text() if cp.exists() else None
if circuit is None: print("warning: visuals/circuit/circuit-p1.svg missing; About panel will have no circuit")
D = dict(months=months, signals=SIG, actions=ACT, sources=SRC, counties=CT, R=R, F=F, S=S, baselines=base, alarms=alarms, q_selected=meta1["q_selected"],
         card=card, slots=slots, briefings=B, briefing_meta=bmeta, paths=paths, ctx=ctx, screening=scr, circuit=circuit, gov=GV,
         runs=dict(model1=str(r1.relative_to(ROOT)), model2=str(r2.relative_to(ROOT)), compare="runs/compare/policy/" + L("runs/compare/policy"), **({"governance": GV["run"]} if GV else {})))
js = json.dumps(D, ensure_ascii=False, separators=(",", ":"))
tpl = (ROOT / "demo/template.html").read_text()
(ROOT / "demo/index.html").write_text(tpl.replace("/*__DATA__*/null", js))
print("demo/index.html", round(len(js) / 1e6, 2), "MB data;", len(B), "briefing checkpoints")
print(json.dumps(scr, indent=0)[:600]); print({k: v["period"] for k, v in ctx.items()})
