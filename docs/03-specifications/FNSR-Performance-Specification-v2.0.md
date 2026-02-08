# FNSR Performance Specification

**Document ID:** `performance-spec-01`
**Version:** 2.0.0
**Status:** Final
**Last Updated:** 2026-02-05

-----

## 1. Purpose and Scope

### 1.1 Mission

This specification formalizes the latency budgets, throughput requirements, resource constraints, cache management policies, degradation behaviors, and observability requirements for the FNSR ecosystem. It is the authoritative source for performance contracts across all three query paths.

### 1.2 The Problem This Spec Solves

FNSR Architecture §3.1 defines three query path tiers — fast (<100ms), standard (<500ms), and full (<2s) — but does not allocate latency budgets to individual services within each path. The Integration Specification §3 (Tension 4: Speed vs. Rigor) names the tension between responsiveness and thoroughness but leaves the resolution to this document. Individual service specifications (APS, CSS, AES, DES, SIS) declare their own latency targets in isolation. This spec harmonizes those declarations into a coherent whole and resolves conflicts where individual service budgets sum to more than the path ceiling.

### 1.3 What This Spec Is Not

This specification defines **performance contracts**, not implementation strategies. It does not prescribe caching technologies, scaling topologies, or monitoring tools. Those are infrastructure concerns and belong behind adapter boundaries per the Edge-Canonical First Principle. This spec tells you how fast things must be. How you achieve that is your problem.

### 1.4 Edge-Canonical Compliance

All latency budgets defined here apply to the **canonical execution model**: a single-process runtime (browser or `node index.js`). Distributed deployments may achieve better throughput through parallelism, but the per-query latency budgets are defined against the single-process baseline. If a service cannot meet its latency budget on a single core with in-memory state, the specification is wrong — not the deployment.

### 1.5 Reference Hardware Baseline

All throughput targets and timing assertions in this specification were derived against the following reference hardware:

|Component|Specification                                        |
|---------|-----------------------------------------------------|
|CPU      |4-core x86-64 @ 2.4GHz (Intel i5-class or equivalent)|
|RAM      |8GB DDR4                                             |
|Storage  |SSD (NVMe or SATA)                                   |
|Browser  |Chromium 120+ or equivalent                          |
|Node.js  |v20 LTS or later                                     |
|OS       |Linux, macOS, or Windows 10+                         |

Conformance reports MUST declare the hardware and runtime versions used. Implementations running on hardware significantly below this baseline (e.g., mobile ARM SoCs with ≤ 2 cores) should follow the adaptive topology in §3.7.

-----

## 2. Query Path Definitions

### 2.1 Path Classification Criteria

The orchestrator classifies each incoming query into a path tier based on the following signals:

|Signal                  |Fast    |Standard    |Full        |
|------------------------|--------|------------|------------|
|Cache hit               |Required|Not required|Not required|
|Abduction needed        |No      |No          |Yes         |
|Simulation requested    |No      |No          |Yes         |
|Maximum taint level     |≤ L1    |≤ L2        |Any (L0–L5) |
|Multi-document reasoning|No      |No          |Yes         |
|High-stakes (full IEE)  |No      |No          |Yes         |

Classification is deterministic. Given the same query metadata, the same path is always selected.

### 2.2 Path Routing Decision

```
Query arrives
    │
    ├─ Cache hit AND taint ≤ L1 AND no flags? ──► FAST PATH
    │
    ├─ No cache hit OR taint ≤ L2, no gaps, no simulation? ──► STANDARD PATH
    │
    └─ Gaps detected OR simulation OR multi-doc OR high-stakes? ──► FULL PATH
```

Path escalation is permitted mid-execution. A query that begins on the standard path may escalate to full if MDRE detects gaps during deduction. Path demotion is never permitted — once escalated, a query stays at the higher tier.

### 2.3 Path Classifier Calibration

The orchestrator SHOULD log a classifier decision record for each query:

```json
{
  "@type": "ClassifierDecision",
  "signals": { "cache_hit": true, "taint": "L1", "abduction": false },
  "assigned_path": "fast",
  "actual_path_used": "fast",
  "escalated": false,
  "escalation_reason": null
}
```

When the path escalation rate exceeds 30% over a 5-minute window, the classifier is miscalibrated. Recommended recalibration procedure:

1. Aggregate classifier decision records over the alert window.
1. Compute a confusion matrix: (assigned_path × actual_path_used).
1. Identify the dominant false classification (e.g., “standard → full escalation”).
1. Tighten the signal threshold for the misclassified dimension (e.g., lower the taint ceiling for standard, or require cache freshness score > threshold).
1. Log the threshold adjustment as a `fnsr.classifier.recalibration` event.

### 2.4 Path SLA Summary

|Property                  |Fast                                    |Standard                                                         |Full                                     |
|--------------------------|----------------------------------------|-----------------------------------------------------------------|-----------------------------------------|
|End-to-end latency ceiling|100ms                                   |500ms                                                            |2,000ms (sync)                           |
|Async extension permitted |No                                      |No                                                               |Yes (unbounded with progress)            |
|Services invoked          |Cache, MDRE (local), IEE (pattern match)|SIS, ECCPS, TagTeam, DES (cached), OERS, MDRE, IEE (tiered), SHML|All services                             |
|Response mode             |Synchronous                             |Synchronous                                                      |Synchronous or async with polling/webhook|

-----

## 3. Concurrency Model

### 3.1 The JavaScript Concurrency Distinction

This specification relies on parallel execution for budget math in §4 (Phases 5 and 7). The correctness of those budgets depends on a precise understanding of what “parallel” means in single-threaded JavaScript runtimes.

**Concurrency ≠ Parallelism.** `Promise.all()` on the main thread interleaves I/O-bound work but serializes CPU-bound work. If three CPU-bound services run via `Promise.all()` on the main thread, total latency is `SUM(a, b, c)`, not `MAX(a, b, c)`.

FNSR services fall into two categories:

|Category     |Services                                                                                                                                                                                               |Nature of Work                                                     |
|-------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------|
|**I/O-bound**|SIS, HIRI, cache lookups, SQO dispatch                                                                                                                                                                 |Pattern match against in-memory data, hash computation, network I/O|
|**CPU-bound**|APS (embedding + vector search + re-ranking), MDRE (Prolog inference), IEE (worldview evaluation), TagTeam (parsing), DES (rule evaluation), CSS (simulation), OERS (string matching + graph traversal)|Sustained computation                                              |

### 3.2 Parallelism Requirement

**Any phase marked “∥” (parallel) in §4 MUST execute in a separate execution context** — a Web Worker (browser) or Worker Thread (Node.js) — for the `MAX()` budget math to hold. If parallel-marked services run on the main thread, the budget is `SUM()`, not `MAX()`, and the path ceiling will be violated.

This is a normative requirement, not an implementation suggestion. Implementations that run parallel-marked phases on the main thread are non-conformant.

### 3.3 Worker Pool Architecture

The target worker pool for budget conformance:

|Environment            |Workers (target)|Assignment                           |
|-----------------------|----------------|-------------------------------------|
|Browser (≥ 4 cores)    |3 Web Workers   |W1: APS, W2: DES+OERS, W3: AES or CSS|
|Node.js (≥ 4 cores)    |3 Worker Threads|Same assignment                      |
|Constrained (≤ 2 cores)|2 Workers       |See §3.7                             |

**Assignment rationale**: APS is the longest-running parallel service (500ms) and must have a dedicated worker. OERS (60ms) and DES (80ms) are short enough to share a worker sequentially within their combined budget (140ms < 500ms APS budget). AES and CSS share a worker because they are in different parallel groups (Phase 7) and, when they execute serially due to dependency, the spec already accounts for this (see §16, T-009).

**Worker lifecycle**: Workers are warm — initialized at startup and reused across queries. Cold worker startup is not included in per-query latency budgets. Implementations must pre-warm workers before accepting queries.

### 3.4 Runtime Capability Detection

On startup, before accepting queries, the orchestrator MUST execute a capability detection step and record a `RuntimeCapabilities` object:

```json
{
  "@type": "RuntimeCapabilities",
  "hardwareConcurrency": 4,
  "sharedArrayBufferAvailable": true,
  "transferableObjectsAvailable": true,
  "maxWorkersAllowed": 4,
  "estimatedPostMessageCost_ms": 1.8,
  "coopCoepEnabled": true,
  "workerTopology": "full_3w",
  "accepting_full_path": true
}
```

**Detection procedure:**

1. Read `navigator.hardwareConcurrency` (browser) or `os.cpus().length` (Node.js).
1. Attempt to create a `SharedArrayBuffer(1)`. Record success/failure.
1. Spawn a test Worker, transfer a 10KB `ArrayBuffer` via `postMessage(..., [buf])`, time the round trip. Record `estimatedPostMessageCost_ms`.
1. Based on results, select `workerTopology` per §3.7.
1. If workers are unavailable, set `accepting_full_path` per §3.8.
1. Log `RuntimeCapabilities` as a startup event.

If the detection step itself exceeds 500ms, log a warning and proceed with conservative defaults (main-thread-only mode).

### 3.5 Worker Data Transfer

Dispatching work to a Worker requires transferring input data across execution contexts. In JavaScript, this uses the **Structured Clone Algorithm**, which copies data. For large payloads (knowledge graphs, JSON-LD documents), cloning can block the main thread.

**Transfer budget**: Worker dispatch overhead — including serialization, postMessage, and deserialization — is allocated **5ms per dispatch** in the budget tables. This is accounted for within the orchestrator’s 10ms allocation (which covers routing AND up to 2 dispatches per query).

**Normative transfer format**: Worker dispatch payloads MUST use a binary, transferable format. The recommended pipeline is:

```
JSON-LD (source) → CBOR compact encoding → ArrayBuffer → postMessage(..., [buffer])
```

This pipeline achieves two goals: (a) CBOR encoding is 30–50% smaller than JSON, reducing clone cost; (b) the resulting `ArrayBuffer` is Transferable, enabling zero-copy transfer. The worker deserializes CBOR back to an in-memory object on receipt.

**Transfer strategy selection** (automatic, by orchestrator):

|Payload Size (post-CBOR)|Transfer Strategy                            |Expected Overhead|
|------------------------|---------------------------------------------|-----------------|
|< 10KB                  |Structured Clone of CBOR ArrayBuffer         |< 1ms            |
|10KB–500KB              |Transferable ArrayBuffer (zero-copy)         |< 1ms            |
|> 500KB                 |Pre-staged (worker loads own copy at warm-up)|~0ms per query   |

**Transferable semantics warning**: Transferring an `ArrayBuffer` via `postMessage(..., [buffer])` **neuters** the buffer on the sender side. The orchestrator MUST NOT reference the buffer after transfer. If the orchestrator needs to retain the data, it must copy before transferring.

**SharedArrayBuffer**: For data shared across multiple workers simultaneously (e.g., a read-only ontology snapshot), `SharedArrayBuffer` avoids both copying and transfer-neutering. However, `SharedArrayBuffer` requires COOP/COEP headers in browsers (see §3.6). Pre-staging remains the recommended default.

**Pre-staging is the default pattern**: Workers W1, W2, and W3 SHOULD load their required knowledge bases during warm-up (§12.3). Per-query dispatch then transfers only the query payload and extracted claims (typically < 10KB after CBOR encoding), keeping dispatch well under 2ms.

**Budget accounting**: If dispatch exceeds 5ms, the orchestrator logs a `dispatch_overhead_exceeded` metric and the budget erosion is visible in the performance report.

### 3.6 COOP/COEP and SharedArrayBuffer

`SharedArrayBuffer` is required for zero-copy shared memory between the main thread and workers. In browsers, it requires the following HTTP headers on the page:

```
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
```

**Operational impact**: These headers prevent the page from interacting with cross-origin popups and require all subresources to opt in via CORS or CORP headers. This may be incompatible with:

- Pages embedded in cross-origin iframes.
- Pages that use cross-origin OAuth popups.
- Third-party scripts that do not send CORP headers.

**If COOP/COEP cannot be enabled**: The orchestrator MUST detect this at startup (§3.4, `coopCoepEnabled: false`) and fall back to Transferable ArrayBuffers for all worker communication. SharedArrayBuffer is an optimization, not a requirement. All conformance requirements can be met with Transferable Objects alone.

**Node.js**: `SharedArrayBuffer` is available natively without header restrictions. No special configuration needed.

### 3.7 Adaptive Worker Topology

Not all environments can sustain 3 dedicated workers. The orchestrator selects a topology based on runtime capabilities:

|Topology    |Condition                      |Workers   |Phase 5 Strategy         |Phase 7 Strategy                            |Full-Path Buffer|
|------------|-------------------------------|----------|-------------------------|--------------------------------------------|----------------|
|`full_3w`   |`hardwareConcurrency ≥ 4`      |W1, W2, W3|APS on W1, OERS+DES on W2|AES→CSS on W3                               |365ms           |
|`reduced_2w`|`hardwareConcurrency == 2 or 3`|W1, W2    |APS on W1, OERS+DES on W2|AES→CSS on main thread (yielding every 50ms)|215ms           |
|`main_only` |Workers unavailable            |None      |All serial on main       |All serial on main                          |290ms           |

**`reduced_2w` details**: AES and CSS run on the main thread using cooperative yielding (`setTimeout(0)` between computation chunks of ≤ 50ms). This keeps the main thread responsive for fast-path queries during Phase 7 but increases Phase 7 wall-clock time due to yield overhead. Estimated Phase 7 on main thread with yielding: ~500ms (vs. 450ms on a dedicated worker). Full-path subtotal: 1,785ms, buffer: 215ms (10.8% — at the minimum threshold).

**Topology selection is logged at startup** as part of the `RuntimeCapabilities` event and is immutable for the process lifetime. To change topology, restart the process.

### 3.8 Worker Unavailability Policy

If the runtime cannot create workers (topology: `main_only`), the orchestrator MUST:

1. Set `accepting_full_path: false` in the `RuntimeCapabilities` event.
1. Accept fast-path and standard-path queries normally.
1. For full-path queries, return a machine-readable refusal:

```json
{
  "@type": "QueryRefusal",
  "reason": "workers_unavailable",
  "message": "Full-path queries require Worker threads. Current runtime does not support workers.",
  "suggested_action": "Retry with a runtime that supports Web Workers or Worker Threads.",
  "fallback_offered": "standard_path_degraded"
}
```

1. If the consumer explicitly opts in to degraded full-path processing (via a request flag `allow_main_thread_full: true`), the orchestrator MAY accept the query with `concurrencyModel: "main_thread_only"` and `degraded: "no_workers"` in the response.

This policy is the default. Implementations MAY configure `worker_unavailable_policy: "accept_degraded"` to skip the refusal and always attempt main-thread execution, but MUST still report the degradation.

**Worker respawn under memory pressure**: If a worker is terminated due to memory pressure (§12.1), the orchestrator MUST:

1. Mark the worker as `unavailable` immediately.
1. Attempt respawn after a 5-second cooldown.
1. If respawn fails, attempt again with exponential backoff (5s, 10s, 20s, 40s, max 60s).
1. After 3 consecutive respawn failures, downgrade topology (e.g., `full_3w` → `reduced_2w`) and log `fnsr.topology.downgrade`.
1. Periodically (every 5 minutes) attempt to restore the original topology.

-----

## 4. Latency Budget Allocation

### 4.1 Principles

The budget allocation follows five rules:

1. **Sum rule**: Per-service budgets within a path must sum to less than or equal to the path ceiling, inclusive of orchestration overhead and a mandatory buffer.
1. **Serialization rule**: Services that execute sequentially consume budget sequentially. Services that can execute in parallel share the longest-leg budget.
1. **Buffer rule**: Every path reserves a minimum 10% of its ceiling as unallocated buffer for adapter overhead, serialization, and network variance (in distributed deployments).
1. **Worker rule**: Parallel budget math (`MAX()`) is valid only when parallel-marked services execute in separate Workers per §3.2. Main-thread-only execution uses `SUM()`.
1. **Transfer rule**: Worker dispatch overhead (§3.5) is included in the orchestrator budget, not the service budget. A service’s latency is measured from when it begins executing in its context, not from when the orchestrator posts the message.

### 4.2 Fast Path Budget (≤ 100ms)

The fast path exists to serve cached results with minimal verification. It bypasses all ingestion, extraction, and deep reasoning services. No workers are used.

|Phase              |Service                 |Budget   |Notes                                          |
|-------------------|------------------------|---------|-----------------------------------------------|
|1. Route           |Orchestrator            |10ms     |Path classification, signal checks, GC headroom|
|2. Cache lookup    |Cache adapter           |5ms      |In-memory map or IndexedDB                     |
|3. Local reasoning |MDRE (cached KB)        |25ms     |Pattern match against cached verdicts          |
|4. Ethics check    |IEE (known-safe pattern)|8ms      |Bloom filter or hash set lookup                |
|5. Output framing  |SHML                    |5ms      |Template application                           |
|6. Provenance stamp|HIRI                    |2ms      |Hash computation                               |
|**Subtotal**       |                        |**55ms** |                                               |
|Buffer             |                        |**45ms** |45%                                            |
|**Ceiling**        |                        |**100ms**|                                               |

**All phases execute on the main thread. No worker dispatch overhead applies.**

**Cache miss behavior**: If the cache lookup in phase 2 fails, the query immediately escalates to the standard path. The 5ms spent on cache lookup is sunk cost; the standard path budget begins fresh from its own 500ms ceiling. There is no “fast path with fallback” — a cache miss is a path change, not a degradation.

### 4.3 Standard Path Budget (≤ 500ms)

The standard path processes fresh input through the full ingestion and reasoning pipeline, but without abductive or counterfactual reasoning.

|Phase               |Service       |Budget|Context|Notes                                   |
|--------------------|--------------|------|-------|----------------------------------------|
|1. Route + dispatch |Orchestrator  |10ms  |Main   |Classification + 1 worker dispatch to W2|
|2. Sanitize         |SIS           |~0ms  |Main   |Absorbed into orchestrator overhead     |
|3. Validate         |ECCPS         |30ms  |Main   |Semantic constraint checking            |
|4. Extract          |TagTeam       |120ms |Main   |Semantic parsing, ontology alignment    |
|5a. Resolve entities|OERS          |40ms  |W2     |∥ hidden behind main-thread phases 6–7  |
|5b. Apply defaults  |DES (cached)  |20ms  |W2     |Sequential after 5a on same worker      |
|6. Reason           |MDRE          |110ms |Main   |Deductive reasoning                     |
|7. Ethics           |IEE (Tier 1+2)|50ms  |Main   |Priority + consequentialist check       |
|8. Frame            |SHML          |15ms  |Main   |Semantic output framing                 |
|9. Sign             |HIRI          |5ms   |Main   |Provenance stamp                        |

**Worked budget example (standard path, `full_3w` topology):**

```
Timeline:

Main thread:  [Orch 10ms][SIS ~0][ECCPS 30ms][TagTeam 120ms]──dispatch W2──[MDRE 110ms][IEE 50ms][SHML 15ms][HIRI 5ms]
Worker W2:                                                    [OERS 40ms][DES 20ms]
                                                              ↑ runs in parallel with MDRE+IEE

Main thread total: 10 + 0 + 30 + 120 + 110 + 50 + 15 + 5 = 340ms
Worker W2 total:   40 + 20 = 60ms (hidden behind MDRE+IEE's 160ms)
Visible latency:   max(340, 340_before_MDRE + max(60, 160)) = 340ms + 0ms hidden worker = 340ms
Buffer:            500 - 340 = 160ms (32%)

Conservative (no workers): 10 + 0 + 30 + 120 + 40 + 20 + 110 + 50 + 15 + 5 = 400ms
Buffer (no workers):       500 - 400 = 100ms (20%)
```

|        |With Workers|No Workers |
|--------|------------|-----------|
|Subtotal|340ms       |400ms      |
|Buffer  |160ms (32%) |100ms (20%)|

Both scenarios are conformant. §3.5’s “main-thread budget” column (345ms with workers) included 5ms dispatch overhead; the worked example shows 340ms because dispatch is absorbed into the orchestrator’s 10ms.

### 4.4 Full Path Budget (≤ 2,000ms synchronous)

The full path activates the complete cognitive bus. All services participate. Phase 7 (AES→CSS) is budgeted as serial (450ms) — this is the normative planning baseline.

|Phase              |Service     |Budget|Context|Notes                                            |
|-------------------|------------|------|-------|-------------------------------------------------|
|1. Route + dispatch|Orchestrator|10ms  |Main   |Classification + saga init + dispatches to W1, W2|
|2. Sanitize        |SIS         |0ms   |Main   |Absorbed into overhead                           |
|3. Validate        |ECCPS       |50ms  |Main   |Deep semantic validation                         |
|4. Extract         |TagTeam     |200ms |Main   |Full extraction with ambiguity lattice           |
|5a. Resolve        |OERS        |60ms  |W2     |∥ parallel group                                 |
|5b. Defaults       |DES (full)  |80ms  |W2     |Sequential after 5a on W2                        |
|5c. Precedent      |APS         |500ms |W1     |∥ parallel group                                 |
|6. Reason          |MDRE        |200ms |Main   |Full deductive reasoning                         |
|7a. Abduction      |AES         |150ms |W3     |Serial on W3                                     |
|7b. Simulation     |CSS         |300ms |W3     |Serial after 7a on W3                            |
|8. Ethics          |IEE (full)  |200ms |Main   |12-worldview evaluation                          |
|9. Frame           |SHML        |20ms  |Main   |Full semantic framing                            |
|10. Sign           |HIRI        |5ms   |Main   |Provenance chain                                 |

**Worked budget example (full path, `full_3w` topology):**

```
Timeline:

Main:  [Orch 10][SIS 0][ECCPS 50][TagTeam 200]──dispatch W1,W2──await──[MDRE 200]──dispatch W3──await──[IEE 200][SHML 20][HIRI 5]
W1:                                              [APS ────────── 500ms ──────────]
W2:                                              [OERS 60][DES 80]
W3:                                                                                [AES 150][CSS 300]

Phase 1-4 (main serial):    10 + 0 + 50 + 200 = 260ms
Phase 5 (parallel):          max(500, 140) = 500ms (main awaits)
Phase 6 (main serial):      200ms
Phase 7 (W3 serial):        150 + 300 = 450ms (main awaits)
Phase 8-10 (main serial):   200 + 20 + 5 = 225ms
────────────────────────────────────────────────────────
Total:                       260 + 500 + 200 + 450 + 225 = 1,635ms
Buffer:                      2,000 - 1,635 = 365ms (18%)
```

### 4.5 Cross-Path Budget Comparison

|Service     |Fast          |Standard              |Full           |Notes                                       |
|------------|--------------|----------------------|---------------|--------------------------------------------|
|Orchestrator|10ms          |10ms                  |10ms           |Includes dispatch overhead                  |
|SIS         |skip          |~0ms                  |~0ms           |Always trivial                              |
|ECCPS       |skip          |30ms                  |50ms           |Deeper validation on full                   |
|TagTeam     |skip          |120ms                 |200ms          |Ambiguity lattice on full                   |
|OERS        |skip          |40ms                  |60ms           |Cross-doc resolution on full                |
|DES         |skip          |20ms (cached)         |80ms (full)    |Anomaly detection on full                   |
|APS         |skip          |skip                  |500ms          |Full path only, Worker W1                   |
|MDRE        |25ms (cached) |110ms                 |200ms          |Increasing KB size                          |
|AES         |skip          |skip                  |150ms          |Full path only, Worker W3                   |
|CSS         |skip          |skip                  |300ms          |Full path only, Worker W3 (serial after AES)|
|IEE         |8ms (pattern) |50ms (T1+2)           |200ms (full)   |Progressive depth                           |
|SHML        |5ms           |15ms                  |20ms           |More context to frame                       |
|HIRI        |2ms           |5ms                   |5ms            |Stable cost                                 |
|**Buffer**  |**45ms (45%)**|**100–160ms (20–32%)**|**365ms (18%)**|Standard range: no-worker to 3-worker       |
|**Total**   |**100ms**     |**500ms**             |**2,000ms**    |                                            |

-----

## 5. Async Processing: Beyond the 2-Second Ceiling

### 5.1 Async Boundary

Certain operations cannot guarantee completion within 2,000ms. These operations cross the **async boundary** and are governed by different performance contracts. Crossing the async boundary is not a failure — it is a designed capability of the full path.

|Operation                  |Typical Duration|Maximum Duration    |Governed By  |
|---------------------------|----------------|--------------------|-------------|
|CSS complex simulation     |2–30s           |5 minutes           |§5.3         |
|AES SQO dispatch + response|1–60s           |Configurable timeout|§5.2         |
|APS re-indexing (batch)    |10–300s         |1 hour              |APS Spec §8.4|
|IEE deadlock resolution    |5–60s           |5 minutes           |IEE Spec §4.2|
|Multi-document TagTeam     |2–10s           |2 minutes           |§5.4         |

### 5.2 SQO Dispatch Budget (AES)

When AES generates a Structured Query Object and dispatches it to an external system, the latency is dominated by the external system’s response time. FNSR cannot control external latency.

```json
{
  "@context": "https://fnsr.dev/performance/",
  "@type": "SQOLatencyContract",
  "aes_internal_budget": {
    "hypothesis_generation": "150ms",
    "sqo_construction": "50ms",
    "dispatch_handoff": "10ms",
    "total_aes_sync": "210ms"
  },
  "external_wait_policy": {
    "default_timeout": "30s",
    "max_timeout": "300s",
    "retry_policy": { "max_retries": 3, "backoff": "exponential", "base_delay": "1s" },
    "on_timeout": "use_highest_plausibility_hypothesis",
    "on_error": "escalate_after_3_retries"
  },
  "progress_reporting": {
    "interval": "5s",
    "report_type": "fnsr.sqo.progress",
    "includes": ["elapsed_time", "retries_attempted", "current_status"]
  }
}
```

### 5.3 CSS Simulation Budget

|Class  |World State Nodes|Propagation Steps|Max Interventions|Budget                           |
|-------|-----------------|-----------------|-----------------|---------------------------------|
|Simple |≤ 50             |≤ 10             |1                |300ms (within sync ceiling)      |
|Medium |51–500           |11–50            |1–3              |2–10s (async)                    |
|Complex|501–5,000        |51–200           |1–10             |10–60s (async)                   |
|Deep   |> 5,000          |> 200            |any              |60s–5min (async, must checkpoint)|

Async simulation contract: progress every 2s, partial results at L4 taint, checkpointing for complex/deep, hard timeout 300s.

### 5.4 Multi-Document TagTeam Budget

|Documents|Budget                          |Mode |
|---------|--------------------------------|-----|
|1        |200ms                           |Sync |
|2–3      |200ms × N × 1.2 (max 720ms)     |Sync |
|4+       |Async with per-document progress|Async|

Async contract: incremental handoff to downstream services per completed document, batch size 3, hard timeout 2s per batch.

-----

## 6. IRIS Perception Latency

### 6.1 Perception as a Pre-Pipeline Operation

IRIS operates *before* the query pipeline. Perception results are materialized as observation events before queries arrive. On-demand perception (query-triggered) requires a latency budget.

### 6.2 On-Demand Perception Budget

|Modality|Total Budget|Notes             |
|--------|------------|------------------|
|CHRONOS |2ms         |Clock reading     |
|INTUS   |8ms         |Metric aggregation|
|OCULIS  |60–210ms    |Model-dependent   |
|SONITUS |120–520ms   |Stream-dependent  |
|SENSUS  |15–55ms     |Sensor polling    |

Fast path: IRIS not invoked (cached only). Standard path: CHRONOS/INTUS only. Full path: all modalities available.

### 6.3 Model Inference Constraints

```json
{
  "@type": "IRISModelConstraints",
  "browser": { "max_model_size": "50MB", "warm_inference_latency": "200ms", "cold_start_budget": "2000ms" },
  "node": { "max_model_size": "500MB", "warm_inference_latency": "500ms", "cold_start_budget": "5000ms" },
  "warm_definition": "Model weights in memory, runtime initialized, first inference completed."
}
```

### 6.4 IRIS Cold-Start Behavior

When a query triggers on-demand perception and the required model is cold (not warmed), the orchestrator MUST select one of two behaviors:

|Mode                |Behavior                                                                                                                 |When to use                                                                     |
|--------------------|-------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------|
|`fallback` (default)|Return `degraded: "iris_cold_start"` with `fallback_signal: "L0_RAW"`. The query proceeds with uninterpreted sensor data.|Non-blocking. Suitable for most queries.                                        |
|`blocking`          |Hold the query until warm-up completes (up to `cold_start_budget`). Return full perception result.                       |Only when the consumer explicitly requests `iris_mode: "blocking"` in the query.|

In `fallback` mode, the cold model continues warming in the background. Subsequent queries will receive warm inference. The cold-start event is logged as `fnsr.iris.cold_start` with `actual_duration_ms`.

-----

## 7. Cache Management

### 7.1 What Is Cached

|Cache          |Contents                 |Populated By        |Consumers             |
|---------------|-------------------------|--------------------|----------------------|
|Verdict cache  |MDRE reasoning results   |Standard/full path  |Fast path             |
|Schema cache   |W2Fuel ontology fragments|W2Fuel standard path|TagTeam, MDRE, Fandaws|
|Default cache  |DES pre-computed defaults|DES full-path       |DES standard path     |
|Ethics cache   |IEE known-safe patterns  |IEE standard/full   |IEE fast path         |
|Entity cache   |OERS resolved identities |OERS standard/full  |Fast path             |
|Embedding cache|APS case embeddings      |APS indexing        |APS full path         |

### 7.2 Cache Representation

```json
{
  "@context": "https://fnsr.dev/cache/",
  "@type": "CacheEntry",
  "cache:key": "content-addressed hash",
  "cache:value": { "@type": "...service-specific..." },
  "cache:metadata": {
    "cache:created": "xsd:dateTime",
    "cache:ttl": "xsd:duration",
    "cache:source_path": "fast | standard | full",
    "cache:source_saga": "saga-id",
    "cache:taint": "L0 | L1 | L2",
    "cache:status": "fresh | stale | revalidating",
    "cache:version_vector": { "ontology": "hash", "rule_db": "hash", "knowledge_base": "hash" },
    "cache:dependency_bloom": "base64-encoded Bloom filter | null",
    "cache:dependency_namespaces_encrypted": "base64-AES-256-GCM encrypted namespace list | null"
  }
}
```

**`cache:dependency_bloom`**: Bloom filter encoding the namespace IRIs this entry depends on. Used for fast O(k) scope checks on the fast path.

**`cache:dependency_namespaces_encrypted`**: The plaintext namespace list, encrypted at rest using AES-256-GCM with a deployment-scoped key. Used only for offline forensic audit (see §7.6). Never consulted at query time. Never logged in plaintext.

### 7.3 Bloom Filter Construction

The Bloom filter parameters are computed from the standard optimal formulas:

Given target false positive rate `p` (default: 0.01) and `n` elements (namespace IRIs):

```
m = ceil( -n × ln(p) / (ln(2))² ) bits
k = round( (m / n) × ln(2) )
```

**Reference table (p = 0.01):**

|n (namespaces)|m (bits)|m (bytes)|k (hash functions)|Actual FP rate|
|--------------|--------|---------|------------------|--------------|
|10            |96      |12       |7                 |0.82%         |
|25            |240     |30       |7                 |0.83%         |
|50            |480     |60       |7                 |0.84%         |
|100           |959     |120      |7                 |0.84%         |
|200           |1,918   |240      |7                 |0.84%         |

**Minimum filter size**: 64 bits (8 bytes), even for n < 7. This prevents degenerate filters with excessive false positives.

Hash function: Use two independent hashes h1, h2 (e.g., MurmurHash3 with two seeds) and derive k hash values as `h_i(x) = (h1(x) + i × h2(x)) mod m` for i in [0, k). This is the Kirschner-Mitzenmacher optimization and requires only 2 hash computations per element.

### 7.4 Cache Invalidation Protocol

**Invalidation triggers:**

|Trigger                        |Scope                       |Mechanism                   |
|-------------------------------|----------------------------|----------------------------|
|Ontology change (W2Fuel)       |Schema cache, verdict cache |Version vector mismatch     |
|Rule change (DES)              |Default cache, verdict cache|Rule DB hash change         |
|Knowledge base update (Fandaws)|Verdict cache, entity cache |KB version increment        |
|Entity merge/split (OERS)      |Entity cache, verdict cache |Entity ID invalidation event|
|IEE policy change              |Ethics cache                |Policy version increment    |
|TTL expiry                     |Per-entry                   |Wall clock comparison       |
|Manual purge                   |Configurable scope          |Operator command            |

**Version vector protocol with stale-while-revalidate:**

```
Read cache entry for key K
  entry.version_vector = { ontology: "abc", rule_db: "def", kb: "ghi" }
  current.version_vector = { ontology: "abc", rule_db: "xyz", kb: "ghi" }
  
  rule_db differs → VERSION MISMATCH DETECTED
  
  Step 1: Bloom filter scope check (< 0.1ms)
    For each changed namespace in the delta, probe entry.dependency_bloom
    
    All miss? → UPDATE version vector, mark FRESH, return cached result
    Any hit?  → Possible overlap → proceed to Step 2
  
  Step 2: Stale-while-revalidate
    Mark entry as STALE
    Return stale result with "cache:status": "stale"
    Enqueue background revalidation on standard path
    
    Fast path: serve stale result with stale flag
    Standard/full path: ignore stale cache, compute fresh
  
  Step 3: Background revalidation
    On completion:
      If new result matches → update version vector, mark FRESH
      If new result differs → replace entry, mark FRESH, log revalidation_changed event
```

**Conservative fallback**: If `cache:dependency_bloom` is null, immediately invalidate on any version vector mismatch.

### 7.5 Fast-Path Safety Invariant

**No L3, L4, or L5 content may ever be cached for fast-path consumption.** This invariant is enforced at cache write time — the cache adapter rejects any entry with taint > L2.

### 7.6 Audit Data Retention Policy

The encrypted `dependency_namespaces_encrypted` field supports forensic reconstruction of scope checks. Retention policy:

1. **Encryption**: AES-256-GCM with a deployment-scoped key. Key rotation per standard key management practices.
1. **Retention period**: 90 days from cache entry creation. After expiration, the encrypted blob is deleted from the cache entry (the Bloom filter is retained indefinitely).
1. **Reconstruction**: An offline audit tool can decrypt the namespace list, recompute the Bloom filter, and verify it matches `dependency_bloom`. This validates that the Bloom filter was correctly constructed at write time.
1. **No plaintext logging**: Namespace IRIs MUST NOT appear in plaintext in metrics, logs, or observable events. They are available only through the encrypted audit field.

### 7.7 Cache Size Constraints

|Environment          |Maximum Cache Size|Eviction Policy   |
|---------------------|------------------|------------------|
|Browser (IndexedDB)  |50MB              |LRU with TTL floor|
|Node.js (in-memory)  |256MB default     |LRU with TTL floor|
|Node.js (disk-backed)|1GB default       |LRU with TTL floor|

-----

## 8. Throughput Requirements

### 8.1 Single-Process Throughput Targets

|Path    |Target QPS (P50)|Target QPS (P95)|Reference Hardware|
|--------|----------------|----------------|------------------|
|Fast    |200             |150             |§1.5 baseline     |
|Standard|5               |3               |§1.5 baseline     |
|Full    |1               |0.8             |§1.5 baseline     |

These targets represent sustained throughput on the reference hardware. Conformance reports MUST declare the hardware profile and measured P50/P95 QPS.

### 8.2 Throughput Under Mixed Load

|Path    |Expected Traffic|Weighted QPS|
|--------|----------------|------------|
|Fast    |70–85%          |140–170     |
|Standard|10–25%          |0.5–1.25    |
|Full    |2–10%           |0.02–0.1    |

**Isolation**: Worker-based execution provides natural isolation — full-path CPU runs on workers while the main thread remains responsive to fast-path cache lookups.

-----

## 9. Degradation Behavior

### 9.1 Degradation Philosophy

FNSR degrades **gracefully downward through query paths**, not through silent quality reduction:

```
FULL PATH → STANDARD PATH → FAST PATH → EXPLICIT FAILURE
```

### 9.2 Per-Service Degradation Contracts

|Service|Degradation Behavior                  |Output                           |
|-------|--------------------------------------|---------------------------------|
|SIS    |Skip (accept risk)                    |`"sis_bypassed"`                 |
|ECCPS  |Shallow checks only                   |`"eccps_shallow"`                |
|TagTeam|Partial parse (completed sentences)   |`"tagteam_partial"`              |
|OERS   |Local-only resolution                 |`"oers_local_only"`              |
|DES    |Cached defaults only                  |`"des_cached_only"`              |
|APS    |Partial results (skip re-ranking)     |`"aps_partial"`                  |
|MDRE   |Incomplete verdict with open questions|`"mdre_incomplete"`              |
|AES    |Top hypothesis without SQO            |`"aes_no_sqo"`                   |
|CSS    |Partial simulation or skip            |`"css_partial"` / `"css_skipped"`|
|IEE    |Tier 1 only                           |`"iee_tier1_only"`               |
|SHML   |Minimal framing                       |`"shml_minimal"`                 |
|HIRI   |Never degrades                        |—                                |

### 9.3 Degradation Reporting

Every FNSR response includes a `PerformanceReport`:

```json
{
  "@type": "PerformanceReport",
  "queryPath": "standard",
  "totalLatency": "387ms",
  "budgetUtilization": 0.77,
  "concurrencyModel": "full_3w",
  "serviceLatencies": { "tagteam": "115ms", "mdre": "98ms" },
  "degradations": [],
  "staleServed": [],
  "cacheHits": ["schema:bfo-core"],
  "cacheMisses": []
}
```

### 9.4 Circuit Breakers

Per-service circuit breakers: window 10, threshold 3 failures, half-open timeout 30s. Open circuit applies degradation behavior immediately without waiting.

-----

## 10. Observability

### 10.1 Metrics

Every service emits structured performance metrics as JSON-LD events:

```json
{
  "@type": "ServiceMetrics",
  "service": "tagteam",
  "saga_id": "saga-12345",
  "query_path": "standard",
  "timing": { "elapsed_ms": 115, "budget_ms": 120, "budget_utilization": 0.96 },
  "execution": {
    "thread": "main",
    "worker_id": null,
    "dispatch_overhead_ms": 0,
    "payload_bytes": 0,
    "transfer_strategy": "n/a",
    "payload_format": "n/a"
  },
  "quality": {
    "claim_count": 23,
    "average_confidence": 0.87,
    "ambiguity_count": 3
  },
  "degradation": null,
  "cache_behavior": "miss"
}
```

### 10.2 Metrics Privacy and Redaction

Metrics are classified into three tiers:

|Tier                                |Fields                                                                          |Default|Opt-in Required                             |
|------------------------------------|--------------------------------------------------------------------------------|-------|--------------------------------------------|
|**Operational** (always emitted)    |service, saga_id, query_path, timing.*, execution.*, degradation, cache_behavior|Yes    |No                                          |
|**Quality** (default on, redactable)|quality.claim_count, quality.average_confidence, quality.ambiguity_count        |Yes    |No                                          |
|**Content-adjacent** (default off)  |Raw input text, claim strings, namespace IRIs, entity names                     |No     |Explicit `telemetry_level: "verbose"` config|

**Redaction rules:**

1. **saga_id**: Opaque identifier. MUST NOT encode PII. Implementations SHOULD use UUIDs.
1. **claim_count**: Safe — integer count only, no content.
1. **Input text / claim strings**: MUST NOT appear in metrics unless `telemetry_level: "verbose"` is explicitly configured. When verbose is enabled, strings longer than 200 characters MUST be truncated with `"...[truncated]"`.
1. **Namespace IRIs**: Operational metadata, not PII, but may reveal ontology structure. Excluded from metrics by default; available only in encrypted audit data (§7.6).

**Telemetry level**: Implementations MUST support a `telemetry_level` configuration:

|Level               |Behavior                                              |
|--------------------|------------------------------------------------------|
|`minimal`           |Operational tier only. No quality metrics.            |
|`standard` (default)|Operational + Quality tiers.                          |
|`verbose`           |All tiers including content-adjacent (dev/debug only).|

### 10.3 Aggregated Health Metrics

|Metric                           |Window|Alert Threshold     |
|---------------------------------|------|--------------------|
|P50 latency per path             |5 min |> 50% of budget     |
|P95 latency per path             |5 min |> 80% of budget     |
|P99 latency per path             |5 min |> 95% of budget     |
|Degradation rate per service     |5 min |> 10%               |
|Cache hit rate (fast path)       |5 min |< 60%               |
|Cache stale-serve rate           |5 min |> 20%               |
|Revalidation-changed rate        |5 min |> 5%                |
|Path escalation rate             |5 min |> 30%               |
|Circuit breaker open events      |1 hr  |> 2 simultaneously  |
|Worker task turnaround P95       |5 min |> 110% of budget    |
|Worker queue depth               |5 min |> 2 tasks           |
|Dispatch overhead P95            |5 min |> 5ms               |
|Speculation hit rate (if enabled)|5 min |< 50% (auto-disable)|

### 10.4 Observability as JSON-LD

All metrics are JSON-LD documents. They do not require Prometheus, Grafana, or any monitoring stack. Metrics MUST be encrypted at rest when persisted to disk. Access to metric logs MUST be controlled per deployment’s access control policy.

-----

## 11. TagTeam Performance Optimization

### 11.1 Tiered Parsing

TagTeam supports two parsing modes to prevent budget blowout on simple queries:

|Mode          |Activation                                                  |Budget                         |Output                                                                            |
|--------------|------------------------------------------------------------|-------------------------------|----------------------------------------------------------------------------------|
|**Fast parse**|Query contains ≤ 3 claims, no ambiguity, single BFO category|40ms                           |Placeholder alignments with `parse_mode: "fast"`. Full deep parse triggered async.|
|**Full parse**|All other queries                                           |120ms (standard) / 200ms (full)|Complete ontology alignment with ambiguity lattice.                               |

Fast parse returns immediately with high-confidence placeholder mappings and enqueues a background deep parse. If the deep parse changes the mappings, a `fnsr.tagteam.reparse` event is emitted and MDRE can optionally re-reason.

### 11.2 BFO Mapping Template Cache

BFO mapping templates (SHACL shapes compiled to optimized matching bytecode) are pre-compiled per grammar/ontology version and stored in the schema cache. This reduces per-query TagTeam cost by 30–50ms for queries against known ontology structures.

Precomputation entry in §12.3: “TagTeam BFO mapping templates | On ontology update | Schema cache | TagTeam all paths”.

-----

## 12. Resource Constraints

### 12.1 Browser Environment

|Resource          |Limit               |Scope                                |
|------------------|--------------------|-------------------------------------|
|Total tab memory  |≤ 512MB             |Main + all Workers                   |
|Main thread heap  |≤ 200MB             |Orchestrator, serial services, cache |
|Per-worker heap   |≤ 100MB             |W1 may need more for APS case library|
|IndexedDB         |≤ 50MB              |Cache storage                        |
|Web Workers       |Per §3.7 topology   |2–3 + 1 spare                        |
|Single computation|≤ 50ms without yield|Per context                          |

**Memory pressure response**: Evict cold cache → terminate idle workers (respawn per §3.8) → reduce IRIS model → log `fnsr.memory.pressure`.

### 12.2 Node.js Environment

|Resource          |Default Limit        |Configurable          |
|------------------|---------------------|----------------------|
|Total heap        |≤ 2GB                |`--max-old-space-size`|
|Main thread heap  |≤ 800MB              |Via config            |
|Per-worker heap   |≤ 400MB              |Via config            |
|Disk cache        |≤ 1GB                |Via config            |
|Worker threads    |Per §3.7 topology    |Via config            |
|Single computation|≤ 200ms without yield|Via config            |

### 12.3 Precomputation Strategy

|Precomputation                    |When                       |Consumed By          |
|----------------------------------|---------------------------|---------------------|
|DES rule evaluation               |On rule change             |DES standard path    |
|APS embedding generation          |On case ingestion          |APS full path        |
|APS case library pre-staging to W1|Process start + incremental|APS queries          |
|MDRE KB pre-staging               |Process start + incremental|MDRE queries         |
|IEE known-safe pattern hash set   |On policy change           |IEE fast path        |
|W2Fuel SHACL shapes               |On ontology update         |TagTeam, Fandaws     |
|TagTeam grammar compilation       |On grammar update          |TagTeam all paths    |
|TagTeam BFO mapping templates     |On ontology update         |TagTeam all paths    |
|IRIS model warm-up                |Process start or idle      |IRIS perception      |
|Worker pre-warming                |Process start              |All parallel phases  |
|Scope Bloom filters               |On version vector change   |Fast-path scope check|

-----

## 13. Offline and Degraded Network

### 13.1 Offline Is Not an Error

Performance contracts remain in force offline. Adjustments: SQO falls back to best hypothesis; OERS uses local KB; W2Fuel uses cached schema; metrics buffered locally.

### 13.2 Offline Performance

Often *faster* than online (no external I/O). Primary risk is completeness, not latency.

-----

## 14. Conformance Tests

### 14.1 Probabilistic Test Semantics

Browser and edge environments exhibit significant latency variance due to GC, tab throttling, and OS scheduling. Conformance tests MUST use probabilistic assertions:

|Assertion Level|Requirement    |
|---------------|---------------|
|**P50**        |≤ budget × 1.0 |
|**P95**        |≤ budget × 1.1 |
|**P99**        |≤ budget × 1.25|

Tests MUST execute a minimum of 100 iterations of each reference query and compute percentile latencies. A test passes if all three assertion levels are met. Single-run assertions (`elapsed_ms ≤ budget_ms`) are informational only, not pass/fail criteria.

### 14.2 Latency Conformance

```
Given: 100 reference queries of known complexity
When: Processed through the full service pipeline
Then: P50 total latency ≤ path ceiling
  AND P95 total latency ≤ path ceiling × 1.1
  AND P50 per-service latency ≤ service budget
```

### 14.3 Degradation Conformance

```
Given: A query where service X is artificially slowed beyond its budget
Then: Service X reports degradation
  AND downstream services are not impacted
  AND total query P95 latency ≤ path ceiling
```

### 14.4 Cache Invalidation Conformance

```
Given: Cached result with Bloom filter encoding ["cco:agent"]
When: Ontology changes in "cco:event" (Bloom miss)
Then: Cached result returned FRESH, version vector updated, scope check < 0.5ms
```

```
Given: Cached result with Bloom filter encoding ["cco:agent"]
When: Ontology changes in "cco:agent" (Bloom hit)
Then: Stale result returned, background revalidation enqueued
```

```
Given: Cached result with null dependency_bloom
When: Any version vector change
Then: CACHE MISS, escalate to standard path
```

### 14.5 Taint Cache Safety

```
Given: Attempt to cache L3 result for fast-path
Then: Write REJECTED, rejection logged, no L3+ in fast-path cache
```

### 14.6 Worker Parallelism Conformance

```
Given: Full-path query, full_3w topology
Then: Phase 5 P95 ≈ max(APS, OERS+DES) × 1.1, not sum
  AND dispatch_overhead_ms P95 ≤ 5ms
```

```
Given: Full-path query, main_only topology, allow_main_thread_full: true
Then: Phase 5 P95 ≈ sum(APS, OERS, DES) × 1.1
  AND concurrencyModel: "main_thread_only"
```

### 14.7 Worker Detection Conformance

```
Given: Process startup
When: Runtime capability detection executes
Then: RuntimeCapabilities event logged within 500ms
  AND workerTopology selected
  AND estimatedPostMessageCost_ms recorded
  AND if estimatedPostMessageCost_ms P95 > 5ms, warning logged
```

### 14.8 Transfer Strategy Conformance

```
Given: Worker dispatch with CBOR-encoded payload > 10KB
Then: transfer_strategy: "transferable"
  AND dispatch_overhead_ms < 2ms
  AND payload_format: "cbor"
```

```
Given: Worker dispatch with CBOR-encoded payload < 10KB
Then: transfer_strategy: "structured_clone" (acceptable)
  AND payload_format: "cbor"
```

### 14.9 Bloom Filter Sanity

```
Given: Bloom filter constructed with n=100, p=0.01
When: 10,000 random non-member namespace IRIs are probed
Then: Measured false positive rate ≤ 1.5% (tolerance above target 1%)
  AND zero false negatives for all 100 members
```

### 14.10 Privacy Conformance

```
Given: telemetry_level: "standard" (default)
When: Metrics are emitted for a query containing PII in input text
Then: No raw input text, claim strings, or plaintext namespace IRIs appear in emitted metrics
  AND quality.claim_count is an integer (not content)
```

### 14.11 Multi-Document Sync Cap

```
Given: Full-path query with 4 documents
Then: Async mode with per-document progress
```

```
Given: Full-path query with 3 documents
Then: Sync completion within 720ms P95
```

### 14.12 Memory Pressure

```
Given: Browser tab memory exceeds 480MB
Then: Cache entries evicted, fnsr.memory.pressure logged, fast-path continues
```

-----

## 15. Spec Test Verification

> Could a developer evaluate, reason about, and execute this system using only a browser, a local NodeJS runtime, and JSON-LD files?

**Yes.** This specification defines:

- Latency budgets measurable with `performance.now()`
- Cache entries as JSON-LD documents in IndexedDB or `Map`
- Bloom filters in ~50 lines of JavaScript (MurmurHash3 + Kirschner-Mitzenmacher)
- CBOR encoding via the `cbor-web` npm package (< 10KB gzipped) or hand-rolled for minimal builds
- Workers via standard `Web Worker` / `worker_threads` APIs
- Transferable Objects via `postMessage(..., [buffer])`
- Degradation as conditional logic within each service
- Metrics as JSON-LD documents writable to files or arrays
- Circuit breakers as counters with timestamps
- Runtime detection via `navigator.hardwareConcurrency` and synthetic dispatch tests

No database, message broker, monitoring stack, or deployment topology is required.

-----

## 16. Tension Log

### T-009: Budget Oversubscription on Full Path — RESOLVED

Serial Phase 7 (450ms) is the normative baseline. Speculative pre-simulation in Appendix A.

### T-010: Cache Invalidation Aggressiveness — RESOLVED

Stale-while-revalidate with Bloom filter scope checking.

### T-011: APS Dominates Full-Path Budget — RESOLVED

Dedicated Worker W1 with pre-staged case library. Circuit breaker.

### T-012: JavaScript Concurrency Trap — RESOLVED

§3 formalizes Worker requirements. §3.5 addresses transfer overhead.

### T-013: Orchestrator Budget Optimism — RESOLVED

10ms on all paths, includes dispatch overhead.

### T-014: IRIS Cold Start vs. Warm Inference — RESOLVED

Separate budgets. Prescriptive fallback vs. blocking behavior (§6.4).

### T-015: Multi-Document TagTeam Budget Blowout — RESOLVED

Capped at 3 sync documents.

### T-016: Structured Clone Serialization Cost — RESOLVED

CBOR + Transferable mandate (§3.5). Pre-staging default.

### T-017: Scope Check Latency on Fast Path — RESOLVED

Bloom filter with correct formula (§7.3). Encrypted audit trail (§7.6).

### T-018: Memory Budget Ambiguity — RESOLVED

Per-context partitioning (§12.1, §12.2).

### T-019: Worker Utilization Measurement — RESOLVED

Observable proxies: turnaround, queue depth, dispatch overhead.

### T-020: Budget Arithmetic Inconsistency — RESOLVED (NEW)

**Tension**: v1.2 §3.5 gave main-thread budgets (Standard: 345ms, Full: 490ms) that did not clearly reconcile with §4 subtotals.

**Resolution**: §4.3 and §4.4 now include worked timeline examples showing exactly how main-thread phases, worker phases, and dispatch overhead sum to the path ceiling. The standalone “main-thread budget” table is removed; the authoritative numbers are the per-path worked examples in §4.

### T-021: Bloom Filter Bit/Byte Mismatch — RESOLVED (NEW)

**Tension**: v1.2 stated “m = max(64, 10×n) bits” then claimed “1KB filter for 100 namespaces.” 10×100 = 1000 bits = 125 bytes, not 1KB.

**Resolution**: §7.3 now uses the standard optimal formula with a reference table showing exact bit/byte counts for typical n values.

### T-022: Worker Fallback Policy Ambiguity — RESOLVED (NEW)

**Tension**: v1.2 left it to implementer judgment whether to refuse or degrade full-path queries without workers.

**Resolution**: §3.8 mandates a prescriptive default: refuse full-path queries with a machine-readable `QueryRefusal` unless the consumer opts in to degraded main-thread execution. Runtime capability detection (§3.4) and adaptive topology (§3.7) ensure the decision is automatic.

### T-023: Transfer Format Optimism — RESOLVED (NEW)

**Tension**: 5ms dispatch budget assumed pre-staged workers with small payloads, but JSON-LD string serialization can exceed this.

**Resolution**: §3.5 mandates CBOR binary encoding for all worker payloads and automatic strategy selection by the orchestrator based on payload size post-encoding.

### T-024: Metrics Privacy Gap — RESOLVED (NEW)

**Tension**: v1.2 metrics included fields that could contain PII (input text, claim strings, namespace IRIs) with no redaction guidance.

**Resolution**: §10.2 defines a three-tier telemetry system with default redaction, explicit opt-in for content-adjacent data, and conformance test (§14.10).

### T-025: IRIS Cold-Start UX Ambiguity — RESOLVED (NEW)

**Tension**: v1.2 said queries “wait or use cached observations” during cold start — ambiguous.

**Resolution**: §6.4 defines two prescriptive modes (fallback/blocking) with default behavior and explicit opt-in for blocking.

### T-026: Conformance Test Brittleness — RESOLVED (NEW)

**Tension**: Strict `elapsed_ms ≤ budget_ms` assertions fail randomly in noisy browser environments due to GC jitter.

**Resolution**: §14.1 mandates probabilistic test semantics: 100-iteration runs with P50/P95/P99 assertions.

-----

## 17. References

|Document                      |Version|Relevant Sections                                |
|------------------------------|-------|-------------------------------------------------|
|FNSR Complete Architecture    |v2.1   |§3.1 (Query Path Classification), §8 (Deployment)|
|FNSR Integration Specification|v1.0   |§2.4 (Latency), §3 (Gap Register)                |
|The Plot                      |—      |§3 (Tension 4: Speed vs. Rigor)                  |
|SIS Specification             |v1.0   |§1 (Microsecond latency)                         |
|ECCPS Specification           |TBD    |§4.1 (Validation depth)                          |
|TagTeam Roadmap               |v5.0   |§2.6 (Efficiency)                                |
|DES Specification             |v2.0   |§10.2 (Single-pass evaluation)                   |
|AES Specification             |v1.1   |§3.3 (Query path), §8.3 (SQO dispatch)           |
|CSS Specification             |v1.0   |§6.3 (Query path), §7 (Offline)                  |
|APS Specification             |v1.1   |§9.2 (Latency budget)                            |
|IEE Specification             |TBD    |§3.4 (Tiered evaluation), §4.2 (Deadlock)        |
|IRIS Specification            |v1.2   |§3.2 (Taint levels), §10 (Roadmap)               |
|W2Fuel Specification          |v1.0   |§10 (Query path behavior)                        |

-----

## 18. Changelog

|Version|Date      |Changes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
|-------|----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|1.0.0  |2026-02-05|Initial specification                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
|1.1.0  |2026-02-05|Worker concurrency model, orchestrator 10ms, SWR cache, serial Phase 7 baseline, multi-doc cap                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
|1.2.0  |2026-02-05|Worker transfer model, Bloom filter scope checks, per-context memory, observable worker metrics                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
|2.0.0  |2026-02-05|**Hardened final.** Reconciled budget arithmetic with worked timeline examples. Corrected Bloom filter formula with reference table. Prescriptive worker fallback (refuse + opt-in degrade). CBOR binary transfer mandate. Metrics privacy/redaction tiers. IRIS cold-start UX modes. Reference hardware baseline. Adaptive worker topology for constrained devices. Path classifier calibration. TagTeam fast-parse mode. COOP/COEP security notes. Probabilistic conformance tests. Audit data retention with encryption. Developer quickstart checklist.|

-----

## Appendix A: Speculative Pre-Simulation (Non-Normative)

**Status**: Optional optimization. Not required for conformance.

When MDRE flags both a gap and a counterfactual need, AND the counterfactual does not depend on the gap, AES and CSS can be parallelized: AES on W3, CSS on main thread (yielding every 50ms). Budget recovery: Phase 7 drops from 450ms to 300ms.

**Normative threshold**: If implemented, the speculation hit rate MUST be tracked. If the hit rate drops below 50% over the last 20 runs, speculation MUST be automatically disabled until the hit rate recovers above 70% over 20 subsequent serial runs. The `speculation_hit_rate` metric is reported in §10.3.

-----

## Appendix B: Developer Quickstart Checklist

**Pre-flight (before accepting queries):**

- [ ] Run runtime capability detection (§3.4). Log `RuntimeCapabilities`.
- [ ] Select worker topology per §3.7. Warm workers.
- [ ] Pre-stage APS case library to W1. Pre-stage MDRE KB.
- [ ] Pre-compile TagTeam grammars and BFO mapping templates.
- [ ] Pre-compute IEE known-safe pattern hash set.
- [ ] Pre-warm IRIS models (if perception enabled).
- [ ] Verify COOP/COEP headers (browser) or SharedArrayBuffer (Node.js) per §3.6.
- [ ] Configure `telemetry_level` per deployment policy (§10.2).
- [ ] Set `worker_unavailable_policy` (§3.8).

**Recommended production config:**

|Parameter                         |Browser                              |Node.js                 |
|----------------------------------|-------------------------------------|------------------------|
|Workers                           |3 (or 2 if `hardwareConcurrency ≤ 3`)|3 (or `cpus - 1`, min 2)|
|Cache size (IndexedDB / in-memory)|50MB                                 |256MB                   |
|Telemetry level                   |`standard`                           |`standard`              |
|Worker unavailable policy         |`refuse_full_path`                   |`refuse_full_path`      |
|CBOR library                      |`cbor-web` (npm)                     |`cbor` (npm)            |
|Bloom filter hash                 |MurmurHash3 (two-seed)               |MurmurHash3 (two-seed)  |

**Runtime health checks:**

- Dispatch overhead P95 < 5ms? (If not, check payload sizes and transfer strategy.)
- Cache hit rate > 60%? (If not, check TTLs and invalidation frequency.)
- Path escalation rate < 30%? (If not, recalibrate classifier per §2.3.)
- Worker queue depth < 2? (If not, queries are arriving faster than workers can process.)

-----

*This specification is designed to be evaluated, reasoned about, and executed using only a browser, a local NodeJS runtime, and JSON-LD files.*