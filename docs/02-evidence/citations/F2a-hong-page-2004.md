---
id: F2a
claim_id: F2
claim: "Added perspectives help only when diverse"
claim_source: "Integral Ethics v2, Foundations: perspectival realism"
citation_as_given: "Hong & Page, PNAS (2004)"
resolved:
  authors: "Hong, L.; Page, S. E."
  year: 2004
  title: "Groups of diverse problem solvers can outperform groups of high-ability problem solvers"
  venue: "Proceedings of the National Academy of Sciences 101(46): 16385-16389"
  doi: "10.1073/pnas.0403723101"
  isbn: ""
  url_opened: "https://pmc.ncbi.nlm.nih.gov/articles/PMC528939/"
  urls_attempted: []
  access: full_text
finding: |
  Design: a formal model plus a computational experiment. No human participants.
  The model: agents are search heuristics over a finite solution space with a value function; a group works by
  passing the current best point from agent to agent until none can improve it. "Diversity" is defined as
  dissimilarity between agents' heuristics.
  Theorem ("A Mathematical Theorem" section): under three assumptions (difficulty: no single agent always finds the
  optimum; diversity: for any non-optimal point some agent can move off it; uniqueness: a unique best agent), with
  probability one there exist sample sizes N1 < N such that the joint performance of N1 randomly drawn agents exceeds
  the joint performance of the N1 individually best agents among N drawn agents.
  Computational experiment ("A Computational Experiment" section, Table 1): solution space n = 2000 with a random
  value function; heuristics parameterised by l = 12 or 20 and k = 3; groups of 10 or 20 agents, either the top
  performers or randomly drawn; results averaged over 50 trials. Table 1, ten agents, l = 12: best agents score
  92.56 with diversity 70.98%; random agents 94.53 with diversity 90.99%. Twenty agents, l = 12: 93.78 vs 94.72.
  The random-group advantage shrinks as group size grows.
  Stated limitations ("Concluding Remarks"): communication costs and learning are ignored; the finiteness of the
  solution space is an artifact the authors flag.
  Direction: random (more diverse) groups outperform best-agent groups in the simulation, by about two points on a
  100-point scale for groups of ten.
quotation: ""
quotation_location: ""
fit: partially_supports
fit_note: |
  What the source shows: in a model of search heuristics, a group whose members differ can collectively outperform a
  group of individually better but similar members, and the theorem gives sufficient conditions for that. What the
  register claims: added perspectives help ONLY when diverse. The paper supports the weaker and more specific
  statement that diversity of heuristics can beat individual ability; it does not test whether non-diverse additions
  never help, and it concerns algorithms, not human perspectives on a moral case. The transfer is an analogy the
  register must argue. The theorem's correctness as stated and its real-world reach are disputed (see F2b and the
  replication sources), so the formal ground is contested rather than settled.
suggested_rewording: "Added perspectives help more when they differ from those already present; in formal models of group search, diverse groups can outperform groups of individually better but similar members."
replication:
  searched: yes
  status: mixed
  sources:
    - citation: "Thompson, A. (2014). Does Diversity Trump Ability? An Example of the Misuse of Mathematics in the Social Sciences. Notices of the AMS 61(9): 1024-1030. doi 10.1090/noti1163"
      url_opened: "https://web.archive.org/web/2022id_/https://www.ams.org/notices/201409/rnoti-p1024.pdf"
      note: "Full text (Wayback copy, read via curl and pdftotext). Reproduces the simulation result that ten random agents beat the ten best (p. 1027), then argues the theorem is incorrect as stated, trivial once corrected, unrelated to the experiment, and that randomness rather than 'diversity' explains the experiment. See record F2b."
    - citation: "Kuehn, D. (2017). Diversity, Ability, and Democracy: A Note on Thompson's Challenge to Hong and Page. Critical Review 29(1): 72-87. doi 10.1080/08913811.2017.1288455"
      url_opened: "https://api.openalex.org/works/doi:10.1080/08913811.2017.1288455"
      note: "Abstract only (OpenAlex; Taylor & Francis page not opened). Holds that Thompson's mathematical criticisms are 'incorrect, misleading, or irrelevant to the validity of the theorem', while crediting her point about the importance of randomization."
    - citation: "Singer, D. J. (2019). Diversity, Not Randomness, Trumps Ability. Philosophy of Science 86(1). Penultimate draft dated 26 March 2018."
      url_opened: "https://www.danieljsinger.com/papers/Singer%20-%20Diverstiy,%20Not%20Randomness,%20Trumps%20Ability%20(draft).pdf"
      note: "Full text of the author's penultimate draft (published version not opened). Re-runs the Hong-Page model (1 million runs); reports that maximally diverse groups do typically outperform random groups, contrary to Thompson's finding, and that a coverage measure of diversity ('C-diversity') correlates r = 0.553 with group competence and screens off Hong and Page's own diversity measure (partial r = 0.0019). Concludes diversity, not randomness, explains the result."
retraction_check: clean
retraction_check_url: "https://api.crossref.org/works/10.1073/pnas.0403723101 (no update-to or relation entries; checked 2026-09-26)"
proposed_strength: Argued only
contested: "The theorem is formally disputed (Thompson 2014) and defended (Kuehn 2017; Singer 2019); Thompson and Singer report opposite results for maximally diverse groups in re-runs of the model."
verified_by: agent
verified_on: 2026-09-26
ratified: false
---

## Notes
- Verified by the coordinator after the batch agent was cut off before writing this record.
- Grim, Singer, Bramson, Holman, McGeehan & Berger (2019), "Diversity, Ability, and Expertise in Epistemic Communities", Philosophy of Science 86(1): 98-123, was located (philarchive.org/archive/GRIDAA-8) but returned a bot-block page to both WebFetch and curl, so it is not cited.
- Grade reasoning: a formal model with no empirical component, partial fit, and a live dispute over the theorem. Under the strength rules that is Argued only. The register's Moderate for F2 rested on this source and on Lorenz et al. (F2c), which is itself contested by Becker et al. 2017.
