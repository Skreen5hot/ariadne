# W2Fuel Adapter Interfaces & Orchestration Contracts

**Document ID:** `w2fuel-adapters-01`
**Version:** 1.1.0
**Status:** DRAFT — Post-Review
**Classification:** FNSR Core Memory/Identity Layer Component
**Companion to:** `w2fuel-core-01` v2.0.0

---

## Version 1.1.0 Summary: Review-Driven Corrections

> **CHANGE DRIVER:** Stakeholder review of v1.0.0 identified three technical risks that the specification must address at the adapter contract level. Two are correctness issues (cache stampede, auth safety); one is a deployment concern deferred to `w2fuel-deploy-01` with a normative cross-reference added here.

| Change | Section | Risk Addressed | Severity |
|--------|---------|----------------|----------|
| Cache stampede protection | §5.2 | Concurrent cache invalidation under load causes thundering herd on GraphStore | High — correctness under concurrency |
| LocalTrustAuthProvider safety | §6.2 | Silent god-mode in default auth can propagate to production undetected | High — security |
| Clock skew advisory | §3.5 (new) | Multi-node deployments may produce timestamp/sequence inversion | Medium — deferred to deploy-01 with normative note |
| Conformance test additions | §5.2, §6.2, Appendix A, B | New tests for stampede and auth safety behaviors | — |

### What Did NOT Change

All orchestration contracts (§3.1–3.4), adapter interfaces, and the AdapterSet structure are unchanged. These additions are backwards-compatible — existing conformant adapters remain conformant unless they claim production readiness for concurrent workloads.

---

## 1. Purpose & Scope

`w2fuel-core-01` defines W2Fuel's computation: deterministic, stateless functions that take JSON-LD in and produce JSON-LD out. This document defines everything else — the boundaries where computation meets the world.

Specifically, this document is responsible for:

1. **Adapter Interfaces** — The normative type contracts that State, Integration, and Orchestration adapters must satisfy.
2. **Orchestration Contracts** — The ordering constraints, consistency invariants, and failure-mode behaviors that govern how computation results flow through adapters. These are the correctness properties that v1.3.1 embedded in its infrastructure spec and that must not be lost in the refactor.
3. **Default Implementations** — Minimal, dependency-free reference implementations for browser and Node.js execution. These are normative in the sense that they define baseline behavior; they are not normative as the only permitted implementations.
4. **Conformance Requirements** — How an adapter proves it satisfies its contract.

### What This Document Is Not

This document does not specify *which* databases, brokers, or cloud services to use. It specifies the *shape of the hole* they must fill. `w2fuel-deploy-01` provides production implementation guidance for specific technologies (Oxigraph, Redis, Kafka, etc.).

### The "Pluggable Doesn't Mean Unowned" Principle

Every adapter interface defined here has:

- A **contract** — what it must do, including failure behavior
- A **default** — a working implementation with no external dependencies
- **Conformance tests** — executable assertions that any implementation must pass
- An **owner** — the role responsible for the adapter's correctness in a given deployment

If an adapter has no owner, it uses the default. If the default is insufficient, someone must own the replacement. There is no middle state where an adapter is "pluggable" but nobody is responsible for it.

---

## 2. Architectural Position

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   w2fuel-core-01 (Computation)                                              │
│   ════════════════════════════                                              │
│   Pure functions: validate, transpile, materialize, disambiguate, ...       │
│   JSON-LD in → JSON-LD out                                                  │
│   No side effects, no dependencies                                          │
│                                                                             │
│          │ outputs JSON-LD artifacts                                         │
│          ▼                                                                  │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                                                                     │   │
│   │   w2fuel-adapters-01 (This Document)                                │   │
│   │   ══════════════════════════════════                                 │   │
│   │                                                                     │   │
│   │   ORCHESTRATION CONTRACTS                                           │   │
│   │   What ordering, consistency, and failure guarantees                 │   │
│   │   must hold when computation meets the world                        │   │
│   │                                                                     │   │
│   │   ADAPTER INTERFACES                                                │   │
│   │   State: GraphStore, Cache, SequenceStore                           │   │
│   │   Integration: EventEmitter, AuthProvider, SecretsProvider, ...     │   │
│   │   Orchestration: Pipeline, TransactionManager                       │   │
│   │                                                                     │   │
│   │   DEFAULT IMPLEMENTATIONS                                           │   │
│   │   Browser/Node.js reference implementations                         │   │
│   │   No external dependencies                                          │   │
│   │                                                                     │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│          │ adapters instantiated by                                          │
│          ▼                                                                  │
│   w2fuel-deploy-01 (Infrastructure)                                         │
│   ════════════════════════════════                                           │
│   Oxigraph, Redis, Kafka, K8s, HA/DR, monitoring, runbooks                  │
│   Non-normative production optimization                                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Orchestration Contracts

These are the correctness properties that must hold when W2Fuel's computation artifacts are persisted, distributed, and acted upon. They are **normative** — any deployment that violates them is non-conformant regardless of which adapter implementations it uses.

These contracts exist because the critique of v2.0.0 correctly identified that v1.3.1's checkpoint ordering (commit → cache invalidate → health check → emit) encoded real correctness invariants, not just infrastructure procedure. Those invariants belong here.

### 3.1 The Persist-Before-Notify Invariant

**Statement:** No consumer may be notified of a schema change before the change is durably available for query.

This is the most important correctness property in the system. Violating it causes consumers to attempt queries against stale data, producing silent correctness failures.

**Formal expression:**

```
For all schema updates U:
  Let T_persist = time at which U is queryable via GraphStore
  Let T_notify  = time at which SchemaUpdatedEvent for U is emitted via EventEmitter
  Let T_cache   = time at which stale cache entries for U are invalidated

  INVARIANT: T_persist < T_cache < T_notify
```

**Why three phases, in this order:**

1. **Persist first.** If the GraphStore write fails, no notification is sent. No consumer sees a phantom update.
2. **Cache invalidate second.** If consumers query between persist and notify (race condition in polling-based systems), they must not get stale cached results.
3. **Notify last.** When a consumer receives the event, the new data is guaranteed to be both persisted and uncached.

**Failure modes and required behavior:**

| Failure Point | State After Failure | Required Recovery |
|--------------|--------------------|--------------------|
| Persist fails | No change visible | Do not invalidate cache, do not emit event. Return pipeline failure. |
| Persist succeeds, cache invalidation fails | New data in store, stale data in cache | Retry cache invalidation. Do not emit event until cache is confirmed clear. If unrecoverable, emit event with `w2fuel:cacheWarning: true`. |
| Persist and cache succeed, event emission fails | New data available, cache clear, consumers unaware | Retry event emission with backoff. If unrecoverable, log and alert. Consumers using polling will eventually converge. |
| All succeed, but consumer misses event | New data available, consumer on stale version | Consumer detects via `sequenceId` gap (core-01 §7.4 R3) and syncs. |

**This invariant must be enforced by the Orchestration layer** — not by individual adapters, which have no knowledge of each other. The `commitSchemaUpdate` orchestration function (§4.1) is the enforcement point.

### 3.2 The Sequence Monotonicity Invariant

**Statement:** `sequenceId` values in emitted events must be strictly monotonically increasing. No gaps are permitted in normal operation; gaps trigger consumer-side recovery.

**Formal expression:**

```
For all events E_i, E_j where E_i is emitted before E_j:
  E_i.sequenceId < E_j.sequenceId
```

**Enforcement:** The SequenceStore adapter must guarantee atomic increment. In single-process environments (browser, single Node.js process), this is trivially satisfied by an integer variable. In multi-process environments, the adapter must use an atomic operation (e.g., Redis INCR, database sequence).

### 3.3 The Deterministic Replay Invariant

**Statement:** Given the same ontology inputs and the same `sequenceId` / `timestamp` parameters, the orchestration layer must produce identical artifacts regardless of which adapter implementations are active.

This invariant ensures that the pipeline can be replayed for debugging, auditing, or disaster recovery. It is a direct consequence of core-01's determinism guarantee extended to the orchestration layer.

**What this prohibits:**

- Adapter implementations that inject non-deterministic data into computation inputs
- Orchestration logic that branches on adapter-specific state (e.g., "if Redis is available, do X; otherwise do Y" in computation code)
- Timestamp or ID generation within computation functions (these are always parameters from the orchestration layer)

**What this permits:**

- Adapters may add non-deterministic metadata to their *own* telemetry (e.g., logging wall-clock time of persist operations)
- Adapters may retry operations with different timing
- Default and production adapters may have different performance characteristics

### 3.4 The Graceful Degradation Invariant

**Statement:** Adapter failures must not produce undefined behavior in computation. Every adapter method must define a failure return type, and orchestration code must handle it.

This is the adapter-layer complement to core-01's offline behavior contracts (§10). Core functions return explicit uncertainty (`{ valid: null, reason: "..." }`). Adapter failures must be similarly explicit.

**Adapter failure taxonomy:**

| Failure Type | Adapter Behavior | Orchestration Response |
|-------------|-----------------|----------------------|
| **Transient** (timeout, network blip) | Throw/return with `transient: true` | Retry with backoff per adapter policy |
| **Permanent** (auth failure, corrupt data) | Throw/return with `transient: false` | Fail the operation, report to NotificationSink |
| **Degraded** (partial success) | Return partial result with `degraded: true` | Continue with advisory, log degradation |
| **Unavailable** (adapter not configured) | Return `null` or `unavailable` sentinel | Use default adapter or skip optional step |

### 3.5 The Timestamp Authority Constraint

> **V1.1.0 Addition:** Identified during stakeholder review. Addresses timestamp/sequence inversion risk in multi-node deployments.

**Statement:** The orchestration layer is responsible for generating the `timestamp` parameter passed to core computation functions (per core-01 §13.5). In multi-node deployments, all nodes producing timestamps for the same W2Fuel instance **must** derive timestamps from a synchronized source with bounded skew.

**Why this matters:** Core-01 correctly requires `timestamp` as an explicit parameter to preserve determinism. But the orchestration layer must ensure that timestamps correlate with `sequenceId` ordering. If Node A generates `sequenceId: 41` at `T=100` and Node B generates `sequenceId: 42` at `T=99` (due to clock skew), consumers observing both events see a temporal paradox — a later sequence with an earlier timestamp.

**Normative requirement (this document):** Orchestration implementations that support multiple concurrent writers **must** document their clock synchronization strategy and declare their maximum expected skew.

**Implementation guidance (deferred to `w2fuel-deploy-01`):** Specific clock synchronization technologies (NTP, PTP, centralized timestamp authority) and acceptable skew tolerances are deployment concerns. `w2fuel-deploy-01` must specify:

- Maximum acceptable clock skew between W2Fuel nodes
- Recommended synchronization protocol
- Monitoring for skew detection
- Behavior when skew exceeds tolerance

**Single-process environments:** This constraint is trivially satisfied. A single Node.js process or browser tab has a single clock source with no skew.

---

## 4. Orchestration Functions

These are the functions that wire core computation to adapters. They are the bridge between pure functions and the stateful world. They enforce the orchestration contracts defined in §3.

### 4.1 `commitSchemaUpdate`

The primary orchestration function. Takes a `PipelineResult` from core-01's `runValidationPipeline` and commits it to the world.

**Enforces:** Persist-Before-Notify (§3.1), Sequence Monotonicity (§3.2)

```
commitSchemaUpdate(
  pipelineResult: PipelineResult,
  adapters: AdapterSet
) → CommitResult (JSON-LD)
```

**Orchestration sequence:**

```
STEP 1: PERSIST
  adapters.transactionManager.begin() → tx
  adapters.graphStore.update(
    additions = pipelineResult.artifacts.datalogRuleSet,
    removals  = previousRuleSet
  )
  adapters.graphStore.update(
    additions = pipelineResult.artifacts.shaclShapesResult.shapesGraph,
    removals  = previousShapes
  )
  adapters.transactionManager.commit(tx)
  ── ON FAILURE: rollback(tx), return { status: "persist_failed", ... }

STEP 2: CACHE INVALIDATE
  for each ns in pipelineResult.artifacts.schemaUpdatedEvent.affectedNamespaces:
    adapters.cache.invalidate("class:" + ns)
    adapters.cache.invalidate("property:" + ns)
    adapters.cache.invalidate("hierarchy:" + ns)
    adapters.cache.invalidate("shacl:" + ns)
  ── ON FAILURE: retry 3x, then continue with cacheWarning: true

STEP 3: NOTIFY
  adapters.eventEmitter.emit(pipelineResult.artifacts.schemaUpdatedEvent)
  ── ON FAILURE: retry with backoff (100ms, 500ms, 2500ms)
  ── ON EXHAUSTION: log, alert via NotificationSink, return { status: "notify_failed", ... }

STEP 4: RECORD
  adapters.metricsSink.record("w2fuel.commit.duration_ms", elapsed)
  adapters.metricsSink.record("w2fuel.commit.triple_count", tripleCount)
  ── ON FAILURE: swallow (metrics are best-effort)

RETURN: CommitResult
```

**Output — `CommitResult`:**
```json
{
  "@type": "w2fuel:CommitResult",
  "w2fuel:status": "committed",
  "w2fuel:sequenceId": 42,
  "w2fuel:persistedAt": "2026-02-01T15:30:01Z",
  "w2fuel:cacheInvalidatedAt": "2026-02-01T15:30:01.5Z",
  "w2fuel:notifiedAt": "2026-02-01T15:30:02Z",
  "w2fuel:cacheWarning": false,
  "w2fuel:metrics": {
    "w2fuel:persistDurationMs": 230,
    "w2fuel:cacheInvalidationDurationMs": 15,
    "w2fuel:notifyDurationMs": 45
  }
}
```

Note: `CommitResult` contains infrastructure timing metadata because it is an orchestration artifact, not a core computation output. This metadata is appropriate here — the critique of v2.0.0 was correct that removing it from the *event* doesn't mean it should disappear entirely.

### 4.2 `handleSchemaQuery`

Orchestrates a schema query through cache and graph store.

**Enforces:** Graceful Degradation (§3.4)

```
handleSchemaQuery(
  queryType: "class" | "property" | "hierarchy" | "disambiguate",
  params: JSON-LD,
  adapters: AdapterSet
) → QueryResult (JSON-LD)
```

**Orchestration sequence:**

```
STEP 1: AUTH
  identity = adapters.authProvider.authenticate(request)
  if not adapters.authProvider.authorize(identity, "read"):
    return { status: "unauthorized" }

STEP 2: CACHE-AWARE COMPUTE (V1.1.0 — revised for stampede protection)
  cacheKey = deriveCacheKey(queryType, params)
  result = adapters.cache.getOrCompute(
    cacheKey,
    async () => {
      // This computeFn runs at most once per key, even under concurrent load.
      // See §5.2 Cache Stampede Protection contract.
      return (call appropriate core function from w2fuel-core-01 §5)
    },
    ttlMs = 3600000  // 1 hour default
  )

STEP 3: RETURN
  return result with { w2fuel:cacheHit: (was cached) }
```

> **V1.1.0 Change:** Steps 2–3 from v1.0.0 (separate `get`, `compute`, `set`) are replaced with a single `getOrCompute` call. This eliminates the window where concurrent cache misses produce redundant GraphStore queries. See §5.2 for the stampede protection contract.

**Cache miss with GraphStore unavailable:**

If `adapters.graphStore.query()` fails, the orchestration function does not throw. It returns:

```json
{
  "@type": "w2fuel:QueryResult",
  "w2fuel:status": "unavailable",
  "w2fuel:reason": "graph_store_unavailable",
  "w2fuel:retryAfterMs": 5000
}
```

### 4.3 `syncConsumerState`

Allows a downstream consumer to synchronize after detecting a sequence gap or restarting.

```
syncConsumerState(
  lastKnownSequenceId: number,
  adapters: AdapterSet
) → SyncResult (JSON-LD)
```

**Output:**
```json
{
  "@type": "w2fuel:SyncResult",
  "w2fuel:currentSequenceId": 42,
  "w2fuel:consistent": true,
  "w2fuel:missedUpdates": [
    {
      "w2fuel:sequenceId": 41,
      "w2fuel:affectedNamespaces": ["automotive"],
      "w2fuel:updateType": "minor"
    }
  ],
  "w2fuel:shaclBundleHashes": {
    "realestate": "sha256:...",
    "automotive": "sha256:..."
  }
}
```

If the GraphStore cannot reconstruct missed updates (e.g., event history was not retained), the sync result indicates this:

```json
{
  "@type": "w2fuel:SyncResult",
  "w2fuel:currentSequenceId": 42,
  "w2fuel:consistent": false,
  "w2fuel:reason": "history_unavailable",
  "w2fuel:recommendation": "full_refresh"
}
```

---

## 5. State Adapter Specifications

### 5.1 GraphStore

Stores and queries RDF graph data. This is the adapter that replaces v1.3.1's hard dependency on Oxigraph.

#### Interface

```typescript
interface GraphStore {
  /**
   * Load a JSON-LD graph into the store, optionally into a named graph.
   * Replaces any existing content in the target graph.
   */
  load(graph: JsonLd, namedGraph?: string): Promise<void>;

  /**
   * Query the store. Accepts SPARQL SELECT/CONSTRUCT/ASK or
   * a JSON-LD graph pattern (implementation may support either or both).
   * Returns JSON-LD.
   */
  query(expression: string | JsonLd): Promise<JsonLd>;

  /**
   * Atomic update: add and remove triples in a single operation.
   * If the store supports transactions, this executes within one.
   */
  update(additions: JsonLd, removals: JsonLd, namedGraph?: string): Promise<void>;

  /**
   * Export all triples as JSON-LD.
   */
  export(namedGraph?: string): Promise<JsonLd>;

  /**
   * Health check. Returns store status.
   */
  health(): Promise<HealthStatus>;
}

interface HealthStatus {
  available: boolean;
  tripleCount?: number;
  graphCount?: number;
  details?: Record<string, unknown>;
}
```

#### Default Implementation: In-Memory

```
Name:         MemoryGraphStore
Environment:  Browser, Node.js
Dependencies: None (pure JS Map-based triple index) or rdf-ext/N3.js
Persistence:  None (state lost on page refresh / process exit)
Capacity:     Suitable for ontologies up to ~50,000 triples
SPARQL:       Basic pattern matching; full SPARQL 1.1 if N3.js is available
Transactions: Implicit (in-memory operations are synchronous and atomic)
```

**Behavioral notes:**

- `load()` replaces the entire content of the target graph. This is append-or-replace, not merge.
- `query()` with a SPARQL string requires a SPARQL parser (N3.js provides one). If unavailable, only JSON-LD pattern queries are supported, and SPARQL queries return `{ status: "unsupported", reason: "sparql_not_available" }`.
- `export()` returns the full graph. For large stores in production adapters, this may be a streaming operation; the interface does not prescribe buffering strategy.

#### Conformance Tests

Any GraphStore implementation must pass these tests:

| Test | Description | Assertion |
|------|-------------|-----------|
| `load_and_query` | Load a 10-triple JSON-LD graph, query for all triples | Result contains exactly 10 triples |
| `named_graphs` | Load into two named graphs, query each independently | Each returns only its own triples |
| `update_add_remove` | Load 10 triples, update (add 3, remove 2) | Store contains 11 triples |
| `update_atomicity` | Update with invalid removal (triple doesn't exist) | Implementation-defined: either full rollback or skip missing. Must not corrupt. |
| `export_roundtrip` | Load graph, export, reload export, query | Identical results (modulo blank node IDs) |
| `empty_query` | Query for nonexistent pattern | Returns empty result set, not error |
| `health_available` | Call health() on initialized store | `{ available: true }` |
| `health_uninitialized` | Call health() before any load | `{ available: true, tripleCount: 0 }` |
| `concurrent_reads` | Issue 10 simultaneous queries | All return correct results (no corruption) |
| `large_load` | Load 50,000 triples | Completes without error (performance not asserted) |

### 5.2 Cache

Caches computation results to avoid redundant work. The cache is a performance optimization — its absence must never cause correctness failures.

#### Interface

```typescript
interface Cache {
  /**
   * Retrieve a cached value. Returns null if key is absent or expired.
   */
  get(key: string): Promise<JsonLd | null>;

  /**
   * Store a value with optional time-to-live.
   * If ttlMs is omitted, the entry does not expire.
   */
  set(key: string, value: JsonLd, ttlMs?: number): Promise<void>;

  /**
   * Retrieve a cached value, or compute and cache it if absent.
   *
   * V1.1.0 ADDITION: This method exists to prevent cache stampede.
   * When multiple concurrent callers request the same absent key,
   * only ONE invocation of computeFn executes. All other callers
   * await the result of that single computation.
   *
   * Default (MemoryCache) implementation: trivially serialized by
   * the JS event loop. Production implementations MUST provide
   * explicit stampede protection (e.g., single-flight, mutex,
   * probabilistic early expiry).
   */
  getOrCompute(
    key: string,
    computeFn: () => Promise<JsonLd>,
    ttlMs?: number
  ): Promise<JsonLd>;

  /**
   * Remove all entries whose key starts with the given prefix.
   */
  invalidate(prefix: string): Promise<void>;

  /**
   * Remove all entries.
   */
  clear(): Promise<void>;
}
```

#### Contract: Cache Is Never Authoritative

**INVARIANT:** The cache is a read-through optimization. If the cache returns null, orchestration code falls through to computation. If the cache returns a stale value (due to race condition between invalidation and read), the worst consequence is a slightly delayed view — the next invalidation cycle or TTL expiry corrects it.

No correctness property of the system may depend on cache contents. Any adapter that violates this — for example, by using the cache as primary storage — is non-conformant.

#### Contract: Cache Stampede Protection (V1.1.0)

> **V1.1.0 Addition:** Identified during stakeholder review. Addresses thundering herd on GraphStore after cache invalidation during `commitSchemaUpdate`.

**The problem:** Step 2 of `commitSchemaUpdate` (§4.1) invalidates cache entries for affected namespaces. In high-concurrency deployments, the window between cache invalidation and the first repopulating query can produce N simultaneous GraphStore queries for the same key — a "thundering herd" or "cache stampede." For large hierarchy queries this can saturate the GraphStore and cascade into downstream timeouts.

**The contract:** The `getOrCompute` method **must** guarantee that for any given key, at most one concurrent invocation of `computeFn` executes at a time. Additional concurrent callers for the same key **must** await the result of the in-flight computation rather than launching their own.

**Minimum conformance levels:**

| Level | Requirement | Suitable For |
|-------|-------------|-------------|
| **Basic** | `getOrCompute` calls `get`, then `computeFn` + `set` if null. No explicit coalescing. | Single-process, low concurrency (browser, dev) |
| **Production** | `getOrCompute` coalesces concurrent misses for the same key into a single `computeFn` invocation. | Multi-thread, multi-process, high concurrency |

Adapters that claim Production-level conformance must pass the `stampede_coalescing` conformance test (see below).

**Recommended strategies for production implementations:**

- **Single-flight / request coalescing:** Track in-flight keys; subsequent callers join the pending Promise.
- **Probabilistic early expiry (PER):** Recompute slightly before TTL expires, avoiding the simultaneous-expiry cliff.
- **Lock-based:** Acquire a distributed lock per key before computing; others wait on lock. Use with caution — lock contention can be worse than the stampede.

**Impact on `handleSchemaQuery` (§4.2):** The orchestration function `handleSchemaQuery` should use `getOrCompute` instead of the `get` / compute / `set` sequence:

```
STEP 2 (REVISED): CACHE-AWARE COMPUTE
  result = adapters.cache.getOrCompute(
    cacheKey,
    async () => { return (call core function); },
    ttlMs
  )
```

#### Default Implementation: In-Memory Map

```
Name:         MemoryCache
Environment:  Browser, Node.js
Dependencies: None
Persistence:  None
TTL:          Enforced via lazy expiry check on get()
Capacity:     Unbounded (caller responsible for not caching excessively)
```

**Default TTL policy:**

| Key Pattern | Default TTL | Rationale |
|-------------|-------------|-----------|
| `class:{ns}:{name}` | 1 hour | Class definitions change infrequently |
| `property:{ns}:{name}` | 1 hour | Property definitions change infrequently |
| `hierarchy:{ns}:{root}` | 1 hour | Hierarchy structure changes infrequently |
| `shacl:{ns}:{version}` | 24 hours | SHACL bundles are versioned and immutable per version |
| `disambiguate:{hash}` | 15 minutes | Disambiguation depends on registry state |

#### Conformance Tests

| Test | Description | Assertion |
|------|-------------|-----------|
| `set_get` | Set a value, get it back | Identical JSON-LD |
| `get_missing` | Get a key that was never set | Returns null |
| `ttl_expiry` | Set with ttlMs=100, wait 150ms, get | Returns null |
| `invalidate_prefix` | Set keys `a:1`, `a:2`, `b:1`, invalidate `a:` | `a:1` and `a:2` return null; `b:1` still present |
| `clear_all` | Set 5 keys, clear, get all | All return null |
| `overwrite` | Set key, set same key with new value, get | Returns new value |
| `get_or_compute_miss` | `getOrCompute` on absent key | `computeFn` called once; result cached and returned |
| `get_or_compute_hit` | Set key, then `getOrCompute` | `computeFn` never called; cached value returned |

**Production-level conformance tests** (required for adapters claiming Production stampede protection):

| Test | Description | Assertion |
|------|-------------|-----------|
| `stampede_coalescing` | Launch 50 concurrent `getOrCompute` calls for the same absent key, where `computeFn` takes 100ms. Count `computeFn` invocations. | `computeFn` called exactly once. All 50 callers receive the same result. |
| `stampede_different_keys` | Launch 50 concurrent `getOrCompute` calls across 10 distinct keys. | Each key's `computeFn` called exactly once. No cross-key blocking. |
| `stampede_error_propagation` | `getOrCompute` where `computeFn` throws. 10 concurrent callers. | All 10 callers receive the error. Subsequent `getOrCompute` retries (does not cache the error). |

### 5.3 SequenceStore

Maintains the monotonically increasing sequence counter for schema update events.

#### Interface

```typescript
interface SequenceStore {
  /**
   * Return the current sequence value without incrementing.
   */
  getCurrent(): Promise<number>;

  /**
   * Atomically increment and return the new value.
   * MUST guarantee that no two calls return the same value,
   * even under concurrent access.
   */
  getNext(): Promise<number>;
}
```

#### Atomicity Requirement

In single-process environments, `getNext()` is trivially atomic (increment a variable). In multi-process environments (e.g., multiple W2Fuel instances behind a load balancer), the adapter **must** use an atomic operation. Failure to guarantee atomicity violates the Sequence Monotonicity invariant (§3.2) and can cause consumers to silently drop events.

#### Default Implementation: Counter Variable

```
Name:         MemorySequenceStore
Environment:  Browser, Node.js (single process)
Dependencies: None
Persistence:  None (resets to 0 on restart)
Atomicity:    Guaranteed (single-threaded JS event loop)
```

**On restart behavior:** The default implementation resets to 0. Orchestration code must call `syncConsumerState` (§4.3) after restart to inform consumers of the discontinuity. Production adapters (Redis INCR, database sequence) persist across restarts.

#### Conformance Tests

| Test | Description | Assertion |
|------|-------------|-----------|
| `initial_value` | getCurrent() on fresh store | Returns 0 |
| `increment` | getNext() three times | Returns 1, 2, 3 |
| `current_after_increment` | getNext(), getCurrent() | getCurrent returns same as last getNext |
| `no_duplicates` | Call getNext() 1000 times, collect results | All values unique, strictly increasing |

---

## 6. Integration Adapter Specifications

### 6.1 EventEmitter

Distributes schema update events to downstream consumers.

#### Interface

```typescript
interface EventEmitter {
  /**
   * Emit a schema update event. Returns an acknowledgment
   * that the event has been accepted by the transport layer.
   *
   * "Accepted" means the transport has taken responsibility
   * for delivery. It does NOT mean all consumers have processed it.
   */
  emit(event: JsonLd): Promise<EmitAck>;
}

interface EmitAck {
  accepted: boolean;
  transportId?: string;    // Kafka offset, message ID, etc.
  timestamp?: string;
  error?: string;
}
```

#### Delivery Semantics

The EventEmitter interface guarantees **at-least-once** delivery semantics. Consumers must be idempotent (core-01 §7.4). The interface does not guarantee ordering across multiple consumers — only that each consumer sees events in order for a given partition/channel.

**Why not exactly-once:** Exactly-once delivery requires coupling between the event transport and the consumer's state store, which violates adapter independence. At-least-once with consumer-side idempotency achieves the same correctness without the coupling.

#### Default Implementation: Callback

```
Name:         CallbackEventEmitter
Environment:  Browser, Node.js
Dependencies: None
Delivery:     Synchronous callback invocation
Persistence:  None (events not buffered)
```

```javascript
// Default: synchronous callback
class CallbackEventEmitter {
  constructor() {
    this.listeners = [];
  }

  subscribe(callback) {
    this.listeners.push(callback);
  }

  async emit(event) {
    for (const listener of this.listeners) {
      listener(event);
    }
    return { accepted: true };
  }
}
```

**Browser variant:** Uses `window.postMessage` for cross-frame communication when W2Fuel runs in an iframe or Web Worker.

#### Conformance Tests

| Test | Description | Assertion |
|------|-------------|-----------|
| `emit_returns_ack` | Emit a valid event | Returns `{ accepted: true }` |
| `emit_reaches_subscriber` | Subscribe, emit, check | Subscriber receives event |
| `emit_preserves_content` | Emit, capture at subscriber | Received event is identical JSON-LD |
| `emit_multiple_subscribers` | Subscribe 3 listeners, emit | All 3 receive the event |
| `emit_failure_returns_nack` | Configure transport to fail, emit | Returns `{ accepted: false, error: "..." }` |

### 6.2 AuthProvider

Authenticates identities and authorizes actions against the RBAC model defined in core-01 §8.3.

#### Interface

```typescript
interface AuthProvider {
  /**
   * Verify an identity from credentials.
   * What "credentials" means is adapter-specific
   * (JWT token, API key, session cookie, etc.).
   */
  authenticate(credentials: unknown): Promise<Identity>;

  /**
   * Check whether an identity has permission for an action.
   * Actions map to core-01 §8.3 RBAC permissions.
   */
  authorize(identity: Identity, action: string): Promise<boolean>;
}

interface Identity {
  id: string;
  roles: string[];           // From core-01 §8.3 RBAC model
  authenticated: boolean;
  metadata?: Record<string, unknown>;
}
```

#### Actions Vocabulary

| Action | Required Role | Description |
|--------|--------------|-------------|
| `schema.read` | `authenticated_service` | Read class/property definitions |
| `schema.query` | `authenticated_service` | SPARQL/pattern queries |
| `shacl.download` | `authenticated_service` | Download SHACL bundles |
| `schema.propose` | `schema_author` | Submit change proposals |
| `schema.approve.minor` | `domain_steward` | Approve minor changes |
| `schema.approve.major` | `governance_body` | Approve major changes |
| `admin.operate` | `operator` | Administrative operations |
| `health.check` | `anonymous` | Health/status only |

#### Default Implementation: Local Trust

```
Name:         LocalTrustAuthProvider
Environment:  Browser, Node.js (local development)
Dependencies: None
Behavior:     All identities are authenticated with all roles
Safety:       Emits warning on every call; marks responses with auth mode (V1.1.0)
```

```javascript
class LocalTrustAuthProvider {
  constructor(notificationSink) {
    this.notificationSink = notificationSink;
    this._warnedThisSession = false;
  }

  async authenticate(_credentials) {
    // V1.1.0: Emit visible warning that local trust is active
    if (this.notificationSink && !this._warnedThisSession) {
      await this.notificationSink.notify({
        "@type": "w2fuel:OperationalAlert",
        "w2fuel:severity": "warning",
        "w2fuel:source": "LocalTrustAuthProvider",
        "w2fuel:message":
          "LOCAL TRUST AUTH ACTIVE — all requests authorized with governance_body role. " +
          "This is appropriate for local development only. Any deployment accepting " +
          "external requests MUST replace this with a production AuthProvider.",
        "w2fuel:timestamp": new Date().toISOString()
      });
      this._warnedThisSession = true;
    }

    return {
      id: "local-user",
      roles: ["governance_body"],  // Maximum permissions
      authenticated: true,
      metadata: {
        "w2fuel:authMode": "local_trust"  // V1.1.0: Always visible in identity
      }
    };
  }

  async authorize(_identity, _action) {
    return true;
  }
}
```

> **V1.1.0 Safety Addition:** The `LocalTrustAuthProvider` now:
>
> 1. **Emits a warning** via NotificationSink on first use per session. In the default adapter set this produces a `console.warn` — visible to developers, auditable in logs, impossible to miss when reviewing output.
> 2. **Tags every identity** with `w2fuel:authMode: "local_trust"` in metadata. Downstream code and HTTP responses (§9.2) can surface this flag. A production monitoring system can alert on any request where `authMode != "production"`.
> 3. **Accepts NotificationSink as constructor parameter.** The `createDefaultAdapters` factory (§7) wires this automatically. If no sink is provided, the warning is skipped (pure testing scenarios).

**Security note:** LocalTrustAuthProvider is appropriate only for local development, testing, and browser-based exploration. Any deployment accepting external requests **must** replace it with a production AuthProvider. The `w2fuel-deploy-01` document specifies OAuth 2.0 + JWT (RS256) as the production implementation.

#### Auth Mode Visibility in HTTP Responses (V1.1.0)

When the HTTP adapter (§9) is active, the `w2fuel:authMode` value from the Identity metadata **should** be surfaced as a response header:

```http
X-W2Fuel-Auth-Mode: local_trust
```

Production deployments can use this header for:

- Load balancer health checks (reject instances running local trust)
- Monitoring alerts (any response with `X-W2Fuel-Auth-Mode: local_trust` in production triggers alert)
- Audit trails

#### Conformance Tests

| Test | Description | Assertion |
|------|-------------|-----------|
| `authenticate_returns_identity` | Call with valid credentials | Returns Identity with `authenticated: true` |
| `authenticate_invalid` | Call with invalid credentials | Returns Identity with `authenticated: false` or throws |
| `authorize_permitted` | Identity with `authenticated_service` role, action `schema.read` | Returns `true` |
| `authorize_denied` | Identity with `anonymous` role, action `schema.propose` | Returns `false` |
| `authorize_hierarchy` | Identity with `governance_body`, action `schema.read` | Returns `true` (higher role includes lower) |
| `local_trust_warning_emitted` | Use LocalTrustAuthProvider with a mock NotificationSink, authenticate once | NotificationSink.notify called with severity `warning` and message containing `LOCAL TRUST` |
| `local_trust_warning_once` | Authenticate 10 times | NotificationSink.notify called exactly once (first call only) |
| `local_trust_metadata_tagged` | Authenticate | Identity.metadata contains `w2fuel:authMode: "local_trust"` |
| `production_auth_no_local_tag` | Use any non-LocalTrust AuthProvider, authenticate | Identity.metadata does NOT contain `w2fuel:authMode: "local_trust"` |

### 6.3 SecretsProvider

Provides cryptographic keys for SHACL bundle signing and verification.

#### Interface

```typescript
interface SecretsProvider {
  /**
   * Return the active Ed25519 private key for signing.
   * Returns null if no signing key is configured (signing disabled).
   */
  getSigningKey(): Promise<Uint8Array | null>;

  /**
   * Return all currently valid Ed25519 public keys for verification.
   * May include the current key plus recently-rotated keys
   * during overlap periods.
   */
  getVerificationKeys(): Promise<VerificationKey[]>;
}

interface VerificationKey {
  keyId: string;
  publicKey: Uint8Array;
  validFrom: string;      // ISO datetime
  validUntil?: string;    // ISO datetime; absent = no expiry
}
```

#### Default Implementation: Environment/File

```
Name:         FileSecretsProvider
Environment:  Node.js
Dependencies: None (reads files or environment variables)
Key Format:   Raw Ed25519 bytes, base64-encoded
```

```
Name:         TestSecretsProvider
Environment:  Browser, Node.js (testing)
Dependencies: None
Behavior:     Returns a hardcoded test keypair
              MUST NOT be used in any deployment accepting external data
```

#### Conformance Tests

| Test | Description | Assertion |
|------|-------------|-----------|
| `signing_key_present` | getSigningKey() when configured | Returns non-null Uint8Array of 32 bytes |
| `signing_key_absent` | getSigningKey() when not configured | Returns null |
| `verification_keys` | getVerificationKeys() | Returns at least one key with valid keyId |
| `sign_verify_roundtrip` | Sign data with signing key, verify with verification keys | Verification succeeds |

### 6.4 NotificationSink

Emits operational alerts for adapter-layer failures and anomalies.

#### Interface

```typescript
interface NotificationSink {
  /**
   * Send an alert. Fire-and-forget — notification failures
   * must not block orchestration.
   */
  notify(alert: JsonLd): Promise<void>;
}
```

**Alert schema:**
```json
{
  "@type": "w2fuel:OperationalAlert",
  "w2fuel:severity": "warning",
  "w2fuel:source": "commitSchemaUpdate",
  "w2fuel:message": "Cache invalidation failed after 3 retries",
  "w2fuel:timestamp": "2026-02-01T15:30:02Z",
  "w2fuel:context": {
    "w2fuel:sequenceId": 42,
    "w2fuel:affectedNamespaces": ["realestate"]
  }
}
```

**Severity levels:** `info`, `warning`, `error`, `critical`

#### Default Implementation: Console

```javascript
class ConsoleNotificationSink {
  async notify(alert) {
    const severity = alert["w2fuel:severity"] || "info";
    const method = severity === "critical" || severity === "error"
      ? "error" : severity === "warning" ? "warn" : "log";
    console[method]("[W2Fuel]", alert["w2fuel:message"], alert);
  }
}
```

### 6.5 MetricsSink

Records performance and health metrics. Metrics are best-effort — failures are silently swallowed.

#### Interface

```typescript
interface MetricsSink {
  /**
   * Record a metric value. Tags provide dimensional context.
   * Failures are silently swallowed — metrics must never
   * interfere with operation.
   */
  record(metric: string, value: number, tags?: Record<string, string>): void;
}
```

#### Metric Vocabulary

These are the metrics that orchestration functions emit. Production MetricsSink implementations should expect them.

| Metric | Unit | Emitted By | Description |
|--------|------|-----------|-------------|
| `w2fuel.pipeline.duration_ms` | ms | Pipeline orchestration | Total pipeline execution time |
| `w2fuel.pipeline.stage_duration_ms` | ms | Pipeline orchestration | Per-stage timing (tag: `stage`) |
| `w2fuel.commit.duration_ms` | ms | `commitSchemaUpdate` | Total commit orchestration time |
| `w2fuel.commit.persist_duration_ms` | ms | `commitSchemaUpdate` | GraphStore persist time |
| `w2fuel.commit.cache_invalidation_ms` | ms | `commitSchemaUpdate` | Cache invalidation time |
| `w2fuel.commit.notify_duration_ms` | ms | `commitSchemaUpdate` | Event emission time |
| `w2fuel.query.duration_ms` | ms | `handleSchemaQuery` | Query handling time |
| `w2fuel.query.cache_hit` | 0/1 | `handleSchemaQuery` | Cache hit rate |
| `w2fuel.event.gap_detected` | count | Consumer sync | Sequence gaps observed |

#### Default Implementation: No-Op

```javascript
class NoOpMetricsSink {
  record(_metric, _value, _tags) {
    // Intentionally empty
  }
}
```

---

## 7. The AdapterSet

All adapters are assembled into a single configuration object passed to orchestration functions. This makes dependencies explicit and prevents ambient service lookup.

```typescript
interface AdapterSet {
  // State
  graphStore: GraphStore;
  cache: Cache;
  sequenceStore: SequenceStore;

  // Integration
  eventEmitter: EventEmitter;
  authProvider: AuthProvider;
  secretsProvider: SecretsProvider;
  notificationSink: NotificationSink;
  metricsSink: MetricsSink;

  // Orchestration
  transactionManager: TransactionManager;
}
```

#### Default AdapterSet Factory

```javascript
function createDefaultAdapters() {
  // V1.1.0: NotificationSink must be created first so LocalTrustAuthProvider
  // can emit its safety warning through it.
  const notificationSink = new ConsoleNotificationSink();

  return {
    graphStore:         new MemoryGraphStore(),
    cache:              new MemoryCache(),
    sequenceStore:      new MemorySequenceStore(),
    eventEmitter:       new CallbackEventEmitter(),
    authProvider:       new LocalTrustAuthProvider(notificationSink),  // V1.1.0: wired
    secretsProvider:    new TestSecretsProvider(),
    notificationSink:   notificationSink,
    metricsSink:        new NoOpMetricsSink(),
    transactionManager: new NoOpTransactionManager()
  };
}
```

This factory produces a fully functional AdapterSet with zero external dependencies. It runs in any browser or Node.js environment. It is the baseline against which all production AdapterSets are measured.

> **V1.1.0 Note:** The factory now wires `notificationSink` into `LocalTrustAuthProvider` so the safety warning (§6.2) is emitted via `console.warn` on first authentication. This makes the "god mode" state visible in developer consoles and CI/CD logs without requiring any configuration.

---

## 8. TransactionManager

Provides atomicity for multi-step state mutations.

#### Interface

```typescript
interface TransactionManager {
  begin(): Promise<Transaction>;
  commit(tx: Transaction): Promise<void>;
  rollback(tx: Transaction): Promise<void>;
}

interface Transaction {
  id: string;
  startedAt: string;
  status: "active" | "committed" | "rolled_back";
}
```

#### Default Implementation: No-Op

In-memory state adapters (MemoryGraphStore, MemoryCache) execute synchronously in the JS event loop. A single `update()` call is atomic by nature. The No-Op TransactionManager satisfies the interface without overhead.

```javascript
class NoOpTransactionManager {
  async begin() {
    return { id: crypto.randomUUID(), startedAt: new Date().toISOString(), status: "active" };
  }
  async commit(tx) { tx.status = "committed"; }
  async rollback(tx) { tx.status = "rolled_back"; }
}
```

**When No-Op is insufficient:** Any deployment where the GraphStore and Cache are separate systems (e.g., Oxigraph + Redis) requires a TransactionManager that coordinates across both. This is the most complex adapter to implement correctly. `w2fuel-deploy-01` provides guidance for the Oxigraph+Redis case.

#### Conformance Tests

| Test | Description | Assertion |
|------|-------------|-----------|
| `begin_returns_active` | begin() | Returns Transaction with `status: "active"` |
| `commit_changes_status` | begin(), commit() | Transaction status is `"committed"` |
| `rollback_changes_status` | begin(), rollback() | Transaction status is `"rolled_back"` |
| `commit_after_rollback` | begin(), rollback(), commit() | Throws or returns error (cannot commit rolled-back tx) |
| `double_commit` | begin(), commit(), commit() | Throws or returns error (idempotent commit is also acceptable) |

---

## 9. HTTP Adapter (Non-Normative Reference)

This section defines a non-normative HTTP mapping for W2Fuel's orchestration functions. It is one possible integration surface — not the only one. A WebSocket adapter, gRPC adapter, or in-process function call are equally valid.

This section preserves the endpoint contract from v1.3.1 §10 for backward compatibility.

### 9.1 Endpoint Mapping

| Method | Path | Orchestration Function | Notes |
|--------|------|----------------------|-------|
| GET | `/v1/class/{prefix}:{localname}` | `handleSchemaQuery("class", ...)` | |
| GET | `/v1/property/{prefix}:{localname}` | `handleSchemaQuery("property", ...)` | |
| GET | `/v1/hierarchy/{prefix}:{localname}` | `handleSchemaQuery("hierarchy", ...)` | |
| POST | `/v1/namespace/resolve` | `handleSchemaQuery("disambiguate", ...)` | Body: DisambiguationContext |
| GET | `/v1/shacl/{namespace}/{version}` | Direct SHACL bundle retrieval | Signed; verify before use |
| GET | `/v1/datalog/{namespace}/{version}` | Direct Datalog rule retrieval | |
| POST | `/v1/sparql` | `adapters.graphStore.query(...)` | Passes through to GraphStore |
| GET | `/v1/health` | `adapters.graphStore.health()` | |
| GET | `/v1/admin/consistency-check` | `syncConsumerState(0, adapters)` | For consumer synchronization |

### 9.2 Response Headers

All responses include metadata headers for consumer awareness:

```http
X-W2Fuel-Verification: verified | lite | partial
X-W2Fuel-Schema-Version: {namespace}-v{semver}
X-W2Fuel-Sequence-Id: {current_sequence_id}
X-W2Fuel-Cache: HIT | MISS | BYPASS
X-W2Fuel-Auth-Mode: {auth_mode}
```

> **V1.1.0 Addition:** `X-W2Fuel-Auth-Mode` is projected from `Identity.metadata["w2fuel:authMode"]`. When LocalTrustAuthProvider is active, this header reads `local_trust` — making the security posture visible in every HTTP response. See §6.2 for monitoring and alerting guidance.

These headers are convenience projections of data available in the JSON-LD response body.

### 9.3 Content Negotiation

```
Accept: application/ld+json          → JSON-LD (canonical)
Accept: text/turtle                  → Turtle (derived)
Accept: application/n-triples        → N-Triples (derived)
Accept: application/sparql-results+json → SPARQL results (for /sparql endpoint)
```

JSON-LD is the default if no Accept header is provided.

---

## 10. Performance Advisory

`w2fuel-core-01` deliberately omits performance commitments because performance is adapter-dependent. This section provides **advisory** performance expectations that inform downstream timeout budgets. These are not SLOs — they are guidance for adapter implementers and consumer architects.

### 10.1 Expected Performance Ranges

| Operation | Default (In-Memory) | Production (Oxigraph+Redis) | Downstream Timeout Guidance |
|-----------|--------------------|-----------------------------|---------------------------|
| Class/property query (cached) | < 1ms | < 5ms | 100ms |
| Class/property query (uncached) | < 50ms | < 100ms | 500ms |
| Hierarchy traversal (depth 5) | < 100ms | < 200ms | 1s |
| Namespace disambiguation | < 10ms | < 50ms | 200ms |
| SHACL bundle download | < 10ms | < 50ms (+ network) | 2s |
| Full pipeline (small ontology) | < 500ms | < 5s | 30s |
| Full pipeline (large ontology) | < 5s | < 30s | 120s |
| Datalog materialization (5k axioms) | < 2s | < 500ms (Nemo) | 30s |

**These numbers are approximate.** Production adapters should publish their own SLOs in `w2fuel-deploy-01`. The "Downstream Timeout Guidance" column provides safe upper bounds that consumers can use for circuit breaker configuration.

### 10.2 Performance Conformance

Adapter implementations are not required to meet specific performance thresholds to be conformant. They *are* required to:

1. **Report timing** via MetricsSink for every operation
2. **Not hang** — every operation must have a finite timeout, declared in adapter configuration
3. **Degrade gracefully** — if a timeout fires, return a well-typed failure, not an opaque error

---

## 11. Adapter Ownership Model

Every adapter in a deployment must have an explicit owner. The owner is responsible for:

- Ensuring the adapter passes all conformance tests
- Monitoring adapter-specific metrics
- Responding to adapter-specific alerts
- Upgrading the adapter when core-01 or adapters-01 evolves

### 11.1 Ownership Table Template

Deployments should maintain a populated version of this table:

| Adapter | Implementation | Owner (Role) | Owner (Person/Team) | Conformance Last Verified |
|---------|---------------|-------------|--------------------|--------------------------:|
| GraphStore | MemoryGraphStore | — | (default, no owner needed) | N/A |
| GraphStore | OxigraphAdapter | SRE Lead | | |
| Cache | MemoryCache | — | (default, no owner needed) | N/A |
| Cache | RedisAdapter | SRE Lead | | |
| SequenceStore | MemorySequenceStore | — | (default, no owner needed) | N/A |
| EventEmitter | CallbackEventEmitter | — | (default, no owner needed) | N/A |
| EventEmitter | KafkaAdapter | Platform Team | | |
| AuthProvider | LocalTrustAuthProvider | — | (default, no owner needed) | N/A |
| AuthProvider | OAuthJwtAdapter | Security Team | | |
| SecretsProvider | TestSecretsProvider | — | (default, no owner needed) | N/A |
| SecretsProvider | VaultAdapter | Security Team | | |
| NotificationSink | ConsoleNotificationSink | — | (default, no owner needed) | N/A |
| MetricsSink | NoOpMetricsSink | — | (default, no owner needed) | N/A |
| TransactionManager | NoOpTransactionManager | — | (default, no owner needed) | N/A |
| TransactionManager | OxigraphTxAdapter | SRE Lead | | |

Default adapters require no owner because they have no external dependencies that can fail in adapter-specific ways. The moment a default is replaced with a production adapter, someone must own it.

---

## 12. Document Coordination Protocol

The three-document split (core-01, adapters-01, deploy-01) creates a coordination risk identified in the v2.0.0 critique. This section defines the protocol for managing cross-document consistency.

### 12.1 Dependency Direction

```
core-01 ←── adapters-01 ←── deploy-01
  (no deps)   (depends on     (depends on
               core-01         both)
               types)
```

**core-01** never references adapters-01 or deploy-01. Changes to core-01 may require updates to both downstream documents.

**adapters-01** references core-01's type definitions (JSON-LD schemas, function signatures). Changes to adapter interfaces may require deploy-01 updates but never core-01 changes.

**deploy-01** references both upstream documents. Changes to deploy-01 never require changes to core-01 or adapters-01.

### 12.2 Change Impact Matrix

| Change In | Core-01 Impact | Adapters-01 Impact | Deploy-01 Impact |
|-----------|---------------|-------------------|-----------------|
| New core function added | — | May need new adapter methods if function has side-effect-free variants | May need deployment guidance |
| Core function signature changed | — | Update orchestration functions that call it | Update CI/CD configuration |
| New adapter interface added | None | — | Must provide production implementation |
| Adapter interface changed | None | — | Must update production implementation |
| New deployment technology | None | None | — |

### 12.3 Version Compatibility

Each document declares which versions of its dependencies it is compatible with:

```
This document: w2fuel-adapters-01 v1.1.0
Requires:      w2fuel-core-01 >= 2.0.0
```

---

## Appendix A: Full Conformance Test Suite Index

> **V1.1.0 Update:** Added 12 new tests (Cache stampede, AuthProvider safety). Test suite now split into Basic (required for all adapters) and Production (required for adapters claiming production readiness).

All conformance tests across all adapters, collected for CI/CD integration:

### Basic Conformance (Required for all implementations)

| Adapter | Test Count | Test Names |
|---------|-----------|------------|
| GraphStore | 10 | `load_and_query`, `named_graphs`, `update_add_remove`, `update_atomicity`, `export_roundtrip`, `empty_query`, `health_available`, `health_uninitialized`, `concurrent_reads`, `large_load` |
| Cache | 8 | `set_get`, `get_missing`, `ttl_expiry`, `invalidate_prefix`, `clear_all`, `overwrite`, `get_or_compute_miss`, `get_or_compute_hit` |
| SequenceStore | 4 | `initial_value`, `increment`, `current_after_increment`, `no_duplicates` |
| EventEmitter | 5 | `emit_returns_ack`, `emit_reaches_subscriber`, `emit_preserves_content`, `emit_multiple_subscribers`, `emit_failure_returns_nack` |
| AuthProvider | 9 | `authenticate_returns_identity`, `authenticate_invalid`, `authorize_permitted`, `authorize_denied`, `authorize_hierarchy`, `local_trust_warning_emitted`, `local_trust_warning_once`, `local_trust_metadata_tagged`, `production_auth_no_local_tag` |
| SecretsProvider | 4 | `signing_key_present`, `signing_key_absent`, `verification_keys`, `sign_verify_roundtrip` |
| TransactionManager | 5 | `begin_returns_active`, `commit_changes_status`, `rollback_changes_status`, `commit_after_rollback`, `double_commit` |
| **Basic Total** | **45** | |

### Production Conformance (Required for adapters claiming production readiness)

| Adapter | Test Count | Test Names |
|---------|-----------|------------|
| Cache (Stampede) | 3 | `stampede_coalescing`, `stampede_different_keys`, `stampede_error_propagation` |
| **Production Total** | **3** | |

### Combined Total: **48 tests**

Any adapter implementation must pass all tests for its interface before deployment.

---

## Appendix B: Orchestration Contract Verification

In addition to per-adapter conformance tests, the orchestration contracts (§3) require end-to-end verification:

| Contract | Test | Description |
|----------|------|-------------|
| Persist-Before-Notify (§3.1) | `e2e_persist_before_notify` | Instrument adapters with timestamps; verify `T_persist < T_cache < T_notify` |
| Persist-Before-Notify failure | `e2e_persist_fails_no_notify` | Configure GraphStore to fail; verify EventEmitter.emit() is never called |
| Sequence Monotonicity (§3.2) | `e2e_sequence_monotonic` | Run 100 commits; verify all sequenceIds are strictly increasing |
| Deterministic Replay (§3.3) | `e2e_deterministic_replay` | Run pipeline twice with same inputs; verify identical PipelineResult |
| Graceful Degradation (§3.4) | `e2e_cache_failure_continues` | Configure Cache to fail; verify commit still succeeds (with cacheWarning) |
| Graceful Degradation (§3.4) | `e2e_metrics_failure_ignored` | Configure MetricsSink to throw; verify commit still succeeds |
| Stampede Protection (§5.2) | `e2e_invalidate_then_query_storm` | Commit a schema update, then immediately issue 50 concurrent queries for an affected key. Verify GraphStore receives ≤ 1 query per key (not 50). |
| Auth Safety (§6.2) | `e2e_local_trust_visible_in_response` | Use default AdapterSet with HTTP adapter; issue a request; verify `X-W2Fuel-Auth-Mode: local_trust` header is present in response. |

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0-draft | 2026-02-19 | Aaron / Claude | Initial specification: adapter interfaces, orchestration contracts, conformance tests, ownership model, document coordination protocol |
| **1.1.0** | **2026-02-19** | **Aaron / Claude** | **Review-driven corrections: Cache stampede protection (§5.2 getOrCompute, conformance levels, production tests); LocalTrustAuthProvider safety (§6.2 warning emission, auth mode tagging, HTTP header); Clock skew advisory (§3.5); handleSchemaQuery revised for getOrCompute (§4.2); AdapterSet factory wiring (§7); Conformance suite expanded from 39 to 48 tests** |

---

*End of Adapter Specification*
