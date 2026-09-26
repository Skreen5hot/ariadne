---
id: E7b
claim_id: E7
claim: "Integrating many views outperforms single-model expertise"
claim_source: "Integral Ethics v2, Cognitive perspectives as instruments"
citation_as_given: "Mellers et al. (2014)"
resolved:
  authors: "Mellers, B.; Ungar, L.; Baron, J.; Ramos, J.; Gurcay, B.; Fincher, K.; Scott, S. E.; Moore, D.; Atanasov, P.; Swift, S. A.; Murray, T.; Stone, E.; Tetlock, P. E."
  year: 2014
  title: "Psychological Strategies for Winning a Geopolitical Forecasting Tournament"
  venue: "Psychological Science 25(5), 1106-1115"
  doi: "10.1177/0956797614524255"
  isbn: ""
  url_opened: "https://learnmoore.org/papers/Mellers%20et%20al%202014.pdf"
  urls_attempted:
    - "https://api.crossref.org/works?query.bibliographic=Mellers+2014+Psychological+strategies+for+winning+a+geopolitical+forecasting+tournament&rows=3 (opened; DOI and pagination)"
    - "https://api.semanticscholar.org/graph/v1/paper/DOI:10.1177/0956797614524255?fields=title,authors,year,venue,abstract,externalIds,citationCount (opened; PubMed ID 24659192, no abstract)"
    - "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=29620401,24659192&rettype=abstract&retmode=text (opened; abstract, no notices)"
  access: full_text
finding: |
  Author-hosted PDF (co-author D. Moore's site); text extracted locally with pdftotext. Page numbers below are
  the PDF's running pagination (1-10).
  Design (Method, pp. 3-4): 2-year IARPA geopolitical forecasting tournament (Sept 2011-Apr 2012; June 2012-
  Apr 2013); 199 geopolitical outcomes forecast on goodjudgmentproject.com. Year 1: randomized 3 (training:
  none / scenario / probability) x 4 (group influence: independent / crowd-belief / team / prediction market)
  factorial. Year 2: 2 (no training / probability) x 3 (independent / team / market) plus an elite "tracking"
  condition. Teams (up to 25 members Y1, 15 Y2) interacted on a web site and shared rationales and
  information; crowd-belief forecasters worked alone but saw the distribution of others' forecasts. Tracking
  placed the top 2% of Year 1 (60 forecasters) into five 12-person superforecaster teams. Entry required a
  bachelor's degree or higher; 76% U.S., 83% male, mean age 36. Outcome: Brier score standardized within
  question (forecasters chose their own questions).
  Sample: Year 1 began with 2,246 participants (1,593 survey respondents randomized to nine conditions,
  ~177 each; 653 market traders); attrition 7%. Year 2 began with 1,648 (943 survey respondents, 705
  traders); attrition 3%. 85 (Y1) and 114 (Y2) questions closed and were scored.
  Effect (Results, pp. 4-6; Fig. 1; Table 1): Training improved Y1 Brier scores, F(2,1586)=14.29, p<.001;
  probability > scenario training, t(1053)=2.23, p=.026; scenario > none, t(1056)=3.25, p<.001; Y2 probability
  training > none, F(1,882)=19.12, p<.001. Group influence: Y1 F(2,1586)=60.68, Y2 F(1,882)=62.76, both
  p<.001; teams more accurate than crowd-belief forecasters, t(1036)=5.52, p<.001, who were more accurate than
  independent forecasters, t(1120)=5.92, p<.001. Number of comments within teams correlated with accuracy,
  r=-.19 (Y1), -.22 (Y2). Superforecaster teams outperformed all other groups with no regression to the mean;
  better calibration than trained regular teams, t(293)=11.03, p<.001; tracking raised resolution, t(293)=4.12,
  p<.001. Table 1 last-week Brier scores, Y2: independent no-training 0.26; teams no-training 0.16;
  superforecasters 0.07. Effects of training and teaming survived controls for forecast timing and updating
  frequency (regressions, pp. 5-6). Only F/t/r statistics are reported; no standardized effect sizes.
  Aggregation: the paper states that statistical aggregation algorithms (differential weighting, temporal
  discounting, extremizing) are "reported elsewhere" (Baron et al.; Satopaa et al. 2014). The proposition
  that aggregates of many judgments beat one person's judgment is cited as background from Page (2007) and
  Soll & Larrick (2009) in the Teaming introduction (p. 2); it is not tested in this paper.
quotation: "Numerous studies have shown that predictions based on the aggregate of many people's judgments are generally more accurate than predictions based on one person's judgment"
quotation_location: "p. 2, Teaming subsection of the introduction (cited background, not a result of this paper)"
fit: partially_supports
fit_note: |
  What the paper shows: forecasters who exchanged information and rationales in teams were more accurate than
  forecasters who only saw the crowd's distribution, who in turn beat forecasters working alone; pooling top
  performers into elite teams raised accuracy further. That is evidence that integrating others' views
  improves forecast accuracy. What it does not show: any comparison against "single-model expertise". The
  participants were educated volunteers, not domain experts, and no single expert or single formal model was
  benchmarked. The crowd-aggregation claim is asserted from prior literature and the aggregation algorithms
  are published elsewhere. Independently of fit, the teaming and training effects were re-analysed by
  Hauenstein et al. (2025) and reported to be substantially diminished or reversed once extraneous method
  variance is controlled (see replication), so this source should not carry the claim on its own.
suggested_rewording: "Forecasters who share information and rationales in teams produce more accurate probability forecasts than forecasters working alone (Mellers et al. 2014; effect contested by Hauenstein et al. 2025)."
replication:
  searched: yes
  status: mixed
  sources:
    - citation: "Hauenstein, C. E.; Thomas, R. P.; Illingworth, D. A.; Dougherty, M. R. (2025). Rethinking the Role of Teams and Training in Geopolitical Forecasting: The Effect of Uncontrolled Method Variance on Statistical Conclusions. Psychological Science 36(1), 3-18. doi:10.1177/09567976241266481, PMID 39630638"
      url_opened: "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=25886768,39630638,27516495&rettype=abstract&retmode=text"
      note: "Abstract only (also https://api.semanticscholar.org/graph/v1/paper/DOI:10.1177/09567976241266481 opened; the OSF author-manuscript link returned HTTP 400). Reanalysis of the same tournament data with item response theory models; with extraneous variables controlled the team and training effects were substantially diminished, reduced, or reversed, and strategic-responding traits distinguished superforecasters."
    - citation: "Mellers, B. et al. (2015). Identifying and cultivating superforecasters as a method of improving probabilistic predictions. Perspectives on Psychological Science 10(3), 267-281. doi:10.1177/1745691615577794, PMID 25987508"
      url_opened: "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=25987508&rettype=abstract&retmode=text"
      note: "Abstract only. Same group; reports superforecasters maintained accuracy across two years, defying regression to the mean. Extension of the tracking result, not an independent replication."
retraction_check: clean
retraction_check_url: "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=29620401,24659192&rettype=abstract&retmode=text (PMID 24659192: no retraction, erratum or concern lines); WebSearch for title + retraction found none"
proposed_strength: Moderate
contested: "Hauenstein, Thomas, Illingworth & Dougherty (2025, Psychological Science 36(1):3-18) reanalysed the same tournament data with IRT models and report the training and teaming effects are substantially diminished or reversed once uncontrolled method variance is accounted for."
verified_by: agent
verified_on: 2026-09-26
ratified: false
---

## Notes
- Mellers et al. 2014 and Tetlock 2005 (E7a) come from the same research programme, so they are not independent lines of evidence for claim E7; together they justify Moderate, not Strong.
- The paper's own Open Practices statement says the data were withheld pending completion of the 4-year tournament.
- Satopaa, Pemantle & Ungar (arXiv:1406.2148, abstract opened) is a modelling paper on extremizing averaged forecasts, not a test of the claim; it was not recorded as evidence.
