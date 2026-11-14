# Master prompt: Equal Care Across Finland (Junction 2026, AstraZeneca challenge)

## Read first: the clock

Final submission is **Sunday 15 November 2026, 10:00 Finnish time (EET)**, and judging starts at 14:00. The challenge page's countdown points somewhat later, so plan to the earlier time and ask Wolfgang to confirm. Work out how many hours you have, and plan backward from a demo that runs and a video that has been watched by 08:00.

## The challenge

**"Equal Care Across Finland", by AstraZeneca.** https://hackjunction.app/participate/45/challenges/344

Goal: equal and effective cancer care everywhere in Finland. Time to diagnosis should be optimal, and patients should start treatment within target times wherever they live. Build an AI-powered system that does three things:

1. **Identify the gap.** Find differences in access to cancer care or in outcomes.
2. **Locate the gap in the pathway.** Show where the difference appears: detection, referral from primary to specialist care, diagnosis, or treatment initiation.
3. **Recommend what to do.** This is the most important part. Give concrete, evidence-based proposals that a wellbeing services county or the nation could implement. Diagnosis alone is not enough.

AstraZeneca names three known bottlenecks: late detection, the primary-to-specialist handover, and diagnosis-to-treatment time.

**Minimum requirements.** Failing any of these loses the challenge.
- Public data and/or AstraZeneca mentor insights only, with the source shown for **every** claim.
- At least one indicator from **Goal 3** of the national strategy (equal and effective treatment).
- Actionable recommendations, not only analysis.
- A **working demo**, shown live to the judges. Slides alone fail.
- Public, aggregate data only. No patient-level or personal data.
- A non-technical decision-maker must get the message and the action in **under two minutes**.

**Judging.** Optimise in this order.

| Weight | Criterion | What the judges ask |
|---|---|---|
| 30% | Actionability | Could a health centre or wellbeing services county implement the proposals? |
| 25% | Insight | Is the gap real and meaningful, and does it show where in the pathway it appears? |
| 20% | Data quality and transparency | Are sources clear, limitations admitted, and assumptions supported? |
| 15% | Execution | Does it work live in front of the judges? |
| 10% | Clarity | Does a decision-maker get the message and the action in two minutes? |

AstraZeneca wants to continue promising work after Junction with a Finnish wellbeing services county. So build every output so that one county could pick it up on Monday.

## Our idea

The strategy's monitoring is annual and looks backward: annual peer review of registry data. We claim that a digital twin of the cancer pathway, re-estimated every time a new period of data arrives, would notice sooner where in the pathway and in which county a gap is opening, and would turn that into a targeted action while it still matters.

We cannot run this live, so we **replay history in order**. The twin sees the data period by period and may use only what had been published by then. That replay is both the experiment and the live demo: the judges press play and watch the gap appear, get located and get an action.

## Sources

### Official documents (provided by the challenge)
- **National Cancer Strategy 2026–2035** (STM, December 2025), which is also the challenge's "background pack": https://files.hackjunction.app/resources/Kansallinen_syopastrategia_2026_2035_FINAL.pdf. Read its equality chapter, Goal 2 (prevention and early detection), Goal 3 (equal and effective treatment) and the Figure 1 indicators.
- **Implementation roadmap 2026–2031** (111 pp., in Finnish): https://files.hackjunction.app/resources/Kansallinen_syopastrategia_toimeenpanon_tiekartta_2026_2031.pdf. Every measure has a responsible actor, a budget, a **2026–2028 milestone**, a 2029–2031 milestone and an indicator. Its equality chapter (pp. 9–25) defines the six equality lenses. The regional inequality section (p. 12) cites large regional variation in time from first symptom to diagnosis and treatment, cancers found later in people living far from hospitals, and distances of 400 km to the nearest central hospital and 700 km to the nearest university hospital.
- **Link collection**: https://files.hackjunction.app/resources/Sy%C3%B6p%C3%A4strategiat%20ja%20sy%C3%B6p%C3%A4data_linkkikokoelma.pdf
- **Equality definitions**: the strategy takes them from THL. Formal equality means everyone gets the same service. De facto equality means everyone has the chance of the same outcome given their need. Measure the second.

Translation notes for machine-translated text: "wellness area" or "welfare area" means wellbeing services county (*hyvinvointialue*), "prevalence class" means stage (*levinneisyysluokka*), and "parity" means equality.

### Public data (from the link collection)
Usable in this time, aggregate:
- **Finnish Cancer Registry**: the statistics app and screening statistics, https://syoparekisteri.fi/tilastot/. Incidence, mortality, survival and screening participation, by region where available.
- **THL Sotkanet**: https://sotkanet.fi/. Regional indicators by wellbeing services county and year.
- **THL data and statistics**: https://thl.fi/data-ja-tilastot. Look for THL's access-to-care statistics (primary care, and specialist care by specialty). They are published monthly by county and are the best candidate for a fine-grained, chronological signal on the referral and treatment-start steps. Check that they exist, what they cover and how they are coded before you build on them.
- **Statistics Finland, causes of death** (StatFin): https://stat.fi/fi/tilasto/ksyyt
- **Kela open data**: special reimbursement rights for medicines, started and ended, https://vip.avoindata.fi/data/fi/dataset/voimassa-olleet-alkaneet-ja-paattyneet-laakekorvausoikeudet, and https://tietotarjotin.fi/tilastodata/2242438/avoin-data. If it can be split by region and by cancer-drug reimbursement code, it is a proxy for treatment starts.
- **NORDCAN**: https://nordcan.iarc.who.int/en. Nordic comparison for the survival target.
- **FICAN** quality registers and cancer registry pages: https://fican.fi/toiminta/arviointi-ja-seuranta/syopien-laaturekisterit/

Out of scope, because they need permits that take months: Findata, FinRegistry, the biobanks and iCAN.

### Mentor insights
These count as evidence. Kaisa Kaitila (Medical Affairs) is available on Saturday. Write Wolfgang a list of 5 to 8 sharp questions, the ones whose answers would change the model: which delays they see most; whether time-to-treatment targets are recorded anywhere; which counties they consider outliers and why; which roadmap measure they expect to slip. Log every answer in `SOURCES.md` as "mentor interview, role, date, time" and cite it like any other source.

### If our planning chat added other datasets
```
<<OPTIONAL: paste any extra datasets or documents from https://claude.ai/share/44abadda-da24-4e62-b31c-4330a177261c>>
```

## Peer-reviewed evidence added from Consensus (14 November 2026)

**Purpose.** Use the following studies to defend *which intervention to recommend*, *which measurable outcome it could plausibly change*, and *which effect sizes may enter a counterfactual*. These are **published results, not observations from Finnish counties**. Papers can use person-level research datasets, but **our system ingests only public aggregate Finnish data**. Never relabel a published before/after association as a causal effect or apply a cancer-specific number to all cancers.

### Nordic pathway interventions: most relevant to roadmap 2.5.2 and 3.1.2

| Evidence ID and study | Reported result and exact endpoint | Interpretation for this project |
|---|---|---|
| **E01 — Jensen et al., 2015, Denmark** ([BMC Cancer](https://consensus.app/papers/jensen-t%C3%B8rring-diagnostic-intervals-before-and-after/w:4c5162b1-af5a-4c03-a3ba-55b4ed998275/)) | GP-questionnaire/registry comparison, **12,558** patients. Adjusted **median diagnostic interval** was **17 days shorter** after implementation of standardized cancer patient pathways than before (95% CI **15–19 days shorter**); patients outside the pathway had a **4-day longer** median diagnostic interval than during implementation (95% CI 1–7). | Strong historical **effect-size candidate for referral/diagnostic pathway**, *not causal proof*. Test for patients excluded from the fast track; a good average can conceal a worsening outside it. Do not equate diagnostic interval with diagnosis-to-treatment time. |
| **E02 — Abuhasanein et al., 2022, Sweden** ([Scandinavian Journal of Urology](https://consensus.app/papers/abuhasanein-jahnson-standardized-care-pathways-for-patients-with/w:654fb4ef-4325-4509-a034-aa16cc380f40/)) | National bladder cancer register, **26,795** cases, pre-2016 vs 2016–2019. Median **referral-to-transurethral resection (TURBT)** fell **37 → 27 days** (**−10 days**); multidisciplinary meeting participation also increased. | Relatively strong *Swedish, cancer-specific before/after* candidate. TURBT may be a diagnostic and/or therapeutic procedure: preserve the precise endpoint, never call it generic *time to first cancer treatment*. Stage improvements were not consistently demonstrated. |
| **E03 — Sørensen et al., 2013, Denmark** ([European Archives of Oto-Rhino-Laryngology](https://consensus.app/papers/s%C3%B8rensen-johansen-a-%E2%80%9Cpackage-solution%E2%80%9D-fast-track-program-can-reduce/w:69425d77-8476-4856-a622-86a583735e77/)) | Head-and-neck cancer fast track with **pre-booked outpatient, imaging and diagnostic procedure slots**. Median **referral-to-first-visit**: **8 → 1 days**; median **referral-to-final-diagnosis**: **24 → 7–10 days** across post-implementation cohorts. | An immediately implementable **capacity/reserved-slot** action for a county. Effects are single-setting, specific to head-and-neck diagnostics, and observed before/after; make it a scoped scenario only when this action maps to a roadmap budget line. |
| **E04 — Villadsen et al., 2019, Denmark** ([Journal of Gastrointestinal and Liver Diseases](https://consensus.app/papers/villadsen-simonsen-effects-of-implementation-of-a-national-fast-track/w:b7deab81-068a-4620-9362-38064a95cb97/)) | Hepatocellular cancer fast-track before/after cohort, **309** suspected patients. Mean **referral-to-treatment** time: **53.2 → 35.9 days** (**−17.3 days**); survival difference **not statistically significant** (p=0.11). | One of the closest published **referral-to-treatment** endpoints. Small, cancer-specific and observational; do not generalise to all cancers or claim that it established a survival benefit. |
| **E05 — Nilssen et al., 2019, Norway** ([Cancer Epidemiology](https://consensus.app/papers/nilssen-brustugun-decreasing-waiting-time-for-treatment-before-and/w:b066be21-861a-42fe-b870-efcdd7ccdf3f/)) | National 2007–2016 trends for several cancers showed shorter treatment waits over time, **but no significant break at the 2015 pathway implementation**. | **Mandatory caution and zero-effect sensitivity case**. Historical improvements may be secular trends, not effects of the intervention. Include a counterfactual with *no incremental pathway benefit*. |
| **E06 — Borg et al., 2023, Sweden** ([Scientific Reports](https://consensus.app/papers/borg-h%C3%B6rstedt-performance-of-standardized-cancer-patient/w:f025cbaa-0a2a-4f15-8aa1-646067534aa6/)) | **19,204** pathway entrants in a Swedish region; observational **state-transition model** displays investigation duration, downstream treatment and missed cancers. Only **12/28** pathways met inclusion targets and **5/28** time targets. | Direct precedent for the **transparent state-transition/pathway visualisation**. It validates an analytical *design*, not our model's accuracy or any intervention effect; Swedish individual-level study data must not be treated as Finnish public data. |
| **E07 — Olsen et al., 2021, Norway** ([BMC Health Services Research](https://consensus.app/papers/olsen-jacobsen-equitable-access-to-cancer-patient-pathways-in/w:49d86e8a-075c-4087-8b09-e9e5bbfc2177/)) | Nationwide study of lung, colorectal, breast and prostate cancer found cancer-pathway access varied particularly by **age and hospital referral area**; among cancer patients, higher income increased the probability of pathway inclusion. | Key support for **Model 1's regional and socioeconomic inclusion gaps**. Measuring the waits of people *inside* the fast track alone can miss unequal access *to* it. No transferable numerical Finnish effect size. |
| **E08 — Lynch et al., 2022** ([British Journal of General Practice](https://consensus.app/papers/details/w:d8b760cb-4a97-4746-9121-093f398e21ec/)) | Comparative analysis of referral structures in 10 international cancer-benchmarking jurisdictions identified differences in **non-specific-symptom routes, direct diagnostic access, autonomy, and emergency pathways**. | Recommend a specified pathway for **non-specific but concerning symptoms**, plus clear GP-to-specialist escalation. This study characterises system differences; **no simulated effect size** is established by it. |
| **E09 — Ridd et al., 2015** ([British Journal of General Practice](https://consensus.app/papers/ridd-ferreira-patient%E2%80%93doctor-continuity-and-diagnosis-of-cancer/w:a9c69c59-650e-4d2c-b93f-27bdab233a6d/)) | English primary-care cohort: GP continuity had **small, inconsistent** associations with time to cancer diagnosis; much of the delay arose **after referral**. | **Do not assign an assumed positive time-saving to roadmap 2.5.1 (named GP)** based on continuity alone. Keep it as a policy action with *effect not estimated*, unless stronger outcome-matched evidence is found. |

### Finnish equity and screening: detection-stage evidence, not Goal 3 treatment-time evidence

| Evidence ID and study | Reported result and exact endpoint | Interpretation for this project |
|---|---|---|
| **E10 — Jäntti et al., 2021, Finland** ([European Journal of Public Health](https://consensus.app/papers/j%C3%A4ntti-hein%C3%A4vaara-sociodemographic-features-and-patterns-of/w:4402cd7a-f408-4fcf-bbc7-407096f1798e/)) | Finnish **2004–2016** colorectal screening programme, **233,211** invitees. **31.6%** did not participate (men **38.8%**, women **24.6%**); roughly **80%** of first-round non-participants also missed round two. | Evidence for **repeated non-participation and unequal detection access**. Programme period predates the present Finnish roll-out: do not use these historical rates as today's county estimates. An aggregate, county-stratified version could motivate tailored outreach. |
| **E11 — Seppänen et al., 2026, Finland** ([Journal of Medical Screening](https://consensus.app/papers/sepp%C3%A4nen-lamminm%C3%A4ki-disparities-in-participation-in-the-finnish/w:23bf7889-b400-478e-afaf-71afbb3c6167/)) | National 2019–2023 cervical screening invitation cohort, **1,395,084** invitees: **71.5%** participated. Participation **50.9%** among women with primary education versus **77.6%** with tertiary education. | Strong published Finnish demonstration of a **socioeconomic participation gap**. Do not imply county-by-education detail is publicly obtainable merely because the paper used linked individual data. This is a Goal 2/equality signal, **not** proof about time to treatment. |
| **E12 — Vives et al., 2024, Spain** ([JMIR Public Health and Surveillance; randomized trial](https://consensus.app/papers/vives-travier-effectiveness-and-acceptability-of-targeted-text/w:35d13aa4-45d9-4161-814f-cf23709fd62f/)) | Randomised reminder to people who picked up but had not returned a FIT kit: **4,563** SMS vs **4,806** control. Return at **30 days**: **64.2% vs 53.7%** (**+10.5 percentage points**); at **126 days**: **82.6% vs 77.7%** (**+4.9 pp**). | A plausible **targeted screening reminder** action and *causal trial evidence for this narrow endpoint*. It is **not** the expected increase in an entire county's screening participation. Include in Models 3/4 only if a concrete roadmap lever and the same budget are documented; otherwise show as **recommendation only, not simulated**. |
| **E13 — Coronado et al., 2023, USA** ([Cancer Epidemiology, Biomarkers & Prevention; cluster-randomized stepped-wedge trial](https://consensus.app/papers/coronado-nyongesa-effectiveness-and-cost-of-an-enhanced-mailed-fecal/w:00217d0d-3b96-4667-933a-807d19038353/)) | **27,585** participants. Enhanced mailed FIT outreach raised **six-month FIT completion by +2.8 pp** (95% CI **+0.4 to +5.2 pp**) in intention-to-treat analysis. Added text+automated-call cost reported as **US$0.66 per patient** in that setting. | A more conservative screening outreach scenario for the **same FIT-completion endpoint**. **Do not treat US costs as Finnish roadmap budgets** or multiply the per-protocol effect by the whole eligible population. |

### Why timeliness matters, and why outcome projections require restraint

| Evidence ID and study | Reported result | Interpretation for this project |
|---|---|---|
| **E14 — Hanna et al., 2020** ([BMJ; systematic review and meta-analysis](https://consensus.app/papers/hanna-king-mortality-due-to-cancer-treatment-delay-systematic/w:88c9ff9c-492d-4c74-a3b9-3b23d250c5c9/)) | **34 studies**, **1,272,681 patients**. For selected cancer surgeries, each additional **four-week treatment delay** was associated with mortality hazard ratios of approximately **1.06–1.08** (varies by cancer and treatment indication). | Strong rationale to **prioritise the Goal 3 time-to-treatment measure**. Association ≠ a causal effect of reducing county-level waits; never transform a specialty waiting-list proxy directly into lives saved or 5-year survival gains. |
| **E15 — Tope et al., 2023** ([eLife; review of reviews](https://consensus.app/papers/tope-farah-the-impact-of-lag-time-to-cancer-diagnosis-and/w:8aa11e9a-f17c-491e-bb21-a82e71b7bc24/)) | Review found **33 distinct definitions of delay intervals** across cancer studies and stressed **waiting-time paradox**, design heterogeneity and inconsistent endpoint definitions. | Guardrail: **define start, end, denominator, tumour type and intervention for every delay**. Urgent, very sick patients can be treated sooner, which can reverse naive wait-vs-mortality comparisons. Do not pool unmatched endpoints. |
| **E16 — Vedsted et al., 2022** ([BMJ Open; international breast cancer cohort](https://consensus.app/papers/vedsted-weller-diagnostic-pathways-for-breast-cancer-in-10/w:e58ee793-fa11-462d-9332-19d573203db3/)) | Breast cancer pathway comparison in **10 jurisdictions**, **3,471** women; large variation in the **patient, primary care, diagnostic and treatment intervals** across locations. | Supports **separate arrows** and reporting *which* interval differs, rather than a single headline 'wait'. Cross-jurisdiction variation is **not an intervention effect**. |

### Literature-driven implementation instructions (do these, not merely cite papers)

1. **Prioritise two narrow, defensible intervention families for the demo.** (A) *Standardised rapid cancer referral plus protected diagnostic slots*, linked to roadmap **2.5.2 / 3.1.2**; E01–E04 support diagnosis/referral endpoints with different scopes. (B) *Targeted reminder outreach for an existing organised screening programme*, linked to an explicitly verified **2.3/2.4** roadmap action only when the action and its funding actually include outreach; E12–E13 support FIT-completion only. Show a concrete delivery owner, patient group, workflow change and roadmap-funded cost for each; **do not invent a budget line**.
2. **Pre-commit the effect assumptions before Model 3 vs Model 4.** For each candidate create `EFFECTS.md` (or equivalent structured registry) with `evidence_id`, `study_design`, `country`, `cancer`, `population`, `intervention`, `comparator`, `time_start`, `time_end`, `outcome`, `absolute_effect`, `unit`, `confidence_interval`, `follow_up`, `transferability`, `roadmap_measure`, `budget_source`, `eligible_to_simulate`, `reason_if_not`, and `zero_effect_sensitivity`. Observed before/after results **must** carry a causal-uncertainty flag. Keep shared effect assumptions, uptake constraints, budgets and outcome definitions identical across Models 3 and 4.
3. **Use matched outcomes only.** E01's *diagnostic interval*, E02's *referral-to-TURBT*, E03's *referral-to-diagnosis*, E04's *referral-to-treatment*, and E12/E13's *FIT return* are **not interchangeable**. Unless the Finnish public aggregate dataset exposes the exact or a defensibly linked endpoint, present the intervention with its literature evidence but mark the **Finnish outcome effect `not estimated`**. A THL specialty wait is **not automatically** cancer diagnosis-to-treatment time.
4. **Show more than an attractive average.** Pair any faster in-pathway waiting time with **eligible-population/pathway inclusion**, non-fast-track referrals, geographical access and socioeconomic differences where aggregate data exist (E01, E07, E10–E11). Stratify or flag unidentifiable cells; don't infer individual-level discrimination from ecological aggregates.
5. **Require sensitivity and falsification.** Run **zero improvement** for pathway interventions (E05), conservative and high effects **only for matched endpoints** (E01–E04), and keep survival effects `not estimated` without patient-mix and stage-valid data (E14–E15). If Model 4 wins only because optimistic pathway effects were assumed, say so. Use a pre-existing trend model and a publication-lag-aware negative/positive control where possible.
6. **Separate evidence for action from evidence for the twin itself.** E06 supports a **state-transition display**, not a proven 'digital twin' or prospective warning lead time. The latter must be demonstrated via the project's **own leakage-free historical replay against persistence and trend baselines**. State every replay date's actually available information.
7. **Design a concrete county recommendation card.** Use: `gap → pathway arrow → measurable indicator → identifiable/uncertain → proposed action → named responsible actor → roadmap measure and € budget → matched published evidence (E-ID) → expected *endpoint-specific* change or not estimated → monitoring interval → failure mode`. Example *format only*: 'Elevated specialist referral wait; pilot protected diagnostic slots for [cancer] within [county]; inspect referral-to-diagnosis monthly and pathway inclusion; effect not estimated until a matched county series is available.' Do **not** present that example as a detected Finnish gap.
8. **Record evidence provenance in `SOURCES.md`.** List each E-ID with title, first author, year, journal, Consensus link, accessed **2026-11-14**, the outcome and exact effect claim used. Add a separate `DATA_MANIFEST.md` entry for every actual **Finnish public aggregate** input. A paper used to justify a policy is **not** a Finnish time-series datapoint.

**Evidence triage for a deadline:** Read **E01, E02, E05, E06, E07, E14 and E15** first. These cover a diagnostic pathway effect candidate, a Swedish cancer-specific comparator, counterevidence on causal attribution, the state-transition concept, equity of inclusion, clinical relevance of treatment delay, and the waiting-time paradox. **E12/E13** are optional if the demo also reaches screening.

## What "twin" means here

The data is aggregate, so **a twin is one wellbeing services county**, split by cancer group and population stratum where the data allows. It is never an individual patient. "Patient habits" means the measured behaviour of that population (smoking, alcohol, overweight, screening attendance, HPV vaccination, contacts with primary care). Say this plainly in every output.

Each twin is a small, explicit model of the pathway, in the challenge's own stages:

population at risk → **detection** (risk exposure, screening, symptomatic presentation) → **referral** from primary to specialist care → **diagnosis**, with stage → **treatment initiation** within target time → survival and mortality

The parameters are interpretable rates and delays on those arrows. At each replay step the twin re-estimates them from everything seen so far and emits one record per signal. The deliverable is a streaming estimator, not a dashboard of raw indicators and not a black-box forecaster.

**AI in the system.** The challenge asks for an AI-powered solution. The AI layer reads the twin's records and writes, for each county, a short decision-maker briefing in Finnish and English: where the gap is, how sure we are, and the recommended action with its sources. It may only cite records and sources that exist, and every sentence must point to one. Run it on the replay, not only at the end.

## The four models

All four run through **one replay protocol, one output schema and one scorecard**, so they can be laid side by side. Build that shared spine first.

**Model 1, the equality twin.** Its signals are gaps and how the gaps move. It uses the six equality lenses from the strategy and the roadmap: socioeconomic position, regional differences, older patients, children and adolescents, rare cancers and hereditary cancer syndromes, and poor-prognosis cancers. For each pathway step, the signal is the distance between counties or strata and its trend, judged against need (age-standardised, case-mix adjusted where the data allows).

**Model 2, the pathway twin.** The same pathway without the equality stratifiers: levels and flows for the population as a whole. Risk behaviour, participation, stage mix, access delays, incidence, survival, mortality.

**Model 3, the strategy to 2028.** The roadmap's **2026–2028 milestones**, run over the replay window as if they had been in place. The relevant ones (roadmap section numbers):
- 2.5.1, the named-GP (*omalääkäri*) programme widens continuity of care in every county.
- 2.5.2, standardised referral criteria and symptom-based pathways for at least the five most common cancers, piloted in the counties.
- 3.1.2, national care-chain descriptions for five cancers, with cancer-specific target times for access to treatment.
- 3.1.4, quality and effectiveness indicators for the five largest cancer groups.
- 3.2.1 to 3.2.4, a cancer quality register under THL (permanent operation from the start of 2028), annual national peer review of the first five cancers, and agreed procedures for reacting to deviations.
- The screening milestones in 2.3 and 2.4, such as breast screening extended to ages 46–74 and a regional lung-screening pilot.

Two rules. First, every lever you simulate needs a published effect size with a citation **and must match the Finnish endpoint being simulated**; apply the evidence registry and counterfactual safeguards in the Consensus literature section above. The Nordic models the roadmap names are the obvious evidence base: Denmark's *kræftpakkeforløb*, Sweden's SVF and Norway's *pakkeforløp*. A measure with no usable evidence is listed as "not simulated", never given an invented effect. Second, Model 3 only reacts to what its own monitoring would have shown: annual peer review of registry data that arrives about a year late.

**Model 4, the challenger.** Model 3's levers, re-targeted (which county, which step, which cancer) and re-timed by the signals from Models 1 and 2. It must use **the same levers and the same total budget as Model 3**. If it wins by doing more, we have shown nothing. Its only advantage is knowing sooner and knowing where. Its output is the recommendation list a county would receive.

The strategy period lies in the future, so Models 3 and 4 on historical data are counterfactuals. Present them as "had this been in place over these years", never as a forecast of 2028 or 2035.

## Success factors

These are the scoreboard. Goal 3 is required, so lead with it.

| Goal | Indicator and target (by 2035, in stages) |
|---|---|
| **3, equal and effective treatment** | **Patients start treatment within target times** (THL guideline 21/2016; cancer-specific target times defined by 2028 under roadmap 3.1.2) |
| | Five-year survival for poor-prognosis cancers reaches the Sweden–Norway average: lung +14 points, pancreas +6, liver +14 from 2023 NORDCAN levels |
| | Cancer mortality down 10% (from about 13,300 deaths a year) |
| | Reliable information on regional differences in diagnosis and treatment practice is available and used to narrow outcome differences (roadmap 3.2.2 and 3.2.3) |
| 2, prevention and early detection | At least 70% of cancers diagnosed at stage I–II |
| | Every screening programme reaches 80% participation in every county |
| | Preventable cancers down by 1,000 cases a year (of about 10,000) |
| 1, inclusion | Care experience (NPS above 80) and quality of life (PROM, EQ-5D-5L) measured and reported |
| 4, changing environment | Clinical trials up 10% a year; over 10% of patients in interventional trials; single-channel drug assessment |
| Equality, cross-cutting | Regional and socioeconomic differences in incidence, treatment and mortality are available to services and used to steer them |

Several of these will have no public data. Report those as **not estimated**. An empty cell is never "on target". The strategy itself says clinical notifications, which carry stage, cover only about 40% of cases, so any stage-based signal carries that caveat.

## How we judge a twin

These rules come from how our team builds physiological twins. They are what makes the "data quality and transparency" score (20%) defensible.

1. **No lookahead.** Use an expanding window. Each record answers "what would we have known by then?" and respects publication lag: registry data usually arrives about a year late.
2. **Interval and identifiability on every record.** Each signal carries an uncertainty interval and an `identifiable` flag. Small counties, small strata and rare cancers will often be unidentifiable. Say so; never raise an alarm on noise.
3. **Thresholds carry their origin.** Tag each one `strategy`, `roadmap`, `literature`, `model` or `qc`. Never present a `model` threshold as an official target.
4. **Controls.** As a positive control, the replay must flag a disruption we know happened, such as the 2020 pandemic dip in screening and diagnoses, and we report how many periods it took. Look for a negative control, a series that should not move. If there is none, say so.
5. **Beat the naive baselines.** Persistence and a straight trend. A twin that does not beat them on periods it never saw is not helping, and we say so.
6. **Pass marks before results.** Write the scorecard definition and commit it before the first Model 3 and Model 4 run.
7. **Fitted versus judged, shown in the plot.** Use one split for every plot: solid where the model was fitted, dashed and shaded where it predicts, with a tick or cross for each prediction.
8. **Artefact rulebook.** Keep a short list of signal combinations that indict the data, not the population. Start with:
   - a stage share that moves while the stage-unknown share also moves;
   - a drop in the newest year, which is registration lag;
   - breaks at 2023, the county reform (hospital districts became wellbeing services counties);
   - changes in screening age ranges and the colorectal screening roll-out from 2022.
9. **Counts name their subset.** "7 of 9 signals" must list which nine and show the misses beside it.
10. **Model before fit.** If no parameter values can reach the data, change the structure. Do not widen bounds, and treat a parameter pinned at a bound as unestimated.
11. **Decision log.** Keep `DECISIONS.md`. Every modelling choice you make is marked unexamined until one of us checks it. Put the ones that could change the headline at the top.

## Deliverables

**1. The live demo.** It is required, and Execution is worth 15%. It is a single page that runs offline from local files with no API call needed during judging. Pre-generate the AI briefings and keep any live call optional. It has:
- a map of Finland's wellbeing services counties, plus the pathway diagram (detection → referral → diagnosis → treatment) with each step lit by its signal status;
- a replay slider with play, and Model 3 and Model 4 side by side in one row, at equal height, on the same time axis;
- a county card: where the gap is, how sure we are, the recommended action, its cost from the roadmap's budget lines, the source for each claim, and "not estimated" where there is no data.

Labels go on the figure; sentences go in the caption.

**2. One visual per model** (four in total; the first brief said three twins), all from one template. They are exports of the demo's views.

**3. The film: Model 3 against Model 4**, signal by signal, scored on the success factors above.
- Two minutes is the target, because the judges' clarity test is two minutes. Use 1080p mp4 with burned-in captions, rendered from code (frames plus ffmpeg), with the scene list in a JSON file so a late rerun regenerates it.
- Spine:
  1. The gap, on the map, in one picture.
  2. The replay: a playhead moves through time, with Model 3 and Model 4 in aligned columns.
  3. Each Goal 3 signal in turn: when each model noticed, what it changed, and where the indicator ends against its target.
  4. A closing scoreboard listing every success factor, including those not estimated and those where Model 4 lost.
  5. The action for one named county.
- Show the method through what it does to the picture. No tiles of statistics.

**4. A two-minute pitch script** for the jury, built on the same spine.

## Order of work, and what to cut

1. **Data audit (first hour).** Write `DATA_MANIFEST.md`: each dataset, its granularity, years, regions and strata, its lag, and which pathway step and success factor it can feed. Write `SOURCES.md`.
2. **Thin slice end to end.** One Goal 3 signal (time to treatment, or its best public proxy), all counties, all four models, the demo page, and a 20-second film. Show Wolfgang.
3. **Widen.** Add the referral and detection steps, more cancers, the equality lenses, and the AI briefings.

If time runs short, cut breadth first: cancer groups, then signals, then lenses. Never cut the Goal 3 indicator, the Model 3 against Model 4 comparison, the per-county recommendations, the controls or the baselines. A narrow result that holds beats a wide one that does not.

## Working rules

- Keep everything in a git repo. Store each run under `runs/<model>/<experiment>/<timestamp>/` with a `meta.json` saying what produced it. Figures, the demo and the film read from the runs; they never recompute.
- Start long renders so they survive the session ending, and write a marker file when each finishes.
- The README needs: how to reproduce, what was built before the event, and where AI wrote the code.
- Ask Wolfgang only about the clock, the optional paste-in, the mentor answers and anything that needs an account. For everything else decide, log the choice in `DECISIONS.md`, and continue.

## When you finish

Report in this order:
1. The gap and where it sits in the pathway, with sources.
2. The scorecard for Model 3 and Model 4, factor by factor.
3. What the controls and baselines showed.
4. What could not be estimated, and why.
5. The unexamined decisions that could change the headline.
6. Where the demo, the visuals, the film and the pitch script are.
