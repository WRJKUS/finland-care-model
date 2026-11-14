"""AI layer: for each replay checkpoint, an LLM reads the twin's records and writes a short county briefing (FI + EN).
It may cite only records, actions and sources that exist; a validator rejects sentences without a valid citation
or with numbers that are not in the cited facts. Runs offline-ahead: the demo reads the stored result."""
import pandas as pd, numpy as np, json, pathlib, subprocess, re, sys, datetime, concurrent.futures as cf
ROOT = pathlib.Path(__file__).resolve().parents[1]
SIG = json.load(open(ROOT / "twin/signals.json")); ACT = json.load(open(ROOT / "twin/actions.json")); SRC = json.load(open(ROOT / "twin/sources.json"))
ts1 = (ROOT / "runs/model1/replay/LATEST").read_text()
rec = pd.read_csv(ROOT / f"runs/model1/replay/{ts1}/records.csv", dtype={"county": str})
names = json.load(open(ROOT / "twin/counties.json"))
MODEL = "sonnet"
CHECK = [str(d.date()) for d in pd.date_range("2021-03-31", "2026-09-30", freq="QE")] + ["2026-10-31"]
if len(sys.argv) > 1: CHECK = sys.argv[1:]
def fmt(cfg, v):
    if v is None or (isinstance(v, float) and np.isnan(v)): return None
    return f"{v:.0f} days" if cfg["unit"] == "days" else f"{100 * v:.0f}%"
def act_for(sig): return "det_screen" if sig.startswith("det_screen") else sig if sig in ACT else None
def facts(T):
    out = {}
    r = rec[(rec.t == T)]
    for c, g in r.groupby("county"):
        rows = []
        for _, x in g.iterrows():
            cfg = SIG[x.signal]
            if cfg["bad_direction"] == 0: continue
            a = act_for(x.signal)
            rows.append(dict(record=x.signal, step=cfg["step"], what=cfg["label_en"], mita=cfg["label_fi"], status=x.status, level=fmt(cfg, x.level),
                             interval80=f"{fmt(cfg, x.lo)} to {fmt(cfg, x.hi)}", national=fmt(cfg, x.get("ref")), data_through=x.data_through,
                             cancer_specific=cfg["cancer_specific"], action=ACT[a]["id"] if a and x.status in ("gap", "watch") else None))
        out[c] = dict(name_fi=names[c]["fi"], name_en=names[c]["en"], records=rows)
    return out
RULES = """You write decision-maker briefings for Finnish wellbeing services counties from the records of an aggregate "county twin" of the cancer pathway (detection -> referral -> diagnosis -> treatment). A twin is one county, never a patient.

Rules, all mandatory:
- For EACH county write 3 to 5 short sentences in English and the same content in Finnish. Plain language for a non-technical county director. No headings, no bullet marks.
- Sentence 1: where the most important gap is (pathway step) or that no identifiable gap is seen. Then: how sure we are (interval, national comparison, or 'unidentifiable'/'stale' = cannot be judged from public data). Then: the recommended action for each gap, using the ACTIONS text. Last: one limitation where relevant (e.g. the signal is not cancer-specific).
- status meanings: gap = at least 90% probability the county is beyond the model threshold versus the national level; watch = 70-90%; ok = no gap seen; unidentifiable = too few patients or interval too wide to judge; stale = no recent data.
- Never call 'unidentifiable' or 'stale' good or on target. Never invent numbers: use only numbers that appear in that county's records or in the cited action. Never predict lives saved or survival.
- Every sentence carries "cites": a list of ids it rests on: record ids (the 'record' field of that county), action ids (e.g. A-T1) and source ids (E01.., S01..). At least one id per sentence. Cite only ids given below.
- Output ONLY a JSON object: {"<county code>": {"en": [{"text": "...", "cites": ["..."]}], "fi": [{"text": "...", "cites": ["..."]}]}, ...} for every county code given. No markdown fence."""
def prompt(T, F):
    acts = {a["id"]: dict(step=a["step"], action_en=a["action_en"], action_fi=a["action_fi"], roadmap=a["roadmap_en"], evidence=a["evidence"], expected_en=a["expected_en"]) for a in ACT.values()}
    return f"{RULES}\n\nReplay date: {T}. Use only what is below; it is what had been published by this date.\n\nACTIONS:\n{json.dumps(acts, ensure_ascii=False)}\n\nSOURCE IDS: {', '.join(SRC)}\n\nCOUNTIES:\n{json.dumps(F, ensure_ascii=False)}"
def validate(T, F, out):
    ok, problems = {}, []
    valid_global = set(SRC) | {a["id"] for a in ACT.values()}
    acttext = " ".join(json.dumps(a, ensure_ascii=False) for a in ACT.values())
    for c, f in F.items():
        b = out.get(c)
        if not b or not b.get("en") or not b.get("fi"): problems.append(f"{c}: missing"); continue
        valid = valid_global | {r["record"] for r in f["records"]}
        nums_ok = set(re.findall(r"\d+(?:[.,]\d+)?", json.dumps(f) + acttext + T)) | {"90", "80", "70"}
        for y, mth, dd in re.findall(r"(\d{4})-(\d\d)-(\d\d)", json.dumps(f) + T):   # Finnish/English date spellings of dates in the facts
            nums_ok |= {f"{int(dd)}.{int(mth)}", f"{dd}.{mth}", f"{int(dd)}.{int(mth)}.{y}", y, str(int(dd)), str(int(mth)), dd, mth}
        good = True
        for lang in ("en", "fi"):
            for s in b[lang]:
                if not s.get("cites") or any(x not in valid for x in s["cites"]): problems.append(f"{c}/{lang}: bad cite {s.get('cites')}"); good = False
                for n in re.findall(r"\d+(?:[.,]\d+)?", s.get("text", "")):
                    if n not in nums_ok and n.replace(",", ".") not in nums_ok: problems.append(f"{c}/{lang}: number {n} not in facts"); good = False
        if good: ok[c] = b
    return ok, problems
def run(T):
    F = facts(T); res, probs = {}, []
    for attempt in range(2):
        todo = {c: f for c, f in F.items() if c not in res}
        if not todo: break
        p = subprocess.run(["claude", "-p", "--model", MODEL], input=prompt(T, todo), capture_output=True, text=True, timeout=900, cwd="/tmp")
        txt = p.stdout.strip(); m = re.search(r"\{.*\}", txt, re.S)
        try: out = json.loads(m.group(0))
        except Exception as e: probs.append(f"attempt {attempt}: unparsable ({e})"); continue
        ok, pr = validate(T, todo, out); res.update(ok); probs += [f"attempt {attempt}: {x}" for x in pr]
    return T, res, probs, sorted(set(F) - set(res))
ts = datetime.datetime.now().strftime("%Y%m%dT%H%M%S"); outdir = ROOT / f"runs/briefings/llm/{ts}"; outdir.mkdir(parents=True)
allb, log = {}, {}
with cf.ThreadPoolExecutor(4) as ex:
    for T, res, probs, missing in ex.map(run, CHECK):
        allb[T] = res; log[T] = dict(problems=probs, rejected_counties=missing); print(T, len(res), "ok;", len(missing), "rejected;", len(probs), "problems", flush=True)
        json.dump(allb, open(outdir / "briefings.json", "w"), ensure_ascii=False, indent=1)
json.dump(dict(produced_by="scripts/gen_briefings.py", timestamp=ts, llm="Claude via `claude -p --model " + MODEL + "`", inputs=f"runs/model1/replay/{ts1}", checkpoints=CHECK, rules=RULES, validation_log=log), open(outdir / "meta.json", "w"), ensure_ascii=False, indent=1)
(ROOT / "runs/briefings/llm/LATEST").write_text(ts); (outdir / "DONE").write_text("done")
