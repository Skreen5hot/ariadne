# Portfolio Planning Service (PPS)

## Technical Specification v1.0.0

**Document ID:** `pps-core-01`
**Version:** 1.0.0
**Status:** DRAFT
**Classification:** FNSR Governance Layer Component

---

> *A pure-function planning engine for dependency-aware roadmap construction and risk-adjusted prioritization*

---

## ARIADNE Preamble

This specification defines the Portfolio Planning Service (PPS), a governance-layer component that transforms specification ecosystem state into actionable roadmaps. PPS serves the ARIADNE thesis by ensuring:

1. **Epistemic honesty** — Plans explicitly acknowledge uncertainty through confidence levels, not false precision
2. **Value pluralism** — Prioritization considers multiple dimensions of value via IEE integration, not just feature velocity
3. **Auditability** — Every sequencing decision is traceable to explicit rationale stored as JSON-LD artifacts with HIRI provenance
4. **Human override** — Plans are hypotheses subject to governance review, not autonomous mandates

PPS is not a prediction engine. It is an **uncertainty reduction function** that surfaces dependencies, risks, and trade-offs for human deliberation.

### Ecosystem Position

```
┌─────────────────────────────────────────────────────────────────────┐
│                        GOVERNANCE LAYER                              │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │              Portfolio Planning Service (PPS)                │    │
│  │  • Dependency graph construction                            │    │
│  │  • Risk-adjusted prioritization                             │    │
│  │  • Roadmap generation with confidence levels                │    │
│  └─────────────────────────────────────────────────────────────┘    │
│         ↑ consumes                              ↓ produces          │
│    ┌─────────────┐                        ┌──────────────┐         │
│    │ Fandaws     │ ← ontology             │ Roadmap      │         │
│    │ APS         │ ← precedents           │ Artifacts    │         │
│    │ IEE         │ ← value assessment     │ (JSON-LD)    │         │
│    │ Spec-Driven │ ← gap analysis         │              │         │
│    │ Discovery   │                        │              │         │
│    └─────────────┘                        └──────────────┘         │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | February 2026 | Initial specification; edge-canonical architecture, JSON-LD canonical, taint-aware outputs |

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Execution Model](#2-execution-model)
3. [Service Identity](#3-service-identity)
4. [Data Model](#4-data-model)
5. [Foundational Principles](#5-foundational-principles)
6. [Dependency Graph Analysis](#6-dependency-graph-analysis)
7. [Risk Assessment](#7-risk-assessment)
8. [Prioritization Framework](#8-prioritization-framework)
9. [Roadmap Generation](#9-roadmap-generation)
10. [Termination Guarantees](#10-termination-guarantees)
11. [State Model](#11-state-model)
12. [Host Interface](#12-host-interface)
13. [Integration Contracts](#13-integration-contracts)
14. [Configuration](#14-configuration)
15. [Conformance](#15-conformance)
16. [Appendices](#appendices)

---

## 1. Executive Summary

The Portfolio Planning Service (PPS) is a **pure-function planning engine** that transforms ecosystem state into roadmap artifacts. Given a set of specifications, their dependencies, and risk assessments, PPS produces:

1. **Dependency Graphs** — DAG representation of specification relationships
2. **Critical Path Analysis** — Identification of load-bearing work
3. **Risk-Adjusted Priorities** — Ordered backlog with explicit rationale
4. **Roadmap Artifacts** — Time-horizon plans with confidence levels

### 1.1 Core Properties

| Property | Description |
|----------|-------------|
| **Pure Function** | `(PortfolioState, Config) → (RoadmapResult, PortfolioState')` — no side effects |
| **Edge-Native** | Runs in browser or Node.js with zero external dependencies |
| **JSON-LD Canonical** | All inputs, outputs, and state are JSON-LD documents |
| **Deterministic** | Same inputs always produce same outputs |
| **Taint-Aware** | Outputs carry epistemic markers reflecting input quality |
| **Host-Agnostic** | Makes no assumptions about deployment environment |

### 1.2 What PPS Is Not

PPS is **not**:

- A prediction engine (no time estimates)
- A resource scheduler
- A project management system
- Dependent on databases, message queues, or caches
- Self-scheduling or self-invoking

PPS **computes structure and sequence**; humans **decide resource allocation and timing**.

> **Terminology Note:** The word "Service" in "Portfolio Planning Service" refers to the logical responsibility within the FNSR architecture, not a deployment topology. PPS is a planning function, not a running process.

### 1.3 Architectural Position

```
┌─────────────────────────────────────────────────────────────────┐
│                      HOST ENVIRONMENT                            │
│               (Browser, Node.js, Cloud Function)                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                    PPS CORE (This Spec)                 │   │
│   │                                                         │   │
│   │   Input:  (PortfolioState, Config)                      │   │
│   │   Output: (RoadmapResult, PortfolioState')              │   │
│   │                                                         │   │
│   │   • Dependency Graph Construction                       │   │
│   │   • Critical Path Analysis                              │   │
│   │   • Risk Assessment Integration                         │   │
│   │   • Prioritization Calculation                          │   │
│   │   • Roadmap Generation                                  │   │
│   │                                                         │   │
│   │   PPS never calls external systems directly.            │   │
│   │   All integration is host-mediated.                     │   │
│   │                                                         │   │
│   └─────────────────────────────────────────────────────────┘   │
│                              │                                   │
│              ┌───────────────┴───────────────┐                   │
│              │                               │                   │
│              ▼                               ▼                   │
│    ┌─────────────────┐             ┌─────────────────┐          │
│    │  Host Storage   │             │ Host Integration │          │
│    │  (IndexedDB,    │             │ (Fandaws, IEE,   │          │
│    │   file, Redis)  │             │  Spec-Driven)    │          │
│    └─────────────────┘             └─────────────────┘          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Execution Model

This section is **normative**. Conforming implementations MUST adhere to this model.

### 2.1 Pure Function Semantics

PPS is defined as a pure function:

```
generateRoadmap : (PortfolioState, Config) → (RoadmapResult, PortfolioState')
```

**Requirements:**

| Requirement | Description |
|-------------|-------------|
| **Referential Transparency** | Given identical inputs, PPS MUST return identical outputs |
| **No Side Effects** | PPS MUST NOT perform IO, mutate external state, or depend on ambient context |
| **No Hidden State** | All state MUST be explicitly passed in and returned |
| **Serializable IO** | All inputs and outputs MUST be serializable to JSON-LD |

### 2.2 Edge-First Constraint

**Canonical execution environments:**

- A browser tab (modern ES6+ with no extensions)
- A Node.js process (v18+ with no native modules)

**Constraint:** If a feature cannot execute in these environments without external services, it is NOT part of PPS core.

```javascript
// This MUST work
import { PPS } from '@fnsr/pps';

const pps = new PPS(config);
const { result, state: nextState } = pps.generateRoadmap(portfolioState);

// No network required
// No database required
// No message queue required
// No external services required
```

### 2.3 Host Responsibilities

PPS emits **declarative artifacts**. The host environment decides how to act on them.

| PPS Emits | Host Decides |
|-----------|--------------|
| `RoadmapArtifact` | Where to store (IndexedDB, file, Redis) |
| `DependencyGraph` | How to visualize |
| `PriorityRationale` | Whether to surface in UI |
| `AssumptionRegister` | When to trigger re-evaluation |

**PPS never assumes hosts will act.** All outputs are useful even if hosts take no action.

### 2.4 Determinism Guarantee

For auditability and reproducibility:

```javascript
const result1 = pps.generateRoadmap(state, config);
const result2 = pps.generateRoadmap(state, config);

assert.deepEqual(result1, result2); // Always true
```

**Implications:**

- No `Date.now()` or `Math.random()` in core logic
- Timestamps are derived from inputs or passed explicitly
- Planning date is provided in config, not sampled

### 2.5 State as Value

State is **passed in** and **returned out**, never held internally:

```javascript
// Correct: State flows through
let state = PPS.initialState();
const r1 = pps.generateRoadmap(state, config);
state = r1.state;
const r2 = pps.generateRoadmap(state, configWithUpdates);
state = r2.state;

// Incorrect: Internal state (NOT CONFORMANT)
pps.loadState(state);        // ❌ Stateful method
pps.generateRoadmap();       // ❌ Implicit state
```

### 2.6 Temporal Purity

**Normative Rule:** All temporal values MUST be provided by the host as inputs or computed deterministically from inputs. PPS MUST NOT sample wall-clock time.

| Temporal Value | Source | Notes |
|----------------|--------|-------|
| `planningDate` | Config-provided input | Anchor for horizon calculations |
| `lastReviewDate` | PortfolioState field | When assumptions were last validated |
| `Roadmap.generatedAt` | Config-provided input | When this plan was computed |

---

## 3. Service Identity

| Attribute | Value |
|-----------|-------|
| **Name** | Portfolio Planning Service |
| **Identifier** | `pps-core-01` |
| **Layer** | Governance (FNSR §2.4) |
| **Metaphor** | Architect / Navigator |
| **Nature** | Pure function over explicit state |
| **Canonical Format** | JSON-LD |

### 3.1 Functional Signature

```typescript
interface PPS {
  generateRoadmap(
    state: PortfolioState,
    config: PPSConfig
  ): { result: RoadmapResult; state: PortfolioState };

  analyzeDepenencies(
    state: PortfolioState,
    config: PPSConfig
  ): { result: DependencyAnalysis; state: PortfolioState };

  calculatePriorities(
    state: PortfolioState,
    config: PPSConfig
  ): { result: PriorityResult; state: PortfolioState };

  assessRisks(
    state: PortfolioState,
    config: PPSConfig
  ): { result: RiskAssessment; state: PortfolioState };

  static initialState(): PortfolioState;
}
```

### 3.2 FNSR Integration

Within the FNSR architecture, PPS:

- **Consumes** ecosystem state from Spec-Driven Discovery
- **Consumes** ontological structure from Fandaws
- **Consumes** value assessments from IEE
- **Consumes** historical precedents from APS
- **Emits** roadmap artifacts as JSON-LD documents
- **Does not** directly communicate with external systems
- **Does not** own network, storage, or orchestration

---

## 4. Data Model

All PPS data structures are **JSON-LD documents**.

### 4.1 Taint Levels

PPS outputs carry epistemic markers reflecting input quality:

| Level | Name | Description | PPS Usage |
|-------|------|-------------|-----------|
| L0 | VERIFIED | Governance decisions | Accepted roadmap (post-review) |
| L1 | ATTESTED | Trusted source | Manually entered constraints |
| L2 | INFERRED | Valid inference | Derived dependencies |
| L3 | SPECULATIVE | Computed output | Generated roadmap (pre-review) |
| L4 | HYPOTHETICAL | Simulation only | "What-if" planning scenarios |

**Invariant:** PPS outputs are **L3** until explicitly promoted through governance review.

### 4.2 PortfolioState

The ecosystem state consumed by PPS:

```json
{
  "@context": "https://fnsr.dev/schema/pps/v1",
  "@type": "PortfolioState",
  "@id": "urn:uuid:portfolio-state-20260208",

  "version": "1.0.0",
  "asOf": "2026-02-08T12:00:00Z",

  "specifications": [
    {
      "@type": "SpecificationEntry",
      "@id": "urn:spec:aes-core-01",
      "name": "Abductive Elicitation Service",
      "version": "2.1.0",
      "status": "proposed",
      "layer": "specifications",
      "thesisAlignment": "abductive-hypothesis-generation",
      "lastReviewDate": "2026-02-03",
      "reviewResult": "pass",
      "flags": ["XS-17", "XS-18"]
    }
  ],

  "dependencies": [
    {
      "@type": "SpecificationDependency",
      "@id": "urn:dep:aes-mdre",
      "source": "urn:spec:aes-core-01",
      "target": "urn:spec:mdre-core-01",
      "dependencyType": "hard",
      "rationale": "AES receives GapEvents from MDRE",
      "taint": "L2"
    }
  ],

  "riskAssessments": [
    {
      "@type": "RiskEntry",
      "@id": "urn:risk:aes-001",
      "specification": "urn:spec:aes-core-01",
      "category": "technical-feasibility",
      "probability": "medium",
      "impact": "medium",
      "mitigation": "Prototype hypothesis lifecycle before full implementation",
      "reviewDate": "2026-02-03"
    }
  ],

  "valueAssessments": [
    {
      "@type": "ValueEntry",
      "@id": "urn:value:aes-001",
      "specification": "urn:spec:aes-core-01",
      "valueType": "dependency-unlocking",
      "magnitude": "high",
      "rationale": "Enables incomplete-information reasoning for entire ecosystem",
      "source": "iee-assessment"
    }
  ],

  "constraints": {
    "teamCapacity": {
      "available": 3,
      "skills": ["bfo-ontology", "edge-canonical", "json-ld"]
    },
    "governanceConstraints": ["ariadne-review-required"],
    "complianceConstraints": []
  },

  "assumptions": [
    {
      "@type": "PlanningAssumption",
      "@id": "urn:assumption:001",
      "statement": "BFO/CCO ontology stable for planning horizon",
      "confidence": 0.9,
      "invalidationTrigger": "bfo-major-version-change",
      "expiresAt": "2026-06-01"
    }
  ]
}
```

### 4.3 DependencyGraph

DAG representation of specification relationships:

```json
{
  "@context": "https://fnsr.dev/schema/pps/v1",
  "@type": "DependencyGraph",
  "@id": "urn:uuid:dep-graph-20260208",

  "generatedAt": "2026-02-08T12:00:00Z",
  "sourceState": "urn:uuid:portfolio-state-20260208",

  "nodes": [
    {
      "@type": "GraphNode",
      "@id": "urn:spec:aes-core-01",
      "inDegree": 1,
      "outDegree": 3,
      "criticalPathMember": true,
      "loadBearing": true
    }
  ],

  "edges": [
    {
      "@type": "GraphEdge",
      "from": "urn:spec:aes-core-01",
      "to": "urn:spec:mdre-core-01",
      "edgeType": "hard",
      "weight": 1.0
    }
  ],

  "analysis": {
    "isDAG": true,
    "hasCycles": false,
    "maxDepth": 5,
    "criticalPath": ["urn:spec:w2fuel", "urn:spec:mdre", "urn:spec:aes"],
    "criticalPathLength": 3,
    "loadBearingNodes": ["urn:spec:fnsr", "urn:spec:mdre"],
    "orphanNodes": [],
    "rootNodes": ["urn:spec:bfo", "urn:spec:cco"]
  },

  "taint": "L2"
}
```

### 4.4 RiskAssessment

Structured risk evaluation:

```json
{
  "@context": "https://fnsr.dev/schema/pps/v1",
  "@type": "RiskAssessment",
  "@id": "urn:uuid:risk-assessment-20260208",

  "generatedAt": "2026-02-08T12:00:00Z",

  "riskMatrix": [
    {
      "@type": "RiskEvaluation",
      "specification": "urn:spec:aes-core-01",
      "dimensions": {
        "technical-feasibility": { "score": 0.7, "confidence": 0.8 },
        "integration-complexity": { "score": 0.6, "confidence": 0.7 },
        "epistemic-uncertainty": { "score": 0.5, "confidence": 0.6 },
        "security-compliance": { "score": 0.9, "confidence": 0.9 },
        "scalability": { "score": 0.8, "confidence": 0.7 },
        "governance-readiness": { "score": 0.85, "confidence": 0.8 }
      },
      "aggregateRisk": 0.65,
      "riskCategory": "medium",
      "nonNegotiableAlignment": {
        "decidability": "aligned",
        "separationOfConcerns": "aligned",
        "uncertaintyVisible": "aligned",
        "defenseInDepth": "aligned",
        "edgeCanonicalFirst": "aligned",
        "humanOverride": "aligned"
      }
    }
  ],

  "portfolioRisk": {
    "aggregate": 0.58,
    "highRiskItems": [],
    "unknownUnknowns": ["cross-service-taint-propagation"]
  },

  "taint": "L3"
}
```

### 4.5 PriorityResult

Ordered backlog with rationale:

```json
{
  "@context": "https://fnsr.dev/schema/pps/v1",
  "@type": "PriorityResult",
  "@id": "urn:uuid:priority-result-20260208",

  "generatedAt": "2026-02-08T12:00:00Z",
  "method": "wsjf-with-risk",

  "rankedItems": [
    {
      "rank": 1,
      "specification": "urn:spec:w2fuel-core-01",
      "score": 0.92,
      "components": {
        "dependencyImpact": 0.95,
        "riskReduction": 0.8,
        "valueContribution": 0.85,
        "thesisAlignment": 0.95
      },
      "rationale": "Highest dependency impact; enables MDRE, AES, DES, CSS",
      "confidence": 0.85
    }
  ],

  "assumptionsDependency": [
    "urn:assumption:001",
    "urn:assumption:002"
  ],

  "taint": "L3"
}
```

### 4.6 RoadmapArtifact

Time-horizon plan with confidence levels:

```json
{
  "@context": "https://fnsr.dev/schema/pps/v1",
  "@type": "RoadmapArtifact",
  "@id": "urn:uuid:roadmap-2026-Q1",

  "version": "1.0",
  "generatedAt": "2026-02-08T12:00:00Z",
  "planningDate": "2026-02-08",

  "horizons": [
    {
      "@type": "PlanningHorizon",
      "horizon": "near-term",
      "range": { "start": "2026-02-08", "end": "2026-05-08" },
      "confidence": 0.85,
      "granularity": "specification",
      "items": [
        {
          "specification": "urn:spec:w2fuel-core-01",
          "sequence": 1,
          "rationale": "Foundation for T-Box operations",
          "dependencies": [],
          "risks": ["urn:risk:w2fuel-001"]
        },
        {
          "specification": "urn:spec:mdre-core-01",
          "sequence": 2,
          "rationale": "Core reasoning engine",
          "dependencies": ["urn:spec:w2fuel-core-01"],
          "risks": []
        }
      ]
    },
    {
      "@type": "PlanningHorizon",
      "horizon": "mid-term",
      "range": { "start": "2026-05-08", "end": "2026-08-08" },
      "confidence": 0.65,
      "granularity": "theme",
      "items": [
        {
          "theme": "reasoning-triad-completion",
          "specifications": ["urn:spec:aes", "urn:spec:des", "urn:spec:css"],
          "rationale": "Complete non-monotonic reasoning capabilities"
        }
      ]
    },
    {
      "@type": "PlanningHorizon",
      "horizon": "long-term",
      "range": { "start": "2026-08-08", "end": "2027-02-08" },
      "confidence": 0.4,
      "granularity": "strategic-intent",
      "items": [
        {
          "intent": "emancipation-readiness",
          "description": "Infrastructure for synthetic personhood transition",
          "rationale": "Thesis-aligned strategic goal"
        }
      ]
    }
  ],

  "assumptions": [
    {
      "@type": "RoadmapAssumption",
      "@id": "urn:assumption:roadmap-001",
      "statement": "Team capacity remains at 3 developers",
      "invalidationTrigger": "team-change",
      "impact": "high"
    }
  ],

  "ariadneChecks": {
    "thesisAlignment": true,
    "nonNegotiablePreservation": true,
    "tensionConsistency": true,
    "crossSpecConsistency": true,
    "archonAlignment": true,
    "auditabilityVerification": true,
    "oneParagraphTest": "This roadmap sequences ecosystem development to establish reasoning foundations (W2Fuel, MDRE) before building dependent reasoning services (AES, DES, CSS), ensuring each component has stable foundations before implementation begins."
  },

  "hiri:manifest": "urn:hiri:manifest:roadmap-2026-Q1",
  "taint": "L3"
}
```

### 4.7 RoadmapResult

Complete output from `generateRoadmap`:

```json
{
  "@context": "https://fnsr.dev/schema/pps/v1",
  "@type": "RoadmapResult",
  "@id": "urn:uuid:roadmap-result-20260208",

  "status": "generated",

  "dependencyGraph": { "@type": "DependencyGraph" },
  "riskAssessment": { "@type": "RiskAssessment" },
  "priorityResult": { "@type": "PriorityResult" },
  "roadmap": { "@type": "RoadmapArtifact" },

  "diagnostics": {
    "specificationsCovered": 22,
    "dependenciesAnalyzed": 45,
    "risksEvaluated": 18,
    "cyclesDetected": 0,
    "orphansDetected": 0,
    "assumptionsRequired": 5
  },

  "recommendations": [
    {
      "@type": "PlanningRecommendation",
      "type": "risk-mitigation",
      "target": "urn:spec:oers-core-01",
      "recommendation": "Consider prototyping entity resolution before full implementation",
      "rationale": "High integration complexity with cross-service dependencies"
    }
  ],

  "taint": "L3"
}
```

---

## 5. Foundational Principles

### 5.1 Dependencies Are First-Class Citizens

Unacknowledged dependencies are the primary cause of late-stage failure. PPS treats dependencies as explicit graph edges with typed semantics.

### 5.2 Dependency Types

| Type | Description | Graph Weight | Example |
|------|-------------|--------------|---------|
| **Hard** | Work cannot proceed | 1.0 | HIRI requires Ed25519 crypto primitives |
| **Soft** | Assumptions possible | 0.5 | DES defaults can inform AES hypotheses |
| **Data** | Schema, contracts | 0.7 | Fandaws → FNSR knowledge ingestion contract |
| **Operational** | Deployment, support | 0.3 | IPFS pinning for HIRI manifests |
| **Governance** | Approvals, audits | 0.6 | ARIADNE review before spec finalization |
| **Epistemic** | Taint level requirements | 0.8 | L3 outputs require promotion before production |

### 5.3 Risk as Cost

Risk reduction has intrinsic value. PPS explicitly values uncertainty elimination in prioritization:

```
adjustedValue(spec) = baseValue(spec) + riskReductionValue(spec)
```

### 5.4 Sequencing Over Speed

The order of work matters more than speed of individual tasks. PPS prioritizes critical path clarity over parallelization opportunities.

### 5.5 Plans as Hypotheses

All plans are L3 (speculative) until governance review promotes them. This aligns with ARIADNE's epistemic firewall principle.

```
═══════════════════════════════════════════════════════════════════
║                    PLANNING FIREWALL                             ║
║                                                                  ║
║    L3 Roadmap (PPS output) → Governance Review → L0 Roadmap     ║
║                                                                  ║
║    Crossing requires:                                            ║
║    • ARIADNE 7-check validation                                  ║
║    • Stakeholder sign-off                                        ║
║    • Assumption review                                           ║
║                                                                  ║
═══════════════════════════════════════════════════════════════════
```

---

## 6. Dependency Graph Analysis

### 6.1 Graph Construction

```
FUNCTION buildDependencyGraph(state: PortfolioState) → DependencyGraph:

  graph = DirectedGraph()

  // Add specification nodes
  FOR EACH spec IN state.specifications:
    graph.addNode({
      id: spec["@id"],
      metadata: {
        name: spec.name,
        status: spec.status,
        layer: spec.layer
      }
    })

  // Add dependency edges
  FOR EACH dep IN state.dependencies:
    weight = DEPENDENCY_WEIGHTS[dep.dependencyType]
    graph.addEdge(dep.source, dep.target, {
      type: dep.dependencyType,
      weight: weight,
      rationale: dep.rationale
    })

  RETURN graph
```

### 6.2 Cycle Detection

PPS MUST reject portfolio states with circular dependencies:

```
FUNCTION detectCycles(graph: DependencyGraph) → CycleReport:

  visited = Set()
  recursionStack = Set()
  cycles = []

  FOR EACH node IN graph.nodes:
    IF hasCycleDFS(node, visited, recursionStack, graph, cycles):
      // Cycle found

  RETURN {
    hasCycles: cycles.length > 0,
    cycles: cycles,
    recommendation: cycles.length > 0 ?
      "Resolve circular dependencies before planning" : null
  }
```

### 6.3 Critical Path Analysis

Identify the longest path through the dependency graph:

```
FUNCTION findCriticalPath(graph: DependencyGraph) → CriticalPath:

  // Topological sort
  sorted = topologicalSort(graph)

  // Calculate longest path to each node
  distances = Map()
  predecessors = Map()

  FOR EACH node IN sorted:
    distances[node] = 0
    predecessors[node] = null

  FOR EACH node IN sorted:
    FOR EACH successor IN graph.getSuccessors(node):
      edgeWeight = graph.getEdgeWeight(node, successor)
      newDist = distances[node] + edgeWeight

      IF newDist > distances[successor]:
        distances[successor] = newDist
        predecessors[successor] = node

  // Find node with maximum distance (sink of critical path)
  sink = argmax(distances)

  // Reconstruct path
  path = reconstructPath(predecessors, sink)

  RETURN {
    path: path,
    length: distances[sink],
    sinkNode: sink
  }
```

### 6.4 Load-Bearing Node Detection

Identify specifications with high downstream impact:

```
FUNCTION identifyLoadBearingNodes(graph: DependencyGraph) → Node[]:

  loadBearing = []

  FOR EACH node IN graph.nodes:
    // Count transitive dependents
    dependents = countTransitiveDependents(graph, node)

    // Node is load-bearing if >30% of specs depend on it
    IF dependents / graph.nodes.length > 0.3:
      loadBearing.push(node)

  RETURN loadBearing
```

---

## 7. Risk Assessment

### 7.1 Risk Dimensions

PPS evaluates risk across dimensions aligned with ARIADNE non-negotiables:

| Dimension | Description | Non-Negotiable Alignment |
|-----------|-------------|-------------------------|
| **Technical Feasibility** | Can we build it? | Decidability |
| **Integration Complexity** | How many touchpoints? | Separation of Concerns |
| **Epistemic Uncertainty** | What don't we know? | Uncertainty Visible |
| **Security Compliance** | Attack surface, regulatory | Defense in Depth |
| **Scalability** | Edge-canonical constraints | Edge-Canonical First |
| **Governance Readiness** | Human oversight capacity | Human Override |

### 7.2 Risk Scoring

```
FUNCTION assessRisk(spec: Specification, state: PortfolioState) → RiskEvaluation:

  dimensions = {}

  // Technical feasibility
  dimensions["technical-feasibility"] = {
    score: assessTechnicalFeasibility(spec, state),
    confidence: 0.8  // Calibrated by domain expert review
  }

  // Integration complexity
  deps = state.dependencies.filter(d => d.source == spec["@id"])
  dimensions["integration-complexity"] = {
    score: 1.0 - (deps.length / MAX_EXPECTED_DEPS),
    confidence: 0.9
  }

  // Epistemic uncertainty
  unknowns = spec.flags?.length ?? 0
  dimensions["epistemic-uncertainty"] = {
    score: 1.0 - (unknowns / MAX_EXPECTED_FLAGS),
    confidence: 0.6  // Lower confidence for unknowns
  }

  // ... other dimensions

  aggregateRisk = weightedAverage(dimensions, RISK_WEIGHTS)

  RETURN {
    specification: spec["@id"],
    dimensions: dimensions,
    aggregateRisk: aggregateRisk,
    riskCategory: categorize(aggregateRisk)
  }
```

### 7.3 Risk Categorization

| Category | Aggregate Score | Treatment |
|----------|-----------------|-----------|
| **Low** | 0.0 - 0.3 | Standard sequencing |
| **Medium** | 0.3 - 0.6 | Monitor assumptions |
| **High** | 0.6 - 0.8 | Pull forward, time-box |
| **Critical** | 0.8 - 1.0 | Escalate to governance |

---

## 8. Prioritization Framework

### 8.1 Inputs to Prioritization

| Input | Weight | Source |
|-------|--------|--------|
| Dependency Impact | 0.30 | Dependency graph analysis |
| Risk Reduction | 0.25 | Risk assessment |
| Value Contribution | 0.20 | IEE integration (if available) |
| Thesis Alignment | 0.15 | ARIADNE 7-check |
| Effort Estimate | 0.10 | Manual input (optional) |

### 8.2 WSJF-with-Risk Calculation

```
FUNCTION calculatePriority(spec: Specification, state: PortfolioState, config: PPSConfig) → number:

  // Cost of Delay components
  dependencyImpact = countTransitiveDependents(state.dependencyGraph, spec) /
                     state.specifications.length

  riskReduction = 1.0 - assessRisk(spec, state).aggregateRisk

  valueContribution = state.valueAssessments
    .find(v => v.specification == spec["@id"])?.magnitude ?? 0.5

  thesisAlignment = assessThesisAlignment(spec, config)

  // Weighted Sum
  costOfDelay = (
    config.weights.dependencyImpact * dependencyImpact +
    config.weights.riskReduction * riskReduction +
    config.weights.valueContribution * valueContribution +
    config.weights.thesisAlignment * thesisAlignment
  )

  // Job Duration (if provided)
  effort = state.effortEstimates?.[spec["@id"]] ?? 1.0

  // WSJF = Cost of Delay / Job Duration
  RETURN costOfDelay / effort
```

### 8.3 Priority Ranking

```
FUNCTION rankSpecifications(state: PortfolioState, config: PPSConfig) → PriorityResult:

  priorities = []

  FOR EACH spec IN state.specifications:
    score = calculatePriority(spec, state, config)

    priorities.push({
      specification: spec["@id"],
      score: score,
      components: {
        dependencyImpact: dependencyImpact,
        riskReduction: riskReduction,
        valueContribution: valueContribution,
        thesisAlignment: thesisAlignment
      },
      rationale: generateRationale(spec, state)
    })

  // Sort descending by score
  priorities.sort((a, b) => b.score - a.score)

  // Assign ranks
  FOR i, item IN enumerate(priorities):
    item.rank = i + 1

  RETURN {
    rankedItems: priorities,
    method: "wsjf-with-risk",
    generatedAt: config.planningDate
  }
```

---

## 9. Roadmap Generation

### 9.1 Horizon Assignment

```
FUNCTION assignHorizons(priorities: PriorityResult, graph: DependencyGraph, config: PPSConfig) → Horizon[]:

  horizons = [
    { horizon: "near-term", items: [], confidence: 0.85, granularity: "specification" },
    { horizon: "mid-term", items: [], confidence: 0.65, granularity: "theme" },
    { horizon: "long-term", items: [], confidence: 0.40, granularity: "strategic-intent" }
  ]

  // Near-term: Top N items that respect dependency order
  nearTermCapacity = config.horizonCapacity.nearTerm
  assigned = Set()

  FOR EACH item IN priorities.rankedItems:
    IF horizons[0].items.length >= nearTermCapacity:
      BREAK

    // Check if all dependencies are assigned
    deps = graph.getDependencies(item.specification)
    IF deps.every(d => assigned.has(d) OR isExternal(d)):
      horizons[0].items.push({
        specification: item.specification,
        sequence: horizons[0].items.length + 1,
        rationale: item.rationale,
        dependencies: deps.filter(d => !isExternal(d)),
        risks: getRisks(item.specification)
      })
      assigned.add(item.specification)

  // Mid-term: Group remaining by theme
  remaining = priorities.rankedItems.filter(i => !assigned.has(i.specification))
  themes = groupByTheme(remaining, config)
  horizons[1].items = themes

  // Long-term: Strategic intents
  horizons[2].items = config.strategicIntents

  RETURN horizons
```

### 9.2 ARIADNE 7-Check Integration

```
FUNCTION validateRoadmap(roadmap: RoadmapArtifact, state: PortfolioState, config: PPSConfig) → ARIADNEChecks:

  checks = {
    thesisAlignment: checkThesisAlignment(roadmap, state),
    nonNegotiablePreservation: checkNonNegotiables(roadmap, state),
    tensionConsistency: checkTensions(roadmap, state),
    crossSpecConsistency: checkCrossSpecConsistency(roadmap, state),
    archonAlignment: checkArchonAlignment(roadmap, state),
    auditabilityVerification: checkAuditability(roadmap),
    oneParagraphTest: generateOneParagraphSummary(roadmap)
  }

  // If any check fails, add to diagnostics
  IF NOT all(checks):
    roadmap.diagnostics.ariadneViolations =
      Object.entries(checks)
        .filter(([k, v]) => v === false)
        .map(([k]) => k)

  RETURN checks
```

### 9.3 Assumption Register

```
FUNCTION buildAssumptionRegister(roadmap: RoadmapArtifact, state: PortfolioState) → Assumption[]:

  assumptions = []

  // Inherit portfolio assumptions
  FOR EACH assumption IN state.assumptions:
    IF affectsRoadmap(assumption, roadmap):
      assumptions.push({
        ...assumption,
        roadmapImpact: assessImpact(assumption, roadmap)
      })

  // Add implicit assumptions
  IF roadmap.horizons[0].items.length > 0:
    assumptions.push({
      statement: "Near-term items have stable dependency foundations",
      confidence: 0.9,
      invalidationTrigger: "critical-dependency-delay",
      impact: "high"
    })

  RETURN assumptions
```

---

## 10. Termination Guarantees

### 10.1 Bounding Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `maxSpecifications` | 100 | Maximum specs in portfolio |
| `maxDependencies` | 500 | Maximum dependency edges |
| `maxIterations` | 10000 | Maximum algorithmic iterations |
| `maxPathLength` | 50 | Maximum critical path length |

### 10.2 Termination Reasons

| Reason | Meaning |
|--------|---------|
| `completed` | All analysis finished successfully |
| `cycle_detected` | Circular dependency found |
| `iteration_limit` | Hit iteration limit |
| `invalid_input` | Portfolio state validation failed |

---

## 11. State Model

### 11.1 State as First-Class Value

PPS state is:

- **Explicit**: Passed in, returned out — never hidden
- **Immutable**: Each operation returns new state
- **Serializable**: Full JSON-LD round-trip without loss
- **Versionable**: Schema version tracked for migrations

### 11.2 Initial State

```javascript
function initialState() {
  return {
    "@context": "https://fnsr.dev/schema/pps/v1",
    "@type": "PortfolioState",
    "version": "1.0.0",
    "asOf": null,  // Must be provided by host
    "specifications": [],
    "dependencies": [],
    "riskAssessments": [],
    "valueAssessments": [],
    "constraints": {},
    "assumptions": []
  };
}
```

### 11.3 State Serialization

State MUST survive JSON-LD round-trip:

```javascript
const serialized = JSON.stringify(state);
const deserialized = JSON.parse(serialized);
assert.deepEqual(
  pps.generateRoadmap(state, config),
  pps.generateRoadmap(deserialized, config)
);
```

---

## 12. Host Interface

### 12.1 Minimal Host Contract

A conforming host MUST:

1. Provide `generateRoadmap` inputs (PortfolioState, Config as JSON-LD)
2. Accept `generateRoadmap` outputs (RoadmapResult, State' as JSON-LD)
3. Manage state persistence (if desired)
4. Provide integration data from upstream services (if available)

A conforming host MAY:

1. Implement visualization adapters
2. Implement notification triggers for assumption invalidation
3. Integrate with governance workflows
4. Persist roadmaps to any backend

### 12.2 Browser Host Example

```javascript
import { PPS } from '@fnsr/pps';

const pps = new PPS(config);
let state = await loadPortfolioState();

async function generateNewRoadmap() {
  const { result, state: newState } = pps.generateRoadmap(state, config);
  state = newState;

  // Store in IndexedDB
  await db.put('state', state);
  await db.put('roadmap', result.roadmap);

  // Render visualization
  renderDependencyGraph(result.dependencyGraph);
  renderRoadmapTimeline(result.roadmap);

  return result;
}
```

### 12.3 Node.js Host Example

```javascript
import { PPS } from '@fnsr/pps';
import { readFile, writeFile } from 'fs/promises';

const pps = new PPS(config);

async function plan() {
  const state = JSON.parse(await readFile('./portfolio-state.json'));
  const { result, state: newState } = pps.generateRoadmap(state, config);

  await writeFile('./portfolio-state.json', JSON.stringify(newState));
  await writeFile('./roadmap-output.json', JSON.stringify(result.roadmap));

  return result;
}
```

---

## 13. Integration Contracts

### 13.1 Fandaws Integration

PPS consumes ontological structure from Fandaws:

```typescript
interface FandawsConsumption {
  // Get specification layer hierarchy
  getLayerHierarchy(): LayerDefinition[];

  // Get thesis alignment vocabulary
  getThesisAlignmentTerms(): ThesisAlignmentTerm[];

  // Validate JSON-LD against ontology
  validateAgainstOntology(artifact: object): ValidationResult;
}
```

### 13.2 IEE Integration

PPS consumes value assessments from IEE:

```typescript
interface IEEConsumption {
  // Get multi-dimensional value assessment
  assessValue(specification: string): ValueAssessment;

  // Get IEE-style deliberation for priority conflicts
  resolveConflict(specs: string[]): ConflictResolution;
}
```

### 13.3 Spec-Driven Discovery Integration

PPS consumes gap analysis from Spec-Driven Discovery:

```typescript
interface SpecDrivenDiscoveryConsumption {
  // Get current ecosystem state
  getEcosystemState(): PortfolioState;

  // Get identified gaps
  getGaps(): Gap[];

  // Get cross-reference analysis
  getCrossReferences(): CrossReference[];
}
```

### 13.4 APS Integration

PPS consumes historical precedents from APS:

```typescript
interface APSConsumption {
  // Get similar planning scenarios
  getSimilarScenarios(portfolio: PortfolioState): Precedent[];

  // Get precedent-based risk adjustments
  getRiskAdjustments(specification: string): RiskAdjustment[];
}
```

### 13.5 Event Protocol

#### Request Event: `fnsr.planning.requested`

```json
{
  "@type": "PlanningRequestedEvent",
  "eventId": "uuid",
  "timestamp": "xsd:dateTime",
  "source": "governance-ui | scheduler",
  "correlationId": "uuid",
  "payload": {
    "@type": "PlanningRequest",
    "portfolioState": "PortfolioState",
    "config": "PPSConfig"
  }
}
```

#### Result Event: `fnsr.planning.result`

```json
{
  "@type": "PlanningResultEvent",
  "eventId": "uuid",
  "timestamp": "xsd:dateTime",
  "source": "pps",
  "correlationId": "uuid",
  "payload": {
    "@type": "RoadmapResult",
    "taint": "L3"
  }
}
```

---

## 14. Configuration

### 14.1 Configuration Schema

```json
{
  "@type": "PPSConfig",
  "version": "1.0.0",

  "planningDate": "2026-02-08",

  "horizonCapacity": {
    "nearTerm": 5,
    "midTermThemes": 3,
    "longTermIntents": 2
  },

  "horizonRanges": {
    "nearTerm": { "months": 3 },
    "midTerm": { "months": 6 },
    "longTerm": { "months": 12 }
  },

  "weights": {
    "dependencyImpact": 0.30,
    "riskReduction": 0.25,
    "valueContribution": 0.20,
    "thesisAlignment": 0.15,
    "effort": 0.10
  },

  "riskWeights": {
    "technical-feasibility": 0.25,
    "integration-complexity": 0.20,
    "epistemic-uncertainty": 0.20,
    "security-compliance": 0.15,
    "scalability": 0.10,
    "governance-readiness": 0.10
  },

  "thresholds": {
    "loadBearingRatio": 0.3,
    "highRiskScore": 0.6,
    "criticalRiskScore": 0.8
  },

  "limits": {
    "maxSpecifications": 100,
    "maxDependencies": 500,
    "maxIterations": 10000,
    "maxPathLength": 50
  },

  "strategicIntents": [
    {
      "intent": "emancipation-readiness",
      "description": "Infrastructure for synthetic personhood transition"
    }
  ],

  "ariadneValidation": {
    "enabled": true,
    "requiredChecks": [
      "thesisAlignment",
      "nonNegotiablePreservation",
      "crossSpecConsistency"
    ]
  }
}
```

---

## 15. Conformance

### 15.1 Core Conformance Requirements

An implementation is **Core Conformant** if:

1. **Pure Function**: `generateRoadmap` has no side effects
2. **Deterministic**: Same inputs → same outputs
3. **JSON-LD IO**: All inputs/outputs serialize to valid JSON-LD
4. **State Transparency**: State is passed in and returned, never hidden
5. **Termination**: Analysis always terminates within bounds
6. **Edge Executable**: Runs in browser/Node.js without external services
7. **Temporal Purity**: No internal time sampling
8. **Cycle Detection**: Circular dependencies rejected
9. **Taint Marking**: All outputs carry appropriate epistemic markers

### 15.2 Conformance Testing

```javascript
describe('PPS Core Conformance', () => {
  test('determinism', () => {
    const r1 = pps.generateRoadmap(state, config);
    const r2 = pps.generateRoadmap(state, config);
    expect(r1).toEqual(r2);
  });

  test('no side effects', () => {
    const original = JSON.stringify(state);
    pps.generateRoadmap(state, config);
    expect(JSON.stringify(state)).toEqual(original);
  });

  test('json-ld round trip', () => {
    const { result } = pps.generateRoadmap(state, config);
    const rt = JSON.parse(JSON.stringify(result));
    expect(rt).toEqual(result);
  });

  test('cycle detection', () => {
    const cyclicState = createCyclicDependencies();
    const { result } = pps.generateRoadmap(cyclicState, config);
    expect(result.status).toBe('error');
    expect(result.error.code).toBe('CYCLE_DETECTED');
  });

  test('taint marking', () => {
    const { result } = pps.generateRoadmap(state, config);
    expect(result.roadmap.taint).toBe('L3');
  });
});
```

---

## 16. Appendices

### Appendix A: Glossary

| Term | Definition |
|------|------------|
| **Critical Path** | Longest path through dependency graph |
| **Load-Bearing Node** | Specification with >30% transitive dependents |
| **Horizon** | Planning time range with associated confidence |
| **WSJF** | Weighted Shortest Job First prioritization |
| **Taint** | Epistemic quality marker (L0-L4) |
| **Planning Firewall** | Boundary between L3 output and L0 accepted plan |

### Appendix B: Error Codes

| Code | Name | Description |
|------|------|-------------|
| `PPS-001` | `INVALID_STATE` | PortfolioState failed validation |
| `PPS-002` | `INVALID_CONFIG` | Config failed validation |
| `PPS-003` | `CYCLE_DETECTED` | Circular dependency found |
| `PPS-004` | `ITERATION_LIMIT` | Max iterations exceeded |
| `PPS-005` | `MISSING_DEPENDENCY` | Referenced spec not in portfolio |
| `PPS-006` | `ARIADNE_VIOLATION` | Failed ARIADNE 7-check |

### Appendix C: Default Configuration

```typescript
const DEFAULT_CONFIG: PPSConfig = {
  version: "1.0.0",
  planningDate: null,  // MUST be provided
  horizonCapacity: { nearTerm: 5, midTermThemes: 3, longTermIntents: 2 },
  horizonRanges: { nearTerm: { months: 3 }, midTerm: { months: 6 }, longTerm: { months: 12 } },
  weights: { dependencyImpact: 0.30, riskReduction: 0.25, valueContribution: 0.20, thesisAlignment: 0.15, effort: 0.10 },
  riskWeights: { "technical-feasibility": 0.25, "integration-complexity": 0.20, "epistemic-uncertainty": 0.20, "security-compliance": 0.15, "scalability": 0.10, "governance-readiness": 0.10 },
  thresholds: { loadBearingRatio: 0.3, highRiskScore: 0.6, criticalRiskScore: 0.8 },
  limits: { maxSpecifications: 100, maxDependencies: 500, maxIterations: 10000, maxPathLength: 50 },
  strategicIntents: [],
  ariadneValidation: { enabled: true, requiredChecks: ["thesisAlignment", "nonNegotiablePreservation", "crossSpecConsistency"] }
};
```

### Appendix D: Reference Implementation Structure

```
pps/
├── src/
│   ├── pps.ts                    # Main engine
│   ├── graph/
│   │   ├── build.ts              # Graph construction
│   │   ├── cycles.ts             # Cycle detection
│   │   ├── critical-path.ts      # Critical path analysis
│   │   └── load-bearing.ts       # Load-bearing node detection
│   ├── risk/
│   │   ├── assess.ts             # Risk assessment
│   │   └── dimensions.ts         # Risk dimension definitions
│   ├── priority/
│   │   ├── wsjf.ts               # WSJF calculation
│   │   └── rank.ts               # Priority ranking
│   ├── roadmap/
│   │   ├── horizons.ts           # Horizon assignment
│   │   ├── ariadne.ts            # ARIADNE validation
│   │   └── assumptions.ts        # Assumption register
│   └── adapters/
│       ├── fandaws.ts            # Fandaws integration
│       ├── iee.ts                # IEE integration
│       └── spec-driven.ts        # Spec-Driven Discovery integration
├── test/
│   ├── conformance/
│   │   ├── determinism.test.ts
│   │   ├── cycles.test.ts
│   │   └── taint.test.ts
│   └── integration/
│       └── full-portfolio.test.ts
└── package.json
```

---

## Document Control

| Attribute | Value |
|-----------|-------|
| **Version** | 1.0.0 |
| **Status** | DRAFT |
| **Authors** | Aaron / Claude |
| **Created** | 2026-02-08 |

### Design Principles

1. **Edge as default truth** — If it works in a browser, it works everywhere
2. **Pure function over explicit state** — Deterministic, testable, replayable
3. **Declarative artifacts** — PPS says what, host decides how
4. **JSON-LD canonical** — Semantic, web-native, serializable
5. **Plans are hypotheses** — L3 until governance promotes to L0
6. **Dependencies first** — Sequencing clarity over parallelization
7. **Risk as value** — Uncertainty reduction is explicitly valued

---

## References

- The Plot §4 (Component Map)
- Spec-Driven Discovery v1.1
- ARIADNE Process Guide v1.0
- Portfolio Planning Foundation Document v1.0
- Fandaws v3.3 (ecosystem integration patterns)
- IEE Architecture (multi-value deliberation)
- AES Technical Spec v2.1 (edge-canonical architecture pattern)
- CSS Specification v2.0 (taint architecture pattern)

---

*PPS is how FNSR navigates complexity. It transforms ecosystem state into actionable sequences, ensuring that development follows dependency order, addresses risks early, and maintains thesis alignment. The L3 taint on outputs ensures that plans remain hypotheses subject to human deliberation, not autonomous mandates.*
