---
id: F2c
claim_id: F2
claim: "Added perspectives help only when diverse"
claim_source: "Integral Ethics v2, Foundations: perspectival realism"
citation_as_given: "Lorenz et al., PNAS (2011)"
resolved:
  authors: "Lorenz, J.; Rauhut, H.; Schweitzer, F.; Helbing, D."
  year: 2011
  title: "How social influence can undermine the wisdom of crowd effect"
  venue: "Proceedings of the National Academy of Sciences 108(22): 9020-9025"
  doi: "10.1073/pnas.1008636108"
  isbn: ""
  url_opened: "https://pmc.ncbi.nlm.nih.gov/articles/PMC3107299/"
  urls_attempted: []
  access: full_text
finding: |
  Design: laboratory experiment. Sample: 144 university students in 12 sessions of 12. Task: six factual
  estimation questions (geography and crime statistics), five consecutive rounds each. Conditions ("Experimental
  Design" section): no information (control); aggregated information (the arithmetic mean of the group's previous
  estimates); full information (all individual estimates). Monetary reward for accuracy.
  Results, by named effect:
  - Social influence effect: diversity of estimates fell substantially across rounds in the two information
    conditions, while the collective error did not improve.
  - Range reduction effect: the truth moved from the centre toward the edge of the distribution of estimates, so the
    crowd became a less reliable guide even as it converged; the paper's wisdom-of-crowd indicator fell by about one
    unit under information exchange.
  - Confidence effect: individual confidence, rated on a six-point scale, rose in the information conditions despite
    no gain in accuracy.
  Stated conclusion: independence of estimates matters for collective accuracy; even mild social influence produces
  convergence that undermines the wisdom of crowds; in democratic societies collecting independent estimates is
  difficult.
  Effect sizes: the fetched text reported directions and the one-unit indicator change; other magnitudes were not
  captured and are not recorded here.
quotation: "The truth becomes less central if social influence is allowed for"
quotation_location: "'Range Reduction Effect' section"
fit: partially_supports
fit_note: |
  The study shows that when estimates converge under social influence, adding rounds of estimation stops improving
  the group's accuracy and the crowd's range stops bracketing the truth: aggregation gains depend on the estimates
  staying diverse. That is the mechanism the register's claim points at. It is partial support because (a) the
  "perspectives" here are numerical estimates of facts, not perspectives on a case; (b) the design manipulates
  social influence, not diversity as such; and (c) the inference that lost diversity undermines accuracy is
  contradicted by Becker et al. (2017), who found that in decentralized networks social influence cut diversity by
  43% and still improved group accuracy. The evidence therefore supports "aggregation needs independent inputs" in
  one paradigm and is contested in a larger one; it does not establish "only when diverse".
suggested_rewording: "Aggregating additional estimates improves collective accuracy only while the estimates remain independent; convergence under social influence can remove the gain."
replication:
  searched: yes
  status: mixed
  sources:
    - citation: "Becker, J.; Brackbill, D.; Centola, D. (2017). Network dynamics of social influence in the wisdom of crowds. PNAS 114(26): E5070-E5076. doi 10.1073/pnas.1615978114"
      url_opened: "https://ndg.asc.upenn.edu/wp-content/uploads/2017/06/PNAS-2017-1615978114-Collective-Intelligence.pdf"
      note: "Full text (author-hosted PDF, read with pdftotext). N = 1,360 web participants; 13 experimental trials, each with one decentralized and one centralized 40-person network, plus eight 40-person control groups; three rounds per question. Replicates Lorenz's diversity reduction (SD of estimates fell 43% over two rounds in decentralized networks, P < 0.001) but finds group accuracy improved there: median error down 12% (P < 0.001), mean error down 10% (P < 0.01); in centralized networks accuracy moved with the central node (error up 19-32% when it pointed away from truth). The abstract explicitly contrasts these results with Lorenz et al. 2011."
retraction_check: clean
retraction_check_url: "https://api.crossref.org/works/10.1073/pnas.1008636108 (no update-to or relation entries; checked 2026-09-26)"
proposed_strength: Hypothesis
contested: "Becker, Brackbill & Centola 2017 (N = 1,360) replicate the diversity-reduction effect but find social influence improves accuracy in decentralized networks, contradicting the inference that convergence undermines the crowd."
verified_by: agent
verified_on: 2026-09-26
ratified: false
---

## Notes
- Verified by the coordinator after the batch agent was cut off before writing this record.
- Grade reasoning: one primary study with partial fit and a larger follow-up that contradicts the accuracy inference. Under the strength rules partial support without otherwise strong evidence does not reach Moderate; the claim as stated is not supported by this source, so the record grade is Hypothesis. The claim-level grade for F2 is set in the register.
