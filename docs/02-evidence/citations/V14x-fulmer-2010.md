---
id: V14x
claim_id: V14
claim: "Cultural coherence predicts wellbeing"
claim_source: "Integral Ethics v1 §4.3 (value entry) / v2 Candidate value ontology table"
citation_as_given: "none (added by the verifier as a better-fitting source for V14)"
resolved:
  authors: "Fulmer, C. A.; Gelfand, M. J.; Kruglanski, A. W.; Kim-Prieto, C.; Diener, E.; Pierro, A.; Higgins, E. T."
  year: 2010
  title: "On 'Feeling Right' in Cultural Contexts: How Person-Culture Match Affects Self-Esteem and Subjective Well-Being"
  venue: "Psychological Science, 21(11), 1563-1569"
  doi: "10.1177/0956797610384742"
  isbn: ""
  url_opened: "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=TITLE:%22feeling%20right%20in%20cultural%20contexts%22&resultType=core&format=json"
  urls_attempted:
    - "https://api.openalex.org/works/doi:10.1177/0956797610384742?select=doi,title,publication_year,is_retracted (opened; retraction flag only)"
  access: abstract_only
finding: |
  Abstract only (Europe PMC record; PMID 20876880). Proposes a person-culture match hypothesis: when a person's
  personality matches the prevalent personalities in a culture, culture amplifies the positive effect of that
  personality on self-esteem and subjective well-being.
  Design: two studies, multilevel random-coefficient analyses of individual-level trait -> wellbeing relations
  with culture-level trait prevalence as moderator.
  Sample: more than 7,000 individuals from 28 societies (as stated in the abstract).
  Effect: where a trait-wellbeing (or trait-self-esteem) relation exists at the individual level, it is stronger
  in cultures high on that trait; replicated across extraversion, promotion focus and locomotion regulatory
  mode. Effect sizes not given in the abstract.
  Location: abstract.
quotation: ""
quotation_location: ""
fit: partially_supports
fit_note: |
  This is the closest published test of 'cultural coherence predicts wellbeing' if coherence means
  person-culture match. It supports a moderation form (match amplifies the wellbeing benefit of one's traits)
  rather than a main effect of match on wellbeing, and it is abstract-only. The claim would need to define
  'cultural coherence' as person-culture match for this source to fit.
suggested_rewording: "Person-culture match (having traits that are prevalent in one's culture) amplifies the wellbeing benefits of those traits."
replication:
  searched: yes
  status: mixed
  sources:
    - citation: "Gebauer, J. E., Eck, J., Entringer, T. M., Bleidorn, W., Rentfrow, P. J., Potter, J., & Gosling, S. D. (2020). The well-being benefits of person-culture match are contingent on basic personality traits. Psychological Science, 31(10), 1283-1293. doi 10.1177/0956797620951115"
      url_opened: "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=PMCID:PMC7549288&resultType=core&format=json"
      note: "Abstract only. Self-reports from 2,672,820 people across 102 countries and informant reports from 850,877 across 61 countries. The person-culture match effect is moderated by basic traits; people low in communion and high in agency show no wellbeing benefit, and some profiles show costs. The authors say the results 'help explain failures to replicate it'."
retraction_check: clean
retraction_check_url: "https://api.openalex.org/works/doi:10.1177/0956797610384742?select=doi,title,publication_year,is_retracted (is_retracted false); Europe PMC record shows no correction or retraction fields"
proposed_strength: Hypothesis
contested: "Gebauer et al. 2020 (N > 3.5 million) report that the person-culture match wellbeing benefit is contingent on personality, absent for some trait profiles, and refer to failures to replicate it."
verified_by: agent
verified_on: 2026-09-26
ratified: false
---

## Notes
- Extra record: not cited in v1; added because V14's cited source (Oishi & Diener) does not test the stated claim.
- Grade is Hypothesis per the coordinator addendum (abstract-only partial support on a single paper, with mixed
  replication). If the full text is opened and the claim is reworded to person-culture match, Moderate would be
  reachable; Strong would require the moderating conditions found by Gebauer et al. to be built into the claim.
