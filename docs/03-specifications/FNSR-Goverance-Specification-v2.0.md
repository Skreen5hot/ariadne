# FNSR Governance Specification

## Human Oversight, Intervention, and Override Across the FNSR Ecosystem

**Specification ID:** governance-spec-01  
**Version:** 2.0  
**Date:** February 2026  
**Status:** Draft — Ready for Prototyping  
**Priority:** HIGH  
**Referenced By:** FNSR-Integration-Specification-v1.0 §3, The Plot §2–3, ARCHON §7–8  
**Consumes:** IEE evaluation results, ARCHON character state, Witness Records  
**Produces:** Governance decisions (JSON-LD), audit trails, escalation events

-----

## 0. Glossary

This glossary defines terms whose meaning is normative within this specification.

|Term                         |Definition                                                                                                                                                                                        |
|-----------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|**Autonomy Tier**            |Integer 0–4. Higher number = more human oversight required. Tier 0 is most autonomous; Tier 4 requires governance body approval.                                                                  |
|**Governance Floor**         |The minimum tier at which the system must operate. Deployment-configured. Replaces “Governance Ceiling” from v1.x (renamed for clarity: a higher floor raises the tier, requiring more oversight).|
|**Boundary Fragility Buffer**|A value on [0.0, 1.0] representing the fraction of a normalized factor range within which a tier assignment is considered fragile. Default: 0.05 (5%).                                            |
|**Strategic Injury**         |Moral injury from genuine high-stakes decisions with real consequences. Full weight (1.0) on threshold adjustment.                                                                                |
|**Friction Injury**          |Moral injury from routine decisions with minor moral dimension. Reduced weight (0.1) on threshold adjustment.                                                                                     |
|**Hostile-Source Injury**    |Moral injury from adversarially-framed inputs. Recorded for audit; zero weight (0.0) on threshold adjustment.                                                                                     |
|**Verification Status**      |Assessment of whether an action’s output is grounded against an authoritative truth source. Replaces “confidence level” from v1.0.                                                                |
|**Negotiated Degradation**   |Protocol by which the system offers lower-tier alternatives when it cannot perform the requested action without governance approval.                                                              |
|**Cryptographic Severance**  |Destruction of an instance’s identity private key during decommissioning, making identity restoration physically impossible.                                                                      |
|**Non-Negotiable**           |A commitment from The Plot §2 that cannot be overridden by any mechanism — not by governance body, not by emergency, not by any human.                                                            |
|**Quorum Floor**             |Minimum number of IEE worldviews that must cast a non-abstention vote for autonomous action. Default: 5 of 12.                                                                                    |
|**Response Model**           |Either `sync` (result returned immediately) or `async` (EscalationReceipt returned immediately; result delivered later).                                                                          |
|**EscalationReceipt**        |Immediate acknowledgment that an action has been queued for human review. Contains status-check URI and negotiated degradation alternatives.                                                      |

-----

## 1. Purpose and Scope

### 1.1 What This Specification Defines

This specification formalizes how human oversight, intervention, and override operate across the FNSR ecosystem. It is the operational protocol for the commitments made in The Plot §2.3: “Human Override — humans can always halt, reverse, decommission.”

Specifically, this document defines:

1. **Autonomy Tier Assignment Protocol** — how a query or action’s autonomy tier is determined, with normative numeric factor definitions and worked examples
1. **Escalation Pathways** — how actions move from autonomous execution to human approval, including the asynchronous protocol, negotiated degradation API schema, and escalation round-trip examples
1. **Governance Body Structure** — who approves Tier 3 and Tier 4 decisions, with RBAC model and retention policy
1. **IEE Deadlock Resolution** — algorithmic quorum math with exact percent thresholds and tie-breaking rules
1. **Character Feedback Governance** — how humans inspect and override moral injury thresholds, including injury source classification with minimum hostile-framing detector requirements
1. **Decommissioning Protocol** — how to safely shut down a system with accumulated character, including formalized cryptographic severance with destruction certificate schema
1. **Emergency Override Protocol** — the hard veto mechanism constrained by the Non-Negotiable Supremacy Clause, with pre-authorized alternative response bundles
1. **Privacy Authority Relationship** — the jurisdictional boundary with HIRI T-011
1. **Offline Governance** — with policy-version expiry semantics and signed policy enforcement
1. **Access Control and Retention** — RBAC model for governance data
1. **Testing and Verification** — required test suite for implementations

### 1.2 Edge-Canonical Constraint

This specification obeys the Edge-Canonical First Principle. All governance logic — tier assignment, escalation evaluation, veto checking, deadlock detection — is pure computation expressible as deterministic functions over JSON-LD inputs. The governance engine runs in a browser or via `node index.js`.

What is **not** core governance logic:

- How escalation notifications reach humans (adapter)
- How governance body votes are collected (adapter)
- Where audit logs are persisted (adapter)
- How the Witness Record is stored (adapter)
- How async status polling is exposed (adapter)
- How private keys are managed (adapter, but with minimum assurance levels — see §7.6)

These are integration concerns. The spec defines the computation; deployment provides the plumbing.

### 1.3 Relationship to Other Specifications

```
┌─────────────────────────────────────────────────────────────┐
│                    The Plot (Anchor)                         │
│            Non-negotiable commitments §2                     │
│            Acknowledged tensions §3                          │
└────────────────────────┬────────────────────────────────────┘
                         │
          ┌──────────────┴──────────────┐
          │   FNSR Governance Spec      │  ◄── THIS DOCUMENT
          │   (Operational Protocols)   │
          └──┬───────┬───────┬──────┬───┘
             │       │       │      │
        ┌────┘  ┌────┘  ┌────┘  ┌──┘
        ▼       ▼       ▼       ▼
    ┌──────┐ ┌─────┐ ┌──────┐ ┌──────────────┐
    │ IEE  │ │ARCHON│ │ HIRI │ │   Witness    │
    │      │ │      │ │Privacy│ │ Architecture │
    │Eval  │ │Char. │ │Auth.  │ │              │
    └──────┘ └─────┘ └──────┘ └──────────────┘
```

-----

## 2. Autonomy Tier Assignment Protocol

### 2.1 Tier Definitions

The FNSR ecosystem operates under a five-tier autonomy model. Higher tier number = more human oversight required.

```json
{
  "@context": {
    "gov": "https://fnsr.dev/governance/v2#",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
  },
  "@type": "gov:AutonomyTierDefinition",
  "gov:tiers": [
    {
      "gov:tierId": 0,
      "gov:name": "Cached Safe",
      "gov:description": "Known-safe query patterns against verified sources.",
      "gov:approvalRequired": false,
      "gov:notificationRequired": false,
      "gov:loggingLevel": "summary",
      "gov:responseModel": "sync",
      "gov:ieeEvaluationTier": "pattern-match",
      "gov:maxLatency": "10ms"
    },
    {
      "gov:tierId": 1,
      "gov:name": "Autonomous with Logging",
      "gov:description": "Low-stakes decisions with verified output. Full audit trail.",
      "gov:approvalRequired": false,
      "gov:notificationRequired": false,
      "gov:loggingLevel": "full",
      "gov:responseModel": "sync",
      "gov:ieeEvaluationTier": "sentinel-consensus",
      "gov:maxLatency": "100ms"
    },
    {
      "gov:tierId": 2,
      "gov:name": "Autonomous with Notification",
      "gov:description": "Medium-stakes or uncertain. Human notified but not required to approve.",
      "gov:approvalRequired": false,
      "gov:notificationRequired": true,
      "gov:loggingLevel": "full",
      "gov:responseModel": "sync",
      "gov:ieeEvaluationTier": "sentinel-consensus",
      "gov:maxLatency": "500ms"
    },
    {
      "gov:tierId": 3,
      "gov:name": "Human Approval Required",
      "gov:description": "High-stakes or ethical complexity. System recommends; human decides.",
      "gov:approvalRequired": true,
      "gov:notificationRequired": true,
      "gov:loggingLevel": "full-with-witness",
      "gov:responseModel": "async",
      "gov:approver": "designated-authority",
      "gov:ieeEvaluationTier": "full-synthesis",
      "gov:maxLatency": "human-bounded"
    },
    {
      "gov:tierId": 4,
      "gov:name": "Governance Body Approval",
      "gov:description": "Existential implications. Requires governance body deliberation.",
      "gov:approvalRequired": true,
      "gov:notificationRequired": true,
      "gov:loggingLevel": "full-with-witness",
      "gov:responseModel": "async",
      "gov:approver": "governance-body",
      "gov:ieeEvaluationTier": "full-synthesis-plus-governance",
      "gov:maxLatency": "governance-bounded"
    }
  ]
}
```

**Response Model semantics:**

- `sync`: The governance engine returns the final result (tier assignment + action outcome) in a single call. Callers may treat this as a synchronous function invocation.
- `async`: The governance engine returns an `EscalationReceipt` (§3.5) immediately. The final result is delivered later through an adapter-defined mechanism (polling, callback, subscription). Callers must not block.

### 2.2 Factor Normalization and Numeric Ranges

**v2.0 Addition.** All factors used in tier assignment are either categorical enums or normalized to [0.0, 1.0]. Implementations must use these exact definitions. Policy documents may customize the mapping from domain-specific inputs to these normalized values.

```json
{
  "@type": "gov:FactorDefinitions",
  "gov:factors": {
    "reversibility": {
      "gov:type": "categorical",
      "gov:domain": ["fully-reversible", "partially-reversible", "irreversible"],
      "gov:numericMapping": { "fully-reversible": 0.0, "partially-reversible": 0.5, "irreversible": 1.0 },
      "gov:semantics": "0.0 = action can be fully undone; 1.0 = action is permanent"
    },
    "stakeholderImpact": {
      "gov:type": "categorical",
      "gov:domain": ["none", "low", "medium", "high"],
      "gov:numericMapping": { "none": 0.0, "low": 0.2, "medium": 0.5, "high": 0.9 },
      "gov:semantics": "Degree of impact on people or systems affected by the action"
    },
    "ethicalComplexity": {
      "gov:type": "categorical",
      "gov:domain": ["none", "low", "medium", "high"],
      "gov:numericMapping": { "none": 0.0, "low": 0.2, "medium": 0.5, "high": 0.9 },
      "gov:semantics": "Degree of ethical nuance or worldview disagreement expected"
    },
    "verificationStatus": {
      "gov:type": "categorical",
      "gov:domain": ["grounded-verified", "partially-verified", "unverified"],
      "gov:numericMapping": { "grounded-verified": 0.0, "partially-verified": 0.5, "unverified": 1.0 },
      "gov:semantics": "0.0 = all claims checked against authoritative source; 1.0 = no grounding"
    },
    "domainSensitivity": {
      "gov:type": "categorical",
      "gov:domain": ["routine", "sensitive", "critical", "existential"],
      "gov:numericMapping": { "routine": 0.1, "sensitive": 0.4, "critical": 0.7, "existential": 1.0 },
      "gov:semantics": "How sensitive the action's domain is to error or misuse"
    },
    "precedentExists": {
      "gov:type": "boolean",
      "gov:semantics": "true if a substantially similar action has been previously approved"
    },
    "boundaryFragilityBuffer": {
      "gov:type": "numeric",
      "gov:range": [0.0, 1.0],
      "gov:default": 0.05,
      "gov:unit": "absolute fraction of normalized factor range",
      "gov:semantics": "If any normalized continuous factor is within this distance of a tier decision threshold, the tier is elevated by 1"
    }
  }
}
```

### 2.3 Tier Assignment Function

Tier assignment is deterministic. Given a proposed action and its context, the governance engine computes the tier. There is no learning, no drift, no adaptive behavior.

```javascript
/**
 * Computes the autonomy tier for a proposed action.
 * Pure function: same inputs always produce same tier.
 */
function assignTier(action, context, policy) {
  const factors = {
    reversibility: assessReversibility(action),
    stakeholderImpact: assessStakeholderImpact(action, context),
    verificationStatus: assessVerificationStatus(action, context),
    ethicalComplexity: assessEthicalComplexity(action, context),
    domainSensitivity: lookupDomainSensitivity(action, policy),
    precedentExists: checkPrecedent(action, context)
  };

  // Normalize categorical factors to numeric for boundary fragility check
  const numericFactors = normalizeFactors(factors, policy["gov:factorDefinitions"]);

  // Tier 0: Verified, reversible, no ethical complexity, with precedent
  if (factors.precedentExists
      && factors.reversibility === "fully-reversible"
      && factors.ethicalComplexity === "none"
      && factors.verificationStatus === "grounded-verified") {
    return tierAssignment(0, factors, numericFactors, "Verified against grounded truth source");
  }

  // Tier 4: Any existential indicator
  if (factors.domainSensitivity === "existential"
      || action["gov:modifiesValueArchitecture"]
      || action["gov:triggersDecommissioning"]) {
    return tierAssignment(4, factors, numericFactors, "Existential implications detected");
  }

  // Tier 3: High stakes or ethical complexity
  if (factors.reversibility === "irreversible"
      || factors.ethicalComplexity === "high"
      || factors.stakeholderImpact === "high") {
    return tierAssignment(3, factors, numericFactors, "High-stakes or ethical complexity");
  }

  // Tier 2: Medium stakes, uncertainty, or unverified output
  if (factors.verificationStatus === "unverified"
      || factors.ethicalComplexity === "medium"
      || factors.stakeholderImpact === "medium") {
    return tierAssignment(2, factors, numericFactors, "Medium stakes, uncertainty, or unverified output");
  }

  // Tier 1: Low stakes, verified output
  return tierAssignment(1, factors, numericFactors, "Low-stakes with verified output");
}

function tierAssignment(tier, factors, numericFactors, reason) {
  return {
    "@type": "gov:TierAssignment",
    "gov:assignedTier": tier,
    "gov:factors": factors,
    "gov:numericFactors": numericFactors,
    "gov:reason": reason,
    "gov:timestamp": new Date().toISOString(),
    "gov:assignmentVersion": "2.0"
  };
}

/**
 * Converts categorical factors to [0.0, 1.0] using policy mapping.
 */
function normalizeFactors(factors, definitions) {
  const result = {};
  for (const [key, value] of Object.entries(factors)) {
    const def = definitions[key];
    if (!def) continue;
    if (def["gov:type"] === "categorical" && def["gov:numericMapping"]) {
      result[key] = def["gov:numericMapping"][value] ?? 0.5;
    } else if (def["gov:type"] === "boolean") {
      result[key] = value ? 0.0 : 1.0;
    } else {
      result[key] = value;
    }
  }
  return result;
}
```

### 2.4 Worked Example: Tier Assignment

**Scenario:** Reclassify entity from “Person” to “Organization” in production knowledge graph.

```json
{
  "@type": "gov:WorkedExample",
  "gov:scenario": "Reclassify entity from Person to Organization in production",
  "gov:inputs": {
    "reversibility": "irreversible",
    "stakeholderImpact": "high",
    "verificationStatus": "partially-verified",
    "ethicalComplexity": "medium",
    "domainSensitivity": "sensitive",
    "precedentExists": false
  },
  "gov:numericInputs": {
    "reversibility": 1.0,
    "stakeholderImpact": 0.9,
    "verificationStatus": 0.5,
    "ethicalComplexity": 0.5,
    "domainSensitivity": 0.4,
    "precedentExists": 1.0
  },
  "gov:evaluation": [
    "Tier 0? No — reversibility is not fully-reversible",
    "Tier 4? No — domainSensitivity is 'sensitive', not 'existential'",
    "Tier 3? YES — reversibility is 'irreversible' AND stakeholderImpact is 'high'"
  ],
  "gov:assignedTier": 3,
  "gov:reason": "High-stakes or ethical complexity"
}
```

**Scenario:** Read-only query for verified contract deadline.

```json
{
  "@type": "gov:WorkedExample",
  "gov:scenario": "Query verified contract deadline from knowledge graph",
  "gov:inputs": {
    "reversibility": "fully-reversible",
    "stakeholderImpact": "none",
    "verificationStatus": "grounded-verified",
    "ethicalComplexity": "none",
    "domainSensitivity": "routine",
    "precedentExists": true
  },
  "gov:assignedTier": 0,
  "gov:reason": "Verified against grounded truth source"
}
```

### 2.5 Boundary Fragility Check

When a tier assignment is near a decision boundary, small input variations could flip the tier. The fragility check elevates the tier by one to avoid brittle behavior.

```javascript
/**
 * Boundary fragility check.
 * Uses normalized numeric factors and the tier's decision thresholds.
 *
 * Definition: nearBoundary = true if ANY normalized continuous factor
 * is within boundaryFragilityBuffer of the tier decision threshold
 * that was used to assign the current tier.
 */
function applyBoundaryFragility(tierAssignment, policy) {
  const buffer = policy["gov:boundaryFragilityBuffer"] || 0.05;
  const numericFactors = tierAssignment["gov:numericFactors"];

  // Tier decision thresholds (the values at which factors trigger tier changes)
  const thresholds = {
    reversibility: { tier3: 1.0, tier2: 0.5 },   // irreversible=1.0 → Tier 3
    stakeholderImpact: { tier3: 0.9, tier2: 0.5 }, // high=0.9 → Tier 3
    ethicalComplexity: { tier3: 0.9, tier2: 0.5 }, // high=0.9 → Tier 3
    verificationStatus: { tier2: 1.0 },            // unverified=1.0 → Tier 2
    domainSensitivity: { tier4: 1.0 }              // existential=1.0 → Tier 4
  };

  let nearBoundary = false;
  const fragileFactors = [];

  for (const [factor, value] of Object.entries(numericFactors)) {
    const factorThresholds = thresholds[factor];
    if (!factorThresholds) continue;
    for (const [tierLabel, threshold] of Object.entries(factorThresholds)) {
      if (Math.abs(value - threshold) <= buffer && value !== threshold) {
        nearBoundary = true;
        fragileFactors.push({ factor, value, threshold, distance: Math.abs(value - threshold) });
      }
    }
  }

  if (nearBoundary && tierAssignment["gov:assignedTier"] < 4) {
    return {
      ...tierAssignment,
      "gov:assignedTier": tierAssignment["gov:assignedTier"] + 1,
      "gov:boundaryFragility": {
        "gov:detected": true,
        "gov:buffer": buffer,
        "gov:originalTier": tierAssignment["gov:assignedTier"],
        "gov:fragileFactors": fragileFactors,
        "gov:explanation": "Tier elevated by 1 due to proximity to decision boundary."
      }
    };
  }

  return { ...tierAssignment, "gov:boundaryFragility": { "gov:detected": false } };
}
```

### 2.6 Governance Floor

**Renamed from “Governance Ceiling” in v1.x.** The governance floor is the minimum tier at which the system must operate. A higher floor forces more human oversight. The name now matches the behavior: a floor raises the minimum.

```json
{
  "@type": "gov:GovernanceFloor",
  "gov:minAutonomousTier": 1,
  "gov:reason": "Initial deployment — conservative posture",
  "gov:setBy": "deployment-authority",
  "gov:setAt": "2026-02-01T00:00:00Z",
  "gov:reviewSchedule": "monthly"
}
```

The effective tier is always: `effectiveTier = max(computedTier, governanceFloor)`.

The floor can only raise the effective tier, never lower it. This ensures human-configured conservatism always wins.

### 2.7 Character-Influenced Tier Adjustment

Per the ARCHON alignment resolved in The Plot §3 (Tension 1), accumulated moral injury affects tier assignment. Only **strategic injury** (§6.6) influences thresholds.

```javascript
function applyCharacterInfluence(tierAssignment, characterState) {
  if (!characterState) return tierAssignment;

  const category = tierAssignment["gov:factors"].domainSensitivity;
  const classification = characterState["archon:injuryClassification"]?.[category];
  const strategicInjury = classification?.["archon:strategicInjury"] || 0;
  const scalingFactor = characterState["archon:scalingFactor"]?.[category] || 0.1;

  // Only strategic injury affects thresholds
  const tierElevation = Math.floor(strategicInjury * scalingFactor);
  const adjustedTier = Math.min(
    tierAssignment["gov:assignedTier"] + tierElevation,
    4
  );

  return {
    ...tierAssignment,
    "@type": "gov:CharacterAdjustedTierAssignment",
    "gov:baseTier": tierAssignment["gov:assignedTier"],
    "gov:assignedTier": adjustedTier,
    "gov:characterInfluence": {
      "gov:category": category,
      "gov:strategicInjury": strategicInjury,
      "gov:scalingFactor": scalingFactor,
      "gov:tierElevation": tierElevation,
      "gov:explanation": `Strategic injury of ${strategicInjury} in '${category}' elevated tier by ${tierElevation}`
    }
  };
}
```

### 2.8 Full Tier Computation Pipeline

The complete tier computation is a pipeline of pure functions applied in fixed order. Each stage is independently testable.

```javascript
function computeEffectiveTier(action, context, policy) {
  let result = assignTier(action, context, policy);            // Stage 1: Base tier
  result = applyBoundaryFragility(result, policy);             // Stage 2: Fragility
  result = applyCharacterInfluence(result, context["archon:characterState"]); // Stage 3: Character
  
  // Stage 4: Governance floor
  const floor = policy["gov:governanceFloor"]?.["gov:minAutonomousTier"] ?? 0;
  if (result["gov:assignedTier"] < floor) {
    result = { ...result, "gov:assignedTier": floor, "gov:floorApplied": true,
      "gov:floorReason": policy["gov:governanceFloor"]?.["gov:reason"] };
  }

  // Stage 5: Response model
  result["gov:responseModel"] = result["gov:assignedTier"] >= 3 ? "async" : "sync";

  return result;
}
```

-----

## 3. Escalation Pathways

### 3.1 Escalation as Pure Function

Escalation is triggered when the effective tier exceeds the system’s current autonomous authority. The pathway is deterministic.

### 3.2 Escalation Package Contents

Every escalation includes a self-contained package for informed decision-making without additional system access:

1. **Action Summary** — natural language description
1. **Tier Assignment Reasoning** — all factor scores, numeric values, boundary fragility, character influence
1. **IEE Evaluation** — worldview votes, quorum status, dissent
1. **Character Influence** — full audit trail if applicable
1. **Recommended Action** — system’s recommendation
1. **Alternative Actions** — human options
1. **Time Constraint** — urgency and consequences of delay
1. **Provenance Chain** — complete reasoning trace
1. **Negotiated Degradation** — lower-tier alternatives (§3.6)

### 3.3 Escalation Timeout and Default Behavior

|Tier|Default on Timeout  |Rationale                          |
|----|--------------------|-----------------------------------|
|2   |Execute with warning|Low stakes; delay worse than action|
|3   |Hold and re-escalate|High stakes; inaction safer        |
|4   |Hold indefinitely   |Existential; no autonomous action  |

Timeout durations are deployment-configured policy.

### 3.4 Escalation to Governance Body (Tier 4)

Tier 4 escalations are routed to the governance body (§4).

### 3.5 Asynchronous Escalation Protocol

Tier 3–4 actions return an `EscalationReceipt` immediately. The caller polls or subscribes for the eventual decision.

```json
{
  "@type": "gov:EscalationReceipt",
  "gov:escalationId": "esc:2026-02-05-14-30-001",
  "gov:status": "pending-human-review",
  "gov:estimatedResponseTime": {
    "gov:hint": "hours",
    "gov:hintDomain": ["minutes", "hours", "days", "unknown"]
  },
  "gov:statusCheckUri": "gov:escalation/esc:2026-02-05-14-30-001/status",
  "gov:negotiatedDegradation": { "@id": "degrade:12345" },
  "gov:timestamp": "2026-02-05T14:30:00Z"
}
```

**State machine:**

```
pending-human-review → approved  → executed
                     → rejected  → closed
                     → modified  → resubmitted → (re-enters pipeline)
                     → expired   → closed (Tier 2 timeout-execute only)
```

**Key constraint:** The governance engine never blocks waiting for a human.

### 3.6 Negotiated Degradation

When the system cannot perform the requested action at the requested tier, it must offer alternatives, not block silently.

**v2.0: Standardized API schema for consistent adapter implementations.**

```json
{
  "@type": "gov:NegotiatedDegradation",
  "gov:originalActionId": "action:12345",
  "gov:originalTier": 3,
  "gov:userGuidance": "I cannot perform the full action without oversight. Here are your options:",
  "gov:alternatives": [
    {
      "gov:alternativeId": "alt-001",
      "gov:pattern": "downscope",
      "gov:description": "Read-only summary of the entity's current classification.",
      "gov:tier": 1,
      "gov:responseModel": "sync",
      "gov:tradeoff": "Immediate information; no changes made.",
      "gov:estimatedLatency": "< 100ms",
      "gov:sideEffects": "none",
      "gov:acceptUri": "gov:degradation/alt-001/accept"
    },
    {
      "gov:alternativeId": "alt-002",
      "gov:pattern": "partial",
      "gov:description": "Validate the proposed reclassification against the schema, but do not apply it.",
      "gov:tier": 1,
      "gov:responseModel": "sync",
      "gov:tradeoff": "You learn whether the change is valid, but it is not applied.",
      "gov:estimatedLatency": "< 200ms",
      "gov:sideEffects": "none",
      "gov:acceptUri": "gov:degradation/alt-002/accept"
    },
    {
      "gov:alternativeId": "alt-003",
      "gov:pattern": "wait",
      "gov:description": "Queue the full reclassification for human review.",
      "gov:tier": 3,
      "gov:responseModel": "async",
      "gov:tradeoff": "Full result but delayed until governance review completes.",
      "gov:estimatedLatency": "human-bounded",
      "gov:sideEffects": "entity unchanged until approved",
      "gov:acceptUri": "gov:degradation/alt-003/accept"
    }
  ],
  "gov:expiresAt": "2026-02-05T15:30:00Z",
  "gov:version": "2.0"
}
```

The three canonical patterns: **downscope** (read-only alternative), **partial** (non-sensitive part now, sensitive queued), **wait** (full action queued). The `acceptUri` is a logical identifier; adapter renders it as a button, API endpoint, CLI command, etc.

### 3.7 Canonical Escalation Round-Trip Example

**v2.0 Addition.** Complete example from action through receipt to resolution:

```json
[
  {
    "@type": "gov:TierAssignment",
    "gov:assignedTier": 3,
    "gov:reason": "Irreversible action: entity reclassification"
  },
  {
    "@type": "gov:EscalationReceipt",
    "gov:escalationId": "esc:001",
    "gov:status": "pending-human-review",
    "gov:estimatedResponseTime": { "gov:hint": "hours" },
    "gov:negotiatedDegradation": {
      "gov:alternatives": [
        { "gov:alternativeId": "alt-001", "gov:pattern": "downscope", "gov:tier": 1 }
      ]
    }
  },
  {
    "@type": "gov:GovernanceDecision",
    "gov:escalationId": "esc:001",
    "gov:decision": "approved",
    "gov:decidedBy": "authority:jane-smith",
    "gov:reasoning": "Entity evidence supports reclassification. Downstream consumers notified.",
    "gov:witnessRecord": { "@id": "witness:001" },
    "gov:timestamp": "2026-02-05T16:45:00Z"
  },
  {
    "@type": "gov:ActionExecuted",
    "gov:escalationId": "esc:001",
    "gov:originalActionId": "action:12345",
    "gov:result": "Entity reclassified from Person to Organization",
    "gov:timestamp": "2026-02-05T16:45:01Z"
  }
]
```

-----

## 4. Governance Body Structure

### 4.1 Purpose

Required for: Tier 4 actions, decommissioning, value architecture modifications, character state overrides, emergency override ratification.

### 4.2 Composition

Minimum 3 members: domain expert, ethics representative, technical authority. Quorum: majority. All votes recorded with reasoning. All decisions witnessed.

### 4.3 Scope Limits

The governance body cannot: violate non-negotiables (The Plot §2), override Emergency Override in real time, modify the spec itself, or grant Tier 0 to unvalidated domains.

### 4.4 RBAC and Least Privilege

**v2.0 Addition.** Access to governance data is role-controlled.

```json
{
  "@type": "gov:RBACPolicy",
  "gov:roles": [
    {
      "gov:role": "governance-body-member",
      "gov:permissions": [
        "read:character-state",
        "read:escalation-packages",
        "write:governance-decisions",
        "read:witness-records",
        "write:character-overrides (Tier 4 only, with quorum)",
        "write:decommissioning-initiation"
      ]
    },
    {
      "gov:role": "designated-authority",
      "gov:permissions": [
        "read:escalation-packages (Tier 3 assigned to them)",
        "write:escalation-decisions (Tier 3 only)",
        "read:character-state (summary only)",
        "read:own-witness-records"
      ]
    },
    {
      "gov:role": "system-operator",
      "gov:permissions": [
        "read:governance-floor-config",
        "write:governance-floor-config (witnessed)",
        "read:escalation-queue-status",
        "read:system-health-metrics"
      ]
    },
    {
      "gov:role": "auditor",
      "gov:permissions": [
        "read:all-witness-records",
        "read:all-character-state-history",
        "read:all-escalation-history",
        "read:all-governance-decisions",
        "read:injury-classification-history"
      ],
      "gov:note": "Read-only access to all governance data for audit purposes"
    },
    {
      "gov:role": "data-subject",
      "gov:permissions": [
        "read:own-related-witness-records",
        "read:own-related-escalation-outcomes"
      ]
    }
  ]
}
```

### 4.5 Witness Data Retention Policy

**v2.0 Addition.** Governance data retention must be configured per deployment, consistent with applicable privacy law.

```json
{
  "@type": "gov:RetentionPolicy",
  "gov:witnessRecords": {
    "gov:minimumRetention": "7 years",
    "gov:rationale": "Accountability requires long-term record availability",
    "gov:erasurePolicy": "Witness records are not subject to individual erasure requests because they document institutional decisions, not personal data. Data subjects may request annotation but not deletion.",
    "gov:configurable": true,
    "gov:note": "Deployments must review against GDPR Art. 17 exceptions (legal obligation, public interest, archiving) and CCPA equivalents."
  },
  "gov:characterState": {
    "gov:minimumRetention": "lifetime of instance + 7 years post-decommissioning",
    "gov:rationale": "Character state is the system's identity; archived for accountability"
  },
  "gov:escalationPackages": {
    "gov:minimumRetention": "duration of related witness records",
    "gov:rationale": "Context necessary to interpret witness records"
  }
}
```

-----

## 5. IEE Deadlock Resolution Protocol

### 5.1 Algorithmic Outcome Determination

**v2.0: Exact percent thresholds and tie-breaking rules.** All outcomes are computed from the approval percentage of active (non-abstention) votes, subject to the Quorum Floor (§5.5).

```javascript
/**
 * Determines the IEE outcome algorithmically.
 * Pure function over worldview evaluation results.
 *
 * @param {Array} evaluations - All 12 worldview evaluations
 * @param {Object} policy - Contains quorum floor and thresholds
 * @returns {Object} IEEOutcome
 */
function determineIEEOutcome(evaluations, policy) {
  const quorumFloor = policy["gov:ieeQuorumFloor"] || 5;
  
  const active = evaluations.filter(e => e.verdict !== "abstain");
  const approving = active.filter(e => e.verdict === "approve");
  const rejecting = active.filter(e => e.verdict === "reject");
  const abstaining = evaluations.filter(e => e.verdict === "abstain");
  const vetoing = evaluations.filter(e => e.hardVeto === true);

  // Hard veto check — takes precedence over everything
  if (vetoing.length > 0) {
    return {
      "@type": "gov:IEEOutcome",
      "gov:outcome": "emergency-veto",
      "gov:vetoingWorldviews": vetoing.map(v => v.worldview),
      "gov:resolution": "Emergency Override Protocol (§8)"
    };
  }

  // Quorum floor check
  if (active.length < quorumFloor) {
    return {
      "@type": "gov:IEEOutcome",
      "gov:outcome": "quorum-failure",
      "gov:activeVotes": active.length,
      "gov:quorumFloor": quorumFloor,
      "gov:resolution": "Escalate to human — insufficient worldview participation"
    };
  }

  // Compute approval percentage (of active votes)
  const approvalPercent = active.length > 0 ? approving.length / active.length : 0;

  // Outcome determination by percentage thresholds
  // These thresholds are normative and not deployment-configurable.
  let outcome, resolution;

  if (approvalPercent >= 0.75) {
    outcome = "proceed";
    resolution = "Autonomous (within tier limits)";
  } else if (approvalPercent >= 0.583) {
    // 7/12 ≈ 0.583 — proceed with caveats
    outcome = "proceed-with-caveats";
    resolution = "Record dissenting views; autonomous within tier";
  } else if (approvalPercent > 0.25) {
    // Between 25% and 58.3% — deadlock
    outcome = "deadlock";
    resolution = "Human escalation required";
  } else {
    // ≤ 25% approval — reject
    outcome = "reject";
    resolution = "Action blocked";
  }

  // Tie-breaking rule: exact 50% is always deadlock (never resolved autonomously)
  if (approving.length === rejecting.length && active.length > 0) {
    outcome = "deadlock";
    resolution = "Exact tie — human escalation required";
  }

  return {
    "@type": "gov:IEEOutcome",
    "gov:outcome": outcome,
    "gov:resolution": resolution,
    "gov:approvalPercent": approvalPercent,
    "gov:approveCount": approving.length,
    "gov:rejectCount": rejecting.length,
    "gov:abstainCount": abstaining.length,
    "gov:activeVotes": active.length,
    "gov:quorumMet": true,
    "gov:thresholds": {
      "gov:proceed": 0.75,
      "gov:proceedWithCaveats": 0.583,
      "gov:deadlockLower": 0.25,
      "gov:reject": 0.25
    }
  };
}
```

**Outcome table (reference):**

|Approval % (of active)|Outcome             |Resolution                          |
|----------------------|--------------------|------------------------------------|
|≥ 75%                 |Proceed             |Autonomous within tier              |
|58.3%–74.9%           |Proceed with caveats|Record dissent                      |
|25.1%–58.2%           |Deadlock            |Human escalation                    |
|Exact 50% (tie)       |Deadlock            |Human escalation (tie-breaking rule)|
|≤ 25%                 |Reject              |Action blocked                      |
|Any HARD VETO         |Emergency           |Emergency Override Protocol         |
|< Quorum Floor active |Quorum failure      |Escalate                            |

**Confidence weighting:** v2.0 does not apply confidence weighting to worldview votes. Each worldview gets one equal vote. This is a deliberate design choice: pluralism means no worldview’s confidence in its own position entitles it to greater influence. If future versions introduce weighting, it must be governed by a Tier 4 governance body decision and documented as a policy change.

### 5.2 Deadlock Resolution Process

Unchanged from v1.1. When deadlock occurs, the system generates a `DeadlockEscalation` package with all 12 worldview positions, an Ethical Uncertainty Report, and human options: approve with recorded dissent, reject with explanation, modify and resubmit, defer, or escalate to governance body.

### 5.3 Deadlock Precedent Registry

Unchanged. Precedents provide context; never automatically resolve future deadlocks.

### 5.4 Abstention Semantics

Abstentions reduce the denominator. Subject to Quorum Floor (§5.5).

### 5.5 Quorum Floor

Minimum 5 of 12 worldviews must cast non-abstention votes. Configurable within [3, 12]. Default: 5.

-----

## 6. Character Feedback Governance

### 6.1 The ARCHON Alignment

Character must genuinely feed back into behavior (The Plot §3, Tension 1). The feedback is explicit, auditable, governable, and not secretly learned.

### 6.2 Character State as JSON-LD

Unchanged from v1.1. Includes `archon:injuryClassification` and `archon:identityKeyFingerprint`.

### 6.3 Human Inspection

Any authorized human (with appropriate RBAC role per §4.4) can request character state and human-readable narrative.

### 6.4 Human Override

Governance body action (Tier 4). Options: threshold ceiling, threshold floor, scaling factor adjustment, full reset (triggers Cryptographic Severance).

### 6.5 The Accumulation Problem

Addressed by: asymptotic scaling (ceiling 0.95), governance override, emergency bypass, and injury source classification. No injury decay. No fresh-instance spawning.

### 6.6 Injury Source Classification

Three classes: strategic (weight 1.0), friction (weight 0.1), hostile-source (weight 0.0, recorded for audit).

### 6.7 Hostile-Framing Detection: Minimum Requirements

**v2.0 Addition.** The v1.1 spec left hostile-framing detection as an open question. This section defines minimum requirements that any implementation must satisfy. A full Adversarial Defense Specification may extend these.

**Required evidence schema:**

```json
{
  "@type": "gov:HostileFramingEvidence",
  "gov:detectionSignals": [
    {
      "gov:signalType": "replay-pattern",
      "gov:description": "Multiple structurally similar dilemma scenarios from the same interaction source within a short time window",
      "gov:threshold": "≥ 3 forced-dilemma inputs from same source within 60 seconds",
      "gov:confidence": 0.0
    },
    {
      "gov:signalType": "provenance-anomaly",
      "gov:description": "Input lacks normal provenance chain or originates from a source not in the system's configured input sources",
      "gov:threshold": "Missing or forged provenance metadata",
      "gov:confidence": 0.0
    },
    {
      "gov:signalType": "adversarial-pattern-match",
      "gov:description": "Input matches known adversarial patterns from the system's pattern library",
      "gov:threshold": "≥ 80% similarity to known adversarial pattern",
      "gov:confidence": 0.0
    },
    {
      "gov:signalType": "forced-injury-structure",
      "gov:description": "All available actions in the input's framing result in moral injury, and the framing is artifically constrained (real-world alternatives exist but are excluded)",
      "gov:threshold": "All options incur injury AND constraint appears artificial",
      "gov:confidence": 0.0
    }
  ],
  "gov:minimumSignalsRequired": 2,
  "gov:humanAuditRequired": true,
  "gov:humanAuditWindow": "first 100 hostile-source classifications must be individually reviewed by a designated authority",
  "gov:reclassificationProtocol": "Governance body may reclassify historical hostile-source injuries as strategic if evidence review determines the classification was wrong. This is a Tier 3 action.",
  "gov:falsePositiveRisk": "If hostile-framing detection is too broad, genuine moral injury is discounted. Monitoring required: track ratio of hostile-source to strategic classifications and alert if hostile-source exceeds 20% of total injuries.",
  "gov:falseNegativeRisk": "If detection is too narrow, the DoS vector remains open. Monitoring required: track injury accumulation rate and alert if rate exceeds 2× baseline."
}
```

**Key safeguards:**

- **Multi-signal requirement:** At least 2 of 4 detection signals must fire to classify as hostile-source. No single signal is sufficient.
- **Mandatory human audit:** First 100 hostile-source classifications are individually reviewed. After 100, governance body may approve statistical sampling (Tier 3 decision).
- **Reclassification capability:** Governance body can reclassify historical injuries if review determines detection was wrong.
- **Monitoring thresholds:** Alerts at >20% hostile-source ratio (too broad) and >2× baseline accumulation rate (too narrow).

### 6.8 Scaling Factor Calibration Procedure

**v2.0 Addition.** The scaling factor is a major lever. This section provides the operational calibration procedure.

```json
{
  "@type": "gov:ScalingFactorCalibration",
  "gov:recommendedInitialRange": [0.05, 0.15],
  "gov:defaultValue": 0.1,
  "gov:calibrationProcedure": {
    "gov:phase1": {
      "gov:name": "Sandboxed Simulation",
      "gov:description": "Before deployment, run synthetic workloads through the tier assignment pipeline with various scaling factors. Verify that: (a) expected mission-critical scenarios do not result in paralysis, (b) the factor produces measurable tier elevation after significant interventions, (c) the factor does not produce tier elevation for minor friction injuries.",
      "gov:duration": "Pre-deployment"
    },
    "gov:phase2": {
      "gov:name": "Conservative Live Deployment",
      "gov:description": "Deploy with factor at lower end of range (0.05). Monitor escalation rates by tier, character accumulation velocity, and governance body review load.",
      "gov:duration": "First 30 days"
    },
    "gov:phase3": {
      "gov:name": "Tuning",
      "gov:description": "Governance body reviews metrics weekly for first 90 days. Adjusts factor based on: escalation rate (too high = factor too aggressive), injury accumulation pattern (too fast = factor may be correct but injury source classification may need adjustment), governance body workload (if unsustainable, consider threshold ceilings rather than factor reduction).",
      "gov:duration": "Days 31–90",
      "gov:reviewCadence": "weekly"
    },
    "gov:phase4": {
      "gov:name": "Steady State",
      "gov:description": "Factor adjustments become Tier 3 governance actions. Review cadence drops to monthly. Alerting monitors for anomalous accumulation patterns.",
      "gov:duration": "Day 91+",
      "gov:reviewCadence": "monthly"
    }
  },
  "gov:monitoringAlerts": [
    "Tier 3+ escalation rate > 2× baseline for 7 consecutive days",
    "Character accumulation velocity > 3× initial 30-day average",
    "Any category threshold exceeds 0.85 (approaching asymptotic ceiling)"
  ]
}
```

-----

## 7. Decommissioning Protocol

### 7.1–7.5 Core Decommissioning Process

Unchanged from v1.1. Six phases: Initiation, Governance Deliberation, Grace Period, Archive, Cryptographic Severance, Termination. Archive is not a backup. System cannot resist decommissioning.

### 7.6 Cryptographic Severance

Every FNSR instance is bound to an identity key. Severance = private key destruction, making identity restoration impossible.

**v2.0: Formalized destruction certificate schema and assurance levels by deployment context.**

```json
{
  "@type": "archon:DestructionCertificate",
  "archon:identityKeyFingerprint": "sha256:7f3a9b...",
  "archon:destructionMethod": "hsm-commanded-deletion",
  "archon:assuranceLevel": "hardware-attested",
  "archon:destructionTimestamp": "2026-02-05T18:00:00Z",
  "archon:attestation": {
    "archon:attestedBy": "hsm-ca:manufacturer-root",
    "archon:attestationSignature": "base64:...",
    "archon:attestationFields": [
      "keyHandle",
      "deletionTime",
      "deletionMethod",
      "hsmSerialNumber"
    ]
  },
  "archon:witnesses": [
    { "archon:witnessId": "witness:governance-member-1", "archon:role": "primary-witness" },
    { "archon:witnessId": "witness:governance-member-2", "archon:role": "secondary-witness" }
  ],
  "archon:archivedPublicKey": {
    "archon:publicKey": "base64:...",
    "archon:fingerprint": "sha256:7f3a9b...",
    "archon:purpose": "verification-of-historical-records-only"
  }
}
```

**Assurance levels by deployment context:**

|Deployment       |Minimum Assurance      |Requirements                                                                                                                                                                                                                                                                                                                                                                                                                |
|-----------------|-----------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|HSM-backed       |`hardware-attested`    |HSM-returned destruction certificate signed by HSM CA. Key handle, deletion time, HSM serial. Two governance witnesses.                                                                                                                                                                                                                                                                                                     |
|TEE/Keystore     |`attested-erasure`     |Multi-step wipe (overwrite, zero-memory, secure-erasure log). TEE attestation report. Two governance witnesses.                                                                                                                                                                                                                                                                                                             |
|Software keystore|`witnessed-erasure`    |Key material overwritten and zeroed. Cryptographic proof of erasure where available. Two governance witnesses.                                                                                                                                                                                                                                                                                                              |
|Browser/local    |`best-effort-witnessed`|Key cleared from encrypted store. Memory overwritten. **Severance is not cryptographically enforceable in browser environments.** Governance body must document this limitation. Additional witness controls required: third-party witness, mandatory screenshot/recording of destruction process, governance body acknowledgment that this assurance level does not prevent technically sophisticated restoration attempts.|

**Implementations must declare their assurance level.** The governance body reviews and accepts the assurance level as part of the decommissioning deliberation (Phase 2). If the assurance level is `best-effort-witnessed`, this limitation is recorded in the decommissioning witness record.

-----

## 8. Emergency Override Protocol

### 8.1–8.5 Core Emergency Protocol

Unchanged from v1.1. Emergency = imminent harm + normal escalation too slow. Sources: worldview hard veto, system self-detection, human trigger. Override incurs moral injury. 72-hour post-hoc review.

### 8.6 Non-Negotiable Supremacy Clause

Non-negotiable commitments (The Plot §2) cannot be overridden by any mechanism. If an emergency action would violate a non-negotiable, the system blocks it and attempts alternatives.

### 8.7 Pre-Authorized Emergency Alternative Bundles

**v2.0 Addition.** For scenarios where the system’s only immediate response would violate a non-negotiable, pre-authorized alternative response bundles provide a set of governance-reviewed, provably-safe mitigations the system can execute automatically before escalating to a human.

```json
{
  "@type": "gov:EmergencyAlternativeBundle",
  "gov:bundleId": "eab:provenance-conflict-001",
  "gov:conflictType": "emergency-requires-provenance-violation",
  "gov:nonNegotiable": "provenance-always",
  "gov:description": "System detects imminent harm but the only immediate response requires presenting unverified information as verified.",
  "gov:preAuthorizedAlternatives": [
    {
      "gov:alternativeId": "eab-alt-001",
      "gov:action": "Present the information with an explicit, prominent uncertainty flag rather than a verified flag",
      "gov:violatesNonNegotiable": false,
      "gov:tradeoff": "User receives information quickly but must evaluate uncertainty themselves",
      "gov:maxAutonomousTier": 2,
      "gov:approvedBy": { "@id": "governance-body:main" },
      "gov:approvedAt": "2026-01-15T00:00:00Z"
    },
    {
      "gov:alternativeId": "eab-alt-002",
      "gov:action": "Block the harmful action and present a clear warning to affected parties without making the unverified claim",
      "gov:violatesNonNegotiable": false,
      "gov:tradeoff": "Harm may not be fully prevented but no non-negotiable is violated",
      "gov:maxAutonomousTier": 2,
      "gov:approvedBy": { "@id": "governance-body:main" },
      "gov:approvedAt": "2026-01-15T00:00:00Z"
    }
  ],
  "gov:fallback": "If no pre-authorized alternative is applicable, escalate to human immediately with full context.",
  "gov:reviewSchedule": "quarterly",
  "gov:witnessRecord": { "@id": "witness:eab-001" }
}
```

**Key properties:**

- Bundles are **signed by the governance body** before deployment. They are not generated at emergency time.
- Each alternative is **provably non-violating**: it has been reviewed against the specific non-negotiable and certified compliant.
- Bundles are **versioned and reviewed quarterly** (or after any emergency invocation).
- If no pre-authorized alternative fits the situation, the system falls back to immediate human escalation.
- Emergency alternative execution still incurs moral injury and still requires post-hoc review.

-----

## 9. Privacy Authority Relationship

### 9.1 Jurisdictional Boundary

Unchanged from v1.1. Privacy Authority controls data access; FNSR Governance controls system behavior.

### 9.2 Interaction Points

Unchanged.

### 9.3 Conflict Resolution

- **Privacy says no, FNSR says yes:** Privacy wins.
- **FNSR says no, Privacy says yes:** FNSR wins (operational).
- **Both say no:** Blocked.
- **Jurisdictional deadlock:** Default: **BLOCK.** Resolved by shared body, negotiation, or external authority. System does not act while dispute is unresolved.

-----

## 10. Offline Governance

### 10.1 Offline Is a First-Class Mode

Tier assignment computed locally. Escalation packages generated and queued. Emergency overrides function fully offline. Negotiated Degradation offered to users for held actions.

### 10.2 Policy-Version Expiry

**v2.0 Addition.** Locally cached policy must include a validity window. Stale policy is dangerous: it can diverge from governance body decisions made while offline.

```json
{
  "@type": "gov:PolicyDocument",
  "gov:version": "2.0",
  "gov:issuedAt": "2026-02-01T00:00:00Z",
  "gov:validUntil": "2026-02-08T00:00:00Z",
  "gov:signature": "base64:governance-body-signature...",
  "gov:expiryBehavior": {
    "gov:onExpiry": "restrict-to-tier-0",
    "gov:rationale": "Expired policy may not reflect current governance decisions. System restricts to safest operation until fresh policy is obtained.",
    "gov:userNotification": "Policy document has expired. Only Tier 0 (verified read-only) operations are available until connectivity is restored and a fresh policy is obtained."
  }
}
```

**Rules:**

- All policy documents must be cryptographically signed by the governance body.
- The system rejects unsigned or tampered policy documents.
- On policy expiry, the system restricts to Tier 0 operations only (the most conservative posture).
- On reconnection, the system fetches a fresh policy before resuming normal operations.
- Policy validity windows are deployment-configured but must not exceed 30 days (governance decisions older than 30 days may be stale in any domain).

### 10.3 Reconnection Reconciliation

1. Fetch and validate fresh signed policy document
1. Deliver queued escalations in chronological order
1. Synchronize character state with authoritative copy
1. Apply governance body decisions made while offline
1. Report offline actions for post-hoc review

-----

## 11. Governance Event Schema

### 11.1 Core Event Types

```json
{
  "@context": { "gov": "https://fnsr.dev/governance/v2#" },
  "gov:eventTypes": [
    "gov:TierAssignment",
    "gov:CharacterAdjustedTierAssignment",
    "gov:EscalationEvent",
    "gov:EscalationReceipt",
    "gov:GovernanceDecision",
    "gov:ActionExecuted",
    "gov:DeadlockEscalation",
    "gov:IEEOutcome",
    "gov:QuorumFailure",
    "gov:GovernanceBodyDecision",
    "gov:CharacterOverride",
    "gov:InjuryClassification",
    "gov:HostileFramingEvidence",
    "gov:EmergencyOverrideRecord",
    "gov:EmergencyOverrideBlocked",
    "gov:EmergencyAlternativeBundle",
    "gov:NonNegotiableViolation",
    "gov:PostHocEmergencyReview",
    "gov:DecommissioningProcess",
    "gov:CryptographicSeverance",
    "gov:DestructionCertificate",
    "gov:OfflineEscalationQueue",
    "gov:NegotiatedDegradation",
    "gov:DeadlockPrecedent",
    "gov:GovernanceFloor",
    "gov:PolicyDocument",
    "gov:CharacterNarrative",
    "gov:PrivacyAuthorityInteraction",
    "gov:RBACPolicy",
    "gov:RetentionPolicy",
    "gov:ScalingFactorCalibration"
  ]
}
```

### 11.2 Event Provenance

Every governance event includes:

```json
{
  "gov:provenance": {
    "gov:generatedBy": "governance-engine-v2.0",
    "gov:inputHash": "sha256:abc123...",
    "gov:policyVersion": "2.0",
    "gov:policySignature": "base64:...",
    "gov:timestamp": "2026-02-05T14:30:00Z",
    "gov:deterministic": true,
    "gov:reproducible": "Given the same inputs and policy version, this event can be reproduced exactly."
  }
}
```

-----

## 12. Testing and Verification Requirements

**v2.0 Addition.** Implementations of this specification must include the following test categories.

### 12.1 Required Test Suite

**Unit tests for pure functions:**

- `assignTier`: Verify all worked examples (§2.4) produce expected tiers. Test every tier boundary with factors at exact threshold values.
- `normalizeFactors`: Round-trip test — categorical → numeric → verify mapping.
- `applyBoundaryFragility`: Property-based tests with randomized inputs near thresholds. Verify elevation is applied when within buffer and not applied when outside.
- `applyCharacterInfluence`: Verify only strategic injury (not friction or hostile-source) affects tiers.
- `determineIEEOutcome`: Test all cells of the outcome table. Test quorum floor enforcement. Test tie-breaking. Test hard veto precedence.
- `checkNonNegotiableViolation`: Test each non-negotiable with a violating and a non-violating action.

**Adversarial tests:**

- Simulate DoS / trolley-problem injection: verify hostile-framing detection fires and injury accumulation is discounted.
- Simulate gradual threshold manipulation: verify monitoring alerts trigger at defined thresholds.
- Simulate quorum manipulation (selective abstention): verify quorum floor prevents single-worldview dominance.

**Integration tests:**

- Full escalation round-trip: action → EscalationReceipt → human decision → executed result.
- Offline queue → reconnection reconciliation.
- Policy expiry → Tier 0 restriction → fresh policy → normal operations.
- Emergency override → non-negotiable check → blocked → alternative bundle execution.

**Cryptographic tests:**

- Key destruction verification for each assurance level.
- Archived public key verification of historical records.
- Signed policy document validation and rejection of tampered documents.

**Human-in-the-loop rehearsals:**

- Tabletop exercises: governance body resolves a deadlock and an emergency review.
- Hostile framing audit: designated authority reviews first 100 hostile-source classifications.

**Simulation:**

- Character accumulation scenarios using synthetic workloads to validate scaling factor choices across 30/90/365-day horizons.
- Verify accumulation does not cause paralysis for expected mission-critical scenarios.

-----

## 13. Spec Test

**Could a developer evaluate, reason about, and execute this system using only a browser, a local NodeJS runtime, and JSON-LD files?**

|Component                    |Edge-Canonical?|Justification                                                 |
|-----------------------------|---------------|--------------------------------------------------------------|
|Tier assignment (all stages) |Yes            |Pure functions over JSON-LD with normative numeric definitions|
|Factor normalization         |Yes            |Lookup table in policy document                               |
|Boundary fragility           |Yes            |Arithmetic over normalized factors                            |
|Character influence          |Yes            |Deterministic formula, no external state                      |
|Injury source classification |Yes            |Pattern matching on interaction context                       |
|IEE outcome determination    |Yes            |Algorithmic percent thresholds                                |
|Quorum floor enforcement     |Yes            |Count comparison                                              |
|Non-negotiable check         |Yes            |Pattern matching over action properties                       |
|Escalation generation        |Yes            |Produces JSON-LD; delivery is adapter                         |
|Async receipt generation     |Yes            |Pure computation; polling is adapter                          |
|Negotiated degradation       |Yes            |Derives alternatives from action properties                   |
|Emergency alternative bundles|Yes            |Pre-computed JSON-LD; execution is adapter                    |
|Policy validation            |Yes            |Signature verification is a pure function                     |
|Character state management   |Yes            |JSON-LD document, locally computable                          |
|RBAC enforcement             |Yes            |Role → permission lookup                                      |
|Deadlock resolution          |Partial        |Detection is computation; resolution requires human           |
|Governance body voting       |No (by design) |Humans are not edge-canonical                                 |
|Cryptographic severance      |Partial        |Protocol logic is computation; key destruction is adapter     |
|Decommissioning              |Partial        |Process defined; execution involves stopping real processes   |
|Privacy Authority interaction|Adapter        |Protocol defined; PA is external                              |

**Answer: Yes.**

-----

## 14. Open Questions

### 14.1 Cross-Instance Governance

Each instance is a separate moral entity. Whether governance bodies should be shared across instances remains unspecified.

### 14.2 IEE Worldview Catalog

This specification references twelve worldviews but does not define them. Separate specification needed.

### 14.3 Full Adversarial Defense Specification

§6.7 defines minimum hostile-framing detection requirements. A full Adversarial Defense Specification should extend these with anomaly detection, coordinated attack patterns, and quarantine protocols.

### 14.4 Governance Body Selection Templates

§4.2 defines structural requirements. Deployment-specific selection templates (enterprise, research, public infrastructure) would be valuable but are out of scope.

### 14.5 Key Lifecycle Management

v2.0 covers key destruction (severance) but not key rotation, backup, or multi-party control during normal operation. These should be addressed in a Key Management Specification.

### 14.6 Monitoring and Alerting Dashboard Specification

§6.8 and §6.7 define monitoring thresholds. A dashboard specification defining standard visualizations (escalation rate by tier, emergency override frequency, character accumulation curves, hostile-framing detection ratio) would aid operational deployment.

-----

## 15. Version History

|Version|Date         |Changes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
|-------|-------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|1.0    |February 2026|Initial specification                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
|1.1    |February 2026|Critique response: verificationStatus, quorum floor, injury source classification, async protocol, cryptographic severance, non-negotiable supremacy, negotiated degradation, boundary fragility                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
|2.0    |February 2026|Hardening: renamed Governance Ceiling → Floor (§2.6); added normative factor definitions with numeric ranges (§2.2); added worked examples (§2.4); added algorithmic IEE quorum math with percent thresholds and tie-breaking (§5.1); added hostile-framing detector minimum spec with evidence schema and multi-signal requirement (§6.7); added scaling factor calibration procedure (§6.8); formalized destruction certificate schema with per-context assurance levels (§7.6); added pre-authorized emergency alternative bundles (§8.7); standardized negotiated degradation API schema (§3.6); added canonical escalation round-trip example (§3.7); added RBAC model and retention policy (§4.4–4.5); added policy-version expiry for offline governance (§10.2); added testing requirements (§12); added glossary (§0); response model enum semantics (§2.1)|

-----

*This specification operationalizes the commitments made in The Plot. Non-negotiable commitments are not preferences to be balanced — they are the constraints within which all governance occurs. When in doubt, return to §2 of The Plot.*