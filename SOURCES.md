# Sources

Generated from `twin/sources.json` (the same registry the demo cites). Every claim in the demo, film and pitch points to one of these IDs.

## Finnish public aggregate data and official documents

| ID | Kind | Title | Link | Accessed |
|---|---|---|---|---|
| S01 | data | THL: Hoitoonpääsy erikoissairaanhoidossa – hoitoa ja hoidon tarpeen arviointia odottavat erikoisaloittain (cube eshjono/jonotilanne) — By wellbeing services county (HUS as one unit) and specialty; 3 snapshots/year 2007-2020, monthly from 2021; cube updated 19.10.2026. | https://sampo.thl.fi/pivot/prod/fi/eshjono/jonotilanne/fact_eshjono_jonotilanne | 2026-11-14 |
| S02 | data | THL: Toimenpidettä odottavat ja odotusajat jonoryhmittäin (cube eshjono/jonoryhma), group 27 endoscopy — From 2016. | https://sampo.thl.fi/pivot/prod/fi/eshjono/jonoryhma/fact_eshjono_jonoryhma | 2026-11-14 |
| S03 | data | Finnish Cancer Registry via Sotkanet, indicator 3621: breast screening participation, % of invited | https://sotkanet.fi/sotkanet/fi/metadata/indicators/3621 | 2026-11-14 |
| S04 | data | Finnish Cancer Registry via Sotkanet, indicator 3620: cervical screening participation, % of invited | https://sotkanet.fi/sotkanet/fi/metadata/indicators/3620 | 2026-11-14 |
| S05 | data | Finnish Cancer Registry via Sotkanet, indicator 6103: colorectal screening participation, % of invited | https://sotkanet.fi/sotkanet/fi/metadata/indicators/6103 | 2026-11-14 |
| S06 | data | Finnish Cancer Registry via Sotkanet, indicators 3625 and 3627: five-year relative survival, breast and colon cancer | https://sotkanet.fi/sotkanet/fi/metadata/indicators/3625 | 2026-11-14 |
| S07 | data | THL via Sotkanet, indicators 4404, 4408, 4410: daily smokers, all / low education / high education | https://sotkanet.fi/sotkanet/fi/metadata/indicators/4404 | 2026-11-14 |
| S08 | data | THL via Sotkanet, indicator 5502: continuity of care (COCI), primary care physician visits | https://sotkanet.fi/sotkanet/fi/metadata/indicators/5502 | 2026-11-14 |
| S09 | data | Statistics Finland: wellbeing services county boundaries 1:4 500 000 (tilastointialueet:hyvinvointialue4500k) | https://geo.stat.fi/geoserver/tilastointialueet/wfs | 2026-11-14 |
| S10 | document | Kansallinen syöpästrategia 2026–2035 (STM, 2025). Figure 1 indicators p. 5; clinical notifications cover about 40% of cases p. 30 | https://files.hackjunction.app/resources/Kansallinen_syopastrategia_2026_2035_FINAL.pdf | 2026-11-14 |
| S11 | document | Kansallisen syöpästrategian toimeenpanon tiekartta 2026–2031. Regional inequality pp. 12–13; measures 2.3–2.5 pp. 44–53; 3.1–3.2 pp. 55–63; cost table pp. 105–107 | https://files.hackjunction.app/resources/Kansallinen_syopastrategia_toimeenpanon_tiekartta_2026_2031.pdf | 2026-11-14 |
| S12 | document | Valtioneuvoston asetus sosiaali- ja terveydenhuollon yhteistyöalueista 91/2022, §1: the five collaborative areas (YTA) and the wellbeing services counties, Helsinki and HUS in each | https://www.finlex.fi/api/media/statute/20090/mainPdf/main.pdf | 2026-11-15 |
| S13 | document | Valtiovarainministeriö: Hyvinvointialueet ja yhteistyöalueet. The county in each collaborative area that maintains a university hospital (HUS in the south) | https://vm.fi/hyvinvointi-ja-yhteistyoalueet | 2026-11-15 |

## Peer-reviewed evidence (via Consensus, accessed 2026-11-14)

Published results, not observations from Finnish counties. The exact claim used is in the title column; simulation eligibility is in `EFFECTS.md`.

| ID | Study, endpoint and exact claim used | Link |
|---|---|---|
| E01 | Jensen et al. 2015, BMC Cancer (Denmark). Diagnostic intervals before and after cancer patient pathways: adjusted median diagnostic interval 17 days shorter (95% CI 15–19); outside the pathway 4 days longer (1–7). Before/after. | https://consensus.app/papers/jensen-t%C3%B8rring-diagnostic-intervals-before-and-after/w:4c5162b1-af5a-4c03-a3ba-55b4ed998275/ |
| E02 | Abuhasanein et al. 2022, Scand J Urol (Sweden). Bladder cancer standardized care pathways: median referral-to-TURBT 37 -> 27 days. Before/after. | https://consensus.app/papers/abuhasanein-jahnson-standardized-care-pathways-for-patients-with/w:654fb4ef-4325-4509-a034-aa16cc380f40/ |
| E03 | Sørensen et al. 2013, Eur Arch Otorhinolaryngol (Denmark). Head-and-neck fast track with pre-booked slots: referral-to-first-visit 8 -> 1 days; referral-to-diagnosis 24 -> 7–10 days. Single setting, before/after. | https://consensus.app/papers/s%C3%B8rensen-johansen-a-%E2%80%9Cpackage-solution%E2%80%9D-fast-track-program-can-reduce/w:69425d77-8476-4856-a622-86a583735e77/ |
| E04 | Villadsen et al. 2019, J Gastrointestin Liver Dis (Denmark). Hepatocellular cancer fast track: mean referral-to-treatment 53.2 -> 35.9 days; survival difference not significant (p=0.11). n=309, before/after. | https://consensus.app/papers/villadsen-simonsen-effects-of-implementation-of-a-national-fast-track/w:b7deab81-068a-4620-9362-38064a95cb97/ |
| E05 | Nilssen et al. 2019, Cancer Epidemiology (Norway). Treatment waits fell 2007–2016 but with no significant break at the 2015 pathway implementation. Zero-effect caution. | https://consensus.app/papers/nilssen-brustugun-decreasing-waiting-time-for-treatment-before-and/w:b066be21-861a-42fe-b870-efcdd7ccdf3f/ |
| E06 | Borg et al. 2023, Scientific Reports (Sweden). State-transition model of standardized cancer patient pathways; 12/28 pathways met inclusion targets, 5/28 time targets. Design precedent only. | https://consensus.app/papers/borg-h%C3%B6rstedt-performance-of-standardized-cancer-patient/w:f025cbaa-0a2a-4f15-8aa1-646067534aa6/ |
| E07 | Olsen et al. 2021, BMC Health Serv Res (Norway). Access to cancer patient pathways varied by age and hospital referral area; higher income raised inclusion. | https://consensus.app/papers/olsen-jacobsen-equitable-access-to-cancer-patient-pathways-in/w:49d86e8a-075c-4087-8b09-e9e5bbfc2177/ |
| E08 | Lynch et al. 2022, Br J Gen Pract. Referral structures in 10 jurisdictions: non-specific-symptom routes, direct diagnostic access. No effect size. | https://consensus.app/papers/details/w:d8b760cb-4a97-4746-9121-093f398e21ec/ |
| E09 | Ridd et al. 2015, Br J Gen Pract. GP continuity: small, inconsistent associations with time to cancer diagnosis. | https://consensus.app/papers/ridd-ferreira-patient%E2%80%93doctor-continuity-and-diagnosis-of-cancer/w:a9c69c59-650e-4d2c-b93f-27bdab233a6d/ |
| E10 | Jäntti et al. 2021, Eur J Public Health (Finland). Colorectal screening 2004–2016: 31.6% non-participation; about 80% of first-round non-participants missed round two. | https://consensus.app/papers/j%C3%A4ntti-hein%C3%A4vaara-sociodemographic-features-and-patterns-of/w:4402cd7a-f408-4fcf-bbc7-407096f1798e/ |
| E11 | Seppänen et al. 2026, J Med Screen (Finland). Cervical screening 2019–2023: participation 50.9% with primary education vs 77.6% with tertiary. | https://consensus.app/papers/sepp%C3%A4nen-lamminm%C3%A4ki-disparities-in-participation-in-the-finnish/w:23bf7889-b400-478e-afaf-71afbb3c6167/ |
| E12 | Vives et al. 2024, JMIR Public Health Surveill (Spain, RCT). SMS reminder to FIT-kit non-returners: return at 30 days 64.2% vs 53.7% (+10.5 pp); at 126 days +4.9 pp. | https://consensus.app/papers/vives-travier-effectiveness-and-acceptability-of-targeted-text/w:35d13aa4-45d9-4161-814f-cf23709fd62f/ |
| E13 | Coronado et al. 2023, Cancer Epidemiol Biomarkers Prev (USA, cluster RCT). Enhanced mailed FIT outreach: six-month completion +2.8 pp (95% CI 0.4–5.2). | https://consensus.app/papers/coronado-nyongesa-effectiveness-and-cost-of-an-enhanced-mailed-fecal/w:00217d0d-3b96-4667-933a-807d19038353/ |
| E14 | Hanna et al. 2020, BMJ (meta-analysis). Each four-week delay of cancer surgery associated with mortality HR about 1.06–1.08. Association, not county-level causal effect. | https://consensus.app/papers/hanna-king-mortality-due-to-cancer-treatment-delay-systematic/w:88c9ff9c-492d-4c74-a3b9-3b23d250c5c9/ |
| E15 | Tope et al. 2023, eLife (review of reviews). 33 distinct definitions of delay intervals; waiting-time paradox. | https://consensus.app/papers/tope-farah-the-impact-of-lag-time-to-cancer-diagnosis-and/w:8aa11e9a-f17c-491e-bb21-a82e71b7bc24/ |
| E16 | Vedsted et al. 2022, BMJ Open. Breast cancer pathways in 10 jurisdictions: large variation in patient, primary care, diagnostic and treatment intervals. | https://consensus.app/papers/vedsted-weller-diagnostic-pathways-for-breast-cancer-in-10/w:e58ee793-fa11-462d-9332-19d573203db3/ |

**Added 2026-11-17** (fetched from PubMed, not via Consensus), shown in the demo as "What a wait does to a tumour":

| ID | Study, endpoint and exact claim used | Link |
|---|---|---|
| E17 | Jensen et al. 2007, Radiother Oncol (Denmark). Head and neck cancer, scans before and after the wait for radiotherapy (median 28 days, 61 patients): 12 (20%) new lymph-node metastases, 10 (16%) progressed in TNM classification; the faster-growing half doubled in volume in 30 days. | https://pubmed.ncbi.nlm.nih.gov/17493700/ |
| E18 | O'Rourke, Edwards 2000, Clin Oncol (UK). 29 lung cancer patients awaiting curative radiotherapy: 6 (21%) became incurable on the waiting list; median 54 days between diagnostic and planning scans. | https://pubmed.ncbi.nlm.nih.gov/10942328/ |
| E19 | Shinkwin et al. 2021, Colorectal Dis (Cardiff). Colorectal cancer in 2020 vs 2018–19: emergency presentation 96/267 (36.0%) vs 154/539 (28.6%), P=0.03; large bowel obstruction 8.6% vs 4.3%; T4 34.5% vs 27.1%. Single centre, before/after. | https://pubmed.ncbi.nlm.nih.gov/33793063/ |
| E20 | Bhat et al. 2021, Tumori (London). 121 resected early-stage lung cancers, median 2.6 months to surgery: 36% upstaged at surgery, but upstaging was not associated with waiting time. Counter-evidence. | https://pubmed.ncbi.nlm.nih.gov/33021465/ |

## Mentor insights

None logged. The mentor (Kaisa Kaitila, Medical Affairs, AstraZeneca) was available on Saturday 14 November 2026; no answers had reached this repository when the runs were made. Questions are in `MENTOR_QUESTIONS.md`. Log answers here as: "mentor interview, role, date, time", then cite them like any other source.

## Not fetched

- THL Ohjaus 21/2016 (*Hoitoonpääsyn seuranta syövän hoidossa*), which the strategy cites for target times (strategy p. 5, footnote). Neither the strategy nor the roadmap prints numeric target times, so no official time target is used anywhere in this project.
- Finnish Cancer Registry statistics application (interactive only; incidence, stage and survival by region were not machine-readable in the time available), Statistics Finland causes of death, Kela reimbursement data, NORDCAN. Success factors depending on them are reported `not estimated`.
