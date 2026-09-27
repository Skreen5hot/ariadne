---
id: V10x
claim_id: V10
claim: "Meaning independent dimension of wellbeing, predicts health and longevity"
claim_source: "Integral Ethics v1 §4.3 (value entry) / v2 Candidate value ontology table"
citation_as_given: "(not cited in v1; added by verifier as the primary source for the health/longevity part of V10)"
resolved:
  authors: "Hill, P. L.; Turiano, N. A."
  year: 2014
  title: "Purpose in life as a predictor of mortality across adulthood"
  venue: "Psychological Science 25(7), 1482-1486"
  doi: "10.1177/0956797614531799"
  isbn: ""
  url_opened: "https://pmc.ncbi.nlm.nih.gov/articles/PMC4224996/"
  urls_attempted:
    - "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:24815612+AND+SRC:MED&resultType=core&format=json"
    - "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC4224996/fullTextXML"
    - "https://europepmc.org/article/PMC/PMC4224996"
  access: full_text
finding: |
  Bibliographic details and DOI confirmed via the Europe PMC record (PMID 24815612, PMCID PMC4224996);
  full text read on PMC.
  Design: prospective cohort, Midlife in the United States (MIDUS) survey, 14-year mortality follow-up;
  Cox proportional-hazards models.
  Sample: N = 6,163 (7,108 at baseline; 945 excluded for missing data), ages 20-75 (M = 46.9, SD = 12.9),
  91% white; 569 deaths (about 9%) during follow-up.
  Measure: purpose in life = three items from Ryff's Psychological Well-Being scales, 1-7 scale
  (M = 5.50, SD = 1.21, alpha = .36).
  Effect: each 1-SD increase in purpose reduced mortality hazard by 15%, HR = 0.85, 95% CI 0.78-0.93,
  controlling age, sex, education, race, work status and three other well-being markers (positive affect,
  negative affect, positive relations with others). The purpose x age-at-death interaction was
  non-significant (HR = 1.00, p = .32): the protective association was similar for younger, middle-aged
  and older adults, and did not depend on retirement.
  Limitations stated by authors: brief purpose measure with low internal consistency (alpha = .36),
  predominantly white sample, baseline-only assessment, mediators not examined. Health behaviours and
  baseline physical health were not among the listed covariates.
  Location: Method and Results sections, PMC full text.
quotation: ""
quotation_location: ""
fit: partially_supports
fit_note: |
  Supports "purpose in life prospectively predicts lower all-cause mortality, over and above affective
  well-being and positive relations" (which is also some evidence that purpose is a distinct dimension of
  well-being). Gaps relative to the exact claim: (1) purpose is one facet of meaning (Steger's model:
  comprehension plus purpose), not meaning in full; (2) "health" is tested only as mortality; (3) the
  models did not adjust for baseline health, so reverse causation (illness lowering purpose) is not ruled
  out here, though Alimujiang et al. 2019 (opened) adjust for health conditions, functional status and
  depression and find the same direction.
suggested_rewording: "Purpose in life prospectively predicts lower all-cause mortality independent of affective well-being (MIDUS HR 0.85 per SD; meta-analytic RR 0.83)"
replication:
  searched: yes
  status: replicated
  sources:
    - citation: "Cohen, R., Bavishi, C. & Rozanski, A. (2016). Purpose in life and its relationship to all-cause mortality and cardiovascular events: a meta-analysis. Psychosomatic Medicine 78(2), 122-133. DOI 10.1097/psy.0000000000000274; PMID 26630073"
      url_opened: "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:26630073+AND+SRC:MED&resultType=core&format=json"
      note: "Abstract only (LWW page returned 402). 10 prospective studies, 136,265 participants; adjusted pooled RR for all-cause mortality 0.83 (95% CI 0.75-0.91), for cardiovascular events 0.83 (95% CI 0.75-0.92). Heterogeneity statistics not in the abstract. Likely includes Hill & Turiano 2014, so not fully independent of it."
    - citation: "Alimujiang, A., Wiensch, A., Boss, J., et al. (2019). Association between life purpose and mortality among US adults older than 50 years. JAMA Network Open 2(5), e194270. DOI 10.1001/jamanetworkopen.2019.4270"
      url_opened: "https://pmc.ncbi.nlm.nih.gov/articles/PMC6632139/"
      note: "Independent cohort (Health and Retirement Study), N = 6,985, mean age 68.6, 776 deaths 2006-2010; 7-item Ryff purpose scale; lowest vs highest purpose category adjusted HR 2.43 (95% CI 1.57-3.75), adjusting for sociodemographics, health behaviours, health conditions, functional status, depression, anxiety, negative and positive affect, optimism (Table 2)."
retraction_check: clean
retraction_check_url: "WebSearch: 'Purpose in life as a predictor of mortality across adulthood' Hill Turiano retraction OR expression of concern OR corrigendum OR erratum (no notice found); Cohen et al. 2016 also searched, none found"
proposed_strength: Moderate
contested: ""
verified_by: agent
verified_on: 2026-09-26
ratified: false
---

## Notes
Extra record for V10. On the strength rules, the longevity part of the claim (purpose -> mortality)
has a meta-analysis plus an independent replication in a consistent direction and would grade Strong on
its own; the record is held at Moderate because the fit to the exact sentence is partial (meaning vs
purpose; health vs mortality; "independent dimension" only indirectly tested). If the coordinator
adopts the suggested rewording, Strong is defensible for the reworded claim.
