# Decision log

Every modelling choice below was made by the AI agent during the build and is **unexamined** until a team member checks it. Ordered by how much it could change the headline.

| # | Decision | Why | Could change the headline? | Status |
|---|---|---|---|---|
| 1 | Goal 3 proxy = oncology (specialty 65) treatment queue ÷ referral inflow per day ("days of inflow in the queue") | Only cancer-specific public series; measured referral-to-treatment days are not public | **Yes.** If the queue holds mostly follow-up bookings, the proxy says nothing about treatment start (mentor question 3) | unexamined |
| 2 | "True gap-month" for scoring = hindsight-smoothed county level above national level by the model threshold | Needed a truth that neither model saw | **Yes.** Thresholds are ours (`model`): ×1.5 national for the oncology index, +10 points for queue shares, +5 points for >21-day referrals and oncology >90 days | unexamined |
| 3 | Budget = 3 concurrent pilot slots per signal, 2021-01 to 2026-10 | Roadmap gives no pilot count; 2.5.2 and 3.1.2 are funded inside 3.1.1 (EUR 25 M / 5 y) | Checked by sensitivity (K = 2, 3, 5; SCORECARD.md): the referral win holds; oncology and endoscopy stay ties except at K = 5 | sensitivity run, still unexamined by a human |
| 4 | Model 3 sees annual figures of year Y−2 on 31 January of year Y; a "fast" variant sees Y−1 | "Annual peer review of registry data about a year late" | **Yes.** Against the fast variant Model 4's referral lead shrinks from 32 to 13 points; on oncology it disappears | unexamined |
| 5 | Model 4 slots run at least 6 months, start the month after the decision | A county cannot stand a pilot up and down monthly | Yes, moderately | unexamined |
| 6 | Referral signal pools pulmonology, gastroenterology, GI surgery, urology, gynaecology (assessment queue > 90 days) | Specialties that diagnose the common cancers | Yes: it is not cancer-specific; suspected cancer may bypass this queue (mentor question 5) | unexamined |
| 7 | Gap = county vs national level, no age or case-mix adjustment | Queue data has no such split | Yes for the equality claim: this is closer to formal than de facto equality | unexamined |
| 8 | THL data usable 45 days after the reference date; annual registry figures on 31.12. of the following year | Cube update dates; typical registry lag | Moderate | unexamined |
| 9 | Estimator: local-level Kalman filter on logit/log scale; observation noise from counts × overdispersion φ; q and φ re-chosen at each replay date by pooled predictive likelihood | Small counties get wide intervals by construction; no lookahead | Moderate. q sits at its upper bound for `treat_onc_wait` → treat that parameter as unestimated; the level there is close to the last value | unexamined |
| 10 | Overdispersion φ added after q hit its bound on three signals | Rule "model before fit": structure changed, bounds not widened | Low | unexamined |
| 11 | Identifiable = 80% interval narrower than 25 points (ratio < 2.5), data fresher than 6 months, queue ≥ 20 patients (oncology ≥ 10) | `qc` thresholds | Moderate: decides which small counties can ever be flagged | unexamined |
| 12 | A pathway step is never shown green on non-cancer-specific signals alone | Avoid false reassurance | Low | unexamined |
| 13 | Annual percentages without denominators get an assumed sd of 1 point | Sotkanet gives no invitee counts | Low | unexamined |
| 14 | E04 used as a *scenario* range on the oncology index, not as a result | Linked, not matched, endpoint | Low: labelled, and it cannot change the ranking | unexamined |
| 15 | Screening reminders: recommendation only | No funded roadmap line (2.3/2.4) | Low | unexamined |
| 16 | AI briefings by Claude (`claude -p --model sonnet`) at quarter ends 2021-03 … 2026-09 and 2026-10-31; sentences with an unknown citation or a number not in the facts are rejected | Run the AI on the replay, not only at the end | Low | unexamined |
| 17 | Clock: planned to the 10:00 EET deadline in the brief, not the later countdown on the challenge page | Earlier is safer | – | **ask Wolfgang** |
