# Weaver SDK Specification

**Document ID:** WEAVER-SDK-SPEC
**Version:** 1.1.0
**Previous:** 1.0.0
**Status:** Draft
**Depends on:** HQL Specification v1.2.0, HIRI Protocol Specification v3.1.1, HIRI Privacy & Confidentiality Extension v1.4.1

---

## v1.1.0 Revision Notes (from v1.0.0)

This revision addresses three implementation realities identified in adversarial review of v1.0.0. No prior normative semantics are removed. All changes are additive or clarifying.

| Issue | Change | Section |
|-------|--------|---------|
| `SharedWorker` absent on Android Chrome and restricted on iOS Safari | `WorkerStrategy` introduced: `SharedWorker` → `DedicatedWorker` → `MainThread` fallback chain; `WorkerClient` detects and negotiates strategy at construction; client API is identical across all strategies | §9, §9.3, §9.4, Appendix B.4 |
| Orphaned WASM memory if `buildGraph` throws mid-execution | `BuildHandle` primitive introduced on `IEngineAdapter`; `beginBuild()` issues a handle that MUST be either committed or aborted; `buildEncryptedGraph` pipeline (§7.4) calls `handle.abort()` on all error paths | §5.6, §7.4 |
| Hardware enclave setups perform derivation and decryption atomically — CEK cannot exist in JS memory | `IEnclaveDecryptor` introduced as a third cryptographic adapter option; co-occurrence rule revised from `(IKeyDerivation AND IDecryptor)` to `(IKeyDerivation AND IDecryptor) OR IEnclaveDecryptor`; `buildEncryptedGraph` branches on adapter type | §5.4, §5.7, §6.1, §7.4 |
| Test vector A.11 strategy-awareness | A.11 extended with strategy negotiation sequence and `DedicatedWorker` fallback sub-vector | Appendix A |

---

## v1.0.0 Revision Notes (from v0.2.0)

v0.2.0 was a design sketch. v1.0.0 is a normative specification. All interfaces are fully defined, all phase boundaries are enforced, and all gaps identified in adversarial review have been closed. The changes are breaking throughout.

| Issue | Change | Section |
|-------|--------|---------|
| Dependency on HQL v1.1.0 | Updated to HQL v1.2.0; `@weaver/worker` now implements the normative HQL §6.6 Worker Message Protocol | §2, §8 |
| Comlink used for worker RPC | Replaced with direct HQL §6.6 protocol implementation; Comlink cannot satisfy Transferable key transfer | §8 |
| `IVerifier` returned `boolean` | Now returns full `VerificationResult` matching HIRI §13.6 | §5.2 |
| `IVerifier` conflated Phase 2 and Phase 3 | Split into `IVerifier` (Phase 2) and `IDecryptor` (Phase 3) | §5.2, §5.4 |
| Key derivation path undefined | `IKeyDerivation` introduced covering X25519 ECDH + HKDF for Mode 2 CEK and Mode 3 HMAC key | §5.3 |
| Sessions keyed by manifest URI | Sessions keyed by manifest content hash; URI resolves to different content at different versions | §7.1 |
| `executeQuery` looked up by URI | Corrected to use `sessionId` per HQL §6.6 | §9.2 |
| `ITimestampProvider.onWake` optional | Made required; dual-clock TTL enforcement on wake is a MUST in HQL §6.4.6 | §5.5 |
| No engine adapter | `IEngineAdapter` introduced abstracting `buildGraph`, `executeQuery`, and N-Quads loading | §5.6 |
| Phase 2 gate not enforced | `PhaseGate` state machine introduced; `SessionManager` cannot reach Phase 3 without a verified manifest | §6.2 |
| Session expiry unhandled in `WorkerClient` | `WorkerClient` now implements `SharedWorkerSessionAdapter` fully, including lifecycle callbacks | §9 |
| `Weaver` constructor undefined | Fully specified with required/optional adapter declaration | §6.1 |
| `SessionOptions` misaligned with HQL | Aligned with `QuerySessionOptions` from HQL §6.4.1 | §7.2 |

---

## Table of Contents

1. [Purpose and Scope](#1-purpose-and-scope)
2. [Normative References](#2-normative-references)
3. [Terminology](#3-terminology)
4. [Architectural Overview](#4-architectural-overview)
5. [Adapter Interfaces](#5-adapter-interfaces)
   - [5.1 `IResolver`](#51-iresolver--network-boundary)
   - [5.2 `IVerifier`](#52-iverifier--phase-2-boundary)
   - [5.3 `IKeyDerivation`](#53-ikeyderivation--key-material-boundary)
   - [5.4 `IDecryptor`](#54-idecryptor--content-decryption-boundary-split-path)
   - [5.5 `ITimestampProvider`](#55-itimestampprovider--time-boundary)
   - [5.6 `IEngineAdapter`](#56-iengineadapter--execution-engine-boundary)
   - [5.7 `IEnclaveDecryptor`](#57-ienclavedecryptor--unified-enclave-decryption-boundary)
6. [Core Module — `@weaver/core`](#6-core-module----weavercore)
7. [Session Management](#7-session-management)
   - [7.4 Key Derivation Pipeline](#74-key-derivation-pipeline-mode-2)
8. [Worker Host Module — `@weaver/worker`](#8-worker-host-module----weaverworker)
9. [Worker Client Module — `@weaver/worker/client`](#9-worker-client-module----weaverworkerclient)
   - [9.1 `WorkerStrategy`](#91-workerstrategy--capability-negotiation)
   - [9.2 Strategy Implementations](#92-strategy-implementations)
   - [9.3 `WorkerClient`](#93-workerclient--full-implementation)
   - [9.4 Recommended Application Pattern](#94-recommended-application-pattern)
10. [Error Handling](#10-error-handling)
11. [Conformance](#11-conformance)

**Appendices**

- [A: Full Type Reference](#appendix-a-full-type-reference)
- [B: Platform Adapter Implementations (Informative)](#appendix-b-platform-adapter-implementations-informative)

---

## 1. Purpose and Scope

Weaver is a TypeScript SDK that implements the HQL Specification v1.2.0 for browser and Node.js environments. It provides:

- A complete, adapter-injected implementation of the HQL execution lifecycle (Phases 1–7)
- Type-safe interfaces for all environmental capabilities the protocol requires but cannot implement itself
- A `SessionManager` implementing the HQL `QuerySession` primitive for Mode 2 encrypted content
- A `@weaver/worker` package implementing the HQL §6.6 Worker Message Protocol for multi-tab session access
- A `@weaver/worker/client` package providing the `WorkerClient` implementation of `SharedWorkerSessionAdapter`

Weaver does NOT:

- Define canonical storage or content addressing — HIRI does this
- Define the SPARQL execution engine — HIRI §15 does this; Weaver wraps it via `IEngineAdapter`
- Make trust decisions — it surfaces `VerificationResult` to the application layer
- Provide default private key management — key material is held by `IKeyDerivation` implementations

---

## 2. Normative References

| Specification | Usage |
|---------------|-------|
| HQL Specification v1.2.0 | Primary specification; Weaver is an implementation of HQL |
| HIRI Protocol Specification v3.1.1 | Base protocol; Phase 1 and Phase 2 semantics |
| HIRI Privacy & Confidentiality Extension v1.4.1 | Privacy modes, key agreement, selective disclosure |
| W3C SPARQL 1.1 Query Language | Via IEngineAdapter |
| RFC 8032 | Ed25519 signatures; IVerifier |
| RFC 9180 | HPKE key agreement; IKeyDerivation |
| RFC 7748 | X25519 ECDH; IKeyDerivation |
| RFC 5869 | HKDF; IKeyDerivation |
| NIST SP 800-38D | AES-256-GCM; IDecryptor |
| W3C Page Visibility API | ITimestampProvider onWake; browser implementations |

---

## 3. Terminology

| Term | Definition |
|------|------------|
| Weaver | This SDK |
| Adapter | An implementation of one of the six Weaver adapter interfaces, provided by the host application |
| PhaseGate | The internal Weaver component that enforces the HIRI Phase 2 → Phase 3 transition guard |
| SessionManager | The internal Weaver component that manages `QuerySession` lifecycle per HQL §6.4 |
| WeaverWorkerHost | The `@weaver/worker` component that runs inside a SharedWorker, holding the `SessionManager` and `SessionGraph` |
| WorkerClient | The `@weaver/worker/client` component implementing `SharedWorkerSessionAdapter` from HQL §6.6.8 |
| ContentHash | The manifest content hash string (`sha256:...` or CIDv1) used as the canonical session key |
| VerificationResult | The structured output of Phase 2 verification, matching HIRI §13.6 |
| CEK | Content Encryption Key — the AES-256-GCM symmetric key used to encrypt Mode 2 content |
| HMAC Key | The per-document secret used for Mode 3 statement-level disclosure proofs |
| WorkerStrategy | The backing execution context selected by `WorkerClient` at construction: `SharedWorker`, `DedicatedWorker`, or `MainThread` |
| WorkerCapabilities | The set of features available under the active `WorkerStrategy`; cross-tab session sharing is only available under `SharedWorker` |
| BuildHandle | An opaque token returned by `IEngineAdapter.beginBuild()` representing an in-progress WASM graph construction; MUST be either committed (producing an `RDFIndex`) or aborted (zeroing allocated WASM pages) |
| IEnclaveDecryptor | An optional unified cryptographic adapter for environments where CEK derivation and content decryption occur atomically inside a hardware enclave or non-extractable WebCrypto context |

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" are interpreted per RFC 2119.

---

## 4. Architectural Overview

### 4.1 Module Structure

```
@weaver/core             — Adapters, PhaseGate, SessionManager, Compiler, phase orchestration
@weaver/worker           — WeaverWorkerHost: SharedWorker-side HQL §6.6 implementation
@weaver/worker/client    — WorkerClient: SharedWorkerSessionAdapter for UI tab side
```

The three modules have a strict dependency direction: `@weaver/worker` imports `@weaver/core`; `@weaver/worker/client` imports nothing from `@weaver/core` or `@weaver/worker` (it communicates only via postMessage). Application code imports from all three as needed.

### 4.2 Phase-to-Module Mapping

| HQL Phase | Responsibility | Weaver Component |
|-----------|---------------|------------------|
| Phase 1: Resolution | Fetch manifest and content by CID or URI | `IResolver` |
| Phase 2: Verification | Verify HIRI signatures, chain, key lifecycle | `IVerifier` → `PhaseGate` |
| Phase 3: Build | Decrypt (Mode 2) and build RDF graph | `IKeyDerivation` + `IDecryptor` + `IEngineAdapter` → `SessionManager` |
| Phase 4: Project | Compile PDL → SPARQL CONSTRUCT, execute | `Compiler` + `IEngineAdapter` |
| Phase 5: Index | Build optional indexes from Projection State | `IndexBuilder` (optional) |
| Phase 6: Query | Compile QDL → SPARQL SELECT, execute | `Compiler` + `IEngineAdapter` |
| Phase 7: Result | Assemble `QueryResult` with ContentStatus | `ResultAssembler` |

### 4.3 Adapter Dependency

```
Weaver (core)
  ├── IResolver           (REQUIRED)  — Phase 1
  ├── IVerifier           (REQUIRED)  — Phase 2
  ├── IEngineAdapter      (REQUIRED)  — Phase 3, 4, 6
  ├── ITimestampProvider  (REQUIRED)  — Session TTL
  ├── IKeyDerivation      (OPTIONAL*) — Phase 3, Mode 2 and Mode 3
  ├── IDecryptor          (OPTIONAL*) — Phase 3, Mode 2
  └── IEnclaveDecryptor   (OPTIONAL†) — Phase 3, Mode 2 (unified enclave path)

* IKeyDerivation and IDecryptor MUST be provided together or not at all.
  Providing one without the other is ADAPTER_DEPENDENCY_ERROR.

† IEnclaveDecryptor is an alternative to the (IKeyDerivation + IDecryptor) pair.
  Providing IEnclaveDecryptor alongside IKeyDerivation or IDecryptor is
  ADAPTER_DEPENDENCY_ERROR — only one decryption path may be active.

Without either path, Mode 2 encrypted content cannot be queried.
```

### 4.4 Purity Boundary

Weaver inherits the HIRI Edge-Canonical First principle. The core computation module MUST NOT call:

- `Date.now()`, `performance.now()`, or any system clock API — these are injected via `ITimestampProvider`
- `fetch()`, `XMLHttpRequest`, or any network API — injected via `IResolver`
- `WebCrypto`, `crypto.subtle`, or any cryptographic API — injected via `IVerifier`, `IKeyDerivation`, `IDecryptor`
- `WebAssembly.instantiate()` or any WASM API — injected via `IEngineAdapter`

Any violation of this boundary is a defect. The purity constraint is enforced at code review, not at runtime.

---

## 5. Adapter Interfaces

### 5.1 `IResolver` — Network Boundary

`IResolver` provides content resolution without coupling Weaver to any specific transport. Network failure is a valid state, not an exception. The resolver MUST NOT throw on network failure; it MUST return a typed `ResolutionState`.

```typescript
export type ResolutionState =
  | { status: "resolved";   bytes: Uint8Array }
  | { status: "unresolved"; reason: "offline" | "timeout" | "not-found" | "invalid-cid" }

export interface IResolver {
  /**
   * Resolves a CID (raw-sha256 or CIDv1) to its content bytes.
   * MUST NOT throw on network failure.
   * MUST return status "resolved" only when bytes are verified at the
   * transport layer (e.g., CID matches content hash). Content-hash
   * verification at the HIRI protocol layer (Phase 2) is performed
   * separately by IVerifier.
   */
  fetchCid(cid: string): Promise<ResolutionState>

  /**
   * Resolves a HIRI manifest URI to its manifest bytes.
   * Implementations MAY cache resolved manifests per the CID cache
   * semantics of HIRI §12 (URI Resolution Algorithm).
   * MUST NOT throw on network failure.
   */
  resolveManifest(uri: string): Promise<ResolutionState>

  /**
   * Resolves a HIRI KeyDocument for a given authority URI.
   * Used by IVerifier during Phase 2 key lifecycle checks (HIRI §13).
   * MUST NOT throw on network failure.
   * Implementations SHOULD cache KeyDocuments per HIRI Privacy
   * Extension §13.1 (recommended cache TTL: 24–72 hours).
   */
  resolveKeyDocument(authorityUri: string): Promise<ResolutionState>
}
```

### 5.2 `IVerifier` — Phase 2 Boundary

`IVerifier` performs HIRI signature verification and chain integrity checks. It corresponds exclusively to Phase 2 of the HQL execution lifecycle. It returns the full `VerificationResult` defined in HIRI §13.6 — not a boolean. The calling code (PhaseGate, §6.2) interprets the result and makes trust decisions.

```typescript
export interface VerificationResult {
  signatureValid:        boolean
  keyStatus:             "active" | "rotated-grace" | "rotated-expired" | "revoked" | "unknown"
  revocationStatus:      "confirmed-valid" | "confirmed-revoked" | "unknown"
  timestampVerification: "tsa-verified" | "advisory-only" | "absent"
  canonicalizationProfile: "JCS" | "URDNA2015"
  privacyMode:           string    // The declared privacy mode from hiri:privacy.mode
  contentHash:           string    // The manifest's hiri:content.hash (for session keying)
  logicalPlaintextHash:  string    // getLogicalPlaintextHash() result per HQL §9.3
}

export interface ChainVerificationResult {
  valid:  boolean
  depth:  number
  warnings: string[]
  // Per-manifest results in chain order (oldest first)
  manifests: VerificationResult[]
}

export interface IVerifier {
  /**
   * Verifies a single HIRI manifest's signature and key lifecycle.
   * Performs the full Phase 2 check per HIRI Protocol §10 and §13.
   *
   * The implementation MUST use the secure document loader (HIRI §7.5)
   * when verifying URDNA2015-profiled manifests.
   *
   * If the KeyDocument cannot be resolved (offline), the result MUST
   * include keyStatus: "unknown" and revocationStatus: "unknown" —
   * it MUST NOT report unconditional validity.
   *
   * MUST NOT throw for valid or invalid manifests. MUST throw only
   * for structurally malformed input that cannot produce a result.
   */
  verifyManifest(
    manifestBytes: Uint8Array,
    keyDocument?: Uint8Array  // Pre-fetched KeyDocument bytes, if available
  ): Promise<VerificationResult>

  /**
   * Walks and verifies a HIRI version chain.
   * Each manifest in the chain must link correctly to its predecessor
   * per HIRI Protocol §11.
   * manifests MUST be provided in chain order (oldest first).
   */
  verifyChain(manifests: Uint8Array[]): Promise<ChainVerificationResult>
}
```

**Why not boolean:** HIRI §13.6 defines five independent status dimensions. A manifest signed by a rotated key within the grace period has `signatureValid: true` but `keyStatus: "rotated-grace"` — it is not the same trust level as an active-key signature. Applications operating in regulated environments may reject rotated-key manifests even within the grace period. That is an application-layer policy decision; Weaver reports the facts and the application decides. Collapsing to `boolean` removes the information the application needs to make that decision.

### 5.3 `IKeyDerivation` — Key Material Boundary

`IKeyDerivation` performs the X25519 ECDH key agreement and HKDF derivation defined in HIRI Privacy Extension §13.2. It is responsible for extracting the CEK (Mode 2) or HMAC key (Mode 3) from the recipient's encrypted key share in the manifest.

The recipient's long-term private key is held by the `IKeyDerivation` implementation. It MUST NOT appear as a parameter in any method signature. The implementation is constructed with access to the private key (via hardware security module, secure enclave, or in-memory key management). This boundary ensures that private key bytes never appear in Weaver's core logic.

```typescript
export interface CEKDerivationParams {
  ephemeralPublicKey: Uint8Array   // From manifest hiri:privacy.parameters.hmacKeyRecipients.ephemeralPublicKey
  recipientId:        string       // Identifies the recipient entry in the manifest
  iv:                 Uint8Array   // AES-GCM IV from the manifest key agreement block
  encryptedKeyShare:  Uint8Array   // The recipient's encryptedKey or encryptedHmacKey field
  keyAgreement:       "X25519-HKDF-SHA256" | "HPKE-Base-X25519-SHA256-AES256GCM"
}

export interface HMACKeyDerivationParams {
  ephemeralPublicKey: Uint8Array
  recipientId:        string
  iv:                 Uint8Array
  encryptedHmacKey:   Uint8Array
}

export interface IKeyDerivation {
  /**
   * Derives the Content Encryption Key for Mode 2 content decryption.
   *
   * Performs:
   *   1. X25519(recipientPrivateKey, ephemeralPublicKey) → sharedSecret
   *   2. HKDF-SHA256(ikm=sharedSecret, salt=iv, info="hiri-cek-v1.1"||recipientId) → KEK
   *   3. AES-256-GCM-Decrypt(KEK, iv, encryptedKeyShare) → CEK
   *
   * Per Privacy Extension §13.2. The recipientPrivateKey is held
   * by the implementation; it MUST NOT be a parameter.
   *
   * Returns the raw CEK bytes. The caller (SessionManager) is
   * responsible for zeroing these bytes after use.
   */
  deriveCEK(params: CEKDerivationParams): Promise<Uint8Array>

  /**
   * Derives the HMAC key for Mode 3 selective disclosure verification.
   *
   * Performs the same ECDH+HKDF derivation as deriveCEK but with
   * the domain-separated info label "hiri-hmac-v1.1"||recipientId
   * per Privacy Extension §8.6.1.
   *
   * Returns the raw HMAC key bytes. The caller is responsible for
   * zeroing these bytes after use.
   */
  deriveHMACKey(params: HMACKeyDerivationParams): Promise<Uint8Array>
}
```

### 5.4 `IDecryptor` — Content Decryption Boundary (Split Path)

`IDecryptor` performs AES-256-GCM content decryption using an already-derived CEK. It is one half of the split decryption path (`IKeyDerivation` + `IDecryptor`). For environments where the CEK cannot exist in JavaScript memory, see `IEnclaveDecryptor` (§5.7).

```typescript
export interface IDecryptor {
  /**
   * Decrypts Mode 2 ciphertext using AES-256-GCM.
   *
   * Parameters:
   *   ciphertext — The encrypted content bytes from HIRI resolution
   *   cek        — The Content Encryption Key from IKeyDerivation.deriveCEK()
   *   iv         — The AES-GCM initialization vector (12 bytes) from the manifest
   *
   * Returns the plaintext bytes (N-Quads or JSON-LD).
   *
   * The CEK MUST be zeroed by the caller (SessionManager) immediately
   * after this method returns, per HQL §16.5.
   *
   * MUST throw if AES-GCM authentication tag verification fails.
   * Authentication failure indicates ciphertext tampering and MUST
   * be treated as a fatal Phase 3 error.
   */
  decryptContent(
    ciphertext: Uint8Array,
    cek:        Uint8Array,
    iv:         Uint8Array
  ): Promise<Uint8Array>
}
```

**Dependency rule:** `IKeyDerivation` and `IDecryptor` MUST be provided together or not at all. Providing `IEnclaveDecryptor` alongside either is `ADAPTER_DEPENDENCY_ERROR`. See §6.1 for constructor enforcement.

### 5.5 `ITimestampProvider` — Time Boundary

`ITimestampProvider` provides dual-clock timestamps for HQL §6.4.6 session TTL enforcement. Both methods are required. `onWake` is required for all implementations — it is NOT optional.

```typescript
export interface ITimestampProvider {
  /**
   * Returns a high-resolution monotonic timestamp in milliseconds.
   * MUST be monotonically non-decreasing within a single runtime session.
   * MAY pause during device sleep (this is the known limitation that
   * necessitates wallClockNow() for cross-check).
   *
   * Browser: performance.now()
   * Node.js: Number(process.hrtime.bigint()) / 1_000_000
   */
  monotonicNow(): number

  /**
   * Returns the current wall-clock time in milliseconds since Unix epoch.
   * MUST reflect real elapsed time including device sleep periods.
   * MAY be adjusted by NTP or system clock changes.
   *
   * Browser: Date.now()
   * Node.js: Date.now()
   */
  wallClockNow(): number

  /**
   * Registers a callback to be invoked when the device wakes from sleep
   * or the browser tab becomes visible after being backgrounded.
   *
   * This is REQUIRED (not optional). Weaver uses it to trigger the
   * dual-clock TTL check on resume per HQL §6.4.6:
   *   "Implementations MUST run the dual-timestamp expiry check
   *    immediately upon any event that indicates the device or tab
   *    has resumed."
   *
   * Browser: document.addEventListener("visibilitychange", ...) when
   *   visibilityState transitions to "visible"; also fires on "focus"
   *   and "pageshow" events.
   * Node.js: No-op implementation is permitted (device sleep is not
   *   a concern in server environments). Implementations MUST still
   *   provide this method; a no-op body is conformant for Node.js.
   *
   * The callback MUST be called synchronously with no arguments.
   * Weaver uses it to trigger immediate session expiry evaluation.
   */
  onWake(callback: () => void): void

  /**
   * Registers a callback to be invoked when the browser tab becomes
   * hidden (backgrounded, screen off, tab switched away).
   *
   * Used by Weaver to optionally close sessions aggressively on
   * backgrounding, per HQL §6.4.6 RECOMMENDED behavior.
   *
   * Browser: document.addEventListener("visibilitychange", ...) when
   *   visibilityState transitions to "hidden".
   * Node.js: No-op implementation is permitted.
   */
  onBackground(callback: () => void): void
}
```

**Why `onWake` is required, not optional:** HQL §6.4.6 states, using MUST language, that dual-timestamp expiry checks must run on device resume. Making `onWake` optional in v0.2.0 meant implementations could silently omit the wake handler, leaving decrypted session graphs in memory for arbitrary wall-clock durations after device sleep. There is no conformant implementation that can satisfy the MUST without this hook.

### 5.6 `IEngineAdapter` — Execution Engine Boundary

`IEngineAdapter` abstracts the Oxigraph WASM engine. It introduces `BuildHandle` — an opaque token that represents an in-progress graph construction. If `buildGraph` throws mid-execution after allocating WASM pages, those pages are not automatically freed because no `RDFIndex` handle was returned. The `BuildHandle` pattern ensures the caller always has a token to abort on the error path, preventing orphaned WASM memory containing decrypted graph fragments.

```typescript
export type EntailmentMode = "none" | "materialized" | "runtime"

export interface RDFIndex {
  readonly _brand: "RDFIndex"
}

export interface RDFDataset {
  readonly _brand: "RDFDataset"
}

/**
 * BuildHandle — an opaque token representing an in-progress WASM graph build.
 *
 * Lifecycle:
 *   const handle = await engine.beginBuild(params)
 *   try {
 *     const index = await handle.commit()   // Build completes → RDFIndex
 *   } catch {
 *     await handle.abort()                  // Build failed → zero and free WASM pages
 *   }
 *
 * A BuildHandle MUST be either committed or aborted. Failure to call
 * either method on an error path is a memory leak. The engine MAY
 * enforce this by tracking outstanding handles.
 *
 * abort() MUST:
 *   1. Signal the WASM engine to terminate any in-progress build
 *   2. Zero any WASM heap pages allocated during the build
 *   3. Free those pages back to the allocator
 * abort() MUST be idempotent — multiple calls are safe.
 */
export interface BuildHandle {
  /**
   * Completes the graph build and returns the RDFIndex.
   * Throws if the build fails (e.g., malformed N-Quads, WASM fault).
   * On throw, the handle transitions to the aborted state — the caller
   * MUST NOT call abort() after commit() throws (it is already aborted).
   */
  commit(): Promise<RDFIndex>

  /**
   * Aborts the build, zeroing and freeing allocated WASM pages.
   * Idempotent. MUST be called in all error paths where commit() was
   * not successfully called.
   */
  abort(): Promise<void>
}

export interface BuildParams {
  content:        Uint8Array
  format:         string
  baseURI:        string
  entailmentMode: EntailmentMode
}

export interface RawBinding {
  [variableName: string]: {
    type:      "uri" | "literal" | "blank"
    value:     string
    datatype?: string
    language?: string
  }
}

export interface RawQueryResult {
  bindings: RawBinding[]
}

export interface IEngineAdapter {
  /**
   * Initializes the WASM engine. MUST be called before any other method.
   * Subsequent calls are no-ops if already initialized.
   */
  initialize(): Promise<void>

  /**
   * Begins a graph build operation and returns a BuildHandle.
   * Replaces the previous single-step buildGraph() method.
   *
   * The build begins loading content into WASM memory when this
   * method is called. The caller MUST either call handle.commit()
   * to complete the build or handle.abort() to free allocated memory.
   *
   * Usage in SessionManager:
   *   const handle = await engine.beginBuild({ content, format, baseURI, entailmentMode })
   *   try {
   *     const index = await handle.commit()
   *     // ... use index
   *   } catch (err) {
   *     await handle.abort()   // zeros WASM pages — no orphaned decrypted fragments
   *     throw err
   *   }
   */
  beginBuild(params: BuildParams): Promise<BuildHandle>

  /**
   * Loads N-Quads into a named graph within a shared RDF dataset.
   * Used for Mode 3 multi-source queries per HQL §9.5.
   */
  loadNQuadsIntoNamedGraph(
    nquads:    string,
    graphName: string,
    dataset:   RDFDataset
  ): Promise<void>

  /**
   * Creates an empty shared RDF dataset for multi-source Mode 3 loading.
   */
  createDataset(): Promise<RDFDataset>

  /**
   * Converts a populated RDF dataset into a queryable RDFIndex.
   */
  datasetToIndex(dataset: RDFDataset): Promise<RDFIndex>

  /**
   * Executes a SPARQL query string against an RDFIndex.
   */
  executeQuery(
    sparql: string,
    index:  RDFIndex
  ): Promise<RawQueryResult>

  /**
   * Releases an RDFIndex and frees associated WASM memory.
   * zero: true signals the engine to zero the memory before freeing.
   * MUST be called with zero: true for all Mode 2 SessionGraph releases.
   */
  releaseIndex(index: RDFIndex, zero: boolean): Promise<void>

  /**
   * Returns current WASM page count or null if not observable.
   * Used for MemoryBudget.maxWasmPages soft limit (HQL §6.4.5).
   */
  observeWasmPageCount(): number | null
}
```

### 5.7 `IEnclaveDecryptor` — Unified Enclave Decryption Boundary

`IEnclaveDecryptor` is an alternative to the `(IKeyDerivation + IDecryptor)` pair for environments where the CEK cannot exist in JavaScript memory at any point. This includes:

- **Hardware Security Modules (HSM)** where key derivation and decryption occur on-device and only plaintext is returned
- **WebCrypto non-extractable key setups** where `CryptoKey` objects for X25519 and AES-GCM operations are marked `extractable: false`, preventing the CEK from ever appearing as a `Uint8Array` in JS
- **Platform Secure Enclave integrations** (e.g., TPM on Windows, Secure Enclave on Apple Silicon) where the entire ECDH + HKDF + AES-GCM chain executes inside the enclave

The critical difference from the split path: in the split path, the CEK briefly exists as a `Uint8Array` in JS memory between `deriveCEK()` returning and `decryptContent()` consuming it — Weaver zeros it immediately, but it existed. In the enclave path, the CEK never appears in JS memory at all.

```typescript
export interface EnclaveDecryptParams {
  manifestBytes:  Uint8Array   // Full manifest bytes; the enclave parses key agreement params
  recipientId:    string       // Identifies the recipient entry; used for HKDF info label
  ciphertext:     Uint8Array   // Encrypted content bytes
}

export interface IEnclaveDecryptor {
  /**
   * Performs the full Mode 2 decryption pipeline atomically:
   *   1. Parses key agreement params (ephemeralPublicKey, iv, encryptedKeyShare)
   *      from manifestBytes for the given recipientId
   *   2. Performs X25519 ECDH using the recipient's private key (held in enclave)
   *   3. Performs HKDF-SHA256 to derive KEK
   *   4. Performs AES-256-GCM decryption to unwrap CEK from encryptedKeyShare
   *   5. Performs AES-256-GCM decryption of ciphertext using CEK
   *   6. Returns plaintext bytes
   *
   * The CEK MUST NOT appear in JavaScript memory at any point.
   * All intermediate key material MUST remain within the enclave boundary.
   *
   * Returns the plaintext content bytes (N-Quads or JSON-LD).
   *
   * MUST throw if:
   *   - The recipient ID is not found in the manifest
   *   - X25519 key agreement fails (wrong key)
   *   - Any AES-GCM authentication tag verification fails (tampering)
   *
   * The caller (SessionManager) applies MemoryBudget.maxInputBytes to
   * the returned plaintext before passing it to IEngineAdapter.beginBuild().
   */
  decryptManifestContent(params: EnclaveDecryptParams): Promise<Uint8Array>

  /**
   * Derives the HMAC key for Mode 3 selective disclosure verification.
   * Equivalent to IKeyDerivation.deriveHMACKey() but operating entirely
   * within the enclave. Returns the HMAC key bytes.
   *
   * NOTE: Unlike the CEK (which need not leave the enclave for content
   * decryption), the HMAC key must be returned to JS so Weaver can
   * verify Mode 3 statement HMAC tags per Privacy Extension §8.6.1.
   * The caller MUST zero this value immediately after use.
   */
  deriveHMACKey(params: HMACKeyDerivationParams): Promise<Uint8Array>
}
```

**Adapter selection logic:** When `IEnclaveDecryptor` is provided, `SessionManager.buildEncryptedGraph()` (§7.4) takes the enclave path. When `(IKeyDerivation + IDecryptor)` are provided, it takes the split path. The two paths are mutually exclusive; the `Weaver` constructor enforces this.

**Why `deriveHMACKey` returns bytes:** In Mode 3 selective disclosure, the HMAC key is used by Weaver's result layer to verify statement membership proofs — a pure computation over the disclosed N-Quad strings. This computation happens in JavaScript, not in the engine. There is no way to perform it inside the enclave without either (a) sending all candidate N-Quad strings into the enclave for checking (a major API change) or (b) returning the HMAC key to JavaScript (the current approach). For Mode 3 deployments with extreme confidentiality requirements, BBS+ selective disclosure (Privacy Extension §8.6.2) is the appropriate alternative — BBS+ verification is a zero-knowledge proof that requires no HMAC key.

---

## 6. Core Module — `@weaver/core`

### 6.1 `Weaver` Constructor

The `Weaver` class is the primary entry point. It accepts an adapter bundle and validates it at construction time.

```typescript
export interface WeaverAdapters {
  resolver:           IResolver            // REQUIRED
  verifier:           IVerifier            // REQUIRED
  engine:             IEngineAdapter       // REQUIRED
  timestampProvider:  ITimestampProvider   // REQUIRED
  keyDerivation?:     IKeyDerivation       // OPTIONAL — split path; must co-occur with decryptor
  decryptor?:         IDecryptor           // OPTIONAL — split path; must co-occur with keyDerivation
  enclaveDecryptor?:  IEnclaveDecryptor    // OPTIONAL — enclave path; mutually exclusive with split path
}

export interface WeaverOptions {
  adapters: WeaverAdapters
  defaultEntailmentMode?: EntailmentMode
  closeSessionOnBackground?: boolean
}

export class Weaver {
  readonly phaseGate:      PhaseGate
  readonly sessionManager: SessionManager
  readonly compiler:       Compiler

  constructor(options: WeaverOptions) {
    this.validateAdapters(options.adapters)
    // ...
  }

  private validateAdapters(adapters: WeaverAdapters): void {
    const hasSplitDerivation = adapters.keyDerivation   !== undefined
    const hasSplitDecryptor  = adapters.decryptor       !== undefined
    const hasEnclave         = adapters.enclaveDecryptor !== undefined

    // Split path: both or neither
    if (hasSplitDerivation !== hasSplitDecryptor) {
      throw new WeaverError(
        "ADAPTER_DEPENDENCY_ERROR",
        "IKeyDerivation and IDecryptor must be provided together or not at all."
      )
    }

    // Enclave path is mutually exclusive with split path
    if (hasEnclave && (hasSplitDerivation || hasSplitDecryptor)) {
      throw new WeaverError(
        "ADAPTER_DEPENDENCY_ERROR",
        "IEnclaveDecryptor cannot be combined with IKeyDerivation or IDecryptor. " +
        "Choose one decryption path: split (IKeyDerivation + IDecryptor) or enclave (IEnclaveDecryptor)."
      )
    }
  }

  /**
   * Executes the full HQL lifecycle (Phases 1–7) against a manifest URI.
   * This is the primary convenience method for single-document queries.
   *
   * For Mode 2 content that will be queried multiple times, prefer
   * openSession() to avoid repeated decryption.
   */
  async query(params: QueryParams): Promise<QueryResult>

  /**
   * Resolves and verifies a manifest (Phases 1–2), then opens a
   * QuerySession (Phase 3) for repeated Mode 2 queries.
   * Requires IKeyDerivation and IDecryptor adapters.
   * Returns a QuerySession per HQL §6.4.
   */
  async openSession(params: OpenSessionParams): Promise<QuerySession>

  /**
   * Resolves and verifies a manifest (Phases 1–2) only.
   * Returns the VerificationResult for application-layer trust decisions.
   * Does not proceed to Phase 3.
   */
  async verify(manifestUri: string): Promise<VerificationResult>
}
```

### 6.2 `PhaseGate` — Phase 2 Enforcement

`PhaseGate` is an internal Weaver component that enforces the HQL §11.2 invariant:

> `buildGraph` and `openQuerySession` MUST NOT be called before Phase 2 completes successfully.

It maintains a state machine per manifest content hash. The `SessionManager` MUST call `phaseGate.requireVerified(contentHash)` before any Phase 3 operation. If the manifest has not completed Phase 2, the gate throws `VERIFICATION_REQUIRED`.

```typescript
type ManifestPhase =
  | { phase: "unresolved" }
  | { phase: "resolved";  bytes: Uint8Array }
  | { phase: "verified";  result: VerificationResult; bytes: Uint8Array }

class PhaseGate {
  private states = new Map<string, ManifestPhase>()

  /**
   * Records successful Phase 1 resolution for a manifest URI.
   * The contentHash is derived from the manifest bytes and used
   * as the canonical key for all subsequent lookups.
   */
  recordResolved(contentHash: string, bytes: Uint8Array): void {
    this.states.set(contentHash, { phase: "resolved", bytes })
  }

  /**
   * Records successful Phase 2 verification.
   * The VerificationResult is stored for retrieval by downstream phases.
   */
  recordVerified(contentHash: string, result: VerificationResult): void {
    const state = this.states.get(contentHash)
    if (!state || state.phase !== "resolved") {
      throw new WeaverError("INVALID_PHASE_TRANSITION",
        `Cannot record verification for ${contentHash}: not in resolved state.`)
    }
    this.states.set(contentHash, { phase: "verified", result, bytes: state.bytes })
  }

  /**
   * Phase 3 gate. Called by SessionManager before any decryption or
   * graph build. Throws VERIFICATION_REQUIRED if Phase 2 has not
   * completed for this content hash.
   *
   * Returns the VerificationResult for use by downstream components.
   */
  requireVerified(contentHash: string): VerificationResult {
    const state = this.states.get(contentHash)
    if (!state || state.phase !== "verified") {
      throw new WeaverError("VERIFICATION_REQUIRED",
        `Manifest ${contentHash} has not completed Phase 2 verification.`)
    }
    return state.result
  }

  /**
   * Returns the verified manifest bytes for Phase 3 content loading.
   */
  getVerifiedBytes(contentHash: string): Uint8Array {
    const state = this.states.get(contentHash)
    if (!state || state.phase !== "verified") {
      throw new WeaverError("VERIFICATION_REQUIRED")
    }
    return state.bytes
  }
}
```

**Phase gate sequence for a complete query:**

```
Phase 1: resolver.resolveManifest(uri)
           → ResolutionState
           → phaseGate.recordResolved(contentHash, bytes)

Phase 2: verifier.verifyManifest(bytes, keyDoc?)
           → VerificationResult
           → phaseGate.recordVerified(contentHash, result)

Phase 3: phaseGate.requireVerified(contentHash)   ← GATE: throws if Phase 2 incomplete
           → VerificationResult (used to determine privacy mode)
           → sessionManager.openSession(...) or engine.buildGraph(...)
```

### 6.3 `Compiler`

The `Compiler` translates PDL `ProjectionDocument` objects and QDL `QueryDocument` objects into SPARQL strings. It is context-aware for Mode 3 default graph detection.

```typescript
export interface CompileContext {
  contentStatus: ContentStatus
  // The Document Graph Name if compiling for a single named source.
  // Derived from QueryDocument.hql:source when present.
  documentGraphName?: string
}

export interface CompileResult {
  sparql:   string
  warnings: string[]
}

class Compiler {
  /**
   * Compiles a PDL ProjectionDocument to a SPARQL CONSTRUCT string.
   * Validates all variable names against [?$][a-zA-Z_][a-zA-Z0-9_]*
   * and escapes all literal values per HQL §16.3.
   */
  compilePDL(
    projectionDocument: object,
    context: CompileContext
  ): CompileResult

  /**
   * Compiles a QDL QueryDocument to a SPARQL SELECT string.
   *
   * Mode 3 default graph detection (HQL §9.6):
   * If context.contentStatus === "partial-disclosure" AND
   *   the QueryDocument lacks hql:source AND
   *   hql:where contains no GRAPH patterns,
   * the compiler MUST add "DEFAULT_GRAPH_QUERY_IN_MODE3" to result.warnings.
   * The SPARQL is still generated and targets the default graph (which is
   * empty for Mode 3). The warning is the signal; the behavior is correct.
   */
  compileQDL(
    queryDocument: object,
    context: CompileContext
  ): CompileResult
}
```

### 6.4 Phase Orchestration

The `Weaver.query()` method orchestrates the full Phase 1–7 lifecycle for single-document queries. The following pseudocode is normative — implementations MUST follow this sequence.

```typescript
async query(params: QueryParams): Promise<QueryResult> {
  // Phase 1: Resolution
  const manifestState = await this.adapters.resolver.resolveManifest(params.manifestUri)
  if (manifestState.status !== "resolved") {
    return this.assembleOfflineResult(manifestState.reason)
  }
  const contentHash = extractContentHash(manifestState.bytes)
  this.phaseGate.recordResolved(contentHash, manifestState.bytes)

  // Phase 2: Verification
  const keyDocState = await this.adapters.resolver.resolveKeyDocument(
    extractAuthority(manifestState.bytes)
  )
  const keyDocBytes = keyDocState.status === "resolved" ? keyDocState.bytes : undefined
  const verification = await this.adapters.verifier.verifyManifest(
    manifestState.bytes, keyDocBytes
  )
  this.phaseGate.recordVerified(contentHash, verification)

  // Phase 2 → Phase 3 gate (implicit in recordVerified; explicit check here for clarity)
  const verifiedResult = this.phaseGate.requireVerified(contentHash)
  const privacyMode    = verifiedResult.privacyMode
  const contentStatus  = deriveContentStatus(verifiedResult, params)

  // Phase 3: Build (dispatched by privacy mode)
  let rdfIndex: RDFIndex | null = null
  if (privacyMode === "public" || privacyMode === "selective-disclosure") {
    const contentState = await this.adapters.resolver.fetchCid(
      extractContentCid(manifestState.bytes)
    )
    if (contentState.status !== "resolved") {
      return this.assembleMissingCidResult(contentStatus)
    }
    const entailment = this.resolveEntailmentMode(privacyMode, params.entailmentMode)
    rdfIndex = await this.adapters.engine.buildGraph(
      contentState.bytes,
      extractContentFormat(manifestState.bytes),
      params.manifestUri,
      entailment
    )
  } else if (privacyMode === "encrypted") {
    // Mode 2 via query() requires a decryption key.
    // For repeated queries, use openSession() instead.
    if (!params.decryptionKey || !this.adapters.keyDerivation || !this.adapters.decryptor) {
      return this.assembleEncryptedNoKeyResult()
    }
    // Key derivation and decryption handled in SessionManager.buildEncryptedGraph()
    // (See §7.4). Single-query Mode 2 via query() uses a transient session-like
    // path that still respects the zeroing requirements of HQL §16.5.
    rdfIndex = await this.sessionManager.buildEncryptedGraph(
      manifestState.bytes, params.decryptionKey, params.recipientId!, contentHash
    )
  } else {
    // Mode 1, Mode 5, unknown mode — no graph
    return this.assembleNoContentResult(contentStatus)
  }

  // Phase 4: Project
  const projectionState = await this.runProjections(rdfIndex, params, contentStatus)

  // Phase 5: Index (optional)
  // Index building is deferred to a future extension per HQL §18.

  // Phase 6: Query
  const compileResult = this.compiler.compileQDL(
    params.queryDocument,
    { contentStatus, documentGraphName: params.source }
  )
  const rawResult = await this.adapters.engine.executeQuery(compileResult.sparql, projectionState)

  // Phase 7: Result
  return this.assembleResult(rawResult, contentStatus, verifiedResult, compileResult.warnings)
}
```

### 6.5 `ResultAssembler`

`ResultAssembler` translates `RawQueryResult` from `IEngineAdapter` into the typed `QueryResult` defined in HQL §12.1, enriching with `ContentStatus`, completeness, and warnings.

```typescript
class ResultAssembler {
  assemble(
    raw:          RawQueryResult,
    contentStatus: ContentStatus,
    verification: VerificationResult,
    warnings:     string[],
    complete:     boolean,
    completenessReason?: CompletionReason
  ): QueryResult {
    return {
      results: raw.bindings.map(b => this.mapBinding(b)),
      complete,
      completenessReason: complete ? undefined : completenessReason,
      contentStatus,
      identityType: deriveIdentityType(verification),
      warnings
    }
  }
}
```

---

## 7. Session Management

### 7.1 `SessionManager`

`SessionManager` implements the HQL `QuerySession` primitive (HQL §6.4) for Mode 2 encrypted content. Sessions are keyed by **manifest content hash**, not by manifest URI.

**Why content hash, not URI:** A HIRI URI (`hiri://authority/data/person`) is stable across versions — the same URI resolves to V1, V2, V3 as the version chain advances. Using the URI as a session key means opening a session against V2 and then resolving the same URI to V3 would falsely block the new session as a `DUPLICATE_SESSION_IN_CONTEXT`. HQL §6.5.4 keys sessions by content hash. Weaver follows this.

```typescript
export interface ActiveSession {
  readonly sessionId:           string
  readonly contentHash:         string    // Manifest content hash — the session key
  readonly manifestUri:         string    // For logging and display only
  readonly openedAt:            number    // Monotonic timestamp
  readonly openedAtWallClock:   number    // Wall-clock timestamp
  readonly expiresAt:           number    // openedAt + ttl
  readonly options:             QuerySessionOptions
  rdfIndex:                     RDFIndex  // The SessionGraph — held in WASM heap
  active:                       boolean
}

class SessionManager {
  private sessions = new Map<string, ActiveSession>()
  // Key: contentHash → ActiveSession

  constructor(
    private readonly engine:            IEngineAdapter,
    private readonly keyDerivation:     IKeyDerivation,
    private readonly decryptor:         IDecryptor,
    private readonly timestampProvider: ITimestampProvider,
    private readonly phaseGate:         PhaseGate
  ) {
    // Register wake handler for dual-clock TTL checks (HQL §6.4.6)
    this.timestampProvider.onWake(() => this.checkAllSessionExpiry())
    // Register background handler for aggressive close (optional per HQL §6.4.6)
  }

  /**
   * Opens a QuerySession for Mode 2 encrypted content.
   *
   * Preconditions (enforced by PhaseGate):
   *   - manifest must have completed Phase 2 (verified)
   *   - privacyMode must be "encrypted"
   *
   * Key derivation and decryption pipeline (§7.4):
   *   1. PhaseGate.requireVerified(contentHash) — gate check
   *   2. Extract key agreement params from manifest
   *   3. IKeyDerivation.deriveCEK(params) → cek
   *   4. MemoryBudget pre-load check on ciphertext (§7.3)
   *   5. IDecryptor.decryptContent(ciphertext, cek, iv) → plaintext
   *   6. Zero cek immediately (§7.4 step 6)
   *   7. IEngineAdapter.buildGraph(plaintext, ...) → RDFIndex
   *   8. Zero plaintext bytes (§7.4 step 8)
   *   9. MemoryBudget WASM page check (§7.3)
   *  10. Store ActiveSession keyed by contentHash
   */
  async openSession(
    manifestUri:    string,
    manifestBytes:  Uint8Array,
    contentHash:    string,
    decryptionKey:  Uint8Array,  // Transferable ArrayBuffer bytes; zeroed by caller after this call
    recipientId:    string,
    options:        QuerySessionOptions
  ): Promise<QuerySession>

  /**
   * Executes a QDL query against an active session's RDFIndex.
   * Performs dual-clock TTL check before executing (HQL §6.4.6).
   */
  async querySession(
    sessionId:     string,
    queryDocument: object,
    compiler:      Compiler
  ): Promise<QueryResult>

  /**
   * Closes a session: zeros the RDFIndex via engine.releaseIndex(index, true),
   * removes from the active sessions map, and fires expiry callbacks.
   */
  closeSession(sessionId: string): void

  /**
   * Closes all sessions. Called when the last worker tab disconnects (§8.4).
   */
  closeAllSessions(): void

  /**
   * Checks all active sessions for TTL expiry using dual-clock logic.
   * Called by the onWake handler and before every query execution.
   */
  private checkAllSessionExpiry(): void
}
```

### 7.2 Session State and `QuerySessionOptions`

Aligned with HQL §6.4.1:

```typescript
export interface QuerySessionOptions {
  ttl:               number           // Session lifetime in milliseconds; MUST be provided
  entailmentMode?:   EntailmentMode   // Defaults to "none"
  memoryBudget?:     MemoryBudget     // See §7.3
}

export interface MemoryBudget {
  maxInputBytes:  number       // Hard limit on decrypted plaintext before WASM load
  maxWasmPages?:  number       // Soft limit on WASM page growth after buildGraph
}
```

The public `QuerySession` interface exposed to callers:

```typescript
export interface QuerySession {
  readonly sessionId:    string
  readonly contentHash:  string
  readonly active:       boolean

  /**
   * Executes a QDL query against the session's SessionGraph.
   * Performs TTL check before execution.
   * Throws SESSION_EXPIRED if TTL has elapsed.
   */
  query(queryDocument: object): Promise<QueryResult>

  /**
   * Closes the session. Zeros the SessionGraph. Idempotent.
   */
  close(): void
}
```

### 7.3 Memory Budget Enforcement

The `SessionManager` enforces `MemoryBudget` per HQL §6.4.5. The measurement sequence is normative:

```typescript
async function enforceMemoryBudget(
  decryptedBytes: Uint8Array,
  budget:         MemoryBudget,
  engine:         IEngineAdapter
): Promise<void> {

  // Step 1: Hard pre-load check on raw decrypted bytes
  if (decryptedBytes.byteLength > budget.maxInputBytes) {
    decryptedBytes.fill(0)
    throw new WeaverError("SESSION_MEMORY_EXCEEDED",
      `Decrypted content (${decryptedBytes.byteLength} bytes) exceeds ` +
      `maxInputBytes limit (${budget.maxInputBytes} bytes). ` +
      `Content zeroed before WASM load.`)
  }

  // Step 2: Record pre-load WASM page count (soft limit, if observable)
  const pagesBefore = budget.maxWasmPages !== undefined
    ? engine.observeWasmPageCount()
    : null

  // (Caller calls engine.buildGraph after this function returns)
  // Step 3 (post-build): Record post-load page count and check delta
  // This is called by SessionManager after buildGraph() completes.
}

async function enforceWasmPageLimit(
  pagesBefore: number | null,
  budget:      MemoryBudget,
  engine:      IEngineAdapter,
  session:     ActiveSession
): Promise<void> {
  if (pagesBefore === null || budget.maxWasmPages === undefined) return

  const pagesAfter = engine.observeWasmPageCount()
  if (pagesAfter === null) return  // Engine cannot observe; skip soft limit

  const delta = pagesAfter - pagesBefore
  if (delta > budget.maxWasmPages) {
    session.active = false
    await engine.releaseIndex(session.rdfIndex, true)  // zero=true
    throw new WeaverError("SESSION_MEMORY_EXCEEDED",
      `WASM page growth (${delta} pages / ${delta * 65536} bytes) exceeded ` +
      `maxWasmPages soft limit (${budget.maxWasmPages} pages).`)
  }
}
```

### 7.4 Key Derivation Pipeline (Mode 2)

The Phase 3 pipeline branches based on the active decryption adapter. Both paths use `BuildHandle` to guarantee no orphaned WASM memory on error paths.

#### 7.4.1 Split Path (`IKeyDerivation` + `IDecryptor`)

```typescript
async buildEncryptedGraph(
  manifestBytes:  Uint8Array,
  decryptionKey:  Uint8Array,
  recipientId:    string,
  contentHash:    string
): Promise<RDFIndex> {

  const verification = this.phaseGate.requireVerified(contentHash)
  const keyParams    = extractKeyAgreementParams(manifestBytes, recipientId)

  let cek:   Uint8Array | null = null
  let plain: Uint8Array | null = null
  let handle: BuildHandle | null = null

  try {
    // Step 1: Derive CEK
    cek = await this.keyDerivation.deriveCEK({
      ephemeralPublicKey: keyParams.ephemeralPublicKey,
      recipientId,
      iv:                 keyParams.iv,
      encryptedKeyShare:  keyParams.encryptedKeyShare,
      keyAgreement:       keyParams.keyAgreement
    })

    // Step 2: Fetch ciphertext
    const cipherState = await this.resolver.fetchCid(extractCiphertextCid(manifestBytes))
    if (cipherState.status !== "resolved") {
      throw new WeaverError("MISSING_CID", "Ciphertext CID could not be resolved.")
    }

    // Step 3: Decrypt — CEK consumed here
    plain = await this.decryptor.decryptContent(cipherState.bytes, cek, keyParams.iv)

    // Step 4: Zero CEK immediately (HQL §16.5) — before any further async work
    cek.fill(0); cek = null

    // Step 5: MemoryBudget pre-load byte check
    await enforceMemoryBudget(plain, this.memoryBudget, this.engine)

    // Step 6: Begin WASM build — get handle before plaintext is consumed
    const pagesBefore = this.engine.observeWasmPageCount()
    handle = await this.engine.beginBuild({
      content:        plain,
      format:         extractContentFormat(manifestBytes),
      baseURI:        extractManifestUri(manifestBytes),
      entailmentMode: "none"
    })

    // Step 7: Zero plaintext — the engine has its copy in WASM memory now
    plain.fill(0); plain = null

    // Step 8: Commit build
    const rdfIndex = await handle.commit()
    handle = null  // committed — no longer needs abort

    // Step 9: WASM page soft limit check
    await enforceWasmPageLimit(pagesBefore, this.memoryBudget, this.engine, rdfIndex)

    return rdfIndex

  } catch (err) {
    // Zero all sensitive material on any error path
    if (cek   !== null) { cek.fill(0) }
    if (plain !== null) { plain.fill(0) }
    // Abort WASM build handle — zeros and frees any allocated WASM pages
    if (handle !== null) { await handle.abort() }
    throw err
  }
}
```

#### 7.4.2 Enclave Path (`IEnclaveDecryptor`)

The enclave path is simpler at the Weaver level precisely because key material stays inside the enclave. The CEK never crosses into JavaScript.

```typescript
async buildEncryptedGraphEnclave(
  manifestBytes: Uint8Array,
  recipientId:   string,
  contentHash:   string
): Promise<RDFIndex> {

  this.phaseGate.requireVerified(contentHash)

  const cipherState = await this.resolver.fetchCid(extractCiphertextCid(manifestBytes))
  if (cipherState.status !== "resolved") {
    throw new WeaverError("MISSING_CID", "Ciphertext CID could not be resolved.")
  }

  let plain:  Uint8Array | null = null
  let handle: BuildHandle | null = null

  try {
    // Step 1: Atomic enclave decryption — CEK never leaves the enclave
    plain = await this.enclaveDecryptor.decryptManifestContent({
      manifestBytes,
      recipientId,
      ciphertext: cipherState.bytes
    })

    // Step 2: MemoryBudget pre-load check on returned plaintext
    await enforceMemoryBudget(plain, this.memoryBudget, this.engine)

    // Step 3: Begin WASM build
    const pagesBefore = this.engine.observeWasmPageCount()
    handle = await this.engine.beginBuild({
      content:        plain,
      format:         extractContentFormat(manifestBytes),
      baseURI:        extractManifestUri(manifestBytes),
      entailmentMode: "none"
    })

    // Step 4: Zero plaintext — engine has its WASM copy
    plain.fill(0); plain = null

    // Step 5: Commit
    const rdfIndex = await handle.commit()
    handle = null

    await enforceWasmPageLimit(pagesBefore, this.memoryBudget, this.engine, rdfIndex)

    return rdfIndex

  } catch (err) {
    if (plain  !== null) { plain.fill(0) }
    if (handle !== null) { await handle.abort() }
    throw err
  }
}
```

#### 7.4.3 Path Dispatch

`SessionManager` dispatches to the appropriate pipeline based on adapter availability:

```typescript
private async buildEncryptedGraphDispatch(
  manifestBytes:  Uint8Array,
  decryptionKey:  Uint8Array,
  recipientId:    string,
  contentHash:    string
): Promise<RDFIndex> {
  if (this.enclaveDecryptor) {
    // decryptionKey is not used in the enclave path — it may be null or empty
    return this.buildEncryptedGraphEnclave(manifestBytes, recipientId, contentHash)
  }
  if (this.keyDerivation && this.decryptor) {
    return this.buildEncryptedGraph(manifestBytes, decryptionKey, recipientId, contentHash)
  }
  throw new WeaverError(
    "ADAPTER_DEPENDENCY_ERROR",
    "No Mode 2 decryption adapter available. Provide IKeyDerivation + IDecryptor or IEnclaveDecryptor."
  )
}
```

### 7.5 Dual-Clock TTL Enforcement

Called before every `session.query()` and on every wake event:

```typescript
private checkSessionExpiry(session: ActiveSession): void {
  const monotonicElapsed  = this.timestampProvider.monotonicNow() - session.openedAt
  const wallClockElapsed  = this.timestampProvider.wallClockNow() - session.openedAtWallClock

  if (monotonicElapsed >= session.options.ttl || wallClockElapsed >= session.options.ttl) {
    this.closeSession(session.sessionId)
    throw new WeaverError("SESSION_EXPIRED",
      `Session ${session.sessionId} expired. ` +
      `Monotonic elapsed: ${monotonicElapsed}ms. ` +
      `Wall-clock elapsed: ${wallClockElapsed}ms. ` +
      `TTL: ${session.options.ttl}ms.`)
  }
}
```

---

## 8. Worker Host Module — `@weaver/worker`

`@weaver/worker` provides `WeaverWorkerHost`, which runs inside a `SharedWorker` and implements the HQL §6.6 Worker Message Protocol directly — without Comlink or any other abstraction layer.

**Why not Comlink:** Comlink uses `structuredClone` for all parameter passing. `structuredClone` copies `ArrayBuffer` objects rather than transferring them. The HQL §6.6.3 Transferable key transfer requirement — that after `postMessage(msg, [keyBuffer])`, the tab's `keyBuffer.byteLength` MUST be zero — cannot be satisfied by any Comlink-mediated API without explicit and non-standard Transferable configuration. Because the key transfer property is testable (HQL test vector A.11) and is a normative conformance requirement, Weaver MUST implement the protocol directly.

### 8.1 Worker Entry Point

```typescript
// weaver.worker.ts — entry point for the SharedWorker script
import { WeaverWorkerHost } from "@weaver/worker"

// The host application provides adapters via a global init message
// (WorkerInitRequest, type: "worker.init") before any session operations.
const host = new WeaverWorkerHost()

self.addEventListener("connect", (event: MessageEvent) => {
  host.handleConnect(event.ports[0])
})
```

### 8.2 `WeaverWorkerHost`

```typescript
export interface WorkerHostOptions {
  // Adapter factory function. Called after worker.init is received.
  // The host application provides adapter implementations appropriate
  // for the worker environment (browser WASM, Node, etc.)
  adapterFactory: (config: WorkerConfig) => WeaverAdapters
}

export class WeaverWorkerHost {
  private connectedPorts = new Set<MessagePort>()
  private weaver:         Weaver | null = null
  private pendingRequests = new Map<string, { resolve: Function; reject: Function }>()

  constructor(private readonly options: WorkerHostOptions) {}

  /**
   * Called by the SharedWorker "connect" event handler.
   * Registers the new port, attaches message and close listeners.
   */
  handleConnect(port: MessagePort): void {
    this.connectedPorts.add(port)

    port.addEventListener("message", (event: MessageEvent) => {
      this.dispatch(port, event).catch(err => {
        // Uncaught error in dispatch — log but do not crash the worker
        console.error("[WeaverWorker] Unhandled dispatch error:", err)
      })
    })

    port.addEventListener("close", () => {
      this.connectedPorts.delete(port)
      if (this.connectedPorts.size === 0 && this.weaver) {
        // Last tab disconnected — close all sessions (HQL §6.6.6)
        this.weaver.sessionManager.closeAllSessions()
      }
    })

    port.start()
  }

  /**
   * Dispatches an incoming WorkerRequest to the appropriate handler.
   */
  private async dispatch(port: MessagePort, event: MessageEvent): Promise<void> {
    const request = event.data as WorkerRequest

    // Validate: prohibited payload check (HQL §6.6.5)
    this.assertNoProhibitedPayload(request, port)

    switch (request.type) {
      case "worker.init":
        await this.handleInit(port, request as WorkerInitRequest, event)
        break
      case "session.open":
        await this.handleSessionOpen(port, request as WorkerSessionOpenRequest, event)
        break
      case "session.query":
        await this.handleSessionQuery(port, request as WorkerSessionQueryRequest)
        break
      case "session.close":
        await this.handleSessionClose(port, request as WorkerSessionCloseRequest)
        break
      default:
        port.postMessage({
          type: "worker.error",
          requestId: (request as any).requestId,
          error: "UNKNOWN_REQUEST_TYPE"
        })
    }
  }
}
```

### 8.3 Normative Request Handlers

#### `worker.init` Handler

```typescript
private async handleInit(
  port:    MessagePort,
  request: WorkerInitRequest,
  event:   MessageEvent
): Promise<void> {
  try {
    const adapters = this.options.adapterFactory(request.config)
    this.weaver = new Weaver({ adapters })
    await this.weaver.adapters.engine.initialize()

    port.postMessage({
      type:      "worker.init.ok",
      requestId: request.requestId
    } satisfies WorkerInitResponse)
  } catch (err) {
    port.postMessage({
      type:      "worker.init.error",
      requestId: request.requestId,
      error:     err instanceof WeaverError ? err.code : "INIT_FAILED",
      message:   err instanceof WeaverError ? err.message : String(err)
    } satisfies WorkerInitResponse)
  }
}
```

#### `session.open` Handler — Normative Transferable Key Receipt

```typescript
private async handleSessionOpen(
  port:    MessagePort,
  request: WorkerSessionOpenRequest,
  event:   MessageEvent
): Promise<void> {
  if (!this.weaver) {
    port.postMessage({
      type:      "session.open.error",
      requestId: request.requestId,
      error:     "WORKER_NOT_INITIALIZED"
    })
    return
  }

  // Receive the Transferable decryption key (HQL §6.6.3)
  // The ArrayBuffer was transferred (not copied) by the tab.
  // It arrives in event.data._transferredKey per the normative convention.
  const keyBuffer = request._transferredKey as ArrayBuffer
  if (!keyBuffer || keyBuffer.byteLength === 0) {
    port.postMessage({
      type:      "session.open.error",
      requestId: request.requestId,
      error:     "MISSING_DECRYPTION_KEY",
      message:   "Decryption key was not transferred or arrived with byteLength 0."
    })
    return
  }
  const decryptionKey = new Uint8Array(keyBuffer)

  try {
    // Phase 1+2 within the worker — independent verification
    const manifestState = await this.weaver.adapters.resolver.resolveManifest(
      request.manifestUri
    )
    if (manifestState.status !== "resolved") {
      throw new WeaverError("MISSING_CID", `Cannot resolve manifest: ${manifestState.reason}`)
    }
    const contentHash   = extractContentHash(manifestState.bytes)
    this.weaver.phaseGate.recordResolved(contentHash, manifestState.bytes)

    const keyDocState   = await this.weaver.adapters.resolver.resolveKeyDocument(
      extractAuthority(manifestState.bytes)
    )
    const verification  = await this.weaver.adapters.verifier.verifyManifest(
      manifestState.bytes,
      keyDocState.status === "resolved" ? keyDocState.bytes : undefined
    )
    this.weaver.phaseGate.recordVerified(contentHash, verification)

    // Phase 3: Open session
    const session = await this.weaver.sessionManager.openSession(
      request.manifestUri,
      manifestState.bytes,
      contentHash,
      decryptionKey,
      request.recipientId,
      request.options
    )

    // Zero the local key view — the IKeyDerivation adapter has already
    // consumed and zeroed its copy during deriveCEK().
    decryptionKey.fill(0)

    port.postMessage({
      type:          "session.open.ok",
      requestId:     request.requestId,
      sessionId:     session.sessionId,
      contentStatus: "decrypted-verified"
    } satisfies WorkerSessionOpenOkResponse)

  } catch (err) {
    decryptionKey.fill(0)  // Zero on error path too
    port.postMessage({
      type:      "session.open.error",
      requestId: request.requestId,
      error:     err instanceof WeaverError ? err.code : "SESSION_OPEN_FAILED",
      message:   err instanceof WeaverError ? err.message : String(err)
    } satisfies WorkerSessionOpenErrorResponse)
  }
}
```

#### `session.query` Handler

```typescript
private async handleSessionQuery(
  port:    MessagePort,
  request: WorkerSessionQueryRequest
): Promise<void> {
  if (!this.weaver) {
    port.postMessage({
      type: "session.query.error", requestId: request.requestId,
      error: "WORKER_NOT_INITIALIZED"
    })
    return
  }
  try {
    const result = await this.weaver.sessionManager.querySession(
      request.sessionId,
      request.queryDocument,
      this.weaver.compiler
    )
    port.postMessage({
      type:      "session.query.ok",
      requestId: request.requestId,
      result:    serializeQueryResult(result)   // → SerializedQueryResult (plain JSON)
    } satisfies WorkerSessionQueryOkResponse)
  } catch (err) {
    const code = err instanceof WeaverError ? err.code : "QUERY_FAILED"
    // If session expired during query, push expiry notification to all tabs
    if (code === "SESSION_EXPIRED") {
      this.broadcastPush({
        type:      "session.expired",
        sessionId: request.sessionId
      })
    }
    port.postMessage({
      type:      "session.query.error",
      requestId: request.requestId,
      error:     code,
      message:   err instanceof WeaverError ? err.message : String(err)
    })
  }
}
```

#### `session.close` Handler

```typescript
private async handleSessionClose(
  port:    MessagePort,
  request: WorkerSessionCloseRequest
): Promise<void> {
  this.weaver?.sessionManager.closeSession(request.sessionId)
  port.postMessage({
    type:      "session.close.ok",
    requestId: request.requestId
  } satisfies WorkerSessionCloseOkResponse)
}
```

### 8.4 Push Notifications and Prohibited Payload Guard

```typescript
/**
 * Broadcasts a WorkerPush to all connected tab ports (HQL §6.6.7).
 */
private broadcastPush(push: WorkerPush): void {
  for (const port of this.connectedPorts) {
    port.postMessage(push)
  }
}

/**
 * Checks a WorkerRequest for prohibited payload types per HQL §6.6.5.
 * Throws WORKER_SERIALIZATION_ERROR if any prohibited type is detected.
 *
 * Called before any handler. Prevents accidental processing of a
 * non-conformant message even if the tab-side adapter fails.
 */
private assertNoProhibitedPayload(request: WorkerRequest, port: MessagePort): void {
  // Scan for ArrayBuffer fields beyond the expected _transferredKey on session.open
  // and for any object that looks like a SessionGraph, RDFIndex, or decrypted bytes.
  const prohibited = findProhibitedFields(request)
  if (prohibited.length > 0) {
    port.postMessage({
      type:  "worker.error",
      error: "WORKER_SERIALIZATION_ERROR",
      message: `Message contains prohibited payload field(s): ${prohibited.join(", ")}`
    })
    throw new WeaverError("WORKER_SERIALIZATION_ERROR")
  }
}
```

---

## 9. Worker Client Module — `@weaver/worker/client`

`WorkerClient` implements the `SharedWorkerSessionAdapter` interface defined in HQL §6.6.8 and adds a `WorkerStrategy` negotiation layer that gracefully degrades when `SharedWorker` is unavailable (Android Chrome, restricted iOS Safari, and certain enterprise browser policies).

`@weaver/worker/client` has zero imports from `@weaver/core` or `@weaver/worker`. It communicates exclusively via postMessage or, in the `MainThread` strategy, via a direct in-process `WeaverWorkerHost` instance.

### 9.1 `WorkerStrategy` — Capability Negotiation

```typescript
export type WorkerStrategy =
  | "SharedWorker"     // Preferred: one session shared across multiple tabs
  | "DedicatedWorker"  // Degraded: one session per tab, main thread unblocked
  | "MainThread"       // Last resort: session runs on main thread; no unblocking

export interface WorkerCapabilities {
  strategy:                WorkerStrategy
  // True only under SharedWorker strategy. Under DedicatedWorker or MainThread,
  // each WorkerClient instance holds its own independent session.
  crossTabSessionSharing:  boolean
  // True under DedicatedWorker and SharedWorker strategies.
  // False under MainThread — WASM runs on the UI thread.
  offMainThread:           boolean
}
```

**Strategy selection algorithm** (run at `WorkerClient` construction):

```typescript
function selectStrategy(preference?: WorkerStrategy): WorkerCapabilities {
  // 1. If caller specifies a preference, try it first
  // 2. Otherwise auto-detect from the environment

  const canSharedWorker    = typeof SharedWorker    !== "undefined"
  const canDedicatedWorker = typeof Worker          !== "undefined"

  if (preference === "SharedWorker" || (!preference && canSharedWorker)) {
    return { strategy: "SharedWorker", crossTabSessionSharing: true, offMainThread: true }
  }
  if (preference === "DedicatedWorker" || (!preference && canDedicatedWorker)) {
    return { strategy: "DedicatedWorker", crossTabSessionSharing: false, offMainThread: true }
  }
  // MainThread fallback — always available
  return { strategy: "MainThread", crossTabSessionSharing: false, offMainThread: false }
}
```

**Caller awareness:** The caller MUST inspect `WorkerClient.capabilities` after construction. If the application requires cross-tab session sharing and `capabilities.crossTabSessionSharing` is `false`, the application SHOULD surface a warning to the user that each tab will require independent decryption. It MUST NOT silently proceed as if sharing were active.

### 9.2 Strategy Implementations

#### `SharedWorker` Strategy (Preferred)

Backed by a SharedWorker running `WeaverWorkerHost`. All postMessage communication follows HQL §6.6 exactly as specified. Multiple tabs share one `SessionGraph` in the worker heap.

```typescript
class SharedWorkerBackend {
  private readonly port: MessagePort
  constructor(workerScriptUrl: string) {
    const sharedWorker = new SharedWorker(workerScriptUrl)
    this.port = sharedWorker.port
    this.port.start()
  }
  // postMessage and pending-request correlation per §9.3
}
```

#### `DedicatedWorker` Strategy (Degraded)

Backed by a `Worker` (dedicated, per-tab). Each tab has its own worker instance and its own `WeaverWorkerHost`. Sessions are not shared across tabs — each tab decrypts independently. This is the correct fallback on Android Chrome, where `SharedWorker` is not supported.

```typescript
class DedicatedWorkerBackend {
  private readonly worker: Worker
  constructor(workerScriptUrl: string) {
    this.worker = new Worker(workerScriptUrl, { type: "module" })
    // postMessage and pending-request correlation per §9.3
    // Worker receives messages on self.onmessage instead of port.onmessage
  }
}
```

**Behavioral difference from `SharedWorker`:** Under `DedicatedWorker`, `connect` / `close` events on the SharedWorker lifecycle do not apply. The dedicated worker is terminated when the tab closes. All sessions it holds are closed and zeroed by the worker's `beforeunload` equivalent. If the worker is terminated unexpectedly (browser kill), WASM heap memory is reclaimed by the browser — no special zeroing is required because the process is gone.

#### `MainThread` Strategy (Last Resort)

No Worker is created. `WeaverWorkerHost` runs synchronously in the same thread as the UI. The HQL §6.6 postMessage protocol is simulated via an in-process event emitter, preserving API uniformity at the cost of main-thread blocking during WASM graph construction.

```typescript
class MainThreadBackend {
  private readonly host: WeaverWorkerHost
  constructor(adapterFactory: (config: WorkerConfig) => WeaverAdapters) {
    // Import WeaverWorkerHost directly — only valid in MainThread strategy
    // @weaver/worker/client normally imports nothing from @weaver/worker,
    // but MainThread strategy is the one exception, and it is optional.
    this.host = new WeaverWorkerHost({ adapterFactory })
  }

  // In-process "postMessage" simulation: calls host.dispatch() directly
  // and returns the response as a Promise, without going through the
  // message serialization/deserialization cycle.
  // The Transferable key buffer detachment IS still enforced: the client
  // detaches its ArrayBuffer reference before passing to dispatch().
}
```

**When to use `MainThread`:** This strategy exists for environments where neither `SharedWorker` nor `Worker` is available (certain WebView contexts, React Native, or very old browsers). It is also useful in test environments where Worker threads complicate test isolation. Applications SHOULD NOT use `MainThread` in production for Mode 2 content if any other strategy is available — WASM graph construction on the main thread will cause UI jank during `buildGraph`.

**WASM initialization warning:** Under `MainThread`, `IEngineAdapter.initialize()` runs on the UI thread. WASM instantiation typically takes 50–200ms. Applications MUST call `await client.init(config)` eagerly (e.g., on app startup) rather than lazily at session open time to avoid visible UI freezes.

### 9.3 `WorkerClient` — Full Implementation



```typescript
export interface WorkerClientOptions {
  // URL of the worker script running WeaverWorkerHost.
  // Required for SharedWorker and DedicatedWorker strategies.
  workerScriptUrl?: string
  // Explicit strategy preference. If not set, auto-detected from environment.
  strategy?: WorkerStrategy
  // Required only for MainThread strategy.
  adapterFactory?: (config: WorkerConfig) => WeaverAdapters
}

export class WorkerClient implements SharedWorkerSessionAdapter {
  readonly capabilities: WorkerCapabilities
  private readonly backend: SharedWorkerBackend | DedicatedWorkerBackend | MainThreadBackend
  private readonly pending: Map<string, { resolve: Function; reject: Function }>
  private sessionExpiredCallbacks:        ((sessionId: string) => void)[] = []
  private sessionMemoryExceededCallbacks: ((sessionId: string) => void)[] = []

  constructor(options: WorkerClientOptions) {
    this.pending      = new Map()
    this.capabilities = selectStrategy(options.strategy)

    switch (this.capabilities.strategy) {
      case "SharedWorker":
        if (!options.workerScriptUrl) throw new WeaverClientError(
          "MISSING_WORKER_URL", "workerScriptUrl is required for SharedWorker strategy."
        )
        this.backend = new SharedWorkerBackend(options.workerScriptUrl, this.pending, this.handlePush.bind(this))
        break
      case "DedicatedWorker":
        if (!options.workerScriptUrl) throw new WeaverClientError(
          "MISSING_WORKER_URL", "workerScriptUrl is required for DedicatedWorker strategy."
        )
        this.backend = new DedicatedWorkerBackend(options.workerScriptUrl, this.pending, this.handlePush.bind(this))
        break
      case "MainThread":
        if (!options.adapterFactory) throw new WeaverClientError(
          "MISSING_ADAPTER_FACTORY", "adapterFactory is required for MainThread strategy."
        )
        this.backend = new MainThreadBackend(options.adapterFactory, this.pending, this.handlePush.bind(this))
        break
    }
  }

  /**
   * Initializes the worker with adapter configuration.
   * MUST be called before open().
   */
  async init(config: WorkerConfig): Promise<void> {
    return this.sendRequest({ type: "worker.init", config })
  }

  /**
   * Opens a session in the worker.
   *
   * decryptionKey is an ArrayBuffer. After this call resolves,
   * decryptionKey.byteLength WILL be 0 — it has been transferred
   * to the worker heap. This is the expected behavior per HQL §6.6.3.
   *
   * Callers MUST set their reference to null after this call:
   *   const sessionId = await client.open(uri, key, id, opts)
   *   key = null  // key.byteLength is already 0; null prevents confusion
   */
  async open(
    manifestUri:   string,
    decryptionKey: ArrayBuffer,
    recipientId:   string,
    options:       WorkerSessionOptions
  ): Promise<string> {
    const requestId = crypto.randomUUID()

    return new Promise((resolve, reject) => {
      this.pending.set(requestId, { resolve, reject })

      // Transferable send: decryptionKey goes in the transfer list.
      // After this call, decryptionKey.byteLength === 0 in this tab.
      this.port.postMessage(
        {
          type:             "session.open",
          requestId,
          manifestUri,
          recipientId,
          options,
          _transferredKey:  decryptionKey  // Named property per HQL §6.6.3 convention
        },
        [decryptionKey]   // ← Transferable; tab buffer is detached after this line
      )
    })
  }

  /**
   * Executes a QDL query against an open session.
   */
  async query(
    sessionId:     string,
    queryDocument: object
  ): Promise<SerializedQueryResult> {
    return this.sendRequest({
      type: "session.query", sessionId, queryDocument
    })
  }

  /**
   * Explicitly closes a session.
   */
  async close(sessionId: string): Promise<void> {
    return this.sendRequest({ type: "session.close", sessionId })
  }

  /**
   * Registers a callback invoked when the worker broadcasts session.expired.
   */
  onSessionExpired(callback: (sessionId: string) => void): void {
    this.sessionExpiredCallbacks.push(callback)
  }

  /**
   * Registers a callback invoked when the worker broadcasts session.memory.exceeded.
   */
  onSessionMemoryExceeded(callback: (sessionId: string) => void): void {
    this.sessionMemoryExceededCallbacks.push(callback)
  }

  /**
   * Terminates the SharedWorker and clears all pending requests.
   */
  terminate(): void {
    for (const [, { reject }] of this.pending) {
      reject(new WeaverClientError("WORKER_TERMINATED"))
    }
    this.pending.clear()
    this.port.close()
  }

  /**
   * Handles inbound messages from the worker (responses and push events).
   */
  private handleInbound(data: WorkerResponse | WorkerPush): void {
    // Push events (no requestId)
    if (data.type === "session.expired") {
      this.sessionExpiredCallbacks.forEach(cb => cb(data.sessionId))
      return
    }
    if (data.type === "session.memory.exceeded") {
      this.sessionMemoryExceededCallbacks.forEach(cb => cb(data.sessionId))
      return
    }

    // Responses (have requestId)
    const response = data as WorkerResponse & { requestId: string }
    const pending  = this.pending.get(response.requestId)
    if (!pending) return

    this.pending.delete(response.requestId)

    if (response.type.endsWith(".error") || response.type.endsWith(".error")) {
      pending.reject(new WeaverClientError(
        (response as any).error,
        (response as any).message
      ))
    } else {
      // Resolve with the appropriate payload
      if (response.type === "session.open.ok") {
        pending.resolve((response as WorkerSessionOpenOkResponse).sessionId)
      } else if (response.type === "session.query.ok") {
        pending.resolve((response as WorkerSessionQueryOkResponse).result)
      } else if (response.type === "session.close.ok") {
        pending.resolve(undefined)
      } else if (response.type === "worker.init.ok") {
        pending.resolve(undefined)
      } else {
        pending.resolve(data)
      }
    }
  }

  /**
   * Sends a request and returns a Promise that resolves/rejects when
   * the corresponding response arrives.
   */
  private sendRequest(body: Omit<WorkerRequest, "requestId">): Promise<any> {
    const requestId = crypto.randomUUID()
    return new Promise((resolve, reject) => {
      this.pending.set(requestId, { resolve, reject })
      this.port.postMessage({ ...body, requestId })
    })
  }
}
```

### 9.4 Recommended Application Pattern

```typescript
// Application initialization — strategy auto-detected from environment
const client = new WorkerClient({
  workerScriptUrl: "/weaver.worker.js",
  // strategy: "SharedWorker"  // optional; auto-detected if omitted
})

// Inspect capabilities and inform the user if degraded
if (!client.capabilities.crossTabSessionSharing) {
  console.warn(
    `Weaver running in ${client.capabilities.strategy} mode. ` +
    "Each browser tab will decrypt content independently. " +
    "SharedWorker is not available in this environment."
  )
}

// Register lifecycle callbacks before opening sessions
client.onSessionExpired((sessionId) => {
  ui.showSessionExpiredBanner()
  promptReAuthentication()
})
client.onSessionMemoryExceeded((sessionId) => {
  ui.showError("Content too large for this device's memory budget.")
})

// Initialize worker with adapter config (same call regardless of strategy)
await client.init({ /* resolver options */ })

// Open a session — API identical across all strategies
let key = await retrieveDecryptionKey()
const sessionId = await client.open(
  "hiri://authority/private/data",
  key,
  "recipient-alice",
  { ttl: 15 * 60 * 1000 }
)
key = null  // key.byteLength is 0 after transfer; null prevents confusion

// Query repeatedly
const list     = await client.query(sessionId, listQuery)
const filtered = await client.query(sessionId, filterQuery)

// Close explicitly when done
await client.close(sessionId)
```

**Android Chrome / iOS Safari behavior:** Under `DedicatedWorker` strategy, the above code works identically. Each browser tab will independently call `client.open()`, independently decrypt the content, and hold its own `SessionGraph`. The user experience is correct; only the efficiency differs (N decryptions for N tabs instead of 1). Applications that want to warn users about this can inspect `client.capabilities.crossTabSessionSharing`.

**Node.js behavior:** Under `DedicatedWorker` or `MainThread` strategy (Worker threads are available in Node.js but SharedWorker is not), the pattern is identical. The `ITimestampProvider.onWake` no-op is used, so sleep/wake TTL is monotonic-only — which is correct for a server environment.

---

## 10. Error Handling

### 10.1 `WeaverError`

All errors thrown within `@weaver/core` and `@weaver/worker` MUST be instances of `WeaverError`. This ensures error codes are preserved across the postMessage boundary.

```typescript
export class WeaverError extends Error {
  constructor(
    public readonly code:    string,
    message?:                string
  ) {
    super(message ?? code)
    this.name = "WeaverError"
  }
}

export class WeaverClientError extends Error {
  constructor(
    public readonly code:    string,
    message?:                string
  ) {
    super(message ?? code)
    this.name = "WeaverClientError"
  }
}
```

### 10.2 Error Code Registry

All error codes inherit from the HQL §15.1 error registry. Weaver-specific additions:

| Code | Origin | Condition |
|------|--------|-----------|
| `ADAPTER_DEPENDENCY_ERROR` | Weaver | `IKeyDerivation` and `IDecryptor` not provided together, or `IEnclaveDecryptor` combined with split-path adapters |
| `MISSING_WORKER_URL` | WorkerClient | `workerScriptUrl` not provided for `SharedWorker` or `DedicatedWorker` strategy |
| `MISSING_ADAPTER_FACTORY` | WorkerClient | `adapterFactory` not provided for `MainThread` strategy |
| `BUILD_HANDLE_ORPHANED` | IEngineAdapter | Engine detects an uncommitted, unaborted `BuildHandle` (implementation MAY enforce) |
| `INVALID_PHASE_TRANSITION` | PhaseGate | Attempt to record a phase state out of sequence |
| `WORKER_NOT_INITIALIZED` | WeaverWorkerHost | `session.open` or `session.query` received before `worker.init.ok` |
| `UNKNOWN_REQUEST_TYPE` | WeaverWorkerHost | Unrecognized `type` field in WorkerRequest |
| `MISSING_DECRYPTION_KEY` | WeaverWorkerHost | `session.open` arrived with missing or zero-length Transferable |
| `INIT_FAILED` | WeaverWorkerHost | Adapter factory threw during `worker.init` |
| `QUERY_FAILED` | SessionManager | Unexpected error during SPARQL execution |
| `WORKER_TERMINATED` | WorkerClient | `terminate()` called with pending requests outstanding |

All HQL §15.1 codes (`VERIFICATION_REQUIRED`, `SESSION_EXPIRED`, `SESSION_MEMORY_EXCEEDED`, `ENTAILMENT_RESTRICTED_BY_PRIVACY_MODE`, `COMPILATION_ERROR`, `WORKER_SERIALIZATION_ERROR`, `DUPLICATE_SESSION_IN_CONTEXT`, `MISSING_CID`, etc.) apply directly.

---

## 11. Conformance

### 11.1 Conformance Levels

**Level 1: Core Weaver**

Requires: HQL Level 1 conformance

MUST implement:
- All six adapter interfaces (`IResolver`, `IVerifier`, `IEngineAdapter`, `ITimestampProvider`, and stubs for `IKeyDerivation` / `IDecryptor` if Mode 2 is not supported)
- `PhaseGate` state machine with `VERIFICATION_REQUIRED` enforcement
- `Compiler` with Mode 3 `DEFAULT_GRAPH_QUERY_IN_MODE3` warning
- `ResultAssembler` with full `QueryResult` including typed `CompletionReason` and `ContentStatus`
- `Weaver.query()` for public and selective-disclosure content
- `Weaver.verify()` returning full `VerificationResult`
- `WeaverError` class with `code` field

MAY implement:
- `SessionManager` (required for Level 2)
- `@weaver/worker` (required for Level 2 browser)
- `@weaver/worker/client` (required for Level 2 browser)

**Level 2: Full Weaver**

Requires: HQL Level 2 conformance

MUST implement everything in Level 1, plus:
- `SessionManager` with full dual-clock TTL, `MemoryBudget` enforcement, `BuildHandle`-based pipeline, and zeroing semantics
- `IKeyDerivation` and `IDecryptor` adapter interfaces (split path), OR `IEnclaveDecryptor` (enclave path) — at least one path MUST be documented as supported
- `@weaver/worker` implementing HQL §6.6 Worker Message Protocol directly (no Comlink)
- `@weaver/worker/client` with `WorkerStrategy` negotiation covering all three strategies (`SharedWorker`, `DedicatedWorker`, `MainThread`)
- `capabilities` field exposed on `WorkerClient` with accurate `crossTabSessionSharing` and `offMainThread` values
- Transferable `ArrayBuffer` key transfer with detachment verification (all strategies that support Transferable)
- Session keying by content hash (not URI)
- `onWake` and `onBackground` on `ITimestampProvider` (no-op permitted for Node.js)
- `DUPLICATE_SESSION_IN_CONTEXT` enforcement within single UI context
- All HQL test vectors A.1–A.11

### 11.2 Conformance Test Vectors

All HQL §A test vectors apply. Weaver implementations MUST pass:
- A.1–A.5, A.7, A.9 (Level 1)
- A.6, A.8, A.10, A.11 (Level 2)

For A.11 (Worker RPC round-trip): after `client.open()` resolves, the `ArrayBuffer` passed to it MUST have `byteLength === 0`. This is a MUST, not a SHOULD. A conformance test MUST verify this programmatically.

---

## Appendix A: Full Type Reference

All types used in this specification, consolidated for implementer convenience.

```typescript
// Adapter interfaces
export type { IResolver, ResolutionState }
export type { IVerifier, VerificationResult, ChainVerificationResult }
export type { IKeyDerivation, CEKDerivationParams, HMACKeyDerivationParams }
export type { IDecryptor }
export type { IEnclaveDecryptor, EnclaveDecryptParams }   // v1.1
export type { ITimestampProvider }
export type { IEngineAdapter, BuildHandle, BuildParams,   // BuildHandle v1.1
              EntailmentMode, RDFIndex, RDFDataset,
              RawQueryResult, RawBinding }

// Core
export type { WeaverAdapters, WeaverOptions }
export type { QueryParams, OpenSessionParams }

// Session
export type { QuerySessionOptions, MemoryBudget, ActiveSession }
export type { QuerySession }

// Result model (re-exported from HQL)
export type { QueryResult, Binding, RDFTerm, ContentStatus, CompletionReason }

// Worker protocol (re-exported from HQL §6.6)
export type {
  WorkerRequest, WorkerInitRequest, WorkerSessionOpenRequest,
  WorkerSessionQueryRequest, WorkerSessionCloseRequest,
  WorkerResponse, WorkerInitResponse, WorkerSessionOpenOkResponse,
  WorkerSessionOpenErrorResponse, WorkerSessionQueryOkResponse,
  WorkerSessionQueryErrorResponse, WorkerSessionCloseOkResponse,
  WorkerPush, WorkerSessionExpiredPush, WorkerSessionMemoryExceededPush,
  SerializedQueryResult, SerializedBinding, SerializedRDFTerm,
  WorkerSessionOptions, WorkerConfig
}

// Client — v1.1 additions
export type { WorkerStrategy, WorkerCapabilities, WorkerClientOptions }  // v1.1
export type { SharedWorkerSessionAdapter }  // From HQL §6.6.8

// Errors
export { WeaverError, WeaverClientError }
```

---

## Appendix B: Platform Adapter Implementations (Informative)

This appendix provides reference implementations for common deployment environments. These are INFORMATIVE — host applications are responsible for providing conformant adapter implementations appropriate to their environment.

### B.1 Browser `ITimestampProvider`

```typescript
export function createBrowserTimestampProvider(): ITimestampProvider {
  return {
    monotonicNow:  () => performance.now(),
    wallClockNow:  () => Date.now(),
    onWake:        (cb) => {
      document.addEventListener("visibilitychange", () => {
        if (document.visibilityState === "visible") cb()
      })
      window.addEventListener("focus", cb)
      window.addEventListener("pageshow", cb)
    },
    onBackground:  (cb) => {
      document.addEventListener("visibilitychange", () => {
        if (document.visibilityState === "hidden") cb()
      })
    }
  }
}
```

### B.2 Node.js `ITimestampProvider`

```typescript
export function createNodeTimestampProvider(): ITimestampProvider {
  return {
    monotonicNow:  () => Number(process.hrtime.bigint()) / 1_000_000,
    wallClockNow:  () => Date.now(),
    onWake:        (_cb) => { /* no-op: device sleep not applicable */ },
    onBackground:  (_cb) => { /* no-op */ }
  }
}
```

### B.3 Browser `IResolver` (IPFS + fetch)

```typescript
export function createBrowserResolver(gateway: string): IResolver {
  const fetchWithTimeout = async (url: string): Promise<ResolutionState> => {
    try {
      const controller = new AbortController()
      const timeout    = setTimeout(() => controller.abort(), 10_000)
      const response   = await fetch(url, { signal: controller.signal })
      clearTimeout(timeout)
      if (!response.ok) return { status: "unresolved", reason: "not-found" }
      const bytes = new Uint8Array(await response.arrayBuffer())
      return { status: "resolved", bytes }
    } catch (err: any) {
      if (err.name === "AbortError") return { status: "unresolved", reason: "timeout" }
      return { status: "unresolved", reason: "offline" }
    }
  }

  return {
    fetchCid:           (cid)  => fetchWithTimeout(`${gateway}/ipfs/${cid}`),
    resolveManifest:    (uri)  => fetchWithTimeout(hiriUriToGatewayUrl(uri, gateway)),
    resolveKeyDocument: (auth) => fetchWithTimeout(authorityToKeyDocUrl(auth, gateway))
  }
}
```

### B.4 `WorkerClient` Strategy Examples

```typescript
// Browser: auto-detect (SharedWorker if available, DedicatedWorker on Android)
const client = new WorkerClient({ workerScriptUrl: "/weaver.worker.js" })

// Force DedicatedWorker (e.g., testing, or application prefers per-tab isolation)
const client = new WorkerClient({
  workerScriptUrl: "/weaver.worker.js",
  strategy: "DedicatedWorker"
})

// MainThread (React Native, test harness, old WebView)
const client = new WorkerClient({
  strategy: "MainThread",
  adapterFactory: (config) => createAdapters(config)
})

// All three use identical open/query/close API:
const sessionId = await client.open(uri, key, recipientId, opts)
const result    = await client.query(sessionId, qdl)
await client.close(sessionId)
```

## Document History

| Version | Date | Status | Notes |
|---------|------|--------|-------|
| 0.2.0 | 2026-04 | Superseded | Initial design sketch |
| 1.0.0 | 2026-04 | Superseded | Full normative specification: adapter interfaces, PhaseGate, SessionManager, key derivation pipeline, Worker Message Protocol, WorkerClient |
| **1.1.0** | **2026-04** | **Draft** | `WorkerStrategy` fallback chain (`SharedWorker` → `DedicatedWorker` → `MainThread`), `BuildHandle` for WASM error-path memory safety, `IEnclaveDecryptor` for hardware enclave / non-extractable CEK environments |

---

## License

**Specification:** CC0 1.0 Universal (Public Domain)
**Reference Implementations:** Apache 2.0

---

*Weaver is a moat, not a castle.*
*The protocol defines what must be true. Weaver makes it impossible to accidentally make it false.*
