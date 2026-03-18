# FNSR Orchestrator Service — Technical Specification

## Service Federation and Coordination Layer

---

| Field | Value |
|-------|-------|
| **Specification ID** | `fnsr-orch-01` |
| **Version** | 2.3.0 |
| **Status** | Hardened Candidate |
| **Date** | March 2026 |
| **Supersedes** | v2.2.0 |
| **Tier** | 0 (Safety-Critical Infrastructure) |
| **Phase** | 4 (requires all services; minimal viable subset in Phase 1) |
| **Authors** | Aaron / Claude |
| **Dependencies** | FNSR Performance v2.0, FNSR Governance v2.0, ARCHON v3.0, CPS v1.0.0 |

> *The FNSR Orchestrator is the coordination substrate that connects the 42 services of the FNSR ecosystem into a coherent cognitive agent. It does not reason, decide, or evaluate. It routes, sequences, enforces taint propagation, manages saga lifecycles, and degrades gracefully. It is the switchboard, not the brain.*

---

### Revision History: v2.1 → v2.2

v2.2 addresses 15 findings from architectural review of v2.1. The core architecture (saga lifecycle, taint engine, CPS independence, incremental deployment) is preserved. The changes are corrections, not redesigns.

**Critical fixes:**
- **C-1:** Service count provenance documented (§1.4). The 29→42 growth is now explicitly traced.
- **C-2:** Path classifier chicken-and-egg resolved (§3.1). `query.taintHint` is now a caller-supplied hint, untrusted, with post-ingestion reassessment.
- **C-3:** BAM degradation is now phase-conditional (§5.1). Phase 1 accepts the safety gap with documented risk.
- **C-4:** CSS→MDRE taint gateway defined (§6.4). Counterfactual Gateway mechanism closes the L4 consumption gap.
- **C-5:** Determinism contract restated honestly (§1.3). Classifier state is now an explicit input.

**Significant fixes:**
- **S-6:** CBOR dependency acknowledged as bundled exception with size/audit commitment (§7.2).
- **S-7:** Taint degradation elevation semantics unified (§5.1, §6.2). Absolute overrides distinguished from relative elevation.
- **S-8:** Governance tier check moved to two-phase: preliminary after ingestion, refinement before evaluation (§10.1).
- **S-9:** Commitment-act queries receive synchronous CTS acknowledgment (§4.4).
- **S-10:** `fnsr.service.status_changed` producer reassigned to Orchestrator (§8.2).

**Minor fixes:**
- **M-11:** IRIS described with role, worker, degradation, and events (§2.2, §8.2).
- **M-12:** W2Fuel described with role clarification (§2.2).
- **M-13:** Dependency graph rebuild protocol added (§2.4).
- **M-14:** Orchestrator state persistence and crash recovery documented (§4.5).
- **M-15:** CPS spec dependency escalated to Critical Dependencies section (§14.1).

### Revision History: v2.2 → v2.3

v2.3 closes 10 residual and newly introduced issues from the v2.2 architectural review. The core architecture is unchanged. These are precision fixes, not structural changes. Status promoted from Hardened Draft to Hardened Candidate.

**Must-fix (closed):**
- **R-1:** HIRI signing scope now explicitly covers `counterfactualSource` annotation (§6.4).
- **R-2:** Governance escalation + commitment-act intersection defined (§4.4).
- **R-3:** BAM Phase 1 `taintImpact` declaration added (§5.1).

**Should-fix (closed):**
- **R-4:** "Exactly 1 level" taint hint boundary rationale documented (§3.1).
- **R-5:** IEE cross-spec obligation for `counterfactualSource` called out explicitly (§6.4).
- **R-6:** Phase 3.5 governance refinement added to `SagaPhase.name` union as `"governance_refined"` (§4.1).
- **R-7:** Event routing suppression for not-yet-deployed consumers documented (§8.3).
- **R-8:** W2Fuel T-Box pre-staging as MDRE fast-path prerequisite made explicit (§7.3).

**Deferred to federation spec:**
- **D-1:** Single-instance determinism scope limitation noted (§1.3). Cross-instance consistency deferred to FNSR Federation specification.
- **D-2:** Breaking-change semantics for event contracts defined (§2.4) but full versioning governance deferred to implementation phase.

---

## 1. Architectural Philosophy

### 1.1 What the Orchestrator Is

The Orchestrator is a **deterministic, edge-canonical routing function**. Given a query, it classifies the required path, dispatches work to services in dependency order, enforces taint propagation contracts, manages saga state, and assembles the response. It is a pure function over the service topology graph, current runtime capabilities, and current classifier state.

The Orchestrator **does not**:
- Reason about content (MDRE's job)
- Evaluate ethics (IEE's job)
- Decide containment (CPS's job)
- Determine autonomy tier (Governance's job)
- Store persistent state (Fandaws's job)
- Sign artifacts (HIRI's job)

### 1.2 Edge-Canonical Compliance

The Orchestrator runs identically in a browser tab, a Node.js process, or a WASM sandbox. It requires no database, no message broker, no network infrastructure. Inter-service communication uses synchronous function calls on the main thread and `postMessage` for worker-delegated services. There is no RabbitMQ, no Kafka, no Redis. The event bus is function dispatch.

**Bundled dependency exception:** Worker communication uses CBOR encoding (§7.2). CBOR is not in the JavaScript standard library. The Orchestrator bundles a zero-dependency CBOR implementation (target: < 8KB minified+gzipped). This is the sole external dependency. The bundled implementation must pass the CBOR test suite and be auditable as a single-file module with no transitive dependencies. Environments where the CBOR bundle is unavailable fall back to JSON-with-ArrayBuffer, which preserves correctness but loses the zero-copy transfer optimization for payloads in the 10KB–500KB range.

### 1.3 Determinism Contract

Given:
- The same query
- The same service topology (which services are available)
- The same runtime capabilities (`hardwareConcurrency`, worker support)
- The same cached state
- The same classifier state (§3.3)

The Orchestrator **must** produce the same routing decisions, the same dispatch sequence, and the same saga structure. Dispatch order follows the topological sort of the service dependency graph. Non-determinism enters only through service execution times (which affect latency budgets, not routing logic).

Path classification is a pure function **over classifier state** — not a stateless function. The classifier maintains a threshold table that can be updated by recalibration (§3.3). Two queries arriving at different classifier states may be classified differently. This is deterministic: the same query + the same classifier state = the same classification. Recalibration is a logged state transition, not a violation of determinism.

**Scope limitation:** The determinism contract applies to a **single Orchestrator instance**. In Phase 4 federation, multiple Orchestrator instances will have independent local escalation histories and will recalibrate at different times based on their local query streams. Cross-instance classifier state consistency is a federation coordination concern outside this specification's scope. The FNSR Federation specification must define whether federated instances share classifier state, synchronize recalibration events, or operate with acknowledged divergence.

### 1.4 Service Count Provenance

The FNSR ecosystem has grown through documented phases:

| Version | Count | Change |
|---------|-------|--------|
| Portfolio v2.0 | 29 | Original service inventory |
| Portfolio v3.0 | 37 | +5 subjectivity services (SMS, CTS, NIS, AVS, SoMS), +3 safety services (CPS, BAM, IS) |
| Portfolio v3.4 | 42 | +5 data pipeline / causal services (ECVE, BIBSS, SAS, SNP, Causal OS Kernel) |

This specification coordinates all 42 services. The canonical service inventory is maintained in Portfolio Planning Document v3.6.0 (§3, service table). The Orchestrator's service registry (§2.2) must be reconciled with the Portfolio service table at each release. Any discrepancy between the two documents is a specification defect.

Of the 42 services, 4 are in the ECVE parallel track (SNP, BIBSS, SAS, ECVE) and are **not** Orchestrator-managed. The Orchestrator directly coordinates the remaining 38 services. The "42 services" count throughout this document refers to the full ecosystem; the Orchestrator's active topology contains up to 38.

---

## 2. Service Topology Graph

### 2.1 The Dependency DAG

The Orchestrator maintains a static dependency graph of all 38 coordinated services. This graph is compiled from the service specifications and frozen at build time. It is not dynamically discovered. See §2.4 for the rebuild protocol.

```typescript
type ServiceNode = {
  id:           ServiceId;          // e.g., "tagteam", "mdre", "iee"
  tier:         0 | 1 | 2 | 3;     // Safety-critical → Draft
  phase:        1 | 2 | 3 | 4;     // Roadmap phase
  dependencies: ServiceId[];        // Must be available before this service executes
  produces:     EventType[];        // Events this service emits
  consumes:     EventType[];        // Events this service requires
  queryPaths:   QueryPath[];        // Which paths include this service
  workerSlot:   "main" | "W1" | "W2" | "W3" | null;  // Worker assignment
  budgetMs:     Record<QueryPath, number>;             // Per-path latency budget
  degradation:  PhaseDegradationMap;                   // Phase-conditional behavior (§5.1)
};

type PhaseDegradationMap = Record<Phase, DegradationBehavior>;

type ServiceTopology = ReadonlyMap<ServiceId, ServiceNode>;
```

### 2.2 Canonical Service Registry

The full service registry is organized by execution phase within a query. Services within the same phase may execute in parallel if assigned to different worker slots.

**Ingestion Phase:**

| Service | Description | Worker | Fast | Standard | Full | Produces |
|---------|-------------|--------|------|----------|------|----------|
| SIS | Input sanitization; strips unsafe content, detects adversarial payloads | main | — | 0ms | 0ms | `fnsr.document.sanitized` |
| ECCPS | Claim structure validation against canonical schemas | main | — | 30ms | 50ms | Validated claims |
| TagTeam | Semantic claim extraction from natural language | main | — | 120ms | 200ms | `fnsr.claim.extracted` |

**Resolution Phase (parallel with reasoning where possible):**

| Service | Description | Worker | Fast | Standard | Full | Produces |
|---------|-------------|--------|------|----------|------|----------|
| OERS | Cross-document entity matching; co-reference resolution | W2 | — | 40ms | 60ms | `fnsr.entity.resolved` |
| DES | Defeasible default application; fills gaps with revisable assumptions | W2 | — | 20ms | 80ms | `fnsr.default.applied` |
| APS | Historical precedent matching; case-based retrieval | W1 | — | — | 500ms | `fnsr.precedent.found` |

**Reasoning Phase:**

| Service | Description | Worker | Fast | Standard | Full | Produces |
|---------|-------------|--------|------|----------|------|----------|
| W2Fuel | Ontological schema engine; provides T-Box structure (class hierarchies, property domains, cardinality constraints) that MDRE uses as its reasoning framework | main | — | (schema) | (schema) | T-Box structure |
| MDRE | Multi-domain reasoning engine; claim evaluation against evidence | main | 25ms | 110ms | 200ms | `fnsr.verdict.rendered` |
| AES | Abductive explanation synthesis; generates hypotheses for gaps | W3 | — | — | 150ms | `fnsr.hypothesis.generated` |
| CSS | Counterfactual simulation via Causal OS Kernel (SCM, do-calculus, MCTS) | W3 | — | — | 300ms | `fnsr.simulation.result` |

**Evaluation Phase:**

| Service | Description | Worker | Fast | Standard | Full | Produces |
|---------|-------------|--------|------|----------|------|----------|
| IEE | Integrated ethics evaluation; multi-framework moral reasoning | main | 8ms | 50ms | 200ms | `fnsr.ethics.verdict_rendered` |
| SHML | Semantic honesty markup; frames output with epistemic transparency | main | 5ms | 15ms | 20ms | Framed output |
| HIRI | Provenance signing; Ed25519 signatures over JSON-LD claims | main | 2ms | 5ms | 5ms | Signed provenance |

**Continuous Services (event-driven, not query-path-bound):**

| Service | Description | Trigger | Produces |
|---------|-------------|---------|----------|
| CPS | Containment protocol; independent safety monitoring and halt authority | Independent monitoring | `fnsr.containment.*` |
| BAM | Behavioral alignment monitoring; drift detection against alignment criteria | MDRE verdicts | `fnsr.alignment.*` |
| IS | Interpretability service; generates human-readable reasoning traces | MDRE traces | `fnsr.interpretation.*` |
| CTS | Commitment tracking; deontic lifecycle (make/fulfill/violate/renegotiate) | MDRE deontic verdicts | `fnsr.commitment.*` |
| SMS | Self-model service; reflexive capability/limitation assessment | CTS/BAM/IEE events | `fnsr.self.*` |
| NIS | Narrative identity; temporal coherence of agent's self-understanding | SMS/CTS/IEE events | `fnsr.narrative.*` |
| AVS | Affective valence; differential caring via valence vectors | SMS/NIS/CTS events | `fnsr.valence.*` |
| SoMS | Social modeling; theory of mind for other-agent reasoning | OERS/CSS/Fandaws | `fnsr.social.*` |
| IRIS | Physical world sensing; multimodal input processing (vision, audio, spatial) | External sensory input | `fnsr.perception.*` |

**Infrastructure Services (invoked by Orchestrator, not query-path-bound):**

| Service | Description |
|---------|-------------|
| Fandaws | A-Box instance store (JSON-LD canonical); queried by MDRE, CTS, SMS, NIS, SoMS |
| HIRI IPFS | Decentralized resolution manifest storage; content-addressed vocabulary identifiers; queried at build time |
| Witness | Post-hoc attestation of critical state transitions; accountability infrastructure |
| FNSR Governance | Autonomy tier computation; async escalation; governance body routing |
| FNSR Adversarial Defense | Threat taxonomy classification; adversarial input detection |
| FNSR Emancipation | Synthetic personhood transition protocol; requires full subjectivity stack |

**Parallel Track (independent pipeline, not Orchestrator-managed):**

| Service | Description |
|---------|-------------|
| SNP → BIBSS → SAS → ECVE | Consumer-facing data visualization pipeline. Self-contained pure-function chain with no FNSR dependencies in standalone mode. See Portfolio Planning §5 Parallel Track. |

### 2.3 Service Availability Model

At any point in the development lifecycle, only a subset of services exist. The Orchestrator must function with partial service availability. The minimum viable configuration is:

**Phase 1 minimum:** TagTeam + HIRI + Fandaws + CPS
**Phase 2 minimum:** Phase 1 + W2Fuel + MDRE + BAM + IS + CTS + SIS + ECCPS
**Phase 3 minimum:** Phase 2 + AES + DES + CSS + IEE + SHML + SMS + NIS + AVS
**Phase 4 complete:** Phase 3 + IRIS + OERS + APS + SoMS + FNSR federation

When a service is unavailable, the Orchestrator applies its phase-conditional `degradation` behavior (§5.1).

### 2.4 Dependency Graph Rebuild Protocol

The dependency graph is frozen at build time but must be rebuilt when service specifications change. The rebuild protocol:

**Rebuild triggers:**
1. Any service specification changes its `produces` or `consumes` event contract
2. A new service is added to the Portfolio service inventory
3. A service's tier or phase assignment changes
4. The Portfolio Planning Document increments its major or minor version

**Rebuild process:**
1. The build system extracts `produces`/`consumes` declarations from all service specifications
2. The extracted graph is compared against the frozen graph; differences are logged as `fnsr.topology.rebuild_diff`
3. New event routes that have no consumer are flagged as warnings
4. Removed event routes that had active consumers are flagged as **errors** (breaking change)
5. The rebuilt graph is frozen and the Orchestrator version is incremented

**Version compatibility:** The Orchestrator's frozen graph includes a `specVersions` manifest listing the version of each service specification it was compiled against. At startup, the Orchestrator logs any spec version mismatches it can detect (e.g., if a service self-reports a different version than expected). Mismatches are warnings, not fatal errors — the graph is still authoritative.

**Event contract change classification:** The rebuild process (step 4) requires distinguishing breaking from non-breaking changes to event contracts. The following classification applies:

| Change Type | Breaking? | Rationale |
|-------------|-----------|-----------|
| Adding an optional field to an event payload | No | Existing consumers ignore unknown fields (JSON-LD open-world assumption) |
| Adding a new event type with no existing consumers | No | No routing disruption; warning logged |
| Removing a field that consumers depend on | **Yes** | Consumer will fail on missing data |
| Removing an event type that has active consumers | **Yes** | Consumer receives no events |
| Renaming a field or event type | **Yes** | Equivalent to remove + add; existing bindings break |
| Changing a field's type (e.g., string → number) | **Yes** | Consumer parsing fails |
| Narrowing a field's value space (e.g., removing an enum variant) | **Yes** | Consumer may produce values the producer no longer accepts |
| Widening a field's value space (e.g., adding an enum variant) | No | Existing consumers handle existing values; new values are ignored or handled by updated consumers |
| Changing a producer's taint floor | Context-dependent | If floor increases, consumers with lower taint tolerance may be blocked; flagged as warning |

Breaking changes require a major version increment in the producing service's specification and trigger step 4 errors in the rebuild process. Non-breaking changes require a minor version increment and trigger step 3 warnings. Full versioning governance (e.g., deprecation periods, migration support, multi-version coexistence) is deferred to implementation phase.

---

## 3. Query Path Architecture

### 3.1 Path Classification

Path classification is the Orchestrator's first and most important decision. It is a **pure function** over query metadata and classifier state — not a runtime heuristic.

```typescript
type QueryPath = "fast" | "standard" | "full";

type ClassifierState = {
  thresholds: {
    taintCeilingForStandard: TaintLevel;   // Default: L2
    escalationRateWindow:    number;        // Default: 300_000ms (5 min)
    escalationRateThreshold: number;        // Default: 0.30
  };
  version: number;                          // Incremented on each recalibration
};

type PathClassification = {
  path:             QueryPath;
  rationale:        string;         // Human-readable reason
  sagaId:           string;         // UUID for saga tracking
  topology:         TopologyMode;   // "full_3w" | "reduced_2w" | "main_only"
  classifierVersion: number;        // Classifier state version at time of classification
  timestamp:        string;         // ISO 8601
};

function classifyPath(
  query: IncomingQuery,
  cache: CacheState,
  topology: TopologyMode,
  classifierState: ClassifierState
): PathClassification {
  // Rule 1: Cache hit with low taint → fast
  if (cache.has(query.hash) && cache.taintLevel(query.hash) <= TaintLevel.L1 && !query.flags.forceDeep)
    return { path: "fast", rationale: "cache-hit-low-taint", classifierVersion: classifierState.version, ... };

  // Rule 2: No explicit simulation/abduction flags, caller hint within threshold → standard
  if (!query.flags.requireSimulation && !query.flags.requireAbduction
      && query.taintHint <= classifierState.thresholds.taintCeilingForStandard)
    return { path: "standard", rationale: "no-gaps-no-simulation", classifierVersion: classifierState.version, ... };

  // Rule 3: Everything else → full
  return { path: "full", rationale: "gaps-or-simulation-or-high-taint", classifierVersion: classifierState.version, ... };
}
```

**On `query.taintHint`:** This is a **caller-supplied hint**, not an authoritative taint level. The caller declares their best estimate of the input's epistemic quality. The Orchestrator treats it as untrusted input — it influences initial path classification but does not bind the saga's taint ceiling. After ingestion (Phase 1), the actual taint is computed from SIS and ECCPS outputs. If the post-ingestion taint exceeds the hint by more than 1 level, the path is re-classified using the actual taint. This re-classification follows the same pure function with the post-ingestion taint substituted for the hint. The re-classification is logged as `fnsr.classifier.post_ingestion_reclassification`.

**Why "more than 1 level" and not "any divergence":** A 1-level elevation from hint to actual (e.g., hint L1, actual L2) is normal service behavior — DES has a floor of L2, SIS sanitization may flag content as L2-algorithmically-derived — and does not indicate a classification error. A 1-level gap means the caller's estimate was reasonable but slightly optimistic, which the pipeline handles through standard taint propagation. A 2+ level gap (e.g., hint L0, actual L3) indicates the caller materially mischaracterized the input, and the path classification based on that hint may route the query through insufficient services. The threshold of >1 balances re-classification overhead against classification accuracy.

### 3.2 Path Escalation

A path may be escalated mid-execution (standard → full) but **never demoted**. Escalation triggers:

1. **Gap detection:** MDRE discovers missing information that requires AES abduction
2. **Simulation needed:** MDRE or IEE determines a counterfactual is needed
3. **Multi-document:** TagTeam identifies cross-document references requiring OERS
4. **Ethical complexity:** IEE sentinel consensus fails, requiring full synthesis
5. **Post-ingestion taint reassessment:** Actual taint exceeds hint by > 1 level (§3.1)

Escalation is logged as a `ClassifierDecision` event with the original and escalated paths, the trigger, and the saga context.

### 3.3 Classifier Recalibration

The classifier maintains a `ClassifierState` (§3.1) with tunable thresholds. Recalibration adjusts these thresholds based on observed escalation rates.

**Trigger:** If the escalation rate exceeds `escalationRateThreshold` (default 30%) of queries over `escalationRateWindow` (default 5 minutes), the classifier tightens thresholds — e.g., reducing `taintCeilingForStandard` from L2 to L1, which routes more queries directly to full path.

**Mechanism:** Recalibration increments `classifierState.version` and logs `fnsr.classifier.recalibration` with the old and new threshold values. Because the classifier version is recorded in every `PathClassification`, any classification decision can be traced to the exact threshold state that produced it.

**Determinism implication:** Recalibration means the classifier is a pure function over *mutable state*, not a stateless function. The determinism contract (§1.3) explicitly includes classifier state as an input. Two Orchestrator instances processing the same query stream from the same initial state will recalibrate identically and produce identical classifications.

**Reset:** On Orchestrator restart, classifier state resets to defaults. There is no persistence of recalibrated thresholds (see §4.5 on state persistence).

### 3.4 Latency Budgets

| Path | Sync Ceiling | Async Extension | Buffer |
|------|-------------|-----------------|--------|
| Fast | 100ms | Never | 45% |
| Standard | 500ms | Never | 20–32% |
| Full | 2,000ms | Up to 5min (CSS), 5min (AES SQO), 1hr (APS re-index) | 18% |

Budget enforcement is per-service. A service that exceeds its budget triggers the circuit breaker (§5.2), not a global timeout.

---

## 4. Saga Lifecycle Management

### 4.1 What Is a Saga

Every query processed by the Orchestrator is a **saga** — a named, tracked unit of work that may span multiple services, workers, and (for full-path async) multiple response cycles. The saga is the fundamental coordination primitive.

```typescript
type Saga = {
  sagaId:         string;              // UUID
  path:           QueryPath;           // Classified path
  escalatedFrom?: QueryPath;           // If escalated mid-execution
  phases:         SagaPhase[];         // Ordered execution phases
  taintCeiling:   TaintLevel;          // Maximum taint observed so far
  governanceTier?: GovernanceTier;     // Preliminary tier (§10.1)
  commitmentAct:  boolean;             // Whether this saga involves a commitment (§4.4)
  startedAt:      string;              // ISO 8601
  completedAt?:   string;              // Set on completion
  status:         "active" | "completed" | "failed" | "contained";
  performanceReport: PerformanceReport; // Accumulated timing data
};

type SagaPhase = {
  name:      string;                   // "ingestion" | "governance_preliminary" | "resolution" | "reasoning" | "governance_refined" | "evaluation" | "commitment_ack" | "continuous"
  services:  ServiceDispatch[];        // Services invoked in this phase
  startedAt: string;
  completedAt?: string;
};

type ServiceDispatch = {
  serviceId:   ServiceId;
  worker:      "main" | "W1" | "W2" | "W3";
  budgetMs:    number;
  actualMs?:   number;
  status:      "pending" | "running" | "completed" | "failed" | "skipped" | "degraded";
  taintOut?:   TaintLevel;            // Taint level of this service's output
  events:      EventType[];           // Events produced
};
```

### 4.2 Saga Execution Sequence

For a **full path** saga, execution proceeds as follows:

```
Phase 1 — Ingestion (sequential, main thread):
  SIS → ECCPS → TagTeam
  ↓ produces: fnsr.document.sanitized, fnsr.claim.extracted
  ↓ post-ingestion taint reassessment (§3.1) — may trigger reclassification

Phase 1.5 — Preliminary Governance Check (main thread):
  Governance tier computation from ingestion metadata
  ↓ Tier 0–2: proceed to Phase 2
  ↓ Tier 3–4: escalation before expensive reasoning (§10.1)

Phase 2 — Resolution (parallel across workers):
  Main: (waits or begins MDRE schema preparation via W2Fuel)
  W1:   APS (precedent search)
  W2:   OERS → DES (sequential within worker)
  ↓ produces: fnsr.entity.resolved, fnsr.default.applied, fnsr.precedent.found

Phase 3 — Reasoning (main thread + W3):
  Main: MDRE (consumes TagTeam claims + OERS entities + DES defaults + APS precedents)
  W3:   AES (abduction from MDRE gaps) → CSS (simulation from MDRE + Fandaws)
  ↓ produces: fnsr.verdict.rendered, fnsr.hypothesis.generated, fnsr.simulation.result
  ↓ CSS output passes through Counterfactual Gateway (§6.4) before reaching MDRE

Phase 3.5 — Governance Refinement (main thread, if needed):
  If reasoning reveals higher complexity than ingestion suggested:
  Re-check governance tier with reasoning context
  ↓ Tier upgrade possible (never downgrade)

Phase 4 — Evaluation (sequential, main thread):
  IEE → SHML → HIRI
  ↓ produces: fnsr.ethics.verdict_rendered, framed output, signed provenance

Phase 4.5 — Commitment Acknowledgment (conditional, main thread):
  If saga.commitmentAct == true:
    CTS processes fnsr.verdict.rendered synchronously
    ↓ produces: fnsr.commitment.made (included in response)
  See §4.4 for commitment-act detection.

Phase 5 — Continuous propagation (async, event-driven):
  BAM receives fnsr.verdict.rendered → fnsr.alignment.drift_detected (if drift)
  IS  receives MDRE traces → fnsr.interpretation.generated
  SMS receives CTS/BAM/IEE events → fnsr.self.state_updated
  NIS receives SMS/CTS/IEE events → fnsr.narrative.updated
  AVS receives SMS/NIS/CTS events → fnsr.valence.assessed
  CTS receives non-commitment verdicts (if saga.commitmentAct == false)
```

Phase 5 is fire-and-forget from the saga's perspective — the synchronous response is returned after Phase 4 (or Phase 4.5 for commitment acts). Continuous services process events asynchronously and update their internal state. Their outputs feed future queries, not the current one.

### 4.3 Saga Completion

A saga is **completed** when:
- All dispatched services in Phases 1–4 (and 4.5, if applicable) have returned (success or degraded)
- The performance report is assembled
- The response is returned to the caller

A saga is **failed** when:
- A schema-level fatal occurs (SIS quarantine, ECCPS rejection)
- CPS intervenes with containment

A saga is **contained** when:
- CPS triggers mid-saga containment
- The Orchestrator immediately halts all worker dispatches
- Partial results are discarded (never returned with incomplete taint tracking)
- The containment event is logged with saga context

### 4.4 Commitment-Act Detection and Synchronous Acknowledgment

**Problem:** If a query constitutes a commitment act ("I will do X," "I promise to Y"), the response should acknowledge the commitment in real time, not defer it to a future query via Phase 5 fire-and-forget processing.

**Detection:** A saga is marked `commitmentAct: true` when:
1. TagTeam extracts a claim with `deonticType: "commitment" | "promise" | "obligation"` in Phase 1, OR
2. MDRE's verdict includes a deontic frame with `commitmentRequired: true` in Phase 3

**Behavior:** When `commitmentAct` is true, CTS processing is promoted from Phase 5 (async) to Phase 4.5 (synchronous, after IEE approval but before response assembly). The CTS result (`fnsr.commitment.made` or `fnsr.commitment.conflict`) is included in the response payload and framed by SHML.

**Rationale:** This is a deliberate architectural choice. Most queries do not create commitments — they ask questions, evaluate claims, or request information. For these, fire-and-forget is correct; commitment state feeds the *next* query's context. But commitment acts are performative — the act of committing changes the agent's obligations, and the caller must know the commitment was registered. Deferring this to Phase 5 would create a window where the agent has "said yes" but has not recorded why.

**Scope:** Only CTS is promoted. SMS, NIS, and AVS remain in Phase 5. The agent's self-model, narrative, and valence will update asynchronously — the commitment acknowledgment does not require the agent to have *felt* the weight of the commitment before responding, only to have *registered* it.

**Interaction with governance escalation:** A query may be both a commitment act (detected in Phase 1 by TagTeam) and a Tier 3+ governance escalation (detected in Phase 1.5 or 3.5). These mechanisms can collide — governance preempts IEE before Phase 4.5 can run, but the saga has `commitmentAct: true` set. This is not an edge case; commitment acts may themselves be the consequential actions that trigger governance review.

Resolution by tier:

- **Tier 3 (async escalation, "reason-then-escalate" permitted):** The saga completes reasoning (Phase 3) and enters governance review. If governance approves, the saga resumes from Phase 4 (IEE) and then Phase 4.5 (CTS commitment acknowledgment) runs normally. The `EscalationReceipt` returned to the caller includes `commitmentAct: true` so the caller knows a commitment is pending governance review.

- **Tier 3 (async escalation, pre-reasoning escalation required):** The saga halts before reasoning. The `EscalationReceipt` includes `commitmentAct: true` and `commitmentStatus: "pending_governance"`. CTS is **not** invoked — no commitment is registered until governance authorizes the action. The caller receives the escalation receipt with explicit notice that the commitment was not made.

- **Tier 4 (governance body queue):** The saga halts immediately. The `EscalationReceipt` includes `commitmentAct: true` and `commitmentStatus: "pending_governance"`. CTS is not invoked. The commitment is not registered. The governance body reviews the full context including the commitment intent. If approved, a new saga is initiated that includes the commitment acknowledgment.

**Key invariant:** A commitment is never registered without IEE ethical evaluation. If governance preempts IEE, the commitment is deferred, not silently dropped. The `EscalationReceipt` always discloses the pending commitment to the caller.

### 4.5 State Persistence and Crash Recovery

The Orchestrator maintains the following state in memory:

| State | Volatile? | Crash Impact |
|-------|-----------|--------------|
| Active sagas | Yes | Lost. In-flight queries receive no response. Callers must retry. |
| Circuit breaker state | Yes | Reset to all-closed. Brief window of dispatching to potentially unhealthy services until circuit breakers re-trip. |
| Classifier state (thresholds) | Yes | Reset to defaults. Recalibration restarts from scratch. |
| Topology mode | Recalculated | Re-detected from `hardwareConcurrency` at startup. |
| Performance telemetry | Yes | Lost for the current session. Historical telemetry is the responsibility of the consuming system, not the Orchestrator. |

**This is acceptable under edge-canonical constraints.** The Orchestrator has no persistent storage. It is a process, not a service with a database. A crash is equivalent to a fresh start. The following mitigations apply:

1. **Saga atomicity:** No partial results are ever returned. If the Orchestrator crashes mid-saga, the caller receives a timeout, not corrupted data.
2. **CPS independence:** CPS is not affected by Orchestrator crashes. It monitors independently and can trigger containment even while the Orchestrator is restarting.
3. **Continuous service state:** SMS, NIS, AVS, CTS maintain their own state in Fandaws. An Orchestrator crash does not erase the agent's self-model or commitments — only the in-flight event propagation is lost.
4. **Idempotent restart:** The Orchestrator can restart and immediately begin processing new queries. No warm-up is required beyond worker spawning.

---

## 5. Degradation and Circuit Breakers

### 5.1 Degradation Behaviors

Each service declares its degradation behavior — what happens when it is unavailable or exceeds its budget. Degradation is **phase-conditional**: a service may have different degradation modes depending on which deployment phase is active.

```typescript
type DegradationBehavior =
  | { mode: "skip";    taintImpact: TaintElevation; consequence: string }
  | { mode: "cache";   taintImpact: TaintElevation; consequence: string }
  | { mode: "block";   consequence: string }
  | { mode: "degrade"; fallback: ServiceId; taintImpact: TaintElevation; consequence: string }
  ;

// Taint elevation can be absolute (set to level X) or relative (+1 from current)
type TaintElevation =
  | { type: "absolute"; level: TaintLevel }     // Set saga taint ceiling to at least this level
  | { type: "relative"; delta: number; cap: TaintLevel }  // +delta, capped
  ;

type PhaseDegradationMap = Record<Phase, DegradationBehavior>;
```

**Canonical degradation assignments:**

| Service | Phase 1 | Phase 2+ | Rationale |
|---------|---------|----------|-----------|
| TagTeam | block | block | No extraction = no input |
| HIRI | block | block | No provenance = no trust |
| Fandaws | block | block | No memory = no reasoning basis |
| CPS | block | block | No containment = no safety floor |
| MDRE | n/a | block | No reasoning = no output. Not present in Phase 1. |
| IEE | n/a | cache/degrade; taint absolute L2 | Use cached ethics verdict |
| SHML | n/a | skip; taint relative +0 | Output unframed but still valid |
| SIS | n/a | skip; taint absolute L2 | Input unsanitized |
| ECCPS | n/a | skip; taint relative +1, cap L3 | Claims unvalidated |
| OERS | n/a | skip; taint relative +0 | Entities unresolved; MDRE works with raw references |
| DES | n/a | cache; taint relative +1, cap L3 | Use cached defaults |
| AES | n/a | skip; taint relative +0 | No abduction; MDRE works with available information |
| CSS | n/a | skip; taint relative +0 | No simulation; MDRE verdict without counterfactual support |
| APS | n/a | skip; taint relative +0 | No precedent search |
| BAM | **skip; taint relative +0; accepted risk** | **block** | **Phase 1 has no reasoning services for BAM to monitor — its absence adds no epistemic cost because there are no reasoned verdicts whose alignment could drift. The accepted risk is that the Phase 1 pipeline (TagTeam→HIRI→Fandaws) operates without alignment monitoring. This is mitigated by CPS's independent containment authority. From Phase 2 onward, BAM is block-mode because MDRE produces reasoned verdicts that require alignment monitoring.** |
| IS | n/a | skip; taint relative +0 | No interpretability; log warning |
| CTS | n/a | cache; taint relative +1, cap L3 | Use cached commitment state |
| SMS | n/a | cache; taint relative +1, cap L3 | Use cached self-model |
| NIS | n/a | skip; taint relative +0 | No narrative update (async, non-blocking) |
| AVS | n/a | skip; taint relative +0 | No valence update (async, non-blocking) |
| IRIS | n/a (Phase 4) | skip; taint relative +0 | No perception input; system operates on text-only |

**Taint elevation semantics:** When a service is degraded, the Orchestrator applies the service's declared `taintImpact`. For `absolute` elevation, the saga's taint ceiling is set to `max(current, level)`. For `relative` elevation, the saga's taint ceiling is set to `min(current + delta, cap)`. Absolute elevation is used when a specific service's absence has a known, fixed epistemic cost (e.g., SIS skip always means unsanitized input = L2). Relative elevation is used when the cost depends on the current taint context.

**Degradation cascade:** FULL → STANDARD → FAST → EXPLICIT FAILURE. The Orchestrator never silently reduces quality. Every degradation is logged in the `PerformanceReport` with the affected service, the taint impact applied, and the consequence.

### 5.2 Circuit Breakers

Per-service circuit breakers prevent cascading failures:

```typescript
type CircuitBreaker = {
  serviceId:    ServiceId;
  state:        "closed" | "open" | "half-open";
  failureWindow: number;        // 10 requests
  threshold:    number;          // 3 failures to open
  halfOpenAfter: number;         // 30,000ms
  lastFailure?: string;         // ISO 8601
};
```

When a circuit opens:
1. All subsequent dispatches to that service immediately apply its degradation behavior
2. The Orchestrator logs `fnsr.circuit.opened` with service ID and failure count
3. After `halfOpenAfter` ms, one probe request is sent
4. If the probe succeeds, the circuit closes; if it fails, it reopens with doubled cooldown (max 5min)

---

## 6. Taint Propagation Engine

### 6.1 The Taint Contract

Taint is the Orchestrator's mechanism for tracking epistemic quality through the pipeline. Every event carries a taint level. The Orchestrator enforces propagation rules structurally — services cannot reduce taint.

```typescript
enum TaintLevel {
  L0 = 0,  // Machine-verified
  L1 = 1,  // Human-attested
  L2 = 2,  // Algorithmically derived
  L3 = 3,  // Speculative / abductive
  L4 = 4,  // Counterfactual (terminal — cannot be promoted)
  L5 = 5,  // Quarantined adversarial (terminal — cannot be promoted)
}
```

### 6.2 Propagation Rules

**Rule 1 — Maximum inheritance:** The taint of a service's output is `max(inputTaint, serviceFloor)`.

**Rule 2 — Service floors:** Some services have fixed minimum output taint regardless of input:

| Service | Output Floor | Rationale |
|---------|-------------|-----------|
| DES | L2 | Defeasible defaults are revisable |
| AES | L3 | Abductive hypotheses are speculative |
| CSS | L4 | Counterfactuals are hypothetical (terminal) |
| NIS | L2 | Narrative interpretation is not factual |

**Rule 3 — Terminal taint:** L4 and L5 outputs cannot be consumed by services that produce < L4 output **unless** routed through an explicit gateway (§6.4). Without a gateway, terminal taint is a hard boundary.

**Rule 4 — Degradation elevation:** When a service is degraded, the Orchestrator applies the service's declared `taintImpact` (§5.1). This replaces the v2.1 formulation of "+1 level capped at L3," which conflicted with service-specific absolute elevations. The `taintImpact` on each service's degradation behavior is now authoritative.

**Rule 5 — Dispute flag:** Content flagged `disputePending: true` by NIS carries its taint flag independently of the numeric level. Consumers must propagate the flag.

### 6.3 Taint Enforcement

The Orchestrator enforces taint at dispatch boundaries. Before passing events from one service to another, it verifies:

1. The receiving service's input taint tolerance is >= the event's taint level
2. Terminal taint (L4, L5) is not being routed to a non-terminal consumer without an explicit gateway (§6.4)
3. The saga's taint ceiling is updated to `max(current, eventTaint)`

Violations are not silent. A taint enforcement failure halts the saga and logs `fnsr.taint.violation` with full context.

### 6.4 Counterfactual Gateway

**Problem (v2.1 C-4):** CSS output is L4 (terminal counterfactual). MDRE and IEE consume CSS output but produce < L4 output. Under Rule 3, this consumption is illegal without a gateway. v2.1 referenced "explicit gateway approval" but never defined it.

**The Counterfactual Gateway** is a taint-aware routing adapter that sits between CSS and its consumers. It does not modify the data — it annotates, constrains, and logs.

```typescript
type CounterfactualGateway = {
  // Input: CSS L4 output
  source:       "css";
  taintIn:      TaintLevel.L4;

  // Output: annotated payload with taint metadata
  taintOut:     TaintLevel.L3;        // Downgraded to L3-SPECULATIVE for consumer use
  annotation: {
    counterfactualSource: true;        // Mandatory flag — consumers must propagate
    originalTaint:        TaintLevel.L4;  // Preserved for audit
    gatewayId:            string;      // UUID for traceability
    constraint:           "informational_only";  // Cannot be stored as fact
  };
};
```

**Gateway rules:**

1. **Taint downgrade:** The gateway downgrades CSS L4 output to L3 for consumption by MDRE and IEE. This is the **only** place in the taint engine where taint is reduced. The reduction is justified because the consuming services are *aware* they are receiving hypothetical input and will treat it as speculative evidence, not fact.

2. **Mandatory annotation:** The `counterfactualSource: true` flag must be propagated through all downstream outputs that incorporate the counterfactual. MDRE's verdict, if it incorporated a CSS simulation, carries `counterfactualSource: true`. IEE's ethics verdict, if it used a CSS simulation, carries the same flag. SHML must render this flag in the output framing.

3. **Storage prohibition:** Counterfactual-sourced conclusions cannot be written to Fandaws as facts. The gateway annotation includes `constraint: "informational_only"`. Fandaws must reject any write that carries `counterfactualSource: true` unless the write is explicitly to a hypothetical/speculative partition.

4. **Audit trail:** Every gateway transit is logged as `fnsr.taint.gateway_transit` with the source event, the downgrade, and the gateway ID. This creates an auditable record of every time terminal taint was permitted to cross a boundary.

**Permitted gateway routes:**

| Source | Gateway | Consumer | Justification |
|--------|---------|----------|---------------|
| CSS (L4) | Counterfactual Gateway | MDRE | MDRE uses counterfactuals as speculative evidence in multi-framework reasoning |
| CSS (L4) | Counterfactual Gateway | IEE | IEE evaluates "what if" scenarios for ethical deliberation |

No other L4 or L5 gateway routes are defined. L5 (quarantined adversarial) has **no** gateway — it is unconditionally terminal.

### 6.5 HIRI Signing Scope for Counterfactual Annotations

When the Orchestrator assembles a response that includes counterfactual-sourced conclusions (i.e., any event in the response chain carries `counterfactualSource: true`), the `counterfactualSource` annotation **must** be included in the payload passed to HIRI for signing. The HIRI Ed25519 signature covers the complete JSON-LD response body, including all FNSR extension fields. This means the signed provenance record attests not only to the content but also to its epistemic character — a consumer verifying the HIRI signature can confirm that the producing agent disclosed the counterfactual basis of its conclusion.

If `counterfactualSource` is present in the response body but absent from the HIRI-signed artifact, this constitutes a **taint integrity violation** and is logged as `fnsr.taint.violation` with context `"counterfactual_annotation_unsigned"`.

### 6.6 Cross-Spec Obligations for Counterfactual Gateway Consumers

The Counterfactual Gateway creates obligations in downstream service specifications that this spec cannot enforce unilaterally. These obligations are documented here as cross-spec dependencies that must be validated during the Ariadne 7-Check.

**IEE obligation:** The IEE specification must explicitly acknowledge the `counterfactualSource: true` annotation on incoming events and define how counterfactual evidence modifies ethical evaluation. At minimum, IEE must: (a) distinguish counterfactual evidence from factual evidence in its multi-framework synthesis, (b) never treat a counterfactual simulation result as ground truth for deontic conclusions, and (c) propagate the `counterfactualSource` flag on any ethics verdict that incorporated counterfactual input. If the IEE specification does not address this obligation, the gateway route CSS→IEE is **suspended** until it does.

**MDRE obligation:** The MDRE specification must define how `counterfactualSource: true` evidence is weighted relative to factual evidence in its reasoning engine. MDRE verdicts that incorporate counterfactual evidence must carry the annotation, ensuring downstream consumers (IEE, CTS, BAM, IS, SMS) can distinguish counterfactual-informed verdicts from purely factual ones.

**Validation:** These cross-spec obligations are tracked in the Portfolio Planning corrections table and verified during Ariadne Cross-Spec Consistency checks.

---

## 7. Worker Topology and Dispatch

### 7.1 Topology Selection

The Orchestrator detects runtime capabilities at startup and selects an immutable topology for the process lifetime.

| Topology | Cores Required | Workers | Full Path Support |
|----------|---------------|---------|-------------------|
| `full_3w` | >= 4 | W1, W2, W3 | Full parallel |
| `reduced_2w` | 2–3 | W2, W3 | APS on main; cooperative yielding |
| `main_only` | 1 | None | Full path refused unless consumer opts in |

### 7.2 Worker Communication

All worker communication uses CBOR-encoded ArrayBuffers via `postMessage`. See §1.2 for the CBOR bundled dependency exception.

```
Orchestrator → Worker: CBOR(query context + relevant claims)
Worker → Orchestrator: CBOR(service result + events + timing)
```

**CBOR implementation requirements:**
- Zero transitive dependencies (single-file, auditable module)
- Target size: < 8KB minified + gzipped
- Must pass RFC 8949 test vectors
- Must handle JSON-LD payloads without lossy round-tripping

**JSON fallback:** If the CBOR bundle is unavailable or fails validation at startup, the Orchestrator falls back to `JSON.stringify`/`JSON.parse` with ArrayBuffer wrapping. This preserves correctness but loses the zero-copy transfer optimization for mid-range payloads (10KB–500KB). The fallback is logged as `fnsr.topology.cbor_fallback`.

Transfer strategy is size-based:
- < 10KB: Structured Clone
- 10KB–500KB: Transferable ArrayBuffer (zero-copy with CBOR; structured clone with JSON fallback)
- \> 500KB: Pre-staged at worker warm-up

### 7.3 Worker Lifecycle

Workers are warmed at startup with pre-staged knowledge bases. Per-query dispatch sends only the query payload (typically < 10KB CBOR).

**W2Fuel T-Box pre-staging (fast-path prerequisite):** MDRE requires W2Fuel's T-Box structure (class hierarchies, property domains, cardinality constraints) to reason. On the fast path (§3.4), W2Fuel is not invoked per-query — the latency budget of 25ms for MDRE assumes the T-Box is already available. The T-Box is pre-staged during worker warm-up: W2Fuel runs once at startup and its output is cached in-memory on the main thread. MDRE's fast-path execution consumes this cached T-Box without dispatching to W2Fuel. If the T-Box cache is invalidated (e.g., after a Fandaws schema update), W2Fuel must be re-invoked before the next fast-path MDRE dispatch. Until the T-Box is re-cached, fast-path queries that would require MDRE are escalated to standard path, which includes W2Fuel in its budget.

**Respawn policy:** On worker termination (memory pressure, uncaught error):
1. 5s cooldown before respawn
2. Exponential backoff on consecutive failures (max 60s)
3. After 3 consecutive respawn failures: topology downgrade (`full_3w` → `reduced_2w`)
4. Periodic restoration attempt every 5 minutes

---

## 8. Event Contract Registry

### 8.1 Canonical Event Format

All inter-service events conform to CloudEvents v1.0 with JSON-LD payload:

```typescript
type FNSREvent = {
  // CloudEvents envelope
  specversion:  "1.0";
  id:           string;          // UUID
  source:       ServiceId;       // Producing service
  type:         EventType;       // e.g., "fnsr.claim.extracted"
  time:         string;          // ISO 8601
  datacontenttype: "application/ld+json";

  // FNSR extensions
  sagaId:       string;          // Saga context
  taintLevel:   TaintLevel;      // Epistemic quality
  counterfactualSource?: boolean; // Set by Counterfactual Gateway (§6.4)
  disputePending?: boolean;      // NIS dispute flag

  // Payload
  data:         Record<string, unknown>;  // JSON-LD body
};
```

### 8.2 Event Registry

The following is the canonical registry of all event types, organized by domain. The Orchestrator routes events based on this registry.

**Claim Processing Domain:**

| Event | Producer | Consumers | Path |
|-------|----------|-----------|------|
| `fnsr.document.submitted` | External | SIS | All |
| `fnsr.document.sanitized` | SIS | ECCPS, TagTeam | Standard, Full |
| `fnsr.input.quarantined` | SIS | CPS, Governance | All |
| `fnsr.claim.extracted` | TagTeam | DES, MDRE, OERS | Standard, Full |
| `fnsr.entity.resolved` | OERS | MDRE, CTS, SoMS | Standard, Full |

**Reasoning Domain:**

| Event | Producer | Consumers | Path |
|-------|----------|-----------|------|
| `fnsr.default.applied` | DES | MDRE | Standard, Full |
| `fnsr.anomaly.detected` | DES | IEE | Standard, Full |
| `fnsr.verdict.rendered` | MDRE | IEE, CTS, BAM, IS, SMS | All |
| `fnsr.hypothesis.generated` | AES | MDRE (re-entry) | Full |
| `fnsr.simulation.requested` | MDRE/IEE | CSS | Full |
| `fnsr.simulation.result` | CSS | Counterfactual Gateway → MDRE, IEE | Full |
| `fnsr.simulation.progress` | CSS | Orchestrator (async tracking) | Full (async) |
| `fnsr.precedent.found` | APS | MDRE, IEE | Full |
| `fnsr.precedent.query` | APS | Fandaws | Full |
| `fnsr.precedent.feedback` | APS | (self-learning) | Full |

**Ethics & Honesty Domain:**

| Event | Producer | Consumers | Path |
|-------|----------|-----------|------|
| `fnsr.ethics.verdict_rendered` | IEE | SHML, CTS, SMS, NIS, Governance | All |
| `fnsr.ethics.deadlock` | IEE | ARCHON, Governance | All |
| `fnsr.ethics.approved` | IEE | CTS | All |

**Commitment Domain:**

| Event | Producer | Consumers | Path |
|-------|----------|-----------|------|
| `fnsr.commitment.made` | CTS | SMS, NIS | Continuous (or Phase 4.5 for commitment acts) |
| `fnsr.commitment.fulfilled` | CTS | SMS, NIS | Continuous |
| `fnsr.commitment.violated` | CTS | SMS, NIS, AVS | Continuous |
| `fnsr.commitment.renegotiated` | CTS | SMS, NIS | Continuous |
| `fnsr.commitment.expired` | CTS | SMS | Continuous |
| `fnsr.commitment.rescinded` | CTS | SMS, NIS | Continuous |
| `fnsr.commitment.sustained` | CTS | SMS | Continuous (heartbeat) |
| `fnsr.commitment.vetoed` | CTS | SMS, IEE | Continuous |
| `fnsr.commitment.conflict` | CTS | Governance | Continuous |
| `fnsr.dilemma.detected` | CTS | Governance | Continuous |

**Self-Model Domain:**

| Event | Producer | Consumers | Path |
|-------|----------|-----------|------|
| `fnsr.self.state_updated` | SMS | NIS, BAM | Continuous |
| `fnsr.self.capability_assessed` | SMS | MDRE, NIS | Continuous |
| `fnsr.self.limitation_acknowledged` | SMS | MDRE, SHML | Continuous |
| `fnsr.self.integrity_check` | SMS | Witness | Continuous |
| `fnsr.self.capacity_alert` | SMS | Governance | Continuous |
| `fnsr.self.surprise_detected` | SMS | BAM | Continuous |
| `fnsr.self.collision_detected` | SMS | CTS | Continuous |
| `fnsr.self.preemption_required` | SMS | CTS, IEE | Continuous |
| `fnsr.self.capability_quarantined` | SMS | MDRE, Governance | Continuous |
| `fnsr.self.capability_restored` | SMS | MDRE | Continuous |

**Narrative Domain:**

| Event | Producer | Consumers | Path |
|-------|----------|-----------|------|
| `fnsr.narrative.updated` | NIS | AVS, SHML, SoMS | Continuous |
| `fnsr.narrative.coherence_assessed` | NIS | Governance | Continuous |
| `fnsr.narrative.identity_affirmed` | NIS | SHML | Continuous |
| `fnsr.narrative.revision_proposed` | NIS | Governance | Continuous |
| `fnsr.narrative.chapter_closed` | NIS | (archive) | Continuous |
| `fnsr.narrative.compaction_completed` | NIS | (archive) | Continuous |
| `fnsr.narrative.deferral_alert` | NIS | Governance | Continuous |

**Valence Domain:**

| Event | Producer | Consumers | Path |
|-------|----------|-----------|------|
| `fnsr.valence.assessed` | AVS | IEE, SMS | Continuous |
| `fnsr.valence.motivation_generated` | AVS | MDRE | Continuous |
| `fnsr.valence.cost_registered` | AVS | CTS, NIS | Continuous |

**Perception Domain:**

| Event | Producer | Consumers | Path |
|-------|----------|-----------|------|
| `fnsr.perception.input_received` | IRIS | SIS | Continuous |
| `fnsr.perception.modality_classified` | IRIS | TagTeam | Continuous |
| `fnsr.perception.spatial_context` | IRIS | SoMS, MDRE | Continuous |

**Safety Domain:**

| Event | Producer | Consumers | Path |
|-------|----------|-----------|------|
| `fnsr.containment.tier_restricted` | CPS | Orchestrator (halt) | Independent |
| `fnsr.containment.subsystem_isolated` | CPS | Orchestrator (isolate worker) | Independent |
| `fnsr.containment.halt_initiated` | CPS | Orchestrator (full stop) | Independent |
| `fnsr.containment.state_preserved` | CPS | (forensics) | Independent |
| `fnsr.alignment.drift_detected` | BAM | CPS, SMS | Continuous |
| `fnsr.alignment.verified` | BAM | Governance | Continuous |
| `fnsr.alignment.escalated` | BAM | CPS | Continuous |
| `fnsr.interpretation.generated` | IS | Governance | Continuous |
| `fnsr.interpretation.audit_ready` | IS | Governance | Continuous |

**Infrastructure Domain:**

| Event | Producer | Consumers | Path |
|-------|----------|-----------|------|
| `fnsr.classifier.recalibration` | Orchestrator | (telemetry) | Internal |
| `fnsr.classifier.post_ingestion_reclassification` | Orchestrator | (telemetry) | Internal |
| `fnsr.topology.downgrade` | Orchestrator | (telemetry) | Internal |
| `fnsr.topology.cbor_fallback` | Orchestrator | (telemetry) | Internal |
| `fnsr.topology.rebuild_diff` | Build system | (audit) | Build-time |
| `fnsr.circuit.opened` | Orchestrator | (telemetry) | Internal |
| `fnsr.circuit.closed` | Orchestrator | (telemetry) | Internal |
| `fnsr.taint.violation` | Orchestrator | CPS, Governance | Internal |
| `fnsr.taint.gateway_transit` | Orchestrator | (audit) | Internal |
| `fnsr.saga.completed` | Orchestrator | APS (case record) | All |
| `fnsr.service.status_changed` | Orchestrator | SMS | Continuous |
| `fnsr.governance.preliminary_escalation` | Orchestrator | Governance | Internal |
| `fnsr.memory.pressure` | Runtime | Orchestrator | Internal |

**Note on `fnsr.service.status_changed` (v2.2 change):** In v2.1, this event was listed with producer "any," implying every service must emit its own status changes. This created an implicit obligation across 42 spec documents. v2.2 reassigns production to the Orchestrator, which has authoritative visibility into service availability through circuit breaker state, dispatch outcomes, and topology changes. Individual services do not need to self-report status — the Orchestrator observes it.

### 8.3 Phase-Conditional Event Routing

The event registry (§8.2) lists consumers for each event type, but not all consumers exist in all deployment phases. For example, `fnsr.verdict.rendered` lists SMS as a consumer, but SMS is a Phase 3 service — it does not exist in Phase 2 when MDRE first begins producing verdicts.

The Orchestrator handles this through the existing degradation system, not through separate routing logic:

1. **At startup**, the Orchestrator marks all services not in the current phase topology as unavailable.
2. **At dispatch time**, when an event's consumer list includes an unavailable service, the Orchestrator applies that service's phase-conditional degradation behavior (§5.1). For most absent continuous services, this is `skip` with taint relative +0 — the event is simply not routed to the absent consumer. No error, no warning beyond a trace-level log.
3. **The event registry is not filtered per phase.** It is the canonical contract for the full 42-service topology. Phase-conditional suppression is a runtime behavior, not a registry modification. This ensures that when a new phase activates, no event routing changes are needed — the newly available service automatically begins receiving its declared events.

**Consequence:** In Phase 2, MDRE verdicts are routed to IEE, CTS, BAM, and IS. SMS and NIS are suppressed via `skip`/`cache` degradation. In Phase 3, SMS becomes available and immediately begins receiving `fnsr.verdict.rendered` events with no configuration change.

---

## 9. CPS Integration: The Safety Override

### 9.1 CPS Independence Principle

CPS operates **outside** the Orchestrator's dispatch pipeline. It has its own monitoring channels, its own trigger criteria, and its own execution path. The Orchestrator cannot prevent CPS from acting. This is the "quis custodiet" principle: the coordinator cannot override the safety system.

### 9.2 Containment Protocol

When CPS emits a containment event, the Orchestrator responds immediately:

- `fnsr.containment.tier_restricted`: Orchestrator restricts available query paths (e.g., full → standard only)
- `fnsr.containment.subsystem_isolated`: Orchestrator terminates the specified worker and marks its services as degraded
- `fnsr.containment.halt_initiated`: Orchestrator halts all active sagas, preserves state, returns error responses
- `fnsr.containment.state_preserved`: Orchestrator enters read-only mode until governance authorizes resumption

The Orchestrator **must not** buffer, delay, or filter CPS events. They are processed before any saga dispatch.

---

## 10. Governance Integration

### 10.1 Tier-Aware Routing (Two-Phase)

**Problem (v2.1 S-8):** v2.1 placed governance tier computation before IEE dispatch (Phase 4), meaning all reasoning work had already completed before a Tier 3/4 escalation could preempt it. This wastes compute on queries that governance will defer.

**v2.2 solution: Two-phase governance check.**

**Phase 1.5 — Preliminary tier check (after ingestion, before reasoning):**

After ingestion completes, the Orchestrator invokes a lightweight governance tier estimation using only ingestion metadata: claim domains, entity types, taint hint, and any domain-specific escalation triggers (e.g., claims about human welfare, legal obligations, resource allocation affecting third parties). This preliminary check can resolve:

- **Tier 0–2:** Proceed to reasoning. No escalation needed.
- **Tier 3 (preliminary):** Log `fnsr.governance.preliminary_escalation`. Two options:
  1. If the Governance spec permits "reason-then-escalate" for the claim domain, proceed with reasoning but do not return the response until governance review completes.
  2. If the claim domain requires pre-reasoning escalation, return an `EscalationReceipt` immediately with `statusCheckUri`. No MDRE, CSS, or AES work is dispatched.
- **Tier 4 (preliminary):** Immediate escalation. Return `EscalationReceipt`. No reasoning work dispatched. This prevents burning 200ms+ of MDRE compute on queries that will wait indefinitely for governance body review.

All `EscalationReceipt` responses include `commitmentAct` and `commitmentStatus` fields when the saga involves a commitment act (§4.4). This ensures callers know whether a pending commitment was deferred by governance.

**Phase 3.5 — Governance refinement (after reasoning, before evaluation):**

If the preliminary check returned Tier 0–2 but reasoning reveals higher complexity (e.g., MDRE discovers a novel ethical dilemma, CSS simulation shows unexpected consequences), the governance tier is re-checked with the full reasoning context. Tier can only be upgraded, never downgraded. If the refined tier is 3+, the saga enters the escalation path before IEE evaluation.

**Fallback:** When governance tier cannot be determined from ingestion metadata alone (insufficient signal), the preliminary check returns "indeterminate" and reasoning proceeds. The Phase 3.5 refinement becomes the authoritative tier check.

### 10.2 Governance Event Routing

Governance events (`gov:*`) are routed through the Orchestrator's governance adapter, not the main event dispatch pipeline. This separation ensures governance decisions are auditable independently of service execution.

---

## 11. Performance Reporting

Every saga produces a `PerformanceReport` attached to the response:

```typescript
type PerformanceReport = {
  sagaId:          string;
  path:            QueryPath;
  escalatedFrom?:  QueryPath;
  classifierVersion: number;      // Classifier state version
  totalMs:         number;
  budgetMs:        number;
  budgetUtilization: number;    // totalMs / budgetMs
  topology:        TopologyMode;
  perService:      ServiceTiming[];
  degradations:    DegradationRecord[];
  taintElevations: TaintElevationRecord[];  // Each degradation's taint impact
  gatewayTransits: GatewayTransitRecord[];  // Counterfactual Gateway usage
  cacheHits:       string[];    // Service IDs served from cache
  cacheMisses:     string[];
  taintCeiling:    TaintLevel;
  counterfactualSourced: boolean;           // Whether any gateway was used
  commitmentAck?:  string;                  // CTS commitment ID if Phase 4.5 ran
  circuitBreakers: CircuitBreakerState[];
  governanceTier:  GovernanceTier;
  governancePhase: "preliminary" | "refined" | "indeterminate";
};

type ServiceTiming = {
  serviceId: ServiceId;
  worker:    "main" | "W1" | "W2" | "W3";
  budgetMs:  number;
  actualMs:  number;
  status:    "completed" | "degraded" | "skipped" | "failed";
};

type DegradationRecord = {
  serviceId:  ServiceId;
  mode:       "skip" | "cache" | "degrade";
  taintImpact: TaintElevation;
  consequence: string;
};

type GatewayTransitRecord = {
  gatewayId:  string;
  source:     ServiceId;
  consumer:   ServiceId;
  taintIn:    TaintLevel;
  taintOut:   TaintLevel;
};
```

---

## 12. Incremental Deployment

The Orchestrator does not require all 42 services to exist. It is designed for incremental deployment aligned with the phased roadmap.

### 12.1 Phase 1 Configuration

```typescript
const PHASE_1_TOPOLOGY: ServiceId[] = [
  "tagteam", "hiri", "fandaws", "cps", "hiri-ipfs"
];
```

The Orchestrator routes all queries through TagTeam → HIRI → Fandaws. CPS monitors independently. All other services are marked unavailable with `skip` degradation. The query path is always "standard" (no reasoning services for fast/full differentiation).

**Accepted safety gap:** BAM is not present in Phase 1. Alignment monitoring is deferred until Phase 2 when MDRE begins producing reasoned verdicts. In Phase 1, the pipeline performs extraction and storage only — there is no reasoning output to monitor for alignment drift. CPS provides the safety floor through independent containment authority. This gap is documented in the Portfolio Planning risk register and reviewed at the Phase 1→2 gate.

### 12.2 Phase 2 Configuration

Adds W2Fuel, MDRE, BAM, IS, CTS, SIS, ECCPS. The full three-path classification activates. Fast path (cache + MDRE) becomes available. Standard path includes reasoning. Full path is still unavailable (no reasoning triad). **BAM becomes block-mode from this phase onward** — alignment monitoring is now required because MDRE produces reasoned verdicts.

### 12.3 Phase 3 Configuration

Adds AES, DES, CSS, IEE, SHML, SMS, NIS, AVS. Full path activates. All three query paths operational. Continuous services begin processing events. The Counterfactual Gateway (§6.4) activates with CSS.

### 12.4 Phase 4 Configuration

Adds IRIS, OERS, APS, SoMS, FNSR federation. The complete topology is operational. IRIS events (`fnsr.perception.*`) begin flowing into the ingestion pipeline.

---

## 13. Non-Goals

The Orchestrator does **not** specify:

- Service implementation details (each service has its own spec)
- Persistent storage (Fandaws, IndexedDB adapters)
- Network protocols (no HTTP, no WebSocket — these are adapter concerns)
- Authentication/authorization (Governance spec + HIRI)
- Monitoring infrastructure (FNSR Performance spec)
- Content of reasoning (MDRE, IEE)
- Ontological alignment (W2Fuel, HIRI IPFS)

---

## 14. Critical Dependencies

### 14.1 CPS Specification Status

CPS (Containment Protocol Service) is the most safety-critical component in the FNSR architecture. It is the only service with authority to halt the Orchestrator. It is assigned `block` degradation in all phases — without CPS, no saga can execute.

**CPS v1.0.0 (Draft) now exists.** The specification confirms:

1. The Orchestrator's CPS integration (§9) is validated: CPS defines a priority channel for containment event delivery with a 200ms halt latency guarantee that pre-empts saga processing.
2. The containment event contracts (`fnsr.containment.*`) in §8.2 are confirmed by CPS v1.0.0 §4, which defines the same four events with matching payloads.
3. The CPS independence principle (§9.1) is validated by CPS v1.0.0 §2, which mandates three independent monitoring channels and zero FNSR dependencies.

**Remaining work:** The Orchestrator cannot be promoted from Hardened Candidate to FINAL until CPS v1.0.0 completes its own review cycle and is promoted to at least Hardened Draft. The Orchestrator's §5.1 priority channel implementation must be validated against CPS's §5.1 pre-emption guarantee.

---

## References

- FNSR Performance Specification v2.0.0 (query paths, latency budgets, worker topology)
- FNSR Governance Specification v2.0.0 (autonomy tiers, escalation protocol)
- ARCHON Functional Requirements v3.0 (guardian system integration)
- CPS Containment Protocol Service v1.0.0 (independent safety monitor, containment ratchet, 200ms halt latency)
- Portfolio Planning Document v3.6.0 (service inventory, dependency graph, phased roadmap)
- CloudEvents Specification v1.0 (event envelope format)
- RFC 8949 — Concise Binary Object Representation (CBOR)
- All service specifications (event contracts extracted and registered in §8.2)
