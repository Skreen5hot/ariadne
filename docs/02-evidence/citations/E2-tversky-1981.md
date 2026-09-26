---
id: E2
claim_id: E2
claim: "Framing changes choice with facts held fixed"
claim_source: "Integral Ethics v2, Cognitive perspectives as instruments"
citation_as_given: "Tversky & Kahneman, Science (1981)"
resolved:
  authors: "Tversky, A.; Kahneman, D."
  year: 1981
  title: "The framing of decisions and the psychology of choice"
  venue: "Science, 211(4481), 453-458"
  doi: "10.1126/science.7455683"
  isbn: ""
  url_opened: "https://psych.hanover.edu/classes/cognition/papers/tversky81.pdf"
  urls_attempted:
    - "https://api.crossref.org/works?query.bibliographic=Tversky+Kahneman+The+framing+of+decisions+and+the+psychology+of+choice+Science+1981&rows=3 (HTTP 429)"
    - "https://doi.org/10.1126/science.7455683 (redirects to science.org)"
    - "https://www.science.org/doi/10.1126/science.7455683 (HTTP 403)"
    - "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=7455683&retmode=xml (opened; PMID 7455683, abstract and DOI confirmed)"
  access: full_text
finding: |
  Source opened is a JSTOR scan of the Science article hosted by Hanover College; text extracted locally with pdftotext. Bibliographic data (title, authors, journal, volume, issue, pages, DOI) confirmed against the PubMed record (PMID 7455683).
  Design: brief written questionnaires answered in classroom settings by students at Stanford University and the University of British Columbia; each framing version given to a different group (between-subjects). N and percentage choosing each option are printed in brackets after each problem (p. 453).
  Sample (Asian disease pair): Problem 1, N = 152; Problem 2, N = 155.
  Effect (p. 453): Problem 1 (gain frame) - Program A "200 people will be saved" chosen by 72%; Program B "1/3 probability that 600 people will be saved, and 2/3 probability that no people will be saved" chosen by 28%. Problem 2 (loss frame, same cover story) - Program C "400 people will die" chosen by 22%; Program D "1/3 probability that nobody will die, and 2/3 probability that 600 people will die" chosen by 78%. The authors state the two problems are effectively identical, differing only in whether outcomes are described as lives saved or lives lost, and that the change of description shifts the majority from risk aversion to risk seeking; they add that the reversal was observed in several groups of respondents including university faculty and physicians (p. 453). No inferential statistic is reported for this pair; proportions only.
  Further problems (3-10, pp. 453-457) show analogous reversals for monetary outcomes, hypothetical and real (e.g., Problem 3, N = 150; Problem 4, N = 86).
  Location: Asian disease problems and percentages, p. 453, columns 2-3.
quotation: ""
quotation_location: ""
fit: supports
fit_note: |
  The Asian disease pair holds the outcomes and probabilities fixed and changes only the description (saved vs. die); the majority choice reverses (72% choose the sure option in the gain frame, 22% in the loss frame). That is exactly "framing changes choice with facts held fixed". Caveats: hypothetical choices, student samples, no test statistic in the original; these are answered by the large-scale replication and meta-analytic evidence below.
suggested_rewording: ""
replication:
  searched: yes
  status: replicated
  sources:
    - citation: "Klein, R. A., et al. (2014). Investigating variation in replicability: A 'many labs' replication project. Social Psychology, 45(3), 142-152. doi 10.1027/1864-9335/a000178"
      url_opened: "https://stanford.edu/~knutson/jdm/klein14.pdf"
      note: "Author/library-hosted PDF, text extracted locally. 36 samples, 6,344 participants in total. Table 2, row 'Gain vs. loss framing': original ES 1.13 (95% CI 0.89-1.37); median replication ES 0.58; aggregate replication ES 0.62 (99% CI 0.52-0.71) and 0.60 (99% CI 0.53-0.67) in the two aggregate columns; proportion of samples with p < .05 in the same direction 0.86, ns 0.14, opposite direction 0.00; aggregate test chi-square(1) = 516.4, N = 6,271, p < .001. Table 3: heterogeneity Q(35) = 37.01, p = .69, I-squared = 0. Effect replicated in direction; magnitude about half the original."
    - citation: "Steiger, A.; Kuhberger, A. (2018). A meta-analytic re-appraisal of the framing effect. Zeitschrift fur Psychologie, 226(1), 45-55. doi 10.1027/2151-2604/a000321"
      url_opened: "https://ouci.dntb.gov.ua/en/works/7A23eG84/"
      note: "Abstract page (Hogrefe landing page returned HTTP 403; volume/issue taken from the Google Scholar lookup URL shown on the search page, not verified on the publisher site). p-curve reanalysis of Kuhberger's 1998 meta-analysis: bias-corrected overall d = 0.52 (vs. d = 0.31 reported by Kuhberger 1998); no evidence of intense p-hacking; consistent with Many Labs d = 0.60 and a 2016 meta-analysis d = 0.56. Authors conclude risky-choice framing effects are reliable and robust."
retraction_check: clean
retraction_check_url: "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=%2810694957%5Buid%5D+OR+7455683%5Buid%5D+OR+6527215%5Buid%5D%29+AND+%28%22retracted+publication%22%5Bpt%5D+OR+%22retraction+of+publication%22%5Bpt%5D%29"
proposed_strength: Strong
contested: ""
verified_by: agent
verified_on: 2026-09-26
ratified: false
---

## Notes
- PubMed retraction query returned Count 0 for PMID 7455683 with publication type "retracted publication"; a web search for the title plus "retraction" / "expression of concern" also found nothing.
- The replicated effect (d about 0.6 across 36 samples) is roughly half the size reported in the original (d = 1.13), but direction and significance are robust and between-sample heterogeneity in Many Labs was zero. This is a magnitude qualification, not a dispute.
- The Steiger & Kuhberger volume/issue could not be verified on the publisher page (403); DOI and pages 45-55 were shown on the OUCI page.
