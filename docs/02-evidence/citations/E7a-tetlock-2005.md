---
id: E7a
claim_id: E7
claim: "Integrating many views outperforms single-model expertise"
claim_source: "Integral Ethics v2, Cognitive perspectives as instruments"
citation_as_given: "Tetlock, Expert Political Judgment (2005)"
resolved:
  authors: "Tetlock, P. E."
  year: 2005
  title: "Expert Political Judgment: How Good Is It? How Can We Know?"
  venue: "Princeton University Press (book). 2005 hardcover; 2006 paperback (352 pp.); New Edition 2017 (368 pp.)"
  doi: "none"
  isbn: "0691123020 (2005 hardcover, Open Library record OL3311005M); 9780691128719 (2006 paperback, Open Library OL7759322M and IJF review listing); 9780691178288 (2017 New Edition hardcover, Princeton UP page)"
  url_opened: "https://faculty.wharton.upenn.edu/wp-content/uploads/2012/08/Tetlock-16.pdf"
  urls_attempted:
    - "https://muse.jhu.edu/book/52760 (opened; table of contents of the 2017 New Edition)"
    - "https://openlibrary.org/isbn/9780691123028.json (opened; 2005 hardcover record)"
    - "https://openlibrary.org/isbn/9780691128719.json (opened; 2006 paperback record)"
    - "https://openlibrary.org/search.json?title=expert+political+judgment&author=tetlock (opened)"
    - "https://press.princeton.edu/books/hardcover/9780691178288/expert-political-judgment (opened; 2017 New Edition page)"
    - "https://ideas.repec.org/a/eee/intfor/v23y2007i2p339-342.html (opened; bibliographic listing of the Tschoegl & Armstrong review)"
    - "https://www.cxoadvisory.com/investing-expertise/expert-political-judgment-how-good-is-it-how-can-we-know-chapter-by-chapter-review/ (opened; blog chapter review, secondary)"
    - "https://en.wikipedia.org/wiki/Expert_Political_Judgment (opened; stub, no study numbers)"
    - "https://press.princeton.edu/books/paperback/9780691128719/expert-political-judgment (HTTP 403)"
    - "https://www.googleapis.com/books/v1/volumes?q=intitle:%22Expert+Political+Judgment%22+inauthor:Tetlock (HTTP 429, three variants tried)"
    - "https://www.newyorker.com/magazine/2005/12/05/everybodys-an-expert (fetch blocked)"
  access: abstract_only
finding: |
  The book itself was not opened. Bibliographic facts come from Open Library, Princeton UP and Project MUSE
  records; the study design and results come from a peer-reviewed book review that reports the numbers:
  Tschoegl, A. E. & Armstrong, J. S. (2007), International Journal of Forecasting 23(2), 339-342
  (author-hosted PDF at the url_opened above; the IDEAS/RePEc listing confirms journal, volume and pages).
  Design (review, p. 1): a two-decade study; 284 people recruited whose professions included "commenting or
  offering advice on political and economic trends"; they gave probability forecasts within and outside their
  areas of expertise and answered questions about how they formed forecasts, handled failures and responded
  to contradictory information. By 2003 the database held 82,361 forecasts. Forecasts were scored against
  outcomes and against alternatives: simple statistical rules/extrapolations, uninformed non-experts and
  well-informed non-experts. (A figure of ~28,000 forecasts appears in search-engine snippets for this book;
  I did not open a source reporting it and record only the review's 82,361.)
  Sample: 284 experts; 82,361 forecasts (as reported by the review).
  Effect (review, pp. 1-2): experts barely, if at all, outperformed informed non-experts; neither did well
  against simple rules and models; with outcomes split into Better/Same/Worse the forecasters frequently did
  worse than assuming each state equally likely. Forecasters classified as "foxes" (draw on many ideas and
  sources of information) produced more accurate forecasts than "hedgehogs" (interpret the world through one
  favourite theory), though neither beat simple rules. The review also reports that Tetlock could push more
  foxes than hedgehogs into forecasts violating probability additivity. No effect sizes are given in the
  review; the book's own statistics were not opened.
  Location (Project MUSE table of contents, 2017 edition): the fox/hedgehog accuracy result is Chapter 3,
  "Knowing the Limits of One's Knowledge: Foxes Have Better Calibration and Discrimination Scores than
  Hedgehogs"; belief updating is Chapter 4, "Honoring Reputational Bets: Foxes Are Better Bayesians than
  Hedgehogs" (the CXO chapter review reports, unverified against the book, that when wrong hedgehogs shift
  19% and foxes 59% of the Bayes-prescribed amount); Chapter 6 is "The Hedgehogs Strike Back". Methodological
  and technical appendices follow Chapter 8.
quotation: "Tetlock found that foxes usually outperform hedgehogs; foxes produced more accurate forecasts than hedgehogs, though again neither beat simple rules."
quotation_location: "Tschoegl & Armstrong (2007) review, p. 2 of the Wharton PDF"
fit: supports
fit_note: |
  The fox/hedgehog contrast is the claim: forecasters who integrate many ideas and sources (foxes) were more
  accurate than forecasters who apply one dominant model (hedgehogs). Three caveats the ratifier should weigh.
  (1) Cognitive style was measured, not manipulated, so the result is correlational. (2) "Outperforms" holds
  relative to hedgehogs only; per the review neither style beat simple statistical extrapolation, so the
  claim must not be read as "many views beat formal models". (3) The evidence here is reported second-hand
  through a peer-reviewed review and the publisher's chapter titles; the book's tables were not opened.
suggested_rewording: ""
replication:
  searched: yes
  status: none_found
  sources:
    - citation: "Mellers, B. et al. (2015). Identifying and cultivating superforecasters as a method of improving probabilistic predictions. Perspectives on Psychological Science 10(3), 267-281. doi:10.1177/1745691615577794"
      url_opened: "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=25987508&rettype=abstract&retmode=text"
      note: "Same research group, later tournament data (abstract only): superforecaster performance explained partly by 'cognitive abilities and styles'. An extension, not an independent replication of the fox/hedgehog effect. No independent replication of the 2005 result was found in the searches run."
retraction_check: clean
retraction_check_url: "WebSearch: Tetlock \"Expert Political Judgment\" retraction OR correction OR errata (no notice found; book, not indexed in PubMed)"
proposed_strength: Moderate
contested: ""
verified_by: agent
verified_on: 2026-09-26
ratified: false
---

## Notes
- Two editions carry different page counts in the records opened: Open Library lists the 2005 hardcover at 321 pp. and the 2006 paperback at 352 pp.; Princeton UP lists the 2017 New Edition at 368 pp. The 2006 paperback is what the IJF review cites (ISBN 978-0-691-12871-9).
- Strength is Moderate, not Strong: one primary study; no meta-analysis or independent replication of the fox/hedgehog effect was found; the follow-on Good Judgment Project work by the same group is contested (see E7b).
- If the ratifier wants a source that directly tests aggregating several people's views against one person's, Mellers et al. 2014 (E7b) cites Page (2007) and Soll & Larrick (2009) as the background literature; neither was opened here.
