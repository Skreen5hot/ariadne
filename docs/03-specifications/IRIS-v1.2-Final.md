# IRIS v1.2: Integrated Real-time Input Sensing

## Direct Perception Layer for FNSR (Final Hardened Revision)

**Version:** 1.2 (Post-Second-Critique Revision)  
**Date:** January 2026  
**Status:** Implementation-Ready Draft  
**Supersedes:** IRIS v1.1  
**Relationship:** Extends FNSR Architecture v2.1

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 0.1 | January 2026 | Initial conceptual draft |
| 1.1 | January 2026 | Theory-ladenness acknowledged, SOCIUS demoted, Pointer Pattern, taint split |
| 1.2 | January 2026 | L1 renamed to L1-ASSERTED, INTUS outputs stratified, Forge constraints hardened, drift governance added, conflict resolution preconditions, language enforcement |

---

## 1. Response to v1.1 Critique

### 1.1 Summary of Required Fixes

The v1.1 critique identified five must-fix issues:

| Issue | Problem | Fix in v1.2 |
|-------|---------|-------------|
| **L1 ambiguity** | "Derived Fact" sounds like truth; documents can lie | Renamed to **L1-ASSERTED** |
| **INTUS as L0-RAW** | "Self-knowledge is direct" is only partly true | Split INTUS outputs: L0-RAW (hardware) vs L1-INTERNAL (aggregates) |
| **Forge under-constrained** | Could become second-order inference engine | Explicit prohibitions added |
| **No drift governance** | Model registry is static | Drift monitoring with auto-actions |
| **Conflict resolution too confident** | "IRIS wins" without preconditions | Sensor integrity preconditions added |

Additionally, the critique recommended:
- **Language enforcement** — Prohibit modal verbs, causal language, normative predicates in IRIS outputs
- **Schema validation** — Make enforcement automatic, not just policy

---

## 2. Revised Taint Levels (v1.2)

### 2.1 The Complete Hierarchy

```
Epistemic Hierarchy (IRIS v1.2):

    L0-RAW  ─────────────────────────────────  Incontrovertible
       │                                       (semantically empty)
       │     "These are the literal sensor readings"
       │     Examples: pixel values, audio samples, voltage, clock ticks
       │
       ▼
  L1-PERCEIVED ──────────────────────────────  Model-mediated perception
       │                                       (probabilistic, external world)
       │     "Model X says this is a door (conf: 0.94)"
       │
       ▼
  L1-INTERNAL ───────────────────────────────  Model-mediated self-observation
       │                                       (probabilistic, internal state)
       │     "Aggregated metrics indicate high cognitive load"         [NEW]
       │     "Moral injury accumulator reports value Y"
       │
       ▼
  L1-ASSERTED ───────────────────────────────  Documentary claims
       │                                       (claimed, not verified)       [RENAMED]
       │     "Document states X was delivered"
       │     NOTE: Documents can lie. This is assertion, not truth.
       │
       ▼
      L2  ───────────────────────────────────  Defeasible
       │                                       (default reasoning)
       │
    ═══════════════ EPISTEMIC FIREWALL ═══════════════
       │
      L3  ───────────────────────────────────  Speculative
       │
      L4  ───────────────────────────────────  Hypothetical
       │
      L5  ───────────────────────────────────  Adversarial
```

### 2.2 Taint Level Definitions (v1.2)

| Level | Name | Source | Certainty | Key Property |
|-------|------|--------|-----------|--------------|
| **L0-RAW** | Raw Signal | Sensor hardware directly | Incontrovertible | Semantically empty |
| **L1-PERCEIVED** | Perceived Feature | Perception model (external) | Probabilistic | About the world |
| **L1-INTERNAL** | Internal Feature | Aggregation/interpretation (self) | Probabilistic | About the system itself |
| **L1-ASSERTED** | Asserted Claim | Documents, testimony | **Claimed, not verified** | Documents can lie |
| **L2** | Defeasible | Default reasoning | Overridable | Common-sense |
| **L3** | Speculative | Abduction | Hypothesis only | Gap-filling |
| **L4** | Hypothetical | Simulation | Never real | Sandbox only |
| **L5** | Adversarial | Unknown/hostile | Quarantined | Under review |

### 2.3 Critical Clarification: L1-ASSERTED

**The critique correctly identified:**

> "Right now, L1 reads as 'safe fact,' which is dangerous."

**The fix:**

L1-ASSERTED explicitly encodes that documentary claims are **assertions**, not truths. The system knows:
- The document *claims* X
- The document may be wrong, fraudulent, or outdated
- Verification requires evidence (including IRIS observations)

```prolog
% L1-ASSERTED is NOT truth — it is recorded testimony
epistemic_status(L1-ASSERTED, asserted).
epistemic_status(L1-ASSERTED, unverified).
epistemic_status(L1-ASSERTED, potentially_false).

% Verification can upgrade or downgrade
verify_assertion(Assertion, Observation, Result) :-
    assertion(Assertion, Content, L1-ASSERTED),
    observation(Observation, ObsContent, L1-PERCEIVED),
    (   consistent(Content, ObsContent)
    ->  Result = corroborated(Assertion, Observation)
    ;   Result = contradicted(Assertion, Observation)
    ).
```

---

## 3. INTUS Stratification (v1.2)

### 3.1 The Problem with "Self-Knowledge is Direct"

The critique correctly identified:

> "CPU load is measured via software abstraction layers. Error patterns are interpreted aggregates. 'Moral injury state' is absolutely not raw."

**The fix:** Split INTUS outputs into two taint levels.

### 3.2 INTUS Output Classification

```yaml
service: intus
type: perception
modality: proprioceptive
version: 1.2

outputs:
  # === TRUE L0-RAW: Hardware counters, direct readings ===
  l0_raw_outputs:
    - name: "hardware_clock"
      description: "System clock ticks"
      taint: L0-RAW
      source: "hardware counter"
      
    - name: "cpu_cycles"
      description: "Raw CPU cycle counter"
      taint: L0-RAW
      source: "hardware performance counter"
      
    - name: "memory_addresses"
      description: "Raw memory allocation addresses"
      taint: L0-RAW
      source: "memory controller"
      
    - name: "network_packets"
      description: "Raw packet counts (in/out)"
      taint: L0-RAW
      source: "NIC hardware counter"
      
    - name: "voltage_readings"
      description: "Power supply voltage (if available)"
      taint: L0-RAW
      source: "hardware sensor"

  # === L1-INTERNAL: Aggregated, interpreted, model-mediated ===
  l1_internal_outputs:
    - name: "cpu_utilization_percent"
      description: "CPU usage as percentage"
      taint: L1-INTERNAL
      source: "aggregation over cpu_cycles + time window"
      note: "This is an interpretation of raw counters"
      
    - name: "memory_pressure"
      description: "Memory pressure indicator"
      taint: L1-INTERNAL
      source: "heuristic over allocation patterns"
      note: "Model-mediated assessment"
      
    - name: "cognitive_load"
      description: "Active queries, pending sagas, inference depth"
      taint: L1-INTERNAL
      source: "aggregation over orchestrator state"
      note: "Interpretation of system activity"
      
    - name: "service_health"
      description: "Health status of FNSR services"
      taint: L1-INTERNAL
      source: "aggregation over health checks"
      note: "Classification (healthy/degraded/failed)"
      
    - name: "error_patterns"
      description: "Detected error patterns"
      taint: L1-INTERNAL
      source: "pattern detection over error logs"
      note: "Model-mediated pattern recognition"
      
    - name: "moral_injury_level"
      description: "Accumulated moral injury"
      taint: L1-INTERNAL  # CRITICAL CHANGE
      source: "character accumulator"
      note: "This is an interpreted aggregate, NOT raw"
      
    - name: "threshold_proximity"
      description: "Distance to intervention thresholds"
      taint: L1-INTERNAL
      source: "computation over moral_injury + thresholds"
      note: "Derived value"
```

### 3.3 Why This Matters

The system must not grant itself **epistemic certainty about its own interpretations**.

| What INTUS Knows Directly | What INTUS Interprets |
|---------------------------|----------------------|
| Clock ticks | "It's been 5 minutes" |
| CPU cycles | "CPU is at 80%" |
| Memory addresses | "Memory pressure is high" |
| Packet counts | "Network is degraded" |
| — | "Moral injury is approaching threshold" |

The second column involves models, heuristics, and aggregations. These can be wrong. The system must know this about itself.

---

## 4. Observation Forge Constraints (v1.2)

### 4.1 The Risk

The critique identified:

> "If the Forge ever merges outputs from multiple models, selects a 'best' feature, or normalizes confidence scores... it becomes a second-order inference engine."

### 4.2 Explicit Prohibitions

```yaml
observation_forge:
  version: 1.2
  
  # === WHAT THE FORGE DOES ===
  permitted_operations:
    - structure_model_output:
        description: "Convert model output to observation node schema"
        
    - attach_provenance:
        description: "Add sensor and model provenance metadata"
        
    - assign_taint:
        description: "Assign appropriate taint level based on source"
        
    - attach_epistemic_metadata:
        description: "Add confidence, limitations, challengeability"
        
    - generate_hiri:
        description: "Create content-addressed identifier"
        
    - validate_schema:
        description: "Ensure output conforms to observation schema"
        
    - enforce_language_constraints:
        description: "Reject outputs containing prohibited language"

  # === WHAT THE FORGE MUST NOT DO ===
  prohibited_operations:
    - fuse_model_outputs:
        description: "Combine outputs from multiple models into single feature"
        reason: "This is inference, not structuring"
        where_it_belongs: "Downstream reasoning (MDRE)"
        
    - resolve_disagreements:
        description: "Choose between conflicting model outputs"
        reason: "This is judgment, not structuring"
        where_it_belongs: "Downstream reasoning (MDRE)"
        
    - adjust_confidence:
        description: "Modify model-reported confidence scores"
        reason: "This obscures model provenance"
        where_it_belongs: "Never — confidence must be preserved as-is"
        
    - temporal_smoothing:
        description: "Average or smooth features over time"
        reason: "This is signal processing / inference"
        where_it_belongs: "Downstream if needed"
        
    - select_best_feature:
        description: "Choose most likely feature from alternatives"
        reason: "This is inference"
        where_it_belongs: "Downstream reasoning"
        
    - normalize_across_models:
        description: "Adjust outputs to make different models comparable"
        reason: "This obscures model-specific behavior"
        where_it_belongs: "Never in perception layer"
        
    - interpret_meaning:
        description: "Add semantic interpretation to features"
        reason: "Interpretation is not perception"
        where_it_belongs: "Downstream reasoning"
        
    - infer_causation:
        description: "Add causal relationships between features"
        reason: "Causation is not observable"
        where_it_belongs: "Downstream reasoning"
```

### 4.3 Enforcement Mechanism

The Forge includes a **prohibition validator**:

```python
class ForgeProhibitionValidator:
    """Ensures Forge operations stay within permitted bounds."""
    
    PROHIBITED_PATTERNS = [
        # Fusion indicators
        r"merged_from_models",
        r"combined_confidence",
        r"consensus_feature",
        
        # Adjustment indicators
        r"adjusted_confidence",
        r"normalized_score",
        r"smoothed_value",
        
        # Inference indicators
        r"selected_best",
        r"resolved_conflict",
        r"inferred_.*",
    ]
    
    def validate_output(self, observation_node: dict) -> ValidationResult:
        """Reject observations that show signs of prohibited operations."""
        # Implementation checks for prohibited patterns
        pass
```

---

## 5. Language Enforcement (v1.2)

### 5.1 The Requirement

The critique recommended:

> "IRIS outputs MUST NOT contain modal verbs, causal language, or normative predicates. Make this enforceable at schema-validation time."

### 5.2 Prohibited Language in IRIS Outputs

```yaml
language_constraints:
  version: 1.2
  
  # === PROHIBITED TERMS ===
  prohibited_modal_verbs:
    - "might"
    - "could"
    - "would"
    - "should"
    - "may"
    - "must"  # Normative, not descriptive
    
  prohibited_causal_language:
    - "because"
    - "due to"
    - "caused by"
    - "resulting from"
    - "leads to"
    - "therefore"
    - "consequently"
    
  prohibited_interpretive_language:
    - "suggests"
    - "indicates"
    - "implies"
    - "appears to"
    - "seems to"
    - "likely"
    - "probably"
    - "possibly"
    
  prohibited_normative_language:
    - "normal"
    - "abnormal"
    - "expected"
    - "unexpected"
    - "correct"
    - "incorrect"
    - "proper"
    - "improper"
    - "appropriate"
    - "inappropriate"
    
  prohibited_intentional_language:
    - "intends"
    - "wants"
    - "tries"
    - "attempts"
    - "deliberately"
    - "purposely"
    
  prohibited_emotional_language:
    - "angry"
    - "happy"
    - "sad"
    - "fearful"
    - "stressed"
    - "anxious"
    - "confident"  # As emotion, not statistical confidence

  # === PERMITTED LANGUAGE ===
  permitted_patterns:
    - "detected"
    - "classified as"
    - "measured"
    - "recorded"
    - "observed"
    - "confidence: X.XX"
    - "at timestamp"
    - "in region"
    - "model reports"
```

### 5.3 Schema Validation

```yaml
observation_schema_v1.2:
  type: object
  required:
    - id
    - type
    - taint
    - signal_provenance
    - model_provenance
    - features
    - epistemic
    
  properties:
    features:
      type: array
      items:
        type: object
        properties:
          label:
            type: string
            pattern: "^[a-z_]+$"  # Lowercase, underscores only
            not:
              pattern: "(suggests|indicates|implies|likely|probably|normal|abnormal|intends|angry|happy|sad)"
              
          description:
            type: string
            not:
              pattern: "(might|could|should|because|due to|caused by|suggests|indicates|appears to|seems to)"
              
  # === CUSTOM VALIDATOR ===
  x-custom-validators:
    - language_constraint_validator:
        description: "Reject any observation containing prohibited language"
        fail_action: "reject_with_error"
        log_action: "log_violation_attempt"
```

### 5.4 Examples: Compliant vs Non-Compliant

| Non-Compliant (REJECTED) | Compliant (ACCEPTED) |
|--------------------------|----------------------|
| "Door **appears to be** open" | "Door state classified as 'open', confidence: 0.94" |
| "Person **seems** stressed" | ❌ Not permitted — emotion not observable |
| "Valve closure **likely due to** pressure" | "Valve state: closed. Pressure reading: 45 PSI." |
| "**Abnormal** temperature detected" | "Temperature: 85°C. Model threshold: 60°C." |
| "User **intends** to submit" | ❌ Not permitted — intent not observable |
| "This **suggests** equipment failure" | "Equipment state classified as 'non-operational', confidence: 0.87" |

---

## 6. Model Drift Governance (v1.2)

### 6.1 The Gap in v1.1

The critique identified:

> "The registry is static. What's missing: performance decay tracking, domain shift detection, automatic de-approval triggers."

### 6.2 Drift Monitoring Specification

```yaml
model_drift_governance:
  version: 1.2
  
  # === MONITORING METRICS ===
  drift_metrics:
    - name: "confidence_distribution_shift"
      description: "Statistical shift in model confidence outputs"
      method: "KL divergence from baseline distribution"
      baseline_window: "first 10,000 inferences"
      measurement_window: "rolling 1,000 inferences"
      thresholds:
        warn: 0.1
        critical: 0.3
        
    - name: "input_feature_entropy"
      description: "Change in input data characteristics"
      method: "Entropy of input feature distributions"
      baseline_window: "first 10,000 inputs"
      measurement_window: "rolling 1,000 inputs"
      thresholds:
        warn: "20% deviation from baseline"
        critical: "50% deviation from baseline"
        
    - name: "disagreement_rate"
      description: "Rate of disagreement with peer/ensemble models"
      method: "Percentage of outputs where models disagree"
      peer_models: ["model_a", "model_b"]  # If available
      thresholds:
        warn: 0.15
        critical: 0.30
        
    - name: "confidence_calibration"
      description: "Alignment between stated confidence and actual accuracy"
      method: "Expected Calibration Error (ECE)"
      requires: "ground truth labels (periodic audit)"
      thresholds:
        warn: 0.10
        critical: 0.20
        
    - name: "latency_degradation"
      description: "Increase in inference time"
      method: "p95 latency vs baseline"
      baseline: "initial deployment"
      thresholds:
        warn: "2x baseline"
        critical: "5x baseline"

  # === AUTOMATIC ACTIONS ===
  drift_actions:
    - trigger: "any metric at WARN"
      actions:
        - log_warning:
            destination: "drift_monitoring_log"
            alert: "model_operators"
        - annotate_outputs:
            add_field: "drift_warning"
            value: "{metric_name}: {current_value}"
            
    - trigger: "any metric at CRITICAL"
      actions:
        - log_critical:
            destination: "drift_monitoring_log"
            alert: ["model_operators", "system_admins"]
        - downgrade_confidence:
            method: "multiply all confidence scores by 0.8"
            note: "Downstream systems see reduced confidence"
        - add_limitation:
            text: "Model showing drift on {metric_name}; outputs may be degraded"
            
    - trigger: "multiple metrics at CRITICAL for > 24 hours"
      actions:
        - revoke_approval:
            method: "move model from 'approved' to 'suspended'"
            effect: "IRIS will not use this model until re-approved"
        - alert_governance:
            destination: "model_governance_board"
            severity: "high"
        - fallback:
            action: "use backup model if available, else reject inputs"

  # === PERIODIC AUDIT ===
  audit_schedule:
    - type: "automated_drift_check"
      frequency: "hourly"
      
    - type: "human_review_of_drift_logs"
      frequency: "weekly"
      
    - type: "full_recalibration_audit"
      frequency: "quarterly"
      requires: "ground truth labels"
```

### 6.3 Model Registry Update

```yaml
model_registry:
  version: 1.2
  
  models:
    - id: "yolov8-n"
      version: "v8.2.0"
      status: "approved"  # approved | suspended | deprecated
      
      # === STATIC PROVENANCE (unchanged from v1.1) ===
      training_data:
        dataset: "COCO-2017"
        hash: "sha256:abc123..."
        known_biases:
          - "Underperforms on non-Western contexts"
          
      # === DYNAMIC DRIFT STATE (new in v1.2) ===
      drift_state:
        last_checked: "2026-01-30T14:00:00Z"
        metrics:
          confidence_distribution_shift: 0.05  # OK
          input_feature_entropy: 0.12  # WARN
          disagreement_rate: 0.08  # OK
          latency_p95_ms: 8.1  # OK (baseline: 6.3)
        status: "warn"  # ok | warn | critical
        warnings:
          - "input_feature_entropy elevated since 2026-01-28"
        actions_taken:
          - "2026-01-28: annotating outputs with drift warning"
          
      # === APPROVAL HISTORY ===
      approval_history:
        - date: "2026-01-01"
          action: "approved"
          by: "model_governance_board"
        - date: "2026-01-28"
          action: "warn_issued"
          reason: "input_feature_entropy drift detected"
```

---

## 7. Conflict Resolution Preconditions (v1.2)

### 7.1 The Problem

The critique identified:

> "'IRIS wins on physical facts' — only if confidence > threshold, sensor integrity is verified, no adversarial conditions detected."

### 7.2 Revised Conflict Resolution with Preconditions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│        CONFLICT RESOLUTION: OBSERVATION vs. DOCUMENT (v1.2)                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   PRECONDITIONS FOR IRIS TO WIN:                                           │
│   ══════════════════════════════                                           │
│                                                                             │
│   Before IRIS can override documentary claims, ALL of the following        │
│   must be true:                                                            │
│                                                                             │
│   □ Observation confidence ≥ policy threshold (default: 0.90)              │
│   □ Sensor status = operational (not degraded, not failed)                 │
│   □ Model status = approved (not suspended, not deprecated)                │
│   □ Model drift status ≠ critical                                          │
│   □ No adversarial indicators detected                                     │
│   □ Observation is within model's approved scope                           │
│   □ Environmental conditions within model's training distribution          │
│                                                                             │
│   If ANY precondition fails → FLAG FOR HUMAN REVIEW                        │
│                                                                             │
│   ─────────────────────────────────────────────────────────────────────────│
│                                                                             │
│   RESOLUTION TABLE (when preconditions met):                               │
│                                                                             │
│   CONFLICT TYPE    │ DOCUMENT SAYS       │ IRIS OBSERVES     │ WINNER     │
│   ─────────────────┼─────────────────────┼───────────────────┼────────────│
│   IS-STATE         │ "Valve is closed"   │ "Valve is open"   │ IRIS*      │
│   OUGHT-STATE      │ "Valve must be      │ "Valve is open"   │ DOCUMENT   │
│                    │  closed per policy" │                   │ (violation)│
│   IDENTITY         │ "Badge says John"   │ "Face unknown"    │ FLAG       │
│   TEMPORAL         │ "Delivered at 3pm"  │ "Dock empty 3pm"  │ IRIS*      │
│   INTENT           │ "He agreed"         │ "Voice stress"    │ DOCUMENT   │
│                                                                             │
│   * = Subject to preconditions                                             │
│                                                                             │
│   ─────────────────────────────────────────────────────────────────────────│
│                                                                             │
│   PRECONDITION FAILURE HANDLING:                                           │
│                                                                             │
│   If confidence < threshold:                                               │
│       → FLAG: "Observation confidence insufficient for override"           │
│                                                                             │
│   If sensor degraded:                                                      │
│       → FLAG: "Sensor integrity compromised; observation unreliable"       │
│                                                                             │
│   If model suspended:                                                      │
│       → FLAG: "Model suspended due to drift; observation unreliable"       │
│                                                                             │
│   If adversarial indicators:                                               │
│       → ESCALATE: "Possible adversarial conditions; human review required" │
│                                                                             │
│   If out of scope:                                                         │
│       → FLAG: "Observation outside model's approved capabilities"          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 7.3 Implementation

```prolog
% v1.2 Conflict Resolution with Preconditions

% Master resolution predicate
resolve_observation_document_conflict(Obs, Doc, Resolution) :-
    check_preconditions(Obs, PreconditionResult),
    (   PreconditionResult = all_passed
    ->  resolve_by_type(Obs, Doc, Resolution)
    ;   PreconditionResult = failed(Reasons)
    ->  Resolution = flag_for_review(Obs, Doc, precondition_failures(Reasons))
    ).

% Precondition checks
check_preconditions(Obs, Result) :-
    findall(Failure, precondition_failed(Obs, Failure), Failures),
    (   Failures = []
    ->  Result = all_passed
    ;   Result = failed(Failures)
    ).

% Individual precondition checks
precondition_failed(Obs, confidence_insufficient) :-
    observation_confidence(Obs, Conf),
    policy_threshold(confidence_override, Threshold),
    Conf < Threshold.

precondition_failed(Obs, sensor_degraded) :-
    observation_sensor(Obs, SensorId),
    sensor_status(SensorId, Status),
    Status \= operational.

precondition_failed(Obs, model_suspended) :-
    observation_model(Obs, ModelId),
    model_status(ModelId, Status),
    Status \= approved.

precondition_failed(Obs, model_drift_critical) :-
    observation_model(Obs, ModelId),
    model_drift_status(ModelId, critical).

precondition_failed(Obs, adversarial_indicators) :-
    observation_context(Obs, Context),
    adversarial_indicators_present(Context).

precondition_failed(Obs, out_of_scope) :-
    observation_model(Obs, ModelId),
    observation_feature_type(Obs, FeatureType),
    \+ model_approved_for(ModelId, FeatureType).

precondition_failed(Obs, environmental_ood) :-
    observation_environment(Obs, Env),
    observation_model(Obs, ModelId),
    model_training_distribution(ModelId, TrainDist),
    out_of_distribution(Env, TrainDist).

% Type-specific resolution (only called if preconditions pass)
resolve_by_type(Obs, Doc, prefer_observation(Obs, Doc, is_state)) :-
    conflict_type(Obs, Doc, is_state).

resolve_by_type(Obs, Doc, violation_detected(Doc, Obs)) :-
    conflict_type(Obs, Doc, ought_state).

resolve_by_type(Obs, Doc, flag_for_review(Obs, Doc, identity_conflict)) :-
    conflict_type(Obs, Doc, identity).

resolve_by_type(Obs, Doc, prefer_observation(Obs, Doc, temporal)) :-
    conflict_type(Obs, Doc, temporal).

resolve_by_type(Obs, Doc, prefer_document(Doc, Obs, intent)) :-
    conflict_type(Obs, Doc, intent).

resolve_by_type(Obs, Doc, flag_for_review(Obs, Doc, unknown_type)) :-
    conflict_type(Obs, Doc, unknown).
```

---

## 8. Revised Observation Node Schema (v1.2)

```yaml
observation_node:
  schema_version: "1.2"
  
  id: uuid
  type: observation
  
  # === TAINT (refined in v1.2) ===
  taint:
    type: enum
    values:
      - L0-RAW
      - L1-PERCEIVED
      - L1-INTERNAL  # New in v1.2
    description: |
      L0-RAW: Direct sensor reading (hardware counters, pixels, samples)
      L1-PERCEIVED: Model-mediated perception of external world
      L1-INTERNAL: Model-mediated self-observation
  
  # === SIGNAL PROVENANCE ===
  signal_provenance:
    sensor_id: string
    sensor_type: enum [camera, microphone, thermometer, clock, ...]
    sensor_status: enum [operational, degraded, failed]  # v1.2: explicit status
    timestamp: ISO-8601
    raw_hiri: "hiri://blob/..."  # Content-addressed via HIRI v2.1 protocol
    raw_hash: "sha256:..."
    # Note: Observation nodes are signed using HIRI Resolution Manifests.
    # The raw_hiri field references a HIRI v2.1 content-addressed identifier.
    # Full HIRI manifest integration (chain linking, compaction support)
    # is specified at the FNSR Integration Spec level, not within IRIS.
    
  # === MODEL PROVENANCE ===
  model_provenance:
    model_id: string
    model_version: string
    model_hash: "sha256:..."
    model_status: enum [approved, suspended, deprecated]  # v1.2: explicit status
    training_set_hash: "sha256:..."
    known_limitations: [string]
    drift_status: enum [ok, warn, critical]  # v1.2: dynamic drift
    drift_warnings: [string]  # v1.2: active warnings
    inference_timestamp: ISO-8601
    
  # === FEATURES (language-constrained in v1.2) ===
  features:
    type: array
    items:
      feature_id: string
      label: string  # Must pass language validation
      value: any
      confidence: float [0.0, 1.0]
      bounding_box: [x, y, w, h]  # If spatial
      # NO modal verbs, causal language, normative predicates
      
  # === EPISTEMIC METADATA ===
  epistemic:
    overall_confidence: float
    challengeable: true
    challenge_mechanism: string
    limitations: [string]
    preconditions_for_override:  # v1.2: explicit preconditions
      confidence_threshold: float
      sensor_status_required: operational
      model_status_required: approved
      drift_status_max: warn
      
  # === LANGUAGE COMPLIANCE (v1.2) ===
  language_compliance:
    validated: boolean
    validator_version: "1.2"
    violations_found: []  # Empty if compliant
    
  # === TEMPORAL ===
  temporal:
    observed_at: ISO-8601
    processed_at: ISO-8601
    valid_from: ISO-8601
    valid_until: ISO-8601 | null
```

---

## 9. INTUS v1.2 Full Specification

```yaml
service: intus
type: perception
modality: proprioceptive
version: 1.2
priority: CRITICAL

# === L0-RAW OUTPUTS (Direct hardware access) ===
l0_raw_outputs:
  - hardware_clock_ticks:
      source: "hardware TSC register"
      taint: L0-RAW
      unit: "ticks"
      
  - cpu_cycle_counter:
      source: "hardware performance counter"
      taint: L0-RAW
      unit: "cycles"
      
  - memory_allocation_events:
      source: "memory controller"
      taint: L0-RAW
      unit: "allocation records"
      
  - network_packet_counters:
      source: "NIC hardware"
      taint: L0-RAW
      unit: "packets (in/out)"
      
  - disk_io_counters:
      source: "storage controller"
      taint: L0-RAW
      unit: "bytes (read/write)"

# === L1-INTERNAL OUTPUTS (Aggregated/interpreted) ===
l1_internal_outputs:
  - cpu_utilization:
      source: "aggregation(cpu_cycles, time_window)"
      taint: L1-INTERNAL
      unit: "percentage"
      interpretation: "Model-mediated; heuristic thresholds"
      
  - memory_pressure:
      source: "heuristic(allocation_patterns, thresholds)"
      taint: L1-INTERNAL
      unit: "enum [low, medium, high, critical]"
      interpretation: "Classification based on configured thresholds"
      
  - cognitive_load:
      source: "aggregation(active_queries, pending_sagas, inference_depth)"
      taint: L1-INTERNAL
      unit: "composite score"
      interpretation: "Weighted combination; model-mediated"
      
  - service_health_status:
      source: "aggregation(health_checks, response_times)"
      taint: L1-INTERNAL
      unit: "enum [healthy, degraded, failed] per service"
      interpretation: "Classification based on thresholds"
      
  - error_pattern_detection:
      source: "pattern_recognition(error_logs)"
      taint: L1-INTERNAL
      unit: "detected patterns"
      interpretation: "Model-mediated pattern matching"
      
  - moral_injury_level:
      source: "character_accumulator"
      taint: L1-INTERNAL  # NOT L0-RAW
      unit: "injury score"
      interpretation: |
        This is an interpreted aggregate, not raw data.
        The accumulation formula is a model.
        The injury concept is a theoretical construct.
        The system should NOT have epistemic certainty about this.
      
  - threshold_proximity:
      source: "computation(moral_injury, configured_thresholds)"
      taint: L1-INTERNAL
      unit: "percentage to threshold"
      interpretation: "Derived value; depends on threshold configuration"

# === ORCHESTRATOR HOOKS (unchanged from v1.1) ===
orchestrator_hooks:
  - trigger: "moral_injury_level > warning_threshold"
    action: "emit SelfCareWarning event"
    
  - trigger: "moral_injury_level > critical_threshold"
    action: "emit SelfCareCritical event"
    response_options:
      - request_ethical_review
      - reduce_autonomy_tier
      - snapshot_and_pause
      
  - trigger: "cognitive_load > critical"
    action: "emit OverloadWarning event"
    
  - trigger: "service_health_status contains 'failed'"
    action: "emit DegradedState event"
```

---

## 10. Summary of Changes: v1.1 → v1.2

| Aspect | v1.1 | v1.2 |
|--------|------|------|
| **L1 naming** | "L1" (ambiguous — sounds like truth) | **L1-ASSERTED** (explicit: claims, not truth) |
| **INTUS taint** | All outputs L0-RAW | Split: **L0-RAW** (hardware) vs **L1-INTERNAL** (aggregates) |
| **Moral injury taint** | L0-RAW (implying certainty) | **L1-INTERNAL** (acknowledging interpretation) |
| **Forge constraints** | Implicit | **Explicit prohibitions** (no fusion, no selection, no normalization) |
| **Language enforcement** | Recommended | **Schema-validated** (prohibited terms rejected automatically) |
| **Model drift** | Not specified | **Full governance** (metrics, thresholds, auto-actions) |
| **Conflict preconditions** | Implicit | **Explicit** (confidence, sensor status, model status, drift, adversarial) |
| **Model registry** | Static | **Dynamic** (drift state, approval history, automatic suspension) |

---

## 11. ARIADNE Compliance Check

### The Plot Alignment

| Non-Negotiable | v1.2 Alignment |
|----------------|----------------|
| **No Oracle Claims** | L1-PERCEIVED and L1-INTERNAL explicitly probabilistic; L1-ASSERTED explicitly "claimed, not verified" |
| **Provenance Always** | Sensor + model + drift provenance on every observation |
| **Uncertainty Visible** | Confidence scores mandatory; drift warnings visible; precondition failures flagged |
| **Speculation Firewalled** | Clear taint hierarchy; language constraints prevent interpretive creep |
| **Moral Injury Real** | INTUS tracks injury, but as L1-INTERNAL (system doesn't have false certainty about itself) |
| **Auditability** | Full provenance chain; drift logs; language validation logs |

### Tension Log Updates

**IRIS-T-001: Model-Mediated Perception vs. Raw Signal**
- Status: **Resolved** — L0-RAW/L1-PERCEIVED split operationalized with drift governance
- Note: This is an IRIS-local tension. Not to be confused with ARIADNE global T-007 (Tool-to-Person Threshold).

**IRIS-T-002: Self-Knowledge Certainty**
- First identified: v1.2 critique
- Description: System should not have epistemic certainty about its own interpreted states
- Resolution: INTUS outputs stratified; moral injury is L1-INTERNAL, not L0-RAW
- Status: **Resolved**
- Note: This is an IRIS-local tension. Not to be confused with ARIADNE global T-008 (Worldview Fixity vs. Evolution).

---

## 12. Conclusion

IRIS v1.2 addresses all five must-fix issues from the critique:

1. ✅ **L1 → L1-ASSERTED**: Documents are claims, not truth
2. ✅ **INTUS stratified**: Hardware counters are L0-RAW; aggregates are L1-INTERNAL
3. ✅ **Forge constrained**: Explicit prohibition list with enforcement
4. ✅ **Drift governance**: Metrics, thresholds, automatic actions, approval history
5. ✅ **Conflict preconditions**: IRIS only wins when sensor/model/confidence all valid

Additionally:
- ✅ **Language enforcement**: Schema-level validation of prohibited terms
- ✅ **Moral injury reclassified**: System doesn't have false certainty about itself

The result is a perception layer that:
- Refuses to claim certainty it doesn't have
- Tracks the provenance of every inference
- Knows its models can drift and governs accordingly
- Distinguishes what it measures from what it interprets
- Enforces epistemic discipline at the schema level

**IRIS v1.2 is ready for implementation review.**

---

*"The beginning of wisdom is the definition of terms."*  
*— Socrates*

---

**IRIS v1.2** — Perception with Epistemic Discipline
