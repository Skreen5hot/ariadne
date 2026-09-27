---
id: F2b
claim_id: F2
claim: "Added perspectives help only when diverse"
claim_source: "Integral Ethics v2, Foundations: perspectival realism"
citation_as_given: "Thompson (2014) critique"
resolved:
  authors: "Thompson, A."
  year: 2014
  title: "Does Diversity Trump Ability? An Example of the Misuse of Mathematics in the Social Sciences"
  venue: "Notices of the American Mathematical Society 61(9): 1024-1030, October 2014"
  doi: "10.1090/noti1163"
  isbn: ""
  url_opened: "https://web.archive.org/web/2022id_/https://www.ams.org/notices/201409/rnoti-p1024.pdf"
  urls_attempted:
    - "https://www.ams.org/notices/201409/rnoti-p1024.pdf (HTTP 403 to WebFetch; curl returned an HTML bot-check page instead of the PDF)"
    - "https://www.ams.org/journals/notices/201409/rnoti-p1024.pdf (HTTP 403)"
    - "https://api.crossref.org/works?query.bibliographic=Does+Diversity+Trump+Ability+Thompson+Notices+American+Mathematical+Society+2014&rows=3 (opened; metadata and DOI 10.1090/noti1163)"
    - "https://api.semanticscholar.org/graph/v1/paper/DOI:10.1090/noti1163 (opened; metadata only, abstract elided)"
  access: full_text
finding: |
  Design: a mathematical critique with a re-run of the Hong-Page simulation. No participants.
  What it argues, by section and page:
  - "A Mathematical Theorem" (pp. 1025-1026): Theorem 1 of Hong & Page is incorrect as stated because the informal
    reading of Assumption 2 ("when one agent gets stuck, there is always another that can find an improvement") fails
    unless the value function is one-to-one; a four-point counterexample is given in the Appendix (p. 1029). Once
    corrected, the theorem reduces to the observation that the full collection of agents always reaches the optimum
    while copies of a single best agent do not. The sample sizes N and N1 in the theorem can be far larger than the
    number of distinct agents, so the theorem says nothing about any proper subset of the pool and nothing about
    hiring (p. 1026).
  - "A Computational Experiment" (pp. 1027-1028): she reproduced the simulation (n = 2000, l = 20, k = 3; pool of
    20 x 19 x 18 = 6840 agents) and confirms that ten random agents outperform the ten best. She argues the theorem's
    hypotheses are not met by the experiment; that the result illustrates the known effectiveness of randomized
    algorithms; that the authors' "diversity" measure is correlational, not causal; and that in her re-run,
    maximally "diverse" groups of ten performed worse than the median of 200 random groups (p. 1028). The same
    measure relabelled "hostility" would license the conclusion that hostility trumps ability (p. 1028).
  - "Summary of Problems" (p. 1028): (1) Theorem 1 incorrect as stated; (2) trivial once corrected; (3) unrelated to
    the experiment; (4) the experiment is a contrived optimisation illustrating that random algorithms work.
  - Conclusion (p. 1029): the claim that diversity trumps ability has been given no foundation by the paper.
  Concession: the simulation result itself (random beats best) is reproduced, not disputed.
quotation: "The claim that diversity trumps ability has been given no foundation by Hong and Page's paper."
quotation_location: "p. 1029, 'Who Uses this Result?'"
fit: does_not_support
fit_note: |
  This is a critique of F2a, entered in the register as such. It does not support the claim; it removes the
  Hong-Page theorem as a formal ground for it, leaving the simulation result standing but contested in
  interpretation. Its own conclusions are in turn disputed: Kuehn (2017) calls her mathematical criticisms
  incorrect or irrelevant while crediting the randomization point, and Singer (2019), re-running the model at
  scale, reports that maximally diverse groups do outperform random groups, contrary to her p. 1028 result. Net
  effect on F2: the formal ground is unsettled either way; F2 cannot rest on the theorem.
suggested_rewording: ""
replication:
  searched: yes
  status: mixed
  sources:
    - citation: "Kuehn, D. (2017). Diversity, Ability, and Democracy: A Note on Thompson's Challenge to Hong and Page. Critical Review 29(1): 72-87. doi 10.1080/08913811.2017.1288455"
      url_opened: "https://api.openalex.org/works/doi:10.1080/08913811.2017.1288455"
      note: "Abstract only. Thompson's mathematical criticisms judged 'incorrect, misleading, or irrelevant to the validity of the theorem'; her discussion of randomization judged valuable."
    - citation: "Singer, D. J. (2019). Diversity, Not Randomness, Trumps Ability. Philosophy of Science 86(1). Penultimate draft dated 26 March 2018."
      url_opened: "https://www.danieljsinger.com/papers/Singer%20-%20Diverstiy,%20Not%20Randomness,%20Trumps%20Ability%20(draft).pdf"
      note: "Full text of the author's draft. Section 1 restates Thompson's argument (her p. 1028 maximal-diversity result); Section 4 reports that in his re-run maximally diverse groups typically outperform random groups and that a coverage measure of diversity correlates r = 0.553 with group competence. He also notes (p. 2, footnote 3) that Kuehn canvasses defences that accept most of Thompson's technical claims."
retraction_check: clean
retraction_check_url: "https://api.crossref.org/works/10.1090/noti1163 (no update-to or relation entries; checked 2026-09-26)"
proposed_strength: Argued only
contested: "Disputed by Kuehn 2017 and Singer 2019; Singer's re-run reverses Thompson's maximal-diversity result."
verified_by: agent
verified_on: 2026-09-26
ratified: false
---

## Notes
- Verified by the coordinator after the batch agent was cut off. The AMS site blocks automated fetches; the PDF was obtained from the Internet Archive's copy of the same URL and read with pdftotext. Page numbers are the journal's.
- The register lists this critique as a citation for F2. It is better recorded as a dispute in contested.md than as evidence; the record exists so that the dispute is traceable.
