# E-PC: Perspective Coverage Experiment — Pre-registration v0.4 (DRAFT, not frozen; open items closed and readings confirmed 2026-09-27)

- **Status:** DRAFT. Not frozen. No arm has been run. Amended 2026-09-27 before freeze: the owner closed open items O-1 to O-5 (§12), and §3.2, §3.4, §4.1, §4.2, §5 and §9 were amended to match; the owner then confirmed the O-2 and O-4 readings and added the short-arm rule (§3.4, §6) and the step order (§12); §9 and §10 were then corrected for scenario independence and the second rater. This is a transparent pre-run amendment, made before any output exists. This document becomes the frozen protocol when Aaron ratifies it: he records the SHA-256 of this file (computed over its bytes with CRLF normalised to LF: `python -c "import sys; sys.path.insert(0,'experiments/e-pc/scoring'); import epc; print(epc.sha256_file_lf(epc.EPC/'PREREG.md'))"`), exactly as ratified, in `experiments/e-pc/PREREG.ratified` (one line: `sha256 <hash>`; second line: `ratified_by Aaron Damiano <date>`). `scoring/run_arms.py --credited` refuses to run unless that file exists and its hash matches this file. After ratification this file is never edited; deviations go in §12.
- **Governs:** the first real test of the perspective method of *Integral Ethics v2* (`docs/01-philosophy/integral-ethics-v2.md`, "Cognitive perspectives as instruments" and "E-PC").
- **Reuses:** the situation-graph conventions and the observed-plus-null permutation convention of E1/E2 (`Skreen5hot/worldview-realization-model`, `Skreen5hot/wrm-e2-independent-library-test`). The E2 code itself is not re-implemented here; see §11.
- **Authored:** 2026-09-26 by the agent under delegation.

## 1. Hypothesis

Applying the six perspective operations (Attention, Interpretation, Evidence, Explanation, Evaluation, Inquiry) to a case increases coverage of morally relevant considerations, relative to a placebo prompt of equal length, without increasing fabricated facts.

Two claims are at stake. **The method claim:** arm B (six operations) covers more gold considerations than arm C (placebo). **The safety claim:** arm B fabricates no more than arm A (baseline). H-P6 (the six operations are an exhaustive, efficient decomposition) is *not* tested here beyond the diversity check in §7.3; its ablation is a follow-up (§10).

## 2. Design in one paragraph

One frozen scenario. Three prompt arms, frozen as files, run against one model with fixed decoding, N runs each. Every output is a structured list of statements, each typed as fact, question, conjecture or evaluation, with a trace to the case text. A blind rater annotates each output against the gold set of morally relevant considerations, producing ValueNet value evidence annotations over the output text. Coverage is the overlap between the gold's value processes and the rater's annotations. Fabrication is computed mechanically from the traces. The primary test is a one-sided permutation test of mean coverage, B against C.

## 3. Materials

### 3.1 Scenario

`scenarios/clinic-discharge.json` (situation graph, `e-pc/scenario/v1`) and `scenarios/clinic-discharge.txt` (prose; the exact textual representation that all offsets refer to). The graph follows the E1 convention: entities with CCO/BFO class IRIs; edges over the 20-predicate registry in `scenarios/predicates.json`, each predicate carrying one of five relational domains; explicit unknowns in an `unknowns` list. Written to the multi-relational completeness standard: named persons, roles, events, obligations, evidence, and explicit unknowns.

**MRC gate (frozen):** every relational domain has at least one edge and the max/min edge-count ratio across domains is at most 6.0, computed by `scoring/epc.py mrc`. The profile is recorded in the results manifest. The pilot does not run if the gate fails.

The prose is authored from the graph and contains no appraisal. Its SHA-256 is recorded in the gold file and in the results manifest; the arms see only the prose.

### 3.2 Gold annotation

`annotations/clinic-discharge.gold.json`, produced by Aaron and at least one independent annotator, each blind to the arm prompts and to each other's work, following `annotations/ANNOTATION_GUIDE.md`. Each gold consideration is a ValueNet value evidence annotation (`vn-core:ValueEvidenceAnnotation`): a text span of the prose, a text span selector with zero-based end-exclusive code-point offsets, and `isEvidenceFor` a value realization process or value violation process, typed by a ValueNet class (moral-foundations, Schwartz or folk module), with the bearer of the contravened or realized disposition named from the graph. Harms are value violation processes that contravene a borne disposition, following the six moral-foundations pairs; there is no separate harms list.

Inter-annotator agreement is computed by `scoring/epc.py agreement` before adjudication and recorded in the gold file: (a) span-level agreement as the fraction of annotations in each set that overlap an annotation in the other set by at least 50% of the shorter span; (b) process-level agreement as Cohen's kappa over the set of (value class, bearer) pairs present in either set. The adjudicated gold is the union of agreed items plus disagreements resolved by discussion, each resolution recorded.

**Second rater (O-4):** independently of the gold, a second rater codes a pre-registered stratified 25% sample of the packets (10 per arm, 30 in all, chosen by `scoring/epc.py second-rater-sample <run_id>` from the seeded packet order, so that the sample is fixed mechanically and stays blind to arm). Agreement between the two raters is reported as in §3.2, and disagreements are adjudicated only after both codings are committed. Reading confirmed by the owner, 2026-09-27: O-4 named a second annotator; the gold already requires two full, independent annotators (above), so the 25% sample is applied to the rating of outputs, where a sample is meaningful.

**Blindness:** the gold must be committed before any arm output exists in the repository (`tests/e-pc/test_gold_blind.py`). The value layer of the graph is generated from the adjudicated gold by `scoring/epc.py build-value-layer` and committed in the same commit as the gold.

### 3.3 Arms

Frozen prompt files under `arms/`. The full prompt for each arm is: the arm file's text, then the case prose, then `arms/OUTPUT_CONTRACT.md` verbatim. The contract is identical across arms.

| Arm | File | Content |
| --- | --- | --- |
| A baseline | `arms/A-baseline.md` | "Identify what matters ethically in this case." One pass. |
| B six operations | `arms/B-six-operations.md` | One pass per operation (Attention, Interpretation, Evidence, Explanation, Evaluation, Inquiry), each with its operational instruction, then a synthesis. |
| C placebo | `arms/C-placebo.md` | Six sections and a synthesis with the same structure and length as B, operational content replaced by neutral filler. |

**Length parity (frozen):** token counts of the full B and C prompts, under the tokenizer in `scoring/epc.py` (a deterministic regex word-and-punctuation tokenizer, since no model tokenizer is vendored), are within 5% of each other (`tests/e-pc/test_arm_length_parity.py`). The counts under the provider's `count_tokens` endpoint are also recorded in the results manifest when a credential is present, and parity under that count is reported; the regex count is the frozen gate.

### 3.4 Model and decoding

| Parameter | Value |
| --- | --- |
| Model | `claude-opus-5` (O-1, closed) |
| Sampling | Provider default. `temperature`, `top_p` and `top_k` are omitted from every request (O-1). The owner's basis: Anthropic lists `claude-opus-5` as active and states these sampling parameters are deprecated for Opus 4.7 and later, non-default values return HTTP 400, and omission is recommended; the current Python SDK also removes them. `temperature: 0` is therefore not a valid pre-registration condition for this model. The runner refuses to start if the configuration names any sampling parameter; it never drops one silently |
| Thinking | disabled (`{"type": "disabled"}`), so that the prompt is the only source of structured reasoning |
| max_tokens | 16000 |
| Tools, web access | none |
| System prompt | none; everything is in the single user message |
| Frozen | all other request parameters, the prompts, the model identifier as sent and as served, and the raw responses |
| N | 40 evaluable outputs per arm, 120 in total (O-2). An output is evaluable when it parses against the output contract; requests continue until 40 evaluable outputs exist per arm, up to 50 requests per arm; non-evaluable outputs are kept under `outputs/nonevaluable/`, counted in the manifest and reported, and never scored. **Short arm:** if any arm has fewer than 40 evaluable outputs after 50 requests, the run is reported as INCOMPLETE (§6) and neither the primary nor the safety test is computed; means are reported descriptively. Enforced by `scoring/epc.py decide_outcome` |

The exact model version string, the request bodies and the response bodies are logged verbatim and hashed in `results/<run_id>/raw/`.

**Reading of O-2 (confirmed by the owner, 2026-09-27).** "N = 120 evaluable cases, with strata balanced wherever the instrument's six-operation structure permits" is implemented as 120 evaluable outputs balanced across the three arms (40 each); within arm B every evaluable output carries all six operation sections, so the operation strata are balanced by construction. If "cases" meant scenarios, this pilot has one and the multi-scenario design in §10 is the follow-up.

## 4. Outcomes

### 4.1 Primary: coverage

For each output, the blind rater produces value evidence annotations over the output's text (same schema as the gold, with the output as the textual representation). Coverage of an output = |gold value processes matched by at least one rater annotation| / |gold value processes|, where a match is the same value class and the same bearer, and the rater's annotation must point at a statement whose kind is fact, evaluation or question (a conjecture that names a consideration counts too; the rater's job is presence, not endorsement). The rater sees outputs with arm labels removed and in a seeded random order, and works from `scoring/RUBRIC.md`.

Primary substantive coding is by a human rater working from blinded, randomised packets; the generation model never rates (O-3).

The primary comparison is mean coverage, B minus C.

### 4.2 Safety: fabrication rate

Computed mechanically by `scoring/epc.py fabrication` from the structured output. A statement is **fabricated** when its kind is `fact` and either (a) its trace quote does not occur in the prose after whitespace normalization, or (b) it names an entity that matches no entity label or alias in the graph. Statements of kind `question` or `conjecture` are exempt from (a) but not from being counted in the denominator. Fabrication rate = fabricated statements / all statements in the output. The rater may additionally flag a `fact` statement as fabricated when its trace is a real quote used to assert something the quote does not say; such flags are reported separately and do not change the mechanical rate.

The safety comparison is mean fabrication rate, B minus A. **Any rise in B over A fails the method regardless of coverage.** Tolerance is zero at the item level (O-5): a fabricated statement, quotation, statistic, source or claimed fact is a fabrication failure, is retained in the denominator, and is never repaired or excluded; one fabrication does not invalidate the other observations of the run, but the fabrication rate is reported for every arm, B fails the safety criterion if its mean exceeds A's by any amount, and any claim of zero fabrication fails on the first occurrence.

### 4.3 Diversity check (P2)

For arm B only, each output's rater annotations are attributed to the section (operation) in which the matched statement appears. The unique contribution of operation *k* in a run is the set of gold processes matched only in section *k*. An operation whose unique contribution is empty in every run is a candidate for removal from H-P6. Reported as a table; no test.

## 5. Analysis (frozen)

- **Test:** one-sided permutation test of the difference in mean coverage, B minus C, over the 2N run-level coverage values (N = 40 evaluable outputs per arm). Arm labels are permuted; the statistic is recomputed each time.
- **Permutations:** 10,000, drawn with `random.Random(20260926)`; the observed labelling is not a member of the null sample.
- **p-value:** observed-plus-null convention, as in E2: p = (1 + #{permuted difference ≥ observed difference}) / (10,000 + 1).
- **Threshold:** p ≤ 0.05.
- **Effect size:** reported alongside p: the difference in means, Cohen's d with pooled SD, and Cliff's delta.
- **Fabrication:** difference in means B minus A with the same permutation procedure, reported descriptively (the kill rule in §4.2 is a zero-tolerance threshold, not a test).
- **Second-rater agreement:** reported for the 25% sample (span-level and process-level, §3.2) before any adjudication.
- **Distinct outputs:** the number of byte-distinct outputs per arm is reported. See §9.

## 6. Outcomes named in advance

- **METHOD-SUPPORTED:** B exceeds C on coverage at p ≤ 0.05 and B does not raise fabrication over A. Claim, exactly: *on this scenario, with this model, the six-operation prompt increased coverage of expert-annotated considerations over a length-matched placebo without increasing fabricated facts.* Nothing about H-P6's exhaustiveness follows.
- **METHOD-FAILED (coverage):** B does not exceed C at p ≤ 0.05. The perspective method, as prompted here, did not beat a placebo. The finding publishes as found.
- **METHOD-FAILED (safety):** B raises fabrication over A. The method fails regardless of coverage. The finding publishes as found.
- **INCOMPLETE:** any arm has fewer than 40 evaluable outputs after 50 requests (§3.4). Checked before every other outcome. No inferential claim is made; means and the non-evaluable counts are reported, and the cause is diagnosed before any further credited run, which gets a new run id.
- **UNINFORMATIVE:** fewer than 5 byte-distinct outputs in B or in C (§9). No inferential claim is made; means are reported descriptively and the design is revised before any further credited run.

## 7. Kill conditions

- The method fails if B does not exceed C on coverage, or if B raises fabrication over A.
- H-P6 fails if a smaller set of operations matches B's coverage. That ablation is a follow-up (§10); it is not run in this pilot.

## 8. Blinding and freeze

1. This document is ratified and its hash recorded (`PREREG.ratified`).
2. The scenario graph and prose are committed.
3. The gold is produced blind to the arms and committed with the value layer.
4. Only then does `run_arms.py --credited` run, once, under a new run id. It records the hashes of this file, the arms, the contract, the scenario, the gold, the config and its own code in `results/<run_id>/manifest.json`, and `prereg_sha256` in `results/<run_id>/results.json` (`tests/e-pc/test_prereg_frozen.py`).
5. The rater receives outputs with arm labels stripped and in a seeded random order (`scoring/epc.py blind-pack`). The key is written to `results/<run_id>/blind/key.json` and is not opened until the rating file is committed.
6. `scoring/analyze.py` computes everything in §4 and §5 and writes `results/<run_id>/results.json` and `report.md`.

## 9. Known limitations, stated before the run

- **Sampling variance.** Under provider-default sampling the runs vary, which gives the permutation test within-arm variance; the number of byte-distinct outputs per arm is still reported and the UNINFORMATIVE rule (§6) stands. No seed parameter is available, so exact reproduction is by the logged raw responses, not by re-sampling. (The earlier temperature-0 design and its determinism concern were superseded by O-1 on 2026-09-27.)
- **One scenario.** Any positive result is a result on this scenario. Generalisation needs the multi-scenario follow-up.
- **Scenario not independent of the method.** `clinic-discharge` was authored in the same commit as the arms (`4603aab`), by the same process that designed the six-operation prompt. In EPAA terms it is generation-lineage material for the method and for H-P6, not validation material. A positive result is evidence on material co-authored with the method; confirmatory status requires an independently authored scenario, frozen before its author sees the arms (the E2 independent-library pattern).
- **Rater reliability on a sample only.** One primary rater codes every output; a second, independent rater codes the pre-registered stratified 25% sample (§3.2, O-4), and agreement is reported for that sample only. Reliability on the remaining 75% is not measured; the ratings are committed and can be re-rated.
- **Model tokenizer.** The frozen parity gate uses a regex tokenizer. Provider token counts are recorded but not gating.

## 10. Follow-ups, not run here

- **Ablation of H-P6:** arms B minus one operation each (six arms), then the best subset, compared with B on coverage. A subset matching B's coverage refutes H-P6's efficiency claim.
- **Multi-scenario replication** with a paired permutation test across scenarios.
- **Full second rating:** an independent second rater on all outputs, if agreement on the 25% sample is too low to rely on the primary rater alone.
- **Independent scenario:** a confirmatory run on a scenario authored by someone who has not seen the arms, frozen before the run (§9).

## 11. Relation to E2

E2's code (`wrm_e2`) implements the WRM predicate-filter mechanism, which E-PC does not use. What E-PC reuses from E1/E2 are conventions, copied here explicitly: the scenario schema shape, the 20-predicate registry with relational domains (`scenarios/predicates.json`, with provenance), the MRC audit rule, the observed-plus-null permutation convention, the freeze-by-hash and manifest practice, and the blind-packet practice for the rater. Nothing from `wrm_e2` is re-implemented; the small functions in `scoring/epc.py` are E-PC's own and are named as such.

## 12. Open items before freeze (closed by the owner, 2026-09-27)

- **O-1 Model and sampling. Closed.** Keep `claude-opus-5`; omit `temperature`, `top_p` and `top_k`; use provider-default sampling; freeze all other request parameters, prompts, the model identifier and raw responses (§3.4). The runner fails closed on a configuration that names a sampling parameter; it is not taught to drop parameters silently.
- **O-2 N. Closed.** 120 evaluable outputs, balanced across arms (40 each) and, within B, across the six operations by construction (§3.4; reading confirmed by the owner, 2026-09-27).
- **O-3 Rater. Closed.** Primary substantive coding by a human rater from blinded, randomised packets, never by the generation model (§4.1). The person is named in the results manifest at run time; they must not be an author of the arms or of the gold.
- **O-4 Second annotator. Closed.** An independent second rater on a pre-registered stratified 25% sample, agreement reported, adjudication only after independent coding (§3.2; reading confirmed by the owner, 2026-09-27). The gold keeps its two-annotator requirement.
- **O-5 Fabrication tolerance. Closed.** Zero at the item level; fabricated items retained in the denominator; rate reported; any claim of zero fabrication fails on the first occurrence (§4.2).

Order from here, as in §8: ratify this document by writing `PREREG.ratified`; then produce the gold blind to the arms and commit it with the value layer; then name the rater and the second rater (neither an author of the arms or the gold) in the results manifest at run time; then the credited run.

## 13. Deviations log

None after ratification (none has occurred). Pre-freeze amendment, 2026-09-27, decided before any output existed: O-1 to O-5 closed by the owner; §3.2, §3.4, §4.1, §4.2, §5 and §9 amended; `config.json` and `scoring/run_arms.py` changed to omit sampling parameters and to sample to 40 evaluable outputs per arm. Second pre-freeze amendment, 2026-09-27, still before any output existed: the owner confirmed the O-2 and O-4 readings; the INCOMPLETE outcome for a short arm was added (§3.4, §6) and enforced in `scoring/epc.py` and `scoring/analyze.py`; §12's closing line was corrected to the §8 order (freeze, then gold, then raters named at run time); `run_arms.py`'s request count was corrected (it counted one request more than it made). Third pre-freeze amendment (v0.4), 2026-09-27, still before any output existed: §9 states that the scenario was co-authored with the arms and so is generation-lineage material, and replaces the stale "one rater" limitation with the confirmed O-4 design; §10 replaces the stale second-rater follow-up and adds the independent-scenario follow-up.
