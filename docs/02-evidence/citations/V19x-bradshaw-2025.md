---
id: V19x
claim_id: V19
claim: "Developmentally appropriate autonomy support predicts optimal outcomes"
claim_source: "Integral Ethics v1 §4.3 (value entry) / v2 Candidate value ontology table"
citation_as_given: "none (added by the verifier as the empirical meta-analysis behind V19)"
resolved:
  authors: "Bradshaw, E. L.; Duineveld, J. J.; Conigrave, J. H.; Steward, B. A.; Ferber, K. A.; Joussemet, M.; Parker, P. D.; Ryan, R. M."
  year: 2025
  title: "Disentangling autonomy-supportive and psychologically controlling parenting: A meta-analysis of self-determination theory's dual process model across cultures"
  venue: "American Psychologist, 80(6), 879-895 (published citation from CrossRef; text read is the accepted manuscript posted 2024, preprint DOI 10.31234/osf.io/maf3e)"
  doi: "10.1037/amp0001389"
  isbn: ""
  url_opened: "https://selfdeterminationtheory.org/wp-content/uploads/2024/09/2024_BradshawDuinevelEtAl_ParentingMeta_PrePrint.pdf"
  urls_attempted:
    - "https://api.crossref.org/works?query.bibliographic=Bradshaw+Duineveld+Disentangling+Autonomy-Supportive+and+Psychologically+Controlling+Parenting+meta-analysis+American+Psychologist&rows=3 (opened; published citation and preprint DOI)"
    - "https://api.openalex.org/works/doi:10.1037/amp0001389?select=doi,title,publication_year,is_retracted (opened; retraction flag)"
  access: full_text
finding: |
  Full text of the accepted manuscript (fetched with WebFetch, converted with pdftotext; page numbers below are
  manuscript pages). Data and R code on OSF (https://osf.io/rcpw2/, as stated on p. 1).
  Design: one-stage and univariate meta-analytic structural equation modelling with moderation, testing SDT's
  dual process model (autonomy support -> wellbeing; psychological control -> ill-being).
  Sample: k = 238 studies, n = 1,040 effect sizes, N = 126,423 (abstract, p. 2). The autonomy-support ->
  wellbeing univariate model pooled 46 studies and 120 effects (p. 19).
  Effect (abstract p. 2; results pp. 19-20): parental autonomy support -> child wellbeing r = 0.30 [95% CI 0.26,
  0.33], Q(119) = 1757.76, p < .001, heterogeneity 31% within-study and 60% between-study, no evidence of
  publication bias (p = .90). Parental psychological control -> child ill-being r = 0.26 [0.23, 0.28]. In the
  one-stage model controlling for the predictors' intercorrelation: autonomy support -> wellbeing r = 0.26
  [0.20, 0.31]; psychological control -> ill-being r = 0.20 [0.17, 0.23].
  Moderators (pp. 20, 22; Table 1, p. 38): effects held across regions, national individualism, cultural
  hierarchy, developmental periods and child sex. Child age was the only moderator of the autonomy-support
  effect: adolescents (12-18) r = 0.34 [0.29, 0.38] vs adults (19+) r = 0.23 [0.15, 0.28]; the effect was
  strongest for life satisfaction and for non-college samples.
  On 'developmentally appropriate': the construct definition includes 'engaging them in purposeful,
  age-appropriate decisions' (p. 4); the authors state that autonomy-supportive parenting 'is not a
  one-size-fits-forever approach' and can be maintained into adolescence 'if adapted to be developmentally
  appropriate' (p. 10), and hypothesised (Hypothesis 5) and found that developmental stage does not remove the
  benefit. Calibration to developmental stage is not itself a coded variable.
  Conclusions (p. 27): autonomy support relates positively to child wellbeing 'across regions and cultures, male
  and female children, and developmental periods'.
quotation: "Autonomy-supportive parenting is not a one-size-fits-forever approach; it is inherently adaptive."
quotation_location: "Introduction, Hypothesis 5 rationale, manuscript p. 10"
fit: partially_supports
fit_note: |
  Strong meta-analytic support for 'parental autonomy support predicts child wellbeing' (r about 0.30, across
  cultures and developmental periods). The claim's qualifier 'developmentally appropriate' is part of how the
  construct is defined and is asserted in the rationale, but it is not measured or manipulated: no analysis
  compares age-calibrated with non-calibrated autonomy support. 'Optimal outcomes' is broader than the
  wellbeing/ill-being outcomes pooled here (Vasquez et al. 2016 add achievement and motivation). Hence partial.
suggested_rewording: "Parental autonomy support predicts child and adolescent wellbeing (meta-analytic r about 0.30) across cultures and developmental periods; whether calibrating autonomy to developmental stage adds to this has not been tested."
replication:
  searched: yes
  status: replicated
  sources:
    - citation: "Vasquez, A. C., Patall, E. A., Fong, C. J., Corrigan, A. S., & Pine, L. (2016). Parent autonomy support, academic achievement, and psychosocial functioning: A meta-analysis of research. Educational Psychology Review, 28(3), 605-644. doi 10.1007/s10648-015-9329-z"
      url_opened: "https://eric.ed.gov/?id=EJ1110197"
      note: "Abstract only. Independent earlier meta-analysis (36 studies) with the same direction: autonomy support related to achievement, autonomous motivation, psychological health (strongest), competence and engagement."
retraction_check: clean
retraction_check_url: "https://api.openalex.org/works/doi:10.1037/amp0001389?select=doi,title,publication_year,is_retracted (is_retracted false)"
proposed_strength: Moderate
contested: ""
verified_by: agent
verified_on: 2026-09-26
ratified: false
---

## Notes
- The published article (American Psychologist 80(6), 879-895) was not opened; all findings are from the
  accepted manuscript, which the authors say 'may differ slightly' from the version of record. OpenAlex lists the
  publication year as 2024 (online first) and CrossRef as 2025 (issue); the record uses the issue year.
- The two meta-analyses come from the SDT research tradition (Ryan is senior author here; Patall is a co-author
  of Vasquez et al.); they are independent of each other but not of the theory being tested.
- Extra record: not cited in v1. Grade Moderate (partial fit on a meta-analysis); Strong would apply to the
  reworded claim without the 'developmentally appropriate' qualifier.
