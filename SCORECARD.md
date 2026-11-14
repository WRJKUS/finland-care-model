# Scorecard definition and pass marks

Committed **before** the first Model 3 / Model 4 run (see git history). Results are in `runs/`; this file is not edited after results except under "Amendments", with a reason.

## Shared protocol
- Replay dates: month ends 2016-01 to 2026-10. An observation is usable at replay date T only if `available <= T` (THL queue snapshot + 45 days; annual registry figures: year Y on 31.12.Y+1).
- One record per (replay date, signal, county): level, 80% interval, `identifiable`, status, threshold with origin.
- Policy window for Models 3 and 4: 2021-01 to 2026-10 (monthly THL data).
- Policy signals (one per pathway step): `treat_onc_wait` (treatment, Goal 3 proxy, cancer-specific), `dx_endo_over90` (diagnosis), `ref_assess_over90` (referral).

## Lever and budget (identical for Models 3 and 4)
- Lever family A: standardised rapid referral pathway with protected diagnostic/treatment slots (roadmap 2.5.2 / 3.1.2), deployed as a **county pilot slot** on one pathway step.
- Budget: **K = 3 concurrent pilot slots per signal**, each slot-month costs the same. Total cap = 3 x 70 months = 210 slot-months per signal for both models. K is our assumption (`model`); the roadmap funds these measures inside the 3.1.1 line (EUR 25 M / 5 years, roadmap p. 55) and does not state a number of pilots.
- Model 3 (strategy monitoring): decides once a year, on 31 January of year Y, from annual pooled values of year Y-2 (annual peer review, data about a year late). Picks up to K counties with the largest excess over the national annual value, provided the excess is above the same `model` threshold delta. Slots run 12 months.
- Model 3-fast (sensitivity): same, but sees year Y-1. Separates "knowing sooner" from "re-deciding more often".
- Model 4 (challenger): decides every month from Model 1 records. Candidates are counties with status `gap` (identifiable, P(gap > delta) >= 0.9), ranked by P x gap. A started slot runs at least 6 months. Never more than K slots.
- Unused slot-months are reported, not reallocated.

## Truth used for judging (hindsight, never used for decisions)
Two-sided smoothed level per county and month with final parameters. A county-month is a **true gap-month** if the smoothed level exceeds the smoothed national level by delta and the county is identifiable in hindsight (same small-number rule).

## Metrics
1. **Coverage**: share of true gap-months on which a slot was active. Primary.
2. **Precision**: share of used slot-months that fell on true gap-months.
3. **Excess-weighted coverage**: as 1, weighted by the size of the excess over the threshold.
4. **Lead time**: for each gap episode (>= 3 consecutive true gap-months), months from episode start to first active slot; missed episodes listed.
5. **Endpoint scenario (not a result)**: only for `treat_onc_wait`, excess queue-days removed under relative effect 0 (E05), conservative and high (E04, referral-to-treatment, HCC, before/after). The Finnish outcome effect is `not estimated`; this is shown as a labelled scenario. Effect assumptions are identical for both models, so they scale both and cannot change the ranking.

## Pass marks
- P1 Twin beats persistence AND linear trend on one-step-ahead MAE for a majority of scored signals. (Result known at commit time: beats trend on 10/10, persistence on 5/10 -> **fails P1 on persistence**; reported as such.)
- P2 Positive control: the 2020 pandemic disruption is flagged (|z| >= 3 on a national series) within 2 data periods. (Known at commit: **not flagged**, z = -0.76 on Jan-Apr 2020 referrals; reported as a failure.)
- P3 Negative control: no alarm on resident population. (Known at commit: passes.)
- P4 Model 4 coverage exceeds Model 3 coverage on the Goal 3 signal `treat_onc_wait`, with a county-block bootstrap 80% interval of the difference excluding 0.
- P5 Model 4 coverage also exceeds Model 3-fast. If P4 holds and P5 fails, the advantage is publication lag only, and we say so.
- P6 Model 4 precision is not lower than Model 3 precision by more than 5 points (no winning by spraying slots).
- Success factors with no public data are reported `not estimated`. Signals where Model 4 loses are listed beside the wins.
