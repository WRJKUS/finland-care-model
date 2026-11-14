# Data manifest

Every Finnish public aggregate input actually used. No patient-level data anywhere. Raw downloads are in `data/raw/`, tidy tables in `data/tidy/`. Fetch scripts: `scripts/fetch_thl.py`, `scripts/fetch_sotkanet.py`. All fetched 2026-11-14.

| Source ID | Dataset | Granularity | Years | Regions and strata | Publication lag (as modelled) | Pathway step | Success factor it feeds |
|---|---|---|---|---|---|---|---|
| S01 | THL specialist-care queues by specialty (`eshjono/jonotilanne`): patients waiting for treatment and for assessment by wait band, referrals and their processing time | 3 snapshots a year 2007–2020 (30.4., 31.8., 31.12.), monthly from 1/2021 to 9/2026 | 2007–2026 | 18 counties + HUS (Uusimaa's four counties and Helsinki report specialist care as HUS); ~100 specialties; no age, sex or diagnosis split | 45 days (cube updated 19.10.2026 holds 30.9.2026) | Referral, treatment start | Goal 3: treatment within target times (proxy only); regional differences known and used |
| S02 | THL procedure queue groups (`eshjono/jonoryhma`), group 27 endoscopy | as above | 2016–2026 | 18 counties + HUS | 45 days | Diagnosis | Goal 3 (proxy) |
| S03 | Breast screening participation, Sotkanet 3621 | annual | 2005–2024 | 22 counties + Helsinki, national | year Y usable from 31.12.Y+1 | Detection | Goal 2: 80% participation in every county |
| S04 | Cervical screening participation, Sotkanet 3620 | annual | 2005–2024 | as above | as above | Detection | Goal 2 |
| S05 | Colorectal screening participation, Sotkanet 6103 | annual | 2022–2024 | as above | as above | Detection | Goal 2 |
| S06 | Five-year relative survival, breast and colon, Sotkanet 3625, 3627 | multi-year periods | 2015–2024 | counties | as above | Outcome | Context only (not the poor-prognosis cancers of Goal 3) |
| S07 | Daily smokers by education, Sotkanet 4404, 4408, 4410 | survey years | 2013–2024 | counties, education level | as above | Risk exposure | Equality lens: socioeconomic (context) |
| S08 | Continuity of care COCI, Sotkanet 5502 | annual | 2019–2025 | counties | as above | Primary care | Context for roadmap 2.5.1 |
| S09 | County boundaries, Statistics Finland | – | 2026 | 21 counties, Helsinki, Åland | – | Map | – |

## What the public data cannot do

- **No measured cancer time intervals.** Days from referral to diagnosis or from diagnosis to first treatment are not published by county. The Goal 3 indicator itself is therefore `not estimated`; we use a cancer-specific queue proxy (oncology, specialty 65) and say so on every output.
- **Specialty is not diagnosis.** Only specialty 65 (oncology) is cancer-specific. Surgery, urology, gastroenterology, pulmonology and the endoscopy queue mix cancer and non-cancer patients; signals built on them are labelled "not cancer-specific". Surgical cancer treatment cannot be separated from elective surgery.
- **HUS is one unit.** The five Uusimaa areas cannot be told apart for specialist care.
- **Kainuu, and several small counties, report no or too few oncology queue patients**: status "cannot be judged", never "no gap".
- **Before 2023** the THL series are hospital-district figures mapped onto counties by THL; a break at 2023 is treated as an artefact first.
- **No age, sex or socioeconomic split** in the queue data: gaps are not adjusted for need. De facto equality is only approximated.
- **Stage, incidence, mortality, poor-prognosis survival by county**: not used (not machine-readable in the time available, or not public). Reported `not estimated`.

## Signals built from the data

Defined in `twin/signals.json` (label, exact definition, source, threshold with origin). Built by `scripts/build_signals.py`.
