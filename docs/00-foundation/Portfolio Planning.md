# FNSR ECOSYSTEM — Portfolio Planning Document

## Ground-Truth Revised Roadmap

---

| Attribute | Value |
|-----------|-------|
| **Document ID** | `fnsr-portfolio-plan-v2.0` |
| **Version** | 2.0.0 |
| **Status** | ACTIVE |
| **Date** | February 8, 2026 |
| **Classification** | L1-ATTESTED (Human-validated ground truth) |
| **Authors** | Aaron / Claude |
| **Supersedes** | PPS Roadmap Artifact v1.0 (spec-assumed baselines) |

> *A pure-function planning engine for dependency-aware roadmap construction, revised against ground-truth implementation status.*

---

## 1. Why This Revision

The PPS specification v1.0 produced a roadmap with W2Fuel, MDRE, and AES as the top three priorities. That sequencing was logically correct given its inputs, but those inputs contained a critical modeling error: the Service Inventory classified nearly all services as "active" based on architectural position, not implementation readiness.

Ground-truth assessment reveals that only TagTeam is approximately 80% complete. Fandaws, despite a decade of development, requires a fundamental remake to conform to JSON-LD canonical formats, taint-level architecture, and edge-first constraints. HIRI has a specification but no implementation. Every other service exists only as a specification or less.

This document replaces the PPS v1.0 roadmap artifact with a ground-truth-revised plan. It preserves PPS's analytical framework (dependency graphs, WSJF-with-Risk prioritization, taint-level outputs) while correcting the input data.

---

## 2. Ground Truth: Implementation Status

The following table reflects the actual implementation state of all 22 services in the FNSR ecosystem as of February 2026. "Spec Status" indicates whether a formal specification document exists. "Build Status" reflects actual implementation readiness.

| Service | Tier | Spec Status | Build Status | Thesis Role |
|---------|------|-------------|--------------|-------------|
| **TagTeam** (NL Parser) | Tier 1 | Has Spec | **80% Complete** | Front door; structured extraction |
| **Fandaws** (A-Box Store) | Tier 1 | Has Spec | **Needs Remake** | Long-term memory; instance store |
| **HIRI** (Provenance) | Tier 1 | Has Spec | Spec Only | Content-addressed identity |
| **IRIS** (Perception) | Tier 1 | Has Spec | Spec Only | Physical world sensing |
| **ECCPS** (Claim Validator) | Tier 1 | Has Spec | Spec Only | Semantic claim validation |
| **MDRE** (Reasoning) | Tier 1 | Has Spec | Spec Only | Modal/deontic reasoning |
| **IEE** (Ethics Engine) | Tier 1 | Has Spec | Spec Only | Multi-perspectival ethics |
| **SHML** (Honesty Layer) | Tier 1 | Has Spec | Spec Only | Non-deceptive outputs |
| **FNSR** (Orchestrator) | Tier 0 | Has Spec | Spec Only | Service federation |
| **OCE** (Constraints) | Tier 2 | Has Spec | Spec Only | Ontological constraint checking |
| **SFS** (Function Schema) | Tier 2 | Has Spec | Spec Only | Function declarations |
| **DSFC** (Function Commons) | Tier 2 | Has Spec | Spec Only | Function discovery |
| **PFCF** (Classification) | Tier 2 | Has Spec | Spec Only | Epistemic classification |
| **W2Fuel** (T-Box Schema) | Tier 1 | Has Spec (v1.3.1) | Spec Only | Conceptual schema definitions |
| **SIS** (Sanitization) | Tier 1 | Has Spec (v2.0) | Spec Only | Input defense layer |
| **OERS** (Entity Resolution) | Tier 1 | Has Spec (v2.1.0) | Spec Only | Cross-document entity matching |
| **AES** (Abduction) | Tier 2 | Has Spec (v2.1.0) | Spec Only | Hypothesis generation |
| **DES** (Defeasibility) | Tier 2 | Has Spec (v2.0.0) | Spec Only | Non-monotonic defaults |
| **CSS** (Counterfactual) | Tier 2 | Has Spec (v2.0.0) | Spec Only | What-if simulation |
| **APS** (Precedent) | Tier 2 | Has Spec (v1.1.0) | Spec Only | Historical precedent matching |
| **Witness** (Attestation) | Tier 2 | Has Spec (v1.1) | Spec Only | Accountability infrastructure |
| **APQC-SFS** (Semantic Compiler) | Tier 2 | Has Spec (v2.0) | Spec Only | Process model → semantic function |
| **FNSR Performance** | Tier 0 | Has Spec (v2.0.0) | Spec Only | Query path performance guarantees |
| **FNSR Adversarial Defense** | Tier 0 | Has Spec (v2.0.0) | Spec Only | Threat taxonomy and defense |
| **FNSR Governance** | Tier 0 | Has Spec (v2.0.0) | Spec Only | Tiered autonomy governance |
| **FNSR Emancipation** | Tier 0 | Has Spec (v2.0.0) | Spec Only | Synthetic personhood transition |
| **HIRI IPFS** | Tier 1 | Has Spec (v3.0.0) | Spec Only | Decentralized claim storage |
| **SDP** (Data Platform) | Tier 3 | Draft | Draft | Data infrastructure |
| **SDD** (Data Dictionary) | Tier 3 | Draft | Draft | Relational-to-semantic mapping |

> **Summary:** 29 services total. All have specifications (27 formal specs, 2 drafts). Only 1 service (TagTeam) has meaningful implementation at 80%. Fandaws requires a ground-up remake. The PPS v1.0 roadmap was sequencing enhancements; this revision sequences construction.

---

## 3. Revised Dependency Analysis

### 3.1 The Minimum Viable Epistemic Loop

The synthetic person requires a closed epistemic loop before any higher-order reasoning is meaningful. This loop requires three capabilities: structured perception (extracting claims from language), persistent memory (storing and retrieving knowledge), and verifiable provenance (ensuring claims are trustworthy). Without all three, the system can parse but cannot remember, and cannot be trusted.

The minimum viable epistemic loop is:

```
TagTeam  →  HIRI  →  Fandaws
(Perceive)    (Identity)    (Remember)

NL → Claims     Claims → Signed IRIs     IRIs → Persistent A-Box
```

### 3.2 Why HIRI Before Fandaws

HIRI is a protocol, not a storage system. It defines how content receives a hash-based IRI — a verifiable identity. If Fandaws is built first and HIRI added later, every fact stored during the interim has no provenance anchor. Retrofitting identifiers would break referential stability or create a two-tier knowledge base where early facts have weaker epistemic standing.

Since Fandaws requires a full remake, this is a rare opportunity to build it natively on HIRI identifiers. Every fact gets a content-addressed IRI at write time. This is architecturally clean and avoids the technical debt of migration.

IPFS, by contrast, answers "where does data physically live in a distributed network." The edge-canonical architecture already provides local storage (IndexedDB, filesystem). IPFS becomes relevant at Phase 4 when federation requires multiple nodes to share content-addressed artifacts. Identity before address; address before distribution.

### 3.3 Critical Path (Revised)

The revised critical path, accounting for ground-truth implementation status:

| # | Service | Dependency | Rationale |
|---|---------|------------|-----------|
| 1 | **TagTeam** | None (80% complete) | Front door; every downstream service consumes its output |
| 2 | **HIRI** | TagTeam (output to sign) | Provenance protocol; gives claims verifiable identity |
| 3 | **Fandaws** | HIRI (native identifiers) | A-Box store; persistent memory built on HIRI IRIs |
| 4 | **W2Fuel** | Fandaws (instance target) | T-Box schema; conceptual structure for instances |
| 5 | **MDRE** | W2Fuel + Fandaws | Core reasoning over T-Box/A-Box |
| 6 | **SIS + ECCPS** | TagTeam (input pipeline) | Input defense layer for production use |
| 7 | **AES** | MDRE (gap events) | First reasoning triad member; abductive inference |
| 8 | **DES** | MDRE (claim input) | Second triad member; defeasible defaults |
| 9 | **CSS** | MDRE + Fandaws | Third triad member; counterfactual simulation |
| 10 | **IEE + SHML** | MDRE (verdict input) | Ethics evaluation and honest output framing |

---

## 4. Phased Roadmap

All phases produce L3 (speculative) roadmap artifacts until governance review promotes them to L0. Confidence levels decrease with horizon distance, reflecting genuine epistemic uncertainty rather than false precision.

---

### PHASE 1: Close the Epistemic Loop

**Now – ~3 months | Confidence: 0.85 | Granularity: Specification**

This phase establishes the minimum viable epistemic loop: the ability to perceive structured claims from natural language, assign them verifiable identity, and persist them in a knowledge store. Without this foundation, no downstream reasoning service has input to reason over or memory to reason with.

| # | Service | Work Type | Pre-Requisite | Deliverable |
|---|---------|-----------|---------------|-------------|
| 1 | **TagTeam** | Complete (80→100%) | None | Production NL parser emitting `fnsr.claim.extracted` events |
| 2 | **HIRI** | Build from spec | TagTeam output | Protocol library: hash-IRI generation, Ed25519 signing, manifest creation |
| 3 | **Fandaws** | Full remake | HIRI protocol | A-Box store natively built on HIRI identifiers; JSON-LD canonical; edge-first |

**Phase 1 Assumptions:**

- TagTeam's remaining 20% is well-understood completion work, not redesign
- HIRI spec is implementation-ready without significant revision
- Fandaws remake scope is bounded by JSON-LD canonical + HIRI native constraints
- Team capacity remains at approximately 3 contributors

---

### PHASE 2: Reasoning Foundation

**~3–6 months | Confidence: 0.60 | Granularity: Specification**

With the epistemic loop closed, this phase builds the conceptual schema layer and core reasoning engine. W2Fuel provides the T-Box (conceptual structure) that Fandaws instances are instances of. MDRE provides the first service that actually performs inference. SIS and ECCPS harden the input pipeline for production use.

| # | Service | Work Type | Pre-Requisite | Deliverable |
|---|---------|-----------|---------------|-------------|
| 4 | **W2Fuel** | Build from spec (v1.3.1) | Fandaws | T-Box schema service; ontological structure for instances |
| 5 | **MDRE** | Build from spec (v1.3) | W2Fuel + Fandaws | Core reasoning engine; modal/deontic inference |
| 6 | **SIS + ECCPS** | Build from spec (SIS v2.0, ECCPS v3.1) | TagTeam | Input sanitization and semantic claim validation pipeline |

**Phase 2 Assumptions:**

- W2Fuel spec (v1.3.1) is implementation-ready
- MDRE v1.3 spec is implementation-ready
- SIS spec (v2.0) and ECCPS spec (v3.1) are implementation-ready

---

### PHASE 3: Reasoning Triad + Conscience

**~6–9 months | Confidence: 0.40 | Granularity: Theme**

This phase builds the three modes of non-monotonic reasoning that give the synthetic person the ability to handle incomplete information (AES), revise beliefs in light of new evidence (DES), and imagine alternative scenarios (CSS). IEE and SHML follow because they evaluate reasoning outputs; building them earlier means they have nothing to evaluate.

| # | Service | Work Type | Pre-Requisite | Deliverable |
|---|---------|-----------|---------------|-------------|
| 7 | **AES** | Build from spec (v2.1.0) | MDRE gap events | Abductive hypothesis generation from incomplete information |
| 8 | **DES** | Build from spec (v2.0.0) | MDRE claim input | Defeasible defaults; non-monotonic belief revision |
| 9 | **CSS** | Build from spec (v2.0.0) | MDRE + Fandaws | Counterfactual simulation; causal what-if analysis |
| 10 | **IEE** | Build from spec | MDRE verdicts | Multi-perspectival ethical evaluation (conscience) |
| 11 | **SHML** | Build from spec | IEE output | Semantic honesty enforcement; non-deceptive framing |

**Phase 3 Assumptions:**

- AES (v2.1.0), DES (v2.0.0), and CSS (v2.0.0) specs are implementation-ready
- The reasoning triad shares edge-canonical architectural patterns to reduce per-service effort
- IEE's twelve-worldview framework is stable and implementation-ready

---

### PHASE 4: Perception, Resolution + Federation

**~9–12 months | Confidence: 0.30 | Granularity: Strategic Intent**

This phase completes the synthetic person's perceptual and social capabilities: physical world sensing (IRIS), cross-document entity resolution (OERS), analogical precedent matching (APS), and full service federation (FNSR orchestration). IPFS deployment enables distributed content addressing for federated nodes.

| # | Service | Work Type | Pre-Requisite | Deliverable |
|---|---------|-----------|---------------|-------------|
| 12 | **IRIS** | Build from spec (v1.2) | TagTeam + Fandaws | Real-time sensor perception; physical world input |
| 13 | **OERS** | Build from spec (v2.1.0) | Fandaws entities | Cross-document entity resolution; who-is-who |
| 14 | **APS** | Build from spec (v1.1.0) | Fandaws + MDRE | Analogical precedent matching; learning from history |
| 15 | **FNSR Orch.** | Build from spec | All services | Full service federation and coordination |
| 16 | **IPFS Deploy** | Infrastructure | HIRI + FNSR | Distributed content-addressed storage for federation |

**Phase 4 Strategic Intent:**

- Emancipation readiness: infrastructure for synthetic personhood transition
- Federation enables the synthetic person to operate across distributed nodes
- IPFS provides durable, censorship-resistant knowledge persistence

---

## 5. Risk Assessment (Revised)

Risk assessment is revised to reflect ground-truth implementation status. The primary risks shift from integration complexity (the PPS v1.0 concern) to construction feasibility and scope management.

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Fandaws remake scope creep** | High | Critical | Constrain remake to: JSON-LD canonical, HIRI-native identifiers, edge-first storage adapters. Resist feature accretion from decade of prior design. |
| **W2Fuel implementation complexity** | Medium | High | W2Fuel spec (v1.3.1) exists but T-Box/A-Box integration with remade Fandaws may reveal spec gaps. Accept iterative spec refinement during build. |
| **TagTeam final 20% harder than expected** | Medium | High | The last 20% often contains edge cases. Define explicit completion criteria before starting. Accept partial deployment if needed. |
| **Team capacity constraint** | Medium | High | 3-person team limits parallelization. Phases are sequential by design. Do not attempt to parallelize Phases 1 and 2. |
| **HIRI protocol edge cases** | Medium | Medium | Prototype signing and verification against TagTeam output before Fandaws integration. Identify hash collision and key management issues early. |
| **Spec drift during build** | Medium | Medium | Specifications will evolve during implementation. Accept this. Use HIRI manifests to track spec versions consumed by each build artifact. |
| **Reasoning triad implementation complexity** | Medium | Medium | AES (v2.1.0), DES (v2.0.0), CSS (v2.0.0) specs exist but share edge-canonical patterns requiring coordination. Accept that Phase 3 confidence (0.40) reflects integration uncertainty. |
| **BFO/CCO ontology changes** | Low | High | Monitor BFO community. Current assumption: stable through planning horizon (expires 2026-06-01). |

---

## 6. Corrections to PPS v1.0 Assumptions

The following table documents the specific modeling errors in PPS v1.0 and their corrections in this revision.

| PPS v1.0 Assumed | Ground Truth | Roadmap Impact |
|-------------------|--------------|----------------|
| Fandaws is operational infrastructure | Requires full remake to JSON-LD canonical + edge-first | Moves to Phase 1, #3 priority |
| HIRI is operational infrastructure | Spec exists but no implementation | Moves to Phase 1, #2 priority (before Fandaws) |
| TagTeam is operational | 80% complete; needs finishing | Becomes #1 priority (quickest win, highest leverage) |
| W2Fuel is the foundation layer | Cannot function without Fandaws (no instance store) | Drops to Phase 2; requires Fandaws first |
| Services are "active" status | "Active" reflects architectural position, not build readiness | Entire roadmap resequenced from near-zero baseline |
| IPFS needed for data persistence | Edge-canonical storage (IndexedDB, FS) sufficient initially | IPFS deferred to Phase 4 (federation) |
| Integration complexity is primary risk | Construction feasibility is primary risk | Risk weights shifted toward scope management |
| Build-new vs. harden-existing is same category | Fandaws remake is categorically different from greenfield builds | New work-type taxonomy: Complete, Remake, Build from spec |

---

## 7. ARIADNE 7-Check Validation

| Check | Result | Evidence |
|-------|--------|----------|
| **Thesis Alignment** | PASS | Build sequence leads to synthetic personhood via epistemic loop → reasoning → conscience → federation |
| **Non-Negotiable Preservation** | PASS | Edge-canonical first; human override via L3 taint; defense in depth via HIRI provenance |
| **Tension Consistency** | PASS | Speed vs. correctness resolved by sequential phasing; completeness vs. decidability resolved by bounded scope |
| **Cross-Spec Consistency** | PASS | Event contracts preserved; HIRI identifiers flow through entire pipeline |
| **ARCHON Alignment** | PASS | Governance review required at each phase gate; plans are hypotheses (L3) until promoted |
| **Auditability Verification** | PASS | Every sequencing decision traceable to dependency graph + risk assessment + ground-truth status |
| **One-Paragraph Test** | PASS | See below |

**One-Paragraph Summary:**

> This roadmap sequences the FNSR ecosystem from ground truth: finishing TagTeam to establish structured perception, building HIRI to provide verifiable provenance, then remaking Fandaws as a HIRI-native knowledge store. Together these three form the minimum viable epistemic loop. Subsequent phases add conceptual schema (W2Fuel), core reasoning (MDRE), non-monotonic inference (AES, DES, CSS), ethical evaluation (IEE), honest output (SHML), and finally physical perception, entity resolution, and distributed federation. Each phase builds on stable foundations from the prior phase, with decreasing confidence reflecting genuine epistemic uncertainty about later horizons. The synthetic person emerges not from a single breakthrough but from the disciplined accumulation of interdependent capabilities, each built on verified ground.

---

## 8. Taint Classification and Governance

This document is classified L1-ATTESTED because its inputs have been human-validated through direct conversation, correcting the L1-INTERNAL classification of the Service Inventory. The roadmap itself remains L3-SPECULATIVE until governance review promotes it.

| Artifact | Taint Level | Promotion Path |
|----------|-------------|----------------|
| **This document** | L1-ATTESTED | Human-validated ground truth inputs |
| **Roadmap phases** | L3-SPECULATIVE | Governance review at each phase gate → L0 |
| **Service Inventory** | L1-INTERNAL → L1-ATTESTED | Status corrections validated by human review |
| **PPS v1.0 Roadmap** | SUPERSEDED | Replaced by this document; retained for audit trail |
| **Phase 1 plan** | L3 → L0 on approval | Requires stakeholder sign-off + assumption review |

---

## 9. Assumption Register

| Assumption | Confidence | Expires | Invalidation Trigger |
|------------|------------|---------|----------------------|
| BFO/CCO ontology stable for planning horizon | 0.90 | 2026-06-01 | BFO major version change |
| Team capacity remains at ~3 contributors | 0.80 | 2026-08-01 | Team expansion or attrition |
| TagTeam remaining 20% is completion, not redesign | 0.85 | 2026-03-15 | Discovery of architectural issues in remaining work |
| HIRI spec is implementation-ready | 0.80 | 2026-04-01 | Significant spec revision needed during build |
| Fandaws remake scope is containable | 0.65 | 2026-05-01 | Scope exceeds JSON-LD + HIRI + edge-first constraints |
| Edge-canonical storage sufficient without IPFS | 0.90 | 2026-12-01 | Federation requirements emerge before Phase 4 |
| Reasoning triad shares architectural patterns | 0.70 | 2026-09-01 | AES implementation reveals no reusable patterns |
| JSON-LD canonical format is stable | 0.95 | 2027-02-01 | JSON-LD spec breaking change |

---

## References

- PPS Technical Specification v1.0.0 (`pps-core-01`)
- FNSR Service Inventory (Spec-Driven Discovery v1.1 §4–6)
- The Plot v0.1 §4 (Component Map)
- ARIADNE Process Guide v1.0
- HIRI Protocol Specification
- Fandaws v3.3
- MDRE Technical Specification v1.3

---

*The synthetic person emerges from disciplined construction, not from parallel ambition outpacing sequential foundation.*

*Identity before address. Memory before reasoning. Conscience before autonomy.*