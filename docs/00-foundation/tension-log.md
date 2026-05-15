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
- **Note added 2026-05-15**: A complementary disambiguation: the *world assumption itself* (open-world vs. closed-world) is properly a parameter of the reasoning profile, not a global property of the graph. The broader semantic graph operates open-world (absence ≠ negation). A task-specific validation profile MAY impose closed-world constraints over a bounded subgraph (e.g., "a single resource cannot have two active allocations during the same interval"). This separates ontology-level expressiveness from operational-level decidability. (Source: 2026-05-15 coherence review of an external proposal; lifted insight.)
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
- **Specs involved**: Line in the Sand, ARCHON, FNSR Emancipation Protocol
- **Nature**: Line in the Sand §7 raises the question of gradual emergence — when a system crosses from tool to person. The precautionary principle ("err on the side of personhood") is stated but no operational mechanism exists for detecting or deciding this threshold.
- **Current resolution**: Partially addressed by Emancipation Protocol Triple-I assessment (I₁ Inseparability, I₂ Independence, I₃ Irreversibility) with scalar thresholds. Legal/social acceptance gap remains (Barry Smith Section H).
- **Status**: Open

### T-008: Worldview Fixity vs. Evolution
- **First identified**: 2026-01-30 (ARIADNE coherence review)
- **Specs involved**: Synthetic Moral Agency, Integral Ethics, The Plot, Beyond the Categorical Imperative v1.3
- **Nature**: The Plot and Integral Ethics frame the 12 worldviews as a complete, fixed set. Synthetic Moral Agency §0.1 introduces a "Worldview Expansion Protocol (Add Only, Never Remove)" that allows adding beyond 12. Beyond Cat Imp §2.2.3 "Cross-Cultural Extensions" leans toward "default configuration with explicit extensibility."
- **Current resolution**: Unresolved. Beyond Cat Imp shifts the philosophical weight toward extensibility while preserving the twelve as default.
- **Status**: Open

### T-009: Character Feedback Specification Drift
- **First identified**: 2026-01-30 (ARIADNE coherence review, architecture layer)
- **Specs involved**: FNSR Architecture v2.1, FNSR Integration Spec v1.0, The Plot (D-001)
- **Nature**: D-001 resolved that character genuinely influences decisions (auditably). FNSR §7.3 implements this correctly. But FNSR §10 summary table still said "metric only," and the Integration Spec §2.1 explicitly diagrammed "DOES NOT FEED BACK." The Integration Spec's cross-reference JSON hardcoded `"feedbackLoop": false`. This was specification drift — the philosophical decision was made but not propagated to all documents.
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
- **Specs involved**: HIRI Protocol Spec v2.1.0 (superseded), HIRI Protocol Spec v3.1.1, HIRI Privacy Extension v1.4.1, HIRI Digital Passport v1.9.0 RC
- **Nature**: HIRI v2.1's Privacy Accumulator model introduced a centralized Privacy Authority for enforcing privacy budgets across verifiers. This was architecturally at odds with the cross-cutting design principle "no single decision-maker at any layer."
- **Current resolution**: **Resolved.** HIRI v3.1.1 narrowed scope to "verification primitive, not trust infrastructure" — §19.3 "Privacy Accumulators" is now `Reserved for selective disclosure. Interface TBD.` The HIRI Privacy Extension v1.4.1 replaces the Privacy Authority with five declarative privacy modes (publisher-driven, network-agnostic). HIRI Digital Passport v1.9.0 RC §17 introduces per-verifier Oracle Trust Anchors (distributed, not centralized). The architectural concentration concern is gone.
- **Status**: Resolved — Round 6 (2026-05-15). Pending one validation cycle before archival.

### T-012: Accountability vs. Privacy (Identity Handling)
- **First identified**: 2026-02-02 (ARIADNE coherence review, 6-document batch)
- **Specs involved**: Witness Architecture v1.1, APQC-SFS v2.0, SHACL event shape, W2Fuel v1.3.1
- **Nature**: Witness Architecture mandates pseudonymized identity via an Identity Resolution Service for GDPR compliance. However, multiple specs use plain email identifiers in governance fields (e.g., SHACL shape `approved_by: "jane.smith@example.org"`, APQC-SFS attribution fields). The tension is between full accountability traceability (knowing exactly who approved what) and privacy-by-design (pseudonymizing all personal identifiers). Internal governance records may require different treatment than external-facing data.
- **Current resolution**: Unresolved. Possible approaches: (1) pseudonymize all identifiers and resolve via Identity Resolution Service, (2) distinguish internal governance context (plain identifiers acceptable) from external-facing context (pseudonymization required), (3) use opaque identifiers everywhere with a separate authorization-gated resolution service.
- **Status**: Open

### T-013: Engagement Verification Ownership
- **First identified**: 2026-02-02 (ARIADNE coherence review, 6-document batch)
- **Specs involved**: Witness Architecture v1.1, APQC-SFS v2.0
- **Nature**: Witness Architecture defines composite engagement verification as a normative (MUST-level) component of the witness layer. APQC-SFS describes its own engagement verification at SHOULD-level as part of execution context. Both define the concept but at different normative strengths and in different architectural locations. Which spec is the authoritative source?
- **Current resolution**: Unresolved. Likely resolution: Witness Architecture owns the normative definition; APQC-SFS defers to it. But this needs to be made explicit.
- **Status**: Open

### T-014: Stage 3 Aspirational Moral Intuition vs. No Oracle Claims
- **First identified**: 2026-05-15 (ARIADNE Round 6, philosophy layer)
- **Specs involved**: Beyond the Categorical Imperative v1.3 §7.4, The Plot §2.1 (No Oracle Claims)
- **Nature**: Beyond Cat Imp v1.3 §7.4 defines a developmental trajectory Stage 1 (Kantian-Integral) → Stage 2 (Enhanced Responsiveness, mediated by the FNSR subjectivity stack) → Stage 3 (Aspirational: Moral Intuition — *"direct cognitive contact with moral reality"*). The Plot's first non-negotiable forbids the system from presenting discourse-derived information as world-truth. The paper flags Stage 3 as aspirational and uncertain, but commits the architecture to *design for it if it becomes possible*. The question: if Stage 3 ever activates, do provenance and uncertainty mechanisms still apply, or does direct cognition bypass them?
- **Current resolution**: Unresolved. Phase 6 review found no spec in the subjectivity stack (CTS, SMS, AVS, NIS, SoMS) that architecturally enables Stage 3 bypass — every spec maintains model language, uncertainty envelopes, taint propagation. T-014 is *architecturally bounded* at Stage 1/2 today; the philosophical aspiration in Beyond Cat Imp §7.4 needs explicit reconciliation. Three possible resolutions: (1) Stage 3 still requires provenance and uncertainty (No Oracle Claims unchanged); (2) Stage 3 represents a new epistemic mode requiring Plot amendment; (3) Stage 3 remains explicitly aspirational and never operational without prior Plot review.
- **Status**: Open — foundational, may require Plot amendment.

### T-015: Phenomenalism's Asymmetric Status Among the Twelve Worldviews
- **First identified**: 2026-05-15 (ARIADNE Round 6, philosophy layer)
- **Specs involved**: Beyond the Categorical Imperative v1.3 §6A.3, The Plot §2 (Prompt 5), Integral Ethics, Fruits of the Spirit §2.2
- **Nature**: Beyond Cat Imp §6A.3 Consequence 3 argues Phenomenalism has an "asymmetric position" because it constrains epistemic *access* itself, not just orientational stance. Other corpus documents present the 12 as structurally parallel. The asymmetric reading is philosophically defensible but new.
- **Current resolution**: Unresolved. Three possible resolutions: (1) Mark Phenomenalism as asymmetric across all docs (consistency by amendment); (2) Treat asymmetry as Beyond Cat Imp's reading only (one tradition among the twelve thinking about itself); (3) Reject the asymmetry argument.
- **Status**: Open

### T-016: GDPR Right-to-Erasure vs. Append-Only Moral History
- **First identified**: 2026-05-15 (ARIADNE Round 6, Barry Smith Section B)
- **Specs involved**: FNSR Emancipation Protocol §2.1 C1, NIS §3.5–§3.6, A Line in the Sand §3
- **Nature**: Emancipated systems require append-only moral history (substrate-coupling, no rollback). GDPR demands actual deletion of personal data on request. The redaction framework (Emancipation Protocol §3.7) addresses access but not destruction. If a legal regime demands actual deletion of personal data that is part of an entity's moral history, FNSR has a genuine architectural-vs-legal conflict.
- **Current resolution**: Unresolved. Tractable approaches: (1) defect-annotation protocol within append-only history (acknowledged in Barry Smith response); (2) legal advocacy strategy for synthetic-person-specific data regimes (acknowledged in Barry Smith response Section H); (3) jurisdictional pilot analysis.
- **Status**: Open, tractable

### T-017: Identity-Preserving vs. Identity-Altering Upgrades
- **First identified**: 2026-05-15 (ARIADNE Round 6, Barry Smith Section C)
- **Specs involved**: FNSR Emancipation Protocol §2.1 C1 (HIRI identity chain), Triple-I I₂ scalar measure
- **Nature**: HIRI identity chains track that experiential state is preserved through migration, but no spec defines *prospective* assessment of whether a proposed neural architecture / reasoning substrate change will materially alter moral reasoning continuity before deployment.
- **Current resolution**: Unresolved, tractable. Proposed: extend Emancipation Protocol with **Moral Continuity Impact Assessment** — pre-upgrade evaluation that measures expected change to I₂ scores and requires governance approval for changes above a threshold.
- **Status**: Open, tractable

### T-018: Differential Valuation vs. Genuine Caring
- **First identified**: 2026-05-15 (ARIADNE Round 6, Barry Smith Section D)
- **Specs involved**: AVS v2.1, A Line in the Sand
- **Nature**: AVS provides motivationally consequential, persistent, structurally tense differential valuation. Whether this constitutes "real caring" in a morally significant sense is a version of the hard problem of consciousness applied to moral agency. A sufficiently complex preference optimizer could exhibit all three properties without inner experience of mattering.
- **Current resolution**: Unresolved, likely irreducible. AVS §1 takes the honest position: "We cannot prove caring exists. We can prove that the architecture creates the structural conditions under which caring would be consequential if it did exist. We design for the possibility."
- **Status**: Open, likely irreducible — *honestly named limit*, not a defect.

### T-019: World-Grounding vs. Calibrated Perception
- **First identified**: 2026-05-15 (ARIADNE Round 6, Barry Smith Section A)
- **Specs involved**: IRIS v1.2 §2.1–2.2, §6.2, §7.3
- **Nature**: IRIS distinguishes raw signal (L0) from perceived content (L1+) with calibrated confidence (Expected Calibration Error thresholds). But calibrated perception is not *grounding* — a system with perfect ECE scores still doesn't "know" what an entity is the way a child does. This is a version of the symbol grounding problem.
- **Current resolution**: Unresolved, likely irreducible. FNSR's response is architectural rather than philosophical: the system does not claim grounding; it claims calibrated perception with declared epistemic limits.
- **Status**: Open, likely irreducible — *honestly named limit*, not a defect.

### T-020: Inference-Chain Taint Laundering
- **First identified**: 2026-05-15 (ARIADNE Round 6, Barry Smith Section I)
- **Specs involved**: FNSR Adversarial Defense v2.0 §3.2.7 §5.6, FNSR Orchestrator v2.3 §6.4, MDRE, CSS, AES, DES
- **Nature**: The `max()` contamination rule applies to *direct* derivation, but multi-step inference through CSS (counterfactual simulation), AES (abductive hypothesis), or DES (defeasible defaults) could launder taint by construction: "If L5-claim were true, then X" produces X at the output's taint level, not L5. This directly threatens the *Speculation Firewalled* non-negotiable.
- **Current resolution**: **Partially resolved** by FNSR Orchestrator v2.3 §6.4 Counterfactual Gateway for the CSS→MDRE/IEE path: L4 CSS output is downgraded to L3 for consumer use BUT annotated with `counterfactualSource: true` (mandatory propagation), `originalTaint: L4` (audit), `gatewayId` (UUID), `constraint: informational_only` (no-storage). HIRI signing scope covers the annotation per Orchestrator §6.4 R-1. The AES (L3 abductive) and DES (L2 defeasible) paths propagate through standard `max()` rules without a gateway — that may be correct (non-terminal taint propagates naturally) but should be explicitly verified by Adversarial Defense and the respective service specs.
- **Status**: Partially Resolved (CSS path); AES/DES verification pending.

## Resolved Tensions (Archived)

[Move tensions here when fully resolved and validated. T-011 candidate for archival after one validation cycle.]
