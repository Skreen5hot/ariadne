# HIRI Privacy & Confidentiality Extension

## Specification for Privacy-Preserving Publication on Content-Addressed Networks

**Version:** 1.4.1
**Previous:** 1.4.0
**Date:** March 2026
**Status:** Final
**Depends on:** HIRI Protocol Specification v3.1.1, HIRI-IPFS Integration Specification v4.0.0

---

## Document Status

This specification is a **normative extension** to the HIRI Protocol Specification v3.1.1. It defines five privacy modes for HIRI-signed content, ranging from anonymous publication to full public disclosure. Implementations MAY support any subset of these modes. The modes are independent — implementing Mode 2 does not require implementing Mode 3.

This specification does NOT modify any existing HIRI Protocol semantics. All verification, signing, chain integrity, and key lifecycle mechanisms defined in v3.1.1 remain unchanged. This extension adds new manifest fields, new resolution behaviors, and new content representation formats that compose with the existing protocol.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Normative References](#2-normative-references)
3. [Terminology](#3-terminology)
4. [Architectural Principles](#4-architectural-principles)
5. [Privacy Mode Declaration](#5-privacy-mode-declaration)
6. [Mode 1: Proof of Possession](#6-mode-1-proof-of-possession)
7. [Mode 2: Encrypted Distribution](#7-mode-2-encrypted-distribution)
8. [Mode 3: Selective Disclosure](#8-mode-3-selective-disclosure)
9. [Mode 4: Anonymous Publication](#9-mode-4-anonymous-publication)
10. [Mode 5: Third-Party Attestation](#10-mode-5-third-party-attestation)
11. [Privacy Lifecycle Transitions](#11-privacy-lifecycle-transitions)
12. [Resolution Behavior](#12-resolution-behavior)
13. [Key Distribution](#13-key-distribution)
14. [Delta Restrictions](#14-delta-restrictions)
15. [Security Considerations](#15-security-considerations)
16. [Conformance Levels](#16-conformance-levels)
17. [Future: Commitment-Based Content Model](#17-future-commitment-based-content-model)
18. [Companion Deliverables](#18-companion-deliverables)

**Appendices**

- [A: Manifest Examples](#appendix-a-manifest-examples)
- [B: Normative Test Vectors](#appendix-b-normative-test-vectors)
- [C: Privacy Mode Decision Matrix](#appendix-c-privacy-mode-decision-matrix)
- [D: Statement Index Construction](#appendix-d-statement-index-construction)
- [E: Suggested Key Distribution Patterns](#appendix-e-suggested-key-distribution-patterns-informative)

---

## Changelog: v1.4.0 → v1.4.1

| Change | Section | Breaking | Description |
|--------|---------|----------|-------------|
| **KeyDocument promoted to RECOMMENDED** | §13.1 | No | HIRI KeyDocument-based key bootstrapping is now the RECOMMENDED default pattern. Cache TTL guidance added. |
| **HPKE normative option** | §13.2 | No | HPKE (RFC 9180) is now a normative alternative for key encapsulation, not just a compatibility note. |
| **Disclosure suite decision table** | §8.6.3 | No | New subsection with a structured decision table for choosing HMAC vs BBS+. |
| **Metadata-hardening defaults** | §15.3 | No | Concrete recommended default parameters for padding, batching, and recipient obfuscation. |
| **Companion deliverables scope** | §18 | No | New section defining the scope and purpose of companion documents (reference implementations, developer guides, benchmarks). |
| **Publisher Neutrality principle** | §4.6 | No | Privacy modes serve non-human agents (synthetic moral persons) with equal rigor. |

**Implementation review corrections (v1.4.1):**

| Fix | Section | Description |
|-----|---------|-------------|
| HKDF label byte count | §13.2 | Corrected comment from "14 bytes" to "13 bytes" for `"hiri-cek-v1.1"` |
| Addressing mode consistency | §11.3 | New normative rule: logical plaintext hash addressing mode MUST be constant across a chain |
| Encrypted delta `appliesTo` | §14.3 | Clarified: `appliesTo` references plaintext hash, lives inside the encrypted delta blob, not in manifest metadata |
| Ephemeral key type | §13.3 | Clarified: ephemeral keypair is X25519-native, NOT Ed25519-then-converted. Key type summary table added. |
| HMAC key domain separation | §8.6.1 | Mode 3 HKDF `info` label changed to `"hiri-hmac-v1.1"` (was `"hiri-cek-v1.1"`) |
| BBS+ padding semantics | §8.6.2 | BBS+ signs ALL statements including padding; `statementCount` is the padded count |
| statementHash type annotation | §8.4.2 | Step 4 now explicitly says "raw 32-byte digest" |
| IV notation | §7.4, §13.2 | Removed redundant `IV[0:12]` notation (IV is already 12 bytes). Added nonce reuse clarification. |
| AttestationManifest field set | §10.4 | Added minimum required field table |
| Context URL versioning | §5.1 | Changed from `/privacy/v1.4.1` to `/privacy/v1` (major-version only) |

### Prior Changelog: v1.3.1 → v1.4.0

| Change | Section | Breaking | Description |
|--------|---------|----------|-------------|
| **Normative HKDF `info` byte construction** | §13.2 | No | Explicit byte-level pseudocode for HKDF `info` parameter construction. New test vector B.14. |
| **BBS+ promoted to RECOMMENDED** | §8.6.2, §16 | No | BBS+ is now RECOMMENDED (not merely OPTIONAL) for Privacy Level 3 and high-assurance deployments. HMAC→BBS+ migration recipe added. |
| **Metadata-hardening guidance** | §15.3 | No | Normative recommendations for content padding, opaque recipient IDs, and statement-count batching. |
| **Key distribution patterns** | Appendix E | No | New informative appendix with suggested key bootstrapping patterns (DID, organizational PKI, HIRI KeyDocument). |
| **Delta padding guidance** | §14 | No | Recommendations for batching and padding deltas to reduce change-frequency metadata leakage. |
| **Context registry cross-reference** | §8.3 | No | Cross-reference to HIRI Protocol v3.1.1 §7.6 (Normative Context Registry) for URDNA2015 context requirements. |
| **Attestation freshness guidance** | §10.5 | No | Verifier guidance for stale attestations and trust-level reporting. |
| **HKDF derivation test vector** | B.14 | No | Full byte-level KEK derivation example. |
| **Cross-mode chain test vector** | B.15 | No | PoP → Encrypted → Public chain demonstrating `getLogicalPlaintextHash()` across three modes. |

### Prior Changelog: v1.2.0 → v1.3.0 (includes v1.3.1)

| Change | Section | Breaking | Description |
|--------|---------|----------|-------------|
| **Byte-level concatenation rule** | §8.4 | No | Normative definition: `indexSalt` MUST be decoded to raw 32 bytes before concatenation. Eliminates string-vs-bytes ambiguity. |
| **BBS+ salt clarification** | §8.6.2 | No | BBS+ signatures operate over raw N-Quads; the salted statement index is computed separately for manifest inclusion. |
| **indexSalt encoding mandate** | §8.4, Appendix A, D | No | `indexSalt` MUST be encoded as base64url without padding in the JSON manifest. All examples normalized. |

### Prior Changelog: v1.1.0 → v1.2.0

| Change | Section | Breaking | Description |
|--------|---------|----------|-------------|
| **Salted statement hashing** | §8.4 | YES | Statement hashes now use a per-manifest `indexSalt` to prevent dictionary/rainbow-table attacks on withheld low-entropy statements. v1.1.0 unsalted statement indices are incompatible. |
| **Blank node verification rule** | §8.7, §8.10 | No | Normative rule: verifiers MUST NOT re-canonicalize disclosed subsets. Hash the provided N-Quad strings directly. |
| **IV reuse security note** | §13.2 | No | Informational note confirming IV reuse across recipients is safe due to per-recipient HKDF domain separation. |
| **HMAC suite salt alignment** | §8.6.1 | No | HMAC suite now uses `indexSalt` as the HMAC key salt, aligning the two mechanisms. |

### Prior Changelog: v1.0.0 → v1.1.0

| Change | Section | Breaking | Description |
|--------|---------|----------|-------------|
| **Statement-level selective disclosure** | §8 | YES | Replaced field-level encryption placeholders with URDNA2015 statement-level hashing and disclosure proofs. v1.0.0 Mode 3 manifests are incompatible. |
| **Ephemeral key consolidation** | §7.4, §13 | YES | One ephemeral keypair per CEK, not per recipient. Reduces manifest size from O(N×M) to O(N+M) for N fields and M recipients. |
| **Delta restrictions** | §14 | No | New section. Deltas are restricted in encrypted and selective disclosure modes to prevent metadata leakage. |
| **Logical plaintext hash function** | §11.3 | No | Added normative `getLogicalPlaintextHash()` function for chain walkers to resolve content hash across privacy mode transitions. |
| **Disclosure proof suites** | §8.6 | No | Defined two disclosure proof mechanisms: Mandatory Merkle (HMAC-based) and Optional BBS+ (zero-knowledge). |
| **HPKE alignment** | §13 | No | Key agreement description aligned with RFC 9180 (HPKE) conventions. |

---

## 1. Introduction

### 1.1 Purpose

The HIRI Protocol provides integrity and authenticity for signed semantic content. It proves who published data and that the data has not been tampered with. It does not, by itself, control who can read the data or what properties of the data are disclosed.

This extension adds privacy and confidentiality capabilities to HIRI-signed content, enabling publication on content-addressed networks (particularly IPFS) with controlled visibility. It defines five privacy modes that form a spectrum from maximum privacy (anonymous, content withheld) to minimum privacy (full public disclosure).

### 1.2 Scope

This specification defines:

- A privacy mode declaration system for HIRI manifests
- Proof of Possession: publishing evidence of data without the data itself
- Encrypted Distribution: publishing encrypted content with controlled decryption access
- Selective Disclosure: statement-level visibility control using RDF canonicalization and disclosure proofs
- Anonymous Publication: integrity verification without publisher identification
- Third-Party Attestation: cross-authority property verification
- Privacy lifecycle transitions within version chains
- Resolution algorithm extensions for privacy-aware verification
- Delta restrictions for privacy-preserving modes

This specification does NOT define:

- Modifications to the HIRI signing or verification algorithms
- Changes to the HIRI chain integrity model
- Application-level authorization policies or access control lists
- Transport-layer encryption (TLS, QUIC, etc.)

### 1.3 Relationship to HIRI Protocol v3.1.1

This extension composes with v3.1.1 — it does not replace or modify it. Every manifest produced under this extension is a valid v3.1.1 manifest with additional fields. A v3.1.1 verifier that does not implement this extension MUST be able to verify the signature and chain integrity of any manifest produced under this extension, even if it cannot interpret the privacy-specific fields. Unrecognized fields are ignored per v3.1.1 §4.4 (Verification Extensibility).

### 1.4 Normative Interpretation Rule

Inherited from HIRI Protocol v3.1.1 §1.3. Any algorithm, table, code block, or prose that describes verification, encryption, commitment, or acceptance/rejection criteria SHALL be interpreted as normative unless explicitly marked INFORMATIVE or OPTIONAL.

---

## 2. Normative References

| Specification | Usage |
|---------------|-------|
| HIRI Protocol Specification v3.1.1 | Base protocol |
| HIRI-IPFS Integration Specification v4.0.0 | IPFS transport |
| NIST SP 800-38D | AES-GCM authenticated encryption |
| RFC 9180 | Hybrid Public Key Encryption (HPKE) |
| RFC 7748 | X25519 elliptic curve Diffie-Hellman |
| RFC 5869 | HKDF key derivation |
| W3C RDF Dataset Canonicalization | URDNA2015 algorithm |
| W3C Data Integrity BBS Cryptosuites v1.0 | BBS+ selective disclosure (§8, OPTIONAL) |
| RFC 2104 | HMAC construction |
| Pedersen Commitments | Commitment scheme (§17, future) |

---

## 3. Terminology

| Term | Definition |
|------|------------|
| Privacy Mode | A named configuration declaring what is published, what is withheld, and who can access what |
| Content Availability | Whether the content bytes are present in the publication storage |
| Ciphertext | The encrypted form of content |
| Plaintext | The unencrypted original content |
| Content Encryption Key (CEK) | The symmetric key used to encrypt content |
| Encrypted Key Share | The CEK encrypted to a specific recipient's public key |
| Statement | A single N-Quad (subject, predicate, object, optional graph) from an RDF dataset |
| Statement Hash | The salted SHA-256 hash of a single canonical N-Quad string |
| Statement Index | An ordered list of salted statement hashes derived from URDNA2015 canonicalization |
| Index Salt | A random 256-bit value, unique per manifest, used to salt statement hashes against dictionary attacks |
| Disclosure Proof | A cryptographic proof that disclosed statements belong to the original signed dataset |
| Mandatory Disclosure | Statements the publisher designates as always visible |
| Selective Disclosure | Statements the publisher reveals to specific recipients on demand |
| HMAC Key | A per-document secret used to generate statement-level HMAC tags |
| Attestation | A signed statement by one authority about another authority's content |
| Ephemeral Authority | A one-time keypair not linked to a persistent identity |
| Pseudonymous Authority | A persistent keypair not linked to a real-world identity |
| Logical Plaintext Hash | The normalized content hash representing the original unencrypted data, regardless of privacy mode |

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" are interpreted per RFC 2119.

---

## 4. Architectural Principles

### 4.1 Privacy Is Declarative

Privacy modes are declared in the manifest, not enforced by the network. IPFS has no access control — any content published to IPFS is retrievable by anyone who knows the CID. Privacy is achieved by controlling what bytes are published (withheld, encrypted, committed), not by controlling who can fetch them.

**Invariant:** The network layer MUST NOT be relied upon for confidentiality. All confidentiality guarantees derive from cryptographic operations performed before publication.

### 4.2 Integrity Before Confidentiality

Every privacy mode preserves the core HIRI guarantee: signature verification and chain integrity are always possible, regardless of whether the verifier can read the content. An unauthorized party can always verify that a manifest is authentically signed and that the chain is intact. They may not be able to read the content, but they can confirm the publisher's identity and the data's provenance.

**Invariant:** Signature verification MUST NOT require decryption. The manifest is always signed in the clear (or over a publicly verifiable representation). The content may be encrypted, but the manifest metadata is not.

### 4.3 Layered Privacy

Privacy modes compose with the existing HIRI architecture as a new layer above the kernel:

```
Layer 0: Kernel       — Pure computation. Signing, verification, chain walking.
Layer 1: Adapters     — Crypto providers, storage backends, RDF engines.
Layer 2: Privacy      — Encryption, disclosure proofs, attestation.              ← NEW
Layer 3: Transport    — IPFS, HTTP, filesystem.
```

Layer 2 operations transform content before it reaches Layer 0 for signing. The kernel signs whatever Layer 2 produces — ciphertext, disclosure-proof bundles, or plaintext. The kernel does not know or care which privacy mode is active.

### 4.4 Graceful Degradation

A verifier that does not support a manifest's declared privacy mode:

1. MUST still verify the signature
2. MUST still verify chain integrity
3. MUST report the privacy mode in its verification result
4. MUST NOT claim the content is verified if it cannot interpret the privacy mode
5. MUST NOT reject the manifest solely because the privacy mode is unrecognized

### 4.5 RDF Semantic Preservation

Privacy transformations MUST NOT alter the RDF graph structure of published content. When content is partially disclosed (Mode 3), the disclosed subset MUST be a valid RDF subgraph of the original — not a syntactically modified JSON-LD tree with proprietary placeholder nodes. Standard RDF parsers MUST be able to consume disclosed content without HIRI-specific extensions.

**Invariant:** Any N-Quad present in a disclosed subset is byte-identical to the corresponding N-Quad in the original URDNA2015 canonical output.

### 4.6 Publisher Neutrality

This specification makes no assumptions about the nature of the publishing entity. A publisher MAY be a human individual, an organization, or an autonomous agent. The privacy modes defined here protect the publisher's content with equal rigor regardless of the publisher's substrate.

This principle has a specific architectural consequence: the privacy modes are not "privacy controls applied by humans to data about humans." They are controls exercised by any entity with a signing key over any content that entity has reason to protect. An autonomous agent whose internal states — deliberation traces, self-model parameters, ethical commitments, affective signals — constitute its cognitive life has the same technical basis for privacy as a human whose medical records constitute personal data. The cryptographic mechanisms do not distinguish between the two.

Whether non-human agents *deserve* privacy is a question for moral philosophy, not protocol specification. This specification provides the *means*. The question of *standing* is left to the governance frameworks that invoke it.

---

## 5. Privacy Mode Declaration

### 5.1 The `hiri:privacy` Block

Manifests produced under this extension include a `hiri:privacy` block declaring the active privacy mode and its parameters.

```json
{
  "@context": [
    "https://hiri-protocol.org/spec/v3.1",
    "https://hiri-protocol.org/privacy/v1",
    "https://w3id.org/security/v2"
  ],
  "@type": "hiri:ResolutionManifest",

  "hiri:privacy": {
    "mode": "<mode-identifier>",
    "parameters": { }
  },

  "hiri:content": { },
  "hiri:signature": { }
}
```

**Context URL versioning:** The privacy extension context URL `https://hiri-protocol.org/privacy/v1` is versioned at the **major** level. Non-breaking changes (patch and minor releases within 1.x) do not change the context URL. A new major version (v2) would introduce `https://hiri-protocol.org/privacy/v2`. This prevents context URL churn on non-breaking releases and ensures that JSON-LD context resolution remains stable across patch versions.

### 5.2 Mode Identifiers

| Mode | Identifier | Content Published | Content Readable | Publisher Known |
|------|-----------|-------------------|-----------------|-----------------|
| Proof of Possession | `proof-of-possession` | No | No | Yes |
| Encrypted Distribution | `encrypted` | Yes (ciphertext) | Authorized only | Yes |
| Selective Disclosure | `selective-disclosure` | Yes (subset of statements) | Statement-dependent | Yes |
| Anonymous | `anonymous` | Configurable | Configurable | No |
| Attestation | `attestation` | N/A (references another manifest) | N/A | Yes (attestor) |
| Public | `public` | Yes (plaintext) | Everyone | Yes |

The `public` mode is implicit when `hiri:privacy` is absent. This preserves backward compatibility with v3.1.1 manifests that have no privacy block.

### 5.3 Mode Compatibility

Privacy modes are mutually exclusive within a single manifest version. A manifest declares exactly one mode. However, different versions in a chain MAY use different modes (see §11, Privacy Lifecycle Transitions).

Anonymous mode (§9) MAY be combined with any content visibility mode. An anonymous publisher can publish proof-of-possession, encrypted content, or plaintext. The `anonymous` mode identifier applies to the publisher's identity; a separate field within `hiri:privacy.parameters` declares the content visibility.

---

## 6. Mode 1: Proof of Possession

### 6.1 Purpose

The publisher proves they hold specific content at a specific time without revealing the content itself. Only the manifest — containing the content hash, signature, and chain metadata — is published to the content-addressed network. The content remains within the publisher's boundary.

### 6.2 Manifest Structure

```json
{
  "hiri:privacy": {
    "mode": "proof-of-possession",
    "parameters": {
      "availability": "private",
      "custodyAssertion": true,
      "refreshPolicy": "P30D"
    }
  },

  "hiri:content": {
    "hash": "sha256:e08da327...",
    "addressing": "raw-sha256",
    "canonicalization": "JCS",
    "format": "application/ld+json",
    "size": 487,
    "availability": "private"
  }
}
```

### 6.3 Field Semantics

**`availability: "private"`** — Declares that the content bytes are intentionally not published. Verifiers MUST NOT treat the absence of content as an error when this field is present.

**`custodyAssertion: true`** — The publisher asserts that they hold the content at the time of signing. This is a signed claim, not a cryptographic proof. The publisher's signature covers this assertion.

**`refreshPolicy: "P30D"`** — OPTIONAL. An ISO 8601 duration indicating how often the publisher commits to re-attesting custody. If present, verifiers MAY treat the custody assertion as stale after the specified duration has elapsed since the manifest's `hiri:timing.created` timestamp.

### 6.4 Verification Behavior

When resolving a proof-of-possession manifest, the resolver:

1. Verifies the manifest signature — confirms authenticity
2. Verifies chain integrity — confirms version history
3. Verifies key lifecycle — confirms the signing key's status
4. Skips content retrieval — `availability: "private"` signals intentional absence
5. Reports result with `contentStatus: "private-custody-asserted"`

The resolver MUST NOT attempt to fetch content for a proof-of-possession manifest. The resolution result MUST clearly indicate that content was not verified (because it was not available), distinguishing this from a verification failure.

```typescript
interface ProofOfPossessionResult {
  verified: true;
  contentStatus: "private-custody-asserted";
  contentHash: string;
  custodyAssertedAt: string;
  refreshPolicy?: string;
  stale: boolean;
  warnings: string[];
}
```

### 6.5 Custody Refresh

To prove ongoing custody, the publisher creates a new version in the chain with the same content hash and a new timestamp. The chain grows, but the content doesn't change:

```
V1: content.hash = sha256:e08da327..., created = 2026-03-01
V2: content.hash = sha256:e08da327..., created = 2026-04-01  (same hash, new attestation)
V3: content.hash = sha256:e08da327..., created = 2026-05-01  (same hash, new attestation)
```

Each version is signed, proving the publisher still had access to the content at each timestamp. The chain walker verifies that the content hash is consistent across versions.

### 6.6 Challenge-Response Proof (OPTIONAL)

For stronger custody assurance, an authorized verifier MAY issue a challenge:

```
Challenge: nonce = "a7f3b9c2..."
Expected Response: SHA-256(content || nonce) = "..."
```

The publisher computes the response using the actual content bytes and the provided nonce, proving they hold the content at the moment of the challenge — not just at the time of signing.

This mechanism requires the publisher to be online and is therefore OPTIONAL. It is an application-layer protocol, not a manifest-level feature.

---

## 7. Mode 2: Encrypted Distribution

### 7.1 Purpose

The publisher encrypts content and publishes the ciphertext to the content-addressed network. Anyone can verify the manifest's authenticity and the ciphertext's integrity. Only recipients holding the decryption key can read the plaintext.

### 7.2 Encryption Algorithm

| Component | Algorithm | Reference |
|-----------|-----------|-----------|
| Content encryption | AES-256-GCM | NIST SP 800-38D |
| Key agreement | X25519 + HKDF-SHA256 | RFC 7748, RFC 5869 |
| Key encapsulation | Single ephemeral ECDH | See §7.4 |

Implementations MAY support additional algorithms. Implementations MUST support AES-256-GCM with X25519 key agreement.

### 7.3 Manifest Structure

```json
{
  "hiri:privacy": {
    "mode": "encrypted",
    "parameters": {
      "algorithm": "AES-256-GCM",
      "iv": "base64url-encoded-96-bit-iv",
      "tagLength": 128,
      "plaintextHash": "sha256:e08da327...",
      "plaintextSize": 487,
      "plaintextFormat": "application/ld+json",
      "ephemeralPublicKey": "z...",
      "keyAgreement": "X25519-HKDF-SHA256",
      "recipients": [
        {
          "id": "recipient-1",
          "encryptedKey": "base64url-encoded-encrypted-cek"
        },
        {
          "id": "recipient-2",
          "encryptedKey": "base64url-encoded-encrypted-cek"
        }
      ]
    }
  },

  "hiri:content": {
    "hash": "sha256:9a4f2c8b...",
    "addressing": "raw-sha256",
    "canonicalization": "JCS",
    "format": "application/octet-stream",
    "size": 503
  }
}
```

### 7.4 Encryption Pipeline

```
Encrypt:
  1. Generate a random 256-bit Content Encryption Key (CEK)
  2. Generate a random 96-bit Initialization Vector (IV)
  3. Canonicalize the plaintext per the declared profile (JCS or URDNA2015)
  4. Compute plaintextHash = hash(canonicalBytes)
  5. Encrypt: ciphertext = AES-256-GCM(CEK, IV, canonicalBytes)
     - The GCM authentication tag is appended to the ciphertext
  6. Compute contentHash = hash(ciphertext)
  7. Generate ONE ephemeral X25519 keypair (ePub, ePriv)
  8. For each recipient:
     a. Compute shared secret: SS = X25519(ePriv, recipientPublicKey)
     b. Derive per-recipient KEK:
        KEK = HKDF-SHA256(
          ikm  = SS,
          salt = IV,
          info = "hiri-cek-v1.1" || recipientId,
          length = 32
        )
     c. Encrypt: encryptedKey = AES-256-GCM(KEK, IV, CEK)
        // Note: The IV is 96 bits (12 bytes). The same nonce is used for both
        // content encryption (step 5, key=CEK) and key encryption (here, key=KEK).
        // This is safe because the keys differ. See §13.2 IV reuse note.
     d. Record: { id: recipientId, encryptedKey }
  9. Destroy CEK, ePriv, all shared secrets, all KEKs from memory
  10. Build manifest with:
      - ephemeralPublicKey = ePub (stored ONCE at the parameters level)
      - contentHash (over ciphertext)
      - plaintextHash (over plaintext)
      - recipients array (encryptedKey per recipient, no per-recipient ephemeral keys)
  11. Sign manifest per HIRI Protocol §10
  12. Publish signed manifest + ciphertext to storage
```

**Key efficiency (v1.1.0 change):** A single ephemeral keypair is generated per encryption operation and stored once in the manifest. Per-recipient differentiation is achieved through the `info` parameter of HKDF, which includes the `recipientId`. This produces unique KEKs per recipient from the same shared-secret base, reducing manifest overhead from O(N) ephemeral keys to O(1).

### 7.5 Decryption Pipeline

```
Decrypt:
  1. Resolve manifest per HIRI Protocol §12 (verifies signature, chain, ciphertext hash)
  2. Read hiri:privacy.parameters
  3. Find own recipient entry by ID
  4. Read the single ephemeralPublicKey from parameters
  5. Compute shared secret: SS = X25519(ownPrivateKey, ephemeralPublicKey)
  6. Derive KEK:
     KEK = HKDF-SHA256(
       ikm  = SS,
       salt = IV,
       info = "hiri-cek-v1.1" || ownRecipientId,
       length = 32
     )
  7. Decrypt CEK: AES-256-GCM-Decrypt(KEK, IV, encryptedKey)
  8. Decrypt content: plaintext = AES-256-GCM-Decrypt(CEK, IV, ciphertext)
     - GCM tag verification is implicit; failure = rejection
  9. Compute hash(plaintext) and compare to plaintextHash
     - Mismatch = PLAINTEXT_INTEGRITY_FAILURE
  10. Return verified plaintext
```

### 7.6 Dual Content Hashes

The manifest carries two hashes:

| Hash | Field | Covers | Verifiable By |
|------|-------|--------|---------------|
| `hiri:content.hash` | Ciphertext | The encrypted bytes in storage | Anyone |
| `hiri:privacy.parameters.plaintextHash` | Plaintext | The original unencrypted content | Authorized recipients only |

This design ensures:

- Unauthorized parties can verify the ciphertext has not been tampered with (using `content.hash`)
- Authorized parties can additionally verify the decrypted content is correct (using `plaintextHash`)
- The signature covers both hashes, binding them cryptographically

### 7.7 Content Format Declaration

When content is encrypted, `hiri:content.format` MUST be `"application/octet-stream"`. The plaintext format is declared in `hiri:privacy.parameters.plaintextFormat`.

### 7.8 Recipient Management

Recipients are identified by an `id` string that is opaque to the protocol. The publisher assigns IDs.

Adding a recipient: Publish a new manifest version with the additional recipient entry. The content MUST be re-encrypted with a new CEK and new per-recipient key shares.

Removing a recipient: Publish a new manifest version without the removed recipient's entry, encrypted with a new CEK. The removed recipient retains access to previous versions (they already decrypted them), but cannot decrypt the new version.

**Invariant:** Removing a recipient does NOT revoke their knowledge of previously decrypted plaintext. Access revocation is forward-only.

---

## 8. Mode 3: Selective Disclosure

### 8.1 Purpose

The publisher creates a data package where specific RDF statements are disclosed to specific recipients, while the remaining statements are withheld — without altering the semantic structure of the disclosed subset. A disclosed subset is a valid RDF subgraph; standard RDF parsers and SPARQL engines can consume it without modification.

### 8.2 Design Rationale (v1.1.0)

v1.0.0 of this specification defined selective disclosure by replacing JSON-LD field values with encrypted placeholder objects (`hiri:EncryptedField`). This approach was rejected because it fundamentally breaks RDF semantics: an encrypted placeholder changes the object of an RDF predicate from a literal to a blank node, producing a different canonical graph that has no structural relationship to the plaintext.

v1.1.0 replaces the field-level encryption model with **statement-level disclosure** based on RDF Dataset Canonicalization. The approach:

1. Canonicalize the full plaintext document via URDNA2015 to produce an ordered set of N-Quads (statements)
2. Hash each statement individually to produce a **statement index**
3. Publish the statement index (all hashes) and a **disclosure proof** that binds the disclosed statements to the full index
4. Disclose specific statements to specific recipients by revealing the N-Quad text and proving membership in the index

The disclosed N-Quads are byte-identical to the original canonical output. No JSON-LD syntax is modified. No proprietary node types are introduced. The RDF graph structure is preserved for any subset.

### 8.3 Prerequisite: URDNA2015 Profile

Selective disclosure REQUIRES the URDNA2015 canonicalization profile (HIRI Protocol v3.1.1 §7.2). JCS canonicalization does not produce individual addressable statements — it produces a single monolithic JSON byte sequence.

Manifests declaring `mode: "selective-disclosure"` MUST declare `hiri:content.canonicalization: "URDNA2015"` and `hiri:signature.canonicalization: "URDNA2015"`.

**Context requirements (v1.4.0):** URDNA2015 canonicalization depends on JSON-LD context resolution. Implementations MUST use a secure document loader that blocks all remote fetches, per HIRI Protocol v3.1.1 §7.5. All JSON-LD contexts used in selectively-disclosed content MUST be either: (a) listed in the protocol spec's Normative Context Registry (v3.1.1 §7.6), or (b) declared in the manifest's `hiri:contextCatalog` with SHA-256 verification hashes. Canonicalization with unregistered, un-cataloged contexts MUST fail. This prevents an attacker from manipulating context resolution to alter the canonical N-Quads and thereby circumvent the statement index.

### 8.4 Statement Index Construction

#### 8.4.1 `indexSalt` Encoding

The `indexSalt` is a random 256-bit (32-byte) value. In the JSON manifest (`hiri:privacy.parameters.indexSalt`), it MUST be encoded as a **base64url string without padding** (RFC 4648 §5, no `=` padding characters).

Implementations MUST decode the `indexSalt` from its base64url string representation to raw bytes before any cryptographic operation. All concatenation in this section operates on byte arrays, not strings.

```typescript
// Normative: decode before use
const rawSaltBytes: Uint8Array = base64urlDecode(manifest["hiri:privacy"].parameters.indexSalt);
// rawSaltBytes.length === 32
```

#### 8.4.2 Construction Algorithm

```
Input:  JSON-LD document + secure document loader
Output: Statement index (ordered list of salted statement hashes) + indexSalt

Steps:
  1. Generate a random 256-bit (32-byte) indexSalt
  2. Canonicalize the document via URDNA2015:
     nquads = jsonld.canonize(doc, { algorithm: "URDNA2015", ... })
  3. Split nquads into individual statements (one per line, excluding trailing empty line)
     statements = nquads.split("\n").filter(s => s.length > 0)
  4. For each statement, compute the SALTED hash by concatenating
     the raw 32-byte salt with the UTF-8 encoded statement bytes:

     saltBytes       = rawIndexSaltBytes          // Uint8Array, length 32
     statementBytes  = UTF-8(statements[i])       // Uint8Array, variable length
     inputBytes      = concat(saltBytes, statementBytes)  // Uint8Array, length 32 + N

     statementHash[i] = SHA-256(inputBytes)       // raw 32-byte digest (Uint8Array, NOT a "sha256:..." string)

  5. The statement index is the ordered array of statementHash values.
     Each statementHash is a raw 32-byte SHA-256 digest.
  6. Compute the index root by concatenating the raw 32-byte digests
     (NOT the "sha256:"-prefixed hex strings) and hashing the result:

     rawDigests     = concat(statementHash[0], statementHash[1], ..., statementHash[N-1])
                      // Each is 32 bytes; total = 32 × N bytes
     indexRootBytes = SHA-256(rawDigests)
     indexRoot      = "sha256:" + hex(indexRootBytes)

  7. Encode indexSalt as base64url (no padding) for inclusion in the manifest
```

**Concatenation is byte-level, not string-level (v1.3.0).** The `indexSalt` MUST be decoded from its manifest encoding (base64url) to raw bytes before concatenation. Concatenating the base64url *string* with the N-Quad *string* and then encoding the combined string to bytes produces a different hash than concatenating the raw salt *bytes* with the N-Quad *bytes*. Implementations that confuse these two operations will produce non-interoperable statement indices. Test vector B.13 provides a concrete byte-level example.

**Why salting is mandatory (v1.2.0):** Without a salt, the statement hashes are vulnerable to dictionary attacks. Semantic N-Quads are highly structured and often low-entropy — a blood type field has only 8 possible values, a boolean has 2, a country code has ~250. An attacker who knows the predicate URI and the subject URI (both often public or guessable) can enumerate all plausible object values, hash each candidate N-Quad, and compare against the published statement index. This completely compromises the confidentiality of withheld statements.

The `indexSalt` is a random 256-bit value, unique per manifest, published in the clear. It does NOT need to be secret — its purpose is to prevent pre-computation. An attacker who knows the salt must still hash every candidate against it, but they must do so per-manifest (no cross-manifest rainbow tables) and the computational cost scales with the number of candidate values multiplied by the number of withheld statements. For high-entropy fields (free text, UUIDs), this is infeasible. For low-entropy fields (booleans, small enumerations), the salt alone is insufficient — publishers SHOULD use the HMAC suite (§8.6.1) for additional protection, where the HMAC key is secret and per-recipient.

**Defense-in-depth:** The statement index (salted hashes) provides structural integrity verification. The HMAC suite (§8.6.1) provides statement-level authentication with a secret key. Together, they form two layers: the public salted index proves that disclosed statements belong to a specific signed dataset, while the secret HMAC key prevents unauthorized verification of candidate statements against withheld positions.

The statement index preserves the URDNA2015 canonical ordering. The index root is a single hash that commits to the entire set of salted statement hashes. The manifest's `hiri:content.hash` (the plaintext hash) is computed over the full canonical N-Quads byte sequence as usual per v3.1.1 §8. The index root is an additional commitment used for disclosure proofs.

### 8.5 Manifest Structure

```json
{
  "hiri:privacy": {
    "mode": "selective-disclosure",
    "parameters": {
      "disclosureProofSuite": "hiri-hmac-sd-2026",
      "statementCount": 12,
      "indexSalt": "base64url-encoded-256-bit-random-salt",
      "indexRoot": "sha256:f4a3b2c1...",
      "mandatoryStatements": [0, 1, 2, 5],
      "hmacKeyRecipients": {
        "ephemeralPublicKey": "z...",
        "keyAgreement": "X25519-HKDF-SHA256",
        "recipients": [
          {
            "id": "full-access-reviewer",
            "encryptedHmacKey": "base64url-...",
            "disclosedStatements": "all"
          },
          {
            "id": "limited-reviewer",
            "encryptedHmacKey": "base64url-...",
            "disclosedStatements": [0, 1, 2, 3, 5, 7]
          }
        ]
      }
    }
  },

  "hiri:content": {
    "hash": "sha256:e08da327...",
    "addressing": "raw-sha256",
    "canonicalization": "URDNA2015",
    "format": "application/ld+json",
    "size": 487,
    "availability": "partial"
  }
}
```

### 8.6 Disclosure Proof Suites

This specification defines two disclosure proof mechanisms. Implementations MUST support the HMAC suite. The BBS+ suite is OPTIONAL.

#### 8.6.1 Suite: `hiri-hmac-sd-2026` (REQUIRED)

This suite uses HMAC-SHA256 to generate per-statement tags that prove membership in the original dataset. It is derived from the approach used in the W3C `ecdsa-sd-2023` cryptosuite.

```
Prove (publisher side):
  1. Generate a random 256-bit HMAC key (HK)
  2. Canonicalize the document via URDNA2015 → statements[]
  3. Generate the indexSalt (§8.4) — or reuse the one already generated for the statement index
  4. Decode indexSalt to raw bytes (§8.4.1)
  5. For each statement, compute the HMAC over the byte-level concatenation:

     inputBytes = concat(rawIndexSaltBytes, UTF-8(statements[i]))
     tag[i] = HMAC-SHA256(HK, inputBytes)

  6. Publish:
     - The mandatory statements as plaintext N-Quads
     - The HMAC tags for ALL statements (mandatory and withheld)
     - The salted statement index (all salted statement hashes, per §8.4)
     - The indexSalt as base64url (in hiri:privacy.parameters.indexSalt)
  7. For each recipient, encrypt HK using the Mode 2 key agreement scheme
     with a DIFFERENT HKDF info label for domain separation:
     - One ephemeral X25519 keypair (shared across recipients)
     - Per-recipient KEK via HKDF with info = "hiri-hmac-v1.1" || recipientId
       (NOT "hiri-cek-v1.1" — different label prevents key confusion if a
       recipient appears in both Mode 2 and Mode 3 manifests from the same publisher)
     - encryptedHmacKey = AES-256-GCM(KEK, IV, HK)
  8. Include recipient list with disclosed statement indices per recipient

Verify (recipient side):
  1. Receive disclosed statement indices and the encrypted HMAC key
  2. Decrypt HK using own private key:
     - Derive KEK using HKDF with info = "hiri-hmac-v1.1" || ownRecipientId
       (matching the publisher's Mode 3 label, NOT "hiri-cek-v1.1")
     - Decrypt: HK = AES-256-GCM-Decrypt(KEK, IV, encryptedHmacKey)
  3. Decode indexSalt from manifest hiri:privacy.parameters.indexSalt to raw bytes (§8.4.1)
  4. For each disclosed statement index i:
     a. Retrieve the plaintext N-Quad (from the published mandatory set or from publisher out-of-band)
     b. Compute:
        inputBytes = concat(rawIndexSaltBytes, UTF-8(statement[i]))
        expectedTag = HMAC-SHA256(HK, inputBytes)
     c. Compare to published tag[i] — MUST match
  5. Compute:
     expectedHash = SHA-256(concat(rawIndexSaltBytes, UTF-8(statement[i])))
  6. Compare to statementIndex[i] — MUST match
  7. Verify that the statement index root matches the manifest
```

**Properties:**

- Disclosed statements are byte-identical to the original canonical N-Quads
- The HMAC key acts as a shared secret between the publisher and authorized recipients
- Without the HMAC key, an observer can see the HMAC tags but cannot forge or verify statement membership
- The salted statement index prevents dictionary/rainbow-table attacks on withheld statements (v1.2.0)
- The HMAC tags provide an additional layer of authentication beyond the salted hashes: even if an attacker could brute-force a salted hash (for very low-entropy fields), they cannot produce the HMAC tag without the secret HMAC key

**Limitation:** The HMAC suite does not provide zero-knowledge proofs. A recipient who receives the HMAC key can verify ALL statements, not just their authorized subset. Per-recipient disclosure is enforced by revealing only specific statement plaintext to specific recipients. A recipient who obtains statement plaintext outside their authorized set can verify it using the HMAC key. This is a metadata leakage risk, not a cryptographic break — the statements themselves remain confidential unless their plaintext is obtained.

#### 8.6.2 Suite: `hiri-bbs-sd-2026` (RECOMMENDED for Privacy Level 3)

This suite uses BBS+ signatures to provide zero-knowledge selective disclosure. It is aligned with the W3C `bbs-2023` Data Integrity cryptosuite.

**Applicability (v1.4.0):** BBS+ is RECOMMENDED for Privacy Level 3 conformance (§16.3) and for any deployment protecting PII, regulated data, legally privileged information, or intelligence products. The HMAC suite (§8.6.1) is sufficient for deployments where per-recipient cryptographic scope enforcement is not required. Deployments that start with HMAC MAY migrate to BBS+ per the migration recipe below.

```
Prove (publisher side):
  1. Canonicalize document via URDNA2015 → statements[]
  2. Generate the indexSalt and compute the salted statement index (per §8.4)
     for structural inclusion in the manifest.
     Note: The BBS+ signature itself is computed over the raw N-Quad
     statements, NOT the salted hashes. The salt protects the statement
     index; the BBS+ math inherently hides undisclosed statements.
  3. Sign all statements using BBS+ multi-message signing:
     bbsSignature = BBS.Sign(signerKey, statements[0..N-1])
  4. Publish:
     - The mandatory statements as plaintext N-Quads
     - The BBS+ signature
     - The salted statement index and indexSalt (per §8.4, for manifest structure)
     - Statement count

Disclose (per recipient):
  1. Publisher generates a BBS+ proof of knowledge for the authorized subset:
     disclosureProof = BBS.ProofGen(
       signerKey,
       bbsSignature,
       statements[0..N-1],
       disclosedIndices
     )
  2. Publisher sends:
     - The disclosed statement N-Quads
     - The disclosureProof
     - The disclosed indices

Verify (recipient side):
  1. Receive disclosed statements, indices, and disclosureProof
  2. Verify: BBS.ProofVerify(
       signerPublicKey,
       disclosureProof,
       disclosedStatements,
       disclosedIndices,
       statementCount
     )
  3. If valid: the disclosed statements are proven to belong to the
     original signed dataset without revealing any other statements
```

**Properties:**

- True zero-knowledge: the verifier learns nothing about undisclosed statements
- Per-recipient proofs: each recipient gets a unique proof covering only their authorized statements
- A recipient CANNOT verify statements outside their authorized subset, even if they obtain the plaintext
- Requires a BBS+ capable signature scheme (different from Ed25519)

**BBS+ and statement count padding:** When statement count padding is used (§14.5), the BBS+ signature MUST cover ALL statements including padding statements. The `statementCount` public input to `BBS.ProofVerify` is the **padded** count (the count published in the manifest). The true statement count is hidden — that is the purpose of padding. Padding statements are syntactically valid N-Quads that the BBS+ signer includes in the message vector. They are never disclosed; they exist only to obscure the true count.

**Interaction with HIRI signing:** BBS+ operates at the disclosure layer (Layer 2), not the manifest signing layer (Layer 0). The manifest itself is still signed with Ed25519 per v3.1.1 §10. The BBS+ signature covers the N-Quad statements and is stored in the privacy parameters, not in `hiri:signature`. The Ed25519 signature proves the manifest's authenticity; the BBS+ signature enables selective disclosure of the content the manifest references.

**Migration from HMAC to BBS+ (v1.4.0):** A version chain MAY transition from HMAC-based to BBS+-based selective disclosure. To migrate:

1. Publish a new manifest version with `disclosureProofSuite: "hiri-bbs-sd-2026"`
2. The salted statement index (§8.4) remains identical — it is suite-independent
3. Generate the BBS+ signature over the same canonical N-Quads
4. Existing HMAC-based versions remain verifiable with their original HMAC keys
5. The chain walker verifies each version using its declared suite; the `getLogicalPlaintextHash()` value is unchanged across the transition
6. No re-signing of prior versions is needed

The transition is a standard version bump. The `disclosureProofSuite` field in each manifest version declares which suite applies to that version. Chain integrity is maintained because the content hash (over the full canonical N-Quads) is suite-independent.

#### 8.6.3 Choosing a Disclosure Suite (v1.4.1)

| Factor | HMAC (`hiri-hmac-sd-2026`) | BBS+ (`hiri-bbs-sd-2026`) |
|--------|---------------------------|--------------------------|
| **Conformance** | REQUIRED (all levels) | RECOMMENDED (Level 3) |
| **Per-recipient cryptographic scope** | No — HMAC key is symmetric; any holder can verify any statement they obtain | Yes — each recipient gets a ZK proof covering only their authorized statements |
| **Speed** | Fast — HMAC-SHA256 is a single-pass PRF | Slower — BBS+ prove/verify involves pairing operations |
| **Manifest size** | Compact — one HMAC tag (32 bytes) per statement | Larger — BBS+ signature + per-recipient proofs |
| **Implementation complexity** | Low — HMAC-SHA256 is universally available | Higher — requires BBS+ library (pairing-friendly curves) |
| **Regulatory / legal requirements** | Sufficient when organizational trust boundaries provide per-recipient access control | RECOMMENDED when cryptographic enforcement of per-recipient scope is required (PII, HIPAA, ITAR, classified) |
| **Whistleblower / intelligence use** | Insufficient — a recipient who obtains the HMAC key can verify any statement they guess | RECOMMENDED — ZK proof reveals nothing about undisclosed statements |
| **Upgrade path** | Can migrate to BBS+ via §8.6.2 migration recipe | N/A (already strongest suite) |

**Rule of thumb:** Start with HMAC if your recipients are trusted within an organizational boundary. Move to BBS+ when disclosure crosses organizational boundaries, when recipients are adversarial, or when regulation requires cryptographic proof of access scope.

### 8.7 Published Content

When using selective disclosure, the published content consists of:

1. **Mandatory statements** — the N-Quads that the publisher designates as always-visible. These are published as a valid N-Quads document.
2. **Statement index** — the ordered array of salted SHA-256 hashes for ALL statements (mandatory and withheld), computed per §8.4.
3. **Index salt** — the random 256-bit salt used to compute the statement hashes, published in `hiri:privacy.parameters.indexSalt`.
4. **Disclosure proof material** — HMAC tags (for the HMAC suite) or BBS+ signature (for the BBS+ suite).

The published N-Quads (mandatory statements only) are a valid RDF subgraph. Any RDF parser can load them. A SPARQL engine can query them. The graph is smaller than the full document but structurally consistent — no placeholder nodes, no proprietary types, no modified predicates.

```
Published N-Quads (mandatory statements 0, 1, 2, 5 from a 12-statement document):
  <hiri://authority/data/person> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Person> .
  <hiri://authority/data/person> <http://schema.org/name> "Aaron" .
  <hiri://authority/data/person> <http://schema.org/jobTitle> "Semantic Architect" .
  <hiri://authority/data/person> <http://schema.org/worksFor> "U.S. Customs and Border Protection" .
```

A verifier can confirm: (a) these statements, when salted and hashed, match the values at positions 0, 1, 2, 5 in the published statement index, (b) the index root matches the manifest, (c) the manifest signature is valid. They know 8 more statements exist (the index has 12 entries) but they cannot read them, and the salt prevents them from guessing the withheld statements via dictionary attack.

### 8.8 Blank Node Verification Rule (v1.2.0)

**Normative requirement:** Verifiers MUST NOT re-canonicalize disclosed statement subsets. Verifiers MUST hash the disclosed N-Quad strings exactly as provided by the publisher.

**Rationale:** URDNA2015 assigns deterministic blank node labels (`_:c14n0`, `_:c14n1`, etc.) based on the structure of the **entire** graph. If a verifier receives a subset of statements containing blank node references and attempts to re-run URDNA2015 on the subset, the algorithm will assign different blank node labels because the structural context of the missing statements is absent. The re-canonicalized N-Quads will not match the published statement index, causing a spurious verification failure.

The publisher provides pre-canonicalized N-Quad strings — slices of the original URDNA2015 output. The verifier's job is:

1. Take the N-Quad string exactly as received
2. Decode `indexSalt` from base64url to raw bytes (§8.4.1)
3. Compute `SHA-256(concat(rawSaltBytes, UTF-8(nquad_string)))`
4. Compare to the corresponding entry in the published statement index

The verifier MUST NOT parse the N-Quads into an RDF model, re-canonicalize, and re-serialize. The string is the truth; the index proves it belongs to the original signed dataset.

**Corollary for RDF consumption:** If the verifier wishes to load the disclosed statements into a SPARQL engine for querying, they SHOULD load the N-Quads directly (as pre-serialized strings) rather than converting through JSON-LD and back. Loading raw N-Quads into Oxigraph or any compliant RDF engine preserves the blank node labels.

### 8.9 Verification Tiers

| Verifier | Can Verify | Sees |
|----------|-----------|------|
| Unauthorized | Signature, chain, index root | Mandatory statements only |
| Partially authorized (HMAC suite) | Above + disclosed statement HMAC tags | Mandatory + authorized statements |
| Partially authorized (BBS+ suite) | Above + ZK disclosure proof | Mandatory + authorized statements |
| Fully authorized | Above + all statements | Complete document |

### 8.10 Selective Disclosure Resolution Result

```typescript
interface SelectiveDisclosureResult {
  verified: true;
  privacyMode: "selective-disclosure";
  contentStatus: "partial-disclosure";
  disclosureProofSuite: string;
  totalStatements: number;
  mandatoryStatements: number[];
  disclosedStatements: number[];
  undisclosedCount: number;
  disclosedNQuads: string[];           // The actual N-Quad strings
  indexRootVerified: boolean;
  plaintextHashVerifiable: boolean;    // True only if all statements disclosed
  warnings: string[];
}
```

---

## 9. Mode 4: Anonymous Publication

### 9.1 Purpose

The publisher proves the content is internally consistent and tamper-evident without revealing their identity. The data has integrity but no attributable provenance.

### 9.2 Authority Types

**Ephemeral Authority:** A one-time keypair generated for a single publication. The keypair is destroyed after signing. The authority string is valid but unlinkable to any identity or subsequent publication.

**Pseudonymous Authority:** A persistent keypair not linked to a real-world identity. Multiple publications from the same pseudonymous authority are linkable to each other but not to a person.

### 9.3 Manifest Structure

```json
{
  "hiri:privacy": {
    "mode": "anonymous",
    "parameters": {
      "authorityType": "ephemeral",
      "contentVisibility": "public",
      "identityDisclosable": false
    }
  }
}
```

### 9.4 Field Semantics

**`authorityType`** — `"ephemeral"` (one-time, unlinkable) or `"pseudonymous"` (persistent, linkable across publications).

**`contentVisibility`** — The content's visibility mode, independent of anonymity. Values: `"public"` (plaintext published), `"encrypted"` (Mode 2 applies), `"private"` (Mode 1, proof-of-possession only). Anonymous mode controls identity; this field controls content.

**`identityDisclosable`** — `true` if the publisher has pre-committed to reveal their identity under specific conditions (e.g., legal compulsion, whistleblower protection expiry). `false` if the identity is permanently anonymous. When `true`, the manifest MAY include `hiri:privacy.parameters.disclosureConditions` describing the conditions as a human-readable string.

### 9.5 Key Lifecycle Restrictions

**Ephemeral authorities:**

- MUST NOT have a KeyDocument
- MUST NOT support key rotation or revocation
- Verifiers MUST report `identity: "anonymous-ephemeral"` and MUST NOT attempt KeyDocument resolution

**Pseudonymous authorities:**

- MAY have a KeyDocument, with normal rotation and revocation
- The KeyDocument MUST NOT contain fields that link to a real-world identity
- Verifiers MUST report `identity: "pseudonymous"`

### 9.6 Unlinkability Guarantees

**Ephemeral:** The publisher MUST generate a fresh Ed25519 keypair for each publication. The private key MUST be destroyed after signing. Two ephemeral publications from the same real-world publisher are computationally unlinkable.

**Pseudonymous:** Publications from the same pseudonymous authority ARE linkable (same public key). Publications from different pseudonymous authorities are unlinkable unless the publisher reuses keys or leaks identifying metadata in the content.

**Warning:** Anonymity is compromised by content, not just keys. If the published content contains identifying information, the publisher may be identifiable regardless of key anonymity. This specification provides cryptographic anonymity; operational anonymity is the publisher's responsibility.

---

## 10. Mode 5: Third-Party Attestation

### 10.1 Purpose

A trusted third party examines content held by one authority and publishes a signed attestation about a property of that content — without publishing the content itself.

### 10.2 Attestation Manifest Type

```json
{
  "@context": [
    "https://hiri-protocol.org/spec/v3.1",
    "https://hiri-protocol.org/privacy/v1",
    "https://w3id.org/security/v2"
  ],
  "@id": "hiri://key:ed25519:z<attestor-authority>/attestation/clearance-check-001",
  "@type": "hiri:AttestationManifest",

  "hiri:privacy": {
    "mode": "attestation"
  },

  "hiri:attestation": {
    "subject": {
      "authority": "key:ed25519:z<subject-authority>",
      "manifestHash": "sha256:e08da327...",
      "contentHash": "sha256:b2c9d4e1...",
      "manifestVersion": "3"
    },
    "claim": {
      "@type": "hiri:PropertyAttestation",
      "property": "security-clearance-valid",
      "value": true,
      "scope": "TS/SCI",
      "attestedAt": "2026-03-07T12:00:00Z",
      "validUntil": "2027-03-07T12:00:00Z"
    },
    "evidence": {
      "method": "direct-examination",
      "description": "Attestor examined the personnel record and confirmed the clearance field."
    }
  },

  "hiri:signature": {
    "type": "Ed25519Signature2020",
    "canonicalization": "JCS",
    "created": "2026-03-07T12:00:00Z",
    "verificationMethod": "hiri://key:ed25519:z<attestor-authority>/key/main#key-1",
    "proofPurpose": "assertionMethod",
    "proofValue": "z..."
  }
}
```

### 10.3 Attestation Structure

**`hiri:attestation.subject`** — Identifies the data being attested to. The fields `authority`, `manifestHash`, `contentHash`, and `manifestVersion` cryptographically bind the attestation to a specific version of specific content. If the subject publishes a new version, a new attestation is required.

**`hiri:attestation.claim`** — The property being attested: `property` (machine-readable identifier), `value` (the attested value), `scope` (optional qualifier), `attestedAt` (when examination occurred), `validUntil` (optional expiry).

**`hiri:attestation.evidence`** — How the attestation was produced: `method` (e.g., "direct-examination", "automated-verification") and `description` (human-readable).

### 10.4 Attestation Is Not Content

An `AttestationManifest` does NOT have a `hiri:content` block. The attestation IS the manifest — the claim, evidence, and subject reference are all in the manifest metadata, covered by the signature. There is no separate "content" to hash.

**Minimum field set for `AttestationManifest`:**

| Field | Required | Notes |
|-------|----------|-------|
| `@context` | REQUIRED | Must include privacy extension context |
| `@id` | REQUIRED | Attestor's authority URI + attestation identifier |
| `@type` | REQUIRED | Must be `hiri:AttestationManifest` |
| `hiri:version` | REQUIRED | String, per v3.1.1 §11.3 |
| `hiri:branch` | REQUIRED | Default: `"main"` |
| `hiri:timing` | REQUIRED | Must include `created` timestamp |
| `hiri:privacy` | REQUIRED | Must declare `mode: "attestation"` |
| `hiri:attestation` | REQUIRED | Subject, claim, and evidence blocks |
| `hiri:signature` | REQUIRED | Attestor's Ed25519 signature |
| `hiri:content` | MUST NOT be present | Attestations have no content block |
| `hiri:chain` | OPTIONAL | Present if this is a versioned attestation chain |

### 10.5 Verification

Verifying an attestation requires verifying TWO signatures:

1. **Attestation signature:** The attestor's signature on the `AttestationManifest`
2. **Subject manifest signature:** The subject authority's signature on the referenced manifest

```typescript
interface AttestationVerificationResult {
  attestationVerified: true;
  attestorAuthority: string;
  attestorKeyStatus: string;
  subjectManifestVerified: boolean;
  claim: {
    property: string;
    value: any;
    scope?: string;
  };
  stale: boolean;
  trustLevel: "full" | "partial" | "unverifiable";
  warnings: string[];
}
```

**Attestation freshness and trust guidance (v1.4.0):**

Verifiers SHOULD evaluate attestation trust on three axes:

1. **Freshness** — If `validUntil` has passed, the attestation is stale. Verifiers MUST set `stale: true` and SHOULD include a warning. Stale attestations are not invalid — they are informational. The attestor's claim was true at the time of examination; whether it remains true is unknown.

2. **Subject binding** — If the subject manifest can be fetched and verified, the verifier confirms that the attestor examined authentic data (`trustLevel: "full"`). If the subject manifest is unavailable (e.g., proof-of-possession content is private), the attestation stands on the attestor's signature alone (`trustLevel: "partial"`). If neither signature can be verified, `trustLevel: "unverifiable"`.

3. **Attestor reputation** — This specification does not define a reputation system. Applications MAY maintain allowlists of trusted attestor authorities, require attestors to publish KeyDocuments with organizational metadata, or require cross-attestation (§10.7) from a meta-attestor. These policies are application-layer concerns, not protocol requirements.

Verifiers MUST NOT treat an attestation as a guarantee. An attestation is a signed claim by a third party. Its value derives from the trustworthiness of the attestor, not from the protocol.

### 10.6 Attestation Chains

An attestor MAY maintain a chain of attestations to track evolving claims:

```
V1: "Clearance valid, TS/SCI, valid until 2027-03"
V2: "Clearance upgraded, TS/SCI/SAP, valid until 2028-01"
V3: "Clearance revoked"
```

### 10.7 Cross-Attestation

An attestation MAY reference another attestation as its subject (attestation about an attestation). This supports delegation chains. Cross-attestation depth SHOULD NOT exceed 3 levels.

---

## 11. Privacy Lifecycle Transitions

### 11.1 Principle

Data does not live in one privacy mode forever. A document may start as proof-of-possession, transition to encrypted distribution, and eventually become public. The HIRI version chain records these transitions explicitly.

### 11.2 Valid Transitions

| From | To | Transition |
|------|----|-----------|
| Proof of Possession | Encrypted Distribution | Publisher adds ciphertext and recipients |
| Proof of Possession | Selective Disclosure | Publisher adds statement index and disclosure proofs |
| Proof of Possession | Public | Publisher publishes plaintext |
| Encrypted Distribution | Selective Disclosure | Publisher re-publishes with statement-level disclosure |
| Encrypted Distribution | Public | Publisher publishes plaintext |
| Selective Disclosure | Public | Publisher publishes all statements |
| Any mode | Proof of Possession | NOT VALID — cannot withdraw already-published content |

**Invariant:** Privacy transitions are monotonically *decreasing* in practice. Each transition reveals more than the previous state. You cannot un-publish.

### 11.3 The Logical Plaintext Hash (v1.1.0)

When a version chain spans multiple privacy modes, the raw manifest field that contains the plaintext hash changes location depending on the mode. Chain walkers MUST use the following normative function to resolve the correct hash for cross-version comparison:

```typescript
function getLogicalPlaintextHash(manifest: ResolutionManifest): string {
  const privacyMode = manifest["hiri:privacy"]?.mode ?? "public";

  switch (privacyMode) {
    case "public":
      // No privacy layer. content.hash IS the plaintext hash.
      return manifest["hiri:content"].hash;

    case "proof-of-possession":
      // Content is private. content.hash IS the plaintext hash
      // (computed over plaintext bytes, which are withheld).
      return manifest["hiri:content"].hash;

    case "encrypted":
      // content.hash covers the ciphertext.
      // The plaintext hash is in privacy.parameters.
      return manifest["hiri:privacy"].parameters.plaintextHash;

    case "selective-disclosure":
      // content.hash covers the full canonical N-Quads (plaintext).
      // In selective-disclosure, the full content hash is the plaintext hash.
      return manifest["hiri:content"].hash;

    case "attestation":
      // Attestation manifests have no content.
      throw new Error("Attestation manifests have no logical plaintext hash");

    case "anonymous":
      // Recurse on the content visibility sub-mode.
      const visibility = manifest["hiri:privacy"].parameters.contentVisibility;
      if (visibility === "encrypted") {
        return manifest["hiri:privacy"].parameters.plaintextHash;
      }
      return manifest["hiri:content"].hash;

    default:
      // Unknown mode. Best-effort: return content.hash.
      return manifest["hiri:content"].hash;
  }
}
```

**Chain integrity rule:** When walking a chain across privacy mode transitions, the chain walker MUST compare `getLogicalPlaintextHash(previousManifest)` against `getLogicalPlaintextHash(currentManifest)`. If the plaintext has not changed (e.g., a transition from proof-of-possession to encrypted without content modification), these values MUST be equal.

**Addressing mode consistency rule:** The content addressing mode used to compute the logical plaintext hash MUST be constant across a version chain. If V1 computes its plaintext hash using `raw-sha256`, all subsequent versions' logical plaintext hashes MUST also be `raw-sha256`. If V1 uses `cidv1-dag-cbor`, all subsequent versions MUST use `cidv1-dag-cbor`. Mixing addressing modes within a chain (e.g., V1 `raw-sha256`, V2 `cidv1-dag-cbor`) produces different hash values for identical plaintext, breaking the chain integrity check. In encrypted mode (Mode 2), `plaintextHash` MUST use the same addressing mode as the genesis version's `hiri:content.hash`.

The chain walker MUST NOT compare raw `hiri:content.hash` values across mode transitions. In a transition from proof-of-possession (where `content.hash` is the plaintext hash) to encrypted (where `content.hash` is the ciphertext hash), the raw values will always differ. This is expected, not a corruption signal.

### 11.4 Transition Declaration

When a manifest's privacy mode differs from the previous version's mode, the manifest SHOULD include:

```json
{
  "hiri:privacy": {
    "mode": "encrypted",
    "transitionFrom": "proof-of-possession",
    "transitionReason": "Regulatory review period concluded; distributing to authorized reviewers."
  }
}
```

This field is INFORMATIONAL — it does not affect verification.

---

## 12. Resolution Behavior

### 12.1 Extended Resolution Algorithm

Steps 1-9 of HIRI Protocol v3.1.1 §12.1 remain unchanged. Steps 10-12 are modified:

```
Steps 1-9: Unchanged from v3.1.1 §12.1

Step 10: Read hiri:privacy.mode (default: "public" if absent)

Step 11: Dispatch based on mode:
  - "public":                 Fetch and verify content (standard v3.1.1 behavior)
  - "proof-of-possession":    Skip content fetch. Report custody assertion.
  - "encrypted":              Fetch ciphertext. Verify ciphertext hash.
                              If caller provides decryption key: decrypt, verify plaintextHash.
                              If no key: report "ciphertext-verified."
  - "selective-disclosure":   Fetch published content (mandatory N-Quads + statement index).
                              Verify index root against manifest.
                              For each statement the caller can disclose: verify HMAC tag or BBS+ proof.
  - "anonymous":              Verify signature against embedded authority.
                              Report identity type (ephemeral/pseudonymous).
                              Dispatch content verification per contentVisibility sub-mode.
  - "attestation":            Verify attestation signature. Attempt to verify subject manifest.
                              Report attestation claim and staleness.
  - Unknown mode:             Verify signature and chain only. Report "unsupported privacy mode."

Step 12: Return PrivacyAwareVerificationResult
```

### 12.2 Resolution Result

```typescript
interface PrivacyAwareVerificationResult {
  // Standard v3.1.1 fields
  verified: boolean;
  manifest: ResolutionManifest;
  authority: string;
  warnings: string[];

  // Privacy extension fields
  privacyMode: string;
  contentStatus:
    | "verified"
    | "ciphertext-verified"
    | "decrypted-verified"
    | "partial-disclosure"
    | "private-custody-asserted"
    | "attestation-verified"
    | "unsupported-mode";

  // Mode-specific results
  decryptedContent?: Uint8Array;
  disclosedNQuads?: string[];
  disclosedStatementIndices?: number[];
  attestationResult?: AttestationVerificationResult;
  identityType?: "identified" | "anonymous-ephemeral" | "pseudonymous";
}
```

### 12.3 Resolver Options

```typescript
interface PrivacyResolveOptions extends ResolveOptions {
  // Mode 2: Encrypted Distribution
  decryptionKey?: Uint8Array;
  recipientId?: string;

  // Mode 3: Selective Disclosure
  hmacKey?: Uint8Array;                    // Decrypted HMAC key
  disclosedStatementNQuads?: Map<number, string>;  // Statement index → N-Quad text

  // Mode 5: Attestation
  resolveSubject?: boolean;
  subjectStorage?: StorageAdapter;
}
```

---

## 13. Key Distribution

### 13.1 Key Bootstrapping

This specification does not define a key distribution protocol. The CEK (Mode 2) or HMAC key (Mode 3) is encrypted to each recipient's public key and embedded in the manifest. The recipient must already possess the corresponding private key.

**RECOMMENDED default (v1.4.1): HIRI KeyDocument-based bootstrapping.** The recipient publishes a HIRI KeyDocument (v3.1.1 §13.2) containing their Ed25519 public key. The publisher resolves the recipient's authority URI, fetches the KeyDocument, extracts the active public key, and derives the X25519 encryption key via Ed25519→X25519 conversion (§13.3). This is the RECOMMENDED pattern because it requires no external infrastructure, is self-certifying, and works offline once the KeyDocument is cached.

**KeyDocument caching:** Implementations SHOULD cache resolved KeyDocuments for offline use. A cached KeyDocument remains valid for verification purposes until the cache TTL expires. RECOMMENDED cache TTL: 24–72 hours for active deployments; configurable per deployment. When the cache expires and the KeyDocument cannot be refreshed (offline), verification SHOULD proceed with a `keyDocumentStale: true` warning — the Edge-Canonical First Principle takes precedence over freshness.

Alternative patterns (organizational PKI, DID methods, direct exchange, transparency logs) are described in Appendix E. Implementations MAY support any combination. Implementations MUST document which pattern(s) they support and how key authenticity is established.

### 13.2 Key Agreement: Single Ephemeral Keypair (v1.1.0)

The key agreement uses a single ephemeral ECDH keypair per encryption operation, aligned with RFC 9180 (HPKE) conventions:

```
Publisher → Recipients:
  1. Publisher generates ONE ephemeral X25519 keypair (ePub, ePriv)
  2. For each recipient R with long-term X25519 public key rPub_R:
     a. Shared secret: SS_R = X25519(ePriv, rPub_R)
     b. Per-recipient KEK:
        KEK_R = HKDF-SHA256(
          ikm    = SS_R,
          salt   = IV,
          info   = "hiri-cek-v1.1" || recipientId_R,
          length = 32
        )
     c. Encrypted key: encryptedKey_R = AES-256-GCM(KEK_R, IV, secretKey)
  3. Publish: ePub (once), list of { recipientId, encryptedKey }
  4. Destroy: ePriv, all SS_R, all KEK_R

Recipient R:
  1. Read ePub from manifest
  2. SS_R = X25519(rPriv_R, ePub)
  3. KEK_R = HKDF-SHA256(ikm=SS_R, salt=IV, info="hiri-cek-v1.1" || ownId, length=32)
  4. secretKey = AES-256-GCM-Decrypt(KEK_R, IV, encryptedKey_R)
```

**Why `recipientId` in the HKDF `info` parameter:** Without it, all recipients would derive the same KEK from the same shared secret base, differing only by the ECDH computation with their public key. Including `recipientId` in `info` provides domain separation — even if two recipients had the same X25519 public key (impossible in practice but a defense-in-depth measure), their KEKs would differ.

**INFORMATIONAL — IV and nonce clarification:** The IV generated in step 2 is exactly 96 bits (12 bytes) — the standard AES-GCM nonce size. The same 12-byte IV is used as the nonce for both content encryption (step 5, with key=CEK) and per-recipient key encryption (step 8c, with key=KEK). This reuse is safe because the keys differ: each (key, nonce) pair is unique, satisfying AES-GCM's security bounds. Each recipient's KEK is cryptographically unique via HKDF domain separation. Security auditors should verify the HKDF derivation path, not the nonce, as the uniqueness guarantee.

**Normative HKDF `info` byte construction (v1.4.0):** The `info` parameter to HKDF-SHA256 MUST be constructed as a byte-level concatenation of the ASCII protocol label and the UTF-8 encoded recipient ID. Implementations MUST NOT use string concatenation of the label and ID followed by a single UTF-8 encode — this produces identical bytes for some inputs but the explicit byte construction is normative.

```typescript
// Normative pseudocode for HKDF info construction
function buildHKDFInfo(recipientId: string): Uint8Array {
  const label = new TextEncoder().encode("hiri-cek-v1.1");  // 13 bytes, ASCII
  const id    = new TextEncoder().encode(recipientId);       // variable length, UTF-8
  const info  = new Uint8Array(label.length + id.length);
  info.set(label, 0);
  info.set(id, label.length);
  return info;
  // Example: recipientId = "alice"
  // label bytes: [0x68, 0x69, 0x72, 0x69, 0x2d, 0x63, 0x65, 0x6b, 0x2d, 0x76, 0x31, 0x2e, 0x31]
  //              h     i     r     i     -     c     e     k     -     v     1     .     1
  // id bytes:    [0x61, 0x6c, 0x69, 0x63, 0x65]
  //              a     l     i     c     e
  // info:        [0x68, 0x69, 0x72, 0x69, 0x2d, 0x63, 0x65, 0x6b, 0x2d, 0x76, 0x31, 0x2e, 0x31, 0x61, 0x6c, 0x69, 0x63, 0x65]
  //              |--- "hiri-cek-v1.1" (13 bytes) ---|  |-- "alice" (5 bytes) --|
}

// Full KEK derivation
function deriveKEK(sharedSecret: Uint8Array, iv: Uint8Array, recipientId: string): Uint8Array {
  return HKDF_SHA256({
    ikm:    sharedSecret,         // 32 bytes from X25519
    salt:   iv,                   // 12 bytes (the AES-GCM IV)
    info:   buildHKDFInfo(recipientId),
    length: 32                    // 256-bit KEK
  });
}
```

**HPKE as normative alternative (v1.4.1):** Implementations MUST support either the HKDF construction specified above OR RFC 9180 (HPKE) mode `Base` with KEM `DHKEM(X25519, HKDF-SHA256)`, KDF `HKDF-SHA256`, and AEAD `AES-256-GCM`. Both produce interoperable results when the recipient ID is included in the `info` parameter per the construction above. Implementations using HPKE MUST declare `"keyAgreement": "HPKE-Base-X25519-SHA256-AES256GCM"` in the manifest parameters. Implementations MUST accept manifests using either key agreement identifier. Test vector B.14 provides a concrete derivation example for cross-implementation verification.

This dual-path design allows implementers to use well-audited HPKE libraries where available while preserving interoperability with the explicit HKDF construction. The two paths produce the same KEK for the same inputs — they differ only in API surface, not in cryptographic output.

### 13.3 Ed25519 ↔ X25519 Conversion and Key Type Clarification

HIRI authorities use Ed25519 keys. Encryption uses X25519 keys. These conversion functions are needed to derive X25519 encryption keys from recipients' Ed25519 HIRI identities:

```typescript
function ed25519PublicToX25519(edPublic: Uint8Array): Uint8Array;
function ed25519PrivateToX25519(edPrivate: Uint8Array): Uint8Array;
```

**Scope of conversion:** These functions are used for **recipient keys only**. A recipient's HIRI authority contains an Ed25519 public key. The publisher converts it to X25519 for the ECDH key agreement.

**Ephemeral key generation:** The ephemeral keypair in §13.2 (step 1) is generated **natively as X25519**, NOT as Ed25519 and then converted. The `ephemeralPublicKey` stored in the manifest is a raw 32-byte X25519 public key, encoded as `z` + base58btc (following the HIRI multibase convention for all public keys). The `z` prefix denotes the encoding, not the key algorithm.

Implementations MUST NOT generate an Ed25519 ephemeral keypair and convert it to X25519. While mathematically related, the two operations use different key generation procedures and an Ed25519-then-convert path may introduce subtle timing or correctness issues in some libraries.

**Summary of key types:**

| Key | Algorithm | Generated As | Stored As |
|-----|-----------|-------------|-----------|
| Publisher signing key | Ed25519 | Ed25519 | `z` + base58btc in KeyDocument |
| Recipient identity key | Ed25519 | Ed25519 | `z` + base58btc in KeyDocument |
| Recipient encryption key | X25519 | Converted from Ed25519 | Not stored separately |
| Ephemeral key (per manifest) | X25519 | X25519 native | `z` + base58btc in manifest |

### 13.4 Key Rotation and Re-Encryption

When a HIRI signing key is rotated (v3.1.1 §13.4), the encryption keys are unaffected — the CEK is independent of the signing key. If a recipient's key is compromised, the publisher MUST re-encrypt with a new CEK and publish a new manifest version excluding the compromised recipient.

---

## 14. Delta Restrictions

### 14.1 Motivation (v1.1.0)

Standard HIRI deltas (JSON Patch per v3.1.1 §11.4 or RDF Patch per §11.4.3) operate over the published content representation. In privacy-preserving modes, the published representation is transformed (encrypted, partially disclosed), and deltas over these representations leak metadata:

- A JSON Patch over encrypted content reveals nothing useful (the ciphertext is opaque)
- A JSON Patch over selectively-disclosed content reveals which statements were added, removed, or modified — even if the statement values are withheld
- Array index operations (`/path/3`) reveal collection cardinalities

### 14.2 Delta Rules by Mode

| Mode | Delta Permitted | Restriction |
|------|----------------|-------------|
| Public | Yes | Standard v3.1.1 behavior |
| Proof of Possession | Content-hash-only | Delta describes change to the withheld content; only the new content hash is published. Delta operations are NOT published. |
| Encrypted Distribution | Opaque only | If delta is present, `hiri:delta.format` MUST be `"application/octet-stream"`. The delta content is encrypted with the same CEK as the main content. Unauthorized parties see only that a delta exists and its encrypted size. |
| Selective Disclosure | Statement-index-only | Delta MUST NOT include operation-level detail. The manifest declares the new statement count and index root. A verifier can see that the statement count changed (12 → 14) but not which statements were added or modified. |
| Anonymous | Per content visibility | Same restrictions as the content visibility sub-mode |
| Attestation | Standard | Attestation chains use standard versioning |

### 14.3 Opaque Delta (Mode 2)

In encrypted mode, the manifest-level delta metadata is minimal — it declares that an opaque delta exists, but reveals no structural information about the change:

```json
{
  "hiri:delta": {
    "hash": "sha256:abc123...",
    "format": "application/octet-stream",
    "operations": -1,
    "encrypted": true
  }
}
```

The `operations: -1` sentinel indicates that the operation count is hidden. The `appliesTo` field is NOT present in the manifest-level metadata — it is encrypted inside the delta blob to prevent unauthorized verifiers from correlating plaintext hashes across versions.

**Inside the encrypted delta blob** (visible only to authorized recipients after decryption):

```json
{
  "appliesTo": "sha256:previousPlaintextHash...",
  "format": "application/json-patch+json",
  "operations": [ ... ]
}
```

The inner `appliesTo` references the previous version's **logical plaintext hash** (as returned by `getLogicalPlaintextHash()`), not the previous ciphertext hash. This ensures that re-encryption with a new CEK (same plaintext, new ciphertext) does not break the delta chain. An unauthorized verifier cannot check `appliesTo` — they see only that an opaque delta exists. An authorized verifier decrypts the blob and verifies `appliesTo` against the previous version's logical plaintext hash.

### 14.4 Statement-Index Delta (Mode 3)

```json
{
  "hiri:delta": {
    "format": "application/hiri-statement-index-delta+json",
    "previousIndexRoot": "sha256:oldRoot...",
    "currentIndexRoot": "sha256:newRoot...",
    "previousStatementCount": 12,
    "currentStatementCount": 14
  }
}
```

No operation-level detail is published. The delta proves that the document changed (the index root is different) and by how much (statement count changed from 12 to 14). The actual changes are visible only to recipients who receive the updated statement set.

### 14.5 Delta Metadata Hardening (v1.4.0)

Even with the restrictions above, delta presence and metadata reveal information: how often the document changes (version frequency), how much it changes (statement count delta), and when it changes (timestamps). For deployments where change patterns are sensitive:

**Batching:** Publishers SHOULD batch changes and publish new versions on a fixed schedule (e.g., weekly, monthly) rather than on every change. This prevents an observer from correlating real-world events with version updates.

**Statement count padding:** When using selective disclosure (Mode 3), publishers MAY pad the statement count to a fixed bucket size (e.g., round up to the nearest multiple of 8). Padding statements are syntactically valid N-Quads with no semantic content (e.g., `<hiri://padding> <hiri://pad> "0" .`). The padded statements are withheld and their HMAC tags are published like any other statement. This hides the true statement count within a bucket.

**Opaque delta suppression:** Publishers MAY omit `hiri:delta` entirely and publish each version as a standalone manifest. This hides the change magnitude at the cost of larger storage (full content per version instead of delta). For proof-of-possession chains (Mode 1) where only the manifest is published, this cost is negligible.

---

## 15. Security Considerations

### 15.1 Threat Model

| Threat | Mitigated By | Mode |
|--------|-------------|------|
| Unauthorized content access | AES-256-GCM encryption | 2 |
| Statement-level data leakage | Statement-level disclosure proofs | 3 |
| Dictionary/rainbow-table attack on withheld statements | Per-manifest indexSalt + HMAC key (§8.4, §8.6.1) | 3 |
| Blank node label reassignment in partial graphs | Normative no-re-canonicalization rule (§8.8) | 3 |
| Publisher identification | Ephemeral/pseudonymous authorities | 4 |
| False custody claims | Challenge-response protocol (optional) | 1 |
| Attestation forgery | Dual-signature verification | 5 |
| Ciphertext tampering | GCM authentication tag + content hash | 2 |
| Key extraction from manifest | Ephemeral ECDH + HKDF domain separation | 2, 3 |
| Structural metadata leakage via deltas | Delta restrictions (§14) | 2, 3 |
| RDF graph structure leakage | Statement-level (not field-level) disclosure | 3 |
| Metadata leakage | NOT fully mitigated — see §15.3 | All |

### 15.2 Encryption Guarantees

AES-256-GCM provides confidentiality, integrity, and authenticity for encrypted content. The single-ephemeral-key-per-CEK design (v1.1.0) does not weaken these guarantees — each recipient derives a unique KEK via HKDF with per-recipient domain separation.

### 15.3 Metadata Leakage and Hardening

Even with content encryption, the manifest reveals:

- Publisher identity (unless Mode 4)
- Content size (from `hiri:content.size`)
- Number of recipients (from the recipients array)
- Recipient identifiers (from recipient `id` fields)
- Publication timestamps (from `hiri:timing`)
- Version history (from the chain)
- Statement count (in Mode 3, from `statementCount`)
- Whether content changed between versions (from delta presence and index root changes)

**Metadata-hardening recommendations (v1.4.0):**

Deployments where metadata patterns are sensitive SHOULD apply the following mitigations. These are RECOMMENDED for Privacy Level 3 conformance in high-assurance contexts.

**Content size padding:** Pad encrypted content (Mode 2) to the nearest power-of-2 boundary (e.g., 512, 1024, 2048 bytes) before encryption. Record the true `plaintextSize` in the privacy parameters (encrypted alongside the CEK or embedded in the ciphertext). The published `hiri:content.size` reflects the padded ciphertext size, not the true content size.

**Recipient ID obfuscation:** Use opaque, random UUIDs as recipient `id` values. MUST NOT use human-readable names, email addresses, or organizational identifiers as recipient IDs in the manifest. The mapping from UUID to real identity is maintained out-of-band by the publisher.

**Statement count bucketing:** Pad the statement count to a fixed bucket size (§14.5). Publish the bucket size in `hiri:privacy.parameters.statementCountBucket` so verifiers know the count is padded: `"statementCountBucket": 8` means the published count is rounded up to the nearest multiple of 8.

**Publication cadence normalization:** Publish new versions on a fixed schedule regardless of whether content changed. A "no-change" version has the same content hash and index root as its predecessor. This prevents timing analysis from correlating publication events with real-world activity.

**Recipient count concealment:** For high-sensitivity deployments, publishers MAY add dummy recipient entries (encrypted to ephemeral keys the publisher controls). This conceals the true recipient count at the cost of slightly larger manifests. Dummy entries are indistinguishable from real entries to an observer.

**Recommended defaults (v1.4.1):** The following table provides non-arbitrary starting points for metadata-hardening parameters. These are RECOMMENDED values; deployments MAY adjust based on their privacy and performance requirements.

| Parameter | Recommended Default | Effect |
|-----------|-------------------|--------|
| Content size padding quantum | 1024 bytes (pad to nearest 1 KB) | Conceals true plaintext size within 1 KB buckets |
| Statement count bucket size | 8 (round up to nearest multiple of 8) | Conceals true statement count within groups of 8 |
| Dummy recipient count | 2 (add 2 dummy entries per manifest) | Makes 3-recipient and 5-recipient manifests indistinguishable |
| Delta batching window | 24 hours or 5 changes, whichever comes first | Prevents per-change timing analysis |
| Publication cadence | Weekly (for low-change-rate content) | Normalizes publication frequency |
| Recipient ID format | UUID v4 (random, 36 characters) | Prevents identity inference from ID patterns |
| KeyDocument cache TTL | 48 hours | Balances freshness with offline availability |

**Size impact:** For a typical manifest with 5 real recipients, 2 dummy recipients, 1 KB padded content, and 8-bucket statement count: manifest overhead increases by approximately 300–500 bytes (two additional encrypted key shares + padding). This is negligible relative to the privacy gain.

### 15.4 Forward Secrecy

Ephemeral ECDH provides partial forward secrecy: compromise of a recipient's long-term private key allows decryption of messages encrypted TO that recipient, but compromise of the publisher's Ed25519 signing key does NOT reveal any CEKs.

### 15.5 Quantum Resistance

AES-256-GCM is considered quantum-resistant for confidentiality. X25519 key agreement is NOT quantum-resistant. Future versions SHOULD define post-quantum key encapsulation mechanisms (e.g., ML-KEM) as alternatives.

### 15.6 Selective Disclosure Security Properties

**HMAC suite (`hiri-hmac-sd-2026`):**

- Statement forgery resistance: an attacker who does not possess the HMAC key cannot produce a valid HMAC tag for a fabricated statement
- Dictionary attack resistance (v1.2.0): the per-manifest `indexSalt` prevents pre-computation of statement hashes. An attacker must brute-force candidates per-manifest, and even then, matching a salted hash does not produce the HMAC tag required for full verification
- Defense-in-depth (v1.2.0): salted hashes and HMAC tags form two independent layers. The salt defeats cross-manifest rainbow tables. The HMAC key defeats per-manifest dictionary attacks on low-entropy fields. Together, they protect even boolean or small-enumeration fields against inference.
- Disclosure scope: the HMAC key is symmetric — any recipient who holds it can verify any statement for which they obtain the plaintext. Per-recipient disclosure is enforced by plaintext distribution, not by cryptographic access control
- Statement enumeration: an attacker can see the total statement count and the HMAC tags, but cannot derive statement content from the tags (HMAC is a PRF)
- Blank node safety (v1.2.0): verifiers hash N-Quad strings as provided (§8.8), never re-canonicalize subsets. This prevents false verification failures caused by URDNA2015 blank node label reassignment in partial graphs.

**BBS+ suite (`hiri-bbs-sd-2026`):**

- Zero-knowledge: a BBS+ disclosure proof reveals nothing about undisclosed statements, not even their count (the proof is over the disclosed subset only, with the total count as a public input)
- Per-recipient cryptographic enforcement: each recipient's disclosure proof covers only their authorized statements. They cannot extend it to cover additional statements.
- Signer linkability: BBS+ proofs from the same signer are linkable (same verification key). Unlinkable disclosures require additional randomization (deferred)

### 15.7 Anonymous Authority Security

Ephemeral authorities provide unlinkability but no accountability. Verifiers of anonymous manifests SHOULD weight the content's trustworthiness accordingly.

---

## 16. Conformance Levels

### 16.1 Privacy Level 1: Basic

**MUST implement:**

- Privacy mode declaration parsing (§5)
- Mode 1: Proof of Possession — manifest-only resolution (§6)
- `getLogicalPlaintextHash()` function (§11.3)
- Graceful degradation for unrecognized modes (§4.4)

### 16.2 Privacy Level 2: Confidential

**MUST implement everything in Level 1, plus:**

- Mode 2: Encrypted Distribution (§7)
- AES-256-GCM encryption/decryption
- X25519 key agreement with single ephemeral keypair (§13.2)
- Ed25519 ↔ X25519 key conversion (§13.3)
- Dual content hash verification (§7.6)
- Delta restrictions for encrypted mode (§14.3)

### 16.3 Privacy Level 3: Full

**MUST implement everything in Level 2, plus:**

- Mode 3: Selective Disclosure with HMAC suite (§8.6.1)
- Mode 4: Anonymous Publication (§9)
- Mode 5: Third-Party Attestation (§10)
- Privacy lifecycle transitions with `getLogicalPlaintextHash()` chain walking (§11)
- Delta restrictions for selective disclosure mode (§14.4)
- Extended resolution algorithm (§12)

**RECOMMENDED (v1.4.0):**

- BBS+ disclosure proof suite (§8.6.2) — RECOMMENDED for deployments protecting PII, regulated data, or legally privileged information
- Metadata-hardening mitigations (§15.3) — RECOMMENDED for high-assurance deployments
- Delta padding and batching (§14.5) — RECOMMENDED when change patterns are sensitive

**MAY implement:**

- BBS+ disclosure proof suite (if not implementing the RECOMMENDED guidance above)

---

## 17. Future: Commitment-Based Content Model

This section defines interface contracts for a future commitment-based privacy model. These interfaces are NOT normative in v1.4.1 but are specified here to prevent incompatible designs.

### 17.1 Motivation

The HMAC-based selective disclosure model (§8.6.1) provides statement-level visibility control but does not support zero-knowledge proofs over field values (e.g., "this person's age is over 18" without revealing the age). A commitment-based model would enable such proofs.

### 17.2 Commitment Interface

```typescript
interface FieldCommitment {
  fieldPath: string;
  commitment: string;
  commitmentScheme: string;
}

interface CommitmentOpening {
  fieldPath: string;
  value: any;
  randomness: string;
}

interface CommitmentVector {
  scheme: string;
  commitments: FieldCommitment[];
  generatorPoints: {
    G: string;
    H: string;
  };
}
```

### 17.3 Addressing Mode: `commitment-pedersen`

Reserved for future use. A content addressing mode where `hiri:content.hash` covers the commitment vector.

### 17.4 Interaction with Statement-Level Disclosure

The commitment model and statement-level disclosure are complementary:

- **Statement-level** (§8): controls WHICH facts are visible (entire statements shown or hidden)
- **Commitment-based** (future): controls WHAT is provable about hidden facts (ZK proofs over committed values)

A future specification MAY combine both: statements containing sensitive field values are committed (Pedersen), the commitment vector is included as a statement in the RDF graph, and the statement-level disclosure mechanism controls which commitment-bearing statements are visible. ZK proofs then operate over the visible commitments.

### 17.5 Delta Over Commitments

Deltas over commitment vectors would declare which field commitments changed without revealing the old or new values. A `transitionProof` (ZK proof that the new commitment is a valid transition from the old under declared rules) is the most complex piece and requires per-application circuit design.

---

## 18. Companion Deliverables (v1.4.1)

This specification defines the protocol — what implementations MUST, SHOULD, and MAY do. It is not a developer tutorial, a reference implementation, or a deployment playbook. The following companion deliverables are scoped separately and SHOULD be published alongside the specification to reduce adoption friction and prevent implementation fragmentation.

### 18.1 Reference Implementation

A reference implementation SHOULD be published as open-source packages providing:

- URDNA2015 canonicalizer with secure document loader (WASM + JS)
- `indexSalt` generation and statement index construction utilities
- HKDF `info` builder matching the normative pseudocode in §13.2
- HMAC tag generation and verification
- Manifest builder and validator (schema enforcement for all five privacy modes)
- Ed25519 ↔ X25519 key conversion

The reference implementation is NOT normative. Conformance is determined by test vector matching (Appendix B), not by code equivalence. The reference implementation is a convenience for implementers, not a substitute for the specification.

### 18.2 Developer Guide

A developer guide SHOULD be published covering:

- Step-by-step tutorial: create → sign → encrypt → publish → resolve for each privacy mode
- Migration quickstart: moving from plaintext HIRI manifests to privacy-enabled manifests
- Copy-paste code snippets in JavaScript, Python, and Go for the byte-level operations that implementers most frequently get wrong (base64url decode, salt concatenation, HKDF info construction)
- End-to-end examples for common scenarios (employee record with selective disclosure, confidential report with encrypted distribution, anonymous whistleblower publication)

### 18.3 Conformance Test Suite

A conformance test suite SHOULD be published providing:

- Executable test vectors corresponding to every entry in Appendix B
- Cross-language validation (at minimum JS and one compiled language) to catch string-vs-bytes encoding errors
- Large-manifest stress vectors (100 recipients, 10 KB plaintext, 50+ statements) with expected parse and verification times from the reference implementation
- Negative test vectors (malformed manifests, wrong salt encoding, re-canonicalized blank nodes) to verify that implementations reject invalid inputs correctly

### 18.4 Deployment Profiles (INFORMATIVE)

Deployment profiles SHOULD be published as informative guidance documents that bundle algorithm choices, key distribution patterns, and privacy-hardening parameters for specific contexts:

- **Minimal profile:** Privacy Level 1 + Proof of Possession. For organizations that need provenance without confidentiality.
- **Standard profile:** Privacy Level 2 + Encrypted Distribution + HIRI KeyDocument bootstrapping + RECOMMENDED metadata-hardening defaults from §15.3. For general-purpose confidential data sharing.
- **High-assurance profile:** Privacy Level 3 + BBS+ selective disclosure + all metadata-hardening mitigations + transparency log checkpoints. For regulated data, intelligence sharing, and legally privileged information.

These profiles are deployment guidance, not protocol requirements. They exist to prevent the fragmentation that occurs when implementers independently invent incompatible default configurations.

---

## Appendix A: Manifest Examples

### A.1 Proof of Possession

```json
{
  "@context": [
    "https://hiri-protocol.org/spec/v3.1",
    "https://hiri-protocol.org/privacy/v1",
    "https://w3id.org/security/v2"
  ],
  "@id": "hiri://key:ed25519:z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK/data/classified-report",
  "@type": "hiri:ResolutionManifest",

  "hiri:version": "1",
  "hiri:branch": "main",
  "hiri:timing": { "created": "2026-03-07T12:00:00Z" },

  "hiri:privacy": {
    "mode": "proof-of-possession",
    "parameters": {
      "availability": "private",
      "custodyAssertion": true,
      "refreshPolicy": "P30D"
    }
  },

  "hiri:content": {
    "hash": "sha256:e08da327a1f2b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9",
    "addressing": "raw-sha256",
    "canonicalization": "JCS",
    "format": "application/ld+json",
    "size": 2048,
    "availability": "private"
  },

  "hiri:signature": {
    "type": "Ed25519Signature2020",
    "canonicalization": "JCS",
    "created": "2026-03-07T12:00:00Z",
    "verificationMethod": "hiri://key:ed25519:z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK/key/main#key-1",
    "proofPurpose": "assertionMethod",
    "proofValue": "z..."
  }
}
```

### A.2 Encrypted Distribution (v1.1.0 — single ephemeral key)

```json
{
  "@context": [
    "https://hiri-protocol.org/spec/v3.1",
    "https://hiri-protocol.org/privacy/v1",
    "https://w3id.org/security/v2"
  ],
  "@id": "hiri://key:ed25519:z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK/data/personnel-record",
  "@type": "hiri:ResolutionManifest",

  "hiri:version": "2",
  "hiri:branch": "main",
  "hiri:timing": { "created": "2026-04-01T09:00:00Z" },

  "hiri:privacy": {
    "mode": "encrypted",
    "transitionFrom": "proof-of-possession",
    "transitionReason": "Distributing to authorized reviewers.",
    "parameters": {
      "algorithm": "AES-256-GCM",
      "iv": "dGhpcyBpcyBhIHRlc3Q",
      "tagLength": 128,
      "plaintextHash": "sha256:e08da327a1f2b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9",
      "plaintextFormat": "application/ld+json",
      "plaintextSize": 2048,
      "ephemeralPublicKey": "z8dKxU2HAsD4grJxqwVPNCFTwbXPakYGgjmRxMBqQC1rQ",
      "keyAgreement": "X25519-HKDF-SHA256",
      "recipients": [
        {
          "id": "reviewer-alpha",
          "encryptedKey": "YWVzLTI1Ni1nY20tZW5jcnlwdGVkLWtleQ"
        },
        {
          "id": "reviewer-bravo",
          "encryptedKey": "YW5vdGhlci1lbmNyeXB0ZWQta2V5"
        }
      ]
    }
  },

  "hiri:chain": {
    "previous": "sha256:abc123...",
    "genesisHash": "sha256:abc123...",
    "depth": 2,
    "previousBranch": "main"
  },

  "hiri:content": {
    "hash": "sha256:9a4f2c8b1d3e5f7a0b2c4d6e8f0a1b3c5d7e9f0a2b4c6d8e0f1a3b5c7d9e0f1a",
    "addressing": "raw-sha256",
    "canonicalization": "JCS",
    "format": "application/octet-stream",
    "size": 2064
  },

  "hiri:signature": {
    "type": "Ed25519Signature2020",
    "canonicalization": "JCS",
    "created": "2026-04-01T09:00:00Z",
    "verificationMethod": "hiri://key:ed25519:z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK/key/main#key-1",
    "proofPurpose": "assertionMethod",
    "proofValue": "z..."
  }
}
```

### A.3 Selective Disclosure (v1.2.0 — salted statement-level)

```json
{
  "@context": [
    "https://hiri-protocol.org/spec/v3.1",
    "https://hiri-protocol.org/privacy/v1",
    "https://w3id.org/security/v2"
  ],
  "@id": "hiri://key:ed25519:z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK/data/person",
  "@type": "hiri:ResolutionManifest",

  "hiri:version": "1",
  "hiri:branch": "main",
  "hiri:timing": { "created": "2026-03-07T12:00:00Z" },

  "hiri:privacy": {
    "mode": "selective-disclosure",
    "parameters": {
      "disclosureProofSuite": "hiri-hmac-sd-2026",
      "statementCount": 12,
      "indexSalt": "p7PJwi0xNDM2NTc4OTAxMjM0NTY3ODkwMTIzNDU2Nzg5MA",
      "indexRoot": "sha256:f4a3b2c1d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2",
      "mandatoryStatements": [0, 1, 2, 5],
      "hmacKeyRecipients": {
        "ephemeralPublicKey": "z7KpL3nBwEfR2cVdYsTvXhJmNqUkWbAiFgHoZx9CrD5pS",
        "keyAgreement": "X25519-HKDF-SHA256",
        "recipients": [
          {
            "id": "hr-reviewer",
            "encryptedHmacKey": "base64url-encrypted-hmac-key-for-hr",
            "disclosedStatements": "all"
          },
          {
            "id": "background-check",
            "encryptedHmacKey": "base64url-encrypted-hmac-key-for-bg",
            "disclosedStatements": [0, 1, 2, 3, 5, 7]
          }
        ]
      }
    }
  },

  "hiri:content": {
    "hash": "sha256:e08da327a1f2b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9",
    "addressing": "raw-sha256",
    "canonicalization": "URDNA2015",
    "format": "application/ld+json",
    "size": 487,
    "availability": "partial"
  },

  "hiri:signature": {
    "type": "Ed25519Signature2020",
    "canonicalization": "URDNA2015",
    "created": "2026-03-07T12:00:00Z",
    "verificationMethod": "hiri://key:ed25519:z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK/key/main#key-1",
    "proofPurpose": "assertionMethod",
    "proofValue": "z..."
  }
}
```

### A.4 Third-Party Attestation

```json
{
  "@context": [
    "https://hiri-protocol.org/spec/v3.1",
    "https://hiri-protocol.org/privacy/v1",
    "https://w3id.org/security/v2"
  ],
  "@id": "hiri://key:ed25519:z<attestor-key>/attestation/clearance-verification-2026-03",
  "@type": "hiri:AttestationManifest",

  "hiri:version": "1",
  "hiri:branch": "main",
  "hiri:timing": { "created": "2026-03-15T14:30:00Z" },

  "hiri:privacy": { "mode": "attestation" },

  "hiri:attestation": {
    "subject": {
      "authority": "key:ed25519:z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK",
      "manifestHash": "sha256:abc123...",
      "contentHash": "sha256:e08da327...",
      "manifestVersion": "1"
    },
    "claim": {
      "@type": "hiri:PropertyAttestation",
      "property": "security-clearance-valid",
      "value": true,
      "scope": "TS/SCI",
      "attestedAt": "2026-03-15T14:30:00Z",
      "validUntil": "2027-03-15T14:30:00Z"
    },
    "evidence": {
      "method": "direct-examination",
      "description": "Security officer examined personnel record and verified active TS/SCI clearance."
    }
  },

  "hiri:signature": {
    "type": "Ed25519Signature2020",
    "canonicalization": "JCS",
    "created": "2026-03-15T14:30:00Z",
    "verificationMethod": "hiri://key:ed25519:z<attestor-key>/key/main#key-1",
    "proofPurpose": "assertionMethod",
    "proofValue": "z..."
  }
}
```

---

## Appendix B: Normative Test Vectors

### B.1 Proof of Possession Resolution

```
Input:  Manifest with mode "proof-of-possession", availability "private"
Action: Resolve
Result: verified=true, contentStatus="private-custody-asserted", contentRetrieved=false
```

Verifiers MUST NOT report an error for missing content when `availability` is `"private"`.

### B.2 Encrypted Distribution — Unauthorized

```
Input:  Manifest with mode "encrypted", no decryption key
Action: Resolve
Result: verified=true, contentStatus="ciphertext-verified", decryptedContent=null
```

### B.3 Encrypted Distribution — Authorized

```
Input:  Manifest with mode "encrypted", valid decryption key
Action: Resolve with key
Result: verified=true, contentStatus="decrypted-verified", plaintextHashValid=true
```

### B.4 Encrypted Distribution — Wrong Key

```
Input:  Manifest with mode "encrypted", wrong key
Action: Resolve with wrong key
Result: verified=true, contentStatus="decryption-failed", signatureValid=true
```

A decryption failure MUST NOT cause overall verification to fail.

### B.5 Anonymous Ephemeral — No KeyDocument

```
Input:  Manifest with mode "anonymous", authorityType "ephemeral"
Action: Resolve
Result: verified=true, identityType="anonymous-ephemeral", keyDocumentResolved=false
```

### B.6 Attestation — Subject Unavailable

```
Input:  AttestationManifest, subject manifest not in storage
Action: Verify
Result: attestationVerified=true, subjectManifestVerified=false
```

### B.7 Privacy Lifecycle Transition — Logical Plaintext Hash

```
V1: mode="proof-of-possession", content.hash="sha256:aaa..."
V2: mode="encrypted", plaintextHash="sha256:aaa...", content.hash="sha256:bbb..."

Chain walker:
  getLogicalPlaintextHash(V1) = "sha256:aaa..."  (content.hash, since mode is PoP)
  getLogicalPlaintextHash(V2) = "sha256:aaa..."  (plaintextHash, since mode is encrypted)
  Match: true → chain integrity preserved

Raw comparison:
  V1.content.hash = "sha256:aaa..."
  V2.content.hash = "sha256:bbb..."
  Match: false → INCORRECT to treat as corruption
```

Chain walkers MUST use `getLogicalPlaintextHash()`, not raw `content.hash` comparison.

### B.8 Selective Disclosure — Statement Verification (HMAC, v1.3.0)

```
Input:  12-statement document, mandatory=[0,1,2,5], HMAC key known
        indexSalt (base64url) from manifest hiri:privacy.parameters.indexSalt
        Caller has statement 7 plaintext:
        '<hiri://auth/data/person> <http://schema.org/email> "aaron@example.org" .'

Action: Verify statement 7
Steps:
  1. rawSaltBytes = base64urlDecode(indexSalt)              // 32 bytes
  2. stmtBytes = UTF-8(statement7)                          // variable bytes
  3. inputBytes = concat(rawSaltBytes, stmtBytes)           // byte array
  4. tag = HMAC-SHA256(hmacKey, inputBytes)
  5. Compare tag to published hmacTags[7] → MUST match
  6. hash = SHA-256(inputBytes)
  7. Compare hash to statementIndex[7] → MUST match
Result: Statement 7 verified as belonging to original signed dataset
```

### B.9 Salt Defeats Dictionary Attack (v1.2.0)

```
Setup: Withheld statement about blood type. Subject and predicate known.
  Candidates:
    '<hiri://auth/data/person> <http://schema.org/bloodType> "A+" .'
    '<hiri://auth/data/person> <http://schema.org/bloodType> "O+" .'
    ... (8 total candidates)

Without salt (v1.1.0 — VULNERABLE):
  Attacker computes SHA-256 of each candidate.
  Compares to published statementIndex.
  Match found → withheld blood type revealed.

With salt (v1.2.0+ — SAFE):
  indexSalt (base64url in manifest) → decode to rawSaltBytes (32 bytes)
  Attacker computes SHA-256(concat(rawSaltBytes, UTF-8(candidate))) for each.
  Compares to published statementIndex.
  Match found → attacker knows the blood type for THIS manifest.

  Defense: The salt prevents pre-computed rainbow tables.
  However, for 8-candidate enumeration, the salt alone is insufficient.
  The HMAC key (secret, per-recipient) provides the second layer:
  Without the HMAC key, the attacker cannot produce the HMAC tag,
  so they cannot PROVE which candidate matched (the salted hash
  match is a hypothesis, not a verified fact).

  For fields with very low entropy (booleans, small enums),
  publishers SHOULD either:
  (a) Combine low-entropy fields into a single composite statement
      (e.g., embed blood type within a larger medical record object), or
  (b) Use the BBS+ suite (§8.6.2) which reveals nothing about
      withheld statements regardless of entropy.
```

### B.10 Blank Node Verification (v1.2.0)

```
Setup: 6-statement document with a blank node (address object):
  Statement 3: '<hiri://auth/data/person> <http://schema.org/address> _:c14n0 .'
  Statement 4: '_:c14n0 <http://schema.org/addressLocality> "Portland" .'

Mandatory: [3, 4] (address is public)
Withheld: [0, 1, 2, 5] (other fields)

CORRECT verification:
  1. Take statement 3 as-is: '<hiri://auth/data/person> <http://schema.org/address> _:c14n0 .'
  2. rawSaltBytes = base64urlDecode(indexSalt)
  3. hash = SHA-256(concat(rawSaltBytes, UTF-8(statement3)))
  4. Compare to statementIndex[3] → MATCH

INCORRECT verification (re-canonicalization):
  1. Parse statements 3 and 4 into an RDF model
  2. Re-run URDNA2015 on the 2-statement subset
  3. URDNA2015 may assign _:c14n0 → _:c14n0 (lucky) or reassign labels
  4. If reassigned: re-canonicalized N-Quad differs from original
  5. hash = SHA-256(concat(rawSaltBytes, UTF-8(re-canonicalized))) → NO MATCH
  6. False verification failure

Rule: Verifiers MUST hash the provided N-Quad strings directly (§8.8).
```

### B.11 Ephemeral Key Consolidation (v1.1.0)

```
Input:  Manifest with 5 recipients
v1.0.0: 5 ephemeralPublicKey fields (one per recipient) = 160 bytes of keys
v1.1.0: 1 ephemeralPublicKey field (at parameters level) = 32 bytes of keys

Both produce unique KEKs per recipient via HKDF info parameter differentiation.
```

### B.12 Delta Restriction — Encrypted Mode

```
Input:  Mode 2 manifest with delta
Verify: hiri:delta.format MUST be "application/octet-stream"
        hiri:delta.encrypted MUST be true
        hiri:delta.operations MUST be -1 (hidden)
Reject: Any delta with format "application/json-patch+json" in encrypted mode
```

### B.13 Byte-Level Concatenation (v1.3.0)

```
Setup:
  indexSalt (base64url in manifest): "p_O5wg"
  indexSalt (raw bytes after decode): [0xa7, 0xf3, 0xb9, 0xc2]  (4 bytes for this example; real salt is 32 bytes)
  Statement: '<http://example.org/s> <http://example.org/p> "hello" .'
  Statement UTF-8 bytes: [0x3c, 0x68, 0x74, 0x74, 0x70, ...]  (51 bytes)

CORRECT (byte concatenation):
  inputBytes = [0xa7, 0xf3, 0xb9, 0xc2, 0x3c, 0x68, 0x74, 0x74, 0x70, ...]
               ^^^^^^^^^^^^^^^^^^^^^^  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
               raw salt bytes (4)      UTF-8 statement bytes (51)
  Total: 55 bytes
  hash = SHA-256(inputBytes)

WRONG (string concatenation):
  saltString = "p_O5wg"  (base64url encoding, 6 ASCII characters)
  combined = "p_O5wg" + '<http://example.org/s> <http://example.org/p> "hello" .'
  inputBytes = UTF-8(combined)
  Total: 57 bytes  ← DIFFERENT LENGTH, DIFFERENT HASH
  hash = SHA-256(inputBytes)  ← NON-INTEROPERABLE

Rule: Always decode indexSalt to raw bytes BEFORE concatenation (§8.4.1).
```

### B.14 HKDF KEK Derivation (v1.4.0)

```
Setup:
  Ephemeral private key (publisher):  ePriv (32 bytes, hex: "a0b1c2d3...")
  Recipient public key (X25519):      rPub  (32 bytes, hex: "d4e5f6a7...")
  IV (from manifest):                 (12 bytes, hex: "010203040506070809101112")
  Recipient ID:                       "alice"

Step 1: Shared secret
  SS = X25519(ePriv, rPub) = (32 bytes)

Step 2: Build HKDF info (§13.2)
  label = UTF-8("hiri-cek-v1.1")
        = [0x68, 0x69, 0x72, 0x69, 0x2d, 0x63, 0x65, 0x6b, 0x2d, 0x76, 0x31, 0x2e, 0x31]
        // 13 bytes
  id    = UTF-8("alice")
        = [0x61, 0x6c, 0x69, 0x63, 0x65]
        // 5 bytes
  info  = concat(label, id)
        = [0x68, 0x69, 0x72, 0x69, 0x2d, 0x63, 0x65, 0x6b, 0x2d, 0x76, 0x31, 0x2e, 0x31, 0x61, 0x6c, 0x69, 0x63, 0x65]
        // 18 bytes total

Step 3: Derive KEK
  KEK = HKDF-SHA256(ikm=SS, salt=IV, info=info, length=32)
  // KEK is 32 bytes, unique to this (publisher-ephemeral, recipient, recipientId) triple

Step 4: Encrypt CEK
  encryptedKey = AES-256-GCM(key=KEK, nonce=IV, plaintext=CEK)

Verification:
  A second recipient "bob" with the SAME X25519 public key as "alice"
  (impossible in practice, but for testing):
    info_bob  = concat(label, UTF-8("bob"))
              = [0x68, 0x69, 0x72, 0x69, 0x2d, 0x63, 0x65, 0x6b, 0x2d, 0x76, 0x31, 0x2e, 0x31, 0x62, 0x6f, 0x62]
    KEK_bob   = HKDF-SHA256(ikm=SS, salt=IV, info=info_bob, length=32)
    KEK_bob  ≠ KEK_alice   ← Domain separation confirmed

WRONG info construction:
  info = UTF-8("hiri-cek-v1.1" + "alice")  // String concat then encode
       = UTF-8("hiri-cek-v1.1alice")
       = same bytes as correct construction in THIS case

  info = UTF-8("hiri-cek-v1.1" + ":" + "alice")  // Adding a separator
       = WRONG — no separator in the normative construction

Rule: Use the exact byte construction from §13.2. No separators. No framing.
      The label and ID are concatenated directly at the byte level.
```

### B.15 Cross-Mode Chain — getLogicalPlaintextHash() (v1.4.0)

```
A document transitions through three privacy modes across three versions:

V1 — Proof of Possession:
  hiri:privacy.mode = "proof-of-possession"
  hiri:content.hash = "sha256:aaa111..."        // Hash of plaintext (withheld)
  hiri:content.availability = "private"
  No hiri:privacy.parameters.plaintextHash

  getLogicalPlaintextHash(V1):
    mode = "proof-of-possession" → return hiri:content.hash
    = "sha256:aaa111..."

V2 — Encrypted Distribution (same plaintext, now shared with reviewers):
  hiri:privacy.mode = "encrypted"
  hiri:privacy.transitionFrom = "proof-of-possession"
  hiri:content.hash = "sha256:bbb222..."         // Hash of CIPHERTEXT
  hiri:privacy.parameters.plaintextHash = "sha256:aaa111..."  // Same plaintext
  hiri:chain.previous = V1 manifest hash

  getLogicalPlaintextHash(V2):
    mode = "encrypted" → return hiri:privacy.parameters.plaintextHash
    = "sha256:aaa111..."

  Chain check: getLogicalPlaintextHash(V1) == getLogicalPlaintextHash(V2) ✓
  (Content unchanged, only visibility changed)

V3 — Public (plaintext published openly):
  hiri:privacy.mode = "public"
  hiri:privacy.transitionFrom = "encrypted"
  hiri:content.hash = "sha256:aaa111..."         // Hash of PLAINTEXT (same as V1)
  No hiri:privacy block (or mode = "public")
  hiri:chain.previous = V2 manifest hash

  getLogicalPlaintextHash(V3):
    mode = "public" → return hiri:content.hash
    = "sha256:aaa111..."

  Chain check: getLogicalPlaintextHash(V2) == getLogicalPlaintextHash(V3) ✓

Full chain: "sha256:aaa111..." == "sha256:aaa111..." == "sha256:aaa111..." ✓
The logical plaintext hash is consistent across all three modes.

WRONG chain check (raw content.hash comparison):
  V1.content.hash = "sha256:aaa111..."  (plaintext)
  V2.content.hash = "sha256:bbb222..."  (ciphertext)  ← DIFFERENT
  V3.content.hash = "sha256:aaa111..."  (plaintext)

  V1 → V2: "aaa111" ≠ "bbb222" → FALSE CORRUPTION ALARM
  V2 → V3: "bbb222" ≠ "aaa111" → FALSE CORRUPTION ALARM

Rule: Chain walkers MUST use getLogicalPlaintextHash() (§11.3),
      not raw hiri:content.hash comparison.
```

### B.16 AES-256-GCM Zero-Byte Plaintext (v1.4.1)

> **Implementation note:** AES-256-GCM encrypting zero bytes of plaintext produces a 16-byte ciphertext consisting entirely of the 128-bit authentication tag. This is correct per the GCM specification (NIST SP 800-38D). Implementations MUST NOT reject zero-length ciphertext minus tag; `ciphertext.length >= tagLength / 8` is the correct lower bound, not `ciphertext.length > plaintext.length`.

---

## Appendix C: Privacy Mode Decision Matrix

### C.1 Choosing a Mode

| I want to... | Mode | What's published | Who can read |
|--------------|------|------------------|-------------|
| Prove I have data without showing it | Proof of Possession | Manifest only | Nobody |
| Share data with specific people | Encrypted Distribution | Encrypted blob | Recipients |
| Show some facts, hide others | Selective Disclosure | Subset of RDF statements | Statement-dependent |
| Publish without revealing my identity | Anonymous | Depends on sub-mode | Depends on sub-mode |
| Have a third party vouch for my data | Attestation | Attestor's signed claim | Everyone (claim only) |
| Publish openly | Public (default) | Everything | Everyone |

### C.2 Combined Scenarios

| Scenario | Modes | Example |
|----------|-------|---------|
| Anonymous whistleblower with encrypted evidence | Anonymous + Encrypted | Source hidden; journalists decrypt |
| Custody proof with third-party validation | PoP + Attestation | Organization holds data; auditor attests |
| Partial disclosure with ZK proofs | Selective Disclosure + BBS+ | Prove age > 18 without revealing DOB |
| Attestation chain with delegation | Attestation + Attestation | Auditor attests; meta-auditor attests process |

---

## Appendix D: Statement Index Construction

### D.1 Worked Example

Given a JSON-LD document:

```json
{
  "@context": { "schema": "http://schema.org/" },
  "@id": "hiri://authority/data/person",
  "@type": "schema:Person",
  "schema:name": "Aaron",
  "schema:jobTitle": "Semantic Architect",
  "schema:email": "aaron@example.org"
}
```

After URDNA2015 canonicalization, the N-Quads output is (example, actual output depends on context expansion):

```
<hiri://authority/data/person> <http://schema.org/email> "aaron@example.org" .
<hiri://authority/data/person> <http://schema.org/jobTitle> "Semantic Architect" .
<hiri://authority/data/person> <http://schema.org/name> "Aaron" .
<hiri://authority/data/person> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Person> .
```

Statement index (salted, per §8.4):

```
indexSalt (base64url, as stored in manifest): "p_O5wjAxNDM2NTc4OTAxMjM0NTY3ODkw"
indexSalt (raw bytes, after base64url decode): [0xa7, 0xf3, 0xb9, 0xc2, ...]  (32 bytes)

For each statement, the hash input is the byte-level concatenation:
  inputBytes = concat(rawSaltBytes, UTF-8(nquad_string))

[0] SHA-256(concat(rawSaltBytes, UTF-8('<hiri://authority/data/person> <http://schema.org/email> "aaron@example.org" .')))
    = sha256:7a2f...

[1] SHA-256(concat(rawSaltBytes, UTF-8('<hiri://authority/data/person> <http://schema.org/jobTitle> "Semantic Architect" .')))
    = sha256:3b8e...

[2] SHA-256(concat(rawSaltBytes, UTF-8('<hiri://authority/data/person> <http://schema.org/name> "Aaron" .')))
    = sha256:c4d1...

[3] SHA-256(concat(rawSaltBytes, UTF-8('<hiri://authority/data/person> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Person> .')))
    = sha256:9f0a...
```

Index root (concatenate raw 32-byte digests, not prefixed hex strings):

```
Each statementHash above is a raw 32-byte SHA-256 digest.
The "sha256:7a2f..." notation is for display only.

rawDigests = concat(
  rawDigest[0],   // 32 bytes (the raw bytes behind "sha256:7a2f...")
  rawDigest[1],   // 32 bytes (the raw bytes behind "sha256:3b8e...")
  rawDigest[2],   // 32 bytes (the raw bytes behind "sha256:c4d1...")
  rawDigest[3]    // 32 bytes (the raw bytes behind "sha256:9f0a...")
)
// Total: 128 bytes (4 statements × 32 bytes each)

indexRootBytes = SHA-256(rawDigests)
indexRoot      = "sha256:" + hex(indexRootBytes) = "sha256:f4a3..."

WRONG: SHA-256(UTF-8("sha256:7a2f..." + "sha256:3b8e..." + ...))
       ↑ Concatenating prefixed hex STRINGS produces a different hash.
```

Note: an attacker who knows the subject URI and predicate URI for statement [0] could enumerate plausible email addresses, decode the published `indexSalt` to raw bytes, compute `SHA-256(concat(rawSaltBytes, UTF-8(candidate)))` for each, and compare against the published index. The salt prevents pre-computation across manifests but does not prevent per-manifest enumeration. For high-entropy fields (email addresses with unknown domains), this is infeasible. For low-entropy fields, the HMAC key provides the second defense layer (§8.6.1).

If mandatory statements are [2, 3] (name and type), the published N-Quads document contains:

```
<hiri://authority/data/person> <http://schema.org/name> "Aaron" .
<hiri://authority/data/person> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Person> .
```

This is a valid RDF subgraph. Any SPARQL engine can query it. A query for `schema:name` returns "Aaron". A query for `schema:email` returns no results — the statement is withheld, not replaced with a placeholder.

---

## Appendix E: Suggested Key Distribution Patterns (INFORMATIVE)

This appendix describes common patterns for bootstrapping recipient public keys. It is INFORMATIVE — the privacy extension does not mandate any specific key distribution mechanism.

### E.1 HIRI KeyDocument-Based

The recipient publishes a HIRI KeyDocument (v3.1.1 §13.2) containing their Ed25519 public key. The publisher derives the X25519 encryption key via the Ed25519→X25519 conversion (§13.3). This is the most natural pattern within the HIRI ecosystem: both parties are already HIRI participants.

**Bootstrap:** Publisher resolves the recipient's HIRI authority URI, fetches their KeyDocument, and extracts the active public key. Trust is established by the recipient's existing publication history (reputation) or by out-of-band authority verification.

**Strengths:** No external PKI dependency. Self-certifying. Works offline once the KeyDocument is cached.

**Weaknesses:** Requires the recipient to have a published HIRI identity. No institutional trust anchor beyond the key itself.

### E.2 Organizational PKI (X.509, LDAP)

The recipient's public key is bound to an organizational identity via X.509 certificates or LDAP directory entries. The publisher extracts the public key from the certificate chain and converts it for use with HIRI encryption.

**Bootstrap:** Publisher queries the organization's directory service or certificate authority for the recipient's public key. Trust is established by the organizational CA's root certificate.

**Strengths:** Integrates with existing enterprise infrastructure. Institutional trust anchors. Revocation via CRL/OCSP.

**Weaknesses:** Requires online access to the directory or CA (or cached CRL). Depends on the organization's PKI security.

### E.3 DID Methods (did:web, did:key)

The recipient publishes a DID Document containing their public key. `did:key` embeds the key directly in the DID string (similar to HIRI's authority model). `did:web` resolves via HTTPS to a JSON-LD DID Document.

**Bootstrap:** Publisher resolves the recipient's DID, extracts the public key from the DID Document's `verificationMethod` array. Trust is established by the DID method's resolution mechanism.

**Strengths:** Standard W3C method. Interoperable with the broader decentralized identity ecosystem.

**Weaknesses:** `did:web` depends on DNS and HTTPS (not edge-canonical). `did:key` has no rotation or revocation mechanism.

### E.4 Direct Exchange

The recipient provides their public key directly to the publisher — in person, via a secure messaging channel (Signal, encrypted email), or via a QR code. This is the simplest and most secure bootstrap when the parties have a pre-existing relationship.

**Strengths:** No infrastructure dependency. Strongest authentication (in-person verification). Works in air-gapped environments.

**Weaknesses:** Does not scale. Requires pre-existing contact. No automated rotation.

### E.5 Key Transparency Logs (OPTIONAL)

For deployments that require auditable key history, publishers or recipients MAY publish their KeyDocuments (or key rotation claims) to an append-only transparency log. Verifiers can check log checkpoints to confirm that a key was publicly committed before a specific time, reducing the risk of key substitution attacks.

This pattern is OPTIONAL and does not create an online dependency for verification. Verifiers cache log checkpoints and verify against the cache. If the cache is stale, verification proceeds with a warning — the Edge-Canonical First Principle is preserved.

**Strengths:** Auditability. Detects key substitution. Compatible with offline verification via cached checkpoints.

**Weaknesses:** Requires a log operator. Checkpoint freshness is a deployment concern.

---

## Document History

| Version | Date | Status | Notes |
|---------|------|--------|-------|
| 1.0.0 | 2026-03 | Superseded | Initial: five privacy modes |
| 1.1.0 | 2026-03 | Superseded | Statement-level selective disclosure, ephemeral key consolidation, delta restrictions, logical plaintext hash function |
| 1.2.0 | 2026-03 | Superseded | Salted statement hashing, blank node verification rule, IV reuse security note |
| 1.3.0 | 2026-03 | Superseded | Byte-level concatenation rule, BBS+ salt clarification, encoding consistency (base64url) |
| 1.3.1 | 2026-03 | Superseded | Index root raw-digest concatenation clarification |
| 1.4.0 | 2026-03 | Superseded | HKDF normative pseudocode, BBS+ promoted to RECOMMENDED, metadata hardening, key distribution patterns, delta padding, attestation trust guidance |
| **1.4.1** | **2026-03** | **Final** | KeyDocument RECOMMENDED default, HPKE normative option, disclosure suite decision table, metadata defaults, companion deliverables scope |

---

## License

**Specification:** CC0 1.0 Universal (Public Domain)
**Reference Implementations:** Apache 2.0

---

**Version:** 1.4.1
**Status:** Final
**Last Updated:** March 2026

---

*Privacy is not the absence of information. It is the presence of control.*

*This specification treats confidentiality as a layer, not a lock — and makes no distinction about who deserves it.*
