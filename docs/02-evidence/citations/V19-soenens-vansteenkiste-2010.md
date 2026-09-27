---
id: V19
claim_id: V19
claim: "Developmentally appropriate autonomy support predicts optimal outcomes"
claim_source: "Integral Ethics v1 §4.3 (value entry) / v2 Candidate value ontology table"
citation_as_given: "Soenens & Vansteenkiste (2010)"
resolved:
  authors: "Soenens, B.; Vansteenkiste, M."
  year: 2010
  title: "A theoretical upgrade of the concept of parental psychological control: Proposing new insights on the basis of self-determination theory"
  venue: "Developmental Review, 30(1), 74-99 (online 23 December 2009)"
  doi: "10.1016/j.dr.2009.11.001"
  isbn: ""
  url_opened: "https://selfdeterminationtheory.org/SDT/documents/2010_SoenensVansteenkiste_DR.pdf"
  urls_attempted:
    - "https://api.openalex.org/works?filter=title.search:theoretical%20upgrade%20parental%20psychological%20control&per-page=3 (opened; metadata, no abstract)"
    - "https://api.openalex.org/works/doi:10.1016/j.dr.2009.11.001 (opened; metadata, closed access)"
    - "https://api.crossref.org/works/10.1016/j.dr.2009.11.001 (opened; metadata, no abstract)"
    - "https://doi.org/10.1016/j.dr.2009.11.001 (redirect to linkinghub.elsevier.com, not followed)"
    - "https://biblio.ugent.be/publication/1006931 (opened; record only, PDF restricted to UGent)"
  access: full_text
finding: |
  Full text (publisher PDF hosted on selfdeterminationtheory.org, fetched with WebFetch and converted with
  pdftotext). A theoretical overview: it reports no new empirical data and no meta-analysis.
  Abstract (p. 74): psychological control is manipulative parental behaviour that intrudes on the child's
  psychological world; over the past decade research has 'consistently demonstrated the negative effects of
  psychologically controlling parenting on children's and adolescents' development'; the paper aims to give a
  clearer definition, a more refined account of its dynamics, and insight into its generalization across age and
  culture, using self-determination theory (SDT).
  Core distinctions: psychological control vs autonomy support, and independence-promotion vs
  volitional-functioning promotion (Fig. 1, p. 84). SDT autonomy support is defined as promoting volitional
  functioning: parents 'empathize with their children's perspective, encourage their children to carefully
  reflect on their values and goals, provide a developmentally appropriate degree of choice, and give a
  meaningful rationale when choice is limited' (p. 84, citing Deci et al. 1994). Psychological control is
  distinguished from behavioural control and structure (Fig. 2, pp. 87-88). Internally vs externally controlling
  parenting are proposed to have different consequences (internalizing vs externalizing problems; pp. 81-83).
  Section 'Why do the effects of psychological control generalize across age?' (p. 92): argues that volitional
  functioning is not a developmental stage but a mode of functioning operative throughout life, so the harm of
  psychological control should not be confined to particular stages, though its manifestation may vary with
  age; notes that the evidence is mostly on adolescents with younger-child studies emerging (p. 76).
  Design: conceptual review. Sample: none. Effect: none reported; no effect sizes.
quotation: "provide a developmentally appropriate degree of choice, and give a meaningful rationale when choice is limited"
quotation_location: "Section on promotion of volitional functioning, p. 84"
fit: partially_supports
fit_note: |
  The paper argues the claim and builds 'developmentally appropriate' choice into its definition of autonomy
  support, but it is a conceptual paper: it reports no data, and it does not treat 'developmentally
  appropriate' or 'graduated' autonomy as a variable that is measured or manipulated. It supports the claim as
  a theoretical position and by citation of the psychological-control literature, not as a finding. Empirical
  support for the unqualified claim ('parental autonomy support predicts better child outcomes') comes from the
  meta-analyses listed under replication; the 'developmentally appropriate' qualifier is asserted, not tested,
  in everything opened.
suggested_rewording: "Parental autonomy support (perspective-taking, rationale, age-appropriate choice) predicts child and adolescent wellbeing and achievement; the added value of calibrating autonomy to developmental stage has not been tested directly."
replication:
  searched: yes
  status: replicated
  sources:
    - citation: "Vasquez, A. C., Patall, E. A., Fong, C. J., Corrigan, A. S., & Pine, L. (2016). Parent autonomy support, academic achievement, and psychosocial functioning: A meta-analysis of research. Educational Psychology Review, 28(3), 605-644. doi 10.1007/s10648-015-9329-z"
      url_opened: "https://eric.ed.gov/?id=EJ1110197"
      note: "Abstract only (ERIC). 36 studies; parent autonomy support related to greater academic achievement and to autonomous motivation, psychological health, perceived competence, engagement and positive attitudes toward school; strongest relation with psychological health; stronger when both parents were rated; relation 'may vary by grade level'. Effect sizes not in the abstract."
    - citation: "Bradshaw, E. L., Duineveld, J. J., Conigrave, J. H., Steward, B. A., Ferber, K. A., Joussemet, M., Parker, P. D., & Ryan, R. M. (2025). Disentangling autonomy-supportive and psychologically controlling parenting: A meta-analysis of self-determination theory's dual process model across cultures. American Psychologist, 80(6), 879-895. doi 10.1037/amp0001389"
      url_opened: "https://selfdeterminationtheory.org/wp-content/uploads/2024/09/2024_BradshawDuinevelEtAl_ParentingMeta_PrePrint.pdf"
      note: "Full text of the accepted manuscript. k = 238 studies, 1,040 effects, N = 126,423. Parental autonomy support -> child wellbeing r = 0.30 [0.26, 0.33]; psychological control -> ill-being r = 0.26 [0.23, 0.28]; both hold controlling for each other (0.26 and 0.20). Effects consistent across regions, individualism, hierarchy and sex; child age was the only moderator of the autonomy-support effect (adolescents r = .34 vs adults r = .23). See record V19x."
retraction_check: clean
retraction_check_url: "https://api.openalex.org/works/doi:10.1016/j.dr.2009.11.001 (is_retracted false); WebSearch '\"A theoretical upgrade of the concept of parental psychological control\" Soenens retraction OR erratum OR correction' returned no notice"
proposed_strength: Argued only
contested: ""
verified_by: agent
verified_on: 2026-09-26
ratified: false
---

## Notes
- Grade rationale: under addendum item 1 the record grades what THIS source contributes; a conceptual review
  with no data contributes argument, so 'Argued only' is the honest record-level grade even though the paper is
  psychological rather than philosophical. The claim-level grade should be set from V19x (Bradshaw et al. 2025)
  and Vasquez et al. 2016: Strong for 'parental autonomy support predicts child wellbeing and achievement',
  Hypothesis for the 'developmentally appropriate / graduated' qualifier, which no opened source tests.
- Vasquez et al. 2016 could only be opened as an abstract (Springer redirected to a login gateway; Semantic
  Scholar had no abstract). Bradshaw et al. 2025 is by an SDT group that overlaps with Vansteenkiste's network
  (Ryan), so the two meta-analyses are not fully independent of the theoretical tradition.
