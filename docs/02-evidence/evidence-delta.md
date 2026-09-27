# Evidence delta: proposed status changes for ratification

This is the ratification document. One row per claim whose proposed strength differs from the
strength printed in *Integral Ethics v2*, or whose wording should change to match its evidence,
with the record that justifies it. It changes nothing by itself: a row takes effect only when Aaron
sets `ratified: true` on the register entry and, where wording changes, edits v2.

Grades follow the strength rules in `README.md`. The rule that matters most here: a claim's grade is
the strongest grade its *fitting* records justify, and a philosophical or formal argument with no
empirical component is "Argued only" however well established it is.

Prepared 2026-09-26. Phase 1 (load-bearing claims) and Phase 2 (candidate values) complete; this
document is the Phase 3 deliverable.

## Ratification checklist (Phase 3)

Across both phases: 42 items graded, 73 records, 0 sources invented, 1 source that could not be
opened at all (Gino & Bazerman 2009, E1x). Proposed grades: Strong 1, Moderate 18, Argued only 15,
Hypothesis 8. v2 printed Strong for 11 claims; the records bear it for one.

To ratify an item: set `ratified: true` and `status: ratified` on its entry in `register.yaml`
(and change `proposed_strength` if you decide otherwise), then run `python tools/render_register.py`
and `python -m pytest tests/evidence`. The tests refuse a ratified flag without a grade and a grade
without records. Wording changes are made in `integral-ethics-v2.md`, never in the register.

| # | Decision | Where | Items |
| --- | --- | --- | --- |
| 1 | Ratify or revise the 19 claim grades | "Load-bearing claims: status changes" | 10 downgrades proposed; E2 stays Strong; E4 and E5 are below Moderate |
| 2 | Ratify or revise the 23 value grades | "Candidate values: status changes" | 10 Moderate, 6 Hypothesis, 7 Argued only; six cited sources were neighbouring claims |
| 3 | Adopt, amend or reject each rewording | both tables, last column | F2, E1, E4, E5, E6, E7, C4a, C5, C7, C8; V01, V04-V06, V08-V12, V14-V19 |
| 4 | Answer the four rules questions | "Rules questions for Aaron" | formal results (affects F1, C5, C6, F2); same-lab replications (E6); abstract-only originals (E3); claims with a normative half (C7, E5) |
| 5 | Apply the citation corrections to v2 | "Citation corrections to v2" | 7 items, including the ValueNet mapping count |
| 6 | Apply the v1 reference corrections | "v1 reference corrections" | Shapiro, Jacobsen, Steiner GA 151; Philosophy of Freedom date noted |
| 7 | Decide the six uncited values | "Uncited values for Aaron to decide" | V02, V03, V20-V23 |
| 8 | Acknowledge the ValueNet gaps or commission classes | "ValueNet gaps" | aimed goods, agency capability, competencies, principle kind, harms outside the six pairs |
| 9 | Close the E-PC pre-registration open items | `experiments/e-pc/PREREG.md` §12 | O-1 model and sampling, O-2 N, O-3 rater, O-4 second annotator, O-5 fabrication tolerance |


## Summary of Phase 1

v2 states: "Fifteen rest on strong or moderate evidence, three on philosophical argument alone, and
one is an open hypothesis." After verification of all 19 claims (40 records, 37 distinct sources,
none invented, every DOI resolved at CrossRef):

| Grade | v2 says | Verified |
| --- | --- | --- |
| Strong | 11 | 1 (E2) |
| Moderate | 4 | 8 (E1, E3, E6, E7, E8, C1, C4a, C7) |
| Argued only | 3 | 8 (F1, F2, E5, C2, C4, C5, C6, C8) |
| Hypothesis | 1 | 2 (E4, H-P6) |

Ten claims go down; none goes up. Two of the downgrades are results in the brief's sense, not
bookkeeping: **E4 (prospective hindsight) and E5 (competing hypotheses) have less evidence than
"Moderate"**, and the register should say so. Four downgrades (F1, C5, C6, and the formal half of
F2) follow from the rules' treatment of formal and philosophical argument and raise a rules question
for Aaron (see "Rules questions").

## Load-bearing claims: status changes

| Claim | Current | Proposed | Why (records) | Proposed rewording (if any) |
| --- | --- | --- | --- | --- |
| F1 No single perspective captures all morally relevant features | Strong | Argued only | All three sources are philosophical or formal-ontological and say what v2 attributes to them, but none concerns morality; the step to "morally relevant features" is v2's own (F1a, F1b, F1c). By rule, argument without an empirical component is Argued only | Keep; note in v2 that the moral specialisation is argued, not cited |
| F2 Added perspectives help only when diverse | Moderate | Argued only | The formal ground (Hong & Page) is disputed and defended in the literature and, either way, concerns search heuristics (F2a, F2b). The empirical ground (Lorenz 2011) is partial and contradicted at scale by Becker et al. 2017 (F2c). The closest empirical analogue (Herzog & Hertwig 2009) supports "more when diverse", not "only when diverse", with mixed follow-ups (F2x). v2 itself says F2 "rests mainly on the logical argument"; the grade should match | "Added perspectives help in proportion to how much they differ from those already present" (F2x); or keep "only" and mark it as the selection argument's conclusion, not an empirical finding |
| E1 People routinely miss available, morally relevant information | Strong | Moderate | Chugh & Bazerman 2007 and Tenbrunsel & Messick 2004 are review or conceptual papers (E1a partially supports; E1b Argued only). Simons & Chabris 1999 shows people miss salient visual events, a neighbouring claim (E1c). The direct test of missing *moral* information (Gino & Bazerman 2009, E1x) could not be opened and its Study 1 failed a preregistered replication | "People routinely fail to notice or use easily available information; there is preliminary and contested evidence that this extends to morally relevant information (e.g., gradual ethical erosion)" (E1a/E1c) |
| E2 Framing changes choice with facts held fixed | Strong | Strong | No change. Replicated at scale (Many Labs 1; Steiger & Kühberger 2018 meta-analysis) at about half the original magnitude (E2) | None |
| E3 Structured consideration of alternatives reduces bias | Strong | Moderate | Original opened as abstract only; three conceptual replications in a consistent direction (Hirt & Markman 1995; Mussweiler et al. 2000; Greitemeyer 2023 in part) but one recent null for a neighbouring strategy (E3). Strong is arguable if the original's statistics are verified from the full text | None |
| E4 Prospective hindsight surfaces more reasons for failure | Moderate | Hypothesis | The primary source could be opened only as an abstract, which attributes the effect to certainty framing rather than temporal perspective and says nothing about failure or reason counts; the "30%" figure appears only in secondary sources; Klein 2007 is a method description with no data; controlled premortem studies are thesis- and poster-level and mixed (E4a, E4b). **This claim's best available evidence is weaker than Moderate** | "Framing a future outcome as already certain (prospective hindsight) elicits longer and more concrete explanations than framing it as uncertain" (E4a). The Explanation operation in v2 should cite this narrower finding or none |
| E5 Holding competing explanations open improves analysis | Moderate | Argued only | Heuer 1999 argues the claim and calls ACH "proven" without a citation; the six controlled tests since are mixed to negative on accuracy, though Dhami et al. 2019 find ACH-trained analysts consider all hypotheses more often (E5). **This claim's best available evidence is weaker than Moderate** | "Keeping competing explanations open until disproved is a recommended analytic discipline (Heuer 1999); controlled tests of the ACH procedure built on it show little or no overall gain in accuracy" (E5) |
| E6 Perspective-shifting improves wise reasoning | Moderate | Moderate | No change in grade. Kross & Grossmann 2012 supports it in two experiments; replications are same-lab, two preregistered (E6a); the 2020 target article is a review that treats perspective-taking as part of wisdom and calls self-distancing underspecified (E6b) | "Self-distancing (adopting an observer or third-person perspective on one's own situation) increases wise reasoning about that situation" (E6b): narrower than "perspective-shifting" |
| E7 Integrating many views outperforms single-model expertise | Strong | Moderate | Tetlock 2005 (book not opened; results from a peer-reviewed review: 284 experts, foxes beat hedgehogs, neither beat simple rules) supports a related claim; Mellers et al. 2014 tests teaming, training and tracking, not "integration vs single-model expertise", and its team and training effects are diminished or reversed in Hauenstein et al. 2025's reanalysis; the two are one research programme (E7a, E7b) | E7b: state the claim as team information-sharing and training improving forecasts, with the Hauenstein caveat; or cite an aggregation study that tests integration directly |
| E8 Asking people beats imagining their view | Strong | Moderate | Eyal, Steffel & Epley 2018 supports the claim across 25 experiments, but no independent replication of the perspective-getting result was found (E8). The wider perspective-taking literature replicates poorly, which supports v2's design choice rather than E8's grade | None |
| C1 Flourishing is multidimensional | Moderate | Moderate | No change. Finnis argues it (C1a); Ryff (C1b) and Keyes (C1f) show more than one dimension, with the count contested; VanderWeele 2017 is conceptual (C1c); the Global Flourishing Study presupposes six domains and reports a composite (C1d); Ryan & Deci 2001 reviews two strands (C1e) | Cite Keyes/Lamers (three-factor CFA) and the Ryff critics as the empirical anchor; drop "six" wherever v2 implies it |
| C4 Genuine goods can conflict without one being unreal | Argued only | Argued only | No change. All five works exist and say what is attributed (C4-1 to C4-5). Two citation corrections below | None |
| C4a Human values show a stable structure of mutual conflict | Strong | Moderate | The circumplex is widely replicated, mostly with Schwartz as co-author, with reported deviations in some countries; "mutual conflict" over-reads a correlational structure of importance ratings (C4a) | "Human value priorities show a stable circumplex structure in which opposing value types are negatively related (motivationally incompatible) and adjacent types compatible" (C4a). Under that wording Strong is available |
| C5 No neutral aggregation of plural criteria into one ranking | Strong | Argued only | Arrow's theorem is about persons' orderings and applies to criteria by analogy; Arrow's conditions contain no neutrality condition (C5a). Keeney & Raiffa construct aggregations under independence conditions rather than deny their possibility (C5b: neighbouring claim). Formal result, no empirical component | "Any aggregation of plural criteria embeds decision-maker-specific trade-off judgments; there is no value-free aggregation" (C5b); cite Arrow & Raynaud 1986 for the impossibility reading |
| C6 Irreversibility warrants extra weight under uncertainty | Strong | Argued only | Arrow & Fisher 1974 states and proves the quasi-option-value result and it is standard (C6). By rule a formal argument is Argued only. See "Rules questions" | None |
| C2 Dignity acts as a side-constraint, not a quantity to trade | Argued only | Argued only | No change. Kant carries the dignity/price distinction (C2a); Nozick carries the side-constraint structure but speaks of rights, not dignity (C2b); Aquinas's exceptionless precept protects the innocent, and the side-constraint reading is an interpretation (C2c) | None; see citation corrections |
| C7 Decision aids bias human choice; the human must stay the decider | Strong | Moderate | Parasuraman & Manzey 2010 integrates the automation-bias evidence (Goddard et al. 2012 systematic review and Lyell & Coiera 2017 opened as replication); the second half of the claim is normative and no evidence can carry it (C7) | Split: "Decision aids bias human choice (automation bias)" (empirical; would meet Strong) and "the human must stay the decider" (commitment, Argued only) |
| C8 Many legitimate paths, not all equally good | Argued only | Argued only | No change in grade. Finnis supports "inexhaustibly many" reasonable life plans but holds the basic goods incommensurable and does not rank legitimate plans; he excludes unreasonable ones (C8) | "Many legitimate paths; some paths are excluded as unreasonable, and the legitimate ones are not ranked on a single scale" (C8). If v2 means legitimate paths are ranked, Finnis is the wrong source |
| H-P6 The six operations are an exhaustive, efficient decomposition | Hypothesis | Hypothesis | No change; no source; tested by E-PC (H-P6) | None |

## Rules questions for Aaron

1. **Formal results.** The strength rules give no grade above "Argued only" to an established theorem
   (Arrow 1951, Arrow & Fisher 1974, Grenon & Smith 2004). Four downgrades (F1, C5, C6, F2's formal
   half) follow from that. Options: accept the rule as written; or add a grade such as "Formal
   (established)" for results that are proved and uncontested in their field, which would restore C6
   and possibly C5 without changing the empirical claims.
2. **Same-lab replications.** E6's replications are all from the originating lab, two preregistered.
   The rules ask for "independent" replications; if preregistered same-lab replications count, E6
   becomes Strong (E6a notes).
3. **Abstract-only primary sources.** E3's original could be opened only as an abstract. If Aaron has
   journal access and the reported statistics check out, E3 is arguably Strong (E3 notes).
4. **Claims with a normative half.** C7 and E5 mix an empirical finding with a commitment or a
   method. Splitting them (as proposed above) lets the empirical half be graded on its evidence.

## Citation corrections to v2 (from Phase 1 records)

| Where | v2 says | Sources say | Record |
| --- | --- | --- | --- |
| C2 | "Nozick, side-constraints (1974)" chapter "Moral Constraints and the Moral State" (as given to the verifier) | The chapter is "Moral Constraints and the State" | C2b |
| C4 | "Chang (1997)" | The parity idea is in Chang 2002, "The Possibility of Parity", Ethics 112(4); the 1997 volume is the edited collection. Cite both | C4-4 |
| C4 | "Williams on moral remainder" | Williams's word is "remainder" (Problems of the Self, p. 179, as quoted by van Domselaar 2022); "moral remainder"/"moral residue" as labels are the secondary literature's | C4-5 |
| F1 | "Aquinas, mode of the knower" with the Latin tag "quidquid recipitur per modum recipientis recipitur" | The tag is a scholastic axiom distilled from Aquinas, not verbatim; Aquinas's own wording at ST I q.12 a.4 is "cognitum est in cognoscente secundum modum cognoscentis". Cite ST I q.12 a.4 co.; cf. I q.75 a.5; I q.84 a.1, and mark the tag as an axiom | F1c |
| F1 | "Bittner & Smith, granular partitions" | Resolve to "A Theory of Granular Partitions" (2003), in Duckham, Goodchild & Worboys (eds.), Foundations of Geographic Information Science, Taylor & Francis, pp. 117-151 | F1b |
| E7 | Tetlock 2005 | Forecast count: the opened review (Tschoegl & Armstrong 2007) reports 82,361 forecasts from 284 experts; search snippets say 28,000. Verify against the book before citing a number | E7a |
| Candidate value ontology | "Its 222 mapping annotations to the original ValueNet" | The vendored `valuenet-mappings.ttl` (checksum-verified) carries 93 (source, target) mapping statements: 14 `historicallyCorrespondsTo`, 79 `hasRelatedConceptualMatch`. Where 222 comes from is not known | (coordinator count) |

## v1 reference corrections

Filled from the Phase 2 reference check (Shapiro 2006/2011; Jacobsen 2006 vol. 94; Steiner GA 151).

| Reference | v1 says | Sources say | Correction |
| --- | --- | --- | --- |
| Shapiro | In text (line 946): "depth of practice predicts benefits, not breadth (Shapiro et al., 2011)". Reference list (line 1597): Shapiro, Carlson, Astin & Freedman (2006), Mechanisms of mindfulness, J Clin Psychol 62(3), 373-386 | The 2006 reference is correct as listed (DOI 10.1002/jclp.20237, PMID 16385481) but is a theoretical model of mechanisms; its abstract says nothing about depth or amount of practice. A real Shapiro et al. 2011 exists (Shapiro, Brown, Thoresen & Plante, J Clin Psychol 67(3), 267-277, DOI 10.1002/jclp.20761, PMID 21254055): an N = 30 RCT in which higher pretreatment trait mindfulness predicts larger MBSR gains; also silent on depth vs breadth. Abstracts only | Log as an in-text/reference mismatch AND an unsupported claim. Do not merely change the year to 2006. Drop the "depth not breadth" clause or find a source that tests practice dose; none was confirmed. If the 2011 paper is kept it supports only "people higher in trait mindfulness benefit more from MBSR" |
| Jacobsen | Line 1554: Jacobsen, Buchta, Köhler & Schröger (2006), Psychological Reports, 94(4), 1253-1260. Line 532 uses it for "aesthetic preferences show cross-cultural patterns" | CrossRef and PubMed agree: 2004, Psychological Reports 94(3, Pt 2), 1253-1260, DOI 10.2466/pr0.94.3c.1253-1260, PMID 15362400. The study: 311 German non-artist students listed adjectives for "aesthetics"; "beautiful" named by over 90%; single culture, single language, about the conceptual structure of "aesthetics", not preferences | Fix the reference (2006 to 2004; 94(4) to 94(3, Pt 2); add the DOI) and the in-text year. Separately, the line-532 use does not fit: reword to what the paper supports (beauty as the primary dimension of aesthetic judgment) or find a genuinely cross-cultural source |
| Steiner, twelve worldviews | Lines 60 and 77 attribute the twelve worldviews to *The Riddles of Philosophy* "and related lectures" (Steiner 1914/2008); line 1602 lists Riddles of Philosophy, Anthroposophic Press | GA 151, *Human and Cosmic Thought*, four lectures, Berlin, 20-23 January 1914 (rsarchive.org, RSP 1991 edition, trans. rev. Charles Davy): Lecture 2 introduces twelve equally justified world-outlooks with the zodiac analogy; Lecture 3 lists all twelve (Materialism, Sensationalism, Phenomenalism, Realism, Dynamism, Monadism, Spiritism, Pneumatism, Psychism, Idealism, Rationalism, Mathematism) with their signs and the seven planetary soul-moods. GA 18, *The Riddles of Philosophy* (trans. Koelln, Anthroposophic Press 1973): a history of world conceptions in 18 chapters; no chapter concerns a twelve-fold scheme (chapter bodies not read, so a passing mention is not excluded). Current English edition: Human and Cosmic Thought (CW 151), Rudolf Steiner Press, 3rd ed. 2015, ISBN 978-1-85584-416-2 | Re-attribute the twelve to GA 151: Steiner, R. (2015). *Human and Cosmic Thought* (CW 151) (C. Davy, Trans.; 3rd ed.). Rudolf Steiner Press. In text (Steiner, 1914/2015), the twelve listed in Lecture 3. Keep GA 18 only as a general citation for Steiner's history of world conceptions, cited as the 1973 Koelln translation (the "2008" edition was not checked) |
| Steiner, Philosophy of Freedom (out of scope, noted) | Line 1603 dates it "1923/1973" | rsarchive lists it as GA 4 (first edition 1894; RSP 1964 translation). The 1923 date looks doubtful. Not verified further | Check before citing |

## ValueNet gaps (protocol question 2)

Classes needed by the register or by E-PC that the BFO-Aligned ValueNet modules do not provide.
Recorded, not invented.

| Need | What exists | Gap |
| --- | --- | --- |
| Flourishing as the state the dispositions aim at (V01) | No class; folk has no `FlourishingDisposition` and there is no state/good class in the pattern | ValueNet models values as realizable entities only; "aimed goods" (V01, V04, V05, V06, V10, V12, V13, V14) have no home. The register records them as `aimed_good` with related dispositions only |
| Agency as a capability (V11) | `vn-core:ValueRelatedRealizableEntity` inheres in a CCO Agent (`ont00001017`); no capability class in the ValueNet modules | The authenticity half is a disposition (`folk:AuthenticityDisposition`); the agency half would be a CCO agent capability, outside ValueNet |
| Competencies (V08, V16, V22) | `folk:WisdomDisposition`, `folk:OpenMindednessDisposition`, `folk:HumilityDisposition` exist as orientations | Being wise or reflective is a capability, not an orientation; related, not identical |
| A "principle" kind (V23) | None | Limited pluralism is a principle about the value space; classified as `constraint` for want of a kind. v2 already proposes removing it from the value list |
| Harms outside the six moral-foundations pairs | `vn-core:ValueViolationProcess` with `contravenes` any disposition | The pilot restricts harms to the six pairs (per brief); annotators record any needed class as `class_fit: gap` |

## Uncited values for Aaron to decide

V02 Human dignity, V03 Truth / reality-alignment, V20 Non-coercion, V21 Transparency, V22 Epistemic
humility, V23 Limited pluralism carry no citation in v1. Per the brief no search was made; each is
recorded as "Argued only" in the register. Aaron decides whether any needs empirical grounding (V22
is the one for which wise-reasoning research measures a close analogue).

## Candidate values: status changes (Phase 2)

v1 attached no strength grade to its value citations, so every row here is a first grade rather
than a change. Fit is judged against v1's own sentence for the value. 31 records cover the 19 cited
values (22 cited sources plus 9 extra records for better-fitting sources the verifiers found); the
six uncited values are "Argued only" by rule.

**Summary.** Moderate 10 (V01, V04-V11, V19); Hypothesis 6 (V12, V14-V18); Argued only 7 (V02,
V03, V13, V20-V23). **Six values' cited sources turned out to be neighbouring claims** (V08, V09,
V12, V14, V17, V18): real papers that do not test the sentence they were cited for. For four of
those a better-fitting source was found and recorded (V08x Ardelt 1997; V09x Park, Peterson &
Seligman 2004; V17x Lerner & Tetlock 1999; V18x Inglehart et al. 2008). **Six values have less
evidence than Moderate as worded** (V12, V14, V15, V16, V17, V18), and one (V17) is contradicted
in its unconditional form by the best source for it.

| Value | Proposed | Fit of the cited source(s) | Why (records) | Proposed rewording / citation change |
| --- | --- | --- | --- | --- |
| V01 Human flourishing | Moderate | partial (V01a, V01b) | Keyes's three-factor structure replicates (Lamers 2011); "cannot be reduced to single measures" is contradicted by direct tests (Disabato 2016) | "Positive mental health comprises emotional, psychological and social wellbeing, which are related but distinguishable factors"; drop "cannot be reduced" or mark it contested |
| V04 Material wellbeing | Moderate | partial (V04) | "Not sufficient" is well supported; strict necessity is not (the poor remain 0.80 as likely as the rich to be satisfied) | "Poverty substantially lowers subjective wellbeing, while income beyond modest affluence adds little: material security matters most at the low end and is not sufficient for wellbeing" |
| V05 Experiential richness | Moderate | partial (V05) | Diener et al. 1999 supports pleasant affect as a separable component of SWB; it says nothing about richness or variety of experience | Either rename the value to what the source supports ("positive affect") or find a source for experiential richness; none was found |
| V06 Meaningful relationships | Moderate | partial (V06a, V06b) | Relationship quality predicts wellbeing (Pinquart & Sörensen 2000 meta-analysis of 286 studies; SDT relatedness meta-analyses); the superlative and "requiring cultural frameworks" are unsupported; the trade book is a secondary source | "Quality of close relationships is among the strongest and most consistent predictors of happiness and later-life health in longitudinal cohorts"; replace Waldinger & Schulz 2023 with Pinquart & Sörensen 2000 and one SDT meta-analysis |
| V07 Mastery and excellence | Moderate | supports (V07) | Competence need satisfaction relates to wellbeing in two meta-analyses (Van den Broeck 2016; Stanley 2021) with significant heterogeneity, which the rules cap at Moderate | Cite Van den Broeck et al. 2016 alongside Deci & Ryan 2000; Strong if the heterogeneity is judged acceptable |
| V08 Wisdom | Moderate | neighbouring (V08); supports (V08x) | Ardelt 2003 validates the 3D-WS and, in the accessible text, says nothing about wellbeing; Ardelt 1997 (N = 120, SEM) makes the register's claim almost verbatim | Cite Ardelt 1997 in place of, or beside, Ardelt 2003: "Wisdom is associated with life satisfaction in older adults over and above objective circumstances such as health, finances and social involvement" |
| V09 Virtue / character | Moderate | neighbouring (V09); partial (V09x) | The handbook is a classification; Park et al. 2004 (N = 5,299) show hope, zest, gratitude, love and curiosity correlate .35-.59 with life satisfaction; kindness and integrity only .19-.36 | "Character strengths correlate with life satisfaction, most strongly hope, zest, gratitude, love and curiosity; kindness and integrity only weakly"; cite Park, Peterson & Seligman 2004; opening the Bruna 2019 or Casali & Feraco 2025 meta-analysis would likely justify Strong for the reworded claim |
| V10 Meaning and purpose | Moderate | partial (V10); partial (V10x) | Steger 2012 reviews meaning and wellbeing but not health or longevity; Hill & Turiano 2014 (MIDUS N = 6,163, HR 0.85 per SD) with Cohen 2016 (meta-analysis, N = 136,265, RR 0.83) and Alimujiang 2019 carry the longevity half | "Meaning in life correlates with wellbeing (Steger 2012); purpose in life prospectively predicts lower mortality independent of affective wellbeing (Hill & Turiano 2014; Cohen et al. 2016)". The longevity half alone would grade Strong |
| V11 Authentic agency | Moderate | partial (V11a, V11b) | Autonomy-as-volition r about .46 with SWB across cultures (Yu 2018); authenticity r about .40 (Sutton 2020); both meta-analyses I² about 90% | "Satisfaction of the need for autonomy, understood as volition, correlates moderately with subjective wellbeing across cultures; dispositional authenticity correlates moderately with wellbeing, more strongly in individualist cultures" |
| V12 Spiritual vitality | Hypothesis | neighbouring (V12a, V12b); partial (V12bx) | Koenig cannot separate spirituality from religion by its own definition; longitudinal effects are small (r = .08); non-religious spiritual practice shows mixed outcomes; Hood measures mysticism but does not show transformation; Griffiths 2006 is one small drug study. **Weaker than Moderate** | Split the sentence: "Religious/spiritual involvement is associated with wellbeing cross-sectionally; longitudinal effects are small; independence from religious belief is unestablished" and, separately, "occasioned mystical-type experiences are followed by self- and observer-reported positive change (Griffiths et al. 2006, 2008)" |
| V13 Harmonic structure | Argued only | partial (V13); partial (V13x) | Sirgy & Wu 2009 is a theoretical proposal with no data; the one empirical test found (Gröpel & Kuhl 2009) concerns work-life balance and runs through need fulfilment | Keep v2's open item (rename to life-domain balance, treat as a profile property, or drop). If kept: "Balance across life domains is proposed to raise wellbeing; tests so far concern work-life balance and are mediated by need fulfilment" |
| V14 Cultural embeddedness | Hypothesis | neighbouring (V14); partial (V14x) | Oishi & Diener 2001 tests goal-motive/culture fit as a moderator of the attainment-SWB link, not "cultural coherence"; Fulmer 2010 (person-culture match) is contested at scale by Gebauer 2020. **Weaker than Moderate** | Define the value before citing for it. If it means person-culture match: "Person-culture match amplifies the wellbeing benefits of one's traits (contested)" |
| V15 Commitment and rootedness | Hypothesis | partial (V15) | The Investment Model runs the other way (satisfaction predicts commitment; commitment predicts persistence); vocational success has no source. **Weaker than Moderate** | "Satisfaction, investment and poor alternatives predict relationship commitment; commitment predicts relationship persistence (Rusbult et al. 1998; Le & Agnew 2003)". Vocational success needs its own source (Meyer et al. 2002 is the lead, not opened) |
| V16 Critical reflection | Hypothesis | partial (V16, V16x) | The cited review argues against unconditional reflection; only narrative-building forms help and self-insight, not reflection, tracks wellbeing. **Weaker than Moderate** | "Congruence between conscious self-views and nonconscious motives is associated with wellbeing; introspection helps only in forms that build a coherent narrative and can harm as rumination or reasons-analysis" |
| V17 Community accountability | Hypothesis (as worded); Moderate for the conditional form | neighbouring (V17); partial (V17x) | Cialdini & Goldstein review compliance and conformity, not accountability; Lerner & Tetlock 1999 shows accountability improves judgment only under specific conditions and rejects the general claim. **As worded, contradicted by its best source** | "Accountability improves judgment when it is pre-decisional, to an audience whose views are unknown and who cares about process; known-audience accountability yields conformity and post-decisional accountability yields defensive bolstering" (Lerner & Tetlock 1999) |
| V18 Freedom to exit | Hypothesis | neighbouring (V18); partial (V18x) | Patall et al. 2008 is about providing choices and intrinsic motivation (d about 0.3, less after trim-and-fill); wellbeing, exit and unexercised freedom are never measured; Inglehart 2008 supports perceived free choice predicting societal happiness only. **Weaker than Moderate** | "Perceived freedom of choice predicts life satisfaction across societies (Inglehart et al. 2008)". The "even when not exercised" component needs exit-option or perceived-control work, not found |
| V19 Graduated autonomy | Moderate | partial (V19, V19x) | Soenens & Vansteenkiste 2010 is conceptual; Bradshaw et al. 2025 (k = 238, N = 126,423, r = .30) and Vasquez et al. 2016 support parental autonomy support predicting wellbeing and achievement; the "developmentally appropriate" qualifier is untested | "Parental autonomy support predicts child and adolescent wellbeing and achievement across developmental periods; whether calibrating autonomy to developmental stage adds to this has not been tested". Without the qualifier, Strong is available |
| V02, V03, V20, V21, V22, V23 | Argued only | no citation | Per the brief, no search was made | Aaron decides whether any needs empirical grounding |

**Citation corrections to v1/v2 from Phase 2.** Oishi & Diener "2009" is the Springer reprint of the
2001 PSPB article (V14). Steger 2012's chapter identifier does not resolve as a DOI; cite by book
ISBN (V10). The Ryan & Deci 2000 DOI is displayed by Europe PMC in the old double-slash form (V11a).
Waldinger & Schulz 2023 should be replaced by primary or meta-analytic sources (V06a).
