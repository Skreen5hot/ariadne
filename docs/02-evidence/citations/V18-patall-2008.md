---
id: V18
claim_id: V18
claim: "Perceived freedom essential to wellbeing even when not exercised"
claim_source: "Integral Ethics v1 §4.3 (value entry) / v2 Candidate value ontology table"
citation_as_given: "Patall, Cooper & Robinson (2008)"
resolved:
  authors: "Patall, E. A.; Cooper, H.; Robinson, J. C."
  year: 2008
  title: "The Effects of Choice on Intrinsic Motivation and Related Outcomes: A Meta-Analysis of Research Findings"
  venue: "Psychological Bulletin, 134(2), 270-300"
  doi: "10.1037/0033-2909.134.2.270"
  isbn: ""
  url_opened: "https://selfdeterminationtheory.org/wp-content/uploads/2019/10/2008_PatallCooperRobinson_PsychBulletin.pdf"
  urls_attempted:
    - "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:18298272%20AND%20SRC:MED&resultType=core&format=json (opened; abstract, PMID 18298272)"
    - "https://api.crossref.org/works?query.bibliographic=Patall+Cooper+Robinson+2008+The+effects+of+choice+on+intrinsic+motivation+and+related+outcomes+a+meta-analysis+Psychological+Bulletin&rows=4 (opened; metadata)"
    - "https://api.semanticscholar.org/graph/v1/paper/DOI:10.1037/0033-2909.134.2.270?fields=title,authors,year,venue,abstract,externalIds,openAccessPdf,citationCount (opened; abstract elided)"
    - "https://api.openalex.org/works/doi:10.1037/0033-2909.134.2.270 (opened; metadata)"
    - "https://pubmed.ncbi.nlm.nih.gov/18298272/ (reCAPTCHA page, no content)"
  access: full_text
finding: |
  Full text (publisher PDF hosted on selfdeterminationtheory.org, fetched with WebFetch and converted with
  pdftotext).
  Design: meta-analysis of experiments that provided participants a choice versus no choice and measured
  intrinsic motivation and related outcomes. Literature 1974-2004; non-North American samples excluded (p. 276).
  41 studies, 46 independent samples, 290 effect sizes in total, 91 overall effect sizes for intrinsic motivation
  (Table 3, p. 287). Total participant N is not reported in the text I read.
  Effect (Table 4, p. 287; fixed-effects d first, random-effects in brackets): intrinsic motivation k = 46,
  d = 0.30 [0.25, 0.35] (RE 0.36 [0.27, 0.46]), Q(45) = 146.30, p < .001; trim-and-fill imputation reduces the
  estimate to about d = 0.21-0.24 ('shrank by about one third', p. 287). Effort k = 13, d = 0.22 [0.08, 0.35]
  (RE 0.28 [0.01, 0.56]). Task performance k = 13, d = 0.32 [0.17, 0.47] (RE 0.36 [0.09, 0.63]). Subsequent
  learning k = 14, d = 0.10, ns. Perceived competence k = 8, d = 0.59. Preference for challenge k = 3, d = 0.71
  (RE 0.74). Pressure/tension k = 3, d = 0.03, ns. Creativity k = 2, d = 0.17, ns. Satisfaction (with the task)
  k = 1, d = 0.08, ns.
  Moderators of the intrinsic-motivation effect (Table 5, p. 289; abstract): larger for instructionally
  irrelevant choices than for choices between activities, task versions or rewards; larger for 2-4 successive
  choices; smaller when a reward followed the choice; larger against the most controlling control groups; larger
  for children (k = 10, d = 0.51) than college students (d = 0.26); larger in yoked designs and in laboratories
  embedded in natural settings.
  Wellbeing: not an outcome in the meta-analysis. Perceived autonomy is the theorised mediator (introduction,
  pp. 270-272), not a measured outcome. Every included study manipulates choices that participants actually make;
  no design tests the effect of an option that is available but not used.
  Location: Tables 3-5 (pp. 287-289); Discussion (p. 294).
quotation: "The results of this meta-analysis suggest that choice can have a positive overall effect on intrinsic motivation"
quotation_location: "Discussion, p. 294"
fit: neighbouring_claim
fit_note: |
  The meta-analysis is about providing choices and their effect on intrinsic motivation, effort and performance.
  It does not measure wellbeing, perceived freedom as such, exit options, or freedom that is not exercised; the
  one 'satisfaction' effect is task satisfaction from a single study and is null. What it supports is:
  'providing people with choices (especially 2-4 trivial ones, unrewarded) increases intrinsic motivation,
  effort and performance, more so in children.' The register's idea (a perceived option to leave matters even
  if unused) needs a different literature: perceived free choice and life satisfaction (Inglehart et al. 2008,
  record V18x) and, for the 'unexercised' part, work on exit options or perceived control, none of which was
  opened here.
suggested_rewording: "Providing people with choices increases intrinsic motivation, effort and performance (meta-analytic d about 0.3), especially when the choices are made freely and not rewarded."
replication:
  searched: yes
  status: none_found
  sources:
    - citation: "Ryan, R. M., Duineveld, J. J., Di Domenico, S. I., Ryan, W. S., Steward, B. A., & Bradshaw, E. L. (2022). We know this much is (meta-analytically) true: A meta-review of meta-analytic findings evaluating self-determination theory. Psychological Bulletin (accepted manuscript; volume and DOI not shown in the opened file)"
      url_opened: "https://selfdeterminationtheory.org/wp-content/uploads/2023/01/2023_RyanDuineveldDiDomenicoEtAl_Meta.pdf"
      note: "Full text of the accepted manuscript. Not an independent replication: it re-reports Patall et al. 2008 (41 studies, 46 samples; choice associated with intrinsic motivation r = .15 and effort r = .11) and its moderators, and identifies no later meta-analysis of choice. Authors overlap with the SDT tradition but not with Patall et al."
retraction_check: clean
retraction_check_url: "https://api.openalex.org/works/doi:10.1037/0033-2909.134.2.270 (is_retracted false); Europe PMC record shows no correction fields; WebSearch '\"The effects of choice on intrinsic motivation and related outcomes\" Patall retraction OR erratum OR correction' returned no notice"
proposed_strength: Hypothesis
contested: ""
verified_by: agent
verified_on: 2026-09-26
ratified: false
---

## Notes
- The paper's own publication-bias analysis (trim-and-fill) reduces the headline intrinsic-motivation effect by
  about a third; worth carrying into any reworded claim.
- No later meta-analysis specifically of choice provision was found in one WebSearch; the 2022 SDT meta-review
  treats Patall et al. as the standing estimate.
