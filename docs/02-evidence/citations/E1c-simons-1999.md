---
id: E1c
claim_id: E1
claim: "People routinely miss available, morally relevant information"
claim_source: "Integral Ethics v2, Cognitive perspectives as instruments"
citation_as_given: "Simons & Chabris (1999)"
resolved:
  authors: "Simons, D. J.; Chabris, C. F."
  year: 1999
  title: "Gorillas in our midst: sustained inattentional blindness for dynamic events"
  venue: "Perception, 28(9), 1059-1074"
  doi: "10.1068/p281059"
  isbn: ""
  url_opened: "http://www.chabris.com/Simons1999.pdf"
  urls_attempted:
    - "https://api.crossref.org/works?query.bibliographic=Simons+Chabris+Gorillas+in+our+midst+...&rows=3 (opened; lists both 10.1068/p281059 and a duplicate registration 10.1068/p2952 for the same article)"
    - "https://pubmed.ncbi.nlm.nih.gov/10694957/ (reCAPTCHA page)"
    - "https://journals.sagepub.com/doi/10.1068/p281059 (HTTP 403)"
    - "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=10694957&retmode=xml (opened; PMID 10694957, abstract and DOI 10.1068/p281059 confirmed)"
  access: full_text
finding: |
  Author-hosted PDF of the published article (journal pagination 1059-1074 visible; text extracted locally with pdftotext).
  Design: one experiment, 2 x 2 x 2 x 2 between-subjects factorial (video style Transparent vs Opaque; unexpected event Umbrella Woman vs Gorilla; attended team White vs Black; monitoring task Easy = count passes vs Hard = separate counts of bounce and aerial passes), 16 conditions (Method, section 2, pp. 1066-1067). Observers watched a 75-s basketball-passing video; the unexpected event lasted 5 s. Noticing was assessed by four escalating post-video questions.
  Sample: 228 observers tested, almost all undergraduates; 36 discarded (14 already knew the paradigm, 9 lost count, 7 incomplete records, 5 uninterpretable answers, 1 outlier), leaving 192, 12 per condition (Results, section 3, p. 1068).
  Effect: overall 54% noticed and 46% failed to notice the unexpected event (p. 1068). Opaque 67% vs Transparent 42% noticed, chi-square(1) = 12.08, p < 0.001; Easy 64% vs Hard 45%, chi-square(1) = 6.80, p = 0.009; Umbrella Woman 65% vs Gorilla 44%, chi-square(1) = 8.39, p = 0.004; the Gorilla was noticed more when observers attended the Black team (58%) than the White team (27%), chi-square(1) = 9.58, p = 0.002 (pp. 1068-1069). Table 1 (p. 1068) gives per-condition noticing rates; Opaque/Gorilla row: White/Easy 42%, Black/Easy 83%, White/Hard 50%, Black/Hard 58%. Additional condition (p. 1070, Figure 3): a gorilla that stops, faces the camera and thumps its chest for 9 s; 12 new observers, White team, Easy task; 50% noticed.
  Location: Table 1 and Results, pp. 1068-1069; Discussion point (i), p. 1069; chest-thumping condition, p. 1070.
quotation: "Approximately half of observers fail to notice an ongoing and highly salient but unexpected event while they are engaged in a primary monitoring task."
quotation_location: "Discussion, section 4, point (i), p. 1069"
fit: neighbouring_claim
fit_note: |
  The study shows that people engaged in an attention-demanding task frequently fail to notice a salient, unexpected visual event. Nothing in the stimulus, task or measure is morally relevant, and no decision or judgment depends on the missed event; "information" here is a perceptual event, not decision-relevant content. It therefore supports the neighbouring claim "under attentional load, roughly half of observers fail to notice a salient, unexpected visual event (inattentional blindness)", which is a mechanism one might extend to moral perception but does not itself establish that people miss morally relevant information. Better-fitting source: Gino & Bazerman (2009), "When misconduct goes unnoticed" (see record E1x), which tests failure to notice gradual unethical behaviour - though its Study 1 has a failed preregistered replication.
suggested_rewording: "People routinely fail to notice available information, even when it is salient (inattentional blindness); whether this extends to morally relevant information requires direct evidence."
replication:
  searched: yes
  status: replicated
  sources:
    - citation: "Drew, T.; Vo, M. L. H.; Wolfe, J. M. (2013). The invisible gorilla strikes again: Sustained inattentional blindness in expert observers. Psychological Science, 24(9), 1848-1853. doi 10.1177/0956797613479386"
      url_opened: "https://pmc.ncbi.nlm.nih.gov/articles/PMC3964612/"
      note: "Full text (PMC). 24 radiologists performing a familiar lung-nodule search; a gorilla 48 times the size of an average nodule inserted in the last case; 83% (20/24) failed to notice it, and eye-tracking showed most of them looked directly at it; 25 naive observers, 100% missed. Framed explicitly as an extension of Simons & Chabris (1999)."
    - citation: "Kreitz, C.; Furley, P.; Memmert, D.; Simons, D. J. (2015). Inattentional blindness and individual differences in cognitive abilities. PLOS ONE, 10(8), e0134675. doi 10.1371/journal.pone.0134675"
      url_opened: "https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0134675"
      note: "Full text. Study 1 N = 116, Study 2 N = 198. Miss rates for the unexpected object: static cross task 53% (near) / 71% (far) in Study 1 (Table 2), 38% / 66% in Study 2 (Table 4); dynamic tracking task 34% / 63% (Table 5). Independent lab; same order of magnitude as the 46% miss rate in the original."
    - citation: "Simons, D. J.; Hults, C. M.; Ding, Y. (2024). Individual differences in inattentional blindness. Psychonomic Bulletin & Review, 31(4), 1471-1502. doi 10.3758/s13423-023-02431-x"
      url_opened: "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=38182856&retmode=xml"
      note: "PubMed abstract. Meta-analysis of 31 records / 74 samples with individual-difference measures; documents the breadth of the inattentional-blindness literature; no overall noticing rate reported in the abstract. Not independent of the original's first author."
retraction_check: clean
retraction_check_url: "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=%2810694957%5Buid%5D+OR+7455683%5Buid%5D+OR+6527215%5Buid%5D%29+AND+%28%22retracted+publication%22%5Bpt%5D+OR+%22retraction+of+publication%22%5Bpt%5D%29"
proposed_strength: Hypothesis
contested: ""
verified_by: agent
verified_on: 2026-09-26
ratified: false
---

## Notes
- This source is real, robust and repeatedly replicated, but it contributes nothing to the claim as worded. Per the verifier rules, proposed_strength here is derived from the other evidence found for the exact claim: E1a (Chugh & Bazerman 2007, partially_supports, Moderate). If E1a is judged not to reach Moderate, this record should be read as Hypothesis for the exact claim.
- CrossRef lists two DOIs for the same article (10.1068/p281059 and 10.1068/p2952); PubMed and SAGE use 10.1068/p281059.
- PubMed retraction query returned Count 0 for PMID 10694957; web search for the title plus "retraction" / "expression of concern" found nothing.
- Coordinator note (2026-09-26): proposed_strength changed from Moderate to Hypothesis. A record's grade states what this source contributes to the stated claim; a neighbouring source contributes nothing. The claim-level grade for E1 is set in register.yaml from E1a and E1b.
