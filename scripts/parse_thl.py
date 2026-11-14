"""Parse raw THL JSON-stat into one tidy parquet/csv: producer, date, specialty, measure, value."""
import json, pathlib, pandas as pd, numpy as np, itertools
ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/thl"; OUT = ROOT / "data/tidy"; OUT.mkdir(parents=True, exist_ok=True)
def parse(f):
    ds = json.load(open(f))["dataset"]
    ids, size = ds["dimension"]["id"], ds["dimension"]["size"]
    cats = []
    for i in ids:
        c = ds["dimension"][i]["category"]
        inv = sorted(c["index"], key=lambda k: c["index"][k])
        cats.append([(k, c["label"][k]) for k in inv])
    vals = ds["value"]
    rows = []
    for n, combo in enumerate(itertools.product(*cats)):
        v = vals.get(str(n)) if isinstance(vals, dict) else vals[n]
        if v is None: continue
        rows.append([c[1] for c in combo] + [v])
    return pd.DataFrame(rows, columns=ids + ["value"])
frames = []
for f in sorted(RAW.glob("jonotilanne_*.json")):
    if "dims" in f.name: continue
    df = parse(f); df["specialty"] = f.stem.split("_")[1]; df["cube"] = "jonotilanne"; frames.append(df)
for f in sorted(RAW.glob("jonoryhma_*.json")):
    if "dims" in f.name: continue
    df = parse(f); df["specialty"] = "proc" + f.stem.split("_")[1]; df["cube"] = "jonoryhma"; frames.append(df)
df = pd.concat(frames, ignore_index=True)
df["value"] = pd.to_numeric(df["value"], errors="coerce")
df = df[df.ajankohta.str.match(r"\d\d\.\d\d\.\d{4}")].copy()
df["date"] = pd.to_datetime(df.ajankohta, format="%d.%m.%Y")
df = df.rename(columns={"tuottaja": "producer"}).drop(columns="ajankohta")
df.to_csv(OUT / "thl_queue.csv", index=False)
print(df.shape, df.specialty.unique())
