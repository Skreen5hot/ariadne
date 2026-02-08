# HIRI IPFS Integration Specification

## Storage & Discovery Layer for the HIRI Protocol

**Version:** 3.0.0  
**Date:** February 2026  
**Status:** Stable  
**Dependencies:** HIRI Protocol Specification v2.1.0

---

## Document Status

This specification has achieved **Stable** status. Breaking changes require a major version increment and deprecation period. Implementations conforming to this version may declare compatibility with identifier `hiri-ipfs-v3`.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Normative References & Assumptions](#2-normative-references--assumptions)
3. [Encoding Standards](#3-encoding-standards)
4. [Deployment Profiles](#4-deployment-profiles)
5. [Naming & Discovery](#5-naming--discovery)
6. [Content Addressing & Canonicalization](#6-content-addressing--canonicalization)
7. [Data Structures & Storage Layout](#7-data-structures--storage-layout)
8. [Signature Construction & Verification](#8-signature-construction--verification)
9. [Chain Integrity & Replay Protection](#9-chain-integrity--replay-protection)
10. [Key Pinning & Trust-on-First-Use](#10-key-pinning--trust-on-first-use)
11. [Privacy & Zero-Knowledge Storage](#11-privacy--zero-knowledge-storage)
12. [Persistence & Availability](#12-persistence--availability)
13. [Offline Operation & Caching](#13-offline-operation--caching)
14. [Security Considerations](#14-security-considerations)
15. [Implementation Reference](#15-implementation-reference)
16. [Conformance Test Suite](#16-conformance-test-suite)
17. [Migration Guide](#17-migration-guide)
18. [Appendix A: HIRI URI Grammar](#appendix-a-hiri-uri-grammar)
19. [Appendix B: URDNA2015 Canonicalization Pipeline](#appendix-b-urdna2015-canonicalization-pipeline)
20. [Appendix C: Normative Test Vectors](#appendix-c-normative-test-vectors)
21. [Appendix D: Deployment Quick-Start Guides](#appendix-d-deployment-quick-start-guides)

---

## Changelog: v2.3.0 → v3.0.0

| Change | Section | Description |
|--------|---------|-------------|
| **Normative Interpretation Rule** | §1.3 | Explicit rule that verification algorithms are normative |
| **Version Integer Semantics** | §9.1 | uint64 with explicit BigInt handling for JS |
| **JSON-LD Context Policy** | §6.2.3 | Mandatory context pinning or embedding |
| **Verification Extensibility** | §1.4 | May be stricter, never weaker |
| **Replay Tracker Locality** | §9.3.3 | Explicit non-synchronization requirement |
| **PeerId Stability Guarantee** | §5.2.3 | Black-box derivation contract |
| **ZK Graceful Degradation** | §11.2.3 | Unsupported curves treated as opaque |
| **Promotion to Stable** | Status | Specification achieves Stable status |

---

## 1. Introduction

This specification defines how the HIRI Protocol (v2.1) utilizes IPFS (InterPlanetary File System) as its primary storage and resolution layer. It provides the complete, unambiguous rules for content addressing, signature verification, and trust establishment necessary for interoperable implementations.

### 1.1 Scope

This document specifies:
- IPFS primitives for HIRI storage and discovery
- Encoding standards for deterministic content addressing
- Canonicalization algorithms for signatures and hashes
- Deployment profiles for operational contexts
- Security requirements and threat mitigations
- Normative test vectors for conformance verification

This document does NOT specify:
- HIRI Protocol semantics (see HIRI Protocol Spec v2.1.0)
- Zero-knowledge proof circuit design
- Application-level policies beyond verification

### 1.2 Terminology

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119.

| Term | Definition |
|------|------------|
| Manifest | A HIRI Resolution Manifest, Compaction Manifest, or Proof Manifest |
| Content | The data referenced by a manifest's `hiri:content` field |
| Authority | The HIRI publisher identifier (key, domain, or consortium) |
| Canonical Form | The deterministic byte sequence used for hashing/signing |
| Profile | A deployment configuration with specific characteristics |
| Multibase | Self-describing base encoding with prefix character |
| Conformant | Producing identical outputs for all test vectors in Appendix C |

### 1.3 Normative Interpretation Rule

**Any algorithm, table, code block, or prose in this specification that describes verification, hashing, signing, canonicalization, encoding, or acceptance/rejection criteria SHALL be interpreted as normative unless explicitly marked OPTIONAL or INFORMATIVE.**

This rule eliminates ambiguity: if the specification describes how something must work, implementations must implement it exactly that way.

### 1.4 Architectural Principles

> **Principle 1: Determinism as Law**
>
> This specification defines deterministic algorithms for content addressing, canonicalization, signature verification, and chain integrity. Compliant implementations MUST produce bit-for-bit identical outputs for identical inputs when using the canonicalization rules and library behaviors specified herein.

> **Principle 2: Test Vectors as Truth**
>
> The test vectors in Appendix C are the authoritative definition of correct behavior. An implementation is conformant if and only if it produces identical outputs for all test vectors. The reference implementation targets browser and Node.js runtimes using the library versions in §2.2.

> **Principle 3: Verification Extensibility**
>
> Implementations MUST NOT weaken or bypass verification semantics defined herein. Implementations MAY apply stricter validation policies (additional checks, tighter bounds, earlier rejection), provided they do not accept inputs that would be rejected by the reference behavior. Implementations that apply stricter policies SHOULD document their additional requirements.

> **Principle 4: Interoperability as Security**
>
> This specification treats interoperability as a security property, not a convenience. Divergent implementations create attack surface. Behavioral equivalence across all deployments is required for the security model to hold.

---

## 2. Normative References & Assumptions

### 2.1 Required Specifications

| Specification | Version | Usage | Stability |
|---------------|---------|-------|-----------|
| HIRI Protocol | v2.1.0 | Core protocol semantics | Stable |
| IPFS | Kubo v0.24+ / Helia v4+ | Storage and retrieval | Stable |
| IPNS | v0.22+ | Mutable name resolution | Stable |
| CIDv1 | multiformats/cid v13+ | Content identifiers | Stable |
| Multibase | multiformats v13+ | Self-describing encoding | Stable |
| RFC 8785 | - | JSON Canonicalization Scheme | Stable |
| URDNA2015 | W3C RDF Dataset Normalization | JSON-LD canonicalization | Stable |
| Ed25519 | RFC 8032 | Signature algorithm | Stable |
| dag-cbor | @ipld/dag-cbor v9+ | Deterministic CBOR | Stable |

### 2.2 Library Dependencies (Reference Versions)

**These exact versions define the reference behavior.** Implementations using other libraries MUST produce identical outputs for all test vectors in Appendix C.

```json
{
  "dependencies": {
    "helia": "^4.0.0",
    "@helia/unixfs": "^3.0.0",
    "@helia/ipns": "^7.0.0",
    "@libp2p/peer-id": "^4.0.0",
    "@libp2p/crypto": "^4.0.0",
    "multiformats": "^13.0.0",
    "@ipld/dag-cbor": "^9.0.0",
    "canonicalize": "^2.0.0",
    "jsonld": "^8.3.0",
    "@noble/ed25519": "^2.0.0"
  }
}
```

### 2.3 Libp2p Key Encoding

HIRI uses Ed25519 keys encoded per the libp2p crypto protobuf specification.

**Protobuf Schema:**

```protobuf
message PublicKey {
  required KeyType Type = 1;
  required bytes Data = 2;
}

enum KeyType {
  RSA = 0;
  Ed25519 = 1;
  Secp256k1 = 2;
  ECDSA = 3;
}
```

**Wire Format for Ed25519 Public Key (36 bytes total):**

```
Offset  Bytes    Value     Meaning
------  -------  --------  ----------------------------------
0-1     08 01    varint    Type = 1 (Ed25519)
2-3     12 20    varint    Field 2, length = 32
4-35    <key>    bytes     32-byte Ed25519 public key
```

### 2.4 Upstream Stability Contract

This specification depends on specific behaviors of upstream libraries. Any upstream change that alters the output of the following operations constitutes a breaking change from the HIRI conformance perspective:

| Operation | Library | Breaking if output changes for same input |
|-----------|---------|-------------------------------------------|
| PeerId derivation | @libp2p/peer-id | PeerId string for given public key |
| CBOR encoding | @ipld/dag-cbor | Byte sequence for given object |
| JSON-LD canonicalization | jsonld | N-Quads for given document |
| Ed25519 signatures | @noble/ed25519 | Signature bytes for given input |

Implementations MUST treat these as black-box functions whose outputs MUST match Appendix C test vectors. **Conformance is determined by test vector matching, not library version.**

---

## 3. Encoding Standards

This section defines the canonical encoding rules for all HIRI-over-IPFS data structures.

### 3.1 Multibase Encoding

All base-encoded strings in HIRI wire formats use [Multibase](https://github.com/multiformats/multibase) encoding, which includes a single-character prefix indicating the scheme.

#### 3.1.1 Encoding Rules

| Context | Multibase | Prefix | Rule |
|---------|-----------|--------|------|
| HIRI Authority Key (in URI) | base58btc | **NONE** | Exception for URI readability |
| CID String | base32lower | `b` | Standard CIDv1 |
| Signature proofValue | base58btc | `z` | Full multibase |
| Hash Values | base16 (hex) | `f` | Full multibase |
| All other wire formats | base58btc | `z` | Full multibase |

**The URI Exception:**

For human readability in HIRI URIs, the authority component uses base58btc encoding **without** the `z` prefix. This is the **only** exception to the multibase-prefix rule.

```
hiri://key:ed25519:6MkhaXgBZDvotDkL.../data/Resource
                   └── NO 'z' prefix (URI context only)

"proofValue": "z6MkhaXgBZDvotDkL..."
               └── WITH 'z' prefix (wire format)
```

#### 3.1.2 Canonical Encode/Decode Functions

```javascript
import { base58btc } from 'multiformats/bases/base58'

/**
 * Encode bytes for HIRI authority string.
 * Used ONLY in hiri:// URI authority component.
 * 
 * @param {Uint8Array} bytes - Raw bytes to encode
 * @returns {string} - base58btc WITHOUT 'z' prefix
 */
function encodeAuthority(bytes) {
  const multibase = base58btc.encode(bytes)  // Returns 'z' + base58
  return multibase.slice(1)                   // Remove 'z' for URI
}

/**
 * Decode HIRI authority string to bytes.
 * 
 * @param {string} encoded - base58btc WITHOUT 'z' prefix
 * @returns {Uint8Array}
 */
function decodeAuthority(encoded) {
  return base58btc.decode('z' + encoded)      // Add 'z' for decoder
}

/**
 * Encode bytes for wire format.
 * Used everywhere EXCEPT URI authority.
 * 
 * @param {Uint8Array} bytes - Raw bytes to encode
 * @returns {string} - Full multibase with 'z' prefix
 */
function encodeMultibase(bytes) {
  return base58btc.encode(bytes)              // Returns 'z...'
}

/**
 * Decode multibase string to bytes.
 * 
 * @param {string} multibaseStr - Full multibase with prefix
 * @returns {Uint8Array}
 */
function decodeMultibase(multibaseStr) {
  if (!multibaseStr.startsWith('z')) {
    throw new HiriError('INVALID_MULTIBASE',
      `Expected base58btc (z prefix), got: ${multibaseStr[0]}`)
  }
  return base58btc.decode(multibaseStr)
}
```

#### 3.1.3 Test Vector

```
Input bytes (hex):
  d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a

encodeAuthority(input):
  "6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK"

encodeMultibase(input):
  "z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK"

Round-trip:
  decodeAuthority(encodeAuthority(input)) === input  ✓
  decodeMultibase(encodeMultibase(input)) === input  ✓
```

### 3.2 CBOR Determinism

All CBOR encoding in HIRI MUST use deterministic dag-cbor encoding as defined by IPLD.

#### 3.2.1 Deterministic Encoding Rules

| Rule | Requirement |
|------|-------------|
| Map key ordering | Bytewise lexicographic sort of UTF-8 keys |
| Length encoding | Definite-length only |
| Integer encoding | Minimal (smallest representation) |
| String encoding | Definite-length only |
| CBOR tags | Only CID tag (42); no others |
| Floating point | Shortest IEEE 754 |

#### 3.2.2 Implementation

```javascript
import * as dagCbor from '@ipld/dag-cbor'

function encodeDeterministicCbor(obj) {
  return dagCbor.encode(obj)
}

function decodeCbor(bytes) {
  return dagCbor.decode(bytes)
}
```

#### 3.2.3 Determinism Verification

Before accepting manifests, implementations MUST verify CBOR determinism:

```javascript
function verifyCborDeterminism(bytes) {
  const decoded = dagCbor.decode(bytes)
  const reencoded = dagCbor.encode(decoded)
  
  if (!bytesEqual(bytes, reencoded)) {
    throw new HiriError('NON_DETERMINISTIC_CBOR',
      'Re-encoding produced different bytes')
  }
  
  return decoded
}
```

### 3.3 Multihash Encoding

HIRI uses SHA2-256 for all content hashes.

| Parameter | Value | Varint |
|-----------|-------|--------|
| Hash algorithm | sha2-256 | `0x12` |
| Digest length | 32 bytes | `0x20` |

---

## 4. Deployment Profiles

### 4.1 Profile Overview

| Profile | Install | Publish | Persist | Privacy | Target |
|---------|---------|---------|---------|---------|--------|
| Gateway Consumer | None | No | Cache only | Low | Readers |
| Browser Publisher | None | Yes | Remote pins | Medium | Web apps |
| Desktop Node | Binary | Yes | Local | High | Developers |
| Server Node | Container | Yes | Local | High | Services |
| Org Cluster | IT deploy | Yes | Replicated | High | Enterprises |

### 4.2 Profile 1: Gateway Consumer

**Zero Install, Read-Only**

```
Browser                     Gateway                    IPFS Network
   │                           │                            │
   │── GET /ipfs/{cid} ───────►│                            │
   │                           │── retrieve ───────────────►│
   │◄── content ───────────────│◄──────────────────────────│
   │                                                        │
   │ [MANDATORY: Verify CID]                                │
   │ [MANDATORY: Verify signature]                          │
```

**Privacy:** Gateways observe IP, CIDs, timing. Rotating gateways reduces concentration but increases exposure surface.

### 4.3 Profile 2: Browser Publisher

**Zero Install, Ephemeral with Remote Pinning**

#### 4.3.1 Content Availability

| State | Availability |
|-------|--------------|
| Tab open, no pinning | DHT only (ephemeral) |
| Tab closed, no pinning | **LOST** |
| Tab open, pinned | DHT + pinning service |
| Tab closed, pinned | Pinning service only |

**Recommendation:** Always use remote pinning for persistent content.

#### 4.3.2 Browser P2P Constraints

Browser nodes cannot accept incoming TCP. They rely on WebRTC, WebSocket, and Circuit Relay.

```javascript
const helia = await createHelia({
  libp2p: {
    addresses: { listen: ['/webrtc'] },
    transports: [webRTC(), webSockets({ filter: filters.all })],
    relay: { enabled: true, hop: { enabled: false } },
    bootstrap: [
      '/dnsaddr/bootstrap.libp2p.io/p2p/QmNnooDu7bfjPFoTZYxMNLWUQJyrVwtbZg5gBMjTezGAJN'
    ]
  }
})
```

### 4.4 Profiles 3-4: Desktop/Server

See v2.2.0 §3.4-3.5 for complete documentation.

### 4.5 Profile Conformance

All profiles MUST:

1. Produce identical CIDs for identical content
2. Produce identical signatures for identical inputs
3. Pass all test vectors in Appendix C
4. Enforce signature verification without bypass
5. Implement key pinning per §10

---

## 5. Naming & Discovery

### 5.1 Discovery Mapping

| HIRI Profile | IPFS Primitive | Security Basis |
|--------------|----------------|----------------|
| HIRI-KEY | IPNS (Ed25519 PeerId) | Self-certifying |
| HIRI-DNS | DNSLink → IPNS | Via resolved key |
| HIRI-IPNS | Native IPNS | Via resolved key |
| HIRI-REG | Registry → IPNS | Via resolved key |

### 5.2 Key Derivation

#### 5.2.1 HIRI Authority → IPNS PeerId

```javascript
import { peerIdFromKeys } from '@libp2p/peer-id'

async function hiriKeyToIPNS(hiriAuthority) {
  const match = hiriAuthority.match(/^key:([a-z0-9]+):([A-Za-z0-9]+)$/)
  if (!match) throw new HiriError('INVALID_AUTHORITY', hiriAuthority)
  
  const [_, algorithm, encodedKey] = match
  if (algorithm !== 'ed25519') {
    throw new HiriError('UNSUPPORTED_ALGORITHM', algorithm)
  }
  
  const publicKeyBytes = decodeAuthority(encodedKey)
  if (publicKeyBytes.length !== 32) {
    throw new HiriError('INVALID_KEY_LENGTH', publicKeyBytes.length)
  }
  
  // Protobuf wrap (see §2.3)
  const protobufKey = new Uint8Array(36)
  protobufKey[0] = 0x08; protobufKey[1] = 0x01
  protobufKey[2] = 0x12; protobufKey[3] = 0x20
  protobufKey.set(publicKeyBytes, 4)
  
  return await peerIdFromKeys(protobufKey)
}
```

#### 5.2.2 IPNS PeerId → HIRI Authority

```javascript
function ipnsToHiriKey(peerId) {
  const proto = peerId.publicKey
  if (proto[0] !== 0x08 || proto[1] !== 0x01) {
    throw new HiriError('WRONG_KEY_TYPE', 'Expected Ed25519')
  }
  const rawKey = proto.slice(4, 36)
  return `key:ed25519:${encodeAuthority(rawKey)}`
}
```

#### 5.2.3 PeerId Derivation Stability

Implementations MUST treat libp2p PeerId derivation as a **black-box function** whose output MUST match Appendix C test vectors exactly.

**Any upstream library change that alters PeerId output for a given public key constitutes a breaking change from the HIRI conformance perspective.** Implementations SHOULD pin library versions and verify against test vectors during CI.

### 5.3 IPNS Parameters

| Parameter | Value |
|-----------|-------|
| lifetime | 24 hours |
| ttl | 1 hour |

---

## 6. Content Addressing & Canonicalization

### 6.1 CID Parameters

| Parameter | Value | Code |
|-----------|-------|------|
| Version | 1 | - |
| Codec | dag-cbor | `0x71` |
| Hash | sha2-256 | `0x12` |

### 6.2 Canonicalization Pipelines

#### 6.2.1 JSON-LD (URDNA2015)

```javascript
async function canonicalizeJsonLd(doc, documentLoader) {
  const nquads = await jsonld.canonize(doc, {
    algorithm: 'URDNA2015',
    format: 'application/n-quads',
    documentLoader
  })
  
  const cborPayload = {
    '@type': 'hiri:CanonicalRDF',
    'hiri:canonicalization': 'URDNA2015',
    'hiri:format': 'application/n-quads',
    'hiri:content': new TextEncoder().encode(nquads)
  }
  
  const bytes = encodeDeterministicCbor(cborPayload)
  const hash = await sha256.digest(bytes)
  const cid = CID.createV1(0x71, hash)
  
  return { cid, bytes, nquads }
}
```

#### 6.2.2 Non-RDF JSON (RFC 8785)

```javascript
async function canonicalizeJson(obj) {
  const canonical = canonicalize(obj)
  const bytes = encodeDeterministicCbor(JSON.parse(canonical))
  const hash = await sha256.digest(bytes)
  return { cid: CID.createV1(0x71, hash), bytes }
}
```

#### 6.2.3 JSON-LD Context Handling Policy

**Remote context fetching introduces availability risk, replay attacks, and non-determinism.** Implementations MUST use one of:

**Option A: Embedded Contexts (RECOMMENDED)**

```javascript
const EMBEDDED_CONTEXTS = {
  'https://hiri-protocol.org/spec/v2.1': { /* definition */ },
  'https://w3id.org/security/v2': { /* definition */ }
}

function createSecureDocumentLoader() {
  return async (url) => {
    if (EMBEDDED_CONTEXTS[url]) {
      return { document: EMBEDDED_CONTEXTS[url], documentUrl: url }
    }
    throw new HiriError('UNKNOWN_CONTEXT', `Not embedded: ${url}`)
  }
}
```

**Option B: Pinned Contexts (CID-verified)**

```javascript
const PINNED_CONTEXTS = {
  'https://hiri-protocol.org/spec/v2.1': 'bafyContextCid...'
}

function createPinnedDocumentLoader(ipfs) {
  return async (url) => {
    const cid = PINNED_CONTEXTS[url]
    if (!cid) throw new HiriError('UNKNOWN_CONTEXT', `Not pinned: ${url}`)
    const doc = await ipfs.fetchVerified(cid)
    return { document: doc, documentUrl: url }
  }
}
```

**Prohibited:**

```javascript
// NON-CONFORMANT — DO NOT USE
documentLoader: jsonld.documentLoaders.node()  // Fetches arbitrary URLs
```

### 6.3 CID Verification

```javascript
async function verifyCid(bytes, expectedCid) {
  const hash = await sha256.digest(bytes)
  const computed = CID.createV1(expectedCid.code, hash)
  return computed.equals(expectedCid)
}
```

CID verification is **mandatory** for all gateway-fetched content.

---

## 7. Data Structures & Storage Layout

### 7.1 Manifest Bundle

```
/ipfs/bafyBundle.../
├── manifest.cbor
├── content/
│   ├── source.cbor
│   └── materialized.cbor
├── proof/
│   ├── materialization.cbor
│   └── compaction.bin
└── .well-known/
    └── hiri-key.cbor
```

### 7.2 Manifest Schema

See HIRI Protocol Spec v2.1.0 §5.2.

---

## 8. Signature Construction & Verification

### 8.1 Algorithm

```
Signature = Ed25519_Sign(PrivateKey, CanonicalBytes)

CanonicalBytes = dag-cbor({
  '@type': 'hiri:SignatureInput',
  'hiri:canonicalization': 'URDNA2015',
  'hiri:content': UTF8(URDNA2015(ManifestWithoutProofValue))
})
```

### 8.2 Signing

```javascript
async function signManifest(manifest, privateKey, verificationMethod) {
  const toSign = structuredClone(manifest)
  toSign['hiri:signature'] = {
    'type': 'Ed25519Signature2020',
    'created': new Date().toISOString(),
    'verificationMethod': verificationMethod,
    'proofPurpose': 'assertionMethod'
  }
  
  const nquads = await jsonld.canonize(toSign, {
    algorithm: 'URDNA2015',
    format: 'application/n-quads',
    documentLoader: createSecureDocumentLoader()
  })
  
  const canonicalBytes = encodeDeterministicCbor({
    '@type': 'hiri:SignatureInput',
    'hiri:canonicalization': 'URDNA2015',
    'hiri:content': new TextEncoder().encode(nquads)
  })
  
  const signature = await ed.signAsync(canonicalBytes, privateKey)
  toSign['hiri:signature'].proofValue = encodeMultibase(signature)
  
  return toSign
}
```

### 8.3 Verification

```javascript
async function verifyManifestSignature(manifest, publicKey) {
  const proofValue = manifest['hiri:signature']?.proofValue
  if (!proofValue) throw new HiriError('NO_SIGNATURE')
  if (!proofValue.startsWith('z')) {
    throw new HiriError('INVALID_SIGNATURE_ENCODING', 'Expected z prefix')
  }
  
  const toVerify = structuredClone(manifest)
  delete toVerify['hiri:signature'].proofValue
  
  const nquads = await jsonld.canonize(toVerify, {
    algorithm: 'URDNA2015',
    format: 'application/n-quads',
    documentLoader: createSecureDocumentLoader()
  })
  
  const canonicalBytes = encodeDeterministicCbor({
    '@type': 'hiri:SignatureInput',
    'hiri:canonicalization': 'URDNA2015',
    'hiri:content': new TextEncoder().encode(nquads)
  })
  
  const signature = decodeMultibase(proofValue)
  return await ed.verifyAsync(signature, canonicalBytes, publicKey)
}
```

---

## 9. Chain Integrity & Replay Protection

### 9.1 Version Semantics

#### 9.1.1 Type Definition

The `hiri:version` field is an **unsigned 64-bit integer** (uint64).

| Property | Value |
|----------|-------|
| Type | Unsigned integer |
| Minimum | 1 |
| Maximum | 2⁶⁴ − 1 |
| Encoding | JSON number or string |

#### 9.1.2 JavaScript Number Limitations

JavaScript `Number` (IEEE 754 double) safely represents integers only to 2⁵³ − 1.

| Version Range | JSON Encoding | JS Handling |
|---------------|---------------|-------------|
| 1 to 2⁵³ − 1 | Number | Native |
| 2⁵³ to 2⁶⁴ − 1 | String | BigInt |

```javascript
function parseVersion(manifest) {
  const v = manifest['hiri:version']
  
  if (typeof v === 'number') {
    if (!Number.isInteger(v) || v < 1) {
      throw new HiriError('INVALID_VERSION', `Must be positive integer: ${v}`)
    }
    if (v > Number.MAX_SAFE_INTEGER) {
      throw new HiriError('VERSION_PRECISION_LOSS',
        `Exceeds safe integer; use string: ${v}`)
    }
    return BigInt(v)
  }
  
  if (typeof v === 'string') {
    const parsed = BigInt(v)
    if (parsed < 1n) throw new HiriError('INVALID_VERSION', v)
    return parsed
  }
  
  throw new HiriError('INVALID_VERSION_TYPE', typeof v)
}

function encodeVersion(version) {
  const v = BigInt(version)
  return v <= BigInt(Number.MAX_SAFE_INTEGER) ? Number(v) : v.toString()
}
```

#### 9.1.3 Monotonicity

```
∀ n > 0: version[n] > version[n-1]
```

Versions must be strictly increasing. Gaps are allowed.

### 9.2 Timestamp Requirements

| Level | Requirement |
|-------|-------------|
| Basic | `created` present |
| Standard | Within ±5 min of verifier clock |
| High | Verified `timestampProof` from TSA |

### 9.3 Replay Protection

#### 9.3.1 Manifest Tracker

```javascript
class ManifestTracker {
  constructor(storage) {
    this.storage = storage
  }
  
  async checkAndRecord(manifest) {
    const key = `${manifest['@id']}:${manifest['hiri:branch'] || 'main'}`
    const record = await this.storage.get(key)
    const version = parseVersion(manifest)
    
    if (record && version <= BigInt(record.lastVersion)) {
      throw new HiriError('VERSION_ROLLBACK',
        `${version} ≤ ${record.lastVersion}`)
    }
    
    await this.storage.put(key, {
      lastVersion: version.toString(),
      lastSeen: Date.now()
    })
  }
}
```

#### 9.3.2 Tracker Locality

**Replay trackers are local security state.** They MUST NOT be shared or synchronized between nodes.

Each node maintains independent tracking. Divergent views are expected. Synchronization would create consensus requirements and attack surface.

```javascript
// CORRECT
const tracker = new ManifestTracker(localIndexedDB)

// INCORRECT — DO NOT DO
const tracker = new ManifestTracker(sharedDatabase)
```

### 9.4 Key Revocation

See v2.3.0 §9.4 for complete revocation protocol.

---

## 10. Key Pinning & Trust-on-First-Use

### 10.1 TOFU Policy

Implementations MUST implement Trust-on-First-Use key pinning.

### 10.2 First Resolution

```javascript
async function firstResolution(authority) {
  const manifest = await resolveManifest(authority)
  const keyDocument = await resolveKeyDocument(manifest)
  const canonicalKey = keyDocument['hiri:authority']
  
  const signingKey = extractSigningKey(keyDocument, manifest)
  if (!await verifyManifestSignature(manifest, signingKey)) {
    throw new HiriError('SIGNATURE_INVALID')
  }
  
  // PIN
  await keyPinStore.pin(authority, canonicalKey, {
    pinnedAt: new Date().toISOString(),
    firstManifestCid: manifest.cid
  })
  
  return { manifest, trusted: 'tofu' }
}
```

### 10.3 Subsequent Resolution

```javascript
async function subsequentResolution(authority) {
  const pin = await keyPinStore.get(authority)
  if (!pin) return await firstResolution(authority)
  
  const manifest = await resolveManifest(authority)
  const keyDocument = await resolveKeyDocument(manifest)
  const currentKey = keyDocument['hiri:authority']
  
  if (currentKey !== pin.canonicalKey) {
    return await handleKeyMismatch(authority, pin, currentKey, keyDocument)
  }
  
  // Normal verification
  const signingKey = extractSigningKey(keyDocument, manifest)
  if (!await verifyManifestSignature(manifest, signingKey)) {
    throw new HiriError('SIGNATURE_INVALID')
  }
  
  return { manifest, trusted: 'pinned' }
}
```

### 10.4 Key Mismatch

On mismatch, implementations MUST NOT silently accept.

| Condition | Action |
|-----------|--------|
| No rotation/revocation | **REJECT** |
| Valid rotation | **PROMPT** or **ACCEPT** |
| Within grace period | **WARN + ACCEPT** |
| Past grace | **UPDATE PIN** |

---

## 11. Privacy & Zero-Knowledge Storage

### 11.1 Storage Separation

| Location | Contains |
|----------|----------|
| IPFS (Public) | Proofs, commitments, roots |
| Local (Private) | Data, credentials, witnesses |

### 11.2 Commitment Schemes

#### 11.2.1 Pedersen Commitments

```
Commitment = g^value · h^blinding
```

#### 11.2.2 Curve Selection

| Curve | Security | SNARK | EVM |
|-------|----------|-------|-----|
| bn254 | ~100 bit | Excellent | Yes |
| BLS12-381 | ~128 bit | Good | Pending |

#### 11.2.3 ZK Graceful Degradation

**ZK features are OPTIONAL.** Verifiers that don't support a curve:

1. MUST treat commitments as opaque data
2. MUST NOT reject manifests due to unsupported ZK
3. MUST still verify non-ZK aspects (signature, chain)

```javascript
async function verifyManifest(manifest, options) {
  await verifySignature(manifest)  // Required
  await verifyChain(manifest)      // Required
  
  if (manifest['hiri:commitment'] && options.zkEnabled) {
    const curve = manifest['hiri:commitment'].curve
    if (supportedCurves.includes(curve)) {
      await verifyCommitment(manifest)
    } else {
      console.log(`ZK skipped: unsupported curve ${curve}`)
    }
  }
}
```

---

## 12. Persistence & Availability

### 12.1 Pinning Responsibilities

| Role | Redundancy |
|------|------------|
| Publisher | 2+ |
| Vocabulary Authority | 3+ |
| Compaction Service | 2+ |

---

## 13. Offline Operation & Caching

### 13.1 Cache Layers

```
L1: Memory (session)
L2: IndexedDB (configurable TTL)
L3: IPNS Cache (1 hour, SWR)
L4: Key Pins (permanent)
L5: Replay Tracker (permanent, local only)
```

---

## 14. Security Considerations

### 14.1 Threat Model

| Threat | Mitigation |
|--------|------------|
| Gateway forgery | CID verification |
| IPNS spoofing | Signature verification |
| IPNS replay | Version monotonicity |
| Key compromise | Revocation protocol |
| Sybil/Eclipse | Bootstrap diversity |
| Context injection | Pinned contexts |

### 14.2 Security Invariants

1. CID verification for ALL gateway content
2. Signature verification for ALL manifests
3. Context pinning for ALL JSON-LD
4. Key pinning after first resolution
5. Version monotonicity enforcement
6. Replay tracker locality (no sync)
7. Audit logging for security events

---

## 15. Implementation Reference

### 15.1 Error Codes

```javascript
class HiriError extends Error {
  constructor(code, message, cause) {
    super(message)
    this.code = code
    this.cause = cause
  }
}

const ERROR_CODES = {
  INVALID_MULTIBASE: { http: 400 },
  NON_DETERMINISTIC_CBOR: { http: 400 },
  INVALID_AUTHORITY: { http: 400 },
  NO_SIGNATURE: { http: 400 },
  SIGNATURE_INVALID: { http: 403 },
  CID_MISMATCH: { http: 403 },
  VERSION_ROLLBACK: { http: 409 },
  KEY_PIN_VIOLATION: { http: 403 },
  UNKNOWN_CONTEXT: { http: 400 },
  FETCH_FAILED: { http: 502, retry: true }
}
```

---

## 16. Conformance Test Suite

### 16.1 Criteria

An implementation is **conformant** iff:

1. All Appendix C test vectors produce identical outputs
2. Round-trips succeed
3. Error cases reject appropriately

### 16.2 CI Configuration

```yaml
name: HIRI Conformance v3
on: [push, pull_request]
jobs:
  test:
    strategy:
      matrix:
        runtime: [node-20, node-22, chrome, firefox]
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run test:conformance
```

---

## 17. Migration Guide

### 17.1 From v2.3.0 to v3.0.0

| Change | Action |
|--------|--------|
| BigInt versions | Add BigInt handling for > 2⁵³ |
| Context policy | Embed or pin all contexts |
| Replay tracker | Verify local-only storage |

No breaking changes for implementations already following v2.3.0.

---

## Appendix A: HIRI URI Grammar

```abnf
hiri-uri      = "hiri://" authority "/" resource-type "/" identifier
key-authority = "key:" algorithm ":" encoded-key
algorithm     = "ed25519"
encoded-key   = 1*base58btc-char  ; NO 'z' prefix
resource-type = "data" / "key" / "compact" / "proof" / "vocab"
```

---

## Appendix B: URDNA2015 Pipeline

See v2.1.0 Appendix A.

---

## Appendix C: Normative Test Vectors

**These vectors are authoritative. Conformant implementations MUST produce identical outputs.**

### C.1 Multibase Encoding

```
Input (hex): d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a

encodeAuthority(): "6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK"
encodeMultibase(): "z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK"
```

### C.2 Key Derivation

```
Authority: key:ed25519:6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK
Pubkey (hex): d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a
Proto (hex): 08011220d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a
PeerId: 12D3KooWRm8J3hPn8KjDWQLQhqWchcNanp3H65K9HzSgXadswCXE

Round-trip: ipnsToHiriKey(hiriKeyToIPNS(authority)) === authority ✓
```

### C.3 CBOR Determinism

```
Input: { "b": 2, "a": 1 }
Output (hex): a2616101616202
Keys: "a" < "b" (bytewise)
```

### C.4 Canonicalization

```
Input: { "@context": {"ex":"http://example.org/"}, "@id": "ex:Alice", "ex:knows": {"@id":"ex:Bob"} }
N-Quads: <http://example.org/Alice> <http://example.org/knows> <http://example.org/Bob> .
```

### C.5 Version Handling

```javascript
// Safe integer
parseVersion({ 'hiri:version': 42 }) === 42n ✓
encodeVersion(42n) === 42 ✓

// Large integer (string)
parseVersion({ 'hiri:version': '9007199254740993' }) === 9007199254740993n ✓
encodeVersion(9007199254740993n) === '9007199254740993' ✓

// Monotonicity
validateVersion({ 'hiri:version': 3 }, { 'hiri:version': 5 })  // throws VERSION_ROLLBACK
```

---

## Appendix D: Quick-Start

See v2.2.0 Appendix C.

---

## Document History

| Version | Date | Status |
|---------|------|--------|
| 1.0.0 | 2025-01 | Draft |
| 2.0.0 | 2026-02 | Reference |
| 2.3.0 | 2026-02 | Reference |
| **3.0.0** | **2026-02** | **Stable** |

---

## License

**Specification:** CC0 1.0 Universal (Public Domain)  
**Reference Implementations:** Apache 2.0

---

**Version:** 3.0.0  
**Status:** Stable  
**Last Updated:** February 2026

---

*This specification treats interoperability as a security property, not a convenience.*

*HIRI is a protocol, not a product. It belongs to everyone who uses it.*
