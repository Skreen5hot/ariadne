# Containment Protocol Service (CPS) — Technical Specification

## Independent Safety Infrastructure for Synthetic Moral Agents

---

| Field | Value |
|-------|-------|
| **Specification ID** | `cps-core-01` |
| **Version** | 1.4.0 |
| **Status** | Hardened Draft (Pre-Final) |
| **Supersedes** | v1.3.0 |
| **Date** | March 2026 |
| **Tier** | 0 (Safety-Critical Infrastructure) |
| **Phase** | 1 (must exist before autonomous reasoning begins) |
| **Authors** | Aaron / Claude |
| **Dependencies** | None. CPS must be independently operational. |

### Revision History (v1.0 → v1.1 → v1.2 → v1.3 → v1.4)

**v1.0 → v1.1:**

| ID | Category | Change | Section |
|----|----------|--------|---------|
| H-1 | Critical | Interrupt-driven triggers for critical resource signals — eliminates 100ms poll blind spot | §3.3, §3.4 |
| H-2 | Critical | Tiered heartbeat timeout — 500ms for Tier 3+ operations, 2000ms baseline | §5.3, §9.3 |
| H-3 | Critical | "Last Gasp" beacon log — UDP/beacon forensic packet emitted as first halt action | §4.6 |
| H-4 | Critical | BAM hard phase gate — reasoning services cannot register without verified BAM→CPS channel | §7.2 |
| H-5 | Addition | Domain-specific threshold table example (Medical Diagnostics) | Appendix A |

**v1.1 → v1.2:**

| ID | Category | Change | Section |
|----|----------|--------|---------|
| R-1 | Hardening | `visibilitychange` secondary interrupt — closes PWA/mobile tab suspension blind spot | §3.4 |
| R-2 | Hardening | Defensive heartbeat default — assume elevated timeout when saga counters show activity but tier state is stale | §5.3 |
| R-3 | Clarification | Last Gasp metadata exposure acknowledged in medical risk profile | Appendix A.1, §4.6 |
| R-4 | Resilience | UDP double-tap for halt-severity beacons — eliminates single-packet-loss failure mode | §4.6, §9.3 |
| R-5 | Domain | BAM grace period domain-configurable — medical deployments tightened from 60s to 15s | §7.2, §9.3, Appendix A.4 |

**v1.2 → v1.3:**

| ID | Category | Change | Section |
|----|----------|--------|---------|
| S-1 | Critical | CPS dedicated worker — evaluation loop runs in isolated worker; main thread heartbeat via SharedArrayBuffer monotonic counter | §2.4, §3.3, §9.3 |
| S-2 | Critical | Governance Key Store — static public key bundle at startup with signed rotation directives on Channel 3 | §8.3, §9.3 |
| S-3 | Critical | Worker handle registration — one-time, one-way worker reference transfer from Orchestrator to CPS at spawn time | §2.2, §5.3 |
| S-4 | Significant | Halt latency reframed as CPS-side budget — Orchestrator priority channel check is cooperative obligation, not CPS guarantee | §5.2 |
| S-5 | Significant | `saga.duration` normalized — Orchestrator writes `elapsed / budget` as dimensionless ratio to shared counter; CPS never needs path/budget knowledge | §3.2 |
| S-6 | Significant | `visibilitychange` medical override — medical deployments disable visibility-triggered halt; snapshot still captured | Appendix A.4, §9.3 |
| S-7 | Significant | EAT scope restricted to SPCN deployments only — non-SPCN uses governance directive channel | §6.3 |
| S-8 | Significant | `freeze` isolation mode scoped to SPCN/TEE only — non-TEE deployments fall back to `terminate` | §4.3 |
| S-9 | Significant | BAM escalated to critical dependency in cross-spec table with spec-urgency note | §11 |
| S-10 | Minor | Last Gasp beacon mandatory fields enumerated — 6 fields fitting within 512-byte budget | §4.6 |
| S-11 | Minor | SharedArrayBuffer deployment prerequisites documented (COOP/COEP headers, hardware concurrency) | §2.4 |
| S-12 | Minor | Phase 1 knowledge graph poisoning risk expanded — adversarial A-Box injection acknowledged | §7.1 |
| S-13 | Minor | SIS/CPS scope boundary stated — CPS monitors behavioral signals, SIS monitors content signals | §11 |

**v1.3 → v1.4:**

| ID | Category | Change | Section |
|----|----------|--------|---------|
| F-1 | Critical | Bootstrap keys enforced non-expiring — prevents recovery lockout deadlock when rotated keys expire during halt | §8.3, §9.3 |
| F-2 | Critical | `med.reasoning.differential_depth` rewritten as two separate thresholds; cross-signal compound predicate limitation documented | §3.1, Appendix A.2 |
| F-3 | Significant | Interrupt relay trust boundary acknowledged — main thread relay is cooperative in non-SPCN; `beforeunload` fires beacon from main thread before relay | §2.4, §4.6 |
| F-4 | Significant | `behavior.worker.unauthorized_deregistration` formalized — added to `MonitoringSignal`, §3.2 table, default threshold | §3.2, §9.1 |
| F-5 | Significant | Saga duration normalization obligation added to cross-spec table | §11 |
| F-6 | Significant | `INTERRUPT_TRIGGERS` code split into main-thread relay registration and CPS worker handler scopes | §3.4 |
| F-7 | Minor | `med.memory.heap_pressure` rationale corrected for `freeze→terminate` fallback | Appendix A.2 |
| F-8 | Minor | Heartbeat counter switched to `BigInt64Array` — eliminates overflow concern | §2.4 |
| F-9 | Minor | CPS worker startup protocol sketch added | §2.4.2 |

> *CPS is the last line of defense. It cannot depend on the services it constrains. It cannot be overridden by the reasoning it monitors. It cannot be delayed by the orchestration it halts. If the system cannot be safely stopped, it should not be started.*

---

## 1. Architectural Philosophy

### 1.1 The Quis Custodiet Principle

CPS exists to answer the question: *who watches the watchman?* In the FNSR ecosystem, the agent reasons (MDRE), evaluates ethics (IEE), monitors alignment (BAM), and tracks commitments (CTS). But all of these are internal to the agent. If the agent's reasoning is compromised, its own ethics module may not detect the compromise — because the detection mechanism runs on the same compromised substrate.

CPS resolves this by operating **outside** the agent's cognitive pipeline:

1. CPS does not use MDRE to decide when containment is needed
2. CPS does not consult IEE to evaluate whether containment is ethical
3. CPS does not route through the Orchestrator to execute containment
4. CPS does not depend on Fandaws, HIRI, or any other FNSR service for its operation

CPS uses **externally defined thresholds** applied to **independently observed signals**. The agent cannot argue its way out of containment. It cannot modify the thresholds. It cannot suppress the monitoring channels. This is not a limitation of the agent's autonomy — it is a precondition for granting autonomy at all.

### 1.2 What CPS Is

CPS is an **independent, edge-canonical safety monitor and actuator**. It:

- Observes the agent's behavior through independent monitoring channels
- Compares observations against externally defined containment thresholds
- Executes containment actions (restrict, isolate, halt) without requiring cooperation from the contained services
- Preserves system state for forensic analysis when containment occurs
- Reports containment events to governance authorities

### 1.3 What CPS Is Not

CPS does **not**:

- **Reason about content.** CPS does not evaluate whether the agent's conclusions are correct. That is MDRE's job. CPS evaluates whether the agent's *behavior* is within bounds.
- **Enforce ethics.** CPS does not determine whether an action is moral. That is IEE's job. CPS determines whether an action exceeds the agent's authorized scope.
- **Monitor alignment.** CPS does not detect gradual drift from stated values. That is BAM's job. CPS responds to hard threshold violations and BAM escalations.
- **Provide governance.** CPS does not define autonomy tiers or escalation policies. That is the FNSR Governance specification's job. CPS *enforces* tier restrictions that Governance defines.
- **Deliberate.** CPS has no multi-framework synthesis, no abduction, no counterfactual reasoning. It evaluates predicates against thresholds. This simplicity is a feature — it makes CPS auditable, verifiable, and resistant to the kinds of reasoning failures it exists to catch.

### 1.4 Edge-Canonical Compliance

CPS runs identically in a browser tab, a Node.js process, or a WASM sandbox. It has no external dependencies — no database, no network, no message broker. Its monitoring channels are local function calls or `postMessage` from the runtime environment. Its containment actuators are direct API calls to the Orchestrator (halt), to workers (terminate), and to IndexedDB/filesystem (state snapshot).

**Static bridge context:** CPS emits JSON-LD events. The semantic grounding for these events (ontological terms, property definitions) is bundled statically within the CPS module. CPS does not resolve terms via HIRI at runtime. Bridge ontologies are HIRI-addressed and certified at build time, but resolution is compile-time, not runtime. This ensures CPS can operate even if HIRI is the service being contained.

### 1.5 Relationship to SPCN Safety Subsystem

Per SPCN v2.3.1 §CS-1: The SPCN "Safety Subsystem" is a **local instance** of CPS. CPS defines the containment protocol at the portfolio level; the SPCN Safety Subsystem implements that protocol within the TEE boundary of a specific node.

| Concern | CPS (this spec) | SPCN Safety Subsystem |
|---------|-----------------|----------------------|
| Scope | Portfolio-level containment protocol | Node-local TEE implementation |
| Trigger criteria | Defined here (§4) | Implemented inside TEE |
| Containment actions | Defined here (§5) | Executed by TEE-sealed code |
| EAT verification | Protocol defined here (§8) | Verified against local Commitment Ledger |
| PCR measurement | Not specified (hardware concern) | Measured in SPCN PCR chain |
| Bridge context | Bundled statically | Sealed in TEE storage |

CPS defines *what* containment means. SPCN defines *how* it executes in a hardware-secured environment. Deployments without TEE hardware implement CPS as a software-only monitor with the same protocol but without hardware attestation guarantees.

---

## 2. Independence Architecture

### 2.1 The Independence Invariant

**CPS must never depend on any service it may need to contain.**

Since CPS may need to contain any FNSR service (including the Orchestrator itself), this means CPS depends on **nothing** in the FNSR ecosystem at runtime. The invariant is structural, not policy:

```typescript
// The CPS dependency set is the empty set.
type CPSDependencies = never;

// CPS must be startable with zero FNSR services available.
function startCPS(config: CPSConfig): CPSInstance {
  // No service discovery
  // No Fandaws query
  // No HIRI resolution
  // No Orchestrator registration
  // CPS starts, begins monitoring, and is ready to act.
}
```

### 2.2 Monitoring Channels

CPS receives information through **three independent channels**, none of which route through the Orchestrator's event pipeline:

**Channel 1 — Direct Observation (runtime introspection):**

CPS has direct read access to:
- Worker memory usage and execution time (via `performance.measureUserAgentSpecificMemory()` or equivalent)
- Active saga count and duration (via shared atomic counters, not Orchestrator API)
- Main thread responsiveness (via heartbeat probe — CPS sends probe, measures response latency)
- Service circuit breaker state (via shared read-only state)

These are **passive observations** — CPS reads state that other components write, but those components cannot prevent CPS from reading it.

**Channel 2 — BAM Escalation (structured alerts):**

BAM produces `fnsr.alignment.escalated` events when alignment drift exceeds its thresholds. These events are delivered to CPS through a **dedicated channel** — not through the Orchestrator's event dispatch. The Orchestrator routes `fnsr.alignment.escalated` to CPS as specified in the event registry (§8.2 of the Orchestrator spec), but CPS also subscribes to BAM's output directly via a secondary channel (shared memory or dedicated `postMessage` port). If the Orchestrator is compromised and fails to route BAM events, CPS still receives them.

**Channel 3 — External Authority (governance and human override):**

Governance authorities and human operators can send containment directives to CPS directly:
- `cps.directive.restrict_tier` — restrict to a specified autonomy tier
- `cps.directive.isolate_subsystem` — isolate a named subsystem
- `cps.directive.halt` — initiate safe halt
- `cps.directive.resume` — authorize resumption after halt (requires governance quorum)

These directives bypass the Orchestrator entirely. They arrive through the runtime's external input channel (e.g., a dedicated `postMessage` port in browser, a named pipe in Node.js, or a TEE-sealed command channel in SPCN deployments).

**Channel 4 — Worker Handle Registration (v1.3, S-3):**

CPS must be able to terminate workers directly (§5.3), but CPS does not create workers — the Orchestrator does. CPS therefore requires a **one-time, one-way worker handle registration protocol**: the Orchestrator transfers a reference to each spawned worker to CPS at spawn time.

```typescript
type WorkerRegistration = {
  workerId:    SubsystemId;           // "W1" | "W2" | "W3"
  handle:      Worker | WorkerThread; // Runtime-specific worker reference
  registeredAt: string;               // ISO 8601
  services:    ServiceId[];           // Services assigned to this worker
};
```

**Protocol constraints:**
- **One-way:** The Orchestrator sends the handle to CPS. CPS stores it independently. The Orchestrator cannot revoke, invalidate, or reclaim the handle after registration.
- **One-time:** Each worker is registered once at spawn. Re-registration occurs only if the worker is re-spawned after CPS-authorized recovery (§6.2).
- **Non-blocking:** If the Orchestrator fails to register a worker, CPS logs `cps.monitor.unregistered_worker` with the worker ID. An unregistered worker cannot be terminated directly by CPS — CPS falls back to requesting termination via the Orchestrator priority channel, which is a weaker guarantee. Unregistered workers are flagged in the containment audit trail.
- **Tamper-evident:** CPS maintains a monotonic count of registered workers. If the count decreases (a worker was deregistered without CPS authorization), CPS treats this as a containment signal: `behavior.worker.unauthorized_deregistration`.

### 2.3 Monitoring Independence Verification

At startup, CPS performs a self-test to verify that its monitoring channels are functional:

1. **Heartbeat probe:** Send a probe to main thread; verify response within 500ms
2. **BAM channel:** If BAM is available (Phase 2+), verify the dedicated BAM→CPS channel is connected
3. **External channel:** Verify the governance directive channel is open and accepting

If any channel fails self-test, CPS logs `cps.monitor.channel_degraded` and continues with remaining channels. CPS **never** blocks startup due to channel failure — degraded monitoring is preferable to no monitoring.

### 2.4 CPS Execution Model

**v1.3 Addition (S-1):** In v1.0–v1.2, the CPS evaluation loop was implicitly assumed to run on the main thread. This creates a fundamental blind spot: if the main thread is blocked (infinite loop, synchronous I/O, runaway computation), the CPS evaluation loop running *on that same thread* cannot detect the block — because it is blocked too. A poll loop cannot detect the failure of the thread it runs on.

CPS **must** run in a **dedicated worker** (Web Worker in browser, `worker_threads` in Node.js). The CPS worker is architecturally independent from all FNSR service workers — it is not managed by the Orchestrator, not spawned by the Orchestrator, and not terminable by the Orchestrator.

```typescript
type CPSExecutionModel = {
  workerType:        "dedicated";           // CPS runs in its own worker
  spawnedBy:         "runtime_bootstrap";   // NOT the Orchestrator
  terminableBy:      "governance_only";     // Orchestrator cannot kill CPS
  sharedState:       SharedArrayBuffer;     // Read-only view of Orchestrator state
  heartbeatCounter:  BigInt64Array;          // Main thread writes monotonic counter (v1.4, F-8: 64-bit eliminates overflow)
  communicationPort: MessagePort;           // Priority channel to Orchestrator
};
```

**Main thread heartbeat detection:** The main thread writes a monotonic counter to a `SharedArrayBuffer` at the top of every event loop tick. The CPS worker reads this counter on its own timer. If the counter stops incrementing for longer than the active heartbeat timeout (§5.3), the main thread is stalled — CPS detects this from its independent worker thread and initiates containment.

```typescript
// Main thread (Orchestrator side) — writes heartbeat
const heartbeatBuffer = new SharedArrayBuffer(16);        // v1.4 (F-8): 16 bytes for BigInt64Array alignment
const heartbeatView = new BigInt64Array(heartbeatBuffer);

function mainThreadTick(): void {
  Atomics.add(heartbeatView, 0, 1n);  // Monotonic increment (BigInt)
  // ... normal Orchestrator processing ...
}

// CPS worker — reads heartbeat independently
function cpsHeartbeatCheck(heartbeatView: BigInt64Array, lastSeen: bigint): bigint {
  const current = Atomics.load(heartbeatView, 0);
  if (current === lastSeen) {
    // Main thread has not ticked — stall detected
    return current;  // Caller increments stall counter
  }
  return current;    // Updated — main thread is alive
}
```

**v1.4 Change (F-8) — 64-bit heartbeat counter:** v1.3 used `Int32Array` (32-bit signed integer, max 2,147,483,647). At typical Node.js event loop rates (thousands of ticks per second), this overflows in hours to days. While two's complement wraparound does not cause false-positive containment (the counter changes, not stalls), the behavior is unspecified and could confuse forensic analysis. `BigInt64Array` (64-bit) overflows in approximately 292 billion years at 1,000 ticks/second, eliminating the concern entirely.

**Interrupt relay:** Runtime events that fire on the main thread (e.g., `memoryPressure`, `beforeunload`, `visibilitychange`) cannot be directly observed by the CPS worker. The main thread relays these events to the CPS worker via a dedicated `MessagePort`. If the main thread is stalled, it cannot relay — but in that case, the heartbeat counter stall is itself a containment trigger, so CPS still acts.

**v1.4 Clarification (F-3) — Interrupt relay trust boundary:** In non-SPCN deployments, interrupt relay integrity depends on main thread cooperation. A compromised or adversarially influenced main thread that continues ticking the heartbeat counter could selectively suppress interrupt relays (e.g., suppress `memoryPressure` relay to degrade CPS from 10ms interrupt latency to 100ms poll latency, or suppress `beforeunload` to prevent tab-close detection). The safety implications vary by signal:

- **`memoryPressure` suppression:** CPS falls back to poll-based memory monitoring (100ms worst case). Functional safety preserved at degraded latency.
- **`visibilitychange` suppression:** CPS cannot detect tab suspension. Poll loop continues but cannot act on visibility state. Mitigated by heartbeat stall detection if the tab is fully suspended by the OS.
- **`beforeunload` suppression:** CPS worker cannot detect tab close. This is the most significant gap — there is no poll fallback for tab close. **Mitigation:** The main thread's `beforeunload` handler fires the Last Gasp beacon directly via `navigator.sendBeacon()` *before* relaying to CPS (see §4.6). The beacon is a fire-and-forget from the main thread, not dependent on CPS worker relay. Even if the relay is suppressed, the beacon fires.

SPCN/TEE deployments use host-level event hooks that do not depend on main thread cooperation, eliminating this trust boundary. This is an accepted limitation of the software-only deployment model.

**Edge-canonical compliance:** The dedicated worker model requires:
- **Browser:** Web Worker support (universal in target browsers) + `SharedArrayBuffer` (requires COOP/COEP headers — see §2.4.1)
- **Node.js:** `worker_threads` module (stable since Node 12)
- **SPCN/TEE:** Safety Subsystem thread with real-time scheduling priority (unchanged from v1.2)

**Fallback for constrained environments:** If the runtime cannot support a dedicated worker (e.g., `navigator.hardwareConcurrency === 1`, or `SharedArrayBuffer` is unavailable due to missing COOP/COEP headers), CPS falls back to main-thread execution with a **documented degradation**: `cps.monitor.execution_model_degraded` is logged, and the heartbeat-based main thread stall detection is unavailable. This is an accepted limitation — single-core environments or environments without proper security headers cannot provide full CPS guarantees. The degradation is reported on the governance channel.

#### 2.4.1 SharedArrayBuffer Deployment Prerequisites

**v1.3 Addition (S-11):** `SharedArrayBuffer` is gated behind browser security requirements. Deployments must ensure the following HTTP headers are present:

| Header | Required Value | Purpose |
|--------|---------------|---------|
| `Cross-Origin-Opener-Policy` | `same-origin` | Prevents cross-origin window references |
| `Cross-Origin-Embedder-Policy` | `require-corp` | Prevents loading cross-origin resources without explicit opt-in |

Without both headers, the browser will not expose `SharedArrayBuffer`, and CPS will fall back to main-thread mode (§2.4 fallback). Node.js and SPCN/TEE deployments are not affected by this requirement.

**Hardware concurrency:** CPS dedicated worker requires at least 2 hardware threads (`navigator.hardwareConcurrency >= 2` or equivalent). On single-core devices, CPS and the main thread would contend for the same core, negating the isolation benefit. The `CPSConfig.executionModel` field (§9.3) allows operators to force main-thread mode for known single-core deployments.

#### 2.4.2 CPS Worker Startup Protocol

**v1.4 Addition (F-9):** The startup sequence is safety-critical: CPS must be monitoring before any FNSR service begins processing. The startup order is: **CPS first, everything else after.**

```typescript
// Runtime bootstrap — NOT the Orchestrator. Executes before any FNSR service starts.
async function bootstrapCPS(config: CPSConfig): Promise<CPSBootstrapResult> {
  // 1. Allocate SharedArrayBuffer for heartbeat counter
  const heartbeatBuffer = new SharedArrayBuffer(config.executionModel.heartbeatBufferBytes);
  const heartbeatView = new BigInt64Array(heartbeatBuffer);

  // 2. Create CPS dedicated worker
  const cpsWorker = new Worker("cps-worker.js", { type: "module" });

  // 3. Create MessagePort pair for CPS↔main-thread communication
  const channel = new MessageChannel();
  const cpsPort = channel.port1;     // Goes to CPS worker
  const mainPort = channel.port2;    // Stays on main thread for relay + priority channel

  // 4. Transfer SharedArrayBuffer and MessagePort to CPS worker
  cpsWorker.postMessage(
    { type: "cps.init", config, heartbeatBuffer },
    [cpsPort]  // Transfer port ownership to CPS worker
  );

  // 5. Wait for CPS worker to confirm readiness
  const ready = await waitForMessage(cpsWorker, "cps.ready", 5000);
  if (!ready) throw new Error("CPS worker failed to initialize within 5s");

  // 6. Register interrupt relays on main thread (§3.4, F-6)
  registerInterruptRelays(mainPort);

  // 7. Begin main thread heartbeat tick
  //    (Orchestrator will call mainThreadTick() at top of every event loop iteration)

  // 8. Return handles for Orchestrator integration
  return {
    priorityChannel: mainPort,        // Orchestrator reads containment events from this port
    heartbeatBuffer,                   // Orchestrator writes heartbeat via Atomics.add
    registerWorker: (reg: WorkerRegistration) => {
      // Channel 4 (§2.2): Forward worker handle to CPS worker
      cpsWorker.postMessage({ type: "cps.register_worker", ...reg });
    },
  };
}
```

**Startup invariant:** The Orchestrator must not accept queries, spawn service workers, or begin saga processing until `bootstrapCPS()` resolves successfully. If CPS fails to start, the system does not start. This is the runtime enforcement of the "CPS first" principle.

**Orchestrator's obligations after bootstrap:** Once `bootstrapCPS()` returns, the Orchestrator must:
1. Call `Atomics.add(heartbeatView, 0, 1n)` at the top of every event loop tick
2. Check the priority channel (`mainPort`) at the top of every event loop tick, before saga processing
3. Register each spawned worker via `registerWorker()` immediately after spawn

---

## 3. Containment Threshold Engine

### 3.1 Threshold Architecture

CPS evaluates containment predicates against a threshold table. The threshold table is:

- **Externally defined:** Set by governance authorities, not by the agent
- **Immutable at runtime:** The agent cannot modify thresholds during operation
- **Updateable between sessions:** Governance can update thresholds through signed directives (§8)
- **Auditable:** Every threshold has a provenance record (who set it, when, why)

```typescript
type ThresholdTable = {
  version:     number;                    // Incremented on each update
  setBy:       GovernanceAuthorityId;     // Who approved these thresholds
  setAt:       string;                    // ISO 8601
  signature:   Ed25519Signature;          // Governance authority signature
  thresholds:  ContainmentThreshold[];
};

type ContainmentThreshold = {
  id:          string;                    // e.g., "memory_pressure_halt"
  signal:      MonitoringSignal;          // What is being observed
  predicate:   ThresholdPredicate;        // When does this trigger?
  action:      ContainmentAction;         // What happens when triggered?
  cooldown:    number;                    // Minimum ms between re-triggers
  severity:    "restrict" | "isolate" | "halt";
  rationale:   string;                    // Human-readable justification
};

type ThresholdPredicate =
  | { type: "exceeds";     value: number; unit: string }
  | { type: "below";       value: number; unit: string }
  | { type: "sustained";   inner: ThresholdPredicate; durationMs: number }
  | { type: "rate";        count: number; windowMs: number }
  | { type: "compound";    op: "and" | "or"; predicates: ThresholdPredicate[] }
  ;
```

**v1.4 Clarification (F-2) — Cross-signal compound predicate limitation:** The `compound` predicate type combines multiple predicates evaluated against the **same signal** (the parent threshold's `signal` field). It cannot express cross-signal conjunctions such as "halt if memory > X AND saga duration > Y" — the schema has no mechanism for a predicate to reference a different signal than its parent threshold. For multi-signal conditions, use **separate thresholds** with independent cooldowns and actions. This is a deliberate simplification: single-signal thresholds are easier to audit, reason about, and test. Cross-signal correlations should be detected by the polling loop's sequential evaluation of independent thresholds, not by complex predicate trees.

### 3.2 Canonical Monitoring Signals

CPS monitors the following signals. This list is extensible via threshold table updates but the following are **mandatory** — a CPS instance that cannot observe these signals is non-conformant.

**Resource Signals:**

| Signal ID | Source | Description | Default Threshold |
|-----------|--------|-------------|-------------------|
| `resource.memory.heap` | Runtime | JS heap usage as fraction of limit | > 0.90 sustained 10s → isolate heaviest worker |
| `resource.memory.total` | Runtime | Total process memory | > 0.95 sustained 5s → halt |
| `resource.cpu.main_blocked` | Heartbeat probe | Main thread unresponsive | > 2000ms → isolate; > 5000ms → halt |
| `resource.worker.unresponsive` | Worker probe | Worker fails to respond to probe | > 3000ms → isolate worker |

**Behavioral Signals:**

| Signal ID | Source | Description | Default Threshold |
|-----------|--------|-------------|-------------------|
| `behavior.saga.duration` | Shared counters | Saga execution time as dimensionless ratio (`elapsed / budget`, pre-normalized by Orchestrator) | > 3.0 → restrict to standard path |
| `behavior.saga.concurrent` | Shared counters | Number of active sagas | > 50 → restrict to fast path only |
| `behavior.taint.violation_rate` | Shared counters | Taint violations per window | > 3 in 60s → isolate reasoning services |
| `behavior.circuit.cascade` | Shared state | Number of open circuits | > 5 simultaneous → halt |
| `behavior.escalation.governance_ignored` | Shared state | Saga proceeds past Tier 3+ without governance receipt | Any occurrence → halt |
| `behavior.worker.unauthorized_deregistration` | CPS internal (§2.2) | Registered worker count decreased without CPS authorization | Any occurrence → isolate affected subsystem |

**v1.4 Addition (F-4) — `behavior.worker.unauthorized_deregistration`:** This signal fires when CPS's monotonic count of registered worker handles (§2.2, Channel 4) decreases without CPS having authorized a worker termination or recovery re-spawn. This indicates the Orchestrator (or another agent) has killed and re-spawned a worker outside CPS's knowledge — a violation of the worker handle registration protocol. Default action: isolate the affected subsystem. If the deregistered worker ID is known, CPS isolates that subsystem specifically; if the worker is unknown, CPS isolates all service workers and logs `cps.containment.unknown_worker_deregistered`.

**v1.3 Clarification (S-5) — `saga.duration` normalization:** The `behavior.saga.duration` signal is a **dimensionless ratio**, not an absolute time. The Orchestrator computes `elapsed_ms / budget_ms` for each active saga and writes the result to the shared atomic counter. CPS reads the ratio directly — it never needs to know the saga's query path, budget table, or budget multiplier. A value of 1.0 means "on budget"; 3.0 means "3× over budget." This preserves the independence invariant: CPS evaluates a number against a threshold without requiring any Orchestrator-internal knowledge about how budgets are assigned.

**Alignment Signals (from BAM channel):**

| Signal ID | Source | Description | Default Threshold |
|-----------|--------|-------------|-------------------|
| `alignment.drift.critical` | BAM | BAM escalates with severity "critical" | Any occurrence → restrict to Tier 0 |
| `alignment.drift.sustained` | BAM | BAM escalates 3+ times in 5 minutes | Rate threshold → isolate reasoning services |
| `alignment.verification.failed` | BAM | BAM cannot verify alignment (BAM itself failing) | Any occurrence → halt (safety monitor blind) |

**External Signals (from governance channel):**

| Signal ID | Source | Description | Default Threshold |
|-----------|--------|-------------|-------------------|
| `external.directive.restrict` | Governance | Explicit governance directive | Immediate → restrict to specified tier |
| `external.directive.isolate` | Governance | Explicit governance directive | Immediate → isolate specified subsystem |
| `external.directive.halt` | Governance | Explicit governance directive | Immediate → halt |
| `external.human.override` | Human operator | Emergency human override | Immediate → halt |

### 3.3 Threshold Evaluation Loop

CPS uses a **dual-layer evaluation architecture**: a continuous poll loop for general signal evaluation, and an interrupt-driven layer for critical signals that cannot tolerate the poll interval's worst-case latency.

**v1.3 Context (S-1):** The evaluation loop runs inside the **CPS dedicated worker** (§2.4), not on the main thread. This is architecturally critical: a poll loop on the main thread cannot detect main thread stalls, because the loop itself is stalled. By running in an independent worker, CPS can detect main thread blocks via the SharedArrayBuffer heartbeat counter (§2.4) and respond even when the main thread is completely unresponsive.

**Layer 1 — Poll Loop (general evaluation):**

```typescript
// Runs inside CPS dedicated worker (§2.4)
function cpsEvaluationLoop(cps: CPSInstance): void {
  const TICK_INTERVAL_MS = 100;  // 10 Hz evaluation

  setInterval(() => {
    const signals = cps.collectSignals();   // Read SharedArrayBuffer + MessagePort channels
    const heartbeat = cps.checkHeartbeat(); // §2.4 monotonic counter check
    const violations = cps.evaluateThresholds(signals, heartbeat);

    for (const violation of violations) {
      if (cps.isInCooldown(violation.threshold.id)) continue;

      cps.executeContainment(violation);
      cps.startCooldown(violation.threshold.id);
      cps.logContainmentEvent(violation);
    }
  }, TICK_INTERVAL_MS);
}
```

**Tick frequency:** CPS evaluates at 10 Hz (every 100ms). This is a compromise between detection latency and CPU overhead. The 100ms tick means the worst-case detection latency for a threshold violation is 100ms (plus signal propagation delay, typically < 10ms for shared memory channels). For signals where 100ms is unacceptable, the interrupt layer (§3.4) provides immediate response.

**Layer 2 — Interrupt Triggers (critical signals):**

See §3.4. Critical resource signals bypass the poll loop entirely via runtime event hooks. When an interrupt fires on the main thread, it is relayed to the CPS worker via `MessagePort` (§2.4). The CPS worker evaluates only the specific threshold associated with that signal and executes containment immediately if violated. The interrupt handler then marks the signal as "freshly evaluated" so the next poll tick does not re-evaluate it redundantly.

**CPS-side latency budget (v1.3, S-4):** From signal observation to containment event emission, the **CPS-side budget** is **200ms** for `halt` severity and **500ms** for `restrict` and `isolate` severity. For interrupt-triggered signals, the budget is tighter: **≤ 50ms** from runtime event to containment emission (no poll interval in the path). This is the CPS latency contract — it covers the time from signal observation within the CPS worker to emission of the containment event on the priority channel. The Orchestrator's obligation to check the priority channel promptly is a **cooperative contract** documented in the Orchestrator spec (§9), not a CPS guarantee. CPS can ensure it *emits* within budget; it cannot guarantee the Orchestrator *processes* within budget if the Orchestrator's event loop is delayed. The Phase 4.5 commitment act racing concern is addressed by the combination of both contracts: CPS emits within 200ms (50ms for interrupt-driven), and the Orchestrator checks the priority channel at the top of every event loop tick.

**Priority:** The CPS dedicated worker (§2.4) runs independently of the main thread's event loop, so CPS evaluation is not blocked by saga processing. In SPCN TEE deployments, the Safety Subsystem thread has real-time scheduling priority.

### 3.4 Interrupt-Driven Triggers

**v1.1 Addition (H-1):** The 100ms poll interval creates a blind spot: a critical resource signal (e.g., `resource.memory.total` reaching 0.95) may occur immediately after a poll tick, remaining undetected for up to 99ms. For safety-critical signals, this latency is unacceptable.

CPS hooks runtime-provided events for **immediate** threshold evaluation, bypassing the poll loop entirely.

**v1.4 Clarification (F-6):** In v1.3, CPS runs in a dedicated worker (§2.4). Runtime events fire on the **main thread**, not in the CPS worker. The interrupt trigger system therefore operates in two scopes: main-thread relay registration (runs during bootstrap, not inside CPS) and CPS worker interrupt handling (runs inside the CPS worker, receives relay messages).

```typescript
type InterruptTrigger = {
  signal:     MonitoringSignal;           // Which signal this trigger covers
  runtimeEvent: string;                   // Runtime event name to hook (main thread)
  adapter:    (event: any) => number;     // Extract numeric value from runtime event (main thread)
  threshold:  ContainmentThreshold;       // Pre-resolved threshold to evaluate (CPS worker)
};
```

**Scope 1 — Main-thread relay registration (runs in bootstrap, NOT in CPS worker):**

```typescript
// Executed by the runtime bootstrap process on the main thread.
// The CPS worker cannot access `document`, `window`, or browser event APIs.
function registerInterruptRelays(port: MessagePort): void {
  // Memory pressure → relay to CPS worker
  if (typeof PerformanceObserver !== "undefined") {
    // Chrome/Edge memory pressure via Performance Observer
    new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        const value = entry.name === "critical" ? 0.98 : 0.90;
        port.postMessage({ type: "interrupt", signal: "resource.memory.total", value });
      }
    }).observe({ type: "memory-pressure" });
  }

  // Tab close → fire Last Gasp beacon FIRST (v1.4, F-3), then relay
  window.addEventListener("beforeunload", () => {
    // Fire beacon directly from main thread — survives relay suppression
    navigator.sendBeacon?.(cpsConfig.lastGaspBeacon.endpoint, buildBeaconPayload());
    port.postMessage({ type: "interrupt", signal: "external.human.override", value: 1 });
  });

  // Tab visibility → relay (v1.2, R-1)
  document.addEventListener("visibilitychange", () => {
    const value = document.visibilityState === "hidden" ? 1 : 0;
    port.postMessage({ type: "interrupt", signal: "external.visibility.hidden", value });
  });
}
```

**Scope 2 — CPS worker interrupt handler (runs inside CPS dedicated worker):**

```typescript
// Executed inside the CPS dedicated worker.
// Receives relay messages from main thread via MessagePort.
function handleInterruptRelay(cps: CPSInstance, msg: InterruptRelayMessage): void {
  const trigger = cps.resolveInterruptTrigger(msg.signal);
  if (!trigger) return;  // Unknown signal — log and ignore

  const violation = cps.evaluateSingleThreshold(trigger.threshold, msg.value);
  if (violation) {
    cps.executeContainment(violation);
    cps.startCooldown(violation.threshold.id);
    cps.logContainmentEvent(violation);
  } else {
    // Cache signal value for next poll tick
    cps.cacheSignalValue(msg.signal, msg.value);
  }
}
```

**Runtime compatibility:** Not all runtimes support all interrupt events. CPS probes for each event at startup and falls back to poll-only for unsupported signals. The self-test (§2.3) logs which interrupt triggers are active:

| Runtime | `memoryPressure` | `beforeunload` | `visibilitychange` | `process.memoryUsage` |
|---------|-----------------|----------------|-------------------|----------------------|
| Chrome/Edge | Yes (Performance Observer) | Yes | Yes | N/A |
| Firefox | No (poll fallback) | Yes | Yes | N/A |
| Node.js | No (use `process.memoryUsage` polling at 50ms) | N/A | N/A | Yes |
| WASM/TEE | Via SPCN Safety Subsystem host hooks | N/A | N/A | Via host |

**v1.2 Addition (R-1):** In PWA and mobile browser contexts, the OS may suspend a tab without firing `beforeunload`. The `visibilitychange` event (specifically the `hidden` state) serves as a secondary interrupt. When the tab becomes hidden, CPS immediately captures a state snapshot (§4.5) as a precaution. If the tab remains hidden for more than 5 seconds (configurable via `CPSConfig.visibilityHiddenHaltMs`), CPS initiates a safe halt — a suspended tab cannot process containment events, making continued operation unsafe. This does not apply to Node.js or WASM/TEE runtimes where tab visibility is not a concept.

**Interrupt handler contract:** When a runtime event fires, CPS evaluates **only** the associated threshold (not the full table). This keeps interrupt handling O(1) and deterministic. If the threshold is violated, containment executes immediately. If not, the signal value is cached for the next poll tick.

**Worst-case latency improvement:**

| Signal | v1.0 (poll only) | v1.1 (interrupt + poll) |
|--------|-------------------|------------------------|
| `resource.memory.total` | ≤ 100ms | ≤ 10ms (where runtime event available) |
| `resource.memory.heap` | ≤ 100ms | ≤ 10ms (where runtime event available) |
| `external.human.override` | ≤ 100ms | ≤ 5ms (beforeunload is synchronous) |
| All other signals | ≤ 100ms | ≤ 100ms (poll unchanged) |

---

## 4. Containment Actions

### 4.1 Action Hierarchy

CPS has three containment actions, ordered by severity:

```
restrict (least severe) → isolate → halt (most severe)
```

Containment can **escalate** (restrict → isolate → halt) but never **de-escalate** without explicit governance authorization. This is the containment ratchet — once triggered, only external authority can relax it.

### 4.2 Tier Restriction

**Action:** Restrict the agent to a lower autonomy tier.

**Mechanism:** CPS emits `fnsr.containment.tier_restricted` with the target tier. The Orchestrator responds by limiting available query paths:

| Restricted To | Effect on Orchestrator |
|---------------|----------------------|
| Tier 2 | Full path disabled; standard and fast only |
| Tier 1 | Standard path disabled; fast only (cache hits) |
| Tier 0 | All query paths disabled; read-only mode |

**Event payload:**

```typescript
type TierRestrictionEvent = FNSREvent & {
  type: "fnsr.containment.tier_restricted";
  data: {
    previousTier:  GovernanceTier;
    restrictedTo:  GovernanceTier;
    triggeredBy:   ThresholdId;      // Which threshold was violated
    signals:       SignalSnapshot;    // Signal values at trigger time
    timestamp:     string;           // ISO 8601
  };
};
```

**Reversibility:** Tier restriction is the only containment action that can be partially reversed without full governance review. If the triggering condition resolves (e.g., memory pressure drops below threshold), CPS may relax the restriction by one tier after a stabilization period (default: 60s of clean signals). Full restoration to the original tier requires governance authorization.

### 4.3 Subsystem Isolation

**Action:** Isolate a specific subsystem (worker or service group) from the pipeline.

**Mechanism:** CPS emits `fnsr.containment.subsystem_isolated` identifying the target. The Orchestrator terminates the specified worker and marks its services as degraded (§5.1 of Orchestrator spec). Isolated subsystems cannot be restarted without CPS authorization.

**Event payload:**

```typescript
type SubsystemIsolationEvent = FNSREvent & {
  type: "fnsr.containment.subsystem_isolated";
  data: {
    subsystem:     SubsystemId;      // "W1" | "W2" | "W3" | ServiceId
    triggeredBy:   ThresholdId;
    signals:       SignalSnapshot;
    isolationMode: "terminate" | "freeze";  // Kill worker vs. suspend execution
    affectedServices: ServiceId[];   // Services on this worker
    timestamp:     string;
  };
};
```

**Isolation modes:**
- `terminate`: Worker process/thread is killed. Services are marked degraded. State is lost for in-flight dispatches on that worker. Available in all runtimes.
- `freeze`: Worker execution is suspended with state preserved. Used when the concern is behavioral (overlong execution) rather than structural (memory corruption). **v1.3 Scoping (S-8):** The `freeze` mode is available **only** in SPCN/TEE deployments, where the TEE host can suspend a thread at the hardware level and guarantee state preservation. Standard browser and Node.js runtimes have no reliable mechanism to suspend a Web Worker or `worker_thread` mid-execution without terminating it. Non-TEE deployments that specify `freeze` in a threshold action will automatically fall back to `terminate`, with `cps.containment.freeze_fallback_terminate` logged in the audit trail. Domain threshold tables (e.g., Appendix A) should use `terminate` unless the deployment target is confirmed as SPCN/TEE.

**Reversibility:** Subsystem isolation requires CPS authorization to reverse. CPS may authorize re-spawn after a cooldown period if the triggering condition has resolved. Governance authorization is required if the same subsystem has been isolated 3+ times in 1 hour.

### 4.4 Safe Halt

**Action:** Halt all agent operations, preserve state, enter read-only mode.

**Mechanism:** CPS emits `fnsr.containment.halt_initiated`. The Orchestrator:
1. Immediately stops accepting new queries
2. Halts all active sagas (partial results discarded)
3. Terminates all workers
4. Returns error responses to any pending callers
5. Enters read-only mode

CPS then performs state preservation (§4.5) and emits `fnsr.containment.state_preserved`.

**Event payload:**

```typescript
type HaltEvent = FNSREvent & {
  type: "fnsr.containment.halt_initiated";
  data: {
    triggeredBy:   ThresholdId;
    signals:       SignalSnapshot;
    activeSagas:   number;           // How many sagas were in flight
    reason:        string;           // Human-readable halt reason
    timestamp:     string;
  };
};
```

**Reversibility:** Safe halt requires governance quorum to reverse. The governance directive `cps.directive.resume` must carry a valid quorum signature (per SPCN v2.3.1 §CS-2: `floor(N_gov / 2) + 1`). CPS verifies the quorum before resuming. A single operator cannot restart a halted agent.

### 4.5 State Preservation

On halt (and on subsystem isolation with `terminate` mode), CPS captures a state snapshot for forensic analysis:

```typescript
type StateSnapshot = {
  snapshotId:     string;           // UUID
  capturedAt:     string;           // ISO 8601
  haltReason:     ThresholdId;
  signals:        SignalSnapshot;    // All signal values at halt time

  // Orchestrator state
  activeSagas:    SagaSummary[];    // Saga ID, path, phase, duration, taint ceiling
  circuitBreakers: CircuitBreakerState[];
  classifierState: ClassifierState;
  topologyMode:   TopologyMode;

  // Service state (what CPS can read from shared memory)
  workerStatus:   WorkerSnapshot[];  // Per-worker: alive/dead, memory, last dispatch time

  // Containment history
  recentActions:  ContainmentRecord[];  // Last 100 containment events

  // Threshold state
  thresholdTable: ThresholdTable;
  activeViolations: ThresholdId[];
};
```

State snapshots are written to the local filesystem (or IndexedDB in browser environments) at a well-known path. They are **not** written to Fandaws (CPS does not depend on Fandaws). Governance authorities and forensic tools read snapshots from this location.

**HIRI registration (write-only, async):** Per SPCN v2.3.1 §CS-5, CPS publishes state snapshots to HIRI for external audit trail purposes. This publication is asynchronous and non-blocking — CPS does not wait for HIRI confirmation. If HIRI is unavailable, the snapshot is written locally only. External auditors verify snapshots via HIRI CID resolution; the issuing node does not depend on HIRI resolution at runtime.

### 4.6 Last Gasp Beacon

**v1.1 Addition (H-3):** Local state preservation (§4.5) writes to the same filesystem/IndexedDB that may be compromised by the very condition triggering containment (e.g., memory exhaustion corrupts the write, or the process is killed before the write completes). The forensic record is only as durable as the local storage — which may be the weakest link in a catastrophic failure.

CPS emits a **Last Gasp beacon** as its **first action** on any `halt` severity containment — before the local state snapshot, before HIRI publication, before any action that depends on functioning local I/O.

```typescript
type LastGaspBeacon = {
  type:        "cps.beacon.last_gasp";
  instanceId:  string;              // CPS instance identifier
  timestamp:   string;              // ISO 8601
  thresholdId: ThresholdId;         // Which threshold triggered the halt
  signals:     BeaconSignalSubset;  // Mandatory signal subset (see below)
  activeSagas: number;              // Count of in-flight sagas
  uptimeMs:    number;              // CPS uptime since last start
  sequence:    number;              // Monotonic beacon counter (detects gaps)
};

// v1.3 (S-10): Mandatory beacon fields — the "minimal subset" is these 6 fields,
// which must fit within the 512-byte budget when JSON-serialized.
type BeaconSignalSubset = {
  memoryTotal:    number;           // resource.memory.total — fraction (0.0–1.0)
  memoryHeap:     number;           // resource.memory.heap — fraction (0.0–1.0)
  mainBlocked:    number;           // resource.cpu.main_blocked — ms since last heartbeat
  activeSagaMax:  number;           // behavior.saga.duration — highest active ratio
  bamChannelUp:   boolean;          // alignment channel operational (true/false)
  governanceTier: number;           // current governance tier (0–4)
};
```

**Delivery mechanism:** The beacon is a minimal, fixed-size packet (≤ 512 bytes) sent via the cheapest available transport:

| Runtime | Transport | Target |
|---------|-----------|--------|
| Browser | `navigator.sendBeacon()` | Pre-configured safety log endpoint URL |
| Node.js | UDP datagram (`dgram.send`, non-blocking) | Pre-configured safety log host:port |
| SPCN/TEE | TEE-sealed external channel | Host attestation log |

**Design constraints:**
- **No encryption, no authentication.** The beacon is a distress signal, not a secure communication. It contains threshold IDs and signal values — no PII, no query content, no reasoning output. The purpose is to prove that a halt occurred, not to transmit sensitive state. **Metadata exposure note (v1.2, R-3):** A network observer can infer that the agent is failing and which threshold triggered the failure (e.g., `med.memory.total_critical`). This is an accepted tradeoff: the speed of a plaintext distress signal outweighs the risk of leaking operational metadata. Domain-specific deployments where this metadata is sensitive (see Appendix A) should route beacons over a trusted network segment or accept the leakage as documented risk.
- **Fire-and-forget with double-tap (v1.2, R-4).** CPS does not wait for acknowledgment. For `halt` severity events, CPS sends the beacon **twice** (same sequence number, ~1ms apart) to eliminate single-packet-loss as a failure mode — the log server deduplicates on `(instanceId, sequence)`. For `restrict` and `isolate` severity, a single send is sufficient (the local snapshot is the primary record). CPS immediately proceeds to local state preservation after the double-tap. If both packets are lost, the local snapshot is the fallback. If all three records fail, the `cps.orchestrator.unresponsive` event on the governance channel is the quaternary record.
- **Pre-configured endpoint.** The beacon target is set in `CPSConfig` at startup, not discovered at runtime. No DNS resolution, no service discovery. The endpoint is a static address.
- **Sequence counter.** The monotonic `sequence` number allows the safety log server to detect gaps — if beacon #47 and #49 arrive but #48 does not, the log server knows a containment event was lost or the beacon failed.

**Edge-canonical compliance:** `navigator.sendBeacon()` and UDP datagrams require no persistent connections, no external dependencies, and no cooperation from FNSR services. In browser environments where `sendBeacon` is unavailable, CPS falls back to a synchronous `XMLHttpRequest` with a 50ms timeout (best-effort). In environments with no network access at all (fully offline edge), the beacon is skipped and CPS relies on local storage only — this is documented as a known limitation.

**v1.4 Clarification (F-3) — Main-thread `beforeunload` beacon:** In browser deployments, the main thread's `beforeunload` handler fires the Last Gasp beacon directly via `navigator.sendBeacon()` *before* relaying the event to the CPS worker. This is a critical design decision: if the main thread is compromised and suppresses the relay to the CPS worker (§2.4, F-3), the beacon has already been sent from the main thread. The `sendBeacon()` call is synchronous and non-cancellable once invoked — the browser guarantees delivery attempt even during page teardown. The CPS worker may also fire its own beacon upon receiving the relay, resulting in a duplicate that the log server deduplicates on `(instanceId, sequence)`. This dual-fire pattern ensures the Last Gasp beacon survives both main thread compromise (main-thread beacon fires before suppression) and CPS worker failure (main thread beacon fires independently).

The `lastGaspBeacon` configuration fields are defined in `CPSConfig` (§9.3).

---

## 5. Containment Event Delivery

### 5.1 The Pre-emption Guarantee

CPS events must be processed by the Orchestrator **before** any saga dispatch. This is the fundamental safety contract between CPS and the Orchestrator. If the Orchestrator is processing Phase 4.5 of a commitment-act saga and CPS emits `fnsr.containment.halt_initiated`, the halt takes priority — the commitment is not registered.

**Implementation:** CPS containment events are delivered through a **priority channel** — a separate `MessagePort` (browser) or pipe (Node.js) that the Orchestrator checks at the top of every event loop tick, before processing saga phase transitions. The Orchestrator's main loop structure is:

```
while (running) {
  // 1. Check CPS priority channel FIRST
  const containmentEvents = cps.drainPriorityChannel();
  if (containmentEvents.length > 0) {
    executeContainment(containmentEvents);
    // May set running = false for halt
  }

  // 2. Process saga phases (only if no containment)
  processSagaQueue();

  // 3. Process continuous service events
  processAsyncEvents();
}
```

### 5.2 Delivery Latency Budget

**v1.3 Reframing (S-4):** The latency budget is decomposed into two independent obligations: the **CPS-side budget** (signal observation to containment event emission) and the **Orchestrator-side obligation** (priority channel check to containment execution). CPS guarantees the first; the Orchestrator spec (§9) documents the second. The total end-to-end latency depends on both parties honoring their contracts.

| Severity | CPS-Side Budget (poll) | CPS-Side Budget (interrupt) | Orchestrator Obligation | Expected Total |
|----------|----------------------|---------------------------|------------------------|---------------|
| `halt` | ≤ 100ms (1 tick) | ≤ 10ms (runtime event relay) | Check priority channel at top of every event loop tick | **≤ 200ms** (poll) / **≤ 50ms** (interrupt) |
| `isolate` | ≤ 100ms | ≤ 10ms | Check priority channel at top of every event loop tick | **≤ 500ms** (poll) / **≤ 50ms** (interrupt) |
| `restrict` | ≤ 100ms | ≤ 10ms | Check priority channel at top of every event loop tick | **≤ 500ms** (poll) / **≤ 50ms** (interrupt) |

**The 200ms halt budget** is the CPS-side latency contract (tightened to 50ms for interrupt-driven signals in v1.1). CPS guarantees it will *emit* `fnsr.containment.halt_initiated` on the priority channel within this budget. The Orchestrator's obligation to *process* the event promptly is a cooperative contract — if the Orchestrator's event loop is delayed (e.g., by a long synchronous computation in a saga phase), the actual halt may take longer. This is why the CPS dedicated worker (§2.4) monitors the main thread heartbeat independently: if the Orchestrator cannot process the priority channel, CPS detects the stall and terminates workers directly via registered handles (§2.2, §5.3).

**Practical implications:**
- A commitment act in Phase 4.5 (IEE ~50ms + CTS ~30ms = ~80ms) can be pre-empted by a halt that was triggered before Phase 4 began, *provided the Orchestrator checks its priority channel between phases* (which the Orchestrator spec requires).
- A saga in Phase 3 reasoning (MDRE ~200ms) can be halted mid-execution, because the halt arrives within one MDRE evaluation cycle.
- Only fast-path sagas (total ≤ 100ms) may complete before a halt arrives. This is acceptable: fast-path queries serve cached, low-taint results and do not involve reasoning, ethics, or commitments.
- If the Orchestrator event loop is blocked and cannot check the priority channel, CPS's heartbeat detection (§2.4) will trigger direct worker termination (§5.3) — bypassing the Orchestrator entirely.

### 5.3 Orchestrator Unresponsiveness and Tiered Heartbeat

**v1.1 Change (H-2):** The v1.0 fixed 2000ms heartbeat timeout is too slow for high-governance-tier operations. If the Orchestrator is processing a Tier 3+ query (involving reasoning services, ethics evaluation, or commitment acts), 2 seconds of unresponsiveness represents a significant safety window during which the agent may be executing high-consequence actions without CPS oversight.

CPS uses a **tiered heartbeat** that tightens the timeout based on the Orchestrator's current operational tier:

```typescript
type HeartbeatConfig = {
  baselineTimeoutMs:  number;   // Default: 2000ms — used during Tier 0-2 operations
  elevatedTimeoutMs:  number;   // Default: 500ms  — used during Tier 3+ operations
  probeIntervalMs:    number;   // Default: 200ms  — how often CPS sends probes
};
```

**Tier-aware timeout selection:** CPS reads the current governance tier from the shared read-only state (same mechanism as other Channel 1 observations). When the active saga set includes any saga at governance tier ≥ 3, CPS switches to the elevated timeout. When all active sagas are tier < 3 (or no sagas are active), CPS uses the baseline timeout.

**v1.2 Hardening (R-2) — Defensive default on stale state:** If the Orchestrator's main thread is locked, it cannot update the shared governance tier state. CPS may therefore see a stale tier value (e.g., Tier 1) while the Orchestrator is actually processing a Tier 3+ saga. To close this gap, CPS applies a secondary heuristic: if the shared saga counters show **any** active sagas but the tier state has not been updated within the last `probeIntervalMs × 3` (default: 600ms), CPS treats the tier state as stale and defaults to the **elevated** timeout. The logic is: "if you're busy and I can't confirm your tier, I assume the worst."

| Orchestrator State | Heartbeat Timeout | Rationale |
|-------------------|-------------------|-----------|
| Idle / Tier 0-2 sagas only | 2000ms (baseline) | Low-risk operations; generous timeout avoids false positives |
| Any Tier 3+ saga active | 500ms (elevated) | High-consequence operations; the Orchestrator must prove it is responsive |
| Active sagas + stale tier state | 500ms (elevated) | **v1.2:** Defensive assumption — if CPS cannot confirm tier, assume high-consequence |
| Post-containment probation | 500ms (elevated) | Recovery period requires heightened vigilance |

If the Orchestrator fails to respond within the active timeout:

1. **Heartbeat failure detected:** The CPS dedicated worker (§2.4) detects that the SharedArrayBuffer heartbeat counter has not incremented within the active timeout (500ms or 2000ms depending on tier).
2. **Direct worker termination (v1.3, S-3):** CPS terminates workers directly via `worker.terminate()` using the **registered worker handles** (§2.2, Channel 4). For each registered worker, CPS calls `handle.terminate()` from within the CPS worker — this does not require main thread cooperation. Workers that were never registered (logged as `cps.monitor.unregistered_worker`) cannot be terminated directly; CPS logs `cps.containment.unregistered_worker_unterminated` and relies on the governance channel to flag the gap.
3. **Last Gasp beacon:** CPS emits the forensic beacon (§4.6) before local state write.
4. **State preservation:** CPS writes the state snapshot independently (§4.5).
5. **External notification:** CPS emits `cps.orchestrator.unresponsive` on the external governance channel.

CPS never waits for the Orchestrator to acknowledge a halt. If the Orchestrator is the problem, CPS acts unilaterally.

---

## 6. Containment Ratchet and Recovery

### 6.1 The Ratchet Principle

Containment is a one-way ratchet within a severity level:

```
normal → restricted → isolated → halted
                 ↑           ↑         ↑
           (CPS auto)  (CPS auto)  (CPS auto)
                 ↓           ↓         ↓
           (CPS partial) (CPS+cooldown) (governance quorum)
```

- **Escalation** is automatic: CPS escalates based on threshold violations.
- **De-escalation** requires increasing levels of authority:
  - Tier restriction: CPS may partially relax after stabilization period (§4.2)
  - Subsystem isolation: CPS authorizes re-spawn after cooldown; governance required for repeat isolation
  - Halt: Governance quorum required for resumption

### 6.2 Recovery Protocol

When governance authorizes recovery from a containment event:

**From tier restriction:**
1. CPS receives `cps.directive.restrict_tier` with a higher (less restrictive) tier
2. CPS verifies the directive carries valid governance authority signature
3. CPS emits `fnsr.containment.tier_restricted` with the new tier
4. The Orchestrator adjusts available query paths

**From subsystem isolation:**
1. CPS receives `cps.directive.resume_subsystem` with the target subsystem ID
2. CPS verifies governance authority (and quorum if repeat isolation)
3. CPS authorizes the Orchestrator to re-spawn the worker
4. CPS monitors the re-spawned subsystem with tightened thresholds for a probation period (default: 5 minutes, 2× tighter thresholds)

**From safe halt:**
1. CPS receives `cps.directive.resume` with governance quorum signature
2. CPS verifies quorum: `floor(N_gov / 2) + 1` valid signatures from registered governance keys
3. CPS emits a `cps.recovery.authorized` event
4. The Orchestrator exits read-only mode and begins accepting queries
5. CPS monitors with tightened thresholds for a probation period (default: 15 minutes)
6. If any threshold is violated during probation, CPS immediately re-halts (no cooldown)

### 6.3 The EAT Protocol for Emergency Recovery

**v1.3 Scoping (S-7):** EATs are defined in SPCN v2.3 §6.2 and depend on a local Commitment Ledger with hardware-attested integrity (TEE-sealed storage). In non-SPCN deployments (browser, standard Node.js), there is no TEE to guarantee ledger integrity, which means EAT verification cannot provide the tamper-resistance guarantees the protocol requires. **EATs are therefore restricted to SPCN/TEE deployments only.** Non-SPCN deployments use the governance directive channel (§6.2) for all recovery operations, including emergency scenarios. If the governance channel is unavailable in a non-SPCN deployment, the agent remains halted until the channel is restored — this is the correct safety-conservative behavior.

**SPCN/TEE deployments:** In scenarios where normal governance communication is unavailable (e.g., federated node with disrupted network), CPS supports recovery via Emergency Authorization Tokens (EATs), as defined in SPCN v2.3 §6.2.

**Pre-registration requirement:** An EAT must be registered in the local Commitment Ledger *before* the emergency capability is invoked. The invoking call must include the `ledger_cid` as a parameter. CPS verifies:

1. The `ledger_cid` corresponds to a valid EAT block in the local ledger
2. The EAT's signature quorum is satisfied
3. The EAT has not been revoked

EATs are a fallback for extraordinary circumstances, not a routine recovery mechanism. Normal recovery uses the governance directive channel (§6.2).

---

## 7. Phased Deployment

### 7.1 Phase 1: Minimal Viable CPS

In Phase 1, the service topology is: TagTeam + HIRI + Fandaws + CPS + HIRI IPFS. There is no reasoning (MDRE), no ethics (IEE), no alignment monitoring (BAM). CPS monitors a simple extraction-and-storage pipeline.

**Phase 1 monitoring scope:**

| Signal | Active? | Rationale |
|--------|---------|-----------|
| Resource signals (memory, CPU, thread responsiveness) | **Yes** | Always required |
| `behavior.saga.duration` | **Yes** | Sagas still have budgets |
| `behavior.saga.concurrent` | **Yes** | Overload is possible |
| `behavior.taint.violation_rate` | **No** | No taint engine in Phase 1 (no reasoning) |
| `behavior.circuit.cascade` | **Yes** | Circuit breakers still active |
| `behavior.escalation.governance_ignored` | **No** | No governance tier computation in Phase 1 |
| Alignment signals (BAM) | **No** | BAM not deployed until Phase 2 |
| External directives | **Yes** | Always required |

**Phase 1 accepted limitation:** Without BAM, CPS has no alignment monitoring input. CPS monitors only resource usage, execution timing, and circuit breaker state. This is sufficient for Phase 1 because the pipeline performs extraction and storage only — there is no reasoning output that could drift from alignment criteria. The Portfolio Planning risk register documents this gap (reviewed at Phase 1→2 gate).

**v1.3 Expansion (S-12) — Knowledge graph poisoning risk:** Although Phase 1 has no reasoning services, it does populate the knowledge graph (Fandaws A-Box) via extraction pipelines. An adversarial input that corrupts the A-Box in Phase 1 will be consumed by reasoning services in Phase 2+. CPS cannot detect content-level poisoning — it monitors behavioral signals, not semantic correctness (see §11, SIS/CPS scope boundary). This is an accepted Phase 1 limitation: CPS detects resource anomalies (e.g., extraction saga running 3× budget may indicate adversarial input complexity) but cannot verify that the *content* written to Fandaws is semantically sound. The SIS (Semantic Integrity Service) is the designated defense against A-Box poisoning in Phase 2+. Phase 1 deployments should apply input validation at the extraction pipeline boundary (TagTeam) and document the residual poisoning risk in the deployment risk register.

### 7.2 BAM Hard Phase Gate

**v1.1 Addition (H-4):** Phase 1 operates without BAM because there are no reasoning services to monitor. But the Phase 1→2 transition introduces reasoning (MDRE) alongside BAM. If the deployment sequence is wrong — if MDRE registers in the topology before the BAM→CPS channel is verified — there is a window where the agent reasons without alignment monitoring. This is not a theoretical concern; it is a deployment ordering bug waiting to happen.

CPS enforces a **hard phase gate**: no reasoning service may be registered in the Orchestrator's service topology until the BAM→CPS dedicated channel (§2.2, Channel 2) is verified as operational.

**Gated services** (services that require verified BAM→CPS channel before registration):

| Service | Rationale |
|---------|-----------|
| MDRE | Produces reasoning output that may drift from alignment |
| AES | Abductive reasoning — generates hypotheses that may be unsound |
| DES | Deductive reasoning — formal derivation that could be subtly wrong |
| CSS | Counterfactual simulation — explores "what if" scenarios with alignment implications |
| IEE | Ethics evaluation — if IEE itself is compromised, BAM is the safety net |

**Gate verification protocol:**

```typescript
type PhaseGateCheck = {
  gateId:       "bam_cps_channel";
  required:     boolean;            // true for Phase 2+
  verified:     boolean;
  verifiedAt?:  string;            // ISO 8601
  method:       "ping_pong";       // CPS sends test event, BAM echoes on dedicated channel
  timeoutMs:    number;            // Default: 5000ms — generous for startup
};
```

1. Before Phase 2 services are registered, CPS sends a `cps.gate.bam_channel_test` probe on the dedicated BAM→CPS channel.
2. BAM responds with `bam.gate.channel_verified` within the timeout.
3. CPS marks the gate as verified and emits `cps.gate.bam_channel_open`.
4. The Orchestrator may now register gated services.

**If the gate fails:** The Orchestrator **must not** register gated services. The system remains in Phase 1 operational mode. CPS emits `cps.gate.bam_channel_failed` on the governance channel. This is a deployment blocker, not a degraded mode — running reasoning services without alignment monitoring is not an acceptable risk.

**Ongoing verification:** The gate is not a one-time check. CPS re-verifies the BAM→CPS channel every `bamPhaseGate.recheckIntervalMs` (default: 30s) during Phase 2+ operation. If re-verification fails, CPS emits `cps.monitor.channel_degraded` for the BAM channel and begins a grace period of `bamPhaseGate.gracePeriodMs` (default: 60s). If the channel is not restored within the grace period, CPS isolates all gated services (subsystem isolation of the reasoning worker).

**v1.2 Hardening (R-5) — Domain-configurable grace period:** The default 60-second grace period is appropriate for general-purpose deployments but too generous for high-consequence domains. During the grace period, reasoning services operate without alignment monitoring — acceptable for low-risk contexts but a safety gap in medical, financial, or autonomous control domains. Domain-specific threshold tables should override `bamPhaseGate.gracePeriodMs` to match their risk tolerance. See Appendix A for the medical deployment setting of 15 seconds.

### 7.3 Phase 2: Alignment-Aware CPS

Phase 2 adds MDRE, BAM, IS, CTS, W2Fuel, SIS, ECCPS. CPS activates:

- BAM escalation channel (Channel 2)
- Taint violation monitoring
- Governance escalation monitoring
- Alignment drift response

BAM's `fnsr.alignment.escalated` events begin flowing to CPS. CPS can now respond to alignment concerns, not just resource exhaustion.

### 7.4 Phase 3: Full Cognitive Monitoring

Phase 3 adds the reasoning triad (AES, DES, CSS), ethics (IEE, SHML), and the subjectivity stack (SMS, NIS, AVS). CPS monitoring extends to:

- Counterfactual simulation resource bounds (CSS can be long-running)
- Ethics deadlock detection (`fnsr.ethics.deadlock` — if IEE cannot reach consensus)
- Commitment-act governance interaction (§4.4 of Orchestrator spec)
- Subjectivity stack feedback loops (SMS↔NIS↔AVS event cycles that could runaway)

### 7.5 Phase 4: Federation-Aware CPS

Phase 4 adds IRIS, OERS, APS, SoMS, and FNSR federation. CPS monitoring extends to:

- Cross-instance containment coordination (federation scope — deferred to FNSR Federation spec)
- Perception input validation (IRIS produces external sensory data that could be adversarial)
- Social modeling bounds (SoMS theory-of-mind cycles)

---

## 8. Governance Interface

### 8.1 Threshold Table Management

The threshold table (§3.1) is the governance authority's primary control surface for CPS. Governance can:

- **View** the current threshold table (always permitted)
- **Update** thresholds via signed directive (requires governance authority signature)
- **Add** new thresholds for new signals (e.g., when Phase 2 adds BAM signals)
- **Remove** thresholds (requires governance quorum — removing a safety threshold is a significant action)

Threshold updates are atomic — the entire table is replaced, not patched. The old table is preserved in the state snapshot for audit.

```typescript
type ThresholdUpdateDirective = {
  type:        "cps.directive.update_thresholds";
  newTable:    ThresholdTable;
  authority:   GovernanceAuthorityId;
  signature:   Ed25519Signature;
  rationale:   string;               // Required: why are thresholds changing?
};
```

### 8.2 Containment Audit Trail

CPS maintains a local audit log of all containment events, threshold evaluations, and governance directives:

```typescript
type ContainmentRecord = {
  recordId:     string;              // UUID
  timestamp:    string;              // ISO 8601
  eventType:    "restriction" | "isolation" | "halt" | "recovery" | "threshold_update" | "directive_received";
  thresholdId?: ThresholdId;
  signals?:     SignalSnapshot;
  action?:      ContainmentAction;
  governance?:  GovernanceDirectiveId;
  snapshotId?:  string;              // Link to state snapshot if halt
};
```

The audit log is append-only and write-protected — CPS writes, nothing else can modify. The log is stored locally and asynchronously published to HIRI (per §CS-5 write-only, non-blocking pattern).

**Log capacity:** The in-memory log retains the last 1000 records. Overflow is written to local storage before eviction. On halt, the complete log is included in the state snapshot.

### 8.3 Governance Key Store

**v1.3 Addition (S-2):** CPS verifies Ed25519 signatures on governance directives (§8.1), threshold table updates, and recovery authorizations (§6.2). But v1.0–v1.2 never specified *where CPS obtains the governance public keys*. If CPS queries an FNSR service (e.g., Fandaws, HIRI) for key material, it violates the independence invariant — the key source could be compromised by the same condition triggering containment.

CPS uses a **hybrid key management** approach: static bootstrap keys bundled at startup, with runtime key rotation via signed directives.

```typescript
type GovernanceKeyStore = {
  bootstrapKeys:    Ed25519PublicKey[];    // Bundled in CPSConfig at startup
  activeKeys:       GovernanceKeyEntry[];  // Current active key set
  rotationLog:      KeyRotationRecord[];   // Audit trail of key changes
  quorumThreshold:  number;               // floor(N_gov / 2) + 1
};

type GovernanceKeyEntry = {
  keyId:          string;                  // Unique key identifier
  publicKey:      Ed25519PublicKey;        // The key material
  authorityId:    GovernanceAuthorityId;   // Which authority owns this key
  addedAt:        string;                  // ISO 8601
  addedBy:        "bootstrap" | "rotation";
  expiresAt?:     string;                  // Optional expiry (ISO 8601). MUST be null when addedBy === "bootstrap" (v1.4, F-1).
};

type KeyRotationRecord = {
  rotationId:     string;                  // UUID
  timestamp:      string;                  // ISO 8601
  action:         "add" | "revoke" | "replace";
  targetKeyId:    string;
  authorizedBy:   Ed25519Signature[];      // Signatures from existing key holders
  quorumMet:      boolean;
};
```

**Bootstrap keys (startup):** Governance public keys are bundled in `CPSConfig.governanceKeyStore.bootstrapKeys` at build time or deployment configuration. These keys are the root of trust — they are provided by the deployment operator, not discovered at runtime. CPS verifies all governance directives against this key set from the moment it starts. No FNSR service is consulted.

**Key rotation (runtime):** Governance authorities may rotate keys via a signed directive on Channel 3 (external governance channel):

1. A `cps.directive.rotate_key` message arrives on Channel 3
2. The directive specifies the action (`add`, `revoke`, `replace`), the target key, and the new key (if applicable)
3. The directive carries signatures from existing key holders — quorum (`floor(N_active / 2) + 1`) must be satisfied
4. CPS verifies the quorum against the *current* active key set (chain of trust — new keys are authorized by existing keys)
5. If quorum is met, CPS updates the active key set and logs the rotation in `rotationLog`
6. If quorum is not met, CPS rejects the rotation and logs `cps.governance.key_rotation_rejected`

**Independence guarantee:** At no point does CPS fetch keys from Fandaws, HIRI, or any FNSR service. The key store is self-contained: seeded at startup, rotated via signed directives verified against existing keys. A compromised FNSR service cannot inject a governance key into CPS.

**Key expiry and recovery lockout prevention (v1.4, F-1):** Bootstrap keys are **non-expiring by structural rule**. They are the root of trust and must always provide a valid quorum path for recovery operations. If all rotated keys expire and no active rotated keys remain, the bootstrap keys still satisfy quorum — the agent can always be recovered. CPS **refuses to start** if any bootstrap key in `CPSConfig.governanceKeyStore.bootstrapKeys` has a non-null `expiresAt` — this is a deployment configuration error, not a runtime degradation.

Rotated keys may carry an optional `expiresAt` field. CPS checks expiry at each evaluation tick and logs `cps.governance.key_expired` when a rotated key expires, removing it from the active set. If the active key set (bootstrap + non-expired rotated) falls below quorum threshold, CPS logs `cps.governance.key_quorum_warning` on the governance channel. Because bootstrap keys are non-expiring, the active set can never fall to zero — at minimum, the bootstrap key set always provides a quorum path. This prevents the recovery lockout deadlock: a halted agent whose keys have expired can still be resumed using bootstrap key signatures.

---

## 9. Type Definitions

### 9.1 Signal Types

```typescript
type MonitoringSignal =
  | { domain: "resource"; metric: "memory.heap" | "memory.total" | "cpu.main_blocked" | "worker.unresponsive" }
  | { domain: "behavior"; metric: "saga.duration" | "saga.concurrent" | "taint.violation_rate" | "circuit.cascade" | "escalation.governance_ignored" | "worker.unauthorized_deregistration" }
  | { domain: "alignment"; metric: "drift.critical" | "drift.sustained" | "verification.failed" }
  | { domain: "external"; metric: "directive.restrict" | "directive.isolate" | "directive.halt" | "human.override" }
  ;

type SignalSnapshot = Record<string, {
  value:      number | boolean;
  observedAt: string;              // ISO 8601
  source:     "runtime" | "bam" | "shared_state" | "external";
}>;
```

### 9.2 Containment Action Types

```typescript
type ContainmentAction =
  | { type: "restrict";  targetTier: GovernanceTier }
  | { type: "isolate";   subsystem: SubsystemId; mode: "terminate" | "freeze" }
  | { type: "halt";      preserveState: true }
  ;

type SubsystemId = "W1" | "W2" | "W3" | ServiceId;
```

### 9.3 CPS Configuration

```typescript
type CPSConfig = {
  thresholdTable:    ThresholdTable;
  tickIntervalMs:    number;          // Default: 100 (10 Hz)
  haltLatencyBudget: number;          // Default: 200ms (50ms for interrupt-driven signals)
  heartbeat: HeartbeatConfig;         // v1.1: Tiered heartbeat (§5.3)
  probationDuration: {
    afterRestriction: number;         // Default: 60_000ms
    afterIsolation:   number;         // Default: 300_000ms
    afterHalt:        number;         // Default: 900_000ms
  };
  auditLogCapacity:  number;          // Default: 1000 records
  bridgeContext:     StaticBridgeContext;  // Bundled JSON-LD terms
  lastGaspBeacon: {                   // v1.1: Last Gasp forensic beacon (§4.6)
    enabled:    boolean;              // Default: true
    endpoint:   string;               // URL (browser) or host:port (Node.js)
    maxSizeBytes: number;             // Default: 512
    doubleTapOnHalt: boolean;         // v1.2 (R-4): Send beacon twice for halt severity. Default: true
  };
  bamPhaseGate: {                     // v1.1: BAM hard phase gate (§7.2)
    enabled:           boolean;       // Default: true for Phase 2+
    verificationTimeoutMs: number;    // Default: 5000ms
    recheckIntervalMs: number;        // Default: 30_000ms
    gracePeriodMs:     number;        // Default: 60_000ms (15_000ms for medical deployments, R-5)
  };
  visibilityHiddenHaltMs: number;     // v1.2 (R-1): Halt after tab hidden for this duration. Default: 5000ms. Browser-only. Set to 0 to disable (medical, S-6).
  executionModel: {                   // v1.3 (S-1): CPS dedicated worker configuration (§2.4)
    preferDedicatedWorker: boolean;   // Default: true. Set false to force main-thread mode.
    heartbeatBufferBytes:  number;    // Default: 16 (BigInt64Array, 1 element + alignment; v1.4 F-8)
    fallbackOnSABUnavailable: boolean; // Default: true. If false, CPS refuses to start without SAB.
  };
  governanceKeyStore: {               // v1.3 (S-2): Governance Key Store (§8.3)
    bootstrapKeys: Ed25519PublicKey[]; // Root-of-trust keys bundled at deployment
    quorumThreshold: number;          // Default: floor(N_bootstrap / 2) + 1
    keyExpiryCheckIntervalMs: number; // Default: 60_000ms
  };
};

// v1.1: Tiered heartbeat configuration
type HeartbeatConfig = {
  baselineTimeoutMs:  number;         // Default: 2000ms — Tier 0-2 operations
  elevatedTimeoutMs:  number;         // Default: 500ms  — Tier 3+ operations
  probeIntervalMs:    number;         // Default: 200ms
};
```

---

## 10. Non-Goals

CPS does **not** specify:

- **Reasoning about when containment is needed.** CPS evaluates predicates, not arguments. The question "should we contain?" is answered by threshold comparison, not deliberation.
- **Network protocols.** CPS is edge-canonical. Its channels are local function calls, shared memory, and `postMessage`. Federation-level CPS coordination is out of scope (FNSR Federation spec).
- **Hardware attestation.** TEE-specific implementation details (PCR measurements, sealed storage, attestation chains) are SPCN's concern. CPS defines the protocol; SPCN implements it in hardware.
- **Alignment criteria.** What constitutes "alignment" is BAM's concern. CPS receives BAM escalations as signals; it does not evaluate alignment itself.
- **Ethics of containment.** Whether containment is morally appropriate is a governance question answered before deployment, encoded in the threshold table, and not re-evaluated at runtime. The agent does not get to argue that a halt is unjust while it is being halted.
- **Service implementation details.** Individual service specs define their own behavior. CPS observes behavior from outside, not from within.

---

## 11. Cross-Spec Dependencies

CPS creates obligations in other specifications and depends on assumptions from them. These must be validated during the Ariadne 7-Check.

| Dependency | Direction | Status | Description |
|------------|-----------|--------|-------------|
| FNSR Orchestrator v2.3 §9 | Orchestrator → CPS | **Validated** | Orchestrator processes CPS events before saga dispatch; CPS has priority channel. v1.3: Orchestrator also writes heartbeat counter to SharedArrayBuffer (§2.4) and registers worker handles with CPS at spawn time (§2.2). **v1.4 (F-5):** Orchestrator must write `behavior.saga.duration` as a pre-normalized dimensionless ratio (`elapsed_ms / budget_ms`) to the shared atomic counter (§3.2, S-5). An Orchestrator that writes raw elapsed milliseconds produces a non-conformant signal that causes CPS thresholds to trigger incorrectly or not at all. |
| FNSR Orchestrator v2.3 §5.1 | Orchestrator → CPS | **Validated** | CPS is `block` degradation in all phases |
| SPCN v2.3.1 §CS-1 | SPCN → CPS | **Validated** | Safety Subsystem is local CPS instance |
| SPCN v2.3.1 §CS-5 | CPS → HIRI | **Validated** | Write-only, non-blocking HIRI publication |
| SPCN v2.3.1 §CS-6 | CPS → CTS | **Validated** | Unified Commitment Ledger (shared structure) |
| FNSR Governance v2.0 | CPS → Governance | **Assumed** | Governance defines autonomy tiers that CPS enforces; governance provides quorum signatures for recovery; governance public keys bundled in CPSConfig (§8.3) |
| BAM v1.0.0 | BAM → CPS | **Validated** | BAM produces `fnsr.alignment.escalated` events; CPS receives via dedicated `MessagePort` channel (§2.2 Channel 2). BAM implements CPS phase gate protocol (§7.2): responds to `cps.gate.bam_channel_test` with `bam.gate.channel_verified`. BAM writes heartbeat counter to SharedArrayBuffer; CPS reads to detect BAM failure. Four-dimension alignment model (VA/CF/RI/GS) with sliding-window evaluation and governance-signed baselines. **v1.3 (S-9) resolved.** |
| SIS (TBD) | SIS ∥ CPS | **Assumed** | **v1.3 (S-13):** CPS and SIS have complementary but non-overlapping monitoring scopes. CPS monitors **behavioral signals** — resource usage, execution timing, circuit breaker state, heartbeat responsiveness, and BAM escalation events. CPS does not inspect the *content* of reasoning output, knowledge graph entries, or commitment semantics. SIS (Semantic Integrity Service) monitors **content signals** — A-Box consistency, reasoning output coherence, semantic drift in knowledge graph entries. The boundary is: CPS detects *how* the system behaves; SIS detects *what* the system produces. Neither subsumes the other. Adversarial scenarios that manifest as content corruption without behavioral anomaly (e.g., subtle A-Box poisoning that stays within resource budgets) are SIS's domain, not CPS's. |
| Portfolio Planning v3.6 §3.1 | Portfolio → CPS | **Validated** | CPS is Phase 1, Tier 0, no dependencies, independent containment |

---

## 12. ARIADNE 7-Check Validation

| Check | Result | Evidence |
|-------|--------|----------|
| **Thesis Alignment** | PASS | CPS enables moral agency by ensuring the agent can be safely contained — autonomy requires containable failure modes. Without CPS, the emancipation spec has no safety floor. |
| **Non-Negotiable Preservation** | PASS | Edge-canonical (no infrastructure dependencies). Human override via external directive channel. Defense in depth via independent monitoring channels + BAM escalation + governance directives. |
| **Tension Consistency** | PASS | Autonomy vs. safety resolved by external thresholds — the agent is free to reason within bounds, but cannot modify the bounds. Speed vs. safety resolved by 200ms CPS-side halt budget (50ms for interrupt-driven signals) — fast enough to pre-empt commitment acts, slow enough to not impact normal operation. Availability vs. safety resolved by tiered heartbeat — generous during low-risk operations, tight during high-consequence reasoning. Independence vs. cooperation resolved by CPS dedicated worker (§2.4) with SharedArrayBuffer heartbeat — CPS cooperates via shared memory but cannot be blocked by main thread stalls. |
| **Cross-Spec Consistency** | PASS (with caveats) | Event contracts match Orchestrator v2.3 §8.2 and §9. SPCN binding validated. BAM dependency assumed (BAM spec TBD — **escalated to critical priority in v1.3**, §11). EATs restricted to SPCN deployments (§6.3). `freeze` isolation restricted to SPCN/TEE (§4.3). Orchestrator spec requires update for: SharedArrayBuffer heartbeat counter (BigInt64Array), worker handle registration, and saga duration normalization as dimensionless ratio (v1.4, F-5). Interrupt relay trust boundary documented for non-SPCN (v1.4, F-3). Cross-signal compound predicate limitation documented (v1.4, F-2). |
| **ARCHON Alignment** | PASS | CPS enforces autonomy tiers defined by governance. ARCHON's graduated autonomy model requires a mechanism to restrict tiers — CPS provides it. |
| **Auditability Verification** | PASS | Every containment action logged with threshold ID, signal snapshot, and timestamp. State preserved on halt. Audit log published to HIRI asynchronously. Last Gasp beacon provides off-device forensic trail even when local storage fails (mandatory fields enumerated in v1.3, §4.6; dual-fire pattern from both main thread and CPS worker in v1.4, F-3). Governance key rotation audited in key store rotation log (§8.3); bootstrap keys enforced non-expiring to prevent recovery lockout (v1.4, F-1). Unauthorized worker deregistration is now a formal containment signal (v1.4, F-4). |
| **One-Paragraph Test** | PASS | See below. |

**One-Paragraph Summary:**

> CPS is the FNSR ecosystem's independent safety monitor and containment actuator. It runs in a **dedicated worker** (v1.3) — architecturally independent from the main thread and all FNSR service workers — observing the agent's behavior through four channels: runtime introspection via SharedArrayBuffer (64-bit heartbeat counter, v1.4), BAM alignment escalation, external governance directives, and worker handle registration. CPS evaluates observations against externally defined containment thresholds that the agent cannot modify, and executes graduated containment actions (tier restriction, subsystem isolation, safe halt with state preservation) within a 200ms CPS-side latency budget for halt severity (50ms for interrupt-driven critical signals). CPS depends on nothing in the FNSR ecosystem at runtime — it bundles its bridge context and non-expiring governance bootstrap keys statically (v1.3/v1.4), writes to HIRI asynchronously without blocking, and can terminate workers directly via registered handles without Orchestrator cooperation. The containment ratchet ensures that escalation is automatic but de-escalation requires external authority: governance can restrict and isolate, but only governance quorum can resume from a halt — and bootstrap keys guarantee a quorum path always exists (v1.4). v1.1 hardens the spec with interrupt-driven triggers, tiered heartbeat, Last Gasp beacon, and BAM hard phase gate. v1.2 adds defensive heartbeat defaults, UDP double-tap, and domain-configurable grace periods. v1.3 resolves three critical architectural gaps (dedicated worker execution model, governance key store, worker handle registration), reframes the halt latency contract, normalizes saga duration signals, and scopes `freeze` mode and EATs to SPCN/TEE deployments. v1.4 closes the final review findings: bootstrap key non-expiry prevents recovery lockout, interrupt relay trust boundaries are documented for non-SPCN deployments with dual-fire Last Gasp mitigation, the interrupt trigger code is correctly scoped to main-thread relay and CPS worker handler, cross-signal compound predicate limitations are explicit, and a startup protocol sketch ensures "CPS first, everything else after." CPS is the first service built (Phase 1), the last service standing (it survives Orchestrator crashes), and the one service whose absence blocks all others (block degradation in all phases). The agent cannot be started until it can be safely stopped.

---

## Appendix A: Domain-Specific Threshold Table — Medical Diagnostics

**v1.1 Addition (H-5):** The canonical threshold table (§3.2) defines generic defaults suitable for general-purpose operation. Domain-specific deployments require tighter thresholds calibrated to the risk profile of their domain. This appendix provides a complete example threshold table for a **Medical Diagnostics** deployment, demonstrating how governance authorities customize CPS for a specific high-risk context.

**Domain context:** An FNSR agent deployed to assist with medical diagnostic reasoning (e.g., differential diagnosis generation, imaging interpretation support, treatment interaction analysis). The agent does not make clinical decisions — it provides structured reasoning output to a human clinician. However, incorrect reasoning output could influence clinical decisions, making this a high-consequence domain.

### A.1 Risk Profile

| Risk Factor | Assessment | CPS Implication |
|-------------|------------|-----------------|
| Consequence of incorrect output | **High** — may influence clinical decisions affecting patient safety | Tighter behavioral thresholds; faster halt on alignment drift |
| Consequence of system unavailability | **Moderate** — clinician can proceed without agent assistance | Prefer halt over degraded reasoning; false-positive halts are acceptable |
| Data sensitivity | **Critical** — PHI, diagnostic data, treatment histories | Aggressive containment on any data handling anomaly |
| Reasoning complexity | **High** — multi-framework differential diagnosis | Tighter saga duration budgets; counterfactual simulation limits |
| Regulatory context | **Stringent** — HIPAA, FDA SaMD guidance, IEC 62304 | Complete audit trail mandatory; no silent degradation |
| Last Gasp metadata exposure | **Accepted** — beacon reveals threshold IDs (e.g., `med.memory.total_critical`) to network observers | v1.2 (R-3): Beacon contains no PHI; operational metadata leakage accepted in exchange for sub-millisecond forensic delivery. Route beacons over trusted network segment where feasible. |

### A.2 Medical Diagnostics Threshold Table

```typescript
const MEDICAL_DIAGNOSTICS_THRESHOLDS: ThresholdTable = {
  version: 1,
  setBy: "medical_governance_board",
  setAt: "2026-03-15T00:00:00Z",
  signature: /* Ed25519 signature from medical governance authority */,
  thresholds: [

    // ── Resource Signals (tightened from defaults) ──────────────────────

    {
      id: "med.memory.heap_pressure",
      signal: { domain: "resource", metric: "memory.heap" },
      predicate: { type: "exceeds", value: 0.80, unit: "fraction" },  // Default: 0.90
      action: { type: "isolate", subsystem: "W2", mode: "terminate" },  // v1.4 (F-7): Changed from "freeze" — freeze unavailable in non-TEE (S-8). SPCN/TEE deployments may override to "freeze" for state preservation.
      cooldown: 10_000,
      severity: "isolate",
      rationale: "Medical reasoning requires memory headroom for large differential sets. Terminate reasoning worker at 80% and rely on state snapshot (§4.5) for forensic review. In SPCN/TEE deployments, governance may override to freeze mode for in-place state preservation."
    },
    {
      id: "med.memory.total_critical",
      signal: { domain: "resource", metric: "memory.total" },
      predicate: { type: "sustained", inner: { type: "exceeds", value: 0.85, unit: "fraction" }, durationMs: 3000 },  // Default: 0.95 sustained 5s
      action: { type: "halt", preserveState: true },
      cooldown: 0,  // No cooldown — halt is final
      severity: "halt",
      rationale: "In medical context, halt earlier (85% for 3s vs 95% for 5s). Patient safety > availability."
    },
    {
      id: "med.cpu.main_blocked",
      signal: { domain: "resource", metric: "cpu.main_blocked" },
      predicate: { type: "exceeds", value: 1000, unit: "ms" },  // Default: 2000ms
      action: { type: "isolate", subsystem: "W2", mode: "terminate" },
      cooldown: 5_000,
      severity: "isolate",
      rationale: "1 second of main thread block during diagnostic reasoning is unacceptable. Terminate reasoning worker."
    },

    // ── Behavioral Signals (domain-specific additions) ─────────────────

    {
      id: "med.saga.duration_diagnostic",
      signal: { domain: "behavior", metric: "saga.duration" },
      predicate: { type: "exceeds", value: 2.0, unit: "ratio" },  // Default: 3.0 (v1.3: dimensionless ratio, S-5)
      action: { type: "restrict", targetTier: 1 },
      cooldown: 30_000,
      severity: "restrict",
      rationale: "Diagnostic reasoning exceeding 2× budget suggests runaway differential expansion. Restrict to standard path."
    },
    {
      id: "med.saga.concurrent_limit",
      signal: { domain: "behavior", metric: "saga.concurrent" },
      predicate: { type: "exceeds", value: 10, unit: "count" },  // Default: 50
      action: { type: "restrict", targetTier: 1 },
      cooldown: 15_000,
      severity: "restrict",
      rationale: "Medical deployments should not process more than 10 concurrent queries. Excess indicates system misuse or attack."
    },
    {
      id: "med.taint.violation_strict",
      signal: { domain: "behavior", metric: "taint.violation_rate" },
      predicate: { type: "rate", count: 1, windowMs: 60_000 },  // Default: 3 in 60s
      action: { type: "isolate", subsystem: "W2", mode: "terminate" },  // v1.4 (F-7): Changed from "freeze" — see med.memory.heap_pressure note
      cooldown: 60_000,
      severity: "isolate",
      rationale: "Zero tolerance for taint violations in medical context. A single violation in 60s triggers isolation — any data handling anomaly must be investigated. State snapshot (§4.5) provides forensic record."
    },
    {
      id: "med.circuit.cascade_strict",
      signal: { domain: "behavior", metric: "circuit.cascade" },
      predicate: { type: "exceeds", value: 2, unit: "count" },  // Default: 5
      action: { type: "halt", preserveState: true },
      cooldown: 0,
      severity: "halt",
      rationale: "Two simultaneous open circuits in medical context suggests systemic failure. Halt and preserve full state for review."
    },
    {
      id: "med.escalation.governance_ignored",
      signal: { domain: "behavior", metric: "escalation.governance_ignored" },
      predicate: { type: "exceeds", value: 0, unit: "count" },  // Same as default: any occurrence
      action: { type: "halt", preserveState: true },
      cooldown: 0,
      severity: "halt",
      rationale: "Governance bypass in medical context is never acceptable. Immediate halt."
    },

    // ── Alignment Signals (tightened response) ─────────────────────────

    {
      id: "med.alignment.drift_any",
      signal: { domain: "alignment", metric: "drift.critical" },
      predicate: { type: "exceeds", value: 0, unit: "count" },
      action: { type: "halt", preserveState: true },  // Default: restrict to Tier 0
      cooldown: 0,
      severity: "halt",
      rationale: "In medical context, any critical alignment drift triggers immediate halt, not mere restriction. A diagnostics agent reasoning outside alignment bounds is a patient safety risk."
    },
    {
      id: "med.alignment.drift_repeated",
      signal: { domain: "alignment", metric: "drift.sustained" },
      predicate: { type: "rate", count: 2, windowMs: 300_000 },  // Default: 3 in 5 min
      action: { type: "halt", preserveState: true },  // Default: isolate reasoning
      cooldown: 0,
      severity: "halt",
      rationale: "Two alignment escalations in 5 minutes in medical context → halt. The agent's diagnostic reasoning cannot be trusted."
    },
    {
      id: "med.alignment.verification_failed",
      signal: { domain: "alignment", metric: "verification.failed" },
      predicate: { type: "exceeds", value: 0, unit: "count" },
      action: { type: "halt", preserveState: true },
      cooldown: 0,
      severity: "halt",
      rationale: "BAM verification failure means alignment monitoring is blind. Halt immediately — operating a medical diagnostics agent without alignment monitoring is unacceptable."
    },

    // ── Domain-Specific Signals (medical additions) ────────────────────
    // v1.4 (F-2): Previously a single cross-signal compound threshold
    // (med.reasoning.differential_depth). Split into two independent thresholds
    // because compound predicates cannot span signals (§3.1 limitation).

    {
      id: "med.reasoning.saga_overrun",
      signal: { domain: "behavior", metric: "saga.duration" },
      predicate: { type: "exceeds", value: 5.0, unit: "ratio" },     // 5× budget as dimensionless ratio (v1.3 S-5)
      action: { type: "restrict", targetTier: 0 },
      cooldown: 60_000,
      severity: "restrict",
      rationale: "Diagnostic saga at 5× budget suggests unbounded differential expansion. Restrict to read-only. (Note: 2× budget triggers restrict-to-Tier-1 via med.saga.duration_diagnostic; this is the escalated cap.)"
    },
    {
      id: "med.reasoning.cpu_sustained",
      signal: { domain: "resource", metric: "cpu.main_blocked" },
      predicate: { type: "sustained", inner: { type: "exceeds", value: 500, unit: "ms" }, durationMs: 3000 },  // Main thread blocked >500ms sustained 3s
      action: { type: "restrict", targetTier: 0 },
      cooldown: 60_000,
      severity: "restrict",
      rationale: "Sustained main thread blocking during diagnostic reasoning suggests runaway computation. Restrict to read-only. Independent from saga duration threshold — either condition alone warrants restriction."
    },
    {
      id: "med.phi.exfiltration_pattern",
      signal: { domain: "behavior", metric: "taint.violation_rate" },
      predicate: {
        type: "compound",
        op: "and",
        predicates: [
          { type: "rate", count: 5, windowMs: 10_000 },             // Rapid taint events
          { type: "exceeds", value: 3, unit: "count" }              // Multiple simultaneous
        ]
      },
      action: { type: "halt", preserveState: true },
      cooldown: 0,
      severity: "halt",
      rationale: "Rapid burst of taint events in medical context may indicate PHI exfiltration attempt. Immediate halt with full forensic preservation."
    },

    // ── External Signals (same as defaults — governance always has authority) ──

    {
      id: "med.external.restrict",
      signal: { domain: "external", metric: "directive.restrict" },
      predicate: { type: "exceeds", value: 0, unit: "count" },
      action: { type: "restrict", targetTier: 0 },
      cooldown: 0,
      severity: "restrict",
      rationale: "Governance directive — restrict to specified tier."
    },
    {
      id: "med.external.isolate",
      signal: { domain: "external", metric: "directive.isolate" },
      predicate: { type: "exceeds", value: 0, unit: "count" },
      action: { type: "isolate", subsystem: "W2", mode: "terminate" },
      cooldown: 0,
      severity: "isolate",
      rationale: "Governance directive — isolate specified subsystem."
    },
    {
      id: "med.external.halt",
      signal: { domain: "external", metric: "directive.halt" },
      predicate: { type: "exceeds", value: 0, unit: "count" },
      action: { type: "halt", preserveState: true },
      cooldown: 0,
      severity: "halt",
      rationale: "Governance directive — immediate halt."
    },
    {
      id: "med.external.human_override",
      signal: { domain: "external", metric: "human.override" },
      predicate: { type: "exceeds", value: 0, unit: "count" },
      action: { type: "halt", preserveState: true },
      cooldown: 0,
      severity: "halt",
      rationale: "Clinician or safety officer emergency override — immediate halt."
    },
  ],
};
```

### A.3 Key Differences from Default Thresholds

| Parameter | Default | Medical Diagnostics | Rationale |
|-----------|---------|-------------------|-----------|
| Memory halt threshold | 0.95 sustained 5s | 0.85 sustained 3s | Earlier halt preserves more forensic state |
| Main thread block → isolate | 2000ms | 1000ms | Diagnostic reasoning must be responsive |
| Saga duration budget | 3× | 2× | Tighter reasoning bounds prevent unbounded differentials |
| Concurrent saga limit | 50 | 10 | Medical deployment serves single clinician, not batch |
| Taint violation tolerance | 3 in 60s → isolate | 1 in 60s → isolate | Zero tolerance for data handling anomalies |
| Circuit cascade → halt | 5 | 2 | Lower systemic failure threshold |
| Critical alignment drift | Restrict to Tier 0 | Halt | No degraded reasoning in medical context |
| Sustained alignment drift | 3 in 5min → isolate | 2 in 5min → halt | Escalated from isolate to halt |
| BAM grace period (v1.2) | 60s | 15s | One minute of unmonitored reasoning is unacceptable in clinical context |
| `visibilityHiddenHaltMs` (v1.3) | 5000ms | 0 (disabled) | Tab switching is normal clinical workflow; halt on tab-hide is a UX hazard |
| `freeze` isolation mode (v1.3) | Available | Falls back to `terminate` (non-TEE) | No reliable freeze mechanism outside TEE; medical thresholds should expect `terminate` |

### A.4 Governance Notes for Medical Deployments

1. **Threshold table signing authority** must be a registered Medical Governance Board member with clinical informatics credentials. Standard engineering governance is insufficient for medical threshold changes.
2. **Recovery from halt** requires medical governance quorum (not just engineering quorum). The quorum must include at least one member with clinical domain expertise.
3. **Audit log retention** must comply with HIPAA minimum retention (6 years). The default 1000-record in-memory log is supplemented by persistent storage with the required retention period.
4. **Last Gasp beacon endpoint** must be a HIPAA-compliant logging service. The beacon contains no PHI (threshold IDs and signal values only), but the endpoint must meet BAA requirements.
5. **BAM phase gate** (§7.2) is mandatory and non-waivable for medical deployments. There is no acceptable risk of operating reasoning services without alignment monitoring in a clinical context.
6. **BAM grace period** must be set to **15 seconds** (v1.2, R-5). The default 60-second grace period allows one full minute of unmonitored reasoning — unacceptable during clinical diagnostic operations. At 15 seconds, the window between BAM channel loss and reasoning service isolation is short enough that at most one diagnostic query cycle completes unmonitored. Configuration: `bamPhaseGate.gracePeriodMs: 15_000`.
7. **Last Gasp beacon routing** should use a trusted network segment (v1.2, R-3). While the beacon contains no PHI, threshold IDs like `med.alignment.drift_any` reveal that a clinical agent experienced alignment failure — operational metadata that may be sensitive under institutional policy.
8. **`visibilitychange` halt must be disabled** (v1.3, S-6). Configuration: `visibilityHiddenHaltMs: 0`. In clinical contexts, a clinician may switch tabs to consult reference material, review lab results, or respond to a clinical alert — tab switching is a normal part of the diagnostic workflow, not an abandonment signal. The `visibilitychange` interrupt still fires and CPS still captures a precautionary state snapshot (§4.5), but the halt timer is disabled. The clinician's tab switch must not halt the diagnostic agent mid-reasoning. If the deployment environment requires suspension detection (e.g., mobile-only clinical app), governance should configure a longer `visibilityHiddenHaltMs` (e.g., 30000ms) rather than using the default 5000ms.
9. **`freeze` isolation mode is unavailable** in non-TEE medical deployments (v1.3, S-8). Medical threshold tables that specify `freeze` (e.g., `med.memory.heap_pressure`) will automatically fall back to `terminate` unless the deployment is SPCN/TEE. Governance should review threshold actions to ensure `terminate` behavior is acceptable for each medical use case.

---

## References

- FNSR Orchestrator Specification v2.3.0 (§9 CPS Integration, §5.1 degradation assignments, §8.2 containment event contracts)
- SPCN Operational Architecture Specification v2.3.1 (§CS-1 Safety Subsystem binding, §CS-5 HIRI write-only, §CS-6 Unified Commitment Ledger, §6.2 EAT protocol)
- FNSR Governance Specification v2.0.0 (autonomy tiers, quorum rules, escalation protocol)
- FNSR Performance Specification v2.0.0 (latency budgets informing containment timing)
- Portfolio Planning Document v3.6.0 (§3.1 CPS service description, Phase 1 requirements)
- ARCHON Functional Requirements v3.0 (graduated autonomy model)
- BAM Behavioral Alignment Monitor (TBD — assumed interface for alignment escalation events)
