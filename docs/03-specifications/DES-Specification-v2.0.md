# Defeasible Expectation Service (DES) Specification

**Identifier:** `des-core-01`
**Version:** 2.0.0
**Status:** Release Candidate
**Taint Level:** L2 (Defeasible) — production-safe but explicitly overridable

---

## 1. Purpose and Scope

### 1.1 Mission

The Defeasible Expectation Service (DES) provides **common-sense reasoning** for the FNSR ecosystem through non-monotonic defaults — rules of the form "typically X, unless Y" that can be retracted when contradicting evidence appears. DES is the system's institutionalized common sense: the accumulated "usually true" knowledge that prevents naive literal interpretation while remaining transparent and auditable.

### 1.2 Architectural Position

DES occupies a critical position between raw claim extraction (TagTeam) and formal reasoning (MDRE):

```
TagTeam ──[fnsr.claim.extracted]──► DES ──[fnsr.default.applied]──► MDRE
                                        └─[fnsr.anomaly.detected]──► IEE/Review
```

Where TagTeam extracts **what was said**, DES infers **what was probably meant** and flags **what seems wrong**. This distinction is essential: DES never overwrites extracted claims but annotates them with defeasible expectations that downstream systems may accept, override, or investigate.

### 1.3 What DES Is Not

- **Not a validator**: ECCPS handles semantic constraint validation. DES detects expectation violations, not schema violations.
- **Not a learning system**: DES does not use gradient descent or opaque statistical models. Pattern recognition is frequency-based from explicit observation logs, preserving full auditability per The Plot §2.3.
- **Not a blocker**: Anomalies are signals for review, not processing halts. The system continues with the anomaly flagged.
- **Not authoritative**: All DES outputs are L2 (Defeasible). Any L1 (Verified) or stronger evidence overrides DES conclusions automatically.
- **Not a chaining engine**: DES performs single-pass evaluation. Multi-step inference chains are the responsibility of MDRE (see §3).

---

## 2. Glossary and Definitions

This section provides precise, machine-checkable definitions for all core terms. Each definition includes an **invariant** that conformance tests must verify.

### 2.1 Core Terms

```json
{
  "@type": "des:Glossary",
  "@id": "urn:des:glossary:v2",
  "terms": {
    "single-pass-evaluation": {
      "definition": "An evaluation model where all applicable rules are evaluated exactly once against the INPUT claim properties. No rule's output may serve as input to another rule within the same evaluation invocation.",
      "invariant": "∀ evaluation E: |E.passes| = 1 ∧ ∀ rule R in E: R.prerequisite ⊆ E.inputProperties",
      "machineCheckable": true,
      "testMethod": "Verify that the set of properties checked by any rule prerequisite is a subset of properties present in the original input claim"
    },
    "internal-chaining": {
      "definition": "A prohibited pattern where Rule B's prerequisite references a property that Rule A's consequent would assert, within the same DES evaluation. This creates a dependency that violates single-pass semantics.",
      "invariant": "∀ rules A, B in same evaluation: B.prerequisite ∩ A.consequent.properties = ∅",
      "machineCheckable": true,
      "testMethod": "Build property dependency graph; fail if any edge exists from consequent to prerequisite within rule set",
      "example": {
        "prohibited": {
          "ruleA": { "consequent": { "hasAccessBadge": true } },
          "ruleB": { "prerequisite": { "hasAccessBadge": true } }
        }
      }
    },
    "external-chaining": {
      "definition": "An allowed pattern where MDRE or another orchestrator invokes DES multiple times, feeding outputs from one invocation as inputs to subsequent invocations. Each DES invocation remains single-pass.",
      "invariant": "Each DES invocation is independent; state is passed explicitly via claim enrichment",
      "machineCheckable": true,
      "testMethod": "Verify DES has no persistent state between invocations except via explicit StateAdapter"
    },
    "taint-level": {
      "definition": "A classification indicating the epistemic status of a claim or inference. DES uses a three-level system.",
      "levels": {
        "L1": {
          "name": "Verified",
          "description": "Claim has been verified against authoritative source or formal proof",
          "desCanProduce": false,
          "desCanConsume": true,
          "propagation": "L1 input does not elevate DES output above L2"
        },
        "L2": {
          "name": "Defeasible",
          "description": "Claim is a reasonable default that may be overridden by stronger evidence",
          "desCanProduce": true,
          "desCanConsume": true,
          "propagation": "All DES outputs are L2 regardless of input taint"
        },
        "L3": {
          "name": "Unverified",
          "description": "Claim origin is unknown or untrusted",
          "desCanProduce": false,
          "desCanConsume": true,
          "propagation": "L3 input may downgrade DES output confidence but not taint level"
        }
      },
      "invariant": "∀ DES output O: O.taintLevel = 'L2'",
      "machineCheckable": true,
      "testMethod": "Assert all AppliedDefault and AnomalyDetected objects have taintLevel === 'L2'"
    },
    "evaluation-context": {
      "definition": "Metadata attached to DES outputs that provides additional epistemic nuance without fragmenting the taint taxonomy. Contains confidence modifiers and flags.",
      "invariant": "evaluationContext is metadata only; it never changes taintLevel",
      "machineCheckable": true,
      "testMethod": "Verify taintLevel field is independent of evaluationContext values"
    },
    "observation-snapshot": {
      "definition": "A point-in-time record of a DES evaluation, including input claim, rules considered, rules applied, anomalies detected, and all version identifiers needed for audit replay.",
      "invariant": "Snapshot contains sufficient information to reproduce the evaluation given the same rule database version",
      "machineCheckable": true,
      "testMethod": "Replay evaluation with snapshotted inputs and verify identical outputs"
    },
    "epistemic-state": {
      "definition": "Classification of how a justification was satisfied during evaluation.",
      "states": {
        "confirmed": "Explicit positive evidence supports the justification",
        "consistent-by-absence": "No contradicting evidence found; assumption rests on lack of counter-evidence",
        "contradicted": "Explicit evidence contradicts the justification"
      },
      "invariant": "Every justification result has exactly one epistemic state",
      "machineCheckable": true
    },
    "specificity-rank": {
      "definition": "A numeric value (1-1000) that determines rule priority when multiple rules compete to assert the same property. Higher rank wins.",
      "invariant": "Conflict resolution is deterministic: highest rank wins, then recency, then anomaly flag",
      "machineCheckable": true,
      "testMethod": "Given rules with known ranks, verify winner selection matches specification"
    },
    "compaction": {
      "definition": "The process of aggregating detailed observation logs into summary statistics to manage storage constraints while preserving audit-relevant information.",
      "invariant": "Compaction preserves aggregate counts; individual observations may be lost after retention period",
      "machineCheckable": true,
      "testMethod": "Verify post-compaction aggregates match pre-compaction counts"
    }
  }
}
```

### 2.2 Allowed vs Prohibited Patterns

```json
{
  "@type": "des:PatternExamples",
  "allowed": [
    {
      "name": "Independent rules on same claim",
      "description": "Multiple rules fire on different properties of the same input",
      "example": {
        "input": { "role": "employee", "department": "engineering" },
        "ruleA": { "prerequisite": { "role": "employee" }, "consequent": { "hasEmail": true } },
        "ruleB": { "prerequisite": { "department": "engineering" }, "consequent": { "hasGitAccess": true } },
        "result": "Both rules fire independently"
      }
    },
    {
      "name": "External chaining via MDRE",
      "description": "MDRE enriches claim and re-invokes DES",
      "example": {
        "invocation1": {
          "input": { "role": "employee" },
          "desOutput": { "hasAccessBadge": true }
        },
        "mdreEnrichment": "Adds hasAccessBadge to claim",
        "invocation2": {
          "input": { "role": "employee", "hasAccessBadge": true },
          "desOutput": { "canEnterBuilding": true }
        },
        "result": "Chaining achieved through orchestration, not internal DES state"
      }
    },
    {
      "name": "External evidence lookup",
      "description": "Rule prerequisite references property that comes from external system (not another DES rule)",
      "example": {
        "input": { "userId": "123", "accountStatus": "active" },
        "note": "accountStatus came from external identity system, not DES inference",
        "result": "Allowed because property is in INPUT, not inferred by DES"
      }
    }
  ],
  "prohibited": [
    {
      "name": "Internal chaining",
      "description": "Rule B depends on Rule A's output within same evaluation",
      "example": {
        "input": { "role": "employee" },
        "ruleA": { "prerequisite": { "role": "employee" }, "consequent": { "hasAccessBadge": true } },
        "ruleB": { "prerequisite": { "hasAccessBadge": true }, "consequent": { "canEnterBuilding": true } },
        "result": "Rule B does NOT fire because hasAccessBadge is not in INPUT"
      },
      "enforcement": "Design-time warning + runtime skip"
    },
    {
      "name": "Circular dependency",
      "description": "Rule A depends on Rule B which depends on Rule A",
      "example": {
        "ruleA": { "prerequisite": { "canEnterBuilding": true }, "consequent": { "hasAccessBadge": true } },
        "ruleB": { "prerequisite": { "hasAccessBadge": true }, "consequent": { "canEnterBuilding": true } }
      },
      "enforcement": "Design-time rejection; neither rule can fire on typical input"
    },
    {
      "name": "Taint elevation",
      "description": "Attempting to produce L1 output from DES",
      "enforcement": "Impossible by design; all outputs hardcoded to L2"
    }
  ]
}
```

---

## 3. Operational Semantics

This section provides a formal step model for DES evaluation, enabling implementers to build conformant engines.

### 3.1 Evaluation Step Model

```json
{
  "@type": "des:OperationalSemantics",
  "@id": "urn:des:semantics:v2",
  "model": "single-pass-functional",
  "description": "DES evaluation is a pure function from (Claim, RuleDatabase, ExceptionRegistry) to (Results). No hidden state mutation occurs.",
  "steps": [
    {
      "step": 1,
      "name": "Input Validation",
      "action": "Validate input claim conforms to fnsr.claim.extracted schema",
      "stateAccess": "read-only: input claim",
      "output": "ValidatedClaim | ValidationError",
      "maxDuration": "10ms"
    },
    {
      "step": 2,
      "name": "Property Extraction",
      "action": "Extract all properties present in input claim into PropertySet",
      "stateAccess": "read-only: validated claim",
      "output": "PropertySet (frozen, immutable for remainder of evaluation)",
      "invariant": "PropertySet is never modified after this step",
      "maxDuration": "5ms"
    },
    {
      "step": 3,
      "name": "Rule Matching",
      "action": "Find all rules whose prerequisites are satisfied by PropertySet",
      "stateAccess": "read-only: PropertySet, RuleDatabase",
      "output": "MatchedRules[]",
      "invariant": "∀ rule in MatchedRules: rule.prerequisite.properties ⊆ PropertySet",
      "maxDuration": "50ms for up to 1000 rules"
    },
    {
      "step": 4,
      "name": "Chaining Validation",
      "action": "Verify no matched rule's prerequisite depends on another matched rule's consequent",
      "stateAccess": "read-only: MatchedRules",
      "output": "ChainingWarnings[] (logged but non-blocking)",
      "enforcement": "warn-and-continue",
      "maxDuration": "10ms"
    },
    {
      "step": 5,
      "name": "Conflict Detection",
      "action": "Group rules by consequent property; identify competing rules",
      "stateAccess": "read-only: MatchedRules",
      "output": "ConflictGroups[]",
      "maxDuration": "10ms"
    },
    {
      "step": 6,
      "name": "Conflict Resolution",
      "action": "For each ConflictGroup, select winner by specificity-then-recency",
      "stateAccess": "read-only: ConflictGroups",
      "output": "ResolvedRules[], ConflictResolutions[]",
      "invariant": "Deterministic: same inputs always produce same winner",
      "maxDuration": "10ms"
    },
    {
      "step": 7,
      "name": "Justification Evaluation",
      "action": "For each ResolvedRule, evaluate justifications against PropertySet",
      "stateAccess": "read-only: ResolvedRules, PropertySet",
      "output": "JustificationResults[] with epistemic states",
      "invariant": "Justification checks only reference PropertySet, never inferred properties",
      "maxDuration": "100ms for up to 100 rules"
    },
    {
      "step": 8,
      "name": "Default Application",
      "action": "For rules with consistent justifications, create AppliedDefault records",
      "stateAccess": "read-only: JustificationResults",
      "output": "AppliedDefaults[]",
      "invariant": "∀ output: output.taintLevel = 'L2'",
      "maxDuration": "20ms"
    },
    {
      "step": 9,
      "name": "Anomaly Detection",
      "action": "For rules with inconsistent justifications, create AnomalyDetected records",
      "stateAccess": "read-only: JustificationResults, ExceptionRegistry",
      "output": "Anomalies[] (after exception filtering)",
      "invariant": "∀ anomaly: anomaly.taintLevel = 'L2'",
      "maxDuration": "20ms"
    },
    {
      "step": 10,
      "name": "Observation Logging",
      "action": "Record evaluation to observation log (async, non-blocking)",
      "stateAccess": "write: ObservationLog via StateAdapter",
      "output": "void (fire-and-forget with retry)",
      "maxDuration": "5ms (async dispatch only)"
    },
    {
      "step": 11,
      "name": "Result Assembly",
      "action": "Assemble final result object",
      "stateAccess": "read-only: all prior outputs",
      "output": "EvaluationResult",
      "maxDuration": "5ms"
    }
  ],
  "totalMaxDuration": {
    "standardPath": "250ms",
    "fullPath": "500ms",
    "fastPath": "5ms (bypass)"
  },
  "stateIsolation": {
    "betweenEvaluations": "No shared mutable state; each evaluation is independent",
    "withinEvaluation": "PropertySet frozen after step 2; no mutation thereafter",
    "persistence": "Only via explicit StateAdapter calls in step 10"
  }
}
```

### 3.2 Formal Invariants

These invariants MUST hold for any conformant implementation:

```json
{
  "@type": "des:FormalInvariants",
  "invariants": [
    {
      "id": "INV-001",
      "name": "Single-Pass Property Isolation",
      "statement": "The set of properties available for prerequisite matching is fixed at evaluation start and never includes properties inferred during the same evaluation",
      "formal": "∀ evaluation E, ∀ step S in E where S.index > 2: S.availableProperties = E.steps[2].output",
      "testMethod": "Inject rule that would fire only if chaining occurred; verify it does not fire"
    },
    {
      "id": "INV-002",
      "name": "Taint Level Immutability",
      "statement": "All DES outputs have taintLevel 'L2' regardless of input taint levels or evaluation path",
      "formal": "∀ output O produced by DES: O.taintLevel = 'L2'",
      "testMethod": "Feed L1, L2, L3 inputs; verify all outputs are L2"
    },
    {
      "id": "INV-003",
      "name": "Deterministic Conflict Resolution",
      "statement": "Given identical inputs, conflict resolution always selects the same winner",
      "formal": "∀ inputs I, evaluations E1(I), E2(I): E1.winners = E2.winners",
      "testMethod": "Run same evaluation 100 times; verify identical results"
    },
    {
      "id": "INV-004",
      "name": "Snapshot Reproducibility",
      "statement": "An evaluation can be exactly reproduced given its snapshot and the referenced rule database version",
      "formal": "∀ snapshot S: replay(S, ruleDb[S.ruleDbVersionId]) = S.results",
      "testMethod": "Store snapshot; replay with versioned rules; compare outputs"
    },
    {
      "id": "INV-005",
      "name": "Compaction Aggregate Preservation",
      "statement": "Compaction preserves aggregate counts even as individual records are purged",
      "formal": "∀ compaction C: sum(C.pre.counts) = sum(C.post.aggregates)",
      "testMethod": "Compact observation log; verify aggregate totals match"
    },
    {
      "id": "INV-006",
      "name": "Exception Suppression Auditability",
      "statement": "Every suppressed anomaly is traceable to a specific exception with documented reason",
      "formal": "∀ suppressed anomaly A: ∃ exception E: E.matches(A) ∧ E.documentedReason ≠ null",
      "testMethod": "Suppress anomaly via exception; verify audit trail contains exception reference"
    }
  ]
}
```

### 3.3 Enforcement Policy

```json
{
  "@type": "des:EnforcementPolicy",
  "chainingViolation": {
    "detectionPhase": "step 4 (Chaining Validation)",
    "runtimeBehavior": {
      "action": "warn-and-skip",
      "description": "Log warning, skip the dependent rule, continue evaluation",
      "rationale": "Fail-safe: system continues operating; violation is visible in logs"
    },
    "alternatives": {
      "fail-fast": {
        "description": "Reject entire evaluation if chaining detected",
        "whenToUse": "High-security contexts where partial results are unacceptable",
        "configuration": "des.enforcement.chainingViolation = 'fail-fast'"
      },
      "mark-inconsistent": {
        "description": "Complete evaluation but mark all outputs as potentially inconsistent",
        "whenToUse": "Audit/investigation contexts",
        "configuration": "des.enforcement.chainingViolation = 'mark-inconsistent'"
      }
    },
    "logging": {
      "level": "WARN",
      "destination": "audit-log + metrics",
      "retention": "P5Y (same as rule retention)",
      "fields": ["timestamp", "evaluationId", "violatingRuleId", "dependsOnRuleId", "dependsOnProperty"]
    },
    "alerting": {
      "threshold": "10 violations per hour",
      "action": "Page on-call + auto-disable violating rule for review"
    }
  },
  "designTimeValidation": {
    "chainingIndependenceVerification": {
      "when": "Rule proposal submission (§5.2)",
      "method": "Static analysis of prerequisite/consequent overlap with existing rules",
      "ciIntegration": {
        "command": "des-lint --check-chaining rules/*.json",
        "failBuild": true,
        "bypassRequires": "Explicit waiver with documented justification"
      }
    }
  }
}
```

---

## 4. Theoretical Foundation

### 4.1 Defeasible Logic Formalism

DES implements a pragmatic subset of Reiter's Default Logic, adapted for JSON-LD representation and edge-canonical execution.

#### 4.1.1 Default Rule Structure

A default rule has the form:

```
prerequisite : justification₁, justification₂, ... , justificationₙ
─────────────────────────────────────────────────────────────────────
                          consequent
```

Read as: "If the prerequisite is believed, and it is consistent to believe each justification, then conclude the consequent."

In JSON-LD representation:

```json
{
  "@context": "https://fnsr.dev/ns/des/v2",
  "@type": "DefaultRule",
  "@id": "urn:des:rule:business-hours-assumption",
  "prerequisite": {
    "@type": "Pattern",
    "matches": {
      "eventType": "Meeting",
      "scheduledTime": { "@exists": true }
    }
  },
  "justifications": [
    {
      "@type": "ConsistencyCheck",
      "@id": "urn:des:justification:business-hours-check",
      "canAssume": {
        "timeOfDay": { "between": ["09:00", "17:00"] }
      }
    }
  ],
  "consequent": {
    "@type": "DefaultInference",
    "assert": {
      "duringBusinessHours": true
    },
    "confidence": 0.85,
    "defeasibleBy": ["explicit-time-statement", "timezone-evidence"]
  },
  "specificity": {
    "rank": 100,
    "inheritedFrom": null,
    "scope": ["Meeting"]
  },
  "domainImpact": {
    "domain": "scheduling",
    "criticality": 0.3,
    "stakeholderClasses": ["operations"]
  },
  "metadata": {
    "domain": "scheduling",
    "source": "organizational-norms",
    "addedBy": "urn:agent:domain-expert-alice",
    "addedAt": "2024-11-15T10:30:00Z",
    "activatedAt": "2024-11-16T00:00:00Z",
    "observationCount": 4521,
    "overrideCount": 127
  }
}
```

#### 4.1.2 Closed-World vs Open-World Reasoning

DES operates in a **locally closed world**: within a defined domain, absence of information triggers default assumptions. Across domain boundaries, DES explicitly marks uncertainty rather than assuming.

```json
{
  "@type": "DomainBoundary",
  "@id": "urn:des:domain:hr-policies",
  "closedWorldScope": [
    "employmentStatus",
    "departmentMembership", 
    "standardBenefits"
  ],
  "openWorldScope": [
    "specialAccommodations",
    "externalCertifications"
  ]
}
```

#### 4.1.3 Epistemic State Classification

DES explicitly distinguishes between three epistemic states when evaluating justifications:

```json
{
  "@type": "des:EpistemicStateClassification",
  "states": {
    "confirmed": {
      "description": "Explicit evidence supports the justification",
      "evidenceBasis": "positive",
      "confidenceModifier": 1.0
    },
    "consistent-by-absence": {
      "description": "No contradicting evidence found; assumption rests on lack of counter-evidence",
      "evidenceBasis": "negative",
      "confidenceModifier": 0.8,
      "requiresFlag": true
    },
    "contradicted": {
      "description": "Explicit evidence contradicts the justification",
      "evidenceBasis": "positive-negative",
      "confidenceModifier": 0.0,
      "triggersAnomaly": true
    }
  }
}
```

### 4.2 The Expectation Lifecycle

```
  ┌─────────────┐
  │  Dormant    │  Rule exists but prerequisite not matched
  └──────┬──────┘
         │ prerequisite matched
         ▼
  ┌─────────────┐
  │  Candidate  │  Checking justification consistency
  └──────┬──────┘
         │ justifications consistent
         ▼
  ┌─────────────┐
  │  Applied    │  Consequent asserted as L2 belief
  └──────┬──────┘
         │ contradicting evidence arrives
         ▼
  ┌─────────────┐
  │  Defeated   │  Consequent retracted, anomaly logged
  └─────────────┘
```

---

## 5. Rule Governance

### 5.1 Rule Lifecycle

Default rules are not code — they are **auditable institutional knowledge** with explicit provenance and governance.

```json
{
  "@type": "des:RuleGovernance",
  "roles": {
    "ruleProposer": {
      "description": "May submit new rules for review",
      "requires": ["domain-expertise-certification"]
    },
    "ruleApprover": {
      "description": "May approve rules for production use",
      "requires": ["governance-authority", "domain-expertise-certification"]
    },
    "ruleAuditor": {
      "description": "May review rule performance and recommend changes",
      "requires": ["audit-authority"]
    }
  },
  "workflow": {
    "proposed": {
      "nextStates": ["under-review", "rejected"],
      "requiredApprovals": 0
    },
    "under-review": {
      "nextStates": ["approved", "rejected", "needs-revision"],
      "requiredApprovals": 1,
      "approverRole": "ruleApprover",
      "requiredChecks": ["chaining-independence-verification", "conflict-analysis"]
    },
    "approved": {
      "nextStates": ["active", "suspended"],
      "activationRequires": ["test-coverage", "domain-boundary-assignment", "specificity-rank-assignment"]
    },
    "active": {
      "nextStates": ["suspended", "deprecated"],
      "monitoring": ["observation-log", "anomaly-rate", "override-rate"]
    },
    "suspended": {
      "nextStates": ["active", "deprecated"],
      "reason": "required"
    },
    "deprecated": {
      "nextStates": [],
      "retention": "P5Y"
    }
  }
}
```

### 5.2 Rule Addition Protocol

```json
{
  "@type": "des:RuleProposal",
  "@id": "urn:des:proposal:prop789",
  "proposedRule": {
    "@type": "DefaultRule",
    "prerequisite": { "matches": { "eventType": "Meeting", "participantRole": "executive" } },
    "justifications": [{ "@type": "ConsistencyCheck", "canAssume": { "expectedDuration": "PT15M" } }],
    "consequent": { "assert": { "expectedDuration": "PT15M" } },
    "specificity": {
      "rank": null,
      "proposedRank": 350,
      "rankJustification": "More specific than base meeting rule (100) due to executive constraint"
    }
  },
  "proposer": "urn:agent:domain-expert-bob",
  "proposedAt": "2024-11-18T09:00:00Z",
  "justification": {
    "businessNeed": "Executive meetings are typically shorter; reduce manual corrections",
    "evidenceBase": {
      "observationSample": 500,
      "successRate": 0.94,
      "samplePeriod": "P90D"
    },
    "riskAssessment": {
      "falsePositiveImpact": "low",
      "falseNegativeImpact": "medium",
      "mitigations": ["human-review-queue for low-confidence matches"]
    }
  },
  "chainingIndependenceVerification": {
    "status": "passed",
    "checkedAgainst": ["urn:des:ruledb:primary:v2024-11-18"],
    "potentialChains": [],
    "verifiedBy": "des-lint v2.0.0",
    "verifiedAt": "2024-11-18T09:05:00Z"
  },
  "conflictAnalysis": {
    "potentialConflicts": [
      {
        "withRule": "urn:des:rule:meeting-duration-default",
        "conflictType": "consequent-overlap",
        "resolution": "specificity-rank (this rule more specific: 350 > 100)"
      }
    ]
  },
  "testCases": [
    {
      "id": "executive-meeting-basic",
      "input": {
        "claims": [
          { "predicate": "eventType", "object": "Meeting" },
          { "predicate": "participantRole", "object": "executive" }
        ]
      },
      "expectedOutput": {
        "appliedDefaults": [{ "property": "expectedDuration", "value": "PT15M" }]
      }
    }
  ]
}
```

### 5.3 Modification Constraints

Rules in `active` state may only be modified through:

1. **Parameter tuning**: Adjusting confidence thresholds within approved bounds
2. **Exception addition**: Adding new entries to `defeasibleBy` list
3. **Suspension**: Temporarily disabling with documented reason
4. **Deprecation**: Marking for removal with migration path

Structural changes (prerequisite, justification, or consequent modification) require a new rule proposal.

---

## 6. Core Data Structures

### 6.1 Default Rule Database Schema

```json
{
  "@context": {
    "des": "https://fnsr.dev/ns/des/v2#",
    "bfo": "http://purl.obolibrary.org/obo/",
    "cco": "http://www.ontologyrepository.com/CommonCoreOntologies/",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
  },
  "@type": "des:RuleDatabase",
  "@id": "urn:des:ruledb:primary",
  "version": "2.0.0",
  "versionId": "urn:des:ruledb:primary:v2024-11-22-001",
  "rules": [],
  "domainBoundaries": [],
  "exceptionRegistry": {
    "@id": "urn:des:exceptions:primary",
    "versionId": "urn:des:exceptions:primary:v2024-11-22-001"
  },
  "observationLog": {
    "@type": "des:ObservationLog",
    "storageAdapter": "pluggable",
    "compactionPolicy": "urn:des:policy:compaction:default"
  }
}
```

### 6.2 Applied Default Record

```json
{
  "@context": "https://fnsr.dev/ns/des/v2",
  "@type": "AppliedDefault",
  "@id": "urn:des:applied:abc123",
  "timestamp": "2024-11-22T14:32:01.123Z",
  "triggeringClaim": "urn:tagteam:claim:xyz789",
  "ruleApplied": "urn:des:rule:business-hours-assumption",
  "taintLevel": "L2",
  "inferredAssertions": [
    {
      "property": "duringBusinessHours",
      "value": true,
      "taintLevel": "L2",
      "defeasibleBy": ["explicit-time-statement", "timezone-evidence"]
    }
  ],
  "justificationSnapshot": {
    "checkedAt": "2024-11-22T14:32:01.123Z",
    "ruleDbVersionId": "urn:des:ruledb:primary:v2024-11-22-001",
    "exceptionRegistryVersionId": "urn:des:exceptions:primary:v2024-11-22-001",
    "consistentWith": ["urn:tagteam:claim:xyz789"],
    "noContradictionFrom": ["explicit-time-statement", "timezone-evidence"],
    "justificationResults": [
      {
        "justificationId": "urn:des:justification:business-hours-check",
        "epistemicState": "consistent-by-absence",
        "evidenceBasis": "negative"
      }
    ]
  },
  "evaluationContext": {
    "hasAbsenceBasedJustification": true,
    "confidenceModifier": 0.8
  },
  "metadata": {
    "processingPath": "standard",
    "cacheHit": true,
    "evaluationDurationMs": 3,
    "specificityRankUsed": 100
  }
}
```

### 6.3 Anomaly Record

```json
{
  "@context": "https://fnsr.dev/ns/des/v2",
  "@type": "AnomalyDetected",
  "@id": "urn:des:anomaly:def456",
  "timestamp": "2024-11-22T14:35:22.456Z",
  "anomalyType": "expectation-violation",
  "taintLevel": "L2",
  "severity": {
    "raw": 0.6,
    "domainImpact": 0.3,
    "effectiveSeverity": 0.18,
    "effectiveCategory": "low"
  },
  "violatedExpectation": {
    "rule": "urn:des:rule:business-hours-assumption",
    "expectedValue": { "duringBusinessHours": true },
    "observedValue": { "scheduledTime": "02:30" }
  },
  "triggeringEvidence": [
    "urn:tagteam:claim:explicit-time-002"
  ],
  "defeatedDefaults": [
    "urn:des:applied:abc123"
  ],
  "recommendedActions": [
    {
      "@type": "ReviewRecommendation",
      "action": "human-review",
      "reason": "Unusual meeting time may indicate error or special circumstance",
      "priority": "normal"
    }
  ],
  "snapshotVersions": {
    "ruleDbVersionId": "urn:des:ruledb:primary:v2024-11-22-001",
    "exceptionRegistryVersionId": "urn:des:exceptions:primary:v2024-11-22-001"
  },
  "metadata": {
    "isBlocking": false,
    "routeTo": ["urn:agent:scheduler-review-queue"],
    "historicalFrequency": {
      "similarAnomalies": 23,
      "timeWindow": "P30D",
      "falsePositiveRate": 0.12
    }
  }
}
```

### 6.4 Audit Trace Record

```json
{
  "@context": "https://fnsr.dev/ns/des/v2",
  "@type": "des:AuditTrace",
  "@id": "urn:des:trace:eval-20241122-143201-abc",
  "schema_version": "2.0.0",
  "timestamp": "2024-11-22T14:32:01.123Z",
  "evaluationId": "eval-20241122-143201-abc",
  "input": {
    "claimId": "urn:tagteam:claim:xyz789",
    "claimHash": "sha256:a1b2c3...",
    "queryPath": "standard",
    "inputPropertiesCount": 5,
    "inputProperties": ["eventType", "scheduledTime", "organizer", "location", "subject"]
  },
  "ruleProcessing": {
    "rulesInDatabase": 150,
    "rulesMatched": 3,
    "rulesMatchedIds": ["urn:des:rule:r1", "urn:des:rule:r2", "urn:des:rule:r3"],
    "rulesApplied": 2,
    "rulesAppliedIds": ["urn:des:rule:r1", "urn:des:rule:r2"],
    "rulesSkippedDueToConflict": 1,
    "rulesSkippedIds": ["urn:des:rule:r3"]
  },
  "chainingValidation": {
    "potentialChainsDetected": 0,
    "chainingWarnings": []
  },
  "conflictResolution": {
    "conflictsDetected": 1,
    "resolutions": [
      {
        "property": "expectedDuration",
        "competingRules": ["urn:des:rule:r1", "urn:des:rule:r3"],
        "winner": "urn:des:rule:r1",
        "method": "specificity-rank",
        "winnerRank": 350,
        "loserRank": 100
      }
    ]
  },
  "epistemicStates": {
    "urn:des:rule:r1": "confirmed",
    "urn:des:rule:r2": "consistent-by-absence"
  },
  "outputs": {
    "appliedDefaultsCount": 2,
    "appliedDefaultIds": ["urn:des:applied:abc123", "urn:des:applied:abc124"],
    "anomaliesDetectedCount": 0,
    "anomalyIds": []
  },
  "exceptionsMatched": [],
  "performance": {
    "totalDurationMs": 12,
    "stepDurations": {
      "inputValidation": 1,
      "propertyExtraction": 1,
      "ruleMatching": 4,
      "chainingValidation": 1,
      "conflictResolution": 2,
      "justificationEvaluation": 2,
      "outputAssembly": 1
    },
    "cacheStatus": "hit"
  },
  "versions": {
    "desVersion": "2.0.0",
    "ruleDbVersionId": "urn:des:ruledb:primary:v2024-11-22-001",
    "exceptionRegistryVersionId": "urn:des:exceptions:primary:v2024-11-22-001"
  },
  "provenance": {
    "inputSource": "urn:tagteam:source:email-parser",
    "evaluationHost": "browser",
    "sessionId": "session-xyz"
  }
}
```

### 6.5 Observation Log Compaction Policy

```json
{
  "@type": "des:CompactionPolicy",
  "@id": "urn:des:policy:compaction:default",
  "description": "Prevents observation log from exceeding edge storage limits while preserving audit-relevant aggregates",
  "tiers": [
    {
      "tier": "hot",
      "retention": "P7D",
      "granularity": "individual-observations",
      "maxSize": "50MB",
      "storage": "primary",
      "piiHandling": "retain-with-access-control"
    },
    {
      "tier": "warm",
      "retention": "P90D",
      "granularity": "hourly-aggregates",
      "aggregationMethod": "frequency-counts-by-rule-and-outcome",
      "maxSize": "10MB",
      "storage": "primary",
      "piiHandling": "redact-before-aggregation"
    },
    {
      "tier": "cold",
      "retention": "P365D",
      "granularity": "daily-aggregates",
      "aggregationMethod": "frequency-counts-by-domain",
      "maxSize": "2MB",
      "storage": "primary",
      "piiHandling": "fully-anonymized"
    },
    {
      "tier": "archive",
      "retention": "P5Y",
      "granularity": "monthly-summaries",
      "storage": "optional-external",
      "offloadTrigger": "storage-adapter-supports-archive",
      "piiHandling": "fully-anonymized",
      "encryption": "required"
    }
  ],
  "compactionSchedule": {
    "trigger": "on-write-if-exceeded OR daily",
    "maxCompactionDuration": "5000ms"
  },
  "edgeConstraints": {
    "localStorageLimit": "5MB",
    "indexedDBLimit": "50MB",
    "gracefulDegradation": {
      "ifLimitApproached": "compact-aggressively",
      "ifLimitExceeded": "drop-oldest-hot-tier"
    }
  },
  "piiPolicy": {
    "identificationMethod": "field-tagging",
    "piiFields": ["userName", "email", "ipAddress", "deviceId"],
    "redactionMethod": "sha256-hash-with-salt",
    "saltRotation": "P30D"
  },
  "encryption": {
    "atRest": {
      "browser": "Web Crypto API (AES-GCM-256)",
      "node": "crypto.createCipheriv (AES-256-GCM)"
    },
    "keyManagement": {
      "derivation": "PBKDF2 from user-provided passphrase or system key",
      "rotation": "P90D recommended"
    }
  }
}
```

---

## 7. Anomaly Detection Model

### 7.1 Anomaly Types

```json
{
  "@type": "des:AnomalyTaxonomy",
  "types": {
    "expectation-violation": {
      "description": "Observed fact contradicts applied default",
      "baseSeverity": "variable",
      "example": "Meeting scheduled at 3 AM violates business-hours assumption"
    },
    "pattern-deviation": {
      "description": "Entity behavior deviates from established pattern",
      "baseSeverity": "variable", 
      "example": "User who always books conference rooms now booking none"
    },
    "frequency-anomaly": {
      "description": "Event frequency outside normal bounds",
      "baseSeverity": "variable",
      "example": "50 expense reports from one employee in one day"
    },
    "consistency-failure": {
      "description": "Multiple defaults cannot be consistently applied",
      "baseSeverity": "high",
      "example": "Entity classified as both 'active employee' and 'terminated'"
    },
    "novel-pattern": {
      "description": "Pattern not matching any known default",
      "baseSeverity": "low",
      "example": "New meeting type not in organizational taxonomy"
    }
  }
}
```

### 7.2 Severity Calculation with Domain Impact

```json
{
  "@type": "des:ThresholdConfiguration",
  "@id": "urn:des:config:thresholds:default",
  "severityCalculation": {
    "formula": "effectiveSeverity = rawSeverity × domainImpact.criticality",
    "components": {
      "rawSeverity": {
        "description": "Statistical anomaly score (0.0-1.0)",
        "factors": [
          { "name": "ruleConfidence", "weight": 0.3 },
          { "name": "evidenceStrength", "weight": 0.4 },
          { "name": "statisticalDeviation", "weight": 0.3 }
        ]
      },
      "domainImpact": {
        "description": "Business importance multiplier from rule definition",
        "source": "rule.domainImpact.criticality",
        "range": [0.1, 1.0],
        "default": 0.5
      }
    }
  },
  "domainImpactRegistry": {
    "@type": "des:DomainImpactRegistry",
    "domains": {
      "identity-verification": {
        "criticality": 1.0,
        "stakeholderClasses": ["security", "compliance", "legal"],
        "escalationPath": "immediate"
      },
      "financial-transactions": {
        "criticality": 0.9,
        "stakeholderClasses": ["finance", "compliance", "audit"],
        "escalationPath": "same-day"
      },
      "access-control": {
        "criticality": 0.85,
        "stakeholderClasses": ["security", "it-ops"],
        "escalationPath": "same-day"
      },
      "scheduling": {
        "criticality": 0.3,
        "stakeholderClasses": ["operations"],
        "escalationPath": "weekly-review"
      },
      "content-metadata": {
        "criticality": 0.2,
        "stakeholderClasses": ["content-ops"],
        "escalationPath": "batch-review"
      }
    }
  },
  "effectiveSeverityThresholds": {
    "low": { "below": 0.2 },
    "moderate": { "between": [0.2, 0.5] },
    "high": { "above": 0.5 }
  }
}
```

---

## 8. Metrics, SLAs, and Tuning

### 8.1 Metric Definitions

```json
{
  "@type": "des:MetricsDefinition",
  "performanceMetrics": {
    "throughput": {
      "definition": "Number of claims processed per second",
      "unit": "claims/sec",
      "measurement": "count(evaluations) / time_window",
      "targets": {
        "browser": "> 10 claims/sec",
        "node": "> 100 claims/sec"
      }
    },
    "latency": {
      "definition": "Time from evaluation start to result assembly",
      "unit": "milliseconds",
      "measurement": "p50, p95, p99 of evaluation duration",
      "targets": {
        "fastPath": { "p95": "< 5ms" },
        "standardPath": { "p95": "< 50ms" },
        "fullPath": { "p95": "< 500ms" }
      }
    },
    "memoryUsage": {
      "definition": "Peak memory during evaluation",
      "unit": "megabytes",
      "measurement": "max(heap_used) during evaluation",
      "targets": {
        "browser": "< 50MB per evaluation",
        "node": "< 200MB per evaluation"
      }
    }
  },
  "accuracyMetrics": {
    "falsePositiveRate": {
      "definition": "Fraction of anomalies detected that were not true anomalies",
      "formula": "FP / (FP + TN)",
      "measurementMethod": "Sample 100 anomalies weekly; human review for ground truth",
      "targets": {
        "production": "< 0.05 (5%)",
        "staging": "< 0.10 (10%)"
      }
    },
    "falseNegativeRate": {
      "definition": "Fraction of true anomalies that were not detected",
      "formula": "FN / (FN + TP)",
      "measurementMethod": "Inject known anomalies; measure detection rate",
      "targets": {
        "production": "< 0.02 (2%)",
        "staging": "< 0.05 (5%)"
      }
    },
    "defaultAccuracy": {
      "definition": "Fraction of applied defaults that were not later overridden",
      "formula": "1 - (overrideCount / appliedCount)",
      "measurementMethod": "Track override events in observation log",
      "targets": {
        "perRule": "> 0.90 (90%)",
        "overall": "> 0.95 (95%)"
      }
    }
  },
  "operationalMetrics": {
    "chainingViolations": {
      "definition": "Number of chaining attempts detected",
      "alertThreshold": "> 10/hour",
      "action": "Page on-call; review rule set"
    },
    "staleExceptions": {
      "definition": "Exceptions not used in P180D",
      "reviewCadence": "weekly",
      "action": "Flag for deletion review"
    },
    "ruleVersionDrift": {
      "definition": "Number of active evaluations using outdated rule versions",
      "alertThreshold": "> 5% of evaluations",
      "action": "Prompt rule sync"
    }
  }
}
```

### 8.2 Tuning Procedure

```json
{
  "@type": "des:TuningProcedure",
  "prerequisites": {
    "labeledDataset": {
      "minimumSize": 10000,
      "composition": {
        "trueAnomalies": "≥ 500 (5%)",
        "trueNegatives": "≥ 9000 (90%)",
        "edgeCases": "≥ 500 (5%)"
      },
      "labelingMethod": "Human expert review with inter-rater reliability > 0.8"
    },
    "evaluationWindow": "P30D of production-like traffic"
  },
  "procedure": [
    {
      "step": 1,
      "action": "Establish baseline metrics with current thresholds",
      "output": "baseline_metrics.json"
    },
    {
      "step": 2,
      "action": "Generate ROC curves for each anomaly type",
      "tool": "des-metrics --roc --by-type",
      "output": "roc_curves/"
    },
    {
      "step": 3,
      "action": "Calculate optimal thresholds maximizing F1 with business weights",
      "formula": "F1_weighted = 2 * (precision * recall) / (precision + recall) where FP_cost = 1, FN_cost = 5",
      "output": "optimal_thresholds.json"
    },
    {
      "step": 4,
      "action": "Validate on held-out test set (20% of labeled data)",
      "acceptanceCriteria": "FP < 5%, FN < 2%"
    },
    {
      "step": 5,
      "action": "Deploy to staging with shadow mode (log but don't act)",
      "duration": "P7D"
    },
    {
      "step": 6,
      "action": "Compare staging metrics to baseline; proceed if within 10% of targets"
    },
    {
      "step": 7,
      "action": "Gradual production rollout (10% → 50% → 100%)",
      "rollbackCriteria": "FP or FN > 2x target for > 1 hour"
    }
  ],
  "calibrationCadence": "quarterly or after major rule changes"
}
```

---

## 9. Rule Conflict Resolution

### 9.1 Specificity Rank System

```json
{
  "@type": "des:SpecificitySystem",
  "description": "Deterministic resolution when multiple rules produce contradictory consequents",
  "rankStructure": {
    "range": [1, 1000],
    "convention": {
      "1-99": "Highly general defaults (apply broadly)",
      "100-299": "Domain-level defaults",
      "300-499": "Entity-type-specific defaults",
      "500-699": "Context-specific defaults",
      "700-899": "Exception-like specificity",
      "900-1000": "Near-override specificity (use sparingly)"
    }
  },
  "resolutionAlgorithm": {
    "steps": [
      { "step": 1, "action": "Identify all applicable rules with matching prerequisites" },
      { "step": 2, "action": "Group by consequent property (rules affecting same property compete)" },
      { "step": 3, "action": "Within each group, select rule with highest specificity rank" },
      { "step": 4, "action": "If tie, select rule with most recent activatedAt timestamp" },
      { "step": 5, "action": "If still tied, flag as consistency-failure anomaly; apply neither" }
    ],
    "invariant": "Deterministic: same inputs always produce same winner"
  }
}
```

---

## 10. Exception Registry

### 10.1 Known Exception Structure

```json
{
  "@type": "des:ExceptionRegistry",
  "@id": "urn:des:exceptions:primary",
  "versionId": "urn:des:exceptions:primary:v2024-11-22-001",
  "exceptions": [
    {
      "@type": "des:KnownException",
      "@id": "urn:des:exception:night-shift-meetings",
      "exceptionFor": "urn:des:rule:business-hours-assumption",
      "condition": {
        "entityHasProperty": {
          "property": "workShift",
          "value": "night"
        }
      },
      "effect": "suppress-anomaly",
      "addedBy": "urn:agent:hr-system",
      "addedAt": "2024-06-01T00:00:00Z",
      "validUntil": null,
      "autoDisable": {
        "enabled": true,
        "inactivityThreshold": "P180D",
        "action": "flag-for-deletion"
      },
      "usageTracking": {
        "lastHit": "2024-11-19T08:15:00Z",
        "hitCount": 342,
        "hitCountPeriod": "P90D"
      },
      "documentedReason": "Night shift workers have different standard hours"
    }
  ]
}
```

### 10.2 Exception Governance

```json
{
  "@type": "des:ExceptionGovernance",
  "creationRequires": ["documented-reason", "scope-limitation"],
  "reviewSchedule": "P90D",
  "expirationPolicy": {
    "default": "P365D",
    "maximum": "P5Y",
    "permanentRequires": ["executive-approval"]
  },
  "autoDisablePolicy": {
    "default": {
      "enabled": true,
      "inactivityThreshold": "P180D",
      "action": "flag-for-deletion"
    },
    "actions": {
      "flag-for-deletion": {
        "notifies": ["exception-owner", "domain-admin"],
        "gracePeriod": "P30D"
      },
      "auto-suspend": {
        "requiresApproval": false
      },
      "auto-delete": {
        "requiresApproval": true,
        "approverRole": "ruleApprover"
      }
    }
  }
}
```

---

## 11. Integration Interfaces

### 11.1 Input: fnsr.claim.extracted

```json
{
  "@type": "des:InputContract",
  "eventType": "fnsr.claim.extracted",
  "expectedStructure": {
    "@context": "https://fnsr.dev/ns/tagteam/v1",
    "@type": "ExtractedClaim",
    "@id": "urn:tagteam:claim:*",
    "source": { "@type": "SourceReference" },
    "extractedAt": "xsd:dateTime",
    "claims": [
      {
        "@type": "Claim",
        "subject": "IRI",
        "predicate": "IRI",
        "object": "any",
        "confidence": "number",
        "taintLevel": "string"
      }
    ]
  },
  "processingGuarantee": "at-least-once",
  "ordering": "per-source-ordered"
}
```

### 11.2 Output: fnsr.default.applied

```json
{
  "@type": "des:OutputContract",
  "eventType": "fnsr.default.applied",
  "structure": {
    "@context": "https://fnsr.dev/ns/des/v2",
    "@type": "AppliedDefault",
    "taintLevel": "L2 (always)",
    "evaluationContext": {
      "hasAbsenceBasedJustification": "boolean",
      "confidenceModifier": "number (0.0-1.0)"
    }
  },
  "consumers": ["MDRE", "downstream-reasoners"],
  "taintLevelGuarantee": "Always L2; confidence nuance in evaluationContext only"
}
```

### 11.3 Output: fnsr.anomaly.detected

```json
{
  "@type": "des:OutputContract",
  "eventType": "fnsr.anomaly.detected",
  "structure": {
    "@context": "https://fnsr.dev/ns/des/v2",
    "@type": "AnomalyDetected",
    "taintLevel": "L2 (always)",
    "severity": {
      "raw": "number",
      "domainImpact": "number",
      "effectiveSeverity": "number",
      "effectiveCategory": "string"
    }
  },
  "consumers": ["IEE", "review-queues", "audit-systems"],
  "isBlocking": false
}
```

### 11.4 Interaction with MDRE

```json
{
  "@type": "des:MDREIntegration",
  "protocol": {
    "defaultsAs": "defeasible-premises",
    "overrideSemantics": {
      "L1-defeats-L2": true,
      "later-L2-defeats-earlier-L2": false,
      "specificity-preference": true
    }
  },
  "chainingOrchestration": {
    "description": "MDRE is responsible for multi-step inference chains",
    "workflow": [
      "MDRE receives DES output",
      "MDRE may derive new claims from DES inferences",
      "MDRE may re-invoke DES with enriched claim set",
      "Each DES invocation is independent single-pass"
    ],
    "terminationResponsibility": "MDRE (not DES)"
  }
}
```

---

## 12. Query Path Behavior

### 12.1 Fast Path

```json
{
  "@type": "des:FastPathBehavior",
  "action": "bypass",
  "rationale": "Fast path prioritizes speed; defaults add latency",
  "implications": {
    "noDefaultsApplied": true,
    "noAnomalyDetection": true,
    "downstreamReceives": "raw-claims-only"
  },
  "performance": {
    "targetLatency": "< 5ms",
    "maxMemory": "< 10MB"
  }
}
```

### 12.2 Standard Path

```json
{
  "@type": "des:StandardPathBehavior",
  "action": "cached-defaults",
  "cacheStrategy": {
    "cacheKey": ["rule-id", "prerequisite-hash"],
    "ttl": "PT1H",
    "invalidateOn": ["rule-update", "exception-update"]
  },
  "performance": {
    "targetLatency": "< 50ms (p95)",
    "maxMemory": "< 50MB"
  }
}
```

### 12.3 Full Path

```json
{
  "@type": "des:FullPathBehavior",
  "action": "full-evaluation",
  "evaluationScope": {
    "fullJustificationCheck": true,
    "crossRuleConsistency": true,
    "anomalyDetection": "complete",
    "patternAnalysis": true
  },
  "performance": {
    "targetLatency": "< 500ms (p95)",
    "maxMemory": "< 100MB"
  }
}
```

---

## 13. Implementation Constraints

### 13.1 Runtime Requirements

```json
{
  "@type": "des:RuntimeRequirements",
  "mandatory": {
    "javascript": "ES2020+ (async/await, optional chaining, nullish coalescing)",
    "jsonld": "JSON-LD 1.1 processing (jsonld.js >= 8.0.0)",
    "storage": "any key-value store (Map, localStorage, IndexedDB)"
  },
  "minimumVersions": {
    "node": "18.0.0",
    "browsers": {
      "chrome": "90",
      "firefox": "88",
      "safari": "14",
      "edge": "90"
    }
  },
  "polyfills": {
    "required": [],
    "recommended": ["structuredClone (for older browsers)"]
  }
}
```

### 13.2 Resource Budgets

```json
{
  "@type": "des:ResourceBudgets",
  "browser": {
    "maxHeapPerEvaluation": "50MB",
    "maxCPUTimePerEvaluation": "500ms",
    "maxConcurrentEvaluations": 4,
    "storageQuota": {
      "localStorage": "5MB (use for config only)",
      "indexedDB": "50MB (use for observation log, cache)"
    },
    "recommendations": {
      "heavyCompute": "Offload to Web Worker",
      "largeRuleSets": "Lazy-load rules by domain",
      "backgroundTasks": "Use requestIdleCallback for compaction"
    }
  },
  "node": {
    "maxHeapPerEvaluation": "200MB",
    "maxCPUTimePerEvaluation": "2000ms",
    "maxConcurrentEvaluations": "limited by available cores",
    "recommendations": {
      "heavyCompute": "Use worker_threads",
      "largeRuleSets": "Stream-load from filesystem",
      "backgroundTasks": "setImmediate for compaction"
    }
  }
}
```

### 13.3 Architecture Patterns

```json
{
  "@type": "des:ArchitecturePatterns",
  "patterns": {
    "webWorkerOffload": {
      "description": "Run DES evaluation in Web Worker to avoid blocking main thread",
      "when": "Browser environment with > 100 rules or full-path evaluation",
      "implementation": {
        "mainThread": "Serializes claim, posts to worker",
        "worker": "Runs DES, posts results back",
        "dataTransfer": "Structured clone (claim, results)"
      }
    },
    "indexedDBStorage": {
      "description": "Use IndexedDB for persistent observation log and cache",
      "schema": {
        "stores": [
          { "name": "observations", "keyPath": "id", "indices": ["timestamp", "ruleId"] },
          { "name": "cache", "keyPath": "cacheKey", "indices": ["expiresAt"] },
          { "name": "aggregates", "keyPath": "period", "indices": ["domain"] }
        ]
      }
    },
    "offlineEvaluation": {
      "description": "For P30D parallel evaluation, run in Node/CI and import results",
      "workflow": [
        "Export rules and sample claims from browser",
        "Run des-eval --parallel --duration P30D in CI",
        "Import aggregated results and tuned thresholds back to browser"
      ],
      "note": "P30D evaluation is OPTIONAL; browser mode supports sampled equivalent"
    },
    "encryptionAtRest": {
      "browser": {
        "api": "Web Crypto API",
        "algorithm": "AES-GCM-256",
        "keyStorage": "IndexedDB with extractable: false"
      },
      "node": {
        "api": "crypto module",
        "algorithm": "aes-256-gcm",
        "keyStorage": "Environment variable or key file with restricted permissions"
      }
    }
  }
}
```

---

## 14. Conformance Tests

### 14.1 Mandatory Conformance Tests

```json
{
  "@type": "des:ConformanceTestSuite",
  "version": "2.0.0",
  "tests": [
    {
      "id": "CONF-001",
      "name": "Single-Pass No Chaining",
      "category": "mandatory",
      "description": "Verify that rules cannot chain within a single evaluation",
      "fixture": {
        "input": {
          "@type": "ExtractedClaim",
          "@id": "urn:test:claim:001",
          "claims": [{ "predicate": "role", "object": "employee" }]
        },
        "rules": [
          {
            "@id": "urn:test:rule:badge",
            "prerequisite": { "matches": { "role": "employee" } },
            "consequent": { "assert": { "hasAccessBadge": true } },
            "specificity": { "rank": 100 }
          },
          {
            "@id": "urn:test:rule:entry",
            "prerequisite": { "matches": { "hasAccessBadge": true } },
            "consequent": { "assert": { "canEnterBuilding": true } },
            "specificity": { "rank": 200 }
          }
        ]
      },
      "expectedOutput": {
        "appliedDefaults": [
          { "ruleApplied": "urn:test:rule:badge", "property": "hasAccessBadge", "value": true }
        ],
        "notApplied": ["urn:test:rule:entry"],
        "chainingWarnings": [
          { "dependentRule": "urn:test:rule:entry", "dependsOnProperty": "hasAccessBadge" }
        ]
      },
      "passCondition": "canEnterBuilding NOT in output; chainingWarning logged"
    },
    {
      "id": "CONF-002",
      "name": "Taint Level Immutability",
      "category": "mandatory",
      "description": "Verify all outputs have taintLevel L2 regardless of input",
      "fixtures": [
        { "inputTaint": "L1", "expectedOutputTaint": "L2" },
        { "inputTaint": "L2", "expectedOutputTaint": "L2" },
        { "inputTaint": "L3", "expectedOutputTaint": "L2" }
      ],
      "passCondition": "∀ output: output.taintLevel === 'L2'"
    },
    {
      "id": "CONF-003",
      "name": "Deterministic Conflict Resolution",
      "category": "mandatory",
      "description": "Same inputs produce same winner 100% of the time",
      "fixture": {
        "input": { "claims": [{ "predicate": "eventType", "object": "Meeting" }] },
        "rules": [
          { "@id": "urn:test:rule:r1", "specificity": { "rank": 100 } },
          { "@id": "urn:test:rule:r2", "specificity": { "rank": 200 } }
        ]
      },
      "iterations": 100,
      "passCondition": "winner === 'urn:test:rule:r2' for all 100 iterations"
    },
    {
      "id": "CONF-004",
      "name": "Snapshot Reproducibility",
      "category": "mandatory",
      "description": "Evaluation can be replayed from snapshot",
      "procedure": [
        "Run evaluation; capture snapshot",
        "Replay with snapshotted input and rule version",
        "Compare outputs"
      ],
      "passCondition": "replay.outputs === original.outputs"
    },
    {
      "id": "CONF-005",
      "name": "Compaction Aggregate Preservation",
      "category": "mandatory",
      "description": "Compaction preserves counts",
      "procedure": [
        "Insert 1000 observations",
        "Trigger compaction",
        "Verify sum(pre.counts) === sum(post.aggregates)"
      ],
      "passCondition": "aggregate totals match within 0.1%"
    },
    {
      "id": "CONF-006",
      "name": "Epistemic State Tracking",
      "category": "mandatory",
      "description": "Absence-based justifications are flagged",
      "fixture": {
        "input": { "claims": [{ "predicate": "hasTitle", "object": "Standup" }] },
        "rules": [{
          "@id": "urn:test:rule:hours",
          "justifications": [{ "canAssume": { "duringBusinessHours": true } }]
        }]
      },
      "passCondition": "justificationResults[0].epistemicState === 'consistent-by-absence'"
    }
  ]
}
```

### 14.2 Stress Tests

```json
{
  "@type": "des:StressTestSuite",
  "tests": [
    {
      "id": "STRESS-001",
      "name": "Browser Memory Limit",
      "description": "Evaluate 100 claims concurrently without exceeding memory budget",
      "setup": {
        "rules": 500,
        "claimsPerBatch": 100,
        "claimSize": "1KB average"
      },
      "passCondition": "peakMemory < 50MB; allEvaluationsComplete; noOOM"
    },
    {
      "id": "STRESS-002",
      "name": "High-Volume Conflict Resolution",
      "description": "50 rules competing for same property",
      "setup": {
        "rules": 50,
        "allCompeteFor": "expectedDuration",
        "specificityRanks": "distributed 1-1000"
      },
      "passCondition": "resolution < 100ms; correct winner; deterministic"
    },
    {
      "id": "STRESS-003",
      "name": "PII Redaction",
      "description": "PII is properly redacted during compaction",
      "setup": {
        "observations": 1000,
        "piiFields": ["userName", "email"],
        "triggerCompaction": true
      },
      "passCondition": "no raw PII in warm/cold tiers; hashes present instead"
    },
    {
      "id": "STRESS-004",
      "name": "Storage Limit Graceful Degradation",
      "description": "System continues operating when approaching storage limits",
      "setup": {
        "fillStorageTo": "90%",
        "continuousWrites": true
      },
      "passCondition": "compaction triggered; oldest data purged; no errors"
    }
  ]
}
```

### 14.3 CI Integration

```json
{
  "@type": "des:CIIntegration",
  "commands": {
    "lint": {
      "command": "des-lint --check-chaining --check-conflicts rules/",
      "failBuild": true,
      "when": "on every PR"
    },
    "conformance": {
      "command": "des-test --suite conformance",
      "failBuild": true,
      "when": "on every PR"
    },
    "stress": {
      "command": "des-test --suite stress --memory-limit 100MB",
      "failBuild": true,
      "when": "nightly"
    },
    "tuning": {
      "command": "des-metrics --roc --output reports/",
      "failBuild": false,
      "when": "weekly"
    }
  },
  "artifacts": {
    "testResults": "reports/test-results.json",
    "coverageReport": "reports/coverage.html",
    "rocCurves": "reports/roc/"
  }
}
```

---

## 15. Observability Checklist

```json
{
  "@type": "des:ObservabilityChecklist",
  "mustObserve": [
    {
      "metric": "des.throughput",
      "unit": "evaluations/sec",
      "alertThreshold": "< 5/sec for > 5min"
    },
    {
      "metric": "des.latency.p95",
      "unit": "ms",
      "alertThreshold": "> 500ms for standard path"
    },
    {
      "metric": "des.memory.peak",
      "unit": "MB",
      "alertThreshold": "> 80% of budget"
    },
    {
      "metric": "des.chaining.violations",
      "unit": "count/hour",
      "alertThreshold": "> 10"
    },
    {
      "metric": "des.anomalies.fp_rate",
      "unit": "percentage",
      "alertThreshold": "> 10%"
    },
    {
      "metric": "des.exceptions.stale",
      "unit": "count",
      "reviewCadence": "weekly"
    },
    {
      "metric": "des.rules.version_drift",
      "unit": "percentage of evaluations",
      "alertThreshold": "> 5%"
    },
    {
      "metric": "des.storage.usage",
      "unit": "percentage of quota",
      "alertThreshold": "> 80%"
    }
  ]
}
```

---

## 16. End-to-End Example

### 16.1 Complete Evaluation Walkthrough

```json
{
  "@type": "des:Example",
  "@id": "urn:des:example:e2e-001",
  "title": "Meeting Scheduling Default Application",
  "description": "Demonstrates full evaluation flow from input to trace",
  
  "step1_input": {
    "@context": "https://fnsr.dev/ns/tagteam/v1",
    "@type": "ExtractedClaim",
    "@id": "urn:tagteam:claim:meeting-001",
    "source": { "@type": "SourceReference", "system": "calendar-parser" },
    "extractedAt": "2024-11-22T10:00:00Z",
    "claims": [
      { "subject": "urn:meeting:m001", "predicate": "eventType", "object": "Meeting" },
      { "subject": "urn:meeting:m001", "predicate": "scheduledTime", "object": "14:30" },
      { "subject": "urn:meeting:m001", "predicate": "organizer", "object": "alice@example.com" }
    ]
  },

  "step2_ruleMatching": {
    "inputProperties": ["eventType", "scheduledTime", "organizer"],
    "matchedRules": [
      {
        "@id": "urn:des:rule:business-hours",
        "matchedOn": ["eventType", "scheduledTime"],
        "specificity": 100
      },
      {
        "@id": "urn:des:rule:meeting-duration",
        "matchedOn": ["eventType"],
        "specificity": 100
      }
    ]
  },

  "step3_chainingValidation": {
    "potentialChains": 0,
    "warnings": []
  },

  "step4_conflictResolution": {
    "conflicts": 0,
    "note": "Rules assert different properties; no conflict"
  },

  "step5_justificationEvaluation": {
    "urn:des:rule:business-hours": {
      "justification": "Is scheduledTime between 09:00-17:00?",
      "evidence": "scheduledTime = 14:30",
      "result": "confirmed",
      "epistemicState": "confirmed"
    },
    "urn:des:rule:meeting-duration": {
      "justification": "Can assume expectedDuration = PT1H?",
      "evidence": "No explicit duration in input",
      "result": "consistent",
      "epistemicState": "consistent-by-absence"
    }
  },

  "step6_output": {
    "appliedDefaults": [
      {
        "@type": "AppliedDefault",
        "@id": "urn:des:applied:ad001",
        "taintLevel": "L2",
        "ruleApplied": "urn:des:rule:business-hours",
        "inferredAssertions": [{ "property": "duringBusinessHours", "value": true }],
        "evaluationContext": { "hasAbsenceBasedJustification": false, "confidenceModifier": 1.0 }
      },
      {
        "@type": "AppliedDefault",
        "@id": "urn:des:applied:ad002",
        "taintLevel": "L2",
        "ruleApplied": "urn:des:rule:meeting-duration",
        "inferredAssertions": [{ "property": "expectedDuration", "value": "PT1H" }],
        "evaluationContext": { "hasAbsenceBasedJustification": true, "confidenceModifier": 0.8 }
      }
    ],
    "anomalies": []
  },

  "step7_trace": {
    "@type": "des:AuditTrace",
    "@id": "urn:des:trace:t001",
    "evaluationId": "eval-001",
    "timestamp": "2024-11-22T10:00:00.050Z",
    "input": { "claimId": "urn:tagteam:claim:meeting-001" },
    "ruleProcessing": { "rulesMatched": 2, "rulesApplied": 2 },
    "performance": { "totalDurationMs": 12 },
    "versions": { "desVersion": "2.0.0", "ruleDbVersionId": "urn:des:ruledb:primary:v2024-11-22-001" }
  }
}
```

---

## 17. Version Compatibility

### 17.1 Compatibility Policy

```json
{
  "@type": "des:CompatibilityPolicy",
  "snapshotCompatibility": {
    "policy": "Snapshots are replayable if rule database version is available",
    "versionRetention": "P5Y (all rule database versions retained)",
    "replayMode": {
      "command": "des-replay --snapshot snapshot.json --rules-version v2024-11-22-001",
      "output": "Identical to original evaluation"
    }
  },
  "upgradePath": {
    "v1.x_to_v2.0": {
      "breaking": false,
      "actions": [
        "Add specificity.rank to all rules (default: 100)",
        "Add domainImpact.criticality to rules (default: 0.5)",
        "Add evaluationContext to output consumers",
        "Run des-lint to verify no chaining dependencies"
      ],
      "automated": "des-migrate --from v1 --to v2"
    }
  },
  "deprecations": {
    "v1.x": {
      "status": "supported",
      "endOfLife": "2025-11-22",
      "recommendation": "Upgrade to v2.0 for chaining validation and improved auditability"
    }
  }
}
```

---

## 18. Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-11-20 | Initial specification |
| 1.1.0 | 2024-11-21 | Added epistemic states, specificity ranks, effective severity, compaction |
| 1.2.0 | 2024-11-21 | Clarified single-pass model, taint immutability |
| 2.0.0 | 2024-11-22 | **Major revision**: Added Glossary (§2), Operational Semantics (§3), Formal Invariants (§3.2), Enforcement Policy (§3.3), Metrics & SLAs (§8), Tuning Procedure (§8.2), Audit Trace Schema (§6.4), Implementation Constraints (§13), Conformance Tests with fixtures (§14), Observability Checklist (§15), End-to-End Example (§16), Version Compatibility (§17), PII handling and encryption policies |

---

## 19. References

1. Reiter, R. (1980). A Logic for Default Reasoning. *Artificial Intelligence*, 13(1-2), 81-132.
2. The Plot: FNSR Architectural Overview, §2.3 (Auditability), §4 (Common Sense Layer)
3. FNSR Integration Specification v1.0, §4.2 (DES Integration Points)
4. Basic Formal Ontology (BFO) 2020 Specification
5. Common Core Ontologies (CCO) Documentation
6. JSON-LD 1.1 Specification (W3C Recommendation)
7. Web Crypto API (W3C Recommendation)

---

## Appendix A: JSON-LD Context

```json
{
  "@context": {
    "@version": 1.1,
    "des": "https://fnsr.dev/ns/des/v2#",
    "bfo": "http://purl.obolibrary.org/obo/",
    "cco": "http://www.ontologyrepository.com/CommonCoreOntologies/",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    
    "DefaultRule": "des:DefaultRule",
    "AppliedDefault": "des:AppliedDefault",
    "AnomalyDetected": "des:AnomalyDetected",
    "AuditTrace": "des:AuditTrace",
    "RuleDatabase": "des:RuleDatabase",
    "ExceptionRegistry": "des:ExceptionRegistry",
    "KnownException": "des:KnownException",
    "ConflictResolution": "des:ConflictResolution",
    "CompactionPolicy": "des:CompactionPolicy",
    "Glossary": "des:Glossary",
    "OperationalSemantics": "des:OperationalSemantics",
    
    "prerequisite": { "@id": "des:prerequisite", "@type": "@json" },
    "justifications": { "@id": "des:justifications", "@container": "@list" },
    "consequent": { "@id": "des:consequent", "@type": "@json" },
    "defeasibleBy": { "@id": "des:defeasibleBy", "@container": "@set" },
    "specificity": { "@id": "des:specificity", "@type": "@json" },
    "domainImpact": { "@id": "des:domainImpact", "@type": "@json" },
    
    "triggeringClaim": { "@id": "des:triggeringClaim", "@type": "@id" },
    "ruleApplied": { "@id": "des:ruleApplied", "@type": "@id" },
    "inferredAssertions": { "@id": "des:inferredAssertions", "@container": "@list" },
    "justificationSnapshot": { "@id": "des:justificationSnapshot", "@type": "@json" },
    "evaluationContext": { "@id": "des:evaluationContext", "@type": "@json" },
    "ruleDbVersionId": { "@id": "des:ruleDbVersionId", "@type": "@id" },
    "exceptionRegistryVersionId": { "@id": "des:exceptionRegistryVersionId", "@type": "@id" },
    "epistemicState": "des:epistemicState",
    "evidenceBasis": "des:evidenceBasis",
    "confidenceModifier": "des:confidenceModifier",
    
    "anomalyType": "des:anomalyType",
    "severity": { "@id": "des:severity", "@type": "@json" },
    "effectiveSeverity": "des:effectiveSeverity",
    "violatedExpectation": { "@id": "des:violatedExpectation", "@type": "@json" },
    "triggeringEvidence": { "@id": "des:triggeringEvidence", "@container": "@set", "@type": "@id" },
    
    "taintLevel": "des:taintLevel",
    "timestamp": { "@id": "des:timestamp", "@type": "xsd:dateTime" },
    "versionId": { "@id": "des:versionId", "@type": "@id" }
  }
}
```

---

*This specification is designed to be evaluated, reasoned about, and executed using only a browser (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+), a local NodeJS runtime (18.0.0+), and JSON-LD files. All durations use ISO-8601 format. P30D parallel evaluation is optional and may be performed offline in CI environments.*