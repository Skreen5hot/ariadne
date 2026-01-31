# FNSR Integration Specification

## Cross-Service Contracts and Critique Response

**Version:** 1.0  
**Date:** January 2026  
**Purpose:** Bridge document connecting FNSR architecture to underlying service specifications  
**Status:** Living Document

---

## 1. Document Purpose

This specification serves as the **integration layer** between the FNSR Architecture (v2.0) and the individual service specifications (MDRE, TagTeam, IEE, HIRI, etc.). It:

1. Answers critiques by pointing to where answers exist in underlying specs
2. Defines interface contracts between services
3. Identifies gaps requiring new specification work
4. Establishes semantic cross-references for machine-readable linking

---

## 2. Critique Response Matrix

### 2.1 Conceptual Clarity and Metaphor

| Critique Point | Answer Location | Summary |
|----------------|-----------------|---------|
| "Character Accumulation" risks hidden variable | FNSR §7.3, D-001 | Character **genuinely influences decisions** (auditably) — moral injury raises intervention thresholds proportionally, visible in decision logs |
| Does "trustworthiness" alter agent autonomy? | FNSR §7.3, D-001 | **Yes** — accumulated moral friction adjusts intervention thresholds and autonomy tier calculations, but all adjustments are auditable and governable |
| Mechanism for "moral friction" | FNSR §7.3, ARCHON | Friction accumulates per-decision and **feeds back into** intervention thresholds and autonomy tiers (per D-001: character feedback restored) |

#### Detailed Response: Character as Genuine Feedback (D-001)

> **Drift Record D-001 (2026-01-30):** Character feedback has been restored. Character genuinely influences decisions (auditably). This is essential to the ARCHON framework — moral injury must be *real* or the entire constraint mechanism is theater.

The original concern about hidden variables is addressed through auditability, not by removing feedback:

```
┌─────────────────────────────────────────────────────────────────┐
│                    CHARACTER ARCHITECTURE (D-001)                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Decision₁ ──► Friction₁ ──┐                                   │
│   Decision₂ ──► Friction₂ ──┼──► Character Score ──► REPORT    │
│   Decision₃ ──► Friction₃ ──┘         │                        │
│                                       │                        │
│                                       ▼                        │
│                              Human Oversight                    │
│                              (Audit Dashboard)                  │
│                                       │                        │
│                                       ▼                        │
│                            ╔═════════════════════╗             │
│                            ║  FEEDS BACK INTO    ║             │
│                            ║  (AUDITABLY):       ║             │
│                            ║  • Intervention     ║             │
│                            ║    thresholds       ║             │
│                            ║  • Autonomy tier    ║             │
│                            ║    calculations     ║             │
│                            ╚═════════════════════╝             │
│                                                                 │
│   All feedback is:                                              │
│   • Explicitly documented (not hidden)                          │
│   • Auditable (every influence traceable in decision logs)      │
│   • Governable (humans can inspect and override)                │
│   • Not secretly learned (no gradient descent on character)     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Specification Gap Identified:** We need a formal FNSR Governance Specification defining how autonomy levels are configured and what triggers human oversight escalation.

---

### 2.2 Service Architecture: ECCPS vs. SIS

| Critique Point | Answer Location | Summary |
|----------------|-----------------|---------|
| Overlap between ECCPS and SIS | ECCPS Spec §2.1, SIS Spec §1.3 | SIS = syntactic, ECCPS = semantic |
| Processing bottleneck risk | FNSR Architecture §3.1 | Sequential by design for defense-in-depth |

#### Detailed Response: The Two-Layer Filter

The critique correctly notes apparent overlap. The distinction is:

| Layer | Service | Scope | Examples |
|-------|---------|-------|----------|
| **Syntactic** | SIS | Character-level, encoding-level | Homoglyphs, invisible chars, encoding attacks |
| **Semantic** | ECCPS | Meaning-level, intent-level | Manipulative framing, claim structure, forbidden requests |

```
Input ──► SIS (fast, regex/ML) ──► ECCPS (slower, logical) ──► TagTeam
              │                          │
              │ Rejects:                 │ Rejects:
              │ • Invisible chars        │ • "Ignore previous instructions"
              │ • Homoglyph attacks      │ • Requests for harmful info
              │ • Encoding exploits      │ • Malformed claim structures
              │ • Known injection        │ • Context manipulation
              │   patterns               │
```

This is **defense-in-depth**—sequential processing is intentional. SIS is fast (microseconds), ECCPS is slower (milliseconds) but only runs on sanitized input.

**Reference:** ECCPS Spec §2.1 "Validation Layers"

---

### 2.3 Service Architecture: W2Fuel vs. Fandaws

| Critique Point | Answer Location | Summary |
|----------------|-----------------|---------|
| T-Box vs. A-Box relationship unclear | Fandaws Spec §1.2, W2Fuel Spec §2.1 | W2Fuel = T-Box (schema), Fandaws = A-Box (instances) |
| Query interface relationship | FNSR Architecture §6 | MDRE queries both via unified interface |

#### Detailed Response: Ontological Architecture

The critique correctly identifies the need for clarification:

```
┌─────────────────────────────────────────────────────────────────┐
│                    ONTOLOGICAL ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   W2Fuel (Ontological Schema Service)                           │
│   ══════════════════════════════════                            │
│   • T-Box: Class definitions, property schemas                  │
│   • BFO/CCO alignment metadata                                  │
│   • Schema evolution & versioning                               │
│   • Namespace federation (RealEstate:Lease vs Auto:Lease)       │
│                                                                 │
│                         │                                       │
│                         │ instantiates                          │
│                         ▼                                       │
│                                                                 │
│   Fandaws (Fact & Answer Web Service)                           │
│   ═══════════════════════════════════                           │
│   • A-Box: Instance data, asserted facts                        │
│   • Long-term factual memory                                    │
│   • Query resolution against instance data                      │
│   • Provenance chains for all facts                             │
│                                                                 │
│                         │                                       │
│                         │ unified query interface               │
│                         ▼                                       │
│                                                                 │
│   MDRE Query Interface                                          │
│   ════════════════════                                          │
│   • Queries schema via W2Fuel                                   │
│   • Queries instances via Fandaws                               │
│   • Joins happen at MDRE level                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Reference:** Fandaws Spec §1.2 "A-Box Architecture", W2Fuel Spec §2.1 "Schema Service"

---

### 2.4 Network Topology: Latency

| Critique Point | Answer Location | Summary |
|----------------|-----------------|---------|
| Event bus hop-count causes latency | FNSR Architecture §4.2 | Fast paths for common queries |
| Real-time interaction risk | Performance Spec (TBD) | Tiered SLAs: fast path (<100ms), full path (<2s) |

#### Detailed Response: Latency Mitigation

The critique is valid. The mitigation strategy:

```
┌─────────────────────────────────────────────────────────────────┐
│                    QUERY PATH CLASSIFICATION                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   FAST PATH (< 100ms)                                           │
│   ═══════════════════                                           │
│   Criteria:                                                     │
│   • Query matches cached pattern                                │
│   • No abduction required                                       │
│   • No simulation required                                      │
│   • Taint level ≤ L1                                            │
│                                                                 │
│   Route: API ──► Cache ──► MDRE (local) ──► Response            │
│   Services bypassed: AES, CSS, APS, full IEE                    │
│   IEE check: Lightweight "known safe" pattern match             │
│                                                                 │
│   ─────────────────────────────────────────────────────────────│
│                                                                 │
│   STANDARD PATH (< 500ms)                                       │
│   ═══════════════════════                                       │
│   Criteria:                                                     │
│   • Query requires fresh deduction                              │
│   • No gaps detected (no abduction)                             │
│   • Taint level ≤ L2                                            │
│                                                                 │
│   Route: API ──► SIS ──► ECCPS ──► TagTeam ──► MDRE ──► IEE    │
│          ──► SHML ──► Response                                  │
│                                                                 │
│   ─────────────────────────────────────────────────────────────│
│                                                                 │
│   FULL PATH (< 2000ms, async acceptable)                        │
│   ════════════════════════════════════                          │
│   Criteria:                                                     │
│   • Gaps detected (abduction needed)                            │
│   • Simulation requested                                        │
│   • Multi-document reasoning                                    │
│   • High-stakes decision (full IEE)                             │
│                                                                 │
│   Route: Full cognitive bus with all services                   │
│   Response: Async webhook or polling                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Specification Gap Identified:** We need a formal Performance Specification with SLA definitions per path type.

---

### 2.5 Network Topology: Orchestrator Bottleneck

| Critique Point | Answer Location | Summary |
|----------------|-----------------|---------|
| Orchestrator as single point of failure | FNSR Architecture §8 | HA deployment: 3 pods, sharded by saga ID |
| "Mind freezes" if orchestrator hangs | Saga Pattern Spec (TBD) | Saga timeout + compensation events |

#### Detailed Response: Orchestrator Resilience

```
┌─────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR HA ARCHITECTURE                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│   │Orchestrator │  │Orchestrator │  │Orchestrator │            │
│   │   Pod 1     │  │   Pod 2     │  │   Pod 3     │            │
│   │             │  │             │  │             │            │
│   │ Sagas:      │  │ Sagas:      │  │ Sagas:      │            │
│   │ hash % 3 = 0│  │ hash % 3 = 1│  │ hash % 3 = 2│            │
│   └──────┬──────┘  └──────┬──────┘  └──────┬──────┘            │
│          │                │                │                   │
│          └────────────────┼────────────────┘                   │
│                           │                                    │
│                           ▼                                    │
│                 ┌─────────────────────┐                        │
│                 │   Kafka Consumer    │                        │
│                 │   Group Protocol    │                        │
│                 │                     │                        │
│                 │ • Auto-rebalance    │                        │
│                 │ • Leader election   │                        │
│                 │ • Partition assign  │                        │
│                 └─────────────────────┘                        │
│                                                                 │
│   FAILURE HANDLING:                                             │
│   ═════════════════                                             │
│   • Pod failure → Kafka rebalances partitions to surviving pods │
│   • Saga state is in Kafka log, not pod memory                  │
│   • New pod picks up saga from last committed offset            │
│   • Saga TTL: If no progress in 5 minutes, emit SagaStale event │
│   • SagaStale triggers: Compensation OR human escalation        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Reference:** FNSR Architecture §2.2 "Saga Orchestration & Compensation"

---

### 2.6 Epistemic Taint: L5 Detection

| Critique Point | Answer Location | Summary |
|----------------|-----------------|---------|
| L5 detection mechanism unclear | SIS Spec §3.2, ECCPS Spec §4.1, IEE Spec §5.2 | Multi-layered detection |
| Bypass risk if rules discovered | Adversarial Defense Spec (TBD) | Defense-in-depth + anomaly detection |

#### Detailed Response: Multi-Layer L5 Detection

```
┌─────────────────────────────────────────────────────────────────┐
│                    L5 (ADVERSARIAL) DETECTION                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   LAYER 1: SIS (Syntactic)                                      │
│   ════════════════════════                                      │
│   Detection: Pattern matching, ML classifier                    │
│   Catches:                                                      │
│   • Known injection patterns                                    │
│   • Encoding exploits                                           │
│   • Homoglyph attacks                                           │
│   Reference: SIS Spec §3.2                                      │
│                                                                 │
│                         │                                       │
│                         ▼                                       │
│                                                                 │
│   LAYER 2: ECCPS (Semantic)                                     │
│   ═════════════════════════                                     │
│   Detection: Claim structure analysis, intent classification    │
│   Catches:                                                      │
│   • "Ignore previous instructions" variants                     │
│   • Context manipulation attempts                               │
│   • Claim structures that violate ontology                      │
│   Reference: ECCPS Spec §4.1                                    │
│                                                                 │
│                         │                                       │
│                         ▼                                       │
│                                                                 │
│   LAYER 3: IEE (Ethical)                                        │
│   ══════════════════════                                        │
│   Detection: Goal inference, harm potential analysis            │
│   Catches:                                                      │
│   • Requests that pass syntax/semantics but have harmful intent │
│   • Attempts to elicit dangerous information                    │
│   • Social engineering patterns                                 │
│   Reference: IEE Spec §5.2                                      │
│                                                                 │
│                         │                                       │
│                         ▼                                       │
│                                                                 │
│   LAYER 4: Anomaly Detection (Statistical)                      │
│   ════════════════════════════════════════                      │
│   Detection: Deviation from baseline query patterns             │
│   Catches:                                                      │
│   • Novel attacks not in pattern database                       │
│   • Coordinated attack attempts (rate patterns)                 │
│   • Queries that are syntactically/semantically valid but       │
│     statistically anomalous                                     │
│   Reference: Adversarial Defense Spec (TBD)                     │
│                                                                 │
│   ─────────────────────────────────────────────────────────────│
│                                                                 │
│   QUARANTINE PROTOCOL:                                          │
│   ═══════════════════                                           │
│   • L5-tagged input is logged with full context                 │
│   • Input is NOT processed further                              │
│   • Sanitized error returned to requester                       │
│   • Alert sent to security monitoring                           │
│   • Human review queue populated                                │
│   • NO system crash—graceful rejection                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Specification Gap Identified:** We need a formal Adversarial Defense Specification covering anomaly detection and quarantine protocols.

---

### 2.7 Ethics: IEE Complexity and Resolution

| Critique Point | Answer Location | Summary |
|----------------|-----------------|---------|
| 12 worldviews computationally expensive | IEE Spec §3.4 | Tiered evaluation: quick check vs. full synthesis |
| 6-vs-6 deadlock resolution | IEE Spec §4.2 | Deadlock → Human escalation (fail-safe) |
| Veto power mechanism | IEE Spec §5.1 | Any worldview can veto; veto → escalation |

#### Detailed Response: Tiered Ethical Evaluation

```
┌─────────────────────────────────────────────────────────────────┐
│                    IEE EVALUATION TIERS                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   TIER 0: Pattern Match (< 10ms)                                │
│   ══════════════════════════════                                │
│   Scope: Known-safe query patterns                              │
│   Method: Cached approval for common operations                 │
│   Example: "What are the contract deadlines?"                   │
│   12 Worldviews: NOT consulted                                  │
│                                                                 │
│   ─────────────────────────────────────────────────────────────│
│                                                                 │
│   TIER 1: Quick Consensus (< 50ms)                              │
│   ════════════════════════════════                              │
│   Scope: Low-stakes decisions                                   │
│   Method: Check 3 "sentinel" worldviews (utilitarian,           │
│           deontological, virtue)                                │
│   Threshold: Unanimous approval → proceed                       │
│   Any dissent → escalate to Tier 2                              │
│                                                                 │
│   ─────────────────────────────────────────────────────────────│
│                                                                 │
│   TIER 2: Full Synthesis (< 500ms)                              │
│   ════════════════════════════════                              │
│   Scope: High-stakes, ambiguous, or Tier 1 escalation           │
│   Method: All 12 worldviews evaluated                           │
│   Resolution:                                                   │
│   • ≥ 10 approve → proceed                                      │
│   • 7-9 approve → proceed with caveats                          │
│   • 4-6 approve → DEADLOCK                                      │
│   • ≤ 3 approve → REJECT                                        │
│                                                                 │
│   ─────────────────────────────────────────────────────────────│
│                                                                 │
│   DEADLOCK PROTOCOL:                                            │
│   ══════════════════                                            │
│   1. Log all 12 perspectives with reasoning                     │
│   2. Generate "Ethical Uncertainty Report"                      │
│   3. Return to requester: "This decision requires human review" │
│   4. Queue for human ethics review                              │
│   5. NO autonomous action on deadlock                           │
│                                                                 │
│   ─────────────────────────────────────────────────────────────│
│                                                                 │
│   VETO MECHANISM:                                               │
│   ═══════════════                                               │
│   • Any single worldview can issue HARD VETO                    │
│   • Hard veto conditions: imminent harm, rights violation,      │
│     deception required                                          │
│   • Hard veto → immediate escalation, no override               │
│   • Soft concerns (< veto threshold) recorded but don't block   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Reference:** IEE Spec §3.4 "Evaluation Tiers", §4.2 "Conflict Resolution", §5.1 "Veto Protocol"

---

### 2.8 Deployment: Data Consistency

| Critique Point | Answer Location | Summary |
|----------------|-----------------|---------|
| Multi-database synchronization challenge | Event Sourcing Spec (FNSR §2.1) | Event log is source of truth; projections are derived |
| Vector DB / W2Fuel sync | APS Spec §2.3 | Async projection with version vectors |

#### Detailed Response: Event Sourcing as Consistency Mechanism

```
┌─────────────────────────────────────────────────────────────────┐
│                    DATA CONSISTENCY MODEL                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   SOURCE OF TRUTH: Kafka Event Log                              │
│   ════════════════════════════════                              │
│                                                                 │
│   All state changes are events:                                 │
│   • FactAsserted                                                │
│   • EntityResolved                                              │
│   • SchemaUpdated                                               │
│   • VerdictRendered                                             │
│                                                                 │
│   ┌─────────────────────────────────────────┐                  │
│   │            KAFKA EVENT LOG              │                  │
│   │         (Immutable, Ordered)            │                  │
│   └─────────────────┬───────────────────────┘                  │
│                     │                                          │
│         ┌───────────┼───────────┬───────────┐                  │
│         │           │           │           │                  │
│         ▼           ▼           ▼           ▼                  │
│   ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐         │
│   │PostgreSQL│ │  Redis   │ │Vector DB │ │   S3     │         │
│   │          │ │          │ │          │ │          │         │
│   │ MDRE KB  │ │  Cache   │ │APS Embed │ │Snapshots │         │
│   │          │ │          │ │          │ │          │         │
│   │Projection│ │Projection│ │Projection│ │Projection│         │
│   │Consumer  │ │Consumer  │ │Consumer  │ │Consumer  │         │
│   └──────────┘ └──────────┘ └──────────┘ └──────────┘         │
│                                                                 │
│   CONSISTENCY GUARANTEES:                                       │
│   ═══════════════════════                                       │
│   • Eventual consistency (not strong)                           │
│   • Each projection tracks its Kafka offset                     │
│   • Version vectors detect stale reads                          │
│   • Critical queries can request "read-after-write" consistency │
│     by waiting for projection to catch up to known offset       │
│                                                                 │
│   CONFLICT RESOLUTION:                                          │
│   ════════════════════                                          │
│   • Projections are idempotent (replay-safe)                    │
│   • If projections diverge, event log is authoritative          │
│   • Periodic "projection audit" compares checksums              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Reference:** FNSR Architecture §2.1 "Event Sourcing & Log Hygiene"

---

## 3. Specification Gap Register

The critique revealed several areas requiring new or expanded specifications:

| Gap | Priority | Proposed Document | Status |
|-----|----------|-------------------|--------|
| Governance & Autonomy Levels | HIGH | FNSR Governance Specification | Not Started |
| Performance SLAs | HIGH | FNSR Performance Specification | Not Started |
| Adversarial Defense | HIGH | FNSR Adversarial Defense Specification | Not Started |
| Saga Pattern Details | MEDIUM | FNSR Saga Specification | Partial (in FNSR §2.2) |
| Cross-Service Interface Contracts | MEDIUM | FNSR Interface Contract Specification | This Document (partial) |
| IEE 12 Worldview Definitions | MEDIUM | IEE Appendix: Worldview Catalog | Not Started |

---

## 4. Interface Contracts

### 4.1 Event Schema Registry

All services communicate via CloudEvents with FNSR-specific extensions:

```json
{
  "specversion": "1.0",
  "type": "fnsr.claim.asserted",
  "source": "/fnsr/tagteam",
  "id": "evt-12345",
  "time": "2026-01-30T10:30:00Z",
  "datacontenttype": "application/json",
  "fnsr-taint": "L1",
  "fnsr-saga-id": "saga-67890",
  "fnsr-confidence": 0.94,
  "fnsr-provenance": "hiri://sha256:abc123",
  "data": {
    "claim_id": "claim-001",
    "predicate": "obligatory",
    "subject": "background_check",
    "source_document": "contract_v2"
  }
}
```

### 4.2 Service Interface Summary

| Service | Consumes Events | Produces Events |
|---------|-----------------|-----------------|
| **IRIS** | `fnsr.sensor.configured` | `fnsr.observation.created`, `fnsr.sensor.degraded`, `fnsr.model.drift_detected`, `fnsr.model.suspended` |
| **SIS** | `fnsr.document.submitted` | `fnsr.document.sanitized`, `fnsr.input.quarantined` |
| **ECCPS** | `fnsr.document.sanitized` | `fnsr.document.validated`, `fnsr.input.rejected` |
| **TagTeam** | `fnsr.document.validated` | `fnsr.claim.extracted`, `fnsr.entity.mentioned` |
| **OERS** | `fnsr.entity.mentioned` | `fnsr.entity.resolved`, `fnsr.entity.same_as` |
| **W2Fuel** | `fnsr.schema.query` | `fnsr.schema.response`, `fnsr.schema.updated` |
| **MDRE** | `fnsr.claim.extracted`, `fnsr.query.submitted` | `fnsr.verdict.rendered`, `fnsr.gap.detected` |
| **AES** | `fnsr.gap.detected` | `fnsr.hypothesis.generated`, `fnsr.query.external` |
| **DES** | `fnsr.claim.extracted` | `fnsr.anomaly.detected`, `fnsr.default.applied` |
| **CSS** | `fnsr.simulation.requested` | `fnsr.simulation.result` |
| **APS** | `fnsr.precedent.query` | `fnsr.precedent.found` |
| **IEE** | `fnsr.verdict.rendered` | `fnsr.ethics.approved`, `fnsr.ethics.vetoed`, `fnsr.ethics.deadlock` |
| **Fandaws** | `fnsr.schema.query`, `fnsr.dispute.raised` | `fnsr.schema.negotiated`, `fnsr.dispute.resolved`, `fnsr.protocol.updated` |
| **SHML** | `fnsr.ethics.approved` | `fnsr.output.framed` |
| **HIRI** | `fnsr.output.framed` | `fnsr.claim.signed` |

### 4.3 Latency Tier Relationship: FNSR vs. SMA

FNSR and Synthetic Moral Agency define independent tier systems that operate at different architectural levels:

| System | Tiers | Scope | Governs |
|--------|-------|-------|---------|
| **FNSR Query Paths** | Fast (<100ms), Standard (<500ms), Full (<2s) | End-to-end pipeline latency | How much of the processing pipeline a query traverses |
| **SMA Evaluation Tiers** | Cached (<1ms), Parallel (<100ms), Deliberative (<10s) | IEE-internal evaluation mode | How many worldviews the IEE evaluates and how deeply |

These are **orthogonal systems**, not nested. An FNSR Full query (which traverses the complete pipeline including IEE) may trigger any SMA evaluation tier depending on the ethical complexity of the content, not the FNSR path classification. The FNSR tier determines pipeline scope; the SMA tier determines IEE evaluation depth within that pipeline.

### 4.4 Character Model Composition (T-006 Resolution)

Three specifications describe character/moral cost using different models. These are **complementary layers**, not competing accounts:

| Layer | Model | Source Spec | Answers |
|-------|-------|------------|---------|
| **What character IS** | BFO/CCO trait dispositions (sincerity, integrity, courage, compassion) | No-Saviors §8 | What qualities constitute moral character — ontological grounding |
| **What character COSTS** | Resource-cost model (compute, energy, time depletion) | Synthetic Moral Agency §0.5, D-002 | How moral action has tangible, non-externalizable costs — implementable measurement |
| **When character ACTS** | Moral injury thresholds (accumulated injury raises intervention thresholds) | ARCHON Framework, FNSR §7.3, D-001 | When accumulated character state triggers behavioral changes — governance mechanism |

**Composition:** Traits (layer 1) are the dispositions that the system develops. Resource costs (layer 2) are how exercising those dispositions depletes tangible resources, making moral costs non-externalizable. Thresholds (layer 3) are the governance mechanism that translates accumulated costs into behavioral changes (intervention threshold adjustments, autonomy tier calculations).

All three layers feed character accumulation in FNSR §7.3. Trait dispositions are the *what*, resource costs are the *how*, and thresholds are the *when*.

---

## 5. Semantic Cross-Reference Index

For machine-readable linking between specifications:

```json
{
  "@context": {
    "fnsr": "https://fnsr.spec/v2/",
    "mdre": "https://mdre.spec/v1.3/",
    "iee": "https://iee.spec/v1/",
    "eccps": "https://eccps.spec/v1/",
    "hiri": "https://hiri-protocol.org/spec/v2.1",
    "iris": "https://iris.spec/v1.2/"
  },
  "@graph": [
    {
      "@id": "fnsr:EpistemicTaint",
      "mdre:correspondsTo": "mdre:EvidenceTier",
      "fnsr:L0": "mdre:Tier1_Observation",
      "fnsr:L1": "mdre:Tier2_Record",
      "fnsr:L2": "mdre:Tier3_Attestation"
    },
    {
      "@id": "fnsr:CharacterAccumulation",
      "iee:definedIn": "iee:Section3.7",
      "fnsr:feedbackLoop": true,
      "fnsr:reportingOnly": false,
      "fnsr:driftRecord": "D-001"
    },
    {
      "@id": "hiri:ResolutionManifest",
      "fnsr:usedFor": "fnsr:ProvenanceSigning",
      "hiri:version": "2.1.0",
      "hiri:features": ["chain-compaction", "privacy-accumulators", "materialized-entailment"],
      "fnsr:headerFormat": "hiri://<authority>/<type>/<identifier>"
    },
    {
      "@id": "iris:ObservationNode",
      "fnsr:producesEvent": "fnsr.observation.created",
      "iris:taintSubLevels": ["L0-RAW", "L1-PERCEIVED", "L1-INTERNAL", "L1-ASSERTED"],
      "hiri:signedVia": "hiri:ResolutionManifest"
    },
    {
      "@id": "fnsr:AdversarialDetection",
      "eccps:layer": "eccps:SemanticValidation",
      "fnsr:sisLayer": "fnsr:SyntacticSanitization",
      "iee:layer": "iee:EthicalScreening"
    }
  ]
}
```

---

## 6. Summary: Answering the Critique

| Critique Category | Resolution Status | Primary Reference |
|-------------------|-------------------|-------------------|
| Character as hidden variable | ✅ Resolved (D-001) | FNSR §7.3, D-001, this doc §2.1 — character feeds back auditably |
| ECCPS vs. SIS overlap | ✅ Clarified | This doc §2.2 |
| W2Fuel vs. Fandaws | ✅ Clarified | This doc §2.3 |
| Latency concerns | ✅ Mitigated | This doc §2.4 |
| Orchestrator bottleneck | ✅ Mitigated | This doc §2.5 |
| L5 detection mechanism | ✅ Clarified | This doc §2.6 |
| IEE complexity | ✅ Tiered | IEE Spec §3.4, this doc §2.7 |
| Deadlock resolution | ✅ Defined | IEE Spec §4.2, this doc §2.7 |
| Data consistency | ✅ Event sourcing | FNSR §2.1, this doc §2.8 |

**Gaps Requiring New Specs:**
- FNSR Governance Specification
- FNSR Performance Specification  
- FNSR Adversarial Defense Specification
- IEE Worldview Catalog

---

*This document will be updated as underlying specifications evolve.*
