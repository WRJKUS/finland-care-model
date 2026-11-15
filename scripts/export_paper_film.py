"""Data for the paper film (county twin scene: COUNTY below, picked at random on 2026-11-15) (film/paper/): reads visuals/circuit/data.json and the stored scorecards, writes film/paper/data.js.
Never recomputes a result. Usage: python scripts/export_paper_film.py"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
C = json.load(open(ROOT / "visuals/circuit/data.json"))
SJ = json.load(open(ROOT / "twin/signals.json"))  # full signal definitions (direction, target, definition text)
pol = C["policy_run"]
sc = json.load(open(ROOT / f"runs/compare/policy/{pol}/scorecard.json"))
SIG = ["ref_assess_over90", "dx_endo_over90", "treat_onc_wait"]
COUNTY, COUNTY_NAME = "21", "Lapland"  # chosen with random.SystemRandom().choice over the 24 county codes
LIVE = list(C["signals"])  # all 11 signals (film/paper/county_twin.html uses every one)
import csv
_rec = [r for r in csv.DictReader(open(ROOT / C["model1_run"] / "records.csv")) if r["county"] == COUNTY and r["signal"] in LIVE]
_f = lambda v: None if v in ("", "nan") else round(float(v), 4)
live = {}
for sg in LIVE:
    rows = {r["t"]: r for r in _rec if r["signal"] == sg}
    live[sg] = {k: [(_f(rows[t][k]) if k not in ("status", "data_through") else rows[t][k]) if t in rows else None for t in C["replay_months"]]
                for k in ("level", "lo", "hi", "thr", "ref", "num", "den", "p_gap", "status", "data_through")}

summary = {}
for s in SIG:
    t = C["timing"][s]
    summary[s] = dict(label=C["signals"][s]["label"], step=C["signals"][s]["step"],
                      m3=t["summary"]["model3"], m3f=t["summary"]["model3fast"], m4=t["summary"]["model4"],
                      diff=t["diff"]["model4_minus_model3_coverage"], diff_fast=t["diff"]["model4_minus_model3fast_coverage"],
                      rows=[dict(county=r["county"], name=r["name"], truth=r["truth"], m3=r["m3"], m4=r["m4"],
                                 gap_months=r["gap_months"], m3_hit=r["m3_hit"], m4_hit=r["m4_hit"]) for r in t["rows"]])

sens = {}
for d in sorted((ROOT / "runs/compare").glob("sensitivity_*")):
    run = sorted(d.iterdir())[-1]
    s = json.load(open(run / "scorecard.json"))["signals"]
    sens[d.name.replace("sensitivity_", "")] = {k: {m: s[k][m]["coverage"] for m in ("model3", "model4")} for k in SIG}

out = dict(
    source=dict(circuit="visuals/circuit/data.json", policy_run=pol, model1_run=C["model1_run"]),
    county=dict(code=COUNTY, name=COUNTY_NAME, live=live),
    budget=sc["budget"], policy_months=C["policy_months"], replay_months=C["replay_months"],
    summary=summary, sensitivity=sens,
    steps=C["steps"], example=C["example"], example_series=C["example_series"],
    channel={k: C["channel"][k] for k in ("signal", "county", "name", "k_policy0", "m3view", "slots3", "slots4",
                                          "truth", "m3", "m4", "need_months", "m3_hit", "m4_hit")},
    signals={k: dict(step=v["step"], label=v["label"], cs=v["cancer_specific"], src=v["source"], star=k in SIG,
                     delta=v["delta"], dtype=v["delta_type"], kind=v["kind"],
                     bad=SJ[k]["bad_direction"], target=SJ[k].get("target"), definition=SJ[k]["definition"]) for k, v in C["signals"].items()},
)
# county outlines for the "what a county twin is" scene: outer rings only, normalised by height, north up
_g = json.load(open(ROOT / "data/raw/geo/hva.geojson"))
_outer = lambda g: [poly[0] for poly in (g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]])]
_pts = [pt for f in _g["features"] for r in _outer(f["geometry"]) for pt in r]
_x0, _y1 = min(q[0] for q in _pts), max(q[1] for q in _pts); _h = _y1 - min(q[1] for q in _pts)
out["geo"] = [dict(code=f["properties"]["hyvinvointialue"],
                   name=f["properties"]["name"].replace(" wellbeing services county", "").replace("City of ", ""),
                   rings=[[[round((x - _x0) / _h, 4), round((_y1 - y) / _h, 4)] for x, y in r] for r in _outer(f["geometry"])])
              for f in _g["features"]]
p = ROOT / "film/paper"; p.mkdir(parents=True, exist_ok=True)
(p / "data.js").write_text("window.D = " + json.dumps(out) + ";\n")
print("wrote", p / "data.js")
