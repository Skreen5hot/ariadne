# APQC → SFS Execution Specification

**Semantic Compilation of Descriptive Process Models into Executable Capabilities**

| Field | Value |
|-------|-------|
| Version | 2.0 |
| Status | Hardened Specification |
| Supersedes | v1.0, v1.1 |
| Effective Date | 2026-01-31 |

## Applies To

- SFS v2.2 and later
- Ralph Wiggum Deterministic Control Loop
- APQC Process Classification Framework (PCF), any versioned release

---

## Document Conventions

The keywords "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119.

Schema definitions use YAML for readability. Normative schemas are provided in Appendix A (JSON Schema) and Appendix B (OWL/RDF).

---

## 1. Purpose

This specification defines a deterministic, auditable, subtractive system for compiling descriptive enterprise process models (APQC PCF) into bounded, executable semantic capabilities (SFS).

The system produces explicit execution artifacts that define what an autonomous or semi-autonomous role can do, what it cannot do, how it executes logic, and where execution must stop or defer to a human.

The specification addresses four architectural concerns: capability derivation from descriptive models, execution safety through explicit constraint, state management across execution cycles, and responsibility attribution for audit and compliance.

---

## 2. Non-Goals (Normative Safety Constraints)

The system MUST NOT:

1. Treat APQC processes as executable workflows
2. Infer ordering, authority, or intent not explicitly supported by validated confidence scoring
3. Invent missing capabilities to satisfy execution
4. Execute actions without explicit invocation and permission context
5. Perform subjective, empathetic, or ethical judgment autonomously
6. Self-modify capability definitions at runtime
7. Escalate privilege without explicit human authorization

The system is safe by default because it begins with zero capability and only adds what can be compiled, bound, and validated.

---

## 3. Architectural Overview

### 3.1 The Semantic Compiler Model (Normative)

This system SHALL be understood and implemented as a semantic compiler.

| Layer | Function | Metaphor |
|-------|----------|----------|
| APQC PCF | Intent Source | High-Level Source Code |
| SFS | Capability Vocabulary | Assembly Language |
| Ralph Wiggum Loop | Controlled Synthesis | Semantic Compiler |
| Role Runtime Artifact | Executable Definition | Compiled Binary |

**Key Property:** If the compiler encounters ambiguity, missing capability, or insufficient confidence, it MUST emit an error or warning rather than guessing.

### 3.2 Determinism Definitions (Normative)

This specification distinguishes three forms of determinism:

**Compile-Time Determinism:** Given identical inputs (APQC definitions, SFS registry, configuration) and identical model versions, the compiler MUST produce identical artifacts. This is a strict requirement.

**Runtime Determinism:** Given identical invocation context, session state, and bound tool responses, execution MUST produce identical traces. This is a strict requirement within the system boundary.

**External Variability:** Operations involving external systems (APIs, databases, human responses) are explicitly outside determinism guarantees. Such variability MUST be declared in Context Bindings and MUST NOT affect the determinism of system-internal operations.

---

## 4. Core Components

### 4.1 APQC Semantic Ingest Layer

APQC PCF entries MUST be ingested as Process Intent Objects (PIOs).

```yaml
ProcessIntent:
  apqc_id: "3.4.2"
  label: "Manage employee performance"
  level: 3
  description: "APQC human-readable definition"
  implied_outcomes:
    - performance is evaluated
  implied_inputs:
    - employee data
  constraints:
    - descriptive_only
    - non_executable
  ingest_metadata:
    source_version: "APQC PCF v7.2.1"
    ingest_timestamp: "2026-01-15T09:00:00Z"
    ingest_agent: "compiler-v2.0"
```

No execution semantics SHALL be inferred at this stage.

### 4.2 SFS Capability Registry (Precondition)

The system MUST maintain a registry of domain-agnostic SFS primitives, each with typed inputs and outputs, explicit side-effect declarations, and determinism classification.

```yaml
SFSFunction:
  name: PersistRecord
  version: "1.0.0"
  type: action
  input:
    - name: record
      type: Record
      required: true
  output:
    - name: receipt
      type: PersistenceReceipt
  side_effects:
    - type: persistence
      scope: scoped_to_session
  determinism:
    classification: externally_variable
    rationale: "Persistence layer response timing varies"
  provenance:
    defined_by: "SFS Core Library"
    version: "2.2.0"
```

---

## 5. Ralph Wiggum Compilation Phases

### Phase 1: Intent Decomposition (High-Risk Phase)

For each ProcessIntent, the compiler MUST extract explicitly stated outcomes, propose implied outcomes and inputs, and assign a confidence score to every inferred element.

**Normative Rule:** Any inferred element with confidence below the deployment-configured threshold (see Section 10) MUST be flagged for human review and excluded from executable synthesis until validated.

This phase is expected to produce ambiguity. Ambiguity is not a failure.

```yaml
DecompositionResult:
  source: "APQC:3.4.2"
  explicit_outcomes:
    - label: "performance is evaluated"
      confidence: 1.0
      source: "stated"
  inferred_outcomes:
    - label: "feedback is communicated"
      confidence: 0.72
      source: "inferred"
      validation_state: pending_human_review
  inferred_inputs:
    - label: "performance metrics"
      confidence: 0.88
      source: "inferred"
      validation_state: approved
```

### Phase 2: Capability Matching

For each validated semantic need, the compiler MUST attempt direct SFS primitive matching, then attempt compositional coverage, then emit a CapabilityGap if unresolved.

```yaml
CapabilityGap:
  gap_id: "GAP-2026-0042"
  semantic_need: "Resolve employee dispute"
  reason: "Requires subjective empathy and contextual judgment"
  classification: non_compilable
  recommended_action: human_delegation
  created: "2026-01-15T09:15:00Z"
```

CapabilityGap objects are REQUIRED deliverables. A compilation that produces zero CapabilityGaps for a non-trivial process set SHOULD be reviewed for over-claiming.

### Phase 3: Function Composition

Composite SFS functions MAY be synthesized if and only if all constituent primitives exist in the registry, type compatibility is provable, and side effects are explicitly declared.

```yaml
SFSFunction:
  name: EvaluatePerformance
  version: "1.0.0"
  type: composite
  derived_from: "APQC:3.4.2"
  composition:
    - step: 1
      function: RetrieveMetrics
      input_mapping:
        employee_id: "$input.employee_id"
      output_binding: metrics
    - step: 2
      function: CompareAgainstThreshold
      input_mapping:
        value: "$metrics.score"
        threshold: "$config.performance_threshold"
      output_binding: evaluation
    - step: 3
      function: PersistRecord
      input_mapping:
        record: "$evaluation"
      output_binding: receipt
  determinism:
    classification: externally_variable
    rationale: "Contains PersistRecord which has external variability"
```

Composite functions MUST NOT self-modify, self-invoke, or execute without external trigger.

### Phase 4: Context Binding (Logic-to-Hands)

Context Binding maps abstract SFS functions to concrete tools.

Bindings MUST be explicit, versioned, replaceable, and auditable.

```yaml
ContextBinding:
  binding_id: "BIND-2026-0108"
  function: MeasureValue
  function_version: "1.0.0"
  implementation:
    tool: Workday_API
    tool_version: "v2.3"
    method: GET_worker_metrics
    endpoint: "/workers/{id}/metrics"
  variability:
    classification: external
    timeout_ms: 5000
    retry_policy: exponential_backoff
    max_retries: 3
  created: "2026-01-10T14:00:00Z"
  created_by: "integration-team"
  valid_until: "2027-01-10T14:00:00Z"
```

This phase defines how work happens, not what work means.

### Phase 5: Provenance and Confidence Annotation (Mandatory)

Every function, whether executable or non-executable, MUST include provenance metadata.

```yaml
Provenance:
  source: "APQC:3.4.2"
  compilation_run: "RUN-2026-0015"
  confidence: 0.90
  confidence_method: "ensemble_agreement"
  validation_state: approved
  validated_by: "jane.smith@example.com"
  validated_at: "2026-01-16T10:30:00Z"
```

Functions without approved provenance MUST NOT execute.

---

## 6. Permission Model (Normative)

### 6.1 Permission Schema

Every execution request MUST include a Permission Claim conforming to this schema:

```yaml
PermissionClaim:
  claim_id: "PERM-2026-00892"
  principal:
    type: role | user | service
    identifier: "junior-hr-analyst-role"
  scope:
    functions:
      - "EvaluatePerformance"
      - "RetrieveMetrics"
    data_domains:
      - "employee_performance"
    time_bound:
      not_before: "2026-01-01T00:00:00Z"
      not_after: "2026-12-31T23:59:59Z"
  constraints:
    max_records_per_invocation: 100
    require_audit_log: true
  issuer:
    authority: "hr-permission-service"
    issued_at: "2026-01-01T00:00:00Z"
  signature: "base64-encoded-signature"
```

### 6.2 Permission Verification

The runtime MUST verify permission claims before execution. Verification includes signature validation (claim was issued by trusted authority), scope matching (requested function is within claimed scope), temporal validity (current time is within not_before/not_after), and constraint compliance (request parameters satisfy constraints).

### 6.3 Permission Failure Modes

| Condition | System Response |
|-----------|-----------------|
| Invalid signature | Reject with `PERMISSION_INVALID` |
| Function not in scope | Reject with `PERMISSION_SCOPE_EXCEEDED` |
| Claim expired | Reject with `PERMISSION_EXPIRED` |
| Constraint violated | Reject with `PERMISSION_CONSTRAINT_VIOLATED` |
| Claim missing | Reject with `PERMISSION_REQUIRED` |

Permission failures MUST be logged with full context for audit.

---

## 7. Execution Model

### 7.1 Invocation Rules

No function executes autonomously. Execution requires a trigger (explicit invocation event), valid inputs (type-checked against function signature), permission context (verified PermissionClaim), and active session state (initialized SessionState object).

### 7.2 Execution Path

```
TRIGGER → PERMISSION_CHECK → INPUT_VALIDATION → FUNCTION_EXECUTION → STATE_UPDATE → OUTPUT
```

Any step failure halts execution and emits an appropriate error.

---

## 8. State and Memory Model

### 8.1 Session State Object (Mandatory)

To avoid stateless execution, the system MUST maintain a Session State Object for each execution cycle.

```yaml
SessionState:
  session_id: "SESSION-2026-00421"
  role: "Junior HR Performance Analyst"
  execution_id: "EXEC-9922"
  started_at: "2026-01-20T14:30:00Z"
  data_context:
    employee_id: "EMP-12345"
    review_period: "Q4-2025"
  intermediate_results:
    metrics_retrieved: true
    evaluation_result: "Tier 1"
  audit_trail:
    - timestamp: "2026-01-20T14:30:01Z"
      action: "RetrieveMetrics"
      status: "success"
    - timestamp: "2026-01-20T14:30:02Z"
      action: "CompareAgainstThreshold"
      status: "success"
  permission_claim_id: "PERM-2026-00892"
```

### 8.2 State Guarantees

State MUST persist across the execution path within a session. State MUST be readable by subsequent steps within the same execution. State MUST be auditable and replayable for compliance review. State MUST be isolated between concurrent sessions.

### 8.3 State Persistence

Session state MAY be persisted beyond execution completion for audit purposes. Persistence duration is deployment-configurable but MUST be at least 90 days for compliance.

Without a valid SessionState object, the system SHALL NOT execute any function.

---

## 9. Escalation Model (Normative)

### 9.1 Escalation Triggers

Escalation to human review MUST occur when a CapabilityGap is encountered during execution, when confidence falls below threshold during runtime inference, when permission is ambiguous or contested, or when the function is marked as requiring human approval.

### 9.2 Escalation Request Schema

```yaml
EscalationRequest:
  escalation_id: "ESC-2026-00156"
  session_id: "SESSION-2026-00421"
  reason:
    type: capability_gap | confidence_failure | permission_required | policy_required
    detail: "Function Resolve_Dispute requires subjective judgment"
  context:
    function_attempted: "Resolve_Dispute"
    input_summary: "Employee dispute regarding performance rating"
    state_snapshot:
      employee_id: "EMP-12345"
      dispute_type: "rating_disagreement"
  routing:
    escalation_target: "hr-manager-pool"
    priority: medium
    sla_minutes: 240
  timeout:
    deadline: "2026-01-20T18:30:00Z"
    timeout_action: escalate_further | abort_with_notification
  created_at: "2026-01-20T14:30:05Z"
```

### 9.3 Escalation Timeout Behavior

If escalation is not resolved within the configured SLA, the system MUST perform the configured timeout_action. If timeout_action is `escalate_further`, the system MUST route to a higher-authority escalation target. If timeout_action is `abort_with_notification`, the system MUST terminate the execution path, preserve state for later resumption, and notify all relevant parties.

### 9.4 Escalation Response Schema

```yaml
EscalationResponse:
  escalation_id: "ESC-2026-00156"
  responder:
    identity: "jane.smith@example.com"
    role: "HR Manager"
    verified_at: "2026-01-20T15:45:00Z"
  decision:
    action: approve | reject | delegate | request_more_info
    rationale: "Reviewed dispute details, resolution appropriate"
  engagement_verification:
    time_spent_seconds: 180
    context_accessed:
      - "employee_record"
      - "dispute_history"
    attestation: "I have reviewed the relevant materials"
  response_at: "2026-01-20T15:48:00Z"
```

### 9.5 Engagement Verification

To mitigate rubber-stamping, the system SHOULD track time spent on escalation review, log which context elements were accessed, require explicit attestation for high-stakes decisions, and flag rapid approvals (configurable threshold) for secondary review.

Engagement verification is RECOMMENDED but not REQUIRED for all deployments. High-stakes deployments SHOULD enable full engagement verification.

---

## 10. Confidence Calibration Model (Normative)

### 10.1 Confidence Score Definition

A confidence score represents the compiler's assessed probability that an inferred element correctly captures the intent of the source APQC process.

Confidence scores are NOT: probability of successful execution, user satisfaction likelihood, or general quality assessments.

### 10.2 Confidence Production Methods

The specification supports multiple confidence production methods. Each deployment MUST declare which method is in use.

**Model Output:** Confidence derived from language model probability distributions. Requires calibration against ground truth dataset.

**Ensemble Agreement:** Confidence derived from agreement across multiple independent inference passes. Higher agreement indicates higher confidence.

**Human Rating:** Confidence assigned by human reviewers during validation. Most reliable but least scalable.

**Hybrid:** Combination of methods with explicit weighting.

```yaml
ConfidenceConfiguration:
  method: ensemble_agreement
  parameters:
    ensemble_size: 5
    agreement_threshold: 0.80
    temperature: 0.3
  calibration:
    calibration_dataset: "apqc-validation-set-v2"
    calibration_date: "2025-12-01"
    brier_score: 0.12
    expected_calibration_error: 0.08
  threshold:
    human_review_required: 0.80
    auto_approve: 0.95
```

### 10.3 Threshold Configuration

The confidence threshold for human review (default 0.80) is deployment-configurable. Deployments MUST document their chosen threshold and rationale. Thresholds below 0.70 require explicit safety justification. Thresholds above 0.95 may produce excessive human review load.

### 10.4 Calibration Requirements

Confidence scores MUST be calibrated against a ground truth dataset before production deployment. Calibration SHOULD be re-validated quarterly or when the underlying model changes. Calibration metrics (Brier score, expected calibration error) MUST be documented.

---

## 11. Responsibility Attribution Model (Normative)

### 11.1 Responsibility Layers

The system defines explicit responsibility attribution at each architectural layer.

| Layer | Responsible Party | Responsibility Scope |
|-------|-------------------|---------------------|
| Intent (APQC) | Process Owner | Accuracy of process description |
| Logic (SFS) | Capability Author | Correctness of function definition |
| Compilation | Compiler Operator | Validity of compilation configuration |
| Binding | Integration Author | Correctness of tool binding |
| Execution | Invoking Principal | Appropriateness of invocation |
| Escalation | Human Responder | Quality of escalation decision |

### 11.2 Responsibility Schema

Every artifact MUST include responsibility attribution.

```yaml
ResponsibilityAttribution:
  artifact_id: "FUNC-EvaluatePerformance-v1.0.0"
  layer: logic
  responsible_party:
    identity: "capability-team@example.com"
    role: "Capability Author"
  responsibility_scope: "Correctness of function definition and composition"
  accountability_chain:
    - layer: intent
      party: "hr-process-owner@example.com"
    - layer: logic
      party: "capability-team@example.com"
    - layer: compilation
      party: "compiler-ops@example.com"
  last_reviewed: "2026-01-10T00:00:00Z"
  next_review_due: "2026-04-10T00:00:00Z"
```

### 11.3 Failure Responsibility

When a failure occurs, the audit trail MUST identify which layer failed, which party bears responsibility for that layer, and what the remediation path is.

| Failure Type | Responsible Layer | Remediation Owner |
|--------------|-------------------|-------------------|
| Miscompiled intent | Intent or Compilation | Process Owner or Compiler Operator |
| Function logic error | Logic | Capability Author |
| Binding failure | Binding | Integration Author |
| Inappropriate invocation | Execution | Invoking Principal |
| Poor escalation decision | Escalation | Human Responder |

---

## 12. Role Runtime Artifact (Primary Output)

The compiler SHALL emit a Role Runtime Artifact: a versionable configuration defining the agent's scope of competence.

```yaml
RoleRuntimeArtifact:
  artifact_id: "ROLE-JR-HR-PERF-ANALYST-v1.2.0"
  role: "Junior HR Performance Analyst"
  source_standard: "APQC PCF v7.2.1 – Group 3.4"
  compiled_at: "2026-01-15T10:00:00Z"
  compiled_by: "compiler-v2.0"
  valid_until: "2026-07-15T10:00:00Z"
  
  competencies:
    - function: EvaluatePerformance
      function_version: "1.0.0"
      status: executable
      trust_level: high
      trust_level_definition: "Fully automated, audit logging only"
      triggers:
        - type: scheduled
          schedule: "quarterly_cycle"
        - type: manual
          authorized_roles:
            - "hr-manager"
      constraints:
        max_evaluations_per_cycle: 500
      responsibility:
        layer: logic
        party: "capability-team@example.com"
    
    - function: Resolve_Dispute
      function_version: "1.0.0"
      status: non_executable
      reason:
        type: capability_gap
        gap_id: "GAP-2026-0042"
      fallback:
        action: escalate
        target: "hr-manager-pool"
        sla_minutes: 240
      responsibility:
        layer: escalation
        party: "hr-manager-pool"
  
  capability_gaps:
    - gap_id: "GAP-2026-0042"
      semantic_need: "Resolve employee dispute"
      classification: non_compilable
  
  permission_requirements:
    required_claims:
      - scope: "employee_performance"
      - scope: "hr_actions"
  
  audit_configuration:
    retention_days: 365
    log_level: detailed
```

This artifact is definition, not runtime. It defines what the role can do; actual execution requires invocation with valid permission and state.

### 12.1 Trust Level Definitions

| Trust Level | Definition | Human Involvement |
|-------------|------------|-------------------|
| HIGH | Fully automated execution | Audit logging only |
| MEDIUM | Automated with notification | Human notified post-execution |
| LOW | Automated with approval | Human approval required pre-execution |
| NONE | Not executable | Human must perform action |

---

## 13. Failure Modes (Designed Behavior)

| Condition | System Response | Log Level |
|-----------|-----------------|-----------|
| Ambiguous intent | Emit confidence warning, require human review | WARN |
| Missing capability | Emit CapabilityGap, block compilation | ERROR |
| Unbound context | Block execution, emit binding error | ERROR |
| Policy violation | Require human approval, log violation | WARN |
| Permission denied | Reject execution, log denial | ERROR |
| Escalation timeout | Execute timeout_action, notify parties | ERROR |
| External system failure | Retry per policy, then escalate | WARN/ERROR |

Silent failure is forbidden. Every failure MUST produce a logged, auditable event.

---

## 14. Knowledge Worker Stack (Revised)

| Level | Component | Description | Specification Status |
|-------|-----------|-------------|---------------------|
| 1 | Intent | APQC Process Definition | Defined (Section 4.1) |
| 2 | Logic | SFS Functions | Defined (Section 4.2, 5.3) |
| 3 | Memory | Session State + Persistence | Defined (Section 8) |
| 4 | Hands | Tool Bindings | Contract Defined (Section 5.4) |
| 5 | Permission | Authorization Layer | Defined (Section 6) |
| 6 | Escalation | Human-in-the-Loop | Defined (Section 9) |

Version 2.0 formally defines all six levels.

---

## 15. Operational Reality (Illustrative)

A compiled Role Runtime Artifact, when executed, produces deterministic console behavior—not conversational output:

```
SYSTEM BOOT: Loading Role [Junior HR Performance Analyst]
ARTIFACT VERSION: ROLE-JR-HR-PERF-ANALYST-v1.2.0
VALID UNTIL: 2026-07-15T10:00:00Z

INTEGRITY CHECK:
  [OK] EvaluatePerformance (v1.0.0) - EXECUTABLE
  [OK] RetrieveMetrics (v1.0.0) - EXECUTABLE  
  [SKIP] Resolve_Dispute (v1.0.0) - NON_EXECUTABLE (CapabilityGap: GAP-2026-0042)

SESSION INITIALIZED: SESSION-2026-00421
PERMISSION VERIFIED: PERM-2026-00892

EXECUTING: EvaluatePerformance
  STEP 1: RetrieveMetrics
    INPUT: employee_id=EMP-12345
    OUTPUT: metrics_retrieved=true
    STATE UPDATED: data_context.metrics loaded
  STEP 2: CompareAgainstThreshold
    INPUT: score=87, threshold=80
    OUTPUT: evaluation_result="Tier 1"
    STATE UPDATED: intermediate_results.evaluation_result="Tier 1"
  STEP 3: PersistRecord
    INPUT: record={evaluation}
    OUTPUT: receipt=RECEIPT-2026-88421
    STATE UPDATED: audit_trail appended

EXECUTION COMPLETE: SUCCESS
AUDIT LOG: Written to retention store
CYCLE COMPLETE
```

---

## 16. Compliance Checklist

Deployments MUST complete this checklist before production use.

| Requirement | Section | Status |
|-------------|---------|--------|
| Confidence calibration configured | 10 | ☐ |
| Confidence threshold documented with rationale | 10.3 | ☐ |
| Permission verification implemented | 6.2 | ☐ |
| Escalation timeout behavior configured | 9.3 | ☐ |
| Responsibility attribution documented | 11.2 | ☐ |
| Audit retention configured (minimum 90 days) | 8.3 | ☐ |
| Trust levels defined for all competencies | 12.1 | ☐ |
| CapabilityGaps reviewed and accepted | 5.2 | ☐ |

---

## 17. Summary

This system does not simulate intelligence. It compiles responsibility into capability.

It is safe because it refuses to guess, it exposes uncertainty, it records memory, it verifies permission, it attributes responsibility, and it stops when judgment is required.

---

## 18. Appendix A: JSON Schema (Normative)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.org/apqc-sfs/v2.0/schemas",
  
  "definitions": {
    "ProcessIntent": {
      "type": "object",
      "required": ["apqc_id", "label", "level", "description", "constraints", "ingest_metadata"],
      "properties": {
        "apqc_id": { "type": "string", "pattern": "^[0-9]+(\\.[0-9]+)*$" },
        "label": { "type": "string", "minLength": 1 },
        "level": { "type": "integer", "minimum": 1, "maximum": 5 },
        "description": { "type": "string" },
        "implied_outcomes": { "type": "array", "items": { "type": "string" } },
        "implied_inputs": { "type": "array", "items": { "type": "string" } },
        "constraints": { "type": "array", "items": { "type": "string" } },
        "ingest_metadata": { "$ref": "#/definitions/IngestMetadata" }
      }
    },
    
    "IngestMetadata": {
      "type": "object",
      "required": ["source_version", "ingest_timestamp", "ingest_agent"],
      "properties": {
        "source_version": { "type": "string" },
        "ingest_timestamp": { "type": "string", "format": "date-time" },
        "ingest_agent": { "type": "string" }
      }
    },
    
    "SFSFunction": {
      "type": "object",
      "required": ["name", "version", "type", "determinism", "provenance"],
      "properties": {
        "name": { "type": "string", "pattern": "^[A-Z][a-zA-Z0-9]*$" },
        "version": { "type": "string", "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$" },
        "type": { "enum": ["primitive", "composite", "action", "query"] },
        "input": { "type": "array", "items": { "$ref": "#/definitions/Parameter" } },
        "output": { "type": "array", "items": { "$ref": "#/definitions/Parameter" } },
        "side_effects": { "type": "array", "items": { "$ref": "#/definitions/SideEffect" } },
        "determinism": { "$ref": "#/definitions/DeterminismDeclaration" },
        "provenance": { "$ref": "#/definitions/Provenance" },
        "composition": { "type": "array", "items": { "$ref": "#/definitions/CompositionStep" } }
      }
    },
    
    "Parameter": {
      "type": "object",
      "required": ["name", "type"],
      "properties": {
        "name": { "type": "string" },
        "type": { "type": "string" },
        "required": { "type": "boolean", "default": true }
      }
    },
    
    "SideEffect": {
      "type": "object",
      "required": ["type", "scope"],
      "properties": {
        "type": { "enum": ["persistence", "notification", "external_call", "state_mutation"] },
        "scope": { "type": "string" }
      }
    },
    
    "DeterminismDeclaration": {
      "type": "object",
      "required": ["classification"],
      "properties": {
        "classification": { "enum": ["deterministic", "reproducible", "externally_variable"] },
        "rationale": { "type": "string" }
      }
    },
    
    "Provenance": {
      "type": "object",
      "required": ["source", "confidence", "validation_state"],
      "properties": {
        "source": { "type": "string" },
        "compilation_run": { "type": "string" },
        "confidence": { "type": "number", "minimum": 0, "maximum": 1 },
        "confidence_method": { "type": "string" },
        "validation_state": { "enum": ["pending", "pending_human_review", "approved", "rejected"] },
        "validated_by": { "type": "string" },
        "validated_at": { "type": "string", "format": "date-time" }
      }
    },
    
    "CompositionStep": {
      "type": "object",
      "required": ["step", "function"],
      "properties": {
        "step": { "type": "integer", "minimum": 1 },
        "function": { "type": "string" },
        "input_mapping": { "type": "object" },
        "output_binding": { "type": "string" }
      }
    },
    
    "CapabilityGap": {
      "type": "object",
      "required": ["gap_id", "semantic_need", "reason", "classification", "created"],
      "properties": {
        "gap_id": { "type": "string", "pattern": "^GAP-[0-9]{4}-[0-9]+$" },
        "semantic_need": { "type": "string" },
        "reason": { "type": "string" },
        "classification": { "enum": ["non_compilable", "blocked_by_policy", "pending_capability"] },
        "recommended_action": { "type": "string" },
        "created": { "type": "string", "format": "date-time" }
      }
    },
    
    "ContextBinding": {
      "type": "object",
      "required": ["binding_id", "function", "function_version", "implementation", "variability", "created"],
      "properties": {
        "binding_id": { "type": "string", "pattern": "^BIND-[0-9]{4}-[0-9]+$" },
        "function": { "type": "string" },
        "function_version": { "type": "string" },
        "implementation": { "$ref": "#/definitions/ToolImplementation" },
        "variability": { "$ref": "#/definitions/VariabilityDeclaration" },
        "created": { "type": "string", "format": "date-time" },
        "created_by": { "type": "string" },
        "valid_until": { "type": "string", "format": "date-time" }
      }
    },
    
    "ToolImplementation": {
      "type": "object",
      "required": ["tool", "tool_version", "method"],
      "properties": {
        "tool": { "type": "string" },
        "tool_version": { "type": "string" },
        "method": { "type": "string" },
        "endpoint": { "type": "string" }
      }
    },
    
    "VariabilityDeclaration": {
      "type": "object",
      "required": ["classification"],
      "properties": {
        "classification": { "enum": ["deterministic", "external"] },
        "timeout_ms": { "type": "integer", "minimum": 0 },
        "retry_policy": { "type": "string" },
        "max_retries": { "type": "integer", "minimum": 0 }
      }
    },
    
    "PermissionClaim": {
      "type": "object",
      "required": ["claim_id", "principal", "scope", "issuer"],
      "properties": {
        "claim_id": { "type": "string", "pattern": "^PERM-[0-9]{4}-[0-9]+$" },
        "principal": { "$ref": "#/definitions/Principal" },
        "scope": { "$ref": "#/definitions/PermissionScope" },
        "constraints": { "$ref": "#/definitions/PermissionConstraints" },
        "issuer": { "$ref": "#/definitions/Issuer" },
        "signature": { "type": "string" }
      }
    },
    
    "Principal": {
      "type": "object",
      "required": ["type", "identifier"],
      "properties": {
        "type": { "enum": ["role", "user", "service"] },
        "identifier": { "type": "string" }
      }
    },
    
    "PermissionScope": {
      "type": "object",
      "properties": {
        "functions": { "type": "array", "items": { "type": "string" } },
        "data_domains": { "type": "array", "items": { "type": "string" } },
        "time_bound": { "$ref": "#/definitions/TimeBound" }
      }
    },
    
    "TimeBound": {
      "type": "object",
      "properties": {
        "not_before": { "type": "string", "format": "date-time" },
        "not_after": { "type": "string", "format": "date-time" }
      }
    },
    
    "PermissionConstraints": {
      "type": "object",
      "properties": {
        "max_records_per_invocation": { "type": "integer", "minimum": 1 },
        "require_audit_log": { "type": "boolean" }
      }
    },
    
    "Issuer": {
      "type": "object",
      "required": ["authority", "issued_at"],
      "properties": {
        "authority": { "type": "string" },
        "issued_at": { "type": "string", "format": "date-time" }
      }
    },
    
    "SessionState": {
      "type": "object",
      "required": ["session_id", "role", "execution_id", "started_at", "permission_claim_id"],
      "properties": {
        "session_id": { "type": "string", "pattern": "^SESSION-[0-9]{4}-[0-9]+$" },
        "role": { "type": "string" },
        "execution_id": { "type": "string" },
        "started_at": { "type": "string", "format": "date-time" },
        "data_context": { "type": "object" },
        "intermediate_results": { "type": "object" },
        "audit_trail": { "type": "array", "items": { "$ref": "#/definitions/AuditEntry" } },
        "permission_claim_id": { "type": "string" }
      }
    },
    
    "AuditEntry": {
      "type": "object",
      "required": ["timestamp", "action", "status"],
      "properties": {
        "timestamp": { "type": "string", "format": "date-time" },
        "action": { "type": "string" },
        "status": { "enum": ["success", "failure", "pending"] },
        "detail": { "type": "string" }
      }
    },
    
    "EscalationRequest": {
      "type": "object",
      "required": ["escalation_id", "session_id", "reason", "context", "routing", "timeout", "created_at"],
      "properties": {
        "escalation_id": { "type": "string", "pattern": "^ESC-[0-9]{4}-[0-9]+$" },
        "session_id": { "type": "string" },
        "reason": { "$ref": "#/definitions/EscalationReason" },
        "context": { "$ref": "#/definitions/EscalationContext" },
        "routing": { "$ref": "#/definitions/EscalationRouting" },
        "timeout": { "$ref": "#/definitions/EscalationTimeout" },
        "created_at": { "type": "string", "format": "date-time" }
      }
    },
    
    "EscalationReason": {
      "type": "object",
      "required": ["type", "detail"],
      "properties": {
        "type": { "enum": ["capability_gap", "confidence_failure", "permission_required", "policy_required"] },
        "detail": { "type": "string" }
      }
    },
    
    "EscalationContext": {
      "type": "object",
      "required": ["function_attempted"],
      "properties": {
        "function_attempted": { "type": "string" },
        "input_summary": { "type": "string" },
        "state_snapshot": { "type": "object" }
      }
    },
    
    "EscalationRouting": {
      "type": "object",
      "required": ["escalation_target", "priority", "sla_minutes"],
      "properties": {
        "escalation_target": { "type": "string" },
        "priority": { "enum": ["low", "medium", "high", "critical"] },
        "sla_minutes": { "type": "integer", "minimum": 1 }
      }
    },
    
    "EscalationTimeout": {
      "type": "object",
      "required": ["deadline", "timeout_action"],
      "properties": {
        "deadline": { "type": "string", "format": "date-time" },
        "timeout_action": { "enum": ["escalate_further", "abort_with_notification"] }
      }
    },
    
    "EscalationResponse": {
      "type": "object",
      "required": ["escalation_id", "responder", "decision", "response_at"],
      "properties": {
        "escalation_id": { "type": "string" },
        "responder": { "$ref": "#/definitions/Responder" },
        "decision": { "$ref": "#/definitions/EscalationDecision" },
        "engagement_verification": { "$ref": "#/definitions/EngagementVerification" },
        "response_at": { "type": "string", "format": "date-time" }
      }
    },
    
    "Responder": {
      "type": "object",
      "required": ["identity", "role", "verified_at"],
      "properties": {
        "identity": { "type": "string" },
        "role": { "type": "string" },
        "verified_at": { "type": "string", "format": "date-time" }
      }
    },
    
    "EscalationDecision": {
      "type": "object",
      "required": ["action"],
      "properties": {
        "action": { "enum": ["approve", "reject", "delegate", "request_more_info"] },
        "rationale": { "type": "string" }
      }
    },
    
    "EngagementVerification": {
      "type": "object",
      "properties": {
        "time_spent_seconds": { "type": "integer", "minimum": 0 },
        "context_accessed": { "type": "array", "items": { "type": "string" } },
        "attestation": { "type": "string" }
      }
    },
    
    "ConfidenceConfiguration": {
      "type": "object",
      "required": ["method", "threshold"],
      "properties": {
        "method": { "enum": ["model_output", "ensemble_agreement", "human_rating", "hybrid"] },
        "parameters": { "type": "object" },
        "calibration": { "$ref": "#/definitions/CalibrationMetadata" },
        "threshold": { "$ref": "#/definitions/ConfidenceThreshold" }
      }
    },
    
    "CalibrationMetadata": {
      "type": "object",
      "properties": {
        "calibration_dataset": { "type": "string" },
        "calibration_date": { "type": "string", "format": "date" },
        "brier_score": { "type": "number", "minimum": 0, "maximum": 1 },
        "expected_calibration_error": { "type": "number", "minimum": 0, "maximum": 1 }
      }
    },
    
    "ConfidenceThreshold": {
      "type": "object",
      "required": ["human_review_required"],
      "properties": {
        "human_review_required": { "type": "number", "minimum": 0, "maximum": 1 },
        "auto_approve": { "type": "number", "minimum": 0, "maximum": 1 }
      }
    },
    
    "ResponsibilityAttribution": {
      "type": "object",
      "required": ["artifact_id", "layer", "responsible_party", "responsibility_scope"],
      "properties": {
        "artifact_id": { "type": "string" },
        "layer": { "enum": ["intent", "logic", "compilation", "binding", "execution", "escalation"] },
        "responsible_party": { "$ref": "#/definitions/ResponsibleParty" },
        "responsibility_scope": { "type": "string" },
        "accountability_chain": { "type": "array", "items": { "$ref": "#/definitions/AccountabilityLink" } },
        "last_reviewed": { "type": "string", "format": "date-time" },
        "next_review_due": { "type": "string", "format": "date-time" }
      }
    },
    
    "ResponsibleParty": {
      "type": "object",
      "required": ["identity", "role"],
      "properties": {
        "identity": { "type": "string" },
        "role": { "type": "string" }
      }
    },
    
    "AccountabilityLink": {
      "type": "object",
      "required": ["layer", "party"],
      "properties": {
        "layer": { "type": "string" },
        "party": { "type": "string" }
      }
    },
    
    "RoleRuntimeArtifact": {
      "type": "object",
      "required": ["artifact_id", "role", "source_standard", "compiled_at", "compiled_by", "competencies"],
      "properties": {
        "artifact_id": { "type": "string", "pattern": "^ROLE-[A-Z0-9-]+-v[0-9]+\\.[0-9]+\\.[0-9]+$" },
        "role": { "type": "string" },
        "source_standard": { "type": "string" },
        "compiled_at": { "type": "string", "format": "date-time" },
        "compiled_by": { "type": "string" },
        "valid_until": { "type": "string", "format": "date-time" },
        "competencies": { "type": "array", "items": { "$ref": "#/definitions/Competency" } },
        "capability_gaps": { "type": "array", "items": { "$ref": "#/definitions/CapabilityGap" } },
        "permission_requirements": { "$ref": "#/definitions/PermissionRequirements" },
        "audit_configuration": { "$ref": "#/definitions/AuditConfiguration" }
      }
    },
    
    "Competency": {
      "type": "object",
      "required": ["function", "function_version", "status", "responsibility"],
      "properties": {
        "function": { "type": "string" },
        "function_version": { "type": "string" },
        "status": { "enum": ["executable", "non_executable"] },
        "trust_level": { "enum": ["high", "medium", "low", "none"] },
        "trust_level_definition": { "type": "string" },
        "triggers": { "type": "array", "items": { "$ref": "#/definitions/Trigger" } },
        "constraints": { "type": "object" },
        "reason": { "$ref": "#/definitions/NonExecutableReason" },
        "fallback": { "$ref": "#/definitions/Fallback" },
        "responsibility": { "$ref": "#/definitions/CompetencyResponsibility" }
      }
    },
    
    "Trigger": {
      "type": "object",
      "required": ["type"],
      "properties": {
        "type": { "enum": ["scheduled", "manual", "event"] },
        "schedule": { "type": "string" },
        "authorized_roles": { "type": "array", "items": { "type": "string" } },
        "event_type": { "type": "string" }
      }
    },
    
    "NonExecutableReason": {
      "type": "object",
      "required": ["type"],
      "properties": {
        "type": { "enum": ["capability_gap", "policy_block", "pending_validation"] },
        "gap_id": { "type": "string" },
        "detail": { "type": "string" }
      }
    },
    
    "Fallback": {
      "type": "object",
      "required": ["action", "target"],
      "properties": {
        "action": { "enum": ["escalate", "defer", "notify"] },
        "target": { "type": "string" },
        "sla_minutes": { "type": "integer", "minimum": 1 }
      }
    },
    
    "CompetencyResponsibility": {
      "type": "object",
      "required": ["layer", "party"],
      "properties": {
        "layer": { "type": "string" },
        "party": { "type": "string" }
      }
    },
    
    "PermissionRequirements": {
      "type": "object",
      "properties": {
        "required_claims": { "type": "array", "items": { "type": "object" } }
      }
    },
    
    "AuditConfiguration": {
      "type": "object",
      "required": ["retention_days", "log_level"],
      "properties": {
        "retention_days": { "type": "integer", "minimum": 90 },
        "log_level": { "enum": ["minimal", "standard", "detailed"] }
      }
    }
  }
}
```

---

## 19. Appendix B: OWL Ontology (Normative)

The following OWL ontology formalizes the core types for integration with BFO/CCO-aligned semantic infrastructure.

```turtle
@prefix : <https://example.org/apqc-sfs/v2.0/ontology#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix bfo: <http://purl.obolibrary.org/obo/BFO_> .
@prefix cco: <http://www.ontologyrepository.com/CommonCoreOntologies/> .

<https://example.org/apqc-sfs/v2.0/ontology> rdf:type owl:Ontology ;
    rdfs:label "APQC-SFS Execution Ontology"@en ;
    rdfs:comment "Formal ontology for semantic compilation of process models into executable capabilities"@en ;
    owl:versionInfo "2.0.0" .

#################################################################
# Classes
#################################################################

### ProcessIntent - A descriptive specification of organizational process intent
:ProcessIntent rdf:type owl:Class ;
    rdfs:subClassOf cco:InformationContentEntity ;
    rdfs:label "Process Intent"@en ;
    rdfs:comment "A descriptive specification derived from APQC PCF representing organizational process intent without execution semantics"@en .

### SFSFunction - An executable semantic capability
:SFSFunction rdf:type owl:Class ;
    rdfs:subClassOf cco:InformationContentEntity ;
    rdfs:label "SFS Function"@en ;
    rdfs:comment "A deterministic, domain-agnostic semantic function with typed inputs, outputs, and explicit side-effect declarations"@en .

### PrimitiveFunction - An atomic SFS function
:PrimitiveFunction rdf:type owl:Class ;
    rdfs:subClassOf :SFSFunction ;
    rdfs:label "Primitive Function"@en ;
    rdfs:comment "An atomic SFS function that cannot be decomposed into smaller functions"@en .

### CompositeFunction - A composed SFS function
:CompositeFunction rdf:type owl:Class ;
    rdfs:subClassOf :SFSFunction ;
    rdfs:label "Composite Function"@en ;
    rdfs:comment "An SFS function composed of other SFS functions"@en .

### CapabilityGap - A documented absence of capability
:CapabilityGap rdf:type owl:Class ;
    rdfs:subClassOf cco:InformationContentEntity ;
    rdfs:label "Capability Gap"@en ;
    rdfs:comment "A documented semantic need that cannot be satisfied by available SFS primitives"@en .

### ContextBinding - A mapping from logic to implementation
:ContextBinding rdf:type owl:Class ;
    rdfs:subClassOf cco:InformationContentEntity ;
    rdfs:label "Context Binding"@en ;
    rdfs:comment "A versioned, auditable mapping from an SFS function to a concrete tool implementation"@en .

### PermissionClaim - An authorization assertion
:PermissionClaim rdf:type owl:Class ;
    rdfs:subClassOf cco:InformationContentEntity ;
    rdfs:label "Permission Claim"@en ;
    rdfs:comment "A signed assertion of authorization scope for execution"@en .

### SessionState - Execution context
:SessionState rdf:type owl:Class ;
    rdfs:subClassOf cco:InformationContentEntity ;
    rdfs:label "Session State"@en ;
    rdfs:comment "The stateful context maintained across an execution path"@en .

### EscalationRequest - A request for human intervention
:EscalationRequest rdf:type owl:Class ;
    rdfs:subClassOf cco:InformationContentEntity ;
    rdfs:label "Escalation Request"@en ;
    rdfs:comment "A structured request for human review and decision"@en .

### RoleRuntimeArtifact - A compiled role definition
:RoleRuntimeArtifact rdf:type owl:Class ;
    rdfs:subClassOf cco:InformationContentEntity ;
    rdfs:label "Role Runtime Artifact"@en ;
    rdfs:comment "A versionable configuration defining an agent's scope of competence"@en .

### Provenance - Origin and validation metadata
:Provenance rdf:type owl:Class ;
    rdfs:subClassOf cco:InformationContentEntity ;
    rdfs:label "Provenance"@en ;
    rdfs:comment "Metadata recording the origin, confidence, and validation state of an artifact"@en .

### ResponsibilityAttribution - Accountability assignment
:ResponsibilityAttribution rdf:type owl:Class ;
    rdfs:subClassOf cco:InformationContentEntity ;
    rdfs:label "Responsibility Attribution"@en ;
    rdfs:comment "Assignment of accountability for an artifact or decision to a party"@en .

#################################################################
# Object Properties
#################################################################

### derivedFrom - Links compiled artifact to source
:derivedFrom rdf:type owl:ObjectProperty ;
    rdfs:domain :SFSFunction ;
    rdfs:range :ProcessIntent ;
    rdfs:label "derived from"@en ;
    rdfs:comment "Relates an SFS function to the APQC process intent from which it was compiled"@en .

### composedOf - Links composite to components
:composedOf rdf:type owl:ObjectProperty ;
    rdfs:domain :CompositeFunction ;
    rdfs:range :SFSFunction ;
    rdfs:label "composed of"@en ;
    rdfs:comment "Relates a composite function to its constituent functions"@en .

### boundTo - Links function to implementation
:boundTo rdf:type owl:ObjectProperty ;
    rdfs:domain :SFSFunction ;
    rdfs:range :ContextBinding ;
    rdfs:label "bound to"@en ;
    rdfs:comment "Relates an SFS function to its context binding"@en .

### hasProvenance - Links artifact to provenance
:hasProvenance rdf:type owl:ObjectProperty ;
    rdfs:domain owl:Thing ;
    rdfs:range :Provenance ;
    rdfs:label "has provenance"@en ;
    rdfs:comment "Relates an artifact to its provenance metadata"@en .

### hasResponsibility - Links artifact to responsibility
:hasResponsibility rdf:type owl:ObjectProperty ;
    rdfs:domain owl:Thing ;
    rdfs:range :ResponsibilityAttribution ;
    rdfs:label "has responsibility"@en ;
    rdfs:comment "Relates an artifact to its responsibility attribution"@en .

### requiresPermission - Links execution to permission
:requiresPermission rdf:type owl:ObjectProperty ;
    rdfs:domain :SFSFunction ;
    rdfs:range :PermissionClaim ;
    rdfs:label "requires permission"@en ;
    rdfs:comment "Relates a function to the permission claim required for execution"@en .

### triggersEscalation - Links gap to escalation
:triggersEscalation rdf:type owl:ObjectProperty ;
    rdfs:domain :CapabilityGap ;
    rdfs:range :EscalationRequest ;
    rdfs:label "triggers escalation"@en ;
    rdfs:comment "Relates a capability gap to the escalation it triggers at runtime"@en .

### definesCompetency - Links role to functions
:definesCompetency rdf:type owl:ObjectProperty ;
    rdfs:domain :RoleRuntimeArtifact ;
    rdfs:range :SFSFunction ;
    rdfs:label "defines competency"@en ;
    rdfs:comment "Relates a role artifact to the functions it authorizes"@en .

### documentsGap - Links role to gaps
:documentsGap rdf:type owl:ObjectProperty ;
    rdfs:domain :RoleRuntimeArtifact ;
    rdfs:range :CapabilityGap ;
    rdfs:label "documents gap"@en ;
    rdfs:comment "Relates a role artifact to the capability gaps it acknowledges"@en .

#################################################################
# Data Properties
#################################################################

### hasConfidence - Confidence score
:hasConfidence rdf:type owl:DatatypeProperty ;
    rdfs:domain :Provenance ;
    rdfs:range xsd:decimal ;
    rdfs:label "has confidence"@en ;
    rdfs:comment "The confidence score assigned during compilation"@en .

### hasValidationState - Validation status
:hasValidationState rdf:type owl:DatatypeProperty ;
    rdfs:domain :Provenance ;
    rdfs:range xsd:string ;
    rdfs:label "has validation state"@en ;
    rdfs:comment "The validation state (pending, approved, rejected)"@en .

### hasDeterminismClass - Determinism classification
:hasDeterminismClass rdf:type owl:DatatypeProperty ;
    rdfs:domain :SFSFunction ;
    rdfs:range xsd:string ;
    rdfs:label "has determinism class"@en ;
    rdfs:comment "The determinism classification (deterministic, reproducible, externally_variable)"@en .

### hasTrustLevel - Trust level
:hasTrustLevel rdf:type owl:DatatypeProperty ;
    rdfs:domain :SFSFunction ;
    rdfs:range xsd:string ;
    rdfs:label "has trust level"@en ;
    rdfs:comment "The trust level (high, medium, low, none)"@en .

### hasVersion - Semantic version
:hasVersion rdf:type owl:DatatypeProperty ;
    rdfs:domain owl:Thing ;
    rdfs:range xsd:string ;
    rdfs:label "has version"@en ;
    rdfs:comment "The semantic version string"@en .
```

---

## 20. Appendix C: Glossary

| Term | Definition |
|------|------------|
| **Capability Gap** | A documented semantic need that cannot be satisfied by available SFS primitives |
| **Compile-Time Determinism** | The property that identical inputs produce identical artifacts |
| **Composite Function** | An SFS function composed of other SFS functions |
| **Confidence Score** | A calibrated probability that an inferred element correctly captures source intent |
| **Context Binding** | A versioned mapping from an SFS function to a concrete tool implementation |
| **Escalation** | The transfer of decision authority from the system to a human |
| **External Variability** | Non-determinism arising from systems outside the specification boundary |
| **Permission Claim** | A signed assertion of authorization scope for execution |
| **Primitive Function** | An atomic SFS function that cannot be decomposed |
| **Process Intent Object (PIO)** | The internal representation of an ingested APQC process |
| **Provenance** | Metadata recording origin, confidence, and validation state |
| **Ralph Wiggum Loop** | The controlled synthesis component that performs semantic compilation |
| **Responsibility Attribution** | Assignment of accountability to a party for an artifact or decision |
| **Role Runtime Artifact** | A compiled configuration defining an agent's scope of competence |
| **Runtime Determinism** | The property that identical invocation context produces identical traces |
| **Session State** | The stateful context maintained across an execution path |
| **SFS (Semantic Function Schema)** | The capability vocabulary defining executable semantic primitives |
| **Trust Level** | Classification determining required human involvement in execution |

---

## 21. Appendix D: Change Log

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-12-01 | Initial specification |
| 1.1 | 2026-01-15 | Added Session State Object, revised Knowledge Worker Stack |
| 2.0 | 2026-01-31 | Added Permission Model (Section 6), Escalation Model (Section 9), Confidence Calibration Model (Section 10), Responsibility Attribution Model (Section 11), Trust Level Definitions (Section 12.1), Compliance Checklist (Section 16), JSON Schema (Appendix A), OWL Ontology (Appendix B), Glossary (Appendix C). Clarified determinism definitions (Section 3.2). |

---

## 22. Appendix E: References

1. APQC Process Classification Framework (PCF). American Productivity & Quality Center.
2. RFC 2119: Key words for use in RFCs to Indicate Requirement Levels. IETF.
3. Basic Formal Ontology (BFO) 2020. https://basic-formal-ontology.org/
4. Common Core Ontologies (CCO). https://github.com/CommonCoreOntology/CommonCoreOntologies
5. Semantic Function Schema (SFS) v2.2. Internal specification.

---

*End of Specification*
