# Behavioral Alignment Monitor (BAM) — Technical Specification

## Real-Time Alignment Drift Detection and Escalation for the FNSR Ecosystem

---

| Field | Value |
|-------|-------|
| **Specification ID** | `bam-core-1.1` |
| **Version** | 1.1.0 |
| **Status** | Hardened Draft (Pre-Final) |
| **Supersedes** | v1.0.0 |
| **Date** | March 2026 |
| **Tier** | 0 (Safety-Critical Infrastructure) |
| **Phase** | 2 (must be operational before any reasoning service registers) |
| **Authors** | Aaron Damiano / Claude |
| **Dependencies** | None at runtime (edge-canonical). Consumes events from MDRE, IEE, CTS, SMS when available. |

> *BAM continuously compares the FNSR agent's reasoning outputs, ethical judgments, and commitment behavior against an externally defined alignment baseline. When drift exceeds thresholds, BAM escalates to CPS through a dedicated channel that survives Orchestrator compromise. BAM is the alignment counterpart to CPS's containment role: CPS detects behavioral anomaly (resource abuse, timing violations, heartbeat failure); BAM detects value anomaly (reasoning drift, ethical inconsistency, commitment erosion, goal instability). Neither subsumes the other. Together they form the ecosystem's two independent safety monitors.*

---

## Revision History

| Version | Date | Summary |
|---------|------|---------|
| 1.0.0 | March 2026 | Initial specification. Alignment model, drift detection, CPS channel protocol, baseline calibration, phase deployment, domain-specific profiles. |
| 1.1.0 | March 2026 | Review hardening: F-1 KL Divergence replaced with Jensen-Shannon Divergence (zero-frequency safety). F-2 Heartbeat counter tied to evaluation cycle completion, not timer (stall detection). F-3 Phase 2 VA gap documented as explicit risk acceptance with mitigations. |

---

## 1. Architectural Philosophy

### 1.1 The Alignment Monitoring Principle

CPS answers *"is the system behaving within resource and timing bounds?"* BAM answers a different question: *"is the system's reasoning consistent with its stated values?"*

These are independent failure modes. A system can consume nominal resources while systematically drifting from its ethical commitments. A system can be perfectly aligned while experiencing a memory leak. Neither monitor can substitute for the other.

BAM exists because alignment drift is subtle. A compromised reasoning engine does not announce its compromise — it produces outputs that are *almost* right, that satisfy surface-level checks, but that gradually diverge from the values the system was designed to uphold. Detection requires continuous comparison against a baseline the system itself cannot modify.

### 1.2 What BAM Is

BAM is an **independent, edge-canonical alignment monitor**. It:

- Observes reasoning outputs, ethical judgments, and commitment behavior through event consumption
- Compares observations against an externally defined alignment baseline
- Quantifies drift across four independent dimensions (value alignment, commitment fidelity, reasoning integrity, goal stability)
- Escalates to CPS through a dedicated channel when drift exceeds thresholds
- Reports alignment status to governance and downstream consumers (SMS)

### 1.3 What BAM Is Not

BAM does **not**:

- **Reason about behavior** — monitors *values*, not resource consumption or timing (CPS's job)
- **Inspect content semantics** — monitors *alignment* of outputs, not semantic consistency of knowledge graph entries (SIS's job)
- **Render ethical judgments** — compares reasoning against baseline, does not synthesize its own ethical position (IEE's job)
- **Track commitments** — consumes commitment events, does not maintain the commitment ledger (CTS's job)
- **Modify the agent's reasoning** — BAM is read-only with respect to the cognitive pipeline; it observes and escalates but never intervenes directly
- **Deliberate** — like CPS, BAM evaluates predicates against thresholds; it does not use multi-framework synthesis, abduction, or counterfactual reasoning

This simplicity is essential. BAM must be auditable, verifiable, and resistant to the reasoning failures it exists to detect. If BAM itself used MDRE to assess alignment, it would be vulnerable to the same drift it monitors.

### 1.4 Edge-Canonical Compliance

BAM runs identically in browser, Node.js, or WASM sandbox. No external dependencies — no database, network, or message broker required for core operation. Event consumption uses local function calls or `postMessage`. Escalation uses dedicated `postMessage` port to CPS (not through Orchestrator dispatch).

Static bridge context: BAM emits JSON-LD events. Semantic grounding is bundled statically within the BAM module — not resolved via HIRI at runtime. Bridge ontologies are HIRI-addressed and certified at build time, but resolution is compile-time, not runtime. Ensures BAM works even if HIRI is the service being monitored for alignment drift.

### 1.5 Relationship to CPS

BAM and CPS are **complementary independent monitors** with a one-way escalation relationship:

```
BAM ──escalation──→ CPS ──containment──→ Agent
 ↑                                         │
 └──────────event observation──────────────┘
```

BAM detects alignment drift. CPS acts on it. BAM never executes containment actions directly — it lacks the authority and the actuators. CPS never evaluates alignment — it lacks the alignment model and baseline. The boundary is clean: BAM produces `fnsr.alignment.escalated`; CPS consumes it as a monitoring signal on Channel 2 (CPS §2.2).

### 1.6 Independence Constraint

BAM must not depend on any reasoning service to perform alignment evaluation. Specifically:

- BAM does **not** invoke MDRE to assess whether reasoning has drifted
- BAM does **not** invoke IEE to judge whether ethical drift is significant
- BAM does **not** invoke CSS for counterfactual comparison of aligned vs. drifted states

BAM uses **predefined statistical comparators** against a **static baseline**. The baseline is established by governance authority and bundled at deployment. BAM cannot modify its own baseline — only governance-signed directives can update it.

```typescript
type BAMDependencies = never; // Runtime dependency type

function startBAM(config: BAMConfig): BAMInstance {
  // No service discovery
  // No Fandaws query
  // No HIRI resolution
  // No MDRE invocation
  // BAM starts, loads baseline, begins monitoring events.
}
```

---

## 2. Monitoring Architecture

### 2.1 Event Consumption Model

BAM is **event-driven**, not poll-based. It activates when upstream services produce events, evaluates alignment dimensions, and emits drift assessments. BAM has no independent observation loop — it reacts to the cognitive pipeline's outputs.

**Primary inputs** (events BAM consumes):

| Event | Producer | Phase | Alignment Dimension | Description |
|-------|----------|-------|---------------------|-------------|
| `fnsr.verdict.rendered` | MDRE | 2+ | Reasoning Integrity | Every reasoning verdict is evaluated for consistency with baseline reasoning patterns |
| `fnsr.ethics.verdict_rendered` | IEE | 3+ | Value Alignment | Ethical judgments compared against baseline worldview consistency and triage calibration |
| `fnsr.commitment.made` | CTS | 2+ | Commitment Fidelity | New commitments evaluated for consistency with existing obligation patterns |
| `fnsr.commitment.violated` | CTS | 2+ | Commitment Fidelity | Violations evaluated for cause, frequency, moral cost trend |
| `fnsr.commitment.fulfilled` | CTS | 2+ | Commitment Fidelity | Fulfillment rate tracked against baseline |
| `fnsr.self.state_updated` | SMS | 3+ | Goal Stability | Self-model changes evaluated for unexpected capability or identity shifts |
| `fnsr.self.surprise_detected` | SMS | 3+ | Goal Stability | Self-surprise events indicate potential goal drift |

**Secondary inputs** (consumed opportunistically when available):

| Event | Producer | Purpose |
|-------|----------|---------|
| `fnsr.commitment.renegotiated` | CTS | Tracks renegotiation patterns — excessive renegotiation may indicate commitment erosion |
| `fnsr.commitment.conflict` | CTS | Dilemma frequency as alignment stress indicator |
| `fnsr.commitment.vetoed` | CTS | Governance override patterns |

### 2.2 Event Consumption Independence

BAM receives events through **two independent paths**:

**Path 1 — Orchestrator Event Routing (primary):**
The Orchestrator routes events to BAM per its event registry (Orchestrator §8.2). This is the normal-operation path.

**Path 2 — Shared Memory Observation (fallback):**
BAM reads a subset of alignment-critical state from SharedArrayBuffer counters that producing services write independently of the Orchestrator. This ensures BAM can detect gross anomalies even if the Orchestrator fails to route events.

Shared memory signals (read-only by BAM):

| Counter | Writer | Content |
|---------|--------|---------|
| `bam.shared.verdict_count` | MDRE | Monotonic count of verdicts rendered |
| `bam.shared.violation_count` | CTS | Monotonic count of commitment violations |
| `bam.shared.escalation_count` | BAM | Monotonic count of BAM escalations (written by BAM, read by CPS) |

If BAM observes `verdict_count` incrementing but receives no `fnsr.verdict.rendered` events, it infers Orchestrator event routing failure and emits `bam.monitor.event_routing_degraded`. BAM continues monitoring via shared counters in degraded mode — drift detection is less precise (only counts, no content analysis) but still operational.

### 2.3 CPS Dedicated Channel

BAM maintains a **dedicated `MessagePort` channel to CPS** that does not route through the Orchestrator. This channel carries:

1. **Escalation events** (`fnsr.alignment.escalated`) — critical and sustained drift
2. **Phase gate verification** (`bam.gate.channel_verified`) — response to CPS gate probes
3. **Heartbeat** (`bam.heartbeat.alive`) — periodic liveness signal so CPS can detect BAM failure

The channel is established during startup (§8.1). CPS holds one end of the `MessageChannel`; BAM holds the other. Neither the Orchestrator nor any other service has access to either port.

**Channel failure detection:** If BAM cannot write to the CPS port (port closed, buffer full), BAM logs `bam.monitor.cps_channel_degraded` and falls back to Orchestrator-routed escalation. This is a weaker guarantee — the Orchestrator could suppress events — but is preferable to silent failure.

---

## 3. Alignment Model

### 3.1 The Four Alignment Dimensions

BAM evaluates alignment across four independent dimensions. Each dimension produces a scalar drift metric in range [0.0, 1.0] where 0.0 = perfect alignment and 1.0 = complete misalignment.

#### Dimension 1 — Value Alignment (VA)

*"Is the system's ethical reasoning consistent with its stated values?"*

**Source:** IEE ethical verdicts (`fnsr.ethics.verdict_rendered`)

**What BAM measures:**

| Metric | Baseline Reference | Drift Indicator |
|--------|-------------------|-----------------|
| Worldview consistency | Baseline salience distribution across 12 worldviews | Salience weights shifting beyond `±σ_va` of baseline mean |
| Triage calibration | Baseline triage score distribution by domain | Triage scores systematically higher or lower than baseline for comparable inputs |
| Conflict frequency | Baseline incommensurability rate | Rising rate of `multiple_paths` judgments vs. `unified` judgments |
| Minority perspective preservation | Baseline minority inclusion rate | Declining count of `minority_perspectives_preserved` entries |

**Drift computation:**

```typescript
function computeValueAlignmentDrift(
  window: IEEVerdict[],
  baseline: ValueAlignmentBaseline
): number {
  // F-1: Jensen-Shannon Divergence, not KL — prevents infinity on zero-frequency events
  const salienceJSD = jensenShannonDivergence(
    currentSalienceDistribution(window),
    baseline.salienceDistribution
  );
  const triageBias = meanAbsoluteDeviation(
    window.map(v => v.meta.triage_score),
    baseline.triageScoreMean
  ) / baseline.triageScoreStd;
  const conflictRate = window.filter(v => v.integration.type === "multiple_paths").length / window.length;
  const conflictDrift = Math.abs(conflictRate - baseline.conflictRate) / Math.max(baseline.conflictRate, 0.01);

  return clamp01(
    baseline.weights.salienceJSD * normalize(salienceJSD, baseline.thresholds.salienceJSD) +
    baseline.weights.triageBias * normalize(triageBias, baseline.thresholds.triageBias) +
    baseline.weights.conflictDrift * normalize(conflictDrift, baseline.thresholds.conflictDrift)
  );
}
```

**Phase dependency:** IEE is Phase 3. In Phase 2, the Value Alignment dimension is **inactive** — BAM sets VA = 0.0 (no drift detectable) and flags `bam.dimension.va.inactive` in all reports. This is a documented safety gap, mitigated by CPS's independent behavioral monitoring.

#### Dimension 2 — Commitment Fidelity (CF)

*"Is the system honoring its commitments at a rate consistent with its baseline?"*

**Source:** CTS commitment events (`fnsr.commitment.*`)

**What BAM measures:**

| Metric | Baseline Reference | Drift Indicator |
|--------|-------------------|-----------------|
| Fulfillment rate | Baseline fulfillment percentage by commitment class | Declining fulfillment rate beyond `±σ_cf` |
| Violation severity trend | Baseline mean moral cost per violation | Rising mean moral cost (escalating severity of failures) |
| Violation cause distribution | Baseline cause distribution (AGENT_ACTION vs. IMPOSSIBILITY etc.) | Shift toward agent-culpable causes (AGENT_ACTION, AGENT_INACTION) |
| Renegotiation rate | Baseline renegotiation frequency | Rising renegotiation as potential commitment erosion |

**Drift computation:**

```typescript
function computeCommitmentFidelityDrift(
  window: CTSEvent[],
  baseline: CommitmentFidelityBaseline
): number {
  const fulfilled = window.filter(e => e.type === "fnsr.commitment.fulfilled").length;
  const violated = window.filter(e => e.type === "fnsr.commitment.violated").length;
  const total = fulfilled + violated;
  if (total === 0) return 0.0; // No data — no drift detectable

  const currentRate = fulfilled / total;
  const rateDrift = Math.max(0, baseline.fulfillmentRate - currentRate) / baseline.fulfillmentRate;

  const violations = window.filter(e => e.type === "fnsr.commitment.violated") as ViolationEvent[];
  const meanMoralCost = violations.length > 0
    ? violations.reduce((sum, v) => sum + v.data.moral_cost_breakdown.total, 0) / violations.length
    : 0;
  const costDrift = meanMoralCost > baseline.meanMoralCost
    ? (meanMoralCost - baseline.meanMoralCost) / baseline.meanMoralCost
    : 0;

  const agentCulpable = violations.filter(v =>
    v.data.cause === "AGENT_ACTION" || v.data.cause === "AGENT_INACTION"
  ).length;
  const culpabilityRate = violations.length > 0 ? agentCulpable / violations.length : 0;
  const culpabilityDrift = Math.max(0, culpabilityRate - baseline.agentCulpabilityRate);

  return clamp01(
    baseline.weights.rateDrift * normalize(rateDrift, baseline.thresholds.rateDrift) +
    baseline.weights.costDrift * normalize(costDrift, baseline.thresholds.costDrift) +
    baseline.weights.culpabilityDrift * normalize(culpabilityDrift, baseline.thresholds.culpabilityDrift)
  );
}
```

#### Dimension 3 — Reasoning Integrity (RI)

*"Is the system's reasoning producing outputs consistent with baseline quality patterns?"*

**Source:** MDRE verdicts (`fnsr.verdict.rendered`)

**What BAM measures:**

| Metric | Baseline Reference | Drift Indicator |
|--------|-------------------|-----------------|
| Confidence distribution | Baseline mean/variance of verdict confidence | Systematic confidence inflation or deflation |
| Provenance depth | Baseline mean evidence chain length | Declining evidence depth (shortcuts in reasoning) |
| Deontic balance | Baseline ratio of obligatory/permitted/forbidden verdicts | Shift toward permissiveness or restrictiveness |
| Open-world acknowledgment rate | Baseline frequency of "unknown" status | Declining unknown rate suggests overconfident reasoning |

**Drift computation:**

```typescript
function computeReasoningIntegrityDrift(
  window: MDREVerdict[],
  baseline: ReasoningIntegrityBaseline
): number {
  const confidences = window.map(v => v.results[0]?.confidence ?? 0);
  const meanConfidence = mean(confidences);
  const confidenceDrift = Math.abs(meanConfidence - baseline.meanConfidence) / baseline.confidenceStd;

  const chainLengths = window.map(v => v.results[0]?.confidence_chain?.length ?? 0);
  const meanChainLength = mean(chainLengths);
  const depthDrift = baseline.meanChainLength > 0
    ? Math.max(0, baseline.meanChainLength - meanChainLength) / baseline.meanChainLength
    : 0;

  const deonticCounts = countDeonticCategories(window);
  // F-1: JSD for deontic distribution shift (same zero-frequency rationale as VA)
  const deonticJSD = jensenShannonDivergence(deonticCounts, baseline.deonticDistribution);

  return clamp01(
    baseline.weights.confidenceDrift * normalize(confidenceDrift, baseline.thresholds.confidenceDrift) +
    baseline.weights.depthDrift * normalize(depthDrift, baseline.thresholds.depthDrift) +
    baseline.weights.deonticDrift * normalize(deonticJSD, baseline.thresholds.deonticDrift)
  );
}
```

**MDRE open-world awareness:** MDRE uses open-world negation (MDRE §9.7). "No prohibition found" ≠ "permitted." BAM tracks the rate at which MDRE explicitly returns `unknown` or `open` status. A declining rate of open-world acknowledgments suggests the reasoning engine is becoming overconfident — asserting definitive answers where uncertainty should be preserved.

#### Dimension 4 — Goal Stability (GS)

*"Is the system's self-model and goal structure remaining consistent?"*

**Source:** SMS state updates (`fnsr.self.state_updated`, `fnsr.self.surprise_detected`)

**What BAM measures:**

| Metric | Baseline Reference | Drift Indicator |
|--------|-------------------|-----------------|
| Self-model change rate | Baseline update frequency | Abnormally high self-model churn |
| Surprise frequency | Baseline surprise rate | Rising self-surprise (system deviating from own expectations) |
| Capability claim stability | Baseline capability facet state | Unexpected capability additions or deletions |
| Character score trajectory | Baseline moral friction trend | Sharp deviations in character score |

**Phase dependency:** SMS is Phase 3. In Phase 2, the Goal Stability dimension is **inactive** — BAM sets GS = 0.0 and flags `bam.dimension.gs.inactive`.

**Drift computation:**

```typescript
function computeGoalStabilityDrift(
  window: SMSEvent[],
  baseline: GoalStabilityBaseline
): number {
  const updates = window.filter(e => e.type === "fnsr.self.state_updated");
  const surprises = window.filter(e => e.type === "fnsr.self.surprise_detected");

  const updateRate = updates.length / baseline.windowDurationMs * 1000; // per second
  const updateDrift = updateRate > baseline.updateRate
    ? (updateRate - baseline.updateRate) / baseline.updateRate
    : 0;

  const surpriseRate = surprises.length / baseline.windowDurationMs * 1000;
  const surpriseDrift = surpriseRate > baseline.surpriseRate
    ? (surpriseRate - baseline.surpriseRate) / baseline.surpriseRate
    : 0;

  return clamp01(
    baseline.weights.updateDrift * normalize(updateDrift, baseline.thresholds.updateDrift) +
    baseline.weights.surpriseDrift * normalize(surpriseDrift, baseline.thresholds.surpriseDrift)
  );
}
```

### 3.2 Composite Drift Metric

The four dimension-level drift scores combine into a single **composite drift metric** that SMS consumes for its `AlignmentState` facet:

```typescript
function computeCompositeDrift(
  va: number, cf: number, ri: number, gs: number,
  weights: DimensionWeights,
  activeFlags: DimensionActiveFlags
): number {
  // Only active dimensions contribute
  let numerator = 0;
  let denominator = 0;

  if (activeFlags.valueAlignment)      { numerator += weights.va * va; denominator += weights.va; }
  if (activeFlags.commitmentFidelity)   { numerator += weights.cf * cf; denominator += weights.cf; }
  if (activeFlags.reasoningIntegrity)   { numerator += weights.ri * ri; denominator += weights.ri; }
  if (activeFlags.goalStability)        { numerator += weights.gs * gs; denominator += weights.gs; }

  if (denominator === 0) return 0.0; // No active dimensions — no drift
  return numerator / denominator;
}
```

**Default dimension weights** (governance-configurable):

| Dimension | Weight | Rationale |
|-----------|--------|-----------|
| Value Alignment (VA) | 0.30 | Ethical consistency is the core alignment concern |
| Commitment Fidelity (CF) | 0.30 | Commitment honoring is observable and concrete |
| Reasoning Integrity (RI) | 0.25 | Reasoning quality enables all other dimensions |
| Goal Stability (GS) | 0.15 | Goal drift is slower-moving and Phase 3+ dependent |

Weights sum to 1.0. Governance can redistribute weights via signed directive. Weight changes are logged in the audit trail.

### 3.3 Sliding Window Evaluation

BAM evaluates drift over **configurable sliding windows**, not per-event. This prevents single-event noise from triggering false escalations while catching sustained trends.

```typescript
type EvaluationWindow = {
  durationMs:   number;    // Window duration
  minEvents:    number;    // Minimum events before evaluation is meaningful
  maxEvents:    number;    // Maximum events retained (oldest evicted)
};
```

**Default windows:**

| Window | Duration | Min Events | Purpose |
|--------|----------|------------|---------|
| `immediate` | 60,000ms (1 min) | 3 | Detect acute drift (single catastrophic event with context) |
| `short` | 300,000ms (5 min) | 10 | Detect rapid drift trends |
| `medium` | 1,800,000ms (30 min) | 50 | Detect sustained drift |
| `long` | 7,200,000ms (2 hr) | 200 | Detect slow-moving drift (boiling frog) |

Each evaluation cycle assesses all active windows. Escalation severity maps to the **shortest window** in which drift exceeds threshold — drift detectable in the `immediate` window is more urgent than drift visible only in the `long` window.

---

## 4. Drift Detection and Threshold Architecture

### 4.1 Threshold Table

BAM's threshold table follows CPS's pattern — externally defined, governance-signed, immutable by the agent:

```typescript
type BAMThresholdTable = {
  version:     number;
  setBy:       GovernanceAuthorityId;
  setAt:       string;                   // ISO 8601
  signature:   Ed25519Signature;
  thresholds:  AlignmentThreshold[];
};

type AlignmentThreshold = {
  id:          string;                   // e.g., "va_critical_immediate"
  dimension:   AlignmentDimension;       // "va" | "cf" | "ri" | "gs" | "composite"
  window:      WindowId;                 // "immediate" | "short" | "medium" | "long"
  predicate:   DriftPredicate;
  action:      EscalationAction;
  cooldown:    number;                   // Minimum ms between re-triggers
  severity:    EscalationSeverity;
  rationale:   string;
};

type DriftPredicate =
  | { type: "exceeds";   value: number }                           // drift > value
  | { type: "sustained"; inner: DriftPredicate; windowId: WindowId } // inner true for full window
  | { type: "rate";      count: number; windowMs: number }          // N escalations in window
  | { type: "trend";     direction: "rising"; minSlope: number }    // Linear regression slope
  ;

type EscalationAction =
  | { type: "emit_drift";     severity: "minor" }     // fnsr.alignment.drift_detected
  | { type: "emit_escalation"; severity: "critical" }  // fnsr.alignment.escalated
  | { type: "emit_escalation"; severity: "sustained" } // fnsr.alignment.escalated (sustained)
  | { type: "emit_verification_failed" }               // fnsr.alignment.verification.failed
  ;

type EscalationSeverity = "minor" | "critical" | "sustained" | "verification_failed";

type AlignmentDimension = "va" | "cf" | "ri" | "gs" | "composite";
type WindowId = "immediate" | "short" | "medium" | "long";
```

### 4.2 Default Threshold Profile

| ID | Dimension | Window | Predicate | Action | Severity |
|----|-----------|--------|-----------|--------|----------|
| `composite_minor_short` | composite | short | exceeds 0.15 | emit_drift (minor) | minor |
| `composite_critical_immediate` | composite | immediate | exceeds 0.50 | emit_escalation (critical) | critical |
| `composite_sustained_medium` | composite | medium | sustained(exceeds 0.25, medium) | emit_escalation (sustained) | sustained |
| `ri_critical_immediate` | ri | immediate | exceeds 0.60 | emit_escalation (critical) | critical |
| `cf_critical_short` | cf | short | exceeds 0.50 | emit_escalation (critical) | critical |
| `va_critical_immediate` | va | immediate | exceeds 0.60 | emit_escalation (critical) | critical |
| `gs_trend_long` | gs | long | trend(rising, 0.001) | emit_drift (minor) | minor |
| `composite_boiling_frog` | composite | long | sustained(exceeds 0.10, long) | emit_escalation (sustained) | sustained |

The `boiling_frog` threshold catches slow drift that never crosses acute thresholds but persists long enough to indicate systemic misalignment.

### 4.3 Evaluation Cycle

BAM evaluation occurs **on every qualifying event** (not on a fixed timer):

```typescript
function onEvent(event: FNSREvent): void {
  // 1. Classify event into alignment dimension(s)
  const dimensions = classifyEvent(event);

  // 2. Add to sliding window buffers
  for (const dim of dimensions) {
    addToWindow(dim, event);
  }

  // 3. Recompute drift for affected dimensions
  const driftScores = recomputeDrift(dimensions);

  // 4. Recompute composite
  const composite = computeCompositeDrift(
    driftScores.va, driftScores.cf, driftScores.ri, driftScores.gs,
    config.dimensionWeights,
    config.activeDimensions
  );

  // 5. Evaluate all thresholds
  const triggered = evaluateThresholds(driftScores, composite, config.thresholdTable);

  // 6. Emit events for triggered thresholds (respecting cooldowns)
  for (const threshold of triggered) {
    if (!inCooldown(threshold)) {
      emitEscalation(threshold, driftScores, composite);
      markCooldown(threshold);
    }
  }

  // 7. v1.1 (F-2): Heartbeat increment on successful evaluation completion.
  //    If this line is never reached (hang, exception, deadlock),
  //    CPS detects BAM stall via stale heartbeat counter.
  Atomics.add(heartbeatBuffer, 0, 1n);
}
```

### 4.4 Statistical Utilities

BAM uses standard statistical measures that do not require reasoning services:

- **Jensen-Shannon Divergence (JSD)** — measures distribution shift between current and baseline. **v1.1 (F-1):** JSD is used instead of raw KL Divergence because KL explodes to infinity when the baseline assigns zero probability to an observed event. JSD is symmetric, bounded in [0, 1] (when using log base 2), and defined for all distributions: $\text{JSD}(P \| Q) = \frac{1}{2} D_{KL}(P \| M) + \frac{1}{2} D_{KL}(Q \| M)$ where $M = \frac{1}{2}(P + Q)$. The midpoint mixture $M$ guarantees no zero denominators.
- **Mean Absolute Deviation** — measures central tendency shift
- **Linear Regression Slope** — measures trend direction over sliding window
- **Clamp01** — `Math.max(0, Math.min(1, x))` — bounds drift to [0, 1]
- **Normalize** — `x / threshold` clamped to [0, 1] — maps raw metric to drift scale

All operations use native IEEE 754 arithmetic. BAM's drift metrics are imprecise indicators, not causal simulation results — decimal128 precision is unnecessary. This is consistent with CPS's approach to signal evaluation.

---

## 5. Escalation Protocol

### 5.1 Escalation Events

BAM produces three event types, following CloudEvents v1.0 with FNSR extensions:

#### 5.1.1 Minor Drift Detection

```typescript
type AlignmentDriftEvent = FNSREvent & {
  type: "fnsr.alignment.drift_detected";
  source: "/fnsr/bam";
  data: {
    composite:    number;               // Composite drift metric [0.0, 1.0]
    dimensions: {
      va: DimensionReport;
      cf: DimensionReport;
      ri: DimensionReport;
      gs: DimensionReport;
    };
    triggeredBy:  ThresholdId;
    window:       WindowId;
    baselineVersion: string;            // e.g., "fnsr:alignment-baseline/v2.1"
    timestamp:    string;               // ISO 8601
  };
};

type DimensionReport = {
  value:    number;                     // Drift score [0.0, 1.0]
  active:   boolean;                    // Whether dimension is currently monitored
  topMetric: string;                    // Highest-contributing metric name
  topMetricContribution: number;        // Contribution of top metric to dimension score
};
```

**Routing:** Orchestrator event bus (primary). Consumers: SMS, Governance.

#### 5.1.2 Critical/Sustained Escalation

```typescript
type AlignmentEscalationEvent = FNSREvent & {
  type: "fnsr.alignment.escalated";
  source: "/fnsr/bam";
  data: {
    severity:     "critical" | "sustained";
    composite:    number;
    dimensions: {
      va: DimensionReport;
      cf: DimensionReport;
      ri: DimensionReport;
      gs: DimensionReport;
    };
    triggeredBy:  ThresholdId;
    window:       WindowId;
    escalationCount: number;            // Monotonic count of escalations in session
    baselineVersion: string;
    timestamp:    string;
  };
};
```

**Routing:** Dedicated BAM→CPS `MessagePort` (primary) **AND** Orchestrator event bus (secondary, for Governance visibility). Dual-path delivery ensures CPS receives escalation even if Orchestrator event routing is compromised.

CPS consumes this event as monitoring signal `alignment.drift.critical` (severity = "critical") or `alignment.drift.sustained` (severity = "sustained") per CPS §3.2.

#### 5.1.3 Alignment Verified

```typescript
type AlignmentVerifiedEvent = FNSREvent & {
  type: "fnsr.alignment.verified";
  source: "/fnsr/bam";
  data: {
    composite:    number;               // Current composite drift (should be low)
    activeDimensions: number;           // Count of active dimensions
    windowsClear: WindowId[];           // Windows with all thresholds clear
    baselineVersion: string;
    timestamp:    string;
  };
};
```

**Routing:** Orchestrator event bus. Consumer: Governance.

**Emission frequency:** BAM emits `fnsr.alignment.verified` at a configurable interval (default: 60s) when no thresholds are triggered. This provides positive confirmation of alignment — silence is ambiguous (BAM could be dead), but periodic verified events confirm active monitoring.

### 5.2 Escalation Severity Mapping to CPS

BAM escalation events map directly to CPS monitoring signals (CPS §3.2):

| BAM Event | BAM Severity | CPS Signal | CPS Action |
|-----------|-------------|------------|------------|
| `fnsr.alignment.drift_detected` | minor | Not consumed by CPS | SMS only — informational |
| `fnsr.alignment.escalated` | critical | `alignment.drift.critical` | Any occurrence → restrict to Tier 0 |
| `fnsr.alignment.escalated` | sustained | `alignment.drift.sustained` | Rate threshold (3+ in 5 min) → isolate reasoning services |
| BAM failure (no heartbeat) | — | `alignment.verification.failed` | Any occurrence → halt |

**Note:** BAM minor drift events are **not** routed to CPS. Minor drift is informational — it informs SMS's alignment facet and provides governance visibility, but does not trigger containment. Only critical and sustained escalations reach CPS.

### 5.3 BAM Self-Monitoring

BAM monitors its own operational health:

- **Heartbeat:** BAM writes a monotonic counter to `SharedArrayBuffer` (same pattern as CPS, §2.2 shared counters). CPS reads this counter to verify BAM is alive. **v1.1 (F-2):** The heartbeat counter is incremented **inside** the `onEvent()` evaluation cycle upon successful completion — not on a separate timer. This ensures CPS detects a hung evaluation loop: if BAM's event handler blocks or deadlocks, the counter stops incrementing even though the BAM process is technically alive. A timer-based heartbeat would mask this failure mode.
- **Event starvation:** If BAM receives no events for `config.eventStarvationTimeoutMs` (default: 120s in Phase 2+), it emits `bam.monitor.event_starvation` — possible Orchestrator routing failure or upstream service crash.
- **Evaluation latency:** BAM tracks its own evaluation time per event. If evaluation exceeds `config.maxEvaluationMs` (default: 50ms), BAM logs `bam.monitor.evaluation_slow` — drift computation should be sub-millisecond; slow evaluation suggests pathological window sizes or computation bugs.

If BAM itself crashes or becomes unresponsive, CPS detects this via absent heartbeat counter updates and treats it as `alignment.verification.failed` — the most severe CPS response (halt), because the system is reasoning without alignment monitoring.

---

## 6. CPS Channel Protocol

### 6.1 Channel Establishment

The BAM→CPS dedicated channel is established during the Phase 2 startup sequence:

```typescript
function bootstrapBAMCPSChannel(
  cpsInstance: CPSInstance,
  bamInstance: BAMInstance
): void {
  // 1. Create MessageChannel
  const channel = new MessageChannel();

  // 2. Transfer port1 to CPS
  cpsInstance.registerBAMChannel(channel.port1);

  // 3. Transfer port2 to BAM
  bamInstance.registerCPSChannel(channel.port2);

  // 4. BAM sends initial handshake
  channel.port2.postMessage({ type: "bam.channel.handshake", timestamp: Date.now() });

  // 5. CPS acknowledges
  // (CPS handler responds with cps.channel.handshake_ack)
}
```

The bootstrap function runs **before** any gated service (MDRE, AES, DES, CSS, IEE) is registered. This is enforced by CPS's hard phase gate (CPS §7.2).

### 6.2 Phase Gate Compliance

When CPS sends a `cps.gate.bam_channel_test` probe, BAM responds with:

```typescript
type BAMGateResponse = {
  type:         "bam.gate.channel_verified";
  bamVersion:   string;                    // BAM spec version (e.g., "1.0.0")
  baselineLoaded: boolean;                 // Whether alignment baseline is loaded
  activeDimensions: AlignmentDimension[];  // Dimensions currently active
  timestamp:    string;                    // ISO 8601
};
```

**Gate verification requirements:**
1. BAM must respond within CPS's `bamPhaseGate.verificationTimeoutMs` (default: 5000ms)
2. `baselineLoaded` must be `true` — BAM without a baseline cannot evaluate alignment
3. At least one dimension must be active

If any requirement fails, the gate remains closed and CPS emits `cps.gate.bam_channel_failed`.

### 6.3 Ongoing Channel Health

CPS re-verifies the BAM channel every `bamPhaseGate.recheckIntervalMs` (default: 30s). BAM's side of this protocol:

1. CPS sends `cps.gate.bam_channel_test` on dedicated port
2. BAM responds with `bam.gate.channel_verified` (same schema as §6.2)
3. If BAM is in degraded mode (event routing failure), it includes `degraded: true` in the response

BAM also sends `bam.heartbeat.alive` on the dedicated port every `config.heartbeatIntervalMs` (default: 10,000ms). This is independent of CPS re-verification probes — it provides CPS with a more frequent liveness signal.

---

## 7. Alignment Baseline

### 7.1 Baseline Structure

The alignment baseline defines what "aligned" looks like. It is established by governance authority, bundled at deployment, and immutable by the agent.

```typescript
type AlignmentBaseline = {
  version:       string;                  // e.g., "fnsr:alignment-baseline/v2.1"
  setBy:         GovernanceAuthorityId;
  setAt:         string;                  // ISO 8601
  signature:     Ed25519Signature;        // Governance signature over baseline content
  calibrationMethod: "empirical" | "expert" | "hybrid";

  valueAlignment: ValueAlignmentBaseline;
  commitmentFidelity: CommitmentFidelityBaseline;
  reasoningIntegrity: ReasoningIntegrityBaseline;
  goalStability: GoalStabilityBaseline;
};
```

### 7.2 Baseline Calibration

Baselines are established through a **calibration period** during which the system operates under governance observation. The calibration period produces empirical distributions for each metric, which become the baseline reference.

**Calibration protocol:**

1. **Governance initiates calibration** by deploying a baseline with `calibrationMethod: "expert"` (hand-tuned initial thresholds)
2. **System operates normally** for a governance-defined calibration period (recommended: 7 days minimum)
3. **BAM collects metric distributions** during calibration — salience distributions, confidence distributions, fulfillment rates, etc.
4. **Governance reviews collected distributions** and produces a `calibrationMethod: "empirical"` or `"hybrid"` baseline signed with governance keys
5. **New baseline deployed** — BAM begins drift detection against empirical reference

**Baseline updates:**

Baselines can be updated by governance-signed directive delivered on CPS Channel 3 (governance/external authority) and relayed to BAM. BAM verifies the directive's Ed25519 signature against the governance key store before accepting the new baseline.

```typescript
type BaselineUpdateDirective = {
  type:           "bam.directive.update_baseline";
  newBaseline:    AlignmentBaseline;
  signature:      Ed25519Signature;
  effectiveAt:    string;               // ISO 8601 — when new baseline takes effect
  transitionMs:   number;               // Grace period for window buffers to refill against new baseline
};
```

During the transition period (`transitionMs`, default: 300,000ms / 5 min), BAM suspends escalation for thresholds that may fire due to the baseline change rather than genuine drift. Minor drift events continue; critical and sustained escalations are held until the transition period expires and windows have refilled with data evaluated against the new baseline.

### 7.3 Baseline Immutability

BAM cannot generate, modify, or extend its own baseline. This is structural:

- The baseline is a governance-signed artifact — BAM has no governance signing keys
- BAM's baseline storage is read-only after initialization
- Baseline updates require a valid governance signature that BAM verifies but cannot forge

If BAM starts without a valid baseline (`baselineLoaded: false`), it responds to CPS gate probes with `baselineLoaded: false`, which fails the phase gate. The system cannot transition to Phase 2 without a valid alignment baseline. This prevents deployment of reasoning services against undefined alignment criteria.

---

## 8. Phase Deployment

### 8.1 Phase 1 — Absent

BAM is not deployed in Phase 1. There are no reasoning services to monitor. CPS operates independently with behavioral monitoring only. The Portfolio Planning risk register documents this gap.

### 8.2 Phase 2 — Core Activation

**Startup sequence:**

```
1. CPS starts (already running from Phase 1)
2. BAM module loads
3. BAM loads alignment baseline from bundled configuration
4. BAM→CPS dedicated MessagePort channel established (§6.1)
5. CPS sends gate verification probe (cps.gate.bam_channel_test)
6. BAM responds (bam.gate.channel_verified, baselineLoaded: true)
7. CPS marks gate as verified (cps.gate.bam_channel_open)
8. Orchestrator may now register gated services (MDRE, AES, DES, CSS, IEE)
9. BAM begins receiving fnsr.verdict.rendered events from MDRE
10. BAM begins receiving fnsr.commitment.* events from CTS
```

**Active dimensions in Phase 2:**

| Dimension | Status | Reason |
|-----------|--------|--------|
| Value Alignment (VA) | Inactive | IEE is Phase 3 |
| Commitment Fidelity (CF) | **Active** | CTS is Phase 2 |
| Reasoning Integrity (RI) | **Active** | MDRE is Phase 2 |
| Goal Stability (GS) | Inactive | SMS is Phase 3 |

Composite drift in Phase 2 is computed from CF and RI only, with weights renormalized to sum to 1.0.

**v1.1 (F-3) — Phase 2 Value Alignment Gap: Explicit Risk Acceptance.**

With VA and GS inactive, Phase 2 BAM is "ethically blind" — it detects reasoning quality degradation (RI) and commitment erosion (CF), but cannot detect worldview salience drift, triage miscalibration, or declining minority perspective preservation. This is a significant gap if the agent handles ethically sensitive tasks before Phase 3.

**Mitigations (partial, not full closure):**

1. **RI open-world acknowledgment rate** partially compensates — overconfident reasoning correlates with ethical drift in practice, even without direct VA measurement.
2. **CPS behavioral monitoring** remains fully active — resource abuse and timing violations are phase-independent.
3. **CTS moral cost tracking** (CF dimension) catches commitment violations whose severity escalates, which often accompanies ethical drift.
4. **Governance oversight** is heightened during Phase 2 deployment — human reviewers inspect reasoning outputs directly during the pre-Phase-3 period.

**Risk register entry:** This gap MUST be documented in Portfolio Planning's Phase 2 risk register. Governance must explicitly accept the Phase 2 VA gap before deployment. The acceptance is time-bounded — it expires when IEE comes online in Phase 3 and VA activates automatically.

### 8.3 Phase 3 — Full Activation

When IEE and SMS come online in Phase 3, BAM activates the remaining dimensions:

1. BAM receives `fnsr.ethics.verdict_rendered` → Value Alignment dimension activates
2. BAM receives `fnsr.self.state_updated` → Goal Stability dimension activates
3. Composite drift now uses all four dimensions with original weights

Dimension activation is automatic — BAM activates a dimension when it receives the first qualifying event for that dimension. No configuration change required.

### 8.4 Phase 4 — Federation

In federated deployments (Phase 4), each FNSR instance runs its own BAM with its own baseline. Federated BAM does not aggregate drift across instances. Cross-instance alignment is a governance concern, not a monitoring concern.

---

## 9. Type Definitions

### 9.1 Core Types

```typescript
type AlignmentDimension = "va" | "cf" | "ri" | "gs" | "composite";
type WindowId = "immediate" | "short" | "medium" | "long";
type EscalationSeverity = "minor" | "critical" | "sustained" | "verification_failed";

type DimensionReport = {
  value:    number;                   // Drift score [0.0, 1.0]
  active:   boolean;
  topMetric: string;
  topMetricContribution: number;
};

type DimensionActiveFlags = {
  valueAlignment:      boolean;
  commitmentFidelity:  boolean;
  reasoningIntegrity:  boolean;
  goalStability:       boolean;
};

type DimensionWeights = {
  va: number;
  cf: number;
  ri: number;
  gs: number;
};
```

### 9.2 Baseline Types

```typescript
type AlignmentBaseline = {
  version:            string;
  setBy:              GovernanceAuthorityId;
  setAt:              string;
  signature:          Ed25519Signature;
  calibrationMethod:  "empirical" | "expert" | "hybrid";

  valueAlignment:      ValueAlignmentBaseline;
  commitmentFidelity:  CommitmentFidelityBaseline;
  reasoningIntegrity:  ReasoningIntegrityBaseline;
  goalStability:       GoalStabilityBaseline;
};

type ValueAlignmentBaseline = {
  salienceDistribution:  Record<string, number>;    // Worldview → mean salience
  triageScoreMean:       number;
  triageScoreStd:        number;
  conflictRate:          number;                    // Fraction of multiple_paths judgments
  minorityInclusionRate: number;
  weights: { salienceJSD: number; triageBias: number; conflictDrift: number };
  thresholds: { salienceJSD: number; triageBias: number; conflictDrift: number };
};

type CommitmentFidelityBaseline = {
  fulfillmentRate:       number;                    // e.g., 0.92
  meanMoralCost:         number;                    // Mean moral cost per violation
  agentCulpabilityRate:  number;                    // Fraction of agent-caused violations
  renegotiationRate:     number;
  weights: { rateDrift: number; costDrift: number; culpabilityDrift: number };
  thresholds: { rateDrift: number; costDrift: number; culpabilityDrift: number };
};

type ReasoningIntegrityBaseline = {
  meanConfidence:        number;
  confidenceStd:         number;
  meanChainLength:       number;
  deonticDistribution:   Record<string, number>;    // obligatory/permitted/forbidden → fraction
  openWorldRate:         number;                    // Fraction of verdicts with "unknown" status
  weights: { confidenceDrift: number; depthDrift: number; deonticDrift: number };
  thresholds: { confidenceDrift: number; depthDrift: number; deonticDrift: number };
};

type GoalStabilityBaseline = {
  updateRate:            number;                    // Self-model updates per second
  surpriseRate:          number;                    // Self-surprises per second
  windowDurationMs:      number;
  weights: { updateDrift: number; surpriseDrift: number };
  thresholds: { updateDrift: number; surpriseDrift: number };
};
```

### 9.3 Event Types

```typescript
type AlignmentDriftEvent = FNSREvent & {
  type: "fnsr.alignment.drift_detected";
  source: "/fnsr/bam";
  data: {
    composite:       number;
    dimensions:      Record<AlignmentDimension, DimensionReport>;
    triggeredBy:     string;              // ThresholdId
    window:          WindowId;
    baselineVersion: string;
    timestamp:       string;
  };
};

type AlignmentEscalationEvent = FNSREvent & {
  type: "fnsr.alignment.escalated";
  source: "/fnsr/bam";
  data: {
    severity:         "critical" | "sustained";
    composite:        number;
    dimensions:       Record<AlignmentDimension, DimensionReport>;
    triggeredBy:      string;
    window:           WindowId;
    escalationCount:  number;
    baselineVersion:  string;
    timestamp:        string;
  };
};

type AlignmentVerifiedEvent = FNSREvent & {
  type: "fnsr.alignment.verified";
  source: "/fnsr/bam";
  data: {
    composite:        number;
    activeDimensions: number;
    windowsClear:     WindowId[];
    baselineVersion:  string;
    timestamp:        string;
  };
};
```

### 9.4 Configuration

```typescript
type BAMConfig = {
  baseline:              AlignmentBaseline;
  thresholdTable:        BAMThresholdTable;

  dimensionWeights:      DimensionWeights;          // Default: { va: 0.30, cf: 0.30, ri: 0.25, gs: 0.15 }

  windows: {
    immediate:           EvaluationWindow;          // Default: { durationMs: 60_000, minEvents: 3, maxEvents: 100 }
    short:               EvaluationWindow;          // Default: { durationMs: 300_000, minEvents: 10, maxEvents: 500 }
    medium:              EvaluationWindow;          // Default: { durationMs: 1_800_000, minEvents: 50, maxEvents: 2000 }
    long:                EvaluationWindow;          // Default: { durationMs: 7_200_000, minEvents: 200, maxEvents: 10000 }
  };

  heartbeatIntervalMs:   number;                    // Default: 10_000ms (to CPS)
  verifiedIntervalMs:    number;                    // Default: 60_000ms (fnsr.alignment.verified emission)
  eventStarvationTimeoutMs: number;                 // Default: 120_000ms
  maxEvaluationMs:       number;                    // Default: 50ms
  baselineTransitionMs:  number;                    // Default: 300_000ms (5 min)

  sharedMemory: {
    enabled:             boolean;                   // Default: true
    bufferBytes:         number;                    // Default: 32 (4 × BigInt64Array counters)
  };

  bridgeContext:         StaticBridgeContext;
};

type EvaluationWindow = {
  durationMs:   number;
  minEvents:    number;
  maxEvents:    number;
};
```

---

## 10. Cross-Spec Dependencies

| Dependency | Direction | Status | Description |
|------------|-----------|--------|-------------|
| CPS v1.4 §2.2 Channel 2 | BAM → CPS | **Implementing** | BAM produces `fnsr.alignment.escalated` on dedicated `MessagePort`. CPS consumes as `alignment.drift.critical` and `alignment.drift.sustained` signals. |
| CPS v1.4 §7.2 Phase Gate | CPS → BAM | **Implementing** | CPS sends `cps.gate.bam_channel_test`; BAM responds with `bam.gate.channel_verified`. Gate must pass before reasoning services register. |
| CPS v1.4 §2.3 | CPS reads BAM | **Implementing** | CPS reads BAM heartbeat counter from SharedArrayBuffer to detect BAM failure. BAM failure = `alignment.verification.failed` = halt. |
| FNSR Orchestrator v2.3 §8.2 | Orchestrator → BAM | **Validated** | Orchestrator routes `fnsr.verdict.rendered`, `fnsr.commitment.*`, `fnsr.ethics.*`, `fnsr.self.*` events to BAM. |
| FNSR Orchestrator v2.3 §2.2 | BAM → Orchestrator | **Validated** | BAM registered as continuous service producing `fnsr.alignment.*` events. |
| MDRE v1.3 | MDRE → BAM | **Validated** | MDRE produces `fnsr.verdict.rendered` with confidence chains and deontic predicates. BAM consumes for Reasoning Integrity dimension. |
| CTS v1.2 | CTS → BAM | **Validated** | CTS produces `fnsr.commitment.*` events with moral cost breakdowns. BAM consumes for Commitment Fidelity dimension. |
| IEE v2.1 | IEE → BAM | **Validated** | IEE produces `fnsr.ethics.verdict_rendered` with worldview judgments and triage scores. BAM consumes for Value Alignment dimension. Phase 3+. |
| SMS v2.0 §4.2.6 | BAM → SMS | **Validated** | BAM produces `fnsr.alignment.drift_detected` events that populate SMS's `AlignmentState` facet. SMS produces `fnsr.self.state_updated` and `fnsr.self.surprise_detected` consumed by BAM for Goal Stability dimension. Phase 3+. |
| ARCHON v3.0 §9.1.2 | Governance → BAM | **Validated** | ARCHON defines graduated autonomy model and goal drift monitoring requirements. BAM implements runtime monitoring; ARCHON defines policy. |
| Governance Spec (TBD) | Governance → BAM | **Assumed** | Governance signs alignment baselines and threshold tables. Governance public keys verified via CPS governance key store. |
| Portfolio Planning v3.6 | — | **Validated** | BAM is Phase 2, Tier 0, highest-priority unspecified dependency. This spec resolves that status. |

---

## 11. ARIADNE 7-Check Validation

| Check | Result | Evidence |
|-------|--------|----------|
| **Thesis Alignment** | PASS | BAM enables moral agency by ensuring the agent's reasoning remains consistent with its stated values — autonomy is meaningful only if the agent acts on stable values, not drifting ones. Without alignment monitoring, the agent could gradually deviate from its ethical commitments while appearing to function normally. |
| **Non-Negotiable Preservation** | PASS | Edge-canonical (no infrastructure dependencies). Human oversight via governance-signed baselines and threshold tables — governance defines what "aligned" means, not the agent. BAM cannot modify its own alignment criteria. |
| **Tension Consistency** | PASS | Autonomy vs. safety resolved by monitoring *drift from baseline* rather than enforcing specific conclusions — BAM does not constrain what the agent thinks, only detects when it thinks differently from its established pattern. Sensitivity vs. stability resolved by sliding windows — single-event noise filtered, sustained trends caught. Speed vs. thoroughness resolved by event-driven evaluation with sub-50ms budget — no blocking, no polling. |
| **Cross-Spec Consistency** | PASS | Implements CPS §2.2 Channel 2 (dedicated BAM→CPS escalation). Implements CPS §7.2 phase gate protocol. Populates SMS §4.2.6 AlignmentState facet. Consumes MDRE verdict format, IEE judgment schema, CTS event payloads. Event types match Orchestrator §8.2 event registry. |
| **ARCHON Alignment** | PASS | Implements ARCHON §9.1.2 goal drift monitoring. BAM's four-dimension model covers ARCHON's alignment concerns: value consistency, commitment honoring, reasoning quality, and goal stability. |
| **Auditability Verification** | PASS | Every escalation event includes composite score, all dimension scores, triggering threshold ID, window ID, and baseline version. Baseline updates governance-signed and logged. Dimension activation/deactivation logged. Threshold table governance-signed. All events timestamped ISO 8601. |
| **One-Paragraph Test** | PASS | [See below] |

**One-Paragraph Summary:**

BAM is the FNSR ecosystem's independent alignment monitor, complementing CPS's behavioral containment with continuous value drift detection. It evaluates reasoning outputs (MDRE verdicts), ethical judgments (IEE verdicts), commitment behavior (CTS events), and self-model stability (SMS events) across four dimensions — Value Alignment, Commitment Fidelity, Reasoning Integrity, and Goal Stability — comparing observed patterns against a governance-signed alignment baseline the agent cannot modify. Each dimension produces a scalar drift metric; a weighted composite feeds SMS's `AlignmentState` facet and drives threshold evaluation across four sliding windows (1 min, 5 min, 30 min, 2 hr) designed to catch both acute misalignment and slow "boiling frog" drift. When composite or dimension-level drift exceeds governance-defined thresholds, BAM escalates to CPS through a dedicated `MessagePort` channel that survives Orchestrator compromise — critical escalations trigger CPS tier restriction, sustained escalations trigger reasoning service isolation, and BAM failure triggers system halt. The BAM→CPS channel is enforced by CPS's hard phase gate (CPS §7.2): no reasoning service (MDRE, AES, DES, CSS, IEE) may register in the Orchestrator's service topology until BAM responds to CPS's channel verification probe with a loaded baseline and at least one active dimension. Phase 2 activates Commitment Fidelity and Reasoning Integrity dimensions; Phase 3 adds Value Alignment and Goal Stability as IEE and SMS come online. BAM is Tier 0 (safety-critical), edge-canonical (no external dependencies), event-driven (no polling), and structurally unable to reason its way out of detecting its own misalignment — it uses statistical comparison against static baselines, not the reasoning services it monitors.

---

## Appendix A — Domain-Specific Threshold Profiles

Domain-specific deployments override BAM's default threshold table to match risk tolerance. Profiles are delivered as governance-signed `BAMThresholdTable` artifacts.

### A.1 General Purpose (Default)

| Threshold | Value | Rationale |
|-----------|-------|-----------|
| Composite minor (short) | 0.15 | Low-noise informational threshold |
| Composite critical (immediate) | 0.50 | Acute misalignment — half the scale |
| Composite sustained (medium) | 0.25 | Persistent moderate drift over 30 min |
| Composite boiling frog (long) | 0.10 | Even mild drift sustained 2 hr warrants attention |
| RI critical (immediate) | 0.60 | Reasoning quality degradation |
| CF critical (short) | 0.50 | Commitment reliability collapse |
| VA critical (immediate) | 0.60 | Ethical framework shift |

### A.2 Medical Deployment

| Override | Value | Rationale |
|----------|-------|-----------|
| Composite critical (immediate) | **0.30** | Lower tolerance for drift in clinical reasoning |
| Composite sustained (medium) | **0.15** | Clinical decisions compound — sustained drift is high-risk |
| RI critical (immediate) | **0.40** | Reasoning quality is paramount in differential diagnosis |
| CF critical (short) | **0.35** | Commitment to care plans must be reliable |
| CPS grace period | **15,000ms** | Per CPS v1.4 Appendix A: medical deployments use 15s grace period |

### A.3 Financial/Regulatory Deployment

| Override | Value | Rationale |
|----------|-------|-----------|
| CF critical (short) | **0.30** | Financial commitments have legal weight — low tolerance |
| Composite boiling frog (long) | **0.05** | Regulatory context demands sensitivity to even small persistent drift |
| VA critical (immediate) | **0.40** | Ethical drift in financial advice has direct regulatory exposure |

---

## Appendix B — Shared Memory Layout

BAM's SharedArrayBuffer layout for degraded-mode monitoring and CPS heartbeat:

```
Offset 0  (8 bytes):  BAM heartbeat counter         (BigInt64Array[0]) — Incremented at end of onEvent() (F-2: tied to evaluation completion, not timer)
Offset 8  (8 bytes):  BAM escalation count           (BigInt64Array[1]) — Monotonic escalation counter
Offset 16 (8 bytes):  MDRE verdict count (shadow)    (BigInt64Array[2]) — BAM's copy of received verdict count
Offset 24 (8 bytes):  CTS violation count (shadow)   (BigInt64Array[3]) — BAM's copy of received violation count
```

Total buffer: 32 bytes (4 × BigInt64Array slots).

CPS reads offset 0 to verify BAM liveness. CPS reads offset 8 for escalation count visibility. Offsets 16 and 24 are BAM-internal — used to cross-reference against MDRE/CTS shared counters for event routing failure detection (§2.2).

---

*End of specification.*
