# Abductive Elicitation Service (AES)

## Technical Specification v2.1.0

**Document ID:** `aes-core-01`  
**Version:** 2.1.0  
**Status:** PROPOSED  
**Classification:** FNSR Core Reasoning Layer Component

---

> *A pure-function reasoning engine for hypothesis generation and knowledge gap resolution*

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | February 2026 | Initial specification |
| 1.1.0 | February 2026 | Semantic Translation, Circuit Breaker, Routing Decoupling |
| 2.0.0 | February 2026 | **Breaking:** Edge-first rewrite. Pure-function model. JSON-LD canonical. |
| 2.1.0 | February 2026 | Temporal purity rules (§2.7), hypothesis identity (§8.5), contradiction thresholds (§8.2), SQO idempotency (§9.4), metrics isolation (§12.4), orchestration boundaries (§2.8), error surfacing (§17.2) |

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Execution Model](#2-execution-model)
3. [Service Identity](#3-service-identity)
4. [Data Model](#4-data-model)
5. [Foundational Principles](#5-foundational-principles)
6. [Abductive Reasoning Framework](#6-abductive-reasoning-framework)
7. [Gap Analysis](#7-gap-analysis)
8. [Hypothesis Generation](#8-hypothesis-generation)
9. [Structured Query Objects](#9-structured-query-objects)
10. [Evidence Integration](#10-evidence-integration)
11. [Termination Guarantees](#11-termination-guarantees)
12. [State Model](#12-state-model)
13. [Host Interface](#13-host-interface)
14. [Validation and Promotion](#14-validation-and-promotion)
15. [Configuration](#15-configuration)
16. [Conformance](#16-conformance)
17. [Appendices](#appendices)

---

## 1. Executive Summary

The Abductive Elicitation Service (AES) is a **pure-function reasoning engine** that handles incomplete information through abductive inference. When deductive reasoning fails due to missing predicates, AES identifies knowledge gaps and generates:

1. **Hypotheses** — Plausible values inferred from available evidence
2. **Structured Query Objects (SQOs)** — Declarative requests for external information

### 1.1 Core Properties

| Property | Description |
|----------|-------------|
| **Pure Function** | `(Event, State, Config) → (Result, State')` — no side effects |
| **Edge-Native** | Runs in browser or Node.js with zero external dependencies |
| **JSON-LD Canonical** | All inputs, outputs, and state are JSON-LD documents |
| **Offline-First** | Produces useful output even when SQOs cannot be fulfilled |
| **Deterministic** | Same inputs always produce same outputs |
| **Host-Agnostic** | Makes no assumptions about deployment environment |

### 1.2 What AES Is Not

AES is **not**:

- A service that must be deployed
- A system that owns network IO
- A stateful agent with lifecycle
- Dependent on databases, message queues, or caches
- Self-scheduling or self-invoking

AES **emits intent**; hosts **fulfill intent**.

> **Terminology Note:** The word "Service" in "Abductive Elicitation Service" refers to the logical responsibility within the FNSR architecture, not a deployment topology. AES is a reasoning function, not a running process.

### 1.3 Architectural Position

```
┌─────────────────────────────────────────────────────────────────┐
│                      HOST ENVIRONMENT                            │
│               (Browser, Node.js, Cloud Function)                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                    AES CORE (This Spec)                 │   │
│   │                                                         │   │
│   │   Input:  (GapEvent, State, Config)                     │   │
│   │   Output: (Result, State')                              │   │
│   │                                                         │   │
│   │   • Gap Analysis                                        │   │
│   │   • Hypothesis Generation                               │   │
│   │   • SQO Emission                                        │   │
│   │   • Evidence Integration                                │   │
│   │                                                         │   │
│   │   AES never calls itself, MDRE, or any external system. │   │
│   │   All orchestration is host-driven.                     │   │
│   │                                                         │   │
│   └─────────────────────────────────────────────────────────┘   │
│                              │                                   │
│              ┌───────────────┴───────────────┐                   │
│              │                               │                   │
│              ▼                               ▼                   │
│    ┌─────────────────┐             ┌─────────────────┐          │
│    │  Host Storage   │             │ Host SQO        │          │
│    │  (IndexedDB,    │             │ Fulfillment     │          │
│    │   file, Redis)  │             │ (fetch, queue)  │          │
│    └─────────────────┘             └─────────────────┘          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Execution Model

This section is **normative**. Conforming implementations MUST adhere to this model.

### 2.1 Pure Function Semantics

AES is defined as a pure function:

```
analyzeGap : (GapEvent, State, Config) → (AnalysisResult, State')
```

**Requirements:**

| Requirement | Description |
|-------------|-------------|
| **Referential Transparency** | Given identical inputs, AES MUST return identical outputs |
| **No Side Effects** | AES MUST NOT perform IO, mutate external state, or depend on ambient context |
| **No Hidden State** | All state MUST be explicitly passed in and returned |
| **Serializable IO** | All inputs and outputs MUST be serializable to JSON-LD |

### 2.2 Edge-First Constraint

**Canonical execution environments:**

- A browser tab (modern ES6+ with no extensions)
- A Node.js process (v18+ with no native modules)

**Constraint:** If a feature cannot execute in these environments without external services, it is NOT part of AES core.

```javascript
// This MUST work
import { AES } from '@fnsr/aes';

const aes = new AES(config);
const { result, state: nextState } = aes.analyzeGap(gapEvent, currentState);

// No network required
// No database required  
// No message queue required
// No external services required
```

**Instance Statefulness:** AES instances created via `new AES(config)` are stateless. The constructor MUST NOT capture mutable state. Configuration is read-only after construction.

### 2.3 Host Responsibilities

AES emits **declarative intent**. The host environment decides how to act on it.

| AES Emits | Host Decides |
|-----------|--------------|
| `SQO` (query intent) | Whether/how to fulfill (fetch, queue, mock, ignore) |
| `Hypothesis` | Whether/how to persist or surface to user |
| `State'` | Where to store (memory, IndexedDB, file, Redis) |
| `PromotionRecommendation` | Whether to accept (apply policies, circuit breakers) |

**AES never assumes hosts will act.** All outputs are useful even if hosts take no action.

### 2.4 Offline-First Semantics

Inability to fulfill SQOs is **not an error**. It is a normal operating mode.

| Scenario | AES Behavior |
|----------|--------------|
| All SQOs fulfilled | Return hypotheses with evidence from responses |
| Some SQOs fulfilled | Return hypotheses with partial evidence, flag gaps |
| No SQOs fulfilled | Return best-effort hypotheses with explicit uncertainty |
| No network available | Operate entirely on local knowledge; SQOs queued as intent |

**Principle:** AES produces the best possible output given available information. Uncertainty is surfaced, not hidden.

### 2.5 Determinism Guarantee

For testing, debugging, and auditability:

```javascript
const result1 = aes.analyzeGap(event, state, config);
const result2 = aes.analyzeGap(event, state, config);

assert.deepEqual(result1, result2); // Always true
```

**Implications:**

- No `Date.now()` or `Math.random()` in core logic
- Timestamps and IDs are derived from inputs or passed explicitly
- Any randomness must come from config (e.g., seed value)

### 2.6 State as Value

State is **passed in** and **returned out**, never held internally:

```javascript
// Correct: State flows through
let state = AES.initialState();
const r1 = aes.analyzeGap(event1, state, config);
state = r1.state;
const r2 = aes.analyzeGap(event2, state, config);
state = r2.state;

// Incorrect: Internal state (NOT CONFORMANT)
aes.loadState(state);      // ❌ Stateful method
aes.analyzeGap(event);     // ❌ Implicit state
```

### 2.7 Temporal Purity (v2.1)

**Normative Rule:** All temporal values MUST be provided by the host as inputs or computed deterministically from inputs. AES MUST NOT sample wall-clock time.

| Temporal Value | Source | Notes |
|----------------|--------|-------|
| `GapEvent.timestamp` | Host-provided input | When the gap was detected |
| `Evidence.sourceMetadata.retrievedAt` | Host-provided input | When external data was fetched |
| `Hypothesis.expiration` | Computed from input timestamp + config duration | Deterministic |
| `AnalysisResult.processingMetadata` | Host-supplied OR omitted | See below |

**Processing Metadata:** The `processingMetadata` block (including `durationMs`) is **informational** and **host-supplied**. If hosts wish to track processing duration, they MUST measure externally and attach it to results. AES core MUST NOT measure elapsed time internally.

```javascript
// Correct: Host measures duration
const start = performance.now();
const { result, state } = aes.analyzeGap(event, state, config);
result.processingMetadata = {
  durationMs: performance.now() - start,
  measuredBy: 'host'
};

// Incorrect: AES measures duration internally
// (violates temporal purity)
```

### 2.8 Orchestration Boundaries (v2.1)

**Normative Rule:** AES never schedules or invokes itself, MDRE, or any external system. All looping, retry, and orchestration behavior is driven by the host.

| Behavior | Responsibility |
|----------|----------------|
| Calling `analyzeGap` | Host |
| Calling `integrateEvidence` | Host |
| Looping MDRE → AES → MDRE | Host orchestration |
| Retrying failed SQOs | Host policy |
| Scheduling re-analysis | Host decision |
| Emitting new GapEvents | MDRE (not AES) |

**AES does not emit GapEvents.** It receives them. The MDRE ↔ AES feedback loop is:

```
Host calls MDRE.deduce()
  → MDRE emits GapEvent (if incomplete)
  → Host calls AES.analyzeGap(gapEvent, state, config)
  → AES returns hypotheses + SQOs
  → Host fulfills SQOs (optional)
  → Host calls AES.integrateEvidence(evidence, state, config)
  → Host calls MDRE.deduce() again (if desired)
```

AES is passive. Hosts drive the loop.

---

## 3. Service Identity

| Attribute | Value |
|-----------|-------|
| **Name** | Abductive Elicitation Service |
| **Identifier** | `aes-core-01` |
| **Layer** | Reasoning (FNSR §2.3) |
| **Metaphor** | Detective / Curiosity |
| **Nature** | Pure function over explicit state |
| **Canonical Format** | JSON-LD |

### 3.1 Functional Signature

```typescript
interface AES {
  analyzeGap(
    event: GapEvent,
    state: AESState,
    config: AESConfig
  ): { result: AnalysisResult; state: AESState };
  
  integrateEvidence(
    evidence: Evidence,
    state: AESState,
    config: AESConfig
  ): { result: IntegrationResult; state: AESState };
  
  static initialState(): AESState;
}
```

### 3.2 FNSR Integration

Within the FNSR architecture, AES:

- **Receives** gap events from MDRE (or equivalent reasoning engine)
- **Emits** hypotheses and SQOs as JSON-LD documents
- **Does not** directly communicate with external systems
- **Does not** own network, storage, or orchestration
- **Does not** call MDRE or schedule its own invocation

---

## 4. Data Model

All AES data structures are **JSON-LD documents**.

### 4.1 Taint Levels

AES tracks epistemic status via taint levels:

| Level | Name | Description | Crosses Firewall? |
|-------|------|-------------|-------------------|
| L0 | VERIFIED | Schema facts, governance decisions | N/A (already trusted) |
| L1 | ATTESTED | Trusted source, digital signature | Yes |
| L2 | INFERRED | Valid deductive inference | Yes |
| L3 | SPECULATIVE | AES hypotheses, unvalidated | **No** (requires promotion) |
| L4 | HYPOTHETICAL | Simulation/sandbox only | No |
| L5 | ADVERSARIAL | Potentially hostile input | No |

**Invariant:** AES outputs are **always L3** until explicitly promoted by the host.

**Promotion Assumption Rule (v2.1):** AES MUST NOT assume promotion has occurred unless evidence is explicitly integrated via `integrateEvidence`. Hypotheses remain L3 in AES's view until confirmed or refuted by evidence.

### 4.2 GapEvent

Input to AES when deductive reasoning cannot proceed:

```json
{
  "@context": "https://fnsr.dev/schema/aes/v2",
  "@type": "GapEvent",
  "@id": "urn:uuid:gap-20260202-001234",
  
  "queryId": "query-12345",
  "sagaId": "saga-employment-check-001",
  "goal": "can_hire(john_doe)",
  
  "recursionContext": {
    "depth": 0,
    "priorAttempts": []
  },
  
  "missingPredicates": [
    {
      "predicate": "background_check_status",
      "arity": 2,
      "boundArguments": { "arg0": "john_doe" },
      "unboundArguments": ["arg1"],
      "expectedType": { 
        "@type": "Enum", 
        "values": ["cleared", "pending", "failed"] 
      },
      "criticality": "blocking"
    }
  ],
  
  "partialProofTree": {
    "goal": "can_hire(john_doe)",
    "proved": [
      "application_complete(john_doe)",
      "reference_check_status(john_doe, passed)"
    ],
    "unproved": ["background_check_status(john_doe, cleared)"]
  },
  
  "taint": "L2",
  "timestamp": "2026-02-02T14:30:00Z"
}
```

### 4.3 Hypothesis

AES-generated speculation about missing values:

```json
{
  "@context": "https://fnsr.dev/schema/aes/v2",
  "@type": "Hypothesis",
  "@id": "urn:uuid:hyp-20260202-001234",
  
  "canonicalKey": {
    "predicate": "background_check_status",
    "boundArguments": { "arg0": "john_doe" },
    "hypothesizedValue": "cleared",
    "originGapId": "urn:uuid:gap-20260202-001234"
  },
  
  "predicate": "background_check_status(john_doe, cleared)",
  
  "plausibility": {
    "score": 0.72,
    "baseScore": 0.72,
    "contradictionFactor": 1.0,
    "scoringProfile": "default"
  },
  
  "reasoning": {
    "method": "analogical_inference",
    "supportingEvidence": [
      {
        "fact": "reference_check_status(john_doe, passed)",
        "taint": "L1",
        "weight": 0.3
      },
      {
        "fact": "prior_background_check(john_doe, 2021, cleared)",
        "taint": "L1", 
        "weight": 0.4
      }
    ],
    "weakeningFactors": [
      "background_check_policy_updated(2024)",
      "no_recent_check_on_record"
    ],
    "contradictions": []
  },
  
  "validationRequirements": {
    "authoritativeSource": "hr_system",
    "freshnessMaxAge": "P1D",
    "confidenceThreshold": 0.95
  },
  
  "expiration": "2026-02-02T15:30:00Z",
  "taint": "L3",
  "originGapId": "urn:uuid:gap-20260202-001234"
}
```

### 4.4 Structured Query Object (SQO)

Declarative request for external information:

```json
{
  "@context": "https://fnsr.dev/schema/aes/v2",
  "@type": "StructuredQueryObject",
  "@id": "urn:uuid:sqo-20260202-001234",
  
  "canonicalKey": {
    "targetService": "hr_system",
    "entityId": "person:john_doe",
    "attribute": "background_check_status"
  },
  
  "origin": {
    "gapId": "urn:uuid:gap-20260202-001234",
    "sagaId": "saga-employment-check-001",
    "recursionDepth": 1
  },
  
  "intent": {
    "targetService": "hr_system",
    "entity": {
      "canonicalId": { "@id": "person:john_doe" },
      "externalHint": {
        "namespace": "hr_system",
        "externalId": "employee_12345"
      }
    },
    "attribute": {
      "name": "background_check_status",
      "schemaRef": { "@id": "w2fuel:hr/background_check_status" },
      "expectedType": "enum",
      "expectedValues": ["cleared", "pending", "failed", "not_started"]
    }
  },
  
  "translation": {
    "adapterId": "hr_system_adapter",
    "valueMappings": {
      "PASSED": "cleared",
      "APPROVED": "cleared",
      "IN_PROGRESS": "pending",
      "FAILED": "failed"
    },
    "onUnmapped": "reject",
    "onNull": "not_started"
  },
  
  "constraints": {
    "freshnessMaxAge": "P1D",
    "requiredTrustLevel": "authoritative"
  },
  
  "taint": "L3",
  "timestamp": "2026-02-02T14:30:10Z"
}
```

**Note:** SQOs contain **no dispatch instructions**. They describe *what* is needed, not *how* to get it.

### 4.5 Evidence

Response to a fulfilled SQO:

```json
{
  "@context": "https://fnsr.dev/schema/aes/v2",
  "@type": "Evidence",
  "@id": "urn:uuid:evd-20260202-001234",
  
  "sqoId": "urn:uuid:sqo-20260202-001234",
  
  "response": {
    "raw": { "status": "PASSED" },
    "translated": {
      "attribute": "background_check_status",
      "value": "cleared",
      "mappingApplied": "PASSED → cleared"
    }
  },
  
  "sourceMetadata": {
    "source": "hr_system",
    "retrievedAt": "2026-02-02T14:34:55Z",
    "trustLevel": "authoritative"
  },
  
  "validation": {
    "schemaValid": true,
    "valueInRange": true,
    "translationSuccessful": true
  },
  
  "suggestedTaint": "L1"
}
```

### 4.6 AESState

Explicit state passed through AES invocations:

```json
{
  "@context": "https://fnsr.dev/schema/aes/v2",
  "@type": "AESState",
  "version": "2.1.0",
  
  "activeHypotheses": [],
  "pendingSQOs": [],
  
  "recursionTracking": {},
  "hypothesisRegistry": {},
  "sqoRegistry": {},
  
  "metrics": {
    "totalGapsAnalyzed": 0,
    "totalHypothesesGenerated": 0,
    "totalSQOsEmitted": 0,
    "totalEvidenceIntegrated": 0
  }
}
```

### 4.7 AnalysisResult

Output from `analyzeGap`:

```json
{
  "@context": "https://fnsr.dev/schema/aes/v2",
  "@type": "AnalysisResult",
  
  "gapId": "urn:uuid:gap-20260202-001234",
  "status": "hypotheses_generated",
  
  "hypotheses": [],
  "sqos": [],
  
  "uncertainty": {
    "level": "medium",
    "reason": "hypothesis_pending_validation",
    "canProceedWithoutSQO": true,
    "bestAvailableHypothesis": "urn:uuid:hyp-20260202-001234"
  },
  
  "terminationReason": "coverage_complete",
  
  "processingMetadata": null
}
```

**Note (v2.1):** `processingMetadata` is `null` by default. Hosts MAY attach timing information externally. See §2.7.

---

## 5. Foundational Principles

### 5.1 Epistemic Firewall

**Critical Invariant:** L3 (Speculative) outputs CANNOT be used as L0-L2 inputs without explicit promotion.

```
═══════════════════════════════════════════════════════════════════
║                    FIREWALL BOUNDARY                             ║
║                                                                  ║
║    Crossing requires:                                            ║
║    • Evidence from authoritative source (L3 → L1), OR            ║
║    • Multiple corroborating sources (L3 → L2), OR                ║
║    • Human attestation (L3 → L1), OR                             ║
║    • Governance decision (L3 → L0)                               ║
║                                                                  ║
║    Host implements promotion policy; AES only recommends.        ║
║                                                                  ║
═══════════════════════════════════════════════════════════════════
```

**Taint Propagation Rule:**

```
taint(conclusion) = max(taint(premise₁), taint(premise₂), ...)
```

### 5.2 Minimal Information Principle

AES requests only what is necessary to resolve the gap. One attribute, one entity, one SQO.

### 5.3 Explicit Uncertainty Principle

AES never hides uncertainty. All outputs include confidence scores, taint levels, expiration times, and reasoning traces.

### 5.4 Composability Principle

AES operations compose cleanly:

```javascript
let state = AES.initialState();
const r1 = aes.analyzeGap(gap1, state, config);
const r2 = aes.analyzeGap(gap2, r1.state, config);
const r3 = aes.integrateEvidence(evidence, r2.state, config);
```

---

## 6. Abductive Reasoning Framework

### 6.1 What is Abduction?

Abduction is "inference to the best explanation." Given observations and rules, what hypotheses would explain the observations?

| Reasoning Type | Direction | AES Role |
|----------------|-----------|----------|
| **Deduction** | Rules + Facts → Conclusions | Not AES (this is MDRE) |
| **Induction** | Examples → Rules | Not AES (this is learning) |
| **Abduction** | Observations + Rules → Hypotheses | **AES core function** |

### 6.2 Formal Definition

Given:
- **T**: Background theory (rules from MDRE/knowledge base)
- **O**: Observations (known facts)
- **G**: Goal (what we're trying to prove)
- **A**: Abducibles (predicates that may be hypothesized)

AES computes a set **Δ** such that:

1. **T ∪ Δ ⊨ G** — Theory plus hypotheses entails the goal
2. **T ∪ Δ ⊭ ⊥** — No contradiction introduced
3. **Δ ⊆ A** — Only abducible predicates are hypothesized
4. **|Δ| is minimal** — Smallest sufficient set

### 6.3 Hypothesis Strategies

| Strategy | Description | When Used |
|----------|-------------|-----------|
| **Historical Inference** | Use past values for same entity | Entity has history in State |
| **Analogical Inference** | Use values from similar entities | Similar entities in State |
| **Default Value** | Use schema-defined default | Schema in Config provides default |
| **Statistical Mode** | Most common value in population | Population statistics in State/Config |
| **SQO Generation** | Request from authoritative source | Source defined in Config |

**Statistical Strategy Constraint (v2.1):** Statistical strategies (including "most common value") are permitted only when population statistics are provided explicitly via State or Config. AES MUST NOT derive population statistics implicitly or from external sources.

```json
{
  "@type": "AESConfig",
  "populationStatistics": {
    "background_check_status": {
      "distribution": {
        "cleared": 0.85,
        "pending": 0.10,
        "failed": 0.05
      },
      "mode": "cleared",
      "sampleSize": 10000,
      "asOfDate": "2026-01-15"
    }
  }
}
```

---

## 7. Gap Analysis

### 7.1 Gap Categories

| Category | Description | Primary Strategy |
|----------|-------------|------------------|
| `ATTRIBUTE_UNKNOWN` | Entity exists, attribute missing | SQO to authoritative source |
| `ENTITY_UNRESOLVED` | Entity reference ambiguous | SQO to entity resolution |
| `RULE_INAPPLICABLE` | No rule covers this case | Escalate to governance |
| `CONFLICT_UNRESOLVED` | Multiple contradictory values | SQO for resolution |
| `TEMPORAL_GAP` | Value may have changed | SQO with freshness constraint |

### 7.2 Gap Analysis Algorithm

```
FUNCTION analyzeGapCategory(gap, config):

  // Guard: Recursion depth
  IF gap.recursionContext.depth >= config.maxRecursionDepth:
    RETURN { status: "RECURSION_LIMIT", action: "ESCALATE" }
  
  // Guard: Prior attempts
  FOR predicate IN gap.missingPredicates:
    IF predicate IN gap.recursionContext.priorAttempts:
      predicate.skipSQO = true
  
  // Classify each predicate
  FOR predicate IN gap.missingPredicates:
    predicate.category = classifyPredicate(predicate)
    predicate.strategy = selectStrategy(predicate, config)
  
  RETURN { predicates: gap.missingPredicates }
```

---

## 8. Hypothesis Generation

### 8.1 Generation Pipeline

1. **Candidate Generation** — Generate possible values from schema, history, analogies
2. **Consistency Check** — Filter candidates that contradict known facts
3. **Plausibility Scoring** — Score by evidence (multiplicative contradiction model)
4. **Ranking & Selection** — Select top-k hypotheses (minimal covering set)

### 8.2 Plausibility Scoring

AES uses a **multiplicative contradiction model**:

```
plausibility(H) = baseScore(H) × contradictionFactor(H)

WHERE:
  baseScore(H) = w₁·evidence + w₂·consistency + w₃·specificity - w₄·recency
  
  contradictionFactor(H) = ∏ (1 - confidence(c_i))
                           for each contradiction c_i
```

**Contradiction Annihilation Rule (v2.1):**

A contradiction **annihilates** a hypothesis (reduces plausibility to 0) when:

1. The contradicting fact has taint ≤ L2 (i.e., it's in the production zone), AND
2. The contradicting fact has confidence ≥ `config.scoring.annihilationThreshold` (default: 0.95)

```
IF contradiction.taint <= L2 AND contradiction.confidence >= annihilationThreshold:
  contradictionFactor = 0  // Hypothesis annihilated
```

**Rationale:** A high-confidence, non-speculative fact should definitively refute a speculation.

| Contradiction Taint | Contradiction Confidence | Effect |
|---------------------|--------------------------|--------|
| L0-L2 | ≥ 0.95 | Annihilates (factor = 0) |
| L0-L2 | < 0.95 | Reduces (factor = 1 - confidence) |
| L3+ | Any | Reduces (factor = 1 - confidence × 0.5) |

### 8.3 Scoring Profiles

Weights are configurable:

```json
{
  "default": {
    "weights": { 
      "evidence": 0.35, 
      "consistency": 0.25, 
      "specificity": 0.15, 
      "recency": 0.10 
    },
    "stalenessThresholdHours": 168,
    "annihilationThreshold": 0.95
  },
  "high_stakes": {
    "weights": { 
      "evidence": 0.40, 
      "consistency": 0.35, 
      "specificity": 0.10, 
      "recency": 0.15 
    },
    "stalenessThresholdHours": 24,
    "minimumPlausibilityThreshold": 0.80,
    "annihilationThreshold": 0.90
  }
}
```

### 8.4 Minimal Covering Set

When multiple hypotheses exist, AES selects the minimal set covering all gaps, ranked by plausibility.

### 8.5 Hypothesis Identity and De-Duplication (v2.1)

**Canonical Key:** Two hypotheses are considered "the same" if they share the same canonical key:

```
canonicalKey = (predicate, boundArguments, hypothesizedValue, originGapId)
```

**De-Duplication Rules:**

| Scenario | Behavior |
|----------|----------|
| New hypothesis, no existing match | Add to registry |
| New hypothesis matches existing by canonicalKey | **Replace** if new plausibility > existing |
| New hypothesis matches existing, lower plausibility | **Discard** new hypothesis |
| Evidence confirms hypothesis | Mark existing as `confirmed`, keep in registry |
| Evidence refutes hypothesis | Mark existing as `refuted`, keep for audit |

**Registry Lifecycle:**

```
PENDING → CONFIRMED (via matching evidence)
PENDING → REFUTED (via contradicting evidence)
PENDING → EXPIRED (via expiration timestamp)
PENDING → SUPERSEDED (via higher-plausibility replacement)
```

**Rationale:** In long-running sagas, hypotheses may be re-generated across multiple `analyzeGap` calls. The registry ensures consistent identity and prevents unbounded hypothesis accumulation.

---

## 9. Structured Query Objects

### 9.1 SQO as Declarative Intent

An SQO describes **what information is needed**, not **how to get it**.

**SQO contains:**
- Target service (logical name, not URL)
- Entity and attribute
- Translation mappings
- Freshness constraints

**SQO does NOT contain:**
- URLs or endpoints
- Authentication credentials
- Retry policies
- Callback addresses

These are **host concerns**.

### 9.2 Translation Specification

```json
{
  "translation": {
    "adapterId": "hr_system_adapter",
    "sourceField": "$.employee.background_check.status",
    "valueMappings": {
      "PASSED": "cleared",
      "IN_PROGRESS": "pending",
      "FAILED": "failed"
    },
    "onUnmapped": "reject",
    "onNull": "not_started"
  }
}
```

### 9.3 SQO Lifecycle

```
AES emits SQO → Host receives SQO → Host decides fulfillment:
  • fetch() immediately
  • Queue for batch processing
  • Mock for testing
  • Ignore (offline mode)
  
Host receives response → Host translates → Host calls integrateEvidence()
```

### 9.4 SQO Identity and Idempotency (v2.1)

**Canonical Key:** Two SQOs are considered "the same" if they share:

```
canonicalKey = (targetService, entityId, attribute)
```

**Idempotency Rules:**

| Scenario | Behavior |
|----------|----------|
| SQO emitted, no existing match | Add to registry as `pending` |
| SQO emitted, matches existing `pending` | **Do not re-emit**; return existing SQO ID |
| SQO emitted, matches existing `fulfilled` | **Re-emit** if freshness constraint not met |
| Evidence arrives for SQO | Mark as `fulfilled`, record timestamp |
| Duplicate evidence arrives | **Ignore** if SQO already fulfilled with same value |
| Duplicate evidence with different value | **Conflict**; flag for resolution |

**Rationale:** Hosts may call `analyzeGap` multiple times for the same saga. Without idempotency, duplicate SQOs would flood external systems.

**Duplicate Evidence Handling:**

```javascript
// In integrateEvidence:
IF sqoRegistry[evidence.sqoId].status === 'fulfilled':
  IF sqoRegistry[evidence.sqoId].value === evidence.response.translated.value:
    RETURN { status: 'duplicate_ignored' }
  ELSE:
    RETURN { status: 'conflict_detected', existingValue, newValue }
```

---

## 10. Evidence Integration

### 10.1 The `integrateEvidence` Function

```
integrateEvidence : (Evidence, State, Config) → (IntegrationResult, State')
```

When the host fulfills an SQO, it provides evidence back to AES. AES:

1. Validates the evidence against the SQO constraints
2. Checks if evidence confirms or refutes existing hypotheses
3. Creates a new fact with suggested taint
4. Returns promotion recommendation

### 10.2 Promotion Recommendations

AES **recommends** promotion; hosts **decide**:

```json
{
  "promotionRecommendation": {
    "suggestedTaint": "L1",
    "confidence": 0.95,
    "basis": [
      "source_authoritative",
      "freshness_acceptable",
      "translation_successful"
    ],
    "hostConsiderations": [
      "circuit_breaker_status",
      "rate_limiting",
      "anomaly_detection"
    ]
  }
}
```

---

## 11. Termination Guarantees

### 11.1 Bounding Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `maxHypothesesPerGap` | 10 | Maximum hypotheses per gap |
| `maxSQOsPerAnalysis` | 5 | Maximum SQOs per analysis |
| `maxRecursionDepth` | 3 | Maximum MDRE ↔ AES loop depth |
| `maxProcessingIterations` | 1000 | Maximum internal loop iterations |

### 11.2 Termination Reasons

| Reason | Meaning |
|--------|---------|
| `coverage_complete` | All gaps covered |
| `max_hypotheses_reached` | Hit hypothesis limit |
| `max_sqos_reached` | Hit SQO limit |
| `iteration_limit_reached` | Hit iteration limit |
| `recursion_limit_exceeded` | Too many cycles |
| `no_viable_candidates` | No hypotheses possible |

---

## 12. State Model

### 12.1 State as First-Class Value

AES state is:

- **Explicit**: Passed in, returned out — never hidden
- **Immutable**: Each operation returns new state
- **Serializable**: Full JSON-LD round-trip without loss
- **Versionable**: Schema version tracked for migrations

### 12.2 Initial State

```javascript
function initialState() {
  return {
    "@type": "AESState",
    "version": "2.1.0",
    "activeHypotheses": [],
    "pendingSQOs": [],
    "recursionTracking": {},
    "hypothesisRegistry": {},
    "sqoRegistry": {},
    "metrics": {
      "totalGapsAnalyzed": 0,
      "totalHypothesesGenerated": 0,
      "totalSQOsEmitted": 0,
      "totalEvidenceIntegrated": 0
    }
  };
}
```

### 12.3 State Serialization

State MUST survive JSON-LD round-trip:

```javascript
const serialized = JSON.stringify(state);
const deserialized = JSON.parse(serialized);
assert.deepEqual(
  aes.analyzeGap(event, state, config),
  aes.analyzeGap(event, deserialized, config)
);
```

### 12.4 Metrics Isolation (v2.1)

**Normative Rule:** Metrics are **informational only** and MUST NOT influence reasoning outcomes.

| Principle | Implication |
|-----------|-------------|
| Metrics are observational | They record what happened, not what should happen |
| Metrics cannot affect scoring | Plausibility formulas MUST NOT reference counters |
| Metrics cannot affect strategy | Hypothesis/SQO generation MUST NOT branch on metrics |
| Metrics are not required | AES MUST function identically with metrics zeroed |

**Conformance Test:**

```javascript
// These MUST produce identical hypotheses and SQOs
const state1 = { ...baseState, metrics: { totalGapsAnalyzed: 0 } };
const state2 = { ...baseState, metrics: { totalGapsAnalyzed: 99999 } };

const r1 = aes.analyzeGap(event, state1, config);
const r2 = aes.analyzeGap(event, state2, config);

assert.deepEqual(r1.result.hypotheses, r2.result.hypotheses);
assert.deepEqual(r1.result.sqos, r2.result.sqos);
```

---

## 13. Host Interface

### 13.1 Minimal Host Contract

A conforming host MUST:

1. Provide `analyzeGap` inputs (GapEvent, State, Config as JSON-LD)
2. Accept `analyzeGap` outputs (AnalysisResult, State' as JSON-LD)
3. Manage state persistence (if desired)
4. Decide SQO fulfillment (if desired)

A conforming host MAY:

1. Implement circuit breakers on promotion
2. Implement rate limiting
3. Implement anomaly detection
4. Route SQOs through service mesh
5. Persist state to any backend
6. Attach processingMetadata externally

### 13.2 Browser Host Example

```javascript
import { AES } from '@fnsr/aes';

const aes = new AES(config);
let state = AES.initialState();

async function handleGap(gapEvent) {
  const start = performance.now();
  
  const { result, state: newState } = aes.analyzeGap(gapEvent, state, config);
  state = newState;
  
  // Host attaches timing (AES doesn't measure)
  result.processingMetadata = {
    durationMs: performance.now() - start,
    measuredBy: 'host'
  };
  
  // Store in IndexedDB
  await db.put('state', state);
  
  // Fulfill SQOs
  for (const sqo of result.sqos) {
    try {
      const response = await fetch(resolveEndpoint(sqo));
      const evidence = translateResponse(response, sqo);
      const integration = aes.integrateEvidence(evidence, state, config);
      state = integration.state;
    } catch (e) {
      console.warn('SQO failed, using hypotheses only');
    }
  }
  
  return result;
}
```

### 13.3 Node.js Host Example

```javascript
import { AES } from '@fnsr/aes';
import { readFile, writeFile } from 'fs/promises';

const aes = new AES(config);

async function analyze(gapEvent) {
  const state = JSON.parse(await readFile('./state.json'));
  const { result, state: newState } = aes.analyzeGap(gapEvent, state, config);
  await writeFile('./state.json', JSON.stringify(newState));
  return result;
}
```

### 13.4 MDRE ↔ AES Orchestration Example

```javascript
// Host orchestrates the loop — AES is passive
async function resolveGoal(goal) {
  let mdreState = MDRE.initialState();
  let aesState = AES.initialState();
  
  for (let i = 0; i < MAX_ITERATIONS; i++) {
    // Step 1: MDRE attempts deduction
    const deduction = mdre.deduce(goal, mdreState, mdreConfig);
    
    if (deduction.status === 'success') {
      return deduction.result;  // Done!
    }
    
    if (deduction.status === 'gap_detected') {
      // Step 2: AES analyzes gap
      const analysis = aes.analyzeGap(deduction.gapEvent, aesState, aesConfig);
      aesState = analysis.state;
      
      // Step 3: Host fulfills SQOs (optional)
      for (const sqo of analysis.result.sqos) {
        const evidence = await fulfillSQO(sqo);
        if (evidence) {
          const integration = aes.integrateEvidence(evidence, aesState, aesConfig);
          aesState = integration.state;
          
          // Update MDRE with new fact
          mdreState = mdre.addFact(integration.result.newFact, mdreState);
        }
      }
      
      // Loop continues — host drives it
    }
  }
  
  return { status: 'max_iterations', bestHypothesis: aesState.activeHypotheses[0] };
}
```

---

## 14. Validation and Promotion

### 14.1 The Promotion Decision

AES **recommends** promotion; hosts **decide**.

```
AES Output:                    Host Decision:
─────────────                  ─────────────
{ suggestedTaint: "L1" }  →    IF circuitBreaker.open: REJECT
                               ELSE IF rateLimit.exceeded: REJECT
                               ELSE IF anomaly.detected: QUEUE_FOR_REVIEW
                               ELSE: ACCEPT
```

### 14.2 Validation Rules

| Rule | Failure Action |
|------|----------------|
| Schema validation | Reject |
| Value range check | Reject |
| Translation success | Reject |
| Freshness check | Warn |
| Source trust check | Downgrade taint |

---

## 15. Configuration

### 15.1 Configuration Schema

```json
{
  "@type": "AESConfig",
  "version": "2.1.0",
  
  "termination": {
    "maxHypothesesPerGap": 10,
    "maxSQOsPerAnalysis": 5,
    "maxRecursionDepth": 3,
    "maxProcessingIterations": 1000
  },
  
  "scoring": {
    "defaultProfile": "default",
    "profiles": {
      "default": {
        "weights": {
          "evidence": 0.35,
          "consistency": 0.25,
          "specificity": 0.15,
          "recency": 0.10
        },
        "stalenessThresholdHours": 168,
        "annihilationThreshold": 0.95
      }
    }
  },
  
  "knownSources": {},
  "adapters": {},
  "populationStatistics": {},
  
  "defaults": {
    "freshnessMaxAge": "P1D",
    "hypothesisExpiration": "PT1H"
  }
}
```

---

## 16. Conformance

### 16.1 Core Conformance Requirements

An implementation is **Core Conformant** if:

1. **Pure Function**: `analyzeGap` has no side effects
2. **Deterministic**: Same inputs → same outputs
3. **JSON-LD IO**: All inputs/outputs serialize to valid JSON-LD
4. **State Transparency**: State is passed in and returned, never hidden
5. **Termination**: Analysis always terminates within bounds
6. **Edge Executable**: Runs in browser/Node.js without external services
7. **Temporal Purity**: No internal time sampling (v2.1)
8. **Metrics Isolation**: Metrics do not influence reasoning (v2.1)
9. **No Self-Invocation**: AES never calls itself or MDRE (v2.1)

### 16.2 Conformance Testing

```javascript
describe('AES Core Conformance', () => {
  test('determinism', () => {
    const r1 = aes.analyzeGap(event, state, config);
    const r2 = aes.analyzeGap(event, state, config);
    expect(r1).toEqual(r2);
  });
  
  test('no side effects', () => {
    const original = JSON.stringify(state);
    aes.analyzeGap(event, state, config);
    expect(JSON.stringify(state)).toEqual(original);
  });
  
  test('json-ld round trip', () => {
    const { result } = aes.analyzeGap(event, state, config);
    const rt = JSON.parse(JSON.stringify(result));
    expect(rt).toEqual(result);
  });
  
  test('metrics isolation', () => {
    const state1 = { ...state, metrics: { totalGapsAnalyzed: 0 } };
    const state2 = { ...state, metrics: { totalGapsAnalyzed: 99999 } };
    const r1 = aes.analyzeGap(event, state1, config);
    const r2 = aes.analyzeGap(event, state2, config);
    expect(r1.result.hypotheses).toEqual(r2.result.hypotheses);
  });
  
  test('no internal timing', () => {
    // processingMetadata should be null from AES
    const { result } = aes.analyzeGap(event, state, config);
    expect(result.processingMetadata).toBeNull();
  });
});
```

---

## 17. Appendices

### Appendix A: Glossary

| Term | Definition |
|------|------------|
| **Abducible** | A predicate that AES may hypothesize values for |
| **Abduction** | Inference to the best explanation |
| **Annihilation** | Reduction of plausibility to 0 due to high-confidence contradiction |
| **Canonical Key** | Tuple uniquely identifying a hypothesis or SQO |
| **Evidence** | Response to a fulfilled SQO |
| **Gap** | A missing predicate blocking deduction |
| **Hypothesis** | A speculative assertion (L3 taint) |
| **Host** | The environment running AES |
| **Plausibility** | Degree of belief in a hypothesis |
| **Promotion** | Transition from L3 to L0/L1/L2 |
| **SQO** | Structured Query Object — declarative data request |
| **Taint** | Epistemic trust level (L0-L5) |

### Appendix B: Error Codes and Surfacing (v2.1)

Errors are returned in `AnalysisResult.status` or `IntegrationResult.status`, never thrown as exceptions (which would break purity).

| Code | Name | Surfaces In | Description |
|------|------|-------------|-------------|
| `AES-001` | `INVALID_GAP_EVENT` | AnalysisResult.status | GapEvent failed validation |
| `AES-002` | `INVALID_STATE` | AnalysisResult.status | State failed validation |
| `AES-003` | `INVALID_CONFIG` | AnalysisResult.status | Config failed validation |
| `AES-004` | `RECURSION_LIMIT` | AnalysisResult.status | Max recursion exceeded |
| `AES-005` | `ITERATION_LIMIT` | AnalysisResult.status | Max iterations exceeded |
| `AES-006` | `NO_VIABLE_HYPOTHESES` | AnalysisResult.status | No hypotheses possible |
| `AES-007` | `TRANSLATION_FAILED` | IntegrationResult.status | Adapter couldn't translate |
| `AES-008` | `UNKNOWN_SQO` | IntegrationResult.status | Evidence references unknown SQO |
| `AES-009` | `VALIDATION_FAILED` | IntegrationResult.status | Evidence failed validation |
| `AES-010` | `DUPLICATE_EVIDENCE` | IntegrationResult.status | SQO already fulfilled |
| `AES-011` | `EVIDENCE_CONFLICT` | IntegrationResult.status | New evidence contradicts existing |

**Error Response Structure:**

```json
{
  "@type": "AnalysisResult",
  "status": "error",
  "error": {
    "code": "AES-001",
    "name": "INVALID_GAP_EVENT",
    "message": "GapEvent missing required field: missingPredicates",
    "details": { "field": "missingPredicates" }
  },
  "hypotheses": [],
  "sqos": []
}
```

### Appendix C: Migration from v1.x / v2.0

| v1.x / v2.0 | v2.1 | Migration |
|-------------|------|-----------|
| `processingMetadata.durationMs` | Host-supplied | Remove internal timing; hosts attach externally |
| Implicit hypothesis identity | `canonicalKey` field | Add canonicalKey to hypothesis schema |
| Implicit SQO identity | `canonicalKey` field | Add canonicalKey to SQO schema |
| Unspecified contradiction threshold | `annihilationThreshold` | Add to scoring profiles |
| Errors thrown | Errors in result.status | Change error handling to return, not throw |

### Appendix D: Scaled Deployment Patterns (Non-Normative)

Hosts MAY implement enterprise patterns. These are **not required for conformance**.

**D.1 Distributed State (Redis)**

```javascript
class RedisStateProvider {
  async load(sagaId) {
    return JSON.parse(await redis.get(`aes:state:${sagaId}`));
  }
  async save(sagaId, state) {
    await redis.set(`aes:state:${sagaId}`, JSON.stringify(state));
  }
}
```

**D.2 Circuit Breaker**

```javascript
class CircuitBreaker {
  isOpen(source) { /* ... */ }
  recordSuccess(source) { /* ... */ }
  recordFailure(source) { /* ... */ }
}
```

**D.3 Message Queue SQO Fulfillment**

```javascript
class KafkaSQOFulfiller {
  async fulfill(sqo) {
    await producer.send({ topic: 'sqo-requests', messages: [sqo] });
    return waitForResponse(sqo['@id']);
  }
}
```

---

## Document Control

| Attribute | Value |
|-----------|-------|
| **Version** | 2.1.0 |
| **Status** | PROPOSED |
| **Authors** | Aaron / Claude |
| **Created** | 2026-02-02 |

### Change Summary: v2.0 → v2.1

| Issue | Resolution | Section |
|-------|------------|---------|
| Time/determinism tension | Temporal Purity rule; processingMetadata is host-supplied | §2.7 |
| Statistical mode data source | Must be explicit in State/Config | §6.3 |
| MDRE ↔ AES loop semantics | Orchestration Boundaries rule; AES never self-invokes | §2.8 |
| Hypothesis identity undefined | canonicalKey + de-duplication rules | §8.5 |
| Contradiction threshold undefined | annihilationThreshold in scoring profiles | §8.2 |
| SQO idempotency undefined | canonicalKey + idempotency rules | §9.4 |
| Metrics could influence reasoning | Metrics Isolation rule | §12.4 |
| Promotion assumption implicit | Explicit rule: AES assumes L3 until evidence | §4.1 |
| Error surfacing undefined | Errors in result.status, not thrown | §17.2 |
| "Service" terminology confusion | Clarifying note in §1.2 | §1.2 |

### Design Principles

1. **Edge as default truth** — If it works in a browser, it works everywhere
2. **Pure function over explicit state** — Deterministic, testable, replayable
3. **Declarative intent** — AES says what, host decides how
4. **JSON-LD canonical** — Semantic, web-native, serializable
5. **Offline-first** — Graceful degradation, not failure
6. **Metrics are observational** — They record, they don't influence (v2.1)
7. **Hosts orchestrate** — AES is passive; loops are external (v2.1)

---

*End of Specification*
