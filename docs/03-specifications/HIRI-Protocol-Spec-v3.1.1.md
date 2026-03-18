# HIRI Protocol Specification

## Verifiable, Edge-Canonical Semantic Knowledge

**Version:** 3.1.1
**Previous:** 3.1.0
**Date:** March 2026
**Status:** Draft
**Supersedes:** HIRI Protocol Specification v2.1.0

---

## Document Status

This specification is a **major version upgrade** from v2.1.0. It introduces breaking changes to authority derivation, canonicalization, content addressing, and version encoding. Implementations conforming to v2.1.0 are NOT interoperable with v3.1.1 without migration (see §17).

### v3.1.1 Revision Notes (from v3.1.0)

v3.1.1 incorporates non-breaking additions from adversarial review, scoped to the protocol layer. No normative semantics changed. Governance, infrastructure, and application-layer concerns remain out of scope — HIRI is a verification primitive, not a trust infrastructure.

| Addition | Section | Nature |
|----------|---------|--------|
| **Normative context registry** | §7.6 | Normative — pins canonical JSON-LD context payloads |
| **Delta atomicity rule** | §11.4.1 | Normative — makes all-or-nothing semantics explicit |
| **Blank node identity in RDF Patch** | §11.4.3 | Normative note |
| **Verification status reporting** | §13.6 | Normative — defines what verifiers report, not what applications decide |
| **TSA priority** | §9.2 | Normative note |
| **Canonicalization resource limits** | §7.7 | Normative — prevents algorithmic DoS |
| **Transport adapter reversibility** | §14.5 | Normative — adapter encodings must round-trip |
| **Expanded test vectors** | Appendix B | Normative — URDNA2015 edge cases, adversarial rejection cases |
| **Determinism checklist** | Appendix E | INFORMATIVE — implementer guidance |

### v3.1.0 Revision Notes (from v3.0.0)

v3.1.0 incorporates four corrections from adversarial architectural review:

| Fix | Severity | Section | Change |
|-----|----------|---------|--------|
| **Delta–canonicalization coupling** | Critical | §11.4 | JSON Patch restricted to JCS profile; RDF Patch required for URDNA2015 |
| **Profile symmetry** | High | §7.3 | Content and signature MUST use the same canonicalization profile |
| **Version type unification** | Medium | §9.2, §11.3 | `hiri:version` is always a JSON String (base-10 integer) |
| **Multibase URI consistency** | Medium | §5.1, §6.1 | Authority in URIs retains `z` multibase prefix |

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Normative References](#2-normative-references)
3. [Terminology](#3-terminology)
4. [Architectural Principles](#4-architectural-principles)
5. [Authority & Identity](#5-authority--identity)
6. [Encoding Standards](#6-encoding-standards)
7. [Canonicalization Profiles](#7-canonicalization-profiles)
8. [Content Addressing](#8-content-addressing)
9. [Resolution Manifests](#9-resolution-manifests)
10. [Signing & Verification](#10-signing--verification)
11. [Chain Integrity](#11-chain-integrity)
12. [URI Resolution](#12-uri-resolution)
13. [Key Lifecycle](#13-key-lifecycle)
14. [Serialization Boundary](#14-serialization-boundary)
15. [RDF Indexing & Query](#15-rdf-indexing--query)
16. [Security Considerations](#16-security-considerations)
17. [Migration from v2.1.0](#17-migration-from-v210)
18. [Conformance Levels](#18-conformance-levels)
19. [Advanced Features](#19-advanced-features)

**Appendices**

- [A: HIRI URI Grammar](#appendix-a-hiri-uri-grammar)
- [B: Normative Test Vectors](#appendix-b-normative-test-vectors)
- [C: Canonicalization Pipeline Details](#appendix-c-canonicalization-pipeline-details)
- [D: Wire Format Examples](#appendix-d-wire-format-examples)
- [E: Determinism Checklist (INFORMATIVE)](#appendix-e-determinism-checklist-informative)

---

## Changelog: v2.1.0 → v3.1.1

| Change | Section | Breaking | Description |
|--------|---------|----------|-------------|
| **Full-key authority** | §5 | YES | Authority contains full base58-encoded public key, not truncated hash |
| **Multibase-consistent URIs** | §5.1, §6.1 | YES | Authority in URIs retains `z` multibase prefix; no parsing exceptions |
| **Canonicalization profiles** | §7 | YES | JCS and URDNA2015 defined as named profiles with explicit negotiation |
| **Profile symmetry** | §7.3 | YES | Content hashing and signature MUST use the same canonicalization profile |
| **Content addressing modes** | §8 | YES | Raw-SHA256 and CIDv1 modes with explicit declaration |
| **Version type unification** | §9.2, §11.3 | YES | `hiri:version` is always a JSON String (base-10 integer) |
| **Delta–canonicalization coupling** | §11.4 | YES | JSON Patch restricted to JCS; RDF Patch required for URDNA2015 |
| **Serialization boundary** | §14 | No | Formal separation of kernel representation and wire format |
| **Signature canonicalization field** | §10 | YES | `hiri:signature` block declares its canonicalization profile |
| **KeyDocument pinning** | §13.5 | No | Clarified: pin target is authority (genesis key), not individual key |
| **Conformance levels** | §18 | No | Three levels: Core, Interoperable, Full |
| **CBOR wire format** | §14.2 | No | dag-cbor defined as the standard wire encoding for networked transport |
| **Normative context registry** | §7.6 | No | Pins canonical JSON-LD context payloads and hashes |
| **Canonicalization resource limits** | §7.7 | No | Prevents algorithmic DoS via pathological blank node graphs |
| **Delta atomicity** | §11.4.1 | No | Explicit all-or-nothing semantics for delta application |
| **Verification status reporting** | §13.6 | No | Defines what verifiers report; separates protocol from policy |
| **Transport adapter reversibility** | §14.5 | No | Adapter encodings must losslessly round-trip |
| **Expanded test vectors** | Appendix B | No | URDNA2015 edge cases, profile/delta rejection, CBOR determinism, status reporting |
| **Determinism checklist** | Appendix E | No | INFORMATIVE implementer guidance |

---

## 1. Introduction

### 1.1 Purpose

HIRI (Hash-IRI) is a protocol for packaging, signing, versioning, and verifying semantic knowledge as self-contained artifacts. It separates data access from trust verification: data can be hosted anywhere, but only the authority's cryptographic signatures make it trustworthy.

### 1.2 Scope

This specification defines:

- Identity and authority derivation from Ed25519 public keys
- Canonicalization and content addressing for deterministic hashing
- Resolution Manifest structure and signing
- Version chain integrity and delta verification
- URI resolution algorithm
- Key lifecycle management (rotation, revocation, temporal verification)
- Serialization boundary between kernel computation and wire transport
- RDF indexing and SPARQL query with entailment control

This specification does NOT define:

- Storage or transport mechanisms (see HIRI-IPFS Integration Spec for IPFS)
- Zero-knowledge proof circuits (see §19 for interface contracts)
- Application-level access control or authorization policies

### 1.3 Normative Interpretation Rule

Any algorithm, table, code block, or prose that describes verification, hashing, signing, canonicalization, encoding, or acceptance/rejection criteria SHALL be interpreted as normative unless explicitly marked INFORMATIVE or OPTIONAL.

### 1.4 Relationship to v2.1.0

This specification supersedes HIRI Protocol Specification v2.1.0 in its entirety. The v2.1.0 "JCS-only" canonicalization and "truncated-hash" authority derivation are preserved as the `core` canonicalization profile and the `v2-legacy` authority format respectively, enabling migration (§17). New implementations MUST implement v3.1.1. Existing v2.1.0 implementations SHOULD migrate per §17.

---

## 2. Normative References

| Specification | Usage |
|---------------|-------|
| RFC 8032 | Ed25519 digital signatures |
| RFC 8785 | JSON Canonicalization Scheme (JCS) |
| W3C RDF Dataset Canonicalization | URDNA2015 algorithm |
| RFC 6902 | JSON Patch (delta format for JCS profile) |
| RDF Patch | Triple-level delta format for URDNA2015 profile (§11.4.3) |
| IPLD dag-cbor | Deterministic CBOR encoding |
| Multibase | Self-describing base encoding |
| Multihash | Self-describing hash encoding |
| CIDv1 | Content identifiers |

---

## 3. Terminology

| Term | Definition |
|------|------------|
| Authority | The HIRI publisher identifier derived from an Ed25519 public key |
| Manifest | A signed Resolution Manifest binding content to an identity |
| Content | The data payload referenced by a manifest's content hash |
| Canonical Form | The deterministic byte sequence used for hashing or signing |
| Profile | A named canonicalization configuration (§7) |
| Kernel | The layer of pure computation with no I/O or non-deterministic calls |
| Adapter | The layer that bridges kernel computation to infrastructure (crypto, storage, RDF engines) |
| Wire Format | The serialization used for network transport or persistent storage |
| Genesis | A version-1 manifest with no predecessor chain link |

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" are interpreted per RFC 2119.

---

## 4. Architectural Principles

### 4.1 Edge-Canonical First Principle

The HIRI kernel MUST run, unmodified, in a browser tab or local Node.js runtime. All verification is local. No network round-trips are required at verification time. The only runtime dependencies are a cryptographic primitive provider (e.g., WebCrypto API) and, for RDF query, a WASM-based graph engine.

### 4.2 Three-Layer Architecture

```
Layer 0: Kernel     — Pure computation. No I/O. No non-deterministic API calls.
Layer 1: Adapters   — Cryptographic providers, storage backends, RDF engines.
Layer 2: Transport  — IPFS, HTTP, filesystem, or any other delivery mechanism.
```

**Invariant:** Layer 0 MUST NOT import from Layer 1 or Layer 2. All external capabilities (hashing, signing, storage, time) are injected as function parameters or interface implementations.

### 4.3 Determinism as Law

Compliant implementations MUST produce bit-for-bit identical outputs for identical inputs when using the same canonicalization profile (§7). Test vectors (Appendix B) are authoritative.

### 4.4 Verification Extensibility

Implementations MUST NOT weaken or bypass verification semantics. Implementations MAY apply stricter validation policies, provided they do not accept inputs that would be rejected by the reference behavior.

---

## 5. Authority & Identity

### 5.1 Authority Derivation

Every HIRI identity starts with an Ed25519 keypair. The **authority** is derived deterministically from the raw 32-byte public key.

```
authority = "key:ed25519:" + base58btc(publicKey)
```

Where `base58btc` produces a multibase string with the standard `z` prefix, encoding the raw 32-byte public key as a 44-45 character string (including the `z`).

The authority retains the `z` multibase prefix in all contexts, including URIs. There are **no parsing exceptions**. Any authority string extracted from a URI can be passed directly to a standard multibase decoding library without modification.

This ensures:

1. **Self-certifying identity:** Anyone who sees a HIRI URI can extract the public key and verify signatures without fetching a KeyDocument first.
2. **Bidirectional derivability:** The authority can be converted to and from the raw public key bytes without loss. This enables direct derivation of IPNS PeerIds, DID document identifiers, and other external identity formats.
3. **No collision risk:** The full 256-bit key space is preserved.
4. **Library compatibility:** Every cryptographic string in HIRI is a valid multibase string, decodable by standard libraries without special-case handling.

#### 5.1.1 Derivation Algorithm

```
Input:  publicKey — Uint8Array of exactly 32 bytes (Ed25519 public key)
        algorithm — string, MUST be "ed25519"

Output: authority — string of form "key:ed25519:z<base58btc-encoded-key>"

Steps:
  1. Verify publicKey.length === 32. If not, reject.
  2. Encode publicKey using multibase base58btc.
     The encoding produces "z" + 43-44 base58 characters.
  3. Return "key:" + algorithm + ":" + encoded string (including the z prefix).
```

#### 5.1.2 Authority ↔ Public Key Round-Trip

```javascript
function deriveAuthority(publicKey, algorithm) {
  if (publicKey.length !== 32) throw new Error('Invalid key length');
  if (algorithm !== 'ed25519') throw new Error('Unsupported algorithm');
  const encoded = base58btc.encode(publicKey);  // Returns 'z' + base58
  return `key:${algorithm}:${encoded}`;          // Retain the 'z' prefix
}

function extractPublicKey(authority) {
  const match = authority.match(/^key:([a-z0-9]+):(z[A-Za-z0-9]+)$/);
  if (!match) throw new Error('Invalid authority format');
  const [_, algorithm, encoded] = match;
  return {
    algorithm,
    publicKey: base58btc.decode(encoded)  // 'z' prefix present; standard library works directly
  };
}
```

**Invariant:** For any valid Ed25519 public key `pk`:
```
extractPublicKey(deriveAuthority(pk, "ed25519")).publicKey === pk
```

#### 5.1.3 HIRI URI Construction

```
hiri://<authority>/<resource-type>/<identifier>
```

Example:
```
hiri://key:ed25519:z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK/data/person-001
hiri://key:ed25519:z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK/key/main
```

Resource types: `data`, `key`, `compact`, `proof`, `vocab`.

### 5.2 Authority Types

| Type | Format | Security Basis | Status |
|------|--------|----------------|--------|
| `key` | `key:ed25519:z<base58btc-pubkey>` | Self-certifying | Normative |
| `domain` | `domain:<fqdn>` | DNS + resolved key | Deferred |
| `consortium` | `consortium:<registry-id>` | Multi-party governance | Deferred |

Only `key`-based authority is normative in v3.1.1. Domain and consortium authorities are defined for future compatibility but MUST NOT be relied upon for verification.

---

## 6. Encoding Standards

### 6.1 Multibase Encoding

| Context | Encoding | Prefix | Rule |
|---------|----------|--------|------|
| Authority (all contexts) | base58btc | `z` | Standard multibase; no exceptions |
| Signature proofValue | base58btc | `z` | Full multibase |
| Public key in KeyDocument | base58btc | `z` | Full multibase |
| Content hash (raw mode) | hex | `f` | Full multibase, with `sha256:` algorithm prefix |
| Content hash (CID mode) | base32lower | `b` | Standard CIDv1 string |

**No Parsing Exceptions:** Every base-encoded string in HIRI, in every context including URIs, uses standard multibase encoding with its prefix character. A developer can pass any authority, signature, or key string directly to a multibase decoding library without modification. This eliminates the class of bugs caused by context-dependent prefix stripping.

### 6.2 Signature Encoding

Signature bytes are encoded as multibase base58btc with `z` prefix:

```
proofValue = "z" + base58btc(signatureBytes)
```

### 6.3 Public Key Encoding

Public keys in KeyDocument `activeKeys` entries use `publicKeyMultibase`:

```
publicKeyMultibase = "z" + base58btc(rawPublicKeyBytes)
```

Note: This is the raw 32-byte Ed25519 public key, NOT wrapped in a multicodec or protobuf envelope. Wrapping for specific transport protocols (e.g., libp2p protobuf for IPFS) is performed by the transport adapter (§14).

---

## 7. Canonicalization Profiles

HIRI v3.1.1 defines two canonicalization profiles. Every manifest and signature declares which profile it uses.

### 7.1 Profile: `JCS`

**JSON Canonicalization Scheme (RFC 8785)**

```
Input:  JSON object
Output: Deterministic UTF-8 byte sequence

Rules:
  - Lexicographic key sorting at all nesting levels
  - No insignificant whitespace
  - ES2015 number serialization
  - Unicode NFC normalization
```

**Properties:**
- Fast, simple, widely available
- Operates on JSON structure, not RDF semantics
- Sufficient for single-authority content where serialization is controlled
- NOT suitable for cross-authority graph merging or RDF-level deduplication

**Implementation:**

```javascript
function canonicalizeJCS(obj) {
  return new TextEncoder().encode(stableStringify(obj));
}
```

Where `stableStringify` implements RFC 8785 deterministic serialization.

### 7.2 Profile: `URDNA2015`

**W3C RDF Dataset Canonicalization**

```
Input:  JSON-LD document + document loader
Output: Deterministic N-Quads string → UTF-8 byte sequence

Rules:
  - JSON-LD expansion and RDF graph construction
  - Blank node canonicalization via URDNA2015
  - Deterministic N-Quads serialization
  - Mandatory secure document loader (no remote context fetching)
```

**Properties:**
- Operates at the RDF graph level — logically equivalent documents produce identical canonical forms
- Required for cross-authority graph merging
- Required for IPFS interoperability (§14)
- Higher computational cost than JCS
- Depends on a JSON-LD processing library

**Implementation:**

```javascript
async function canonicalizeURDNA2015(doc, documentLoader) {
  const nquads = await jsonld.canonize(doc, {
    algorithm: 'URDNA2015',
    format: 'application/n-quads',
    documentLoader  // MUST be a secure loader that blocks remote fetches
  });
  return new TextEncoder().encode(nquads);
}
```

### 7.3 Profile Declaration and Symmetry Rule

Manifests declare their canonicalization profile in two locations:

1. **Content canonicalization** — in `hiri:content.canonicalization`
2. **Signature canonicalization** — in `hiri:signature.canonicalization`

**NORMATIVE: These MUST be identical.** The canonicalization profile declared in `hiri:signature.canonicalization` MUST be the same profile declared in `hiri:content.canonicalization`.

This is the **Profile Symmetry Rule**. It enforces the invariant that what-you-sign-is-what-you-see: the bytes used to compute the content hash and the bytes used to compute the signature are produced by the same canonicalization algorithm. Without this constraint, an attacker could exploit structural differences between JCS and URDNA2015 to construct a manifest where the content hash is valid under one algorithm while the signature verifies under the other, pointing to semantically different data.

```json
{
  "hiri:content": {
    "hash": "sha256:e08da327...",
    "canonicalization": "JCS"
  },
  "hiri:signature": {
    "type": "Ed25519Signature2020",
    "canonicalization": "JCS",
    "proofValue": "z58DAdFfa9..."
  }
}
```

A manifest where `hiri:content.canonicalization` and `hiri:signature.canonicalization` differ MUST be rejected by the verifier.

### 7.4 Profile Requirements by Conformance Level

| Profile | Core (§18.1) | Interoperable (§18.2) | Full (§18.3) |
|---------|-------------|----------------------|--------------|
| JCS | REQUIRED | REQUIRED | REQUIRED |
| URDNA2015 | OPTIONAL | REQUIRED | REQUIRED |

All implementations MUST support JCS. Implementations claiming Interoperable or Full conformance MUST also support URDNA2015.

### 7.5 Document Loader Security

When using the URDNA2015 profile, implementations MUST use a secure document loader that:

1. MUST NOT fetch remote URLs
2. MUST resolve contexts from an embedded or pinned registry
3. MUST throw an error for unknown context URIs

```javascript
const EMBEDDED_CONTEXTS = {
  'https://hiri-protocol.org/spec/v3.1': { /* ... */ },
  'https://w3id.org/security/v2': { /* ... */ }
};

function createSecureDocumentLoader() {
  return async (url) => {
    if (EMBEDDED_CONTEXTS[url]) {
      return { document: EMBEDDED_CONTEXTS[url], documentUrl: url };
    }
    throw new Error(`Unknown context: ${url}`);
  };
}
```

### 7.6 Normative Context Registry

Implementations using the URDNA2015 profile MUST embed or pin the following JSON-LD contexts. These are the canonical payloads for HIRI v3.1.1. Context content is identified by its SHA-256 hash; implementations SHOULD verify context integrity at build time.

| Context URL | SHA-256 (of canonical payload) | Status |
|-------------|-------------------------------|--------|
| `https://hiri-protocol.org/spec/v3.1` | Published at protocol release | REQUIRED |
| `https://w3id.org/security/v2` | Published at protocol release | REQUIRED |

**Context Versioning:** The HIRI context URL includes the spec version. A v3.1.1 manifest MUST reference `https://hiri-protocol.org/spec/v3.1`. Manifests referencing unknown context versions MUST be rejected by the verifier.

**Non-Standard Contexts:** Manifests that require additional JSON-LD contexts beyond the two above MUST include a `hiri:contextCatalog` field in the manifest, mapping each additional context URL to its SHA-256 hash:

```json
{
  "hiri:contextCatalog": {
    "https://schema.org/": "sha256:<hash-of-pinned-schema-org-context>"
  }
}
```

The verifier MUST reject any manifest that references a context URL not in the embedded registry AND not in the manifest's `hiri:contextCatalog`. This prevents silent reliance on remote context fetching.

### 7.7 Canonicalization Resource Limits

URDNA2015 blank node canonicalization has worst-case exponential complexity for pathological inputs. Implementations MUST enforce resource limits during canonicalization to prevent algorithmic denial-of-service:

| Resource | Recommended Limit | Behavior on Exceed |
|----------|-------------------|-------------------|
| Blank nodes per document | 1,000 | Reject before canonicalization |
| Canonicalization wall-clock time | 5 seconds | Abort and reject |
| N-Quads output size | 10 MB | Abort and reject |

These limits are RECOMMENDED defaults. Implementations MAY adjust them, but MUST enforce *some* limit for each resource. Implementations MUST NOT attempt unbounded canonicalization.

Rejection due to resource limits MUST produce a specific error (e.g., `CANONICALIZATION_RESOURCE_EXCEEDED`) distinct from canonicalization failure, so the caller can distinguish pathological input from legitimate large documents.

---

## 8. Content Addressing

HIRI v3.1.1 defines two content addressing modes.

### 8.1 Mode: `raw-sha256`

Content hash is computed directly over the canonicalized bytes.

```
Input:  canonicalBytes — output of the declared canonicalization profile
Output: "sha256:" + hex(SHA-256(canonicalBytes))
```

**Properties:**
- Simple, no dependencies beyond SHA-256
- Hash is a prefixed hex string
- Suitable for local verification and edge-canonical deployments
- NOT directly usable as an IPFS CID

### 8.2 Mode: `cidv1-dag-cbor`

Content is wrapped in a dag-cbor envelope before hashing, producing a CIDv1.

```
Input:  canonicalBytes — output of the declared canonicalization profile
        profile — the canonicalization profile name

Output: CIDv1 with codec dag-cbor (0x71) and hash sha2-256 (0x12)

Steps:
  1. Construct CBOR payload:
     {
       '@type': 'hiri:CanonicalContent',
       'hiri:canonicalization': profile,
       'hiri:content': canonicalBytes
     }
  2. Encode payload as deterministic dag-cbor bytes
  3. Compute SHA-256 multihash of the dag-cbor bytes
  4. Construct CIDv1: version=1, codec=0x71, hash=multihash
  5. Return CID as base32lower multibase string (prefix 'b')
```

**Properties:**
- Directly usable as an IPFS content address
- Content is self-describing (includes canonicalization metadata)
- Requires dag-cbor library
- Required for IPFS interoperability

### 8.3 Mode Declaration

The content addressing mode is declared in `hiri:content.addressing`:

```json
{
  "hiri:content": {
    "hash": "sha256:e08da327...",
    "addressing": "raw-sha256",
    "canonicalization": "JCS",
    "format": "application/ld+json",
    "size": 487
  }
}
```

Or for CIDv1:

```json
{
  "hiri:content": {
    "hash": "bafyreig5xkya...",
    "addressing": "cidv1-dag-cbor",
    "canonicalization": "URDNA2015",
    "format": "application/ld+json",
    "size": 487
  }
}
```

### 8.4 Mode Requirements by Conformance Level

| Mode | Core (§18.1) | Interoperable (§18.2) | Full (§18.3) |
|------|-------------|----------------------|--------------|
| raw-sha256 | REQUIRED | REQUIRED | REQUIRED |
| cidv1-dag-cbor | OPTIONAL | REQUIRED | REQUIRED |

### 8.5 Hash Algorithm Registry

Implementations MUST dispatch content hash verification through a registry that parses the hash prefix or CID codec, not through hardcoded algorithm calls.

```typescript
interface HashAlgorithm {
  readonly prefix: string;
  hash(content: Uint8Array): Promise<string>;
  verify(content: Uint8Array, hash: string): Promise<boolean>;
}

interface HashRegistry {
  register(algorithm: HashAlgorithm): void;
  resolve(prefixedHash: string): HashAlgorithm;
  hash(content: Uint8Array, prefix?: string): Promise<string>;
  verify(content: Uint8Array, prefixedHash: string): Promise<boolean>;
}
```

The registry MUST ship with at least `SHA256Algorithm`. Implementations supporting `cidv1-dag-cbor` MUST additionally register a `CIDv1Algorithm`.

---

## 9. Resolution Manifests

### 9.1 Manifest Structure

```json
{
  "@context": [
    "https://hiri-protocol.org/spec/v3.1",
    "https://w3id.org/security/v2"
  ],
  "@id": "hiri://key:ed25519:z<authority>/data/<identifier>",
  "@type": "hiri:ResolutionManifest",

  "hiri:version": "1",
  "hiri:branch": "main",

  "hiri:timing": {
    "created": "<ISO-8601>"
  },

  "hiri:content": {
    "hash": "<content-hash>",
    "addressing": "<raw-sha256 | cidv1-dag-cbor>",
    "canonicalization": "<JCS | URDNA2015>",
    "format": "application/ld+json",
    "size": "<byte-count>"
  },

  "hiri:chain": {
    "previous": "<manifest-hash>",
    "genesisHash": "<genesis-manifest-hash>",
    "depth": 2,
    "previousBranch": "main"
  },

  "hiri:delta": {
    "hash": "<delta-hash>",
    "format": "<application/json-patch+json | application/rdf-patch>",
    "appliesTo": "<previous-content-hash>",
    "operations": 3
  },

  "hiri:semantics": {
    "entailmentMode": "none"
  },

  "hiri:signature": {
    "type": "Ed25519Signature2020",
    "canonicalization": "<JCS | URDNA2015>",
    "created": "<ISO-8601>",
    "verificationMethod": "hiri://key:ed25519:z<authority>/key/main#key-1",
    "proofPurpose": "assertionMethod",
    "proofValue": "<z-prefixed-base58btc-signature>"
  }
}
```

### 9.2 Field Semantics

**`hiri:version`** — A JSON String representing a base-10 unsigned integer. Version `"1"` is genesis. Strictly monotonically increasing. Implementations parse this string into their native 64-bit integer type (BigInt in JavaScript, u64 in Rust, uint64 in Go). The string encoding eliminates the class of precision-loss bugs caused by JSON number types in languages with IEEE 754 double-precision floats. See §11.3.

**`hiri:branch`** — String identifier for the version branch. Default: `"main"`. Branching semantics are OPTIONAL in v3.1.1.

**`hiri:content.addressing`** — REQUIRED. Declares the content addressing mode. Verifiers MUST dispatch to the correct verification algorithm based on this field.

**`hiri:content.canonicalization`** — REQUIRED. Declares how the content was canonicalized before hashing.

**`hiri:signature.canonicalization`** — REQUIRED in v3.1.1. Declares how the manifest was canonicalized before signing. MUST be identical to `hiri:content.canonicalization` (Profile Symmetry Rule, §7.3). This field was absent in v2.1.0 (which assumed JCS implicitly).

**`hiri:chain`** — MUST be absent for genesis manifests (version `"1"` with no predecessor). MUST be present for all non-genesis manifests.

**`hiri:delta`** — OPTIONAL. When present, contains the delta from the previous version's content to this version's content. The delta format MUST correspond to the manifest's canonicalization profile: `application/json-patch+json` for JCS, `application/rdf-patch` for URDNA2015 (§11.4).

**`hiri:delta.operations`** — For JSON Patch, this is the number of RFC 6902 operations (integer). For RDF Patch, this is the number of add/remove operations (integer).

**`hiri:timing.created`** — REQUIRED. ISO 8601 timestamp of manifest creation. This timestamp is advisory unless accompanied by a TSA proof. It is an injected parameter (§16.3), never derived from the system clock.

**`hiri:timing.timestampProof`** — OPTIONAL. When present, contains a Timestamp Authority proof anchoring the `created` timestamp to an external time source. When `timestampProof` is present and verifiable, it takes precedence over `created` for all temporal decisions (grace period computation, retroactive revocation boundaries). See §13.6 for verifier reporting semantics.

**`hiri:semantics.entailmentMode`** — Declares the RDF entailment regime. Values: `"none"` (default, REQUIRED), `"materialized"` (OPTIONAL), `"runtime"` (OPTIONAL). Only `"none"` is normative in v3.1.1.

### 9.3 Genesis Manifest Rules

A manifest is genesis if and only if `hiri:version === "1"` AND `hiri:chain` is absent.

| Version | Chain Present | Valid |
|---------|---------------|-------|
| `"1"` | No | YES — genesis |
| `"1"` | Yes | YES — V1 can optionally chain |
| > `"1"` | No | NO — non-genesis MUST chain |
| > `"1"` | Yes | YES — standard chained manifest |

---

## 10. Signing & Verification

### 10.1 Signing Algorithm

```
Input:
  manifest — unsigned manifest (complete except hiri:signature.proofValue)
  privateKey — Ed25519 private key
  profile — canonicalization profile name ("JCS" or "URDNA2015")
  timestamp — ISO 8601 string (injected, never from system clock)
  crypto — CryptoProvider interface

Output:
  signedManifest — manifest with hiri:signature.proofValue populated

Precondition:
  manifest['hiri:content']['canonicalization'] MUST equal profile (Profile Symmetry Rule, §7.3)

Steps:
  1. Verify Profile Symmetry: if manifest.content.canonicalization !== profile, reject.
  2. Construct the signature metadata block:
     {
       "type": "Ed25519Signature2020",
       "canonicalization": profile,
       "created": timestamp,
       "verificationMethod": "<key-uri>#<key-id>",
       "proofPurpose": "assertionMethod"
     }
  3. Attach this block as hiri:signature (without proofValue).
  4. Canonicalize the entire manifest (including signature metadata, excluding proofValue)
     using the declared profile:
     - JCS:       canonicalBytes = stableStringify(manifest) → UTF-8 bytes
     - URDNA2015: canonicalBytes = URDNA2015(manifest, secureDocLoader) → UTF-8 N-Quads bytes
  5. Sign:   signatureBytes = Ed25519_Sign(privateKey, canonicalBytes)
  6. Encode: proofValue = "z" + base58btc(signatureBytes)
  7. Attach proofValue to hiri:signature.
  8. Return the complete signed manifest.
```

### 10.2 Verification Algorithm

```
Input:
  manifest — signed manifest
  publicKey — Ed25519 public key (Uint8Array, 32 bytes)
  crypto — CryptoProvider interface

Output:
  boolean — true if signature is valid

Steps:
  1. Extract proofValue from hiri:signature.
  2. Extract canonicalization profile from hiri:signature.canonicalization.
     If absent, assume "JCS" (v2.1.0 backward compatibility).
  3. Enforce Profile Symmetry: if hiri:signature.canonicalization is present AND
     differs from hiri:content.canonicalization, reject immediately.
  4. Reconstruct unsigned manifest:
     Remove proofValue from hiri:signature (keep all other signature fields).
  5. Canonicalize using the declared profile:
     - JCS:       canonicalBytes = stableStringify(manifest) → UTF-8 bytes
     - URDNA2015: canonicalBytes = URDNA2015(manifest, secureDocLoader) → UTF-8 N-Quads bytes
  6. Decode signature: signatureBytes = base58btc.decode("z" + proofValue.slice(1))
  7. Verify: Ed25519_Verify(publicKey, canonicalBytes, signatureBytes)
  8. Return result.
```

### 10.3 CryptoProvider Interface

The kernel MUST NOT import cryptographic libraries directly. All operations are injected:

```typescript
interface CryptoProvider {
  hash(bytes: Uint8Array): Promise<string>;
  sign(bytes: Uint8Array, privateKey: Uint8Array): Promise<Uint8Array>;
  verify(bytes: Uint8Array, signature: Uint8Array, publicKey: Uint8Array): Promise<boolean>;
}
```

### 10.4 Manifest Hashing

The hash of a signed manifest (used in `hiri:chain.previous`) is computed over the **complete signed manifest** including the signature:

```
manifestHash = hash(canonicalize(signedManifest))
```

The canonicalization profile used for manifest hashing is the same as declared in `hiri:signature.canonicalization`. This ensures that a re-signed manifest with a different key produces a different hash, making the chain tamper-evident at the signature level.

---

## 11. Chain Integrity

### 11.1 Chain Link Validation

Six rules are checked at each link:

1. **ID consistency** — `@id` is identical across all manifests in the chain
2. **Version monotonicity** — each version > previous version (strictly increasing)
3. **Previous hash** — `chain.previous` matches the computed hash of the predecessor manifest
4. **Genesis immutability** — `chain.genesisHash` is constant throughout the chain
5. **Depth accuracy** — `chain.depth` increments correctly
6. **Branch consistency** — `chain.previousBranch` matches the predecessor's branch

### 11.2 Chain Walking

```typescript
async function verifyChain(
  head: ResolutionManifest,
  publicKey: Uint8Array,
  fetchManifest: (hash: string) => Promise<Uint8Array | null>,
  fetchContent: (hash: string) => Promise<Uint8Array | null>,
  crypto: CryptoProvider
): Promise<ChainWalkResult>
```

The chain walker traverses `chain.previous` links from head to genesis, verifying signatures and chain link rules at each step. When delta verification fails, the walker falls back to full content hash comparison and records a warning.

```typescript
interface ChainWalkResult {
  valid: boolean;
  depth: number;
  reason?: string;
  warnings: string[];
  manifests: ResolutionManifest[];
}
```

### 11.3 Version Encoding

`hiri:version` MUST be encoded as a **JSON String** containing a base-10 representation of an unsigned integer. The value MUST be ≥ 1.

**Rationale:** Heterogeneous types (a field that can be a number OR a string depending on magnitude) are a deserialization hazard in strictly typed languages (Rust, Go, Swift, Java). They force custom unmarshalers for a single field. The industry standard for 64-bit identifiers in JSON (Twitter/X Snowflake IDs, GraphQL IDs) is universal string encoding. HIRI follows this convention.

```json
{
  "hiri:version": "1"
}
```

```json
{
  "hiri:version": "9007199254740993"
}
```

**Parsing:**

```javascript
function parseVersion(manifest) {
  const v = manifest['hiri:version'];

  if (typeof v !== 'string') {
    throw new Error(`hiri:version MUST be a string, got ${typeof v}`);
  }

  const parsed = BigInt(v);
  if (parsed < 1n) throw new Error(`Invalid version: ${v}`);
  return parsed;
}

function encodeVersion(version) {
  return BigInt(version).toString();
}
```

```rust
// Rust: deserializes directly into u64 from a JSON string
#[derive(Deserialize)]
struct Manifest {
    #[serde(rename = "hiri:version")]
    #[serde(deserialize_with = "deserialize_string_u64")]
    version: u64,
}
```

**Monotonicity:**

```
∀ n > 0: parseVersion(manifest[n]) > parseVersion(manifest[n-1])
```

Versions must be strictly increasing. Gaps are allowed.

**v2.1.0 Compatibility:** v2.1.0 implementations that encoded version as a JSON Number SHOULD be accepted during migration. Verifiers encountering a JSON Number for `hiri:version` SHOULD parse it as if it were a string, but MUST emit a warning. New manifests MUST use string encoding.

### 11.4 Delta Verification

#### 11.4.1 The Delta–Canonicalization Coupling Rule

**NORMATIVE: The delta format MUST be coupled to the manifest's canonicalization profile.** This is not optional or advisory.

JSON Patch (RFC 6902) operates on the structural syntax tree of a JSON document — it uses JSON Pointer paths like `/schema:address/schema:addressLocality` that depend on exact key ordering and nesting. This is safe when the canonical form is structural (JCS), because JCS guarantees a single deterministic JSON representation for any logical object.

However, URDNA2015 canonicalization operates at the RDF graph level. Two JSON-LD documents that produce identical RDF graphs may have completely different JSON structures (different key order, compacted vs. expanded form, different blank node labels). A JSON Patch computed against one structural representation will fail with path errors when applied to a semantically equivalent but structurally different representation. This is not a theoretical risk — it is the expected behavior of any adapter that compacts, expands, or re-frames JSON-LD.

**Delta Atomicity:** Delta application is atomic. Either all operations succeed and the resulting hash matches `hiri:content.hash`, or the entire delta is discarded and the verifier falls back to full content verification. Partial application MUST NOT be attempted. This applies to both JSON Patch and RDF Patch. The chain walker MUST NOT report a delta as partially valid.

#### 11.4.2 Delta Format by Profile

| Canonicalization Profile | Permitted Delta Format | Format Identifier |
|--------------------------|----------------------|-------------------|
| JCS | JSON Patch (RFC 6902) | `application/json-patch+json` |
| URDNA2015 | RDF Patch | `application/rdf-patch` |

**JCS + JSON Patch:** The delta contains RFC 6902 operations against the JCS-canonicalized JSON structure. Because JCS produces a unique structural representation, the patch paths are stable.

**URDNA2015 + RDF Patch:** The delta contains triple-level operations (add/remove) against the canonical N-Quads representation. The patch operates on the RDF graph, not the JSON syntax tree, making it immune to structural reformatting.

#### 11.4.3 RDF Patch Format

RDF Patch operations are encoded as a JSON array of triple-level add/remove instructions:

```json
{
  "hiri:delta": {
    "hash": "sha256:<delta-hash>",
    "format": "application/rdf-patch",
    "appliesTo": "<previous-content-hash>",
    "operations": [
      {
        "op": "remove",
        "subject": "<http://example.org/person-001>",
        "predicate": "<http://schema.org/addressLocality>",
        "object": "\"Portland\""
      },
      {
        "op": "add",
        "subject": "<http://example.org/person-001>",
        "predicate": "<http://schema.org/addressLocality>",
        "object": "\"Seattle\""
      }
    ]
  }
}
```

Each operation specifies a subject, predicate, and object in N-Quads notation. The operations are applied in order. The result is a modified RDF graph that is then re-canonicalized via URDNA2015 and hashed for verification.

**Blank Node Identity:** RDF Patch operations that reference blank nodes MUST use the canonical blank node identifiers produced by URDNA2015 (e.g., `_:c14n0`, `_:c14n1`). These identifiers are stable across canonicalization runs for the same graph. However, adding or removing triples that participate in blank node subgraphs may cause URDNA2015 to reassign canonical identifiers in the resulting graph. Implementations MUST NOT assume blank node identifiers are stable across patch application — the post-patch graph is re-canonicalized independently, and the resulting N-Quads are hashed as-is.

#### 11.4.4 Delta Verification Pipeline (JCS Profile)

When `hiri:delta` is present and the manifest's canonicalization profile is JCS:

1. Fetch previous content bytes from storage
2. Verify previous content hash matches `delta.appliesTo`
3. Parse previous content bytes as JSON
4. Apply JSON Patch (RFC 6902) operations
5. Canonicalize the result via JCS (stableStringify)
6. Hash the canonical bytes
7. Compare to current `hiri:content.hash`

On failure at any step, the walker falls back to fetching and verifying full content directly.

#### 11.4.5 Delta Verification Pipeline (URDNA2015 Profile)

When `hiri:delta` is present and the manifest's canonicalization profile is URDNA2015:

1. Fetch previous content bytes from storage
2. Verify previous content hash matches `delta.appliesTo`
3. Parse previous content as JSON-LD
4. Canonicalize previous content via URDNA2015 to N-Quads
5. Parse N-Quads into a set of quads
6. Apply RDF Patch operations (add/remove) to the quad set
7. Serialize the modified quad set as canonical N-Quads
8. Hash the canonical bytes
9. Compare to current `hiri:content.hash`

On failure at any step, the walker falls back to fetching and verifying full content directly.

#### 11.4.6 Delta Format Mismatch Rejection

If a manifest declares canonicalization profile `URDNA2015` but contains a delta with format `application/json-patch+json`, the verifier MUST reject the delta and fall back to full content verification, emitting a warning. The converse (JCS profile with `application/rdf-patch`) MUST also be rejected.

---

## 12. URI Resolution

### 12.1 Resolution Algorithm

```
Input:
  uri — HIRI URI string
  storage — StorageAdapter implementation
  options — { crypto, publicKey, manifestHash, keyDocument?, verificationTime? }

Output:
  VerifiedContent — { content, contentHash, manifest, authority, warnings }

Steps:
  1. Parse URI → authority, resourceType, identifier
  2. Derive public key from authority (§5.1.2)
  3. Verify authority matches the provided publicKey
  4. Fetch manifest bytes from storage using manifestHash
  5. Verify manifest hash matches
  6. Parse manifest JSON
  7. Verify manifest signature (§10.2) using publicKey
  8. If keyDocument provided: verify with key lifecycle (§13)
  9. If chain present: walk and verify chain (§11.2)
  10. Fetch content bytes from storage using manifest.content.hash
  11. Verify content hash (§8) using declared addressing mode
  12. Return verified content with metadata
```

### 12.2 Storage Adapter Interface

```typescript
interface StorageAdapter {
  get(hash: string): Promise<Uint8Array | null>;
  has(hash: string): Promise<boolean>;
}
```

The resolver is storage-agnostic. It works identically with in-memory maps, filesystem adapters, IPFS adapters, or any implementation of this two-method interface.

### 12.3 Resolution Errors

| Code | Meaning |
|------|---------|
| `MANIFEST_NOT_FOUND` | Manifest hash not in storage |
| `STORAGE_CORRUPTION` | Content hash mismatch |
| `SIGNATURE_VERIFICATION_FAILED` | Signature invalid |
| `AUTHORITY_MISMATCH` | URI authority doesn't match derived authority |
| `CHAIN_VERIFICATION_FAILED` | Chain walk found invalid link |
| `KEY_LIFECYCLE_REJECTED` | Key revoked or expired |

---

## 13. Key Lifecycle

### 13.1 Key States

| Status | Meaning | Manifests Signed By This Key |
|--------|---------|------------------------------|
| `active` | Key is currently valid | Accepted |
| `rotated-grace` | Key rotated, within grace period | Accepted with warning |
| `rotated-expired` | Key rotated, grace period expired | Rejected |
| `revoked` | Key revoked (compromise suspected) | Rejected after `manifestsInvalidAfter` |
| `unknown` | Key not in KeyDocument | Rejected |

### 13.2 KeyDocument Structure

```json
{
  "@context": ["https://hiri-protocol.org/spec/v3.1", "https://w3id.org/security/v2"],
  "@id": "hiri://key:ed25519:z<authority>/key/main",
  "@type": "hiri:KeyDocument",

  "hiri:version": "1",
  "hiri:authority": "key:ed25519:z<authority>",
  "hiri:authorityType": "key",

  "hiri:activeKeys": [{
    "@id": "hiri://key:ed25519:z<authority>/key/main#key-1",
    "@type": "Ed25519VerificationKey2020",
    "controller": "hiri://key:ed25519:z<authority>/key/main",
    "publicKeyMultibase": "z<base58btc-encoded-32-byte-key>",
    "purposes": ["assertionMethod"],
    "validFrom": "<ISO-8601>"
  }],

  "hiri:rotatedKeys": [],
  "hiri:revokedKeys": [],

  "hiri:policies": {
    "gracePeriodAfterRotation": "P180D",
    "minimumKeyValidity": "P365D"
  },

  "hiri:signature": { "..." : "..." }
}
```

### 13.3 Temporal Verification

```typescript
function resolveSigningKey(
  manifest: ResolutionManifest,
  keyDocument: KeyDocument,
  verificationTime: string  // ISO 8601, injected
): KeyVerificationResult
```

Returns `{ keyStatus, valid, keyId, warning? }`.

The verifier checks:
1. Which key in the KeyDocument matches the manifest's `verificationMethod`
2. The temporal validity of that key at `verificationTime`
3. Grace period boundaries (computed from `rotatedAt` + `gracePeriodAfterRotation`)
4. Retroactive revocation (`manifestsInvalidAfter`)

### 13.4 Rotation Proof

Key rotation requires a **dual-signature proof**: both the old key and the new key MUST sign a rotation claim.

```typescript
interface RotationClaim {
  oldKeyId: string;
  newKeyId: string;
  rotatedAt: string;
  reason: string;
}
```

The signing target is `stableStringify(rotationClaim)`. Both keys sign the same canonical bytes. Verification reconstructs the claim from the `RotatedKey` entry and verifies both signatures.

### 13.5 KeyDocument Pinning

When implementations cache or pin KeyDocuments for trust-on-first-use:

- The **pin target** is the authority string (derived from the genesis key), NOT any individual key within the document.
- The authority is immutable — it derives from the first public key and never changes, even after rotation.
- KeyDocument content evolves (keys are added, rotated, revoked), but the authority it governs remains constant.
- If the authority in a fetched KeyDocument does not match the pinned authority, the implementation MUST reject.

### 13.6 Verification Status Reporting

The verifier MUST report the revocation and freshness status of every signature it evaluates. The verifier reports *information* — the application decides what to do with it.

**Required status fields:**

| Field | Values | Meaning |
|-------|--------|---------|
| `signatureValid` | `true`, `false` | Cryptographic signature verification result |
| `keyStatus` | `active`, `rotated-grace`, `rotated-expired`, `revoked`, `unknown` | Key lifecycle state at verification time |
| `revocationStatus` | `confirmed-valid`, `confirmed-revoked`, `unknown` | Whether revocation state could be determined |
| `timestampVerification` | `tsa-verified`, `advisory-only`, `absent` | Strength of the timestamp evidence |

**The `unknown` revocation status:** If the verifier cannot access a current KeyDocument (e.g., offline operation, stale cache), it MUST report `revocationStatus: "unknown"`. It MUST NOT report a signature as unconditionally `valid` when revocation status is undetermined.

**TSA priority:** When `hiri:timing.timestampProof` is present and verifiable, the TSA-anchored timestamp takes precedence over `hiri:timing.created` for all temporal decisions (grace period computation, retroactive revocation boundary). When absent, `hiri:timing.created` is advisory and the verifier SHOULD note `timestampVerification: "advisory-only"` in its report.

**Architectural note:** The verifier reports status. The application interprets it. A browser demo might accept `revocationStatus: "unknown"` with a visual warning. An enterprise deployment might reject it. A regulated environment might require `tsa-verified` timestamps. These are application-layer policies, not protocol semantics. HIRI defines the verification primitive; it does not prescribe trust decisions.

---

## 14. Serialization Boundary

### 14.1 Principle

The kernel operates exclusively on JSON-LD objects and UTF-8 byte sequences. Wire formats (CBOR, protocol buffers, etc.) are handled by adapters at the transport layer.

```
          Kernel                    Adapter                   Transport
  ┌────────────────────┐   ┌────────────────────┐   ┌────────────────────┐
  │  JSON-LD manifests │──►│  Serialize to wire  │──►│  IPFS / HTTP / FS  │
  │  UTF-8 bytes       │   │  format (dag-cbor)  │   │                    │
  │  Pure computation  │◄──│  Deserialize from   │◄──│  Retrieve bytes    │
  │                    │   │  wire + validate    │   │                    │
  └────────────────────┘   └────────────────────┘   └────────────────────┘
```

### 14.2 dag-cbor Wire Format

For IPFS transport, the standard wire format is dag-cbor:

```
Encode: JSON-LD manifest → deterministic dag-cbor bytes → IPFS put
Decode: IPFS get → dag-cbor bytes → verify determinism → JSON-LD manifest
```

#### 14.2.1 CBOR Determinism Rules

| Rule | Requirement |
|------|-------------|
| Map key ordering | Bytewise lexicographic sort of UTF-8 keys |
| Length encoding | Definite-length only |
| Integer encoding | Minimal representation |
| String encoding | Definite-length only |
| CBOR tags | Only CID tag (42) |
| Floating point | Shortest IEEE 754 |

#### 14.2.2 Determinism Verification

Adapters MUST verify CBOR determinism on inbound data:

```javascript
function verifyCborDeterminism(bytes) {
  const decoded = dagCbor.decode(bytes);
  const reencoded = dagCbor.encode(decoded);
  if (!bytesEqual(bytes, reencoded)) {
    throw new Error('Non-deterministic CBOR');
  }
  return decoded;
}
```

### 14.3 Local Wire Format

For local storage (filesystem, IndexedDB), implementations MAY use JSON serialization directly. The canonical form for hashing and signing is always the profile-specific canonicalization (§7), not the wire format.

### 14.4 Adapter Responsibilities

| Responsibility | Kernel | Adapter |
|----------------|--------|---------|
| Canonicalization | YES | No |
| Hash computation | YES (via CryptoProvider) | Provides CryptoProvider |
| Signing / verification | YES (via CryptoProvider) | Provides CryptoProvider |
| Wire serialization | No | YES |
| CBOR determinism check | No | YES |
| CID construction | No | YES |
| Transport protocol | No | YES |
| Key encoding for transport | No | YES (e.g., libp2p protobuf wrap) |

### 14.5 Transport Adapter Reversibility

All adapter-layer encodings MUST be losslessly reversible. Any transformation applied by an adapter (CBOR encoding, protobuf key wrapping, CID construction) MUST round-trip without alteration to the kernel-layer data.

**Normative invariant:** For any manifest `M` and any adapter `A`:

```
A.decode(A.encode(M)) === M
```

Where equality is byte-level identity of the kernel's canonical form (JCS or URDNA2015 output).

Adapters that wrap Ed25519 public keys for transport (e.g., libp2p protobuf encoding) MUST document the wrapping format and MUST provide an unwrap function that recovers the original 32-byte public key. Verifiers receiving transport-wrapped keys MUST unwrap to raw bytes before passing to the kernel's verification functions. The kernel MUST NOT be aware of transport-specific key encoding.

---

## 15. RDF Indexing & Query

### 15.1 Graph Construction

Verified content (JSON-LD) is loaded into an in-memory RDF index for local querying. No database server is required.

```typescript
async function buildGraph(
  content: Uint8Array,
  format: string,
  baseURI: string,
  config: { entailmentMode: EntailmentMode },
  indexFactory: () => RDFIndex
): Promise<RDFIndex>
```

### 15.2 Entailment Modes

| Mode | Behavior | Status |
|------|----------|--------|
| `none` | No inference. Only asserted triples returned. | REQUIRED |
| `materialized` | Pre-computed inference triples added at load time. | OPTIONAL, throws if unsupported |
| `runtime` | Inference applied at query time. | OPTIONAL, throws if unsupported |

`buildGraph` MUST throw if an unsupported entailment mode is requested. This prevents silent inference leakage.

### 15.3 SPARQL Execution

```typescript
async function executeQuery(
  sparql: string,
  index: RDFIndex,
  engine: SPARQLEngine
): Promise<QueryResult>
```

The recommended SPARQL engine is Oxigraph WASM. Implementations MUST ensure the engine respects the declared entailment mode — specifically, that `mode: "none"` suppresses all RDFS/OWL inference.

### 15.4 JSON-LD Loading Pipeline

For content declared as `application/ld+json`:

1. Parse content bytes as JSON
2. If RDF engine does not natively support JSON-LD: convert via `jsonld.toRDF()` to N-Quads
3. Load N-Quads into the RDF index
4. Block all remote context fetches via secure document loader

---

## 16. Security Considerations

### 16.1 Threat Model

| Threat | Mitigation |
|--------|------------|
| Content forgery | Content hash verification |
| Manifest tampering | Signature verification |
| Authority spoofing | Self-certifying key derivation |
| Key compromise | Revocation with retroactive invalidation |
| Context injection | Mandatory secure document loader |
| Version rollback | Monotonic version enforcement |
| Replay attack | Version tracking (operational layer) |
| Inference leakage | Entailment mode enforcement |
| Cross-profile semantic split | Profile Symmetry Rule (§7.3) — content and signature use same profile |
| Delta structural mismatch | Delta–Canonicalization Coupling (§11.4) — format matches profile |
| Version precision loss | Universal string encoding for `hiri:version` (§11.3) |
| Multibase parsing exception | No URI exception; standard multibase everywhere (§6.1) |
| Canonicalization DoS | Resource limits on blank nodes, time, output size (§7.7) |
| Transport key manipulation | Adapter reversibility invariant; kernel never sees wrapped keys (§14.5) |
| Stale revocation acceptance | Verifiers MUST report `revocationStatus: "unknown"` when undetermined (§13.6) |

### 16.2 Kernel Purity Invariants

The following APIs MUST NOT appear in kernel code:

- `Date.now()`, `new Date()` without injected timestamp
- `Math.random()`, `crypto.getRandomValues()`
- `fetch()`, `XMLHttpRequest`
- `process.env`, `require('fs')`, `import('fs')`
- Any import from adapter or transport layers

### 16.3 Timestamp Policy

All timestamps in the kernel are injected parameters. The kernel MUST NOT access the system clock. This ensures deterministic behavior and enables temporal testing with mock clocks.

---

## 17. Migration from v2.1.0

### 17.1 Authority Migration

v2.1.0 authorities use truncated hashes: `key:ed25519:<base58(sha256(pubkey))[0:20]>`

v3.1.1 authorities use full keys with multibase prefix: `key:ed25519:z<base58btc(pubkey)>`

**Migration procedure:**

1. For each v2.1.0 authority, the corresponding KeyDocument contains the full public key in `publicKeyMultibase`.
2. Extract the raw public key from `publicKeyMultibase`.
3. Derive the v3.1.1 authority using §5.1.1 (including the `z` prefix).
4. Re-sign all manifests under the new authority.
5. Publish a signed migration manifest linking the v2.1.0 authority to the v3.1.1 authority.

**Coexistence:** During migration, implementations MAY accept both authority formats. The `hiri:signature.canonicalization` field (present in v3.1.1, absent in v2.1.0) serves as a version discriminator: if the field is absent, the implementation SHOULD treat the manifest as v2.1.0 and apply JCS canonicalization. Authorities without a `z` prefix SHOULD be treated as v2.1.0 legacy format.

### 17.2 Version Encoding Migration

v2.1.0 encodes `hiri:version` as a JSON Number. v3.1.1 encodes it as a JSON String.

**Parsing:** v3.1.1 verifiers encountering a JSON Number for `hiri:version` SHOULD parse it as if it were a string and emit a deprecation warning. New manifests MUST use string encoding.

**Re-signing:** When re-signing a v2.1.0 manifest as v3.1.1, convert the version number to a string: `1` → `"1"`, `42` → `"42"`.

### 17.3 Canonicalization Migration

v2.1.0 manifests are signed with JCS (implicit). v3.1.1 manifests declare their canonicalization explicitly and enforce profile symmetry.

**Round-trip:** A v2.1.0 manifest can be re-signed with v3.1.1 by:

1. Verifying the existing JCS signature
2. Adding `hiri:signature.canonicalization: "JCS"` and `hiri:content.canonicalization: "JCS"` (making implicit explicit)
3. Converting `hiri:version` from Number to String
4. Updating the authority to the full-key `z`-prefixed format
5. Re-canonicalizing with the target profile
6. Re-signing with the same or a new key
7. Updating the chain link to reference the new manifest hash

### 17.4 Content Hash Migration

v2.1.0 content uses `raw-sha256` addressing (implicit). v3.1.1 adds `cidv1-dag-cbor`.

**Forward migration:** To publish existing content to IPFS:

1. Fetch the original content bytes
2. Verify against the v2.1.0 `raw-sha256` hash
3. Canonicalize with the target profile
4. Construct the dag-cbor envelope
5. Compute the CIDv1
6. Create a new v3.1.1 manifest with `addressing: "cidv1-dag-cbor"`
7. Sign and chain to the previous manifest

The original content and its `raw-sha256` hash remain valid. The new manifest simply provides an additional, IPFS-compatible content address.

### 17.5 Delta Format Migration

v2.1.0 manifests using deltas implicitly use JSON Patch (RFC 6902).

**No change required** for manifests remaining on the JCS profile — JSON Patch continues to be the correct delta format.

**When upgrading to URDNA2015:** Any existing JSON Patch deltas remain valid for their original JCS-canonicalized manifests. New manifests using the URDNA2015 profile MUST use RDF Patch for deltas (§11.4). There is no automatic conversion between JSON Patch and RDF Patch; the delta must be recomputed from the original content versions.

---

## 18. Conformance Levels

### 18.1 Level 1: Core

The minimum implementation for local, edge-canonical verification.

**MUST implement:**
- Authority derivation (§5.1) with full-key format
- JCS canonicalization (§7.1)
- raw-sha256 content addressing (§8.1)
- Resolution Manifest construction and parsing (§9)
- Ed25519 signing and verification with JCS profile (§10)
- Chain link validation and chain walking (§11)
- URI resolution (§12)
- Key lifecycle (§13)
- HashRegistry with SHA256Algorithm (§8.5)
- Entailment mode `"none"` for RDF query (§15.2)

**MAY implement:**
- URDNA2015 canonicalization
- cidv1-dag-cbor content addressing
- CBOR wire format
- Materialized or runtime entailment modes

### 18.2 Level 2: Interoperable

Adds cross-system compatibility for federated and networked deployments.

**MUST implement everything in Level 1, plus:**
- URDNA2015 canonicalization (§7.2)
- cidv1-dag-cbor content addressing (§8.2)
- Secure document loader (§7.5)
- Signing and verification with URDNA2015 profile (§10)
- CIDv1Algorithm in HashRegistry (§8.5)

**MAY implement:**
- CBOR wire format (§14.2)
- Transport-specific key encoding (§14.4)

### 18.3 Level 3: Full

Complete implementation including IPFS transport readiness.

**MUST implement everything in Level 2, plus:**
- dag-cbor wire format with determinism verification (§14.2)
- Transport key encoding (e.g., libp2p protobuf wrap) (§14.4)
- CBOR determinism verification on inbound data (§14.2.2)
- Key pinning / Trust-on-First-Use (§13.5)
- Replay protection via ManifestTracker (operational layer)

---

## 19. Advanced Features (Interface Contracts)

The following features are defined as interface contracts for future implementation. They are NOT normative in v3.1.1 but are specified here to prevent incompatible designs.

### 19.1 Chain Compaction (Recursive ZK-SNARKs)

Long-lived chains may be compressed into a single proof. The compaction manifest type (`hiri:CompactionManifest`) is reserved. Implementations encountering a compaction manifest they cannot verify MUST reject it, not silently skip it.

### 19.2 Zero-Knowledge Proofs

Manifests MAY include `hiri:commitment` fields containing Pedersen commitments or other ZK structures. Verifiers that do not support the declared curve:

1. MUST treat commitments as opaque data
2. MUST NOT reject manifests due to unsupported ZK
3. MUST still verify non-ZK aspects (signature, chain)

### 19.3 Privacy Accumulators

Reserved for selective disclosure. Interface TBD.

### 19.4 Timestamp Authority Integration

The `hiri:timing.timestampProof` field is reserved for TSA-verified timestamps. When absent, timestamps are advisory only.

---

## Appendix A: HIRI URI Grammar

```abnf
hiri-uri       = "hiri://" authority "/" resource-type "/" identifier
authority      = key-authority / domain-authority / consortium-authority
key-authority  = "key:" algorithm ":" "z" encoded-key
algorithm      = "ed25519"
encoded-key    = 1*base58btc-char          ; Full public key, WITH 'z' multibase prefix
resource-type  = "data" / "key" / "compact" / "proof" / "vocab"
identifier     = 1*( unreserved / pct-encoded )
```

---

## Appendix B: Normative Test Vectors

These vectors are authoritative. Conformant implementations MUST produce identical outputs.

### B.1 Authority Derivation

```
Public key (hex):
  d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a

Authority:
  key:ed25519:z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK

URI:
  hiri://key:ed25519:z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK/data/test

Round-trip:
  extractPublicKey(deriveAuthority(pubkey, "ed25519")).publicKey === pubkey  ✓
```

### B.2 JCS Canonicalization

```
Input:  { "b": 2, "a": 1, "c": { "d": 4, "c": 3 } }
Output: {"a":1,"b":2,"c":{"c":3,"d":4}}
SHA256: <computed-over-utf8-bytes-of-output>
```

### B.3 Content Hash (raw-sha256)

```
Content (canonical JCS bytes): <utf8 bytes of canonical JSON>
Hash: sha256:<hex-digest>
```

### B.4 Version Handling

```javascript
// String encoding (normative)
parseVersion({ 'hiri:version': '42' }) === 42n                          ✓
parseVersion({ 'hiri:version': '9007199254740993' }) === 9007199254740993n  ✓
encodeVersion(42n) === '42'                                              ✓
encodeVersion(9007199254740993n) === '9007199254740993'                  ✓

// Number encoding (v2.1.0 compat — accept with warning)
parseVersion({ 'hiri:version': 42 }) === 42n  ✓ (with deprecation warning)

// Rejection
parseVersion({ 'hiri:version': '0' })   // throws: version must be ≥ 1
parseVersion({ 'hiri:version': '-1' })  // throws: version must be ≥ 1
parseVersion({ 'hiri:version': 'abc' }) // throws: not a valid integer
```

### B.5 Multibase Encoding

```
Input bytes (hex):
  d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a

Authority encoding (WITH z prefix — same as wire):
  z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK

Wire encoding (z prefix):
  z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK

Note: Authority and wire encodings are now identical.
No special-case parsing is required.
```

### B.6 Profile Symmetry Rejection (v3.1.0)

Verifiers MUST reject manifests where content and signature canonicalization profiles differ.

```
Input manifest:
  hiri:content.canonicalization = "JCS"
  hiri:signature.canonicalization = "URDNA2015"

Expected: REJECT — profile symmetry violation
Error: PROFILE_SYMMETRY_VIOLATION
```

```
Input manifest:
  hiri:content.canonicalization = "URDNA2015"
  hiri:signature.canonicalization = "JCS"

Expected: REJECT — profile symmetry violation
```

### B.7 Delta Format Mismatch Rejection (v3.1.0)

Verifiers MUST reject deltas whose format does not match the manifest's canonicalization profile.

```
Input manifest:
  hiri:content.canonicalization = "URDNA2015"
  hiri:delta.format = "application/json-patch+json"

Expected: REJECT delta (fall back to full content verification)
Warning: DELTA_FORMAT_MISMATCH
```

```
Input manifest:
  hiri:content.canonicalization = "JCS"
  hiri:delta.format = "application/rdf-patch"

Expected: REJECT delta (fall back to full content verification)
Warning: DELTA_FORMAT_MISMATCH
```

### B.8 URDNA2015 Equivalence Cases (v3.1.1)

The following JSON-LD documents are graph-equivalent and MUST produce identical URDNA2015 canonical N-Quads output:

**Case 8a: Key ordering variation**

```json
// Variant A
{ "@context": {"ex": "http://example.org/"}, "@id": "ex:Alice", "ex:name": "Alice", "ex:age": 30 }

// Variant B (different key order)
{ "ex:age": 30, "@id": "ex:Alice", "ex:name": "Alice", "@context": {"ex": "http://example.org/"} }

Expected: Identical N-Quads output for both variants.
```

**Case 8b: Compact vs expanded form**

```json
// Compact
{ "@context": {"ex": "http://example.org/"}, "@id": "ex:Alice", "ex:name": "Alice" }

// Expanded
[{ "@id": "http://example.org/Alice", "http://example.org/name": [{"@value": "Alice"}] }]

Expected: Identical N-Quads output.
```

**Case 8c: Language-tagged literals**

```json
{ "@context": {"ex": "http://example.org/"},
  "@id": "ex:Doc",
  "ex:title": [
    {"@value": "Hello", "@language": "en"},
    {"@value": "Hola", "@language": "es"}
  ]
}

Expected N-Quads include:
  <http://example.org/Doc> <http://example.org/title> "Hello"@en .
  <http://example.org/Doc> <http://example.org/title> "Hola"@es .
```

**Case 8d: Typed literal vs plain literal**

```json
// Explicit xsd:string type
{ "@context": {"ex": "http://example.org/", "xsd": "http://www.w3.org/2001/XMLSchema#"},
  "@id": "ex:Item", "ex:label": {"@value": "Test", "@type": "xsd:string"} }

// Implicit string (no @type)
{ "@context": {"ex": "http://example.org/"},
  "@id": "ex:Item", "ex:label": "Test" }

Expected: Identical N-Quads — both produce a plain literal "Test".
```

**Case 8e: Blank node canonicalization**

```json
{ "@context": {"ex": "http://example.org/"},
  "@id": "ex:Alice",
  "ex:knows": { "ex:name": "Bob" }
}

Expected N-Quads:
  <http://example.org/Alice> <http://example.org/knows> _:c14n0 .
  _:c14n0 <http://example.org/name> "Bob" .

The blank node label _:c14n0 is deterministic across implementations.
```

### B.9 CBOR Non-Determinism Rejection (v3.1.1)

Adapters MUST reject CBOR bytes that fail the re-encoding determinism check.

```
Input (hex): a2616202616101
  Decodes to: { "b": 2, "a": 1 }
  Re-encodes to: a2616101616202  (keys sorted: "a" < "b")
  Input !== Re-encoded → REJECT

Error: NON_DETERMINISTIC_CBOR
```

```
Input (hex): a2616101616202
  Decodes to: { "a": 1, "b": 2 }
  Re-encodes to: a2616101616202
  Input === Re-encoded → ACCEPT
```

### B.10 Verification Status Reporting (v3.1.1)

```
Scenario: Manifest signed by active key, KeyDocument available
Expected report:
  signatureValid: true
  keyStatus: "active"
  revocationStatus: "confirmed-valid"
  timestampVerification: "advisory-only"

Scenario: Manifest signed by rotated key within grace period
Expected report:
  signatureValid: true
  keyStatus: "rotated-grace"
  revocationStatus: "confirmed-valid"
  timestampVerification: "advisory-only"

Scenario: Manifest valid but KeyDocument unavailable (offline)
Expected report:
  signatureValid: true
  keyStatus: "unknown"
  revocationStatus: "unknown"
  timestampVerification: "advisory-only"
Note: Verifier MUST NOT report unconditional validity.
```

---

## Appendix C: Canonicalization Pipeline Details

### C.1 JCS Pipeline

```
JSON object
  → RFC 8785 deterministic serialization
  → UTF-8 byte encoding
  → canonical bytes (used for hashing or signing)
```

### C.2 URDNA2015 Pipeline

```
JSON-LD document + secure document loader
  → JSON-LD expansion
  → RDF dataset construction
  → URDNA2015 blank node canonicalization
  → Deterministic N-Quads serialization
  → UTF-8 byte encoding
  → canonical bytes (used for hashing or signing)
```

### C.3 CIDv1 Content Addressing Pipeline

```
canonical bytes (from JCS or URDNA2015)
  → dag-cbor envelope: {
      '@type': 'hiri:CanonicalContent',
      'hiri:canonicalization': '<profile>',
      'hiri:content': canonicalBytes
    }
  → deterministic dag-cbor encoding
  → SHA-256 multihash
  → CIDv1 (codec=0x71, hash=0x12)
  → base32lower multibase string
```

---

## Appendix D: Wire Format Examples

### D.1 Manifest Bundle (IPFS Layout)

```
/ipfs/bafyBundle.../
├── manifest.cbor          ← dag-cbor encoded manifest
├── content/
│   └── source.cbor        ← dag-cbor wrapped content
├── .well-known/
│   └── hiri-key.cbor      ← dag-cbor encoded KeyDocument
```

### D.2 Manifest Bundle (Local Filesystem Layout)

```
./data/
├── sha256--<manifest-hash>.json    ← JSON manifest
├── sha256--<content-hash>.json     ← JSON content
├── sha256--<keydoc-hash>.json      ← JSON KeyDocument
```

---

## Appendix E: Determinism Checklist (INFORMATIVE)

This appendix is INFORMATIVE. It provides practical guidance for implementers, not normative requirements.

### E.1 Kernel Determinism

Verify that your kernel produces identical outputs across runs:

- [ ] `stableStringify(obj)` produces identical bytes for identical logical objects (test with reordered keys, nested structures, Unicode edge cases)
- [ ] Hash of `stableStringify(obj)` is stable across Node.js versions and browser engines
- [ ] Ed25519 signatures are deterministic (same key + same input → same signature). Note: Ed25519 is inherently deterministic per RFC 8032; verify your library doesn't add randomized nonce padding
- [ ] `parseVersion("1")` returns the same BigInt/u64 across all target languages
- [ ] JSON-LD canonicalization (if URDNA2015) produces identical N-Quads across `jsonld` library versions — test with Appendix B.8 vectors

### E.2 Adapter Determinism

- [ ] dag-cbor round-trip: `decode(encode(obj))` produces byte-identical CBOR to the original `encode(obj)` for all test fixtures
- [ ] CIDv1 for identical content is identical across `multiformats` library versions
- [ ] libp2p protobuf key wrapping is reversible: `unwrap(wrap(key))` === `key` for all 32-byte inputs
- [ ] CBOR non-determinism rejection catches all Appendix B.9 vectors

### E.3 Cross-Language Verification

If your implementation targets multiple languages, verify:

- [ ] Same test fixture → same content hash in all languages
- [ ] Same test fixture → same signature bytes in all languages
- [ ] Same signed manifest → same manifest hash in all languages
- [ ] Same chain → same verification result (valid/invalid + depth + warnings) in all languages

### E.4 Recommended Test Harness

A minimal determinism test harness:

1. Serialize the `person.jsonld` test fixture with JCS
2. Hash with SHA-256 → compare to known vector
3. Sign with a fixed test keypair (seed: 32 zero bytes) → compare to known signature vector
4. Build a 3-deep chain → verify chain walk produces `{ valid: true, depth: 3 }`
5. If URDNA2015: canonicalize all Appendix B.8 variants → verify identical N-Quads
6. If dag-cbor: encode manifest → verify byte-identical to known CBOR vector

Implementations SHOULD run this harness in CI against every target runtime.

---

## Document History

| Version | Date | Status | Notes |
|---------|------|--------|-------|
| 1.0.0 | 2025-01 | Draft | Initial specification |
| 2.0.0 | 2025-09 | Draft | Added chain compaction, ZK, privacy |
| 2.1.0 | 2025-12 | Stable | Promoted to stable; MVP reference spec |
| 3.0.0 | 2026-03 | Draft | Full-key authority, canonicalization profiles, content addressing modes, serialization boundary |
| 3.1.0 | 2026-03 | Draft | Profile symmetry, delta–canonicalization coupling, version type unification, multibase URI consistency |
| **3.1.1** | **2026-03** | **Draft** | Context registry, delta atomicity, verification status reporting, canonicalization resource limits, expanded test vectors |

---

## License

**Specification:** CC0 1.0 Universal (Public Domain)
**Reference Implementations:** Apache 2.0

---

**Version:** 3.1.1
**Status:** Draft
**Last Updated:** March 2026

---

*HIRI is a protocol, not a product. It belongs to everyone who uses it.*

*This specification treats interoperability as a security property, not a convenience.*
