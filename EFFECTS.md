# Effect registry (pre-committed with the scorecard, before interpreting Model 3 vs Model 4)

Shared by Models 3 and 4. All before/after results carry a causal-uncertainty flag. A paper is evidence for an action, not a Finnish datapoint.

| evidence_id | study_design | country | cancer | intervention | comparator | time_start → time_end | absolute_effect | CI | transferability | roadmap_measure | budget_source | eligible_to_simulate | reason_if_not | zero_effect_sensitivity |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E01 | before/after, questionnaire + registry, n=12,558 | Denmark | all (pathway) | standardised cancer patient pathways | before implementation | first presentation → diagnosis (diagnostic interval) | −17 days median; +4 days outside pathway | 15–19; 1–7 | medium (Nordic), causal-uncertain | 2.5.2 | inside 3.1.1 (EUR 25 M / 5 y, p. 55) | **no** | No Finnish public series of diagnostic interval; `ref_assess_over90` is a queue share over all referral reasons | n/a |
| E02 | before/after, national register, n=26,795 | Sweden | bladder | standardised care pathway | pre-2016 | referral → TURBT | 37 → 27 days median | – | low (cancer-specific, procedure endpoint) | 3.1.2 | inside 3.1.1 | **no** | No matched Finnish endpoint | n/a |
| E03 | before/after, single setting | Denmark | head and neck | fast track with pre-booked slots | before | referral → diagnosis | 24 → 7–10 days median | – | low | 2.5.2 / 3.1.2 | inside 3.1.1 | **no** | No matched Finnish endpoint; endoscopy queue is all-indication | n/a |
| E04 | before/after cohort, n=309 | Denmark | hepatocellular | national fast track | before | referral → treatment | 53.2 → 35.9 days mean (−32.5%) | – ; survival p=0.11 | low (one cancer, small) | 3.1.2 | inside 3.1.1 | **scenario only** | Linked, not matched, to `treat_onc_wait` (queue ÷ referral inflow, in days). Shown as a labelled range, never as a result | yes: 0, half, full |
| E05 | national trend analysis | Norway | several | pathway implementation 2015 | pre-trend | treatment wait | no significant break | – | – | 2.5.2 / 3.1.2 | – | counter-evidence | Defines the zero-effect case | is the zero case |
| E09 | cohort | England | several | GP continuity | – | time to diagnosis | small, inconsistent | – | – | 2.5.1 | national named-GP programme (no amount in roadmap) | **no** | No usable positive effect; 2.5.1 listed as "not simulated" | n/a |
| E12 | RCT, n=9,369 | Spain | colorectal (FIT) | SMS reminder to kit non-returners | no SMS | kit pick-up → return | +10.5 pp at 30 d; +4.9 pp at 126 d | – | medium for that narrow endpoint | none funded (2.3/2.4 fund no outreach) | none | **no** | No roadmap budget line; endpoint is not county participation | n/a |
| E13 | cluster RCT, n=27,585 | USA | colorectal (FIT) | enhanced mailed outreach | usual | 6-month FIT completion | +2.8 pp | 0.4–5.2 | low | none funded | none (US costs not used) | **no** | as E12 | n/a |

Not simulated at all (no effect evidence matched to a Finnish endpoint): 2.5.1 named GP; 3.1.4 indicators; 3.2.1–3.2.4 quality register and peer review (they are the monitoring itself, represented by Model 3's decision rule); 2.3.3 breast screening 46–74; 2.3.4 lung pilot.

Survival and mortality effects: `not estimated` for every lever (E14, E15).

**What the Model 3 vs Model 4 comparison therefore rests on:** not effect sizes, but *where and when the same pilot slots sit* relative to gap-months judged in hindsight. Effect assumptions scale both models equally; with zero effect (E05) both achieve nothing.
