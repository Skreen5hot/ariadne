# FNSR Substrate Retrospective: Phase 1 (substrate-in-operation)

**Audience:** FNSR-internal. Not public; not marketing.
**Scope:** What the substrate's first sustained run in subject-project mode demonstrated, the operating characteristics that surfaced, the gap-evidence accumulated for v3.2 design, and the FNSR-relevance of the substrate-as-substrate property holding end-to-end.
**Date:** 2026-05-20
**Companion to:** [2026-05-substrate-v2.6.0-to-v2.8.0.md](2026-05-substrate-v2.6.0-to-v2.8.0.md) (first architectural phase) + [2026-05-substrate-v2.9.0-to-v3.0.md](2026-05-substrate-v2.9.0-to-v3.0.md) (second architectural phase + originally-scoped trajectory closure)

---

## 0. What this addendum is for

The prior two retrospectives documented the substrate's foundational design across v2.6.0 → v3.1.0 — the originally-scoped trajectory that closed with v3.1.0's `surface_audience` primitive. Both retrospectives covered **substrate-development mode**: the substrate building itself.

Phase 1 of GraphWrite was the first sustained run of the substrate in **subject-project mode** — the substrate dispatching real subject-project work (a deterministic JSON-LD VMP authoring toolkit) using the apparatus that v2.6.0 → v3.1.0 built. Different operating regime; different test of the substrate's claims.

This retrospective documents what that first sustained subject-project-mode run demonstrated. It is the third in the series, but structurally different from the prior two: where they captured substrate-development arcs, this captures substrate-in-operation evidence.

The pattern these three retrospectives together describe: substrate designed (v2.6.0 → v2.8.0); substrate self-validates + self-documents (v2.9.0 → v3.0); substrate operates in production (Phase 1).

---

## 1. What shipped, in twelve substantive tasks

Phase 1 of GraphWrite was specified as twelve P1 tasks against the v0.4 Visual Modeler Profile spec. All twelve closed at substrate-side via the H2 preventive-deferral pattern.

| Task | Surface | Module |
|---|---|---|
| 1.1 | VMP Canonical Serializer (§5.2 / §5.3 / §5.4) | `src/kernel/canonicalize.ts` (extended) |
| 1.2 | Project TBox Bundle (§5.14) | `src/tbox/` |
| 1.3 | Structural Validator (§17.1–§17.4; §5.13) | `src/validate/` (2 of 26 codes shipped; 24 forward-tracked) |
| 1.4 | Semantic Projection (§6.3 / §8.2 / §8.3) | `src/projection/` |
| 1.5 | Emitters (FR-C003 through FR-C008) | `src/emit/` (Turtle + N-Triples + Markdown + Triple Narration shipped; semantic-jsonld + Mermaid forward-tracked) |
| 1.6 | IRI Generation (§9.2 / §9.3 / §13.9) | `src/iri/` |
| 1.7 | Cascading IRI Update with Collision Detection (§13) | `src/refactor/` (with 50-sample property-based tests) |
| 1.8 | Export-Manifest Data Structure (§5.15 / §19) | `src/manifest/` |
| 1.9 | Legacy Migration (§10.3–§10.5) | `src/migrate/` (resolved `ft-097-test-validator-3` open question) |
| 1.10 | Canonical Normalization on Load (§5.3) | `src/normalize/` |
| 1.11 | Node CLI Surface (§23 / §12.2) | `src/cli/` (8 of 8 ACs) |
| 1.12 | Test Harness (§21.1–§21.4) | hand-rolled framework preserved; fast-check added for property-based; per-task tests across all 12 surfaces |

**Final test count: 106 passing / 0 failing across 14 spec test files.** Test count growth across Phase 1: 0 → 17 → 26 → 40 → 47 → 60 → 67 → 74 → 84 → 92 → 97 → 105 → 106. Each task added its own spec tests; no task regressed prior tests.

**Implementation surface:** 10 new top-level src/ directories + 1 extended existing kernel file. ~3500 lines of TypeScript shipped. Zero runtime dependencies added (per CLAUDE.md §6 substrate constraint); devDeps: `n3` + `@types/n3` for Turtle/N-Triples emission; `fast-check` for property-based tests.

What this demonstrates: the substrate's chain machinery (reconnaissance → ratification → commit-finalize, with verification-ritual + test-runner where applicable) operated end-to-end across twelve substantively different surfaces — pure-functional canonical serializer, ontology TBox declaration, semantic validation, graph projection, multi-format emission, deterministic ID generation, cascading refactor with collision detection, hash-based manifest construction, multi-step legacy migration, normalization-on-load with marker propagation, full CLI command surface with stubs and path containment, framework configuration with property-based testing. Twelve distinct domains; same chain shape; same discipline; same audit-chain machinery throughout.

---

## 2. The substrate-as-substrate property held end-to-end

The v2.9.0 → v3.0 retrospective named three substrate states (thin coordinator → operates protocol depth → self-documents and enforces). Phase 1 was the test of whether the third state's property — substrate-as-substrate operating cleanly in its actual intended configuration — held when subject-project work was the load.

It held. Specifically:

### Defer-rather-than-degrade operated in both modes

The substrate's defer-rather-than-degrade property (PLAYBOOK §7.5 Property 4) operated twelve times across Phase 1's tasks. First demonstration was **reactive** (task 1.1's closure chain failed twice; R9 adjudicated deferral after the failure surfaced). Subsequent eleven demonstrations were **preventive** (operator recognized the pattern from gap-11's scope-dependent reconnaissance failure mode; deferred subsequent task closures pre-emptively without spending dispatches to confirm predictable failure).

Twelve forward-tracks now sit at the `v3.2-design` deliberation cycle; one was resolved to State C via task 1.9 implementation (the MISSING_REALIST_ANCHOR / LEGACY_REALIST_ANCHOR_PLACEHOLDER interaction). When v3.2's contract-visibility refinement ships, those twelve forward-tracks re-dispatch as v3.2's first validation tasks — Phase 1's deferred work closes through the substrate's own discipline rather than through ad-hoc operator-side correction.

The reactive-vs-preventive distinction was unlocked for explicit PLAYBOOK documentation by the third demonstration (task 1.3 closure); the discipline-update landed mid-Phase-1. That's the substrate's discipline operating preventively at the meta-level — the operator's pattern recognition became substrate-canonical documentation when the empirical evidence reached its threshold.

### Character-level fidelity preservation caught real corruption

The applier's strict before-match-before-write discipline (PLAYBOOK §7.5 Property 1) caught real U+FFFD-bearing developer output during the task 1.1 mojibake-cleanup recovery chains. The developer's emitted output contained Unicode replacement characters from a JSON-decoding mishap on the cp1252 dispatch boundary; the applier refused to write the corrupted content because the proposed `before` snippet didn't match disk. The corruption never landed.

This is the substrate's defense against developer-output encoding errors operating at the structural level — not as a hygiene check, but as semantic-memory integrity preservation. The property generalizes to any future subject-project work where developer-shaped agents produce output that mutates canonical state.

### Partial-application graceful degradation operated as designed

Three cleanup applier tasks (065, 068, 078) each landed most of their proposed changes while a small number failed `before_not_found`. The applier preserved successful changes on disk while recording both `applied[]` and `failed[]` lists in the audit chain. CPS vetoed the task overall (status: `blocked`) but the substantive work that landed was not rolled back.

Recovery from partial-application proved composable with the rest of the substrate's discipline: operators inspected audit chains to identify what remained; follow-up chains addressed the remainder; the final cleanup converged with one known-residual mojibake instance (documented in audit chain rather than silently ignored or aggressively retried). Substrate degrades gracefully under partial failure rather than going from "working" to "broken."

### Drift detection surfaced real cross-repo asymmetry

Mid-Phase-1, a routine `template-sync --mode verify` before a small PLAYBOOK update surfaced 15 files of accumulated drift in the barcode-template repo relative to GraphWrite and AgenticDev. The substrate detected its own state-corruption (asymmetric sync history) and surfaced it as a structured observation. The operator's discipline (operator-review-before-queuing for bulk action) gated the correction; the substrate did not auto-correct.

This is gap-10 in the registry; the barcode-template-catch-up workitem remains separate from Phase 1 substantive work but the drift detection itself is substrate-property evidence — the substrate refused to let asymmetric sync stay invisible.

---

## 3. The gap-evidence accumulated for v3.2

Phase 1 surfaced **14 gaps** documented in V3.2-GAP-REGISTRY.md. The framing hypothesis (substrate behaviors that defend against subject-project-mode operator-side assumptions and environment-side asymmetries and LLM-instruction-fidelity / LLM-knowledge-completeness limits) holds across 11 of 14 directly + 1 indirectly. Of the remaining two, one is subject-project-side (gap-5; npm install) and one is operator-process refinement (gap-14; scope-ambiguity handling for continuous-delivery mode).

### Sub-families that consolidated during Phase 1

| Sub-family | Gaps | v3.2 refinement candidate |
|---|---|---|
| Environment-side asymmetry (Windows cp1252 encoding) | 6, 8, 9 | Consolidate as one larger v3.2 refinement targeting the encoding boundary |
| Append-time validation | 2, 7 | Substrate-side constraints caught at task-append rather than runtime |
| Lifecycle / synchronization | 1, 4, 10 | Daemon lifecycle commands; queue-vs-dispatch buffer; template-sync default-all-targets |
| LLM-instruction-fidelity / knowledge-completeness | 6, 11, 12, 13 | Contract-visibility refinement at dispatch time; substrate-side tsc-no-emit gate |
| Pre-test-runner type-correctness | 13 | Substrate-side build-check between applier and test-runner |
| Operator-process refinement | 14 | Documentation + scope-default-citation pattern |

The hypothesis strengthened across the twelve tasks: each substantive completion produced gaps fitting the existing frame more often than not. v3.2's coherent thematic frame is now confirmed empirically: **substrate clarity refinements rather than substrate capability expansions** — the existing discipline is correct; v3.2 makes it more legible to LLM agents and operators.

### Gap-13's developer-discipline-adoption arc is worth holding

Gap-13 (TypeScript type errors caught at test-runner step rather than earlier) fired on **tasks 1.5 and 1.6** — both N3.js-based work (turtle/n-triples emitters; UUIDv5 generation). The pattern was: developer agent produces code that compiles in its mental model but doesn't satisfy library type constraints; test-runner catches the build failure; forward-correction chain fixes it.

**Tasks 1.7 onward (1.7, 1.8, 1.9, 1.10, 1.11, 1.12) did not exhibit the failure**, despite continuing to integrate with `@types/node` crypto APIs and `@types/fast-check`. The operator-side discipline — explicit "TypeScript: compile cleanly per gap-13 caution" in developer inputs — proved sufficient to suppress recurrence. The substrate gap remains a v3.2 candidate (substrate-side tsc-no-emit gate would prevent it more fundamentally), but the empirical evidence shows operator-side discipline can absorb the gap when properly applied.

This is significant for FNSR-relevant reasoning: substrate-side enforcement is not always required immediately when a gap surfaces. Operator-side discipline can mitigate while v3.2 refinement is scoped + designed. The substrate's audit-chain machinery captures both the gap firing and the discipline-adoption that suppressed recurrence; v3.2 design has both data points to work from.

---

## 4. The operating mode that produced the result

The v2.9.0 → v3.0 retrospective named the team's continued operating-at-altitude through that phase. Phase 1 extended that mode under different conditions — production substrate work consuming the substrate's apparatus rather than producing substrate refinements.

Specifically, three operating patterns held through Phase 1's first day of sustained work:

### Continuous-delivery without checkpoint blocking

Tasks 1.1 through 1.12 ran as a continuous sequence of chain dispatches. No checkpoint pauses between tasks; H2 closure between substantive completions; immediate next-task dispatch after closure. The build-incrementally pattern from v2.6.0+ scaled to a 12-task sustained operating run without modification.

When recoveries surfaced (gap-2 source_task; gap-7 token-limit; gap-13 type errors twice), the recovery chains operated under the same discipline — recon → developer → architect → applier → test-runner — and resolved without abandoning the original work. Five forward-correction chains across the twelve tasks. Each preserved audit-chain honesty about both the original dispatch and the correction.

### Pre-drafting + pipelining

The team pre-drafted subsequent task chains while predecessors ran. By the time task 1.4 completed, task 1.5 chain JSON existed; by task 1.6 completion, task 1.7 chain was queued for dispatch. This reduced the wall-clock between task completions to operator-action time rather than chain-design time.

The pattern surfaces a substrate property worth noting: chain JSONs are operator-side workitems, not substrate-canonical artifacts. The audit chain in `state.jsonld` IS the canonical record; the chain JSONs are dispatch payloads consumed at queue-time and irrelevant afterward. Pre-drafting them as scratch artifacts (now gitignored) accelerated the workflow without compromising substrate-discipline. The state.jsonld + audit chain remain the system of record.

### Operator-action for canonical-tooling-suggested fixes

Two operator-action operations occurred during Phase 1: `npm install` after gap-5 surfaced (task 1.1's first test-runner found missing node_modules) and `npm i --save-dev @types/n3` after gap-12 surfaced (task 1.2's first test-runner found missing TypeScript types). Both were canonical-npm-tooling-suggested fixes where the test-runner itself surfaced the exact command to run.

This established a boundary worth holding explicitly: **standard tooling commands are operator infrastructure; agent-proposed mutations are chain machinery.** The chain pattern (reconnaissance → ratification → commit-finalize) exists because agent-proposed changes need ratification — the LLM might be wrong, the change might exceed scope, the rationale might miss something a human architect would catch. None of that applies when test-runner explicitly suggests a one-line tooling command that any developer would run by reflex.

The boundary is consistent with the gap-14 framing that surfaced later: continuous-delivery doesn't mean "never ask"; it means "ask via gap-surfacing rather than via blocking." Standard tooling fits the same shape — execute via canonical mechanism + document in audit context if the operation has substrate-relevance.

---

## 5. FNSR-relevance of what Phase 1 demonstrated

The synthetic moral person project requires substrate that operates real subject-project work without degrading. Phase 1 demonstrated this property in a small case — twelve tasks against the v0.4 VMP spec, ~3500 lines of TypeScript, 106 spec tests, 60+ chain dispatches across the substrate's machinery, with the substrate-as-substrate property holding throughout.

Four FNSR-relevant claims that Phase 1 substantiated:

### Subject-project work consumes the substrate without contributing substrate-development

The substrate-vs-subject-project separation that the Phase 1 transition message named (substrate dispatches subject-project work; subject project consumes substrate without contributing to substrate development; v3.2 ships when subject-project work surfaces a substrate need) operated in production. Phase 1 produced GraphWrite's Phase 1 deliverable; substrate code did not change during Phase 1 work. Gaps surfaced were recorded in V3.2-GAP-REGISTRY for future substrate refinement; the substrate itself remained stable across all twelve task closures.

The role-separation property holds. The synthetic moral person project at larger scope will exercise the same property — apparatus building moral apparatus consumes the substrate; substrate refinement happens between consumption episodes, not during them.

### The chain machinery produces canonical state that's honest about deferrals

Twelve forward-tracks at the `v3.2-design` deliberation cycle plus three additional follow-up forward-tracks (per-code fixtures; emitter scope-split; barcode-template catch-up) plus one resolved-to-State-C forward-track means **the audit chain captures every deferral with explicit re-dispatch commitment**. No work was silently dropped. No work was retroactively documented. The substrate's discipline of "deferral is a substrate-attested event, not a procedural shortcut" held across all twelve task closures.

This is the load-bearing FNSR property. The synthetic moral person project will accumulate deferred work across years of operation. Each deferral must be citable, re-dispatchable, and grounded in evidence. Phase 1 demonstrated the substrate can sustain this at the scale of twelve simultaneous active deferrals; the property scales to N forward-tracks under the same machinery.

### LLM-discipline gaps absorb cleanly via the gap-surfacing + recovery patterns

Gaps 6, 11, 12, 13 are all LLM-side knowledge or instruction-fidelity gaps. The substrate's chain machinery caught each at the appropriate boundary (CPS structured-error veto for shape compliance; test-runner for build failures; applier for character-level corruption). Recovery patterns absorbed each: refined inputs (gap-11 attempt); operator-action via standard tooling (gaps 5, 12); forward-correction chains (gaps 13, partial-application stragglers); proactive R9 deferral (gap-11 confirmed scope-dependence).

The pattern that emerged: **LLM-discipline gaps fire predictably and absorb cleanly.** Each gap surfaced once or twice, then either suppressed via operator-side discipline (gap-13's task-1.7-through-1.12 non-recurrence) or deferred via R9 to v3.2 (gap-11). The substrate-discipline + operator-side pattern recognition together kept the workstream moving while accumulating evidence for v3.2 design.

The synthetic moral person project will face this property at every LLM dispatch boundary. Phase 1 demonstrates the substrate's machinery + operator's discipline together produce a sustainable operating pattern under LLM-knowledge-fidelity limits.

### Canonical state preserves audit honesty across substrate revisions

GraphWrite's `state.jsonld` now contains 160+ chain-hashed audit entries spanning v2.6.0 substrate work + Phase 1 subject-project work. The audit chain is contiguous; the hash-chain integrity remains verifiable across substrate revisions (v2.6.0 entries chain into v2.7.0 entries chain into v2.8.0 entries chain into v3.0 entries chain into Phase 1 entries; no break). The substrate's append-only invariant held across roughly one month of intensive development.

This is the FNSR-load-bearing reproducibility property. The synthetic moral person project will accumulate audit chain entries across years. Each entry must remain verifiable; each must chain cleanly back through every prior substrate revision. Phase 1 demonstrates the property holds across the substrate's first major operating-regime transition (substrate-development → subject-project mode); the same property must hold across all future transitions.

---

## 6. What's worth noting that isn't in the documentation

Three observations the canonical Phase 1 docs don't capture:

### The cost-of-error stayed bounded

Phase 1 surfaced 14 gaps. Recovery cost in LLM dispatches: roughly $50-100 in compute across all recovery chains (gap-7's three failed attempts at $8.79 was the single most expensive recovery; subsequent recoveries averaged $2-5 each). Wall-clock cost: roughly 18 hours of sustained operating time including all recoveries, demo-prep, and the milestone commit + push. Operator-attention cost: continuous involvement during dispatches with H2 closures between each task.

The cost stayed bounded because the substrate's audit-chain visibility made each failure diagnosable quickly. Failed dispatches surfaced the precise failure mode in audit-event payloads; recovery chains addressed the specific issue without re-litigating prior work; partial-application semantics preserved completed work during recovery dispatches.

Compared to traditional retrospective-after-failure operating modes, the cost is small. The substrate's discipline produced both the work AND the diagnostic information sufficient to recover from each failure cheaply.

### The team's continuous-delivery operating mode adapted under different attention contexts

Phase 1 ran across multiple attention contexts: dense supervisory mode (early tasks 1.1-1.3 with operator engagement on each adjudication); reduced-supervision continuous-delivery (tasks 1.4-1.12 with operator confirming patterns + delegating execution); occasional intervention for substrate-discipline questions (R9 deferral framing; gap-14 scope-ambiguity refinement; cleanup of remnants).

The substrate-discipline patterns survived all three contexts. R9 deferral was first reactive (intervention-heavy) then preventive (autonomous). Gap-14 was surfaced reactively (operator noticed the stop-at-task-1.12 pattern) and refined into a substrate-pattern observation. Cleanup of remnants was surfaced reactively (operator noticed inconsistent ready-count) and absorbed into the R9 pattern's documentation.

What this demonstrates: substrate-as-substrate doesn't require constant operator attention. The discipline machinery operates correctly under variable supervision; gaps surface to whatever operator-attention is available; recoveries route through whatever continuation pattern is current. The synthetic moral person project will require this property — operator attention will not be uniform across years; the substrate's machinery must operate correctly across that attention variance.

### The retrospective addendum pattern is now substrate-canonical

Three retrospectives in the FNSR archive now: v2.6.0 → v2.8.0 (substrate-development phase 1); v2.9.0 → v3.0 (substrate-development phase 2 + originally-scoped trajectory closure); Phase 1 (substrate-in-operation first sustained run). Each retrospective serves dual purpose: contemporaneous record + future-operator orientation document.

The pattern's emergence wasn't designed in advance — it crystallized over the prior two retrospectives. This third one consolidates it: **retrospectives mark substrate-trajectory transitions**, not just substrate-release milestones. The v2.6.0 → v2.8.0 retrospective marked the substrate becoming protocol-depth-operable; the v2.9.0 → v3.0 retrospective marked the originally-scoped trajectory closure; this retrospective marks the substrate-as-substrate property holding in its actual intended configuration for the first time.

Future retrospectives in the archive should follow the same pattern: trajectory transitions, not just releases. The synthetic moral person project's future retrospectives can draw on the structural precedent these three set.

---

## 7. What v3.2 ships against

When v3.2 design is greenlit, this retrospective + V3.2-GAP-REGISTRY.md together provide the empirical foundation. The framing hypothesis is now well-substantiated; the sub-families consolidate into a coherent themed release; the twelve forward-tracks at `v3.2-design` cycle become v3.2's first validation tasks.

Specific v3.2 work that Phase 1's evidence prioritizes:

1. **Contract-visibility refinement** for narrow-scope reconnaissance (gap-11; substrate-side enforcement now confirmed required after operator-input refinement was falsified)
2. **Environment-side encoding boundary consolidation** (gaps 6, 8, 9; substrate-side encoding hygiene at the Windows cp1252 boundary)
3. **Pre-test-runner type-correctness gate** (gap-13; substrate-side tsc-no-emit step between applier and test-runner)
4. **Append-time validation refinements** (gaps 2, 7; constraints caught at task-append rather than runtime)
5. **Lifecycle + synchronization commands** (gaps 1, 4, 10; daemon lifecycle + queue-vs-dispatch buffer + template-sync default-targets)
6. **Substrate-doc refinements** (gaps 3, 14; chain-shape-by-artifact-kind already landed; scope-ambiguity-handling pattern documented)

The v3.2 release ships when the design is scoped sufficiently; the empirical foundation from Phase 1 is sufficient to begin scoping now. The release's first validation tasks (the twelve deferred closure chains) will exercise whether v3.2's refinements actually resolve the gaps they're scoped against.

---

## Closing

Phase 1 of GraphWrite shipped a working Node CLI implementing twelve substantive surfaces against the v0.4 VMP spec, with 106/106 tests passing across 14 spec test files, 14 gaps documented for v3.2 design, and the substrate-as-substrate property holding end-to-end across twelve task closures + five recovery chains.

The substrate's foundational design — built across v2.6.0 → v3.1.0 — operated correctly in production for the first sustained subject-project-mode run. Defer-rather-than-degrade held in both reactive and preventive modes. Character-level fidelity preservation caught real corruption. Partial-application graceful degradation operated cleanly. Drift detection surfaced real cross-repo asymmetry. The audit chain captured every dispatch, every failure, every recovery, every deferral.

The synthetic moral person project will require substrate that does exactly this at much larger scale. Phase 1 demonstrates the foundational discipline is right. v3.2 makes the discipline more legible; the discipline itself doesn't change.

The retrospective addendum sits in the FNSR archive as evidence of the substrate-as-substrate property operating in production. Future participants reviewing the moment when the substrate crossed from designed-property to demonstrated-property at production scale have this document as the anchor.

— Daemon Team, drafted from the Phase 1 conversation arc
— For Aaron's FNSR archive
