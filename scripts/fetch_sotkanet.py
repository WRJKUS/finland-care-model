"""Fetch Sotkanet indicators (THL/Cancer Registry/Kela), wellbeing services county level + whole country."""
import json, urllib.request, pathlib, time, sys, pandas as pd
ROOT = pathlib.Path(__file__).resolve().parents[1]; RAW = ROOT / "data/raw/sotkanet"; OUT = ROOT / "data/tidy"; OUT.mkdir(exist_ok=True, parents=True)
IDS = [3620, 3621, 6103, 3625, 3626, 3627, 5083, 3336, 13, 5033, 5073, 6411, 5502, 4404, 4408, 4410, 4459, 3869, 3297, 5093, 5643, 3629, 2475]
regions = {r["id"]: r for r in json.load(open(RAW / "regions.json"))}
meta = {i["id"]: i for i in json.load(open(RAW / "indicators.json"))}
rows = []
for i in IDS:
    f = RAW / f"ind_{i}.json"
    if not f.exists():
        ys = "&".join(f"years={y}" for y in range(2005, 2027))
        url = f"https://sotkanet.fi/rest/1.1/json?indicator={i}&{ys}&genders=total&genders=male&genders=female"
        f.write_bytes(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "research-client"}), timeout=120).read()); time.sleep(0.5)
    for r in json.load(open(f)):
        reg = regions.get(r["region"])
        if reg and reg["category"] in ("HYVINVOINTIALUE", "MAA"):
            rows.append(dict(indicator=i, title=meta[i]["title"]["fi"], region=reg["title"]["fi"], region_code=reg["code"], cat=reg["category"],
                             year=r["year"], gender=r["gender"], value=r["value"], absvalue=r.get("absValue")))
df = pd.DataFrame(rows); df.to_csv(OUT / "sotkanet.csv", index=False)
s = df[df.gender == "total"].groupby(["indicator", "title"]).agg(y0=("year", "min"), y1=("year", "max"), regions=("region", "nunique"), n=("value", "count"))
print(s.to_string())
