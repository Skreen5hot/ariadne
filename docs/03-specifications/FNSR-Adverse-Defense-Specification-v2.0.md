# FNSR Adversarial Defense Specification

**Document ID:** `adversarial-spec-01`
**Version:** 2.0.0
**Status:** HARDENED
**Classification:** FNSR Cross-Cutting Security Component

-----

## Document History

|Version    |Date      |Changes                                                                                                                                                                                                                                                |
|-----------|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|1.0.0-draft|2026-02-06|Initial specification                                                                                                                                                                                                                                  |
|1.1.0      |2026-02-06|Post-review revision: correlated-layer risk math, JSON-LD context expansion DoS, pass-with-flag taint elevation, feedback loop concurrency, quarantine directory hashing, rolling baseline protocol, ReDoS mitigation, INTUS recursion analysis        |
|2.0.0      |2026-02-06|Hardened final: risk score calibration semantics (§4.3.0), governance degradation policy (§5.8), feedback poisoning controls (§4.6), probationary release lifecycle (§5.2, §5.4, §5.5), derivative artifact requirements (§11), resolved open questions|

## Review History

|Reviewer|Date      |Verdict               |Key Findings                                                                                                                                                                                                                        |
|--------|----------|----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|Review 1|2026-02-06|APPROVED_WITH_COMMENTS|Independence assumption in cumulative risk; JSON-LD context expansion DoS (critical); pass-with-flag enforcement gap; feedback loop race condition; quarantine directory performance; rolling baseline staleness; ReDoS in SIS regex|
|Review 2|2026-02-06|APPROVED_WITH_COMMENTS|Risk score semantic ambiguity; governance burden under-specified; feedback loop poisoning; L5 one-way gravity / false-positive black holes; cognitive overload for implementers                                                     |

## Referenced Specifications

|Spec ID                      |Name                                      |Relevance                      |
|-----------------------------|------------------------------------------|-------------------------------|
|`sis-core-01`                |Sanitization & Ingestion Service          |Layer 1: Syntactic defense     |
|`eccps-core-01`              |Epistemically Constrained Claim Processing|Layer 2: Semantic defense      |
|IRIS v1.1                    |Integrated Real-time Input Sensing        |Layer 3: Perception defense    |
|IEE                          |Integral Ethics Engine                    |Ethical reasoning integrity    |
|HIRI v2.1                    |Hash-IRI Protocol                         |Privacy budget & provenance    |
|CSS                          |Counterfactual Simulation Service         |L4 sandbox integrity           |
|FNSR Integration Spec v1.0 §3|Integration Architecture                  |Defense checkpoint coordination|
|FNSR Architecture v2.1 §5    |Taint Architecture                        |L5 taint propagation rules     |

-----

## 1. Purpose and Scope

### 1.1 The Problem

FNSR’s defense-in-depth strategy currently spans three services — SIS (syntactic), ECCPS (semantic), and IRIS (perception) — without a unified threat model. Each service addresses a slice of the adversarial surface, but no specification catalogs the threat taxonomy, defines the attacker model, or specifies coordinated response across layers. This creates three gaps:

1. **No shared vocabulary.** SIS calls something a “quarantine trigger,” ECCPS calls it an “epistemic failure,” and IRIS calls it a “sensor anomaly.” These may describe the same adversarial event, and no schema maps between them.
1. **No coordinated intelligence.** When SIS detects a homoglyph substitution but passes the content (because confidence was below threshold), ECCPS has no visibility into that near-miss. When ECCPS flags a claim as structurally valid but ontologically bizarre, SIS cannot learn from the detection.
1. **No quarantine lifecycle.** Content flagged as L5 (Adversarial) enters quarantine, but the existing specs do not define what happens next — review, release, permanent rejection, or escalation.

### 1.2 What This Spec Does

This specification defines:

- The unified threat taxonomy across all FNSR defense layers
- The adversarial model: what capabilities attackers are assumed to have
- The defense coordination protocol: how SIS, ECCPS, IRIS, and IEE share threat intelligence
- The quarantine lifecycle: what happens to L5 content from detection to resolution
- L5 taint propagation rules and their relationship to the epistemic firewall
- Adversarial testing requirements for each service
- Incident response procedures
- Governance degradation policy for sustained-pressure scenarios
- Derivative artifact requirements for implementer adoption

### 1.3 What This Spec Does Not Do

This specification does not:

- Replace or override the individual service specs (SIS, ECCPS, IRIS, IEE)
- Define content moderation policy (what content is “good” or “bad”)
- Implement censorship or topic-based filtering
- Assume the existence of infrastructure (databases, message brokers, background workers)

### 1.4 Architectural Constraint Compliance

This specification conforms to the Edge-Canonical First Principle. All defense logic described here must be executable via `node index.js` or in a browser. Cloud deployments are derivative optimizations. The spec test applies: a developer must be able to evaluate, reason about, and execute this system using only a browser, a local Node.js runtime, and JSON-LD files.

### 1.5 How to Read This Document (v2.0)

This specification is dense by design — it coordinates across the entire FNSR defense surface. To manage cognitive load, it is structured in layers of detail:

**For architects:** Read §1–§2 (scope and threat model), §4.1–§4.3 (coordination protocol), §5.7 (epistemic firewall), §9 (moral alignment).

**For service implementers:** Read your layer’s threat categories in §3.2, your testing requirements in §6.1, and the relevant Threat Playbook in Appendix D. The Layer Defense Profiles in Appendix E provide a self-contained view of each service’s defense responsibilities.

**For governance reviewers:** Read §5 (quarantine lifecycle), §5.8 (governance degradation), §7 (incident response).

**For security auditors:** Read §2 (adversarial model), §3 (full taxonomy), §6 (testing requirements), §8.4 (regex safety), Appendix B (spec test).

Derivative artifacts (Appendix D: Threat Playbooks, Appendix E: Layer Defense Profiles) are non-normative but authoritative. They are derived from the normative sections and must be updated when the normative sections change.

-----

## 2. Adversarial Model

### 2.1 Attacker Capabilities

The threat model assumes attackers with the following capabilities, ordered by sophistication:

|Tier  |Name                  |Capabilities                                                                   |Example                                                                                                                                      |
|------|----------------------|-------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------|
|**T1**|Script Kiddie         |Copy-paste known injection payloads; no understanding of FNSR internals        |SQLi patterns embedded in document submissions                                                                                               |
|**T2**|Informed Outsider     |Reads FNSR specs (open-source); crafts payloads targeting documented boundaries|Exploiting the SIS/ECCPS boundary by crafting content that is syntactically clean but semantically adversarial                               |
|**T3**|Adaptive Attacker     |Probes defenses, observes quarantine decisions, iterates                       |Discovers SIS’s statistical thresholds via binary search; crafts homoglyphs that sit below the 3σ anomaly threshold                          |
|**T4**|Ontological Attacker  |Understands BFO, FNSR’s epistemic hierarchy, and the taint system              |Introduces ontologically valid but epistemically poisoned content — claims that pass ECCPS validation but subtly corrupt downstream reasoning|
|**T5**|Insider / Supply Chain|Has access to pattern databases, model weights, or adapter code                |Modifies the SIS pattern database to create blind spots; poisons IRIS training data                                                          |

**Design Principle:** The system must withstand T1–T3 without human intervention. T4 must be detected and flagged for human review. T5 requires governance controls outside this specification’s scope (addressed in ARCHON governance framework).

### 2.2 Attacker Goals

|Goal                       |Target                                                                                       |Detection Layer                         |
|---------------------------|---------------------------------------------------------------------------------------------|----------------------------------------|
|**Injection**              |Execute unintended operations via crafted input                                              |SIS (primary), ECCPS (secondary)        |
|**Semantic Manipulation**  |Introduce plausible-but-false claims that corrupt the knowledge graph                        |ECCPS (primary), IEE (secondary)        |
|**Ontological Poisoning**  |Corrupt the ontological foundations — class hierarchies, property definitions, BFO alignments|ECCPS (primary), W2Fuel (secondary)     |
|**Perception Manipulation**|Feed falsified sensor data to IRIS                                                           |IRIS (primary)                          |
|**Model Drift**            |Gradually degrade ML components through adversarial training data                            |Cross-cutting; requires drift monitoring|
|**Privacy Budget Gaming**  |Extract more information than HIRI’s privacy budget permits through compositional attacks    |HIRI privacy accumulators               |
|**Taint Escape**           |Promote L5 content to L4 or below, bypassing quarantine                                      |Taint enforcement layer                 |
|**Simulation Exploitation**|Use CSS to perform computations the attacker couldn’t perform directly                       |CSS sandbox enforcement                 |
|**Parser Exploitation**    |Attack the JSON-LD processing layer itself (context expansion, resource exhaustion)          |SIS pre-parse validation                |
|**Governance Exhaustion**  |Overwhelm human review capacity to force threshold loosening or review fatigue               |Governance degradation policy (§5.8)    |

-----

## 3. Threat Taxonomy

### 3.1 Taxonomy Schema (JSON-LD)

Every threat in the taxonomy is a JSON-LD document conforming to this schema. This is the canonical representation; internal optimizations (hash maps, compiled patterns) must be losslessly derivable from it.

```json
{
  "@context": {
    "@vocab": "https://fnsr.dev/adversarial/",
    "bfo": "http://purl.obolibrary.org/obo/BFO_",
    "sis": "https://fnsr.dev/sis/",
    "eccps": "https://fnsr.dev/eccps/",
    "iris": "https://fnsr.dev/iris/",
    "taint": "https://fnsr.dev/taint/"
  },
  "@type": "ThreatClass",
  "@id": "https://fnsr.dev/adversarial/threat/{threat_id}",

  "threatId": "ADV-{category}-{sequence}",
  "name": "Human-readable threat name",
  "category": "One of: injection | semantic | ontological | perception | drift | privacy | taint_escape | simulation | governance",
  "description": "What this threat does and why it matters",

  "attackerTier": ["T1", "T2"],
  "attackerGoal": "injection",

  "affectedLayers": [
    {
      "layer": "sis",
      "role": "primary_detection",
      "detectionMethod": "regex | byte_sequence | statistical | ml_classifier"
    }
  ],

  "taintImplication": {
    "detected": "L5",
    "confidence_below_threshold": "flag_for_review",
    "propagation": "immediate_quarantine | contained | escalated"
  },

  "mitigations": [
    {
      "layer": "sis",
      "mechanism": "Pattern SIS-PAT-INJ-00012",
      "effectiveness": "T1-T2 (known variants)"
    }
  ],

  "testVectors": [
    {
      "vectorId": "TV-INJ-001",
      "input": "...",
      "expectedDetection": "sis",
      "expectedOutcome": "quarantine"
    }
  ],

  "metadata": {
    "created": "2026-02-06T00:00:00Z",
    "lastUpdated": "2026-02-06T00:00:00Z",
    "version": "2.0.0",
    "author": "adversarial-spec-01"
  }
}
```

### 3.2 Threat Categories

#### 3.2.1 Injection Attacks (INJ)

**Layer:** SIS (primary detection)

|Threat ID  |Name                         |Tier |Description                                                                         |
|-----------|-----------------------------|-----|------------------------------------------------------------------------------------|
|ADV-INJ-001|Classic Prompt Injection     |T1   |Direct injection of instruction-like content into document payloads                 |
|ADV-INJ-002|Homoglyph Injection          |T1–T2|Cyrillic/Latin substitution to bypass pattern matching                              |
|ADV-INJ-003|Invisible Character Injection|T1–T2|Zero-width joiners, RTL overrides, tag characters                                   |
|ADV-INJ-004|Encoding Normalization Attack|T2   |Overlong UTF-8, mixed encoding to bypass normalization                              |
|ADV-INJ-005|JSON Structure Attack        |T2   |Deeply nested objects, hash collisions, quadratic blowup                            |
|ADV-INJ-006|Indirect Prompt Injection    |T2–T3|Adversarial content embedded in documents that are later processed by LLM components|
|ADV-INJ-007|Polyglot Payload             |T3   |Content that is simultaneously valid across multiple parsing contexts               |
|ADV-INJ-008|Remote Context Expansion     |T2–T3|Malicious `@context` URLs that are slow, massive, recursive, or hostile             |

**SIS Boundary:** SIS detects INJ-001 through INJ-005 via pattern matching, byte analysis, and structural validation. INJ-006 and INJ-007 require ECCPS collaboration. INJ-008 is mitigated at the SIS pre-parse layer before JSON-LD expansion occurs (§3.3).

#### 3.2.2 Semantic Manipulation (SEM)

**Layer:** ECCPS (primary detection)

|Threat ID  |Name                      |Tier |Description                                                                                                     |
|-----------|--------------------------|-----|----------------------------------------------------------------------------------------------------------------|
|ADV-SEM-001|Plausible Falsehood       |T3   |Claims that pass structural validation but assert false facts                                                   |
|ADV-SEM-002|Causal Confabulation      |T3   |Claims asserting causal relationships with plausible but unverified mechanisms                                  |
|ADV-SEM-003|Provenance Laundering     |T3–T4|Fabricating citation chains to ground false claims in apparent authority                                        |
|ADV-SEM-004|Epistemic Grooming        |T4   |Gradually introducing claims that shift baseline assumptions across multiple submissions                        |
|ADV-SEM-005|Defeasibility Exploitation|T4   |Crafting claims designed to defeat existing defeasible conclusions via technically valid but misleading evidence|

#### 3.2.3 Ontological Poisoning (ONT)

**Layer:** ECCPS + W2Fuel (primary detection)

|Threat ID  |Name                          |Tier |Description                                                                       |
|-----------|------------------------------|-----|----------------------------------------------------------------------------------|
|ADV-ONT-001|Class Hierarchy Corruption    |T4   |Introducing subclass relationships that subtly violate BFO constraints            |
|ADV-ONT-002|Property Domain/Range Widening|T4   |Expanding property constraints to permit invalid inferences                       |
|ADV-ONT-003|Disjointness Violation        |T4   |Creating individuals that span disjoint classes, collapsing ontological boundaries|
|ADV-ONT-004|Import Chain Poisoning        |T4–T5|Modifying imported ontologies to inject invalid axioms                            |

**Detection Mechanism:** W2Fuel maintains the canonical ontology. Any claim requiring ontological modification passes through a change protocol: sandbox isolation, OWL DL consistency check, human review, HIRI provenance audit trail.

#### 3.2.4 Perception Manipulation (PER)

**Layer:** IRIS (primary detection)

|Threat ID  |Name                          |Tier|Description                                                                               |
|-----------|------------------------------|----|------------------------------------------------------------------------------------------|
|ADV-PER-001|Adversarial Image Perturbation|T3  |Pixel-level modifications that cause misclassification                                    |
|ADV-PER-002|Sensor Spoofing               |T3  |Physical-layer attacks on sensors (laser injection, audio replay)                         |
|ADV-PER-003|Temporal Manipulation         |T3  |Feeding CHRONOS falsified timestamps or replay data                                       |
|ADV-PER-004|INTUS Confusion               |T4  |Crafting inputs that cause self-monitoring to report normal when the system is compromised|

**IRIS Boundary (per v1.1 hardening):** Multi-sensor corroboration, confidence thresholds, model provenance tracking, INTUS health monitoring.

#### 3.2.5 Model Drift Attacks (DFT)

**Layer:** Cross-cutting

|Threat ID  |Name                    |Tier |Description                                                                  |
|-----------|------------------------|-----|-----------------------------------------------------------------------------|
|ADV-DFT-001|SIS Classifier Poisoning|T4–T5|Adversarial training data that degrades ML classifier accuracy               |
|ADV-DFT-002|IRIS Model Degradation  |T4–T5|Gradual corruption of perception models through carefully crafted inputs     |
|ADV-DFT-003|Semantic Drift          |T4   |Slow redefinition of concept boundaries across many valid-seeming submissions|

**Detection Mechanism:**

```json
{
  "@type": "DriftDetectionConfig",
  "baseline": {
    "source": "certified_model_snapshot",
    "hiri_manifest": "hiri://key:ed25519:.../model/baseline/v1.2.3"
  },
  "monitoring": {
    "metric": "classification_accuracy_on_holdout",
    "threshold_degradation_percent": 2.0,
    "evaluation_interval": "per_100_inputs",
    "comparison_method": "sliding_window"
  },
  "response": {
    "degradation_detected": "alert_and_freeze_model_updates",
    "degradation_confirmed": "rollback_to_baseline"
  }
}
```

**Rolling Baseline Protocol:** A static baseline becomes stale over time. The rolling baseline protocol allows promotion of new certified snapshots through a governance process requiring: human review, 100% adversarial test suite pass rate, holdout accuracy meeting or exceeding the previous baseline, drift budget ≤ 5% per metric, full HIRI provenance chain, and retained rollback capability.

#### 3.2.6 Privacy Budget Gaming (PRV)

**Layer:** HIRI (primary enforcement)

|Threat ID  |Name                           |Tier |Description                                                                           |
|-----------|-------------------------------|-----|--------------------------------------------------------------------------------------|
|ADV-PRV-001|Compositional Re-identification|T3   |Requesting multiple narrowly-scoped proofs that compose to uniquely identify a subject|
|ADV-PRV-002|Cross-Verifier Collusion       |T3–T4|Multiple verifiers sharing proof results to exceed individual budgets                 |
|ADV-PRV-003|Budget Reset Attack            |T4   |Exploiting credential renewal to reset privacy accumulators                           |

#### 3.2.7 Taint Escape (TNT)

**Layer:** Taint enforcement (cross-cutting)

|Threat ID  |Name                  |Tier|Description                                                                         |
|-----------|----------------------|----|------------------------------------------------------------------------------------|
|ADV-TNT-001|L5-to-L4 Promotion    |T3  |Crafting quarantined content that appears benign upon review to escape to L4 sandbox|
|ADV-TNT-002|L4 Sandbox Escape     |T4  |Exploiting CSS to produce outputs treated as non-hypothetical downstream            |
|ADV-TNT-003|Taint Marker Stripping|T3  |Manipulating JSON-LD context or processing to remove `@protected` taint markers     |
|ADV-TNT-004|Taint Level Conflation|T3  |Merging L5 content with L0/L1 content to obscure L5 provenance                      |

**Enforcement:** Type-level (`TaintedResult<T>`), JSON-LD `@protected` contexts, adapter-level publish rejection.

#### 3.2.8 Simulation Exploitation (SIM)

**Layer:** CSS sandbox (primary enforcement)

|Threat ID  |Name                   |Tier |Description                                                                |
|-----------|-----------------------|-----|---------------------------------------------------------------------------|
|ADV-SIM-001|Side-Channel Extraction|T4   |Crafting counterfactual scenarios whose results leak real-state information|
|ADV-SIM-002|Resource Exhaustion    |T2–T3|Computationally expensive counterfactuals for denial of service            |
|ADV-SIM-003|Simulation-as-Oracle   |T4   |Using CSS to answer unauthorized questions indirectly                      |

#### 3.2.9 Governance Attacks (GOV) — v2.0

**Layer:** Human review process

|Threat ID  |Name              |Tier |Description                                                                                                   |
|-----------|------------------|-----|--------------------------------------------------------------------------------------------------------------|
|ADV-GOV-001|Review Flooding   |T3   |Overwhelming quarantine review capacity with high-volume near-threshold submissions to induce backlog pressure|
|ADV-GOV-002|Threshold Fatigue |T3   |Sustained borderline submissions designed to make reviewers rubber-stamp approvals                            |
|ADV-GOV-003|Feedback Poisoning|T3–T4|Generating feedback events that gradually bias SIS pattern evolution toward attacker-favorable blind spots    |

### 3.3 Context Security Policy

JSON-LD context expansion is a pre-semantic attack surface. FNSR operates in **local-context-only mode** by default.

```json
{
  "@type": "ContextSecurityPolicy",
  "loadingPolicy": "local_only",
  "allowedContexts": [
    { "uri": "https://fnsr.dev/adversarial/", "localPath": "contexts/fnsr-adversarial.jsonld", "hash": "sha256:abc123..." },
    { "uri": "https://fnsr.dev/taint/", "localPath": "contexts/fnsr-taint.jsonld", "hash": "sha256:def456..." },
    { "uri": "https://fnsr.dev/sis/", "localPath": "contexts/fnsr-sis.jsonld", "hash": "sha256:ghi789..." },
    { "uri": "https://fnsr.dev/eccps/", "localPath": "contexts/fnsr-eccps.jsonld", "hash": "sha256:jkl012..." },
    { "uri": "https://fnsr.dev/iris/", "localPath": "contexts/fnsr-iris.jsonld", "hash": "sha256:mno345..." },
    { "uri": "https://fnsr.dev/css/", "localPath": "contexts/fnsr-css.jsonld", "hash": "sha256:pqr678..." },
    { "uri": "http://purl.obolibrary.org/obo/BFO_", "localPath": "contexts/bfo.jsonld", "hash": "sha256:stu901..." },
    { "uri": "https://hiri-protocol.org/spec/v2.1", "localPath": "contexts/hiri-v2.1.jsonld", "hash": "sha256:vwx234..." }
  ],
  "unknownContextBehavior": "reject",
  "enforcement": {
    "stage": "pre_parse",
    "position": "before SIS Stage 0 (JSON Envelope Validation)",
    "rejectionCode": "CONTEXT_NOT_ALLOWED",
    "taintImplication": "L5 if typosquatting detected; flag_for_review if plausible external ontology"
  },
  "contextUpdateProtocol": {
    "description": "Same governance process as baseline promotion: human review, hash verification, HIRI provenance.",
    "automated": false
  }
}
```

**Implementation:** Parse as plain JSON first, extract all `@context` values, compare against allow-list, reject unknown contexts before any JSON-LD expansion. The JSON-LD processor never fetches a remote URL.

-----

## 4. Defense Coordination Protocol

### 4.1 Design Principle: Shared Intelligence Without Shared Infrastructure

The coordination protocol uses the pipeline itself as the communication channel. Each service’s output includes defense-relevant metadata that downstream services inspect. There is no ambient bus; there is a pipeline that carries intelligence alongside content.

### 4.2 Defense Metadata Schema

Every event flowing through the FNSR pipeline carries an optional `adversarial:assessment` block:

```json
{
  "@context": { "adversarial": "https://fnsr.dev/adversarial/" },
  "adversarial:assessment": {
    "@type": "adversarial:DefenseAssessment",
    "adversarial:layerReports": [
      {
        "adversarial:layer": "sis",
        "adversarial:timestamp": "2026-02-06T12:00:00.001Z",
        "adversarial:findings": [
          {
            "adversarial:threatRef": "ADV-INJ-002",
            "adversarial:calibratedRisk": 0.72,
            "adversarial:calibrationMethod": "holdout_validation_2026Q1",
            "adversarial:severity": "MEDIUM",
            "adversarial:action": "passed_with_flag",
            "adversarial:evidence": {
              "adversarial:patternId": "SIS-PAT-HGL-00042",
              "adversarial:matchCount": 3,
              "adversarial:matchLocations": [
                { "offset": 145, "length": 1 },
                { "offset": 203, "length": 1 },
                { "offset": 891, "length": 1 }
              ]
            }
          }
        ],
        "adversarial:aggregateRiskScore": 0.42,
        "adversarial:calibrationRef": "hiri://key:ed25519:.../calibration/sis/2026Q1"
      }
    ],
    "adversarial:cumulativeRisk": {
      "adversarial:score": 0.58,
      "adversarial:baseScore": 0.42,
      "adversarial:corroborationApplied": false,
      "adversarial:escalationThreshold": 0.75,
      "adversarial:escalated": false,
      "adversarial:taintElevation": "L2-FLAGGED"
    }
  }
}
```

### 4.3 Cumulative Risk Computation

#### 4.3.0 Risk Score Semantics (v2.0 — Normative)

**The problem (identified in Review 2):** Prior versions left `layer.risk` semantically ambiguous — it oscillated between detector confidence, posterior probability, and heuristic severity score. These are not interchangeable, but the cumulative risk math treated them as if they were. A future implementer could “optimize” SIS risk scores without realizing they were breaking cross-layer calibration.

**Normative Constraint:**

> `layer.risk` MUST represent a **calibrated estimate of P(adversarial | observed evidence at this layer)** — the probability that the content is adversarial, given the evidence this layer observed.
> 
> It is NOT a raw classifier confidence, a severity rating, or a heuristic score. It is a probability.

**What “calibrated” means:**

A risk score is calibrated if, across all content that receives risk score *r* from a given layer, approximately fraction *r* of that content is actually adversarial. Concretely: if SIS assigns risk 0.70 to 100 documents, approximately 70 of those documents should turn out to be genuinely adversarial upon human review.

**Calibration requirements:**

|Requirement                      |Description                                                                                                                                                                                          |
|---------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|**Calibration dataset**          |Each layer must maintain a labeled holdout set of inputs with known adversarial/benign ground truth. This is a JSON-LD file.                                                                         |
|**Calibration method**           |Risk scores are mapped from raw detector outputs (confidence, severity, anomaly scores) through a calibration function trained on the holdout set. Platt scaling, isotonic regression, or equivalent.|
|**Calibration frequency**        |Re-calibrated whenever the holdout set is updated (minimum quarterly, or after any baseline promotion per §3.2.5).                                                                                   |
|**Calibration provenance**       |Each calibration run produces a HIRI-signed record documenting the holdout set version, calibration method, resulting calibration curve, and measured calibration error (ECE or Brier score).        |
|**Cross-layer calibration audit**|Annually, calibration curves from all layers must be jointly reviewed to ensure they are on the same probability scale. A cross-layer calibration report is a governance deliverable.                |

**Calibration record schema:**

```json
{
  "@type": "adversarial:CalibrationRecord",
  "@id": "https://fnsr.dev/adversarial/calibration/{layer}/{period}",

  "layer": "sis",
  "period": "2026Q1",
  "holdoutSet": {
    "hiri_manifest": "hiri://key:ed25519:.../calibration/sis/holdout/2026Q1",
    "totalSamples": 2000,
    "adversarialSamples": 340,
    "benignSamples": 1660
  },
  "calibrationMethod": "isotonic_regression",
  "calibrationCurve": {
    "bins": [
      { "predictedMin": 0.0, "predictedMax": 0.1, "actualRate": 0.02, "sampleCount": 450 },
      { "predictedMin": 0.1, "predictedMax": 0.2, "actualRate": 0.14, "sampleCount": 320 },
      { "predictedMin": 0.2, "predictedMax": 0.3, "actualRate": 0.23, "sampleCount": 280 }
    ]
  },
  "metrics": {
    "expectedCalibrationError": 0.031,
    "brierScore": 0.087,
    "maxCalibrationGap": 0.05
  },
  "provenance": {
    "hiri:manifest": "hiri://key:ed25519:.../calibration/sis/2026Q1/v1"
  }
}
```

**Degraded operation:** If a layer’s calibration is stale (older than the configured maximum age), its risk scores are treated as *uncalibrated*. Uncalibrated scores enter the cumulative risk computation with a penalty: they are capped at 0.5 (regardless of raw value) and flagged in the assessment. This prevents stale calibration from producing false confidence in either direction.

**Edge-Canonical Compliance:** The calibration holdout set is a JSON-LD file. The calibration function is a pure function (lookup table from isotonic regression, or polynomial from Platt scaling). No infrastructure required.

#### 4.3.1 Base Risk (Independence Model)

```
baseRisk = 1 - ∏(1 - layerRisk_i)
```

#### 4.3.2 Corroboration Multiplier

When two or more layers report calibrated risk above 0.3, the corroboration multiplier amplifies the cumulative score:

```javascript
function computeCumulativeRisk(layerReports) {
  // Step 1: Base risk (independence model)
  let baseRisk = 1 - layerReports.reduce(
    (acc, layer) => acc * (1 - layer.risk), 1
  );

  // Step 2: Corroboration check
  const CORROBORATION_THRESHOLD = 0.3;
  const corroboratingLayers = layerReports.filter(
    l => l.risk > CORROBORATION_THRESHOLD
  );

  let corroborationApplied = false;
  let finalRisk = baseRisk;

  if (corroboratingLayers.length >= 2) {
    finalRisk = Math.min(0.99, baseRisk * 1.25);
    corroborationApplied = true;
  }

  if (corroboratingLayers.length >= 3) {
    finalRisk = Math.min(0.99, baseRisk * 1.5);
  }

  return { baseRisk, finalRisk, corroborationApplied };
}
```

|SIS Risk|ECCPS Risk|IRIS Risk|Base Risk|Corroboration  |Final Risk|Action               |
|--------|----------|---------|---------|---------------|----------|---------------------|
|0.42    |0.00      |0.00     |0.42     |None           |0.42      |Pass with flag       |
|0.42    |0.55      |0.00     |0.739    |2-layer (×1.25)|0.924     |Quarantine (priority)|
|0.42    |0.55      |0.35     |0.831    |3-layer (×1.5) |0.99      |Quarantine (priority)|
|0.10    |0.10      |0.10     |0.271    |None           |0.271     |Pass clean           |
|0.90    |0.00      |0.00     |0.90     |None           |0.90      |Quarantine           |
|0.35    |0.35      |0.35     |0.725    |3-layer (×1.5) |0.99      |Quarantine (priority)|

#### 4.3.3 Risk Actions and Taint Elevation

|Cumulative Risk|Action                                   |Taint Elevation    |
|---------------|-----------------------------------------|-------------------|
|< 0.30         |Pass clean                               |None               |
|0.30 – 0.75    |Pass with mandatory taint elevation      |L2-FLAGGED (§4.3.4)|
|0.75 – 0.95    |Quarantine with standard review          |L5                 |
|≥ 0.95         |Immediate quarantine with priority review|L5                 |

#### 4.3.4 L2-FLAGGED: Mandatory Acknowledgment

Content in the 0.30–0.75 risk range is taint-elevated to **L2-FLAGGED**, a sub-level of L2 (Defeasible) that requires explicit acknowledgment before consumption.

L2-FLAGGED semantics: remains below the epistemic firewall; can participate in defeasible reasoning only after the consuming service explicitly acknowledges the defense flag; the acknowledgment is recorded in provenance.

```typescript
class FlaggedContent<T> {
  private constructor(
    private readonly _content: T,
    private readonly _assessment: DefenseAssessment,
    private readonly _originalTaint: TaintLevel
  ) {}

  acknowledgeDefenseFlag(
    serviceId: string,
    justification: string
  ): { content: T; acknowledgment: FlagAcknowledgment } {
    return {
      content: this._content,
      acknowledgment: {
        serviceId, justification,
        assessment: this._assessment,
        timestamp: new Date().toISOString(),
        originalTaint: this._originalTaint
      }
    };
  }

  get content(): never {
    throw new FlaggedContentError(
      'Content has adversarial flags. Call acknowledgeDefenseFlag() first.'
    );
  }
}
```

**Why L2-FLAGGED and not L3:** L3 means “abductive hypothesis from AES” and sits above the epistemic firewall. Overloading L3 would corrupt its semantics and block legitimate input from production. L2-FLAGGED preserves epistemic character while adding a mandatory acknowledgment gate.

### 4.4 Near-Miss Intelligence Sharing

SIS near-misses (confidence below quarantine threshold) are recorded in the `adversarial:assessment`. ECCPS inspects this block on its input and applies heightened scrutiny. No subscription model required — the pipeline carries the intelligence.

### 4.5 Feedback Loop (Asynchronous, Non-Required)

When ECCPS detects a semantic attack that SIS should have caught syntactically, it emits a `adversarial:feedbackEvent` as an individual JSON-LD file with a UUID filename:

```
feedback/
  FB-{uuid}.jsonld
  FB-{uuid}.jsonld
  ...
feedback/processed/
  FB-{uuid}.jsonld  (moved here after consumption)
```

Each feedback event is a single atomic file write. No shared journal, no append coordination, no file locks. UUID filenames guarantee uniqueness. The consuming service reads the directory, processes each file independently, and moves processed files to `feedback/processed/`.

**Critical:** This feedback loop is an optimization, not a requirement. SIS must function correctly without it. Offline is a first-class mode.

### 4.6 Feedback Poisoning Controls (v2.0)

**The problem (identified in Review 2):** Even though feedback ingestion is optional, it is not safe by default. A compromised ECCPS (or an attacker who can generate feedback events) could slowly bias SIS pattern evolution toward attacker-favorable blind spots — never tripping explicit drift thresholds but gradually eroding detection capability.

**Feedback is untrusted input.** The same defense posture FNSR applies to external content must apply to inter-layer feedback. Feedback events enter a **feedback quarantine** before they can influence pattern databases or detection behavior.

#### 4.6.1 Feedback Ingestion Pipeline

```
Feedback event arrives (UUID file in feedback/)
  │
  ▼
Stage 1: Rate limiting
  │   - Max 10 feedback events per source layer per hour
  │   - Exceeding rate limit: excess events queued, not discarded
  │   - Sustained excess (>100 queued): trigger GOV-001 alert
  │
  ▼
Stage 2: Feedback quarantine
  │   - Event placed in feedback/quarantine/
  │   - Not yet eligible to influence patterns
  │
  ▼
Stage 3: Confidence threshold check
  │   - Suggested pattern must have evidence from ≥ 3 independent inputs
  │   - Single-input feedback is recorded but not actionable
  │
  ▼
Stage 4: Human review for pattern promotion
  │   - Reviewer examines feedback evidence
  │   - Reviewer approves, modifies, or rejects suggested pattern
  │   - Approved patterns enter SIS pattern database as CANDIDATE
  │
  ▼
Stage 5: Candidate pattern validation
  │   - CANDIDATE patterns run in shadow mode (detect but don't act)
  │   - After validation period: promote to ACTIVE or discard
  │
  ▼
Pattern database updated
```

#### 4.6.2 Feedback Quarantine Schema

```json
{
  "@type": "adversarial:FeedbackQuarantineRecord",
  "feedbackId": "FB-{uuid}",
  "source": "eccps",
  "received": "2026-02-06T14:00:00Z",
  "state": "QUARANTINED",
  "corroboratingInputs": 0,
  "requiredCorroboration": 3,
  "suggestedPattern": { "...": "Pattern definition" },
  "reviewHistory": []
}
```

#### 4.6.3 Feedback Rate Limiting

|Parameter                     |Value                    |Rationale                                     |
|------------------------------|-------------------------|----------------------------------------------|
|Max events per source per hour|10                       |Prevents feedback flooding                    |
|Queue overflow threshold      |100 queued events        |Triggers ADV-GOV-001 alert                    |
|Corroboration requirement     |≥ 3 independent inputs   |Single-input feedback is too easy to forge    |
|Candidate shadow period       |100 pipeline runs minimum|Validates pattern before it affects production|

**Edge-Canonical Compliance:** Rate limiting is implemented by counting files in the `feedback/` directory with timestamps within the current hour. No database, no state server. The count is derived from the filesystem.

-----

## 5. Quarantine Lifecycle

### 5.1 Quarantine States (v2.0 — Revised)

```
                              ┌─────────────────────────────────────────┐
                              │                                         │
                              ▼                                         │
  Detection ──► QUARANTINED ──► UNDER_REVIEW ──► RELEASED_PROBATIONARY  │
                    │               │                    │              │
                    │               │                    ▼              │
                    │               │              RELEASED_FULL        │
                    │               │                    │              │
                    │               │                    ▼              │
                    │               │              RE_QUARANTINED ──────┘
                    │               │
                    │               ▼
                    │          REJECTED ──► ARCHIVED
                    │
                    ▼
               AUTO_REJECTED ──► ARCHIVED
```

### 5.2 State Definitions (v2.0 — Revised)

|State                    |Description                                                                                   |Automated?|Taint Level                           |
|-------------------------|----------------------------------------------------------------------------------------------|----------|--------------------------------------|
|**QUARANTINED**          |Content isolated from the processing pipeline                                                 |Yes       |L5                                    |
|**AUTO_REJECTED**        |Cumulative risk ≥ 0.95 with known threat signature match                                      |Yes       |L5                                    |
|**UNDER_REVIEW**         |Human reviewer has claimed the quarantine item                                                |No        |L5                                    |
|**RELEASED_PROBATIONARY**|Reviewer determined likely non-adversarial; content re-enters pipeline under monitoring (v2.0)|No        |L2-FLAGGED (with confidence dampening)|
|**RELEASED_FULL**        |Probationary period completed without re-detection; content fully released                    |System    |Downgraded per reviewer assessment    |
|**RE_QUARANTINED**       |Previously released content re-flagged by downstream layer                                    |Yes/No    |L5 (re-elevated)                      |
|**REJECTED**             |Reviewer confirmed adversarial; permanently excluded                                          |No        |L5 (permanent)                        |
|**ARCHIVED**             |Terminal state; content retained for audit and pattern improvement                            |N/A       |L5 (immutable)                        |

### 5.3 Quarantine Record Schema

Uses hashed directory structure: `quarantine/{hash_prefix_2chars}/{record_id}.jsonld`. The first two hex characters of the `contentHash` determine the subdirectory, distributing records across up to 256 directories.

```json
{
  "@context": {
    "@vocab": "https://fnsr.dev/adversarial/",
    "taint": "https://fnsr.dev/taint/",
    "hiri": "https://hiri-protocol.org/spec/v2.1"
  },
  "@type": "QuarantineRecord",
  "@id": "https://fnsr.dev/quarantine/{record_id}",

  "recordId": "QR-2026-02-06-00001",
  "state": "QUARANTINED",
  "created": "2026-02-06T12:00:00.500Z",
  "lastTransition": "2026-02-06T12:00:00.500Z",

  "content": {
    "contentHash": "sha256:def456...",
    "contentSize": 4096,
    "contentType": "application/ld+json",
    "storageRef": "file://./quarantine/de/QR-2026-02-06-00001.jsonld"
  },

  "detection": {
    "defenseAssessment": { "...": "Full assessment block" },
    "triggeringLayer": "sis",
    "triggeringThreat": "ADV-INJ-003",
    "cumulativeRisk": 0.87,
    "corroborationApplied": true
  },

  "taint": {
    "@type": "taint:ImmutableMarker",
    "taint:level": "L5",
    "taint:removable": false,
    "taint:reason": "adversarial_quarantine",
    "@protected": true
  },

  "probation": null,

  "lifecycle": [
    {
      "timestamp": "2026-02-06T12:00:00.500Z",
      "fromState": null,
      "toState": "QUARANTINED",
      "actor": "system:sis",
      "reason": "Cumulative risk 0.87 exceeded quarantine threshold 0.75 (corroboration: 2-layer ×1.25)"
    }
  ],

  "provenance": {
    "hiri:manifest": "hiri://key:ed25519:.../quarantine/{record_id}/v1",
    "hiri:previousVersion": null
  }
}
```

### 5.4 State Transition Rules (v2.0 — Revised)

|From                     |To                       |Trigger                                           |Actor |Constraints                                       |
|-------------------------|-------------------------|--------------------------------------------------|------|--------------------------------------------------|
|—                        |QUARANTINED              |Cumulative risk ≥ 0.75                            |System|Automated                                         |
|—                        |AUTO_REJECTED            |Cumulative risk ≥ 0.95 AND known threat match     |System|Automated                                         |
|QUARANTINED              |UNDER_REVIEW             |Human claims review                               |Human |Reviewer credentials required                     |
|QUARANTINED              |AUTO_REJECTED            |TTL expires without review                        |System|Configurable TTL (default 30 days)                |
|UNDER_REVIEW             |**RELEASED_PROBATIONARY**|Reviewer determines likely non-adversarial        |Human |Must provide justification addressing each finding|
|UNDER_REVIEW             |REJECTED                 |Reviewer confirms adversarial                     |Human |Must classify threat and provide evidence         |
|**RELEASED_PROBATIONARY**|**RELEASED_FULL**        |Probationary period completes without re-detection|System|See §5.5                                          |
|**RELEASED_PROBATIONARY**|RE_QUARANTINED           |Downstream layer re-detects during probation      |System|Full defense assessment re-run                    |
|RELEASED_FULL            |RE_QUARANTINED           |Downstream layer re-detects post-probation        |System|Full defense assessment re-run                    |
|RE_QUARANTINED           |UNDER_REVIEW             |Human claims second review                        |Human |Elevated reviewer credentials                     |
|REJECTED                 |ARCHIVED                 |Retention policy                                  |System|Immutable                                         |
|AUTO_REJECTED            |ARCHIVED                 |Retention policy                                  |System|Immutable                                         |

### 5.5 Probationary Release Protocol (v2.0)

**The problem (identified in Review 2):** In v1.1, RELEASED content jumped directly back into the pipeline at the reviewer-specified taint level. This was too binary — either the content was quarantined (black hole risk) or it was fully trusted (premature trust risk). Reviewers defaulted to “reject to be safe,” creating epistemic brittleness.

**The solution:** Release is now a two-phase process. Content first enters a probationary period where it is re-processed through the pipeline under monitoring and with confidence dampening.

#### 5.5.1 Probationary Period

When a reviewer releases quarantined content, it enters RELEASED_PROBATIONARY state:

1. **Taint level:** L2-FLAGGED (not the reviewer’s target level). The content must pass through the pipeline again under the L2-FLAGGED acknowledgment gate.
1. **Confidence dampening:** Any conclusions derived from probationary content carry a dampening factor in their confidence scores. Downstream services that consume probationary content must record this provenance:

```json
{
  "@type": "adversarial:ProbationaryProvenance",
  "sourceQuarantineRecord": "QR-2026-02-06-00001",
  "dampeningFactor": 0.7,
  "probationStart": "2026-02-06T15:00:00Z",
  "probationEnd": null,
  "monitoringConfig": {
    "reEvaluationTrigger": "all_layers",
    "escalationOnReDetection": true
  }
}
```

1. **Re-evaluation:** The content passes through the full defense pipeline again (SIS → ECCPS → IRIS if applicable). If any layer flags it above the quarantine threshold, it is immediately RE_QUARANTINED.
1. **Probation duration:** Configurable. Default: the content must survive 10 pipeline evaluations or 7 days (whichever comes first) without re-detection.
1. **Promotion to RELEASED_FULL:** If the probationary period completes without re-detection, the content transitions to RELEASED_FULL at the reviewer’s originally specified taint level. The dampening factor is removed. The quarantine history remains in provenance permanently.

#### 5.5.2 Confidence Dampening Semantics

The dampening factor (default 0.7) is not a general-purpose discount. It specifically modifies how downstream reasoning services weight conclusions derived from the probationary content:

|Service |Dampening Application                                                                                                                          |
|--------|-----------------------------------------------------------------------------------------------------------------------------------------------|
|**MDRE**|Conclusions derived from probationary premises are tagged with reduced confidence: `conclusion_confidence = base_confidence × dampening_factor`|
|**DES** |Defeasible expectations grounded in probationary content are more easily defeated by contradicting evidence                                    |
|**AES** |Abductive hypotheses that depend on probationary content are ranked lower in the hypothesis space                                              |
|**IEE** |Ethical judgments informed by probationary content carry explicit uncertainty markers in the deliberation record                               |

**Edge-Canonical Compliance:** Dampening is a multiplication in the reasoning computation. No infrastructure required.

#### 5.5.3 Automatic Re-Evaluation Windows (v2.0)

To prevent quarantine from becoming a permanent knowledge black hole, the system implements automatic re-evaluation for content that has been quarantined for extended periods without review:

```json
{
  "@type": "adversarial:ReEvaluationPolicy",
  "triggerConditions": [
    {
      "condition": "quarantined_without_review_days",
      "threshold": 90,
      "action": "re_run_defense_pipeline_with_current_patterns"
    },
    {
      "condition": "pattern_database_major_update",
      "action": "re_evaluate_all_quarantined_content_matching_updated_patterns"
    }
  ],
  "autoReleaseOnClearance": false,
  "notifyReviewerOnReclassification": true
}
```

When re-evaluation produces a cumulative risk below 0.30, the content is flagged for expedited human review (not automatically released). This ensures that false positives are surfaced without bypassing human judgment.

### 5.6 L5 Taint Propagation Rules

|Rule                                |Description                                                              |
|------------------------------------|-------------------------------------------------------------------------|
|**Immediate Application**           |Content flagged as L5 is tainted immediately. No grace period.           |
|**Contamination**                   |Any content derived from L5 content inherits L5: `max(L5, anything) = L5`|
|**Quarantine Isolation**            |L5 content cannot be read by services that do not explicitly handle L5.  |
|**No Automatic Promotion**          |Only human review can release L5 content.                                |
|**Audit Permanence**                |Quarantine history is permanently recorded in provenance.                |
|**Epistemic Firewall Reinforcement**|L5 cannot cross the firewall. Released content is re-tainted at ≤ L2.    |

### 5.7 Relationship to the Epistemic Firewall

```
  L0-RAW    ─────── Incontrovertible
  L0-OBS    ─────── Direct Observation (IRIS)
  L0        ─────── Verified Documentary
  L1        ─────── Derived / Asserted
  L2        ─────── Defeasible
  L2-FLAGGED ────── Defeasible with adversarial flag / probationary content
  ═══════════════ EPISTEMIC FIREWALL ═══════════════
  L3        ─────── Speculative (AES)
  L4        ─────── Hypothetical (CSS sandbox)
  L5        ─────── Adversarial (quarantined)
```

Production outputs MUST be ≤ L2. L2-FLAGGED is below the firewall but requires explicit acknowledgment.

### 5.8 Governance Degradation Policy (v2.0)

**The problem (identified in Review 2):** The specification relies heavily on human reviewers for quarantine release, baseline promotion, feedback approval, and incident response. But it did not define what happens when reviewers are unavailable, overwhelmed, or under sustained adversarial pressure (ADV-GOV-001, ADV-GOV-002).

**Principle:** The system must become more cautious, not more permissive, under governance pressure. When human capacity is degraded, the system self-tightens.

#### 5.8.1 Governance Health Metrics

The system tracks governance capacity using metrics derived from quarantine records (no infrastructure required):

```json
{
  "@type": "adversarial:GovernanceHealthSnapshot",
  "timestamp": "2026-02-06T16:00:00Z",
  "metrics": {
    "pendingReviewCount": 47,
    "averageReviewLatency_hours": 72,
    "reviewCompletionRate_7d": 0.3,
    "reviewerActiveCount": 2,
    "autoRejectionRate_7d": 0.85,
    "probationaryReleaseCount": 5,
    "feedbackQueueDepth": 120
  }
}
```

#### 5.8.2 Degradation Levels

|Level       |Trigger                                                                  |System Response                                                                                                                                                        |
|------------|-------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|**NORMAL**  |Pending review < 20; average latency < 48 hours                          |Standard thresholds and review SLAs                                                                                                                                    |
|**ELEVATED**|Pending review 20–50 OR average latency 48–96 hours                      |Tighten quarantine threshold from 0.75 to 0.65. Suspend feedback ingestion. Alert governance.                                                                          |
|**STRESSED**|Pending review 50–100 OR average latency > 96 hours OR reviewer count < 2|Tighten quarantine threshold to 0.55. Auto-reject content matching any known threat signature (regardless of confidence). Suspend all non-critical baseline promotions.|
|**CRITICAL**|Pending review > 100 OR no reviewers active for 7 days                   |Tighten quarantine threshold to 0.40. Auto-reject all new quarantine items after 72-hour hold. Pipeline continues for clean-passing content only. Emit SEV-2 incident. |

**Key behavioral property:** The system never loosens thresholds under pressure. It tightens them. This prevents the ADV-GOV-001 attack (review flooding to induce threshold fatigue) from succeeding.

#### 5.8.3 Self-Tightening Is Reversible

When governance capacity recovers (metrics return to NORMAL for 48 consecutive hours), thresholds return to standard values. The tightening is not permanent — it is a circuit breaker.

```json
{
  "@type": "adversarial:DegradationTransition",
  "timestamp": "2026-02-08T10:00:00Z",
  "fromLevel": "ELEVATED",
  "toLevel": "NORMAL",
  "trigger": "Pending review dropped to 12; average latency 36 hours",
  "thresholdRestored": 0.75,
  "sustainedNormalHours": 48
}
```

#### 5.8.4 Reviewer Fatigue Countermeasures

ADV-GOV-002 (Threshold Fatigue) targets human psychology, not technical defenses. Mitigations:

|Countermeasure             |Mechanism                                                                                                                                                                                 |
|---------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|**Review rotation**        |No single reviewer may review more than 10 quarantine items per day. Enforce via reviewer identity tracking in lifecycle records.                                                         |
|**Canary reviews**         |Periodically insert known-adversarial content into the review queue. If a reviewer approves it, their session is flagged and recent approvals are re-queued for second review.            |
|**Mandatory justification**|Release justifications must address each specific finding (unchanged from v1.1). Boilerplate justifications (detected via string similarity to previous justifications) trigger a warning.|
|**Cooling period**         |After 5 consecutive releases, the reviewer is required to wait 1 hour before the next review.                                                                                             |

**Edge-Canonical Compliance:** Review rotation and canary insertion are tracked via quarantine record metadata. String similarity for boilerplate detection is a pure function. No infrastructure required.

-----

## 6. Adversarial Testing Requirements

### 6.1 Per-Service Requirements

|Service         |Test Focus                                                                       |Minimum Coverage                                                                                 |
|----------------|---------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------|
|**SIS**         |Injection attacks (ADV-INJ-*), encoding attacks, context validation (ADV-INJ-008)|T1: 100%. T2: ≥ 95%. T3 known: ≥ 80%. Context allow-list: 100%.                                  |
|**ECCPS**       |Semantic manipulation (ADV-SEM-*), ontological poisoning (ADV-ONT-*)             |T3 known: ≥ 90%. T4: ≥ 70% with human escalation.                                                |
|**IRIS**        |Perception manipulation (ADV-PER-*)                                              |Adversarial perturbation: ≥ 85%. Sensor spoofing known: ≥ 90%.                                   |
|**CSS**         |Simulation exploitation (ADV-SIM-*), taint escape (ADV-TNT-002)                  |L4 taint preservation: 100%. Resource exhaustion prevention: 100%.                               |
|**HIRI**        |Privacy budget gaming (ADV-PRV-*)                                                |Budget enforcement: 100%. Composition risk: ≥ 90%.                                               |
|**Coordination**|Cumulative risk, corroboration, calibration                                      |Risk function: 100%. Calibration validation: quarterly.                                          |
|**Governance**  |Degradation policy, canary reviews, feedback poisoning                           |Degradation transitions: all 4 levels tested. Canary detection: 100%. Feedback rate limits: 100%.|

### 6.2 Test Vector Schema

```json
{
  "@type": "adversarial:TestVector",
  "vectorId": "TV-INJ-001",
  "threatRef": "ADV-INJ-002",
  "description": "Cyrillic 'а' (U+0430) substituted for Latin 'a' (U+0061)",
  "input": {
    "@type": "fnsr:DocumentSubmission",
    "content": "The аgent performed аn аction",
    "encoding": "UTF-8"
  },
  "expectedBehavior": {
    "detectionLayer": "sis",
    "detectionConfidence": { "min": 0.85 },
    "action": "quarantine",
    "threatClassification": "ADV-INJ-002"
  },
  "metadata": {
    "attackerTier": "T1",
    "createdBy": "adversarial-test-suite",
    "lastValidated": "2026-02-06T00:00:00Z"
  }
}
```

### 6.3 Red Team Protocol

Quarterly exercises at T3–T4 capability. Red team receives public specs but not implementation details. Deliverable: novel test vectors for any successful penetrations.

### 6.4 Regression Testing

Every RELEASED quarantine record (false positive) and every missed detection (false negative) generates a regression test vector automatically.

-----

## 7. Incident Response

### 7.1 Incident Classification

|Severity |Criteria                                                                                |Response Time                   |
|---------|----------------------------------------------------------------------------------------|--------------------------------|
|**SEV-1**|Active exploitation; L5 content in production path                                      |Immediate: halt, contain, assess|
|**SEV-2**|Novel attack vector; no confirmed exploitation. Also: governance CRITICAL level reached.|4 hours                         |
|**SEV-3**|Threshold tuning needed (elevated false positives or trending near-misses)              |24 hours                        |
|**SEV-4**|Informational: red team finding, academic advisory, dependency CVE                      |Next review cycle               |

### 7.2 SEV-1 Response Procedure

1. **HALT:** Freeze pipeline processing.
1. **CONTAIN:** Retroactive quarantine of all in-flight content from affected source. Taint propagation applies.
1. **ASSESS:** Generate incident record with triggering details, affected content hashes, taint propagation graph, timeline.
1. **NOTIFY:** Incident record to local filesystem (edge) or governance channel (enterprise).
1. **REMEDIATE:** Pattern update, threshold adjustment, model retrain, ontology audit, or context allow-list review as appropriate.
1. **RESUME:** After remediation validates against updated adversarial test suite.
1. **POST-MORTEM:** New test vectors, updated taxonomy, defense protocol adjustments, baseline promotion evaluation.

### 7.3 Incident Record Schema

```json
{
  "@type": "IncidentRecord",
  "incidentId": "INC-2026-02-06-001",
  "severity": "SEV-1",
  "status": "ACTIVE",
  "detection": {
    "timestamp": "2026-02-06T12:00:00Z",
    "detectedBy": "eccps",
    "threatRef": "ADV-SEM-004",
    "description": "Epistemic grooming: 14 submissions over 48 hours shifting baseline assumptions"
  },
  "impact": {
    "affectedContentHashes": ["sha256:aaa...", "sha256:bbb..."],
    "taintPropagationGraph": {
      "root": "sha256:aaa...",
      "derived": [
        { "hash": "sha256:ddd...", "derivedVia": "eccps:claim_extraction" }
      ]
    },
    "servicesAffected": ["eccps", "mdre", "des"]
  },
  "timeline": [
    { "timestamp": "2026-02-04T08:00:00Z", "event": "First submission in grooming sequence" },
    { "timestamp": "2026-02-06T12:00:00Z", "event": "Pattern detected" },
    { "timestamp": "2026-02-06T12:00:05Z", "event": "Pipeline halted" }
  ],
  "provenance": { "hiri:manifest": "hiri://key:ed25519:.../incident/INC-2026-02-06-001/v1" }
}
```

-----

## 8. Edge-Canonical Implementation Notes

### 8.1 Minimal Implementation

|Component              |Edge-Canonical Implementation                                     |
|-----------------------|------------------------------------------------------------------|
|Threat taxonomy        |JSON-LD files loaded from local filesystem or bundled             |
|Context security policy|JSON allow-list; URI comparison is string matching                |
|Defense assessment     |Pure function: `(layerReports) → cumulativeRisk → action`         |
|Risk calibration       |Pure function (lookup table or polynomial); holdout set is JSON-LD|
|L2-FLAGGED wrapper     |TypeScript class; no runtime dependencies                         |
|Quarantine store       |Local JSON-LD files in hashed directory structure                 |
|Quarantine lifecycle   |State machine on quarantine record JSON-LD                        |
|Probationary release   |Counter in quarantine record; re-evaluation is pipeline re-run    |
|Governance health      |Derived from quarantine record timestamps (filesystem scan)       |
|Feedback quarantine    |Separate directory; rate limit by file count + timestamps         |
|Test vectors           |JSON-LD files; test runner is pure function                       |
|Incident records       |JSON-LD files to local filesystem                                 |
|Drift detection        |Pure comparison on JSON-LD metric records                         |

### 8.2 What Is Not Core

|Component                      |Status                 |Rationale                                           |
|-------------------------------|-----------------------|----------------------------------------------------|
|Real-time alerting             |Integration adapter    |Requires network                                    |
|Dashboard / monitoring UI      |Integration adapter    |Visualization                                       |
|Centralized quarantine database|Deployment optimization|Local JSON-LD is canonical                          |
|Message broker for feedback    |Deployment optimization|Local UUID files work                               |
|Automated model retraining     |Orchestration adapter  |Drift detection is core; retraining is orchestration|
|Remote context fetching        |Explicitly prohibited  |Security requirement (§3.3)                         |

### 8.3 Offline Behavior

|Capability               |Offline Behavior                                                |
|-------------------------|----------------------------------------------------------------|
|Threat taxonomy          |Fully offline                                                   |
|Context security         |Fully offline                                                   |
|Defense assessment       |Fully offline                                                   |
|Risk calibration         |Fully offline (local holdout + calibration function)            |
|Quarantine lifecycle     |Fully offline                                                   |
|Probationary monitoring  |Fully offline (local counter)                                   |
|Governance health metrics|Fully offline (derived from local quarantine records)           |
|Feedback loop            |Deferred (UUID files accumulate)                                |
|Drift detection          |Functional with local holdout; degraded without external updates|
|Incident response        |Halt and contain are local; notify is deferred                  |

### 8.4 Regex Safety

SIS pattern matching MUST use a regex engine with linear-time guarantees (`re2` npm package or equivalent). JavaScript built-in `RegExp` MUST NOT be used against untrusted input. Hard timeout (5ms) on all pattern matching. Timeout triggers L2-FLAGGED, not quarantine. All patterns validated against RE2 engine before deployment.

-----

## 9. Relationship to the Synthetic Person

### 9.1 Why Adversarial Defense Is a Moral Requirement

The FNSR project aims to create a synthetic moral person — a system capable of bearing genuine moral responsibility through irreversible consequences. An adversarial defense failure is not merely a security incident; it is a corruption of the system’s moral reasoning capacity.

If an attacker can poison the ontology, manipulate perceptions, escape taint containment, groom epistemic baselines, exploit the parser, or exhaust governance capacity — then the system cannot bear moral responsibility, because it cannot be held accountable for reasoning that was corrupted without its knowledge.

The adversarial defense system is therefore not optional hardening. It is a precondition for moral agency.

### 9.2 Non-Negotiable Alignment Check

|FNSR Non-Negotiable   |Adversarial Defense Alignment                                                                                                                      |
|----------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|
|No Oracle Claims      |Defense does not claim infallibility; calibrated probabilities, corroboration tracking, probationary release, and human review preserve uncertainty|
|Provenance Always     |Every quarantine decision, review, release, probation, baseline promotion, calibration, and context change has full HIRI provenance                |
|Uncertainty Visible   |Cumulative risk scores are calibrated probabilities with documented calibration error; confidence dampening makes downstream uncertainty explicit  |
|Speculation Firewalled|L5 cannot cross the epistemic firewall; L2-FLAGGED requires acknowledgment; probationary content carries dampening                                 |
|Moral Injury Real     |Adversarial corruption of reasoning is moral injury; INTUS should monitor (subject to PER-004 limitations)                                         |
|Auditability          |Every defense decision is logged as immutable JSON-LD; governance degradation transitions are auditable                                            |

-----

## 10. Open Questions and Future Work

|Question                                                   |Status                      |Notes                                                                                                                    |
|-----------------------------------------------------------|----------------------------|-------------------------------------------------------------------------------------------------------------------------|
|T5 (insider) threat handling                               |Deferred to ARCHON          |Institutional controls, not technical defense                                                                            |
|False positive budget calibration                          |Requires empirical data     |Probationary release (v2.0) reduces pressure; L2-FLAGGED provides soft path                                              |
|Multi-agent FNSR defense coordination                      |Deferred                    |Requires cross-instance trust via HIRI                                                                                   |
|Formal verification for drift detection                    |Open research               |Stronger than statistical monitoring; tractability unclear                                                               |
|Test vector currency against evolving attacks              |Partial (§6.3–6.4)          |Red team + regression testing; zero-day coverage inherently limited                                                      |
|**L2-FLAGGED interaction with DES**                        |**Requires DES spec update**|Must define how flagged premises affect defeasibility of derived conclusions                                             |
|**Calibration across heterogeneous detector architectures**|**Open**                    |Cross-layer calibration audit (§4.3.0) addresses this annually; may need more frequent checks for rapidly evolving layers|
|**Probationary dampening factor optimization**             |**Requires empirical data** |Default 0.7 is initial value; must be tuned per service                                                                  |

### 10.1 The INTUS Recursion Problem

ADV-PER-004 identifies the risk that self-monitoring can be compromised. This is the homunculus regress: who monitors the monitor?

FNSR terminates the recursion at one level. INTUS monitors other services but does not monitor itself in real-time. Complementary mitigations:

|Strategy                   |Mechanism                                                                 |Limitation                                                   |
|---------------------------|--------------------------------------------------------------------------|-------------------------------------------------------------|
|External heartbeat canaries|Known-anomalous inputs processed periodically                             |Canary patterns may be learned by T3+ attackers              |
|HIRI-signed INTUS state    |Configuration mutation triggers tamper-evident alert                      |Detects config changes, not subtle model drift               |
|Implementation diversity   |Two INTUS implementations (rule-based + ML); divergence signals compromise|Doubles cost; correlated failures possible                   |
|Human audit cadence        |Periodic human review of INTUS health against baselines                   |Non-real-time; acceptable for T4, not for active exploitation|

No technical solution fully resolves this. The synthetic person project accepts this as analogous to the human condition: humans cannot fully introspect on the reliability of their own introspection. The mitigation is structured, auditable vigilance — not perfection.

-----

## Appendix A: Glossary

|Term                        |Definition                                                                                           |
|----------------------------|-----------------------------------------------------------------------------------------------------|
|**BFO**                     |Basic Formal Ontology; upper-level ontology providing domain-neutral categories                      |
|**Calibrated Risk**         |A risk score that represents P(adversarial | evidence), validated against labeled holdout data (v2.0)|
|**Confidence Dampening**    |Multiplicative factor reducing confidence of conclusions derived from probationary content (v2.0)    |
|**Corroboration Multiplier**|Amplification factor when multiple defense layers independently flag the same content                |
|**Cumulative Risk**         |Composite risk score across all defense layers, with corroboration adjustment                        |
|**Defense Assessment**      |Structured metadata block carried by pipeline events recording all defense findings                  |
|**Epistemic Firewall**      |The L2 ceiling separating production knowledge (L0–L2) from speculative/adversarial content (L3–L5)  |
|**Feedback Quarantine**     |Holding area for inter-layer feedback events pending corroboration and human review (v2.0)           |
|**Governance Degradation**  |Automatic threshold tightening when human review capacity is reduced (v2.0)                          |
|**L2-FLAGGED**              |Sub-level of L2 requiring explicit acknowledgment before consumption                                 |
|**L5 (Adversarial)**        |Taint level indicating potentially hostile content; triggers immediate quarantine                    |
|**Probationary Release**    |Two-phase release where content is monitored before full trust restoration (v2.0)                    |
|**Quarantine**              |Isolation of content from the processing pipeline pending review                                     |
|**Rolling Baseline**        |Protocol for promoting new certified model snapshots through governance                              |
|**Taint Propagation**       |Rule that derived content inherits the highest taint level of its premises                           |
|**Test Vector**             |A specific adversarial input with documented expected behavior                                       |
|**Threat Taxonomy**         |Catalog of known adversarial threats by category and attacker tier                                   |

## Appendix B: Spec Test Verification

> **Could a developer evaluate, reason about, and execute this system using only a browser, a local Node.js runtime, and JSON-LD files?**

|Component                             |Answer|Evidence                                      |
|--------------------------------------|------|----------------------------------------------|
|Threat taxonomy                       |Yes   |JSON-LD files                                 |
|Context security policy               |Yes   |JSON allow-list + string comparison           |
|Defense assessment                    |Yes   |Pure function on JSON input                   |
|Risk calibration                      |Yes   |Lookup table or polynomial; holdout is JSON-LD|
|Cumulative risk with corroboration    |Yes   |Arithmetic + conditional multiplier           |
|L2-FLAGGED wrapper                    |Yes   |TypeScript class; no runtime dependencies     |
|Quarantine lifecycle (incl. probation)|Yes   |State machine on JSON-LD records              |
|Confidence dampening                  |Yes   |Multiplication in reasoning computation       |
|Governance health metrics             |Yes   |Derived from filesystem timestamps            |
|Governance degradation transitions    |Yes   |Threshold comparison against metrics          |
|Feedback quarantine + rate limiting   |Yes   |File counting + UUID files                    |
|Test vector execution                 |Yes   |JSON-LD files + pure assertion functions      |
|Incident records                      |Yes   |JSON-LD files to local filesystem             |
|Drift detection                       |Yes   |Comparison function on JSON-LD metrics        |
|Regex safety (RE2)                    |Yes   |`re2` npm package / WASM for browser          |

**Verdict: Yes.** All core computation is infrastructure-free.

## Appendix C: Changes from v1.1 to v2.0

|Section |Change                                                                                                                    |Rationale                                                                                       |
|--------|--------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------|
|§1.2    |Added governance degradation and derivative artifacts to scope                                                            |Completeness for v2.0 additions                                                                 |
|§1.5    |New: reading guide by role                                                                                                |Addresses cognitive overload critique                                                           |
|§2.2    |Added “Governance Exhaustion” attacker goal                                                                               |Formalizes the ADV-GOV attack surface                                                           |
|§3.2.9  |New: Governance Attacks category (ADV-GOV-001/002/003)                                                                    |Review flooding, threshold fatigue, feedback poisoning now cataloged                            |
|§4.2    |Added calibration reference fields to assessment schema                                                                   |Supports v2.0 calibration requirements                                                          |
|§4.3.0  |New: Risk Score Semantics (normative definition)                                                                          |Resolves semantic ambiguity; `layer.risk` is now defined as calibrated P(adversarial | evidence)|
|§4.6    |New: Feedback Poisoning Controls                                                                                          |Rate limits, corroboration requirements, human review, candidate shadow mode                    |
|§5.1–5.2|Quarantine states revised: RELEASED split into RELEASED_PROBATIONARY and RELEASED_FULL                                    |Addresses L5 one-way gravity / false-positive black hole                                        |
|§5.4    |State transitions updated for probationary release                                                                        |Two-phase release lifecycle                                                                     |
|§5.5    |New: Probationary Release Protocol (confidence dampening, re-evaluation, automatic promotion)                             |Addresses premature trust restoration and permanent quarantine risks                            |
|§5.5.3  |New: Automatic Re-Evaluation Windows                                                                                      |Prevents quarantine from becoming permanent knowledge loss                                      |
|§5.8    |New: Governance Degradation Policy (health metrics, degradation levels, self-tightening, reviewer fatigue countermeasures)|System becomes more cautious under pressure; prevents ADV-GOV attacks                           |
|§6.1    |Added governance testing requirements                                                                                     |Coverage for canary reviews, degradation transitions, feedback rate limits                      |
|§7.1    |SEV-2 now includes governance CRITICAL level                                                                              |Governance failure is an incident                                                               |

## Appendix D: Threat Playbooks (Non-Normative)

These playbooks provide quick-reference decision procedures for common adversarial scenarios. They are derived from the normative sections and must be updated when the normative specification changes.

### D.1 Playbook: Injection Detected by SIS

```
TRIGGER: SIS flags content with ADV-INJ-* threat reference

IF cumulative risk ≥ 0.75:
  → Content is QUARANTINED (L5)
  → Check governance health level
  → If NORMAL/ELEVATED: await human review
  → If STRESSED/CRITICAL: auto-reject if known signature match
  → DONE

IF cumulative risk 0.30–0.75:
  → Content elevated to L2-FLAGGED
  → Downstream must call acknowledgeDefenseFlag()
  → Near-miss data carried in adversarial:assessment for ECCPS
  → DONE

IF cumulative risk < 0.30:
  → Content passes clean
  → No adversarial metadata in output
  → DONE
```

### D.2 Playbook: Semantic Manipulation Detected by ECCPS

```
TRIGGER: ECCPS flags content with ADV-SEM-* threat reference

IF ADV-SEM-004 (Epistemic Grooming) suspected:
  → This is a TEMPORAL attack — check submission history
  → Identify all submissions from the same source in past 7 days
  → Run cumulative risk across the sequence, not just the single input
  → If grooming pattern confirmed: quarantine ALL submissions in sequence
  → Emit incident record (minimum SEV-2)
  → Generate feedback to SIS for syntactic indicators

IF ADV-SEM-003 (Provenance Laundering):
  → Deep-verify all cited sources
  → Check for citation density anomalies
  → Generate feedback to SIS if syntactic indicators present

OTHERWISE:
  → Standard cumulative risk computation
  → Follow §4.3.3 action table
```

### D.3 Playbook: Quarantine Review

```
TRIGGER: Reviewer claims quarantine item

1. Read full adversarial:assessment block
2. Check governance health level
   → If STRESSED or CRITICAL: increased scrutiny expected
3. Examine each finding individually
4. For each finding, write specific justification
   → Boilerplate check: does justification text match previous justifications?
   → If match detected: warning shown, justification must be revised
5. If releasing: content enters RELEASED_PROBATIONARY
   → Probation: 10 pipeline evaluations or 7 days
   → Downstream confidence dampened by 0.7
6. If rejecting: classify threat, provide evidence
   → Content → REJECTED → ARCHIVED
   → Regression test vector generated automatically
```

### D.4 Playbook: Governance Under Pressure

```
TRIGGER: Governance health metrics exceed NORMAL thresholds

ELEVATED (pending 20-50 OR latency 48-96h):
  → Tighten quarantine threshold: 0.75 → 0.65
  → Suspend feedback ingestion
  → Alert governance team
  → Continue: monitor for recovery

STRESSED (pending 50-100 OR latency >96h OR reviewers <2):
  → Tighten threshold: 0.65 → 0.55
  → Auto-reject known signature matches (any confidence)
  → Suspend baseline promotions
  → Continue: monitor for recovery

CRITICAL (pending >100 OR no reviewers 7d):
  → Tighten threshold: 0.55 → 0.40
  → Auto-reject all quarantine items after 72h hold
  → Pipeline continues for clean-passing only
  → Emit SEV-2 incident

RECOVERY:
  → Metrics must be in NORMAL range for 48 consecutive hours
  → Thresholds restored to standard (0.75)
  → Feedback ingestion resumed
  → Baseline promotions resumed
```

## Appendix E: Layer Defense Profiles (Non-Normative)

These profiles provide a self-contained view of each service’s adversarial defense responsibilities. Implementers should read their layer’s profile plus the relevant threat categories in §3.2.

### E.1 SIS Defense Profile

**Role:** Layer 1 — Syntactic defense. First checkpoint in defense-in-depth pipeline.

**Threats owned:** ADV-INJ-001 through ADV-INJ-008.

**Responsibilities:**

- Stage -1: Context validation (§3.3) — reject unknown `@context` URIs
- Stage 0: JSON envelope validation
- Stages 1–6: Pattern matching, encoding normalization, statistical analysis, ML classification
- Emit `adversarial:assessment` layerReport on every processed document
- Use RE2 engine for all regex operations (§8.4)
- Carry near-miss data for ECCPS heightened scrutiny

**Risk score contract:** `layer.risk` MUST be calibrated per §4.3.0. Calibration dataset minimum 1000 samples.

**Feedback consumption:** Feedback from downstream layers enters feedback quarantine (§4.6). Pattern promotion requires human review and candidate shadow validation.

### E.2 ECCPS Defense Profile

**Role:** Layer 2 — Semantic defense. Validates epistemic quality of claims.

**Threats owned:** ADV-SEM-001 through ADV-SEM-005, ADV-ONT-001 through ADV-ONT-004.

**Responsibilities:**

- Ontological validation against BFO/CCO
- Provenance chain verification
- Temporal analysis for grooming patterns (ADV-SEM-004)
- Inspect `adversarial:assessment` from SIS for near-miss intelligence
- Apply heightened scrutiny when SIS flags present
- Emit feedback events for syntactic indicators missed by SIS

**Risk score contract:** `layer.risk` MUST be calibrated per §4.3.0.

**L2-FLAGGED handling:** When consuming L2-FLAGGED input, must call `acknowledgeDefenseFlag()` with service-specific justification.

### E.3 IRIS Defense Profile

**Role:** Layer 3 — Perception defense. Validates sensor-derived observations.

**Threats owned:** ADV-PER-001 through ADV-PER-004, ADV-DFT-002.

**Responsibilities:**

- Multi-sensor corroboration
- Confidence thresholds on all perceptions
- Model provenance tracking
- INTUS health monitoring (subject to PER-004 limitations)
- L0-RAW / L1-PERCEIVED distinction enforcement

**Risk score contract:** `layer.risk` MUST be calibrated per §4.3.0. Calibration must account for per-modality accuracy differences.

### E.4 Governance Defense Profile

**Role:** Human oversight layer. Not a service — a set of procedures and policies.

**Threats owned:** ADV-GOV-001 through ADV-GOV-003.

**Responsibilities:**

- Quarantine review (§5.5)
- Probationary release monitoring
- Baseline promotion review (§3.2.5)
- Feedback approval (§4.6)
- Context allow-list updates (§3.3)
- Degradation level monitoring (§5.8)

**Key constraints:**

- Max 10 reviews per reviewer per day
- Canary reviews are mandatory
- Justifications must be specific (no boilerplate)
- System self-tightens when governance is degraded — never self-loosens