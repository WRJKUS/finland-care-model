# Governance suggestions: rules

Written **before** the first governance run (`scripts/run_governance.py`), in the same way `SCORECARD.md` was written before the first Model 3/4 run. Results are in `runs/governance/replay/`. This file is not edited after results except under "Amendments", with a reason. Plan and reasoning: `plans/governance_suggestions_plan.pdf`.

## What a suggestion is

The county card says *what* to do about a gap. A governance suggestion says *who decides, in which forum, by when, and what happens if nothing changes*. There is one per county (HUS for the queue figures it reports as a whole), signal and month, chosen by the fixed rules below from the stored Model 1 records and Model 2 alarms. Nothing is recomputed and nothing looks ahead. The platform suggests; a person decides.

Every field carries a status label: **sourced** (a page in the roadmap or strategy, or a decree), **our proposal** (the sources are silent), **unchecked** (no human has confirmed it yet; that applies to everything here until the check in step 6 of the plan).

## The ladder

| Rung | Forum | Decision asked | Review | Escalates when | Status |
|---|---|---|---|---|---|
| 1 | County service unit that holds the queue | Put the signal on the unit's monthly review; no pilot decision yet | next month | still in gap after `persist_months` = 3 months in a row | our proposal (the roadmap gives pathway implementation to the counties and HUS, 3.1.2 p. 56) |
| 2 | County management (the owner named on the card's action) | Start the recommended action or not; name its owner; set a review date | decision + `min_action_months` = 6 months | still in gap 6 months after the decision | our proposal |
| 3 | The county's collaborative area (YTA), with its regional cancer centre | Review the division of responsibility for this pathway under the YTA agreement | 6 months | `national_counties` = 4 or more counties in gap on the signal, or a Model 2 national alarm on it in the last `alarm_window_months` = 3 months | forum sourced: YTA membership decree 91/2022 §1; YTA agreements divide regional pathway responsibility (roadmap 3.1.2, p. 57); the regional cancer centre follows the counties and reacts (3.2.3, p. 61); FICAN's five regional centres work with the university hospitals (strategy p. 9). Trigger: our proposal |
| 4 | National: FICAN's management group, where STM is represented | Treat it as a pathway design question, not a county failing; take it to the national review | the annual national peer review | – | sourced: mechanisms agreed in FICAN's management group with STM (3.2.3, p. 61); results reviewed nationally, peer reviews once a year (3.2.2, p. 60). Trigger: our proposal |

Rung 4 is reached by the national condition alone: a county newly in gap on a signal that is in gap in 4 or more counties goes straight to rung 4 (it is not a county failing). Otherwise the rungs are climbed in order by time in gap.

Thresholds are tied to numbers the model already uses: 3 months = the length of a gap episode in `SCORECARD.md`; 6 months = Model 4's minimum pilot length (decision 5) and the data freshness limit (decision 11); 4 counties = more counties than the K = 3 pilot slots (decision 3) can cover.

## Side tracks (never escalate)

| Code | Twin state | Suggestion | Status |
|---|---|---|---|
| D | Cannot be judged (too few patients, too wide an interval) | Ask for the data needed to judge. Never escalated, never read as "fine". For the cancer-specific treatment signals this is the existing data-gap action A-Q1; the cancer quality register (roadmap 3.2.1, pp. 59–60) is where such data is to come from | our proposal; register sourced |
| S | No new figure for over 6 months | Flag to the data owner (THL publishes the queue figures); no other suggestion on this signal until data returns | our proposal |
| H | A gap that reached rung 2 or higher has closed, for fewer than `closed_months` = 3 months | Keep the action running until the gap stays closed | our proposal |
| X | Closed 3 months in a row after reaching rung 2 or higher | Stop rule: release the pilot slot and record the outcome (one month) | our proposal |
| w | Watch (P 0.7–0.9) | No decision asked | – |

## Record

Each suggestion asks for the same record: the decision, its date, the reason, and the twin record cited (county, signal, month).

## Medicines (treatment step)

Not a county decision, and not a twin state: shown beside the treatment step as context. A new hospital medicine or a significant new indication is to get a national decision or guideline, usable in all counties, which the counties commit to follow, on a set timetable (roadmap 4.5.1, p. 94). Assessment and decision are to be gathered into one actor, through which the national assessment after the EU HTA assessment runs, building on Fimea, Palko and Hila (4.5.2, p. 95); for all new cancer medicines and significant indication extensions by 2029–2031 (p. 96). The strategy's indicator: cancer medicines are assessed through a single channel (strategy p. 5). There is no public county-level figure on when a new medicine reaches patients: `not estimated`.

## What the replay scores (2021-01 to 2026-10, the three policy signals, against the hindsight truth of `SCORECARD.md`)

1. Gap episodes (3 or more true gap-months in a row) that got a county management decision (rung 2 or higher) while the episode lasted, and the months from episode start to that decision.
2. Escalations to a collaborative area (entries into rung 3), per area per year: the load the ladder would put on the regional cancer centres.
3. Escalations raised in a month that hindsight does not confirm as a true gap-month.
4. National episodes (months in a row with the national condition) and how many hindsight does not confirm.
5. True gap-months with no suggestion at all, and months on the data track.

Reported as counts with their denominators, and reported even if unflattering (for example if the ladder fires so often it would swamp a regional cancer centre).

## What cannot be scored

Whether a county would have acted on the suggestion; whether the named forum has the authority attributed to it; any effect on waiting times, survival or mortality. These stay labelled as open on the page.

## Amendments (after results)

None.
