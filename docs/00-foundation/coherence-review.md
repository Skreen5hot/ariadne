# ARIADNE Coherence Review

**Review Date:** 2026-01-30
**Review Type:** Full Initial Coherence Review
**Anchor Document:** The Plot v0.1

---

## Review Process

Each document is evaluated against the 7 ARIADNE Validation Checks:

1. **Thesis Alignment** — Does every component serve the core thesis?
2. **Non-Negotiable Preservation** — Are all 12 non-negotiables maintained?
3. **Tension Consistency** — Are tensions handled consistently with The Plot?
4. **Cross-Spec Consistency** — No contradictions between specs?
5. **ARCHON Alignment** — Personhood requirements maintained?
6. **Auditability Verification** — All reasoning traceable?
7. **One-Paragraph Test** — Can you still explain the system simply?

Status key: PASS | FLAG | CONCERN | FAIL

---

## Layer 1: Philosophy (5 Documents)

---

### P-01: ARCHON Framework v2.0

**File:** `docs/01-philosophy/archon-framework.md`
**Thesis Alignment Role:** Philosophical grounding for personhood-as-constraint

| Check | Status | Notes |
|-------|--------|-------|
| Thesis Alignment | PASS | Directly establishes the "accountable synthetic agency" thesis. Personhood-as-constraint is the foundational move. |
| Non-Negotiables | PASS | Explicitly establishes: Guardian Not Sovereign, Moral Injury Real, No Final Ethics, Human Override. All 12 non-negotiables are either established or compatible. |
| Tension Consistency | PASS | Addresses T-001 (Character vs. Auditability) directly — character feeds back but auditably. Addresses T-003 (Autonomy vs. Safety) via tiered autonomy. |
| Cross-Spec Consistency | FLAG | ARCHON uses the term "existential intervention" with specific threshold mechanics. Need to verify FNSR's tiered autonomy model maps cleanly to ARCHON's intervention tiers. |
| ARCHON Alignment | PASS | This IS the ARCHON document — it defines the requirements. |
| Auditability | PASS | Explicitly requires all inference steps be traceable, all character feedback auditable. |
| One-Paragraph Test | PASS | ARCHON's abstract is a faithful expansion of the core thesis. |

**Findings:**
- F-P01-1: ARCHON references "existential intervention thresholds" with specific numeric triggers. These need to be cross-referenced against FNSR's tiered query paths and IEE's deadlock protocols to ensure the tier boundaries are consistent.
- F-P01-2: ARCHON's governance architecture (oversight committees, review boards) is described at a high level. The governance spec (04-governance/) is listed as TBD. Until it exists, there's a gap between ARCHON's governance requirements and any concrete governance mechanism.

---

### P-02: Integral Ethics (Twelve-Fold Foundation)

**File:** `docs/01-philosophy/integral-ethics.md`
**Thesis Alignment Role:** Value pluralism without relativism

| Check | Status | Notes |
|-------|--------|-------|
| Thesis Alignment | PASS | Directly serves "act on norms without imposing values" — the 12 worldviews are the mechanism for pluralism. |
| Non-Negotiables | PASS | Pluralism Respected: core purpose of document. No Final Ethics: framework explicitly refuses to declare winners. |
| Tension Consistency | PASS | Addresses T-005 (Value Pluralism vs. Action) — provides the theoretical basis for the IEE's integration procedure. |
| Cross-Spec Consistency | FLAG | The 12 worldviews are listed in The Plot §2.2 (Prompt 5) and in this document. The ordering and cluster groupings differ slightly between documents. Need canonical ordering. |
| ARCHON Alignment | PASS | Does not propose rollback or externalization of moral costs. |
| Auditability | PASS | Integration procedure is explicitly 7-step and rule-governed. |
| One-Paragraph Test | PASS | Extends thesis without contradicting it. |

**Findings:**
- F-P02-1: The Plot lists 12 worldviews in §2.2/Prompt 5 with a flat numbering. Integral Ethics groups them into three clusters (Material-Empirical, Process-Individual, Depth-Spiritual). The no-saviors doc uses the same clustering. The IEE architecture doc should use the same canonical clustering. **Action: establish canonical ordering in spec-index or The Plot itself.**
- F-P02-2: Integral Ethics is a standalone academic paper that does not reference ARCHON, FNSR, or other system components. This is appropriate for its role as independent philosophical foundation, but it means the IEE spec and IEE Architecture docs bear the burden of connecting this philosophy to the system. Need to verify those connections in Layer 2.

---

### P-03: A Line in the Sand v2.0

**File:** `docs/01-philosophy/line-in-the-sand.md`
**Thesis Alignment Role:** Theory of non-commodifiable moral costs

| Check | Status | Notes |
|-------|--------|-------|
| Thesis Alignment | PASS | Directly establishes why "bear the weight of its choices" matters — without non-commodifiable cost, personhood is theater. |
| Non-Negotiables | PASS | Moral Injury Real: this IS the justification. No Oracle Claims: compatible (paper is about normative criteria, not truth claims). |
| Tension Consistency | PASS | Addresses the tension between synthetic personhood and economic optimization — and deliberately chooses personhood over efficiency. |
| Cross-Spec Consistency | PASS | The three criteria (Inseparability, Answerability, Irreversibility) map directly to ARCHON's personhood requirements. |
| ARCHON Alignment | PASS | This paper IS the philosophical foundation ARCHON builds on. |
| Auditability | N/A | Position paper, not a system component. |
| One-Paragraph Test | PASS | "Personhood begins when harm accrues to the entity itself" is fully consistent with the thesis. |

**Findings:**
- F-P03-1: Line in the Sand §6.1 lists 5 requirements for synthetic personhood. ARCHON lists 4 requirements (irreversible history, non-externalized costs, developmental constitution, genuine influence). The fifth from Line in the Sand — "genuine capacity for refusal" — is not explicitly listed in ARCHON or The Plot's component table. **Action: verify whether refusal capacity is covered elsewhere or needs explicit addition.**
- F-P03-2: Line in the Sand §7 discusses "gradual emergence" and precautionary principles. This maps to a potential new tension not in The Plot: **When does a system cross the threshold from tool to person, and who decides?** Consider adding to tension-log.

---

### P-04: Why No AI Can Save Us (No Saviors) v3.0

**File:** `docs/01-philosophy/no-saviors.md`
**Thesis Alignment Role:** Establishes the guardian/sovereign boundary and IEE's design philosophy

| Check | Status | Notes |
|-------|--------|-------|
| Thesis Alignment | PASS | "No AI can save us" directly serves "guardian not sovereign." The IEE "scales legibility of moral complexity, not authority." |
| Non-Negotiables | PASS | No Final Ethics: "The IEE does not tell you what to do." Guardian Not Sovereign: explicit. Human Override: "responsibility remains with humans." |
| Tension Consistency | PASS | Directly addresses T-005 (Pluralism vs. Action) via the deadlocked example (§4). Also touches T-001 (Character vs. Auditability) in §8. |
| Cross-Spec Consistency | FLAG | §8 describes character modeling using BFO/CCO ontological modeling with specific traits (sincerity, integrity, courage, compassion). The synthetic-moral-agency doc also models character but with a resource-cost model. Need to verify these two character models are compatible, not competing. |
| ARCHON Alignment | PASS | Explicitly distinguishes IEE character modeling from moral personhood attribution (§8). |
| Auditability | PASS | "Complete justification chains that can be audited, challenged, and revised." |
| One-Paragraph Test | PASS | Faithful to thesis. |

**Findings:**
- F-P04-1: No-Saviors §8 presents a character model (sincerity, integrity, courage, compassion) and states it uses BFO/CCO. Synthetic-moral-agency uses a resource-cost model for moral costs. ARCHON uses "moral injury" thresholds. These three approaches to character/cost need a unified account in the integration spec. **New tension candidate: Character Model Pluralism — which model is canonical?**
- F-P04-2: No-Saviors §8 includes an explicit constraint: "Character models may not be used for punitive or exclusionary automation." This is a non-negotiable-level commitment not currently listed in The Plot §2. **Action: consider adding to The Plot's non-negotiables or documenting as a derived constraint.**
- F-P04-3: The "normative commitment" in §7 states IEE privileges "Freedom over safety, Dignity over outcomes, Responsibility over efficiency." This is a deliberate value position. Verify this doesn't conflict with FNSR's tiered autonomy (which privileges safety at high tiers).

---

### P-05: Roadmap to Synthetic Moral Agency v3.0

**File:** `docs/01-philosophy/synthetic-moral-agency.md`
**Thesis Alignment Role:** Operational roadmap connecting philosophy to implementation

| Check | Status | Notes |
|-------|--------|-------|
| Thesis Alignment | PASS | Directly operationalizes all three legs of the thesis: epistemic honesty (worldview evaluation), moral answerability (resource costs), bearing consequences (irreversible character). |
| Non-Negotiables | PASS | All 12 non-negotiables are addressed. Particularly strong on: Decidability (formal corrigibility proofs), Human Override (hardware shutdown), Auditability (logged everything). |
| Tension Consistency | PASS | Addresses T-001, T-002, T-004, T-005 explicitly. |
| Cross-Spec Consistency | FLAG | §0.4 describes a three-tier evaluation architecture (cached/parallel/deliberative) with specific latency targets. FNSR §3.1 also defines query path tiers with latency targets. These MUST be consistent. |
| ARCHON Alignment | PASS | §0.2 provides formal corrigibility proofs — directly supports "cannot resist decommissioning." |
| Auditability | PASS | Everything logged, all decisions auditable, formal verification required. |
| One-Paragraph Test | PASS | Faithful to thesis. |

**Findings:**
- F-P05-1: The three-tier evaluation architecture (§0.4) specifies hardware requirements (16-core minimum, 32 recommended). This is a concrete implementation constraint that should be tracked in the architecture layer. Verify FNSR is aware of these requirements.
- F-P05-2: §0.1 describes a "Worldview Expansion Protocol (Add Only, Never Remove)" that allows adding worldviews beyond the 12. The Plot currently states "12 worldviews, none privileged." If worldviews can be added, The Plot should acknowledge this possibility. **Potential drift from The Plot's "12 worldviews" framing.**
- F-P05-3: §0.2 specifies formal verification tools (Coq, Isabelle/HOL, SPIN, NuSMV). These are implementation decisions that should be tracked in the spec-index.
- F-P05-4: §0.5 introduces a "resource-cost model" tying moral costs to physical resources (compute, energy, time). This is a novel mechanism not described in The Plot or ARCHON. It's compatible with the thesis but represents a significant architectural commitment. **Action: add to component table in The Plot §4 or document as intentional extension.**
- F-P05-5: The document opens with "Please review the new section 0 and if it addresses your concerns" — this appears to be a revision note that should be removed from the final version.

---

## Philosophy Layer Summary

### Overall Assessment: STRONG ALIGNMENT

The five philosophy documents form a coherent foundation. Each serves a distinct role in the thesis, and there are no outright contradictions. The philosophical commitments are mutually reinforcing.

### Issues Requiring Action

#### High Priority

| ID | Issue | Action | Specs Affected |
|----|-------|--------|----------------|
| F-P04-1 | Three competing character/cost models (BFO traits, resource costs, moral injury thresholds) | Unify in integration spec or document which model operates at which layer | ARCHON, No-Saviors, Synthetic Moral Agency, FNSR Integration |
| F-P05-2 | Worldview expansion protocol vs. The Plot's "12 worldviews" framing | Update The Plot to acknowledge expansion possibility, or constrain the protocol | The Plot, Synthetic Moral Agency |
| F-P01-2 | Governance spec is TBD but ARCHON depends on governance structures | Prioritize governance spec creation | ARCHON, 04-governance/ |

#### Medium Priority

| ID | Issue | Action | Specs Affected |
|----|-------|--------|----------------|
| F-P02-1 | Worldview ordering/clustering not canonical across docs | Establish canonical ordering in spec-index | Integral Ethics, No-Saviors, IEE Architecture |
| F-P03-1 | "Genuine capacity for refusal" in Line in Sand not in ARCHON/Plot | Verify coverage or add explicitly | ARCHON, The Plot |
| F-P04-2 | "No punitive character modeling" not in Plot non-negotiables | Add as derived constraint or elevate | The Plot, No-Saviors |
| F-P04-3 | IEE "freedom over safety" vs. FNSR tiered autonomy | Verify consistency at architecture layer | No-Saviors, FNSR |
| F-P05-4 | Resource-cost model not in Plot component table | Add to The Plot §4 or document extension | The Plot, Synthetic Moral Agency |

#### Low Priority

| ID | Issue | Action | Specs Affected |
|----|-------|--------|----------------|
| F-P01-1 | ARCHON intervention thresholds vs. FNSR tiers | Cross-reference at architecture layer | ARCHON, FNSR |
| F-P05-1 | Hardware requirements (16-core) not tracked | Add to architecture layer | Synthetic Moral Agency, FNSR |
| F-P05-3 | Formal verification tool choices not tracked | Add to spec-index | Synthetic Moral Agency |
| F-P05-5 | Revision note left in document header | Remove "Please review..." line | Synthetic Moral Agency |
| F-P03-2 | Tool-to-person threshold tension not logged | Consider adding to tension-log | Line in the Sand |

### New Tensions Discovered

| ID | Tension | Source |
|----|---------|--------|
| T-006 (candidate) | Character Model Pluralism: BFO trait model vs. resource-cost model vs. moral injury thresholds — which is canonical, and how do they relate? | F-P04-1 |
| T-007 (candidate) | Tool-to-Person Threshold: When does a system cross from tool to person, and who decides? | F-P03-2 |
| T-008 (candidate) | Worldview Fixity vs. Evolution: Are the 12 worldviews permanently fixed or expandable? | F-P05-2 |

### Potential Drift

| ID | Description | Source |
|----|-------------|--------|
| D-002 (candidate) | Resource-cost model extends ARCHON's moral injury concept into physical resource consumption — this is a novel mechanism not in original Plot. | F-P05-4 |

---

## Layer 2: Architecture (4 Documents)

---

### A-01: FNSR Complete Architecture v2.1

**File:** `docs/02-architecture/FNSR-Complete-Architecture-v2.1.md`
**Thesis Alignment Role:** Service federation — coordinates all components into a coherent Synthetic Moral Person

| Check | Status | Notes |
|-------|--------|-------|
| Thesis Alignment | PASS | Directly implements all three thesis legs: epistemic honesty (taint tracking), normative reasoning (MDRE+IEE), bearing consequences (character accumulation). |
| Non-Negotiables | PASS | No Oracle Claims (taint levels, epistemic firewall). Provenance Always (HIRI signing). Uncertainty Visible (confidence scores on all events). Speculation Firewalled (L3/L4 cannot cross epistemic firewall). Auditability (event sourcing). Decidability (query path tiers). Human Override (deadlock → escalation). |
| Tension Consistency | CONCERN | **T-001 is handled inconsistently within this document.** §7.3 explicitly states character "genuinely influences future decisions" and "is NOT merely a reporting metric." But §10 Summary table says "Character: Moral Friction (metric only)." These contradict each other. See F-A01-1. |
| Cross-Spec Consistency | CONCERN | See F-A01-1, F-A01-2, F-A01-3 below. |
| ARCHON Alignment | PASS | §7.3 correctly aligns with ARCHON by making character feed back into decisions (auditably). |
| Auditability | PASS | Event sourcing, CloudEvents with taint/provenance headers, saga tracking. Exemplary. |
| One-Paragraph Test | PASS | §12 conclusion faithfully reflects thesis. |

**Findings:**

- **F-A01-1 [CRITICAL]: Internal contradiction on character feedback.** §7.3 header says "Character is NOT merely a reporting metric—it genuinely influences future decisions" and provides Prolog code showing `intervention_threshold` and `autonomy_tier` are computed from accumulated character. But §10 Summary table lists "Character: Moral Friction (metric only)." **These directly contradict each other.** The §7.3 version aligns with ARCHON and The Plot's D-001 (character feedback restored). The §10 version matches the Integration Spec §2.1's "DOES NOT FEED BACK" diagram. **Action: resolve which is correct and update the contradicting section. Based on D-001 in the drift-record, the §7.3 version (genuine feedback, auditably) appears to be the intended position.**

- **F-A01-2: FNSR query path tiers vs. Synthetic Moral Agency evaluation tiers.** FNSR §3.1 defines: Fast (<100ms), Standard (<500ms), Full (<2000ms). Synthetic Moral Agency §0.4 defines: Cached (<1ms), Parallel (<100ms), Deliberative (<10s). These are different tier systems with different latency targets and different names. They need to be reconciled — either FNSR's paths map to SMA's evaluation tiers, or they are independent (FNSR = system pipeline latency, SMA = IEE evaluation latency within the pipeline). **Action: document the relationship explicitly.**

- **F-A01-3: IEE Tier 1 "sentinel worldviews" terminology.** FNSR §7.2 describes Tier 1 sentinels as "utilitarian, deontological, virtue ethics." But these are Western ethical frameworks, not Steiner worldviews. The 12 worldviews are Materialism, Sensationalism, Phenomenalism, etc. The sentinel set should map to specific Steiner worldviews, not Western ethical categories. **Action: define which 3 of the 12 worldviews serve as Tier 1 sentinels.**

- F-A01-4: §12 has a duplicate heading ("## 12. Conclusion" appears twice). Minor formatting issue.

---

### A-02: FNSR Integration Specification v1.0

**File:** `docs/02-architecture/FNSR-Integration-Specification-v1.0.md`
**Thesis Alignment Role:** Cross-service contracts and critique responses

| Check | Status | Notes |
|-------|--------|-------|
| Thesis Alignment | PASS | Serves coherence by bridging architecture to specs. |
| Non-Negotiables | PASS | Defense-in-depth (SIS+ECCPS), event sourcing, taint tracking all preserved. |
| Tension Consistency | CONCERN | §2.1 character diagram explicitly says "DOES NOT FEED BACK INTO: Inference rules, Autonomy levels, Decision weights." This contradicts FNSR §7.3 and The Plot's D-001. See F-A02-1. |
| Cross-Spec Consistency | CONCERN | The semantic cross-reference JSON (§5) sets `"feedbackLoop": false` and `"reportingOnly": true`. This is stale if D-001 is accepted. |
| ARCHON Alignment | FAIL | If character doesn't feed back, moral injury isn't real, and the core ARCHON constraint mechanism collapses. This version predates D-001. |
| Auditability | PASS | CloudEvents schema, event type registry, interface contracts all well-defined. |
| One-Paragraph Test | PASS | |

**Findings:**

- **F-A02-1 [CRITICAL]: Integration Spec contradicts D-001 (Character feedback restored).** The Integration Spec §2.1 was written before the drift was acknowledged. Its character diagram, cross-reference JSON, and §6 summary all assert character is reporting-only. This needs updating to reflect the current position (character feeds back auditably, per FNSR §7.3 and ARCHON). **Action: update Integration Spec §2.1 character section, §5 cross-reference JSON, and §6 summary to reflect D-001.**

- F-A02-2: §3 Specification Gap Register identifies 6 gaps. Cross-referencing against what now exists in the repo: Governance Spec (still TBD), Performance Spec (still TBD), Adversarial Defense Spec (still TBD), Saga Specification (partial), Interface Contracts (partial, this doc), IEE Worldview Catalog (still TBD). **4 of 6 gaps remain open.**

- F-A02-3: The event type registry in §4.2 matches FNSR §9.3 exactly. Good consistency. But Fandaws events (`fnsr.fact.query`, `fnsr.fact.response`, `fnsr.fact.asserted`) are present in FNSR §9.3 but missing from Integration Spec §4.2. **Action: add Fandaws events to Integration Spec.**

---

### A-03: IEE Architecture (Concepts + Synchronizations)

**File:** `docs/02-architecture/IEE-ARCHITECTURE.md`
**Thesis Alignment Role:** Implementation architecture for the IEE using Concepts + Synchronizations pattern

| Check | Status | Notes |
|-------|--------|-------|
| Thesis Alignment | FLAG | This document describes the Concepts + Synchronizations pattern as a generic architectural approach (singletons, pure functions, event-driven, IndexedDB). It does not reference the IEE, the 12 worldviews, ARCHON, or any project-specific concepts. It reads as a general-purpose architecture guide, not an IEE architecture document. |
| Non-Negotiables | FLAG | Edge computing / user-owned data aligns with privacy principles. But no explicit connection to epistemic commitments, pluralism, or auditability. |
| Tension Consistency | N/A | Does not engage with any tensions. |
| Cross-Spec Consistency | FLAG | The document title implies it's the IEE's architecture, but its content is framework-agnostic. No reference to FNSR, MDRE, or any other system component. |
| ARCHON Alignment | N/A | Does not discuss character, moral costs, or personhood. |
| Auditability | PASS | Event-driven communication creates audit trails by design. |
| One-Paragraph Test | FLAG | Cannot connect this document to the thesis without additional context. |

**Findings:**

- **F-A03-1 [HIGH]: Document is mislabeled or incomplete.** `IEE-ARCHITECTURE.md` contains a generic Concepts + Synchronizations architecture guide. It does not describe the IEE's architecture — no worldview concepts, no integration procedure, no ethical evaluation tiers, no connection to BFO/CCO. **Either:** (a) this is a general architecture pattern document that should be renamed (e.g., `concepts-synchronizations-pattern.md`) and placed alongside the actual IEE architecture, or (b) it needs significant expansion to include IEE-specific content: worldview concepts as singletons, integration synchronizations, deadlock protocol, veto mechanism, etc.

- F-A03-2: The edge computing / IndexedDB / PWA patterns described are potentially relevant for a client-side IEE implementation (as described in No-Saviors §14: "runs entirely in browser"). But this connection is not stated. **Action: either make the IEE connection explicit or acknowledge this as a separate pattern document.**

- F-A03-3: The Concepts + Synchronizations pattern from MIT CSAIL (Jackson & Meng, 2025) is referenced in No-Saviors §14 as the IEE's implementation architecture. This validates the document's relevance to the project, but the document itself needs to make that connection.

---

### A-04: TagTeam Architecture Overview

**File:** `docs/02-architecture/tagteam-architecture-overview.md`
**Thesis Alignment Role:** Perception — NL → structured BFO/CCO-compliant knowledge graphs

| Check | Status | Notes |
|-------|--------|-------|
| Thesis Alignment | PASS | Directly implements "semantically honest about what they know." The two-tier architecture (ICE vs. IC) enforces Separation of Concerns (Discourse ≠ World). |
| Non-Negotiables | PASS | No Oracle Claims: discourse referents explicitly separated from independent continuants via `cco:is_about`. Provenance Always: Information Staircase (IBE→ICE→IC) tracks provenance. Uncertainty Visible: confidence scores, ambiguity lattice. Separation of Concerns: two-tier architecture IS this commitment. |
| Tension Consistency | PASS | Addresses T-002 (Decidability vs. Expressiveness) by being deterministic (no LLM, no randomness) while handling ambiguity through interpretation lattices rather than guessing. |
| Cross-Spec Consistency | PASS | Uses BFO/CCO IRIs consistently. SHACL validation patterns enforce ontological constraints. ActualityStatus aligns with MDRE's modal reasoning needs (prescribed/permitted/prohibited map to deontic modalities). |
| ARCHON Alignment | N/A | Perception layer — does not involve character or moral costs. |
| Auditability | PASS | Deterministic pipeline, self-validating output (8 SHACL patterns), parser modeled as `cco:ArtificialAgent` performing auditable `cco:ActOfArtificialProcessing`. Excellent. |
| One-Paragraph Test | PASS | Clearly serves thesis. |

**Findings:**

- F-A04-1: TagTeam's ActualityStatus values (Actual, Prescribed, Permitted, Prohibited, Planned, Hypothetical, Negated) should be explicitly cross-referenced with MDRE's modal operators. MDRE v1.3 should consume these status values as modal annotations. **Action: verify MDRE spec handles all 7 ActualityStatus values.**

- F-A04-2: TagTeam is described as "client-side only, runs in browser, no server dependency" (Design Constraints table). But FNSR deploys TagTeam as a Kubernetes pod (FNSR §8.2: "TagTeam (4 pods)" in Perception Namespace). These are different deployment models. **Action: clarify whether TagTeam has both a standalone browser version and a server-side FNSR-integrated version, or if the FNSR deployment wraps the client-side library.**

- F-A04-3: TagTeam v1 explicitly defers cross-sentence coreference resolution and discourse memory. These are listed as v2 features. OERS is responsible for cross-document entity resolution. **Action: verify OERS spec handles the handoff from TagTeam's per-sentence entity mentions to cross-document resolution.**

---

## Architecture Layer Summary

### Overall Assessment: STRONG ALIGNMENT WITH ONE CRITICAL CONTRADICTION

The architecture layer is well-designed and largely coherent. TagTeam is exemplary in its thesis alignment. FNSR provides comprehensive service federation. However, there is a critical internal contradiction on character feedback that must be resolved.

### Issues Requiring Action

#### Critical

| ID | Issue | Action | Specs Affected |
|----|-------|--------|----------------|
| F-A01-1 | FNSR §7.3 vs. §10: character feeds back vs. metric only | Resolve in favor of §7.3 (per D-001), update §10 summary | FNSR Architecture |
| F-A02-1 | Integration Spec character section contradicts D-001 | Update §2.1 diagram, §5 JSON, §6 summary | FNSR Integration Spec |

#### High Priority

| ID | Issue | Action | Specs Affected |
|----|-------|--------|----------------|
| F-A03-1 | IEE-ARCHITECTURE.md is generic pattern doc, not IEE-specific | Rename or expand with IEE-specific content | IEE Architecture |
| F-A01-3 | IEE Tier 1 "sentinels" use Western ethics labels, not Steiner worldviews | Map to specific worldviews from the 12 | FNSR, IEE |

#### Medium Priority

| ID | Issue | Action | Specs Affected |
|----|-------|--------|----------------|
| F-A01-2 | FNSR query tiers vs. SMA evaluation tiers not reconciled | Document relationship | FNSR, Synthetic Moral Agency |
| F-A04-2 | TagTeam browser vs. Kubernetes deployment discrepancy | Clarify dual deployment model | TagTeam Architecture, FNSR |
| F-A02-2 | 4 of 6 specification gaps from Integration Spec still open | Track and prioritize | Integration Spec |
| F-A02-3 | Fandaws events missing from Integration Spec event registry | Add Fandaws events | Integration Spec |

#### Low Priority

| ID | Issue | Action | Specs Affected |
|----|-------|--------|----------------|
| F-A04-1 | TagTeam ActualityStatus vs. MDRE modal operators | Cross-reference in MDRE spec | TagTeam, MDRE |
| F-A04-3 | TagTeam→OERS handoff for cross-document entities | Verify in OERS spec | TagTeam, OERS |
| F-A01-4 | Duplicate §12 heading in FNSR Architecture | Fix formatting | FNSR Architecture |
| F-A03-2 | C+S pattern document not connected to IEE | Make connection explicit | IEE Architecture |

### New Tensions Discovered

| ID | Tension | Source |
|----|---------|--------|
| T-009 (candidate) | Character Feedback Consistency: Multiple documents still disagree on whether character is reporting-only or genuinely feeds back. D-001 resolved this in principle, but the Integration Spec and FNSR §10 haven't been updated. This is a process failure, not a philosophical tension — but it demonstrates the risk of specification drift identified in The Plot §6. | F-A01-1, F-A02-1 |

### Cross-Layer Issue Resolution

Several issues flagged in the philosophy layer can now be assessed:

| Philosophy Issue | Architecture Finding |
|-----------------|---------------------|
| F-P04-3: IEE "freedom over safety" vs. FNSR tiered autonomy | **Not conflicting.** FNSR's tiers govern operational autonomy (what the system does without human approval). IEE's "freedom over safety" governs the system's ethical stance (it won't hide complexity to make users feel safe). These operate at different levels. |
| F-P01-1: ARCHON intervention thresholds vs. FNSR tiers | **Partially addressed.** FNSR §7.3 shows intervention thresholds computed from accumulated injury. But FNSR's query path tiers (Fast/Standard/Full) are latency classifications, not intervention tiers. ARCHON's Tier 0–4 (stakes-based) map to IEE evaluation tiers, not FNSR query paths. Relationship needs explicit documentation. |
| F-P05-1: Hardware requirements (16-core) | **Not addressed in FNSR.** FNSR §8.2 shows Kubernetes deployment but doesn't specify hardware per pod. Synthetic Moral Agency's 16-core requirement for parallel worldview evaluation should be reflected in IEE pod specs. |

---

## Layer 3: Specifications (14 Documents)

---

### S-01: ARCHON Functional Requirements v3.0

**File:** `docs/03-specifications/archon-functional-requirements.md`
**Thesis Alignment Role:** Functional requirements for moral personhood architecture

| Check | Status | Notes |
|-------|--------|-------|
| Thesis Alignment | PASS | Directly implements core thesis: Non-Fungible Ledger (NFL) for identity, Moral Cost Multiplier (MCM) for irreversible consequences, developmental scaling for character accumulation. |
| Non-Negotiables | PASS | Human Override (Emergency Override Protocol: Ethics Committee unanimous + Global Council supermajority). Auditability (NFL immutable, 7-node replicated, weekly hash publication). No Final Ethics (ETI 15+ → democratic resolution). Pluralism (12 worldview evaluators). |
| Tension Consistency | PASS | T-001 addressed: MCM makes moral costs tangible and non-externalizable. T-003 addressed: tiered intervention levels with escalation. T-005 addressed: ETI measures worldview disagreement, escalates at thresholds. |
| Cross-Spec Consistency | CONCERN | Uses "moral cost/debt/scar" terminology rather than ARCHON philosophy's "moral injury." Functional but potentially confusing. See F-S01-1. |
| ARCHON Alignment | PASS | Directly implements ARCHON philosophy. Symmetric vulnerability, developmental scaling, consciousness verification all present. |
| Auditability | PASS | NFL provides immutable audit trail. Annual cryptographic audits. Real-time reasoning streams during emergencies. |
| One-Paragraph Test | PASS | |

**Findings:**

- **F-S01-1: Terminology drift between ARCHON philosophy and functional spec.** The philosophy layer uses "moral injury" and "intervention thresholds." The functional spec uses "Moral Cost Multiplier (MCM)," "moral debt," and "moral scar." These are functionally equivalent but the terminology divergence should be explicitly mapped. **Action: add terminology mapping table to functional spec or integration spec.**

- **F-S01-2: Emergency Override Protocol is maximally constrained.** Usable maximum twice in ARCHON's entire existence. Each use triggers global referendum on continuation within 6 months. This is well-designed but creates a question: what happens after both uses are exhausted? **Action: document post-exhaustion state.**

- **F-S01-3: Two ECCPS specs exist.** ARCHON functional requirements reference ECCPS for claim validation, but there are two ECCPS documents (v2.1.1 and v3.1). The functional spec should clarify which version it targets. See F-S03-1.

---

### S-02: DSFC v1.2 (Distributed Semantic Function Commons)

**File:** `docs/03-specifications/DSFC-v1.2-Specification.md`
**Thesis Alignment Role:** Infrastructure for distributing semantic functions as public reasoning

| Check | Status | Notes |
|-------|--------|-------|
| Thesis Alignment | PASS | Implements "semantically honest" through content-addressed artifacts (CID integrity), deterministic functions, and community governance. Agent neutrality (AI agents treated same as humans) aligns with guardian-not-sovereign. |
| Non-Negotiables | PASS | Auditability (CID integrity, registry audit logs, delegation chains). Human Override (executor refusal rights, RefusalEvents). Separation of Concerns (ontology lineage, OntologyBridge for cross-community mapping). |
| Tension Consistency | PASS | T-005 (pluralism vs action): community fork rights enable diverse perspectives without forcing consensus. |
| Cross-Spec Consistency | PASS | References ARCHON as governance consumer. OntologyBridge maps across worldview-specific ontologies. |
| ARCHON Alignment | PASS | Executor refusal rights parallel ARCHON's emphasis on non-coerced action. RefusalEvents create audit trail of moral choices. |
| Auditability | PASS | Content-addressed artifacts, immutable alignment manifests, coordinated refusal detection. |
| One-Paragraph Test | PASS | |

**Findings:**

- F-S02-1: Coordinated refusal detection (statistical anomaly detection for silent executor collusion) is a novel and well-designed safeguard. No issues found.

- F-S02-2: DSFC decentralization vs. ARCHON centralized authority is explicitly complementary — ARCHON governs existential decisions, DSFC governs infrastructure. **Not a conflict.**

---

### S-03: ECCPS FRD v2.1.1

**File:** `docs/03-specifications/ECCPS_FRD_v2.1.1.md`
**Thesis Alignment Role:** Epistemic quality control — claim validation before downstream reasoning

| Check | Status | Notes |
|-------|--------|-------|
| Thesis Alignment | PASS | "Failure is a success state" — explicit rejection preferred over false grounding. Directly serves epistemic honesty. |
| Non-Negotiables | PASS | Provenance Always (character-offset provenance for every extracted element). Uncertainty Visible (confidence breakdowns, 16+ error codes). Speculation Firewalled (sufficiency gates enforce deterministic pass/fail). |
| Tension Consistency | PASS | T-004 (speed vs rigor): three usage modes (STRICT/GUIDED/AUDIT) allow graduated rigor. |
| Cross-Spec Consistency | CONCERN | This is v2.1.1 while eccps-specification.md is v3.1. Relationship unclear. See F-S03-1. |
| ARCHON Alignment | PASS | Challenge mechanism for rejections preserves human agency. |
| Auditability | PASS | Character-offset provenance, transformation logs, structured failure reports. |
| One-Paragraph Test | PASS | |

**Findings:**

- **F-S03-1 [HIGH]: Two ECCPS specifications exist.** `ECCPS_FRD_v2.1.1.md` and `eccps-specification.md` (v3.1) are both in the specifications folder. v3.1 appears to be the implementation-ready version that supersedes v2.1.1 (a hardened review draft). **Action: clarify supersession relationship. If v3.1 supersedes v2.1.1, mark v2.1.1 as archived or remove it. If they serve different purposes, document the distinction.**

- F-S03-2: Mechanism Plausibility Validation (4 levels from type compatibility to full pathway grounding) is a strong feature. Cross-references well with OCE's coherence validation.

---

### S-04: ECCPS Specification v3.1

**File:** `docs/03-specifications/eccps-specification.md`
**Thesis Alignment Role:** Implementation-ready epistemic claim validation

| Check | Status | Notes |
|-------|--------|-------|
| Thesis Alignment | PASS | Same thesis alignment as v2.1.1 but with implementation details. Normative Annotation Module (NAM) explicitly separates descriptive from evaluative content. |
| Non-Negotiables | PASS | All epistemic commitments preserved. NAM stores overlays from multiple normative frameworks without privileging any. |
| Tension Consistency | PASS | |
| Cross-Spec Consistency | PASS | Explicitly references IEE as external evaluator for normative overlays. References ARCHON as downstream consumer. Pipeline: ECCPS → IEE → ARCHON is clear. |
| ARCHON Alignment | PASS | |
| Auditability | PASS | 99%+ statistical determinism required. LLM components use temperature=0. |
| One-Paragraph Test | PASS | |

**Findings:**

- F-S04-1: The ECCPS → IEE → ARCHON pipeline is cleanly defined: ECCPS outputs descriptive graphs, IEE applies 12-worldview evaluations as overlays, ARCHON uses all perspectives for decision-making. This is the clearest cross-spec integration in the ecosystem.

---

### S-05: Fandaws v3.0 (Runtime Semantic Negotiation)

**File:** `docs/03-specifications/fandaws-v3.md`
**Thesis Alignment Role:** Runtime term grounding — ensures ontological consistency

| Check | Status | Notes |
|-------|--------|-------|
| Thesis Alignment | PASS | Enables "semantically honest" by grounding ambiguous terms at runtime. IS_A/HAS dialogue phases are transparent and auditable. Scope hierarchy (context/user/global) preserves pluralism. |
| Non-Negotiables | PASS | Uncertainty Visible (conflicts presented to user as options, not forced). Human Override (curators control term promotion; sessions can be paused/abandoned). Auditability (complete session logs, relationship change history). |
| Tension Consistency | PASS | T-005: scope hierarchy enables local worldview-specific definitions without forcing global consensus. |
| Cross-Spec Consistency | PASS | References ARCHON, ECCPS, IEE, HIRI. 8 consistency checks provide deterministic validation. |
| ARCHON Alignment | PASS | Users define terms; system facilitates, doesn't impose. Aligns with guardian-not-sovereign. |
| Auditability | PASS | Complete negotiation session logs. All relationship changes timestamped with actor. |
| One-Paragraph Test | PASS | |

**Findings:**

- F-S05-1: Fandaws scope hierarchy (context → user → global) is well-designed but raises a question: what prevents scope homogenization over time? If global scope becomes dominant, local variation may be suppressed. **Action: consider documenting diversity-preservation mechanisms.**

---

### S-06: Integral Ethics Agent (IEA)

**File:** `docs/03-specifications/Integral_Ethics_Agent.md`
**Thesis Alignment Role:** 12-worldview normative deliberation engine

| Check | Status | Notes |
|-------|--------|-------|
| Thesis Alignment | PASS | Non-reductive integration of 12 worldviews. Explicit refusal to collapse plurality. Tier-1 values (Dignity, Flourishing, Truth) anchor deliberation without determining outcomes. |
| Non-Negotiables | PASS | Pluralism Respected (12 worldviews honored, none privileged). No Final Ethics (incommensurability preserved, not resolved). Guardian Not Sovereign (triage escalation upward only; cannot collapse plurality downward). |
| Tension Consistency | PASS | T-005 (pluralism vs action): directly addresses this — deliberation produces ranked paths, not single answers. Human escalation for deadlock. |
| Cross-Spec Consistency | PASS | References TagTeam for NL extraction, OCE for possibility checking, ECCPS for fidelity validation, HIRI for precedent, Fandaws for schema enforcement. |
| ARCHON Alignment | FLAG | IEA does not reference ARCHON, moral injury, or character feedback. It operates as the ethical deliberation engine but does not address how its outputs connect to ARCHON's MCM or intervention thresholds. See F-S06-1. |
| Auditability | PASS | Justification chains for all worldview reasoning. |
| One-Paragraph Test | PASS | |

**Findings:**

- **F-S06-1 [MEDIUM]: IEA does not reference ARCHON.** The IEA specification describes the 12-worldview deliberation engine but never mentions ARCHON, moral cost, or character. The ECCPS → IEE → ARCHON pipeline described in ECCPS v3.1 is not reflected from the IEA side. **Action: IEA should document its relationship to ARCHON — specifically how worldview evaluations feed ARCHON's ETI and how IEA outputs connect to MCM calculations.**

- F-S06-2: IEA's Tier-1 values (Dignity, Flourishing, Truth) likely embody The Plot's non-negotiables but this connection is not made explicit. **Action: cross-reference IEA Tier-1 values to Plot §2 non-negotiables.**

---

### S-07: MDRE Technical Specification v1.3

**File:** `docs/03-specifications/MDRE-Technical-Specification-v1.3 (1).md`
**Thesis Alignment Role:** Modal/deontic reasoning over discourse commitments

| Check | Status | Notes |
|-------|--------|-------|
| Thesis Alignment | PASS | Discourse commitment principle ensures system reasons about what texts commit to, not what is true. Directly implements "No Oracle Claims." |
| Non-Negotiables | PASS | No Oracle Claims (discourse-derived, never world-truth). Decidability (Datalog fragment ensures termination). Uncertainty Visible (5-tier evidence system). |
| Tension Consistency | PASS | T-002 (decidability vs expressiveness): Datalog fragment is decidable. Extensions via external solvers for SOL/temporal/probabilistic. |
| Cross-Spec Consistency | CONCERN | 5-tier evidence system (Tier 1-5) uses different terminology than FNSR's epistemic taint levels (L0-L5). Functional mapping unclear. See F-S07-1. |
| ARCHON Alignment | FLAG | Does not reference ARCHON, moral injury, or character. Operates below ARCHON's layer. |
| Auditability | PASS | `derived_from/3` and `inferred_from/3` provenance predicates. All inferences traceable. |
| One-Paragraph Test | PASS | |

**Findings:**

- **F-S07-1 [MEDIUM]: MDRE evidence tiers vs. FNSR epistemic taint levels.** MDRE uses a 5-tier evidence system (Tier 1 = verified, Tier 5 = unverified claim). FNSR uses L0-L5 epistemic taint levels. These serve similar functions with different terminology and granularity. **Action: document the mapping between MDRE evidence tiers and FNSR taint levels, or unify the systems.**

- F-S07-2: MDRE extracts modal commitments (obligations, permissions, possibilities) that are input to IEA deliberation. Each worldview may interpret these differently. This handoff is architecturally sound but not explicitly documented in either spec.

---

### S-08: SHML (Semantic Honesty Middle Layer)

**File:** `docs/03-specifications/middle-layer-shml.md`
**Thesis Alignment Role:** Semantic honesty enforcement — ensures assertions are events, not unmediated truth claims

| Check | Status | Notes |
|-------|--------|-------|
| Thesis Alignment | PASS | Core innovation: assertions modeled as occurrents (events), not predicates. Prevents treating discourse-derived information as world-truth. Directly implements "No Oracle Claims" and "Separation of Concerns." |
| Non-Negotiables | PASS | Separation of Concerns (mention ≠ entity; discourse ≠ world). Speculation Firewalled (belief-scoped reasoning). |
| Tension Consistency | PASS | |
| Cross-Spec Consistency | PASS | References Fandaws for runtime negotiation, BFO/CCO for grounding, Semantic Data Dictionary for data mapping. |
| ARCHON Alignment | N/A | Foundational layer — does not directly engage with character or moral costs. |
| Auditability | PASS | Assertion event traceability inherent in the model. |
| One-Paragraph Test | PASS | |

**Findings:**

- F-S08-1: SHML's "assertions as occurrents" principle is foundational to the entire ecosystem's epistemic honesty. Well-aligned with TagTeam's Information Staircase (IBE → ICE → IC) and ECCPS's claim validation. No issues found.

---

### S-09: Ontological Constraint Engine (OCE) v1.3

**File:** `docs/03-specifications/ontological-constraint-engine-spec-v1.3.md`
**Thesis Alignment Role:** Possibility boundary oracle — validates world states against BFO commitments

| Check | Status | Notes |
|-------|--------|-------|
| Thesis Alignment | PASS | Validates ontological coherence without making epistemic commitments about truth. "Epistemically passive" — proposes repairs but upstream layers decide. Guardian-like behavior at the ontological level. |
| Non-Negotiables | PASS | Decidability (bounded search, tractable OWL 2 EL/RL fragments). Separation of Concerns (OCE validates coherence; epistemic layer decides belief; IEE decides ethics). Human Override (OCE proposes, humans/upstream choose). |
| Tension Consistency | PASS | T-002 (decidability vs expressiveness): uses tractable OWL fragments, Allen Interval Algebra, RCC-8 as external solvers. Clear hand-off. |
| Cross-Spec Consistency | PASS | References IEE (consumer for possibility checking), ECCPS (upstream gate), ARCHON (meta-level constraints), Fandaws (inter-agent negotiation). |
| ARCHON Alignment | FLAG | ARCHON referenced as operating at "meta-level above OCE" but no details. See F-S09-1. |
| Auditability | PASS | Typed violations with BFO grounding, constraint references, repair path explanations. |
| One-Paragraph Test | PASS | |

**Findings:**

- **F-S09-1: OCE-ARCHON relationship underdeveloped.** OCE §12.4 states "ARCHON may constrain which ontological commitments the agent may hold — a meta-level above OCE" but provides no details. **Action: specify the ARCHON-OCE interface — how does ARCHON's character state influence OCE's constraint set?**

- F-S09-2: OCE's uncertainty handling (§9.3-9.4) is marked EXPERIMENTAL and may be moved to a dedicated spec in v2.0. Good architectural discipline — avoids overloading the core spec.

- F-S09-3: OCE's teleological interface (intent-weighted repair ranking) supports IEE by allowing ethical relevance to influence repair suggestions without altering possibility verdicts. Clean separation of concerns.

---

### S-10: PFCF v2.1 (Programming Function Classification Framework)

**File:** `docs/03-specifications/PFCF-v2.1-Specification.md`
**Thesis Alignment Role:** Governance surface for function classification and policy-aware orchestration

| Check | Status | Notes |
|-------|--------|-------|
| Thesis Alignment | PASS | Governance Primacy Rule ensures compliance/safety functions are classified correctly. Epistemic Properties (§4.5) two-axis model separates uncertainty type from reproducibility. Supports auditability through mandatory behavioral declarations. |
| Non-Negotiables | PASS | Auditability (mandatory behavioral guarantee declarations). Decidability (deterministic classification). |
| Tension Consistency | PASS | T-004 (speed vs rigor): behavioral guarantees allow orchestrators to make informed latency/safety tradeoffs. |
| Cross-Spec Consistency | PASS | Epistemic Properties axis (Deterministic/Aleatory/Epistemic/Mixed) is consistent with SFS and SDP confidence models. |
| ARCHON Alignment | N/A | Infrastructure classification framework — does not engage with moral costs. |
| Auditability | PASS | Mandatory machine-readable declarations with full behavioral specification. |
| One-Paragraph Test | PASS | |

**Findings:**

- F-S10-1: PFCF's epistemic properties model (uncertainty type × reproducibility) should be cross-referenced with MDRE's evidence tiers and FNSR's taint levels. All three address epistemic quality but with different vocabularies. See F-S07-1.

---

### S-11: Semantic Data Dictionary v2.0

**File:** `docs/03-specifications/semantic-data-dictionary.md`
**Thesis Alignment Role:** Maps relational data to BFO/CCO-compliant assertion events

| Check | Status | Notes |
|-------|--------|-------|
| Thesis Alignment | PASS | Assertion Events model treats data as events (occurrents), not bare facts. Directly implements SHML's "assertions as occurrents" principle. Null semantics distinguish missing data (ignorance) from negative assertion. |
| Non-Negotiables | PASS | Separation of Concerns (Information Staircase: IBE → ICE → IC). Uncertainty Visible (null semantics, epistemic taint from missing foreign keys). Provenance Always (invertible relations enable bidirectional traceability). |
| Tension Consistency | PASS | |
| Cross-Spec Consistency | PASS | Directly implements SHML architecture. Consistent with TagTeam's Information Staircase. |
| ARCHON Alignment | N/A | Data layer — does not engage with moral costs. |
| Auditability | PASS | Invertible relations and assertion event structure enable full traceability. |
| One-Paragraph Test | PASS | |

**Findings:**

- F-S11-1: The critical distinction between null-as-ignorance and null-as-negation is well-handled. Missing foreign key = information gap (epistemic taint). Explicit null value = negative assertion (no taint). This aligns with the ecosystem's epistemic honesty commitments.

---

### S-12: Semantic Data Platform v1.1

**File:** `docs/03-specifications/semantic-data-platform_v1.1.md`
**Thesis Alignment Role:** Operational platform for ingesting, reconciling, and querying semantic data

| Check | Status | Notes |
|-------|--------|-------|
| Thesis Alignment | PASS | Ontology Registry Service (new in v1.1) prevents schema inconsistency. HITL Reconciliation Service preserves human override for entity matching. Processing Status Service enables auditability. |
| Non-Negotiables | PASS | Human Override (HITL service: confidence <0.85 requires human review). Auditability (Processing Status Service tracks all pipeline stages). Separation of Concerns (8 architectural layers with clear boundaries). |
| Tension Consistency | PASS | T-004 (speed vs rigor): confidence thresholds (≥0.95 auto-commit, 0.85-0.94 auto-commit + audit flag, <0.85 human review). |
| Cross-Spec Consistency | PASS | References TagTeam as ingestion adapter. Ontology Registry enforces CCO version consistency across adapters. |
| ARCHON Alignment | N/A | Data platform — does not engage with moral costs. |
| Auditability | PASS | Processing Status Service provides pipeline-wide observability. |
| One-Paragraph Test | PASS | |

**Findings:**

- F-S12-1: SDP's confidence thresholds for auto-commit (≥0.95) vs. human review (<0.85) are well-calibrated. The 0.85-0.94 "auto-commit + flag for audit" tier is a pragmatic middle ground.

---

### S-13: SFS v2.2 (Semantic Function Schema)

**File:** `docs/03-specifications/SFS-v2.2-Specification.md`
**Thesis Alignment Role:** Schema for declaring semantic function behavior — the contract between functions and orchestrators

| Check | Status | Notes |
|-------|--------|-------|
| Thesis Alignment | PASS | Pure and deterministic functions are non-negotiable. Effects separated from side effects (critical for AI safety: semantic engine determines needed effects; authorization layer decides if allowed). |
| Non-Negotiables | PASS | Auditability (delegation chains trace all agent actions). Human Override (Authorization Gates new in v2.2; Plan Handshakes require explicit approval). Decidability (deterministic functions only). |
| Tension Consistency | PASS | |
| Cross-Spec Consistency | PASS | Epistemic properties (Deterministic/Aleatory/Epistemic/Mixed) consistent with PFCF v2.1. Authorization Gates align with DSFC executor refusal rights. |
| ARCHON Alignment | N/A | Function schema — does not engage with moral costs. |
| Auditability | PASS | Delegation chains, authorization gates, plan verification. |
| One-Paragraph Test | PASS | |

**Findings:**

- F-S13-1: SFS v2.2's effect/side-effect separation is an important safety pattern. The semantic engine determines what effects are needed; the authorization layer decides if they're allowed. This is consistent with the guardian-not-sovereign principle at the function level.

---

### S-14: TagTeam Consolidated Roadmap v6.6.0

**File:** `docs/03-specifications/tagteam-ROADMAP.md`
**Thesis Alignment Role:** Implementation roadmap for the TagTeam semantic parser

| Check | Status | Notes |
|-------|--------|-------|
| Thesis Alignment | PASS | "Better to output structured uncertainty than false precision." Browser-first, deterministic. Phase 5 ambiguity flagging and Phase 6 interpretation lattice directly serve epistemic honesty. |
| Non-Negotiables | PASS | Uncertainty Visible (ambiguity flags surface in @graph nodes, not hidden). Auditability (resolution logging, golden corpus validation). |
| Tension Consistency | PASS | |
| Cross-Spec Consistency | PASS | Phase 6.5 BridgeOntologyLoader maps to IEE worldviews via `ethics:mapsToWorldview`. This is the only spec that operationally connects to the 12 worldviews at the parsing level. |
| ARCHON Alignment | N/A | Parser — does not engage with moral costs. |
| Auditability | PASS | Deterministic rules, golden corpus validation, phase-by-phase completion tracking. |
| One-Paragraph Test | PASS | |

**Findings:**

- F-S14-1: Phase 6.5.4 BridgeOntologyLoader maps TagTeam values → ValueNet dispositions → IEE worldviews (e.g., `tagteam:Autonomy` → `vn:AutonomyDisposition` → `iee:SelfDirectionWorldview`). This is a concrete IEE integration that should be cross-referenced in the IEA specification.

- F-S14-2: Phase 7 (Epistemic Layer) includes certainty markers (hedges/boosters) with 24 passing tests. This connects to MDRE's evidence tiers and FNSR's taint levels. **Action: document mapping between TagTeam certainty scores and MDRE evidence tiers.**

- F-S14-3: v1/v2 scope contract (2026-01-28) is well-defined. v1 is stabilization (single-clause, deterministic), v2 is structural semantics and normalization. Realistic scoping.

---

## Specifications Layer Summary

### Overall Assessment: STRONG COHERENCE WITH INTEGRATION GAPS

The specifications layer is remarkably internally consistent. All 14 documents share common design principles: failure preferred over false certainty, auditability as non-negotiable, human override at every layer, BFO/CCO as ontological foundation. No contradictions were found between specifications.

The primary issues are integration gaps — specifications that don't reference each other when they should, and terminology divergences for functionally equivalent concepts.

### Issues Requiring Action

#### High Priority

| ID | Issue | Action | Specs Affected |
|----|-------|--------|----------------|
| F-S03-1 | Two ECCPS specs (v2.1.1 and v3.1) — relationship unclear | Clarify supersession or archive v2.1.1 | ECCPS FRD, ECCPS Spec |
| F-S06-1 | IEA does not reference ARCHON or its pipeline role | Document IEA → ARCHON interface | IEA, ARCHON Functional |
| F-S07-1 | MDRE evidence tiers vs. FNSR taint levels — different terminology for similar concepts | Create unified mapping or terminology table | MDRE, FNSR, PFCF, TagTeam |

#### Medium Priority

| ID | Issue | Action | Specs Affected |
|----|-------|--------|----------------|
| F-S01-1 | Terminology drift: "moral injury" (philosophy) vs. "moral cost/debt/scar" (functional spec) | Add terminology mapping table | ARCHON Philosophy, ARCHON Functional |
| F-S09-1 | OCE-ARCHON relationship underdeveloped | Specify ARCHON-OCE interface | OCE, ARCHON |
| F-S01-2 | Emergency Override post-exhaustion state undefined | Document what happens after 2 uses | ARCHON Functional |
| F-S05-1 | Scope homogenization risk in Fandaws | Document diversity-preservation mechanisms | Fandaws |

#### Low Priority

| ID | Issue | Action | Specs Affected |
|----|-------|--------|----------------|
| F-S06-2 | IEA Tier-1 values not cross-referenced to Plot non-negotiables | Make connection explicit | IEA, The Plot |
| F-S10-1 | Multiple epistemic quality vocabularies across specs | Cross-reference PFCF, MDRE, FNSR, TagTeam epistemic models | Multiple |
| F-S14-1 | TagTeam BridgeOntologyLoader not referenced in IEA | Cross-reference Phase 6.5.4 in IEA spec | TagTeam, IEA |
| F-S14-2 | TagTeam certainty markers not mapped to MDRE evidence tiers | Document mapping | TagTeam, MDRE |

### New Tensions Discovered

| ID | Tension | Source |
|----|---------|--------|
| T-010 (candidate) | Epistemic Quality Vocabulary Fragmentation: At least four different systems describe epistemic quality — FNSR taint levels (L0-L5), MDRE evidence tiers (1-5), PFCF uncertainty types (Deterministic/Aleatory/Epistemic/Mixed), and TagTeam certainty markers (hedges/boosters). These are functionally related but use incompatible terminology and scales. | F-S07-1, F-S10-1, F-S14-2 |

### Cross-Layer Integration Patterns

The specifications layer reveals a clear processing pipeline:

```
Input (NL) → TagTeam (parsing) → ECCPS (validation) → MDRE (modal reasoning)
    → OCE (coherence) → IEA (deliberation) → ARCHON (governance)
```

Supporting infrastructure:
- **SHML** provides the foundational principle (assertions as events)
- **SDD** implements SHML for relational data
- **SDP** provides the operational platform
- **Fandaws** handles runtime term negotiation at every stage
- **DSFC** distributes semantic functions across communities
- **SFS** defines the function contract schema
- **PFCF** classifies functions for governance
- **HIRI** records precedents (referenced but not in spec set)

### Cross-Cutting Design Principles (Confirmed Across All 14 Specs)

1. **Failure preferred over false certainty** — every spec implements this
2. **Auditability as non-negotiable** — every spec has audit mechanisms
3. **Human override preserved** — escalation, refusal, challenge mechanisms throughout
4. **BFO/CCO as ontological backbone** — consistent across all specs
5. **Determinism required** — functions must be pure/deterministic; LLM components use temperature=0
6. **Distributed authority** — no single decision-maker at any layer

---

*Layer 3 (Specifications) review complete. See Specifications Layer Summary above for action items.*

---

## Layer 3 Addendum: New Specifications (2026-01-31)

### HIRI Protocol Spec v2.1.0

| Check | Result | Notes |
|-------|--------|-------|
| 1. Thesis Alignment | **PASS** | HIRI provides "verifiable claim identifiers" — directly serves the "trust without centralization" role mapped in The Plot §4. Local-first, content-addressed verification is deeply aligned with the core thesis of accountable synthetic agency. |
| 2. Non-Negotiable Preservation | **PASS** | All 12 non-negotiables maintained. Provenance Always: content-addressed hashes + signature chains. Auditability: sequential history with compaction proofs. Uncertainty Visible: trust levels and verification modes explicitly documented. No Oracle Claims: HIRI separates "data access" from "truth verification" (§2.2 — "Data access and truth verification are not the same problem"). |
| 3. Tension Consistency | **PASS** | Touches T-004 (Speed vs. Rigor) via cold-start strategies with explicit trust trade-offs (TOFU → full verification). Does not create new tensions with Plot §3. |
| 4. Cross-Spec Consistency | **FLAG** | (F-S15-1) HIRI is referenced in the Integration Spec event registry (`fnsr.claim.signed`) and in CloudEvents headers (`fnsr-provenance: "hiri://sha256:abc123"`), but the Integration Spec references HIRI v1 implicitly. HIRI v2.1 introduces chain compaction, privacy accumulators, and materialized entailment — none of these are reflected in the Integration Spec contracts. The `fnsr-provenance` header format should be validated against HIRI v2.1 URI scheme. |
| 4. Cross-Spec Consistency | **FLAG** | (F-S15-2) HIRI §11 (Semantic Interoperability) references BFO and shared upper ontologies but does not cross-reference the TagTeam BridgeOntologyLoader or the Semantic Data Dictionary, which are the FNSR-specific mechanisms for vocabulary alignment. |
| 4. Cross-Spec Consistency | **FLAG** | (F-S15-3) HIRI §9 (ZK Claims Layer) introduces a privacy budget framework and Privacy Accumulators that have no counterpart in IEA or ARCHON governance. If FNSR uses HIRI for provenance signing, ARCHON's governance authority should have a defined relationship to HIRI's Privacy Authority concept. |
| 5. ARCHON Alignment | **PASS** | HIRI does not conflict with ARCHON's governance model. HIRI provides infrastructure-level primitives that ARCHON can use. The chain compaction model (recursive SNARKs proving history validity) is compatible with the auditability non-negotiable — history is compressed but verifiable, not deleted. |
| 6. Auditability Verification | **PASS (exemplary)** | HIRI is auditability infrastructure. Sequential manifest chains, content-addressed hashes, key lifecycle management, chain compaction with cryptographic proofs, explicit trust assumptions at every layer. §14 (Security Model) documents every trust assumption explicitly — aligned with Plot §2.3. |
| 7. One-Paragraph Test | **PASS** | HIRI provides the decentralized, verifiable provenance layer that makes "Provenance Always" implementable without centralized trust anchors. Every claim in the FNSR pipeline can be content-addressed, signed, and verified offline. Without HIRI, the system depends on server trust for claim integrity, violating the separation-of-concerns non-negotiable. |

**Findings:**
- **F-S15-1** (Medium): Integration Spec references to HIRI need updating for v2.1 features (compaction, privacy accumulators, materialized entailment).
- **F-S15-2** (Low): HIRI's vocabulary alignment strategies should cross-reference FNSR-specific ontology mechanisms (BridgeOntologyLoader, Semantic Data Dictionary).
- **F-S15-3** (Medium): HIRI Privacy Authority ↔ ARCHON governance relationship undefined. If FNSR uses HIRI for provenance, the governance layer needs to know about privacy budget enforcement.

**New Tension Candidate:**
- **T-011: Privacy Budget Authority vs. Distributed Governance** — HIRI's Privacy Accumulator model (§9.5) introduces a centralized Privacy Authority for budget enforcement. This is architecturally at odds with the distributed-authority design principle ("no single decision-maker at any layer"). HIRI acknowledges this trade-off (§9.5.7: federated authorities, §1.2: "HIRI does not solve all coordination problems") but the FNSR ecosystem hasn't decided whether to accept a Privacy Authority as a governance entity or treat it as an infrastructure primitive outside ARCHON's jurisdiction.

---

### IRIS v1.2 — Integrated Real-time Input Sensing

| Check | Result | Notes |
|-------|--------|-------|
| 1. Thesis Alignment | **PASS (strong)** | IRIS provides the direct perception layer — the system's "eyes and ears" for the physical world. Extends the processing pipeline upstream of TagTeam. Directly serves the thesis by enabling the system to reason about the world while maintaining epistemic discipline about what perception actually provides. |
| 2. Non-Negotiable Preservation | **PASS (exemplary)** | No Oracle Claims: L1-ASSERTED explicitly marks documents as "claimed, not verified" — directly operationalizes the non-negotiable. Provenance Always: sensor provenance + model provenance + drift state on every observation. Uncertainty Visible: confidence scores mandatory, drift warnings visible, precondition failures flagged. Speculation Firewalled: clear taint hierarchy with epistemic firewall between L2 and L3. Moral Injury Real: INTUS tracks injury as L1-INTERNAL (system doesn't grant itself false certainty about its own moral state). |
| 3. Tension Consistency | **PASS** | IRIS's internal "T-007" and "T-008" (§11) use different numbering than the ARIADNE tension log. IRIS's T-007 (model-mediated perception vs. raw signal) is a local resolution, not a conflict with the global T-007 (tool-to-person threshold). IRIS's T-008 (self-knowledge certainty) is also a local resolution. No conflicts with Plot §3 tensions. |
| 3. Tension Consistency | **FLAG** | (F-S16-1) IRIS §11 defines its own tension numbers (T-007, T-008) that collide with the ARIADNE tension log numbering. These should be either renamed to IRIS-local identifiers or mapped to the global log. |
| 4. Cross-Spec Consistency | **FLAG** | (F-S16-2) IRIS extends the FNSR taint hierarchy with sub-levels (L0-RAW, L1-PERCEIVED, L1-INTERNAL, L1-ASSERTED) that are more granular than FNSR's L0-L5. The Epistemic Vocabulary Mapping spec (v1.0) does not include IRIS's sub-levels. This is a gap in the mapping. |
| 4. Cross-Spec Consistency | **FLAG** | (F-S16-3) IRIS is not listed in the Integration Spec §4.2 event registry. IRIS should produce events (e.g., `fnsr.observation.created`, `fnsr.sensor.degraded`, `fnsr.model.drift_detected`) and consume events (e.g., `fnsr.document.validated` for conflict resolution). |
| 4. Cross-Spec Consistency | **FLAG** | (F-S16-4) IRIS references HIRI for content addressing (`raw_hiri: "hiri://blob/..."` in the observation schema, §8) but does not specify how IRIS observations are signed or chained using HIRI v2.1 manifests. The HIRI integration is referenced but not specified. |
| 4. Cross-Spec Consistency | **PASS** | IRIS's language enforcement (§5) — prohibiting modal verbs, causal language, normative predicates — is consistent with SHML's semantic honesty mandate. IRIS enforces at the perception layer what SHML enforces at the output layer. |
| 5. ARCHON Alignment | **PASS** | IRIS correctly classifies moral injury as L1-INTERNAL rather than L0-RAW. This means ARCHON's character accumulation model receives interpreted data, not falsely certain data. The INTUS subsystem's moral_injury_level output is explicitly marked as "an interpreted aggregate, NOT raw" — consistent with D-001 (character genuinely influences decisions, but the system doesn't claim certainty about its own moral state). |
| 6. Auditability Verification | **PASS** | Full provenance chain: sensor → model → drift state → observation node. Language compliance validated at schema level. Conflict resolution requires explicit preconditions. Model drift governance includes audit schedule (hourly automated, weekly human review, quarterly recalibration). |
| 7. One-Paragraph Test | **PASS** | IRIS provides epistemically disciplined perception — the system's interface with the physical world, where every observation carries its sensor provenance, model provenance, confidence bounds, and drift state. Without IRIS, the system would either lack real-world sensing or would claim false certainty about what it perceives. IRIS ensures the system "refuses to claim certainty it doesn't have" at the very first point of contact with reality. |

**Findings:**
- **F-S16-1** (Low): IRIS tension numbering collides with ARIADNE global tension log. Rename to IRIS-T-001/IRIS-T-002 or assign new global IDs.
- **F-S16-2** (Medium): IRIS's taint sub-levels (L0-RAW, L1-PERCEIVED, L1-INTERNAL, L1-ASSERTED) not reflected in Epistemic Vocabulary Mapping spec.
- **F-S16-3** (Medium): IRIS missing from Integration Spec event registry.
- **F-S16-4** (Low): IRIS → HIRI integration referenced but not fully specified.

---

### Addendum Summary

| Priority | Finding | Action |
|----------|---------|--------|
| **Medium** | F-S15-1: Integration Spec HIRI references need v2.1 update | Round 3-style cross-reference edit |
| **Medium** | F-S15-3: HIRI Privacy Authority ↔ ARCHON governance undefined | Requires design decision |
| **Medium** | F-S16-2: Epistemic Vocabulary Mapping needs IRIS sub-levels | Update existing spec |
| **Medium** | F-S16-3: IRIS missing from Integration Spec event registry | Round 3-style cross-reference edit |
| **Low** | F-S15-2: HIRI vocabulary alignment → BridgeOntologyLoader cross-ref | Cross-reference edit |
| **Low** | F-S16-1: IRIS tension numbering collision | Rename in IRIS doc |
| **Low** | F-S16-4: IRIS → HIRI observation signing not specified | Future spec work |

**New Tension:** T-011 (Privacy Budget Authority vs. Distributed Governance) — see HIRI review above.
