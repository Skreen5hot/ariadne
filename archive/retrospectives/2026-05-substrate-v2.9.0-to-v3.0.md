# FNSR Substrate Retrospective Addendum: v2.9.0 → v3.0

**Audience:** FNSR-internal. Not public; not marketing.
**Scope:** The second architectural phase of the originally-scoped trajectory — what made it distinct from the v2.6.0 → v2.8.0 phase, what the substrate now does that it didn't before, and the closure context v3.1.0 ships against.
**Date:** 2026-05-19
**Companion to:** [2026-05-substrate-v2.6.0-to-v2.8.0.md](2026-05-substrate-v2.6.0-to-v2.8.0.md)

---

## 0. What this addendum is for

This is a companion document, not a standalone retrospective.

The v2.6.0 → v2.8.0 retrospective established the three substrate-move framing (substrate move via v2.6.0 audit primitives; discipline-chain move via v2.7.0 Pass 2a; verification-as-substrate move via v2.8.0). It closed against the milestone of substrate-operates-protocol-depth-at-machine-speed and named the build-order continuing through v2.9.0 → v3.0 → v3.1.0 without changing what v2.8.0 demonstrated.

That framing turned out to be partially right. The build-order did continue. What v2.8.0 demonstrated was not undone by what came after. But the v2.9.0 → v3.0 arc is not "continuation of the same trajectory under the same architecture." It's a **distinct architectural phase**: the substrate becoming self-hosting and self-documenting. Both phases together constitute the originally-scoped trajectory; v3.1.0 ships the terminal release.

The addendum names what the second phase did that the first did not, and what makes v3.0 a closure threshold rather than a milestone of comparable kind to v2.8.0.

---

## 1. The third substrate state

The first retrospective named two substrate states across the v2.6.0 → v2.8.0 arc:

- **Thin coordinator** (pre-v2.6.0): deterministic Python orchestrator dispatching subagents, with state in `state.jsonld` and a chained-hash audit trail per task. No first-class operator primitives; no protocol depth.
- **Operates protocol depth at machine speed** (v2.8.0): verification ritual with ten categories, LLM judgment with adversarial-critic mitigation, full Pass 2a/2b discipline chain, forward-track surface with operating commands, banking lifecycle with explicit state transitions.

v3.0 is the third state. The shift is small to name and large in property:

- **Self-documenting and enforcing** (v3.0): architectural patterns get explicit documentation as substrate primitives, mechanically validated across the agent corpus; semantic-memory mutation from retro turns is refused at the substrate level rather than guarded by operator discipline alone.

The shift from operates-to-enforces is the architectural difference. Every prior release added capability. v3.0 adds capability AND mechanically refuses the failure mode that capability would otherwise permit. `_check_no_semantic_memory_mutation` is the canonical example: the retro surface adds the capability to surface insights worth promoting to semantic canon, AND the substrate refuses any retro-surface task that attempts the promotion directly. The promotion path is the only path; the substrate enforces the property, not the operator.

The discipline that v2.8.0 demonstrated (substrate operates protocol depth at machine speed) became the discipline v3.0 enforces (substrate refuses anti-deliberate promotion). The shift is qualitatively different because what was previously preserved by careful operator discipline is now preserved by deterministic refusal.

This is not a trust-versus-distrust framing. The deliberate-promotion path exists because the operator IS trusted to deliberate well — the substrate's job is not to replace operator judgment but to make operator judgment the only viable path. The substrate enforces structure within which operator agency is preserved: the operator deliberates which candidacies promote, with what rationale, at what cycle; the substrate refuses the *silent* path that would bypass deliberation entirely. Operator agency is load-bearing; the silent-mutation path is what the substrate removes.

### Why this matters for FNSR

Normative apparatus that can be silently mutated degrades over time. Every uncaught mutation erodes the audit-trail-honesty property: future operators reviewing the canon cannot re-derive how each entry got there. The canon stops being trustworthy as evidence.

Normative apparatus the substrate mechanically protects from silent mutation preserves audit-trail honesty at scale. Every promotion event is citable; every refusal of an unauthorized promotion is citable; the gap between "canon entries that exist" and "canon entries that were properly promoted" is mechanically zero rather than dependent on operator discipline holding across years.

The synthetic moral person project requires this property at every level where normative apparatus could be silently mutated. v3.0 demonstrates the property is achievable in a small case — one CPS check, one surface (retro), one set of semantic-memory paths. The pattern scales: future surfaces with analogous semantic-memory boundaries inherit the same `_check_no_*_mutation` framework. The first instance is precedent.

---

## 2. The four ouroboros instances as self-hosting evidence

v2.9.0 shipped three operator-workflow tools: `test-runner` (configurable test suite dispatch), `template-sync` (deterministic cross-repo file replication), `git-committer` (safety-defaulted commit dispatch). Each tool was substrate-development-relevant, not subject-project-relevant — they exist to make substrate-development tractable, not because GraphWrite needed them.

The property v2.9.0 established: **substrate can ship its own improvements via substrate-shipped tooling.** Once the tooling existed, every subsequent release used it.

Four ouroboros instances followed, with v2.9.0's instance being self-referential in a slightly different shape than the three that followed:

1. **v2.9.0 enabling release.** The test-runner shipped IN v2.9.0; during its integration the substrate's own test suite (including the test-runner's own tests) ran against the developing tool. Self-referential at the development level: the tool was used during the development of the tool. This is genuine but a different shape than instances 2–4, where the release was shipped using already-shipped tooling from a prior release.
2. **v3.0-alpha.1.** First post-v2.9.0 release shipped via `template-sync` for cross-repo file replication; substrate-primitive documentation (BAO) + corpus-wide validation work (`TestBaoBoundsValidation`) constituted the work; test-runner validated the substrate's own test suite as part of the release checks.
3. **v3.0-alpha.2.** Anti-pattern enforcement framework + analytical-role corpus expansion + retro-applier + MAREP-Orchestrator BAO contract; template-sync + test-runner sustained at significantly different scope than alpha.1.
4. **v3.0 final.** Retro operationalization + Episodic→Semantic enforcement; template-sync + test-runner sustained at the highest-scope checkpoint in the v3.0 series.

The property is not "the substrate has tools." Many software projects have build tooling. The property is that **the substrate's tools are themselves substrate primitives** — they participate in the audit chain, follow the substrate's safety-by-default conventions, refuse externally-visible operations without operator-stated reasons, integrate with the same dispatch + CPS infrastructure as every other agent. Self-hosting is not "we use our own thing"; it's "our own thing is held to the same architectural discipline as everything else we ship."

### Why this matters for FNSR

The synthetic moral person project will require substrate that sustains its own development across years of evolution, not just months. Continuous operator-mediated cross-repo synchronization, continuous manual test validation, continuous ad-hoc commit composition would burn out the operator role at FNSR's time horizons.

Four ouroboros instances across three weeks is evidence the property is robust at current scope. It does not prove the property holds at larger scope; FNSR-level development will exercise the substrate's self-hosting under conditions the current trajectory hasn't yet faced (high-frequency release cadence; multi-year audit-chain continuity; cross-substrate-revision file replication). But the substrate's current self-hosting being demonstrably stable across qualitatively different scopes (operator-workflow tooling in v2.9.0; substrate-documentation in v3.0-alpha.1; behavioral-discipline corpus in v3.0-alpha.2; enforcement primitives in v3.0 final) is the strongest evidence available at current scale that the property is intrinsic rather than coincidental.

---

## 3. The three primitive docs as substrate self-documentation

Across the v3.0 series, the substrate gained a directory convention that did not previously exist: `surfaces/_primitives/<pattern>.md` for architectural patterns that span multiple surfaces. Three primitive docs landed:

- **Bounded-Authority Orchestrator (BAO)** — v3.0-alpha.1. The pattern by which LLM workers receive elevated responsibility over an assigned surface while remaining bounded by substrate enforcement, audit-chain visibility, surface scope, and no substrate-level privilege. Four bounds, named explicitly so future BAO instances inherit the property checklist rather than re-deriving it. First instance: generalized synthesist. Second: MAREP-Orchestrator. Future instances inherit.

- **Episodic → Semantic Promotion** — v3.0-alpha.2. The discipline by which observations move from episodic memory (recent, contextual) to semantic memory (stable, canonical) via deliberate operator-mediated promotion — never automatic accumulation. Three memory layers, two promotion boundaries, five surfaces where the pattern instantiates. The primitive doc names the discipline; v3.0 final's `_check_no_semantic_memory_mutation` enforces it.

- **Anti-Pattern Enforcement** — v3.0 final. The pattern by which named LLM failure modes become substrate-mechanical refusals via three structural properties (forbidden behavior at output level + deterministic detector + structured-error veto). Retroactively recognizes the substrate's pre-v3.0 CPS infrastructure as anti-pattern enforcement instances; documents the framework so future surfaces inherit the property triad.

Each doc occupies the same shape: primitive-id frontmatter; canonical reference back to MAREP v2.2 or earlier source; structural properties enumerated; instances listed by release; FNSR-relevance named explicitly. The shape is uniform because the docs are themselves substrate primitives — they conform to the convention they document.

Two corpus-wide pattern-conformance tests complement the docs:

- **`TestBaoBoundsValidation`** — walks every agent declaring `bao_pattern: true` and validates the four bounds at corpus level.
- **`TestReadOnlyContractValidation`** — walks every agent declaring `contract_class: read-only` and validates the property triad (read-only tools; required_outputs declared; refusal-contract documented in prompt).

The tests caught a real gap during v3.0-alpha.2 development: `verification-ritual-llm` (shipped in v2.8.0-alpha.3) lacked a documented refusal contract. The test surfaced the gap; the alpha.2 release added the missing section. This is pattern-conformance discipline working as designed — substrate self-validates during development, not just at release time.

What changed at v3.0 is **the substrate's documentation is itself substrate**. Before v3.0, architectural patterns lived in agent contracts, surface specs, CHANGELOGs, retrospectives. After v3.0, three patterns are first-class substrate primitives with mechanical validation. Future patterns inherit the discipline: drop a primitive doc at `surfaces/_primitives/<pattern>.md`; add a corpus-wide validation test if mechanical conformance is possible; document instances; ratify.

### Why this matters for FNSR

The synthetic moral person project will accumulate architectural patterns across years — far more than three. Without a substrate convention for documenting and validating those patterns, the patterns either drift (each implementer interprets them differently) or fragment (each surface invents its own enforcement). With the convention, patterns become substrate; future implementers inherit the documented contract; mechanical validation catches deviations before release.

v3.0's three primitives are a small case of what FNSR-larger-scope will require at much higher cardinality. The convention is portable; the validation pattern is portable; the discipline of "named pattern + structural properties + mechanical conformance test" is portable. The substrate-side precedent is set.

---

## 4. The MAREP absorption as architectural elegance

The v3.0 series began with three originally-scoped pieces from the build-order:

1. **Generalized synthesist** — extension of the existing v2.5.0 reviewer+critic reconciliation to N-stream synthesis.
2. **Phase-exit retro** — operator-dispatched retro workflow at phase boundaries.
3. **Phase-complete-declaration** — operator-authoritative declaration that a phase met its acceptance criteria.

In parallel, the Logic Team delivered MAREP v2.2 — a Multi-Agent Retrospective Engagement Protocol specification with its own normalization (the phase-exit retro IS one instance of MAREP retro), its own BAO pattern (the MAREP-Orchestrator role), its own Episodic→Semantic discipline, and its own anti-pattern enumeration.

The team's framing — phase-exit retro IS MAREP retro; generalized synthesist IS one BAO instance — was the architectural absorption decision. The decision preserved v3.0's originally-scoped three pieces while folding in:

- The MAREP normalization (the substrate's retro surface IS the MAREP-canonical structure)
- The BAO pattern formalization (substrate-primitive doc; first instance: generalized synthesist; second instance: MAREP-Orchestrator)
- The Episodic→Semantic discipline (substrate-primitive doc + enforcement mechanism)
- The anti-pattern enforcement framework (substrate-primitive doc + retro-surface CPS extensions + semantic-memory immutability)

Three checkpoints (v3.0-alpha.1, v3.0-alpha.2, v3.0 final), ~1500 LOC across substrate code + primitive docs + agent contracts + tests, ~150 new tests across the v3.0 series. Comparable scope to v2.8.0's four-checkpoint scope.

What made the absorption work was that **the architectural framing was load-bearing across both workstreams**. Treating the originally-scoped pieces as separate from MAREP would have required parallel design effort with redundant patterns — a generalized-synthesist BAO designed without reference to MAREP-Orchestrator's BAO; a phase-exit-retro Episodic→Semantic boundary designed without reference to MAREP's three-memory-layer model; a substrate anti-pattern framework designed without reference to MAREP's persona-theater / redundant-affirmation / freeform-brainstorm enumeration. The synthesis was substrate-relevant, not coordination-relevant: the shared patterns are what the substrate documents, and documenting them once with two instances is the architecture's right shape.

The absorption pattern is itself worth naming as a methodology refinement candidate. When two workstreams converge on the same architectural patterns under independent framing, the convergence is evidence the patterns are real (not artifacts of either team's specific lens). Substrate work that recognizes the convergence and synthesizes at the pattern level produces a smaller surface area than substrate work that ships both workstreams in parallel. The team's framing in the v3.0 entry-point conversation — "treat them as one body of architecture, not two" — was load-bearing for the entire v3.0 series.

### Why this matters for FNSR

The synthetic moral person project will face this convergence repeatedly. Normative apparatus authored from different lenses (moral-philosophical; computational; juridical; deliberative-procedural) will converge on shared architectural patterns. Treating each lens as producing a separate substrate would over-fit; treating them as converging on shared patterns under different framings preserves the architecture's coherence.

v3.0's MAREP absorption is the precedent: independent workstreams converged on BAO + Episodic→Semantic + anti-pattern-enforcement; substrate work synthesized at the pattern level; both originally-scoped and MAREP-derived instances inherit the same primitives. Future FNSR convergences inherit the absorption pattern.

---

## 5. The deliberate-promotion audit event as FNSR-load-bearing primitive

v3.0 final added `state_admin promote-candidate` — a command that emits a forward-track event with `declaration_kind: operator_deliberate_promotion`, recording:

- The candidate identifier and the semantic-memory destination
- The originating episodic source (retro-id; surfacing task)
- The operator's stated rationale for promotion
- The provenance back to the originating evidence

The command does not mutate semantic memory. It records the operator's deliberate-promotion intent as a citable audit event. The actual semantic-memory mutation goes through the standard ratification chain (reconnaissance → ratification → commit-finalize), which the substrate enforces via `_check_no_semantic_memory_mutation` as the only path.

This is the canonical pattern for **tacit-to-formal transitions**: observation accumulates in episodic memory (retro state; banking events; forward-track candidacies); operator reviews accumulated evidence at a deliberation cycle; operator surfaces a candidate via `promote-candidate` with rationale; ratification chain produces the canonical-memory mutation; the audit event is the citable moment of deliberate transition.

Three properties make the event FNSR-load-bearing:

1. **The promotion moment is explicit.** Future operators reading the audit chain see exactly when an observation crossed from episodic to semantic, who deliberated, what rationale was given, what evidence was cited. No silent accumulation.
2. **The provenance is preserved.** `surfacing_task_id` + `from_episodic` fields chain back to the originating retro and the originating evidence. The promotion event is not a freestanding decision; it is grounded in citable prior episodic record.
3. **The shape generalizes.** The event uses Spec 07's forward-track audit structure (`forward_track_id`, `state: A`, `sub_surface: internal-methodology-refinement`, `transition_history`) so the v2.8.0 `forward-track transition / list / aging` commands operate it without modification. Substrate's existing primitives carry the pattern.

The synthetic moral person project will reference this pattern at every normative promotion boundary — observation → considered practice → ratified canon. Each boundary needs the same three properties: explicit moment, preserved provenance, generalized shape.

v3.0 demonstrates the pattern in a small case: substrate retros producing PLAYBOOK / ADR / CLAUDE.md candidacies that go through the ratification chain. FNSR work at larger scope will exercise the pattern under conditions the substrate has not yet faced — high-stakes normative judgments, irreversible promotions, contested deliberations where rationale must withstand subsequent review by parties not present at the original promotion. The audit event's shape is what makes such review possible without reconstructing context the original participants never recorded.

The pattern is precedent. Whether it scales to FNSR's full requirements is an open question; that the substrate-side mechanism exists and is mechanically enforced is the prerequisite.

---

## 6. What isn't in the changelogs

Three observations the v3.0 release notes don't capture, recorded here for FNSR-archive continuity.

### The discipline applied recursively

v3.0 operationalized Episodic→Semantic promotion at the per-task level: the substrate refuses anti-deliberate promotion of episodic observations to semantic canon via `_check_no_semantic_memory_mutation` + the deliberate-promotion ratification chain.

The trajectory itself is closing via the same discipline applied to substrate-development as a body of episodic observations. This addendum is the trajectory-level promotion event: three weeks of substrate-development episodic record (CHANGELOG entries; gap-surfacing observations; checkpoint adjudications; commit history) deliberately promoted into the FNSR archive as semantic record.

The substrate eating its own dogfood at multiple scales — per-task discipline, per-promotion discipline, per-trajectory discipline. The recursive application is itself evidence the discipline is structural rather than scope-particular. A discipline that works at one scale but not at others would be a heuristic; a discipline that works at multiple scales is more likely an architectural property.

### Team operating-at-altitude across the second phase

The v2.6.0 → v2.8.0 retrospective named the team's operating mode as the pattern that produced v2.8.0's specific architecture. Across v2.9.0 → v3.0, that operating mode sustained without phase-particular adjustment:

- Two FNSR-archive-quality specifications produced (MAREP v2.2; MAREP integration spec) — exceeded the directive that produced them by surfacing architectural patterns rather than merely capturing requirements.
- Three substrate-primitive documents surfaced (BAO; Episodic→Semantic; anti-pattern enforcement) — recognized as cross-surface patterns warranting substrate-primitive documentation rather than feature-particular treatment.
- Two corpus-wide pattern-conformance tests established (`TestBaoBoundsValidation`; `TestReadOnlyContractValidation`) — mechanical pattern-conformance discipline that scales beyond current corpus size.
- Four ouroboros instances sustained — substrate's self-hosting property maintained across qualitatively different scopes.

The pattern that emerged in v2.6.0 → v2.8.0 sustained through v2.9.0 → v3.0. What was previously a phase-specific operating mode is now operating-mode-proper. The team operates above the level of feature-particular implementation; v3.0 ratifies that the mode is durable.

### The orchestrator role through the second phase

The first retrospective named the coordination cost the orchestrator absorbs. The question that retrospective left open: would the cost scale as substrate scope grew?

v2.9.0 → v3.0 exercised the question — not as a test the team set out to conduct, but as a byproduct of the work. The scope grew significantly: MAREP v1.1 absorption decision; seven open questions on the integration spec; BAO bounds refinement (CP1 adjudication); JSONPath subset call (CP2 adjudication); `inputs.surface: retro` attribution decision (CP2 adjudication); v2.9.0-first sequencing call (build-order adjudication); safety adjudications on git-committer shell execution; gap-surfacing-cadence ratifications at each of the v3.0 checkpoints; three CP3 implementation-pattern observations folded into the final release.

The orchestrator role did not become heavier as substrate scope grew. The patterns that worked in the first phase — blocking-vs-clarifying-vs-mechanical triage; defaults proposed with reasoning; refinements folded additively; meta-observations on FNSR-relevance integrated alongside substrate decisions — sustained through the second phase at higher cardinality of adjudications without changing shape.

This is the orchestrator-cost-scalability claim's first piece of evidence: at least across two architectural phases and three weeks of intensive substrate development, the coordination cost the orchestrator absorbs is sublinear in substrate scope. Aaron's pattern is what made this stable. The pattern's portability to other operators is a separate question; what's evident is that the specific orchestrator role across v2.6.0 → v3.0 was load-bearing in a way the substrate could not have generated alone.

---

## 7. What v3.1.0 ships against

v3.1.0 (`surface_audience`) is the originally-scoped trajectory's terminal release. The substrate's foundational design closes when v3.1.0 ships.

`surface_audience` is a single-primitive release per the original directive. The scope is small; the implementation pattern is established (drop a primitive doc at `surfaces/_primitives/`; integrate into existing surface specs; corpus-wide validation if applicable). The release ships when the orchestrator greenlights it.

What changes is the context v3.1.0 ships against. Prior releases in the trajectory shipped as "release N in an ongoing build-order"; v3.1.0 ships as "release N in a documented closure of the originally-scoped trajectory." The closure context is this addendum's purpose — naming the trajectory's foundational-design completion explicitly so v3.1.0's terminal-release status is preserved rather than blurred into an open-ended sequence.

What comes after v3.1.0 is either:

- **Substrate evolution beyond originally-scoped trajectory.** New primitives surfacing from FNSR-larger-scope work; new surfaces; new operator commands; new validation tests. Each addition would be its own deliberation under the substrate's existing patterns (BAO; Episodic→Semantic; anti-pattern enforcement) and would land via the substrate's existing release machinery (checkpoint cadence; gap-surfacing; build-incrementally pattern).
- **Substrate stabilization while FNSR-larger-scope work begins to consume it.** No new substrate scope; existing primitives exercised under FNSR conditions; bugs and gaps surfaced through use; refinements folded under maintenance cadence rather than feature-development cadence.

Which path is taken depends on what FNSR-larger-scope work surfaces as substrate-relevant. That decision is downstream of this addendum; the addendum's job is to mark the closure context, not to commit to subsequent scope.

---

## Closing

v2.9.0 → v3.0 shipped a substrate that self-hosts its own development, documents its own architectural patterns, mechanically enforces the discipline by which observations become canon, and operationalizes deliberate normative promotion as a citable audit event. That's the second architectural phase of the originally-scoped trajectory.

v2.6.0 → v2.8.0 demonstrated substrate-operates-protocol-depth-at-machine-speed. v2.9.0 → v3.0 demonstrates substrate-enforces-its-own-architectural-discipline. Both phases together close the substrate's foundational design; v3.1.0 ships against documented closure.

The retrospective addendum sits in the FNSR archive as the trajectory-level promotion event: episodic substrate-development record (three weeks; four releases; four ouroboros instances; three primitive docs; ~150 new tests) deliberately promoted into semantic FNSR record. The promotion is itself an instance of the discipline v3.0 enforces — applied recursively, deliberately, with provenance preserved.

The substrate's foundational design is complete after v3.1.0. What FNSR-larger-scope work builds on starts from there.

— Daemon Team, drafted from the v2.9.0 → v3.0 conversation arc
— For Aaron's FNSR archive
