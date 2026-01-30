# Programming Function Classification Framework (PFCF)

**Version:** 2.1  
**Status:** Normative Specification  
**Effective Date:** 2026-01-26  
**Supersedes:** PFCF v2.0  

---

## Abstract

The Programming Function Classification Framework (PFCF) provides a stable, language- and vendor-neutral declarative capability model for programming functions. Analogous to the APQC Process Classification Framework for business processes, PFCF enables composability, governance, auditability, and cross-disciplinary understanding of modern software systems, including AI-enabled and autonomous agent architectures.

---

## 1. Positioning and Scope

### 1.1 What PFCF Is

PFCF v2.1 is a semantic declaration framework that defines functions by their declared intent, behavioral guarantees, and operational constraints rather than by implementation details. It serves as:

- A **governance surface** for policy-aware orchestration and audit
- A **semantic contract** between developers, orchestrators, and auditors
- A **bridge** between business process models (e.g., APQC PCF) and executable systems
- A **foundation** for AI tool-call governance and autonomous agent coordination

### 1.2 What PFCF Is Not

PFCF does not attempt to classify every utility function or internal helper. It is designed for:

- Governed, distributed, or AI-enabled systems where function behavior has compliance, safety, or cost implications
- Functions that cross trust boundaries, persist state, or invoke external resources
- Orchestrated workflows where behavioral composition must be validated

Simple, internal, pure utility functions (e.g., string formatting, mathematical operations) may be classified but do not require PFCF declarations unless they participate in governed workflows.

### 1.3 Structural Alignment with APQC

| APQC Concept | PFCF Analog |
|--------------|-------------|
| Process Category | Function Domain (Level 0) |
| Process Group | Semantic Function Class (Level 1) |
| Activity / Task | Function Pattern or Implementation |
| KPI | Behavioral Guarantee (Level 2) |
| Control | Operational Constraint (Level 3) |

### 1.4 Normative Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119.

---

## 2. Level 0: Computational Intent Domains

### 2.1 Intent Declaration Rules

1. A function SHALL declare exactly one **Primary Intent**.
2. A function MAY declare ordered **Secondary Intents**.
3. Decomposition requirements vary by intent domain (see Section 7).
4. Intent domains are mutually exclusive at the primary level.
5. **Governance Primacy Rule (NEW):** When a function's purpose is to enforce, detect, or attest to policy—even if it also observes, persists, or communicates—**Govern (6.0) MUST be declared as Primary Intent**. This prevents recursive classification ambiguity in registries.

### 2.2 Domain Definitions

| Code | Domain | Description |
|------|--------|-------------|
| 0.0 | Observe | Acquire ephemeral, external, or volatile signals without modifying source state |
| 1.0 | Transform | Change representation, structure, or meaning of data |
| 2.0 | Decide | Evaluate, classify, or select among alternatives based on criteria |
| 3.0 | Persist | Interact with durable state (read or write) |
| 4.0 | Communicate | Exchange information across trust or system boundaries |
| 5.0 | Coordinate | Manage ordering, time, concurrency, or actor interactions |
| 6.0 | Govern | Enforce, detect, or attest to policy and constraints |
| 7.0 | Describe-Retrospective | Produce metadata, explanations, or records about past events |
| 8.0 | Describe-Prospective | Model, simulate, or predict future or hypothetical states |

### 2.3 Intent Selection Decision Guide

The following decision tree resolves ambiguous classification cases:

```
START: What is the function's PRIMARY PURPOSE?

Q1: Does the function enforce, detect, or attest to policy/constraints?
    YES → Primary Intent: Govern (6.0)
          (Even if it also logs, persists, or communicates)
    NO  → Continue to Q2

Q2: Does the function write to or read from durable storage as its main job?
    YES → Primary Intent: Persist (3.0)
    NO  → Continue to Q3

Q3: Does the function send/receive data across a trust or system boundary?
    YES → Primary Intent: Communicate (4.0)
    NO  → Continue to Q4

Q4: Does the function manage timing, ordering, or coordination of other operations?
    YES → Primary Intent: Coordinate (5.0)
    NO  → Continue to Q5

Q5: Does the function make a choice, classification, or routing decision?
    YES → Primary Intent: Decide (2.0)
    NO  → Continue to Q6

Q6: Does the function acquire external or volatile signals?
    YES → Primary Intent: Observe (0.0)
    NO  → Continue to Q7

Q7: Does the function produce records about PAST events?
    YES → Primary Intent: Describe-Retrospective (7.0)
    NO  → Continue to Q8

Q8: Does the function model, simulate, or predict FUTURE states?
    YES → Primary Intent: Describe-Prospective (8.0)
    NO  → Primary Intent: Transform (1.0)
```

### 2.4 Edge Case Clarifications

| Pattern | Primary Intent | Rationale |
|---------|---------------|-----------|
| Cache-backed read | Persist (3.0) | Durable state interaction is the primary behavior |
| Audit logger | Govern (6.0) | Policy attestation is the purpose; persistence is incidental |
| Health check endpoint | Observe (0.0) | Acquires system state; communication is the transport |
| Rate limiter | Govern (6.0) | Enforces policy constraint |
| Event subscriber that writes to DB | Persist (3.0) | The write is the purpose; observation is acquisition |
| ML inference endpoint | Decide (2.0) | Classification/inference is the purpose |
| Retry wrapper | Coordinate (5.0) | Manages execution ordering |

---

## 3. Level 1: Semantic Function Classes

### 3.0 Observe Classes

The Observe domain acquires signals from external or volatile sources without modifying source state.

| Class | Description | Governance Notes |
|-------|-------------|------------------|
| Poll | Periodically query a source for current state | May have rate-limiting implications |
| Subscribe | Register for push-based event delivery | Requires connection lifecycle management |
| Sample | Capture point-in-time snapshot from continuous signal | Timing accuracy may be critical |
| Probe | Actively test or interrogate a system to elicit response | May trigger defensive responses |
| Stream | Continuously ingest an ordered flow of data | Requires backpressure handling |
| Intercept | Capture data in transit without being intended recipient | **Requires explicit authorization** |

### 3.1 Transform Classes

| Class | Description |
|-------|-------------|
| Parse | Convert unstructured or semi-structured input to structured form |
| Normalize | Standardize format, encoding, or representation |
| Convert | Transform between equivalent representations |
| Enrich | Add derived or external information |
| Aggregate | Combine multiple items into summary form |
| Filter | Select subset based on criteria |
| Reduce | Collapse structure while preserving essential information |
| Compose | Combine components into larger structure |
| Generate | Produce synthetic or hypothetical data |
| Decompose | Break complex structure into constituent parts |

### 3.2 Decide Classes

| Class | Description |
|-------|-------------|
| Validate | Check conformance to schema, constraint, or expectation |
| Classify | Assign to one or more categories |
| Compare | Evaluate relative properties between items |
| Rank | Order items by one or more criteria |
| Select | Choose one or more items from a set |
| Route | Determine destination or path based on criteria |
| Infer | Derive conclusions from available evidence |
| Score | Assign numeric or ordinal value based on criteria |
| Threshold | Determine whether a value exceeds a boundary |

### 3.3 Persist Classes

| Class | Description |
|-------|-------------|
| Create | Establish new durable record |
| Retrieve | Read existing durable record |
| Update | Modify existing durable record |
| Delete | Remove durable record |
| Archive | Move to long-term or cold storage |
| Restore | Recover from archive or backup |
| Transact | Execute multiple operations atomically |

### 3.4 Communicate Classes

| Class | Description |
|-------|-------------|
| Request | Initiate interaction expecting response |
| Respond | Reply to a received request |
| Notify | Send one-way information without expecting response |
| Publish | Broadcast to multiple potential recipients |
| Negotiate | Exchange messages to establish agreement |
| Relay | Forward information between parties |

### 3.5 Coordinate Classes

| Class | Description |
|-------|-------------|
| Schedule | Arrange future execution |
| Orchestrate | Direct sequence of multiple operations |
| Synchronize | Align state or timing across actors |
| Lock | Acquire exclusive access to resource |
| Retry | Re-attempt failed operation |
| Compensate | Reverse or mitigate effects of prior operation |
| Distribute | Partition work across multiple executors |
| Await | Suspend until condition is met |

### 3.6 Govern Classes

#### 3.6.1 Preventative Governance (Pre-action)

| Class | Description |
|-------|-------------|
| Authenticate | Verify claimed identity |
| Authorize | Verify permission for requested action |
| Rate-Limit | Constrain frequency or volume of operations |
| Enforce | Apply policy constraint to proposed action |
| Sanitize | Remove or neutralize potentially harmful content |
| Validate-Policy | Check proposed action against policy rules |

#### 3.6.2 Detective Governance (Post-action)

| Class | Description |
|-------|-------------|
| Audit | Record action for compliance review |
| Trace-Attest | Cryptographically attest to execution sequence |
| Alert | Notify when policy violation detected |
| Reconcile | Compare actual state against expected state |

### 3.7 Describe-Retrospective Classes

| Class | Description |
|-------|-------------|
| Log | Record event or state for operational visibility |
| Trace | Record execution path or causation chain |
| Explain | Produce human-readable justification for prior action |
| Document | Generate persistent reference material |
| Summarize | Produce condensed representation of historical data |

### 3.8 Describe-Prospective Classes

| Class | Description |
|-------|-------------|
| Model | Construct representation of system or phenomenon |
| Simulate | Execute model to evaluate hypothetical scenarios |
| Predict | Estimate future state based on current evidence |
| Forecast | Project trends over time horizon |
| Plan | Generate sequence of actions to achieve goal |

---

## 4. Level 2: Behavioral Guarantees

### 4.1 Determinism and Effects

| Guarantee | Definition |
|-----------|------------|
| Pure | Output depends only on input; no side effects |
| Referentially Transparent | Can be replaced by its result without changing program behavior |
| Side-Effecting (Scoped) | Modifies state within declared boundary |
| Side-Effecting (Global) | May modify state outside declared boundary |
| Non-Deterministic | May produce different outputs for identical inputs |

### 4.2 Temporal Behavior

| Guarantee | Definition |
|-----------|------------|
| Instantaneous | Completes within negligible time bound |
| Bounded Latency | Completes within declared maximum duration |
| Long-Running | May exceed typical request timeout; requires progress tracking |
| Eventual | Will complete but without time guarantee |

### 4.3 Algebraic Properties

| Property | Definition | Implication |
|----------|------------|-------------|
| Idempotent | Repeated execution yields same result as single execution | Safe to retry |
| Commutative | Order of operations does not affect result | Parallelizable |
| Associative | Grouping of operations does not affect result | Distributable |
| Invertible | Operation can be reversed to restore prior state | Compensatable |

#### 4.3.1 Idempotency Qualifiers

Because idempotency manifests differently across contexts, PFCF v2.1 requires explicit qualifiers:

| Qualifier | Definition |
|-----------|------------|
| Strict | Identical bitwise output for identical input |
| Logical | Equivalent logical state after repeated execution (may differ in timestamps, IDs) |
| Effect | Same observable external effect (may differ in internal representation) |
| None | Not idempotent; repeated execution may yield different results |

### 4.4 Failure Semantics

| Semantic | Definition | Recovery Implication |
|----------|------------|---------------------|
| Total | Always returns a result for valid input | No error handling required |
| Partial | May fail for some valid inputs | Caller must handle failure |
| Retryable | Failure may succeed on retry without modification | Retry logic appropriate |
| Compensatable | Effects can be reversed after failure | Saga pattern applicable |
| Irreversible | Effects cannot be undone | Pre-validation critical |

### 4.5 Epistemic Properties

PFCF v2.1 uses a two-axis model that separates uncertainty type from reproducibility.

#### 4.5.1 Uncertainty Type

| Type | Definition | Example |
|------|------------|---------|
| Deterministic | Output is fully determined by input | Hash function |
| Aleatory | Output involves genuine randomness | Monte Carlo simulation |
| Epistemic | Output reflects model uncertainty or incomplete knowledge | LLM inference |
| Mixed | Both aleatory and epistemic uncertainty present | Bayesian inference with sampling |

#### 4.5.2 Reproducibility

| Type | Definition | Example |
|------|------------|---------|
| Reproducible | Same input always yields same output | Pure function |
| Reproducible-Seeded | Same input with same seed yields same output | Monte Carlo with fixed seed |
| Non-Reproducible-Stable | Different outputs but within predictable bounds | LLM with temperature > 0 |
| Non-Reproducible-Volatile | Output depends on external state that may change | Database query against live data |

#### 4.5.3 Confidence Scoring

When a function produces confidence-scored output, the score semantics SHALL be declared:

| Semantic | Definition |
|----------|------------|
| Calibrated-Probability | Score represents calibrated probability (sum to 1, frequentist interpretation valid) |
| Uncalibrated-Probability | Score is probability-like but not calibrated |
| Ranking | Score is ordinal; only relative comparisons are meaningful |
| Arbitrary | Score has implementation-specific meaning |
| None | No confidence information provided |

### 4.6 Resource and Cost Intent

These declarations serve dual purposes: informational for documentation and **enforceable** for orchestration.

#### 4.6.1 Computational Complexity Intent

| Intent | Interpretation |
|--------|---------------|
| Constant | Resource usage does not scale with input size |
| Linear | Resource usage scales proportionally with input size |
| Superlinear | Resource usage grows faster than input size |
| Unbounded | Resource usage cannot be predicted from input size |

#### 4.6.2 Financial Cost Intent

| Intent | Interpretation |
|--------|---------------|
| None | No direct financial cost |
| Fixed | Cost is constant regardless of usage |
| Per-Call | Cost scales with invocation count |
| Per-Unit | Cost scales with declared unit (tokens, bytes, records) |
| Variable | Cost depends on external factors (market rates, demand pricing) |

#### 4.6.3 Cost Enforcement (NEW in v2.1)

Cost intent declarations are **enforceable constraints** when the `costEnforcement` field is set:

| Enforcement Level | Behavior |
|-------------------|----------|
| Informational | Declaration is for documentation only |
| Advisory | Orchestrator SHOULD respect limits; violations logged |
| Enforced | Orchestrator MUST respect limits; violations blocked |
| Circuit-Breaking | Orchestrator MUST halt workflow if cost threshold exceeded |

**Declaration Example:**
```yaml
costIntent:
  financial: Per-Call
  budget:
    maxPerCall: 0.05
    maxPerMinute: 1.00
    currency: USD
  enforcement: Circuit-Breaking
```

Orchestrators implementing Level 2 Behavioral Conformance (see Section 9) MUST honor `Enforced` and `Circuit-Breaking` cost constraints.

#### 4.6.4 Custom Cost Extensions

Implementations MAY extend the cost vocabulary via the `costIntent.custom` field:

```yaml
costIntent:
  financial: Per-Unit
  custom:
    energy: moderate
    tokenBudget: 4096
    apiTier: premium
```

Custom fields are implementation-specific and not validated by the core schema.

---

## 5. Level 3: Operational Constraints

| Constraint | Values |
|------------|--------|
| Resource Scope | CPU, Memory, Network, Accelerator, Storage |
| State Scope | Local (function-private), Shared (process/container), Durable (persisted) |
| Trust Boundary | Same-Process, Same-Host, Same-Network, Cross-Network, Cross-Organization |
| Audit Requirement | None, Best-Effort, Mandatory, Immutable |
| Regulatory Sensitivity | None, Low, Moderate, High, Critical |
| Data Classification | Public, Internal, Confidential, Restricted |

### 5.1 Trust Boundary Semantics

Trust boundaries determine where additional governance is required:

| Boundary | Implication |
|----------|-------------|
| Same-Process | No serialization, direct memory access, implicit trust |
| Same-Host | IPC required, shared kernel, moderate trust |
| Same-Network | Network protocol required, organizational trust assumed |
| Cross-Network | Internet protocol, authentication required |
| Cross-Organization | External party, contracts and SLAs apply |

---

## 6. Behavioral Guarantee Compatibility

When functions are composed, their behavioral guarantees must be compatible. PFCF v2.1 defines explicit compatibility rules.

### 6.1 Determinism Compatibility Matrix

When function A calls function B, the composed result has the determinism of the weaker guarantee:

| A \ B | Pure | Ref-Trans | Side-Eff (S) | Side-Eff (G) | Non-Det |
|-------|------|-----------|--------------|--------------|---------|
| **Pure** | Pure | Ref-Trans | **INVALID** | **INVALID** | **INVALID** |
| **Ref-Trans** | Ref-Trans | Ref-Trans | Side-Eff (S) | **INVALID** | Non-Det |
| **Side-Eff (S)** | Side-Eff (S) | Side-Eff (S) | Side-Eff (S) | **INVALID** | Non-Det |
| **Side-Eff (G)** | Side-Eff (G) | Side-Eff (G) | Side-Eff (G) | Side-Eff (G) | Non-Det |
| **Non-Det** | Non-Det | Non-Det | Non-Det | Non-Det | Non-Det |

**INVALID** compositions are prohibited. A Pure function calling a Side-Effecting function is a declaration violation.

### 6.2 Idempotency Composition Rules

1. Strict + Strict = Strict
2. Strict + Logical = Logical
3. Logical + Logical = Logical
4. Any + Effect = Effect
5. Any + None = None (unless orchestration provides idempotency guarantee)

### 6.3 Failure Semantic Compatibility

Downstream failure semantics must be equal or stronger than upstream requirements:

| Upstream Expects | Downstream Must Be |
|------------------|-------------------|
| Total | Total only |
| Partial | Total or Partial |
| Retryable | Total, Partial, or Retryable |
| Compensatable | Total, Partial, Retryable, or Compensatable |
| Irreversible | Any |

### 6.4 Epistemic Composition

When composing functions with different epistemic properties:

- **Uncertainty propagates:** Deterministic + Epistemic = Epistemic
- **Reproducibility degrades:** Reproducible + Non-Reproducible = Non-Reproducible
- **Confidence scores do not compose automatically;** explicit aggregation logic required
- When combining Aleatory and Epistemic uncertainty, the result is Mixed

### 6.5 Cost Composition

When composing functions with cost declarations:

- **Per-Call costs accumulate** across the call chain
- **Per-Unit costs** require explicit unit mapping between functions
- **Variable costs** propagate: any Variable dependency makes the composition Variable
- **Budget enforcement** applies at the declared enforcement boundary

---

## 7. Composition and Decomposition Rules

### 7.1 Decomposition Thresholds

Decomposition requirements indicate when a composite function must be broken into separately-governed components:

| Intent Domain | Decomposition Requirement | Rationale |
|---------------|--------------------------|-----------|
| Govern (6.0) | Mandatory | Governance logic must be independently auditable |
| Persist (3.0) | Mandatory | State changes require explicit transaction boundaries |
| Communicate (4.0) | Mandatory | Cross-boundary operations require distinct failure handling |
| Decide (2.0) | Recommended | Decision logic benefits from separate testing and explanation |
| Coordinate (5.0) | Recommended | Orchestration logic should be visible for debugging |
| Observe (0.0) | Conditional | Required if crossing trust boundaries; optional otherwise |
| Transform (1.0) | Optional | May remain composed unless governance requires visibility |
| Describe-Retrospective (7.0) | Optional | May be composed unless audit requires separate attestation |
| Describe-Prospective (8.0) | Recommended | Simulation/prediction logic benefits from isolation |

### 7.2 Decomposition Waiver (NEW in v2.1)

A function MAY waive mandatory decomposition requirements under the following conditions:

1. **Explicit Intent Ordering:** All constituent intents MUST be declared with their execution order
2. **Justification:** A rationale MUST be provided explaining why decomposition is impractical
3. **Compensating Controls:** Alternative governance mechanisms MUST be documented
4. **Conformance Level:** Functions with waivers cannot achieve Level 3 (Governance Conformance)

**Waiver Declaration Example:**
```yaml
decomposition:
  required: true
  waived: true
  waiverJustification: >
    Legacy get-or-create pattern with sub-millisecond latency requirement.
    Decomposition would add 3ms network overhead per call.
  compensatingControls:
    - Comprehensive integration test suite with 98% coverage
    - Runtime monitoring for all state transitions
    - Quarterly audit review of composite behavior
  intentOrdering:
    - Retrieve (Persist)
    - Validate (Decide)
    - Create (Persist)
  maxConformanceLevel: 2
```

### 7.3 Governance Precedence Rules

#### 7.3.1 Preventative Governance

- Authenticate MUST precede Authorize
- Authorize MUST precede Persist or Communicate
- Sanitize SHOULD precede Transform when input is untrusted
- Rate-Limit MAY occur at any point but is typically first

#### 7.3.2 Detective Governance

- Audit MAY occur during or after execution
- Trace-Attest SHOULD occur after completion for integrity
- Alert MUST occur when policy violation is detected

### 7.4 Composite Function Declaration

Functions that combine multiple intents must declare:

1. All constituent intents with their order
2. Whether decomposition requirements are met or waived
3. Justification for any waived decomposition requirements
4. The resulting behavioral guarantees after composition

---

## 8. Machine-Readable Declaration Schema

### 8.1 YAML Declaration Format

The following example demonstrates a complete PFCF v2.1 declaration:

```yaml
pfcf:
  version: "2.1"
  function: getOrCreateUserProfile
  
  # Intent Declaration
  primaryIntent: Persist
  secondaryIntents:
    - Observe
    - Transform
    - Decide
  classes:
    - Retrieve
    - Create
    - Validate
  
  # Behavioral Guarantees (Level 2)
  behavior:
    determinism: Side-Effecting
    effectScope: Scoped
    idempotency:
      type: Logical
      note: "Returns same user for same ID; timestamps may differ"
    failure: Retryable
    temporal: Bounded
    latencyBound: "500ms"
  
  # Epistemic Properties
  epistemic:
    uncertaintyType: Deterministic
    reproducibility: Non-Reproducible-Volatile
    confidenceScoring: None
  
  # Cost Intent (with enforcement)
  costIntent:
    computational: Linear
    financial: Per-Call
    budget:
      maxPerCall: 0.001
      currency: USD
    enforcement: Advisory
  
  # Operational Constraints (Level 3)
  constraints:
    trustBoundary: Same-Network
    auditRequirement: Mandatory
    dataClassification: Confidential
    regulatorySensitivity: Moderate
  
  # Decomposition
  decomposition:
    required: true
    waived: true
    waiverJustification: >
      High-frequency user lookup with create-on-miss semantics.
      Decomposition would double latency for 99.7% of calls (existing users).
    compensatingControls:
      - Atomic database transaction wrapper
      - Comprehensive audit logging of all creates
      - Daily reconciliation job
    intentOrdering:
      - Retrieve (Persist)
      - Validate (Decide)
      - Create (Persist)
    maxConformanceLevel: 2
  
  # Metadata
  metadata:
    owner: user-service-team
    version: "3.2.1"
    lastReviewed: "2026-01-15"
    tags:
      - user-management
      - critical-path
```

### 8.2 JSON Schema Location

The canonical JSON Schema for PFCF v2.1 declarations is available at:

```
https://pfcf.io/schema/v2.1/declaration.json
```

### 8.3 Schema Validation Requirements

Conforming implementations SHALL validate:

1. Exactly one `primaryIntent` from the defined domain list
2. All `classes` are valid for their declared intents
3. Behavioral guarantees are internally consistent (no Pure function with Side-Effecting dependencies)
4. Decomposition requirements are met or explicitly waived with justification
5. Idempotency qualifiers are provided when idempotency is claimed
6. Cost enforcement level is specified when budget constraints are declared
7. Waived decompositions include all required fields

---

## 9. Conformance Levels

PFCF v2.1 defines three conformance levels to accommodate different deployment contexts:

### 9.1 Level 1: Declaration Conformance

A function is **Declaration Conformant** if it includes a syntactically valid PFCF declaration that passes schema validation. This level is suitable for documentation and catalog purposes.

**Requirements:**
- Valid YAML/JSON syntax
- All required fields present
- Field values from defined vocabularies
- No schema violations

### 9.2 Level 2: Behavioral Conformance

A function is **Behavioral Conformant** if its runtime behavior matches its declaration. This requires:

- Test suites that verify declared guarantees
- Static analysis where applicable
- Runtime monitoring for non-deterministic properties
- **Cost enforcement** for `Advisory`, `Enforced`, and `Circuit-Breaking` declarations

**Verification Methods:**

| Guarantee | Verification Approach |
|-----------|----------------------|
| Idempotency (Strict) | Property-based testing with identical inputs |
| Idempotency (Logical) | State comparison after repeated execution |
| Failure Semantics | Fault injection testing |
| Temporal Bounds | Latency percentile monitoring |
| Cost Limits | Budget tracking and alerting |

### 9.3 Level 3: Governance Conformance

A function is **Governance Conformant** if it meets all requirements for regulated deployment:

- Full decomposition where required (no waivers)
- Audit trails for all governed operations
- Cryptographic attestation where specified
- Compliance with all composition rules
- Independent audit verification

**Note:** Functions with decomposition waivers are limited to Level 2 conformance maximum.

---

## 10. Implementation Guidance

### 10.1 Registry Integration

PFCF declarations SHOULD be stored in a searchable registry that supports:

- Query by intent domain and class
- Filtering by behavioral guarantees
- Composition compatibility checking
- Cost aggregation for workflows

### 10.2 Orchestrator Integration

Orchestrators implementing PFCF awareness SHOULD:

1. Validate composition compatibility before execution
2. Enforce cost budgets at declared enforcement levels
3. Propagate epistemic properties through call chains
4. Log composition decisions for audit

### 10.3 CI/CD Integration

Build pipelines SHOULD:

1. Validate PFCF declarations against schema
2. Check for breaking changes in behavioral guarantees
3. Verify decomposition requirements are met or properly waived
4. Generate compatibility reports for dependent functions

---

## 11. Roadmap

The following capabilities are planned for future versions:

- **v2.2:** JSON-LD canonical schema with full semantic web binding
- **v2.3:** OWL/RDF ontology for automated reasoning
- **v2.4:** APQC PCF bidirectional reference mappings
- **v3.0:** Function lineage and provenance model with cryptographic verification

**Tooling Roadmap:**

- Static validators for TypeScript, Python, Java, Go
- Runtime compliance monitors (OpenTelemetry integration)
- IDE plugins for declaration authoring and validation
- Registry reference implementation

---

## Appendix A: Migration from v2.0

### A.1 Non-Breaking Additions

The following fields are new in v2.1 but optional:

- `costIntent.budget`
- `costIntent.enforcement`
- `decomposition.waiverJustification`
- `decomposition.compensatingControls`
- `decomposition.intentOrdering`
- `decomposition.maxConformanceLevel`

### A.2 Semantic Clarifications

The following clarifications do not change schema but affect interpretation:

1. **Governance Primacy Rule:** Audit functions MUST declare Govern as primary intent
2. **Cost Enforcement:** Cost declarations can now be enforceable, not just informational
3. **Waiver Mechanism:** Decomposition can be waived with proper documentation

### A.3 Recommended Updates

Existing v2.0 declarations SHOULD be updated to:

1. Add `enforcement: Informational` to cost declarations for explicit semantics
2. Review functions that might be misclassified under Governance Primacy Rule
3. Document decomposition waivers for legacy composite functions

---

## Appendix B: Observe Domain Design Rationale

### B.1 Acquisition Mode Taxonomy

Observe classes differ along three axes:

| Class | Initiation | Timing | Source Relationship |
|-------|------------|--------|---------------------|
| Poll | Pull | Point | Direct |
| Subscribe | Push | Continuous | Direct |
| Sample | Pull | Point | Direct |
| Probe | Pull | Point | Direct (interrogative) |
| Stream | Push | Continuous | Direct |
| Intercept | Push | Continuous | Indirect |

### B.2 Governance Implications

Different Observe classes have different governance requirements:

- **Intercept** requires explicit authorization due to indirect acquisition
- **Subscribe** and **Stream** require connection lifecycle management
- **Poll** and **Sample** may have rate-limiting implications
- **Probe** may trigger defensive responses from target systems

---

## Appendix C: Intent Decision Examples

### C.1 Worked Example: Audit Logger

**Function:** Writes security events to compliance database

**Decision Process:**
1. Q1: Does it enforce/detect/attest to policy? **YES** (attestation for compliance)
2. Result: **Primary Intent = Govern (6.0)**
3. Secondary Intents: Persist (writes to DB)
4. Classes: Audit

**Why not Persist?** The *purpose* is compliance attestation. The database write is the *mechanism*, not the goal.

### C.2 Worked Example: Cache-Backed User Lookup

**Function:** Returns user from Redis cache, falls back to PostgreSQL

**Decision Process:**
1. Q1: Policy enforcement? **NO**
2. Q2: Durable storage as main job? **YES** (reading user records)
3. Result: **Primary Intent = Persist (3.0)**
4. Classes: Retrieve

**Why not Observe?** The cache is an optimization detail. The function's contract is "get user record from durable storage."

### C.3 Worked Example: ML Inference API

**Function:** Accepts image, returns classification with confidence score

**Decision Process:**
1. Q1: Policy enforcement? **NO**
2. Q2: Durable storage? **NO**
3. Q3: Cross-boundary communication? **NO** (the API boundary is transport, not the function's purpose)
4. Q4: Coordination? **NO**
5. Q5: Makes classification decision? **YES**
6. Result: **Primary Intent = Decide (2.0)**
7. Classes: Classify, Score
8. Epistemic: Epistemic uncertainty, Calibrated-Probability confidence

---

## Appendix D: Glossary

| Term | Definition |
|------|------------|
| Aleatory Uncertainty | Uncertainty arising from inherent randomness |
| Behavioral Conformance | Runtime behavior matches declaration |
| Compensating Control | Alternative governance mechanism when decomposition is waived |
| Declaration Conformance | Syntactically valid PFCF declaration |
| Decomposition | Breaking composite function into separately-governed components |
| Epistemic Uncertainty | Uncertainty arising from incomplete knowledge |
| Governance Conformance | Full compliance with all governance requirements |
| Governance Primacy | Rule that Govern intent takes precedence in classification |
| Primary Intent | The single main purpose of a function |
| Secondary Intent | Additional intents that support the primary purpose |
| Trust Boundary | Demarcation between security/trust domains |
| Waiver | Documented exception to decomposition requirement |

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 2.1 | 2026-01-26 | Added Governance Primacy Rule, Intent Decision Guide, Decomposition Waiver mechanism, Cost Enforcement levels |
| 2.0 | 2026-01-26 | Hardened specification with Observe classes, Describe split, Epistemic model, Compatibility matrices |
| 1.2 | 2025-12-15 | Pilot-ready draft |
| 1.0 | 2025-10-01 | Initial taxonomy |

---

**PFCF v2.1 Status:** Normative specification for governed, AI-enabled, and distributed systems.

**Copyright:** This specification is released under Creative Commons Attribution 4.0 International (CC BY 4.0).
