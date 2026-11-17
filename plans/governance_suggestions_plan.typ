#let ink = rgb("#1b2430")
#let mute = rgb("#5b6675")
#let line-c = rgb("#d5dae1")
#let accent = rgb("#0b5c8a")
#let tint = rgb("#eef4f8")
#let warn = rgb("#8a4b0b")

#set document(title: "Governance suggestions for the county twin: approach plan")
#set page(paper: "a4", margin: (x: 20mm, top: 20mm, bottom: 19mm),
  footer: context [
    #set text(size: 7.5pt, fill: mute)
    Governance suggestions: approach plan (draft, 15 November 2026)
    #h(1fr) #counter(page).display() / #counter(page).final().first()
  ])
#set text(font: ("Lato", "DejaVu Sans"), size: 9.6pt, fill: ink, lang: "en")
#set par(leading: 0.62em, spacing: 0.95em, justify: false)
#show raw: set text(font: "IBM Plex Mono", size: 0.9em)
#show heading.where(level: 1): it => block(above: 1.5em, below: 0.7em)[
  #set text(size: 13pt, weight: "bold", fill: accent)
  #it.body
]
#show heading.where(level: 2): it => block(above: 1.1em, below: 0.5em)[
  #set text(size: 10pt, weight: "bold")
  #it.body
]
#set table(stroke: (x, y) => (bottom: 0.5pt + line-c), inset: (x: 5pt, y: 5pt))
#show table.cell.where(y: 0): set text(weight: "bold", size: 8.4pt, fill: mute)
#let tag(body, c: accent) = box(inset: (x: 4pt, y: 1.5pt), radius: 2pt, fill: c.lighten(88%))[#text(size: 7.6pt, weight: "bold", fill: c)[#body]]
#let note(body) = block(fill: tint, inset: 9pt, radius: 3pt, width: 100%)[#body]

#text(size: 8.5pt, fill: mute, weight: "bold")[EQUAL CARE ACROSS FINLAND · COUNTY PATHWAY TWIN]
#v(-4pt)
#text(size: 21pt, weight: "bold")[Governance suggestions: approach plan]
#v(-6pt)
#text(size: 10.5pt, fill: mute)[Draft for team and mentor review. Nothing in this plan is built yet.]
#v(4pt)

#note[
  *In short.* The platform tells a county _what_ to do about a gap. It does not say _who decides, in which forum, by when, and what happens if nothing changes_. I would add that as a fixed-shape "governance suggestion" on every county card, chosen by written rules from the twin's own records, anchored to roadmap measure 3.2.3, replayed through 2021–2026 like every other output, and labelled as a proposal wherever the roadmap is silent. The rule thresholds and the body names need a human check before anything is shown as fact.
]

= 1. The gap

A county card today carries an action from `twin/actions.json` (five entries: A-T1, A-D1, A-R1, a screening entry and a data-gap entry). Each has an action, a named owner, the roadmap measure, the budget line, evidence, what to monitor and how it could fail. That answers "what". Three things are missing between the signal and the action:

- *Decision route.* The owner is a role inside the county. Nothing says where the decision is taken, who must be consulted, or when it moves beyond the county.
- *Timing.* The twin updates monthly. Mentor question 8 asks whether a county would act on a monthly signal at all. If the decision cycle is annual regardless, Model 4's lead on the referral handover (51% against 20% of gap-months reached) cannot be realised. Governance is the part that decides this, and the platform is silent on it.
- *Follow-through.* There is no stop rule, no escalation rule and no record of what was decided.

The roadmap has a place for exactly this. Measure 3.2.3 (pp. 61–62) asks FICAN and the ministry (STM) to "define and launch steering and management mechanisms" for responding to deviations, with EUR 3 M start-up funding and operating models to be agreed in 2026–2028. Measure 3.1.2 says responsibility for regional pathways is to be agreed in the collaborative-area (YTA) agreements. Its stated aim is that register data "must not stay at reporting level". The mechanisms themselves are still to be defined, so what the platform offers can only be a suggestion.

= 2. What a governance suggestion is

One record per county, pathway step and month, with the same fields every time:

#table(
  columns: (27mm, 1fr, 34mm),
  table.header[Field][Content][Where it comes from],
  [Trigger], [The twin state that fired it: identifiable gap and its duration, national alarm, not identifiable, stale data, gap closed.], [Model 1 and 2 records],
  [Forum and level], [County unit, county management, collaborative area with the regional cancer centre, or national (FICAN, STM).], [Roadmap, with page],
  [Decision asked], [Start the action, keep or release a pilot slot, request data, or watch.], [Rule table (section 3)],
  [Decision owner], [The role that decides, and who is consulted.], [`actions.json` owner, roadmap],
  [Review date], [When the decision is looked at again.], [Rule table],
  [Escalation rule], [What moves it up a level, stated as a twin condition.], [Rule table],
  [Stop rule], [When the slot is released.], [Rule table],
  [Record], [What should be written down: decision, date, reason, twin record cited.], [Fixed text],
  [Status label], [#tag[sourced] roadmap page given · #tag(c: warn)[our proposal] roadmap is silent · #tag(c: mute)[unchecked] no human has confirmed it], [Per field],
)

The status label matters most. Body names and decision rights that the roadmap states get a source chip like everything else in the demo. Everything else is shown as our proposal, in the same way `DECISIONS.md` marks modelling choices as unexamined.

= 3. The rule table

Written rules pick the suggestion. The language model only words it, under the same validator as the county briefings: a sentence that cites an unknown ID or a number not in the facts is rejected.

#table(
  columns: (40mm, 1fr, 40mm),
  table.header[Twin state][Suggested governance response][Level],
  [Gap identifiable, new], [Put on the unit's monthly review. No slot decision yet.], [County unit],
  [Gap identifiable, persisting], [Decision asked of county management: start the card's action, name the owner, set a review date.], [County management],
  [Gap persists after the action has run its minimum period], [Escalate: review of pathway responsibilities under the YTA agreement.], [Collaborative area, regional cancer centre],
  [Same gap in several counties, or a Model 2 national alarm], [Treat as a pathway design question, not a county failing.], [FICAN, STM],
  [Not identifiable (too few patients, wide interval)], [Ask for data, never escalate and never report "fine". Uses the existing data-gap action.], [County and quality register],
  [Data older than the freshness limit], [Flag to the data owner. Suspend other suggestions for that step.], [Data owner],
  [Gap closed and stays closed], [Stop rule: release the slot, record the outcome.], [County management],
)

#text(size: 8.6pt, fill: mute)[The numbers behind "new", "persisting", "several" and "stays closed" are deliberately left blank here. I would propose defaults tied to values the model already uses (the 6-month minimum slot length, the 6-month data freshness limit), write them into a `GOVERNANCE.md` before the first run, and log each as unexamined in `DECISIONS.md`.]

= 4. How I would build it

#table(
  columns: (6mm, 44mm, 1fr, 40mm),
  table.header[][Step][What is done][Output],
  [1], [Source the governance map], [Extract from the roadmap and strategy text who is responsible for what at each level (3.2.3, 3.1.2, 3.2.2, the implementation monitoring group), with page numbers. Mark every gap in the source as a gap.], [`twin/governance.json`],
  [2], [Commit the rules first], [Write the rule table and thresholds before any run, as was done for `SCORECARD.md`.], [`GOVERNANCE.md`],
  [3], [Compute on the replay], [Apply the rules to the stored Model 1 records, Model 2 alarms and Model 3/4 slots for every month of 2021–2026. No lookahead, no recomputation of the models.], [`runs/governance/replay/<timestamp>/`],
  [4], [Measure what can be measured], [See section 5.], [Governance block in the scorecard],
  [5], [Show it], [A "Who decides" block on the county card under the action; the ladder with the county's current rung marked; EN and FI; source chips; status labels. Briefings may cite governance IDs.], [`demo/template.html`, `build_demo.py`, `gen_briefings.py`],
  [6], [Human check], [Mentor and one county-side reader go through the governance map and thresholds. Answers logged in `SOURCES.md`; labels move from unchecked to checked or the entry is removed.], [Updated labels],
)

Steps 1 to 3 are small and depend only on files already in the repository. Step 5 is the largest piece of work. Step 6 is the one that decides whether the feature is credible, and it cannot be done by the agent.

= 5. How it would be judged

The replay can score the rules against the same hindsight gap-months the scorecard already uses. It cannot score whether a meeting would have led to a change.

#grid(columns: (1fr, 1fr), gutter: 8mm,
[
  == Can be measured
  - Months from gap onset to the first suggestion.
  - Escalations per county per year, as a measure of the load placed on the bodies named.
  - Share of escalations raised on gaps that hindsight says were not real.
  - Share of true gap-months with no suggestion.
  - Suggestions withheld because the county was not identifiable.
],
[
  == Cannot be measured
  - Whether a county would have acted.
  - Whether the named forum has the authority we attribute to it.
  - Any effect on waiting times, survival or mortality.

  These stay labelled as open, on the page, next to the suggestion.
])

= 6. Principles carried over from the rest of the build

- The platform suggests and a person decides. A twin is a county, never a patient.
- Uncertainty changes the ask. A county that cannot be judged gets a data request, not an escalation.
- No body is named without a source or a visible "our proposal" label.
- Rules are committed before the run and the result is reported even if it is unflattering, for example if the ladder fires so often it would swamp a regional cancer centre.

= 7. A second reading: governance of the twin itself

"Governance" may also mean who is accountable for the platform. That is a smaller, separate piece and I would not mix it into the county cards. It would be one page in About covering: who signs off the 17 entries in `DECISIONS.md` (none has yet been checked by a team member); who may change a threshold and how the change is recorded; the validator on AI-written text; and the rule that only public aggregate data is used. If this is the reading you meant, it can be done first, since it needs no new modelling.

= 8. Questions that change the plan

+ Which body receives a county-level deviation today, and is the collaborative area or the regional cancer centre the right first step above the county?
+ Would a county act on a monthly signal (mentor question 8)? If not, the ladder should be built around the annual cycle with a fast lane for exceptions.
+ Who would own the decision record: the county, FICAN, or nobody yet?
+ Is the aim suggestions to counties (sections 1 to 6), governance of the platform (section 7), or both?
