"""One visual per model, all exports of the demo's views (same template, film mode without caption)."""
import subprocess, pathlib, urllib.parse
ROOT = pathlib.Path(__file__).resolve().parents[1]; V = ROOT / "visuals"; V.mkdir(exist_ok=True)
VIEWS = {"model1": dict(film="p-map,p-lens", cols="0.7fr 1.5fr", step="all", county="09", zoom="1.18", head="Model 1 · Equality twin: where each county stands against the national level"),
         "model2": dict(film="p-m2", zoom="1.12", head="Model 2 · Pathway twin: national levels and flows as the replay knew them"),
         "model3": dict(film="p-pol", lane="model3", sig="ref_assess_over90", county="09", zoom="1.0", head="Model 3 · Strategy monitoring: annual review, figures two years old"),
         "model4": dict(film="p-pol", lane="model4", sig="ref_assess_over90", county="09", zoom="1.0", head="Model 4 · Challenger: same slots, re-targeted monthly by the twin")}
for name, p in VIEWS.items():
    url = "file://" + str(ROOT / "demo/index.html") + "?" + urllib.parse.urlencode(p)
    subprocess.run(["google-chrome", "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars", "--window-size=1920,1080", "--virtual-time-budget=3000",
                    f"--user-data-dir=/tmp/chrome-vis-{name}", f"--screenshot={V / (name + '.png')}", url], capture_output=True, timeout=120)
    print(name, (V / (name + ".png")).exists())
