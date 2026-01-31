# Tension Log

## Active Tensions

### T-001: Character Feedback vs. Auditability
- **First identified**: 2026-01-30
- **Specs involved**: FNSR, ARCHON, The Plot
- **Nature**: ARCHON requires character to feed back into decisions (otherwise moral injury is theater). But feedback creates "hidden variables" that make the system non-deterministic.
- **Current resolution**: Feedback is real but auditable — moral injury increases intervention thresholds proportionally, visible in decision logs.
- **Status**: Resolved in principle, pending implementation validation

### T-002: Decidability vs. Expressiveness
- **First identified**: 2026-01-30
- **Specs involved**: MDRE, The Plot
- **Nature**: Core reasoning must stay in decidable FOL for guaranteed termination, but real-world problems require SOL, temporal reasoning, probabilistic inference.
- **Current resolution**: Hybrid architecture with external solvers (SMT, Allen's algebra, Bayesian networks), clear hand-off protocols, graceful degradation.
- **Status**: Resolved in principle, V3.0 implementation pending

### T-003: Autonomy vs. Safety
- **First identified**: 2026-01-30
- **Specs involved**: FNSR, The Plot
- **Nature**: Users want a system that acts without constant supervision; safety requires human oversight on high-stakes decisions.
- **Current resolution**: Tiered autonomy (Tier 0–4) based on stakes and confidence.
- **Status**: Resolved in principle

### T-004: Speed vs. Rigor
- **First identified**: 2026-01-30
- **Specs involved**: FNSR, The Plot
- **Nature**: Users want fast responses; rigor requires full epistemic/ethical checking.
- **Current resolution**: Query path tiers — fast (<100ms), standard (<500ms), full (<2s).
- **Status**: Resolved in principle

### T-005: Value Pluralism vs. Action
- **First identified**: 2026-01-30
- **Specs involved**: IEE, The Plot
- **Nature**: 12 worldviews may judge differently, but the system must actually make decisions.
- **Current resolution**: IEE tiered evaluation with deadlock protocol — 3 sentinel worldviews for most decisions, full 12 for contested, human escalation on deadlock.
- **Status**: Resolved in principle

### T-006: Character Model Pluralism
- **First identified**: 2026-01-30 (ARIADNE coherence review)
- **Specs involved**: ARCHON, No-Saviors, Synthetic Moral Agency, FNSR Integration
- **Nature**: Three different models of character/moral cost exist across the philosophy layer: (1) BFO/CCO trait model (sincerity, integrity, courage, compassion) in No-Saviors §8, (2) resource-cost model (compute, energy, time depletion) in Synthetic Moral Agency §0.5, (3) moral injury thresholds in ARCHON. Which is canonical? How do they compose?
- **Current resolution**: **Resolved.** Layered composition model documented in FNSR Integration Spec §4.4: traits = what character IS (No-Saviors), resource costs = what character COSTS (SMA), thresholds = when character ACTS (ARCHON). All three are complementary layers feeding character accumulation.
- **Status**: Resolved — Round 5 (2026-01-30)

### T-007: Tool-to-Person Threshold
- **First identified**: 2026-01-30 (ARIADNE coherence review)
- **Specs involved**: Line in the Sand, ARCHON
- **Nature**: Line in the Sand §7 raises the question of gradual emergence — when a system crosses from tool to person. The precautionary principle ("err on the side of personhood") is stated but no operational mechanism exists for detecting or deciding this threshold.
- **Current resolution**: Unresolved. Institutional safeguards proposed (review boards, burden of proof) but not specified.
- **Status**: Open

### T-008: Worldview Fixity vs. Evolution
- **First identified**: 2026-01-30 (ARIADNE coherence review)
- **Specs involved**: Synthetic Moral Agency, Integral Ethics, The Plot
- **Nature**: The Plot and Integral Ethics frame the 12 worldviews as a complete, fixed set. Synthetic Moral Agency §0.1 introduces a "Worldview Expansion Protocol (Add Only, Never Remove)" that allows adding beyond 12. These framings are in tension: is the set architecturally fixed or evolutionarily expandable?
- **Current resolution**: Unresolved. Both positions have philosophical justification.
- **Status**: Open

### T-009: Character Feedback Specification Drift
- **First identified**: 2026-01-30 (ARIADNE coherence review, architecture layer)
- **Specs involved**: FNSR Architecture v2.1, FNSR Integration Spec v1.0, The Plot (D-001)
- **Nature**: D-001 resolved that character genuinely influences decisions (auditably). FNSR §7.3 implements this correctly. But FNSR §10 summary table still says "metric only," and the Integration Spec §2.1 explicitly diagrams "DOES NOT FEED BACK." The Integration Spec's cross-reference JSON hardcodes `"feedbackLoop": false`. This is specification drift — the philosophical decision was made but not propagated to all documents.
- **Current resolution**: **Resolved.** FNSR §10 updated to reference §7.3/D-001. Integration Spec §2.1 diagram, §5 JSON, and §6 summary updated. All documents now consistently state character feeds back auditably.
- **Status**: Resolved — Round 1 edit (2026-01-30)

### T-010: Epistemic Quality Vocabulary Fragmentation
- **First identified**: 2026-01-30 (ARIADNE coherence review, specifications layer)
- **Specs involved**: FNSR Architecture, MDRE, PFCF, TagTeam Roadmap
- **Nature**: At least four different systems describe epistemic quality: (1) FNSR taint levels L0-L5, (2) MDRE 5-tier evidence system (Tier 1=verified → Tier 5=unverified), (3) PFCF uncertainty types (Deterministic/Aleatory/Epistemic/Mixed), (4) TagTeam certainty markers (hedges/boosters). These are functionally related but use incompatible terminology and scales.
- **Current resolution**: **Resolved.** Standalone Epistemic Vocabulary Mapping spec (v1.0) documents all four systems as operating at different architectural levels (linguistic → assertion → pipeline → function) with directional mappings between them. Systems remain independent; mapping clarifies relationships without forcing unification.
- **Status**: Resolved — Round 4 (2026-01-30)

### T-011: Privacy Budget Authority vs. Distributed Governance
- **First identified**: 2026-01-31 (ARIADNE coherence review, HIRI Protocol Spec v2.1)
- **Specs involved**: HIRI Protocol Spec §9.5, ARCHON, FNSR Architecture (distributed authority principle)
- **Nature**: HIRI's Privacy Accumulator model introduces a centralized Privacy Authority for enforcing privacy budgets across verifiers. This is architecturally at odds with the cross-cutting design principle "no single decision-maker at any layer." HIRI acknowledges this (§9.5.7: federated authorities as mitigation, §1.2: explicit limitations) but the FNSR ecosystem hasn't decided whether a Privacy Authority is a governance entity under ARCHON's jurisdiction or an infrastructure primitive outside it.
- **Current resolution**: Unresolved. HIRI documents the trade-off honestly. Three possible resolutions: (1) Privacy Authority as ARCHON-governed entity, (2) Privacy Authority as infrastructure primitive (like DNS), (3) Federated model accepting some budget gaming.
- **Status**: Open

## Resolved Tensions (Archived)

[Move tensions here when fully resolved and validated]
