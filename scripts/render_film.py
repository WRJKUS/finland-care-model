"""Render the film from code: headless-Chrome screenshots of the demo page in film mode (captions burned in by the page), then ffmpeg.
Scene list: film/scenes.json. Usage: python scripts/render_film.py [scene_id ...]  (no args = all). Writes film/DONE when finished."""
import json, pathlib, subprocess, sys, urllib.parse, concurrent.futures as cf, re
ROOT = pathlib.Path(__file__).resolve().parents[1]; F = ROOT / "film"; FR = F / "frames"; FR.mkdir(parents=True, exist_ok=True)
sc = json.load(open(F / "scenes.json")); fps = sc["fps"]; W, H = sc["size"]
html = (ROOT / "demo/index.html").read_text()
months = json.loads(re.search(r'"months":(\[[^\]]*\])', html).group(1)); PM0 = months.index("2021-01-31"); TL = len(months) - 1
jobs, concat = [], []
for s in sc["scenes"]:
    if len(sys.argv) > 1 and s["id"] not in sys.argv[1:]: continue
    if s.get("replay"):
        ts = list(range(PM0 - 1, TL + 1)); n = len(ts); hold = 2.5; per = (s["seconds"] - hold) / n
        for i, t in enumerate(ts):
            cap = s["caps"][min(len(s["caps"]) - 1, i * len(s["caps"]) // n)]
            jobs.append((f'{s["id"]}_{i:03d}', dict(s["params"], t=t, cap=cap))); concat.append((f'{s["id"]}_{i:03d}', per + (hold if i == n - 1 else 0)))
    else:
        jobs.append((s["id"], dict(s["params"], cap=s["cap"]))); concat.append((s["id"], s["seconds"]))
def shot(j):
    name, p = j; url = "file://" + str(ROOT / "demo/index.html") + "?" + urllib.parse.urlencode(p)
    subprocess.run(["google-chrome", "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars", f"--window-size={W},{H}", "--virtual-time-budget=3000",
                    f"--user-data-dir=/tmp/chrome-film-{name}", f"--screenshot={FR / (name + '.png')}", url], capture_output=True, timeout=120)
    return name
with cf.ThreadPoolExecutor(6) as ex:
    for k, n in enumerate(ex.map(shot, jobs)):
        if k % 25 == 0: print("frame", k, "/", len(jobs), flush=True)
missing = [n for n, _ in concat if not (FR / (n + ".png")).exists()]
print("missing frames:", missing)
with open(F / "concat.txt", "w") as f:
    for n, d in concat: f.write(f"file 'frames/{n}.png'\nduration {d:.3f}\n")
    f.write(f"file 'frames/{concat[-1][0]}.png'\n")
out = F / ("film.mp4" if len(sys.argv) == 1 else "film_partial.mp4")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(F / "concat.txt"), "-vf", f"fps={fps},scale={W}:{H},format=yuv420p", "-t", f"{sum(d for _, d in concat):.2f}", "-c:v", "libx264", "-crf", "20", str(out)], check=True)
print("wrote", out, sum(d for _, d in concat), "s"); (F / "DONE").write_text("done")
