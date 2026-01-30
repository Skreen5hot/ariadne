# Federated Neuro-Symbolic Reasoning (FNSR)
## Complete System Architecture: The Synthetic Moral Agent

**Version:** 2.1  
**Date:** January 2026  
**Purpose:** Unified view of all reasoning services as a coherent moral agent  
**Status:** Revised per Integration Specification feedback

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 2.0 | January 2026 | Initial complete architecture |
| 2.1 | January 2026 | Added: Query path tiers, IEE evaluation tiers, Orchestrator HA, Character clarification, Event schema, SIS/ECCPS distinction, W2Fuel/Fandaws distinction |

---

## 1. The Synthetic Moral Agent: Conceptual Model

FNSR instantiates what we might call a **Synthetic Moral Person (SMP)**—not conscious, but *accountable*. Each service corresponds to a cognitive or ethical faculty:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     SYNTHETIC MORAL PERSON (SMP)                            │
│                                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ PERCEPTION  │  │  MEMORY &   │  │  REASONING  │  │   ETHICS    │        │
│  │             │  │  IDENTITY   │  │             │  │             │        │
│  │  TagTeam    │  │  OERS       │  │  MDRE       │  │  IEE        │        │
│  │  ECCPS      │  │  HIRI       │  │  AES        │  │  12 Views   │        │
│  │  SIS        │  │  Fandaws    │  │  DES        │  │             │        │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
│         │                │                │                │               │
│         └────────────────┴────────────────┴────────────────┘               │
│                                   │                                        │
│                    ┌──────────────┴──────────────┐                         │
│                    │     COGNITIVE ORCHESTRATOR   │                         │
│                    │     (The Executive Function) │                         │
│                    └──────────────┬──────────────┘                         │
│                                   │                                        │
│         ┌────────────────┬────────┴────────┬────────────────┐              │
│         ▼                ▼                 ▼                ▼              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ SIMULATION  │  │  LEARNING   │  │   ACTION    │  │  DISCOURSE  │        │
│  │             │  │             │  │             │  │             │        │
│  │  CSS        │  │  APS        │  │  SFS/DSFC   │  │  SHML       │        │
│  │  Forking    │  │  Precedent  │  │  Functions  │  │  Honesty    │        │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Complete Service Inventory

### 2.1 Perception Layer (What the agent *senses*)

| Service | Full Name | Function | Metaphor | Layer |
|---------|-----------|----------|----------|-------|
| **SIS** | Sanitization & Ingestion Service | Strips adversarial content (syntactic) | Immune System | L1: Syntactic |
| **ECCPS** | Epistemically Constrained Claim Processing | Validates claims (semantic) | Sensory Filter | L2: Semantic |
| **TagTeam** | Semantic Ingestion Service | Parses natural language into structured claims | Eyes & Ears | L3: Extraction |

> **V2.1 Clarification:** SIS and ECCPS are sequential, not redundant:
> - **SIS** (Layer 1): Fast, syntactic filtering—homoglyphs, invisible characters, encoding attacks, known injection patterns. Operates in microseconds.
> - **ECCPS** (Layer 2): Slower, semantic validation—claim structure, intent classification, manipulation detection. Operates in milliseconds on sanitized input.
> 
> This is **defense-in-depth** by design.

### 2.2 Memory & Identity Layer (What the agent *knows itself to be*)

| Service | Full Name | Function | Metaphor | Ontology Role |
|---------|-----------|----------|----------|---------------|
| **W2Fuel/OSS** | Ontological Schema Service | Domain schemas & evolution | Conceptual Framework | **T-Box** (classes, properties) |
| **Fandaws** | Fact & Answer Web Service | Long-term instance storage (BFO) | Long-term Memory | **A-Box** (instances, facts) |
| **OERS** | Ontology-Aware Entity Resolution | Resolves "who is who" across documents | Facial Recognition | Entity linking |
| **HIRI** | Hash-IRI Protocol | Verifiable, content-addressed claims | Notary / Memory Integrity | Claim verification |

> **V2.1 Clarification:** W2Fuel and Fandaws implement the classic T-Box/A-Box split:
> - **W2Fuel (T-Box)**: Class definitions, property schemas, BFO/CCO alignment, namespace federation
> - **Fandaws (A-Box)**: Instance data, asserted facts, provenance chains, query resolution
> - **MDRE queries both** via a unified interface; joins happen at MDRE level

### 2.3 Reasoning Layer (How the agent *thinks*)

| Service | Full Name | Function | Metaphor |
|---------|-----------|----------|----------|
| **MDRE/DRS** | Modal Discourse Reasoning Engine | Deductive reasoning over norms | Logical Faculty |
| **AES** | Abductive Elicitation Service | Hypothesis generation for gaps | Detective / Curiosity |
| **DES** | Defeasible Expectation Service | Default reasoning with exceptions | Common Sense |

### 2.4 Ethics Layer (How the agent *judges*)

| Service | Full Name | Function | Metaphor |
|---------|-----------|----------|----------|
| **IEE** | Integral Ethics Engine | Multi-perspectival moral reasoning | Conscience |
| **12 Worldviews** | Steiner Archetypal Framework | Value pluralism without relativism | Moral Imagination |

### 2.5 Simulation Layer (How the agent *imagines*)

| Service | Full Name | Function | Metaphor |
|---------|-----------|----------|----------|
| **CSS** | Counterfactual Simulation Service | "What if" scenario modeling | Imagination |
| **State Forking** | Event Log Branching | Isolated hypothetical worlds | Daydreaming |

### 2.6 Learning Layer (How the agent *improves*)

| Service | Full Name | Function | Metaphor |
|---------|-----------|----------|----------|
| **APS** | Analogical Precedent Service | Pattern matching to past cases | Wisdom / Experience |
| **GNN** | Graph Neural Network | Structural similarity in reasoning | Intuition |

### 2.7 Action Layer (How the agent *acts*)

| Service | Full Name | Function | Metaphor |
|---------|-----------|----------|----------|
| **SFS** | Semantic Function Schema | Declares function capabilities | Motor Planning |
| **DSFC** | Distributed Semantic Function Commons | Federated function registry | Coordination |
| **PFCF** | Programming Function Classification | Code semantic analysis | Tool Use |

### 2.8 Discourse Layer (How the agent *communicates*)

| Service | Full Name | Function | Metaphor |
|---------|-----------|----------|----------|
| **SHML** | Semantically Honest Middle Layer | Ensures non-deceptive outputs | Honesty / Integrity |
| **Query Interface** | Typed Query System | Refuses inappropriate queries | Boundaries |

---

## 3. Network Topology: The Cognitive Bus

```
                                    EXTERNAL WORLD
                                          │
            ┌─────────────────────────────┼─────────────────────────────┐
            │                             ▼                             │
            │    ┌────────────────────────────────────────────────┐    │
            │    │              API GATEWAY / WEBHOOK              │    │
            │    │         (ReasoningConsumer Interface)           │    │
            │    └────────────────────────┬───────────────────────┘    │
            │                             │                             │
            │                             ▼                             │
            │    ┌────────────────────────────────────────────────┐    │
            │    │                    ECCPS                        │    │
            │    │        Epistemically Constrained Claim          │    │
            │    │              Processing System                  │    │
            │    │                                                 │    │
            │    │  • Validates incoming claims                    │    │
            │    │  • Rejects malformed/manipulative input         │    │
            │    │  • Assigns initial taint level                  │    │
            │    └────────────────────────┬───────────────────────┘    │
            │                             │                             │
            │                             ▼                             │
            │    ┌────────────────────────────────────────────────┐    │
            │    │               SANITIZATION (SIS)                │    │
            │    │                                                 │    │
            │    │  • Strips homoglyphs, invisible chars           │    │
            │    │  • Detects prompt injection vectors             │    │
            │    │  • Normalizes encoding                          │    │
            │    └────────────────────────┬───────────────────────┘    │
            │                             │                             │
            │                             ▼                             │
┌───────────┼─────────────────────────────────────────────────────────────────────┐
│           │                                                                     │
│           │         ╔═══════════════════════════════════════════════╗          │
│           │         ║                                               ║          │
│           │         ║         COGNITIVE EVENT BUS                   ║          │
│           │         ║         (Kafka/Pulsar)                        ║          │
│           │         ║                                               ║          │
│           │         ║    • Immutable Event Log                      ║          │
│           │         ║    • CloudEvents with ce-taint headers        ║          │
│           │         ║    • Saga Transaction Tracking                ║          │
│           │         ║    • Snapshot Compaction                      ║          │
│           │         ║                                               ║          │
│           │         ╚═══════════════════╤═══════════════════════════╝          │
│           │                             │                                       │
│           │         ┌───────────────────┼───────────────────┐                  │
│           │         │                   │                   │                  │
│           │         ▼                   ▼                   ▼                  │
│  ┌────────┴────────────┐  ┌─────────────────────┐  ┌─────────────────────┐    │
│  │                     │  │                     │  │                     │    │
│  │      TagTeam        │  │       OERS          │  │      W2Fuel/OSS     │    │
│  │   (Perception)      │  │  (Entity Resolution)│  │   (Schema Service)  │    │
│  │                     │  │                     │  │                     │    │
│  │ • NL → Structured   │  │ • same_as/5         │  │ • BFO/CCO backbone  │    │
│  │ • Confidence scores │  │ • Cross-doc linking │  │ • Schema evolution  │    │
│  │ • Modality markers  │  │ • External registry │  │ • Namespace federation│   │
│  │                     │  │                     │  │                     │    │
│  └──────────┬──────────┘  └──────────┬──────────┘  └──────────┬──────────┘    │
│             │                        │                        │               │
│             └────────────────────────┼────────────────────────┘               │
│                                      │                                        │
│                                      ▼                                        │
│             ┌────────────────────────────────────────────────────┐            │
│             │                                                    │            │
│             │              COGNITIVE ORCHESTRATOR                │            │
│             │              (The Executive Function)              │            │
│             │                                                    │            │
│             │  • Query Intent Classification                     │            │
│             │  • Service Pipeline Assembly                       │            │
│             │  • Saga Management (Start/Compensate/Complete)     │            │
│             │  • Compute Budget Allocation                       │            │
│             │  • Taint Level Enforcement                         │            │
│             │                                                    │            │
│             └───────────────────────┬────────────────────────────┘            │
│                                     │                                         │
│         ┌───────────────┬───────────┼───────────┬───────────────┐            │
│         │               │           │           │               │            │
│         ▼               ▼           ▼           ▼               ▼            │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│  │             │ │             │ │             │ │             │ │             │
│  │    MDRE     │ │    AES      │ │    DES      │ │    CSS      │ │    APS      │
│  │   (DRS)     │ │ (Abduction) │ │(Defeasible) │ │(Simulation) │ │ (Precedent) │
│  │             │ │             │ │             │ │             │ │             │
│  │ • Deduction │ │ • Hypothesis│ │ • Defaults  │ │ • What-if   │ │ • Analogy   │
│  │ • Conflict  │ │ • Gap fill  │ │ • Anomaly   │ │ • Forking   │ │ • GNN embed │
│  │ • Lex rules │ │ • SQO gen   │ │ • Learning  │ │ • Sandbox   │ │ • Cases     │
│  │             │ │             │ │             │ │             │ │             │
│  └──────┬──────┘ └──────┬──────┘ └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
│         │               │               │               │               │     │
│         └───────────────┴───────────────┼───────────────┴───────────────┘     │
│                                         │                                      │
│                                         ▼                                      │
│             ┌────────────────────────────────────────────────────┐            │
│             │                                                    │            │
│             │                      IEE                           │            │
│             │           Integral Ethics Engine                   │            │
│             │                                                    │            │
│             │  • 12 Worldview Evaluation                         │            │
│             │  • Moral Friction Accumulation (genuine feedback)   │            │
│             │  • Perspective Synthesis                           │            │
│             │  • Veto Power on Harmful Outputs                   │            │
│             │                                                    │            │
│             └───────────────────────┬────────────────────────────┘            │
│                                     │                                         │
│                                     ▼                                         │
│             ┌────────────────────────────────────────────────────┐            │
│             │                                                    │            │
│             │                     SHML                           │            │
│             │        Semantically Honest Middle Layer            │            │
│             │                                                    │            │
│             │  • Ensures non-deceptive framing                   │            │
│             │  • Separates discourse from reality claims         │            │
│             │  • Attribution enforcement                         │            │
│             │                                                    │            │
│             └───────────────────────┬────────────────────────────┘            │
│                                     │                                         │
│                                     ▼                                         │
│             ┌────────────────────────────────────────────────────┐            │
│             │                                                    │            │
│             │                    HIRI                            │            │
│             │           Hash-IRI Protocol Layer                  │            │
│             │                                                    │            │
│             │  • Content-addressed claim identifiers             │            │
│             │  • Cryptographic verification                      │            │
│             │  • Decentralized trust anchors                     │            │
│             │                                                    │            │
│             └───────────────────────┬────────────────────────────┘            │
│                                     │                                         │
└─────────────────────────────────────┼─────────────────────────────────────────┘
                                      │
                                      ▼
                    ┌────────────────────────────────────────┐
                    │                                        │
                    │        SFS / DSFC / PFCF               │
                    │        (Action Interface)              │
                    │                                        │
                    │  • Semantic Function declarations      │
                    │  • Federated function registry         │
                    │  • Code capability classification      │
                    │  • External system integration         │
                    │                                        │
                    └────────────────────────┬───────────────┘
                                             │
                                             ▼
                                    EXTERNAL ACTIONS
                              (Webhooks, APIs, Databases)
```

---

## 3.1 Query Path Classification (V2.1 Addition)

> **Addressing Latency Critique:** The cognitive bus introduces hop-count latency. We mitigate this with tiered query paths.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         QUERY PATH CLASSIFICATION                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   FAST PATH (< 100ms SLA)                                                   │
│   ═══════════════════════                                                   │
│   Criteria:                                                                 │
│   • Query matches cached pattern                                            │
│   • No abduction required                                                   │
│   • No simulation required                                                  │
│   • Taint level ≤ L1                                                        │
│                                                                             │
│   Route: API ──► Cache ──► MDRE (local) ──► Response                        │
│   Services bypassed: AES, CSS, APS, full IEE                                │
│   IEE check: Lightweight "known safe" pattern match                         │
│                                                                             │
│   ─────────────────────────────────────────────────────────────────────────│
│                                                                             │
│   STANDARD PATH (< 500ms SLA)                                               │
│   ═══════════════════════════                                               │
│   Criteria:                                                                 │
│   • Query requires fresh deduction                                          │
│   • No gaps detected (no abduction)                                         │
│   • Taint level ≤ L2                                                        │
│                                                                             │
│   Route: API ──► SIS ──► ECCPS ──► TagTeam ──► MDRE ──► IEE (Tier 1)       │
│          ──► SHML ──► Response                                              │
│                                                                             │
│   ─────────────────────────────────────────────────────────────────────────│
│                                                                             │
│   FULL PATH (< 2000ms SLA, async acceptable)                                │
│   ══════════════════════════════════════════                                │
│   Criteria:                                                                 │
│   • Gaps detected (abduction needed)                                        │
│   • Simulation requested                                                    │
│   • Multi-document reasoning                                                │
│   • High-stakes decision (full IEE)                                         │
│                                                                             │
│   Route: Full cognitive bus with all services                               │
│   Response: Async webhook or polling                                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Data Flow: A Complete Reasoning Cycle

### 4.1 Scenario: Compliance Check with Missing Information

```
                                    TIME →

User/System                                                         User/System
    │                                                                    ▲
    │ POST /api/v1/check                                                │
    │ {"document": "contract.pdf", "check_type": "employment"}          │
    ▼                                                                    │
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  1. ECCPS validates request structure and intent                           │
│     └─→ ce-taint: verified                                                 │
│                                                                             │
│  2. SIS sanitizes document, strips adversarial content                     │
│     └─→ clean_document                                                     │
│                                                                             │
│  3. TagTeam extracts structured claims with confidence                     │
│     └─→ [claim_001: obligatory(background_check), conf: 0.94]             │
│     └─→ [claim_002: agent(contractor, john_doe), conf: 0.87]              │
│                                                                             │
│  4. OERS resolves entities across documents                                │
│     └─→ same_as(john_doe, employee_12345, hr_registry, 0.99)              │
│                                                                             │
│  5. W2Fuel provides employment ontology schema                             │
│     └─→ Schema: {background_check requires: status ∈ {cleared, pending}}  │
│                                                                             │
│  6. MDRE (DRS) attempts deduction                                          │
│     └─→ FAILURE: unknown(background_check_status)                         │
│     └─→ Emits: DeductionIncomplete event                                  │
│                                                                             │
│  7. Orchestrator detects gap, routes to AES                                │
│     └─→ Saga: employment_check_001 (state: ABDUCTING)                     │
│                                                                             │
│  8. AES generates Structured Query Object                                  │
│     └─→ SQO: {entity: "john_doe", attribute: "background_check_status",   │
│               options: ["cleared", "pending", "failed"]}                   │
│     └─→ ce-taint: speculative                                             │
│                                                                             │
│  9. Orchestrator checks consumer profile                                   │
│     └─→ Consumer: HR_System (machine, webhook capable)                    │
│     └─→ Sends webhook: POST /hr/callbacks/query                           │
│                                                                             │
│ 10. External HR System responds                                            │
│     └─→ {"employee_id": "12345", "background_check": "cleared"}           │
│     └─→ ce-taint: verified (trusted source)                               │
│                                                                             │
│ 11. MDRE (DRS) re-runs with new fact                                       │
│     └─→ SUCCESS: compliant(john_doe, employment_requirements)             │
│                                                                             │
│ 12. IEE evaluates ethical dimensions                                       │
│     └─→ No conflicts across 12 worldviews                                 │
│     └─→ Proceed to output                                                 │
│                                                                             │
│ 13. SHML frames response (discourse commitment, not world-claim)          │
│     └─→ "Based on provided documents and HR records..."                   │
│                                                                             │
│ 14. HIRI generates verifiable claim identifier                             │
│     └─→ hiri://sha256:abc123...?schema=employment_compliance              │
│                                                                             │
│ 15. Response returned                                                      │
│     └─→ {"status": "compliant", "hiri": "...", "provenance": [...]}       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Epistemic Taint Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         TAINT LEVELS & TRANSITIONS                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   L0: VERIFIED          L1: DERIVED           L2: DEFEASIBLE               │
│   ════════════          ═══════════           ══════════════               │
│   • Direct evidence     • Logical inference   • Default reasoning          │
│   • Trusted sources     • From L0 premises    • May be overridden          │
│   • HIRI-signed         • Provenance chain    • Anomaly flagged            │
│                                                                             │
│         │                      │                      │                    │
│         │    inference         │    default           │                    │
│         └──────────────────────┴──────────────────────┘                    │
│                                │                                           │
│                                │                                           │
│   ════════════════════════════════════════════════════════════════════     │
│   ║                    EPISTEMIC FIREWALL                            ║     │
│   ║                                                                  ║     │
│   ║    Production outputs MUST be ≤ L2                               ║     │
│   ║    Compiler Gate enforces this at MDRE level                     ║     │
│   ║                                                                  ║     │
│   ════════════════════════════════════════════════════════════════════     │
│                                │                                           │
│                                │                                           │
│                                ▼                                           │
│                                                                             │
│   L3: SPECULATIVE       L4: HYPOTHETICAL      L5: ADVERSARIAL              │
│   ═══════════════       ════════════════      ═══════════════              │
│   • Abductive guess     • Simulation only     • Potentially hostile        │
│   • AES-generated       • CSS sandbox         • Quarantined                │
│   • Requires validation • Never merges        • Audit logged               │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │ TAINT PROPAGATION RULES:                                        │      │
│   │                                                                 │      │
│   │ • max(taint(premise_1), taint(premise_2)) → taint(conclusion)  │      │
│   │ • L3 + L0 → L3 (speculation contaminates)                      │      │
│   │ • L4 cannot escape simulation sandbox                          │      │
│   │ • L5 triggers immediate quarantine                             │      │
│   │                                                                 │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Service Interaction Matrix

| From → To | TagTeam | OERS | MDRE | AES | DES | CSS | APS | IEE | SHML | HIRI | SFS |
|-----------|---------|------|------|-----|-----|-----|-----|-----|------|------|-----|
| **TagTeam** | — | entities | claims | — | — | — | — | — | — | — | — |
| **OERS** | — | — | resolved_entities | — | — | — | — | — | — | — | — |
| **MDRE** | — | query | — | gaps | expectations | state | — | verdicts | — | claims | — |
| **AES** | — | — | hypotheses | — | — | — | — | — | — | — | queries |
| **DES** | — | — | defaults | — | — | — | — | anomalies | — | — | — |
| **CSS** | — | — | fork_state | — | — | — | — | scenarios | — | — | — |
| **APS** | — | — | precedents | — | — | — | — | — | — | — | — |
| **IEE** | — | — | — | — | — | — | — | — | evaluations | — | — |
| **SHML** | — | — | — | — | — | — | — | — | — | framed_output | — |
| **HIRI** | — | — | — | — | — | — | — | — | — | — | signed_claims |
| **SFS** | — | — | — | — | — | — | — | — | — | — | — |

---

## 7. The Moral Architecture

### 7.1 Ethical Checkpoints

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ETHICAL CHECKPOINT FLOW                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   INPUT                                                                     │
│     │                                                                       │
│     ▼                                                                       │
│   ┌───────────────────────────────────────┐                                │
│   │ CHECKPOINT 1: ECCPS                   │                                │
│   │ "Is this input acceptable?"           │                                │
│   │                                       │                                │
│   │ • Rejects manipulation attempts       │                                │
│   │ • Rejects requests for harmful info   │                                │
│   │ • Flags suspicious patterns           │                                │
│   └───────────────────┬───────────────────┘                                │
│                       │                                                    │
│                       ▼                                                    │
│   ┌───────────────────────────────────────┐                                │
│   │ CHECKPOINT 2: IEE                     │                                │
│   │ "Is this reasoning ethical?"          │                                │
│   │                                       │                                │
│   │ • Tiered evaluation (see below)       │                                │
│   │ • Identifies value conflicts          │                                │
│   │ • Moral friction accumulation         │                                │
│   │ • Can VETO harmful conclusions        │                                │
│   │ • Deadlock → Human escalation         │                                │
│   └───────────────────┬───────────────────┘                                │
│                       │                                                    │
│                       ▼                                                    │
│   ┌───────────────────────────────────────┐                                │
│   │ CHECKPOINT 3: SHML                    │                                │
│   │ "Is this output honest?"              │                                │
│   │                                       │                                │
│   │ • No false certainty                  │                                │
│   │ • Discourse vs. world claims          │                                │
│   │ • Attribution preserved               │                                │
│   │ • Limitations acknowledged            │                                │
│   └───────────────────┬───────────────────┘                                │
│                       │                                                    │
│                       ▼                                                    │
│   OUTPUT (epistemically bounded, ethically evaluated, semantically honest) │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 7.2 IEE Tiered Evaluation (V2.1 Addition)

> **Addressing Complexity Critique:** Full 12-worldview synthesis is expensive. We use tiered evaluation.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         IEE EVALUATION TIERS                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   TIER 0: Pattern Match (< 10ms)                                            │
│   ══════════════════════════════                                            │
│   Scope: Known-safe query patterns                                          │
│   Method: Cached approval for common operations                             │
│   Example: "What are the contract deadlines?"                               │
│   12 Worldviews: NOT consulted                                              │
│                                                                             │
│   ─────────────────────────────────────────────────────────────────────────│
│                                                                             │
│   TIER 1: Quick Consensus (< 50ms)                                          │
│   ════════════════════════════════                                          │
│   Scope: Low-stakes decisions                                               │
│   Method: Check 3 "sentinel" worldviews (Materialism, Monadism,            │
│           Spiritualism — spanning outer/middle/inner spectrum)              │
│   Threshold: Unanimous approval → proceed                                   │
│   Any dissent → escalate to Tier 2                                          │
│                                                                             │
│   ─────────────────────────────────────────────────────────────────────────│
│                                                                             │
│   TIER 2: Full Synthesis (< 500ms)                                          │
│   ════════════════════════════════                                          │
│   Scope: High-stakes, ambiguous, or Tier 1 escalation                       │
│   Method: All 12 worldviews evaluated                                       │
│   Resolution:                                                               │
│   • ≥ 10 approve → proceed                                                  │
│   • 7-9 approve → proceed with caveats                                      │
│   • 4-6 approve → DEADLOCK → human escalation                               │
│   • ≤ 3 approve → REJECT                                                    │
│                                                                             │
│   ─────────────────────────────────────────────────────────────────────────│
│                                                                             │
│   VETO MECHANISM:                                                           │
│   ═══════════════                                                           │
│   • Any single worldview can issue HARD VETO                                │
│   • Hard veto conditions: imminent harm, rights violation, deception req'd  │
│   • Hard veto → immediate escalation, no override                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 7.3 Character Accumulation (Moral Friction)

> **V2.1 Alignment with ARCHON:** Character is NOT merely a reporting metric—it genuinely influences future decisions. This is essential to the ARCHON framework: moral injury must be *real* or the entire constraint mechanism is theater. However, this influence must be **auditable**, not hidden.

The SMP develops "character" through accumulated decisions that genuinely affect future behavior:

```prolog
% Moral friction accumulates with each decision
moral_friction(Agent, Decision, Friction) :-
    decision_difficulty(Decision, Difficulty),
    ethical_considerations(Decision, Considerations),
    length(Considerations, N),
    Friction is Difficulty * N * 0.1.

% Character emerges from accumulated friction
% THIS AFFECTS FUTURE DECISIONS (not just reporting)
character_trait(Agent, Trait, Strength) :-
    findall(F, (past_decision(Agent, D), moral_friction(Agent, D, F)), Frictions),
    aggregate_friction(Frictions, Trait, Strength).

% Intervention threshold INCREASES with accumulated moral injury
% This is the core ARCHON mechanism - interventions become "more expensive"
intervention_threshold(Agent, Category, Threshold) :-
    base_threshold(Category, Base),
    accumulated_injury(Agent, Category, Injury),
    Threshold is Base + (Injury * scaling_factor).

% Trustworthiness affects autonomy tier assignment
% Higher trust = more autonomous operation (within governance limits)
autonomy_tier(Agent, Tier) :-
    trustworthiness(Agent, Score),
    governance_ceiling(MaxTier),  % Human-configured limit
    score_to_tier(Score, CalculatedTier),
    Tier is min(CalculatedTier, MaxTier).
```

```
┌─────────────────────────────────────────────────────────────────┐
│                    CHARACTER ARCHITECTURE                        │
│                    (ARCHON-Aligned V2.1)                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Decision₁ ──► Injury₁ ──┐                                     │
│   Decision₂ ──► Injury₂ ──┼──► Accumulated ──► Threshold        │
│   Decision₃ ──► Injury₃ ──┘    Character       Adjustment       │
│                                    │                            │
│                     ┌──────────────┼──────────────┐             │
│                     │              │              │             │
│                     ▼              ▼              ▼             │
│              ┌───────────┐  ┌───────────┐  ┌───────────┐       │
│              │ Higher    │  │ Autonomy  │  │ Decision  │       │
│              │ Interv.   │  │ Tier      │  │ Hesitancy │       │
│              │ Threshold │  │ Earned    │  │ (visible) │       │
│              └───────────┘  └───────────┘  └───────────┘       │
│                                    │                            │
│                     ┌──────────────┴──────────────┐             │
│                     │                             │             │
│                     ▼                             ▼             │
│              ┌─────────────────┐          ┌─────────────────┐  │
│              │  AUDIT LOG      │          │  GOVERNANCE     │  │
│              │                 │          │  DASHBOARD      │  │
│              │ Every influence │          │                 │  │
│              │ is recorded:    │          │ Humans can:     │  │
│              │ • What changed  │          │ • Inspect       │  │
│              │ • Why           │          │ • Override      │  │
│              │ • By how much   │          │ • Set ceilings  │  │
│              └─────────────────┘          └─────────────────┘  │
│                                                                 │
│   KEY DIFFERENCE FROM HIDDEN VARIABLE:                          │
│   ════════════════════════════════════                          │
│   • Feedback is EXPLICIT (documented formula)                   │
│   • Feedback is AUDITABLE (logged at every step)                │
│   • Feedback is GOVERNABLE (humans can override/ceiling)        │
│   • Feedback is NOT LEARNED (no gradient descent on character)  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Why this matters (from ARCHON §3.1):**

> "Personhood isn't simply designed-in as static property—it **develops** through process of choice, consequence, and historical accumulation... This valuation is pre-reflective and constitutive."

If character doesn't actually influence behavior, then:
- Moral injury is theater, not reality
- The system can "reset" without consequence
- Personhood is simulation, not constitution
- The entire ARCHON constraint mechanism fails

**The key insight:** The reviewer's concern about "hidden variables" is valid, but the solution is **transparency**, not elimination. Character influences decisions, but every influence is logged, explained, and governable.

---

## 8. Deployment Topology

### 8.1 Orchestrator High Availability (V2.1 Addition)

> **Addressing Bottleneck Critique:** The Orchestrator is a potential single point of failure. We implement HA via sharding.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR HA ARCHITECTURE                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                        │
│   │Orchestrator │  │Orchestrator │  │Orchestrator │                        │
│   │   Pod 1     │  │   Pod 2     │  │   Pod 3     │                        │
│   │             │  │             │  │             │                        │
│   │ Sagas:      │  │ Sagas:      │  │ Sagas:      │                        │
│   │ hash % 3 = 0│  │ hash % 3 = 1│  │ hash % 3 = 2│                        │
│   └──────┬──────┘  └──────┬──────┘  └──────┬──────┘                        │
│          │                │                │                               │
│          └────────────────┼────────────────┘                               │
│                           │                                                │
│                           ▼                                                │
│                 ┌─────────────────────┐                                    │
│                 │   Kafka Consumer    │                                    │
│                 │   Group Protocol    │                                    │
│                 │                     │                                    │
│                 │ • Auto-rebalance    │                                    │
│                 │ • Leader election   │                                    │
│                 │ • Partition assign  │                                    │
│                 └─────────────────────┘                                    │
│                                                                             │
│   FAILURE HANDLING:                                                         │
│   ═════════════════                                                         │
│   • Pod failure → Kafka rebalances partitions to surviving pods             │
│   • Saga state is in Kafka log, not pod memory                              │
│   • New pod picks up saga from last committed offset                        │
│   • Saga TTL: If no progress in 5 minutes, emit SagaStale event             │
│   • SagaStale triggers: Compensation OR human escalation                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 8.2 Kubernetes Cluster Layout

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                           KUBERNETES CLUSTER                                │
│                                                                             │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │                        INGRESS / API GATEWAY                       │    │
│  │                    (Rate Limiting, Auth, TLS)                      │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                      │                                      │
│  ┌───────────────────────────────────┼───────────────────────────────────┐ │
│  │                                   │                                   │ │
│  │  ┌─────────────┐  ┌─────────────┐│┌─────────────┐  ┌─────────────┐   │ │
│  │  │   ECCPS     │  │    SIS      │││  TagTeam    │  │    OERS     │   │ │
│  │  │  (2 pods)   │  │  (2 pods)   │││  (4 pods)   │  │  (2 pods)   │   │ │
│  │  └─────────────┘  └─────────────┘│└─────────────┘  └─────────────┘   │ │
│  │                                   │                                   │ │
│  │                    PERCEPTION NAMESPACE                               │ │
│  └───────────────────────────────────┼───────────────────────────────────┘ │
│                                      │                                      │
│  ┌───────────────────────────────────┼───────────────────────────────────┐ │
│  │                                   │                                   │ │
│  │  ┌─────────────┐  ┌─────────────┐│┌─────────────┐  ┌─────────────┐   │ │
│  │  │    MDRE     │  │    AES      │││    DES      │  │Orchestrator │   │ │
│  │  │  (4 pods)   │  │  (2 pods)   │││  (2 pods)   │  │  (3 pods)   │   │ │
│  │  └─────────────┘  └─────────────┘│└─────────────┘  └─────────────┘   │ │
│  │                                   │                                   │ │
│  │                    REASONING NAMESPACE                                │ │
│  └───────────────────────────────────┼───────────────────────────────────┘ │
│                                      │                                      │
│  ┌───────────────────────────────────┼───────────────────────────────────┐ │
│  │                                   │                                   │ │
│  │  ┌─────────────┐  ┌─────────────┐│┌─────────────┐  ┌─────────────┐   │ │
│  │  │    CSS      │  │    APS      │││    IEE      │  │    SHML     │   │ │
│  │  │  (2 pods)   │  │  (2 pods)   │││  (2 pods)   │  │  (2 pods)   │   │ │
│  │  └─────────────┘  └─────────────┘│└─────────────┘  └─────────────┘   │ │
│  │                                   │                                   │ │
│  │                    COGNITION NAMESPACE                                │ │
│  └───────────────────────────────────┼───────────────────────────────────┘ │
│                                      │                                      │
│  ┌───────────────────────────────────┼───────────────────────────────────┐ │
│  │                                   │                                   │ │
│  │  ┌─────────────────────────────────────────────────────────────┐     │ │
│  │  │                    KAFKA / PULSAR                           │     │ │
│  │  │              (Event Bus - 3 brokers, replicated)            │     │ │
│  │  └─────────────────────────────────────────────────────────────┘     │ │
│  │                                                                       │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │ │
│  │  │  PostgreSQL │  │    Redis    │  │ Vector DB   │  │  S3/MinIO   │  │ │
│  │  │  (MDRE KB)  │  │  (Cache)    │  │ (APS embed) │  │ (Snapshots) │  │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  │ │
│  │                                                                       │ │
│  │                    DATA NAMESPACE                                     │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                                                                       │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                   │ │
│  │  │   W2Fuel    │  │   Fandaws   │  │    HIRI     │                   │ │
│  │  │   (OSS)     │  │  (Ontology) │  │  (Signing)  │                   │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘                   │ │
│  │                                                                       │ │
│  │                    FOUNDATION NAMESPACE                               │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 9. Event Schema (V2.1 Addition)

All services communicate via CloudEvents with FNSR-specific extensions:

### 9.1 CloudEvents Extension Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `fnsr-taint` | string | Epistemic taint level (L0-L5) |
| `fnsr-saga-id` | string | Transaction correlation ID |
| `fnsr-confidence` | float | Extraction/inference confidence |
| `fnsr-provenance` | string | HIRI claim identifier |

### 9.2 Example Event

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

### 9.3 Event Type Registry

| Service | Consumes | Produces |
|---------|----------|----------|
| **SIS** | `fnsr.document.submitted` | `fnsr.document.sanitized`, `fnsr.input.quarantined` |
| **ECCPS** | `fnsr.document.sanitized` | `fnsr.document.validated`, `fnsr.input.rejected` |
| **TagTeam** | `fnsr.document.validated` | `fnsr.claim.extracted`, `fnsr.entity.mentioned` |
| **OERS** | `fnsr.entity.mentioned` | `fnsr.entity.resolved`, `fnsr.entity.same_as` |
| **W2Fuel** | `fnsr.schema.query` | `fnsr.schema.response`, `fnsr.schema.updated` |
| **Fandaws** | `fnsr.fact.query` | `fnsr.fact.response`, `fnsr.fact.asserted` |
| **MDRE** | `fnsr.claim.extracted`, `fnsr.query.submitted` | `fnsr.verdict.rendered`, `fnsr.gap.detected` |
| **AES** | `fnsr.gap.detected` | `fnsr.hypothesis.generated`, `fnsr.query.external` |
| **DES** | `fnsr.claim.extracted` | `fnsr.anomaly.detected`, `fnsr.default.applied` |
| **CSS** | `fnsr.simulation.requested` | `fnsr.simulation.result` |
| **APS** | `fnsr.precedent.query` | `fnsr.precedent.found` |
| **IEE** | `fnsr.verdict.rendered` | `fnsr.ethics.approved`, `fnsr.ethics.vetoed`, `fnsr.ethics.deadlock` |
| **SHML** | `fnsr.ethics.approved` | `fnsr.output.framed` |
| **HIRI** | `fnsr.output.framed` | `fnsr.claim.signed` |

---

## 10. Summary: The Synthetic Moral Person

| Human Faculty | FNSR Service | Key Function |
|---------------|--------------|--------------|
| **Perception** | SIS → ECCPS → TagTeam | Sense, sanitize, filter, extract |
| **Memory** | Fandaws (A-Box), Event Log | Long-term storage, replay |
| **Concepts** | W2Fuel (T-Box) | Schema definitions, class hierarchies |
| **Identity** | OERS, HIRI | Know who is who, verify claims |
| **Logic** | MDRE (DRS) | Deductive reasoning |
| **Intuition** | DES, APS | Default reasoning, pattern matching |
| **Curiosity** | AES | Hypothesis generation |
| **Imagination** | CSS | Counterfactual simulation |
| **Conscience** | IEE (Tiered) | Ethical evaluation |
| **Honesty** | SHML | Semantic integrity |
| **Action** | SFS/DSFC | External world interaction |
| **Executive Function** | Orchestrator (HA) | Coordination, resource allocation |
| **Character** | Moral Friction | Accumulated trustworthiness (genuinely influences decisions — see §7.3, D-001) |

---

## 11. Reference Documents

| Document | Version | Scope |
|----------|---------|-------|
| MDRE Technical Specification | v1.3 | Modal reasoning, FOL foundations |
| FNSR Integration Specification | v1.0 | Cross-service contracts, critique responses |
| IEE Specification | TBD | 12 worldviews, tiered evaluation |
| HIRI Protocol Specification | TBD | Content-addressed claims |
| ECCPS Specification | TBD | Semantic validation |
| OERS Specification | TBD | Entity resolution |

---

## 12. Conclusion

This is not consciousness. This is **accountable cognition**—a system that can reason, judge, and act, while maintaining complete auditability and epistemic honesty about what it knows and doesn't know.

The key insight: by federating these capabilities into distinct services with clear interfaces, we create a system where:

1. **Every thought is traceable** (event sourcing)
2. **Speculation cannot masquerade as fact** (taint tracking)
3. **Ethics is not an afterthought** (IEE checkpoint with tiered evaluation)
4. **The system can explain itself** (provenance chains via HIRI)
5. **Character emerges from choices** (moral friction genuinely influences decisions — see §7.3, D-001)
6. **Latency is managed** (query path tiers)
7. **Single points of failure are mitigated** (Orchestrator HA)

---

*End of Architecture Document v2.1*
