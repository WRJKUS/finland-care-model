"""Fetch THL specialist-care queue cubes (eshjono) as raw JSON-stat. Public aggregate data.
Source: https://sampo.thl.fi/pivot/prod/fi/eshjono/  (THL, Hoitoonpääsy erikoissairaanhoidossa)
"""
import json, time, urllib.request, pathlib, sys, datetime
OUT = pathlib.Path(__file__).resolve().parents[1] / "data/raw/thl"
BASE = "https://sampo.thl.fi/pivot/prod/fi/eshjono/"
def get(url):
    for k in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "research-client"})
            return urllib.request.urlopen(req, timeout=180).read().decode("utf-8")
        except Exception as e:
            print("retry", k, e, file=sys.stderr); time.sleep(3 + 3 * k)
    raise SystemExit("failed " + url)
def dims(cube):
    t = get(BASE + cube + ".dimensions.json")
    return json.loads(t[t.index("(") + 1:t.rindex(")")])
def leaves(n, out):
    ch = n.get("children", [])
    if not ch: out.append(n)
    for c in ch: leaves(c, out)
    return out
manifest = {"fetched_utc": datetime.datetime.utcnow().isoformat(), "files": []}
# 1) queue status by specialty
cube = "jonotilanne/fact_eshjono_jonotilanne"
d = {x["id"]: x for x in dims(cube)}
json.dump(list(d.values()), open(OUT / "jonotilanne_dims.json", "w"), ensure_ascii=False)
meas = [m["sid"] for m in leaves(d["measure"]["children"][0], [])]
spec = {s["label"].split(" ")[0]: s["sid"] for s in leaves(d["erikoisala"]["children"][0], [])}
spec["ALL"] = d["erikoisala"]["children"][0]["sid"]
want = sys.argv[1:] or ["65", "30S", "10H", "20U", "20G", "10G", "80", "20", "10", "50", "20O", "55", "30", "ALL"]
mstr = ".".join(str(m) for m in meas) + "."
for code in want:
    f = OUT / f"jonotilanne_{code}.json"
    if not f.exists():
        url = (f"{BASE}{cube}.json?row=tuottaja-976329&row=ajankohta-976319&column=measure-{mstr}"
               f"&filter=erikoisala-{spec[code]}")
        f.write_text(get(url)); time.sleep(1)
    manifest["files"].append({"file": f.name, "specialty": code, "sid": spec[code]})
    print(code, f.stat().st_size)
# 2) procedure queue groups (endoscopy = diagnostic step proxy)
cube = "jonoryhma/fact_eshjono_jonoryhma"
d = {x["id"]: x for x in dims(cube)}
json.dump(list(d.values()), open(OUT / "jonoryhma_dims.json", "w"), ensure_ascii=False)
meas = [m["sid"] for m in leaves(d["measure"]["children"][0], [])]
mstr = ".".join(str(m) for m in meas) + "."
for g in leaves(d["jonoryhma"]["children"][0], []):
    if g["code"] in ("27", "1", "6", "12"):
        f = OUT / f"jonoryhma_{g['code']}.json"
        if not f.exists():
            url = (f"{BASE}{cube}.json?row=tuottaja-976329&row=ajankohta-976319&column=measure-{mstr}"
                   f"&filter=jonoryhma-{g['sid']}")
            f.write_text(get(url)); time.sleep(1)
        manifest["files"].append({"file": f.name, "queue_group": g["label"], "sid": g["sid"]})
        print(g["label"], f.stat().st_size)
json.dump(manifest, open(OUT / "fetch_manifest.json", "w"), ensure_ascii=False, indent=1)
