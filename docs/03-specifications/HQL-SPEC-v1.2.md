# HIRI Query Layer Specification

**Document ID:** HQL-SPEC-QL
**Version:** 1.2.0
**Previous:** 1.1.0
**Status:** Draft — Candidate for Stable
**Type:** Normative Edge-Canonical Module
**Depends on:** HIRI Protocol Specification v3.1.1, HIRI Privacy & Confidentiality Extension v1.4.1

---

## v1.2.0 Revision Notes (from v1.1.0)

This revision addresses one substantive implementation risk identified in adversarial review of v1.1.0. No prior normative semantics are removed. All changes are additive.

| Change | Section | Nature | Reason |
|--------|---------|--------|--------|
| **Worker Message Protocol defined** | §6.6 | Additive — Normative | v1.1.0 described the SharedWorker architecture as RECOMMENDED but left the `postMessage` wire format unspecified; without a defined protocol, every SDK implementation invents its own serialization, creating cross-implementation incompatibility and introducing security risks (accidental serialization of decrypted graph data or retained decryption key copies) |
| **`SharedWorkerSessionAdapter` promoted to RECOMMENDED for Level 2 browser implementations** | §6.5.3, §17.1 | Promoting | v1.1.0 marked this MAY; in practice it is required for safe multi-tab access; application developers must not be expected to write bespoke RPC wrappers over a cryptographic session boundary |
| **Decryption key transfer via Transferable `ArrayBuffer` made normative** | §6.6.3 | Additive — Normative | Sending the decryption key as a postMessage copy leaves a retained copy in the tab heap; ownership transfer via Transferable detaches the tab's buffer, ensuring the key exists only in the worker after session open |
| **`WORKER_SERIALIZATION_ERROR` added to error registry** | §15.1 | Additive | Covers attempts to pass prohibited objects (SessionGraph, decrypted bytes, QuerySession) across the postMessage boundary |
| **Test vector A.11 added** | Appendix A | Additive | Covers the full Worker RPC round-trip including key transfer, query execution, and session expiry push notification |

---

## v1.1.0 Revision Notes (from v1.0.0)

This revision addresses four implementation edge cases identified in adversarial review of v1.0.0, all arising from the realities of WASM execution and browser runtime environments. No prior normative semantics are removed. All changes are additive or clarifying.

| Change | Section | Nature | Reason |
|--------|---------|--------|--------|
| **`MemoryBudget` model introduced; `maxMemoryBytes` measurement point defined** | §6.4.1, §6.4.5 | Additive | WASM heap size is not directly observable from the host JS environment; `maxMemoryBytes` required a precise measurement point to be implementable |
| **Session concurrency model defined** | §6.5 | Additive | v1.0.0 prohibited "opening multiple sessions against the same manifest simultaneously" without distinguishing in-process duplication (prohibited) from independent UI contexts such as browser tabs (permitted); SharedWorker pattern added as RECOMMENDED architecture |
| **Sleep/wake TTL enforcement defined** | §6.4.6 | Additive | Monotonic clocks pause during device sleep in browser environments; wall-clock cross-check on resume is required to prevent session TTL from freezing |
| **Default graph behavior for Mode 3 made explicit** | §9.6 | Additive | Mode 3 N-Quads load exclusively into named graphs, leaving the default graph empty; a QDL document without `hql:source` silently returns no results, which requires explicit documentation and a compiler warning |
| **Test vectors A.9, A.10 added** | Appendix A | Additive | Cover default graph empty behavior and independent tab session concurrency |
| **`SESSION_DEFAULT_GRAPH_QUERY` warning added to error registry** | §15.1 | Additive | Non-fatal warning for QDL documents that query the default graph during Mode 3 execution |

---

## Table of Contents

1. [Purpose](#1-purpose)
2. [Normative References](#2-normative-references)
3. [Terminology](#3-terminology)
4. [Architectural Position](#4-architectural-position)
5. [Core Principles](#5-core-principles)
6. [Execution Substrate](#6-execution-substrate)
   - [6.6 Worker Message Protocol](#66-worker-message-protocol)
7. [Projection Model (PDL)](#7-projection-model-pdl)
8. [Query Model (QDL)](#8-query-model-qdl)
9. [Privacy-Aware Query Semantics](#9-privacy-aware-query-semantics)
10. [Index Model](#10-index-model)
11. [Execution Lifecycle](#11-execution-lifecycle)
12. [Result Model](#12-result-model)
13. [Caching](#13-caching)
14. [Offline Behavior](#14-offline-behavior)
15. [Error Handling](#15-error-handling)
16. [Security Considerations](#16-security-considerations)
17. [Conformance](#17-conformance)
18. [Future Extensions](#18-future-extensions)

**Appendices**

- [A: Normative Test Vectors](#appendix-a-normative-test-vectors)
- [B: PDL-to-SPARQL Compilation Examples](#appendix-b-pdl-to-sparql-compilation-examples)
- [C: Privacy Mode Query Behavior Reference](#appendix-c-privacy-mode-query-behavior-reference)

---

## 1. Purpose

This specification defines a **deterministic, edge-canonical query layer** for systems using HIRI over IPFS. It provides:

- A standard compilation layer from JSON-LD-native query documents to SPARQL
- A privacy-aware result model that reflects HIRI Privacy Extension v1.4.1 content status
- A deterministic projection model over HIRI-verified RDF graphs
- A `QuerySession` primitive for efficient multi-query access to privacy-restricted content
- A portable, edge-executable query interface

This specification does NOT:

- Define canonical storage — HIRI does this
- Define the query execution engine — HIRI §15 does this (Oxigraph WASM)
- Require infrastructure (databases, servers, etc.)
- Introduce non-deterministic execution
- Reimplement graph pattern matching — SPARQL 1.1 semantics govern this

---

## 2. Normative References

| Specification | Usage |
|---------------|-------|
| HIRI Protocol Specification v3.1.1 | Base protocol, execution substrate (§15) |
| HIRI Privacy & Confidentiality Extension v1.4.1 | Privacy mode semantics |
| W3C SPARQL 1.1 Query Language | Execution language for QDL compilation targets |
| W3C SPARQL 1.1 Update | Projection materialization |
| W3C RDF 1.1 N-Quads | Wire format for Mode 3 disclosed statement loading |
| W3C RDF Dataset Canonicalization | URDNA2015 (via HIRI §7.2) |
| RFC 8785 | JCS (via HIRI §7.1) |
| Oxigraph WASM | RECOMMENDED execution engine (via HIRI §15.3) |
| W3C Page Visibility API | RECOMMENDED for browser session lifecycle management (§6.4.6) |

---

## 3. Terminology

| Term | Definition |
|------|------------|
| HQL | HIRI Query Layer — this specification |
| PDL | Projection Definition Language — a JSON-LD-native format that compiles to SPARQL CONSTRUCT queries |
| QDL | Query Definition Language — a JSON-LD-native format that compiles to SPARQL SELECT queries |
| Projection | A pure function from a verified RDF graph to a derived RDF graph, executed as a SPARQL CONSTRUCT query |
| Query | A pure function from a derived RDF graph and indexes to a result set, executed as a SPARQL SELECT query |
| ProjectionDocument | A JSON-LD document conforming to the PDL schema that describes a projection declaratively |
| QueryDocument | A JSON-LD document conforming to the QDL schema that describes a query declaratively |
| Compiled Query | The SPARQL string produced by compiling a ProjectionDocument or QueryDocument |
| Projection State | The derived RDF graph produced by executing a Projection against canonical inputs |
| Index | A materialized structure derived from Projection State that accelerates query execution |
| Execution Substrate | The RDF index and SPARQL engine defined in HIRI Protocol v3.1.1 §15 |
| ContentStatus | The privacy-aware availability state of the content backing a query result |
| LogicalPlaintextHash | As defined in HIRI Privacy Extension v1.4.1 §11.3 |
| QuerySession | A bounded scope within which a decrypted Mode 2 RDF graph is held in volatile memory and made available for repeated queries |
| SessionGraph | The in-memory RDF index held by an active QuerySession |
| Document Graph Name | The HIRI content hash URI used as the named graph identifier when loading Mode 3 N-Quads from a specific manifest into a shared Oxigraph dataset |
| SharedWorkerSessionAdapter | A conformant implementation of the Worker Message Protocol (§6.6) that wraps a QuerySession held in a SharedWorker and exposes it to UI tabs via defined postMessage RPC messages |
| WorkerRequest | A structured message sent from a UI tab to the SharedWorker, identifying a requested operation by `type` and a correlation `requestId` |
| WorkerResponse | A structured message sent from the SharedWorker to a UI tab in reply to a WorkerRequest, carrying the same `requestId` for correlation |
| WorkerPush | An unsolicited structured message sent from the SharedWorker to all connected UI tabs, used for session lifecycle events not tied to a specific request |
| Transferable Decryption Key | The decryption key `ArrayBuffer` sent from a UI tab to the SharedWorker via `postMessage` as a Transferable object; after transfer the tab's buffer is detached and the key exists only in the worker heap |

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" are interpreted per RFC 2119.

---

## 4. Architectural Position

### 4.1 Stack

```text
[ HIRI / IPFS (Canonical State) ]
              ↓
[ HIRI §15: Verified JSON-LD → N-Quads → RDF Index (Oxigraph WASM) ]
              ↓
[ HQL Projection Layer (PDL → SPARQL CONSTRUCT) ]     ← THIS SPEC
              ↓
[ HQL Query Layer (QDL → SPARQL SELECT) ]             ← THIS SPEC
              ↓
[ Application Logic ]
```

### 4.2 Relationship to HIRI §15

HQL operates exclusively **above** the execution substrate defined in HIRI Protocol v3.1.1 §15. That section normatively defines:

- The `buildGraph` function that loads verified JSON-LD into an in-memory RDF index
- The `executeQuery` function that runs SPARQL against that index
- The entailment modes (`none`, `materialized`, `runtime`) and their enforcement
- The RECOMMENDED engine: **Oxigraph WASM**

**HQL implementations MUST use the HIRI §15 execution substrate.** An HQL implementation MUST NOT:

- Substitute a different SPARQL engine without declaring it as a non-conformant extension
- Bypass `buildGraph` and build its own graph from raw JSON-LD
- Execute PDL or QDL documents directly as pattern matchers — they MUST first be compiled to SPARQL

This constraint is normative. Its purpose is to ensure that the security guarantees in HIRI §15 — particularly entailment mode enforcement and the secure document loader — are not silently violated by the query layer.

### 4.3 Relationship to HIRI Privacy Extension v1.4.1

All five privacy modes defined in the Privacy Extension alter what content is available to the query layer. HQL MUST reflect the `contentStatus` of every query result and MUST NOT suppress, flatten, or re-interpret privacy signals from the HIRI resolution layer. See §9 for full semantics.

### 4.4 Separation of Concerns

| Layer | Responsibility |
|-------|----------------|
| HIRI Protocol | Canonical state, signing, verification, chain integrity |
| HIRI §15 | RDF graph construction, SPARQL execution, entailment control |
| HQL PDL | JSON-LD-native projection authoring, compiled to SPARQL CONSTRUCT |
| HQL QDL | JSON-LD-native query authoring, compiled to SPARQL SELECT |
| HQL QuerySession | Bounded volatile scope for multi-query access to decrypted content |
| Application | Business logic, privacy policy, trust decisions |

---

## 5. Core Principles

### 5.1 Derived State Only

All queryable state MUST be derived from canonical HIRI content via the HIRI §15 `buildGraph` pipeline. No queryable structure is authoritative. HQL does not hold canonical state — it derives queryable state from it.

### 5.2 Deterministic Compilation

Given identical canonical inputs, identical ProjectionDocument, and identical entailment mode, the compiled SPARQL MUST be syntactically identical, and the SPARQL execution MUST produce logically identical results across environments.

### 5.3 Local Execution

All compilation and query execution MUST be possible in a browser tab or Node.js runtime with no external services required, by inheritance from HIRI §4.1 (Edge-Canonical First).

### 5.4 Disposability

Implementations MUST treat all projection state and indexes as rebuildable. Loss of HQL-derived state MUST NOT result in data loss. QuerySession graphs are explicitly volatile — their loss requires the caller to open a new session, but no canonical data is lost.

### 5.5 Entailment Passthrough and Privacy-Mode Override

HQL MUST pass the caller-declared entailment mode to the HIRI §15 `buildGraph` call without modification **except** where a privacy mode mandates a restriction (see §9.2, Mode 3). HQL MUST NOT silently upgrade or downgrade the entailment mode.

**Why `allowInferenceLeakage` is architecturally incorrect for Mode 3 content:**

The Privacy Extension v1.4.1 §4.1 establishes that "all confidentiality guarantees derive from cryptographic operations performed before publication." Selective disclosure (Mode 3) is a publisher assertion: the publisher determined, before signing, which statements to withhold. The querier is a consumer of that signed contract — they did not create it and cannot revise it unilaterally.

An `allowInferenceLeakage` flag would transfer the publisher's disclosure authority to the querier. This violates the Privacy Extension's architectural invariant that the network layer is not relied upon for confidentiality and that the protocol layer does not prescribe application-layer trust decisions (Privacy Extension §13.6). The correct response to "I want to run inference over disclosed statements" is: obtain the full disclosed set from the publisher through an authorized disclosure channel, then build a local graph from that — not ask the query layer to derive statements the publisher has not authorized.

The hard rejection (`ENTAILMENT_RESTRICTED_BY_PRIVACY_MODE`) is therefore not paternalism toward the application layer. It is the query layer enforcing the publisher's cryptographic intent, which no application-layer flag can legitimately override.

### 5.6 Privacy Signal Preservation

HQL MUST NOT collapse, suppress, or re-interpret the `contentStatus` returned by the HIRI Privacy Extension resolution layer. A partial disclosure result is not the same as a missing-CID result — the distinction is security-relevant to the caller.

---

## 6. Execution Substrate

### 6.1 Engine

The normative execution substrate is defined by HIRI Protocol v3.1.1 §15:

```typescript
// HIRI §15.1
async function buildGraph(
  content: Uint8Array,
  format: string,
  baseURI: string,
  config: { entailmentMode: EntailmentMode },
  indexFactory: () => RDFIndex
): Promise<RDFIndex>

// HIRI §15.3
async function executeQuery(
  sparql: string,
  index: RDFIndex,
  engine: SPARQLEngine
): Promise<QueryResult>
```

The RECOMMENDED `SPARQLEngine` is Oxigraph WASM.

### 6.2 JSON-LD Loading

For content in `application/ld+json` format (the standard HIRI content type), HIRI §15.4 defines the loading pipeline:

1. Parse content bytes as JSON
2. Convert to N-Quads via `jsonld.toRDF()` using the secure document loader
3. Load N-Quads into the RDF index

**HQL MUST NOT bypass this pipeline.** In particular:
- HQL MUST NOT load JSON-LD objects directly into a document store as a substitute for the N-Quads RDF index
- HQL MUST use the secure document loader (HIRI §7.5) that blocks remote context fetches

### 6.3 Entailment Modes

HQL supports the three entailment modes defined in HIRI §15.2:

| Mode | Behavior | HQL Status |
|------|----------|------------|
| `none` | No inference. Only asserted triples returned. | REQUIRED |
| `materialized` | Pre-computed inference triples added at load time. | OPTIONAL |
| `runtime` | Inference applied at query time. | OPTIONAL |

HQL implementations MUST default to `mode: "none"` when the caller does not specify an entailment mode. Implementations that do not support `materialized` or `runtime` MUST throw `UNSUPPORTED_ENTAILMENT_MODE` rather than silently falling back to `none`.

### 6.4 QuerySession

A **QuerySession** is a bounded, volatile scope within which a decrypted Mode 2 RDF graph is held in memory and made available for repeated queries without reconstruction. It is the primary mechanism for interactive UI scenarios involving encrypted private content (sorting, filtering, paginating a personal dataset).

#### 6.4.1 Session Lifecycle Interface

```typescript
interface QuerySession {
  readonly sessionId: string           // Opaque, random, non-persistent identifier
  readonly manifestHash: string        // Content hash of the manifest that opened this session
  readonly contentStatus: ContentStatus
  readonly openedAt: number            // Injected monotonic timestamp at session open
  readonly openedAtWallClock: number   // Injected wall-clock timestamp at session open (§6.4.6)
  readonly expiresAt: number           // openedAt + options.ttl (monotonic domain)

  query(queryDocument: QueryDocument): Promise<QueryResult>
  close(): void
  readonly active: boolean
}

async function openQuerySession(
  manifest: ResolutionManifest,
  decryptionKey: Uint8Array,
  recipientId: string,
  options: QuerySessionOptions
): Promise<QuerySession>

interface QuerySessionOptions {
  ttl: number                    // Session lifetime in milliseconds; MUST be specified by caller
  entailmentMode?: EntailmentMode  // Defaults to "none"
  memoryBudget?: MemoryBudget    // See §6.4.5; SHOULD be specified
}
```

#### 6.4.2 Session Invariants

1. **One graph build per session.** `buildGraph` is called exactly once when the session is opened. All subsequent `session.query()` calls execute against the same `SessionGraph` in memory.

2. **Volatile-only.** The `SessionGraph` MUST NOT be persisted to disk, IndexedDB, localStorage, or any durable storage. It MUST reside only in the runtime heap.

3. **Automatic expiry.** A session MUST automatically close when expiry is reached per the rules in §6.4.6. If a query is in progress when the session expires, it MUST complete with the already-loaded graph and the session MUST close immediately after. Subsequent `session.query()` calls MUST throw `SESSION_EXPIRED`.

4. **Memory pressure close.** If a session's pre-load byte check or WASM page soft limit is exceeded per §6.4.5, the session MUST close and all decrypted data MUST be zeroed. The caller MUST receive `SESSION_MEMORY_EXCEEDED`.

5. **Explicit close zeroes the graph.** When `session.close()` is called, or when the session closes for any reason, the implementation MUST zero out the decrypted byte arrays and release the `SessionGraph`. This is a MUST — the zeroing is the security property that bounds the lifetime of decrypted content to the authorized session scope.

6. **Non-transferable.** A `QuerySession` MUST NOT be serialized, cloned, or passed across process boundaries. `sessionId` is opaque and MUST NOT be usable to reconstruct the session from outside the UI context (§3) that created it.

#### 6.4.3 Session Use for Interactive UI

A QuerySession is the correct primitive for UI scenarios where a user is browsing, sorting, filtering, or paginating their own encrypted private data. The recommended pattern is:

```typescript
// Open a session when the user navigates to their private data view
const session = await openQuerySession(manifest, decryptionKey, recipientId, {
  ttl: 15 * 60 * 1000,  // 15-minute session matching a typical idle timeout
  memoryBudget: {
    maxInputBytes: 10 * 1024 * 1024,  // Reject if N-Quads exceed 10 MB before WASM load
    maxWasmPages: 200                 // Soft limit: ~12.8 MB of WASM heap growth
  }
});

// All queries in this UI view execute against the same SessionGraph
const people   = await session.query(listPeopleQuery);
const filtered = await session.query(filterByNameQuery);
const page2    = await session.query(paginatedQuery);

// Close explicitly when the user navigates away
session.close();
// Or let TTL expiry close it automatically
```

#### 6.4.4 Session Prohibition: Intentional In-Process Duplication

The following are prohibited within a single UI context (a single browser tab, worker, or Node.js process):

- Opening more than one active session against the same manifest simultaneously
- Re-opening a closed session by reusing a prior `sessionId`
- Opening a session solely to pre-warm a graph cache for future accesses

These prohibitions target **intentional programmatic parallelization** within a single runtime. They do not govern independent UI contexts. See §6.5 for the concurrency model across contexts.

#### 6.4.5 `MemoryBudget` and WASM Measurement Model

WASM heap memory is allocated in coarse pages of 64 KB and is not directly introspectable from the host JavaScript environment in a way that permits precise per-object accounting. The `MemoryBudget` model therefore defines two distinct measurement points: one that is always precise and one that is an optional heuristic.

```typescript
interface MemoryBudget {
  // REQUIRED: Hard limit on the raw decrypted N-Quads byte array BEFORE it is
  // passed to buildGraph. This is measured in the host environment, where the
  // byte array is directly accessible. If the decrypted content exceeds this
  // limit, the session MUST NOT call buildGraph; it MUST throw
  // SESSION_MEMORY_EXCEEDED and zero the decrypted bytes immediately.
  maxInputBytes: number

  // OPTIONAL: Soft limit on WASM memory page growth observed during buildGraph.
  // One WASM page = 65,536 bytes (64 KB). If the implementation can observe
  // WebAssembly.Memory.buffer.byteLength before and after buildGraph, and the
  // delta in pages exceeds this value, the session SHOULD close and zero.
  // If the implementation cannot observe WASM page count, this field is ignored.
  // This is a SHOULD, not a MUST, because WASM page observability is
  // platform-dependent. Implementations MUST document whether they enforce it.
  maxWasmPages?: number
}
```

**Measurement semantics:**

```
Step 1: Decrypt content bytes → decryptedBytes: Uint8Array

Step 2: Check hard limit
  if decryptedBytes.byteLength > memoryBudget.maxInputBytes:
    zero(decryptedBytes)
    throw SESSION_MEMORY_EXCEEDED
    // buildGraph is NEVER called

Step 3: Observe pre-load WASM pages (if maxWasmPages is set)
  pagesBefore = wasmMemory?.buffer.byteLength / 65536 ?? null

Step 4: Call buildGraph(decryptedBytes, ...)

Step 5: Observe post-load WASM pages (if maxWasmPages is set and pagesBefore was observed)
  pagesAfter = wasmMemory?.buffer.byteLength / 65536 ?? null
  if pagesAfter !== null && (pagesAfter - pagesBefore) > memoryBudget.maxWasmPages:
    session.close()  // triggers zeroing per §6.4.2 invariant 5
    throw SESSION_MEMORY_EXCEEDED
```

**Why this division:** The `maxInputBytes` check is the primary, always-enforceable limit. An application that has content regularly exceeding this limit should increase the budget or redesign the content model — the limit provides a fail-safe against unexpectedly large encrypted payloads that would exhaust WASM heap. The `maxWasmPages` check is a secondary heuristic for applications with tight memory envelopes (e.g., mobile browsers). Oxigraph's internal structures may expand the input data by a factor of 3–10x after indexing; a page-growth delta check catches this expansion even when the raw bytes appeared within budget.

**Recommended defaults** (INFORMATIVE):

| Context | `maxInputBytes` | `maxWasmPages` |
|---------|-----------------|----------------|
| Desktop browser | 50 MB | 1000 (~64 MB heap growth) |
| Mobile browser | 10 MB | 200 (~12.8 MB heap growth) |
| Node.js server | 200 MB | Not set (Node has no WASM page limit) |
| Edge/WASM serverless | 5 MB | 80 (~5.1 MB heap growth) |

These defaults are INFORMATIVE. Callers MUST set values appropriate to their deployment context.

#### 6.4.6 TTL Enforcement: Sleep/Wake and Monotonic Clock Freeze

Browser monotonic clocks (e.g., `performance.now()`) may pause or advance slowly during device sleep, tab backgrounding, or OS power management. A session whose TTL appears unexpired under the monotonic clock may have exceeded its intended wall-clock lifetime if the device was suspended.

**Dual-timestamp requirement:**

Sessions MUST record both a monotonic timestamp (`openedAt`) and a wall-clock timestamp (`openedAtWallClock`) at session open time. Both are injected parameters — the kernel does not call system clock APIs directly (inherited from HIRI §16.3):

```typescript
interface TimestampProvider {
  monotonicNow(): number    // e.g., performance.now() in browsers
  wallClockNow(): number    // e.g., Date.now()
}
```

**Expiry check algorithm (MUST be applied before every `session.query()` call):**

```
monotonicElapsed = monotonicNow() - session.openedAt
wallClockElapsed = wallClockNow() - session.openedAtWallClock

if monotonicElapsed >= ttl OR wallClockElapsed >= ttl:
  session.close()  // zeros SessionGraph
  throw SESSION_EXPIRED
```

Either condition independently triggers expiry. If the monotonic clock froze during sleep (monotonicElapsed appears small) but the wall clock advanced past the TTL, the wall-clock condition triggers expiry. This prevents a sleeping device from indefinitely extending the lifetime of a decrypted session graph.

**Page Visibility API integration (RECOMMENDED for browser implementations):**

Implementations running in a browser environment SHOULD register a Page Visibility listener at session open:

```javascript
function onVisibilityChange() {
  if (document.visibilityState === 'hidden') {
    // Tab is backgrounded, device screen off, or tab is being closed.
    // Close the session immediately to prevent the decrypted graph
    // from persisting in memory during an uncertain suspension period.
    session.close()
  }
}
document.addEventListener('visibilitychange', onVisibilityChange)

// Remove listener on explicit close to avoid double-close
session.addEventListener('close', () => {
  document.removeEventListener('visibilitychange', onVisibilityChange)
})
```

This behavior is RECOMMENDED, not REQUIRED, because:
- Some applications legitimately need a session to survive brief tab-switching (e.g., a user copying a value from another tab)
- The TTL mechanism provides the backstop guarantee even if the visibility listener is not registered

Applications that handle regulated or classified content SHOULD treat visibility-hidden as a mandatory close trigger and SHOULD set short TTLs (≤ 5 minutes).

**On device wake/resume:** Implementations MUST run the dual-timestamp expiry check immediately upon any event that indicates the device or tab has resumed (e.g., `visibilitychange → visible`, `focus`, `pageshow`). If the wall-clock elapsed time exceeds the TTL, the session MUST close before servicing any pending or new queries.

---

### 6.5 Session Concurrency Model

#### 6.5.1 The Prohibition Defined Precisely

Section §6.4.4 prohibits opening multiple sessions against the same manifest **within a single UI context** (a single browser tab, web worker, or Node.js process). This prohibition targets intentional in-process duplication — using multiple simultaneous sessions as a parallelization mechanism or as a performance optimization.

It does NOT prohibit:

- A user opening two browser tabs to view the same private content
- A desktop application launching two process instances
- A test harness opening sequential sessions against the same manifest

Each of these involves independent, isolated UI contexts. They are not covered by the prohibition.

#### 6.5.2 Independent UI Contexts Are Permitted

A **UI context** (§3) is an isolated runtime environment with its own heap. Separate browser tabs, separate workers, and separate processes each constitute distinct UI contexts. Each context holds its own independent session state that is not shared with other contexts.

**When a user opens two browser tabs to the same private document:**

- Tab A opens `SessionA` against manifest `sha256:abc123`
- Tab B opens `SessionB` against manifest `sha256:abc123`
- `SessionA` and `SessionB` are independent — they have separate heaps, separate `sessionId` values, separate TTLs
- Both are permitted. Each represents an independent authorized access event.
- Closing Tab A closes `SessionA` and zeros its graph; Tab B's session is unaffected.

This is the correct behavior. The per-context session limit prevents a single piece of code from creating redundant graph copies in one runtime; it does not prevent a user from having two open views of their own content.

#### 6.5.3 SharedWorkerSessionAdapter (RECOMMENDED for Level 2 Browser Implementations)

When an application needs multiple tabs to share a single SessionGraph, the RECOMMENDED architecture is a **SharedWorker** holding the session, with UI tabs communicating via the Worker Message Protocol defined in §6.6.

```
Tab A ──WorkerRequest──┐
Tab B ──WorkerRequest──┤──► SharedWorker (holds ONE QuerySession) ──► Oxigraph WASM
Tab C ──WorkerRequest──┘
         ▲
         └── WorkerResponse / WorkerPush
```

**Properties of this architecture:**

- One decryption per content load, regardless of how many tabs are open
- Session TTL is enforced at the worker level, independent of any individual tab's lifecycle
- The non-transferable invariant (§6.4.2) is preserved — the `QuerySession` object never crosses the worker boundary; only serialized `QueryResult` objects do
- The decryption key is transferred as a Transferable `ArrayBuffer` (§6.6.3), detaching it from the tab immediately after the session-open request

**Why RECOMMENDED rather than OPTIONAL:**

Application developers MUST NOT be expected to write bespoke postMessage RPC wrappers over a cryptographic session boundary. Custom serialization at this layer introduces exactly the class of security errors the specification is designed to prevent — most critically, accidental serialization of decrypted content or retention of a key copy in the tab. A conformant `SharedWorkerSessionAdapter` implementing the Worker Message Protocol (§6.6) is the safe path. Implementations targeting browser environments at Level 2 conformance SHOULD provide one.

The Worker Message Protocol (§6.6) is normative. Implementations providing a `SharedWorkerSessionAdapter` MUST conform to it.

#### 6.5.4 Session Count Enforcement

Implementations MUST track the count of active sessions per manifest CID within each UI context. If a second `openQuerySession()` call is made within the same UI context against a manifest that already has an active session, the implementation MUST throw `DUPLICATE_SESSION_IN_CONTEXT`.

This enforcement does not apply across UI context boundaries — a SharedWorker and its parent tab are separate contexts, and a tab that opens a session after the SharedWorker already holds one is not a violation.

---

### 6.6 Worker Message Protocol

This section is NORMATIVE. It defines the wire format for communication between UI tabs and a SharedWorker holding a `QuerySession`. Implementations providing a `SharedWorkerSessionAdapter` MUST conform to this protocol. Implementations that deviate from this protocol MUST NOT claim conformance even if their behavior is functionally equivalent.

#### 6.6.1 Design Principles

The Worker Message Protocol is governed by three constraints that follow directly from the security requirements of the surrounding specification:

1. **Nothing sensitive crosses the boundary as a copy.** The decryption key is a Transferable — ownership moves to the worker, the tab's buffer is detached. No decrypted graph data, no `SessionGraph`, no `QuerySession` object, and no compiled SPARQL string ever appears in a postMessage payload.

2. **All messages are plain JSON or Transferable `ArrayBuffer`.** Complex JavaScript objects, class instances, `Error` objects, and `Uint8Array` views MUST NOT be sent via postMessage. Error conditions are communicated as string error codes. This ensures that a misconfigured `structuredClone` or postMessage environment cannot accidentally serialize prohibited data.

3. **Requests and responses are correlated by `requestId`.** A tab may have multiple concurrent outstanding requests. The worker echoes the caller-supplied `requestId` in every response. Push notifications (unsolicited events from the worker) carry no `requestId`.

#### 6.6.2 Message Type Registry

**WorkerRequest** (tab → worker):

```typescript
type WorkerRequest =
  | WorkerInitRequest
  | WorkerSessionOpenRequest
  | WorkerSessionQueryRequest
  | WorkerSessionCloseRequest

interface WorkerInitRequest {
  type: "worker.init"
  requestId: string       // UUID v4, caller-generated
  config: WorkerConfig
}

interface WorkerConfig {
  // HIRI resolution options passed to the worker's internal resolver
  // Contents are implementation-defined; no sensitive material.
  resolverOptions?: object
}

interface WorkerSessionOpenRequest {
  type: "session.open"
  requestId: string
  manifestUri: string      // HIRI URI of the manifest to resolve and verify
  recipientId: string      // Plain string; no sensitive material
  options: WorkerSessionOptions
  // NOTE: decryptionKey is NOT in this interface.
  // It is sent as a Transferable in the postMessage transfer list. See §6.6.3.
}

interface WorkerSessionOptions {
  ttl: number
  entailmentMode?: "none" | "materialized" | "runtime"
  memoryBudget?: {
    maxInputBytes: number
    maxWasmPages?: number
  }
}

interface WorkerSessionQueryRequest {
  type: "session.query"
  requestId: string
  sessionId: string        // sessionId returned by a prior session.open.ok response
  queryDocument: object    // Serialized QDL document (JSON-LD object; safe to clone)
}

interface WorkerSessionCloseRequest {
  type: "session.close"
  requestId: string
  sessionId: string
}
```

**WorkerResponse** (worker → tab, in reply to a WorkerRequest):

```typescript
type WorkerResponse =
  | WorkerInitResponse
  | WorkerSessionOpenOkResponse
  | WorkerSessionOpenErrorResponse
  | WorkerSessionQueryOkResponse
  | WorkerSessionQueryErrorResponse
  | WorkerSessionCloseOkResponse

interface WorkerInitResponse {
  type: "worker.init.ok" | "worker.init.error"
  requestId: string
  error?: string            // Error code string if type is "worker.init.error"
}

interface WorkerSessionOpenOkResponse {
  type: "session.open.ok"
  requestId: string
  sessionId: string         // Opaque identifier; worker-generated
  contentStatus: string     // ContentStatus string value
}

interface WorkerSessionOpenErrorResponse {
  type: "session.open.error"
  requestId: string
  error: string             // Error code from §15.1 registry, e.g. "SESSION_MEMORY_EXCEEDED"
  message?: string          // Optional human-readable detail; MUST NOT contain key material
}

interface WorkerSessionQueryOkResponse {
  type: "session.query.ok"
  requestId: string
  result: SerializedQueryResult
}

interface WorkerSessionQueryErrorResponse {
  type: "session.query.error"
  requestId: string
  error: string             // Error code, e.g. "SESSION_EXPIRED", "COMPILATION_ERROR"
  message?: string
}

interface WorkerSessionCloseOkResponse {
  type: "session.close.ok"
  requestId: string
}
```

**WorkerPush** (worker → all connected tabs, unsolicited):

```typescript
type WorkerPush =
  | WorkerSessionExpiredPush
  | WorkerSessionMemoryExceededPush

interface WorkerSessionExpiredPush {
  type: "session.expired"
  sessionId: string
  // No requestId — this is a push event, not a response to a request
}

interface WorkerSessionMemoryExceededPush {
  type: "session.memory.exceeded"
  sessionId: string
}
```

#### 6.6.3 Decryption Key Transfer

The decryption key MUST be transmitted from the tab to the worker as a Transferable `ArrayBuffer`. It MUST NOT be sent as a copied value (i.e., it MUST appear in the transfer list of the `postMessage` call, not only in the message body).

```javascript
// Tab side — normative send pattern
async function openWorkerSession(worker, manifestUri, decryptionKey, recipientId, options) {
  const requestId = crypto.randomUUID()

  // The decryptionKey ArrayBuffer is listed in the transfer array.
  // After this call, decryptionKey.byteLength === 0 in the tab.
  // The key exists only in the worker heap.
  worker.port.postMessage(
    {
      type: "session.open",
      requestId,
      manifestUri,
      recipientId,
      options,
      // decryptionKey is deliberately absent from the message body.
      // It is transferred separately via the transfer list below.
    },
    [decryptionKey]   // ← Transferable; tab buffer detached after this line
  )

  return new Promise((resolve, reject) => {
    // ... correlation logic awaiting session.open.ok or session.open.error
  })
}
```

```javascript
// Worker side — normative receive pattern
self.addEventListener("connect", (connectEvent) => {
  const port = connectEvent.ports[0]
  port.addEventListener("message", async (event) => {
    if (event.data.type === "session.open") {
      // The transferred ArrayBuffer arrives in event.ports or as a transferred
      // buffer. Implementations MUST retrieve it from the transfer list, not
      // attempt to reconstruct it from the message body.
      const decryptionKeyBuffer = event.data._transferredKey  // convention; see note
      const decryptionKey = new Uint8Array(decryptionKeyBuffer)

      // Use decryptionKey to open a QuerySession (§6.4)
      // ...

      // Zero the key bytes after buildGraph completes (§16.5)
      decryptionKey.fill(0)
    }
  })
  port.start()
})
```

**Implementation note on the transfer convention:** The Web Workers API does not attach transferred `ArrayBuffer` objects to a named property in the message body automatically. The sender MUST include the `ArrayBuffer` in the `postMessage` transfer list, and MUST also include a reference to it in the message body under a defined property name so the receiver can access it. The property name `_transferredKey` is the normative convention for this specification. Implementations MUST use this name for interoperability.

**Zeroing obligation:** The worker MUST zero the decryption key bytes (`.fill(0)`) immediately after `buildGraph` has consumed them, consistent with the lifecycle requirements of §16.5. The key is not retained for the session duration — only the built `SessionGraph` persists.

#### 6.6.4 SerializedQueryResult

`QueryResult` objects (§12.1) MUST be serialized as plain JSON before crossing the postMessage boundary. The `SerializedQueryResult` type is structurally identical to `QueryResult` — all fields use JSON-primitive types and are safe for `structuredClone`.

```typescript
interface SerializedQueryResult {
  results: SerializedBinding[]
  complete: boolean
  completenessReason?: string        // CompletionReason string value
  contentStatus: string             // ContentStatus string value
  identityType?: string
  warnings: string[]
}

interface SerializedBinding {
  [variableName: string]: SerializedRDFTerm
}

interface SerializedRDFTerm {
  type: "uri" | "literal" | "blank"
  value: string
  datatype?: string
  language?: string
}
```

This type is identical in shape to `QueryResult` / `Binding` / `RDFTerm` from §12.1. The separate definition exists to make the serialization contract explicit: a receiver MUST be able to reconstruct the full `QueryResult` from a `SerializedQueryResult` by direct field mapping with no additional decoding steps.

#### 6.6.5 Prohibited Payloads

The following MUST NOT appear in any `WorkerRequest`, `WorkerResponse`, or `WorkerPush` message body:

| Prohibited Object | Reason |
|---|---|
| `QuerySession` instance | Non-transferable; contains live graph reference |
| `RDFIndex` / `SessionGraph` | Contains decrypted graph data; MUST remain in worker heap |
| Decrypted `Uint8Array` or `ArrayBuffer` other than the key during `session.open` | Exposes plaintext content to tab heap |
| Compiled SPARQL string | Intermediate artifact; no cross-boundary utility |
| JavaScript `Error` object | Not reliably serializable; error codes MUST be used instead |
| `CryptoKey` (WebCrypto) | Key material; MUST remain in worker |

An implementation that detects an attempt to include any of the above in a message payload MUST throw `WORKER_SERIALIZATION_ERROR` and MUST NOT dispatch the message.

#### 6.6.6 Worker Lifecycle and Tab Disconnect

The SharedWorker MUST track connected tab count via `connect` and port close events:

```javascript
let connectedPorts = new Set()

self.addEventListener("connect", (event) => {
  const port = event.ports[0]
  connectedPorts.add(port)

  port.addEventListener("close", () => {
    connectedPorts.delete(port)
    if (connectedPorts.size === 0) {
      // All tabs disconnected — close all active sessions
      closeAllSessions()
    }
  })
  port.start()
})
```

When the last connected tab disconnects, all active `QuerySession` instances held by the worker MUST be closed and their `SessionGraph` instances zeroed (§6.4.2 invariant 5). This prevents a detached SharedWorker from holding decrypted graphs after all authorized UI contexts have closed.

#### 6.6.7 Push Notification Delivery

`WorkerPush` messages (session expiry, memory exceeded) MUST be broadcast to all currently connected ports:

```javascript
function broadcastPush(push) {
  for (const port of connectedPorts) {
    port.postMessage(push)
  }
}
```

Tabs MUST handle `WorkerPush` messages regardless of whether they have a pending request outstanding. A tab that receives `session.expired` or `session.memory.exceeded` SHOULD surface the appropriate UX to the user (e.g., a "session expired — please re-authenticate" prompt).

#### 6.6.8 SharedWorkerSessionAdapter Interface

Implementations providing a `SharedWorkerSessionAdapter` MUST expose the following interface. This is the type-safe surface that application code interacts with; the Worker Message Protocol (§6.6.2–§6.6.7) is the underlying wire format.

```typescript
interface SharedWorkerSessionAdapter {
  // Open a session in the SharedWorker.
  // decryptionKey is an ArrayBuffer; after this call returns, the caller's
  // buffer is detached (byteLength === 0). This is the expected behavior.
  open(
    manifestUri: string,
    decryptionKey: ArrayBuffer,   // Transferred; caller's reference is detached
    recipientId: string,
    options: WorkerSessionOptions
  ): Promise<string>              // Resolves to sessionId

  // Execute a QDL query against an open session.
  query(
    sessionId: string,
    queryDocument: object
  ): Promise<SerializedQueryResult>

  // Explicitly close a session.
  close(sessionId: string): Promise<void>

  // Register a callback for session expiry push events.
  onSessionExpired(callback: (sessionId: string) => void): void

  // Register a callback for session memory-exceeded push events.
  onSessionMemoryExceeded(callback: (sessionId: string) => void): void

  // Terminate the SharedWorker and close all sessions.
  terminate(): void
}
```

**Caller contract for `open()`:** The caller MUST NOT use the `decryptionKey` `ArrayBuffer` after calling `open()`. The buffer will be detached and any attempt to read it will produce a `TypeError`. Callers SHOULD explicitly set the reference to `null` after the call to prevent accidental access:

```typescript
const key = await getDecryptionKey()
const sessionId = await adapter.open(manifestUri, key, recipientId, opts)
// key.byteLength is now 0 — it is detached. Set to null to prevent confusion:
key = null
```

---



### 7.1 Definition

A **Projection** is a pure function from a verified RDF graph to a derived RDF graph:

```
ProjectionFn = (graph: RDFGraph) → DerivedGraph
```

Projections are authored as **ProjectionDocuments** (JSON-LD, the PDL format) and executed by compiling them to SPARQL CONSTRUCT queries. A Projection does not bind to specific input CIDs — it operates on whatever graph is provided. The binding between a Projection and specific HIRI manifests is a concern of the calling application layer.

### 7.2 ProjectionDocument Schema

```typescript
type ProjectionDocument = {
  "@context": "https://hiri-protocol.org/query/v1",
  "@type": "hql:Projection",
  "@id": string,                    // IRI identifying this projection definition
  "hql:version": string,            // Semantic version string (e.g., "1.0.0")
  "hql:construct": HQLTemplate,     // The CONSTRUCT template — what the output graph contains
  "hql:where": HQLPattern[],        // The WHERE patterns — what to match in the input graph
  "hql:optional"?: HQLPattern[],    // Optional WHERE patterns
  "hql:filter"?: HQLFilter[],       // Filter expressions applied within WHERE
}
```

### 7.3 Compilation to SPARQL CONSTRUCT

A ProjectionDocument MUST be compiled to a SPARQL CONSTRUCT query before execution. The compilation is deterministic — identical ProjectionDocuments produce byte-identical SPARQL strings.

```
ProjectionDocument → compilePDL() → SPARQL CONSTRUCT string → executeQuery()
```

The compiler MUST:

- Expand all JSON-LD property shorthand using the declared `@context` before compilation. Compilation operates on expanded IRIs, not compact terms.
- Translate `hql:where` patterns to SPARQL `WHERE` graph patterns
- Translate `hql:construct` to a SPARQL CONSTRUCT template
- Translate `hql:optional` to SPARQL `OPTIONAL {}` blocks
- Translate `hql:filter` to SPARQL `FILTER()` expressions

**SPARQL 1.1 semantics govern all edge cases without exception.** Blank node handling, `@type` array matching, variable scoping, optional binding propagation — all are resolved by the W3C SPARQL 1.1 specification. HQL does not define or extend SPARQL semantics. This is the architectural purpose of compiling to SPARQL rather than reimplementing pattern matching.

### 7.4 ProjectionDocument Example

```json
{
  "@context": "https://hiri-protocol.org/query/v1",
  "@type": "hql:Projection",
  "@id": "hql:PublicPersonProjection",
  "hql:version": "1.0.0",

  "hql:construct": {
    "hql:template": [
      {
        "@id": "?person",
        "schema:name": "?name",
        "schema:jobTitle": "?title"
      }
    ]
  },

  "hql:where": [
    {
      "@id": "?person",
      "@type": "schema:Person",
      "schema:name": "?name"
    }
  ],

  "hql:optional": [
    {
      "@id": "?person",
      "schema:jobTitle": "?title"
    }
  ]
}
```

### 7.5 Compiled SPARQL (Informative)

```sparql
PREFIX schema: <https://schema.org/>

CONSTRUCT {
  ?person schema:name ?name .
  ?person schema:jobTitle ?title .
}
WHERE {
  ?person a schema:Person .
  ?person schema:name ?name .
  OPTIONAL { ?person schema:jobTitle ?title . }
}
```

### 7.6 Projection Chaining

Projections MAY be chained. A downstream ProjectionDocument MAY declare an upstream projection as its input:

```json
{
  "@type": "hql:Projection",
  "@id": "hql:EmployeeProjection",
  "hql:version": "1.0.0",
  "hql:input": "hql:PublicPersonProjection",
  "hql:where": [
    { "@id": "?person", "org:memberOf": "?org" }
  ]
}
```

When chained, the downstream projection executes against the derived RDF graph produced by the upstream projection. Chained projections MUST produce identical results whether the upstream projection output is materialized as an intermediate graph or computed inline as a sub-query. Circular chains MUST be rejected with `INVALID_PROJECTION_CHAIN`.

### 7.7 Determinism Constraints

ProjectionDocuments MUST NOT contain system time references, network calls, randomness, or execution-order dependencies. These constraints are structurally enforced by the compilation target — SPARQL CONSTRUCT has no access to these capabilities.

---

## 8. Query Model (QDL)

### 8.1 Definition

A **Query** is a pure function from a Projection State and optional Indexes to a result set:

```
QueryFn = (projectionState: RDFGraph, indexes: Index[], params: QueryParams) → QueryResult
```

Queries are authored as **QueryDocuments** (JSON-LD, the QDL format) and executed by compiling them to SPARQL SELECT queries.

### 8.2 QueryDocument Schema

```typescript
type QueryDocument = {
  "@context": "https://hiri-protocol.org/query/v1",
  "@type": "hql:Query",
  "@id": string,
  "hql:version": string,
  "hql:source"?: string,            // Document Graph Name for Mode 3 named graph scoping (§9.5)
  "hql:select": string[],           // Variable names to project
  "hql:where": HQLPattern[],        // Match patterns
  "hql:optional"?: HQLPattern[],    // Optional patterns
  "hql:filter"?: HQLFilter[],       // Filter expressions
  "hql:orderBy"?: HQLOrderSpec[],   // Order specification
  "hql:limit"?: number,             // Maximum result count
  "hql:offset"?: number             // Result offset for pagination
}
```

### 8.3 Compilation to SPARQL SELECT

A QueryDocument MUST be compiled to a SPARQL SELECT query before execution. The compiler MUST expand all JSON-LD compact terms to full IRIs before generating SPARQL. All SPARQL 1.1 semantics apply without exception or extension.

**Compiler warning for Mode 3 default graph queries:** If the execution context is Mode 3 (`contentStatus: "partial-disclosure"`) and the QueryDocument does not include `hql:source` and does not contain any `GRAPH` patterns in `hql:where`, the compiler MUST emit `DEFAULT_GRAPH_QUERY_IN_MODE3` as a non-fatal warning alongside the compiled SPARQL. See §9.6.

### 8.4 QueryDocument Example

```json
{
  "@context": "https://hiri-protocol.org/query/v1",
  "@type": "hql:Query",
  "@id": "hql:FindPersonByName",
  "hql:version": "1.0.0",
  "hql:source": "sha256:e08da327...",
  "hql:select": ["?person", "?name", "?title"],
  "hql:where": [
    {
      "@id": "?person",
      "@type": "schema:Person",
      "schema:name": "?name"
    }
  ],
  "hql:optional": [
    { "@id": "?person", "schema:jobTitle": "?title" }
  ],
  "hql:filter": [
    { "op": "contains", "left": "?name", "right": "Aaron" }
  ],
  "hql:limit": 10
}
```

### 8.5 Compiled SPARQL (Informative)

```sparql
PREFIX schema: <https://schema.org/>

SELECT ?person ?name ?title
WHERE {
  GRAPH <sha256:e08da327...> {
    ?person a schema:Person .
    ?person schema:name ?name .
    OPTIONAL { ?person schema:jobTitle ?title . }
    FILTER(CONTAINS(?name, "Aaron"))
  }
}
LIMIT 10
```

### 8.6 Operator Reference

| HQL Operator | SPARQL Translation |
|---|---|
| `eq` | `FILTER(?x = ?y)` |
| `neq` | `FILTER(?x != ?y)` |
| `contains` | `FILTER(CONTAINS(?x, "literal"))` |
| `startsWith` | `FILTER(STRSTARTS(?x, "literal"))` |
| `lt`, `lte`, `gt`, `gte` | `FILTER(?x < ?y)`, etc. |
| `regex` | `FILTER(REGEX(?x, "pattern", "flags"))` |
| `langMatches` | `FILTER(LANGMATCHES(LANG(?x), "en"))` |
| `bound` | `FILTER(BOUND(?x))` |
| `isIRI` | `FILTER(ISIRI(?x))` |

### 8.7 Determinism Rules

Queries MUST produce identical results for identical projection state. If result ordering is required, the QueryDocument MUST specify `hql:orderBy`. SPARQL 1.1 does not guarantee row ordering without an explicit ORDER BY clause, and HQL does not add a guarantee that SPARQL does not provide.

---

## 9. Privacy-Aware Query Semantics

This section is normative. The HIRI Privacy Extension v1.4.1 defines five privacy modes that each alter what content is available to HQL. The query layer MUST handle each mode correctly. Failure to do so constitutes a security violation.

### 9.1 The ContentStatus Field

Every HQL result set MUST carry a `contentStatus` field that reflects the privacy-aware availability of the content it was computed from:

| ContentStatus | Meaning for HQL |
|---|---|
| `verified` | Full plaintext verified. Query results are complete. |
| `partial-disclosure` | Mode 3 selective disclosure. Results reflect the disclosed statement set only. Absent predicates are withheld by the publisher. |
| `ciphertext-verified` | Mode 2 encrypted; no decryption key provided. No graph built; no query results possible. |
| `decrypted-verified` | Mode 2 encrypted; decryption key provided within a QuerySession. Full plaintext available. |
| `private-custody-asserted` | Mode 1 proof of possession. No content bytes available. |
| `attestation-verified` | Mode 5 attestation. No content body. |
| `unsupported-mode` | Unknown privacy mode. Signature verified; content not interpreted. |

### 9.2 Mode-by-Mode Semantics

#### Mode 1: Proof of Possession

No content is available. `buildGraph` MUST NOT be called. The result set MUST be empty with `contentStatus: "private-custody-asserted"` and `complete: false, completenessReason: "proof-of-possession"`. Applications MUST NOT interpret an empty result as indicating the queried data does not exist.

---

#### Mode 2: Encrypted Distribution

**Without decryption key:** `buildGraph` MUST NOT be called. The result set is empty with `contentStatus: "ciphertext-verified"` and `complete: false, completenessReason: "encrypted-no-key"`.

**With decryption key — QuerySession required:**

The caller MUST open a `QuerySession` (§6.4). The QuerySession decrypts the content, applies the `MemoryBudget` checks (§6.4.5), builds the graph exactly once, and holds it in volatile memory.

```typescript
const session = await openQuerySession(manifest, decryptionKey, recipientId, {
  ttl: callerDefinedTTL,
  entailmentMode: "none",
  memoryBudget: { maxInputBytes: callerDefinedBudget }
});
const results = await session.query(myQueryDocument);
session.close();
```

`contentStatus` for all session results is `"decrypted-verified"`. **QuerySession is the exclusive access mechanism for Mode 2 content.** Implementations MUST NOT provide a path to build a Mode 2 graph outside of a QuerySession.

---

#### Mode 3: Selective Disclosure

**Key normative behaviors:**

1. **Empty results for withheld predicates are correct.** `completenessReason: "partial-disclosure"` is the signal.

2. **Entailment mode MUST be `"none"` — no override permitted.** HQL MUST throw `ENTAILMENT_RESTRICTED_BY_PRIVACY_MODE` if the caller requests a non-`none` mode. No application-layer flag can override this. See §5.5 for the full rationale.

3. **No re-canonicalization of disclosed N-Quads.** Published N-Quads are loaded directly into the named graph without re-processing through URDNA2015.

4. **Named graph scoping required.** See §9.5.

5. **Default graph is intentionally empty.** See §9.6.

6. **Disclosure key material expands the disclosed set.** HMAC key or BBS+ proofs provided via `ResolveOptions` load additional statements. `contentStatus` remains `"partial-disclosure"` unless the disclosed set equals the full statement count.

---

#### Mode 4: Anonymous Publication

Content availability depends on the `contentVisibility` sub-mode. Query behavior is identical to the corresponding non-anonymous mode. The `identityType` field from the resolution result MUST be preserved in HQL query result metadata. Applications MUST NOT treat an ephemeral authority as a persistent identity.

---

#### Mode 5: Third-Party Attestation

`buildGraph` MUST NOT be called. Result set is empty with `contentStatus: "attestation-verified"`. To query the subject manifest, the caller MUST resolve and query it independently.

---

### 9.3 Privacy Mode and the Projection Cache

Cache validity MUST use `getLogicalPlaintextHash()` (Privacy Extension §11.3), not the raw `hiri:content.hash`.

A cached Projection State MUST be invalidated if:
1. `getLogicalPlaintextHash(currentManifest)` differs from the stored value
2. The ProjectionDocument `@id` or `hql:version` changed
3. The `contentStatus` changed to a more-available state (e.g., `partial-disclosure` → `verified`)
4. The content addressing mode changed (Privacy Extension §11.3)

Condition 3 is critical: a cached partial-disclosure projection is a strict subset of what is available after the content becomes public. Serving it would silently suppress authorized triples.

### 9.4 Mode Summary Table

| Privacy Mode | Build Graph? | Entailment Override | `complete` | `completenessReason` | `contentStatus` | Cache Allowed? |
|---|---|---|---|---|---|---|
| `public` | YES | None | `true` | — | `verified` | YES |
| `proof-of-possession` | NO | N/A | `false` | `"proof-of-possession"` | `private-custody-asserted` | YES (empty) |
| `encrypted` (no key) | NO | N/A | `false` | `"encrypted-no-key"` | `ciphertext-verified` | YES (empty) |
| `encrypted` (with key, QuerySession) | YES (session) | None | `true` | — | `decrypted-verified` | NO |
| `selective-disclosure` | YES (partial) | MUST be `"none"`; throw otherwise | `false` | `"partial-disclosure"` | `partial-disclosure` | YES (partial) |
| `anonymous-ephemeral` | Per sub-mode | Per sub-mode | Per sub-mode | Per sub-mode | Per sub-mode | Per sub-mode |
| `anonymous-pseudonymous` | Per sub-mode | Per sub-mode | Per sub-mode | Per sub-mode | Per sub-mode | Per sub-mode |
| `attestation` | NO | N/A | `false` | `"attestation"` | `attestation-verified` | YES (empty) |
| Unknown mode | NO | N/A | `false` | — | `unsupported-mode` | NO |

### 9.5 Blank Node Namespacing for Multi-Source Queries

**Problem:** URDNA2015 blank node labels are deterministic within a single document but not globally unique. Two independently canonicalized documents both produce blank nodes labeled `_:c14n0`, `_:c14n1`, etc. Loading Mode 3 N-Quads from multiple manifests into a shared Oxigraph dataset without scoping merges these labels into single nodes, corrupting both documents' graph structure and producing false cross-authority relationships.

**Solution — Named Graph Scoping:**

Each Mode 3 document's N-Quads MUST be loaded into a named graph whose IRI is the manifest's content hash:

```
Document Graph Name = manifest["hiri:content"]["hash"]
```

Example: `<sha256:e08da327...>`

Blank nodes are scoped to their named graph in Oxigraph and in all SPARQL 1.1-compliant RDF datasets. `_:c14n0` in `GRAPH <sha256:aaa...>` is a distinct node from `_:c14n0` in `GRAPH <sha256:bbb...>`. Implementations using a non-Oxigraph RDF engine MUST verify that blank nodes are scoped per named graph.

**Single-document queries** inject a `GRAPH` wrapper via the `hql:source` field (§8.2):

```sparql
SELECT ?name WHERE {
  GRAPH <sha256:e08da327...> { ?person schema:name ?name . }
}
```

**Multi-document queries** use `GRAPH ?g` patterns in `hql:where` without `hql:source`.

**This rule applies only to Mode 3 content.** Public content and Mode 2 session content load into a document-specific RDF index, not a shared dataset.

### 9.6 Default Graph Behavior for Mode 3

Because Mode 3 N-Quads load exclusively into named graphs (§9.5), **the default graph of the Oxigraph dataset is intentionally and necessarily empty** during all Mode 3 query executions.

A QDL document that omits `hql:source` and contains no explicit `GRAPH` patterns in `hql:where` will compile to a SPARQL query over the default graph. That query will return an empty result set. This is **correct behavior, not a bug** — but it is a common developer error that produces silent failures indistinguishable from "no matching data."

**Normative requirements:**

1. The compiler MUST emit `DEFAULT_GRAPH_QUERY_IN_MODE3` as a non-fatal warning whenever it compiles a QDL document that will query the default graph during a Mode 3 execution context.

2. The `QueryResult` returned from such a query MUST include `"DEFAULT_GRAPH_QUERY_IN_MODE3"` in its `warnings` array alongside the empty result set.

3. Implementations MUST NOT automatically redirect default graph queries to named graphs. The named graph structure is the correct query target; automatic redirection would conceal a developer error and could produce unexpected results in multi-source scenarios.

**Developer guidance (INFORMATIVE):** If results are unexpectedly empty during Mode 3 query development, the first diagnostic step is to check whether the QDL document includes `hql:source`. A QDL document without `hql:source` in a Mode 3 context is almost certainly a bug. Adding `"hql:source": "<contentHash>"` resolves the issue for single-source queries.

**Named graphs visible to SPARQL:**

To inspect which named graphs are present in the dataset (useful for debugging):

```sparql
SELECT DISTINCT ?g WHERE { GRAPH ?g { } }
```

This query returns the Document Graph Names of all loaded Mode 3 documents. Applications MAY execute this query to discover available sources before constructing targeted QDL documents.

---

## 10. Index Model

### 10.1 Definition

Indexes are derived structures that accelerate queries against Projection State without changing their results.

```typescript
type Index = {
  name: string,
  version: string,
  build: (projectionState: RDFGraph) => IndexData,
  query: (indexData: IndexData, params: QueryParams) => AcceleratedResult
}
```

### 10.2 Constraints

Indexes MUST:
- Be derived only from Projection State — never from raw canonical content directly
- Be rebuildable at any time from their source Projection State
- Produce results consistent with full SPARQL execution for the same queries

Indexes MUST NOT:
- Introduce new triples not present in the Projection State
- Be built from Mode 2 QuerySession graph content (the prohibition on durably storing decrypted graphs applies to indexes)

### 10.3 Standard Index Types

Implementations SHOULD support the following index types:

| Index Type | Description | Build Strategy |
|---|---|---|
| `byType` | Groups subjects by `rdf:type` | O(n) scan, hash map |
| `byPredicate` | Inverted index over predicates | O(n) scan, hash map |
| `fullText` | Text search over literal values | Implementation-defined tokenization |

Custom index types MUST be declared with a versioned `@id`.

### 10.4 Index Authority: A Conformance Property, Not a Runtime Check

Indexes are accelerators. Their role is to return results faster than a full SPARQL scan, not to replace SPARQL as the semantic authority.

**This rule is a normative statement about conformance, not a requirement for runtime contradiction detection.** An implementation is non-conformant if its indexes produce results that differ from full SPARQL execution against the same Projection State. The implementation is not required to run both a full SPARQL query and an index query in parallel to detect contradictions at runtime. If an index is correctly derived from Projection State, it will not contradict SPARQL.

Detection of index non-conformance is the role of the test vector suite (Appendix A), not of runtime self-verification.

---

## 11. Execution Lifecycle

### 11.1 Phases

```
Phase 1: Resolution   — Resolve HIRI manifest and content (HIRI layer)
Phase 2: Verification — Verify signatures, chain, and privacy mode (HIRI layer)
Phase 3: Build        — Build RDF graph via HIRI §15 buildGraph, or open QuerySession (HIRI §15 + HQL §6.4)
Phase 4: Project      — Execute compiled PDL CONSTRUCT queries (HQL)
Phase 5: Index        — Build optional indexes from Projection State (HQL)
Phase 6: Query        — Execute compiled QDL SELECT queries (HQL)
Phase 7: Result       — Return result set with ContentStatus, completeness, and warnings (HQL)
```

### 11.2 Phase 2 Gate

`buildGraph` and `openQuerySession` MUST NOT be called before Phase 2 completes successfully. Loading unverified content into the RDF index permits arbitrary triple injection into the query substrate.

### 11.3 Phase 3: Graph Construction Decision

```
if privacyMode == "encrypted" AND decryptionKey provided:
  → apply MemoryBudget checks (§6.4.5)
  → open QuerySession; all subsequent queries use session.query()
else if privacyMode allows content access:
  → call buildGraph() with appropriate entailmentMode and content bytes
else:
  → skip buildGraph(); produce empty result with appropriate ContentStatus
```

### 11.4 Phase 4: Projection Execution

```
ProjectionState = executeQuery(compilePDL(ProjectionDocument), rdfIndex, engine)
```

If no ProjectionDocuments are declared, the Projection State is the full RDF index (identity projection).

### 11.5 Phase 6: Query Execution

```
ResultSet = executeQuery(compileQDL(QueryDocument), projectionStateIndex, engine)
```

---

## 12. Result Model

### 12.1 QueryResult Type

```typescript
type CompletionReason =
  | "missing-cids"            // One or more input CIDs could not be resolved (offline)
  | "partial-disclosure"      // Mode 3: statements withheld by publisher
  | "encrypted-no-key"        // Mode 2: no decryption key provided
  | "proof-of-possession"     // Mode 1: no content bytes available
  | "attestation"             // Mode 5: attestation manifest has no content
  | "incomplete-upstream"     // Chained projection: upstream returned complete: false
  | "session-expired"         // QuerySession TTL exceeded (monotonic or wall-clock)
  | "session-memory-exceeded" // QuerySession closed under memory pressure

type ContentStatus =
  | "verified"
  | "partial-disclosure"
  | "ciphertext-verified"
  | "decrypted-verified"
  | "private-custody-asserted"
  | "attestation-verified"
  | "unsupported-mode"

type QueryResult = {
  results: Binding[],
  complete: boolean,
  completenessReason?: CompletionReason,  // MUST be present when complete === false
  contentStatus: ContentStatus,
  identityType?: "identified" | "anonymous-ephemeral" | "pseudonymous",
  warnings: string[]                       // Non-fatal issues; includes DEFAULT_GRAPH_QUERY_IN_MODE3
}

type Binding = {
  [variableName: string]: RDFTerm
}

type RDFTerm = {
  type: "uri" | "literal" | "blank",
  value: string,
  datatype?: string,
  language?: string
}
```

### 12.2 The `complete` Flag

`complete: false` applies in the conditions enumerated by `CompletionReason`. `completenessReason` MUST be present whenever `complete` is `false`.

`complete: true` MUST only be set when all of the following hold:
- All input CIDs resolved successfully
- `contentStatus` is `"verified"` or `"decrypted-verified"`
- No upstream projection returned `complete: false`

Applications MUST NOT treat `complete: false` as an error. The `completenessReason` type enables distinct application responses: a "sign in to decrypt" prompt for `"encrypted-no-key"`, a "some fields are hidden" indicator for `"partial-disclosure"`, a retry for `"missing-cids"`, and a session re-open flow for `"session-expired"` or `"session-memory-exceeded"`.

---

## 13. Caching

### 13.1 What MAY be Cached

| Cache Target | Allowed | Restriction |
|---|---|---|
| Compiled SPARQL | YES | Invalidate if document `hql:version` changes |
| Projection State | YES | See §13.2 |
| Index data | YES | Invalidate if Projection State invalidates |
| Mode 2 SessionGraph | Volatile only | MUST NOT be persisted; zeroed on close |
| Empty results from no-content modes | YES | Invalidate if manifest version changes |

### 13.2 Projection State Cache Validity

A cached Projection State is valid if and only if all of the following hold:
1. `getLogicalPlaintextHash(currentManifest)` equals the stored `logicalPlaintextHash`
2. The ProjectionDocument `@id` and `hql:version` are unchanged
3. The `contentStatus` has not changed to a more-available state
4. The content addressing mode is unchanged

If any condition fails, the cache MUST be invalidated and Projection State recomputed.

### 13.3 QuerySession Is Not a Cache

A QuerySession is an access scope, not a cache. Opening sessions to pre-warm a persistent cache, persisting `sessionId` across restarts, or using simultaneous in-context sessions for parallelization are all prohibited (§6.4.4, §6.5.4).

---

## 14. Offline Behavior

HQL inherits the offline-first principle from HIRI §4.1. Implementations MUST:
- Operate on available resolved content when CIDs cannot be fetched
- Return partial results with `complete: false, completenessReason: "missing-cids"` for unresolvable CIDs
- Distinguish CID-missing incompleteness from privacy-mode incompleteness via `completenessReason`
- Not treat offline state as a fatal error

If a QuerySession is open when the network becomes unavailable, the session continues against its in-memory SessionGraph. Network unavailability does not cause session expiry. TTL expiry and device sleep/wake behavior are governed by §6.4.6.

---

## 15. Error Handling

### 15.1 Error and Warning Registry

| Code | Type | Condition | Behavior |
|---|---|---|---|
| `COMPILATION_ERROR` | Error | PDL or QDL document fails to produce valid SPARQL | Reject; report details |
| `CONTEXT_RESOLUTION_FAILURE` | Error | `@context` URI not in pinned registry | Reject |
| `VERIFICATION_REQUIRED` | Error | `buildGraph` called before Phase 2 | Halt |
| `ENTAILMENT_RESTRICTED_BY_PRIVACY_MODE` | Error | Non-`none` entailment requested for Mode 3 | Throw; no override |
| `UNSUPPORTED_ENTAILMENT_MODE` | Error | `materialized` or `runtime` unsupported by implementation | Throw; do not silently fall back |
| `DECRYPTED_GRAPH_PERSISTENCE_VIOLATION` | Error | Attempt to persist SessionGraph to durable storage | Halt; zero immediately |
| `MISSING_CID` | Incompleteness | CID resolution failure | Partial execution; `complete: false` |
| `INVALID_PROJECTION_CHAIN` | Error | Circular or broken chain | Reject |
| `UPSTREAM_PROJECTION_INCOMPLETE` | Incompleteness | Upstream returned `complete: false` | Propagate |
| `SESSION_EXPIRED` | Error | QuerySession TTL exceeded (monotonic or wall-clock) | Close; zero; throw on next call |
| `SESSION_MEMORY_EXCEEDED` | Error | Pre-load byte limit or WASM page soft limit exceeded | Close; zero; throw |
| `WORKER_SERIALIZATION_ERROR` | Error | Attempt to include a prohibited object in a WorkerRequest, WorkerResponse, or WorkerPush payload (§6.6.5) | Throw; do not dispatch message |
| `DUPLICATE_SESSION_IN_CONTEXT` | Error | Second session opened against same manifest in same UI context | Throw |
| `BLANK_NODE_SCOPE_VIOLATION` | Error | Mode 3 N-Quads loaded without named graph when other Mode 3 sources are present | Reject load |
| `DEFAULT_GRAPH_QUERY_IN_MODE3` | Warning | QDL document queries default graph during Mode 3 execution | Emit warning; execute query; return empty results |

### 15.2 Failure vs. Incompleteness

**Failures** (errors) prevent or terminate execution. **Incompleteness** produces valid partial results. Privacy-mode restrictions, offline CIDs, partial disclosures, and session expiry during a result set all produce queryable states — not fatal failures. Only structural problems are failures.

---

## 16. Security Considerations

### 16.1 HQL Must Not Weaken HIRI Verification

HQL MUST NOT receive or process content that has not passed HIRI Phase 2 verification. A query result derived from unverified content cannot be trusted regardless of SPARQL execution correctness.

### 16.2 Entailment Mode as Security Boundary

The hard rejection of non-`none` entailment for Mode 3 content extends HIRI's "inference leakage" threat mitigation into the query layer. No application-layer flag can override this without violating the publisher's cryptographic disclosure intent (§5.5).

### 16.3 Compiled SPARQL Injection

The SPARQL compiler MUST:
- Validate variable names against `[?$][a-zA-Z_][a-zA-Z0-9_]*`
- Expand and validate all IRIs against the pinned context registry
- Escape all literal values in FILTER expressions
- Reject documents referencing unknown `@context` URIs

### 16.4 Index Non-Authority

Indexes accelerate SPARQL; they do not replace it. An incorrectly derived index is a conformance failure, not a new query semantic.

### 16.5 Decrypted Content Lifecycle

Implementations MUST:
- Zero decrypted byte arrays after `buildGraph` receives them
- Zero the SessionGraph on session close (any cause)
- Not log, persist, transmit, or replicate SessionGraph state
- Treat `SESSION_EXPIRED`, `SESSION_MEMORY_EXCEEDED`, and `DUPLICATE_SESSION_IN_CONTEXT` as close-and-zero events
- Apply the wall-clock TTL check on device resume (§6.4.6)

### 16.6 Named Graph Scoping as Integrity Property

Blank node collision between Mode 3 documents from different publishers would silently produce cross-authority relationship assertions that neither publisher made. Named graph scoping (§9.5) is therefore not only a correctness measure but a **cross-authority graph integrity property** — it prevents one publisher's blank node structure from contaminating another's within a shared dataset.

### 16.7 Session Concurrency and Heap Isolation

The in-process session duplication prohibition (§6.5.4) prevents a single UI context from accumulating multiple copies of decrypted graph data in the heap simultaneously. In combination with the `MemoryBudget` limits (§6.4.5), this bounds the maximum decrypted data resident in memory at any time within a single context to one SessionGraph. Independent UI contexts (browser tabs, workers) each enforce this limit independently — their heaps are isolated by the browser's process model.

---

## 17. Conformance

### 17.1 Conformance Levels

**Level 1: Core HQL**
Requires: HIRI Protocol v3.1.1 Core conformance

MUST implement:
- PDL-to-SPARQL CONSTRUCT compilation (§7)
- QDL-to-SPARQL SELECT compilation with `DEFAULT_GRAPH_QUERY_IN_MODE3` warning (§8.3, §9.6)
- Integration with HIRI §15 execution substrate (§6.1)
- `entailmentMode: "none"` enforcement as default and as Mode 3 restriction (§6.3, §9.2)
- Result model with typed `CompletionReason`, `ContentStatus`, and `warnings` (§12)
- Privacy mode handling for `public` and `selective-disclosure` content (§9.2)
- Named graph scoping for Mode 3 multi-source queries (§9.5)
- Default graph empty behavior and `DEFAULT_GRAPH_QUERY_IN_MODE3` warning (§9.6)
- Cache validity via `getLogicalPlaintextHash()` (§13.2)
- Full error and warning registry (§15.1)
- Appendix A test vectors: A.1, A.2, A.3, A.4, A.5, A.7, A.9

MAY implement:
- QuerySession for Mode 2 content (§6.4)
- `MemoryBudget.maxWasmPages` soft limit (§6.4.5)
- Page Visibility API session lifecycle (§6.4.6)
- Entailment modes `materialized` and `runtime`
- Projection chaining (§7.6)
- Index model (§10)

**Level 2: Full HQL**
Requires: HIRI Protocol v3.1.1 Interoperable or Full conformance

MUST implement everything in Level 1, plus:
- QuerySession with full lifecycle semantics: TTL, wall-clock expiry, `MemoryBudget` (mandatory `maxInputBytes`), zeroing, and `DUPLICATE_SESSION_IN_CONTEXT` enforcement (§6.4, §6.5)
- Page Visibility API session lifecycle (§6.4.6) — REQUIRED for browser implementations
- All five privacy mode handling behaviors (§9.2)
- QuerySession as the exclusive Mode 2 access mechanism (§9.2)
- Projection chaining (§7.6)
- Index model with at least `byType` and `byPredicate` (§10.3)
- Worker Message Protocol conformance (§6.6) for browser implementations providing multi-tab session access — RECOMMENDED; a `SharedWorkerSessionAdapter` conforming to §6.6.8 MUST be provided if the implementation supports multi-tab session sharing
- Appendix A test vectors: all vectors including A.6, A.7, A.8, A.9, A.10, A.11

### 17.2 Test Vector Requirement

Conformance is demonstrated by passing the Appendix A test vectors for the declared level. Test vectors are normative and override prose where ambiguity exists.

---

## 18. Future Extensions

- Declarative index definitions as JSON-LD documents
- CRDT-based incremental projections
- Streaming projection output for large graphs
- Federation across multiple HIRI authorities into a merged named dataset
- Standard HQL query DSL for non-JSON-LD clients
- Commitment-based projection integrity (Privacy Extension §17)
- QuerySession replay audit log for regulated environments
- `maxWasmPages` promoted to REQUIRED once WASM memory introspection is standardized across browser engines

---

## Appendix A: Normative Test Vectors

Implementations MUST produce byte-identical compiled SPARQL strings (modulo whitespace normalization per SPARQL 1.1) and semantically identical result sets including `complete`, `completenessReason`, `contentStatus`, and `warnings`.

---

### A.1 Basic Projection — Public Content (Level 1)

**Input content:**
```json
{
  "@context": "https://schema.org/",
  "@id": "hiri://key:ed25519:zTest.../data/person-001",
  "@type": "Person",
  "name": "Aaron",
  "jobTitle": "Semantic Architect"
}
```

**Input PDL:**
```json
{
  "@context": "https://hiri-protocol.org/query/v1",
  "@type": "hql:Projection",
  "@id": "hql:PersonProjection",
  "hql:version": "1.0.0",
  "hql:construct": { "hql:template": [{ "@id": "?p", "schema:name": "?n" }] },
  "hql:where": [{ "@id": "?p", "@type": "schema:Person", "schema:name": "?n" }]
}
```

**Expected compiled SPARQL:**
```sparql
PREFIX schema: <https://schema.org/>
CONSTRUCT { ?p schema:name ?n . }
WHERE { ?p a schema:Person . ?p schema:name ?n . }
```

**Expected result:**
```json
{
  "results": [
    {
      "p": { "type": "uri", "value": "hiri://key:ed25519:zTest.../data/person-001" },
      "n": { "type": "literal", "value": "Aaron" }
    }
  ],
  "complete": true,
  "contentStatus": "verified",
  "warnings": []
}
```

---

### A.2 Selective Disclosure — Withheld Predicate Returns Empty (Level 1)

**Content status:** `partial-disclosure`. Published N-Quads loaded into `GRAPH <sha256:abc123>`.

```
<hiri://key:ed25519:zTest.../data/person> <http://schema.org/name> "Aaron" .
<hiri://key:ed25519:zTest.../data/person> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Person> .
```

**Withheld by publisher:** `schema:email`

**QDL:**
```json
{
  "@context": "https://hiri-protocol.org/query/v1",
  "@type": "hql:Query",
  "@id": "hql:GetEmail",
  "hql:version": "1.0.0",
  "hql:source": "sha256:abc123",
  "hql:select": ["?person", "?email"],
  "hql:where": [{ "@id": "?person", "schema:email": "?email" }]
}
```

**Expected result:**
```json
{
  "results": [],
  "complete": false,
  "completenessReason": "partial-disclosure",
  "contentStatus": "partial-disclosure",
  "warnings": []
}
```

**Conformance note:** Empty results with `completenessReason: "partial-disclosure"` is the ONLY conformant result. Implementations MUST NOT return an error, infer a value, or indicate the subject lacks an email address.

---

### A.3 Entailment Mode Rejection for Mode 3 (Level 1)

**Condition:** Caller requests `entailmentMode: "materialized"` for Mode 3 content.

**Expected:** `ENTAILMENT_RESTRICTED_BY_PRIVACY_MODE` thrown before `buildGraph`. No override flag is accepted. No RDF index is built.

---

### A.4 Projection Cache Invalidation on Privacy Transition (Level 1)

**Chain:** V1 `proof-of-possession` → V2 `selective-disclosure` → V3 `public`, all with `getLogicalPlaintextHash()` = `"sha256:abc123"`.

**Cache built from V2:** `logicalPlaintextHash: "sha256:abc123"`, `contentStatus: "partial-disclosure"`.

**V3 arrives:** `contentStatus` changes to `"verified"`.

**Expected:** Cache IS invalidated. `contentStatus` changed to a more-available state. Projection recomputed from V3's full plaintext.

---

### A.5 SPARQL Injection Rejection (Level 1)

**Input:**
```json
{ "hql:where": [{ "@id": "?x ; DROP GRAPH <hiri://authority/data/person> ; ?y" }] }
```

**Expected:** `COMPILATION_ERROR`. Variable name fails pattern `[?$][a-zA-Z_][a-zA-Z0-9_]*`. SPARQL string NOT generated.

---

### A.6 QuerySession — Single Graph Build for Multiple Queries (Level 2)

**Condition:** Mode 2 encrypted manifest; decryption key provided; session opened with `ttl: 60000`, `memoryBudget: { maxInputBytes: 10485760 }`.

**Expected sequence:**
1. `buildGraph` called exactly **once** during `openQuerySession()`
2. Three `session.query()` calls execute without calling `buildGraph` again
3. All three results: `contentStatus: "decrypted-verified"`, `complete: true`, `warnings: []`
4. `session.close()` → decrypted bytes and SessionGraph zeroed
5. Fourth `session.query()` → throws `SESSION_EXPIRED`

**Verification metric:** `buildGraph` call count for this sequence MUST equal 1.

---

### A.7 Blank Node Namespacing — Multi-Source Mode 3 (Level 1)

**Source A** (`sha256:aaa111`):
```
<hiri://authorityA/data/person> <http://schema.org/name> "Alice" .
_:c14n0 <http://schema.org/knows> <hiri://authorityA/data/person> .
```

**Source B** (`sha256:bbb222`):
```
<hiri://authorityB/data/person> <http://schema.org/name> "Bob" .
_:c14n0 <http://schema.org/knows> <hiri://authorityB/data/person> .
```

Loaded into `GRAPH <sha256:aaa111>` and `GRAPH <sha256:bbb222>` respectively.

**Query:** `SELECT ?person ?name WHERE { GRAPH ?g { ?person schema:name ?name . } }`

**Expected result:**
```json
{
  "results": [
    { "person": { "type": "uri", "value": "hiri://authorityA/data/person" }, "name": { "type": "literal", "value": "Alice" } },
    { "person": { "type": "uri", "value": "hiri://authorityB/data/person" }, "name": { "type": "literal", "value": "Bob" } }
  ],
  "complete": false,
  "completenessReason": "partial-disclosure",
  "contentStatus": "partial-disclosure",
  "warnings": []
}
```

**Collision check:** Query `SELECT ?bn ?person WHERE { GRAPH ?g { ?bn schema:knows ?person . } }` MUST return exactly **two** results — one per named graph. If the blank nodes were merged, it would return four (each `_:c14n0` claiming to know both Alice and Bob), which is a cross-authority graph corruption failure.

---

### A.8 QuerySession Expiry Under Memory Pressure (Level 2)

**Condition:** Session opened with `memoryBudget: { maxInputBytes: 1024 }`. Decrypted content is 2048 bytes.

**Expected:**
1. `openQuerySession()` decrypts content to a 2048-byte `Uint8Array`
2. Pre-load check: `2048 > 1024` → decrypted bytes zeroed immediately
3. `openQuerySession()` throws `SESSION_MEMORY_EXCEEDED`
4. `buildGraph` is NEVER called
5. No `QueryResult` is produced

---

### A.9 Default Graph Empty for Mode 3 — Warning Emitted (Level 1)

**Context:** Mode 3 content loaded into `GRAPH <sha256:abc123>`. Default graph is empty.

**QDL (no `hql:source`, no `GRAPH` pattern):**
```json
{
  "@context": "https://hiri-protocol.org/query/v1",
  "@type": "hql:Query",
  "@id": "hql:NoSourceQuery",
  "hql:version": "1.0.0",
  "hql:select": ["?person", "?name"],
  "hql:where": [{ "@id": "?person", "schema:name": "?name" }]
}
```

**Expected result:**
```json
{
  "results": [],
  "complete": false,
  "completenessReason": "partial-disclosure",
  "contentStatus": "partial-disclosure",
  "warnings": ["DEFAULT_GRAPH_QUERY_IN_MODE3"]
}
```

**Conformance note:** The `DEFAULT_GRAPH_QUERY_IN_MODE3` warning MUST appear in `warnings`. The implementation MUST NOT redirect the query to the named graph. The empty result with the warning is the ONLY conformant output. Implementations that return results from the named graph (without the caller specifying `hql:source`) are non-conformant.

---

### A.10 Independent Tab Sessions — Concurrency Permitted (Level 2)

**Condition:** Two independent browser tabs (Tab A and Tab B), each a separate UI context, both open a QuerySession against the same manifest (`sha256:abc123`).

**Expected:**
1. Tab A calls `openQuerySession(manifest, key, id, opts)` → `SessionA` created successfully
2. Tab B calls `openQuerySession(manifest, key, id, opts)` → `SessionB` created successfully
3. `SessionA` and `SessionB` are independent — distinct `sessionId` values, distinct heaps, distinct TTLs
4. `SessionA.query(q)` returns results; `SessionB.query(q)` returns identical results (same content)
5. `SessionA.close()` → SessionA zeroed; SessionB continues unaffected
6. `SessionB.close()` → SessionB zeroed

**Conformance note:** Implementations MUST NOT throw `DUPLICATE_SESSION_IN_CONTEXT` for cross-context concurrency. The `DUPLICATE_SESSION_IN_CONTEXT` error applies only within a single UI context. Cross-context sessions are isolated by the browser process model and are each independently valid.

### A.11 SharedWorkerSessionAdapter — RPC Round-Trip with Key Transfer (Level 2)

This vector tests the full Worker Message Protocol lifecycle: session open with Transferable key transfer, query execution, and session expiry push notification.

**Setup:**
- Mode 2 encrypted manifest at URI `hiri://key:ed25519:zTest.../data/private-001`
- Decryption key: a valid 32-byte `ArrayBuffer`
- SharedWorker running with a conformant `SharedWorkerSessionAdapter`
- TTL: 5000 ms
- `memoryBudget.maxInputBytes`: 10 MB (content is within budget)

**Step 1 — Tab sends `session.open` with Transferable key:**

```javascript
// Tab side
const keyBuffer = await getDecryptionKey()  // ArrayBuffer, 32 bytes
adapter.open("hiri://key:ed25519:zTest.../data/private-001", keyBuffer, "reviewer-1", {
  ttl: 5000,
  memoryBudget: { maxInputBytes: 10485760 }
})
// After this line: keyBuffer.byteLength === 0  (detached)
```

**Expected WorkerRequest on the wire:**
```json
{
  "type": "session.open",
  "requestId": "<uuid>",
  "manifestUri": "hiri://key:ed25519:zTest.../data/private-001",
  "recipientId": "reviewer-1",
  "options": { "ttl": 5000, "memoryBudget": { "maxInputBytes": 10485760 } }
}
```
With the decryption key `ArrayBuffer` in the Transferable transfer list.

**Expected WorkerResponse:**
```json
{
  "type": "session.open.ok",
  "requestId": "<uuid>",
  "sessionId": "<worker-generated-opaque-id>",
  "contentStatus": "decrypted-verified"
}
```

**Conformance check — key detachment:** After `open()` resolves, `keyBuffer.byteLength` MUST equal `0`. If the key was copied rather than transferred, `byteLength` remains 32 — this is a conformance failure.

---

**Step 2 — Tab sends `session.query`:**

```json
{
  "type": "session.query",
  "requestId": "<uuid-2>",
  "sessionId": "<worker-generated-opaque-id>",
  "queryDocument": {
    "@context": "https://hiri-protocol.org/query/v1",
    "@type": "hql:Query",
    "@id": "hql:ListPeople",
    "hql:version": "1.0.0",
    "hql:select": ["?person", "?name"],
    "hql:where": [{ "@id": "?person", "@type": "schema:Person", "schema:name": "?name" }]
  }
}
```

**Expected WorkerResponse:**
```json
{
  "type": "session.query.ok",
  "requestId": "<uuid-2>",
  "result": {
    "results": [
      {
        "person": { "type": "uri", "value": "hiri://key:ed25519:zTest.../data/private-001" },
        "name":   { "type": "literal", "value": "Aaron" }
      }
    ],
    "complete": true,
    "contentStatus": "decrypted-verified",
    "warnings": []
  }
}
```

**Conformance check — SessionGraph not in payload:** The `result` field MUST be a plain JSON object matching `SerializedQueryResult`. It MUST NOT contain any `ArrayBuffer`, class instance, or RDF engine object reference.

---

**Step 3 — Session expires (TTL elapsed); WorkerPush broadcast:**

After 5000 ms, the worker closes the session and broadcasts:

```json
{
  "type": "session.expired",
  "sessionId": "<worker-generated-opaque-id>"
}
```

This message MUST be delivered to all connected tab ports. It carries no `requestId`.

**Step 4 — Tab attempts query after expiry:**

```json
{
  "type": "session.query",
  "requestId": "<uuid-3>",
  "sessionId": "<worker-generated-opaque-id>",
  "queryDocument": { ... }
}
```

**Expected WorkerResponse:**
```json
{
  "type": "session.query.error",
  "requestId": "<uuid-3>",
  "error": "SESSION_EXPIRED"
}
```

**Conformance check — no partial result:** The error response MUST NOT include a `result` field. `SESSION_EXPIRED` terminates the session; no further query results are produced.

---

**Step 5 — Prohibited payload rejection:**

A non-conformant tab attempts to include a `Uint8Array` of decrypted bytes in a `session.query` message body.

**Expected behavior:** `WORKER_SERIALIZATION_ERROR` thrown before the message is dispatched. The message MUST NOT be sent. If the worker receives such a message despite the check, it MUST throw `WORKER_SERIALIZATION_ERROR` and MUST NOT process the request.

---

## Appendix B: PDL-to-SPARQL Compilation Examples

This appendix is INFORMATIVE.

### B.1 Optional Pattern

```json
{ "hql:optional": [{ "@id": "?p", "schema:email": "?email" }] }
```
```sparql
OPTIONAL { ?p schema:email ?email . }
```

### B.2 Filter with Regex

```json
{ "hql:filter": [{ "op": "regex", "left": "?name", "right": "^Aaron", "flags": "i" }] }
```
```sparql
FILTER(REGEX(?name, "^Aaron", "i"))
```

### B.3 Nested Traversal

```json
{
  "hql:where": [
    { "@id": "?person", "org:memberOf": { "@id": "?org", "schema:name": "?orgName" } }
  ]
}
```
```sparql
WHERE {
  ?person org:memberOf ?org .
  ?org schema:name ?orgName .
}
```

### B.4 Named Graph Query — Single Source (Mode 3)

```json
{ "hql:source": "sha256:e08da327...", "hql:select": ["?name"], "hql:where": [{ "@id": "?person", "schema:name": "?name" }] }
```
```sparql
SELECT ?name WHERE { GRAPH <sha256:e08da327...> { ?person schema:name ?name . } }
```

### B.5 Named Graph Query — Multi-Source (Mode 3)

```json
{
  "hql:select": ["?g", "?name"],
  "hql:where": [
    { "hql:graph": "?g", "hql:patterns": [{ "@id": "?person", "schema:name": "?name" }] }
  ]
}
```
```sparql
SELECT ?g ?name WHERE { GRAPH ?g { ?person schema:name ?name . } }
```

### B.6 Named Graph Discovery Query (Mode 3 Debugging)

```sparql
SELECT DISTINCT ?g WHERE { GRAPH ?g { } }
```

Returns the Document Graph Names of all loaded Mode 3 documents. Use to verify which named graphs are present before writing targeted QDL documents.

---

## Appendix C: Privacy Mode Query Behavior Reference

This appendix is NORMATIVE.

| Privacy Mode | Build Graph? | Entailment Override | `complete` | `completenessReason` | `contentStatus` | Cache Allowed? |
|---|---|---|---|---|---|---|
| `public` | YES | None | `true` | — | `verified` | YES |
| `proof-of-possession` | NO | N/A | `false` | `"proof-of-possession"` | `private-custody-asserted` | YES (empty) |
| `encrypted` (no key) | NO | N/A | `false` | `"encrypted-no-key"` | `ciphertext-verified` | YES (empty) |
| `encrypted` (with key, QuerySession) | YES (session) | None | `true` | — | `decrypted-verified` | NO (session-volatile) |
| `selective-disclosure` | YES (partial) | MUST be `"none"`; throw `ENTAILMENT_RESTRICTED_BY_PRIVACY_MODE` | `false` | `"partial-disclosure"` | `partial-disclosure` | YES (partial) |
| `anonymous-ephemeral` | Per sub-mode | Per sub-mode | Per sub-mode | Per sub-mode | Per sub-mode | Per sub-mode |
| `anonymous-pseudonymous` | Per sub-mode | Per sub-mode | Per sub-mode | Per sub-mode | Per sub-mode | Per sub-mode |
| `attestation` | NO | N/A | `false` | `"attestation"` | `attestation-verified` | YES (empty) |
| Unknown mode | NO | N/A | `false` | — | `unsupported-mode` | NO |

---

## Document History

| Version | Date | Status | Notes |
|---------|------|--------|-------|
| 0.1.0 | 2026-04 | Superseded | Initial draft |
| 0.2.0 | 2026-04 | Superseded | Breaking rewrite: SPARQL substrate, privacy semantics, testable conformance |
| 1.0.0 | 2026-04 | Superseded | QuerySession, blank node namespacing, entailment rationale, index authority, typed result model |
| 1.1.0 | 2026-04 | Superseded | `MemoryBudget` model, session concurrency, sleep/wake TTL, Mode 3 default graph, `DEFAULT_GRAPH_QUERY_IN_MODE3` warning |
| **1.2.0** | **2026-04** | **Draft — Candidate for Stable** | Worker Message Protocol (§6.6), `SharedWorkerSessionAdapter` promoted to RECOMMENDED, Transferable key transfer normative, `WORKER_SERIALIZATION_ERROR`, test vector A.11 |

---

## License

**Specification:** CC0 1.0 Universal (Public Domain)
**Reference Implementations:** Apache 2.0

---

*HQL is a query compiler and privacy-aware result layer, not a query engine.*
*The engine is already specified. This spec tells you how to use it correctly.*
