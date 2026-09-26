---
id: V14
claim_id: V14
claim: "Cultural coherence predicts wellbeing"
claim_source: "Integral Ethics v1 §4.3 (value entry) / v2 Candidate value ontology table"
citation_as_given: "Oishi & Diener (2009)"
resolved:
  authors: "Oishi, S.; Diener, E."
  year: 2001
  title: "Goals, Culture, and Subjective Well-Being"
  venue: "Personality and Social Psychology Bulletin, 27(12), 1674-1682; reprinted 2009 as chapter 5 (pp. 93-108) of E. Diener (ed.), Culture and Well-Being, Social Indicators Research Series 38, Springer (chapter DOI 10.1007/978-90-481-2352-0_5)"
  doi: "10.1177/01461672012712010"
  isbn: ""
  url_opened: "https://api.openalex.org/works/doi:10.1177/01461672012712010"
  urls_attempted:
    - "https://api.crossref.org/works?query.bibliographic=Oishi+Diener+Goals+culture+subjective+well-being+2001&rows=3 (opened; metadata for the 2001 article and the 2009 reprint chapter)"
    - "https://journals.sagepub.com/doi/10.1177/01461672012712010 (HTTP 403)"
    - "https://link.springer.com/chapter/10.1007/978-90-481-2352-0_5 (WebFetch redirected to idp.springer.com; curl returned a JavaScript challenge page with no content)"
    - "https://labs.psychology.illinois.edu/~ediener/publication.html (opened; lists the citation, no PDF link)"
    - "https://oishi.socialpsychology.org/publications (opened; lists the citation, no PDF link)"
  access: abstract_only
finding: |
  Abstract only (OpenAlex record; abstract reconstructed from the indexed text). Three studies on independent
  versus interdependent goal pursuit and subjective well-being (SWB) in Asian American and European American
  college students, with a Japanese sample in Study 3. Study 1: independent goal pursuit (pursuing goals for fun
  and enjoyment) increased the SWB benefit of goal attainment among European Americans but not Asian Americans.
  Study 2: goal pursuit to please parents and friends increased the SWB benefit of goal attainment among Asian
  Americans but not European Americans. Study 3: independent goal attainment increased SWB among European
  American students but not Japanese students. Authors' conclusion: independent and interdependent goal
  pursuits have divergent affective consequences across cultures.
  Design: three student studies relating goal attainment and goal motives to SWB (design details are not in
  the abstract).
  Sample: N not reported in the accessed text.
  Effect: a culture x goal-motive interaction on the goal-attainment -> SWB relation; effect sizes not reported
  in the accessed text.
  Location: abstract.
quotation: ""
quotation_location: ""
fit: neighbouring_claim
fit_note: |
  The source does not measure 'cultural coherence' or 'cultural embeddedness' and does not test whether either
  predicts wellbeing. What it reports is a moderation: the wellbeing payoff of ATTAINING a goal is larger when
  the motive for pursuing it (for fun vs to please parents and friends) matches the independent or
  interdependent orientation typical of the student's culture. That is a claim about goal-motive/culture fit
  moderating the attainment-SWB link, not a main effect of coherence on wellbeing. Under a charitable reading
  ('coherence' = fit between one's pursuits and one's culture) it comes closer, but even then the evidence is
  abstract-only, student samples, no effect sizes. If the register means person-culture fit, Fulmer et al. 2010
  (record V14x) is the better-fitting source.
suggested_rewording: "The wellbeing benefit of attaining a goal is larger when the motive for pursuing it (independent vs interdependent) fits the person's cultural orientation."
replication:
  searched: yes
  status: none_found
  sources: []
retraction_check: clean
retraction_check_url: "https://api.openalex.org/works/doi:10.1177/01461672012712010 (is_retracted false); WebSearch '\"Goals, culture, and subjective well-being\" Oishi Diener retraction OR erratum OR correction' returned no notice"
proposed_strength: Hypothesis
contested: ""
verified_by: agent
verified_on: 2026-09-26
ratified: false
---

## Notes
- The citation as given (2009) is the Springer reprint; the original is the 2001 PSPB article. Both records were
  seen in CrossRef; only the abstract (via OpenAlex) could be opened. Sample sizes and effect sizes are therefore
  not recorded.
- Replication: one WebSearch ('Oishi Diener 2001 independent interdependent goal pursuit culture subjective
  well-being replication OR meta-analysis') found no direct replication or meta-analysis of the culture x
  goal-motive interaction. Not opened: Sheldon et al. 2004 (self-concordance and SWB in four cultures) surfaced
  in search but tests a different proposition.
