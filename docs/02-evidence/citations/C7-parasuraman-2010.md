---
id: C7
claim_id: C7
claim: "Decision aids bias human choice; the human must stay the decider"
claim_source: "Integral Ethics v2, Core commitments"
citation_as_given: "Parasuraman & Manzey, Human Factors (2010)"
resolved:
  authors: "Parasuraman, R.; Manzey, D. H."
  year: 2010
  title: "Complacency and Bias in Human Use of Automation: An Attentional Integration"
  venue: "Human Factors 52(3), 381-410"
  doi: "10.1177/0018720810376055"
  isbn: ""
  url_opened: "https://api-depositonce.tu-berlin.de/server/api/core/bitstreams/cafd2873-814b-4c59-bab1-addd42e249d2/content"
  urls_attempted:
    - "https://doi.org/10.1177/0018720810376055 (302 redirect to journals.sagepub.com; SAGE not fetched, returns 403 in this session)"
    - "https://depositonce.tu-berlin.de/bitstreams/cafd2873-814b-4c59-bab1-addd42e249d2/download (302 redirect to the url_opened; TU Berlin institutional repository)"
    - "https://api.crossref.org/works?query.bibliographic=Parasuraman+Manzey+2010+Complacency+and+bias+in+human+use+of+automation+attentional+integration&rows=3 (opened; DOI and pagination)"
    - "https://api.semanticscholar.org/graph/v1/paper/DOI:10.1177/0018720810376055?fields=title,authors,year,venue,abstract,externalIds,citationCount (opened; PMID 21077562, 1,512 citations, no abstract)"
    - "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=21077562&rettype=abstract&retmode=text (opened; abstract, no notices)"
  access: full_text
finding: |
  Narrative review and theoretical integration (not a meta-analysis); full text from the TU Berlin
  repository PDF, extracted locally with pdftotext. Journal pagination 381-410.
  Definitions (p. 391): automation bias follows Mosier & Skitka (1996), using a decision aid's output as a
  heuristic replacement for vigilant information seeking and processing. Omission error: the user fails to
  respond to a critical event because the aid did not alert. Commission error: the user follows an incorrect
  recommendation. Bias is inconsequential when the aid is right and costly when it is wrong.
  Evidence integrated ("Evidence for Automation Bias", pp. 392-395):
  Aviation. Mosier et al. (1992): 75% of pilots followed an electronic checklist's wrong engine-shutdown
  recommendation vs 25% with a paper checklist. Mosier et al. (1998), experienced commercial pilots in a
  simulator: omission error rate 55%; on a false engine-fire alert, 100% shut down the engine, and 67%
  reported seeing confirmatory indications that were absent ("phantom memory"). Skitka, Mosier & Burdick
  (1999), nonpilots on W/PANES: 41% omission error rate vs ~3% for unaided participants (97% detected);
  ~65% commission errors on wrong directives. Sarter & Schroeder (2001), in-flight icing aids: with accurate
  aids early buffets 7.87% vs 20.56% unaided and stalls 18.08% vs 30.00%; with inaccurate aids buffets rose to
  73.61% and stalls to 88.89%; the command-vs-status display interaction did not replicate (McGuirl & Sarter
  2006). Health care. McKibbon & Fridsma (2006) and Westbrook et al. (2005): physicians changed a correct
  answer to an incorrect one after consulting electronic sources in 11% and 7% of cases (no non-electronic
  control group). Alberdi et al. (2004), radiologists with a mammography prompting aid: detection of unmarked
  cancers fell from 46% unaided to 21% aided; incorrectly marked cases 66% to 53% (omission bias); no
  commission effect in 2004, weak effect in the 2008 reanalysis (false prompts raised marking probability by
  12.3%). Process control. Bahner et al. (2008), Manzey et al. (2008, 2009): 20% to 50% of participants
  committed a commission error on the aid's first wrong diagnosis (first-failure effect). Command and
  control. Rovira et al. (2007): decision accuracy 89% manual vs 70% with an incorrect aid.
  Moderators (pp. 395-397): accountability for overall performance or accuracy reduced omission and
  commission errors (Skitka, Mosier & Burdick 2000; N=181 nonpilots); a second crewmember had no effect
  (Skitka et al. 2000; Mosier et al. 2001, 48 glass-cockpit pilots); training and instruction interventions had
  no effect on the strength of the bias.
  Conclusion (Summary, p. 397; Abstract, p. 381): automation bias is a robust phenomenon found across
  settings, in naive and expert participants, dependent on the aid's level of automation and reliability, not
  prevented by training or explicit instructions to verify, moderated by perceived accountability, and present
  in individuals and teams. The paper then proposes an integrated attentional model of complacency and bias
  and design options for mitigation. It makes no claim about who should hold decision authority.
quotation: "Automation bias occurs in both naive and expert participants, cannot be prevented by training or instructions"
quotation_location: "Abstract (Results), p. 381"
fit: partially_supports
fit_note: |
  First half of the claim ("Decision aids bias human choice"): supported. The review integrates evidence from
  aviation, medicine, process control and military command-and-control that imperfect automated aids produce
  omission and commission errors in novices and experts alike. Second half ("the human must stay the
  decider"): normative, and not something this paper argues or can support. Worse for the claim as worded,
  the integrated evidence shows that humans who were the deciders still followed wrong aids (100% commission
  in Mosier et al. 1998), and that adding a second human or training did not reduce the bias; the
  mitigators the paper points to are accountability, aid design (status vs command displays), confidence
  information and reliability. The empirical premise and the normative commitment should be separated.
suggested_rewording: "Imperfect automated decision aids induce automation bias (omission and commission errors) in both novice and expert users, and training alone does not prevent it (Parasuraman & Manzey 2010; Goddard et al. 2012; Lyell & Coiera 2017). [Normative commitment stated separately: the human remains the decider.]"
replication:
  searched: yes
  status: replicated
  sources:
    - citation: "Goddard, K.; Roudsari, A.; Wyatt, J. C. (2012). Automation bias: a systematic review of frequency, effect mediators, and mitigators. Journal of the American Medical Informatics Association 19(1), 121-127. doi:10.1136/amiajnl-2011-000089, PMID 21685142"
      url_opened: "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=21077562,21685142&rettype=abstract&retmode=text"
      note: "Abstract only (PubMed HTML and OUP pages blocked). Systematic review of 74 studies; automation bias defined as over-reliance on automation; mediators include cognitive style, experience, trust, workload and time pressure; mitigators include training, emphasising user accountability, and DSS design (display position, confidence indicators, information presentation)."
    - citation: "Lyell, D.; Coiera, E. (2017). Automation bias and verification complexity: a systematic review. Journal of the American Medical Informatics Association 24(2), 423-431. doi:10.1093/jamia/ocw105, PMID 27516495, PMCID PMC7651899"
      url_opened: "https://pmc.ncbi.nlm.nih.gov/articles/PMC7651899/"
      note: "Full text. 890 papers screened, 40 included (34 human factors, 6 health care). Omission errors found in 25 of 31 studies testing them (81%); commission errors in 21 of 23 (91%). Bias occurs in single tasks with high verification complexity, not only under multitasking; only 9 studies tested bias against a manual control."
    - citation: "Wickens, C. D.; Clegg, B. A.; Vieane, A. Z.; Sebok, A. L. (2015). Complacency and Automation Bias in the Use of Imperfect Automation. Human Factors 57(5), 728-739. doi:10.1177/0018720815581940, PMID 25886768"
      url_opened: "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=25886768,39630638,27516495&rettype=abstract&retmode=text"
      note: "Abstract only. Single experiment: after a run of correct advice, a wrong recommendation (automation wrong) impaired accuracy more than absent advice (automation gone). Consistent direction; not a meta-analysis."
retraction_check: clean
retraction_check_url: "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=21077562&rettype=abstract&retmode=text (no retraction, erratum or concern lines); WebSearch for title + retraction found none"
proposed_strength: Moderate
contested: "Phenomenon not disputed; but Lyell & Coiera (2017) note only 9 of 40 included studies tested automation bias against a manual control, so frequency estimates rest on weak comparisons, and Parasuraman & Manzey themselves note the Sarter & Schroeder (2001) display-type interaction failed to replicate."
verified_by: agent
verified_on: 2026-09-26
ratified: false
---

## Notes
- Grade logic: the empirical half is backed by this review plus two systematic reviews in a consistent direction, which would meet the Strong bar on its own; fit is partially_supports because the claim bundles a normative sentence the source cannot bear, so the record proposes Moderate per the strength rules. If the claim is split as suggested, the empirical half could be re-graded Strong on the same evidence.
- Goddard et al. 2012 was reachable only as a PubMed abstract via the E-utilities API; the reported range of bias rates in its abstract was not captured and is not recorded.
