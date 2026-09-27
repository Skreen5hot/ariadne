---
id: V18x
claim_id: V18
claim: "Perceived freedom essential to wellbeing even when not exercised"
claim_source: "Integral Ethics v1 §4.3 (value entry) / v2 Candidate value ontology table"
citation_as_given: "none (added by the verifier as a better-fitting source for V18)"
resolved:
  authors: "Inglehart, R.; Foa, R.; Peterson, C.; Welzel, C."
  year: 2008
  title: "Development, Freedom, and Rising Happiness: A Global Perspective (1981-2007)"
  venue: "Perspectives on Psychological Science, 3(4), 264-285"
  doi: "10.1111/j.1745-6924.2008.00078.x"
  isbn: ""
  url_opened: "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:26158947%20AND%20SRC:MED&resultType=core&format=json"
  urls_attempted:
    - "https://api.openalex.org/works?filter=doi:10.1111/j.1745-6924.2008.00078.x&select=doi,title,publication_year,is_retracted (opened in a batch call; retraction flag)"
  access: abstract_only
finding: |
  Abstract only (Europe PMC record; PMID 26158947; JSON also read directly with curl).
  Design: analysis of representative national surveys carried out 1981-2007 with time series for 52 countries;
  regression analyses of societal happiness on free choice and development indicators.
  Sample: national survey data; N not given in the abstract.
  Effect: happiness rose in 45 of the 52 countries with substantial time-series data. 'Regression analyses
  suggest that the extent to which a society allows free choice has a major impact on happiness.' Economic
  development, democratization and increasing social tolerance raised the extent to which people perceive that
  they have free choice, which in turn raised happiness. Coefficients are not given in the abstract.
  Location: abstract.
quotation: ""
quotation_location: ""
fit: partially_supports
fit_note: |
  Supports 'perceived free choice predicts (societal) happiness' with cross-national survey data. It does not
  test whether freedom matters when it is NOT exercised, nor freedom to exit specifically, and it is
  correlational at the society level. Closer to the claim than Patall et al. 2008, but still not the 'even when
  not exercised' component.
suggested_rewording: "Perceived freedom of choice predicts life satisfaction and happiness across societies, over and above income."
replication:
  searched: yes
  status: none_found
  sources: []
retraction_check: clean
retraction_check_url: "https://api.openalex.org/works?filter=doi:10.1111/j.1745-6924.2008.00078.x&select=doi,title,publication_year,is_retracted (is_retracted false, batch call)"
proposed_strength: Hypothesis
contested: ""
verified_by: agent
verified_on: 2026-09-26
ratified: false
---

## Notes
- Related but not opened: Verme, P. (2009), 'Happiness, freedom and control', Journal of Economic Behavior &
  Organization 71, 146-161, doi 10.1016/j.jebo.2009.04.008 (CrossRef and OpenAlex metadata opened; no abstract
  available in either). Search snippets describe it as finding a freedom-of-choice/locus-of-control variable that
  predicts life satisfaction in 74 of 75 countries; that description is unverified.
- The 'even when not exercised' component still has no source; it would need work on exit options, perceived
  control, or counterfactual freedom.
