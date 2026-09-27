---
id: V05
claim_id: V05
claim: "Positive experiences independent contributor to wellbeing"
claim_source: "Integral Ethics v1 §4.3 (value entry) / v2 Candidate value ontology table"
citation_as_given: "Diener, Suh, Lucas & Smith (1999)"
resolved:
  authors: "Diener, E.; Suh, E. M.; Lucas, R. E.; Smith, H. L."
  year: 1999
  title: "Subjective well-being: Three decades of progress"
  venue: "Psychological Bulletin 125(2), 276-302"
  doi: "10.1037/0033-2909.125.2.276"
  isbn: ""
  url_opened: "http://media.rickhanson.net/Papers/SubjectiveWell-BeingDiener.pdf"
  urls_attempted:
    - "https://api.crossref.org/works?query.bibliographic=Diener+Suh+Lucas+Smith+1999+Subjective+well-being+three+decades+of+progress+Psychological+Bulletin&rows=3"
    - "https://api.semanticscholar.org/graph/v1/paper/DOI:10.1037/0033-2909.125.2.276?fields=title,authors,year,venue,abstract,externalIds,citationCount"
    - "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=TITLE:%22Subjective%20well-being%3A%20three%20decades%20of%20progress%22&resultType=core&format=json"
    - "https://psycnet.apa.org/record/1999-10106-007"
  access: full_text
finding: |
  Type: narrative review. DOI confirmed via CrossRef and Semantic Scholar (abstract withheld
  there; not indexed in Europe PMC; PsycNet page did not load). Full text read from a third-party
  hosted copy of the APA typeset PDF, downloaded with curl and read with pdftotext (see Notes).
  Abstract (p. 276): the field should develop theories explaining why variables "differentially
  influence the different components of SWB (life satisfaction, pleasant affect, and unpleasant
  affect)". Introduction (p. 276): researchers once treated SWB as monolithic, but "it is now
  clear that there are separable components".
  Components of SWB (p. 277, Table 1): SWB is "a broad category of phenomena" comprising emotional
  responses (pleasant affect: joy, elation, contentment, pride, affection, happiness, ecstasy;
  unpleasant affect: guilt, sadness, anxiety, anger, stress, depression, envy), domain
  satisfactions and global life-satisfaction judgements; components "often correlate
  substantially, suggesting the need for the higher order factor". Evidence cited for
  separability: Bradburn & Caplovitz (1965) two independent affect factors; Diener & Emmons
  (1984) pleasant and unpleasant affect increasingly separate as the time frame lengthens;
  Diener, Smith & Fujita (1995) SEM with multimethod measurement, "moderately inversely
  correlated but clearly separable"; Andrews & Withey (1976) life satisfaction a separate factor;
  Lucas, Diener & Suh (1996) multitrait-multimethod analysis showing pleasant affect, unpleasant
  affect and life satisfaction separable, with validity coefficients exceeding cross-construct
  correlations over two years and across self- and informant reports. The authors note the
  independence of momentary affect "is still debated" and recommend assessing components
  separately.
  Variety or richness of experience: a full-text search for variety, novelty and richness found
  no passage treating breadth or richness of experience as a contributor to SWB.
  Sample: not applicable (review); effect sizes for the cited studies are not reported in the text.
quotation: "it is now clear that there are separable components that exhibit unique patterns of relations with different variables"
quotation_location: "p. 276, introduction"
fit: partially_supports
fit_note: |
  Supports the defensible core of the sentence: pleasant (positive) affect is a separable
  component of subjective wellbeing, not reducible to the absence of unpleasant affect or to life
  satisfaction, on cited factor-analytic and multitrait-multimethod evidence. Two gaps: (1) the
  source treats positive affect as a component of SWB, not as a "contributor to" wellbeing in a
  causal sense; (2) the value label "experiential richness" (variety or richness of experience)
  is not what the paper is about at all; for that construct the source is neighbouring at best.
suggested_rewording: "Pleasant affect is a separable component of subjective wellbeing, not reducible to the absence of unpleasant affect or to life satisfaction."
replication:
  searched: yes
  status: mixed
  sources:
    - citation: "Busseri, M. A. (2015). Toward a resolution of the tripartite structure of subjective well-being. Journal of Personality 83(4), 413-428. DOI 10.1111/jopy.12116; PMID 25039466"
      url_opened: "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:25039466%20AND%20SRC:MED&resultType=core&format=json"
      note: "Abstract: longitudinal MIDUS data, N = 3,707 US adults aged 20-75; tests four structural models (separate components, hierarchical, causal system, composite); the components show joint relatedness and independence within and across time, and the models differ in how well they accommodate this; no single model declared definitive."
    - citation: "Busseri, M. A. & Sadava, S. W. (2011). A review of the tripartite structure of subjective well-being: implications for conceptualization, operationalization, analysis, and synthesis. Personality and Social Psychology Review 15(3), 290-314. DOI 10.1177/1088868310391271; PMID 21131431"
      url_opened: "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:21131431%20AND%20SRC:MED&resultType=core&format=json"
      note: "Abstract: five competing structural conceptualisations of SWB (three separate components, hierarchical, causal system, composite, configurations); 'it is premature to propose a definitive structure of SWB'. Separability of the three components is common ground; how they combine is unresolved."
retraction_check: clean
retraction_check_url: "WebSearch: \"Subjective well-being: three decades of progress\" Diener 1999 retraction (no notice in results)"
proposed_strength: Moderate
contested: "The tripartite structure of SWB is unresolved (Busseri & Sadava 2011): the components are separable but substantially correlated, and whether they are best modelled as separate, hierarchical, causal or composite remains open."
verified_by: agent
verified_on: 2026-09-26
ratified: false
---

## Notes
The PDF at the url_opened is a copy of the APA typeset article hosted on a third-party site
(WebFetch failed on a TLS certificate mismatch; the file was downloaded with curl over http and
read via pdftotext). Page numbers are the journal's. A meta-analysis of the PA-NA-LS associations
exists (Busseri 2018, Personality and Individual Differences 122, 68-71, DOI 10.1016/j.paid.2017.10.003,
metadata seen on CrossRef) but its abstract was withheld from the APIs I could reach, so it is not
cited as a replication source. If the ratifier keeps the value label "experiential richness", a
different source is needed; this paper does not address variety or richness of experience.
