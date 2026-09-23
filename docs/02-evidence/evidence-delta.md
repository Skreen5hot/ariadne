# Evidence delta: proposed changes for ratification

Status: proposed, 2026-09-23. Nothing here changes a claim's standing until Aaron ratifies it. Each row names the record that justifies it.

**Headline.** No citation in the v2 register or the candidate table has been verified. The environment these records were made in could not reach any scholarly source (see `README.md`). So no strength that depends on a source's content can yet be confirmed, raised or lowered. The v2 sentence *"Fifteen rest on strong or moderate evidence"* describes grades entered from recall, not verified evidence. Until the records are completed, the best available evidence for every empirical claim is **unverified**. That is weaker than Moderate, and it is stated here plainly.

## 1. Proposed strength changes

Only changes that the strength rules set without reading a source.

| ID | Claim | Current | Proposed | Why | Record |
| --- | --- | --- | --- | --- | --- |
| F1 | No single perspective captures all morally relevant features | Strong | **Argued only** | The claim is logical and ontological. The rule for philosophical claims (brief, Phase 1) and the strength table both give Argued only: none of the cited works is empirical, and Strong requires a meta-analysis or replications. The cited works themselves are unverified. | [F1](citations/F1-single-perspective-incomplete.md) |

No change is proposed for C2, C4 and C8 (Argued only → Argued only) or for H-P6 (Hypothesis → Hypothesis). Their records confirm the grade by rule. The attributions to Kant, Nozick, Aquinas, Ross, Berlin, Raz, Chang, Williams and Finnis are **not verified**; the works could not be opened.

If F1 is ratified, the register's tally moves from 15 / 3 / 1 to 14 strong-or-moderate, 4 argued only and 1 hypothesis, and all 14 remaining grades are still unverified.

## 2. Proposed citation-check status

| IDs | Current "Citation check" | Proposed | Record |
| --- | --- | --- | --- |
| F1, F2, E1–E8, C1, C2, C4, C4a, C5, C6, C7, C8 | Unverified | **Could not access (2026-09-23)**: sources not opened; re-run with network access | one record per ID in `citations/` |
| H-P6 | Unverified | **No citation** (none claimed) | [H-P6](citations/H-P6-six-operations-decomposition.md) |

## 3. Grades that cannot be proposed yet

These 14 claims keep their current grade as an unverified entry. No proposal can be made until the source is opened: F2, E1, E2, E3, E4, E5, E6, E7, E8, C1, C4a, C5, C6, C7.

## 4. A scale problem: formal claims

C5 (Arrow; Keeney & Raiffa) and C6 (Arrow & Fisher) are entered as **Formal** with grade Strong. The strength table has no grade for a proved formal result. Its only formal row is "Argued only: philosophical or formal argument with no empirical component." Applied literally, C5 and C6 grade **Argued only** even after their sources are verified. Strong would need a meta-analysis or replications, which a theorem does not have.

Not proposed as a change, because the records could not confirm what the sources prove. **Decision for Aaron:** accept Argued only for formal results, or add a grade (e.g. "Proved, under stated assumptions") to the table. With either choice, C6's fit depends on whether the result's assumptions match our use of it, and a verifier should check that explicitly.

## 5. Claims whose wording needs attention, whatever the sources say

These come from reading the claims, not the sources. They are offered so the next verifier tests the right sentence.

| ID | Current wording | Problem | Proposed wording (for ratification) |
| --- | --- | --- | --- |
| C7 | Decision aids bias human choice; the human must stay the decider | Two claims in one. The first is empirical. The second is normative and cannot be supported by an empirical source. | C7a (empirical): *Decision aids can bias human choice (automation bias).* C7b (normative, Argued only): *The human must remain the decider.* |
| F2 | Added perspectives help only when diverse | "Only when" is a universal negative, which no set of studies can establish. v2's own ground is the formal selection argument. | F2a (formal, Argued only): *A perspective that is redundant with those already applied adds no coverage.* F2b (empirical): *Groups or procedures with more diverse views outperform less diverse ones on [task class].* The task class must be filled from the sources. |
| H-P6 | The six operations are an exhaustive, efficient decomposition | E-PC can test efficiency (ablation, unique contribution) and coverage gain. It cannot test exhaustiveness: no finite experiment shows nothing is missing. | *Each of the six operations contributes unique coverage, and no smaller set matches their joint coverage.* Exhaustiveness stays an open question. |

## 6. Candidate values

### 6a. Uncited values recorded as Argued only (decision needed)

V02 human dignity, V03 truth / reality-alignment, V20 non-coercion, V21 transparency, V22 epistemic humility, V23 limited pluralism. Each is recorded as **Argued only** without a search, as instructed.

**Decision for Aaron:** may these stand on argument, or does any need empirical grounding? A note to help decide: V02, V03, V20, V21 and V23 act as constraints or principles in v2, where argument is the natural ground. V22 is a competency. v2's section on integrative ethical reasoning says wise-reasoning research already measures intellectual humility, so V22 is the likeliest candidate for empirical grounding.

### 6b. Suspected neighbouring claims: not tested

The brief asks for V18, V17 and V13 to be tested first. None could be opened, so **no fit was assessed and none is graded `neighbouring_claim`**. The table shows the mismatch visible in **our own v1 reference strings**. Those strings were entered from recall and are unverified, so these are leads for the next verifier, not findings.

| ID | Claim (v1 wording) | Title as given in v1 reference list (unverified) | Apparent mismatch to test |
| --- | --- | --- | --- |
| V18 | Perceived freedom essential to wellbeing even when not exercised | "The effects of choice on intrinsic motivation and related outcomes: A meta-analysis of research findings" | Choice → intrinsic motivation, not exit rights or unexercised freedom → wellbeing |
| V17 | Social accountability improves behavior | "Social influence: Compliance and conformity" | A review of compliance, not of accountability's benefits |
| V13 | Balance across life domains predicts wellbeing | "The pleasant life, the engaged life, and the meaningful life: What about the balanced life?" | Title reads as a theoretical proposal; test whether it reports any predictive data |
| V19 | Developmentally appropriate autonomy support predicts optimal outcomes | "A theoretical upgrade of the concept of parental psychological control…" | Theoretical paper about psychological control, not about graduated autonomy |
| V15 | Commitment predicts relationship satisfaction and vocational success | "The Investment Model Scale: Measuring commitment level…" | A measurement paper; "vocational success" may be outside it |
| V16 | Reflective capacity predicts better life outcomes | "Self-knowledge: Its limits, value, and potential for improvement" | Self-knowledge, not reflective capacity. The title says "limits". |
| V06 | Relationships most robust predictor of life satisfaction | *The Good Life…* (Simon & Schuster, 2023) | A trade book. "Most robust predictor" needs the underlying study, not the book. |

### 6c. ValueNet kinds

All 23 candidates carry a `valuenet_kind` in `register.yaml`. Summary:

| Kind | Candidates |
| --- | --- |
| value_disposition | V09 virtue / character (`vn-core:ValueDisposition`, family), V11 authentic agency (`vn-folk:AuthenticityDisposition`), V15 commitment and rootedness (`vn-folk:CommitmentDisposition`) |
| value_role | V17 community accountability (`vn-folk:AccountabilityRole`) |
| aimed_good | V01, V04, V05, V06, V07, V10, V12, V13, V14 |
| constraint | V02, V03, V18, V19, V20, V21 |
| competency | V08, V16, V22 |
| *(none fits)* | V23 limited pluralism |

Borderline calls for Aaron are marked in each record's `valuenet_kind_note`: V07 (attainment or striving), V12 ("vitality" as a state, or spirituality as a disposition) and V15 (rootedness as a separate aimed good).

## 7. v1 reference corrections

Checked against the v1 manuscript in this repository. The external facts needed to *correct* each entry could not be checked.

| Slip | What the repository shows | Status |
| --- | --- | --- |
| Shapiro et al. year | `integral-ethics.md` line 946 cites "Shapiro et al., 2011". Line 1597 lists "Shapiro, S. L., Carlson, L. E., Astin, J. A., & Freedman, B. (2006). Mechanisms of mindfulness." | **Inconsistency confirmed.** Which year is right is not determined. Also flagged: line 946 cites it for "depth of practice predicts benefits, not breadth". Whether a paper titled *Mechanisms of mindfulness* supports that is a fit question, so the in-text citation may point to a different work. |
| Jacobsen et al. volume/year | Line 1554: "Jacobsen, T., Buchta, K., Köhler, M., & Schröger, E. (2006). The primacy of beauty in judging the aesthetics of objects. Psychological Reports, 94(4), 1253-1260." Line 532 cites it as 2006. | **Entry confirmed as reported.** Whether volume 94 belongs to a different year could not be checked. Not corrected. |
| Steiner, twelve worldviews | Line 77 attributes the twelve to *The Riddles of Philosophy* "and related lectures", citing (1914/2008, 1923/1973). Line 1602: "Steiner, R. (1914/2008). The Riddles of Philosophy." Line 1603: "Steiner, R. (1923/1973). The Philosophy of Freedom…" | **Attribution to *Riddles* confirmed present in v1.** That the twelve come from *Human and Cosmic Thought* (GA 151, 1914 lectures) could not be confirmed; no edition could be opened. Also flagged: the second citation (1923/1973) points to *The Philosophy of Freedom*. Check whether it is cited for the twelve at all. |

## 8. ValueNet gaps

Recorded here instead of inventing classes (brief, "ValueNet is reused").

1. **No aimed-good class, and no relation from a disposition to what it aims at.** Nine candidates are aimed goods: V01, V04, V05, V06, V07, V10, V12, V13, V14. Their records name the dispositions that aim at them in `valuenet_related`, but ValueNet cannot state the link.
2. **No class for constraints, rights or permissions.** This covers V02, V03, V18, V19, V20 and V21. Non-coercion comes closest to existing structure: coercion resembles `vn-mf:OppressionProcess`, which `contravenes` `vn-mf:LibertyDisposition`.
3. **No competency class.** This covers V08, V16 and V22, and also the Tier 0 "integrative ethical reasoning". The nearest class is `vn-moral-epistemics:PrudenceDisposition`, a *moral value disposition* to apply right reason to particular practical judgments. v2 describes integrative reasoning as close to *prudentia*, so that class is worth reviewing as its anchor.
4. **No "principle" kind in the task's enum.** V23 (limited pluralism) is a principle in v2. The field is left empty.
5. **Harms outside the six moral-foundation pairs.** The moral-foundations module has six disposition / violation pairs: care/harm, fairness/cheating, loyalty/betrayal, authority/subversion, sanctity/degradation and liberty/oppression. A harm that contravenes another disposition, such as dignity or honesty, can only be typed as generic `vn-core:ValueViolationProcess`. E-PC scenario graphs will hit this.
6. **E-PC annotation target.** The brief says a gold annotation `isEvidenceFor` a *value realization process*. In ValueNet, `vn-core:isEvidenceFor` is an annotation property whose documented range is any BFO process, and harms are *violation* processes. A gold consideration that records a harm should therefore be evidence for a `ValueViolationProcess`. **Decision for Aaron:** allow both targets in the E-PC gold schema.

## 9. Decisions requested

1. Ratify or reject the F1 downgrade (§1).
2. Ratify the citation-check status change (§2).
3. Choose how formal results are graded (§4).
4. Ratify, amend or reject the C7, F2 and H-P6 rewordings (§5).
5. Decide whether V02, V03 and V20–V23 need empirical grounding (§6a).
6. Settle the borderline kinds V07, V12, V15 and V23 (§6c, §8.4).
7. Allow `ValueViolationProcess` as an E-PC annotation target (§8.6).
8. Decide where E-PC lives, given that the E2 machinery is in `wrm-e2-independent-library-test` (see `README.md`).
9. Arrange a verification environment with scholarly network access, and re-run Phases 1–2.
