# Equal Care Across Finland — county pathway twin

Junction 2026, AstraZeneca challenge. A streaming, aggregate "twin" of the cancer pathway for each Finnish wellbeing services county, replayed through history in order, with a like-for-like comparison of the strategy's annual monitoring (Model 3) against twin-targeted monitoring (Model 4).

**A twin here is one county, never a patient.** Public aggregate data only.

## Open the demo

**Live site: https://equal-care-across-finland.vercel.app/** The explanation is on the site: the opening popup starts a guided showcase of what the twin shows and why it matters, and **About** shows how the twin works on one page.

Offline: open `demo/index.html` in a browser. It is one self-contained file: no server, no network, no API call. Press **Play**, click a county, switch pathway step, switch EN/FI. Click any source chip to see the source.

## Where things are

| What | Where |
|---|---|
| Live demo | `demo/index.html` (built from `demo/template.html`) |
| Film (1080p, captions burned in) | `film/film.mp4`; scene list `film/scenes.json` |
| One visual per model | `visuals/model1.png` … `model4.png` |
| The system drawn as a circuit (Typst, 8 pages) | `visuals/circuit/circuit.pdf`; source `visuals/circuit/circuit.typ`, data from `scripts/export_circuit.py` |
| Pitch script | `PITCH.md` |
| Scorecard definition (committed before the first Model 3/4 run) | `SCORECARD.md` |
| Sources, data manifest, effect registry | `SOURCES.md`, `DATA_MANIFEST.md`, `EFFECTS.md` |
| Unexamined modelling decisions | `DECISIONS.md` |
| Mentor questions | `MENTOR_QUESTIONS.md` |
| Runs (records, forecasts, policy slots, scorecard, AI briefings) | `runs/<model>/<experiment>/<timestamp>/` with `meta.json` |

## Reproduce

Python 3 with numpy, pandas, scipy; Google Chrome and ffmpeg for the film; the `claude` CLI for the AI briefings.

```
python scripts/fetch_thl.py          # THL queue cubes -> data/raw/thl
python scripts/fetch_sotkanet.py     # Sotkanet indicators -> data/raw/sotkanet
python scripts/parse_thl.py
python scripts/build_signals.py      # data/tidy/signals.csv
python scripts/run_replay.py         # Models 1 and 2, baselines, controls
python scripts/run_policy.py         # Models 3, 3-fast and 4, scorecard
python scripts/gen_briefings.py      # AI briefings on the replay (LLM calls; optional, stored result is used)
python scripts/export_circuit.py     # visuals/circuit/data.json
typst compile visuals/circuit/circuit.typ   # visuals/circuit/circuit.pdf
typst compile --format svg --pages 1 visuals/circuit/circuit.typ visuals/circuit/circuit-p1.svg   # page 1, shown in the demo's About panel
python scripts/build_demo.py         # demo/index.html
python scripts/render_film.py        # film/film.mp4
python scripts/export_visuals.py     # visuals/*.png
```

Figures, demo and film read from `runs/`; they never recompute.

## The four models

1. **Equality twin**: county against national level per pathway step, with interval, identifiability flag and gap probability.
2. **Pathway twin**: national levels and flows, with surprise alarms.
3. **Strategy to 2028**: the roadmap's pathway lever (2.5.2 / 3.1.2) as three county pilot slots, re-decided once a year from annual figures two years old.
4. **Challenger**: the same slots, re-decided monthly from Model 1's records.

Models 3 and 4 on history are counterfactuals ("had this been in place over these years"), not forecasts.

## Honest summary of results

- Model 4 beats Model 3 on the referral handover (51% vs 20% of gap-months reached); ties on the oncology queue (60% vs 56%) and endoscopy (38% vs 34%).
- The twin beats a linear trend on all scored signals but persistence on only half.
- Positive control failed: the 2020 pandemic dip was not flagged.
- The Goal 3 indicator proper (days to treatment) cannot be estimated from public data; we use a labelled proxy.

## What was built before the event

Nothing. The brief (`MASTER_PROMPT.md`), including the literature table, was prepared by the team before the build; all code, runs and outputs were made during the event.

## Where AI wrote the code

All code, documentation, the film and this README were written by an AI coding agent (Claude Code) from the team's brief, on 14 November 2026. A sub-agent extracted the roadmap budgets from the PDFs (`data/raw/docs/ROADMAP_EXTRACT.md`). The county briefings in the demo are written by Claude from the twin's records and pass a citation validator (`scripts/gen_briefings.py`). The modelling decisions the AI made are listed in `DECISIONS.md` as unexamined until a team member checks them.
