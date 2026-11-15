// The county pathway twin drawn as a circuit.
// Reads data.json (written by scripts/export_circuit.py from runs/); recomputes nothing.
// Build: typst compile visuals/circuit/circuit.typ
#import "@preview/cetz:0.3.4"

#let D = json("data.json")

// palette: same tokens as demo/template.html
#let ink = rgb("#1c2430")
#let mut = rgb("#5d6878")
#let line-c = rgb("#dfe3e8")
#let bg = rgb("#f4f5f7")
#let c-gap = rgb("#c8372d")
#let c-watch = rgb("#e0a030")
#let c-ok = rgb("#4f9d7c")
#let c-unid = rgb("#aab1bb")
#let c-none = rgb("#e9ecef")
#let c-m3 = rgb("#7b6cb0")
#let c-m4 = rgb("#2a6f97")
#let c-ai = rgb("#b5651d")
#let step-c = (detection: rgb("#5b8e7d"), referral: rgb("#2a6f97"), diagnosis: rgb("#8a5a9e"), treatment: rgb("#b5651d"))
#let st-col = (g: c-gap, w: c-watch, o: c-ok, u: c-unid, s: rgb("#cfd4db"), n: c-none, x: rgb("#f3f4f6"))
#let st-name = (g: "gap", w: "watch", o: "no gap seen", u: "cannot be judged", s: "stale", x: "no data")

#set page(paper: "a4", flipped: true, margin: (x: 11mm, top: 10mm, bottom: 10mm), fill: white,
  footer: context [#set text(6.5pt, fill: mut); Source of every number: #raw(D.model1_run) and runs/compare/policy/#D.policy_run, exported by scripts/export_circuit.py. Public aggregate data only; a twin is one county, never a patient. #h(1fr) #counter(page).display()])
#set text(font: ("FreeSans", "DejaVu Sans"), size: 8pt, fill: ink)
#set par(leading: 0.5em)
#show raw: set text(font: "IBM Plex Mono", size: 0.95em)
#let num(x) = text(font: "IBM Plex Mono", x)
#let ck = text(font: "DejaVu Sans", fill: c-ok, weight: "bold", "✓")
#let pct(x) = str(calc.round(x * 100, digits: 1)) + "%"
#let pct0(x) = str(calc.round(x * 100)) + "%"
#let title(t, sub) = {
  text(15pt, weight: "bold", t)
  linebreak()
  text(8.5pt, fill: mut, sub)
  v(1.5mm)
}
#let tag(t, c) = box(fill: c.lighten(80%), stroke: 0.5pt + c, radius: 2pt, inset: (x: 2pt, y: 1pt), text(5.8pt, fill: c.darken(30%), weight: "bold", t))
#let cs = tag("cancer-specific", c-gap)
#let ncs = tag("proxy", mut)
#let chip(t, c, fg: white) = box(fill: c, inset: (x: 2pt, y: 1.2pt), radius: 1.5pt, text(fill: fg, size: 6.5pt, t))
#let sec(letter) = box(fill: ink, radius: 1.5pt, inset: (x: 2.5pt, y: 1.5pt), text(6.5pt, fill: white, weight: "bold", letter))
#let hd(t, c) = text(weight: "bold", fill: c, size: 7.4pt, t)
#let sm(t) = text(fill: mut, size: 6.4pt, t)

// ============================================================ PAGE 1: the circuit, in named sections
#title("The county twin as a circuit",
  [Top row: the twin itself, one per county. It turns published numbers into a status for every signal, every month. Bottom row: what reads those records. Letters A–J name the sections; page 2 explains each one.])

#align(center, cetz.canvas(length: 1mm, {
  import cetz.draw: *
  let frame(x0, y0, x1, y1, t) = {
    rect((x0, y0), (x1, y1), radius: 2, fill: rgb("#f7f8fa"), stroke: 0.5pt + rgb("#c5cbd3"))
    content((x0 + 1.2, y1 - 1.2), anchor: "north-west", box(fill: ink, radius: 1.5pt, inset: (x: 3pt, y: 2pt), text(6.8pt, fill: white, weight: "bold", t)))
  }
  let blk(c, w, h, body, stroke: 0.6pt + ink, fill: white) = {
    let (x, y) = c
    rect((x - w / 2, y - h / 2), (x + w / 2, y + h / 2), radius: 1.2, stroke: stroke, fill: fill)
    content(c, box(width: (w - 3) * 1mm, align(left, text(6.8pt, body))))
  }
  let st(c: ink, w: 0.7pt, dash: none) = (paint: c, thickness: w, dash: dash)
  let arrow(..pts, c: ink, w: 0.7pt, dash: none) = line(..pts, stroke: st(c: c, w: w, dash: dash), mark: (end: "stealth", fill: c, scale: 0.55))
  let wire(..pts, c: ink, w: 0.7pt, dash: none) = line(..pts, stroke: st(c: c, w: w, dash: dash))
  let dot(p, c: ink) = circle(p, radius: 0.6, fill: c, stroke: none)
  let hop(x, y, c: ink, dash: none) = arc((x, y + 1.4), start: 90deg, stop: -90deg, radius: 1.4, stroke: st(c: c, w: 0.7pt))

  // ---------------- frames
  frame(0, 78, 33, 156, "A · Inputs")
  frame(36, 78, 64, 156, "B · Clock")
  frame(67, 78, 121, 156, "C · Signals")
  frame(124, 78, 161, 156, "D · Estimator")
  frame(164, 78, 194, 156, "E · Judge")
  frame(197, 78, 222, 156, "F · Status")
  frame(225, 78, 275, 156, "G · Records")
  frame(0, 0, 91, 61, "H · Display")
  frame(96, 0, 199, 61, "I · Policy")
  frame(203, 0, 275, 61, "J · Scoring")

  // ---------------- A inputs -> B clock
  blk((16.5, 132), 29, 17, [#hd("S01 · THL queues", ink)\ #sm[specialist care by specialty: wait bands, referrals; 3 a year to 2020, then monthly]], fill: bg)
  blk((16.5, 111), 29, 17, [#hd("S02 · THL procedures", ink)\ #sm[procedure queues, incl. endoscopy (group 27), from 2016]], fill: bg)
  blk((16.5, 90), 29, 17, [#hd("S03–S05 · Sotkanet", ink)\ #sm[screening participation by county, yearly]], fill: bg)
  for y in (132, 111, 90) { wire((31, y), (34.5, y)) }
  wire((34.5, 90), (34.5, 132), w: 1.4pt)
  arrow((34.5, 111), (37, 111))
  blk((50, 111), 26, 48, [#hd("Publication gate", c-gap)\ a number enters the replay at month T only once it had been published\ #v(0.6mm) #sm[THL: 45 days after the reference date\ yearly figures: 31 Dec of the next year]\ #v(0.6mm) #sm[so the replay never uses hindsight]], stroke: 1pt + c-gap, fill: c-gap.lighten(93%))

  // ---------------- B -> C signals (bus)
  wire((63, 111), (65.5, 111)); dot((65.5, 111))
  wire((65.5, 87), (65.5, 144.25), w: 1.4pt)
  let sigs = (
    (144.25, 10.5, [#hd("Detection", step-c.detection) #sm[· 3 signals] #cs\ #sm[screening participation: breast, cervix, colorectal]], step-c.detection, none),
    (131.25, 11.5, [#hd("Referral", step-c.referral) #sm[· 2 + flow] #ncs\ #sm[★ waiting > 90 d for a first assessment · referral handled after 21 d]], step-c.referral, none),
    (118.5, 10, [#hd("Diagnosis", step-c.diagnosis) #sm[· 1 signal] #ncs\ #sm[★ endoscopy queue: share waiting > 90 d]], step-c.diagnosis, none),
    (102.5, 18, [#hd("Treatment", step-c.treatment) #sm[· 3 signals]\ #sm[★ oncology queue ÷ referrals (Goal 3 proxy)] #cs\ #sm[oncology > 90 d] #cs\ #sm[surgery + urology > 90 d] #ncs], step-c.treatment, none),
    (87, 9, [#hd("Control", mut) #sm[· population change: should never alarm]], mut, "dashed"),
  )
  for (y, h, body, c, dash) in sigs {
    blk((94, y), 50, h, body, stroke: (paint: c, thickness: 0.8pt, dash: dash))
    arrow((65.5, y), (69, y), dash: dash)
    wire((119, y), (122.5, y), dash: dash)
  }
  wire((122.5, 87), (122.5, 144.25), w: 1.4pt)
  arrow((122.5, 116), (126, 116))

  // ---------------- D estimator
  blk((142.5, 116), 33, 58, [#hd("Estimator", ink) #sm[(the twin)]\ one small model for every signal in every county\ #v(0.6mm) keeps a running estimate of the true level and an 80% interval, updated as each number is published\ #v(0.6mm) #sm[local-level Kalman filter on the logit / log scale; noise from the counts × φ; drift q; q and φ re-fitted every month on past data only]\ #v(0.6mm) #sm[small county ⇒ wide interval]], stroke: 1.1pt + ink)

  // ---------------- D -> E judge
  wire((159, 116), (162.5, 116)); dot((162.5, 116))
  arrow((162.5, 116), (162.5, 132), (166, 132))
  arrow((162.5, 116), (162.5, 99), (166, 99))
  blk((179, 132), 26, 30, [#hd("Comparator", ink)\ is the county worse than national + δ? ⇒ #num("P(gap)")\ #v(0.4mm) #sm[national = the same estimator run for all of Finland · δ origin: model]])
  blk((179, 99), 26, 30, [#hd("Enough data?", ink)\ 80% interval < 25 pts\ data < 6 months old\ ≥ 20 patients\ #sm[(oncology index ≥ 10) · origin: qc]])

  // ---------------- E -> F status
  arrow((192, 132), (195.5, 132), (195.5, 124), (199, 124))
  arrow((192, 99), (195.5, 99), (195.5, 108), (199, 108))
  blk((209.5, 116), 21, 44, [#hd("Status", ink)\ #v(0.4mm) #chip("gap", c-gap) #sm[P ≥ 0.9]\ #chip("watch", c-watch, fg: ink) #sm[≥ 0.7]\ #chip("ok", c-ok)\ #chip("cannot judge", c-unid, fg: ink)\ #v(0.4mm) #sm[stale: nothing new for 6 months]], stroke: 1.1pt + ink)

  // ---------------- F -> G records
  arrow((220, 116), (227, 116), w: 1.1pt)
  blk((249, 124), 44, 26, [#hd("Model 1", ink) #sm[· equality twin]\ one record per month × signal × county: level, interval, #num("P(gap)"), status, data-through date\ #sm[runs/model1/…/records.csv]], fill: ink.lighten(90%), stroke: 1.2pt + ink)
  arrow((249, 111), (249, 102))
  content((250.5, 106.5), anchor: "west", sm[national rows])
  blk((249, 93), 44, 18, [#hd("Model 2", ink) #sm[· pathway twin]\ #sm[the national rows; an alarm when a new value is ≥ 3 standard errors from its forecast]], fill: ink.lighten(94%))

  // ---------------- record bus
  wire((271, 124), (273.5, 124), w: 1.5pt)
  wire((273.5, 124), (273.5, 67), (4, 67), w: 1.5pt)
  content((5, 68.6), anchor: "south-west", text(6.5pt, weight: "bold")[record bus #text(weight: "regular", fill: mut)[· everything below reads only these records]])

  // ---------------- bypass wires (cross the bus without connecting)
  wire((50, 87), (50, 72.5), (93.5, 72.5), (93.5, 68.4), c: c-m3, dash: "dashed")
  hop(93.5, 67, c: c-m3)
  arrow((93.5, 65.6), (93.5, 13), (100, 13), c: c-m3, dash: "dashed")
  wire((150, 87), (150, 72.5), (222, 72.5), (222, 68.4), c: mut, dash: "dashed")
  hop(222, 67, c: mut)
  arrow((222, 65.6), (222, 54), c: mut, dash: "dashed")
  content((223.5, 63.5), anchor: "west", sm[from D, after the fact])

  // ---------------- H display
  dot((30, 67)); arrow((30, 67), (30, 53))
  blk((22, 36), 40, 34, [#hd("Step combiner", step-c.diagnosis)\ each pathway step shows the *worst* status among its signals\ #v(0.6mm) #sm[a step that has a cancer-specific signal is green only if that signal is ok; referral and diagnosis have none]], stroke: 0.9pt + step-c.diagnosis)
  dot((70, 67)); arrow((70, 67), (70, 56))
  blk((70, 45), 36, 22, [#hd("AI briefing", c-ai) #sm[· Claude]\ #sm[county text in Finnish and English; a sentence citing an unknown id or a number not in the records is rejected]], stroke: 0.9pt + c-ai)
  arrow((42, 36), (47, 36), (47, 15), (52, 15))
  arrow((70, 34), (70, 24))
  blk((70, 15), 36, 18, [#hd("Demo", ink)\ #sm[map, pathway lights, county card, replay; also shows I and J]])

  // ---------------- I policy
  dot((124, 67)); arrow((124, 67), (124, 55), c: c-m4, w: 0.9pt)
  blk((124, 42), 48, 26, [#hd("Model 4", c-m4) #sm[· challenger]\ decides *every month* from Model 1: counties with status gap, ranked by #num("P × excess")\ #sm[data ≈ 45 days old · 3 slots · a slot runs ≥ 6 months]], stroke: 1.1pt + c-m4, fill: c-m4.lighten(93%))
  content((99, 26), anchor: "west", text(6pt, fill: c-m3)[from B: raw yearly values, two years old])
  blk((124, 13), 48, 20, [#hd("Model 3", c-m3) #sm[· the strategy's own monitoring]\ decides *once a year* (31 Jan) from raw yearly values two years old\ #sm[top 3 above national + δ · 12-month slots]], stroke: 1.1pt + c-m3, fill: c-m3.lighten(93%))
  arrow((148, 42), (152, 42), (152, 32), (157, 32), c: c-m4, w: 0.9pt)
  arrow((148, 13), (152, 13), (152, 24), (157, 24), c: c-m3, w: 0.9pt)
  blk((176, 28), 38, 24, [#hd("Pilot slots", ink)\ the same lever for both: a fast-track pathway pilot #sm[(roadmap 2.5.2 / 3.1.2)]\ #sm[budget: 3 slots at a time per ★ signal]])

  // ---------------- J scoring
  blk((222, 42), 28, 24, [#hd("Hindsight truth", mut)\ #sm[the need: when was the county really worse than national + δ? Uses all data, both directions]], stroke: (paint: mut, thickness: 0.8pt, dash: "dashed"))
  arrow((236, 40), (241, 40))
  arrow((195, 28), (241, 28))
  blk((257, 24), 32, 40, [#hd("Scorecard", ink)\ #sm[*coverage* = need-months with a slot ÷ need-months]\ #sm[*precision* = slot-months on need ÷ slot-months]\ #v(0.6mm) #sm[Model 4 vs Model 3: referral 51% vs 20%; endoscopy 38 vs 34; oncology 60 vs 56]], stroke: 1.1pt + ink)
}))

#v(1mm)
#text(7pt, fill: mut)[
  #box(width: 6mm, line(length: 6mm, stroke: 0.7pt + ink)) data flow #h(4mm)
  #box(width: 6mm, line(length: 6mm, stroke: 1.5pt + ink)) bus: one line carrying many signals or records #h(4mm)
  #box(width: 6mm, line(length: 6mm, stroke: (paint: mut, dash: "dashed"))) bypass or after the fact #h(4mm)
  #text(font: "DejaVu Sans")[⌒] wires cross without connecting #h(4mm)
  ★ signal that Models 3 and 4 act on #h(4mm)
  #tag("proxy", mut) not cancer-specific
]

// ============================================================ PAGE 2: the sections, explained
#pagebreak()
#title("What each section does",
  [In plain words, with the settings and their origin (`strategy`, `roadmap`, `literature`, `model` = our choice, `qc` = a data-quality rule), and what to watch out for. Code paths are relative to the repository.])

#let row(letter, name, what, code, settings, watch) = (
  [#sec(letter) #h(1mm) #text(weight: "bold", name)],
  [#what #linebreak() #text(6.3pt, fill: mut, font: "IBM Plex Mono", code)],
  settings,
  watch,
)
#set table(stroke: (x, y) => (bottom: 0.4pt + line-c))
#table(columns: (24mm, 1fr, 68mm, 84mm), inset: (x: 3pt, y: 3.6pt), align: left + top,
  table.header(..([*Section*], [*What it does*], [*Settings (origin)*], [*Watch out for*]).map(x => text(7pt, x))),
  ..row("A", "Inputs",
    [Public, aggregate numbers only: THL specialist-care queues by specialty (S01) and procedure queues including endoscopy (S02), per provider; screening participation per county (S03–S05).],
    "scripts/fetch_thl.py · parse_thl.py · build_signals.py",
    [Fetched 14 Nov 2026. THL: three snapshots a year to 2020, monthly from 2021. Sotkanet: yearly.],
    [Queues are counted where the patient waits (the provider), not where they live. For treatment queues, THL's own-residents version moves the > 90-day share by under 1.3 points in every county but one. No age or sex split, so no need adjustment. Before 2023, hospital districts are mapped onto counties.]),
  ..row("B", "Clock",
    [Keeps the replay honest: at each replay month, only numbers already published by then can be used.],
    "scripts/run_replay.py",
    [THL: 45 days after the reference date (cube update dates). Yearly figures for year Y: from 31 Dec Y+1. (DECISIONS #8)],
    [If real publication was slower, the twin looks faster than it could have been.]),
  ..row("C", "Signals",
    [Turns raw counts into 11 measures, each tied to a pathway step: detection 3, referral 2 plus referral volume, diagnosis 1, treatment 3, and a negative control. ★ marks the three that Models 3 and 4 act on.],
    "twin/signals.json · build_signals.py",
    [Definitions, thresholds and minimum sizes per signal in twin/signals.json.],
    [Only screening and oncology (specialty 65) are cancer-specific. Oncology referrals range from 0.8 to 12.8 per 1,000 residents between providers, which points to coding rather than need. That denominator drives the Goal 3 proxy (DECISIONS.md, decision 1).]),
  ..row("D", "Estimator",
    [The twin itself. For every signal in every county, a small model keeps a running estimate of the true level and how sure it is, and updates it as each number is published. Small counties get wide intervals automatically.],
    "twin/core.py · run_replay.py",
    [Local-level Kalman filter, logit scale for shares, log for ratios; noise from the counts × overdispersion φ; monthly drift q. q and φ are chosen at each replay month from past data only (`model`, DECISIONS #9–10).],
    [Beats a straight-line trend on 10 of 10 signals but last-value persistence on only 5 of 10 (pass mark P1 failed). q sits at its bound for the oncology index: treat it as unestimated.]),
  ..row("E", "Judge",
    [Two questions per record. Is the county worse than the national level by more than δ, and how likely is that (P(gap))? Is there enough data to judge at all?],
    "scripts/run_replay.py",
    [δ: +10 pts for queue shares; +5 pts for oncology > 90 d and referrals > 21 d; ×1.5 for the oncology index; −5 pts for screening (`model`). Enough data: 80% interval under 25 pts (×2.5 for ratios), data under 6 months old, ≥ 20 patients (`qc`, DECISIONS #11).],
    [The national level is not a target: HUS holds about half of the national oncology queue. Legal limits (3 weeks, 3 months, 6 months) and the 80% screening target are not used here.]),
  ..row("F", "Status",
    [One word per signal, county and month.],
    "records.csv: status",
    [gap: P ≥ 0.9 · watch: 0.7–0.9 · ok: below · cannot judge: not enough data · stale: nothing new for 6 months (`model`).],
    ["Gap" means worse than national by more than δ. It is not a verdict that care is unhealthy.]),
  ..row("G", "Records",
    [Model 1, the equality twin: all county records. Model 2, the pathway twin: the national rows, with an alarm when a new value is at least 3 standard errors from its forecast.],
    "runs/model1/replay · runs/model2/replay",
    [One row per month × signal × county: level, 80% interval, P(gap), status, data-through date.],
    [Positive control failed: the 2020 pandemic dip was not flagged (z = −0.76). Negative control (population) passed.]),
  ..row("H", "Display",
    [The step combiner gives each pathway step the worst status among its signals, for the map and pathway lights. The AI briefing writes each county's text in Finnish and English from the records; a sentence that cites an unknown id or a number not in the records is rejected.],
    "demo/template.html · scripts/gen_briefings.py",
    [Worst-of rule. Green is blocked only where a step has a cancer-specific signal.],
    [Referral and diagnosis can show green on proxies alone; decision 12 says they should not. Treatment can show red on the surgery queue alone (239 of 602 red county-months).]),
  ..row("I", "Policy",
    [Two ways to place the same lever with the same budget. Model 3, the strategy's own monitoring: once a year (31 Jan) from raw yearly values two years old. Model 4, the challenger: every month from Model 1's gap records.],
    "scripts/run_policy.py",
    [Lever: county fast-track pilot (roadmap 2.5.2 / 3.1.2). 3 slots at a time per ★ signal (`model`; also run with 2 and 5). Model 3 slots last 12 months; Model 4 slots at least 6.],
    [A counterfactual on history, not a forecast. No effect size is simulated: the comparison is only about where and when the slots sit.]),
  ..row("J", "Scoring",
    [After the fact, the estimator is re-run on all data in both directions to mark the months when a county really was worse than national + δ: the need. Each model is scored on how much of that need its slots covered.],
    "scripts/run_policy.py · SCORECARD.md",
    [Coverage = need-months with a slot ÷ need-months. Precision = slot-months on need ÷ slot-months. Pass marks written before the runs.],
    [Need is judged against national + δ, not against need-adjusted or legal targets. Referral: Model 4 51% vs Model 3 20% (+32 pts). Endoscopy 38 vs 34 and oncology 60 vs 56 are ties.]),
)

// ============================================================ PAGE 3: one channel, with real numbers
#pagebreak()
#let E = D.example
#title("One record, traced through the circuit",
  [North Ostrobothnia, endoscopy queue (#num("dx_endo_over90")), replay month #num(E.t). Every value on the wires comes from the Model 1 record. Letters match the sections on page 1.])

#let wtxt(t) = text(6.8pt, fill: mut, t)
#let vtxt(t) = text(7.5pt, font: "IBM Plex Mono", weight: "bold", t)
#align(center, cetz.canvas(length: 1mm, {
  import cetz.draw: *
  let lt(p, l) = content(p, box(fill: ink, radius: 1.2pt, inset: (x: 1.8pt, y: 1.2pt), text(6pt, fill: white, weight: "bold", l)))
  let bx(pos, w, h, body, stroke: 0.7pt + ink, fill: white, l: none) = {
    rect((pos.at(0) - w / 2, pos.at(1) - h / 2), (pos.at(0) + w / 2, pos.at(1) + h / 2), stroke: stroke, fill: fill, radius: 1.5)
    content(pos, box(width: (w - 3) * 1mm, align(center, body)))
    if l != none { lt((pos.at(0) - w / 2 + 2.4, pos.at(1) + h / 2 + 2.2), l) }
  }
  let wire(..pts, c: ink, w: 0.8pt, dash: none) = line(..pts, stroke: (paint: c, thickness: w, dash: dash), mark: (end: "stealth", fill: c, scale: 0.6))
  let comparator(p) = {
    let (x, y) = p
    line((x, y - 9), (x, y + 9), (x + 15, y), close: true, stroke: 0.9pt + ink, fill: white)
    content((x + 2.5, y + 4.5), text(9pt)[+])
    content((x + 2.5, y - 4.5), text(9pt)[−])
    content((x + 6.5, y), text(6.5pt)[P(·>·)])
  }
  let andg(p, h: 16) = {
    let (x, y) = p
    merge-path(close: true, stroke: 0.9pt + ink, fill: white, {
      line((x + 7, y + h / 2), (x, y + h / 2), (x, y - h / 2), (x + 7, y - h / 2))
      arc((x + 7, y - h / 2), start: -90deg, stop: 90deg, radius: h / 2)
    })
    content((x + 7, y), text(9pt)[#sym.and])
  }
  let maxg(p, h: 16) = {
    let (x, y) = p
    merge-path(close: true, stroke: 0.9pt + step-c.diagnosis, fill: step-c.diagnosis.lighten(90%), {
      bezier((x, y + h / 2), (x + 17, y), (x + 10, y + h / 2))
      bezier((x + 17, y), (x, y - h / 2), (x + 10, y - h / 2))
      bezier((x, y - h / 2), (x, y + h / 2), (x + 4.5, y))
    })
    content((x + 8, y), text(6.5pt, weight: "bold")[MAX])
  }

  bx((14, 62), 26, 18, [*S02, THL*\ #vtxt[50 of 175]\ #wtxt[waiting > 90 days\ data through #E.data_through]], fill: bg, l: "A·C")
  wire((27, 62), (35, 62))
  bx((49, 62), 26, 18, [*Publication gate*\ #wtxt[snapshot 30.4. + 45 d\ usable from mid-June]\ #vtxt[≤ #E.t] #ck], stroke: 0.9pt + c-gap, fill: c-gap.lighten(92%), l: "B")
  wire((62, 62), (70, 62))
  bx((86, 62), 30, 18, [*Transform*\ #vtxt[logit(50.5/176)]\ #wtxt[noise from counts:\ 1/50.5 + 1/125.5, × φ = #E.phi]], l: "D")
  wire((101, 62), (109, 62))
  bx((128, 62), 36, 18, [*Kalman update*\ #wtxt[prior = last level, drift q = #E.q]\ #vtxt[level #pct(E.level)]\ #wtxt[80%: #pct(E.lo) – #pct(E.hi)]], stroke: 1pt + ink, l: "D")
  wire((146, 62), (158, 62), (158, 56.5), (166, 56.5))
  comparator((166, 52))
  lt((168.5, 63), "E")
  bx((128, 38), 36, 16, [*National channel*\ #wtxt[same estimator, county = FI]\ #vtxt[#pct(E.ref) + δ 10 pt = #pct(E.thr)]], fill: bg, l: "D")
  content((128, 27.5), wtxt[δ origin: `model` (ours, not an official target)])
  wire((146, 38), (158, 38), (158, 47.5), (166, 47.5))
  wire((181, 52), (198, 52))
  content((189.5, 55.5), vtxt[P = #E.p_gap])
  bx((211, 52), 26, 14, [*Threshold*\ #wtxt[≥ 0.9 gap · ≥ 0.7 watch]\ #vtxt[→ gap]], l: "F")
  wire((224, 52), (232, 52), (232, 47), (238, 47))

  let w80 = calc.round((E.hi - E.lo) * 100, digits: 1)
  bx((49, 20), 34, 9, [#wtxt[80% width] #vtxt[#w80 pt ≤ 25] #ck], l: "E")
  bx((88, 20), 30, 9, [#wtxt[data age] #vtxt[2 mo ≤ 6] #ck], l: "E")
  bx((128, 14), 30, 9, [#wtxt[queue size] #vtxt[175 ≥ 20] #ck], l: "E")
  wire((66, 20), (68, 20), (68, 9), (182, 9), (182, 32.5), (190, 32.5))
  wire((103, 20), (105, 20), (105, 25), (184, 25), (184, 36), (190, 36))
  wire((143, 14), (186, 14), (186, 39.5), (190, 39.5))
  andg((190, 36), h: 12)
  content((197, 27.5), wtxt[identifiable])
  wire((203, 36), (232, 36), (232, 41), (238, 41))
  andg((238, 44), h: 14)
  wire((252, 44), (258, 44))
  rect((258, 38), (277, 50), fill: c-gap, stroke: none, radius: 1.5)
  content((267.5, 44), text(white, weight: "bold")[GAP])
  lt((260.4, 52.2), "F")
  content((267.5, 35), wtxt[record status])

  wire((267.5, 32), (267.5, 27), (228, 27), (228, 17), (234, 17))
  wire((214, 9), (234, 9), dash: "dashed", c: mut)
  content((207, 12.5), wtxt[other diagnosis signals: none])
  maxg((234, 13))
  lt((236, 22.5), "H")
  wire((251, 13), (258, 13))
  rect((258, 7), (277, 19), fill: c-gap.lighten(15%), stroke: 1pt + step-c.diagnosis, radius: 1.5)
  content((267.5, 13), text(white, weight: "bold", size: 7pt)[DIAGNOSIS\ step: gap])
}))

#v(4mm)
#grid(columns: (1fr, 1fr), column-gutter: 8mm,
  box(stroke: 0.6pt + c-m4, inset: 6pt, radius: 3pt, width: 100%)[
    #text(fill: c-m4, weight: "bold")[What Model 4 did with this record (section I)]\
    Its score was #num("P × excess ÷ threshold") ≈ #num(str(calc.round(E.p_gap * (E.level - E.thr) / E.thr, digits: 2))), but all three endoscopy slots were taken (Central Ostrobothnia, Päijät-Häme, Central Finland), so it waited. It started in August 2021 on data through May (49 of 124 over 90 days). By then the June data was out: 3 of 77 (3.9%), and the gap was gone. The slot still ran its 6-month minimum.],
  box(stroke: 0.6pt + c-m3, inset: 6pt, radius: 3pt, width: 100%)[
    #text(fill: c-m3, weight: "bold")[What Model 3 did with the same county (section I)]\
    It never sees this record. On 31 January 2021 it read the *2019* yearly value (44.1% against national 15.3%) and gave the county a 12-month slot. It was right, but only because a two-year-old gap happened still to be open.],
)
#v(4mm)
#text(weight: "bold")[How to read the gates]
#v(0.5mm)
#let gate(sym-body, name, t) = box(width: 100%, stroke: 0.4pt + line-c, radius: 2pt, inset: 5pt)[#sym-body #h(1mm) #text(weight: "bold", name)\ #text(7pt, t)]
#grid(columns: (1fr,) * 5, column-gutter: 3mm,
  gate(text(9pt)[▷], [Comparator · E], [Is the county above national + δ? It answers with a probability, P(gap), because both levels are estimates with an interval.]),
  gate(text(8pt, font: "IBM Plex Mono")[≥0.9], [Threshold · F], [Turns the probability into a word: gap at 0.9 or more, watch from 0.7, otherwise ok.]),
  gate(text(9pt)[#sym.and], [Data checks · E], [All three must pass: a narrow enough interval, data under 6 months old, at least 20 patients. If any fails: cannot judge.]),
  gate(text(9pt)[#sym.and], [Status · F], [The word from the threshold only goes out if the data checks pass. That is why a county with too few patients shows grey, never green.]),
  gate(text(7pt, weight: "bold")[MAX], [Step combiner · H], [The pathway step shows the worst of its signals. Diagnosis has only this one, so it shows gap.]),
)
#v(3mm)
#text(7.5pt, fill: mut)[The next page follows this channel through the whole replay: when action was actually needed, what each model could see at the time, and where its slots landed.]

// ============================================================ PAGE 4: need against the models, whole replay
#pagebreak()
#let CH = D.channel
#title([One channel over the whole replay: when was action needed, and what did each model do?],
  [#CH.name, endoscopy queue: share waiting over 90 days (#num(CH.signal)), not cancer-specific. One time axis for all three panels.])

#let yrs = range(2016, 2027)
#align(center, cetz.canvas(length: 1mm, {
  import cetz.draw: *
  let X0 = 31.0
  let W = 243.0
  let N = 130
  let px(k) = X0 + k * W / N
  let pe(k) = px(k + 1)
  let A0 = 94.0
  let AH = 42.0
  let B0 = 51.0
  let BH = 37.0
  let ymax = 0.7
  let ya(v) = A0 + calc.min(calc.max(v, 0), ymax) / ymax * AH
  let yb(v) = B0 + calc.min(calc.max(v, 0), ymax) / ymax * BH
  let lab(p, t, a: "west", c: ink, s: 6pt) = content(p, anchor: a, text(s, fill: c, t))
  let kp = CH.k_policy0

  // scored window and year grid
  rect((px(kp), B0), (px(N), A0 + AH), fill: rgb("#eef2f7"), stroke: none)
  for y in yrs {
    let k = (y - 2016) * 12
    line((px(k), 3.5), (px(k), A0 + AH), stroke: 0.3pt + rgb("#d3d8de"))
    content((px(k) + 0.6, 1.6), anchor: "west", text(6pt, fill: mut, str(y)))
  }
  lab((px(kp) + 1, A0 + AH - 2), [scored window (Models 3 and 4)], c: mut)

  // ----- panel 1: what happened (hindsight)
  rect((X0, A0), (X0 + W, A0 + AH), stroke: 0.4pt + rgb("#c5cbd3"))
  for v in (0.1, 0.2, 0.3, 0.4, 0.5, 0.6) {
    line((X0, ya(v)), (X0 + W, ya(v)), stroke: 0.25pt + rgb("#e3e7ec"))
    lab((X0 + 0.6, ya(v) + 1), str(int(v * 100)) + "%", c: mut, s: 5.5pt)
  }
  content((X0 - 1.5, A0 + AH), anchor: "north-east", box(width: 28mm, align(right)[#text(7.5pt, weight: "bold")[1 · What happened]\ #text(6.2pt, fill: mut)[looking back with all data (the estimator run in both directions)]]))
  for r in CH.need_runs {
    if r.len() >= 2 {
      line(..r.map(p => (pe(p.at(0)), ya(p.at(1)))), ..r.rev().map(p => (pe(p.at(0)), ya(p.at(2)))), close: true, fill: c-gap.lighten(62%), stroke: none)
    } else {
      let p = r.at(0)
      rect((pe(p.at(0)) - 0.7, ya(p.at(2))), (pe(p.at(0)) + 0.7, ya(p.at(1))), fill: c-gap.lighten(62%), stroke: none)
    }
  }
  line(..CH.nat_line.map(p => (pe(p.at(0)), ya(p.at(1)))), stroke: 0.9pt + rgb("#8a94a3"))
  line(..CH.nat_line.map(p => (pe(p.at(0)), ya(p.at(2)))), stroke: (paint: c-gap, thickness: 0.7pt, dash: "dashed"))
  line(..CH.hind.map(h => (pe(h.k), ya(h.level))), stroke: 1.1pt + ink)
  for h in CH.hind {
    let r = 0.3 + 0.075 * calc.sqrt(h.den)
    if h.den >= CH.min_den { circle((pe(h.k), ya(h.share)), radius: r, fill: ink.lighten(25%), stroke: 0.3pt + white) }
    else { circle((pe(h.k), ya(h.share)), radius: r, fill: white, stroke: 0.5pt + ink) }
  }
  lab((px(24), ya(0.655)), [Dec 2017 – May 2021: above national + 10 pts for 3½ years], c: c-gap.darken(20%))
  line((px(66), ya(0.06)), (px(67.5), ya(0.44)), stroke: 0.4pt + mut)
  content((px(67.8), ya(0.535)), anchor: "north-west", box(width: 40mm, text(6pt, fill: mut)[Jun 2021: 124 → 77 patients, 40% → 4%. Queue cleared, or a reporting change?]))
  line((px(92.6), ya(0.6)), (px(97.5), ya(0.625)), stroke: 0.4pt + mut)
  content((px(97.8), ya(0.675)), anchor: "north-west", box(width: 58mm, text(6pt, fill: mut)[2023: the county reform restarts the series with 10–19 patients (hollow dots): too few to judge]))

  // ----- panel 2: what each model could see at the time
  rect((X0, B0), (X0 + W, B0 + BH), stroke: 0.4pt + rgb("#c5cbd3"))
  for v in (0.1, 0.2, 0.3, 0.4, 0.5, 0.6) {
    line((X0, yb(v)), (X0 + W, yb(v)), stroke: 0.25pt + rgb("#e3e7ec"))
    lab((X0 + 0.6, yb(v) + 1), str(int(v * 100)) + "%", c: mut, s: 5.5pt)
  }
  content((X0 - 1.5, B0 + BH), anchor: "north-east", box(width: 28mm, align(right)[#text(7.5pt, weight: "bold")[2 · What each model could see]\ #text(6.2pt, fill: mut)[at the time, with its delay]]))
  let rt = CH.rt.filter(r => r.level != none)
  line(..rt.map(r => (pe(r.k), yb(r.hi))), ..rt.rev().map(r => (pe(r.k), yb(r.lo))), close: true, fill: c-m4.lighten(78%), stroke: none)
  line(..rt.filter(r => r.thr != none).map(r => (pe(r.k), yb(r.thr))), stroke: (paint: c-gap, thickness: 0.5pt, dash: "dashed"))
  line(..rt.map(r => (pe(r.k), yb(r.level))), stroke: 1pt + c-m4)
  for v in CH.m3view {
    let c = if v.eligible { c-m3 } else { c-unid }
    line((pe(v.k_from), yb(v.val)), (pe(v.k_to), yb(v.val)), stroke: (paint: c, thickness: 1.6pt, dash: if v.eligible { none } else { "dotted" }))
    line((pe(v.k_from), yb(v.thr)), (pe(v.k_to), yb(v.thr)), stroke: (paint: c-m3, thickness: 0.6pt, dash: "dashed"))
    line((pe(v.k_from) - 0.9, yb(v.val)), (pe(v.k_from), yb(v.val) + 0.9), (pe(v.k_from) + 0.9, yb(v.val)), (pe(v.k_from), yb(v.val) - 0.9), close: true, fill: c, stroke: none)
    lab((pe(v.k_from) + 1.2, yb(v.val) + 1.6), if v.eligible [uses #v.data_year] else [uses #v.data_year: too few patients], c: if v.eligible { c-m3.darken(10%) } else { mut }, s: 5.6pt)
  }
  let v21 = CH.m3view.at(0)
  line((pe(42), ya(v21.val)), (pe(v21.k_from) - 1.2, yb(v21.val) + 1.2), stroke: (paint: c-m3, thickness: 0.6pt, dash: "dashed"), mark: (end: "stealth", fill: c-m3, scale: 0.5))
  lab((px(57.5), A0 - 3), [in 2021, Model 3 acts on 2019's number], c: c-m3.darken(10%))
  let card = CH.rt.find(r => r.k == 65)
  circle((pe(65), yb(card.level)), radius: 1.1, stroke: 0.8pt + c-gap, fill: none)
  line((pe(65) - 0.8, yb(card.level) - 0.8), (pe(62), yb(0.1)), stroke: 0.4pt + c-gap)
  lab((pe(62) - 0.4, yb(0.08)), [the card you pasted (30 Jun 2021): #pct0(card.level)], a: "east", c: c-gap.darken(10%))
  lab((X0 + 1.5, B0 + BH - 2.5), [#text(fill: c-m4, weight: "bold")[blue]: the twin's estimate and 80% interval as known each month, about 45 days late. Model 4 acts on this. #text(fill: c-m3, weight: "bold")[purple]: Model 3's yearly number, two years old.], c: mut)

  // ----- panel 3: lanes
  content((X0 - 1.5, 49.5), anchor: "north-east", box(width: 28mm, align(right)[#text(7.5pt, weight: "bold")[3 · Need and actions]\ #text(6.2pt, fill: mut)[month by month]]))
  let lane(y, h, label, f, k0, n) = {
    lab((X0 - 1.5, y + h / 2), label, a: "east", s: 6.2pt)
    for i in range(n) {
      let c = f(i)
      if c != none { rect((px(k0 + i), y), (px(k0 + i + 1), y + h), fill: c, stroke: 0.15pt + white) }
    }
  }
  let pre(k) = CH.need_runs.any(r => r.at(0).at(0) <= k and k <= r.at(-1).at(0))
  lane(37.5, 4, [Need (hindsight)], i => if pre(i) { c-gap.lighten(55%) } else { rgb("#eef0f3") }, 0, kp)
  lane(37.5, 4, [Need (hindsight)], i => if CH.truth.at(i) == 1 { c-gap } else { c-none }, kp, CH.truth.len())
  lane(31.5, 4, [Model 1 status, as known], i => none, 0, 0)
  for r in CH.rt { rect((px(r.k), 31.5), (px(r.k + 1), 35.5), fill: st-col.at(r.status), stroke: 0.15pt + white) }
  let slotlane(y, act, c, label) = lane(y, 4, label, i => if act.at(i) == 1 { if CH.truth.at(i) == 1 { c } else { c.lighten(62%) } } else { none }, kp, act.len())
  let uselane(y, use, c, label) = {
    lab((X0 - 1.5, y + 1.6), label, a: "east", s: 6.2pt)
    for (i, u) in use.enumerate() {
      if u > 0 { rect((px(kp + i), y), (px(kp + i + 1), y + 3.2 * u / 3), fill: if u == 3 { c } else { c.lighten(55%) }, stroke: 0.15pt + white) }
    }
    line((px(kp), y + 3.2), (px(N), y + 3.2), stroke: (paint: mut, thickness: 0.25pt, dash: "dotted"))
  }
  slotlane(23, CH.m4, c-m4, [Model 4: slot here])
  uselane(18, CH.use4, c-m4, [Model 4: slots in use, of 3])
  slotlane(11, CH.m3, c-m3, [Model 3: slot here])
  uselane(6, CH.use3, c-m3, [Model 3: slots in use, of 3])
  for s in CH.slots4 {
    let x = pe(s.k_decided)
    line((x - 0.9, 29.4), (x + 0.9, 29.4), (x, 27.8), close: true, fill: c-m4, stroke: none)
  }
  lab((pe(CH.slots4.at(0).k_decided) + 1.2, 28.8), [decided 31 Jul 2021 on data through May], c: c-m4, s: 5.5pt)
  lab((pe(CH.slots4.at(1).k_decided) - 1.2, 28.8), [decided 31 Dec 2025], a: "east", c: c-m4, s: 5.5pt)
  for s in CH.slots3 {
    let x = pe(s.k_decided)
    line((x - 0.9, 17.4), (x + 0.9, 17.4), (x, 15.8), close: true, fill: c-m3, stroke: none)
  }
  lab((pe(CH.slots3.at(0).k_decided) - 1.2, 16.8), [31 Jan 2021, on 2019], a: "east", c: c-m3, s: 5.5pt)
  lab((pe(CH.slots3.at(1).k_decided) + 1.2, 16.8), [31 Jan 2022, on 2020 (the gap was already gone)], c: c-m3, s: 5.5pt)
  lab((pe(CH.slots3.at(2).k_decided) - 1.2, 16.8), [31 Jan 2026, on 2024], a: "east", c: c-m3, s: 5.5pt)
}))

#v(0.5mm)
#text(6.8pt, fill: mut)[
  #box(width: 2.4mm, height: 2.4mm, radius: 1.2mm, fill: ink.lighten(25%), baseline: 0.3mm) published value (size = patients; hollow = under 20) #h(2mm)
  #box(width: 5mm, line(length: 5mm, stroke: 1.1pt + ink)) county, hindsight #h(2mm)
  #box(width: 5mm, line(length: 5mm, stroke: 0.9pt + rgb("#8a94a3"))) national #h(2mm)
  #box(width: 5mm, line(length: 5mm, stroke: (paint: c-gap, dash: "dashed"))) national + 10 pts #h(2mm)
  #box(width: 2.4mm, height: 2.4mm, fill: c-gap, baseline: 0.3mm)#box(width: 2.4mm, height: 2.4mm, fill: c-gap.lighten(55%), baseline: 0.3mm) need: scored / before 2021 #h(2mm)
  #box(width: 2.4mm, height: 2.4mm, fill: c-m4, baseline: 0.3mm)#box(width: 2.4mm, height: 2.4mm, fill: c-m4.lighten(62%), baseline: 0.3mm) slot on need / wasted #h(2mm)
  #text(fill: c-m4)[▼] decision #h(2mm)
  #for k in ("g", "w", "o", "u") [#box(width: 2.4mm, height: 2.4mm, fill: st-col.at(k), baseline: 0.3mm) #st-name.at(k) #h(1.2mm)]
]
#v(1.2mm)
#grid(columns: (1fr, 1fr, 1fr, 1.45fr), column-gutter: 5mm,
  [#text(fill: c-gap, weight: "bold")[Need] #text(7pt)[Months when, looking back with all data, the county was more than 10 points above the national level with at least 20 patients waiting. This is need against the national level. It is not adjusted for age (no such data) and is not a legal limit.]],
  [#text(fill: c-m4, weight: "bold")[Model 4] #text(7pt)[Sees the twin's monthly estimate about 45 days late (blue, panel 2). It acts the month after a gap status, if one of its 3 slots is free, and a slot runs at least 6 months.]],
  [#text(fill: c-m3, weight: "bold")[Model 3] #text(7pt)[Sees one yearly number per county, two years old (purple steps). Every 31 January it gives its 3 slots to the counties furthest above national + 10 pts, for 12 months.]],
  [#text(weight: "bold")[What this county shows] #text(7pt)[*2021:* Model 3 covered Feb–May on 2019's number. Model 4 saw the gap but ranked behind Central Finland and Ostrobothnia for the one free slot, and started in August, after the queue collapsed. *2024:* both missed. The queue was too small to judge until April, Model 4's slots were full all year, and Model 3 was looking at 2022 (13%). *2025–26:* the twin flagged in December; Model 4 started in January, Model 3 in February. Of #CH.need_months need-months, Model 3 covered #CH.m3_hit and Model 4 #CH.m4_hit. Across all counties: #pct0(CH.all_cov.m4) vs #pct0(CH.all_cov.m3), a tie.]],
)

// ============================================================ PAGE 5: how signals accumulate
#pagebreak()
#title("How signals add up, and where they do not",
  [Signals are combined by taking the *worst*, not by adding them (section H). Right: how many counties each pathway step shows in each state, month by month through the replay, using the same rule as the demo map.])

#grid(columns: (80mm, 1fr), column-gutter: 7mm,
[
  #text(weight: "bold")[The step combiner, as a truth table]
  #v(0.5mm)
  #table(columns: (43mm, 1fr), stroke: 0.4pt + line-c, inset: 3.5pt,
    table.header([*signals at the step*], [*the step shows*]),
    [any one #chip("gap", c-gap)], [gap],
    [two #chip("watch", c-watch, fg: ink)], [watch. Two watches do *not* make a gap],
    [watch + cannot judge], [watch],
    [all #chip("ok", c-ok), one is cancer-specific], [ok],
    [ok on #ncs signals; the step's cancer-specific signal cannot be judged], [*cannot be judged*],
    [referral or diagnosis, all ok. These steps have no cancer-specific signal], [*ok: green on proxies alone.* Decision 12 in DECISIONS.md says this should not happen],
    [all cannot be judged or stale], [cannot be judged / stale],
  )
  #text(fill: mut, size: 7pt)[Order: gap > watch > ok > cannot be judged > stale > no data.]

  #v(2.5mm)
  #text(weight: "bold")[What accumulates today]
  #set list(spacing: 0.7em)
  - *Evidence over time, inside one channel.* The Kalman filter carries everything published so far, and the interval narrows as data arrives. This is the only true accumulation in the system.
  - *Across signals at one step:* the worst one wins (OR-like). Nothing is added up.
  - *Across steps:* "any step" on the map is the worst step. A referral delay is *not* carried into diagnosis or treatment.
  - *Policy:* three separate channels, each with its own 3 slots. A county with gaps at two steps can hold two slots, and nothing links them.

  #v(2mm)
  #box(stroke: (paint: c-ai, dash: "dashed"), inset: 5pt, radius: 3pt)[
    #text(fill: c-ai, weight: "bold")[Not built: a serial pathway]\
    A patient's total delay is the *sum* of the waits at each step. A real cumulative signal would add a county's referral, endoscopy and treatment waits in series. Public data does not support that today, because only oncology is cancer-specific and each step counts different patients. It needs the county's own pathway data.]
],
[
  #let months = D.replay_months
  #let n = months.len()
  #let bw = 1.43mm
  #let H = 26mm
  #let order = ("g", "w", "o", "u", "s", "x")
  #for step in ("detection", "referral", "diagnosis", "treatment") {
    let S = D.steps.at(step)
    let U = S.units
    let bar(i) = box(width: bw, height: H, align(bottom, stack(dir: btt, ..order.map(k => {
      let v = S.counts.at(k).at(i)
      if v > 0 { box(width: bw - 0.22mm, height: H * v / U, fill: st-col.at(k), stroke: none) }
    }).filter(x => x != none))))
    block(below: 4.5mm, above: 0mm)[
      #text(weight: "bold", fill: step-c.at(step), upper(step)) #h(2mm) #text(fill: mut, size: 7pt)[#U units · #D.signals.pairs().filter(p => p.at(1).step == step).len() signals]
      #v(-1.5mm)
      #box(stack(dir: ltr, ..range(n).map(bar)))
      #v(-2.2mm)
      #box(width: n * bw, height: 2.5mm, {
        for (i, m) in months.enumerate() {
          if m.slice(5, 7) == "01" { place(dx: i * bw, text(6pt, fill: mut, m.slice(0, 4))) }
        }
      })
    ]
  }
  #for k in ("g", "w", "o", "u", "s", "x") [#box(width: 3mm, height: 2.5mm, fill: st-col.at(k), stroke: 0.3pt + line-c, baseline: 0.4mm) #st-name.at(k) #h(3mm)]
  #v(0.5mm)
  #text(fill: mut, size: 7pt)[Each bar is one replay month, with all counties stacked. Treatment shows the most red, but 239 of its 602 red county-months are red only because of the GI-surgery + urology queue, which is not cancer-specific. Most grey is in treatment before 2021 (small oncology queues): about 11 counties a month in 2016–19, 6–7 in 2024–26. Diagnosis has no data before mid-2016.]
])

// ============================================================ PAGES 6–8: timing diagrams
#let sig-title = (
  ref_assess_over90: ("Referral handover", "Waiting for first specialist assessment > 90 days, five cancer-diagnosing specialties", step-c.referral),
  dx_endo_over90: ("Diagnosis", "Endoscopy queue: share waiting > 90 days", step-c.diagnosis),
  treat_onc_wait: ("Treatment start, the Goal 3 proxy", "Oncology treatment queue in days of referral inflow", step-c.treatment),
)
#let cw = 3.18mm
#let lh = 2.15mm
#for sig in ("ref_assess_over90", "dx_endo_over90", "treat_onc_wait") {
  pagebreak()
  let T = D.timing.at(sig)
  let (name, lab, col) = sig-title.at(sig)
  let s3 = T.summary.model3
  let s4 = T.summary.model4
  let df = T.diff.model4_minus_model3_coverage
  title([Logic-analyser view: #text(fill: col, name)],
    [#lab (#num(sig)), policy window 2021-01 to 2026-10, all counties (sections I and J). Coverage is the AND of two wires: *slot active* #sym.and *need*. Model 4 covers #num(pct0(s4.coverage)) and Model 3 #num(pct0(s3.coverage)) of #s3.true_gap_months need-months, a difference of #num(str(calc.round(df.point * 100)) + " pt") (80% interval #num(str(calc.round(df.lo80 * 100)) + " to " + str(calc.round(df.hi80 * 100)))): #if df.lo80 > 0 [*Model 4 wins*] else [*a tie*]. Precision: Model 4 #num(pct0(s4.precision)), Model 3 #num(pct0(s3.precision)).])
  let pm = T.rows.at(0).truth.len()
  let lane(vals, f) = box(stack(dir: ltr, ..vals.enumerate().map(((i, v)) => box(width: cw, height: lh, fill: f(i, v), stroke: (left: if calc.rem(i, 12) == 0 { 0.4pt + mut } else { none })))))
  grid(columns: (52mm, auto), column-gutter: 1mm,
    [], box(width: pm * cw, height: 3mm, { for y in range(0, pm, step: 12) { place(dx: y * cw + 0.5mm, text(6.5pt, fill: mut, str(2021 + int(y / 12)))) } }))
  for r in T.rows {
    let truth = r.truth
    block(below: 1.1mm, grid(columns: (52mm, auto), column-gutter: 1mm, align: horizon,
      [#text(weight: "bold", size: 7pt, r.name) \ #text(size: 6.3pt, fill: mut)[#r.gap_months need-mo · M3 hit #r.m3_hit · M4 hit #r.m4_hit]],
      stack(dir: ttb, spacing: 0.35mm,
        lane(r.m1.clusters(), (i, v) => st-col.at(v)),
        lane(truth, (i, v) => if v == 1 { ink } else { c-none }),
        lane(r.m3, (i, v) => if v == 1 { if truth.at(i) == 1 { c-m3 } else { c-m3.lighten(70%) } } else { white }),
        lane(r.m4, (i, v) => if v == 1 { if truth.at(i) == 1 { c-m4 } else { c-m4.lighten(70%) } } else { white }),
      )))
  }
  v(1fr)
  grid(columns: (52mm, 1fr), column-gutter: 1mm,
    text(size: 7pt, fill: mut)[Four wires per county, top to bottom:],
    [
      #box(width: 2mm, height: 2.2mm, fill: c-gap)#box(width: 2mm, height: 2.2mm, fill: c-watch)#box(width: 2mm, height: 2.2mm, fill: c-ok)#box(width: 2mm, height: 2.2mm, fill: c-unid) Model 1 status as known that month #h(3mm)
      #box(width: 6mm, height: 2.2mm, fill: ink) need (hindsight truth) #h(3mm)
      #box(width: 3mm, height: 2.2mm, fill: c-m3)#box(width: 3mm, height: 2.2mm, fill: c-m3.lighten(70%)) Model 3 slot: on need / wasted #h(3mm)
      #box(width: 3mm, height: 2.2mm, fill: c-m4)#box(width: 3mm, height: 2.2mm, fill: c-m4.lighten(70%)) Model 4 slot: on need / wasted
      #linebreak()
      #text(size: 7pt, fill: mut)[Black with nothing under it is a missed need-month. Only counties with any need or any slot are drawn. A Model 4 slot starts the month after a red Model 1 cell. That lag is the decision step, not the data.]
    ])
}
