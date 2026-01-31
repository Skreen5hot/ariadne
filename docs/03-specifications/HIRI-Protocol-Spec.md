# HIRI: Hash-IRI Protocol
## A Protocol-Agnostic, Local-First, Verifiable Knowledge & Claim Foundation

**Version:** 2.1.0  
**Status:** Specification  
**Last Updated:** January 2026

---

## Table of Contents

1. [Overview](#1-overview)
2. [Motivation](#2-motivation)
3. [Core Design Principles](#3-core-design-principles)
4. [Architecture](#4-architecture)
5. [Layer 1: Protocol Foundation](#5-layer-1-protocol-foundation)
6. [Layer 2: Resolution & Discovery](#6-layer-2-resolution--discovery)
7. [Layer 3: Storeless Index](#7-layer-3-storeless-index)
8. [Layer 4: Query & Verification](#8-layer-4-query--verification)
9. [Zero-Knowledge Claims Layer](#9-zero-knowledge-claims-layer)
10. [Key Management & Rotation](#10-key-management--rotation)
11. [Semantic Interoperability](#11-semantic-interoperability)
12. [Chain Compaction](#12-chain-compaction)
13. [Operational Considerations](#13-operational-considerations)
14. [Security Model](#14-security-model)
15. [Workflows](#15-workflows)
16. [Conformance Profiles](#16-conformance-profiles)
17. [Advantages & Trade-offs](#17-advantages--trade-offs)
18. [Roadmap](#18-roadmap)
19. [Contributing](#19-contributing)
20. [References](#20-references)

---

## Changelog: v2.0.0 → v2.1.0

| Change | Section | Description |
|--------|---------|-------------|
| **Chain Compaction** | §12 (new) | Recursive SNARK-based chain compression for long-lived entities |
| **Privacy Accumulators** | §9.5 (new) | Protocol-level privacy budget enforcement via cryptographic accumulators |
| **Materialized Entailment** | §8.1.2 (new) | Publisher-side inference materialization with verification |
| **Discovery Hierarchy** | §6.1 (revised) | HIRI-KEY elevated to security baseline; DNS as convenience layer |
| **Compaction Manifest** | §5.7 (new) | New manifest type for chain compression |
| **Privacy Credential** | §9.5.2 (new) | Anonymous credential for cross-verifier budget tracking |

---

## 1. Overview

**HIRI (Hash-IRI)** is a protocol for decentralized, verifiable knowledge and claims that operates **local-first**, **offline-capable**, and without dependence on centralized servers, blockchains, or protocol-specific trust anchors.

### 1.1 Core Capabilities

- **Offline-first verification** of data integrity and authorship
- **Client-side SPARQL querying** without graph servers
- **Low-friction updates** with no global consensus required
- **Immutable, auditable history** through sequential manifest linking
- **Chain compaction** via recursive proofs for long-lived entities
- **Privacy-preserving public verification** using zero-knowledge proofs
- **Protocol-level privacy budget enforcement** via cryptographic accumulators
- **Materialized entailment** for lightweight client-side reasoning
- **Protocol independence** with no lock-in to specific networks or technologies
- **Explicit key lifecycle management** with rotation and revocation
- **Hierarchical discovery** with self-certifying keys as security baseline

### 1.2 What HIRI Is Not

HIRI does not eliminate costs—it shifts them from protocol fees to infrastructure costs (storage, bandwidth, compute). HIRI does not solve all coordination problems—it provides primitives that applications must compose responsibly. HIRI does not guarantee privacy through magic—it provides cryptographic tools that require careful application-level design, with protocol-level enforcement where feasible.

---

## 2. Motivation

### 2.1 The Problem Space

Modern knowledge systems fail in complementary ways:

| System Type | Failure Mode | Impact |
|-------------|--------------|--------|
| **Web2 Centralized** | Trust anchored in servers | Single points of failure, surveillance, mutability |
| **Blockchain/Web3** | Trust anchored in global consensus | Expensive, slow, high infrastructure cost |
| **Semantic Web** | Trust anchored in HTTP authorities | Offline unusable, mutable references, link rot |
| **P2P Networks** | Trust anchored in social graphs | Inconsistent, partition-prone, discovery problems |

### 2.2 The Core Insight

**Data access and truth verification are not the same problem.**

Most systems conflate these concerns. HIRI recognizes that:

- **Data access** is about authorization, storage, and retrieval
- **Truth verification** is about cryptographic integrity and provenance
- **Discovery** is about finding current manifests for identifiers
- **Trust** is about key management and authority delegation
- **History** can be compressed without losing verifiability

By separating these concerns, HIRI enables:

- Private data with public verifiable claims
- Offline verification without online dependencies
- Local querying without centralized infrastructure
- Immutable history without blockchains
- Long-lived entities without unbounded chain growth
- Flexible discovery without protocol lock-in

### 2.3 Cost Model Transparency

HIRI shifts costs rather than eliminating them:

| Cost Category | Traditional Systems | HIRI |
|---------------|---------------------|------|
| **Publishing** | Transaction fees, gas | Storage hosting, bandwidth |
| **Verification** | Network requests, API calls | Client compute, local storage |
| **Discovery** | Centralized registries | Discovery infrastructure (varies by profile) |
| **Proof Generation** | N/A | Significant compute (often delegated) |
| **Proof Verification** | N/A | Modest client compute |
| **Chain Compaction** | N/A | Periodic compaction proof generation |

This transparency is intentional: implementers must understand their actual cost structure.

---

## 3. Core Design Principles

### 3.1 Local-First Verification
All trust decisions are made on the client using cryptographic primitives. No network dependency for verification of already-fetched content.

### 3.2 Content-Addressed Truth
Hashes, not servers or authorities, define integrity. URIs are stable, content is immutable.

### 3.3 Sequential History Without Consensus
Version chains provide tamper-evident history without requiring global agreement or blockchain infrastructure.

### 3.4 Compressible History
Long chains can be compressed via recursive proofs without losing verifiability guarantees.

### 3.5 Storeless Knowledge
RDF graphs are queryable on the client without requiring a triple store server, within practical size limits.

### 3.6 Separation of Data and Claims
Private data may exist without public exposure. Public claims may exist without revealing underlying data.

### 3.7 Provable Truth Without Disclosure
Zero-knowledge proofs allow public verification of properties without revealing the data itself. Proof generation and verification have asymmetric resource requirements.

### 3.8 Enforceable Privacy Budgets
Protocol-level mechanisms enable cross-verifier privacy budget enforcement without revealing interaction history.

### 3.9 Protocol Agnosticism with Concrete Profiles
No lock-in to specific cryptographic systems, storage networks, or trust models—but concrete conformance profiles ensure interoperability.

### 3.10 Explicit Trust Assumptions
Every trust assumption is documented. No hidden dependencies on external systems or authorities.

### 3.11 Self-Certifying Security Baseline
Discovery convenience layers (DNS, registries) must not compromise security guarantees achievable through self-certifying keys.

### 3.12 Graceful Degradation
Systems should fail safely and transparently when components are unavailable.

---

## 4. Architecture

HIRI consists of four layers, all operating primarily on the client:

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 4: Query & Verification                              │
│  • Local SPARQL (with entailment options)                   │
│  • Materialized Inference Verification                      │
│  • ZK Proof Verification                                    │
│  • Policy Evaluation                                        │
│  • Result Caching                                           │
└─────────────────────────────────────────────────────────────┘
                              ▲
┌─────────────────────────────────────────────────────────────┐
│  Layer 3: Storeless Index                                   │
│  • Private/Authorized RDF Index                             │
│  • Public Proof Index                                       │
│  • Delta Application                                        │
│  • Index Size Management                                    │
└─────────────────────────────────────────────────────────────┘
                              ▲
┌─────────────────────────────────────────────────────────────┐
│  Layer 2: Resolution & Discovery                            │
│  • Discovery (hierarchical profiles)                        │
│  • Manifest Fetch & Signature Verification                  │
│  • Chain Verification (with compaction support)             │
│  • Content Fetch & Hash Verification                        │
│  • Key Resolution & Rotation Handling                       │
└─────────────────────────────────────────────────────────────┘
                              ▲
┌─────────────────────────────────────────────────────────────┐
│  Layer 1: Protocol Foundation                               │
│  • Hash-IRI Identifiers                                     │
│  • Resolution Manifests                                     │
│  • Compaction Manifests                                     │
│  • Proof Manifests                                          │
│  • Key Documents                                            │
│  • Privacy Credentials                                      │
│  • Sequential Linking                                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Layer 1: Protocol Foundation

### 5.1 Hash-IRI Scheme

HIRI uses a stable identifier scheme:

```
hiri://<authority>/<type>/<identifier>
```

**Components:**

| Component | Description | Examples |
|-----------|-------------|----------|
| `authority` | Publisher identifier | `example.org`, `key:ed25519:abc123...` |
| `type` | Resource type | `data`, `proof`, `policy`, `key`, `vocab`, `compact` |
| `identifier` | Unique ID within scope | `Person123`, `AgeVerification`, `v1` |

**Authority Types (in order of security preference):**

1. **Key Authority** (RECOMMENDED): `key:<algorithm>:<public-key-hash>`
   - Self-certifying: the authority IS the key
   - No external trust dependencies for verification
   - Security baseline for HIRI
   - Example: `key:ed25519:7Hf9sK3m...`

2. **Consortium Authority**: `consortium:<consortium-id>`
   - Governed by multi-party Key Document
   - Requires threshold signatures
   - Example: `consortium:healthcare-standards-body`

3. **Domain Authority** (convenience layer): `example.org`
   - Relies on DNS for initial resolution
   - MUST publish a Key Document at a well-known location
   - Subject to DNS trust assumptions (documented in §14)
   - Security properties derive from underlying key, not domain

**Examples:**
```
hiri://key:ed25519:7Hf9sK3m.../data/Person123
hiri://key:ed25519:7Hf9sK3m.../proof/AgeVerification
hiri://consortium:w3c-credentials/policy/Over18
hiri://example.org/vocab/PersonOntology
hiri://key:ed25519:7Hf9sK3m.../compact/2025-Q1
```

### 5.2 Resolution Manifest

A Resolution Manifest maps a stable HIRI to versioned content.

```json
{
  "@context": [
    "https://hiri-protocol.org/spec/v2.1",
    "https://w3id.org/security/v2"
  ],
  "@id": "hiri://key:ed25519:7Hf9sK3m.../data/Person123",
  "@type": "hiri:ResolutionManifest",
  
  "hiri:version": 5,
  "hiri:branch": "main",
  
  "hiri:timing": {
    "created": "2025-01-15T14:30:00Z",
    "expires": "2026-01-15T14:30:00Z",
    "timestampProof": {
      "authority": "hiri://key:ed25519:TSAkey.../tsa/main",
      "signature": "0xTSA..."
    }
  },
  
  "hiri:content": {
    "hash": "sha256:Qmb4pXH3...",
    "format": "application/ld+json",
    "size": 4096,
    "compression": "none"
  },
  
  "hiri:delta": {
    "hash": "sha256:QmDelta...",
    "format": "application/json-patch+json",
    "appliesTo": "sha256:Qmb4pXH2...",
    "operations": 3
  },
  
  "hiri:contentLayers": {
    "public": {
      "hash": "sha256:QmPublic...",
      "authorization": "none"
    },
    "registered": {
      "hash": "sha256:QmRegistered...",
      "authorization": {
        "type": "capability",
        "required": ["role:registered"]
      }
    }
  },
  
  "hiri:chain": {
    "previous": "sha256:QmPrevious...",
    "previousBranch": "main",
    "genesisHash": "sha256:QmGenesis...",
    "depth": 5,
    "compactionRef": {
      "manifest": "hiri://key:ed25519:7Hf9sK3m.../compact/2024-Q4",
      "coversThrough": "sha256:QmCompacted...",
      "coversDepth": 1000
    }
  },
  
  "hiri:semantics": {
    "entailmentMode": "materialized",
    "baseRegime": "rdfs",
    "vocabularies": [
      "hiri://key:ed25519:vocab.../vocab/PersonOntology",
      "https://schema.org/"
    ],
    "predicateEquivalences": "hiri://key:ed25519:7Hf9sK3m.../vocab/equivalences",
    "materializationProof": "sha256:QmMatProof..."
  },
  
  "hiri:signature": {
    "type": "Ed25519Signature2020",
    "created": "2025-01-15T14:30:00Z",
    "verificationMethod": "hiri://key:ed25519:7Hf9sK3m.../key/main#key-1",
    "proofPurpose": "assertionMethod",
    "proofValue": "z58DAdFfa9..."
  }
}
```

**Field Specifications:**

| Field | Required | Description |
|-------|----------|-------------|
| `@id` | Yes | The HIRI being resolved |
| `@type` | Yes | Must be `hiri:ResolutionManifest` |
| `hiri:version` | Yes | Monotonically increasing integer |
| `hiri:branch` | Yes | Branch name (default: "main") |
| `hiri:timing` | Yes | Timestamp information (see §5.4) |
| `hiri:content` | Yes | Primary content reference |
| `hiri:delta` | No | Incremental update from previous version |
| `hiri:contentLayers` | No | Multi-level authorization layers |
| `hiri:chain` | Yes* | Chain linking (*absent only for genesis) |
| `hiri:semantics` | No | Semantic interpretation guidance |
| `hiri:signature` | Yes | Cryptographic signature |

### 5.3 Key Document

A Key Document establishes the cryptographic identity of an authority and enables key rotation.

```json
{
  "@context": [
    "https://hiri-protocol.org/spec/v2.1",
    "https://w3id.org/security/v2"
  ],
  "@id": "hiri://key:ed25519:7Hf9sK3m.../key/main",
  "@type": "hiri:KeyDocument",
  
  "hiri:version": 3,
  
  "hiri:authority": "key:ed25519:7Hf9sK3m...",
  "hiri:authorityType": "key",
  
  "hiri:domainAliases": [
    {
      "domain": "example.org",
      "verifiedAt": "2025-01-01T00:00:00Z",
      "verificationMethod": "dns-txt"
    }
  ],
  
  "hiri:activeKeys": [
    {
      "@id": "hiri://key:ed25519:7Hf9sK3m.../key/main#key-3",
      "@type": "Ed25519VerificationKey2020",
      "controller": "hiri://key:ed25519:7Hf9sK3m.../key/main",
      "publicKeyMultibase": "z6Mkf5rGM...",
      "purposes": ["assertionMethod", "authentication"],
      "validFrom": "2025-01-01T00:00:00Z",
      "validUntil": "2026-12-31T23:59:59Z"
    }
  ],
  
  "hiri:rotatedKeys": [
    {
      "@id": "hiri://key:ed25519:7Hf9sK3m.../key/main#key-2",
      "rotatedAt": "2025-01-01T00:00:00Z",
      "rotatedTo": "hiri://key:ed25519:7Hf9sK3m.../key/main#key-3",
      "reason": "scheduled-rotation",
      "verifyUntil": "2025-06-01T00:00:00Z"
    }
  ],
  
  "hiri:revokedKeys": [
    {
      "@id": "hiri://key:ed25519:7Hf9sK3m.../key/main#key-0",
      "revokedAt": "2023-06-15T00:00:00Z",
      "reason": "compromise-suspected",
      "manifestsInvalidAfter": "2023-06-01T00:00:00Z"
    }
  ],
  
  "hiri:recoveryKeys": [
    {
      "@id": "hiri://key:ed25519:7Hf9sK3m.../key/main#recovery-1",
      "@type": "Ed25519VerificationKey2020",
      "publicKeyMultibase": "z6MkRecov...",
      "purposes": ["keyRotation"],
      "threshold": 2,
      "holders": 3
    }
  ],
  
  "hiri:policies": {
    "rotationNotice": "P30D",
    "gracePeriodAfterRotation": "P180D",
    "minimumKeyValidity": "P365D",
    "compactionInterval": "P90D"
  },
  
  "hiri:chain": {
    "previous": "sha256:QmPrevKey...",
    "genesisHash": "sha256:QmGenesisKey...",
    "depth": 3
  },
  
  "hiri:signature": {
    "type": "Ed25519Signature2020",
    "created": "2025-01-01T00:00:00Z",
    "verificationMethod": "hiri://key:ed25519:7Hf9sK3m.../key/main#key-2",
    "proofPurpose": "keyRotation",
    "proofValue": "z58DAdFfa9..."
  }
}
```

**Key Lifecycle States:**

```
┌──────────┐     ┌──────────┐     ┌─────────────┐     ┌─────────┐
│  Created │────▶│  Active  │────▶│   Rotated   │────▶│ Expired │
└──────────┘     └──────────┘     └─────────────┘     └─────────┘
                      │                  │
                      │                  │ (grace period
                      │                  │  for verification)
                      ▼                  │
                 ┌─────────┐             │
                 │ Revoked │◀────────────┘
                 └─────────┘    (if compromise detected)
```

**Key States:**

| State | Can Sign New Manifests | Verifies Past Manifests |
|-------|------------------------|-------------------------|
| Active | Yes | Yes |
| Rotated | No | Yes (during grace period) |
| Expired | No | No (must re-sign) |
| Revoked | No | No (all signatures invalid after revocation point) |

### 5.4 Timestamp Trust Model

Timestamps in HIRI serve different purposes with different trust requirements:

**Advisory Timestamps** (low trust required):
- `hiri:timing.created`: When the manifest was created
- Used for display, sorting, cache management
- Not cryptographically verified

**Verified Timestamps** (high trust required):
- `hiri:timing.timestampProof`: Third-party attestation
- Required for privacy budget enforcement
- Required for time-sensitive proofs

**Timestamp Authority Integration:**

```json
{
  "hiri:timing": {
    "created": "2025-01-15T14:30:00Z",
    "timestampProof": {
      "authority": "hiri://key:ed25519:TSAkey.../tsa/main",
      "hash": "sha256:QmManifestHash...",
      "timestamp": "2025-01-15T14:30:05Z",
      "signature": "z58TSA..."
    }
  }
}
```

**When Verified Timestamps Are Required:**

| Use Case | Advisory OK | Verified Required |
|----------|-------------|-------------------|
| Content versioning | ✓ | |
| Cache invalidation | ✓ | |
| Privacy budget tracking | | ✓ |
| Time-bound proofs | | ✓ |
| Legal compliance | | ✓ |
| Audit trails | | ✓ |
| Chain compaction | | ✓ |

### 5.5 Proof Manifest

A Proof Manifest represents a verifiable claim using zero-knowledge proofs.

```json
{
  "@context": "https://hiri-protocol.org/spec/v2.1",
  "@id": "hiri://key:ed25519:7Hf9sK3m.../proof/AgeVerification/Person123",
  "@type": "hiri:ProofManifest",
  
  "hiri:version": 1,
  
  "hiri:timing": {
    "created": "2025-01-15T14:35:00Z",
    "validFrom": "2025-01-15T14:35:00Z",
    "validUntil": "2025-01-15T15:35:00Z",
    "timestampProof": {
      "authority": "hiri://key:ed25519:TSAkey.../tsa/main",
      "signature": "z58TSA..."
    }
  },
  
  "hiri:claim": {
    "policy": "hiri://consortium:standards/policy/Over21",
    "subject": "commitment:pedersen:0x789abc...",
    "subjectType": "commitment"
  },
  
  "hiri:proofSystem": {
    "@id": "hiri://consortium:registry/proof-system/groth16-bn254-v1",
    "verifier": {
      "hash": "sha256:QmVerifier...",
      "format": "application/wasm",
      "fetchFrom": [
        "ipfs://QmVerifier...",
        "https://hiri-protocol.org/verifiers/groth16-bn254-v1.wasm"
      ]
    }
  },
  
  "hiri:proof": {
    "hash": "sha256:QmProof...",
    "format": "application/octet-stream",
    "size": 256
  },
  
  "hiri:publicInputs": {
    "commitment": "0x789abc...",
    "policyHash": "sha256:QmPolicy...",
    "timestampHash": "sha256:QmTimestamp..."
  },
  
  "hiri:privacyMetadata": {
    "category": "age",
    "informationBits": 1,
    "budgetConsumption": {
      "credentialRequired": true,
      "accumulatorUpdate": "sha256:QmAccUpdate..."
    }
  },
  
  "hiri:generation": {
    "method": "client-local",
    "proverService": null
  },
  
  "hiri:chain": {
    "previous": "sha256:QmPrevProof...",
    "genesisHash": "sha256:QmGenesisProof..."
  },
  
  "hiri:signature": {
    "type": "Ed25519Signature2020",
    "verificationMethod": "hiri://key:ed25519:7Hf9sK3m.../key/main#key-3",
    "proofValue": "z58DAdFfa9..."
  }
}
```

### 5.6 Delta Format Specification

HIRI standardizes on JSON Patch (RFC 6902) with semantic extensions for RDF operations.

**Standard JSON Patch:**
```json
{
  "@context": "https://hiri-protocol.org/spec/v2.1/delta",
  "@type": "hiri:Delta",
  "format": "application/json-patch+json",
  "operations": [
    { "op": "replace", "path": "/name", "value": "Jane Doe" },
    { "op": "add", "path": "/email", "value": "jane@example.org" }
  ]
}
```

**RDF-Aware Delta (for graph content):**
```json
{
  "@context": "https://hiri-protocol.org/spec/v2.1/delta",
  "@type": "hiri:RDFDelta",
  "format": "application/hiri-rdf-patch",
  "operations": [
    {
      "op": "delete",
      "subject": "hiri://key:ed25519:7Hf9sK3m.../data/Person123",
      "predicate": "http://schema.org/name",
      "object": { "@value": "John Doe" }
    },
    {
      "op": "insert",
      "subject": "hiri://key:ed25519:7Hf9sK3m.../data/Person123",
      "predicate": "http://schema.org/name",
      "object": { "@value": "Jane Doe" }
    }
  ]
}
```

**Delta Verification:**
1. Fetch delta content
2. Verify delta hash matches manifest
3. Apply delta to cached content
4. Hash result
5. Verify result hash matches manifest content hash
6. If mismatch: fetch full content, report delta corruption

### 5.7 Compaction Manifest (NEW in v2.1)

A Compaction Manifest provides a cryptographic proof that a chain segment is valid, enabling clients to skip individual verification of historical manifests.

```json
{
  "@context": "https://hiri-protocol.org/spec/v2.1",
  "@id": "hiri://key:ed25519:7Hf9sK3m.../compact/2024-Q4",
  "@type": "hiri:CompactionManifest",
  
  "hiri:version": 1,
  
  "hiri:timing": {
    "created": "2025-01-01T00:00:00Z",
    "timestampProof": {
      "authority": "hiri://key:ed25519:TSAkey.../tsa/main",
      "signature": "z58TSA..."
    }
  },
  
  "hiri:scope": {
    "authority": "key:ed25519:7Hf9sK3m...",
    "resource": "hiri://key:ed25519:7Hf9sK3m.../data/Person123",
    "branch": "main"
  },
  
  "hiri:compactedRange": {
    "fromGenesis": true,
    "fromManifest": null,
    "fromVersion": 1,
    "toManifest": "sha256:QmManifest1000...",
    "toVersion": 1000,
    "manifestCount": 1000
  },
  
  "hiri:proofSystem": {
    "@id": "hiri://consortium:registry/proof-system/recursive-snark-v1",
    "type": "recursive-snark",
    "baseSystem": "groth16-bn254",
    "verifier": {
      "hash": "sha256:QmRecursiveVerifier...",
      "format": "application/wasm"
    }
  },
  
  "hiri:compactionProof": {
    "hash": "sha256:QmCompactionProof...",
    "format": "application/octet-stream",
    "size": 512
  },
  
  "hiri:publicInputs": {
    "genesisHash": "sha256:QmGenesis...",
    "finalManifestHash": "sha256:QmManifest1000...",
    "authorityKeyHash": "sha256:7Hf9sK3m...",
    "manifestCount": 1000,
    "keyRotationsIncluded": 3
  },
  
  "hiri:stateSnapshot": {
    "finalContentHash": "sha256:QmFinalContent...",
    "keyDocumentHash": "sha256:QmKeyDoc...",
    "accumulatedDeltas": false
  },
  
  "hiri:previousCompaction": {
    "manifest": null,
    "coversThrough": null
  },
  
  "hiri:signature": {
    "type": "Ed25519Signature2020",
    "verificationMethod": "hiri://key:ed25519:7Hf9sK3m.../key/main#key-3",
    "proofValue": "z58DAdFfa9..."
  }
}
```

**Compaction Proof Properties:**

The recursive SNARK proves:
1. Each manifest in the range has a valid signature from an authorized key
2. Each manifest correctly links to its predecessor
3. Key rotations within the range follow protocol rules
4. No revoked keys signed manifests after their revocation point
5. The final content hash is reachable from genesis through valid transformations

**Compaction Benefits:**

| Chain Length | Without Compaction | With Compaction |
|--------------|-------------------|-----------------|
| 100 manifests | ~100 signature verifications | 1 SNARK verification |
| 1,000 manifests | ~1,000 signature verifications | 1 SNARK verification |
| 10,000 manifests | ~10,000 signature verifications | 1-2 SNARK verifications |

---

## 6. Layer 2: Resolution & Discovery

### 6.1 Discovery Profile Hierarchy

HIRI defines a hierarchical discovery model where **self-certifying security is the baseline** and convenience layers are optional additions.

```
┌─────────────────────────────────────────────────────────────┐
│                    Security Guarantee                        │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  HIRI-KEY (Self-Certifying)                         │   │
│  │  • Security baseline                                │   │
│  │  • No external trust dependencies                   │   │
│  │  • All other profiles MUST resolve to keys          │   │
│  └─────────────────────────────────────────────────────┘   │
│                          ▲                                  │
│                          │ derives security from            │
│  ┌───────────────────────┴─────────────────────────────┐   │
│  │  Convenience Layers (optional)                      │   │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐   │   │
│  │  │  HIRI-DNS   │ │  HIRI-IPNS  │ │  HIRI-REG   │   │   │
│  │  │  (domains)  │ │  (IPFS)     │ │  (registry) │   │   │
│  │  └─────────────┘ └─────────────┘ └─────────────┘   │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**Critical Invariant:** All discovery profiles MUST ultimately resolve to a Key Document. The domain or registry provides *discoverability*, not *security*. Security derives exclusively from cryptographic verification against the resolved key.

#### 6.1.1 Profile: Key-Based Discovery (HIRI-KEY) — SECURITY BASELINE

**Status:** REQUIRED for all implementations. This is the security foundation.

**Mechanism:** Self-certifying authorities with deterministic manifest locations

**Resolution Process:**
```
1. Authority IS the public key hash (e.g., key:ed25519:7Hf9sK3m...)
2. Manifest location derived deterministically or provided out-of-band
3. Fetch manifest from any available source
4. Verify signature against authority key
5. Security is COMPLETE—no external trust required
```

**Deterministic Location Derivation:**
```
Given: authority = key:ed25519:7Hf9sK3m...
       type = data
       identifier = Person123

Content-addressed location (IPFS):
  /ipns/{authority-as-ipns-key}/manifest/{type}/{identifier}

Or with well-known gateway:
  https://hiri.gateway.example/{authority}/{type}/{identifier}/manifest.json
```

**Trust Assumptions:**
- Cryptographic signature verification only
- No DNS, no registries, no external authorities
- If signature verifies against authority key, content is authentic

**Advantages:**
- Maximum decentralization
- Maximum security
- Works offline after initial fetch
- No infrastructure dependencies

**When to Use:**
- High-security applications
- Offline-first systems
- Long-term archival
- Any case where security cannot be compromised

#### 6.1.2 Profile: DNS-Based Discovery (HIRI-DNS) — CONVENIENCE LAYER

**Status:** OPTIONAL convenience layer. Security still derives from HIRI-KEY.

**Mechanism:** DNS TXT records + HTTPS well-known endpoints → Key Document → verification

**Resolution Process:**
```
1. Extract domain from authority (e.g., "example.org")
2. Query DNS TXT record: _hiri.example.org
3. Parse TXT record for Key Document location
4. Fetch Key Document
5. Extract canonical key authority from Key Document
6. FROM THIS POINT: resolution proceeds as HIRI-KEY
7. All verification is against the key, not the domain
```

**DNS TXT Record Format:**
```
_hiri.example.org. 300 IN TXT "v=HIRI1; key=hiri://key:ed25519:7Hf9sK3m.../key/main"
```

**Well-Known Endpoints:**
```
GET /.well-known/hiri/key → Key Document
GET /.well-known/hiri/manifest/{type}/{identifier}
```

**Trust Model:**
- DNS provides *discoverability* of the key
- DNS does NOT provide security
- Compromise of DNS can cause denial of service or misdirection
- Compromise of DNS CANNOT forge valid signatures
- Key pinning RECOMMENDED after first successful resolution

**Advantages:**
- Familiar to users (domain names)
- Easy initial deployment
- Works with existing web infrastructure

**Limitations:**
- Discovery depends on DNS availability
- Initial resolution subject to DNS attacks (mitigated by key pinning)
- Domain ownership can change

**Security Downgrade Warning:**
If a client accepts domain-based authority without resolving to and pinning the underlying key, security is degraded. Implementations SHOULD warn users and MUST document this behavior.

#### 6.1.3 Profile: IPNS-Based Discovery (HIRI-IPNS) — CONVENIENCE LAYER

**Status:** OPTIONAL convenience layer for decentralized discovery.

**Mechanism:** IPFS naming system → Key Document → verification

**Resolution Process:**
```
1. Authority provides IPNS name (derived from key or via DNSLINK)
2. Resolve IPNS name to current CID
3. Fetch Key Document from IPFS
4. Extract canonical key authority
5. FROM THIS POINT: resolution proceeds as HIRI-KEY
```

**Trust Model:**
- IPNS provides decentralized discoverability
- Security derives from key verification, not IPFS
- IPNS key should ideally BE the HIRI authority key

**Advantages:**
- Decentralized discovery
- Content-addressed verification
- Censorship resistance

**Limitations:**
- IPNS propagation can be slow
- Requires IPFS infrastructure or gateways

#### 6.1.4 Profile: Registry-Based Discovery (HIRI-REG) — CONVENIENCE LAYER

**Status:** OPTIONAL convenience layer for enterprise/federated scenarios.

**Mechanism:** Trusted registries → Key Document → verification

**Resolution Process:**
```
1. Query registry for authority's Key Document location
2. Fetch Key Document
3. Extract canonical key authority
4. FROM THIS POINT: resolution proceeds as HIRI-KEY
```

**Registry API:**
```
GET /v1/resolve/{authority} → Key Document location
GET /v1/key/{authority} → Key Document (cached)
POST /v1/subscribe → Update notifications
WebSocket /v1/updates → Real-time updates
```

**Trust Model:**
- Registry provides efficient discovery
- Registry CANNOT forge signatures
- Multiple registries can be queried for redundancy
- Key pinning prevents registry misdirection after first resolution

**Advantages:**
- Efficient for high-volume systems
- Supports push updates
- Enterprise-friendly

**Limitations:**
- Registry availability dependency
- Potential centralization (mitigated by multiple registries)

### 6.2 Resolution Algorithm

```python
def resolve(hiri_uri: str, config: ResolverConfig) -> VerifiedContent:
    """
    Resolve a HIRI to verified content.
    
    Security invariant: All paths ultimately verify against a cryptographic key.
    """
    
    # Step 1: Parse HIRI
    authority, resource_type, identifier = parse_hiri(hiri_uri)
    
    # Step 2: Resolve to Key Document (profile-specific discovery)
    key_document = resolve_key_document(authority, config)
    
    # Step 3: Extract canonical key authority
    # THIS IS THE SECURITY ANCHOR
    canonical_authority = key_document.authority
    if key_document.authorityType != "key":
        # For domain/consortium authorities, extract underlying key
        canonical_authority = extract_key_authority(key_document)
    
    # Step 4: Check key pinning (if enabled)
    if config.key_pinning.enabled:
        pinned = config.key_pinning.get(hiri_uri)
        if pinned and pinned != canonical_authority:
            raise SecurityError(f"Key mismatch: expected {pinned}, got {canonical_authority}")
        if not pinned:
            config.key_pinning.pin(hiri_uri, canonical_authority)
    
    # Step 5: Discover manifest location
    manifest_location = discover_manifest(
        canonical_authority, resource_type, identifier, config.discovery_profile
    )
    
    # Step 6: Fetch manifest
    manifest = fetch_manifest(manifest_location)
    
    # Step 7: Get signing key from Key Document
    signing_key = get_verification_key(
        key_document, 
        manifest.signature.verificationMethod
    )
    
    # Step 8: Validate key status
    key_status = validate_key_status(signing_key, key_document, manifest.timing)
    if key_status == KeyStatus.REVOKED:
        raise KeyError(f"Signing key revoked: {signing_key.id}")
    if key_status == KeyStatus.EXPIRED:
        raise KeyError(f"Signing key expired: {signing_key.id}")
    
    # Step 9: Verify manifest signature
    # THIS IS WHERE SECURITY IS ESTABLISHED
    if not verify_signature(manifest, signing_key):
        raise SignatureError(f"Invalid signature on manifest: {hiri_uri}")
    
    # Step 10: Verify chain integrity (with compaction support)
    verify_chain_with_compaction(manifest, key_document, config)
    
    # Step 11: Determine authorization and fetch content
    auth_level = determine_authorization(manifest, config.credentials)
    content_ref = select_content_layer(manifest, auth_level)
    content = fetch_and_verify_content(manifest, content_ref, config)
    
    # Step 12: Handle proof manifests specially
    if manifest.type == "hiri:ProofManifest":
        verify_zk_proof(manifest, content, config)
    
    # Step 13: Cache and return
    config.cache.store(content_ref.hash, content)
    
    return VerifiedContent(
        data=content,
        manifest=manifest,
        verification=VerificationMetadata(
            canonical_authority=canonical_authority,
            key_status=key_status,
            chain_verified=True,
            compaction_used=manifest.chain.compactionRef is not None
        )
    )


def verify_chain_with_compaction(
    manifest: Manifest, 
    key_document: KeyDocument,
    config: ResolverConfig
):
    """
    Verify manifest chain, using compaction proofs when available.
    """
    # Check for compaction reference
    if manifest.chain and manifest.chain.compactionRef:
        compaction = fetch_compaction_manifest(manifest.chain.compactionRef.manifest)
        
        # Verify compaction proof
        if verify_compaction_proof(compaction, config):
            # Compaction covers history up to coversThrough
            # Only need to verify from there to current
            verify_chain_segment(
                from_hash=manifest.chain.compactionRef.coversThrough,
                to_manifest=manifest,
                key_document=key_document,
                config=config
            )
            return
        else:
            log.warning("Compaction proof invalid, falling back to full verification")
    
    # No compaction or compaction failed: verify full chain
    verify_chain_full(manifest, key_document, config)


def verify_compaction_proof(compaction: CompactionManifest, config: ResolverConfig) -> bool:
    """
    Verify a recursive SNARK compaction proof.
    """
    # Fetch verifier
    verifier_code = fetch_content(compaction.proofSystem.verifier.hash)
    if hash_content(verifier_code) != compaction.proofSystem.verifier.hash:
        return False
    
    # Load verifier (sandboxed)
    verifier = load_wasm_verifier(verifier_code, config.sandbox)
    
    # Fetch proof
    proof = fetch_content(compaction.compactionProof.hash)
    
    # Verify
    result = verifier.verify(
        public_inputs=compaction.publicInputs,
        proof=proof
    )
    
    return result.valid
```

### 6.3 Cold-Start Strategies

New clients face a bootstrapping problem. HIRI provides multiple strategies with explicit trade-offs:

#### 6.3.1 Full Verification (Maximum Security)

- Verify complete chain from genesis
- No external trust assumptions beyond cryptography
- High initial cost

**When to use:** High-security contexts, audit scenarios, legal compliance

#### 6.3.2 Compaction-Assisted (RECOMMENDED for long chains)

- Verify most recent compaction proof (single SNARK verification)
- Verify chain segment from compaction to current
- Trust assumption: compaction proof system is sound

**When to use:** Long-lived entities, mobile clients, general production use

#### 6.3.3 Trusted Checkpoint (Pragmatic)

- Verify chain back to a published checkpoint
- Trust assumption: checkpoint publisher is honest
- Checkpoint should be multi-party attested

**When to use:** Enterprise deployments, moderate-security applications

#### 6.3.4 Trust-On-First-Use (TOFU)

- Accept first-seen manifest
- Verify subsequent updates against first-seen
- Vulnerable to first-contact attacks

**When to use:** Development, testing, low-stakes applications only

---

## 7. Layer 3: Storeless Index

### 7.1 Index Architecture

Clients maintain local indices without requiring server infrastructure. Two logically isolated indices ensure privacy:

```
┌─────────────────────────────────────────┐
│         Client Application               │
├─────────────────────────────────────────┤
│                                         │
│  ┌─────────────────┐ ┌─────────────────┐│
│  │  Private Index  │ │  Public Index   ││
│  │                 │ │                 ││
│  │ • Full RDF data │ │ • Proof refs    ││
│  │ • Credentials   │ │ • Policy refs   ││
│  │ • Personal info │ │ • Commitments   ││
│  │                 │ │                 ││
│  │ NEVER EXPOSED   │ │ FREELY SHARED   ││
│  └─────────────────┘ └─────────────────┘│
│           │                   │         │
│           │    NO JOIN        │         │
│           └───────X───────────┘         │
│                                         │
└─────────────────────────────────────────┘
```

**Critical Invariant:** Private and public indices MUST NOT be joined in queries.

### 7.2 Index Size Management

Local RDF indices have practical limits:

| Tier | Triple Count | Recommended Index | Entailment Support |
|------|--------------|-------------------|-------------------|
| Small | < 10,000 | In-memory | Full runtime |
| Medium | 10,000 - 100,000 | SQLite-backed | Materialized preferred |
| Large | 100,000 - 1,000,000 | Dedicated store | Materialized required |
| Enterprise | > 1,000,000 | External service | Materialized + federated |

### 7.3 Index Building Process

```python
def build_index(manifest: ResolvedManifest, index_manager: IndexManager):
    """
    Build or update local index from manifest content.
    """
    content = manifest.verified_content
    
    if manifest.type == "hiri:ResolutionManifest":
        # Parse base graph
        graph = parse_rdf(content, manifest.semantics.vocabularies)
        
        # Handle entailment based on mode
        if manifest.semantics.entailmentMode == "materialized":
            # Publisher has pre-computed inferences
            # Verify materialization if proof provided
            if manifest.semantics.materializationProof:
                verify_materialization(graph, manifest.semantics)
            # Graph already includes inferences—use directly
            
        elif manifest.semantics.entailmentMode == "runtime":
            # Client must compute inferences
            if index_manager.supports_runtime_entailment(manifest.semantics.baseRegime):
                graph = apply_entailment(graph, manifest.semantics.baseRegime)
            else:
                raise CapabilityError("Client cannot perform required entailment")
                
        elif manifest.semantics.entailmentMode == "none":
            # No inference—use graph as-is
            pass
        
        # Add to private index
        index_manager.private.add_graph(
            graph,
            provenance=manifest.id,
            version=manifest.version
        )
        
    elif manifest.type == "hiri:ProofManifest":
        # Add to public index
        proof_record = ProofRecord(
            id=manifest.id,
            policy=manifest.claim.policy,
            subject=manifest.claim.subject,
            valid_from=manifest.timing.validFrom,
            valid_until=manifest.timing.validUntil,
            verified=True
        )
        index_manager.public.add_proof(proof_record)
```

---

## 8. Layer 4: Query & Verification

### 8.1 Entailment Modes

HIRI v2.1 introduces explicit entailment modes to address the performance concerns of client-side reasoning.

#### 8.1.1 Entailment Mode: Runtime

Traditional approach where the client computes inferences.

```json
{
  "hiri:semantics": {
    "entailmentMode": "runtime",
    "baseRegime": "rdfs",
    "vocabularies": ["https://schema.org/"]
  }
}
```

**Characteristics:**
- Client performs RDFS/OWL reasoning
- Flexible: client can use any compatible reasoner
- Expensive: unsuitable for large graphs on constrained devices

**When to use:** Small graphs, powerful clients, maximum flexibility

#### 8.1.2 Entailment Mode: Materialized (NEW in v2.1)

Publisher pre-computes the inferential closure and signs the result.

```json
{
  "hiri:semantics": {
    "entailmentMode": "materialized",
    "baseRegime": "rdfs",
    "vocabularies": ["https://schema.org/"],
    "materializationProof": "sha256:QmMatProof...",
    "materializationMethod": "full-closure"
  }
}
```

**Materialization Document:**

```json
{
  "@context": "https://hiri-protocol.org/spec/v2.1",
  "@type": "hiri:MaterializationProof",
  
  "hiri:sourceGraph": {
    "hash": "sha256:QmSourceGraph...",
    "tripleCount": 1000
  },
  
  "hiri:materializedGraph": {
    "hash": "sha256:QmMaterializedGraph...",
    "tripleCount": 1500
  },
  
  "hiri:entailmentRegime": "rdfs",
  "hiri:vocabulariesUsed": [
    {
      "uri": "https://schema.org/",
      "hash": "sha256:QmSchemaOrg..."
    }
  ],
  
  "hiri:reasoner": {
    "name": "Apache Jena",
    "version": "4.10.0",
    "configuration": "rdfs-full"
  },
  
  "hiri:inferredTriples": {
    "count": 500,
    "hash": "sha256:QmInferredOnly..."
  },
  
  "hiri:verificationHint": {
    "method": "sample-check",
    "sampleSize": 50,
    "sampleSeed": "0x12345..."
  }
}
```

**Client Verification Options:**

| Verification Level | Trust | Compute Cost |
|-------------------|-------|--------------|
| Trust publisher | Full trust in publisher's reasoner | None |
| Sample check | Verify random sample of inferences | Low |
| Full recompute | Recompute closure independently | High |
| ZK proof (future) | Cryptographic proof of correct reasoning | Medium |

**Sample Check Algorithm:**

```python
def verify_materialization_sample(
    source_graph: Graph,
    materialized_graph: Graph,
    proof: MaterializationProof,
    config: VerificationConfig
) -> bool:
    """
    Verify a random sample of materialized inferences.
    """
    # Extract inferred triples (materialized - source)
    inferred = materialized_graph - source_graph
    
    # Deterministic sample selection
    rng = seeded_random(proof.verificationHint.sampleSeed)
    sample = rng.sample(inferred, proof.verificationHint.sampleSize)
    
    # Verify each sampled inference
    for triple in sample:
        if not can_derive(source_graph, triple, proof.entailmentRegime):
            return False
    
    # Check no obviously invalid triples
    for triple in inferred:
        if is_obviously_invalid(triple, proof.entailmentRegime):
            return False
    
    return True
```

**Characteristics:**
- Publisher bears reasoning cost
- Client verifies (trust, sample, or full)
- Suitable for constrained devices
- Graph content is pre-expanded

**When to use:** Mobile clients, large graphs, OWL-RL, constrained environments

#### 8.1.3 Entailment Mode: None

No inference—graph is used exactly as provided.

```json
{
  "hiri:semantics": {
    "entailmentMode": "none"
  }
}
```

**When to use:** Raw data, application-specific semantics, maximum control

### 8.2 Query Execution

```python
def execute_query(
    query: str, 
    index_manager: IndexManager,
    query_context: QueryContext
) -> QueryResult:
    """
    Execute SPARQL query against local index.
    """
    parsed = parse_sparql(query)
    
    # Security check
    if uses_both_indices(parsed):
        raise SecurityError("Cannot query across private and public indices")
    
    # Determine target
    if references_proofs(parsed):
        target = index_manager.public
    else:
        target = index_manager.private
    
    # Authorization check
    if target == index_manager.private:
        if not query_context.credentials:
            raise AuthorizationError("Private index requires credentials")
    
    # Execute with limits
    try:
        with timeout(query_context.timeout_seconds):
            result = target.execute(parsed)
    except TimeoutError:
        raise QueryError("Query execution timeout")
    
    if len(result) > query_context.max_results:
        result = result[:query_context.max_results]
        result.truncated = True
    
    return result
```

### 8.3 Proof Verification

```python
def verify_proof(manifest: ProofManifest, config: VerifierConfig) -> ProofVerificationResult:
    """
    Verify a zero-knowledge proof.
    """
    # Resolve proof system
    proof_system = resolve_proof_system(manifest.proofSystem.id)
    
    # Fetch and verify verifier code
    verifier_code = fetch_content(manifest.proofSystem.verifier.hash)
    if hash_content(verifier_code) != manifest.proofSystem.verifier.hash:
        raise VerifierError("Verifier code hash mismatch")
    
    # Allowlist check (defense in depth)
    if config.verifier_allowlist:
        if manifest.proofSystem.verifier.hash not in config.verifier_allowlist:
            raise VerifierError("Verifier not in allowlist")
    
    # Load and execute verifier
    verifier = load_wasm_verifier(verifier_code, config.sandbox)
    proof = fetch_content(manifest.proof.hash)
    
    result = verifier.verify(
        public_inputs=manifest.publicInputs,
        proof=proof
    )
    
    if not result.valid:
        return ProofVerificationResult(valid=False, reason="Proof verification failed")
    
    # Check timing constraints
    now = get_verified_time(config)
    if manifest.timing.validFrom and now < manifest.timing.validFrom:
        return ProofVerificationResult(valid=False, reason="Proof not yet valid")
    if manifest.timing.validUntil and now > manifest.timing.validUntil:
        return ProofVerificationResult(valid=False, reason="Proof expired")
    
    return ProofVerificationResult(
        valid=True,
        policy=manifest.claim.policy,
        subject=manifest.claim.subject,
        verified_at=now
    )
```

---

## 9. Zero-Knowledge Claims Layer

### 9.1 Overview

HIRI supports zero-knowledge proofs as first-class artifacts, enabling:

> **"Public verification that private data satisfies a policy—without revealing the data."**

### 9.2 Proof Generation Architecture

**Critical Asymmetry:** Proof verification is lightweight. Proof generation is expensive.

#### 9.2.1 Client-Local Generation

```
┌──────────────────────────────────────┐
│            Client Device             │
│  ┌─────────────┐  ┌───────────────┐ │
│  │ Private Data│─▶│  ZK Prover    │ │
│  └─────────────┘  │  (local)      │ │
│                   └───────┬───────┘ │
│                           ▼         │
│                   ┌───────────────┐ │
│                   │     Proof     │ │
│                   └───────────────┘ │
└──────────────────────────────────────┘
```

**Requirements:** Significant CPU/memory, local proving key

**Manifest Annotation:**
```json
{
  "hiri:generation": {
    "method": "client-local",
    "provingTime": "PT5S",
    "hardwareRequirements": { "memory": "4GB", "cpu": "modern-x64" }
  }
}
```

#### 9.2.2 Delegated Generation (Prover Service)

```
┌───────────────┐          ┌─────────────────────┐
│    Client     │          │   Prover Service    │
│ ┌───────────┐ │ encrypt  │  ┌───────────────┐  │
│ │Private    │─┼─────────▶│  │ Secure Enclave│  │
│ │Data       │ │          │  │    Prover     │  │
│ └───────────┘ │          │  └───────┬───────┘  │
│               │◀─────────┼──────────┘          │
│               │  proof   │   (data deleted)    │
└───────────────┘          └─────────────────────┘
```

**Trust Assumptions:** Prover service sees data (in enclave). Must trust non-retention.

#### 9.2.3 Threshold/MPC Generation

Multiple parties each hold shares; no single party sees complete data.

**Trust Assumptions:** Threshold of parties must be honest.

### 9.3 Proof System Registry

```json
{
  "@context": "https://hiri-protocol.org/spec/v2.1",
  "@id": "hiri://consortium:registry/proof-system/groth16-bn254-v1",
  "@type": "hiri:ProofSystem",
  
  "hiri:name": "Groth16 over BN254",
  "hiri:version": "1.0.0",
  
  "hiri:securityProperties": {
    "soundness": "computational",
    "zeroKnowledge": "perfect",
    "assumptions": ["discrete-log-bn254", "knowledge-of-exponent"],
    "trustedSetup": true,
    "quantumResistant": false
  },
  
  "hiri:performance": {
    "proofSize": 128,
    "verificationTime": "~10ms",
    "provingTime": "circuit-dependent"
  },
  
  "hiri:implementations": {
    "wasm": {
      "hash": "sha256:QmWasmVerifier...",
      "audit": "hiri://consortium:audits/groth16-wasm-v1"
    }
  }
}
```

### 9.4 Privacy Budget Framework

**Status:** v2.1 adds protocol-level enforcement via cryptographic accumulators. Application-level policies remain important for domain-specific concerns.

#### 9.4.1 Information Leakage Model

| Proof Type | Information Revealed |
|------------|---------------------|
| Binary predicate | 1 bit |
| Range proof (decade) | ~3.3 bits |
| Exact value proof | log₂(range) bits |
| Set membership | log₂(set size) bits |

#### 9.4.2 Composition Risk

Multiple proofs compound:
```
Proof 1: Over 21 → ~1 bit
Proof 2: Under 65 → ~1 bit  
Proof 3: California resident → ~4 bits
Proof 4: Works in tech → ~3 bits
Combined: ~9 bits → ~1/500 of population
```

### 9.5 Privacy Accumulators (NEW in v2.1)

#### 9.5.1 The Enforcement Problem

In v2.0, privacy budgets were advisory: a malicious verifier could extract unlimited proofs. v2.1 introduces **Privacy Accumulators**—cryptographic structures that enforce budget limits across verifiers without revealing interaction history.

#### 9.5.2 Privacy Credential

A Privacy Credential is a cryptographic token that:
- Tracks cumulative information disclosure
- Can be updated with each proof
- Can prove "budget not exceeded" without revealing which proofs were issued
- Is bound to a subject commitment

```json
{
  "@context": "https://hiri-protocol.org/spec/v2.1",
  "@id": "hiri://key:ed25519:7Hf9sK3m.../privacy-credential/Subject123",
  "@type": "hiri:PrivacyCredential",
  
  "hiri:version": 47,
  
  "hiri:subject": {
    "commitment": "commitment:pedersen:0x789abc...",
    "blindingFactor": "encrypted:holder-key:0x..."
  },
  
  "hiri:budget": {
    "totalBits": 10,
    "currentUsage": 5,
    "usageCommitment": "commitment:pedersen:0xUsage...",
    "categoryCommitments": {
      "demographics": "commitment:pedersen:0xDemo...",
      "location": "commitment:pedersen:0xLoc...",
      "employment": "commitment:pedersen:0xEmp..."
    }
  },
  
  "hiri:accumulator": {
    "type": "rsa-accumulator",
    "value": "0xAccumulator...",
    "membershipWitness": "0xWitness..."
  },
  
  "hiri:timing": {
    "created": "2025-01-01T00:00:00Z",
    "lastUpdated": "2025-01-15T14:35:00Z",
    "validUntil": "2025-12-31T23:59:59Z"
  },
  
  "hiri:issuer": {
    "authority": "hiri://consortium:privacy-authority/issuer/main",
    "signature": "z58Issuer..."
  }
}
```

#### 9.5.3 Proof Issuance with Budget Enforcement

```
┌─────────────────────────────────────────────────────────────────────┐
│                 Proof Issuance with Privacy Accumulator              │
└─────────────────────────────────────────────────────────────────────┘

  Subject              Privacy Authority           Verifier
     │                        │                       │
     │ 1. Request proof       │                       │
     │    + credential        │                       │
     │───────────────────────▶│                       │
     │                        │                       │
     │                   2. Verify credential         │
     │                   3. Check budget remaining    │
     │                   4. If OK: update accumulator │
     │                        │                       │
     │ 5. Updated credential  │                       │
     │    + proof            │                       │
     │◀───────────────────────│                       │
     │                        │                       │
     │ 6. Present proof ──────┼──────────────────────▶│
     │    + budget proof      │                       │
     │                        │                       │
     │                        │     7. Verify proof   │
     │                        │     8. Verify budget  │
     │                        │        not exceeded   │
     │                        │                       │
```

#### 9.5.4 Budget Proof

When presenting a proof, the subject also presents a **Budget Proof**:

```json
{
  "@context": "https://hiri-protocol.org/spec/v2.1",
  "@type": "hiri:BudgetProof",
  
  "hiri:claim": "usage-under-budget",
  
  "hiri:publicInputs": {
    "budgetLimit": 10,
    "categoryLimit": {
      "demographics": 3
    },
    "accumulatorRoot": "0xAccRoot...",
    "credentialCommitment": "0xCredCommit..."
  },
  
  "hiri:proof": {
    "hash": "sha256:QmBudgetProof...",
    "system": "hiri://consortium:registry/proof-system/groth16-bn254-v1"
  }
}
```

**The Budget Proof proves (in zero knowledge):**
1. Subject holds a valid credential
2. Credential shows usage ≤ budget
3. Credential is in the accumulator (not revoked/outdated)
4. The proof being requested fits within remaining budget

**Verifier's view:**
- Verifier learns: "Subject has budget remaining for this proof type"
- Verifier does NOT learn: which other verifiers subject interacted with, total usage, interaction history

#### 9.5.5 Accumulator Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Privacy Authority                         │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                Global Accumulator                      │  │
│  │  • Contains all valid credential commitments           │  │
│  │  • Updated on credential issuance/update/revocation    │  │
│  │  • Published periodically (e.g., hourly)               │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │ Credential DB    │  │ Update Service   │                │
│  │ (encrypted)      │  │ (enclave)        │                │
│  └──────────────────┘  └──────────────────┘                │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ accumulator root
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Public Bulletin                           │
│  • Accumulator root published on schedule                   │
│  • Verifiers fetch current root                             │
│  • Subjects update membership witnesses                     │
└─────────────────────────────────────────────────────────────┘
```

#### 9.5.6 Trust Model for Privacy Accumulators

| Component | Trust Assumption | Mitigation |
|-----------|------------------|------------|
| Privacy Authority | Correctly tracks budgets | Multiple authorities, audits, reputation |
| Accumulator | Correctly reflects valid credentials | Public bulletin, verifiable updates |
| Subject | Presents current credential | Accumulator membership proof |
| Verifier | Checks budget proof | Protocol enforcement |

**Key Property:** Even a malicious verifier cannot cause a subject to exceed their budget, because the Privacy Authority will refuse to update the credential beyond budget limits.

**Limitation:** Subject must interact with Privacy Authority for each proof. This is a trade-off: decentralized issuance would require blockchain-like global state.

**FNSR Governance Note (ARIADNE T-011):** Within the FNSR ecosystem, the Privacy Authority's relationship to ARCHON governance is an open design question. Three candidate models:
1. **ARCHON-governed entity** — Privacy Authority operates under ARCHON's governance framework, subject to the same auditability and human-override non-negotiables.
2. **Infrastructure primitive** — Privacy Authority operates outside ARCHON's jurisdiction, like DNS or storage infrastructure. ARCHON governs what the system *does* with privacy budgets, not the budget enforcement mechanism itself.
3. **Federated model** — Multiple Privacy Authorities (§9.5.7) with accepted budget gaming at boundaries, consistent with the distributed-authority design principle.

This tension is documented in the ARIADNE tension log as T-011 and remains unresolved pending ecosystem-level design decision.

#### 9.5.7 Federated Privacy Authorities

For decentralization, multiple Privacy Authorities can operate:

```json
{
  "@type": "hiri:PrivacyAuthorityFederation",
  
  "hiri:authorities": [
    "hiri://consortium:privacy-eu/authority/main",
    "hiri://consortium:privacy-us/authority/main",
    "hiri://consortium:privacy-apac/authority/main"
  ],
  
  "hiri:interoperability": {
    "crossAuthorityProofs": true,
    "sharedAccumulator": false,
    "budgetSynchronization": "eventual"
  }
}
```

**Trade-off:** Cross-authority scenarios may allow budget gaming (getting proofs from multiple authorities). Full prevention requires either:
- Single global authority (centralization)
- Cross-authority budget proofs (complex)
- Accept some leakage in federated model (pragmatic)

### 9.6 Application Responsibilities

Even with protocol-level accumulators, applications MUST:

1. **Request budget proofs** for sensitive operations
2. **Implement domain-specific limits** beyond protocol budgets
3. **Warn users** about high-information proofs
4. **Consider auxiliary data** in risk assessment
5. **Provide user control** over proof generation

---

## 10. Key Management & Rotation

### 10.1 Key Lifecycle

```
┌──────────┐     ┌──────────┐     ┌─────────────┐     ┌─────────┐
│  Created │────▶│  Active  │────▶│   Rotated   │────▶│ Expired │
└──────────┘     └──────────┘     └─────────────┘     └─────────┘
                      │                  │
                      ▼                  │
                 ┌─────────┐             │
                 │ Revoked │◀────────────┘
                 └─────────┘
```

### 10.2 Rotation Protocol

#### 10.2.1 Scheduled Rotation

```json
{
  "@type": "hiri:KeyRotation",
  "hiri:type": "scheduled",
  
  "hiri:oldKey": {
    "@id": "hiri://key:ed25519:7Hf9sK3m.../key/main#key-2",
    "status": "rotated",
    "verifyUntil": "2025-07-01T00:00:00Z"
  },
  
  "hiri:newKey": {
    "@id": "hiri://key:ed25519:7Hf9sK3m.../key/main#key-3",
    "status": "active",
    "validFrom": "2025-01-01T00:00:00Z"
  },
  
  "hiri:signatures": [
    {
      "purpose": "old-key-authorizes-rotation",
      "verificationMethod": "hiri://key:ed25519:7Hf9sK3m.../key/main#key-2",
      "proofValue": "z58OldKey..."
    },
    {
      "purpose": "new-key-confirms-rotation",
      "verificationMethod": "hiri://key:ed25519:7Hf9sK3m.../key/main#key-3",
      "proofValue": "z58NewKey..."
    }
  ]
}
```

#### 10.2.2 Emergency Rotation (Compromise Response)

Uses recovery keys when normal rotation is not possible.

### 10.3 Consortium Key Management

Multi-party key management with threshold signatures.

---

## 11. Semantic Interoperability

### 11.1 The Vocabulary Problem

Different authorities use different vocabularies. If proofs are bound to predicates, interoperability breaks.

### 11.2 Vocabulary Alignment Strategies

#### 11.2.1 Shared Upper Ontology

Authorities agree on foundational vocabularies (Schema.org, BFO, Dublin Core).

**FNSR Integration Note:** Within the FNSR ecosystem, vocabulary alignment is handled by TagTeam's `BridgeOntologyLoader` (TagTeam Roadmap §6.5.4), which provides `owl:sameAs` and `owl:relatedTo` mappings between domain vocabularies and the BFO/CCO backbone. The Semantic Data Dictionary (v2.0) defines canonical term definitions. HIRI publishers within FNSR SHOULD reference these mechanisms in their `hiri:semantics.vocabularies` field and use the BridgeOntologyLoader's equivalence mappings for `hiri:semantics.predicateEquivalences`.

#### 11.2.2 Predicate Equivalence Declarations

```turtle
ex:birthDate owl:equivalentProperty schema:birthDate .
```

#### 11.2.3 Policy-Level Abstraction

Proofs reference abstract policies that accept multiple predicates:

```json
{
  "@id": "hiri://consortium:standards/policy/AgeOver21",
  "@type": "hiri:Policy",
  
  "hiri:acceptedPredicates": [
    "http://schema.org/birthDate",
    "http://example.org/vocab#birthDate",
    "http://xmlns.com/foaf/0.1/birthday"
  ]
}
```

### 11.3 Semantic Scoping

| Scope | Interoperability |
|-------|------------------|
| Single authority | Guaranteed |
| Shared vocabulary | High |
| Equivalence-mapped | Medium |
| Unmapped | None |

---

## 12. Chain Compaction (NEW in v2.1)

### 12.1 The Chain Length Problem

For long-lived entities (e.g., a person's identity over 20 years with daily updates), manifest chains can grow to thousands of entries. Full verification becomes impractical for mobile clients.

### 12.2 Solution: Recursive SNARKs

A **Compaction Manifest** uses recursive SNARKs to prove the validity of an entire chain segment in a single proof.

**What the Recursive SNARK Proves:**

1. **Signature Validity:** Every manifest in the range has a valid signature
2. **Chain Integrity:** Each manifest correctly links to its predecessor
3. **Key Authorization:** All signing keys were authorized at signing time
4. **Rotation Compliance:** Key rotations followed protocol rules
5. **No Revocation Violations:** No revoked keys signed manifests after revocation

### 12.3 Compaction Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│                      Chain Compaction Workflow                       │
└─────────────────────────────────────────────────────────────────────┘

  Publisher                    Compaction Service              Client
     │                               │                            │
     │ 1. Chain reaches threshold    │                            │
     │    (e.g., 1000 manifests)     │                            │
     │                               │                            │
     │ 2. Request compaction ───────▶│                            │
     │    (chain segment)            │                            │
     │                               │                            │
     │                          3. Generate recursive SNARK       │
     │                             proving chain validity         │
     │                               │                            │
     │ 4. Compaction manifest ◀──────│                            │
     │    + proof                    │                            │
     │                               │                            │
     │ 5. Publish compaction         │                            │
     │                               │                            │
     │ 6. Reference in new ──────────┼───────────────────────────▶│
     │    manifests                  │                            │
     │                               │                            │
     │                               │      7. Verify compaction  │
     │                               │         (single SNARK)     │
     │                               │                            │
     │                               │      8. Trust history      │
     │                               │         covered by         │
     │                               │         compaction         │
```

### 12.4 Compaction Policies

```json
{
  "hiri:policies": {
    "compactionInterval": "P90D",
    "compactionThreshold": 1000,
    "retainUncompactedDepth": 100,
    "compactionProofSystem": "hiri://consortium:registry/proof-system/recursive-snark-v1"
  }
}
```

| Policy | Description | Recommended |
|--------|-------------|-------------|
| `compactionInterval` | Time between compactions | 90 days |
| `compactionThreshold` | Manifest count trigger | 1000 |
| `retainUncompactedDepth` | Recent manifests to keep uncompacted | 100 |

### 12.5 Compaction Trust Model

| Trust Level | Verification Method |
|-------------|---------------------|
| Full | Verify recursive SNARK |
| Partial | Spot-check random manifests in range |
| Delegated | Trust compaction service reputation |

**Recommendation:** Verify recursive SNARK (single verification, strong guarantees).

### 12.6 Recursive Proof System Requirements

The compaction proof system must support:
- Recursive composition (proof of proofs)
- Variable-length inputs (arbitrary chain lengths)
- Efficient verification (constant or logarithmic)

**Recommended Systems:**

| System | Properties | Verification Cost |
|--------|------------|-------------------|
| Nova/SuperNova | Folding-based, efficient recursion | O(1) |
| Halo2 | No trusted setup, recursive | O(log n) |
| STARK-based | Post-quantum, transparent | O(log² n) |

---

## 13. Operational Considerations

### 13.1 Storage Infrastructure

HIRI is storage-agnostic but requires content-addressable retrieval.

| Option | Characteristics | Best For |
|--------|-----------------|----------|
| IPFS | Decentralized, content-addressed | Public data, censorship resistance |
| S3 + hash verification | Centralized, reliable | Enterprise, high availability |
| Local filesystem | Simple, offline-first | Personal/small deployments |

### 13.2 Cost Estimation

| Operation | Approximate Cost (2025) |
|-----------|------------------------|
| Manifest storage (IPFS pinned) | ~$0.01/GB/month |
| ZK proof generation (service) | $0.01-0.10/proof |
| Compaction proof generation | $0.50-5.00/compaction |
| Privacy credential update | $0.01-0.05/update |

### 13.3 Performance Guidelines

| Operation | Target Latency |
|-----------|----------------|
| Manifest verification | < 10ms |
| Compaction proof verification | < 100ms |
| SPARQL query (10K triples) | < 100ms |
| ZK proof verification | < 100ms |
| Privacy budget proof verification | < 50ms |

---

## 14. Security Model

### 14.1 Trust Assumptions

| Component | Trust Assumption | Mitigation |
|-----------|------------------|------------|
| Cryptographic primitives | Standard security | Audited implementations |
| Key management | Private keys remain private | HSMs, secure practices |
| Discovery (convenience layers) | May be unavailable/attacked | Key pinning, multiple profiles |
| ZK proof systems | Soundness | Audited implementations |
| Privacy Authority | Correct budget tracking | Multiple authorities, audits |
| Compaction service | Correct proofs | Verify recursive SNARK |

### 14.2 Discovery Security Hierarchy

| Profile | Security Derivation | Failure Mode |
|---------|---------------------|--------------|
| HIRI-KEY | Self-certifying | None (baseline) |
| HIRI-DNS | Via pinned key | DoS, initial misdirection |
| HIRI-IPNS | Via pinned key | DoS, propagation delay |
| HIRI-REG | Via pinned key | Registry unavailability |

**Critical:** All convenience profiles derive security from the underlying key. Domain/registry compromise cannot forge signatures.

### 14.3 Security Levels

| Level | Requirements |
|-------|--------------|
| Basic | Signature verification, TOFU |
| Standard | Chain verification, key pinning |
| High | Compaction verification, verified timestamps |
| Maximum | Full chain audit, hardware keys, multi-party |

---

## 15. Workflows

### 15.1 Publishing with Materialized Entailment

```
Publisher                                          Storage
   │                                                  │
   │ 1. Create RDF content                            │
   │ 2. Run reasoner (RDFS/OWL)                       │
   │ 3. Generate materialization proof                │
   │ 4. Create manifest with entailmentMode=materialized
   │ 5. Sign and publish ────────────────────────────▶│
```

### 15.2 Verification with Compaction

```
Client                           Storage            Compaction
   │                                │                   │
   │ 1. Fetch manifest              │                   │
   │◀────────────────────────────────                   │
   │                                │                   │
   │ 2. Check compactionRef         │                   │
   │ 3. Fetch compaction manifest ──┼──────────────────▶│
   │◀───────────────────────────────┼───────────────────│
   │                                │                   │
   │ 4. Verify recursive SNARK      │                   │
   │ 5. Verify recent chain segment │                   │
   │ 6. Trust complete history      │                   │
```

### 15.3 Proof with Privacy Budget

```
Subject             Privacy Authority            Verifier
   │                       │                        │
   │ 1. Request proof      │                        │
   │   + current credential│                        │
   │──────────────────────▶│                        │
   │                       │                        │
   │               2. Verify budget                 │
   │               3. Generate proof                │
   │               4. Update credential             │
   │               5. Update accumulator            │
   │                       │                        │
   │ 6. Proof + credential │                        │
   │◀──────────────────────│                        │
   │                       │                        │
   │ 7. Present proof + budget proof ──────────────▶│
   │                       │                        │
   │                       │        8. Verify proof │
   │                       │        9. Verify budget│
   │                       │       10. Accept       │
```

---

## 16. Conformance Profiles

### 16.1 HIRI-Core

**Required:** Hash-IRI parsing, manifest verification, chain verification

### 16.2 HIRI-Publisher

**Additional:** Manifest generation, signing, key management

### 16.3 HIRI-Verifier

**Additional:** Full chain verification, compaction support, key rotation handling

### 16.4 HIRI-ZK

**Additional:** Proof verification, policy resolution, privacy budget verification

### 16.5 HIRI-Compact (NEW)

**Additional:** Compaction manifest generation, recursive SNARK proving

### 16.6 HIRI-Privacy (NEW)

**Additional:** Privacy credential management, accumulator integration, budget proof generation/verification

---

## 17. Advantages & Trade-offs

### 17.1 Advantages

| Advantage | Description |
|-----------|-------------|
| **Offline verification** | No network for cached content verification |
| **Protocol independence** | No lock-in |
| **Self-certifying security** | DNS/registries are convenience, not security |
| **Compressible history** | Long chains don't burden clients |
| **Enforceable privacy budgets** | Protocol-level, not just advisory |
| **Lightweight reasoning** | Materialized entailment for constrained devices |

### 17.2 Trade-offs

| Trade-off | Impact | Mitigation |
|-----------|--------|------------|
| **Compaction infrastructure** | Requires recursive SNARK generation | Compaction services, batch processing |
| **Privacy Authority dependency** | Centralization for budget enforcement | Federation, multiple authorities |
| **Materialization trust** | Must trust or verify publisher's reasoning | Sample verification, ZK reasoning proofs (future) |
| **Key pinning complexity** | Clients must track pinned keys | Automatic pinning, pin management UI |

---

## 18. Roadmap

### Phase 1: v2.1 Finalization (Q1 2026)
- Finalize compaction specification
- Define privacy accumulator cryptographic details
- Publish materialization proof format

### Phase 2: Reference Implementation (Q2-Q3 2026)
- Compaction proof generation (Nova-based)
- Privacy accumulator implementation
- Materialized entailment tooling

### Phase 3: Ecosystem (Q4 2026)
- Federated Privacy Authority protocol
- Cross-authority budget proofs
- Compaction service infrastructure

### Phase 4: Production (2027)
- Security audits
- Performance optimization
- Enterprise deployment guides

---

## 19. Contributing

Contributions welcome in:
- Specification refinement
- Recursive SNARK implementations
- Privacy accumulator research
- Materialization verification methods
- Client implementations

---

## 20. References

### Standards
- RFC 6902: JSON Patch
- W3C RDF 1.1, SPARQL 1.1, JSON-LD 1.1

### Cryptography
- Groth16, PLONK, Nova/SuperNova
- RSA Accumulators, Bilinear Accumulators
- Anonymous Credentials (Camenisch-Lysyanskaya)

### Related Work
- IPFS, DID, Verifiable Credentials
- Semaphore (anonymous signaling)
- Zcash (shielded transactions)

---

## License

**Specification:** CC0 1.0 Universal (Public Domain)

**Reference Implementations:** Apache 2.0

---

**Version:** 2.1.0  
**Status:** Specification  
**Last Updated:** January 2026

---

*HIRI is a protocol, not a product. It belongs to everyone who uses it.*
