---
id: V15
claim_id: V15
claim: "Commitment predicts relationship satisfaction and vocational success"
claim_source: "Integral Ethics v1 §4.3 (value entry) / v2 Candidate value ontology table"
citation_as_given: "Rusbult, Martz & Agnew (1998)"
resolved:
  authors: "Rusbult, C. E.; Martz, J. M.; Agnew, C. R."
  year: 1998
  title: "The Investment Model Scale: Measuring commitment level, satisfaction level, quality of alternatives, and investment size"
  venue: "Personal Relationships, 5(4), 357-387 (CrossRef and OpenAlex both give 357-387; the citation as given and several secondary lists give 357-391)"
  doi: "10.1111/j.1475-6811.1998.tb00177.x"
  isbn: ""
  url_opened: "https://api.openalex.org/works/doi:10.1111/j.1475-6811.1998.tb00177.x"
  urls_attempted:
    - "https://api.crossref.org/works?query.bibliographic=Rusbult+Martz+Agnew+1998+The+Investment+Model+Scale+Personal+Relationships&rows=4 (opened; metadata)"
    - "https://doi.org/10.1111/j.1475-6811.1998.tb00177.x (redirect to Wiley)"
    - "https://onlinelibrary.wiley.com/doi/10.1111/j.1475-6811.1998.tb00177.x (HTTP 403)"
    - "https://api.semanticscholar.org/graph/v1/paper/DOI:10.1111/j.1475-6811.1998.tb00177.x?fields=title,authors,year,venue,abstract,externalIds,openAccessPdf,citationCount (opened; abstract elided by publisher, no OA PDF)"
    - "https://repositorio.iscte-iul.pt/bitstream/10071/7272/5/The%20Investment%20Model%20Scale%20(IMS).pdf (WebFetch and curl both returned a DSpace HTML shell, not the PDF)"
  access: abstract_only
finding: |
  Abstract only (OpenAlex record). Three studies evaluated the reliability and validity of the Investment Model
  Scale, which measures commitment level and three bases of dependence: satisfaction level, quality of
  alternatives and investment size. All three studies showed good internal consistency for each construct;
  principal components analyses showed the items loading on separate factors. Studies 2 and 3 related the model
  variables to other relationship measures and to personal dispositions: model variables were moderately
  associated with measures of superior couple functioning (dyadic adjustment, trust, inclusion of other in the
  self) and essentially unrelated to personal dispositions. Study 3 showed that earlier measures of the model
  variables predicted later dyadic adjustment and later relationship status (persisted vs ended).
  Design: three scale-validation studies, the third with a longitudinal follow-up.
  Sample: N not reported in the accessed text. (Le & Agnew 2003, Table 1, opened for the replication check, lists
  Rusbult, Martz & Agnew 1998 Study 1 as N = 415 and Study 3 as N = 313; those figures come from the 2003
  meta-analysis, not from the 1998 paper itself.)
  Effect: not reported in the abstract. (Le & Agnew 2003, Table 1, gives for Study 1 correlations of commitment
  with satisfaction .84, alternatives -.62, investments .33, and with stay-leave .53; for Study 3 .75, -.60, .60.)
  Location: abstract.
quotation: ""
quotation_location: ""
fit: partially_supports
fit_note: |
  Two problems. (1) Direction: in the Investment Model, satisfaction is a PREDICTOR of commitment (one of its
  three bases), not an outcome of it. What commitment predicts in this source is persistence (stay/leave) and,
  jointly with the other model variables, later dyadic adjustment (Study 3). So 'commitment predicts
  relationship satisfaction' is supported only in the adjacent form 'commitment predicts relationship
  persistence and later adjustment'. (2) 'Vocational success' does not appear in this source at all; the
  workplace evidence in Le & Agnew 2003 concerns job COMMITMENT and job stay/leave, not success. The
  relationship half is therefore partially supported; the vocational half is unsupported by this citation.
suggested_rewording: "Satisfaction, investment and poor alternatives predict relationship commitment; commitment in turn predicts relationship persistence (stay/leave). Any claim about vocational success needs a separate source."
replication:
  searched: yes
  status: replicated
  sources:
    - citation: "Le, B., & Agnew, C. R. (2003). Commitment and its theorized determinants: A meta-analysis of the Investment Model. Personal Relationships, 10(1), 37-57. doi 10.1111/1475-6811.00035"
      url_opened: "http://static1.1.sqspcdn.com/static/f/984219/13434258/1311966710690/Le_Agnew_2003_PR.pdf"
      note: "Full text (read via pdftotext from the WebFetch-saved file). 52 studies, 60 independent samples, N = 11,582. Weighted correlations with commitment: satisfaction r = .68 [.67, .69], alternatives r = -.48 [-.49, -.46], investments r = .46 [.45, .48] (Figure 1; Results p. 45); the three bases jointly account for 61% of the variance in commitment (R2 = .61 [.59, .63], N = 4360, k = 32; p. 45). Commitment predicts later stay-leave behaviour r = .47 [.43, .50] (N = 1720; 12 studies, 10 romantic and 2 job; p. 45). The model is significantly weaker for workplace than for interpersonal commitment (job-only: satisfaction .51, alternatives -.26, investments .34; Table 2, p. 46; Z = 5.36, p < .001, p. 47). Same lab as the original (Agnew is a co-author of both)."
retraction_check: clean
retraction_check_url: "https://api.openalex.org/works/doi:10.1111/j.1475-6811.1998.tb00177.x (is_retracted false); WebSearch '\"Investment Model Scale\" Rusbult Martz Agnew 1998 retraction OR erratum OR correction' returned no notice"
proposed_strength: Hypothesis
contested: ""
verified_by: agent
verified_on: 2026-09-26
ratified: false
---

## Notes
- Grade follows coordinator addendum item 2: abstract-only partial support on a single primary study is
  Hypothesis. The Le & Agnew meta-analysis is strong evidence for the REWORDED claim (bases -> commitment ->
  persistence), not for the claim as written.
- Vocational lead, not opened for content: Meyer, Stanley, Herscovitch & Topolnytsky (2002), 'Affective,
  continuance, and normative commitment to the organization: A meta-analysis of antecedents, correlates, and
  consequences', Journal of Vocational Behavior 61(1), 20-52, doi 10.1006/jvbe.2001.1842 (OpenAlex metadata
  opened; abstract not available there or on Semantic Scholar). If 'vocational success' is kept, that is where to
  look, and it concerns organizational commitment, a different construct from relationship commitment.
- Page discrepancy (357-387 vs 357-391) noted above; the DOI is unambiguous.
