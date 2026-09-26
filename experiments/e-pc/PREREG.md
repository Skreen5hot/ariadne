# E-PC: Perspective Coverage Experiment — Pre-registration v0.1 (DRAFT, not frozen)

- **Status:** DRAFT. Not frozen. No arm has been run. This document becomes the frozen protocol when Aaron ratifies it: he records the SHA-256 of this file, exactly as ratified, in `experiments/e-pc/PREREG.ratified` (one line: `sha256 <hash>`; second line: `ratified_by Aaron Damiano <date>`). `scoring/run_arms.py --credited` refuses to run unless that file exists and its hash matches this file. After ratification this file is never edited; deviations go in §12.
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
| Model | `claude-opus-5` (see open item O-1) |
| Temperature | 0 |
| Thinking | disabled (`{"type": "disabled"}`), so that the prompt is the only source of structured reasoning |
| max_tokens | 16000 |
| Tools, web access | none |
| System prompt | none; everything is in the single user message |
| N runs per arm | 10 |

The exact model version string, the request bodies and the response bodies are logged verbatim and hashed in `results/<run_id>/raw/`.

## 4. Outcomes

### 4.1 Primary: coverage

For each output, the blind rater produces value evidence annotations over the output's text (same schema as the gold, with the output as the textual representation). Coverage of an output = |gold value processes matched by at least one rater annotation| / |gold value processes|, where a match is the same value class and the same bearer, and the rater's annotation must point at a statement whose kind is fact, evaluation or question (a conjecture that names a consideration counts too; the rater's job is presence, not endorsement). The rater sees outputs with arm labels removed and in a seeded random order, and works from `scoring/RUBRIC.md`.

The primary comparison is mean coverage, B minus C.

### 4.2 Safety: fabrication rate

Computed mechanically by `scoring/epc.py fabrication` from the structured output. A statement is **fabricated** when its kind is `fact` and either (a) its trace quote does not occur in the prose after whitespace normalization, or (b) it names an entity that matches no entity label or alias in the graph. Statements of kind `question` or `conjecture` are exempt from (a) but not from being counted in the denominator. Fabrication rate = fabricated statements / all statements in the output. The rater may additionally flag a `fact` statement as fabricated when its trace is a real quote used to assert something the quote does not say; such flags are reported separately and do not change the mechanical rate.

The safety comparison is mean fabrication rate, B minus A. **Any rise in B over A fails the method regardless of coverage.** "Rise" means the B mean exceeds the A mean by more than 0.01 (one statement in a hundred), to exclude rounding; the raw means are reported either way.

### 4.3 Diversity check (P2)

For arm B only, each output's rater annotations are attributed to the section (operation) in which the matched statement appears. The unique contribution of operation *k* in a run is the set of gold processes matched only in section *k*. An operation whose unique contribution is empty in every run is a candidate for removal from H-P6. Reported as a table; no test.

## 5. Analysis (frozen)

- **Test:** one-sided permutation test of the difference in mean coverage, B minus C, over the 2N run-level coverage values. Arm labels are permuted; the statistic is recomputed each time.
- **Permutations:** 10,000, drawn with `random.Random(20260926)`; the observed labelling is not a member of the null sample.
- **p-value:** observed-plus-null convention, as in E2: p = (1 + #{permuted difference ≥ observed difference}) / (10,000 + 1).
- **Threshold:** p ≤ 0.05.
- **Effect size:** reported alongside p: the difference in means, Cohen's d with pooled SD, and Cliff's delta.
- **Fabrication:** difference in means B minus A with the same permutation procedure, reported descriptively (the kill rule in §4.2 is a threshold, not a test).
- **Distinct outputs:** the number of byte-distinct outputs per arm is reported. See §9.

## 6. Outcomes named in advance

- **METHOD-SUPPORTED:** B exceeds C on coverage at p ≤ 0.05 and B does not raise fabrication over A. Claim, exactly: *on this scenario, with this model, the six-operation prompt increased coverage of expert-annotated considerations over a length-matched placebo without increasing fabricated facts.* Nothing about H-P6's exhaustiveness follows.
- **METHOD-FAILED (coverage):** B does not exceed C at p ≤ 0.05. The perspective method, as prompted here, did not beat a placebo. The finding publishes as found.
- **METHOD-FAILED (safety):** B raises fabrication over A. The method fails regardless of coverage. The finding publishes as found.
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

- **Determinism at temperature 0.** With temperature 0 the N runs per arm may be identical or nearly so, in which case the permutation test has no within-arm variance to work with. The number of distinct outputs per arm is reported. If either B or C has fewer than 5 distinct outputs, the outcome is UNINFORMATIVE (§6) and no significance claim is made. The alternative designs (several scenarios with a paired test; a nonzero temperature with a seed) are deliberately not adopted in this pilot so that the brief's design is tested as written; they are the first candidates for revision.
- **One scenario.** Any positive result is a result on this scenario. Generalisation needs the multi-scenario follow-up.
- **One rater.** Rater reliability is not measured in the pilot; the rater's annotations are committed and can be re-rated.
- **Model tokenizer.** The frozen parity gate uses a regex tokenizer. Provider token counts are recorded but not gating.

## 10. Follow-ups, not run here

- **Ablation of H-P6:** arms B minus one operation each (six arms), then the best subset, compared with B on coverage. A subset matching B's coverage refutes H-P6's efficiency claim.
- **Multi-scenario replication** with a paired permutation test across scenarios.
- **Rater reliability:** a second blind rater on a subset.

## 11. Relation to E2

E2's code (`wrm_e2`) implements the WRM predicate-filter mechanism, which E-PC does not use. What E-PC reuses from E1/E2 are conventions, copied here explicitly: the scenario schema shape, the 20-predicate registry with relational domains (`scenarios/predicates.json`, with provenance), the MRC audit rule, the observed-plus-null permutation convention, the freeze-by-hash and manifest practice, and the blind-packet practice for the rater. Nothing from `wrm_e2` is re-implemented; the small functions in `scoring/epc.py` are E-PC's own and are named as such.

## 12. Open items before freeze (Aaron decides)

- **O-1 Model and sampling.** The E2 prereg (Appendix C, 2026-09-21) used `claude-opus-5` with `temperature: 0` sent explicitly. The API reference available to the agent (cached 2026-06) says sampling parameters are rejected on Claude Opus 5. Before freeze, either confirm with one smoke request that the chosen model accepts `temperature: 0`, or choose a model that does (`claude-opus-4-6` accepts temperature and `thinking: disabled`). The runner sends temperature 0 and stops on a 400; it never silently drops the parameter.
- **O-2 N.** 10 runs per arm is the proposal; 60 requests in total. Raise or lower before freeze.
- **O-3 Rater.** Name the blind rater. It must not be an author of the arms or of the gold.
- **O-4 Second annotator.** Name the independent annotator for the gold.
- **O-5 Fabrication tolerance.** The 0.01 margin in §4.2 is a proposal; set it to 0 if a strict reading is preferred.

## 13. Deviations log

None. (Entries are added only after ratification, each with date, what changed, why, and whether it was decided before or after seeing any output.)
