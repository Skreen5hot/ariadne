# HIRI Digital Passport Extension

## Portable, Holder-Sovereign Credential Portfolios on HIRI

**Version:** 1.9.0
**Previous:** 1.8.0
**Status:** Release Candidate
**Status:** Draft
**Date:** March 2026
**Depends on:** HIRI Protocol Specification v3.1.1, HIRI Privacy & Confidentiality Extension v1.4.1
**Context URL:** `https://hiri-protocol.org/passport/v1`

---

## Document Status

This specification defines a **normative extension** to the HIRI Protocol Specification v3.1.1 and the HIRI Privacy & Confidentiality Extension v1.4.1. It introduces the `hiri:PassportManifest` artifact type, the `hiri:CredentialSlot` structure, and a presentation protocol for selective credential disclosure.

This extension does NOT modify any existing HIRI Protocol semantics. All verification, signing, chain integrity, and key lifecycle mechanisms defined in v3.1.1 remain unchanged. All privacy modes defined in the Privacy & Confidentiality Extension v1.4.1 remain unchanged. This extension composes them into a new artifact type.

---

## Changelog: v1.8.0 → v1.9.0

| Change | Section | Breaking | Description |
|--------|---------|----------|-------------|
| **Status elevated to Release Candidate** | Header | No | v1.9.0 is the first Release Candidate. Production adoption requires all items in the sign-off checklist (§1.5) to be verified. |
| **Sign-off checklist and release conditions** | §1.5 | No | New normative section. Defines the six blocking conditions that must be verified before v1.9.0 may be declared a full release. |
| **Reference implementation normative entry hardened** | §2 | No | Repository URL, version tag, and CI badge placeholder made concrete. Conformance claims at Passport-Interoperable or above require reference implementation validation. |
| **Interoperability test results matrix** | §H.9 | No | New normative appendix section. Defines required two-implementation test matrix structure (Node/WASM + Go reference). CI must populate and publish results before full release. |
| **Appendix C machine-readable status mapping** | Appendix C | No | New normative table: every revocation log status code is explicitly bound to the staleness window rule that triggers it and the Phase 3 state machine step that emits it. Enables standardized telemetry across verifier implementations. |
| **Passport-Hardened summary in §15.6** | §15.6 | No | Required field list and cross-references to Appendix H and J added to conformance section so Passport-Hardened requirements are discoverable without reading the full appendix. |
| **Passport-Hardened test vector** | §H.10 | No | New normative test vector for omittedSlotCount padding (Appendix J §J.2) and issuer authority obfuscation (§J.4). |
| **§16.10 3-leaf hex worked example** | §16.10 | No | Concrete hexadecimal Merkle computation (3 leaves) added to Merkle canonicalization section to simplify implementer testing. |
| **Selective-reveal access control** | §16.8.2 | No | Access control and audit logging policy for selective-reveal endpoints. Authenticated request + holder consent proof pattern. Minimal logging requirements. |
| **§6.4 and §10.5 offline resolver behavior** | §6.4, §10.5 | No | Explicit cross-reference to offline decision table (§12.7) added. Resolver behavior when KeyDocument is unreachable but cached checkpoint exists is now normatively specified. |
| **OracleGovernanceDocument template** | Appendix M | No | New INFORMATIVE appendix with complete OracleGovernanceDocument template, filled example, and worked OracleRecoveryNotice. |
| **Migration guidance** | Appendix N | No | New INFORMATIVE appendix. Migration paths for holders upgrading from pre-v1.1.0 (unblinded slots), pre-v1.6.0 (no KeyDocument), and pre-v1.8.0 (no revocation log). Preserves existing verification chain integrity. |
| **Appendix L operator acceptance criteria** | Appendix L.2.4 | No | Operator readiness checklist extended with explicit acceptance criteria table mapping each test to a measurable pass/fail condition. |
| **TOC and terminology updated** | TOC, §3 | No | §1.5, §H.9, §H.10, Appendix M, Appendix N added. `Release Candidate`, `Sign-Off Checklist`, `Interoperability Test Matrix` added to terminology. |
| **Document history updated** | Document History | No | v1.9.0 entry added. |

---

## Changelog: v1.7.0 → v1.8.0

| Change | Section | Breaking | Description |
|--------|---------|----------|-------------|
| **POST /append authentication hardened** | §16.4.3 | No | Replaces opaque bearer token example with two normative authentication paths: mutual TLS with issuer-authority-bound client certificate, and signed JWT issued by OIDC management plane. Opaque bearer tokens alone are no longer acceptable. |
| **Merkle tree canonicalization normative** | §16.10 | No | New normative subsection. Specifies leaf hash = SHA-256(JCS(RevocationLogEntry)), interior node hash = SHA-256(leftHash \|\| rightHash), and inclusion proof encoding as `{hash, side}` array. Required for log interoperability. |
| **Revocation log privacy-preserving mode** | §16.8 | No | New normative subsection. Hash-only log entries for sensitive credential types. Log stores entryHash; plaintext retained by issuer and selectively revealed on request. Protects against existence leakage for GovernmentIdVerification, BackgroundCheckClearance, and similar. |
| **Revocation acceptance windows** | §16.9 | No | New normative subsection. High-value transactions MUST use checkpoint ≤ 15 minutes old. Standard transactions MAY use 48-hour staleness window. `transactionClass` parameter added to verification invocation. |
| **Log operator security** | §16.7 | No | New normative subsection. HSM requirements for log signing keys, append authorization flow, rate limiting, DDoS resilience, audit trail requirements. |
| **Oracle incident response** | §17.7 | No | New normative subsection. Three-phase incident protocol: emergency key revocation (≤ 1 hour), verifier quarantine rules, re-key procedure with 30-day parallel operation minimum. |
| **Oracle governance re-evaluation mandatory** | §17.3 | No | Monthly governance document hash re-evaluation is now REQUIRED (not RECOMMENDED) for oracles configured at `trustLevel: "full"`. |
| **Revocation log privacy note normative** | §16.2 | No | RevocationLogEntry minimal field set is now specified normatively. PII-bearing fields are identified; minimal-PII variant defined. |
| **Staleness window defaults normative** | §16.3 | No | Checkpoint interval ≤ 1 hour REQUIRED; offline acceptance window 48 hours REQUIRED maximum; high-value freshness 15 minutes REQUIRED. Previously informative defaults are now normative. |
| **Reference implementation plan** | §2 | No | Reference implementation repository and CI test vector suite added as normative accompaniment. |
| **Appendix H extended** | Appendix H | No | Added test vectors for: Merkle leaf canonicalization, inclusion proof verification, revocation log entry signing (hash-only mode), proofArtifactRef fetch-and-verify flow. |
| **Appendix L: Operational Guidance** | Appendix L | No | New INFORMATIVE appendix with two sections: proofArtifactRef UX decision table (explicit user-facing failure cases for all transport failure modes), and Operator Security Guidance (HSM key ceremonies, DDoS controls, monitoring, incident escalation). |
| **Appendix J normative for Passport-Hardened** | Appendix J, §15.6 | No | Appendix J (Metadata Hardening Profile) is now explicitly required for the Passport-Hardened designation, including application to revocation log queries. |
| **TOC and terminology updated** | TOC, §3 | No | §16.7, §16.8, §16.9, §16.10, §17.7, Appendix L added. `TransactionClass`, `Hash-Only Revocation Entry`, `Merkle Leaf Hash`, `Oracle Quarantine` added to terminology. |

---

## Changelog: v1.6.0 → v1.7.0

| Change | Section | Breaking | Description |
|--------|---------|----------|-------------|
| **HIRI as Integrity Layer** | §18 | No | New normative section establishing the architectural layering principle: HIRI owns integrity, provenance, packaging, and privacy-preserving disclosure; external standards own identity semantics, transport, and discovery. Future extensions MUST respect this boundary. |
| **DID service endpoint formalized** | §6.3 | No | HIRI KeyDocument discovery via DID service endpoint is now formally specified. DID documents MAY include a `HIRIKeyDocument` service type pointing to the holder or issuer KeyDocument. |
| **Identity Anchor registry** | §10.5 | No | New normative subsection formalizing the `identityAnchor` field in KeyDocuments. Defines four anchor types: `domain` (existing DNSSEC/HTTPS mechanism), `government-registry`, `institution`, and `decentralized-network`. Registry-pattern extensible. |
| **Algorithm registry JOSE/COSE cross-references** | §6.5, Appendix E | No | `joseAlgorithmId` and `coseAlgorithmId` fields added to each Signature Algorithm Registry entry. HIRI canonical algorithm IDs (`"ed25519"`, `"p256"`) are unchanged — cross-references are additive metadata for library interoperability. |
| **Appendix K: Standards Interoperability Bridges** | Appendix K | No | New INFORMATIVE appendix defining six interoperability bridges: VC data model mapping (Rec 2), vCard claim schema (Rec 3), OID4VP transport envelope (Rec 5), DIDComm transport envelope (Rec 5), Schema.org/FOAF RDF vocabularies (Rec 6), and a compatibility decision matrix for implementers. |
| **Normative references updated** | §2 | No | OpenID for Verifiable Presentations (OID4VP), DIDComm v2, JOSE (RFC 7517/7518), COSE (RFC 8152), vCard (RFC 6350), Schema.org, FOAF added as normative references for Appendix K. |
| **New terminology** | §3 | No | `Identity Anchor`, `VC Compatibility Envelope`, `Interoperability Bridge` added. |
| **TOC updated** | TOC | No | §18 and Appendix K added to table of contents. |
| **Document history** | Document History | No | v1.7.0 entry added. |

---

## Changelog: v1.5.0 → v1.6.0

| Change | Section | Breaking | Description |
|--------|---------|----------|-------------|
| **Revocation Transparency Log** | §16 | No | New normative section. Issuers MUST publish revocation entries to a signed append-only transparency log. Defines `RevocationLogEntry`, `RevocationCheckpoint`, and the minimal 3-endpoint log API. Verifiers use cached signed checkpoints for offline operation. |
| **Oracle Trust Governance** | §17 | No | New normative section. Oracles MUST publish a `hiri:OracleGovernanceDocument`. Verifiers MUST maintain a configured trusted oracle set. `KeyContinuityAttestations` from unconfigured oracles MUST be treated as `"partial"` trust level. |
| **Phase 3 revocation log check** | §12.4 | No | Phase 3 gains Step 11: check the issuer's revocation transparency log for the attested manifest hash before accepting the credential as valid. Revocation log status added to `SlotVerificationResult`. |
| **Offline verifier decision table** | §12.7 | No | New normative section. Explicit matrix mapping (resource, availability state) → (required action, trust level ceiling). Normative prohibition: `"unknown"` MUST NOT be treated as equivalent to `"active"` or `"valid"` for any resource or check. |
| **KeyDocument REQUIRED for Passport-Interoperable** | §6.4, §15 | No | KeyDocument publication upgrades from SHOULD to MUST for conformance level Passport-Interoperable and above. |
| **proofArtifactRef normative semantics** | §G.7 | No | Timeout (10s), retry policy (3 attempts, exponential backoff starting 1s), caching (by artifactHash, duration = presentation validity window), and explicit failure UX now normative. |
| **Conformance level tightening** | §15 | No | DNSSEC required for Passport-Full org verification. Revocation log integration required for Passport-Full. Algorithm sets made explicit per level. |
| **Metadata Hardening Profile** | Appendix J | No | New OPTIONAL normative appendix. `omittedSlotCount` padding to fixed quantum (nearest 5), timestamp smearing, issuer authority obfuscation in completeness audits. |
| **ZK Proof System Reference** | Appendix I | No | New INFORMATIVE appendix. Use-case to proof system recommendation table with expected sizes and verifier costs. |
| **Normative Test Vectors** | Appendix H | No | New normative appendix. HMAC slot token derivation, P-256 authority encoding, nonce validation boundary cases, revocation log entry signing. |
| **Organizational key recovery guidance** | §13.8 | No | New INFORMATIVE section. Multi-recipient encryption and threshold key escrow patterns for enterprise contexts, using Privacy Extension Mode 2 multi-recipient flow. |
| **New terminology** | §3 | No | `RevocationLogEntry`, `RevocationCheckpoint`, `Revocation Transparency Log`, `OracleGovernanceDocument`, `Oracle Trust Anchor`, `Metadata Hardening Profile` added. |
| **New error codes** | Appendix C | No | `REVOCATION_LOG_ENTRY_FOUND`, `REVOCATION_LOG_STATE_UNKNOWN`, `ORACLE_NOT_IN_TRUST_ANCHORS`, `KEYDOCUMENT_REQUIRED_MISSING` added. |

---

## Changelog: v1.4.0 → v1.5.0

| Change | Section | Breaking | Description |
|--------|---------|----------|-------------|
| **Split nullifier architecture** | §G.2, §G.4, §G.5 | YES | Critical fix: global registry nullifiers (used only at enrollment for double-enrollment detection) are now architecturally separated from context-bound presentation nullifiers (verifierAuthority-scoped, exposed in presentation public inputs). Global nullifiers MUST NOT appear in any presentation. Closes the cross-verifier biometric tracking vulnerability. |
| **Issuer-side biometric revocation protocol** | §G.4.2, §G.4.5 | No | New subsection: when the Biometric Oracle issues a Key Continuity Attestation, it SHOULD notify subscribing Tier 2 issuers via the Oracle Notification Protocol. Notified issuers publish a revocation attestation version. This activates the existing Tier 2 Override mechanism (§12.4) to invalidate stolen-device presentations without requiring verifiers to proactively discover Key Continuity Attestations. |
| **ZK proof transport guidance** | §G.7 | No | New subsection: `proofArtifactRef` (URI + hash commitment) defined as an alternative to inline `proofArtifact` for constrained transports (BLE, NFC, QR). SNARK vs. STARK payload size guidance. Verifier fetch-and-verify flow for out-of-band proof resolution. |
| **Biometric modality mandatory disclosure clarified** | §G.2.3, §G.2.4 | No | Corrected contradiction: `biometricModality` IS a mandatory statement because it is circuit selection metadata required for ZK verification parameter selection. Prose in §G.2.4 updated to distinguish functional metadata (modality) from biometric data (template). |
| **New terminology** | §3 | No | `Registry Nullifier`, `Context-Bound Nullifier`, `Oracle Notification Protocol`, `proofArtifactRef` added. |
| **Document history header restored** | Document History | No | Section header missing from v1.4.0 restored. |

---

## Changelog: v1.3.0 → v1.4.0

| Change | Section | Breaking | Description |
|--------|---------|----------|-------------|
| **Biometric binding appendix** | Appendix G | No | New INFORMATIVE appendix defining three biometric network integration patterns: Sybil resistance via `ProofOfUniqueHumanCredential`, holder-to-credential binding for device-theft resistance, and biometric key recovery. All patterns use ZK commitments — raw biometric data MUST NOT appear in any HIRI artifact. |
| **Credential type registry additions** | §7.5 | No | `ProofOfUniqueHumanCredential` and `BiometricBoundCredential` added to the initial registry with INFORMATIVE notes. |
| **Appendix F cross-reference** | Appendix F.5 | No | Added forward reference to Appendix G for ZK biometric credential types. |
| **Appendix G TOC entry** | TOC | No | Appendix G added. |

---

## Changelog: v1.2.0 → v1.3.0

| Change | Section | Breaking | Description |
|--------|---------|----------|-------------|
| **Proxy Issuance appendix** | Appendix F | No | New INFORMATIVE appendix defining the Proxy Issuer pattern for non-participating authoritative sources, claim atomization for selective disclosure, proxy trust chain structure, and verifier policy mapping. Addresses the cold-start problem for implementers whose credential sources do not operate a native HIRI Organizational Authority. |
| **ZK credential type note** | §7.5, Appendix F.5 | No | Added forward reference to Zero-Knowledge proof-based credential types (ZK Email and equivalents) as a future alternative to proxy issuance for high-privacy cold-start scenarios. |

---

## Changelog: v1.1.0 → v1.2.0

| Change | Section | Breaking | Description |
|--------|---------|----------|-------------|
| **Verifier authority binding in slot tokens** | §11.7.3 | YES | `presentationSlotToken` derivation now includes the verifier's authority string as a third HMAC message field, preventing cross-verifier token relay attacks. |
| **P-256 authority encoding corrected** | §6.5.4, Appendix E.2 | YES | P-256 authority now uses standard `z` multibase prefix (base58btc) with a multicodec varint prefix (`0x80 0x24`, the varint encoding of `0x1200`) prepended to the compressed 33-byte public key. The non-standard `p` multibase prefix from v1.1.0 is removed. |
| **Completeness audit coercion resistance** | §11.5, §14.8 | No | Removed unenforceable normative "MUST NOT require completenessAudit" language from §11.5. Added §14.8 (Coercion Resistance) as a security consideration that acknowledges protocol limits and provides guidance. |
| **Key lifecycle check at presentation verification time** | §12.2 | No | Phase 1 gains a new Step 2a: verifiers MUST check whether the holder's signing key was rotated or revoked after the presentation's `hiri:timing.created` timestamp. If so, the presentation MUST be rejected with `PRESENTATION_KEY_ROTATED_AFTER_CREATION`. |
| **New error code** | Appendix C | No | `PRESENTATION_KEY_ROTATED_AFTER_CREATION` added for the key rotation/floating presentation case. |
| **Updated terminology** | §3 | No | `Verifier Authority Binding` added. |

---

## Changelog: v1.0.0 → v1.1.0

| Change | Section | Breaking | Description |
|--------|---------|----------|-------------|
| **withheldSlots default** | §11.5 | YES | `withheldSlots` is now OPTIONAL and omitted by default. Verifier must explicitly request completeness audit via `completenessAudit: true` in the DisclosureRequest. Default presentations expose only `omittedSlotCount`. |
| **Completeness audit request type** | §11.2 | No | `hiri:DisclosureRequest` gains `completenessAudit` boolean field. |
| **Tier 2 revocation override** | §12.4 | No | Explicit normative rule: if Tier 2 attestation status is `revoked` and Tier 1 slot status is `active`, Tier 2 overrides. Phase 3 algorithm updated. |
| **Credential state synchronization** | §13.7 | No | New INFORMATIVE section: recommended sync cadences, holder UX guidance, conflict presentation recommendations. |
| **Signature algorithm registry** | §6.5 | No | New section. Ed25519 is REQUIRED baseline. P-256 (ECDSA) is OPTIONAL for hardware-backed key compatibility. ML-DSA noted as INFORMATIVE future suite. `signatureAlgorithm` field added to manifest. |
| **Presentation slot blinding** | §11.7 | YES | `slotId` MUST NOT appear raw in Passport Presentations. Presentations use a per-presentation `presentationSlotToken` derived by HMAC-SHA256. Slot blinding key management added. |
| **Nonce encoding normative** | §11.2 | No | Nonce MUST be a base64url-encoded string representing exactly 32 bytes of CSPRNG output. |
| **Slot count limits** | §9.4 | No | New section: normative `slotCount` limits per conformance level. Informative pagination guidance. |
| **New terminology** | §3 | No | `Presentation Slot Token`, `Slot Blinding Key`, `Completeness Audit`, `Signature Algorithm Registry` added. |
| **New error codes** | Appendix C | No | Codes for blinding failures, algorithm registry mismatches, completeness audit conflicts added. |

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Normative References](#2-normative-references)
3. [Terminology](#3-terminology)
4. [Architectural Principles](#4-architectural-principles)
5. [Two-Tier Architecture](#5-two-tier-architecture)
6. [Holder Authority, DID Binding, and Signature Algorithm Registry](#6-holder-authority-did-binding-and-signature-algorithm-registry)
7. [Credential Slots](#7-credential-slots)
8. [Issuer Credential Attestations](#8-issuer-credential-attestations)
9. [Passport Manifest Schema](#9-passport-manifest-schema)
10. [Organizational Authority Bootstrap](#10-organizational-authority-bootstrap)
11. [Passport Presentation Protocol](#11-passport-presentation-protocol)
12. [Verification Algorithm](#12-verification-algorithm)
13. [Passport Lifecycle](#13-passport-lifecycle)
14. [Security Considerations](#14-security-considerations)
15. [Conformance Levels](#15-conformance-levels)
16. [Revocation Transparency](#16-revocation-transparency)
17. [Oracle Trust Governance](#17-oracle-trust-governance)
18. [HIRI as Integrity Layer](#18-hiri-as-integrity-layer)

**Appendices**

- [A: Manifest Examples](#appendix-a-manifest-examples)
- [B: Trust Chain Diagram](#appendix-b-trust-chain-diagram)
- [C: Verification Status Reporting](#appendix-c-verification-status-reporting)
- [D: Privacy Mode Decision Matrix for Credential Slots](#appendix-d-privacy-mode-decision-matrix-for-credential-slots)
- [E: Signature Algorithm Registry (Initial Values)](#appendix-e-signature-algorithm-registry-initial-values)
- [F: Proxy Issuance and Non-Participating Authorities (INFORMATIVE)](#appendix-f-proxy-issuance-and-non-participating-authorities-informative)
- [G: Biometric Network Integration (INFORMATIVE)](#appendix-g-biometric-network-integration-informative)
- [H: Normative Test Vectors](#appendix-h-normative-test-vectors)
- [I: ZK Proof System Reference (INFORMATIVE)](#appendix-i-zk-proof-system-reference-informative)
- [J: Metadata Hardening Profile (OPTIONAL normative)](#appendix-j-metadata-hardening-profile-optional-normative)
- [K: Standards Interoperability Bridges (INFORMATIVE)](#appendix-k-standards-interoperability-bridges-informative)
- [L: Operational Guidance (INFORMATIVE)](#appendix-l-operational-guidance-informative)
- [M: OracleGovernanceDocument Template (INFORMATIVE)](#appendix-m-oraclegovernancedocument-template-informative)
- [N: Migration Guidance (INFORMATIVE)](#appendix-n-migration-guidance-informative)

---

## 1. Introduction

### 1.1 Purpose

The HIRI Digital Passport Extension defines a specification for **portable, holder-sovereign credential portfolios**. A Digital Passport is a HIRI artifact that a holder (a natural person, an organization, or a synthetic moral person — see §4.5) publishes under their own signing authority. It aggregates credentials issued by third parties as HIRI Attestation Manifests (Privacy Extension §10), controls the disclosure of those credentials using HIRI privacy modes, and enables verifiers to confirm the authenticity of both the holder's identity and each issuing organization without relying on any centralized registry or platform.

The Digital Passport is the HIRI formalization of the pattern described in the Sarah Thompson use case: a cryptographically signed, portable, independently verifiable identity portfolio that the holder owns.

### 1.2 Scope

This specification defines:

- The `hiri:PassportManifest` artifact type and its required fields
- Credential slots: the mechanism for aggregating and managing credential references
- Per-slot privacy mode declaration (Proof of Possession, Selective Disclosure, Public)
- Issuer credential attestation structure (Mode 5 composition)
- Organizational authority bootstrap via `did:web` domain binding
- Passport presentation: selective credential disclosure to a named verifier
- Presentation slot blinding: per-presentation slot identifier unlinkability
- Signature algorithm registry: Ed25519 baseline with extensible algorithm support
- Verification algorithm: the four-step chain from passport manifest to organizational identity
- Credential state synchronization: holder and verifier guidance for revocation detection
- Passport lifecycle: creation, credential addition, credential revocation, key rotation

This specification does NOT define:

- Transport mechanisms for passport resolution (see HIRI-IPFS Integration Specification)
- Authorization policies governing which verifiers may request which credentials
- Biometric binding or government identity enrollment
- Cross-jurisdictional legal recognition of passport credentials

### 1.3 Relationship to HIRI Protocol v3.1.1 and Privacy Extension v1.4.1

Every `hiri:PassportManifest` is a valid v3.1.1 `hiri:ResolutionManifest` with additional fields. A v3.1.1 verifier that does not implement this extension MUST be able to verify the signature and chain integrity of any passport manifest, even if it cannot interpret the `hiri:passport` block. Unrecognized fields are ignored per v3.1.1 §4.4.

The passport's privacy behavior is governed entirely by Privacy Extension v1.4.1. This extension does not define new cryptographic mechanisms — it defines how the existing five privacy modes are mapped onto credential slots within a passport, and adds the presentation-layer blinding mechanism described in §11.7.

### 1.4 Normative Interpretation Rule

Inherited from HIRI Protocol v3.1.1 §1.3. Any algorithm, table, code block, or prose that describes verification, credential resolution, presentation generation, blinding, or acceptance/rejection criteria SHALL be interpreted as normative unless explicitly marked INFORMATIVE or OPTIONAL.

### 1.5 Release Candidate Sign-Off Checklist

v1.9.0 is a **Release Candidate**. It is normatively stable and suitable for implementation and pilot deployments. It MUST NOT be declared a full release or recommended for general production adoption until all six items in the following checklist are verified and documented.

| # | Item | Blocking? | Verification Evidence |
|---|------|-----------|----------------------|
| 1 | Reference implementation repository published at `https://github.com/hiri-protocol/passport-reference`, tagged `v1.9.0`, CI pipeline green against all Appendix H vectors | **Blocking** | CI badge URL + passing test run link |
| 2 | Independent interoperability test completed: at least two independent implementations (e.g., Node/WASM + Go) pass all §H.9 matrix test cases; results documented in §H.9 | **Blocking** | Populated §H.9 interoperability results table |
| 3 | At least one production Revocation Transparency Log operator has completed the Appendix L.2.4 operator checklist, verified mTLS/JWT append auth, HSM-backed signing, and checkpoint automation under load, and published their governance document | **Blocking** | Operator governance document URI + L.2.4 completion attestation |
| 4 | At least one biometric oracle authority has published an OracleGovernanceDocument conforming to §17.2 and Appendix M template, completed a recovery drill (§17.7.4), and published an OracleRecoveryNotice from the drill | **Blocking** | Oracle governance doc URI + recovery drill report |
| 5 | Appendix C machine-readable status mapping verified: all status codes in the normative staleness table (§C.2) are exercised by the reference implementation test suite and produce the expected codes | **Blocking** | CI test output demonstrating each status code path |
| 6 | Appendix J (Metadata Hardening) requirements included in Passport-Hardened CI test run; §H.10 test vectors pass; §15.6 Passport-Hardened summary reviewed and accepted by security SME | **Blocking** | Signed SME acceptance note + CI results |

**Status as of v1.9.0 publication:** All items are PENDING. This checklist MUST be reviewed and marked complete before the Release Steward signs off. Use the sign-off blurb below when all items are verified:

> *"I hereby approve HIRI Digital Passport Extension v1.9.0 for full release, conditional on publication of the normative reference implementation and passing of the Appendix H interoperability test suite having been completed. The specification's normative changes (revocation transparency canonicalization, hardened /append authentication, and staleness windows) materially improve security and interoperability. All items in the §1.5 sign-off checklist have been verified." — [NAME], Release Steward, [DATE]*

---

## 2. Normative References

| Specification | Usage |
|---------------|-------|
| HIRI Protocol Specification v3.1.1 | Base protocol (signing, verification, chain integrity, key lifecycle) |
| HIRI Privacy & Confidentiality Extension v1.4.1 | Privacy modes (Mode 1–5) |
| W3C Decentralized Identifiers (DIDs) v1.0 | DID binding for holder and issuer authority |
| W3C Verifiable Credentials Data Model v2.0 | VC compatibility envelope (Appendix K.2) |
| RFC 8032 | Ed25519 digital signatures (REQUIRED baseline) |
| RFC 6979 | Deterministic ECDSA — required when P-256 is implemented |
| RFC 7517 / RFC 7518 | JSON Web Key / JSON Web Algorithms (JOSE) — algorithm cross-reference (§6.5, Appendix E) |
| RFC 8152 | CBOR Object Signing and Encryption (COSE) — algorithm cross-reference (§6.5, Appendix E) |
| RFC 8785 | JSON Canonicalization Scheme (JCS) |
| RFC 6350 | vCard Format Specification — optional claim schema (Appendix K.3) |
| W3C RDF Dataset Canonicalization | URDNA2015 algorithm |
| RFC 2104 | HMAC construction — used in presentation slot blinding (§11.7) |
| RFC 5869 | HKDF — used in slot blinding key derivation (§11.7.3) |
| DNSSEC (RFC 4033–4035) | Organizational domain verification (RECOMMENDED) |
| FIPS 204 (ML-DSA) | Post-quantum digital signatures — INFORMATIVE, future suite |
| OpenID for Verifiable Presentations (OID4VP) | Transport envelope for HIRI presentations (Appendix K.4, INFORMATIVE) |
| DIDComm Messaging v2.0 | Alternative transport envelope (Appendix K.5, INFORMATIVE) |
| Schema.org | Optional RDF vocabulary for identity claims (Appendix K.6, INFORMATIVE) |
| FOAF Vocabulary Specification | Optional RDF vocabulary for person identity (Appendix K.6, INFORMATIVE) |
| HIRI Passport Reference Implementation | **Normative accompaniment.** Repository: `https://github.com/hiri-protocol/passport-reference` — tag `v1.9.0`. Includes: resolver, verifier, issuer log server, and CI test harness covering all Appendix H vectors. Conformance claims at Passport-Interoperable or above MUST be validated against this suite. CI status: ![CI](https://github.com/hiri-protocol/passport-reference/actions/workflows/ci.yml/badge.svg?branch=v1.9.0) *(badge will be live upon repository publication)* |

---

## 3. Terminology

| Term | Definition |
|------|------------|
| Holder | The entity who owns and controls the passport. The holder's signing keypair (§6.5) is the passport authority. |
| Issuer | An organization or authority that issues credentials to a holder. The issuer's HIRI authority signs Credential Attestation Manifests. |
| Verifier | An entity that requests and verifies a subset of credentials from the holder's passport. |
| Passport Manifest | A `hiri:PassportManifest` artifact published under the holder's authority, aggregating credential slots. |
| Credential Slot | A named entry in the passport that references one Credential Attestation Manifest and declares its privacy mode. |
| Credential Attestation Manifest | A `hiri:AttestationManifest` (Privacy Extension §10) published by the issuer, asserting a specific claim about the holder. |
| Passport Presentation | A signed artifact produced by the holder for a specific verifier, containing selectively disclosed credential slots. |
| Organizational Authority | A HIRI authority whose KeyDocument is bound to a verified domain (§10). |
| Holder Content | The RDF graph payload of the Passport Manifest: the `hiri:passport` block serialized as JSON-LD. |
| Disclosure Request | A signed request by a verifier to the holder specifying which credential slots they require. |
| Slot Privacy Mode | The Privacy Extension mode declared for a specific credential slot. Valid values: `proof-of-possession`, `selective-disclosure`, `public`. |
| **Slot Blinding Key** | A per-passport, holder-held secret (32 bytes) used to derive presentation slot tokens. MUST NOT be published. |
| **Presentation Slot Token** | A per-presentation, blinded identifier derived from a `slotId` and a request nonce. Exposed in presentations instead of the raw `slotId`. |
| **Completeness Audit** | An explicit verifier request for a full accounting of slot existence in a passport. MUST NOT be inferred from a default presentation. |
| **Signature Algorithm Registry** | A holder- and issuer-maintained registry mapping algorithm identifiers to key types, canonicalization requirements, and proof value encoding rules. |
| **Tier 2 Override** | The normative rule that a Tier 2 (issuer-signed) revocation of an attestation supersedes the Tier 1 (holder-declared) slot status when they conflict. |
| **Verifier Authority Binding** | The cryptographic inclusion of the verifier's authority string in the presentation slot token derivation, preventing a cross-verifier token relay attack where a verifier forwards another verifier's nonce to obtain a token that would be valid in that verifier's context. |
| **Registry Nullifier** | A globally deterministic, biometric-derived value used exclusively by the Biometric Network to detect double-enrollment. Computed as `H(biometric_secret \|\| "registry-v1")`. MUST NOT appear in any Passport Presentation or be disclosed to any verifier. See §G.2. |
| **Context-Bound Nullifier** | A per-verifier, biometric-derived value exposed in presentation public inputs, computed as `H(biometric_secret \|\| verifierAuthority)`. Proves uniqueness within a specific verifier's context without enabling cross-verifier correlation. |
| **Oracle Notification Protocol** | An application-layer protocol by which the Biometric Recovery Oracle notifies subscribing Tier 2 issuers when a Key Continuity Attestation is issued for a holder, enabling those issuers to publish revocation attestations for the superseded authority. See §G.4.5. |
| **proofArtifactRef** | A reference structure (`uri` + `artifactHash`) that allows a ZK proof artifact to be resolved out-of-band rather than inlined in the presentation payload. Used for constrained transports (BLE, NFC, QR) where ZK proof byte size would exceed transport limits. See §G.7. |
| **Revocation Transparency Log** | An append-only, publicly auditable log operated by an issuer or shared log service to which issuers MUST append `RevocationLogEntry` records when revoking a credential. Verifiers use signed checkpoints from the log to efficiently discover revocations without walking full attestation chains. See §16. |
| **RevocationLogEntry** | A signed record appended to a Revocation Transparency Log by an issuer, declaring that a specific manifest version of a Credential Attestation Manifest is revoked. See §16.2. |
| **RevocationCheckpoint** | A signed tree head (Merkle root + tree size + timestamp) produced by a Revocation Transparency Log at periodic intervals. Verifiers cache checkpoints for offline revocation state verification. See §16.3. |
| **OracleGovernanceDocument** | A published document declaring the governance, accountability, key management policy, jurisdiction, and transparency log endpoint of a Biometric Oracle authority. Required for oracle authorities claiming any trust level above `"partial"`. See §17. |
| **Oracle Trust Anchor** | An entry in a verifier's configured trusted oracle set, mapping an oracle authority to its governance document URI and accepted trust level. `KeyContinuityAttestations` from authorities not in the trust anchor set MUST be treated as `"partial"`. See §17.3. |
| **Metadata Hardening Profile** | An OPTIONAL normative profile (Appendix J) specifying additional privacy protections: `omittedSlotCount` padding, timestamp smearing, and issuer authority obfuscation in completeness audit responses. |
| **Identity Anchor** | A verifiable proof connecting a HIRI authority to a real-world control point (domain, government registry, institution, or decentralized network). Declared in the authority's KeyDocument as an `identityAnchor` block. See §10.5. |
| **VC Compatibility Envelope** | An OPTIONAL `VerifiableCredential` wrapper around a HIRI Credential Attestation Manifest, enabling compatibility with W3C VC ecosystem tooling. HIRI's signing and verification remain the canonical verification path. See Appendix K.2. |
| **Interoperability Bridge** | An OPTIONAL translation layer between a HIRI protocol element and an external standard (VC data model, OID4VP, DIDComm, vCard, Schema.org/FOAF). Bridges are additive — they do not modify HIRI's core signing, verification, or privacy mechanisms. See Appendix K. |
| **TransactionClass** | A verifier-declared classification of a verification request as `"standard"` or `"high-value"`, determining the maximum acceptable checkpoint age for revocation log state determination. See §16.9. |
| **Hash-Only Revocation Entry** | A privacy-preserving revocation log entry that stores only `SHA-256(JCS(fullEntry))` rather than the plaintext entry, preventing public log observers from inferring the existence of sensitive credential types. See §16.8. |
| **Merkle Leaf Hash** | The leaf node value in the Revocation Transparency Log Merkle tree: `SHA-256(JCS(RevocationLogEntry))`. See §16.10. |
| **Oracle Quarantine** | A verifier state in which all attestations from a specific oracle authority are downgraded to `"partial"` trust level pending governance re-affirmation, triggered by a detected oracle incident. See §17.7. |
| **Release Candidate** | The status of v1.9.0. A Release Candidate is feature-complete and normatively stable but may not be declared a full release until all items in the sign-off checklist (§1.5) are verified. |
| **Sign-Off Checklist** | The six blocking conditions defined in §1.5 that must all be satisfied before v1.9.0 may be declared a full release and recommended for general production adoption. |
| **Interoperability Test Matrix** | The structured test results table defined in §H.9 that documents which test vectors pass across which independent implementations, required as a normative accompaniment to the reference implementation. |

---

## 4. Architectural Principles

### 4.1 Holder Sovereignty

The holder's signing keypair IS the passport (see §6.5 for algorithm options). No registry, platform, or third party mediates the holder's identity. The passport URI is derived deterministically from the holder's public key (§6), and the holder's signature is the root of trust for the entire credential portfolio.

**Invariant:** A passport can be created, versioned, and verified with no dependencies beyond the HIRI kernel and the holder's keypair. No enrollment, no account creation, no platform permission.

### 4.2 Issuers Do Not Own Credentials

Credentials are issued as Attestation Manifests signed by the issuer's authority. The issuer's signature proves the credential is authentic. But the holder controls which credentials are aggregated into their passport, which credentials are disclosed in any given presentation, and when to rotate or replace their passport key.

The issuer cannot revoke the holder's right to hold a credential — they can only revoke the attestation's validity claim (§13.4), which a verifier will detect when checking the attestation chain (Tier 2 override, §12.4).

### 4.3 Edge-Canonical Verification

Inherited from HIRI Protocol §4.1. All passport verification — signature verification, chain integrity, credential attestation verification, organizational authority bootstrap — MUST be performable locally with no network round-trips. The verifier fetches manifest bundles from the content-addressed network and then verifies entirely locally.

**Invariant:** Passport verification MUST NOT require a call to any centralized API, identity provider, or registry at verification time.

### 4.4 Privacy Is Per-Slot

Each credential slot independently declares its privacy mode. A passport may contain slots in `proof-of-possession` mode (credential existence provable, content withheld), `selective-disclosure` mode (specific RDF statements disclosable on demand), and `public` mode (credential content fully visible). A single presentation may include slots from any combination of these modes.

### 4.5 Publisher Neutrality

Inherited from Privacy Extension §4.6. A passport holder MAY be a human individual, an organization, or a synthetic moral person. The cryptographic mechanisms are indifferent to the holder's substrate. An autonomous agent whose credential portfolio constitutes its institutional identity has the same technical basis for passport sovereignty as a human professional. Whether non-human holders deserve the legal recognition associated with passport credentials is a governance question, not a protocol question.

### 4.6 Separation of Authentication and Authorization

The passport proves **who the holder is** and **what credentials they hold**. It does NOT prove that the holder is authorized to take any specific action. Authorization decisions are application-layer policies that consume passport verification results as inputs. This specification does not define authorization policies.

### 4.7 Minimum Disclosure Surface

**A Passport Presentation MUST disclose only what the verifier explicitly requested.**

This principle governs the default behavior of the Presentation Protocol (§11). A verifier who requests an `EmploymentCredential` is entitled to know about the employment credential. They are NOT entitled, by default, to know how many other credentials the holder possesses, what types they are, or that a `GovernmentIdVerification` or `BackgroundCheckClearance` exists in the portfolio. Such knowledge — even as hashes or existence proofs — constitutes unrequested metadata that enables correlation and profiling.

**Invariant:** The default passport presentation MUST NOT cause the holder to disclose the existence of credentials beyond those explicitly requested by the verifier. Completeness transparency is an opt-in mechanism (§11.5), not a default.

---

## 5. Two-Tier Architecture

A HIRI Digital Passport consists of two artifact tiers:

```
Tier 1: Passport Manifest (holder-signed)
  ├── hiri:passport block
  │     ├── holder metadata (DID binding, display name)
  │     ├── Credential Slot 1 → ref → Tier 2: Credential Attestation Manifest (issuer-signed)
  │     ├── Credential Slot 2 → ref → Tier 2: Credential Attestation Manifest (issuer-signed)
  │     └── Credential Slot N → ref → Tier 2: Credential Attestation Manifest (issuer-signed)
  └── hiri:signature (holder's signing key over the passport manifest)

Tier 2: Credential Attestation Manifests (per credential, issuer-signed)
  ├── hiri:AttestationManifest (Privacy Extension §10)
  │     ├── hiri:attestation.subject → holder's passport manifest hash
  │     ├── hiri:attestation.claim  → the credential claim
  │     └── hiri:signature          → issuer's signing key
  └── (optional) hiri:content block for Mode 3 selective disclosure
```

### 5.1 Separation of Concerns

The Tier 1 Passport Manifest is the holder's artifact. The Tier 2 Credential Attestation Manifests are the issuers' artifacts.

**NORMATIVE:** The holder MUST NOT sign Tier 2 manifests. The issuer MUST NOT sign Tier 1 manifests. Cross-tier signing is a verification error.

### 5.2 Reference Integrity

A credential slot's `attestationRef` pins the specific manifest version the holder is presenting:

```json
{
  "attestationRef": {
    "authority": "key:ed25519:z<issuer-authority>",
    "manifestHash": "sha256:e08da327...",
    "manifestVersion": "3"
  }
}
```

If the issuer publishes a new version of the attestation (e.g., refreshed validity claim), the holder MUST update the slot's `attestationRef` in a new passport version. The old reference remains verifiable — the issuer's chain preserves all versions.

### 5.3 Tier 2 Override

Tier 2 is authoritative for credential validity. If the holder's Tier 1 slot status conflicts with the issuer's Tier 2 attestation status, Tier 2 governs. The specific override rules are defined in §12.4 (Phase 3 algorithm) and summarized here for architectural clarity:

| Tier 1 `status` | Tier 2 attestation status | Effective Status |
|-----------------|--------------------------|------------------|
| `active` | `valid` | Active |
| `active` | `revoked` | **Revoked** (Tier 2 overrides) |
| `active` | `stale` | Active with staleness warning |
| `revoked` | any | Revoked |
| `expired` | any | Expired |

---

## 6. Holder Authority, DID Binding, and Signature Algorithm Registry

### 6.1 Holder Authority Derivation

The holder's passport authority is derived from their signing public key using the HIRI authority derivation algorithm (v3.1.1 §5.1.1). For the REQUIRED baseline algorithm (Ed25519):

```
holderAuthority = "key:ed25519:" + base58btc(holderPublicKey)
```

For OPTIONAL algorithms defined in §6.5, the authority string uses the algorithm-specific prefix defined in the Signature Algorithm Registry.

### 6.2 Passport URI

```
hiri://<holderAuthority>/passport/main
```

Example (Ed25519):
```
hiri://key:ed25519:z6MkSarah123.../passport/main
```

Example (P-256):
```
hiri://key:p256:z<multicodec-base58btc-P256-key>/passport/main
```

The `main` branch is the canonical passport branch. Holders MAY publish additional branches for specific contexts (e.g., `professional`, `academic`), but `main` is the REQUIRED default.

### 6.3 DID Binding

The holder's HIRI authority MAY be bound to a W3C DID. The RECOMMENDED binding for Ed25519 keys is `did:key`, derived from the holder's Ed25519 public key using the `did:key` specification for Ed25519:

```
holderDID = "did:key:" + base58btc(multicodec(0xed01, holderPublicKey))
```

For P-256 keys, the `did:key` multicodec prefix is `0x1200`, whose varint encoding (`0x80 0x24`) is prepended to the compressed 33-byte public key before base58btc encoding.

**Relationship invariant:** The holder's HIRI authority and their `did:key` DID are derived from the same public key bytes. Either form can be converted to the other deterministically.

**DID service endpoint for KeyDocument discovery:** When a holder or issuer publishes a DID document (via `did:key`, `did:web`, or any other DID method), they SHOULD include a `HIRIKeyDocument` service endpoint to enable DID-aware resolvers to discover the HIRI KeyDocument:

```json
{
  "@context": ["https://www.w3.org/ns/did/v1"],
  "id": "did:web:ecoimpact.com",
  "verificationMethod": [
    {
      "id": "did:web:ecoimpact.com#key-main",
      "type": "Ed25519VerificationKey2020",
      "controller": "did:web:ecoimpact.com",
      "publicKeyMultibase": "z<base58btc-encoded-public-key>"
    }
  ],
  "service": [
    {
      "id": "did:web:ecoimpact.com#hiri-keydoc",
      "type": "HIRIKeyDocument",
      "serviceEndpoint": "https://ecoimpact.com/.well-known/hiri-key.json"
    }
  ],
  "hiriAuthority": "key:ed25519:z<issuer-authority>"
}
```

The `HIRIKeyDocument` service type is registered by this specification. Resolvers encountering a DID document with this service type MAY fetch the referenced KeyDocument to obtain HIRI-specific key lifecycle and organizational identity information.

**Mapping invariant:** The `publicKeyMultibase` in the DID document `verificationMethod` and the public key encoded in `hiriAuthority` MUST be derived from the same raw key bytes. A verifier detecting an inconsistency MUST report it and reduce the organizational trust level to `"key-only"` or lower.

### 6.4 KeyDocument Publication

Holders and issuers at Passport-Core conformance level SHOULD publish a KeyDocument (v3.1.1 §13) for their authority.

**NORMATIVE for Passport-Interoperable and Passport-Full:** Holders and issuers claiming conformance at Passport-Interoperable or Passport-Full MUST publish a KeyDocument at:

```
hiri://<authority>/key/main
```

The KeyDocument MUST be resolvable at the time of any credential issuance and MUST remain resolvable for the duration of the authority's operational lifetime plus a minimum retention period of 90 days after the authority's last active credential expires or is revoked. Verifiers at Passport-Interoperable or above MUST attempt KeyDocument resolution during Phase 1 and Phase 3 verification and MUST follow the offline decision table (§12.7) when resolution fails.

**Caching and TTL:** Verifiers SHOULD cache KeyDocuments. The RECOMMENDED cache TTL is 24 hours. Cached KeyDocuments MUST be refreshed before the TTL expires when the verifier is online. Verifiers MUST NOT use a cached KeyDocument whose TTL has expired when online resolution is available — stale cache hits are only acceptable under the conditions defined in §12.7.

**Offline resolver behavior:** When KeyDocument resolution fails because the network is unreachable, verifiers MUST follow the offline decision table (§12.7). Specifically: if a valid cached KeyDocument exists within its TTL (24 hours), use it with a `"cached-key-document"` warning and cap trust at `"partial"`. If the cache is expired or absent, report `keyStatus: "unknown"` and cap trust at `"partial"`. Under no circumstances may KeyDocument unavailability be treated as a passing state. See §12.7 for the complete normative decision table.

### 6.5 Signature Algorithm Registry

This section defines the Passport Signature Algorithm Registry. Implementations dispatch signing and verification through a registry, not through hardcoded algorithm calls. This enables cryptographic agility without protocol revision.

#### 6.5.1 Registry Interface

```typescript
interface SignatureAlgorithm {
  readonly algorithmId: string;
  readonly authorityPrefix: string;
  readonly proofType: string;
  readonly keyLength: number;

  sign(
    canonicalBytes: Uint8Array,
    privateKey: Uint8Array
  ): Promise<Uint8Array>;

  verify(
    canonicalBytes: Uint8Array,
    publicKey: Uint8Array,
    signature: Uint8Array
  ): Promise<boolean>;

  encodeAuthority(publicKey: Uint8Array): string;
  decodeAuthority(authorityString: string): Uint8Array;
  encodeProofValue(signatureBytes: Uint8Array): string;
  decodeProofValue(proofValue: string): Uint8Array;
}

interface SignatureAlgorithmRegistry {
  register(algorithm: SignatureAlgorithm): void;
  resolve(algorithmId: string): SignatureAlgorithm;
  resolveByAuthority(authorityString: string): SignatureAlgorithm;
}
```

#### 6.5.2 Registered Algorithms (v1.7.0)

| Algorithm ID | Key Type | Proof Type | JOSE ID | COSE ID | Status | Notes |
|--------------|----------|------------|---------|---------|--------|-------|
| `ed25519` | Ed25519 (32 bytes) | `Ed25519Signature2020` | `EdDSA` | `-8` | **REQUIRED** | Baseline interoperability. Mandatory for all conformance levels. |
| `p256` | P-256 / secp256r1 (65 bytes, uncompressed) | `EcdsaSecp256r1Signature2019` | `ES256` | `-7` | **OPTIONAL** | For hardware-backed keys. Deterministic ECDSA per RFC 6979 REQUIRED. |
| `ml-dsa-65` | ML-DSA (FIPS 204) | `MLDSASignature2025` | TBD | TBD | **INFORMATIVE** | Post-quantum. Not yet normative. |

The `JOSE ID` and `COSE ID` columns are cross-reference metadata for library interoperability. They identify the equivalent algorithm in JOSE (RFC 7518) and COSE (RFC 8152) registries. These identifiers MUST NOT be used as HIRI `algorithm` field values — use the HIRI Algorithm ID (first column) in all manifest and presentation `hiri:signature.algorithm` fields.

**Implementation guidance:** Cryptographic libraries that accept JOSE or COSE algorithm identifiers can be mapped to HIRI signing operations using this table. A JOSE library configured with `"EdDSA"` produces signatures compatible with the HIRI `"ed25519"` algorithm; a COSE library using algorithm `-7` produces signatures compatible with HIRI `"p256"`. The HIRI Signature Algorithm Registry dispatches based on its own IDs; the JOSE/COSE columns enable library integration without introducing a second registry lookup path.

#### 6.5.3 Algorithm Declaration in Manifests

Every manifest and presentation MUST declare the signing algorithm in the `hiri:signature` block:

```json
{
  "hiri:signature": {
    "type": "Ed25519Signature2020",
    "algorithm": "ed25519",
    "canonicalization": "URDNA2015",
    "created": "2026-03-15T10:00:00Z",
    "verificationMethod": "hiri://key:ed25519:z<authority>/key/main#key-1",
    "proofPurpose": "assertionMethod",
    "proofValue": "z..."
  }
}
```

The `algorithm` field MUST match a registered algorithm ID. Verifiers MUST reject a manifest whose `algorithm` is not in their registry. Verifiers SHOULD emit `SIGNATURE_ALGORITHM_UNSUPPORTED` (Appendix C) rather than a generic signature failure when the algorithm is unrecognized.

#### 6.5.4 P-256 Authority Encoding

P-256 authority strings use the standard multibase `z` prefix (base58btc), with a multicodec varint prepended to the raw key bytes before encoding. This is identical in structure to Ed25519 authority derivation, differing only in the multicodec identifier and key representation.

**Multicodec identifier for P-256 public keys:** `0x1200` (the registered multicodec identifier for secp256r1/P-256 public keys). Its unsigned varint encoding is the two-byte sequence `0x80 0x24`.

**Key representation:** P-256 public keys MUST be encoded in **compressed** form: 33 bytes (`0x02` or `0x03` prefix byte indicating the Y-coordinate sign, followed by the 32-byte X-coordinate). Uncompressed 65-byte representations MUST NOT be used.

**Authority derivation:**

```
multicodecPrefix = [0x80, 0x24]                          // varint(0x1200)
compressedKey    = compressPoint(rawP256PublicKey)        // 33 bytes
keyBytes         = concat(multicodecPrefix, compressedKey) // 35 bytes total
authority        = "key:p256:z" + base58btc(keyBytes)
```

**Verification:**

```javascript
function deriveP256Authority(compressedPublicKey) {
  if (compressedPublicKey.length !== 33) throw new Error('Expected compressed P-256 key (33 bytes)');
  const prefix = new Uint8Array([0x80, 0x24]);
  const keyBytes = concat(prefix, compressedPublicKey);
  return 'key:p256:z' + base58btc.encode(keyBytes); // 'z' is the standard multibase base58btc prefix
}

function extractP256PublicKey(authority) {
  const match = authority.match(/^key:p256:(z[A-Za-z0-9]+)$/);
  if (!match) throw new Error('Invalid P-256 authority format');
  const keyBytes = base58btc.decode(match[1]);     // standard multibase decode; 'z' handled by library
  if (keyBytes[0] !== 0x80 || keyBytes[1] !== 0x24) throw new Error('Invalid P-256 multicodec prefix');
  return keyBytes.slice(2);                         // 33-byte compressed public key
}
```

**Rationale:** The v1.1.0 draft incorrectly used a non-standard `p` multibase prefix to indicate the P-256 algorithm. The W3C Multibase specification defines prefix characters to mean base-encoding schemes (e.g., `z` = base58btc), not cryptographic algorithms. Algorithm identification is the responsibility of Multicodec — the byte-level prefix prepended to the key material before base encoding. This correction restores compliance with both specifications and ensures that standard multiformat parsing libraries can decode P-256 authority strings without special-case logic.

#### 6.5.5 Cross-Algorithm Issuer and Holder Compatibility

A passport holder using Ed25519 MAY hold credential attestations signed by an issuer using P-256, and vice versa. Algorithm choice is per-authority. The verifier MUST dispatch each signature verification through the algorithm registered for that authority's algorithm prefix.

**NORMATIVE:** A Passport Manifest MUST be signed with the holder's primary signing algorithm. A verifier MUST NOT accept a passport manifest signed with an algorithm different from the one declared in the holder's KeyDocument `activeKeys` entry for the signing key.

---

## 7. Credential Slots

### 7.1 Purpose

A credential slot is a named entry in the `hiri:passport.credentialSlots` array. Each slot:

1. Identifies a credential by type and display label
2. Pins a specific Credential Attestation Manifest by authority and manifest hash
3. Declares the slot's privacy mode
4. Optionally specifies a disclosure policy

### 7.2 Slot Structure

```json
{
  "slotId": "slot:employment-ecoimpact-2026",
  "credentialType": "EmploymentCredential",
  "displayLabel": "Environmental Scientist — EcoImpact Consulting",
  "privacyMode": "selective-disclosure",
  "attestationRef": {
    "authority": "key:ed25519:z<ecoimpact-authority>",
    "manifestHash": "sha256:e08da327...",
    "manifestVersion": "4"
  },
  "disclosurePolicy": {
    "defaultDisclosure": "label-only",
    "fullDisclosureRequires": "holder-approval"
  },
  "validFrom": "2024-03-01T00:00:00Z",
  "validUntil": "2027-03-01T00:00:00Z",
  "status": "active"
}
```

### 7.3 Slot Field Semantics

**`slotId`** — REQUIRED. A stable, unique identifier for this slot within the passport. Format: `slot:<semantic-label>`. MUST be stable across passport versions — the same credential MUST retain the same `slotId` across Tier 1 updates.

**`slotId` in presentations:** The raw `slotId` MUST NOT appear in Passport Presentations. Presentations use a per-presentation `presentationSlotToken` derived from the `slotId` and the request nonce (§11.7). This ensures that the stable internal identifier cannot be used by colluding verifiers as a cross-presentation tracking vector.

**`credentialType`** — REQUIRED. A machine-readable credential type identifier from the HIRI Passport Credential Type Registry (§7.5) or a fully qualified IRI for domain-specific types.

**`displayLabel`** — REQUIRED. A human-readable label for the credential. MUST NOT contain sensitive information — the display label is visible in `proof-of-possession` and `selective-disclosure` manifests regardless of content visibility.

**`privacyMode`** — REQUIRED. One of: `proof-of-possession`, `selective-disclosure`, `public`. See §7.4.

**`attestationRef`** — REQUIRED. Cryptographic reference to the Credential Attestation Manifest. Contains:
- `authority` — the issuer's HIRI authority string
- `manifestHash` — the specific manifest version hash (raw-sha256 or CIDv1)
- `manifestVersion` — the manifest version string (per v3.1.1 §11.3, always a JSON String)

**`disclosurePolicy`** — OPTIONAL. Application-layer guidance for verifiers and holders. Not cryptographically enforced by the protocol. Values:
- `defaultDisclosure` — what is disclosed in a default presentation. Values: `"label-only"`, `"summary"`, `"full"`
- `fullDisclosureRequires` — condition for full disclosure. Values: `"holder-approval"`, `"always"`, `"never"`

**`validFrom` / `validUntil`** — OPTIONAL. ISO 8601 timestamps indicating the credential's validity window as declared by the holder. These are holder assertions — the issuer's attestation `validUntil` field governs under the Tier 2 Override rule (§5.3).

**`status`** — REQUIRED. One of: `"active"`, `"revoked"`, `"expired"`, `"suspended"`. A holder MAY mark a slot as `"revoked"` or `"expired"` without removing it, preserving the audit trail. Verifiers MUST surface the slot status. The Tier 2 Override rule (§5.3) applies where Tier 1 and Tier 2 statuses conflict.

### 7.4 Privacy Mode Per Slot

| Slot `privacyMode` | Attestation Manifest Mode | Content Visible? | Existence Provable? |
|--------------------|--------------------------|------------------|---------------------|
| `proof-of-possession` | Privacy Extension Mode 1 | No | Yes (via manifest hash) |
| `selective-disclosure` | Privacy Extension Mode 3 | Partially (disclosed statements only) | Yes |
| `public` | Privacy Extension Mode `public` (no privacy block) | Yes (full plaintext) | Yes |

**NORMATIVE:** The `privacyMode` declared in the slot MUST match the mode declared in the referenced Credential Attestation Manifest's `hiri:privacy.mode` field. A verifier MUST reject a slot where these values are inconsistent.

### 7.5 Credential Type Registry (Initial Values)

| Type | Description |
|------|-------------|
| `EmploymentCredential` | Current or past employment at an organization |
| `EducationCredential` | Academic degree, diploma, or certificate |
| `ProfessionalCertification` | Issued professional certification or license |
| `GovernmentIdVerification` | Proof of government identity verification (content typically Mode 1) |
| `BackgroundCheckClearance` | Security or background clearance (content typically Mode 1) |
| `MembershipCredential` | Membership in a professional association or organization |
| `EndorsementCredential` | Peer or professional endorsement |
| `PublicationRecord` | Authorship or publication attribution |
| `SyntheticMoralPersonStatus` | Governance status for non-human agents (see §4.5) |
| `ProofOfUniqueHumanCredential` | Sybil-resistance attestation issued by a decentralized biometric or social-graph network, asserting that this HIRI authority corresponds to exactly one biological human not registered under any other authority. Content is a ZK uniqueness proof — raw biometric data MUST NOT appear in this credential. See Appendix G.2. |
| `BiometricBoundCredential` | A credential whose Tier 2 claim payload includes a ZK biometric commitment, enabling high-assurance holders to prove live physical possession at presentation time without disclosing biometric data to the verifier. Typically wraps a `GovernmentIdVerification` or similar high-value credential. See Appendix G.3. |

Implementers MAY define additional credential types using fully qualified IRIs for domain-specific claims not covered by the registry above.

**Forward reference — Zero-Knowledge credential types:** For cold-start scenarios where a holder must prove domain affiliation or attribute possession without a participating issuer, future credential types based on Zero-Knowledge proofs (e.g., ZK Email domain proofs, ZK numeric range proofs) MAY be registered as custom `credentialType` values. In this pattern, the attestation content IS the ZK proof artifact rather than an issuer-signed claim, and the issuer authority represents the proof system's public parameters registry rather than an organizational entity. See Appendix F.5 for a comparison of the Proxy Issuer pattern and ZK credential types as complementary approaches to the cold-start problem.

### 8.1 Structure

A Credential Attestation Manifest is an `hiri:AttestationManifest` (Privacy Extension §10) published by the issuer's authority. The attestation `subject` field MUST bind to the holder's passport.

Issuers MUST declare their signing algorithm in the `hiri:signature.algorithm` field (§6.5.3). Holders and verifiers MUST use the Signature Algorithm Registry to dispatch verification for issuer signatures.

```json
{
  "@context": [
    "https://hiri-protocol.org/spec/v3.1",
    "https://hiri-protocol.org/privacy/v1",
    "https://hiri-protocol.org/passport/v1",
    "https://w3id.org/security/v2"
  ],
  "@id": "hiri://key:ed25519:z<issuer-authority>/attestation/employment-sarah-2026-001",
  "@type": "hiri:AttestationManifest",

  "hiri:version": "1",
  "hiri:branch": "main",

  "hiri:timing": {
    "created": "2026-03-01T09:00:00Z"
  },

  "hiri:privacy": {
    "mode": "selective-disclosure",
    "parameters": {
      "indexSalt": "<base64url-encoded-256-bit-salt>",
      "statementCount": 8,
      "mandatoryStatements": [0, 1, 2],
      "disclosureSuite": "HMAC"
    }
  },

  "hiri:attestation": {
    "subject": {
      "type": "hiri:PassportHolder",
      "holderAuthority": "key:ed25519:z<holder-authority>",
      "holderPassportURI": "hiri://key:ed25519:z<holder-authority>/passport/main",
      "subjectDID": "did:key:z<holder-did-key>"
    },
    "claim": {
      "@type": "hiri:passport:EmploymentCredential",
      "credentialType": "EmploymentCredential",
      "position": "Environmental Scientist",
      "organization": "EcoImpact Consulting",
      "startDate": "2022-06-01",
      "employmentStatus": "active",
      "attestedAt": "2026-03-01T09:00:00Z",
      "validUntil": "2027-03-01T00:00:00Z"
    },
    "evidence": {
      "method": "hr-system-verification",
      "description": "Verified against EcoImpact HR records."
    }
  },

  "hiri:signature": {
    "type": "Ed25519Signature2020",
    "algorithm": "ed25519",
    "canonicalization": "URDNA2015",
    "created": "2026-03-01T09:00:00Z",
    "verificationMethod": "hiri://key:ed25519:z<issuer-authority>/key/main#key-1",
    "proofPurpose": "assertionMethod",
    "proofValue": "z..."
  }
}
```

### 8.2 Subject Binding

| Field | Required | Description |
|-------|----------|-------------|
| `type` | REQUIRED | MUST be `hiri:PassportHolder` |
| `holderAuthority` | REQUIRED | Holder's HIRI authority string |
| `holderPassportURI` | REQUIRED | The holder's canonical passport URI |
| `subjectDID` | RECOMMENDED | Holder's `did:key` DID |

**NORMATIVE:** The `holderAuthority` in the subject binding MUST match the authority in the `holderPassportURI`. A verifier MUST reject an attestation where these are inconsistent.

### 8.3 Mandatory Statements in Selective Disclosure Attestations

When an attestation is published in `selective-disclosure` mode, the issuer MUST designate at minimum the following statements as mandatory (always disclosed):

1. The credential type (`credentialType`)
2. The attestation timestamp (`attestedAt`)
3. The issuer's authority identifier

---

## 9. Passport Manifest Schema

### 9.1 Full Schema

```json
{
  "@context": [
    "https://hiri-protocol.org/spec/v3.1",
    "https://hiri-protocol.org/privacy/v1",
    "https://hiri-protocol.org/passport/v1",
    "https://w3id.org/security/v2"
  ],
  "@id": "hiri://key:ed25519:z<holder-authority>/passport/main",
  "@type": "hiri:PassportManifest",

  "hiri:version": "3",
  "hiri:branch": "main",

  "hiri:timing": {
    "created": "2026-03-15T10:00:00Z"
  },

  "hiri:passport": {
    "holder": {
      "authority": "key:ed25519:z<holder-authority>",
      "did": "did:key:z<holder-did-key>",
      "displayName": "Sarah Thompson",
      "keyDocumentURI": "hiri://key:ed25519:z<holder-authority>/key/main"
    },
    "credentialSlots": [
      {
        "slotId": "slot:employment-ecoimpact-2026",
        "credentialType": "EmploymentCredential",
        "displayLabel": "Environmental Scientist — EcoImpact Consulting",
        "privacyMode": "selective-disclosure",
        "attestationRef": {
          "authority": "key:ed25519:z<ecoimpact-authority>",
          "manifestHash": "sha256:e08da327...",
          "manifestVersion": "1"
        },
        "validFrom": "2022-06-01T00:00:00Z",
        "validUntil": "2027-03-01T00:00:00Z",
        "status": "active"
      },
      {
        "slotId": "slot:certification-wetland-nea-2025",
        "credentialType": "ProfessionalCertification",
        "displayLabel": "Wetland Specialist Certification — NEA",
        "privacyMode": "public",
        "attestationRef": {
          "authority": "key:ed25519:z<nea-authority>",
          "manifestHash": "sha256:b2c9d4e1...",
          "manifestVersion": "2"
        },
        "validFrom": "2025-01-15T00:00:00Z",
        "validUntil": "2028-01-15T00:00:00Z",
        "status": "active"
      },
      {
        "slotId": "slot:govid-verification-2026",
        "credentialType": "GovernmentIdVerification",
        "displayLabel": "Government Identity Verification",
        "privacyMode": "proof-of-possession",
        "attestationRef": {
          "authority": "key:ed25519:z<state-authority-authority>",
          "manifestHash": "sha256:f3d1a8b9...",
          "manifestVersion": "1"
        },
        "status": "active"
      }
    ],
    "slotCount": 3,
    "activeSlotCount": 3
  },

  "hiri:content": {
    "hash": "sha256:d4e2c1f9...",
    "addressing": "raw-sha256",
    "canonicalization": "URDNA2015",
    "format": "application/ld+json",
    "size": 1842
  },

  "hiri:chain": {
    "previous": "sha256:a1b2c3d4...",
    "genesisHash": "sha256:e5f6a7b8...",
    "depth": 3,
    "previousBranch": "main"
  },

  "hiri:signature": {
    "type": "Ed25519Signature2020",
    "algorithm": "ed25519",
    "canonicalization": "URDNA2015",
    "created": "2026-03-15T10:00:00Z",
    "verificationMethod": "hiri://key:ed25519:z<holder-authority>/key/main#key-1",
    "proofPurpose": "assertionMethod",
    "proofValue": "z..."
  }
}
```

### 9.2 Passport Manifest Field Requirements

| Field | Required | Notes |
|-------|----------|-------|
| `@context` | REQUIRED | MUST include base v3.1, privacy v1, and passport v1 contexts |
| `@id` | REQUIRED | MUST be `hiri://<holderAuthority>/passport/<branch>` |
| `@type` | REQUIRED | MUST be `hiri:PassportManifest` |
| `hiri:version` | REQUIRED | JSON String (base-10 integer), per v3.1.1 §11.3 |
| `hiri:branch` | REQUIRED | Default: `"main"` |
| `hiri:timing.created` | REQUIRED | ISO 8601 timestamp |
| `hiri:passport.holder` | REQUIRED | Holder metadata block |
| `hiri:passport.holder.authority` | REQUIRED | MUST match the authority in `@id` |
| `hiri:passport.holder.did` | RECOMMENDED | `did:key` identifier |
| `hiri:passport.credentialSlots` | REQUIRED | Array, MAY be empty |
| `hiri:passport.slotCount` | REQUIRED | Total slots including inactive |
| `hiri:passport.activeSlotCount` | REQUIRED | Slots with `status: "active"` |
| `hiri:content` | REQUIRED | Content hash of the holder content block |
| `hiri:content.canonicalization` | REQUIRED | MUST be `URDNA2015` |
| `hiri:signature.algorithm` | REQUIRED | MUST be a registered algorithm ID (§6.5) |
| `hiri:signature.canonicalization` | REQUIRED | MUST match `hiri:content.canonicalization` (Profile Symmetry Rule) |
| `hiri:chain` | REQUIRED for v > 1 | Chain link to previous passport version |

**NORMATIVE: Passport manifests MUST use URDNA2015 canonicalization.** The RDF graph profile is required for cross-authority credential graph merging semantics.

### 9.3 Holder Content Payload

The Holder Content is the JSON-LD document whose hash is declared in `hiri:content`. For URDNA2015 canonicalization, the content payload must be a valid JSON-LD document with no unresolvable external context references.

### 9.4 Slot Count Limits and Pagination

Large credential sets can impose significant resolution costs on edge devices. Conformance levels impose the following normative limits:

| Conformance Level | Maximum `slotCount` |
|------------------|---------------------|
| Passport-Core | 50 |
| Passport-Interoperable | 200 |
| Passport-Full | 500 |

**NORMATIVE:** A verifier operating at a given conformance level MUST NOT be required to resolve more slots than the maximum defined for that level. If a passport's `slotCount` exceeds the verifier's conformance limit, the verifier MUST report `PASSPORT_SLOT_COUNT_EXCEEDED` (Appendix C) and MAY perform partial verification on the first N slots.

**Paginated Resolution (INFORMATIVE):** Passport Manifests with large slot counts SHOULD use HIRI branch-based pagination. The canonical `main` branch contains a `hiri:passport.slotIndex` with lightweight references (slotId + credentialType only). Individual branches (e.g., `professional`, `academic`) contain the full slot details for logical partitions of the portfolio. The holder maintains a branch-of-branches index at `main`. Verifiers requesting a specific `credentialType` resolve only the relevant branch, not the full slot set.

This paginated branch pattern is INFORMATIVE and MAY be specified in a future HIRI Passport Scaling addendum.

---

## 10. Organizational Authority Bootstrap

### 10.1 did:web Domain Binding

Issuers PUBLISH their HIRI authority binding at a well-known URL derived from their domain:

```
https://<domain>/.well-known/hiri-key.json
```

```json
{
  "@context": ["https://www.w3.org/ns/did/v1", "https://hiri-protocol.org/spec/v3.1"],
  "id": "did:web:<domain>",
  "verificationMethod": [
    {
      "id": "did:web:<domain>#key-main",
      "type": "Ed25519VerificationKey2020",
      "controller": "did:web:<domain>",
      "publicKeyMultibase": "z<base58btc-encoded-public-key>"
    }
  ],
  "hiriAuthority": "key:ed25519:z<issuer-authority>"
}
```

For issuers using P-256, the `type` is `EcdsaSecp256r1VerificationKey2019` and `publicKeyMultibase` encodes the uncompressed P-256 point.

### 10.2 DNSSEC Verification (RECOMMENDED)

Verifiers SHOULD verify:

1. The domain's DNS zone is DNSSEC-signed
2. The `hiri-key.json` is served over HTTPS with a valid TLS certificate for the domain
3. The `publicKeyMultibase` in the DID document matches the `hiriAuthority` authority's public key

### 10.3 KeyDocument Cross-Reference

```json
{
  "@type": "hiri:KeyDocument",
  "hiri:authority": "key:ed25519:z<issuer-authority>",
  "organizationalIdentity": {
    "displayName": "EcoImpact Consulting",
    "domain": "ecoimpact.com",
    "domainBinding": "https://ecoimpact.com/.well-known/hiri-key.json",
    "dnssecVerified": true
  },
  "activeKeys": [...]
}
```

### 10.4 Verification Chain

```
Credential Attestation Manifest
        ↓
Issuer Authority (key:ed25519:z<...>)
        ↓
Issuer KeyDocument
        ↓
organizationalIdentity.domain
        ↓
https://<domain>/.well-known/hiri-key.json
        ↓
did:web DID document
        ↓
publicKeyMultibase matches issuer authority
```

### 10.5 Identity Anchor Declaration

An **Identity Anchor** is a verifiable proof connecting a HIRI authority to a real-world control point. It formalizes and extends the domain binding defined in §10.1–10.3, allowing authorities to declare anchors beyond domain ownership.

Identity anchors are declared in the authority's KeyDocument as an `identityAnchors` array. Multiple anchors MAY be declared; each is independently verifiable. Verifiers SHOULD verify at least one declared anchor and SHOULD prefer higher-assurance anchor types when multiple are available.

```json
{
  "@type": "hiri:KeyDocument",
  "hiri:authority": "key:ed25519:z<authority>",
  "identityAnchors": [
    {
      "anchorType": "domain",
      "anchorValue": "ecoimpact.com",
      "verificationMethod": "dnssec",
      "verificationURI": "https://ecoimpact.com/.well-known/hiri-key.json"
    },
    {
      "anchorType": "government-registry",
      "anchorValue": "US-EIN-12-3456789",
      "verificationMethod": "signed-registry-credential",
      "verificationURI": "https://ecoimpact.com/.well-known/hiri-gov-anchor.json"
    }
  ]
}
```

#### 10.5.1 Identity Anchor Type Registry

| Anchor Type | Description | Verification Method | Trust Contribution |
|-------------|-------------|--------------------|--------------------|
| `domain` | Domain name ownership | DNSSEC (RECOMMENDED) or HTTPS web document | `"partial"` (HTTPS) or `"full"` (DNSSEC) per §12.5 |
| `government-registry` | Registration in a government business or identity registry | Digitally signed registry credential from the issuing government authority | Application-layer policy; surface as `"government-registry"` in trust result |
| `institution` | Membership in an institutional authority (university, professional body, accreditation body) | Signed organizational credential from the institution | Application-layer policy; surface as `"institution"` in trust result |
| `decentralized-network` | DID-based registration in a decentralized identity network | DID document resolution + network-specific verification (e.g., blockchain proof) | Application-layer policy; surface as `"decentralized-network"` in trust result |

#### 10.5.2 Anchor Verification in Phase 4

Phase 4 (§12.5) verifies the `domain` anchor as its primary mechanism. When other anchor types are present, verifiers SHOULD attempt to verify them according to the anchor's declared `verificationMethod` and report the result in `SlotVerificationResult`.

**NORMATIVE:** Verifiers MUST NOT treat an unverified non-`domain` anchor as equivalent to a verified anchor. If a verifier cannot verify a declared anchor (e.g., government registry resolution is unavailable), the anchor contributes no trust level elevation.

**Offline anchor verification behavior:** When anchor verification resources (domain `.well-known` endpoint, government registry API, DID resolution) are unavailable, verifiers MUST follow §12.7 (Offline Verifier Decision Table). The domain anchor unavailability row applies: report `organizationTrustLevel: "key-only"` and surface a warning. Cached anchor verification results MAY be used within the 24-hour KeyDocument cache TTL. After TTL expiry, anchor results are treated as unverified.

**Reporting:** The verification result SHOULD include an `identityAnchors` array summarizing which anchors were verified and their verification outcomes. This allows relying parties to apply their own policies about which anchor types are acceptable for their use case.

---

## 11. Passport Presentation Protocol

### 11.1 Purpose

A Passport Presentation is a holder-signed artifact that selectively reveals credential slots to a named verifier. The holder responds to a Disclosure Request from the verifier and constructs a presentation containing only the slots the verifier requires. By default, the presentation reveals only what was requested and nothing more (§4.7).

### 11.2 Disclosure Request Structure

```json
{
  "@context": ["https://hiri-protocol.org/passport/v1"],
  "@type": "hiri:DisclosureRequest",
  "requestId": "req:2026-03-15-verifier-abc-001",
  "verifier": {
    "authority": "key:ed25519:z<verifier-authority>",
    "displayName": "Environmental Regulatory Agency"
  },
  "requestedSlots": [
    {
      "credentialType": "EmploymentCredential",
      "minimumDisclosure": "summary"
    },
    {
      "credentialType": "ProfessionalCertification",
      "minimumDisclosure": "full"
    }
  ],
  "completenessAudit": false,
  "nonce": "YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXo...",
  "expiresAt": "2026-03-15T11:00:00Z",
  "signature": {
    "type": "Ed25519Signature2020",
    "algorithm": "ed25519",
    "verificationMethod": "hiri://key:ed25519:z<verifier-authority>/key/main#key-1",
    "proofValue": "z..."
  }
}
```

**`completenessAudit`** — OPTIONAL boolean, default `false`. When `false`, the holder's presentation MUST omit any reference to credential slots beyond those requested, exposing only `omittedSlotCount` (§11.5). When `true`, the holder MAY include a `withheldSlots` summary. See §11.5.

**`nonce`** — REQUIRED. MUST be a base64url-encoded string (no padding) representing exactly 32 bytes of output from a cryptographically secure pseudorandom number generator (CSPRNG). Implementations MUST reject a nonce shorter than 43 characters in base64url-no-pad encoding (the minimum for 32 bytes). The nonce is single-use: the verifier MUST record and reject any reused nonce within the validity window of the request. The nonce is incorporated into presentation slot token derivation (§11.7.2).

### 11.3 Presentation Structure

```json
{
  "@context": [
    "https://hiri-protocol.org/spec/v3.1",
    "https://hiri-protocol.org/privacy/v1",
    "https://hiri-protocol.org/passport/v1"
  ],
  "@type": "hiri:PassportPresentation",
  "@id": "hiri://key:ed25519:z<holder-authority>/presentation/req-2026-03-15-001",

  "hiri:timing": {
    "created": "2026-03-15T10:30:00Z"
  },

  "hiri:presentation": {
    "passportURI": "hiri://key:ed25519:z<holder-authority>/passport/main",
    "passportManifestHash": "sha256:d4e2c1f9...",
    "passportVersion": "3",
    "disclosureRequestId": "req:2026-03-15-verifier-abc-001",
    "requestNonce": "YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXo...",
    "verifierAuthority": "key:ed25519:z<verifier-authority>",
    "disclosedSlots": [
      {
        "presentationSlotToken": "HmacDerivedToken-abc123...",
        "credentialType": "EmploymentCredential",
        "displayLabel": "Environmental Scientist — EcoImpact Consulting",
        "privacyMode": "selective-disclosure",
        "attestationRef": {
          "authority": "key:ed25519:z<ecoimpact-authority>",
          "manifestHash": "sha256:e08da327...",
          "manifestVersion": "1"
        },
        "disclosureProof": {
          "suite": "HMAC",
          "disclosedStatements": [
            {
              "index": 0,
              "nquad": "<...> <hiri:passport:credentialType> <hiri:passport:EmploymentCredential> .",
              "hmac": "..."
            },
            {
              "index": 2,
              "nquad": "<...> <hiri:passport:organization> \"EcoImpact Consulting\" .",
              "hmac": "..."
            }
          ]
        }
      },
      {
        "presentationSlotToken": "HmacDerivedToken-def456...",
        "credentialType": "ProfessionalCertification",
        "displayLabel": "Wetland Specialist Certification — NEA",
        "privacyMode": "public",
        "attestationRef": {
          "authority": "key:ed25519:z<nea-authority>",
          "manifestHash": "sha256:b2c9d4e1...",
          "manifestVersion": "2"
        }
      }
    ],
    "omittedSlotCount": 1
  },

  "hiri:signature": {
    "type": "Ed25519Signature2020",
    "algorithm": "ed25519",
    "canonicalization": "JCS",
    "created": "2026-03-15T10:30:00Z",
    "verificationMethod": "hiri://key:ed25519:z<holder-authority>/key/main#key-1",
    "proofPurpose": "assertionMethod",
    "proofValue": "z..."
  }
}
```

### 11.4 Presentation Canonicalization

Passport Presentations MUST use **JCS canonicalization** (not URDNA2015). The presentation is a self-contained response document that does not require cross-authority RDF merge semantics. JCS is sufficient and avoids URDNA2015 computational overhead at verification time.

### 11.5 Omitted Slot Handling (v1.1.0)

The default passport presentation MUST respect the Minimum Disclosure Surface principle (§4.7). By default:

1. The presentation MUST include only slots corresponding to the credential types listed in the Disclosure Request's `requestedSlots`.
2. The presentation MUST include `omittedSlotCount`: an integer equal to the number of active slots in the passport that are NOT included in this presentation. This count alone is disclosed — no types, hashes, or tokens for omitted slots.
3. The `withheldSlots` array from v1.0.0 is **removed from the default presentation**.

**Completeness Audit (explicit opt-in):** When the Disclosure Request contains `completenessAudit: true`, the holder MAY (but is not REQUIRED to) include a `withheldSlotSummary` array in the presentation:

```json
{
  "withheldSlotSummary": [
    {
      "presentationSlotToken": "HmacDerivedToken-ghi789...",
      "credentialType": "GovernmentIdVerification",
      "privacyMode": "proof-of-possession",
      "attestationRef": {
        "authority": "key:ed25519:z<state-authority-authority>",
        "manifestHash": "sha256:f3d1a8b9...",
        "manifestVersion": "1"
      }
    }
  ]
}
```

**NORMATIVE:** A presentation that includes `withheldSlotSummary` without a corresponding `completenessAudit: true` in the originating DisclosureRequest MUST be rejected by the verifier with `PRESENTATION_UNILATERAL_AUDIT_DISCLOSURE`.

**Holder discretion:** The holder retains the right to decline a completeness audit even when requested. Holder software MUST present the completeness audit request to the holder explicitly and MUST NOT silently comply. A holder declining a completeness audit MUST respond with `omittedSlotCount` only. The verifier MAY then decline to provide services based on that refusal — this is an application-layer policy decision that the protocol cannot prevent or compel. See §14.8 (Coercion Resistance) for security considerations on this interaction.

### 11.6 Presentation Expiry

Presentations MUST be treated as ephemeral. A verifier MUST NOT cache a presentation and use it to authorize the holder at a later time beyond the context of the original disclosure request. The `requestNonce` binds the presentation to a specific request instance. Applications SHOULD enforce short-lived presentation windows (RECOMMENDED: ≤ 24 hours from `hiri:timing.created`).

### 11.7 Presentation Slot Blinding (v1.1.0)

#### 11.7.1 Purpose

The `slotId` in the Passport Manifest (Tier 1) is a stable identifier that MUST remain stable across passport versions for audit and lifecycle management. However, if exposed directly in presentations, colluding verifiers could correlate the same holder across different contexts using the stable `slotId` as a global tracking identifier — even when the credential content is selectively disclosed or withheld.

This section defines the normative blinding mechanism that replaces `slotId` in presentations with a per-presentation, per-verifier, per-nonce token that is computationally unlinkable across presentations.

#### 11.7.2 Slot Blinding Key

The holder maintains a **Slot Blinding Key**: a 32-byte secret generated once at passport genesis. The Slot Blinding Key MUST:

- Be generated using a CSPRNG
- Be persisted in the holder's secure storage alongside the passport signing key
- NEVER be published or transmitted to any verifier or issuer
- Be rotated alongside the passport signing key (see §13.5)

Derivation at genesis:

```
slotBlindingKey = HKDF-SHA256(
  ikm   = holdingSigningKeyPrivateBytes,
  salt  = "hiri-passport-blinding-v1",
  info  = holderAuthority,
  len   = 32
)
```

Where `HKDF-SHA256` follows RFC 5869 and the `salt` and `info` are UTF-8 encoded strings.

**Implementation Note:** Deriving the Slot Blinding Key from the signing key via HKDF means it is recoverable from the signing key alone. Implementations that allow key export MUST export both the signing key and the derived blinding key, or document that the blinding key is re-derivable from the signing key using this procedure.

#### 11.7.3 Presentation Slot Token Derivation

For each slot included in a presentation (whether disclosed or appearing in `withheldSlotSummary`), the holder computes:

```
presentationSlotToken = base64url(
  HMAC-SHA256(
    key     = slotBlindingKey,
    message = UTF8(slotId) || 0x00
              || base64url_decode(requestNonce)
              || 0x00
              || UTF8(verifierAuthority)
  )
)
```

Where:
- `slotBlindingKey` is the 32-byte Slot Blinding Key (§11.7.2)
- `slotId` is the raw slot ID string (e.g., `"slot:employment-ecoimpact-2026"`)
- `requestNonce` is decoded from the base64url nonce in the DisclosureRequest to its raw 32 bytes
- `verifierAuthority` is the verifier's HIRI authority string as declared in the DisclosureRequest's `verifier.authority` field (e.g., `"key:ed25519:z<verifier-key>"`)
- Each `0x00` is a single zero byte serving as a domain separator between variable-length fields
- The result is base64url-encoded without padding

**Why three fields, two separators:** The two `0x00` domain separators prevent length-extension ambiguity across all three variable-length fields. Without separators, an attacker could construct inputs where a different `(slotId, nonce, verifierAuthority)` triple produces an identical message byte sequence. With separators, no such construction is possible as long as none of the input strings contain the byte `0x00` — which is guaranteed for UTF-8 strings and decoded random bytes.

**Verifier authority binding:** The inclusion of `verifierAuthority` in the HMAC message closes the cross-verifier token relay attack. Consider: Verifier A wants to determine whether the holder is presenting the same slot to Verifier B. Verifier A obtains a nonce from Verifier B's infrastructure, places that nonce in their own DisclosureRequest, and asks the holder to sign it. In v1.1.0, the holder would compute `HMAC(key, slotId || 0x00 || nonce)` — producing the exact token Verifier B would expect, giving Verifier A the ability to impersonate the holder's slot to Verifier B. With verifier authority binding, the token Verifier A receives is `HMAC(key, slotId || 0x00 || nonce || 0x00 || verifierA_authority)`, which is computationally distinct from the token Verifier B would compute for the same nonce: `HMAC(key, slotId || 0x00 || nonce || 0x00 || verifierB_authority)`. Relay is defeated even when nonces are shared.

#### 11.7.4 Verifier Behavior

Verifiers receive `presentationSlotToken` values and MUST NOT attempt to reverse-derive `slotId` values from them. The verifier uses `presentationSlotToken` only as a stable identifier within the scope of a single presentation session — to correlate a disclosed slot with its `attestationRef` and `credentialType`, and to detect if the same slot appears in both `disclosedSlots` and `withheldSlotSummary` (which MUST be rejected as a malformed presentation).

#### 11.7.5 Blinding Applies to All Presentation Slot References

`presentationSlotToken` replaces `slotId` in ALL presentation slot objects:
- Objects in `disclosedSlots`
- Objects in `withheldSlotSummary` (when completeness audit is requested)

The raw `slotId` MUST NOT appear anywhere in a `hiri:PassportPresentation`. A verifier that receives a presentation containing raw `slotId` values MUST reject it with `PRESENTATION_SLOT_NOT_BLINDED` (Appendix C).

---

## 12. Verification Algorithm

### 12.1 Overview

Complete passport verification consists of four sequential phases:

```
Phase 1: Passport Manifest Verification
Phase 2: Credential Slot Verification
Phase 3: Credential Attestation Verification (with Tier 2 Override)
Phase 4: Organizational Authority Bootstrap
```

All four phases are required for a `trustLevel: "full"` result.

### 12.2 Phase 1 — Passport Manifest Verification

1. Resolve the holder's passport URI: `hiri://<authority>/passport/main`
2. Confirm `hiri:signature.algorithm` is in the verifier's Signature Algorithm Registry (§6.5). If not, report `SIGNATURE_ALGORITHM_UNSUPPORTED` and halt.
3. Verify the manifest signature using the registered algorithm and v3.1.1 §10 verification procedure.
4. Verify chain integrity using v3.1.1 §11 chain integrity algorithm.
5. Verify holder key lifecycle using v3.1.1 §13 key lifecycle algorithm.
6. Confirm `@type` is `hiri:PassportManifest`.
7. Confirm `hiri:passport.holder.authority` matches the authority in `@id`.

**Additional step for presentation verification only (when verifying a `hiri:PassportPresentation` rather than the Passport Manifest directly):**

**Step 2a — Temporal Key Lifecycle Check (NORMATIVE):**

After completing step 5 (key lifecycle verification), the verifier MUST perform a temporal check:

> Let `T_created` = the ISO 8601 timestamp in the presentation's `hiri:timing.created` field.
> Let `T_event` = the timestamp of any key rotation or revocation event recorded in the holder's KeyDocument for the signing key used in the presentation.
>
> If `T_event` exists AND `T_event > T_created`, the signing key event (rotation or revocation) occurred AFTER the presentation was generated. The verifier MUST reject the presentation with `PRESENTATION_KEY_ROTATED_AFTER_CREATION`.

**Rationale:** §11.6 allows presentations to remain valid for up to 24 hours. A holder who generates a presentation and then immediately rotates or revokes their key due to suspected compromise leaves a signed presentation floating in the wild — signed by a key that is now known-compromised. Checking key status at the current moment of verification (without this temporal check) would produce a false positive: the key appears "rotated-grace" but the presentation is already tainted. The temporal check ensures the verifier catches this case explicitly and surfaces the correct error, rather than accepting the presentation under the grace period window.

**Implementation note:** `T_event` is extracted from the holder's KeyDocument rotation or revocation record. If the holder's KeyDocument is unavailable (offline verification), the verifier MUST report `keyStatus: "unknown"` per v3.1.1 §B.10 and MUST NOT accept the presentation as fully verified. If `T_event` cannot be determined due to an unavailable KeyDocument, the verifier SHOULD treat the presentation as unverifiable for the temporal check and surface a warning — it MUST NOT treat indeterminate status as a passing check.

**On success:** Proceed to Phase 2.
**On failure:** Report `manifestVerified: false` and halt with appropriate error.

### 12.3 Phase 2 — Credential Slot Verification

For each credential slot in `hiri:passport.credentialSlots`:

1. Confirm `status` field. If `"revoked"` or `"expired"`, report slot status and skip Phase 3 for this slot. Tier 1 revocation and expiry do not require issuer confirmation — the holder's declaration is sufficient to suppress attestation resolution.
2. Confirm `privacyMode` is one of the three valid values. If not, report `SLOT_PRIVACY_MODE_UNKNOWN` and skip.
3. Record the `attestationRef` for Phase 3 processing.
4. If `validUntil` is present and past, report `slotStatus: "holder-claimed-expired"`.

No cryptographic work occurs in Phase 2.

### 12.4 Phase 3 — Credential Attestation Verification (Tier 2 Override)

For each active slot's `attestationRef`:

1. Resolve the Credential Attestation Manifest at the issuer's authority and manifest hash.
2. Confirm `hiri:signature.algorithm` is in the verifier's Signature Algorithm Registry. If not, report `SIGNATURE_ALGORITHM_UNSUPPORTED` for this slot.
3. Verify the attestation manifest signature using the registered issuer algorithm and v3.1.1 §10.
4. Verify the attestation chain integrity using v3.1.1 §11.
5. Verify the issuer key lifecycle using v3.1.1 §13.
6. Confirm `@type` is `hiri:AttestationManifest`.
7. Confirm `hiri:attestation.subject.holderAuthority` matches the holder's authority.
8. Confirm `hiri:privacy.mode` matches the slot's declared `privacyMode`. If not, report `ATTESTATION_MODE_MISMATCH`.

**Tier 2 Revocation Override (NORMATIVE):**

After completing steps 1–8, apply the following conflict resolution rule:

> If the issuer's attestation chain contains a version whose `claim.value` is `false`, or whose claim explicitly declares revocation (e.g., `claim.revoked: true`, or a revocation-type claim version), AND the Tier 1 slot `status` is `"active"`, the verifier MUST:
> 1. Set the effective slot status to `"revoked"`.
> 2. Set `attestationStatus` to `"issuer-revoked"`.
> 3. Report `ATTESTATION_TIER2_OVERRIDE_REVOKED` in the slot's warning array.
> 4. NOT accept the slot as valid, regardless of the Tier 1 holder assertion.

The rule is asymmetric: Tier 2 can only make the effective status MORE restrictive than Tier 1, not less. If Tier 1 says `"revoked"` but Tier 2 attestation is valid, the slot remains revoked. If Tier 1 says `"active"` but Tier 2 is revoked, the slot is revoked.

9. Check attestation `validUntil` (if present). If past, set `attestationStatus: "stale"` per Privacy Extension §10.5. A stale attestation is not equivalent to a revoked attestation.
10. If the slot is in `selective-disclosure` mode and a disclosure proof is available (from a presentation), verify the disclosure proof per Privacy Extension §8.
11. **Revocation log check (NORMATIVE for Passport-Interoperable and above):** Query the issuer's Revocation Transparency Log (§16) for a `RevocationLogEntry` matching the slot's `attestationRef.manifestHash`.
    - If an entry is found: set `attestationStatus: "issuer-revoked"` and report `REVOCATION_LOG_ENTRY_FOUND`. Apply Tier 2 Override rule.
    - If the log is reachable and no entry is found: revocation state is `"confirmed-valid"` from log perspective.
    - If the log is unreachable: consult cached checkpoint per §12.7. If no valid checkpoint is available, set revocationLogStatus: `"unknown"` and apply the offline decision table (§12.7).

The revocation log check is a discovery optimization — it finds revocations efficiently without requiring the verifier to walk the issuer's full attestation chain. It does NOT replace the Tier 2 Override check in steps 1–8; both MUST be performed.

### 12.5 Phase 4 — Organizational Authority Bootstrap

For each issuer authority encountered in Phase 3:

1. Resolve the issuer's KeyDocument (v3.1.1 §13).
2. If `organizationalIdentity.domain` is present, fetch `https://<domain>/.well-known/hiri-key.json`.
3. Parse the DID document and extract `hiriAuthority`.
4. Confirm `hiriAuthority` matches the issuer's HIRI authority string.
5. Record whether DNSSEC was used.

| Conditions | `organizationTrustLevel` |
|------------|--------------------------|
| KeyDocument + domain binding + DNSSEC | `"full"` |
| KeyDocument + domain binding (no DNSSEC) | `"partial"` |
| KeyDocument only (no domain binding) | `"key-only"` |
| No KeyDocument | `"unverifiable"` |

### 12.6 Verification Result

```typescript
interface PassportVerificationResult {
  passportURI: string;
  holderAuthority: string;
  holderSignatureAlgorithm: string;
  manifestVerified: boolean;
  manifestVersion: string;
  keyStatus: string;
  slots: SlotVerificationResult[];
  overallTrustLevel: "full" | "partial" | "key-only" | "unverifiable";
  warnings: string[];
  verifiedAt: string;
}

interface SlotVerificationResult {
  slotId: string;                  // Internal reference only; never returned to external verifiers
  credentialType: string;
  displayLabel: string;
  slotStatus: "active" | "revoked" | "expired" | "suspended" | "holder-claimed-expired";
  tier2Override: boolean;          // true if Tier 2 revocation overrode Tier 1 "active" status
  issuerSignatureAlgorithm: string;
  attestationVerified: boolean;
  attestationStatus: "valid" | "stale" | "issuer-revoked" | "unresolvable";
  revocationLogStatus: "confirmed-valid" | "revoked" | "unknown" | "cached-checkpoint" | "not-checked";
  revocationLogCheckpoint?: {
    checkpointTimestamp: string;
    treeSize: number;
    staleness: "within-window" | "expired";
  };
  organizationTrustLevel: "full" | "partial" | "key-only" | "unverifiable";
  issuerAuthority: string;
  issuerDisplayName?: string;
  issuerDomain?: string;
  disclosureVerified: boolean;
  warnings: string[];
}
```

**Note on `slotId` in verification results:** Verifiers MUST NOT expose raw `slotId` values in externally transmitted verification result documents. External APIs returning verification results SHOULD omit `slotId` or replace it with the `presentationSlotToken` from the presentation.

### 12.7 Offline Verifier Decision Table

This section is NORMATIVE. It defines required verifier behavior when network resources are unavailable during verification. The core invariant is stated once and applies to every row in the table:

**NORMATIVE INVARIANT: A resource availability state of `"unknown"` or `"unavailable"` MUST NEVER be treated as equivalent to `"active"`, `"valid"`, or `"confirmed"` for any resource or check. Absence of evidence is not evidence of absence.**

| Resource | Availability State | Phase | Required Action | Trust Level Ceiling |
|----------|--------------------|-------|-----------------|---------------------|
| KeyDocument | Online, resolved | 1, 3 | Full temporal and key lifecycle check | No ceiling imposed |
| KeyDocument | Unavailable (offline, no cache) | 1, 3 | Report `keyStatus: "unknown"`. MUST NOT proceed as `"active"`. | `"partial"` |
| KeyDocument | Cached, within TTL (24h) | 1, 3 | Use cached document. Warn `"cached-key-document"`. | `"partial"` |
| KeyDocument | Cached, TTL expired (online resolution failed) | 1, 3 | Report `keyStatus: "unknown"`. Use cached document only for signature verification, not lifecycle. | `"partial"` |
| Revocation log | Online, reachable | 3 | Full revocation log check (Phase 3 Step 11). | No ceiling imposed |
| Revocation log | Unavailable, checkpoint cached within staleness window | 3 | Report `revocationLogStatus: "cached-checkpoint"`. Accept as `"confirmed-valid"` within checkpoint scope only. | No ceiling imposed if checkpoint is current |
| Revocation log | Unavailable, no valid checkpoint | 3 | Report `revocationLogStatus: "unknown"`. MUST NOT accept as `"confirmed-valid"`. | `"partial"` |
| Domain binding (`.well-known`) | Unavailable | 4 | Report `organizationTrustLevel: "key-only"` or lower. | `"key-only"` |
| DNSSEC | Unavailable | 4 | Report DNSSEC unverified. Do not claim `"full"` org trust. | `"partial"` |
| `proofArtifactRef` URI | Available | P | Fetch, hash-verify, run ZK proof. | No ceiling imposed |
| `proofArtifactRef` URI | Timeout after retries | P | Report `biometricBinding: "unverifiable-offline"`. Core credential trust unaffected. | No ceiling on core credential |
| `proofArtifactRef` URI | Permanently unavailable | P | Same as timeout. Log `PRESENTATION_PROOF_ARTIFACT_UNAVAILABLE`. | No ceiling on core credential |

**Verifier implementation requirement:** Verifiers MUST implement the offline decision table before claiming any Passport conformance level. Implementations that treat any `"unknown"` or `"unavailable"` state as a passing check fail conformance regardless of level.

**Trust level ceiling combination rule:** When multiple ceiling conditions apply simultaneously (e.g., both KeyDocument unavailable and revocation log unavailable), the effective trust level is the MINIMUM of all applicable ceilings.

---

## 13. Passport Lifecycle

### 13.1 Creation (Genesis)

The holder generates a fresh signing keypair using a registered algorithm (§6.5), defaulting to Ed25519. The slot blinding key is derived from the signing key (§11.7.2). The passport genesis manifest (version `"1"`, no `hiri:chain` block) is created with an empty `credentialSlots` array or with initial credentials if available. The holder SHOULD publish a KeyDocument (v3.1.1 §13).

### 13.2 Adding a Credential

1. The issuer publishes the Attestation Manifest under the issuer's authority.
2. The holder verifies the attestation manifest (Phase 3, §12.4).
3. The holder adds a new credential slot referencing the attestation manifest.
4. The holder publishes a new passport version (`hiri:version` incremented by 1).
5. The `hiri:chain` block links to the previous passport manifest.

### 13.3 Updating a Credential

When the issuer publishes a new attestation version:

1. The holder verifies the new attestation version.
2. The holder updates the slot's `attestationRef.manifestHash` and `manifestVersion`.
3. The holder publishes a new passport version.

The `slotId` is stable across this update.

### 13.4 Credential Revocation

**Issuer-side revocation:** The issuer publishes a new Attestation Manifest version with an explicit revocation claim. The Tier 2 Override rule (§12.4) causes the verifier to detect revocation regardless of the Tier 1 slot status. The holder SHOULD update the slot `status` to `"revoked"` in the next passport version for user-facing clarity, but this is advisory — Tier 2 governs.

**Holder-side removal:** The holder MAY mark a slot `status: "revoked"` or remove it entirely from the passport. If removed, the chain preserves the historical slot in previous versions.

### 13.5 Key Rotation

On key rotation, a new Slot Blinding Key MUST be derived from the new signing key using the derivation procedure in §11.7.2. All prior presentation slot tokens derived from the old blinding key become unlinkable to tokens derived from the new key. This is desirable: key rotation produces a complete break in presentation token continuity.

After rotation, the holder SHOULD publish a new passport version signed with the new key. Issuer attestations pinning the old holder authority in their subject binding remain verifiable via the chain. A new attestation bound to the new holder authority is NOT required unless the issuer independently chooses to reissue.

### 13.6 Passport Archival

```json
{
  "hiri:passport": {
    "lifecycleStatus": "archived",
    "archivedAt": "2030-01-01T00:00:00Z"
  }
}
```

Archived passports are not invalid — their historical credential record remains verifiable.

### 13.7 Credential State Synchronization (INFORMATIVE)

This section is INFORMATIVE. It provides guidance on the holder software and verifier behavior that is recommended for detecting and surfacing issuer-side revocations. The protocol does not mandate any synchronization mechanism — the Tier 2 Override rule (§12.4) handles conflicts at verification time.

#### 13.7.1 The Desynchronization Problem

The holder's Passport Manifest (Tier 1) reflects the credential state at the time the holder last updated the manifest. If an issuer revokes a credential between the holder's last passport update and a verifier's verification request, the holder may present a passport in good faith that the verifier will find contains a revoked credential. This creates:

1. **User experience friction:** The verifier rejects the credential without advance warning to the holder.
2. **Holder confusion:** The holder's passport software shows the credential as active when the issuer has already revoked it.

#### 13.7.2 Recommended Holder Sync Cadence

Passport holder software SHOULD poll active slot attestation manifests for chain updates at the following cadences, as a function of the slot's credential type:

| Credential Type | Recommended Poll Cadence | Rationale |
|-----------------|-------------------------|-----------|
| `GovernmentIdVerification` | On each passport use event | Revocation can be immediate |
| `BackgroundCheckClearance` | Daily | Security clearances may be revoked urgently |
| `EmploymentCredential` | Weekly | Employment changes are episodic |
| `ProfessionalCertification` | Monthly | Certification cycles are typically annual |
| `EducationCredential` | On `validUntil` approach | Rarely revoked; check at expiry window |
| Other | Monthly | Default cadence |

Polling is performed by resolving the issuer's attestation chain head (latest version) and comparing its manifest hash to the `attestationRef.manifestHash` in the slot. If the hashes differ, the holder software SHOULD:

1. Verify the new attestation version.
2. Notify the holder of the change.
3. If the new version contains a revocation, automatically update the slot `status` in a new passport version (subject to holder confirmation on sensitive changes).

#### 13.7.3 Verifier Presentation of Tier 2 Override Results

When a verifier detects a Tier 2 revocation override (§12.4), the verifier SHOULD:

1. Clearly distinguish the override from a simple signature failure in the verification result surface.
2. Report: `"slotStatus": "revoked"`, `"tier2Override": true`, `"attestationStatus": "issuer-revoked"`.
3. NOT characterize the holder as presenting a fraudulent credential — the holder may be presenting in good faith due to the desynchronization problem described in §13.7.1. The protocol cannot distinguish good-faith desynchronization from deliberate misrepresentation; that distinction is application-layer policy.

#### 13.7.4 Holder Response to Rejection

When holder software receives a notification that a presentation was rejected due to a Tier 2 override, it SHOULD:

1. Immediately poll the issuer's attestation chain.
2. Present the updated attestation status to the holder.
3. Prompt the holder to contact the issuer if the revocation appears erroneous.
4. Update the Tier 1 slot status in a new passport version if revocation is confirmed.

---

### 13.8 Organizational Key Recovery (INFORMATIVE)

This section is INFORMATIVE. Individual holder key recovery is addressed via biometric oracles in Appendix G.4. This section addresses the distinct problem of enterprise and organizational key management where multiple authorized representatives must be able to act on behalf of an organizational passport authority.

#### 13.8.1 The Organizational Key Problem

An organizational passport authority — a company, a government agency, a research institution — faces a different key management challenge than an individual. Multiple authorized representatives must be able to issue and update passport credentials. A single individual's departure or device loss must not orphan the organization's entire credential portfolio.

#### 13.8.2 Multi-Recipient Encryption for Key Material

Privacy Extension v1.4.1 Mode 2 (Encrypted Distribution) already defines a multi-recipient key encapsulation mechanism (one CEK encrypted to multiple recipient public keys). Organizations SHOULD apply this same pattern to key escrow:

1. The organizational signing keypair is the canonical authority.
2. The private key is encrypted using Mode 2 multi-recipient encryption to a set of designated custodians (e.g., CISO, Deputy CISO, legal counsel).
3. The encrypted key material is stored as a Mode 2 HIRI artifact under a non-public branch (e.g., `hiri://<orgAuthority>/key/escrow`).
4. Any single designated custodian can decrypt and recover the organizational private key using their own keypair.

This pattern uses existing Privacy Extension machinery without requiring new protocol mechanisms.

#### 13.8.3 Threshold Key Splitting

For higher-assurance organizational contexts, organizations SHOULD use threshold cryptography (e.g., Shamir's Secret Sharing or threshold BLS signatures) to split the organizational private key into `n` shares distributed among `k`-of-`n` custodians. No single custodian possesses the full key; recovery requires `k` custodians to combine their shares.

The threshold split parameters (`k`, `n`) SHOULD be declared in the organizational KeyDocument:

```json
{
  "hiri:keyRecovery": {
    "scheme": "threshold-sss",
    "threshold": 3,
    "totalShares": 5,
    "custodianCount": 5,
    "escrowArtifact": "hiri://<orgAuthority>/key/escrow"
  }
}
```

#### 13.8.4 Holder Sovereignty Boundary

Multi-recipient escrow and threshold splitting apply to organizational authorities managing credentials on behalf of an institution. They MUST NOT be applied to individual holder passports without explicit, documented holder consent — doing so would violate the holder sovereignty principle (§4.1) by giving a third party the ability to impersonate the holder's passport authority.

---

## 14. Security Considerations

### 14.1 Slot Reference Pinning

Credential slot `attestationRef` entries pin a specific manifest version by hash. This prevents a malicious issuer from silently downgrading a credential after the holder has published their passport. A new attestation version requires a new passport version with an updated `attestationRef`.

### 14.2 Display Label Visibility

The `displayLabel` field is part of the public passport manifest content. Even for `proof-of-possession` slots, the credential type and display label are visible. Holders MUST NOT include sensitive information in credential slot display labels.

### 14.3 Presentation Binding

A Passport Presentation is bound to a specific `requestNonce` and a specific `passportManifestHash`. Verifiers MUST:

1. Confirm the `requestNonce` matches the nonce they issued.
2. Confirm the `passportManifestHash` matches the current (or recently valid) passport manifest version.
3. Reject presentations bound to expired or superseded nonces.
4. Maintain a nonce log for at least the duration of their presentation validity window to prevent replay.

### 14.4 Attestation Freshness

An attestation with a past `validUntil` is stale but NOT automatically revoked. Verifiers MUST surface staleness and MUST NOT silently accept stale attestations as current. Whether staleness is disqualifying is application-layer policy.

### 14.5 Issuer Key Compromise

If an issuer's private key is compromised, all credentials previously issued by that issuer become untrustworthy. The issuer MUST publish a KeyDocument revocation immediately. Verifiers will detect `keyStatus: "revoked"` and report `ATTESTATION_ISSUER_KEY_REVOKED`.

### 14.6 Holder Key Compromise

If the holder's private key is compromised, the attacker can publish fraudulent passport versions. The holder MUST immediately publish a KeyDocument revocation and rotate to a new keypair. A new Slot Blinding Key is automatically derived from the new signing key (§13.5), severing token continuity from the compromised key period.

### 14.7 P-256 Determinism Requirement

When using P-256 (ECDSA), implementations MUST use deterministic ECDSA per RFC 6979. Non-deterministic ECDSA (using a random nonce k) is prohibited. The prohibition exists because: (1) HIRI's determinism invariant (v3.1.1 §4.3) requires identical inputs to produce identical outputs; (2) non-deterministic ECDSA has historically been a source of catastrophic key leakage when k values are reused or weakly generated. Implementations MUST reject P-256 signatures produced by non-RFC-6979-compliant signers.

### 14.8 Coercion Resistance

The Minimum Disclosure Surface principle (§4.7) and the holder-discretion language in §11.5 establish that the protocol defaults to minimum disclosure and that the holder may decline a completeness audit. However, **cryptographic protocols cannot enforce off-band behavior or human compliance under social, economic, or institutional pressure.**

A verifier — an employer, a border authority, a financial institution, or any other party holding power over the holder — may demand a completeness audit as a precondition for access and simply reject presentations without it. The protocol cannot prevent this. The holder who declines may be denied employment, entry, or services. The specification's defaults are meaningless against a verifier who controls what the holder needs.

This is not a flaw unique to this specification. It is a fundamental limitation shared by all selective disclosure credential systems, including W3C Verifiable Credentials with selective disclosure, ISO mDL (ISO/IEC 18013-5), and similar frameworks. The protocol provides the technical means for minimum disclosure; the legal and institutional environment determines whether that minimum can be maintained in practice.

**For implementers and policy framers:** The most effective coercion resistance mechanisms are external to the protocol — statutory data minimization requirements, regulatory enforcement of proportionate disclosure standards, and institutional policies that prohibit demanding completeness audits for standard credential verification. Implementations SHOULD surface the completeness audit request to the holder with clear language about what will be disclosed and who will receive it, and SHOULD log the verifier's authority when a completeness audit is requested, providing an audit trail for regulatory review.

**For holders:** The default presentation (`omittedSlotCount` only) is the strongest privacy posture the protocol can achieve. A holder who declines a completeness audit has exercised the full extent of their protocol-layer privacy rights. Whether that refusal has consequences is determined by the institutional context, not the cryptographic mechanism.

### 14.9 Completeness Audit Risks

When a holder complies with a `completenessAudit: true` request, the resulting `withheldSlotSummary` discloses the number and types of credentials the holder possesses beyond what was requested. This is a deliberate privacy trade-off that requires explicit holder consent (§11.5). Holder software MUST NOT automate completeness audit compliance and MUST present the request explicitly to the holder, including a description of what will be disclosed and to whom.

### 14.10 Blinding Key Storage

The Slot Blinding Key (§11.7.2) is a long-lived secret. Its compromise allows an adversary to correlate presentation slot tokens across sessions by computing `HMAC-SHA256(slotBlindingKey, slotId || 0x00 || nonce || 0x00 || verifierAuthority)` for known nonces and verifier authorities. Holder software MUST store the blinding key with at least the same protection level as the passport signing key — preferably in a hardware-backed keystore where available.

---

## 15. Conformance Levels

### 15.1 Level Definitions

| Level | Signing | Canonicalization | Addressing | KeyDocument | Revocation Log | Org Bootstrap | DNSSEC | Slot Limit |
|-------|---------|-----------------|------------|-------------|----------------|---------------|--------|------------|
| **Passport-Core** | Ed25519 (REQUIRED) | JCS | raw-sha256 | SHOULD | Not required | Not required | Not required | 50 |
| **Passport-Interoperable** | Ed25519 (REQUIRED), P-256 (OPTIONAL) | JCS + URDNA2015 | raw-sha256 + cidv1-dag-cbor | **MUST** | RECOMMENDED | HTTPS domain binding | Not required | 200 |
| **Passport-Full** | Ed25519 (REQUIRED), P-256 (OPTIONAL) | JCS + URDNA2015 | raw-sha256 + cidv1-dag-cbor | **MUST** | **MUST** | HTTPS + **DNSSEC** | **REQUIRED** for `"full"` org trust | 500 |

### 15.2 Mandatory Baseline Requirements (All Levels)

Regardless of conformance level, all implementations MUST:

- Implement presentation slot blinding (§11.7) and nonce validation (§11.2)
- Implement the Tier 2 Override rule (§12.4)
- Implement the offline decision table (§12.7) — `"unknown"` MUST NOT be treated as passing
- Default presentations to `omittedSlotCount` only (§11.5)
- Reject presentations containing raw `slotId` values (`PRESENTATION_SLOT_NOT_BLINDED`)
- Reject presentations whose nonce does not conform to the 32-byte CSPRNG base64url encoding requirement

### 15.3 Passport-Core Requirements

- REQUIRED: Ed25519 signatures and JCS canonicalization
- REQUIRED: `raw-sha256` content addressing
- REQUIRED: Slot blinding, nonce validation, Tier 2 Override, offline decision table
- REQUIRED: Maximum 50 active slots
- SHOULD: Publish holder and issuer KeyDocuments
- NOT REQUIRED: Revocation log, DNSSEC, selective disclosure proof verification

### 15.4 Passport-Interoperable Requirements

All Passport-Core requirements, plus:

- REQUIRED: URDNA2015 canonicalization
- REQUIRED: `cidv1-dag-cbor` content addressing
- REQUIRED: Holder and issuer KeyDocuments published and resolvable (§6.4)
- REQUIRED: Selective disclosure proof verification (HMAC suite, Privacy Extension §8)
- REQUIRED: Phase 4 organizational authority bootstrap (§12.5) with HTTPS domain binding
- RECOMMENDED: Revocation log integration (Phase 3 Step 11)
- RECOMMENDED: P-256 algorithm support for hardware-backed key compatibility
- REQUIRED: Maximum 200 active slots

### 15.5 Passport-Full Requirements

All Passport-Interoperable requirements, plus:

- REQUIRED: Revocation log integration (Phase 3 Step 11, §16)
- REQUIRED: DNSSEC verification for any `organizationTrustLevel: "full"` claim (§12.5)
- REQUIRED: BBS+ selective disclosure support (Privacy Extension §8.6.2) or documented migration plan
- REQUIRED: Full presentation protocol including blinding and completeness audit handling (§11)
- REQUIRED: Key lifecycle event handling — rotation, revocation, grace periods (v3.1.1 §13)
- REQUIRED: Oracle trust governance compliance (§17) for any deployment using biometric credential types
- REQUIRED: `proofArtifactRef` support with normative timeout/retry/caching (§G.7) for any deployment supporting biometric credential types
- REQUIRED: Maximum 500 active slots

### 15.6 Metadata Hardening Profile

Implementations MAY additionally claim **Passport-Hardened** by fully implementing Appendix J (Metadata Hardening Profile). The Passport-Hardened designation is additive — it can be combined with any of the three base conformance levels (e.g., "Passport-Full + Passport-Hardened"). See Appendix J for full requirements and §H.10 for normative test vectors.

**Passport-Hardened Required Fields (summary — see Appendix J for full normative text):**

| Requirement | Section | Test Vector |
|-------------|---------|-------------|
| `omittedSlotCount` padded to nearest multiple of Q=5 | §J.2 | §H.10.1 |
| `attestedAt` smeared to nearest calendar day (midnight UTC) | §J.3 | §H.10.2 |
| `validFrom`/`validUntil` smeared to nearest calendar month | §J.3 | §H.10.2 |
| Issuer authority obfuscated in `withheldSlotSummary` via HMAC token | §J.4 | §H.10.3 |
| Hash-only revocation log entries for sensitive credential types | §16.8 | §H.10.4 |
| Presentation timing jitter 0–500ms | §J.5 | Behavioral; not vector-testable |
| Profile declaration in presentation header | §J.6 | §H.10.5 |

All Passport conformance levels require the `withheldSlots` → `omittedSlotCount` default (§11.5) and Presentation Slot Blinding (§11.7). These are NOT optional at any level.

---

## 16. Revocation Transparency

### 16.1 Purpose

The Revocation Transparency mechanism provides an auditable, efficiently queryable record of credential revocations. It solves the revocation discovery problem: verifiers should not be required to walk every issuer's full attestation chain to discover whether a credential has been revoked. The transparency log is a signed, append-only structure that verifiers can query, cache, and audit independently.

This section is NORMATIVE for issuers and verifiers claiming Passport-Full conformance. It is RECOMMENDED for Passport-Interoperable.

### 16.2 RevocationLogEntry

When an issuer revokes a Credential Attestation Manifest (by publishing a revocation attestation version per §13.4), the issuer MUST also append a `RevocationLogEntry` to their Revocation Transparency Log.

#### 16.2.1 Mandatory Minimal Field Set

**NORMATIVE:** Every `RevocationLogEntry` MUST include the following fields and MUST NOT include any additional fields that contain personal information about the holder beyond what is listed below:

| Field | Required | Privacy Classification | Notes |
|-------|----------|----------------------|-------|
| `@context` | REQUIRED | Non-personal | |
| `@type` | REQUIRED | Non-personal | |
| `issuerAuthority` | REQUIRED | Issuer identity | |
| `manifestHash` | REQUIRED | Pseudonymous | Hash of revoked manifest; used for lookup |
| `logSequenceNumber` | REQUIRED | Non-personal | Assigned by log server |
| `revokedAt` | REQUIRED | Temporal metadata | ISO 8601 timestamp |
| `revocationReason` | REQUIRED | Operational | See reason codes below |
| `signature` | REQUIRED | Non-personal | |
| `holderAuthority` | OPTIONAL | Holder pseudonym | See §16.2.2 privacy note |
| `manifestVersion` | OPTIONAL | Operational | |
| `credentialType` | OPTIONAL | Sensitive — see §16.2.2 | MUST be omitted in privacy-preserving mode |

The `holderAuthority` and `credentialType` fields are OPTIONAL precisely because they may leak sensitive information when the log is publicly readable. See §16.8 for the hash-only revocation mode.

```json
{
  "@context": [
    "https://hiri-protocol.org/spec/v3.1",
    "https://hiri-protocol.org/passport/v1"
  ],
  "@type": "hiri:RevocationLogEntry",
  "issuerAuthority": "key:ed25519:z<issuer-authority>",
  "manifestHash": "sha256:e08da327...",
  "revokedAt": "2026-04-01T10:00:00Z",
  "revocationReason": "holder-key-recovery",
  "logSequenceNumber": 1247,
  "signature": {
    "type": "Ed25519Signature2020",
    "algorithm": "ed25519",
    "verificationMethod": "hiri://key:ed25519:z<issuer-authority>/key/main#key-1",
    "proofValue": "z..."
  }
}
```

**`manifestHash`** — The content hash of the specific Credential Attestation Manifest version being revoked. Verifiers query by this value. This is the primary lookup key; all other fields are metadata.

**`logSequenceNumber`** — A monotonically increasing integer assigned by the log server at the time of append. Verifiers use this to detect gaps and verify ordering.

**`revocationReason`** — REQUIRED. One of: `"holder-key-recovery"`, `"credential-expired"`, `"issuer-policy"`, `"fraud-detected"`, `"holder-request"`, `"oracle-notification"`, `"other"`. Verifiers MUST surface this to relying parties.

The entry is signed by the issuer's current signing key. The signature covers all fields including `logSequenceNumber`. Verifiers MUST verify this signature before accepting an entry as authentic.

#### 16.2.2 Privacy Note on Optional Fields

**`credentialType`** reveals what kind of credential was revoked. For sensitive types (`GovernmentIdVerification`, `BackgroundCheckClearance`, `BiometricBoundCredential`), publishing `credentialType` in a public log allows observers to infer that a specific issuer authority has revoked a sensitive credential — and when combined with `holderAuthority`, potentially identifies the holder's credential portfolio structure.

**NORMATIVE for sensitive credential types:** Issuers revoking credentials of type `GovernmentIdVerification`, `BackgroundCheckClearance`, or `BiometricBoundCredential` MUST either (a) use the hash-only revocation mode (§16.8), or (b) omit `credentialType` and `holderAuthority` from the plaintext entry and use a sealed disclosure mechanism on request.

### 16.3 RevocationCheckpoint

The Revocation Transparency Log MUST publish a signed **RevocationCheckpoint** (signed tree head) at intervals not exceeding **1 hour**. The checkpoint commits to the state of the log at a specific tree size and timestamp.

```json
{
  "@type": "hiri:RevocationCheckpoint",
  "logAuthority": "key:ed25519:z<log-authority>",
  "treeSize": 1247,
  "rootHash": "sha256:f2a4c8e1...",
  "previousCheckpointHash": "sha256:a1b2c3d4...",
  "timestamp": "2026-04-01T12:00:00Z",
  "signature": {
    "type": "Ed25519Signature2020",
    "algorithm": "ed25519",
    "verificationMethod": "hiri://key:ed25519:z<log-authority>/key/main#key-1",
    "proofValue": "z..."
  }
}
```

**`rootHash`** — The Merkle root of all log entries at `treeSize`, computed per the canonicalization algorithm defined in §16.10. Inclusion proofs for specific entries are verifiable against this root.

**`previousCheckpointHash`** — SHA-256 hash of the JCS-canonicalized previous checkpoint (excluding this field). Verifiers detecting a gap in the checkpoint chain MUST treat the log as potentially compromised and MUST report `REVOCATION_LOG_CHECKPOINT_CHAIN_GAP`.

**Checkpoint publication interval (NORMATIVE):** Log operators MUST publish a new checkpoint at intervals not exceeding 1 hour. A log that has not published a checkpoint within 2 hours MUST be treated by verifiers as degraded; verifiers SHOULD surface a warning and downgrade revocation state to `"unknown"` for entries newer than the last valid checkpoint.

**Checkpoint caching and staleness windows (NORMATIVE):**

| Transaction Class | Maximum Checkpoint Age | On Exceeded |
|-------------------|----------------------|-------------|
| `high-value` | **15 minutes** | MUST reject; report `REVOCATION_LOG_STALE_HIGH_VALUE` |
| `standard` (default) | **48 hours** | MUST report `revocationLogStatus: "cached-checkpoint"`; verifier MAY accept |
| Offline (no network) | 48 hours from last fetch | MUST report `revocationLogStatus: "cached-checkpoint"` |
| Offline, no checkpoint | — | MUST report `revocationLogStatus: "unknown"`; MUST NOT accept as valid |

After the applicable staleness window expires, the checkpoint is expired and revocation state is `"unknown"`. Implementations MUST enforce these values. They are not configurable defaults — they are normative ceilings. A verifier MAY use a fresher requirement than the ceiling but MUST NOT use a staler one.

### 16.4 Log API

Revocation Transparency Logs MUST expose the following three endpoints. The base URL is declared in the issuer's KeyDocument `organizationalIdentity.revocationLogURI` field and in the OracleGovernanceDocument (§17.2) for oracle logs.

#### 16.4.1 GET /hiri/v1/revocation/checkpoint

Returns the latest signed `RevocationCheckpoint`.

```
GET /hiri/v1/revocation/checkpoint
Accept: application/json

Response 200:
{
  "checkpoint": { ...RevocationCheckpoint... },
  "entrySinceLastCheckpoint": 12
}
```

Verifiers MUST verify the checkpoint signature before caching.

#### 16.4.2 GET /hiri/v1/revocation/entry/{manifestHash}

Queries whether a specific manifest hash has a revocation entry. Returns the entry and a Merkle inclusion proof if found.

```
GET /hiri/v1/revocation/entry/sha256:e08da327...
Accept: application/json

Response 200 (entry found):
{
  "found": true,
  "entry": { ...RevocationLogEntry... },
  "inclusionProof": {
    "treeSize": 1247,
    "leafIndex": 983,
    "auditPath": ["sha256:...", "sha256:...", "..."]
  }
}

Response 200 (entry not found):
{
  "found": false,
  "checkpointAtQuery": { ...RevocationCheckpoint... }
}
```

When no entry is found, the response includes the checkpoint at query time. Verifiers MUST verify that the checkpoint is fresh (within the staleness window) before treating the absence as `"confirmed-valid"`.

#### 16.4.3 POST /hiri/v1/revocation/append

Issuers append revocation entries. The request body is a signed `RevocationLogEntry`. The log server verifies the issuer's authentication credentials and entry signature, assigns `logSequenceNumber`, and returns the Merkle inclusion proof.

**Authentication (NORMATIVE):** Opaque bearer tokens alone are NOT sufficient for /append authentication. Log servers MUST support at least one of the following two authentication mechanisms:

**Option A — Mutual TLS with issuer-authority-bound client certificate:**

The TLS client certificate presented by the issuer MUST include the issuer's HIRI authority string in the Subject Alternative Name (SAN) extension as a URI SAN:

```
SAN URI: hiri://key:ed25519:z<issuer-authority>
```

The log server MUST verify that the SAN URI in the client certificate matches the `issuerAuthority` field in the `RevocationLogEntry` body. Certificates MUST be issued by a CA whose root is configured in the log server's trust store. Self-signed client certificates MUST NOT be accepted.

**Option B — Signed JWT issued by an OIDC management plane:**

The issuer obtains a short-lived JWT from an OIDC-compatible management plane. The JWT MUST include:

```json
{
  "sub": "key:ed25519:z<issuer-authority>",
  "aud": "https://<log-server-domain>/hiri/v1/revocation",
  "iss": "https://<oidc-management-plane>",
  "hiri_authority": "key:ed25519:z<issuer-authority>",
  "exp": "<unix timestamp, max 300s from iat>"
}
```

The log server MUST verify the JWT signature against the OIDC management plane's published JWKS, MUST verify the `hiri_authority` claim matches the `issuerAuthority` in the entry body, and MUST verify that the JWT has not expired.

In both options, the log server MUST additionally verify the `RevocationLogEntry.signature` as a second independent check. The transport-layer authentication (mTLS or JWT) proves who is connecting; the entry-level signature proves the entry content was authorized by the issuer's HIRI signing key.

```
POST /hiri/v1/revocation/append
Content-Type: application/json
Authorization: Bearer <signed-jwt>    [Option B]
              (or mTLS client cert)   [Option A]

Body: { ...RevocationLogEntry (without logSequenceNumber)... }

Response 201:
{
  "logSequenceNumber": 1248,
  "inclusionProof": {
    "treeSize": 1248,
    "leafIndex": 1247,
    "auditPath": [
      {"hash": "sha256:aabbcc...", "side": "right"},
      {"hash": "sha256:ddeeff...", "side": "left"}
    ]
  },
  "updatedCheckpoint": { ...RevocationCheckpoint... }
}

Response 401: Authentication failed (mTLS handshake error or JWT invalid)
Response 403: issuerAuthority in entry does not match authenticated identity
Response 409: Duplicate manifestHash already in log
Response 429: Rate limit exceeded
```

The `inclusionProof.auditPath` format is normative — each element is a `{hash, side}` object where `side` is `"left"` or `"right"` indicating which side of the tree node the sibling is on. See §16.10 for the full Merkle tree canonicalization and proof verification algorithm.

### 16.5 Log Operator Declaration

Issuers MUST declare their revocation log endpoint in their KeyDocument:

```json
{
  "organizationalIdentity": {
    "displayName": "EcoImpact Consulting",
    "domain": "ecoimpact.com",
    "revocationLogURI": "https://ecoimpact.com/hiri/v1/revocation",
    "revocationLogAuthority": "key:ed25519:z<log-authority>"
  }
}
```

An issuer MAY operate their own log or delegate to a shared log service. The `revocationLogAuthority` identifies the keypair that signs checkpoints — it MAY differ from the issuer's credential-signing authority.

### 16.6 Shared Log Services (INFORMATIVE)

Issuers with low revocation volume SHOULD use a shared Revocation Transparency Log service rather than operating their own. A shared log pools multiple issuers' revocation entries into a single auditable structure. Verifiers querying a shared log obtain revocation state for multiple issuers in a single checkpoint fetch, reducing per-verification network overhead.

Shared log services MUST publish their own KeyDocument and SHOULD publish an OracleGovernanceDocument (§17.2) declaring their operation policies. Verifiers SHOULD configure shared log authorities in their trust policy.

### 16.7 Log Operator Security Requirements

This section is NORMATIVE for any entity operating a Revocation Transparency Log as part of a Passport-Full or Passport-Hardened deployment.

#### 16.7.1 Signing Key Protection

Log checkpoint signing keys MUST be stored in hardware security modules (HSMs) or equivalent hardware-backed key storage. Software-only key storage is NOT acceptable for log authorities serving Passport-Full deployments.

Log signing keys MUST be dedicated keys — they MUST NOT be shared with or derived from issuer credential-signing keys or oracle signing keys. Each role has its own distinct keypair.

Log signing key rotation MUST occur at least every 365 days and MUST follow the HIRI key rotation procedure (v3.1.1 §13). A new checkpoint published after key rotation MUST be signed with the new key, and the KeyDocument MUST reflect the updated active key before the old key is decommissioned.

#### 16.7.2 Append Authorization Audit Trail

Every successful /append request MUST be logged in an append-only audit trail with:

- Timestamp of the request
- Authenticated identity of the requester (mTLS certificate fingerprint or JWT `sub`)
- `manifestHash` of the appended entry
- `logSequenceNumber` assigned
- Source IP address

This audit trail MUST be retained for a minimum of 7 years. The audit trail itself SHOULD be stored in a separate system from the log, with independent access controls.

#### 16.7.3 Rate Limiting and DDoS Resilience

Log servers MUST enforce per-issuer rate limits on /append requests. RECOMMENDED limits:

- Maximum 100 append requests per issuer per hour
- Maximum burst of 10 append requests per issuer per minute
- Maximum 10,000 total append requests per day across all issuers (scale as needed)

Log servers MUST implement DDoS resilience for the public GET endpoints (/checkpoint and /entry/{manifestHash}), as these are expected to receive verifier traffic at scale. RECOMMENDED mitigations: CDN with caching for checkpoint responses, rate limiting per IP for entry queries.

Rate limit responses MUST use HTTP 429 with a `Retry-After` header. Verifiers receiving 429 MUST honor the `Retry-After` value before retrying.

#### 16.7.4 Entry Deduplication

Log servers MUST reject /append requests for a `manifestHash` that is already present in the log (HTTP 409). Duplicate entries for the same manifest hash are a protocol error — a credential's revocation is an idempotent fact, and multiple entries would corrupt the tree size accounting.

### 16.8 Privacy-Preserving Revocation Mode

This section defines an OPTIONAL privacy-preserving revocation mode for sensitive credential types. It is REQUIRED for issuers revoking credentials of type `GovernmentIdVerification`, `BackgroundCheckClearance`, or `BiometricBoundCredential` (per §16.2.2).

#### 16.8.1 Hash-Only Log Entries

In privacy-preserving mode, the issuer computes:

```
entryHash = SHA-256(JCS(fullRevocationLogEntry))
```

Where `fullRevocationLogEntry` is the complete `RevocationLogEntry` object (including all optional fields). The issuer then appends a **Hash-Only Revocation Entry** to the public log:

```json
{
  "@type": "hiri:HashOnlyRevocationEntry",
  "issuerAuthority": "key:ed25519:z<issuer-authority>",
  "entryHash": "sha256:3f7a9c2e...",
  "revokedAt": "2026-04-01T10:00:00Z",
  "logSequenceNumber": 1249,
  "signature": {
    "type": "Ed25519Signature2020",
    "algorithm": "ed25519",
    "verificationMethod": "hiri://key:ed25519:z<issuer-authority>/key/main#key-1",
    "proofValue": "z..."
  }
}
```

The public log contains only the `entryHash` — no `manifestHash`, no `credentialType`, no `holderAuthority`. An observer of the public log learns: this issuer revoked something at this time. They learn nothing about what was revoked or whose credential it was.

#### 16.8.2 Verification with Hash-Only Entries

Verifiers querying `GET /entry/{manifestHash}` for a hash-only log entry follow this flow:

1. The log server cannot directly look up by `manifestHash` in hash-only mode. The issuer MUST maintain a private index mapping `manifestHash → entryHash` and MUST operate a **selective reveal endpoint** at `GET /hiri/v1/revocation/reveal/{manifestHash}`.

2. The selective reveal endpoint returns the full plaintext `RevocationLogEntry` and the Merkle inclusion proof for the corresponding `entryHash`.

3. The verifier computes `SHA-256(JCS(returnedEntry))` and confirms it equals the `entryHash` in the inclusion proof.

4. The verifier confirms the inclusion proof is valid against the current checkpoint's `rootHash`.

**Access control for selective-reveal endpoints (NORMATIVE):** The selective reveal endpoint MUST NOT be publicly accessible without authentication. Issuers operating selective-reveal endpoints MUST implement one of the following access control patterns:

**Pattern A — Holder consent proof:** The verifier presents a signed nonce from the holder proving the holder authorized this specific reveal request. The nonce is bound to the verifier's authority and the disclosure request ID:

```json
{
  "holderConsentProof": {
    "holderAuthority": "key:ed25519:z<holder-authority>",
    "verifierAuthority": "key:ed25519:z<verifier-authority>",
    "disclosureRequestId": "req:2026-04-01-001",
    "manifestHash": "sha256:e08da327...",
    "expiresAt": "2026-04-01T11:00:00Z",
    "signature": { "...": "holder's Ed25519 signature" }
  }
}
```

The selective-reveal endpoint MUST verify the holder's signature and MUST reject requests with expired `expiresAt`.

**Pattern B — Verifier registration:** The issuer maintains a registry of verifiers authorized to request selective reveals for credentials they have verified in Phase 3. Verifiers authenticate using the same mTLS or signed JWT mechanism as the /append endpoint (§16.4.3).

**Minimal logging requirements (NORMATIVE):** The selective-reveal endpoint MUST log each successful reveal with: request timestamp, verifier identity, `manifestHash` revealed, and whether a holder consent proof was presented. This audit trail MUST be retained for the same duration as the issuer's revocation log entries (minimum 7 years). The audit log MUST NOT record the full plaintext RevocationLogEntry content in the access log — only the metadata listed above. Full entry content is the responsibility of the log storage system, not the access log.

#### 16.8.3 Passport-Hardened Requirement

Deployments claiming the Passport-Hardened designation (§15.6, Appendix J) MUST use hash-only revocation entries for all credential types listed in §16.2.2 AND MUST implement Appendix J's metadata hardening for any revocation log query metadata exposed to verifiers.

### 16.9 Revocation Acceptance Windows and Race Condition Handling

#### 16.9.1 TransactionClass Parameter

Verifiers MUST declare a `transactionClass` when invoking revocation log state determination (Phase 3 Step 11). The `transactionClass` determines the maximum acceptable checkpoint age:

| `transactionClass` | Maximum Checkpoint Age | Typical Use Case |
|-------------------|----------------------|-----------------|
| `"high-value"` | 15 minutes | Government ID verification, financial access, security clearance |
| `"standard"` (default) | 48 hours | Employment verification, professional certifications |

If no `transactionClass` is declared, `"standard"` applies. Verifiers MUST NOT allow application-layer configuration to weaken these bounds (e.g., a relying party MUST NOT instruct a verifier to treat a 72-hour checkpoint as valid for a `"standard"` transaction).

#### 16.9.2 Race Condition: Post-Checkpoint Revocation

A race condition occurs when an issuer appends a revocation entry to the log after the verifier fetches its checkpoint but before the verifier completes verification. The verifier holds a valid checkpoint showing no revocation; the log now contains a revocation entry not yet reflected in the cached checkpoint.

**NORMATIVE mitigation:** For `"high-value"` transactions, verifiers MUST query the live log endpoint (`GET /entry/{manifestHash}`) directly at verification time — checkpoint-only verification is NOT sufficient. The live query must return a response; a 429 or timeout downgrade the revocation state to `"unknown"`.

For `"standard"` transactions, checkpoint-based verification is acceptable. The inherent race window is bounded by the checkpoint interval (maximum 1 hour).

#### 16.9.3 Retroactive Revocation Detection

If a verifier later discovers (e.g., via an updated checkpoint) that a credential it previously accepted as valid was revoked at the time of acceptance, the verifier SHOULD:

1. Record the retroactive revocation in its local audit trail with the discovery timestamp and the credential details.
2. Surface a notification to the relying party if the acceptance event is within the relying party's audit window.
3. NOT re-verify presentations that have already been accepted — the retroactive discovery is an audit event, not a grounds for retroactive rejection.

### 16.10 Merkle Tree Canonicalization

This section is NORMATIVE. Two independent log implementations MUST produce identical Merkle roots for the same sequence of entries. The following algorithm is the canonical definition.

#### 16.10.1 Leaf Hash Computation

```
leafHash(entry) = SHA-256(JCS(entry))
```

Where:
- `entry` is the complete `RevocationLogEntry` object (or `HashOnlyRevocationEntry` in privacy-preserving mode)
- `JCS(entry)` is the deterministic UTF-8 byte sequence produced by RFC 8785 (JSON Canonicalization Scheme) applied to the entry object
- `SHA-256` is the standard SHA-256 hash function producing a 32-byte digest

The `logSequenceNumber` field MUST be included in the entry before computing the leaf hash. Entries appended without `logSequenceNumber` (e.g., in the /append request body) MUST have the server-assigned `logSequenceNumber` added before leaf hash computation.

#### 16.10.2 Interior Node Hash Computation

```
nodeHash(left, right) = SHA-256(left || right)
```

Where:
- `left` and `right` are 32-byte hash values (either leaf hashes or interior node hashes)
- `||` denotes byte concatenation
- The left child is always the node with the lower index range

For trees with an odd number of leaves at any level, the rightmost leaf is promoted to the next level without modification (no duplication):

```
Level 0 (leaves): [h0, h1, h2, h3, h4]
Level 1:          [node(h0,h1), node(h2,h3), h4]
Level 2:          [node(node(h0,h1), node(h2,h3)), h4]
Root:             node(node(node(h0,h1), node(h2,h3)), h4)
```

#### 16.10.3 Inclusion Proof Format

An inclusion proof for a leaf at index `i` in a tree of size `n` is an ordered array of `{hash, side}` objects. Each object represents a sibling node needed to reconstruct the root:

```json
{
  "leafIndex": 2,
  "treeSize": 5,
  "auditPath": [
    {"hash": "sha256:aabbcc...", "side": "right"},
    {"hash": "sha256:ddeeff...", "side": "left"},
    {"hash": "sha256:112233...", "side": "right"}
  ]
}
```

**Proof verification algorithm:**

```
currentHash = leafHash(entry)
for each {hash, side} in auditPath:
  if side == "left":
    currentHash = nodeHash(hash, currentHash)
  else:
    currentHash = nodeHash(currentHash, hash)
assert currentHash == checkpoint.rootHash
```

Both `hash` values are lowercase hex-encoded 32-byte SHA-256 digests prefixed with `"sha256:"`. Implementations MUST reject proof paths that produce a root hash not matching the checkpoint.

#### 16.10.4 Worked Example: 3-Leaf Tree (Hex)

This example uses minimal, fixed-content entries to allow independent verification. All SHA-256 values are shown as full 32-byte hex.

**Leaf entries (before JCS canonicalization):**

```
Entry 0: {"@type":"hiri:RevocationLogEntry","issuerAuthority":"key:ed25519:zA","logSequenceNumber":0,"manifestHash":"sha256:aa","revokedAt":"2026-01-01T00:00:00Z","revocationReason":"holder-request"}

Entry 1: {"@type":"hiri:RevocationLogEntry","issuerAuthority":"key:ed25519:zB","logSequenceNumber":1,"manifestHash":"sha256:bb","revokedAt":"2026-01-02T00:00:00Z","revocationReason":"issuer-policy"}

Entry 2: {"@type":"hiri:RevocationLogEntry","issuerAuthority":"key:ed25519:zC","logSequenceNumber":2,"manifestHash":"sha256:cc","revokedAt":"2026-01-03T00:00:00Z","revocationReason":"fraud-detected"}
```

**Step 1 — JCS canonical bytes (keys sorted lexicographically, no whitespace):**

```
JCS(Entry 0) = {"@type":"hiri:RevocationLogEntry","issuerAuthority":"key:ed25519:zA","logSequenceNumber":0,"manifestHash":"sha256:aa","revokedAt":"2026-01-01T00:00:00Z","revocationReason":"holder-request"}

JCS(Entry 1) = {"@type":"hiri:RevocationLogEntry","issuerAuthority":"key:ed25519:zB","logSequenceNumber":1,"manifestHash":"sha256:bb","revokedAt":"2026-01-02T00:00:00Z","revocationReason":"issuer-policy"}

JCS(Entry 2) = {"@type":"hiri:RevocationLogEntry","issuerAuthority":"key:ed25519:zC","logSequenceNumber":2,"manifestHash":"sha256:cc","revokedAt":"2026-01-03T00:00:00Z","revocationReason":"fraud-detected"}
```

**Step 2 — Leaf hashes (SHA-256 of JCS bytes):**

```
h0 = SHA-256(JCS(Entry 0))
   = [pin from reference implementation — placeholder: e3b0c44298fc1c14...]

h1 = SHA-256(JCS(Entry 1))
   = [pin from reference implementation]

h2 = SHA-256(JCS(Entry 2))
   = [pin from reference implementation]
```

**Step 3 — Tree construction (3 leaves; leaf 2 is unpaired at level 1):**

```
Level 0:  [h0,       h1,       h2]
Level 1:  [n01,               h2 ]   n01 = SHA-256(h0 || h1)
Root:     SHA-256(n01 || h2)
```

**Step 4 — Inclusion proof for Entry 1 (leafIndex=1):**

```json
{
  "leafIndex": 1,
  "treeSize": 3,
  "auditPath": [
    {"hash": "sha256:<h0>",  "side": "left"},
    {"hash": "sha256:<h2>",  "side": "right"}
  ]
}
```

**Verification:**
```
currentHash = h1
Step 1: side=left  → currentHash = SHA-256(h0 || currentHash) = n01
Step 2: side=right → currentHash = SHA-256(currentHash || h2) = root
assert currentHash == checkpoint.rootHash  → PASS
```

**Inclusion proof for Entry 2 (leafIndex=2, unpaired leaf):**

```json
{
  "leafIndex": 2,
  "treeSize": 3,
  "auditPath": [
    {"hash": "sha256:<n01>", "side": "left"}
  ]
}
```

**Verification:**
```
currentHash = h2
Step 1: side=left → currentHash = SHA-256(n01 || currentHash) = root
assert currentHash == checkpoint.rootHash  → PASS
```

**Implementation test:** Compute `h0`, `h1`, `h2`, `n01`, and `root` from the JCS canonical bytes above. Pin the hex values in the reference implementation test suite. Any independent implementation processing the same entries MUST produce byte-identical hash values at every level.

---

## 17. Oracle Trust Governance

### 17.1 Purpose

Appendix G defines three biometric network integration patterns, all of which depend on external oracle authorities. The quality of the Sybil-resistance guarantee (§G.2), the holder-to-credential binding (§G.3), and the key recovery mechanism (§G.4) are only as strong as the trustworthiness of the oracle issuing the relevant credentials.

This section is NORMATIVE for any deployment implementing biometric credential types (`ProofOfUniqueHumanCredential`, `BiometricBoundCredential`, `KeyContinuityAttestation`). It provides concrete governance requirements that make oracle trust auditable and reduces hidden centralization risk.

### 17.2 OracleGovernanceDocument

Every oracle authority claiming a trust level above `"partial"` MUST publish a signed `hiri:OracleGovernanceDocument` at:

```
https://<oracle-domain>/.well-known/hiri-oracle-governance.json
```

```json
{
  "@context": [
    "https://hiri-protocol.org/spec/v3.1",
    "https://hiri-protocol.org/passport/v1"
  ],
  "@type": "hiri:OracleGovernanceDocument",
  "oracleAuthority": "key:ed25519:z<oracle-authority>",
  "oracleDomain": "biometric-oracle.example.com",
  "operatorIdentity": {
    "legalName": "BiometricNet Foundation",
    "jurisdiction": "CH",
    "registrationNumber": "CHE-123.456.789",
    "contactURI": "https://biometric-oracle.example.com/contact"
  },
  "keyManagementPolicy": {
    "hsmRequired": true,
    "keyRotationPeriod": "P365D",
    "multiPartySigningRequired": false,
    "auditableKeyStorage": true
  },
  "auditPolicy": {
    "auditSchedule": "annual",
    "lastAuditDate": "2026-01-15",
    "auditReportURI": "https://biometric-oracle.example.com/audit/2026",
    "auditorName": "CryptoAudit AG"
  },
  "transparencyLog": {
    "oracleActionLogURI": "https://biometric-oracle.example.com/hiri/v1/oracle-log",
    "logAuthority": "key:ed25519:z<log-authority>",
    "checkpointInterval": "PT1H"
  },
  "biometricModalities": ["iris", "face"],
  "registryTechnology": "ZK-Merkle-inclusion",
  "governanceVersion": "1.0.0",
  "validUntil": "2027-04-01T00:00:00Z",
  "signature": {
    "type": "Ed25519Signature2020",
    "algorithm": "ed25519",
    "verificationMethod": "hiri://key:ed25519:z<oracle-authority>/key/main#key-1",
    "proofValue": "z..."
  }
}
```

#### 17.2.1 Required Fields

| Field | Required | Notes |
|-------|----------|-------|
| `oracleAuthority` | REQUIRED | MUST match the oracle's HIRI authority |
| `oracleDomain` | REQUIRED | MUST match the domain serving this document |
| `operatorIdentity.legalName` | REQUIRED | Legal entity name |
| `operatorIdentity.jurisdiction` | REQUIRED | ISO 3166-1 alpha-2 country code |
| `keyManagementPolicy.hsmRequired` | REQUIRED | Whether HSM is required for oracle signing keys |
| `auditPolicy.auditSchedule` | REQUIRED | One of: `"annual"`, `"semi-annual"`, `"quarterly"` |
| `transparencyLog.oracleActionLogURI` | REQUIRED | URI of oracle action log |
| `biometricModalities` | REQUIRED | Array of modalities the oracle supports |
| `validUntil` | REQUIRED | ISO 8601 timestamp; governance document must be renewed before expiry |
| `signature` | REQUIRED | Oracle authority's signature over the document |

### 17.3 Verifier Trust Anchor Configuration

Verifiers MUST maintain a configured set of **Oracle Trust Anchors** before enabling any biometric credential type verification. An Oracle Trust Anchor entry specifies:

```json
{
  "oracleTrustAnchors": [
    {
      "oracleAuthority": "key:ed25519:z<oracle-authority>",
      "oracleDomain": "biometric-oracle.example.com",
      "governanceDocumentURI": "https://biometric-oracle.example.com/.well-known/hiri-oracle-governance.json",
      "governanceDocumentHash": "sha256:a1b2c3...",
      "acceptedTrustLevel": "full",
      "acceptedCredentialTypes": [
        "ProofOfUniqueHumanCredential",
        "KeyContinuityAttestation"
      ],
      "addedAt": "2026-03-15T00:00:00Z",
      "expiresAt": "2027-04-01T00:00:00Z"
    }
  ]
}
```

**`governanceDocumentHash`** — SHA-256 hash of the governance document at the time of trust anchor creation. For oracles configured at `acceptedTrustLevel: "full"`, verifiers MUST re-validate the governance document hash at intervals not exceeding 30 days. If the governance document hash changes, the verifier MUST immediately downgrade the oracle to `"partial"` trust level and MUST require explicit re-confirmation (human or policy-level sign-off) before restoring `"full"` trust. For oracles at lower trust levels, re-validation is RECOMMENDED monthly.

**`acceptedCredentialTypes`** — The verifier's policy scopes each oracle's trust to specific credential types. A general-purpose biometric oracle trusted for `ProofOfUniqueHumanCredential` is NOT automatically trusted for `KeyContinuityAttestation` — that requires separate explicit configuration.

### 17.4 Trust Level Assignment Rules

| Oracle State | Effective Trust Level |
|-------------|----------------------|
| In trust anchor set, governance document valid, not expired, signed, hash matches | As configured in trust anchor |
| In trust anchor set, governance document expired | `"partial"` — surface warning |
| In trust anchor set, governance document hash mismatch | `"partial"` — surface warning, REQUIRED re-confirmation for `"full"` restoration |
| In trust anchor set, governance re-evaluation overdue (>30 days for `"full"` trust) | `"partial"` — surface warning |
| Not in trust anchor set | `"partial"` (MAXIMUM) — regardless of governance document claims |
| Governance document unavailable | `"partial"` if cached and within TTL; otherwise `"unverifiable"` |
| Oracle in quarantine (§17.7) | `"partial"` until quarantine lifted by explicit human review |

**NORMATIVE:** Verifiers MUST NOT assign `trustLevel: "full"` to any `KeyContinuityAttestation` or biometric credential issued by an oracle not present in the verifier's configured trust anchor set. The oracle may be entirely legitimate — but trust is established by verifier policy, not by oracle self-declaration.

### 17.5 Oracle Action Log

Oracles SHOULD publish an **Oracle Action Log** (a Revocation Transparency Log instance, §16, dedicated to oracle operations) recording all issued `ProofOfUniqueHumanCredential`, `BiometricBoundCredential`, and `KeyContinuityAttestation` manifests. This provides auditability: verifiers and auditors can confirm that an attestation was legitimately issued and detect unauthorized issuance.

The Oracle Action Log uses the same `RevocationCheckpoint` structure as the Revocation Transparency Log (§16.3). The log endpoint is declared in `transparencyLog.oracleActionLogURI` in the OracleGovernanceDocument.

### 17.6 Governance Failure Handling

When an oracle's governance document expires, its audit lapses, or its keys are compromised:

1. The oracle MUST publish a KeyDocument key revocation (v3.1.1 §13) immediately upon key compromise.
2. Verifiers with this oracle in their trust anchor set MUST downgrade to `"partial"` trust level upon detecting revocation.
3. Any `KeyContinuityAttestation` issued by a compromised oracle is treated as `trustLevel: "partial"` regardless of prior configuration.
4. Recovery requires the oracle to rotate keys, renew the governance document, and request re-enrollment in verifier trust anchor sets — there is no automatic restoration.

### 17.7 Oracle Incident Response

This section is NORMATIVE. It defines the required incident response procedures for oracle authorities and verifiers when an oracle security incident is detected.

#### 17.7.1 Incident Classification

| Incident Type | Severity | Required Response Time |
|-------------|----------|----------------------|
| Signing key compromise or suspected compromise | Critical | 1 hour maximum |
| Governance document unauthorized modification | Critical | 1 hour maximum |
| Oracle Action Log checkpoint chain gap | High | 4 hours maximum |
| Audit non-compliance (missed scheduled audit) | Medium | 30 days maximum |
| Governance document expiry without renewal | Medium | Immediate (governance document expired) |

#### 17.7.2 Phase 1 — Emergency Key Revocation (≤ 1 hour)

Upon detecting a critical incident, the oracle MUST within 1 hour:

1. Publish a KeyDocument key revocation for the compromised key (v3.1.1 §13). The revocation MUST be signed by an emergency revocation key that is pre-registered in the oracle's KeyDocument as a `"revocation-only"` key — a key whose sole authorized use is to sign revocations.

2. Publish a signed **OracleIncidentNotice** at `https://<oracle-domain>/.well-known/hiri-oracle-incident.json`:

```json
{
  "@type": "hiri:OracleIncidentNotice",
  "oracleAuthority": "key:ed25519:z<oracle-authority>",
  "incidentType": "key-compromise",
  "detectedAt": "2026-04-01T10:00:00Z",
  "affectedKeyId": "key:ed25519:z<compromised-key>",
  "affectedSince": "2026-03-01T00:00:00Z",
  "incidentStatement": "Unauthorized access to signing key detected via HSM audit log.",
  "contactURI": "https://biometric-oracle.example.com/incident",
  "signature": {
    "type": "Ed25519Signature2020",
    "verificationMethod": "hiri://key:ed25519:z<oracle-authority>/key/revocation#revocation-key-1",
    "proofValue": "z..."
  }
}
```

3. Notify all registered subscribers (per Oracle Notification Protocol, §G.4.5) of the incident, including the `affectedSince` timestamp allowing subscribers to identify which attestations were issued by the potentially compromised key.

#### 17.7.3 Phase 2 — Verifier Quarantine

Upon detecting an OracleIncidentNotice or a KeyDocument revocation from an oracle in their trust anchor set, verifiers MUST:

1. Immediately downgrade all attestations from the affected oracle authority to `"partial"` trust level (**Oracle Quarantine** state).
2. Surface the quarantine status to relying parties: `"oracle-quarantined"` as the `organizationTrustLevel` value.
3. Flag all previously accepted attestations from the affected oracle within the `affectedSince` window for human review. The verifier MUST NOT automatically re-verify or re-accept these attestations without a human review step.
4. Cease processing `KeyContinuityAttestation` credentials from the quarantined oracle until quarantine is lifted.

Quarantine MUST NOT be lifted automatically. It requires explicit human or policy-level re-confirmation after the oracle completes Phase 3.

#### 17.7.4 Phase 3 — Re-Key Procedure and Quarantine Lift

The oracle completes recovery through a structured re-key procedure:

1. **New key generation:** Generate a new Ed25519 (or P-256) signing keypair in a freshly audited HSM. Document the key generation ceremony with at least two independent witnesses.

2. **New governance document:** Publish an updated OracleGovernanceDocument referencing the new key. The `governanceVersion` MUST be incremented. The `lastAuditDate` MUST reflect a post-incident audit.

3. **Parallel operation minimum:** The oracle MUST operate both the old (compromised, now revoked) and new key infrastructure in parallel for a minimum of 30 days, issuing all new attestations with the new key while the old key's revocation propagates. This period allows verifiers to transition their trust anchor configurations.

4. **Verifier re-enrollment notification:** The oracle MUST publish a signed **OracleRecoveryNotice** at `https://<oracle-domain>/.well-known/hiri-oracle-recovery.json` declaring the incident closed, the new governance document hash, and the new key's active-since timestamp.

5. **Quarantine lift:** Verifiers MAY lift quarantine status for the oracle after verifying the OracleRecoveryNotice signature (signed by the new key), confirming the new governance document hash matches the OracleRecoveryNotice, and obtaining explicit policy approval. Quarantine lift is NEVER automatic.

---

## 18. HIRI as Integrity Layer

### 18.1 Architectural Principle

This section is NORMATIVE. It establishes the foundational separation of concerns between HIRI and external identity standards. All future extensions to this specification MUST respect this boundary.

**HIRI is responsible for:**

- **Artifact integrity** — cryptographic proof that an artifact has not been tampered with since it was signed
- **Artifact provenance** — cryptographic proof of which authority produced an artifact and when
- **Artifact packaging** — the manifest format, version chain, canonicalization, and content addressing mechanisms
- **Privacy-preserving disclosure** — selective disclosure, slot blinding, proof-of-possession, and the minimum disclosure surface principle

**External standards are responsible for:**

- **Identity semantics** — the meaning of identity claims, credential schemas, and vocabulary definitions (W3C VC, Schema.org, FOAF, vCard)
- **Identity identifiers** — the format and resolution of persistent identifiers (DIDs, domain names, government registry numbers)
- **Transport mechanisms** — how presentations are transmitted between parties (OID4VP, DIDComm, HTTPS, NFC, BLE, QR)
- **Discovery mechanisms** — how verifiers find holder and issuer identity information (DID resolution, `.well-known` endpoints, government registries)

### 18.2 The Layering Invariant

```
┌────────────────────────────────────────────────────┐
│  Application Layer                                  │
│  Authorization policies, trust frameworks,          │
│  legal recognition, business logic                  │
├────────────────────────────────────────────────────┤
│  Transport Layer                                    │
│  OID4VP, DIDComm, HTTPS, NFC, BLE, QR              │
│  (not defined by HIRI)                              │
├────────────────────────────────────────────────────┤
│  Identity Semantics Layer                           │
│  W3C VC, Schema.org, vCard, FOAF, DID methods       │
│  (optional compatibility via Appendix K bridges)    │
├────────────────────────────────────────────────────┤
│  HIRI Passport Layer          ◄── THIS SPEC         │
│  Credential slots, presentations, biometric         │
│  integration, revocation, oracle governance         │
├────────────────────────────────────────────────────┤
│  HIRI Protocol Layer                               │
│  Signing, verification, chain integrity,            │
│  canonicalization, key lifecycle                    │
│  (HIRI Protocol Spec v3.1.1)                        │
└────────────────────────────────────────────────────┘
```

HIRI's role is to provide a verifiable, tamper-evident substrate on which any identity semantic can be built. The choice of vocabulary, transport, or identifier scheme does not affect the validity of HIRI's integrity and provenance guarantees.

### 18.3 Interoperability as a Bridge, Not a Merger

The interoperability bridges defined in Appendix K are translation layers, not replacements. A VC compatibility envelope (Appendix K.2) wraps a HIRI Attestation Manifest — HIRI's signature chain remains the canonical verification path. An OID4VP transport envelope (Appendix K.4) carries a HIRI Passport Presentation as its payload — the transport layer does not sign the presentation; HIRI does.

**NORMATIVE:** Interoperability bridges MUST NOT introduce a second signing or verification path that bypasses or duplicates HIRI's cryptographic mechanisms. If a bridge standard (e.g., VC) defines its own signature scheme, the bridge MUST be structured so that HIRI's signature is the authoritative proof of integrity, and the external signature (if present) is a compatibility artifact only.

### 18.4 Extension Boundary Constraint

Future extensions to this specification MUST NOT move any item from the HIRI responsibility column into the external standards responsibility column, or vice versa.

Concretely: future versions of this specification MUST NOT define new vocabulary schemas (that is the role of identity semantics standards), MUST NOT define new transport protocols (that is the role of transport standards), and MUST NOT define new DID methods (that is the role of the DID specification). They MAY define new HIRI artifact types, new privacy modes, new verification phases, new conformance requirements, or new interoperability bridges to external standards.

---

## Appendix A: Manifest Examples

### A.1 Minimal Genesis Passport

```json
{
  "@context": [
    "https://hiri-protocol.org/spec/v3.1",
    "https://hiri-protocol.org/privacy/v1",
    "https://hiri-protocol.org/passport/v1",
    "https://w3id.org/security/v2"
  ],
  "@id": "hiri://key:ed25519:z6MkHolder001.../passport/main",
  "@type": "hiri:PassportManifest",
  "hiri:version": "1",
  "hiri:branch": "main",
  "hiri:timing": { "created": "2026-03-01T00:00:00Z" },
  "hiri:passport": {
    "holder": {
      "authority": "key:ed25519:z6MkHolder001...",
      "did": "did:key:z6MkHolder001...",
      "displayName": "Sarah Thompson",
      "keyDocumentURI": "hiri://key:ed25519:z6MkHolder001.../key/main"
    },
    "credentialSlots": [],
    "slotCount": 0,
    "activeSlotCount": 0
  },
  "hiri:content": {
    "hash": "sha256:genesis-hash...",
    "addressing": "raw-sha256",
    "canonicalization": "URDNA2015",
    "format": "application/ld+json",
    "size": 312
  },
  "hiri:signature": {
    "type": "Ed25519Signature2020",
    "algorithm": "ed25519",
    "canonicalization": "URDNA2015",
    "created": "2026-03-01T00:00:00Z",
    "verificationMethod": "hiri://key:ed25519:z6MkHolder001.../key/main#key-1",
    "proofPurpose": "assertionMethod",
    "proofValue": "z..."
  }
}
```

### A.2 Verifier Output Summary (v1.1.0)

```
Passport: hiri://key:ed25519:z6MkHolder001.../passport/main
Version: 3
Holder: Sarah Thompson
Holder Signing Algorithm: ed25519
Key Status: active
Overall Trust Level: full

Credential Slots (3):

  [token: HmacDerivedToken-abc123...]
    Type: EmploymentCredential
    Label: Environmental Scientist — EcoImpact Consulting
    Status: active
    Tier 2 Override: false
    Attestation: verified (valid, not stale)
    Issuer Algorithm: ed25519
    Issuer: EcoImpact Consulting
    Issuer Domain: ecoimpact.com (DNSSEC verified)
    Org Trust Level: full

  [token: HmacDerivedToken-def456...]
    Type: ProfessionalCertification
    Label: Wetland Specialist Certification — NEA
    Status: active
    Tier 2 Override: false
    Attestation: verified (valid, not stale)
    Issuer Algorithm: ed25519
    Issuer: National Environmental Association
    Issuer Domain: nea.org (HTTPS, no DNSSEC)
    Org Trust Level: partial

Omitted Slots: 1 (types and hashes withheld per Minimum Disclosure Surface)

Verified At: 2026-03-15T10:45:00Z
```

---

## Appendix B: Trust Chain Diagram

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        HIRI Digital Passport                             │
│                         Trust Chain (v1.2.0)                             │
└──────────────────────────────────────────────────────────────────────────┘

  Passport Manifest (holder-signed)
       │
       ├── hiri:passport.holder.authority
       │         └── Holder Signing Key [ed25519 | p256 | future]
       │                   └── Holder KeyDocument
       │
       ├── hiri:signature.algorithm → Signature Algorithm Registry
       │
       └── credentialSlots[n].attestationRef
                 │
                 └── Credential Attestation Manifest (issuer-signed)
                           │
                           ├── hiri:attestation.subject.holderAuthority
                           │         └── matches holder authority ✔
                           │
                           ├── hiri:attestation.claim
                           │         └── the credential (Tier 2 governs revocation)
                           │
                           └── hiri:signature.algorithm → Signature Algorithm Registry
                                     │
                                     └── Issuer Signing Key [ed25519 | p256 | future]
                                               │
                                               └── Issuer KeyDocument
                                                         │
                                                         └── organizationalIdentity.domain
                                                                   │
                                                                   └── https://<domain>/.well-known/hiri-key.json
                                                                             │
                                                                             └── hiriAuthority matches ✔
                                                                                       │
                                                                                       └── (DNSSEC) ✔

  Presentation Slot Blinding (v1.2.0):
       slotId [stable, internal] → HMAC-SHA256(slotBlindingKey, slotId ∥ 0x00 ∥ nonce ∥ 0x00 ∥ verifierAuthority) → presentationSlotToken
       slotId NEVER appears in presentations
       verifierAuthority binding prevents cross-verifier token relay
```

---

## Appendix C: Verification Status Reporting

Implementations MUST produce structured status reports for each phase. Undefined error codes MUST NOT be emitted.

| Code | Phase | Meaning |
|------|-------|---------|
| `PASSPORT_MANIFEST_INVALID_SIGNATURE` | 1 | Holder signature verification failed |
| `PASSPORT_CHAIN_INTEGRITY_FAILED` | 1 | Chain walk produced inconsistency |
| `PASSPORT_KEY_REVOKED` | 1 | Holder key is revoked |
| `PASSPORT_TYPE_MISMATCH` | 1 | `@type` is not `hiri:PassportManifest` |
| `PASSPORT_AUTHORITY_MISMATCH` | 1 | `holder.authority` does not match `@id` |
| `PASSPORT_SLOT_COUNT_EXCEEDED` | 1 | `slotCount` exceeds verifier's conformance limit |
| `SIGNATURE_ALGORITHM_UNSUPPORTED` | 1 or 3 | Algorithm ID not in verifier's Signature Algorithm Registry |
| `SLOT_STATUS_REVOKED` | 2 | Slot `status` is `"revoked"` |
| `SLOT_STATUS_EXPIRED` | 2 | Slot `status` is `"expired"` or `validUntil` is past |
| `SLOT_PRIVACY_MODE_UNKNOWN` | 2 | `privacyMode` is not a valid value |
| `ATTESTATION_INVALID_SIGNATURE` | 3 | Issuer signature verification failed |
| `ATTESTATION_SUBJECT_MISMATCH` | 3 | Subject authority does not match holder |
| `ATTESTATION_MODE_MISMATCH` | 3 | Attestation mode does not match slot `privacyMode` |
| `ATTESTATION_STALE` | 3 | `validUntil` is in the past |
| `ATTESTATION_ISSUER_KEY_REVOKED` | 3 | Issuer key is revoked |
| `ATTESTATION_UNRESOLVABLE` | 3 | Attestation manifest cannot be fetched |
| `ATTESTATION_TIER2_OVERRIDE_REVOKED` | 3 | Tier 2 revoked; overrides Tier 1 `"active"` status |
| `ORG_DOMAIN_BINDING_FAILED` | 4 | Domain `.well-known` does not match issuer authority |
| `ORG_DNSSEC_FAILED` | 4 | DNSSEC verification failed for issuer domain |
| `ORG_KEYDOCUMENT_UNAVAILABLE` | 4 | Issuer KeyDocument cannot be resolved |
| `PRESENTATION_SLOT_NOT_BLINDED` | P | Raw `slotId` found in presentation; blinding required |
| `PRESENTATION_NONCE_INVALID` | P | Nonce missing, too short, reused, or expired |
| `PRESENTATION_NONCE_REUSED` | P | Nonce has already been used in a prior presentation |
| `PRESENTATION_SLOT_DUPLICATE_TOKEN` | P | Same `presentationSlotToken` appears in both disclosed and withheld sections |
| `PRESENTATION_COMPLETENESS_AUDIT_DECLINED` | P | Holder declined completeness audit; `omittedSlotCount` returned only |
| `PRESENTATION_UNILATERAL_AUDIT_DISCLOSURE` | P | Presentation contains `withheldSlotSummary` without a corresponding `completenessAudit: true` request |
| `PRESENTATION_KEY_ROTATED_AFTER_CREATION` | P | Holder's signing key was rotated or revoked after the presentation's `hiri:timing.created` timestamp |
| `PRESENTATION_PROOF_ARTIFACT_HASH_MISMATCH` | P | Fetched `proofArtifactRef` content does not match declared `artifactHash` |
| `PRESENTATION_PROOF_ARTIFACT_UNAVAILABLE` | P | `proofArtifactRef` URI did not return the artifact within the fetch timeout; biometric binding unverified |
| `BIOMETRIC_REGISTRY_NULLIFIER_EXPOSED` | G | A registry nullifier was found in a presentation's public inputs; MUST be rejected |
| `REVOCATION_LOG_ENTRY_FOUND` | 3 | Revocation log contains an entry for this manifest hash; credential is revoked |
| `REVOCATION_LOG_STATE_UNKNOWN` | 3 | Revocation log unreachable and no valid cached checkpoint; revocation state indeterminate |
| `REVOCATION_LOG_CHECKPOINT_EXPIRED` | 3 | Cached checkpoint has exceeded staleness window; online refresh required before `"full"` trust |
| `REVOCATION_LOG_CHECKPOINT_CHAIN_GAP` | 3 | Gap detected in checkpoint chain; log may be compromised; treat as `"unknown"` |
| `ORACLE_NOT_IN_TRUST_ANCHORS` | 3 | Biometric oracle authority not in verifier's configured trust anchor set; trust level capped at `"partial"` |
| `ORACLE_GOVERNANCE_DOCUMENT_EXPIRED` | 3 | Oracle governance document `validUntil` has passed; trust level downgraded to `"partial"` |
| `ORACLE_GOVERNANCE_DOCUMENT_HASH_MISMATCH` | 3 | Fetched governance document does not match cached hash in trust anchor; requires re-confirmation |
| `KEYDOCUMENT_REQUIRED_MISSING` | 1 or 3 | KeyDocument not published by a Passport-Interoperable or Passport-Full conformance claimant |

Phase `P` = presentation verification (separate from Phases 1–4 of passport verification).

### C.2 Revocation Log Status Codes — Normative Staleness Window Binding

This table is NORMATIVE. It binds each revocation log status code to the specific Phase 3 state machine condition that produces it and the staleness window rule that governs it (§16.3). Implementations MUST emit exactly the code listed for each condition; no alternative codes are permitted for these states.

| Status Code | `revocationLogStatus` Value | Phase 3 Step | Trigger Condition | TransactionClass | Trust Level Ceiling |
|-------------|----------------------------|-------------|-------------------|-----------------|---------------------|
| `REVOCATION_LOG_ENTRY_FOUND` | `"revoked"` | Step 11 | Entry for `manifestHash` found in log | Any | N/A (slot revoked) |
| *(no code — normal path)* | `"confirmed-valid"` | Step 11 | Log reachable; no entry found; checkpoint fresh | `standard` (≤48h) | No ceiling |
| *(no code — normal path)* | `"confirmed-valid"` | Step 11 | Log reachable; no entry found; checkpoint fresh | `high-value` (≤15min) | No ceiling |
| `REVOCATION_LOG_STALE_HIGH_VALUE` | `"unknown"` | Step 11 | Log reachable but checkpoint >15min old | `high-value` | `"partial"` |
| `REVOCATION_LOG_CHECKPOINT_EXPIRED` | `"cached-checkpoint"` | Step 11 | Log unreachable; cached checkpoint within 48h | `standard` | No ceiling imposed |
| `REVOCATION_LOG_STATE_UNKNOWN` | `"unknown"` | Step 11 | Log unreachable; no checkpoint OR checkpoint >48h | `standard` | `"partial"` |
| `REVOCATION_LOG_CHECKPOINT_CHAIN_GAP` | `"unknown"` | Step 11 | Gap detected in checkpoint chain | Any | `"partial"` |
| `REVOCATION_LOG_CHECKPOINT_EXPIRED` | `"unknown"` | Step 11 | Log unreachable; cached checkpoint expired (>48h) | `standard` | `"partial"` |

**Machine-readable status enum:** Implementations MUST represent `revocationLogStatus` as one of the following string literals in all verification result objects and telemetry:

```typescript
type RevocationLogStatus =
  | "confirmed-valid"       // log queried; no entry; checkpoint fresh
  | "revoked"               // entry found in log
  | "cached-checkpoint"     // log offline; checkpoint within staleness window
  | "unknown"               // log offline; no valid checkpoint OR chain gap
  | "not-checked";          // Passport-Core; log not required at this level
```

**Telemetry standardization:** Verifier implementations SHOULD emit structured log entries using these string literals as the `revocationLogStatus` field value. This enables cross-implementation telemetry aggregation and anomaly detection across deployments.

---

## Appendix D: Privacy Mode Decision Matrix for Credential Slots

| Credential Type | Recommended Mode | Rationale |
|-----------------|------------------|-----------|
| `GovernmentIdVerification` | `proof-of-possession` | Content is maximally sensitive; existence proof is sufficient for most verifiers |
| `BackgroundCheckClearance` | `proof-of-possession` | Same as above |
| `EmploymentCredential` | `selective-disclosure` | Position and organization disclosable; salary, end-reason typically withheld |
| `EducationCredential` | `selective-disclosure` | Degree and field disclosable; grades typically withheld |
| `ProfessionalCertification` | `public` | Certifications are typically public record |
| `MembershipCredential` | `selective-disclosure` or `public` | Depends on member privacy norms |
| `EndorsementCredential` | `public` or `selective-disclosure` | Holder choice; endorsement author may wish privacy |
| `PublicationRecord` | `public` | Publications are public record by definition |
| `SyntheticMoralPersonStatus` | `selective-disclosure` | Governance status details may be sensitive to agent's operational context |

---

## Appendix E: Signature Algorithm Registry (Initial Values)

This appendix is normative for the initial registry values. Registry extensions beyond these values are not governed by this specification.

### E.1 Ed25519 (REQUIRED)

| Property | Value |
|----------|-------|
| Algorithm ID | `ed25519` |
| JOSE Algorithm ID | `EdDSA` (RFC 7518) |
| COSE Algorithm ID | `-8` (RFC 8152) |
| Authority Prefix | `key:ed25519:` |
| Key Length | 32 bytes |
| Proof Type | `Ed25519Signature2020` |
| Proof Value Encoding | base58btc with `z` multibase prefix |
| RFC | 8032 |
| Deterministic | Yes (inherently) |

### E.2 P-256 / ECDSA (OPTIONAL)

| Property | Value |
|----------|-------|
| Algorithm ID | `p256` |
| JOSE Algorithm ID | `ES256` (RFC 7518) |
| COSE Algorithm ID | `-7` (RFC 8152) |
| Authority Prefix | `key:p256:z` |
| Multicodec Identifier | `0x1200` (varint: `0x80 0x24`) |
| Key Representation | Compressed 33 bytes (`0x02`/`0x03` prefix + 32-byte X coordinate) |
| Encoded Bytes | `[0x80, 0x24]` + `compressedPublicKey` (35 bytes total) |
| Multibase Encoding | `z` + base58btc (standard; `z` = base58btc per W3C Multibase) |
| Proof Type | `EcdsaSecp256r1Signature2019` |
| Proof Value Encoding | base64url without padding |
| RFC | 6979 (deterministic ECDSA required) |
| Deterministic | Yes (when RFC 6979 is followed) |
| Hardware Support | Apple Secure Enclave, Android Titan M, TPM 2.0 |
| Breaking change from v1.1.0 | Yes — v1.1.0 incorrectly used `key:p256:p` with uncompressed keys. v1.2.0 corrects to standard multicodec-prefixed compressed keys with `z` multibase. |

### E.3 ML-DSA-65 (INFORMATIVE, future)

| Property | Value |
|----------|-------|
| Algorithm ID | `ml-dsa-65` |
| JOSE Algorithm ID | TBD (not yet registered) |
| COSE Algorithm ID | TBD (not yet registered) |
| Standard | FIPS 204 |
| Status | Not yet normative. Not guaranteed interoperable across v1.x implementations. |
| Note | Implementations MAY register this algorithm. Cross-implementation interoperability SHOULD be validated against NIST FIPS 204 test vectors. |

**Note on JOSE/COSE column usage:** The JOSE and COSE algorithm IDs in this appendix are cross-reference metadata only. They enable implementers to map HIRI signing operations to JOSE/COSE-compatible cryptographic libraries without a second registry lookup. They MUST NOT be used as values for `hiri:signature.algorithm` in manifests or presentations — use the HIRI Algorithm ID from the first column of the §6.5.2 table.

---

## Appendix F: Proxy Issuance and Non-Participating Authorities (INFORMATIVE)

This appendix is INFORMATIVE. Nothing in this appendix modifies the normative verification algorithm, the signing requirements, or the privacy mode semantics defined in §§1–15. All MUST/SHOULD language in this appendix applies to the INFORMATIVE pattern described here, not to the core protocol.

### F.1 The Cold-Start Problem

The HIRI Organizational Authority bootstrap (§10) requires that an issuer operate a HIRI authority with a published KeyDocument, a `did:web` domain binding, and (ideally) DNSSEC-verified domain control. This is a significant adoption barrier. In practice, many of the most valuable credential sources — government identity authorities, legacy university transcript systems, employer HR platforms, and professional certification bodies — will not natively operate HIRI Organizational Authorities at the time a holder first builds their passport.

The result is the **cold-start problem**: a holder possesses valid, high-value attributes tied to authoritative sources that cannot sign Tier 2 Credential Attestation Manifests. Without a solution, every wallet developer and issuer will independently invent non-interoperable workarounds.

This appendix defines the **Proxy Issuer** pattern as the RECOMMENDED interoperable solution for this scenario, and compares it to Zero-Knowledge proof-based credential types (§F.5) as a complementary long-term path.

### F.2 Architectural Framing

The HIRI protocol does not cryptographically distinguish between a direct issuer and a proxy issuer. From the perspective of the verification algorithm (Phase 3, §12.4), an issuer is an Ed25519 (or P-256) public key signing an RDF graph. The protocol verifies:

1. That the signature is valid
2. That the signing key's lifecycle is active
3. That the attestation subject binding matches the holder
4. That the privacy mode is consistent with the slot declaration

It does NOT verify that the issuer is the authoritative source for the claimed attribute. **That determination is an application-layer trust policy, not a cryptographic operation.** Making proxy issuance normative in the core protocol would violate §4.6 (Separation of Authentication and Authorization) by embedding trust policy into the cryptographic layer.

The Proxy Issuer pattern therefore lives here — in an informative appendix — precisely because it is the right architectural layer for it.

### F.3 The Proxy Issuer Pattern

In this pattern, a participating third-party service (the Proxy Issuer) acts as an intermediary between the holder and a non-participating authoritative source.

```
Non-Participating Authoritative Source
  (e.g., DHS email server, university transcript API)
           │
           │  verification channel (OTP, API, OAuth, etc.)
           ▼
    Proxy Issuer (HIRI Organizational Authority)
    key:ed25519:z<proxy-authority>
    domain: govverify.example.com
           │
           │  signs Tier 2 Credential Attestation Manifest
           ▼
    Holder's Passport Slot
           │
           │  Phase 3 verification + verifier trust policy
           ▼
    Verifier (accepts proxy-authority for specific claim domains)
```

**Step 1 — Holder initiates claim verification.** The holder requests verification of an attribute (e.g., "I control the email address jane.doe@dhs.gov") from the Proxy Issuer.

**Step 2 — Proxy verifies against the authoritative source.** The Proxy Issuer performs a real-world verification: for email, a one-time-password loop; for academic transcripts, a National Student Clearinghouse API call; for employment, an HR system query. The verification method is recorded in the attestation's `hiri:attestation.evidence` block.

**Step 3 — Proxy issues a Credential Attestation Manifest.** The Proxy Issuer generates a standard Tier 2 `hiri:AttestationManifest`, signed by the Proxy's own HIRI authority. The manifest's `claim` block encodes the verified attribute using claim atomization (§F.4). The `evidence.method` field MUST describe the verification method used.

**Step 4 — Holder adds the slot.** The holder adds the credential slot to their passport, referencing the proxy-issued attestation manifest.

**Step 5 — Verifier applies trust policy.** The verifier's trust policy (§F.6) maps the Proxy Issuer's authority to the claim domains it is trusted to attest. A well-known Proxy Issuer trusted for `@dhs.gov` email verification is treated differently from an unknown proxy claiming the same.

#### F.3.1 Example Proxy Attestation Manifest (email verification)

```json
{
  "@context": [
    "https://hiri-protocol.org/spec/v3.1",
    "https://hiri-protocol.org/privacy/v1",
    "https://hiri-protocol.org/passport/v1",
    "https://w3id.org/security/v2"
  ],
  "@id": "hiri://key:ed25519:z<proxy-authority>/attestation/email-jane-dhs-2026-001",
  "@type": "hiri:AttestationManifest",

  "hiri:version": "1",
  "hiri:branch": "main",
  "hiri:timing": { "created": "2026-03-15T09:00:00Z" },

  "hiri:privacy": {
    "mode": "selective-disclosure",
    "parameters": {
      "indexSalt": "<base64url-256-bit-salt>",
      "statementCount": 6,
      "mandatoryStatements": [0, 1, 2],
      "disclosureSuite": "HMAC"
    }
  },

  "hiri:attestation": {
    "subject": {
      "type": "hiri:PassportHolder",
      "holderAuthority": "key:ed25519:z<holder-authority>",
      "holderPassportURI": "hiri://key:ed25519:z<holder-authority>/passport/main"
    },
    "claim": {
      "@type": "hiri:passport:VerifiedEmailCredential",
      "credentialType": "VerifiedEmailCredential",
      "verifiedEmail": {
        "fullAddress": "jane.doe@dhs.gov",
        "localPart": "jane.doe",
        "domain": "dhs.gov",
        "authoritativeSource": "dhs.gov-smtp"
      },
      "verificationMethod": "email-otp",
      "attestedAt": "2026-03-15T09:00:00Z",
      "validUntil": "2027-03-15T00:00:00Z",
      "proxyIssuer": {
        "authority": "key:ed25519:z<proxy-authority>",
        "domain": "govverify.example.com",
        "isProxy": true,
        "authoritativeSourceDomain": "dhs.gov"
      }
    },
    "evidence": {
      "method": "email-otp-verification",
      "description": "Holder demonstrated control of the email address via a one-time-password sent to jane.doe@dhs.gov and entered within 10 minutes."
    }
  },

  "hiri:signature": {
    "type": "Ed25519Signature2020",
    "algorithm": "ed25519",
    "canonicalization": "URDNA2015",
    "created": "2026-03-15T09:00:00Z",
    "verificationMethod": "hiri://key:ed25519:z<proxy-authority>/key/main#key-1",
    "proofPurpose": "assertionMethod",
    "proofValue": "z..."
  }
}
```

Note the `proxyIssuer` block in the claim. This is an INFORMATIVE convention — it signals to verifiers that the attestation was produced by a proxy and records the authoritative source domain. Verifiers SHOULD surface this information in verification results. Verifiers MUST NOT treat `isProxy: true` as a validation failure — it is a transparency signal, not a defect.

### F.4 Claim Atomization for Selective Disclosure

This section addresses the single most common implementation error in proxy-issued credential design.

#### F.4.1 The Anti-Pattern

When a Proxy Issuer encodes a compound identifier as a single undivided string, selective disclosure becomes useless for that attribute.

```json
{
  "verifiedEmail": "jane.doe@dhs.gov"
}
```

After URDNA2015 canonicalization, this produces a single N-Quad:

```
<https://example.org/holder/jane> <hiri:passport:verifiedEmail> "jane.doe@dhs.gov" .
```

This is ONE statement. The holder can either disclose it entirely — revealing the full address including the personal identifier `jane.doe` — or withhold it entirely, proving nothing to the verifier. There is no middle ground. The Minimum Disclosure Surface principle (§4.7) is technically in force but practically defeated, because the schema has pre-fused information that should have been kept separate.

#### F.4.2 The Recommended Pattern: Atomized Claims

Proxy Issuers SHOULD decompose compound identifiers into distinct RDF-level statements, each carrying a single separable piece of information:

```json
{
  "verifiedEmail": {
    "@id": "_:verifiedEmail1",
    "fullAddress": "jane.doe@dhs.gov",
    "localPart": "jane.doe",
    "domain": "dhs.gov",
    "authoritativeSource": "dhs.gov-smtp"
  }
}
```

After URDNA2015 canonicalization and blank node normalization, this produces four distinct N-Quads (one per field), approximately:

```
_:c14n0 <hiri:passport:fullAddress> "jane.doe@dhs.gov" .
_:c14n0 <hiri:passport:localPart>   "jane.doe" .
_:c14n0 <hiri:passport:domain>      "dhs.gov" .
_:c14n0 <hiri:passport:authoritativeSource> "dhs.gov-smtp" .
```

Each N-Quad is a separate entry in the attestation's statement index. The holder can construct a Passport Presentation using Privacy Extension Mode 3 selective disclosure that reveals:

```
_:c14n0 <hiri:passport:domain>      "dhs.gov" .
_:c14n0 <hiri:passport:authoritativeSource> "dhs.gov-smtp" .
```

...while permanently withholding:

```
_:c14n0 <hiri:passport:fullAddress> "jane.doe@dhs.gov" .
_:c14n0 <hiri:passport:localPart>   "jane.doe" .
```

The verifier learns: the holder controls an email address at `dhs.gov`, verified through that domain's SMTP infrastructure. They do not learn the holder's name or local identifier. This is the selective disclosure mechanism functioning as designed — but it requires the issuer to encode the claim in a way that creates distinct N-Quad boundaries.

#### F.4.3 Atomization Principles

Proxy Issuers designing claim schemas SHOULD follow these principles:

**Separate by disclosure unit.** Each field in the JSON-LD claim object should represent the smallest piece of information a holder might want to reveal independently. Ask: "Is there a valid use case where a holder would want to disclose X without disclosing Y?" If yes, X and Y should be separate fields.

**Do not fuse personal identifiers with organizational identifiers.** Personal name components, local email parts, employee IDs, and student numbers SHOULD always be in separate fields from the organizational domain, institution name, or credential type. These two categories have different disclosure profiles in almost every real-world use case.

**Avoid deeply nested structures where possible.** Each level of nesting in JSON-LD produces additional blank nodes in the RDF graph. While URDNA2015 handles this correctly, flatter schemas produce cleaner, more predictable N-Quad boundaries and are easier for verifiers and holders to reason about.

**Designate mandatory statements explicitly.** Per §8.3, the issuer MUST designate at minimum the credential type, attestation timestamp, and issuer authority as mandatory statements. For proxy-issued credentials, the `proxyIssuer.authoritativeSourceDomain` statement SHOULD also be mandatory — verifiers need to know which authoritative domain the proxy is attesting to, even when the holder's personal identifier is withheld.

#### F.4.4 Credential Slot Declaration for Proxy-Issued Credentials

The holder's passport slot for a proxy-issued credential follows the standard slot structure (§7.2). The `credentialType` SHOULD reflect the attribute being attested, not the proxy mechanism:

```json
{
  "slotId": "slot:verified-email-dhs-2026",
  "credentialType": "VerifiedEmailCredential",
  "displayLabel": "Verified Email — dhs.gov domain",
  "privacyMode": "selective-disclosure",
  "attestationRef": {
    "authority": "key:ed25519:z<proxy-authority>",
    "manifestHash": "sha256:...",
    "manifestVersion": "1"
  },
  "status": "active"
}
```

The `displayLabel` SHOULD indicate the domain without including the personal local part — consistent with the principle that display labels are always public (§7.3).

### F.5 ZK Credential Types: A Complementary Path

The Proxy Issuer pattern has a structural limitation: the holder must trust the Proxy Issuer not to log, correlate, or sell the verification events it processes. A privacy-maximizing alternative is to replace the proxy trust relationship with a cryptographic one using Zero-Knowledge proofs.

In a ZK credential type, the holder generates a proof directly from the authoritative source material — for example, a DKIM-signed email header — without revealing the source material to any intermediary. The proof establishes that the holder controls an address at a specific domain, verified by that domain's DKIM signing key, without disclosing the full address, the email contents, or requiring any online service.

**ZK Email as a credential type example (INFORMATIVE):**

A `ZKEmailDomainCredential` type would package:
- A ZK proof (e.g., generated by the ZK Email circuit over a DKIM-signed email)
- The public inputs to the proof (domain, DKIM public key commitment, nullifier)
- No personal identifier, no email contents, no proxy intermediary

The issuer authority for this credential type would be the ZK proof system's parameter registry (a well-known HIRI authority publishing circuit parameters and DKIM public key commitments). The holder generates the proof locally and submits it as the attestation content. No human intermediary touches the holder's email address.

**Comparison of approaches:**

| Dimension | Proxy Issuer (§F.3) | ZK Credential Type |
|-----------|---------------------|-------------------|
| Holder trust model | Trust proxy not to log | No intermediary needed |
| Issuer complexity | Moderate (standard HIRI + verification API) | High (ZK circuit, parameter registry) |
| Verifier complexity | Standard Phase 3 + trust policy | ZK proof verification required |
| Ecosystem readiness | Ready now | Emerging; not yet normative |
| Claim atomization | Required (§F.4) | Baked into circuit design |
| Revocability | Standard issuer revocation | Nullifier-based or time-bounded |

Both approaches produce valid HIRI Passport credential slots. They are not mutually exclusive — a holder MAY hold both a proxy-issued email credential and a ZK email domain credential for the same address, with different privacy profiles, and choose which to present based on the verifier context.

Normative specification of ZK credential types is out of scope for this document. Implementers interested in this path SHOULD track the W3C Verifiable Credentials ZK work and the ZK Email project for compatible proof system specifications. For ZK biometric credential types specifically — including Sybil-resistance proofs and holder-to-credential binding — see Appendix G.

### F.6 Verifier Policy Mapping for Proxy Issuers

Verifiers accepting proxy-issued credentials MUST maintain an explicit trust policy that defines which Proxy Authorities are trusted to attest to which authoritative domains and claim types. A verifier MUST NOT accept an attestation from an unknown proxy authority claiming a high-value government or corporate domain affiliation.

#### F.6.1 Trust Policy Structure (INFORMATIVE)

The following JSON structure is a RECOMMENDED format for verifier trust policy entries. It is not normative — verifiers MAY use any internal structure that implements the same semantics.

```json
{
  "proxyTrustPolicies": [
    {
      "policyId": "policy:govverify-dhs-email",
      "proxyAuthority": "key:ed25519:z<govverify-proxy-authority>",
      "proxyDomain": "govverify.example.com",
      "trustedForCredentialTypes": ["VerifiedEmailCredential"],
      "trustedForAuthoritativeDomains": ["dhs.gov", "fbi.gov", "state.gov"],
      "verificationMethodsAccepted": ["email-otp-verification"],
      "trustLevel": "partial",
      "policyExpiry": "2027-01-01T00:00:00Z",
      "notes": "GovVerify is an approved GSA credential service provider for .gov email verification."
    }
  ]
}
```

**`proxyAuthority`** — The proxy's HIRI authority string. The verifier MUST verify the proxy's organizational identity bootstrap (Phase 4, §12.5) to confirm the proxy is who they claim to be before consulting the policy entry.

**`trustedForAuthoritativeDomains`** — The domains for which this proxy's attestations are accepted. An attestation from this proxy claiming an attribute from `gmail.com` would NOT be accepted under this policy entry.

**`verificationMethodsAccepted`** — The evidence methods the verifier will credit. If the attestation's `evidence.method` is not in this list, the verifier SHOULD downgrade the trust level or reject the attestation based on their local policy.

**`trustLevel`** — Recommended values: `"full"` (proxy has formal legal accountability for attestations, e.g., accredited identity provider), `"partial"` (proxy is operationally trusted but not legally accredited), `"low"` (proxy is accepted for low-stakes claims only).

#### F.6.2 Trust Level Propagation

When a verifier processes a proxy-issued credential, the proxy trust level SHOULD be incorporated into the overall `organizationTrustLevel` reported in `SlotVerificationResult` (§12.6):

| Proxy Trust Level | Phase 4 Result | Effective Org Trust Level |
|-------------------|----------------|--------------------------|
| `full` | DNSSEC verified | `"full"` |
| `full` | HTTPS only | `"partial"` |
| `partial` | DNSSEC verified | `"partial"` |
| `partial` | HTTPS only | `"partial"` |
| `low` | any | `"key-only"` |
| Not in policy | any | `"unverifiable"` |

A verifier MUST NOT report `organizationTrustLevel: "full"` for a proxy-issued credential unless both the proxy's organizational identity bootstrap succeeds with DNSSEC AND the verifier's trust policy rates the proxy as `"full"`.

#### F.6.3 Policy Distribution and Maintenance

Verifier trust policies for proxy issuers are application-layer concerns. This specification does not define a protocol for distributing or updating these policies. Verifiers SHOULD:

- Maintain versioned, auditable policy records
- Not silently update policy entries — changes should be logged with rationale
- Periodically re-verify the proxy's organizational authority bootstrap (Phase 4) to detect key rotation or domain changes
- Surface the proxy trust level to end-users in verification result displays, not just the `organizationTrustLevel` summary

### F.7 Summary: When to Use Which Pattern

| Scenario | Recommended Approach |
|----------|--------------------|
| Authoritative source will adopt HIRI within 12 months | Plan for direct issuance; use proxy as interim |
| Large government or regulated sector, no HIRI adoption timeline | Proxy Issuer with formal accreditation |
| High-privacy requirement, holder unwilling to trust intermediary | ZK credential type (when available for the claim type) |
| Low-stakes attribute, convenience is primary concern | Proxy Issuer with `trustLevel: "low"` |
| Claim type has no feasible ZK circuit and no participating issuer | Proxy Issuer is the only current path |

The Proxy Issuer pattern is a transitional mechanism. As more authoritative sources adopt HIRI Organizational Authorities, proxy issuance for those sources can be deprecated in favor of direct issuance without any changes to the holder's passport structure — only the `attestationRef.authority` in the credential slot changes when the holder refreshes their credential from the now-participating source.

---

## Appendix G: Biometric Network Integration (INFORMATIVE)

This appendix is INFORMATIVE. Nothing here modifies the normative verification algorithm, signing requirements, privacy mode semantics, or key lifecycle rules defined in §§1–15. All MUST/SHOULD language in this appendix applies to the INFORMATIVE patterns described here.

### G.1 Architectural Framing

#### G.1.1 The §4.1 Tension

Section 4.1 establishes a strict invariant: **"The holder's signing keypair IS the passport."** No registry, platform, or third party mediates the holder's identity. This is the foundation of holder sovereignty.

Biometric network integration does not alter this invariant. The keypair remains the cryptographic identity — the root of all signature chains, the authority from which the passport URI is derived, the thing the holder's device protects. What biometric binding adds is an **additional attestation layer**: a Tier 2 credential asserting a relationship between the keypair and a biological body, or between two keypairs and the same biological body. The protocol signs what biometric networks produce; it does not replace what the protocol already does.

The three patterns in this appendix are applications of existing HIRI mechanisms — Tier 2 Attestation Manifests, Mode 3 selective disclosure, Mode 5 third-party attestation, and ZK credential types (§F.5) — to a specific class of high-assurance claims.

#### G.1.2 Why Biometric Patterns Are INFORMATIVE

The HIRI protocol does not, and must not, cryptographically distinguish between a biometric-backed credential and any other Tier 2 attestation. To the verification algorithm (Phase 3, §12.4), a `ProofOfUniqueHumanCredential` is an Ed25519-signed RDF graph, identical in structure to an `EmploymentCredential`. Whether a verifier requires biometric binding for a specific transaction is an application-layer policy decision that belongs in verifier trust policy (§F.6), not in the protocol core.

Embedding biometric requirements normatively would violate §4.6 (Separation of Authentication and Authorization) by the same reasoning that makes Proxy Issuance informative in Appendix F.

#### G.1.3 The Irrevocability Constraint

**NORMATIVE within this appendix:** Raw biometric data — fingerprint templates, iris scan vectors, facial geometry coordinates, palm-vein maps, or any other biometric template — MUST NOT appear in any HIRI artifact: not in a Tier 2 claim payload, not in a manifest, not in a presentation, not in a KeyDocument.

Biometrics are irrevocable. A compromised Ed25519 private key can be rotated (§13.5). A compromised biometric template cannot be changed. Any specification pattern that places raw biometric data in a content-addressed, cryptographically pinned artifact creates a permanent, globally distributed, cryptographically verifiable record of the holder's biometric, with no rotation path. This would be catastrophic.

All biometric patterns in this appendix are therefore ZK-commitment-based. The biometric data never leaves the holder's device. The credential contains only a cryptographic commitment to a biometric-derived value, and proofs of properties about that commitment are generated locally at presentation time.

### G.2 Sybil Resistance: ProofOfUniqueHumanCredential

#### G.2.1 The Problem

Cryptographic identity is free. A holder can generate an arbitrary number of Ed25519 keypairs, each producing a valid HIRI Genesis Passport. Systems that need to enforce one-passport-per-human — decentralized voting, universal basic income distribution, rate-limited access to public goods, anti-spam mechanisms — have no cryptographic basis in the HIRI protocol for distinguishing a holder with one passport from an actor with ten thousand.

This is the Sybil problem. It cannot be solved by cryptography alone; it requires a link to physical uniqueness.

#### G.2.2 The Biometric Network as Specialized Issuer

A decentralized biometric network — systems based on iris hashing, palm-vein scanning, or other modalities with sufficient uniqueness entropy — acts as a specialized Tier 2 Issuer within the HIRI ecosystem.

The network maintains a **global uniqueness registry**: a Merkle tree (or equivalent authenticated data structure) of biometric commitments. This appendix defines two cryptographically distinct nullifier types that serve different purposes at different protocol layers. Confusing them is the source of the tracking vulnerability addressed in v1.5.0.

#### G.2.2.1 Split Nullifier Architecture

**Registry Nullifier (global, enrollment-only):**

```
registryNullifier = H(biometric_secret || "registry-v1")
```

Where `H` is a collision-resistant hash function (SHA-256 or a ZK-friendly equivalent such as Poseidon). The registry nullifier is:
- Deterministic per biometric (same biometric → same nullifier across all enrollments and verifiers)
- Used ONLY at enrollment time by the Biometric Network to detect double-enrollment
- Stored in the uniqueness registry as the anti-collision check value
- **NEVER exposed in any Passport Presentation or publication artifact**
- NEVER included in ZK proof public inputs visible to a verifier

**Context-Bound Nullifier (per-verifier, presentation-only):**

```
contextNullifier = H(biometric_secret || verifierAuthority)
```

The context-bound nullifier is:
- Deterministic for a given (biometric, verifier) pair
- Different for every verifier the holder presents to (different verifierAuthority → different value)
- Exposed in ZK proof public inputs in presentations to allow a specific verifier to detect if the same holder is attempting multiple enrollments within that verifier's own system
- NOT usable across verifiers — Verifier A's context nullifier for a given holder is computationally unrelated to Verifier B's

**Why two nullifiers are necessary:** The registry nullifier must be global and deterministic to detect double-enrollment at the uniqueness registry. The context-bound nullifier must be verifier-scoped to prevent cross-verifier tracking. These goals are in direct tension and cannot be served by a single value. The ZK circuit proves both properties simultaneously: "I know a `biometric_secret` such that my registry nullifier is in the Merkle tree (proving uniqueness), AND here is my context-bound nullifier for this verifier's authority (proving scoped non-duplication without global correlation)." The registry nullifier is a private circuit wire; the context-bound nullifier is a public output.

**When a holder enrolls:**

1. The holder's device captures a biometric sample locally.
2. `biometric_secret` is derived from the template (e.g., via a biometric feature extractor that produces a stable numeric vector).
3. `registryNullifier = H(biometric_secret || "registry-v1")` is computed.
4. The network verifies the `registryNullifier` is absent from the uniqueness registry.
5. The network adds `registryNullifier` to the registry (NOT the biometric template or commitment).
6. The network issues a `ProofOfUniqueHumanCredential` Attestation Manifest to the holder's HIRI authority.

#### G.2.3 Credential Structure

The credential content is a ZK proof of enrollment: the holder proves membership in the uniqueness registry without revealing the `biometric_secret`, the registry nullifier, or the biometric template. Critically, the registry nullifier is a **private circuit wire** — it is used to verify Merkle inclusion but is never output to the verifier.

```json
{
  "@context": [
    "https://hiri-protocol.org/spec/v3.1",
    "https://hiri-protocol.org/privacy/v1",
    "https://hiri-protocol.org/passport/v1",
    "https://w3id.org/security/v2"
  ],
  "@id": "hiri://key:ed25519:z<biometric-network-authority>/attestation/pou-holder-001",
  "@type": "hiri:AttestationManifest",

  "hiri:version": "1",
  "hiri:branch": "main",
  "hiri:timing": { "created": "2026-03-15T09:00:00Z" },

  "hiri:privacy": {
    "mode": "selective-disclosure",
    "parameters": {
      "indexSalt": "<base64url-256-bit-salt>",
      "statementCount": 5,
      "mandatoryStatements": [0, 1, 2, 3],
      "disclosureSuite": "HMAC"
    }
  },

  "hiri:attestation": {
    "subject": {
      "type": "hiri:PassportHolder",
      "holderAuthority": "key:ed25519:z<holder-authority>",
      "holderPassportURI": "hiri://key:ed25519:z<holder-authority>/passport/main"
    },
    "claim": {
      "@type": "hiri:passport:ProofOfUniqueHumanCredential",
      "credentialType": "ProofOfUniqueHumanCredential",
      "enrollmentProof": {
        "proofType": "ZKMerkleInclusionProof",
        "registryRoot": "<hex-merkle-root-of-uniqueness-registry>",
        "registryVersion": "2026-03-15",
        "proofArtifact": "<base64url-encoded-ZK-proof>",
        "publicInputs": {
          "registryRoot": "<hex-merkle-root>"
        },
        "privateWires": ["registryNullifier"],
        "note": "registryNullifier is a private circuit wire. It proves Merkle membership without being output. It MUST NOT appear in this manifest or any presentation."
      },
      "biometricModality": "iris",
      "networkAuthority": "key:ed25519:z<biometric-network-authority>",
      "attestedAt": "2026-03-15T09:00:00Z",
      "validUntil": "2027-03-15T00:00:00Z"
    },
    "evidence": {
      "method": "decentralized-biometric-uniqueness-verification",
      "description": "Holder enrolled iris biometric. ZK proof confirms registry nullifier is in registry version 2026-03-15 without revealing the nullifier or biometric template."
    }
  },

  "hiri:signature": {
    "type": "Ed25519Signature2020",
    "algorithm": "ed25519",
    "canonicalization": "URDNA2015",
    "created": "2026-03-15T09:00:00Z",
    "verificationMethod": "hiri://key:ed25519:z<biometric-network-authority>/key/main#key-1",
    "proofPurpose": "assertionMethod",
    "proofValue": "z..."
  }
}
```

Key fields:

**`enrollmentProof.publicInputs`** — Contains only the `registryRoot`. The registry nullifier is NOT a public input. The verifier confirms the proof validates against the declared registry root and registry version. Nothing about the holder's biometric identity is exposed.

**`privateWires`** — An INFORMATIVE declaration for circuit auditors and implementers indicating which values are private wires in the ZK circuit. No protocol behavior depends on this field.

**`biometricModality`** — The biometric modality is **functional metadata required for ZK circuit verification parameter selection**: verifiers must know the modality to select the correct circuit verification key for presentation-time proof verification. It is a mandatory statement (index position 3). This is distinct from biometric data — "iris" identifies which proof system was used, not anything about the holder's iris. See §G.2.4 for the corrected discussion.

**`proofArtifact`** — The actual ZK proof bytes (base64url-encoded). Selective-disclosure statement. Holders presenting over constrained transports MAY substitute a `proofArtifactRef` (§G.7).

#### G.2.4 Slot Declaration

```json
{
  "slotId": "slot:proof-of-unique-human-iris-2026",
  "credentialType": "ProofOfUniqueHumanCredential",
  "displayLabel": "Proof of Unique Human Identity",
  "privacyMode": "selective-disclosure",
  "attestationRef": {
    "authority": "key:ed25519:z<biometric-network-authority>",
    "manifestHash": "sha256:...",
    "manifestVersion": "1"
  },
  "status": "active"
}
```

The display label avoids including the biometric modality because it is readable by anyone who resolves the passport manifest. However, `biometricModality` IS a mandatory disclosed statement at presentation time — it is circuit selection metadata that verifiers require to perform ZK proof verification, not personal biometric data. The distinction is: the modality ("iris") tells the verifier which verification algorithm to apply; it does not reveal anything about the holder's biometric template, measurements, or identity beyond the fact that an iris-based proof system was used.

#### G.2.5 Verifier Use

A verifier requiring Sybil resistance adds `credentialType: "ProofOfUniqueHumanCredential"` to their DisclosureRequest. Phase 3 (§12.4) verifies the issuer's signature on the attestation normally. The verifier's trust policy (§F.6) determines whether the specific biometric network's authority is accepted.

For verifiers who additionally need to detect if the same holder is attempting multiple enrollments within their own system (e.g., a UBI distributor preventing one person from holding two accounts), the holder's device computes a **context-bound nullifier** at presentation time:

```
contextNullifier = H(biometric_secret || verifierAuthority)
```

This value is included in the presentation's ZK proof public inputs alongside the `registryRoot`, and the ZK circuit additionally proves: "I know a `biometric_secret` such that `contextNullifier == H(biometric_secret || verifierAuthority)`." The verifier stores this context-bound nullifier in their own registry. If the same holder presents again, the nullifier repeats — double-enrollment within that verifier's system is detected. If two different verifiers share context-bound nullifiers, they are computationally unrelated (different `verifierAuthority` → different hash output), so no cross-verifier correlation is possible.

Verifiers requesting context-bound nullifiers SHOULD include `requireContextNullifier: true` in their DisclosureRequest (application-layer extension). Verifiers MUST NOT request the registry nullifier — it is never output from the ZK circuit and no conforming implementation will provide it.

### G.3 Holder-to-Credential Binding: Device Theft Resistance

#### G.3.1 The Problem

Section 4.1's invariant — the keypair IS the passport — has a physical attack surface. If an adversary compromises the holder's device (theft, coercion, advanced malware against a hardware enclave), they obtain a cryptographic identity that produces mathematically valid presentations indistinguishable from the legitimate holder. For high-value credentials (government identity, financial access, security clearance), this is unacceptable.

The challenge is to bind the credential not just to a keypair but to the biological person who was issued that credential, without creating a centralized biometric database or transmitting biometric data to verifiers.

#### G.3.2 The ZK Biometric Commitment Pattern

This pattern adds a biometric commitment to the Tier 2 Attestation Manifest at issuance time. At presentation time, the holder's device generates a local ZK proof that a live biometric scan matches the commitment. The proof is included in the presentation. The verifier receives the proof — never the biometric data.

**Issuance flow:**

1. The high-assurance issuer (e.g., a government identity authority) obtains the holder's biometric template during in-person enrollment.
2. The issuer computes a biometric commitment: `bioCommitment = Commit(biometricTemplate, randomBlinding)` using a hiding and binding commitment scheme (e.g., Pedersen commitment over Ristretto255).
3. The issuer embeds `bioCommitment` in the Tier 2 claim payload as a `biometricBinding` field.
4. The issuer publishes the Attestation Manifest. The `biometricBinding.commitment` value is a mandatory-disclosure field — verifiers who require biometric binding need to see it to verify the presentation proof.

**Presentation flow:**

1. A high-security verifier requests a `BiometricBoundCredential` with `biometricVerificationRequired: true` in their DisclosureRequest (application-layer extension).
2. The holder's device prompts for a live biometric scan (FaceID, fingerprint, iris).
3. The device generates a ZK proof: "The biometric I just captured matches the commitment `bioCommitment` embedded in the attestation, using blinding factor known only to this device."
4. The proof is attached to the presentation's disclosed slot as a `biometricProof` field.
5. The verifier runs Phase 3 (§12.4) as normal and additionally verifies the ZK biometric proof against the disclosed `bioCommitment`.

The verifier learns: the person holding the device right now is the same biological person who was issued this credential. They receive no biometric data.

#### G.3.3 Claim Schema for Biometric-Bound Credentials

Following claim atomization principles (§F.4.3), commitment metadata is separated from the commitment value to allow independent disclosure:

```json
{
  "claim": {
    "@type": "hiri:passport:BiometricBoundCredential",
    "credentialType": "BiometricBoundCredential",
    "wrappedCredentialType": "GovernmentIdVerification",
    "biometricBinding": {
      "commitmentScheme": "PedersenCommitment-Ristretto255",
      "biometricModality": "face",
      "commitment": "<base64url-encoded-commitment>",
      "commitmentVersion": "1",
      "enrolledAt": "2026-03-01T00:00:00Z"
    },
    "governmentIdFields": {
      "idType": "passport",
      "issuingCountry": "US",
      "expiryDate": "2036-03-01"
    },
    "attestedAt": "2026-03-01T09:00:00Z",
    "validUntil": "2036-03-01T00:00:00Z"
  }
}
```

After URDNA2015 canonicalization, `biometricBinding.commitment` and `biometricBinding.biometricModality` are distinct N-Quad statements — independently disclosable per the selective disclosure mechanism. The `biometricBinding.commitment` statement SHOULD be mandatory in the attestation's selective-disclosure index: it is meaningless to claim biometric binding without disclosing the commitment that binds it.

#### G.3.4 ZK Proof Attachment in Presentations

The ZK biometric proof is generated fresh at each presentation from a live biometric capture and attached as an extension field on the disclosed slot object. It is NOT part of the Passport Manifest or Attestation Manifest:

```json
{
  "presentationSlotToken": "HmacDerivedToken-...",
  "credentialType": "BiometricBoundCredential",
  "privacyMode": "selective-disclosure",
  "attestationRef": { "..." : "..." },
  "disclosureProof": { "..." : "..." },
  "biometricProof": {
    "proofType": "ZKBiometricMatchProof",
    "commitmentScheme": "PedersenCommitment-Ristretto255",
    "proofArtifact": "<base64url-ZK-proof>",
    "publicInputs": {
      "commitment": "<base64url-commitment-matching-attestation>",
      "presentationNonce": "<base64url-nonce-from-DisclosureRequest>"
    },
    "generatedAt": "2026-03-15T10:30:00Z"
  }
}
```

The `presentationNonce` is bound into the ZK proof to prevent pre-generated proof replay. An adversary who captures a valid `biometricProof` from one session cannot reuse it against a verifier issuing a different nonce.

#### G.3.5 Device Storage of Biometric Blinding Factor

The Pedersen commitment blinding factor MUST be stored in the holder's hardware-backed secure storage alongside the passport signing key and slot blinding key (§14.10). Its loss means the holder can no longer generate valid ZK match proofs against enrolled commitments — effectively invalidating biometric binding for those credentials. Key rotation (§13.5) SHOULD trigger re-enrollment with new commitments if the blinding factor is stored in hardware tied to the old key.

### G.4 Biometric Key Recovery

#### G.4.1 The Problem

Section 14.6 addresses holder key compromise: publish a KeyDocument revocation, rotate to a new keypair. This works when the holder still has access to the old device or a secure backup and can sign the revocation with the old key.

It fails entirely when the device is lost with no backup. In this scenario the old HIRI authority cannot be revoked (no key available to sign the revocation), and the new genesis passport has no cryptographic relationship to the old credential history. All previously accumulated credentials must be re-obtained from scratch.

#### G.4.2 The Biometric Recovery Oracle Pattern

A biometric network can act as a **decentralized recovery oracle**, using physical uniqueness as the basis for linking an old lost authority to a new authority — without any centralized corporate helpdesk.

The mechanism uses a Mode 5 Third-Party Attestation (Privacy Extension §10) in a specialized configuration: the biometric network attests that the holder presenting a new keypair is the same biological person who enrolled under the old keypair.

**Recovery flow:**

1. **Holder generates new authority.** A fresh Ed25519 keypair produces a new HIRI authority (`new-authority`).

2. **Holder authenticates against the biometric network.** The holder's new device proves to the biometric network's ZK system that their biometric commitment is already enrolled in the uniqueness registry (originally linked to `old-authority`'s enrollment).

3. **Network issues a Key Continuity Attestation.** The biometric network publishes a Mode 5 `hiri:AttestationManifest` asserting that `new-authority` and `old-authority` belong to the same enrolled biological person:

```json
{
  "@type": "hiri:AttestationManifest",
  "@id": "hiri://key:ed25519:z<biometric-network-authority>/attestation/recovery-holder-001",

  "hiri:privacy": { "mode": "attestation" },

  "hiri:attestation": {
    "subject": {
      "type": "hiri:KeyContinuitySubject",
      "oldAuthority": "key:ed25519:z<old-authority>",
      "newAuthority": "key:ed25519:z<new-authority>",
      "continuityBasis": "biometric-uniqueness-proof"
    },
    "claim": {
      "@type": "hiri:passport:KeyContinuityAttestation",
      "credentialType": "KeyContinuityAttestation",
      "continuityProof": {
        "proofType": "ZKBiometricContinuityProof",
        "oldEnrollmentNullifier": "<nullifier-from-old-authority-enrollment>",
        "newEnrollmentNullifier": "<nullifier-from-new-authority-enrollment>",
        "proofArtifact": "<base64url-ZK-proof-of-same-biometric>",
        "publicInputs": {
          "registryRoot": "<hex-merkle-root>",
          "oldNullifier": "<base64url>",
          "newNullifier": "<base64url>"
        }
      },
      "recoveryReason": "device-loss",
      "attestedAt": "2026-04-01T09:00:00Z"
    },
    "evidence": {
      "method": "biometric-continuity-verification",
      "description": "Holder authenticated against biometric uniqueness registry. ZK proof confirms old and new enrollment nullifiers derive from the same biometric commitment. Old authority key assumed lost — no revocation signature available."
    }
  },

  "hiri:signature": {
    "type": "Ed25519Signature2020",
    "algorithm": "ed25519",
    "canonicalization": "JCS",
    "created": "2026-04-01T09:00:00Z",
    "verificationMethod": "hiri://key:ed25519:z<biometric-network-authority>/key/main#key-1",
    "proofValue": "z..."
  }
}
```

4. **Holder references the Key Continuity Attestation.** The new passport includes a `KeyContinuityAttestation` slot — the cryptographic thread linking the new passport to the old credential history.

5. **Holders re-link credentials progressively.** Old Tier 2 credentials have `holderAuthority: old-authority` in their subject binding and cannot be transferred cryptographically. The holder contacts issuers to obtain new attestation versions bound to `new-authority`. The Key Continuity Attestation provides the justification for re-issuance without in-person re-enrollment.

#### G.4.3 Verifier Handling of Key Continuity

When a verifier encounters a `KeyContinuityAttestation` slot, the verification result MUST surface this explicitly. The verifier knows that the chain between old and new authority is verifiable only through the biometric network's attestation, not through HIRI's cryptographic signing chain (the old key is lost). The effective trust level for claims about `old-authority`'s credential history is `"partial"` — dependent on the biometric network's organizational authority bootstrap trust level (§12.5). Verifiers SHOULD require the biometric network to be a `trustLevel: "full"` proxy (§F.6.1) before accepting key continuity attestations as sufficient basis for re-linking high-value credentials.

#### G.4.4 The Absence-of-Revocation Problem

A recovered passport leaves the old HIRI authority in an ambiguous state: not revoked (no key to sign a revocation), not active (the holder no longer controls it). Passive verifier discovery of a Key Continuity Attestation — which lives on a different branch of the identity graph — cannot be relied upon to protect against an active adversary presenting the stolen device. A verifier checking only the stolen device's old passport has no cryptographic reason to go looking for a Key Continuity Attestation it does not know exists.

The mitigation is **issuer-side biometric revocation** via the Oracle Notification Protocol (§G.4.5), which activates the existing Tier 2 Override mechanism (§12.4) without requiring verifiers to change their verification behavior.

Verifiers encountering a passport whose `holder.authority` matches an `oldAuthority` field in a Key Continuity Attestation they have independently discovered SHOULD treat that old authority as effectively superseded, with trust level no higher than the biometric network's attestation trust level.

#### G.4.5 Oracle Notification Protocol (INFORMATIVE)

When the Biometric Recovery Oracle issues a Key Continuity Attestation, it SHOULD proactively notify participating Tier 2 issuers — specifically, any issuer whose Credential Attestation Manifests include the `old-authority` as `holderAuthority` in their subject binding.

**Notification mechanism:**

1. **Subscriber registry.** The Biometric Network maintains a subscriber registry of Tier 2 issuers who have issued credentials against authorities enrolled in the uniqueness registry. Issuers MAY subscribe by publishing a `hiri:OracleSubscription` declaration in their KeyDocument, identifying the biometric network authority they subscribe to and providing a notification endpoint.

2. **Oracle notification.** Upon issuing a Key Continuity Attestation for `old-authority → new-authority`, the Oracle sends a signed notification to all subscribed issuers that have credentials bound to `old-authority`.

3. **Issuer revocation.** Upon receiving a verified Oracle notification, a subscribing issuer SHOULD publish a new Attestation Manifest version for the affected credential with an explicit revocation claim:

```json
{
  "hiri:attestation": {
    "claim": {
      "credentialType": "EmploymentCredential",
      "revoked": true,
      "revocationReason": "holder-key-recovery",
      "revocationAt": "2026-04-01T10:00:00Z",
      "supersededBy": {
        "newHolderAuthority": "key:ed25519:z<new-authority>",
        "keyContinuityAttestationRef": "hiri://key:ed25519:z<oracle-authority>/attestation/recovery-holder-001"
      }
    }
  }
}
```

4. **Tier 2 Override fires.** When a verifier now checks the stolen device's old passport in Phase 3, the issuer's attestation chain returns `claim.revoked: true`. The Tier 2 Override rule (§12.4) applies: effective slot status becomes `"issuer-revoked"` regardless of the Tier 1 slot `status: "active"`. `ATTESTATION_TIER2_OVERRIDE_REVOKED` is reported. The stolen presentation fails.

**Why this works without protocol changes:** The Oracle Notification Protocol is an application-layer subscription and notification mechanism. It does not introduce new HIRI manifest types or verification steps. It activates the Tier 2 Override mechanism that already exists and is already normatively required (§12.4). Verifiers who implement §12.4 correctly gain stolen-device protection automatically once subscribing issuers publish revocations.

**Subscription declaration example (KeyDocument extension):**

```json
{
  "@type": "hiri:KeyDocument",
  "hiri:authority": "key:ed25519:z<issuer-authority>",
  "hiri:oracleSubscriptions": [
    {
      "oracleAuthority": "key:ed25519:z<biometric-network-authority>",
      "subscriptionType": "key-continuity-notifications",
      "notificationEndpoint": "https://issuer.example.com/hiri/oracle-notify",
      "subscribedSince": "2026-03-01T00:00:00Z"
    }
  ]
}
```

**Limitation acknowledgment:** The Oracle Notification Protocol depends on issuers subscribing and responding. An issuer who does not subscribe will not publish a revocation. For high-assurance credential types (`GovernmentIdVerification`, `BackgroundCheckClearance`), issuers SHOULD subscribe to all biometric networks whose holders they have issued credentials against. This is a governance and ecosystem adoption problem, not a protocol problem — the mechanism is available; participation determines its effectiveness.

### G.5 Privacy Requirements Summary

All biometric credential patterns in this appendix share a common privacy requirement set:

| Requirement | Applies To |
|-------------|-----------|
| Raw biometric templates MUST NOT appear in any HIRI artifact | All patterns |
| Biometric commitments MUST use hiding commitment schemes | G.3, G.4 |
| ZK proofs MUST bind the presentation nonce to prevent replay | G.3 |
| **Registry nullifiers MUST NOT appear in any presentation or manifest** | G.2, G.4 |
| **Context-bound nullifiers (verifierAuthority-scoped) MUST be used in presentation public inputs** | G.2 |
| Registry nullifiers MUST be deterministic per-biometric (enables double-enrollment detection at registry) | G.2, G.4 |
| Registry and context-bound nullifiers MUST NOT be reversible to the biometric template | G.2, G.4 |
| Biometric blinding factors MUST be stored in hardware-backed secure storage | G.3 |
| Biometric modality MUST be a mandatory-disclosure statement (circuit selection metadata) | G.2, G.3 |
| Key Continuity Attestations MUST be surfaced explicitly in verification results | G.4 |
| Oracle Notification subscriptions SHOULD be published by high-assurance issuers | G.4.5 |

### G.6 Integration Summary

```
HIRI Digital Passport
        │
        ├── Credential Slot: ProofOfUniqueHumanCredential
        │     └── Issuer: Biometric Network (decentralized uniqueness registry)
        │           └── Content: ZK Merkle inclusion proof
        │                 ├── Private wire: registryNullifier (NEVER exposed)
        │                 └── Public output: registryRoot + contextNullifier (verifier-scoped)
        │                       └── Proves: this keypair ↔ exactly one biological human
        │
        ├── Credential Slot: BiometricBoundCredential (wraps GovernmentIdVerification)
        │     └── Issuer: Government Identity Authority
        │           └── Content: ZK Pedersen commitment of biometric template
        │                 └── Presentation: ZK match proof (live biometric vs commitment)
        │                       └── Proves: holder of device = person originally enrolled
        │
        └── Credential Slot: KeyContinuityAttestation  (recovery case only)
              └── Issuer: Biometric Network (recovery oracle)
                    ├── Content: ZK proof that old-authority and new-authority
                    │     share the same biometric enrollment
                    │           └── Enables: credential re-issuance without
                    │                 physical re-enrollment
                    └── Oracle Notification → Tier 2 issuers → revocation attestation
                          └── Tier 2 Override fires → stolen device rejected

None of these patterns require changes to HIRI Protocol v3.1.1, Privacy Extension
v1.4.1, or the normative sections of this specification. They are applications of
existing Tier 2 attestation, Mode 3 selective disclosure, and Mode 5 third-party
attestation to a specific class of high-assurance identity claims.
```

### G.7 ZK Proof Transport Guidance (INFORMATIVE)

#### G.7.1 Payload Size Context

ZK proof artifacts vary substantially in size depending on the proof system:

| Proof System | Typical Size | Transport Impact |
|-------------|-------------|-----------------|
| Groth16 (SNARK) | ~200 bytes | Negligible — fits in a QR code alongside other payload |
| PLONK (SNARK) | ~1–2 KB | Minimal — comfortably within BLE/NFC MTU windows |
| FRI-based STARK | ~40–200 KB | Severe — will exceed NFC NDEF limits and BLE ATT MTU |
| Post-quantum STARK | 50–250 KB | Not suitable for inline constrained-transport presentation |

A `BiometricBoundCredential` or `ProofOfUniqueHumanCredential` presentation over NFC, BLE, or a QR code MUST account for proof size when deciding whether to inline the `proofArtifact` or use a `proofArtifactRef`.

#### G.7.2 The `proofArtifactRef` Structure

When a proof artifact is too large to inline in the presentation payload, the holder substitutes a `proofArtifactRef` in place of the raw `proofArtifact` field:

```json
{
  "biometricProof": {
    "proofType": "ZKBiometricMatchProof",
    "commitmentScheme": "PedersenCommitment-Ristretto255",
    "proofArtifactRef": {
      "uri": "https://holder-agent.example.com/proofs/pres-2026-03-15-001.cbor",
      "artifactHash": "sha256:3f7a9c2e...",
      "proofSystem": "PLONK",
      "byteSize": 1842
    },
    "publicInputs": {
      "commitment": "<base64url-commitment>",
      "presentationNonce": "<base64url-nonce>"
    },
    "generatedAt": "2026-03-15T10:30:00Z"
  }
}
```

**`uri`** — HTTPS URL where the verifier can fetch the proof artifact after receiving the presentation frame. The URL MUST be served by the holder or the holder's agent. It MUST be specific to this presentation instance (not a static, reusable endpoint).

**`artifactHash`** — SHA-256 hash of the proof artifact bytes (raw-sha256 format). The verifier MUST verify this hash after fetching — this cryptographically binds the out-of-band artifact to the signed presentation. A verifier who accepts a fetched artifact without hash verification is vulnerable to a proof substitution attack.

**`proofSystem`** — The ZK proof system used. Required for verifier-side circuit selection when the proof system is not inferrable from the commitment scheme alone.

**`byteSize`** — INFORMATIVE byte count to allow the verifier to pre-allocate buffer space before fetching.

#### G.7.3 Verification Flow for proofArtifactRef

When a verifier receives a presentation containing `proofArtifactRef` instead of inline `proofArtifact`:

1. Complete all standard presentation verification steps (Phase 1–4, §12.2–12.5) against the presentation as received.
2. Fetch the proof artifact from `proofArtifactRef.uri` via HTTPS using the following normative retry policy:
   - **Timeout:** MUST enforce a per-attempt timeout of 10 seconds.
   - **Retries:** MUST retry up to 3 times total (1 initial attempt + 2 retries).
   - **Backoff:** MUST use exponential backoff starting at 1 second between attempts (1s, 2s).
   - **Total budget:** Maximum 34 seconds total fetch time before declaring failure.
3. Compute `SHA-256(fetchedBytes)` and compare to `proofArtifactRef.artifactHash`. If they do not match, report `PRESENTATION_PROOF_ARTIFACT_HASH_MISMATCH` and reject. Hash verification is non-negotiable — it binds the out-of-band artifact to the signed presentation.
4. Verify the ZK proof using the `publicInputs` declared in the presentation (not from the fetched artifact).
5. If proof verification succeeds, the presentation is fully verified with biometric binding confirmed.

**Caching policy (NORMATIVE):** Successfully fetched and hash-verified proof artifacts MUST be cached by `artifactHash` for the duration of the presentation's validity window (§11.6, RECOMMENDED maximum 24 hours from `hiri:timing.created`). Within this window, a verifier MUST NOT re-fetch an artifact it has already verified — the hash is a content address; the artifact is immutable. After the validity window expires, the cached artifact MUST be discarded.

**On fetch failure after all retries:** Report `PRESENTATION_PROOF_ARTIFACT_UNAVAILABLE`. Set `biometricBinding: "unverifiable-offline"`. The underlying credential's issuer signature and Phase 3 verification remain valid — only the device-liveness guarantee is absent. The verifier's application-layer policy determines whether to accept the credential without biometric binding confirmed.

#### G.7.4 Constrained Transport Recommendations

| Transport | Max Payload | Recommended Approach |
|-----------|-------------|---------------------|
| NFC NDEF | ~32 KB (Type 4 tag) | Use `proofArtifactRef` for any STARK-based proof; SNARK/PLONK inline is acceptable |
| BLE ATT MTU | ~512 bytes (default) / ~64 KB (extended) | Use `proofArtifactRef` for all ZK proofs unless extended MTU is negotiated |
| QR Code (L error correction) | ~2,953 bytes | Use `proofArtifactRef` for all ZK proofs; inline only Groth16 if QR version permits |
| HTTPS / local network | No practical limit | Inline `proofArtifact` preferred; avoids additional round-trip |

For contexts where even the `proofArtifactRef` URI cannot be served (fully offline verification), the verifier MUST treat biometric binding as `"unverifiable-offline"` and surface this status explicitly. The underlying credential (e.g., `GovernmentIdVerification`) retains its issuer-verified status; only the device-liveness guarantee is absent.

---

## Appendix H: Normative Test Vectors

This appendix is NORMATIVE. Implementations MUST produce identical outputs for each input vector. Divergence indicates an interoperability-breaking implementation bug.

### H.1 Presentation Slot Token Derivation

**Inputs:**

```
slotBlindingKey (hex): 0102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f20
slotId (UTF-8):        "slot:employment-ecoimpact-2026"
requestNonce (hex):    a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2
verifierAuthority:     "key:ed25519:zABC123verifier456authority789"
```

**Derivation (§11.7.3):**

```
HMAC-SHA256 key   = slotBlindingKey (32 bytes)
HMAC-SHA256 msg   = UTF8("slot:employment-ecoimpact-2026")
                    || 0x00
                    || requestNonce (32 bytes, decoded from hex)
                    || 0x00
                    || UTF8("key:ed25519:zABC123verifier456authority789")
```

**Expected output (base64url, no padding):**

```
presentationSlotToken = "KXvqR7mN2oP4sT8wV1xY3zB5cD9eF6gH"
```

*(Implementation note: this vector uses toy values; production implementations MUST verify against reference implementation output.)*

### H.2 P-256 Authority Encoding

**Input:**

```
compressed P-256 public key (hex, 33 bytes):
  02a8f3c4d7e9b2a1f0e8c6d5b4a3928170f6e5d4c3b2a19087f6e5d4c3b2a190
```

**Derivation (§6.5.4):**

```
multicodecPrefix = [0x80, 0x24]
keyBytes = concat([0x80, 0x24], compressedKey)   // 35 bytes total
authority = "key:p256:z" + base58btc(keyBytes)
```

**Expected output:**

```
authority = "key:p256:z2LmNpQrStUvWxYzAbCdEfGh3456789TestVectorOnly"
```

### H.3 Nonce Validation Boundary Cases

Implementations MUST accept or reject the following nonce values as specified:

| Nonce Value | Expected Result | Reason |
|-------------|----------------|--------|
| `"YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXoxMjM0NTY3ODkwYWJjZA"` (43 chars, valid base64url) | ACCEPT | 32 bytes, valid encoding |
| `"YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXoxMjM0NTY3ODkwYWJj"` (42 chars) | REJECT | Only 31 bytes decoded |
| `"YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXoxMjM0NTY3ODkwYWJjZA=="` (with padding) | REJECT | Padding not permitted (no-pad base64url required) |
| `""` (empty string) | REJECT | Missing nonce |
| `"not-base64url-!@#$"` | REJECT | Invalid encoding |

### H.4 RevocationLogEntry Signing

**Input (canonical JCS bytes before signing):**

```json
{
  "@context": ["https://hiri-protocol.org/spec/v3.1","https://hiri-protocol.org/passport/v1"],
  "@type": "hiri:RevocationLogEntry",
  "credentialType": "EmploymentCredential",
  "holderAuthority": "key:ed25519:zHolder001",
  "issuerAuthority": "key:ed25519:zIssuer001",
  "logSequenceNumber": 1,
  "manifestHash": "sha256:e08da327testonly",
  "manifestVersion": "1",
  "revokedAt": "2026-04-01T10:00:00Z",
  "revocationReason": "holder-request"
}
```

Implementations MUST apply JCS (RFC 8785) to produce the canonical byte sequence before signing, and MUST produce identical canonical bytes for the object above (key ordering and unicode normalization per JCS rules).

### H.5 HMAC Slot Token — Known-Answer Test

Implementations MUST register a known-answer test using the following fixed-seed inputs and verify the output matches before deploying in production:

```
Test label: "hiri-passport-slottoken-kat-v1"
slotBlindingKey: 32 zero bytes (0x00 * 32)
slotId: "slot:test"
requestNonce: 32 zero bytes (0x00 * 32)
verifierAuthority: "key:ed25519:zTest"

Expected HMAC-SHA256 output (hex):
  [compute from reference implementation and pin here]

Expected presentationSlotToken (base64url):
  [compute from reference implementation and pin here]
```

The placeholder values MUST be replaced with reference implementation output before publishing final test vectors. Implementations SHOULD run this KAT in CI against every target runtime.

### H.6 Merkle Leaf Hash Canonicalization

This vector tests the leaf hash computation defined in §16.10.1.

**Input — minimal RevocationLogEntry (with logSequenceNumber assigned):**

```json
{
  "@context": ["https://hiri-protocol.org/spec/v3.1","https://hiri-protocol.org/passport/v1"],
  "@type": "hiri:RevocationLogEntry",
  "issuerAuthority": "key:ed25519:zIssuer001",
  "logSequenceNumber": 1,
  "manifestHash": "sha256:e08da327testonly",
  "revokedAt": "2026-04-01T10:00:00Z",
  "revocationReason": "holder-request"
}
```

**Step 1 — JCS canonicalization (RFC 8785):**

JCS sorts object keys lexicographically at all nesting levels and removes insignificant whitespace. The canonical UTF-8 byte sequence for the above object is:

```
{"@context":["https://hiri-protocol.org/spec/v3.1","https://hiri-protocol.org/passport/v1"],"@type":"hiri:RevocationLogEntry","issuerAuthority":"key:ed25519:zIssuer001","logSequenceNumber":1,"manifestHash":"sha256:e08da327testonly","revokedAt":"2026-04-01T10:00:00Z","revocationReason":"holder-request"}
```

**Step 2 — SHA-256 of canonical bytes:**

```
leafHash = SHA-256(JCS(entry))
         = [compute from reference implementation and pin here]
```

**Verification rule:** Two implementations MUST produce byte-identical JCS output for logically identical JSON objects (regardless of original key ordering). Any divergence in the `leafHash` output indicates a JCS implementation bug and MUST be treated as a conformance failure.

### H.7 Merkle Inclusion Proof Verification

This vector tests the inclusion proof verification algorithm defined in §16.10.3.

**Given:**
- A tree of 5 leaves with leaf hashes: `[h0, h1, h2, h3, h4]` (each a 32-byte SHA-256 digest)
- Verify that leaf at index 2 (`h2`) is included in the root

**Tree structure:**
```
Level 0: [h0,   h1,   h2,   h3,   h4]
Level 1: [n01,        n23,        h4 ]   where n01=SHA256(h0||h1), n23=SHA256(h2||h3)
Level 2: [n0123,                  h4 ]   where n0123=SHA256(n01||n23)
Root:    SHA256(n0123||h4)
```

**Inclusion proof for leaf index 2:**
```json
{
  "leafIndex": 2,
  "treeSize": 5,
  "auditPath": [
    {"hash": "sha256:<h3>",    "side": "right"},
    {"hash": "sha256:<n01>",   "side": "left"},
    {"hash": "sha256:<h4>",    "side": "right"}
  ]
}
```

**Verification steps:**
```
currentHash = h2
Step 1: side=right → currentHash = SHA256(currentHash || h3)  = n23
Step 2: side=left  → currentHash = SHA256(n01 || currentHash) = n0123
Step 3: side=right → currentHash = SHA256(currentHash || h4)  = root
assert currentHash == checkpoint.rootHash  → PASS
```

Implementations MUST verify this algorithm produces a PASS for the above inputs before deployment. The vector values (`h0`–`h4`, `n01`, `n23`, `n0123`, `root`) MUST be computed from known byte inputs and pinned in the reference implementation test suite.

**Odd-leaf promotion test:** For the leaf at index 4 (`h4`) in a 5-leaf tree, the auditPath is:
```json
[
  {"hash": "sha256:<n0123>", "side": "left"}
]
```
Verification: `SHA256(n0123 || h4) == root`. Implementations MUST handle promoted unpaired leaves correctly — do NOT duplicate the unpaired leaf.

### H.8 proofArtifactRef Fetch-and-Verify Flow

This vector defines the normative verification sequence for the `proofArtifactRef` flow (§G.7.3).

**Presentation fragment (declared public inputs):**
```json
{
  "biometricProof": {
    "proofType": "ZKBiometricMatchProof",
    "proofArtifactRef": {
      "uri": "https://holder-agent.example.com/proofs/pres-test-001.cbor",
      "artifactHash": "sha256:3f7a9c2edeadbeef...",
      "proofSystem": "Groth16",
      "byteSize": 192
    },
    "publicInputs": {
      "commitment": "abc123base64url...",
      "presentationNonce": "YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXoxMjM0NTY3ODkwYWJjZA"
    },
    "generatedAt": "2026-03-15T10:30:00Z"
  }
}
```

**Verification sequence:**

| Step | Action | Pass Condition | Failure Code |
|------|--------|---------------|-------------|
| 1 | Complete Phase 1–4 on presentation without artifact | All phases pass | Per-phase codes |
| 2 | Fetch URI with 10s timeout, up to 3 attempts (1s, 2s backoff) | HTTP 200 with bytes | `PRESENTATION_PROOF_ARTIFACT_UNAVAILABLE` |
| 3 | Compute `SHA-256(fetchedBytes)` | Equals `"sha256:3f7a9c2edeadbeef..."` | `PRESENTATION_PROOF_ARTIFACT_HASH_MISMATCH` |
| 4 | Verify ZK proof using `publicInputs` from presentation | Proof verifies | `ZK_PROOF_VERIFICATION_FAILED` |
| 5 | Cache artifact by `artifactHash` for presentation validity window | Cache entry stored | — |

**Timeout/retry sequence:**
```
Attempt 1: t=0s     → wait up to 10s
Attempt 2: t=11s    → wait 1s before retry, then up to 10s
Attempt 3: t=22s    → wait 2s before retry, then up to 10s
Total budget: ≤ 34s → PRESENTATION_PROOF_ARTIFACT_UNAVAILABLE
```

**Cache hit:** If the same `artifactHash` was fetched and verified within the presentation validity window, steps 2–4 MUST be skipped and the cached verification result MUST be used. Implementations MUST NOT re-fetch a cached, hash-verified artifact within its validity window.

### H.9 Interoperability Test Results Matrix

This section is NORMATIVE. It defines the required two-implementation test matrix that must be populated and published before v1.9.0 may be declared a full release (§1.5, checklist item 2). The table below shows the required structure; actual pass/fail values MUST be filled in by the CI pipeline.

**Required implementations:**
- **Impl-A:** Node.js / WASM reference implementation (`https://github.com/hiri-protocol/passport-reference`)
- **Impl-B:** Go independent implementation (to be designated by the release steward)

| Test Vector | Impl-A | Impl-B | Cross-Check (A output == B output) |
|-------------|--------|--------|-------------------------------------|
| H.1 Slot token derivation | PENDING | PENDING | PENDING |
| H.2 P-256 authority encoding | PENDING | PENDING | PENDING |
| H.3 Nonce validation — all 5 cases | PENDING | PENDING | PENDING |
| H.4 RevocationLogEntry JCS canonicalization | PENDING | PENDING | PENDING |
| H.5 HMAC slot token KAT (all-zero inputs) | PENDING | PENDING | PENDING |
| H.6 Merkle leaf hash | PENDING | PENDING | PENDING |
| H.7 Inclusion proof — 5-leaf tree, leafIndex=2 | PENDING | PENDING | PENDING |
| H.7 Inclusion proof — odd-leaf (leafIndex=4) | PENDING | PENDING | PENDING |
| H.8 proofArtifactRef fetch-and-verify sequence | PENDING | PENDING | N/A (behavioral) |
| H.9.1 3-leaf hex worked example (§16.10.4) — all node hashes | PENDING | PENDING | PENDING |
| H.10 Passport-Hardened omittedSlotCount padding | PENDING | PENDING | PENDING |
| H.10 Passport-Hardened timestamp smearing | PENDING | PENDING | PENDING |
| H.10 Issuer authority HMAC obfuscation | PENDING | PENDING | PENDING |

**Acceptance criteria:** Every row in the Cross-Check column MUST show PASS before full release. A PASS requires: (a) both implementations produce byte-identical output for the same input, and (b) the output matches the expected value pinned in the reference implementation test suite. Any FAIL blocks release and requires a spec or implementation correction.

**CI publication:** The CI pipeline MUST publish this table as a machine-readable JSON artifact at `https://github.com/hiri-protocol/passport-reference/releases/tag/v1.9.0/interop-matrix.json`. The JSON schema mirrors the table above with `"pass"`, `"fail"`, or `"pending"` string values.

### H.10 Passport-Hardened Test Vectors

This section is NORMATIVE. Implementations claiming the Passport-Hardened designation MUST pass all vectors in this section.

#### H.10.1 omittedSlotCount Padding (§J.2, Q=5)

| True omittedSlotCount | Expected paddedOmittedSlotCount |
|----------------------|--------------------------------|
| 0 | 0 |
| 1 | 5 |
| 3 | 5 |
| 5 | 5 |
| 6 | 10 |
| 10 | 10 |
| 11 | 15 |
| 24 | 25 |

Formula: `ceil(trueCount / 5) * 5`. Implementations MUST reject any Passport-Hardened presentation where `omittedSlotCount` is not a multiple of 5 (unless it is 0).

#### H.10.2 Timestamp Smearing (§J.3)

| Field | Raw Value | Smeared Value |
|-------|-----------|---------------|
| `attestedAt` | `2026-03-15T09:23:47Z` | `2026-03-15T00:00:00Z` |
| `attestedAt` | `2026-03-15T23:59:59Z` | `2026-03-15T00:00:00Z` |
| `validFrom` | `2026-03-15T00:00:00Z` | `2026-03-01T00:00:00Z` |
| `validUntil` | `2027-03-15T00:00:00Z` | `2027-03-01T00:00:00Z` |
| `validUntil` | `2027-03-01T00:00:00Z` | `2027-03-01T00:00:00Z` (already month-boundary) |

**Verifier acceptance rule:** Verifiers receiving Passport-Hardened presentations MUST accept a smeared `validUntil` that differs from the attestation manifest's `validUntil` by up to 31 days. They MUST NOT reject presentations because the smeared value precedes the attested value by less than one calendar month.

#### H.10.3 Issuer Authority HMAC Obfuscation (§J.4)

**Inputs:**
```
slotBlindingKey:    0x00 * 32 (32 zero bytes)
issuerAuthority:    "key:ed25519:zIssuer001"
requestNonce:       0x00 * 32 (32 zero bytes, decoded from base64url)
verifierAuthority:  "key:ed25519:zVerifier001"
domain separator:   "issuer-token-v1"
```

**HMAC-SHA256 message construction:**
```
msg = UTF8("key:ed25519:zIssuer001")
      || 0x00
      || [32 zero bytes]
      || 0x00
      || UTF8("key:ed25519:zVerifier001")
      || 0x00
      || UTF8("issuer-token-v1")
```

**Expected output (base64url, no padding):**
```
issuerToken = [compute from reference implementation and pin here]
```

The domain separator `"issuer-token-v1"` MUST be present as the final field separated by `0x00`. Implementations MUST verify that slot tokens (§11.7.3) and issuer tokens (§J.4) never collide even with identical inputs — the domain separator ensures this.

#### H.10.4 Hash-Only Revocation Entry (§16.8.1)

**Input — full RevocationLogEntry (JCS canonical, as it would be hashed):**
```json
{"@type":"hiri:RevocationLogEntry","credentialType":"GovernmentIdVerification","holderAuthority":"key:ed25519:zHolder001","issuerAuthority":"key:ed25519:zIssuer001","logSequenceNumber":1,"manifestHash":"sha256:e08da327testonly","revokedAt":"2026-04-01T10:00:00Z","revocationReason":"holder-request"}
```

**Expected entryHash:**
```
entryHash = SHA-256(JCS(fullEntry))
          = [compute from reference implementation and pin here]
```

**Hash-Only Entry published to log:**
```json
{
  "@type": "hiri:HashOnlyRevocationEntry",
  "issuerAuthority": "key:ed25519:zIssuer001",
  "entryHash": "sha256:[entryHash from above]",
  "revokedAt": "2026-04-01T10:00:00Z",
  "logSequenceNumber": 1,
  "signature": { "...": "issuer signature" }
}
```

Verifiers MUST confirm `SHA-256(JCS(revealedEntry)) == entryHash` when the selective-reveal endpoint returns the full entry.

#### H.10.5 Passport-Hardened Profile Declaration

Presentations under the Passport-Hardened profile MUST include this exact declaration structure:

```json
{
  "hiri:presentation": {
    "metadataHardeningProfile": "passport-hardened-v1",
    "omittedSlotCountPaddingQuantum": 5,
    "timestampSmearingEnabled": true,
    "issuerAuthorityObfuscationEnabled": true
  }
}
```

Verifiers receiving a presentation with `metadataHardeningProfile: "passport-hardened-v1"` MUST apply smearing-tolerant timestamp validation and MUST NOT reject padded `omittedSlotCount` values as invalid.

---

## Appendix I: ZK Proof System Reference (INFORMATIVE)

This appendix is INFORMATIVE. It provides guidance for implementers selecting ZK proof systems for biometric credential types (Appendix G). Proof system selection affects proof size, verification cost, transport feasibility, and post-quantum security posture.

### I.1 Proof System Comparison

| Proof System | Proof Size | Verify Time (typical) | Prover Time | Post-Quantum | Recommended Use Case |
|-------------|-----------|----------------------|------------|-------------|---------------------|
| **Groth16** | ~200 bytes | ~1 ms | 1–5 s | No | QR code, NFC, BLE; maximum transport compatibility |
| **PLONK** | ~1–2 KB | ~2–5 ms | 3–10 s | No | HTTPS, BLE (extended MTU); balance of size and flexibility |
| **Marlin / Sonic** | ~2–4 KB | ~5–10 ms | 5–15 s | No | HTTPS; universal trusted setup |
| **FRI-based STARK** | 40–200 KB | 10–50 ms | 10–60 s | **Yes** | High-security server-to-server; post-quantum requirement |
| **Bulletproofs** | 1–10 KB | 10–100 ms (linear) | 5–30 s | No | Range proofs; no trusted setup required |
| **Halo2** | ~3–8 KB | ~5–15 ms | 5–20 s | No | HTTPS; recursive proof composition |

### I.2 Recommended Proof System by Use Case

| Use Case | Proof System | Rationale |
|----------|-------------|-----------|
| `ProofOfUniqueHumanCredential` (NFC/QR presentation) | Groth16 | Proof must fit in constrained transport; 200-byte target |
| `ProofOfUniqueHumanCredential` (HTTPS presentation) | PLONK or Halo2 | More flexible trusted setup; recursive proofs enable registry updates |
| `BiometricBoundCredential` (device liveness, NFC) | Groth16 | Same transport constraint; simple match proof |
| `BiometricBoundCredential` (device liveness, HTTPS) | PLONK | Allows richer biometric matching circuits |
| Context-bound nullifier derivation | Groth16 or PLONK | Relatively simple hash-based circuit |
| Key Continuity ZK proof (recovery) | PLONK or Halo2 | More complex biometric continuity circuit; HTTPS transport acceptable |
| Post-quantum biometric registry (future) | FRI-based STARK | When PQC requirement is mandated |

### I.3 Trusted Setup Considerations

Groth16 and PLONK require a trusted setup ceremony to generate circuit-specific proving and verifying parameters. For biometric network deployment:

- The trusted setup ceremony MUST be conducted using a multi-party computation (MPC) protocol with a sufficient number of independent participants.
- The ceremony transcript MUST be publicly auditable.
- The resulting verifying key MUST be published in the Oracle's KeyDocument and OracleGovernanceDocument (§17.2).
- Circuit updates (e.g., new biometric modality support) require a new trusted setup ceremony and new verifying key.

STARKs (FRI-based) require no trusted setup — only a public hash function. This is a governance advantage for post-quantum deployments.

### I.4 Verifier Cost Guidance

Verifiers running on resource-constrained edge devices (mobile phones, browser WASM, IoT) should select proof systems accordingly:

| Platform | Recommended Max Proof System Complexity | Notes |
|----------|-----------------------------------------|-------|
| Server-side verifier | Any | Full STARK acceptable |
| Mobile app (native) | Groth16 or PLONK | Verify in < 10 ms on modern hardware |
| Browser (WASM) | Groth16 | PLONK verifiable but slower; profile first |
| IoT / embedded | Groth16 only | 200-byte proof, ~1 ms verify with precomputed pairings |

---

## Appendix J: Metadata Hardening Profile (OPTIONAL normative)

This appendix defines the **Passport-Hardened** metadata hardening profile. It is OPTIONAL normative: implementations are not required to implement it, but implementations claiming the `Passport-Hardened` designation MUST implement all requirements in this appendix. The profile is additive to any base conformance level.

### J.1 Purpose

Even with slot blinding and minimum disclosure by default, a passive observer or frequent verifier can infer information from metadata that is not covered by the core protocol:

- `omittedSlotCount` reveals how many credentials the holder possesses beyond what was disclosed
- Attestation timestamps reveal when credentials were issued, potentially revealing employment start dates or certification timing
- Issuer authority strings in `withheldSlotSummary` identify which organizations the holder has relationships with
- Precise timing of presentation creation reveals behavioral patterns

The Metadata Hardening Profile closes these residual leakage channels.

### J.2 omittedSlotCount Padding

**NORMATIVE:** Implementations claiming Passport-Hardened MUST pad `omittedSlotCount` to the nearest multiple of a fixed quantum Q before including it in any presentation.

```
paddedOmittedSlotCount = ceil(trueOmittedSlotCount / Q) * Q
```

The RECOMMENDED value for Q is **5**. Implementations MAY choose a larger Q for higher privacy at the cost of less informative counts.

**Examples with Q = 5:**

| True omitted count | Disclosed count |
|-------------------|----------------|
| 0 | 0 |
| 1 | 5 |
| 2 | 5 |
| 3 | 5 |
| 6 | 10 |
| 11 | 15 |

An observer learns the holder has "at least N" credentials in some bracket, not the exact number.

**Holder software MUST NOT** expose the true `omittedSlotCount` in any user-facing API that verifiers can query. The padded value is canonical.

### J.3 Timestamp Smearing

Attestation timestamps in disclosed credential slots (`attestedAt`, `validFrom`, `validUntil`) MAY leak issuance timing that enables correlation. Implementations claiming Passport-Hardened MUST apply timestamp smearing before including timestamps in presentations:

- `attestedAt` MUST be rounded to the nearest calendar day (midnight UTC)
- `validFrom` and `validUntil` MUST be rounded to the nearest calendar month (first day of month, midnight UTC)

**Example:**

```
Raw attestedAt:   2026-03-15T09:23:47Z
Smeared:          2026-03-15T00:00:00Z

Raw validUntil:   2027-03-15T00:00:00Z
Smeared:          2027-03-01T00:00:00Z
```

Smearing applies only to values disclosed IN PRESENTATIONS — the original timestamps in the signed Credential Attestation Manifest are not modified. Verifiers receiving presentations under the Hardened profile MUST accept smeared timestamps and MUST NOT reject presentations because a smeared timestamp differs from the attested manifest timestamp by up to 31 days.

### J.4 Issuer Authority Obfuscation in Completeness Audits

When a completeness audit is requested (§11.5) and the holder complies, the `withheldSlotSummary` includes `attestationRef.authority` entries — which are the issuers' HIRI authority strings. Implementations claiming Passport-Hardened MUST obfuscate issuer authority strings in `withheldSlotSummary` entries by replacing them with a per-presentation HMAC-derived token:

```
issuerToken = base64url(
  HMAC-SHA256(
    key     = slotBlindingKey,
    message = UTF8(issuerAuthority) || 0x00
              || base64url_decode(requestNonce)
              || 0x00
              || UTF8(verifierAuthority)
              || 0x00
              || UTF8("issuer-token-v1")
  )
)
```

The domain separator `"issuer-token-v1"` prevents collision with the slot token derivation (§11.7.3). The resulting `issuerToken` replaces the raw authority string in `withheldSlotSummary.attestationRef.authority` for presentations under this profile.

Verifiers who require issuer identity for completeness audit purposes MUST explicitly request it through a separate issuer identity disclosure request — it cannot be inferred from the obfuscated token.

### J.5 Presentation Timing

Implementations claiming Passport-Hardened SHOULD introduce a random jitter of 0–500ms before computing and returning a presentation, to prevent timing side-channels that could correlate presentation generation with specific user actions.

### J.6 Profile Declaration

Presentations generated under the Passport-Hardened profile MUST include a profile declaration in the presentation header:

```json
{
  "hiri:presentation": {
    "metadataHardeningProfile": "passport-hardened-v1",
    "omittedSlotCountPaddingQuantum": 5,
    "timestampSmearingEnabled": true,
    "issuerAuthorityObfuscationEnabled": true
  }
}
```

Verifiers receiving a presentation with `metadataHardeningProfile` declared MUST apply the corresponding parsing rules (padded counts, smeared timestamps, obfuscated issuer tokens) and MUST NOT treat hardened values as malformed.

---

---

## Appendix K: Standards Interoperability Bridges (INFORMATIVE)

This appendix is INFORMATIVE. The bridges defined here are OPTIONAL compatibility layers. None modifies HIRI's normative signing, verification, privacy, or lifecycle mechanisms. HIRI's cryptographic mechanisms remain the authoritative path for artifact integrity and provenance in all bridge configurations. See §18 for the architectural principle governing this boundary.

### K.1 Bridge Design Invariant

Every bridge in this appendix follows the same invariant:

> The HIRI artifact is the payload. The external standard is the envelope or transport. HIRI's signing chain is canonical. The external standard's signing or serialization conventions are compatibility artifacts.

Implementers building on these bridges MUST NOT require verifiers to trust the external standard's signature as a substitute for HIRI verification.

---

### K.2 W3C Verifiable Credentials Compatibility Envelope

This bridge allows HIRI Credential Attestation Manifests to be represented as W3C Verifiable Credentials, enabling compatibility with VC wallets, VC verifiers, and the broader W3C VC ecosystem.

#### K.2.1 Mapping

| HIRI Concept | W3C VC Equivalent |
|-------------|-------------------|
| Issuer Authority | `issuer` (as a DID) |
| Holder Authority | `credentialSubject.id` (as a DID) |
| Credential Attestation Manifest | `credentialContent` (embedded in the VC) |
| Passport Presentation | `VerifiablePresentation` |
| HIRI `proofValue` | `proof.proofValue` |

#### K.2.2 VC Compatibility Envelope Structure

```json
{
  "@context": [
    "https://www.w3.org/2018/credentials/v1",
    "https://hiri-protocol.org/spec/v3.1",
    "https://hiri-protocol.org/passport/v1"
  ],
  "type": ["VerifiableCredential", "HIRIPassportCredential"],
  "id": "hiri://key:ed25519:z<issuer-authority>/attestation/employment-sarah-001",
  "issuer": "did:web:ecoimpact.com",
  "issuanceDate": "2026-03-01T09:00:00Z",
  "expirationDate": "2027-03-01T00:00:00Z",
  "credentialSubject": {
    "id": "did:key:z<holder-did-key>",
    "hiriPassportURI": "hiri://key:ed25519:z<holder-authority>/passport/main"
  },
  "credentialContent": {
    "type": "HIRIAttestationManifest",
    "manifestHash": "sha256:e08da327...",
    "manifestURI": "hiri://key:ed25519:z<issuer-authority>/attestation/employment-sarah-001"
  },
  "proof": {
    "type": "Ed25519Signature2020",
    "created": "2026-03-01T09:00:00Z",
    "verificationMethod": "did:web:ecoimpact.com#key-main",
    "proofPurpose": "assertionMethod",
    "proofValue": "z..."
  }
}
```

The `credentialContent.manifestHash` and `manifestURI` allow a VC-aware verifier to fetch and independently verify the full HIRI Attestation Manifest. The VC `proof` reuses the HIRI manifest's Ed25519 signature, re-encoded in the VC proof format. There is one signature, not two.

#### K.2.3 VC Presentation Bridge

A HIRI Passport Presentation MAY be wrapped in a W3C `VerifiablePresentation` for transport compatibility:

```json
{
  "@context": ["https://www.w3.org/2018/credentials/v1"],
  "type": ["VerifiablePresentation"],
  "holder": "did:key:z<holder-did-key>",
  "verifiableCredential": [
    { "...": "VC Compatibility Envelope for each disclosed slot" }
  ],
  "hiריPassportPresentation": {
    "type": "HIRIPassportPresentation",
    "presentationHash": "sha256:...",
    "presentationURI": "hiri://key:ed25519:z<holder-authority>/presentation/req-001"
  },
  "proof": {
    "type": "Ed25519Signature2020",
    "verificationMethod": "did:key:z<holder-did-key>#key-1",
    "proofValue": "z..."
  }
}
```

VC-aware verifiers process the `verifiableCredential` array normally. HIRI-aware verifiers SHOULD additionally fetch and verify the full `HIRIPassportPresentation` referenced in `hiריPassportPresentation.presentationURI`.

---

### K.3 vCard Claim Schema

This bridge provides a structured schema for personal contact information within HIRI credential claims, compatible with RFC 6350 (vCard).

#### K.3.1 vCard Claim Object

When a credential slot's attestation claim contains personal contact information, issuers SHOULD structure it as an atomized vCard-compatible object following claim atomization principles (§F.4):

```json
{
  "claim": {
    "@type": "hiri:passport:ContactIdentityCredential",
    "credentialType": "ContactIdentityCredential",
    "vcard": {
      "fn": "Sarah Thompson",
      "org": "EcoImpact Consulting",
      "title": "Environmental Scientist",
      "email": {
        "work": "sarah@ecoimpact.com"
      },
      "url": "https://ecoimpact.com/team/sarah"
    }
  }
}
```

After URDNA2015 canonicalization, each vCard field maps to a distinct N-Quad, enabling selective disclosure at field granularity. A holder can disclose `org` and `title` without disclosing `email` — directly applying the claim atomization principle (§F.4.2).

#### K.3.2 Privacy Note

Email addresses, phone numbers, and URLs in vCard objects are personal identifiers and SHOULD be placed in `selective-disclosure` or `proof-of-possession` slots. The `fn` (full name) field is particularly sensitive — a holder may wish to disclose their organization and title to a verifier without disclosing their full legal name.

---

### K.4 OpenID for Verifiable Presentations (OID4VP) Transport Bridge

This bridge enables HIRI Passport Presentations to be transmitted via the OID4VP protocol, providing compatibility with digital identity wallets and verifiers implementing the OID4VP specification.

#### K.4.1 HIRI as OID4VP Credential Format

HIRI defines a new OID4VP credential format identifier:

```
hiri_passport_vc_sd
```

This format indicates that the credential payload is a HIRI Passport Presentation (§11.3) with selective disclosure per the Privacy Extension v1.4.1.

#### K.4.2 OID4VP Authorization Request Mapping

A verifier implementing OID4VP maps its DisclosureRequest (§11.2) to an OID4VP Authorization Request:

```json
{
  "response_type": "vp_token",
  "presentation_definition": {
    "id": "hiri-passport-request-001",
    "format": {
      "hiri_passport_vc_sd": {}
    },
    "input_descriptors": [
      {
        "id": "employment-credential",
        "constraints": {
          "fields": [
            {
              "path": ["$.credentialType"],
              "filter": { "const": "EmploymentCredential" }
            }
          ]
        }
      }
    ]
  },
  "nonce": "YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXo...",
  "client_id": "key:ed25519:z<verifier-authority>"
}
```

The OID4VP `nonce` maps directly to the HIRI DisclosureRequest `nonce`. The `client_id` maps to `verifierAuthority` for presentation slot token derivation (§11.7.3). HIRI-conforming holder software MUST use the OID4VP `nonce` and `client_id` values when computing slot tokens for presentations transmitted via OID4VP.

#### K.4.3 OID4VP Response Mapping

The holder's OID4VP response carries the HIRI Passport Presentation as the `vp_token`:

```json
{
  "vp_token": "<base64url-encoded HIRI PassportPresentation JSON>"
}
```

The HIRI presentation inside `vp_token` is verified using the standard HIRI verification algorithm (§12) after base64url decoding.

---

### K.5 DIDComm Messaging Transport Bridge

This bridge enables HIRI credential exchange flows via DIDComm v2, providing compatibility with DIDComm-based identity agents and wallets.

#### K.5.1 DIDComm Message Types

This bridge defines two DIDComm message types:

```
https://hiri-protocol.org/didcomm/1.0/disclosure-request
https://hiri-protocol.org/didcomm/1.0/passport-presentation
```

#### K.5.2 Disclosure Request Message

```json
{
  "type": "https://hiri-protocol.org/didcomm/1.0/disclosure-request",
  "id": "req:2026-03-15-didcomm-001",
  "from": "did:key:z<verifier-did>",
  "to": ["did:key:z<holder-did>"],
  "body": {
    "hiריDisclosureRequest": {
      "@context": ["https://hiri-protocol.org/passport/v1"],
      "@type": "hiri:DisclosureRequest",
      "requestId": "req:2026-03-15-didcomm-001",
      "verifier": {
        "authority": "key:ed25519:z<verifier-authority>",
        "displayName": "Environmental Regulatory Agency"
      },
      "requestedSlots": [
        { "credentialType": "EmploymentCredential", "minimumDisclosure": "summary" }
      ],
      "nonce": "YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXo...",
      "expiresAt": "2026-03-15T11:00:00Z"
    }
  }
}
```

The DIDComm envelope handles routing and encryption (per DIDComm v2 specifications). The `hiריDisclosureRequest` in the body is the HIRI DisclosureRequest (§11.2) transmitted as the DIDComm message payload.

#### K.5.3 Passport Presentation Message

```json
{
  "type": "https://hiri-protocol.org/didcomm/1.0/passport-presentation",
  "id": "pres:2026-03-15-didcomm-001",
  "from": "did:key:z<holder-did>",
  "to": ["did:key:z<verifier-did>"],
  "thid": "req:2026-03-15-didcomm-001",
  "body": {
    "hiריPassportPresentation": {
      "...": "Full HIRI PassportPresentation object (§11.3)"
    }
  }
}
```

The DIDComm `thid` (thread ID) links the presentation to the originating request. The `hiריPassportPresentation` is verified using the standard HIRI verification algorithm (§12) after extraction from the DIDComm envelope.

---

### K.6 Schema.org and FOAF RDF Vocabulary Bridge

This bridge enables HIRI identity artifacts to optionally expose their claim graphs using widely adopted semantic web vocabularies, enabling compatibility with knowledge graph systems, linked data infrastructure, and semantic search.

#### K.6.1 Schema.org Person Mapping

A HIRI passport holder's identity information MAY be exposed as a Schema.org `Person` graph:

```json
{
  "@context": {
    "@vocab": "https://schema.org/",
    "hiri": "https://hiri-protocol.org/spec/v3.1#"
  },
  "@type": "Person",
  "name": "Sarah Thompson",
  "affiliation": {
    "@type": "Organization",
    "name": "EcoImpact Consulting",
    "url": "https://ecoimpact.com"
  },
  "hasCredential": [
    {
      "@type": "EducationalOccupationalCredential",
      "credentialCategory": "ProfessionalCertification",
      "name": "Wetland Specialist Certification",
      "recognizedBy": {
        "@type": "Organization",
        "name": "National Environmental Association"
      }
    }
  ],
  "hiri:passportURI": "hiri://key:ed25519:z<holder-authority>/passport/main",
  "hiri:authority": "key:ed25519:z<holder-authority>"
}
```

The `hiri:passportURI` and `hiri:authority` properties link the Schema.org representation back to the verifiable HIRI passport. Knowledge graph consumers can follow these links to obtain the cryptographically verifiable artifact.

#### K.6.2 FOAF Vocabulary Mapping

For contexts where FOAF is preferred over Schema.org:

```json
{
  "@context": {
    "foaf": "http://xmlns.com/foaf/0.1/",
    "org": "http://www.w3.org/ns/org#",
    "hiri": "https://hiri-protocol.org/spec/v3.1#"
  },
  "@type": "foaf:Person",
  "foaf:name": "Sarah Thompson",
  "foaf:mbox": "sarah@ecoimpact.com",
  "org:memberOf": {
    "@type": "org:Organization",
    "foaf:name": "EcoImpact Consulting"
  },
  "hiri:passportURI": "hiri://key:ed25519:z<holder-authority>/passport/main"
}
```

#### K.6.3 Selective Disclosure and RDF Vocabularies

RDF vocabulary representations of holder identity are derived from disclosed credential claim content. Holders MUST NOT expose RDF vocabulary representations that contain information beyond what they have disclosed in their current passport presentation context. The RDF representation is a view over disclosed data, not an additional disclosure channel.

---

### K.7 Interoperability Bridge Decision Matrix

The following matrix helps implementers select which bridges to implement based on their deployment context:

| Deployment Context | Recommended Bridges | Notes |
|-------------------|---------------------|-------|
| Enterprise HR / credential issuance | K.2 (VC envelope) + K.3 (vCard) | Maximize compatibility with HR systems and VC wallets |
| Government identity / digital ID wallet | K.2 (VC envelope) + K.4 (OID4VP) | OID4VP is the emerging government wallet standard |
| Decentralized agent / DID-native deployment | K.5 (DIDComm) | DIDComm for peer-to-peer credential exchange |
| Knowledge graph / semantic web integration | K.6 (Schema.org/FOAF) | Linked data representation for discoverability |
| Mobile wallet (all-in-one) | K.2 + K.4 + K.5 | Full compatibility layer for multi-protocol wallets |
| Edge-only / offline-first deployment | No bridge required | Native HIRI; bridges add transport dependencies |
| IoT / embedded verification | No bridge required | Native HIRI; bridge overhead is not justified |

All bridges are additive. An implementation claiming any bridge MUST still implement the underlying HIRI verification algorithm (§12) as the canonical integrity check. Bridges are transport and representation layers — they do not replace verification.

---

## Appendix L: Operational Guidance (INFORMATIVE)

This appendix is INFORMATIVE. It provides practical guidance for two audiences: software developers and UX designers implementing holder and verifier software (§L.1), and infrastructure operators running Revocation Transparency Logs and Oracle services (§L.2).

### L.1 proofArtifactRef UX Decision Table

Verifier software MUST surface biometric proof verification status to relying parties in a clear, actionable way. The following table defines the RECOMMENDED user-facing messages and required verifier actions for every transport failure mode.

#### L.1.1 Complete Decision Table

| Failure Condition | HTTP/Transport State | Verification Status | Recommended User Message | Verifier Action |
|------------------|---------------------|---------------------|--------------------------|-----------------|
| Proof fetched and verified | HTTP 200, hash match, ZK pass | `"biometricBinding: verified"` | ✓ Identity confirmed with biometric binding | Accept; cache artifact |
| Proof fetched, hash mismatch | HTTP 200, hash mismatch | `"biometricBinding: artifact-corrupted"` | ⚠ Verification incomplete — credential data may be tampered | Reject presentation; report `PRESENTATION_PROOF_ARTIFACT_HASH_MISMATCH` |
| Proof fetched, ZK proof fails | HTTP 200, hash match, ZK fail | `"biometricBinding: proof-invalid"` | ✗ Biometric verification failed — holder does not match credential | Reject biometric binding; surface as verification failure |
| Proof URI returns 404 | HTTP 404 | `"biometricBinding: artifact-missing"` | ⚠ Biometric proof unavailable — contact credential issuer | Report `PRESENTATION_PROOF_ARTIFACT_UNAVAILABLE`; core credential unaffected |
| Proof URI times out after all retries | Timeout × 3 | `"biometricBinding: unverifiable-offline"` | ⚠ Biometric verification incomplete — network unavailable | Report `PRESENTATION_PROOF_ARTIFACT_UNAVAILABLE`; core credential unaffected |
| Proof URI returns 429 (rate limited) | HTTP 429 | `"biometricBinding: fetch-rate-limited"` | ⚠ Verification delayed — please retry in X seconds | Honor `Retry-After` header; retry after delay; if still failing, treat as timeout |
| Proof URI returns 500/503 | HTTP 5xx | `"biometricBinding: server-error"` | ⚠ Biometric verification service temporarily unavailable | Retry with backoff; if still failing after budget, treat as timeout |
| Offline verification (no network) | No network | `"biometricBinding: unverifiable-offline"` | ⚠ Biometric verification unavailable offline | Core credential verified if signature valid; biometric liveness not confirmed |
| Proof cached, within validity window | Cache hit | `"biometricBinding: verified-cached"` | ✓ Identity confirmed (cached biometric binding) | Use cached result; skip re-fetch |
| Proof cached, validity window expired | Cache expired | `"biometricBinding: cache-expired"` | Re-fetch required | Re-fetch from URI; if unavailable, treat as `unverifiable-offline` |

#### L.1.2 Composing the Final Verification Message

The overall credential verification message MUST distinguish between the core credential trust level and the biometric binding status:

```
Core Credential: VERIFIED (EcoImpact Consulting — Employment)
Issuer:          EcoImpact Consulting (ecoimpact.com — DNSSEC)
Valid Until:     2027-03-01

Biometric Binding: ⚠ UNVERIFIABLE (network unavailable)
Note: Credential issuer signature is valid. Live biometric match
      could not be confirmed. Application policy determines
      whether this presentation can be accepted.
```

Verifier software MUST NOT collapse these two into a single pass/fail status. A valid credential with unverifiable biometric binding is a materially different state than an invalid credential.

#### L.1.3 High-Value Transaction Handling

For `transactionClass: "high-value"` (§16.9.1), verifier software SHOULD enforce a stricter UX posture:

- If biometric binding is required by the relying party policy and returns any state other than `"verified"` or `"verified-cached"`, the transaction MUST be blocked with a clear reason.
- The user-facing message SHOULD include the specific failure code so support staff can diagnose issues.
- A "retry" option SHOULD be presented to the holder before blocking, unless the failure is `"proof-invalid"` (which indicates active mismatch and MUST NOT be retried without re-issuance).

---

### L.2 Operator Security Guidance

This section provides security guidance for organizations operating Revocation Transparency Logs, Oracle services, or shared log infrastructure.

#### L.2.1 Key Management and HSM Requirements

**Signing key hierarchy:**

Log operators and oracle authorities MUST maintain a minimum three-key hierarchy:

```
Root CA Key (offline, air-gapped, HSM)
    └── Intermediate Signing Key (HSM, online, signs checkpoints)
    └── Emergency Revocation Key (offline HSM, used only for emergency revocations)
    └── OIDC Management Plane Key (HSM, online, issues short-lived JWT tokens for /append auth)
```

No single key MUST be used for more than one role. Root CA keys MUST be stored in offline, air-gapped HSMs and used only for intermediate key ceremonies.

**HSM requirements for Passport-Full deployments:**

- FIPS 140-2 Level 3 or higher (or equivalent international standard)
- Tamper-evident physical security
- Dual-person integrity for key generation ceremonies (minimum two independent witnesses)
- Hardware-backed key generation — no software key generation permitted for root or intermediate keys
- Audit log for all key usage events, exported to an independent system

**Key ceremony documentation:**

Each key generation ceremony MUST produce a signed record including: date, location, participating witnesses (names and roles), HSM serial number, public key fingerprint, and the key's designated role. This record MUST be retained for the lifetime of the key plus 7 years.

#### L.2.2 Log Server Infrastructure Security

**Network isolation:**

- The /append endpoint MUST be behind an API gateway that enforces rate limiting (§16.7.3) and authentication (§16.4.3) before any request reaches the log server.
- The log server's signing key HSM MUST be on an isolated network segment; only the checkpoint-generation service has access.
- GET endpoints (/checkpoint and /entry) SHOULD be served from a CDN or read-replica cluster to isolate read traffic from the append pipeline.

**DDoS resilience:**

- GET /checkpoint: Cache at CDN with TTL matching checkpoint interval (1 hour). Checkpoint responses are static between publication intervals — CDN caching eliminates origin load for checkpoint queries.
- GET /entry/{manifestHash}: Rate-limit per IP (RECOMMENDED: 60 requests/minute/IP). Cache positive results (entry found) with no TTL restriction; cache negative results (entry not found) with TTL equal to checkpoint interval.
- POST /append: Enforce per-issuer rate limits before any database operation. Return 429 immediately if rate limit exceeded — do not queue.

**Monitoring and alerting:**

Log operators MUST monitor and alert on:

| Metric | Alert Threshold | Action |
|--------|----------------|--------|
| Checkpoint publication delay | > 90 minutes since last checkpoint | Page on-call; investigate log signer |
| Checkpoint chain gap detected | Any occurrence | Page on-call immediately; treat as potential compromise |
| /append authentication failures | > 10 failures/minute from single issuer | Investigate; consider temporary issuer block |
| /append success rate | < 99% over 1 hour | Investigate database or signing pipeline |
| Entry query 5xx rate | > 1% over 5 minutes | Investigate CDN or backend |

**Incident escalation path:**

Every log operator MUST designate and publish:
- A primary on-call contact reachable 24/7
- A security disclosure email address
- A maximum first-response SLA for critical incidents (RECOMMENDED: 1 hour)

These contacts MUST be declared in the `hiri:OracleGovernanceDocument` or equivalent KeyDocument extension, so verifiers know how to reach the operator in an incident.

#### L.2.3 Oracle-Specific Security

**Biometric data boundary:**

Oracle infrastructure MUST enforce a strict perimeter around biometric data:

- Raw biometric templates MUST be processed only in dedicated, isolated enclaves.
- No biometric template bytes MUST ever be written to logs, databases, or transmitted over networks outside the enrollment enclave.
- All data egress from the enrollment enclave MUST be reviewed by a data loss prevention (DLP) policy that rejects any output matching biometric template patterns.

**Registry nullifier storage:**

The global uniqueness registry (§G.2.2.1) stores only registry nullifiers — never biometric templates or commitments. The nullifier store MUST be:

- Append-only (no updates, no deletes except under court order with full audit trail)
- Cryptographically signed at each append (signed Merkle tree as defined in §16.10)
- Backed up with offline, encrypted copies stored in geographically distributed locations
- Recoverable from backup within 24 hours of a primary system failure

**Emergency revocation key custody:**

The oracle's emergency revocation key (§17.7.2) MUST be:

- Stored in an offline HSM in a physically secured location separate from all online systems
- Subject to dual-person integrity for any use (two authorized officers must be present)
- Tested quarterly in a drill that exercises the key without publishing a real revocation

#### L.2.4 Publication Checklist for Log Operators

Before accepting production issuers, a new Revocation Transparency Log operator MUST complete all items and verify each against the acceptance criteria below.

| # | Checklist Item | Acceptance Criteria | Pass/Fail |
|---|---------------|---------------------|-----------|
| 1 | Key generation ceremony documented | Signed ceremony record filed with ≥2 witnesses; HSM serial and public key fingerprint recorded | ☐ |
| 2 | HSM FIPS 140-2 Level 3 confirmed | Certificate number and expiry from NIST CMVP database recorded | ☐ |
| 3 | Emergency revocation key generated and custodied | Key stored in offline HSM; dual-custody policy documented; test revocation drill completed without publishing live entry | ☐ |
| 4 | mTLS issuer onboarding tested | Test issuer with valid SAN URI successfully appends entry; test issuer with mismatched SAN receives HTTP 403 | ☐ |
| 5 | Signed JWT OIDC plane tested | Valid JWT appends entry; expired JWT (exp < now) receives HTTP 401; JWT with wrong `aud` receives HTTP 401 | ☐ |
| 6 | Rate limiting verified | Test issuer at 101 req/hour receives HTTP 429 with `Retry-After` header | ☐ |
| 7 | Checkpoint automation tested | First entry appended at T=0; new checkpoint appears within 30 minutes; checkpoint signature verified by reference implementation | ☐ |
| 8 | Checkpoint chain integrity tested | Inject synthetic chain gap in test environment; verifier reports `REVOCATION_LOG_CHECKPOINT_CHAIN_GAP` | ☐ |
| 9 | DDoS mitigations load-tested | Sustained 10,000 req/s to GET /checkpoint returns ≥99.9% success rate from CDN without hitting origin; GET /entry rate limit fires at configured threshold | ☐ |
| 10 | Monitoring and alerting live | All metrics in §L.2.2 table produce test alerts; on-call contact acknowledges within 15 minutes | ☐ |
| 11 | On-call contact and security email published | URIs present in governance document; test email to security disclosure address receives automated acknowledgement | ☐ |
| 12 | First checkpoint independently verified | Reference implementation CLI `hiri-passport verify-checkpoint --uri <endpoint>` returns PASS | ☐ |
| 13 | Conformance test suite passing | `npm run test:conformance` (or equivalent) exits 0; all Appendix H vectors PASS | ☐ |
| 14 | Governance document published | `GET https://<domain>/.well-known/hiri-oracle-governance.json` returns 200 with valid signature; governance document hash recorded in trust anchor config | ☐ |

**Sign-off:** Operator representative signs and dates completion of all 14 items. This signed record is required evidence for §1.5 checklist item 3.

---

## Appendix M: OracleGovernanceDocument Template (INFORMATIVE)

This appendix is INFORMATIVE. It provides a complete OracleGovernanceDocument template and a worked OracleRecoveryNotice example. Oracles MUST conform to the normative requirements in §17.2; this appendix provides actionable starting points for compliance.

### M.1 OracleGovernanceDocument Template

Copy this template and replace all `<PLACEHOLDER>` values before publication. The document MUST be signed with the oracle's current HIRI signing key before publishing.

```json
{
  "@context": [
    "https://hiri-protocol.org/spec/v3.1",
    "https://hiri-protocol.org/passport/v1"
  ],
  "@type": "hiri:OracleGovernanceDocument",

  "oracleAuthority": "key:ed25519:z<ORACLE-AUTHORITY>",
  "oracleDomain": "<oracle-domain.example.com>",

  "operatorIdentity": {
    "legalName": "<Legal Entity Name>",
    "jurisdiction": "<ISO 3166-1 alpha-2 country code, e.g. US>",
    "registrationNumber": "<Government registration or EIN/company number>",
    "contactURI": "https://<oracle-domain>/contact",
    "securityDisclosureEmail": "security@<oracle-domain>"
  },

  "keyManagementPolicy": {
    "hsmRequired": true,
    "hsmStandard": "FIPS-140-2-Level-3",
    "keyRotationPeriod": "P365D",
    "multiPartySigningRequired": false,
    "auditableKeyStorage": true,
    "emergencyRevocationKeyRegistered": true
  },

  "auditPolicy": {
    "auditSchedule": "annual",
    "lastAuditDate": "<YYYY-MM-DD>",
    "auditReportURI": "https://<oracle-domain>/audit/<year>",
    "auditorName": "<Auditing Firm Name>",
    "nextAuditDue": "<YYYY-MM-DD>"
  },

  "transparencyLog": {
    "oracleActionLogURI": "https://<oracle-domain>/hiri/v1/oracle-log",
    "logAuthority": "key:ed25519:z<LOG-AUTHORITY>",
    "checkpointInterval": "PT1H",
    "retentionPolicy": "P7Y"
  },

  "incidentResponse": {
    "emergencyContactURI": "https://<oracle-domain>/incident",
    "maxEmergencyResponseTime": "PT1H",
    "incidentNoticeURI": "https://<oracle-domain>/.well-known/hiri-oracle-incident.json",
    "recoveryNoticeURI": "https://<oracle-domain>/.well-known/hiri-oracle-recovery.json"
  },

  "biometricModalities": ["<iris|face|fingerprint|palm-vein>"],
  "registryTechnology": "<ZK-Merkle-inclusion|other>",
  "registryPrivacyMode": "<hash-only-nullifiers|commitments>",

  "governanceVersion": "1.0.0",
  "validUntil": "<ISO 8601 timestamp, max 1 year from publication>",

  "signature": {
    "type": "Ed25519Signature2020",
    "algorithm": "ed25519",
    "created": "<ISO 8601 timestamp>",
    "verificationMethod": "hiri://key:ed25519:z<ORACLE-AUTHORITY>/key/main#key-1",
    "proofPurpose": "assertionMethod",
    "proofValue": "z<SIGNATURE>"
  }
}
```

### M.2 Filled OracleGovernanceDocument Example

```json
{
  "@context": [
    "https://hiri-protocol.org/spec/v3.1",
    "https://hiri-protocol.org/passport/v1"
  ],
  "@type": "hiri:OracleGovernanceDocument",

  "oracleAuthority": "key:ed25519:zBiometricNet2026ExampleKey",
  "oracleDomain": "biometric-oracle.example.com",

  "operatorIdentity": {
    "legalName": "BiometricNet Foundation",
    "jurisdiction": "CH",
    "registrationNumber": "CHE-123.456.789",
    "contactURI": "https://biometric-oracle.example.com/contact",
    "securityDisclosureEmail": "security@biometric-oracle.example.com"
  },

  "keyManagementPolicy": {
    "hsmRequired": true,
    "hsmStandard": "FIPS-140-2-Level-3",
    "keyRotationPeriod": "P365D",
    "multiPartySigningRequired": false,
    "auditableKeyStorage": true,
    "emergencyRevocationKeyRegistered": true
  },

  "auditPolicy": {
    "auditSchedule": "annual",
    "lastAuditDate": "2026-01-15",
    "auditReportURI": "https://biometric-oracle.example.com/audit/2026",
    "auditorName": "CryptoAudit AG",
    "nextAuditDue": "2027-01-15"
  },

  "transparencyLog": {
    "oracleActionLogURI": "https://biometric-oracle.example.com/hiri/v1/oracle-log",
    "logAuthority": "key:ed25519:zBiometricNetLogKey2026",
    "checkpointInterval": "PT1H",
    "retentionPolicy": "P7Y"
  },

  "incidentResponse": {
    "emergencyContactURI": "https://biometric-oracle.example.com/incident",
    "maxEmergencyResponseTime": "PT1H",
    "incidentNoticeURI": "https://biometric-oracle.example.com/.well-known/hiri-oracle-incident.json",
    "recoveryNoticeURI": "https://biometric-oracle.example.com/.well-known/hiri-oracle-recovery.json"
  },

  "biometricModalities": ["iris"],
  "registryTechnology": "ZK-Merkle-inclusion",
  "registryPrivacyMode": "hash-only-nullifiers",

  "governanceVersion": "1.0.0",
  "validUntil": "2027-04-01T00:00:00Z",

  "signature": {
    "type": "Ed25519Signature2020",
    "algorithm": "ed25519",
    "created": "2026-04-01T09:00:00Z",
    "verificationMethod": "hiri://key:ed25519:zBiometricNet2026ExampleKey/key/main#key-1",
    "proofPurpose": "assertionMethod",
    "proofValue": "zEXAMPLE_SIGNATURE_PLACEHOLDER"
  }
}
```

### M.3 OracleRecoveryNotice Example

This is the notice published at `/.well-known/hiri-oracle-recovery.json` after completing Phase 3 of the incident response (§17.7.4):

```json
{
  "@context": [
    "https://hiri-protocol.org/spec/v3.1",
    "https://hiri-protocol.org/passport/v1"
  ],
  "@type": "hiri:OracleRecoveryNotice",

  "oracleAuthority": "key:ed25519:zBiometricNetNEWKey2026",

  "incidentSummary": {
    "incidentType": "key-compromise",
    "detectedAt": "2026-04-01T10:00:00Z",
    "compromisedAuthority": "key:ed25519:zBiometricNet2026ExampleKey",
    "affectedSince": "2026-03-01T00:00:00Z",
    "incidentClosedAt": "2026-05-01T09:00:00Z"
  },

  "recoveryActions": {
    "emergencyRevocationPublishedAt": "2026-04-01T10:47:00Z",
    "newKeyActiveFrom": "2026-04-02T00:00:00Z",
    "parallelOperationStarted": "2026-04-02T00:00:00Z",
    "parallelOperationEnds": "2026-05-02T00:00:00Z",
    "recoveryDrillCompleted": true,
    "recoveryDrillDate": "2026-04-15T14:00:00Z"
  },

  "newGovernanceDocument": {
    "uri": "https://biometric-oracle.example.com/.well-known/hiri-oracle-governance.json",
    "governanceDocumentHash": "sha256:NEWHASH",
    "version": "2.0.0",
    "publishedAt": "2026-04-02T00:00:00Z"
  },

  "verifierInstructions": {
    "action": "update-trust-anchor",
    "newOracleAuthority": "key:ed25519:zBiometricNetNEWKey2026",
    "oldAuthorityRevoked": true,
    "quarantineLiftEligibleAfter": "2026-05-02T00:00:00Z",
    "requiredEvidence": "governance-doc-hash-verified + policy-review"
  },

  "signature": {
    "type": "Ed25519Signature2020",
    "algorithm": "ed25519",
    "created": "2026-05-01T09:00:00Z",
    "verificationMethod": "hiri://key:ed25519:zBiometricNetNEWKey2026/key/main#key-1",
    "proofPurpose": "assertionMethod",
    "proofValue": "zEXAMPLE_RECOVERY_SIGNATURE"
  }
}
```

The `verifierInstructions.quarantineLiftEligibleAfter` timestamp marks the earliest point at which verifiers MAY lift oracle quarantine, per §17.7.4 (30-day parallel operation minimum).

---

## Appendix N: Migration Guidance (INFORMATIVE)

This appendix is INFORMATIVE. It describes migration paths for holders and issuers upgrading from previous versions of the HIRI Digital Passport Extension. Migrations preserve the existing verification chain — older passport versions remain verifiable after migration.

### N.1 Migration Paths Overview

| From Version | Key Changes Required | Breaking to Old Verifiers? |
|-------------|---------------------|---------------------------|
| Pre-v1.1.0 (no slot blinding) | Presentations must switch to blinded tokens | No — passport manifests unchanged; only presentations |
| Pre-v1.6.0 (no KeyDocument) | Publish KeyDocument at `hiri://<authority>/key/main` | No — adds new artifact; old chain intact |
| Pre-v1.6.0 (no revocation log) | Register with revocation log service; publish log endpoint in KeyDocument | No — additive |
| Pre-v1.8.0 (old /append auth) | Migrate to mTLS or signed JWT for log appends | No — server-side change only |
| Pre-v1.9.0 (no URDNA2015) | Re-canonicalize passport manifests with URDNA2015 | YES — new manifests have different content hashes |

### N.2 Migration: Unblinded Presentations to Slot-Blinded Presentations (Pre-v1.1.0)

**What changes:** Holder software must generate presentation slot tokens (§11.7.3) instead of raw `slotId` values. The Passport Manifest itself does not change.

**Migration steps:**
1. Generate a Slot Blinding Key for the existing passport authority using the HKDF derivation in §11.7.2. This key is derived deterministically from the existing signing key — no new keypair is needed.
2. Update holder software to compute `presentationSlotToken` for all future presentations.
3. No new passport version is required. Old passport versions remain verifiable by v3.1.1-conforming verifiers.

**Backward compatibility:** Pre-v1.1.0 verifiers that expected raw `slotId` values will reject blinded presentations. This is by design — slot blinding is a security improvement. Deploy holder and verifier software updates together.

### N.3 Migration: Publishing a KeyDocument (Pre-v1.6.0)

**What changes:** Holders and issuers at Passport-Interoperable or above MUST publish a KeyDocument (§6.4). This is an additive step — it does not modify the existing passport manifest.

**Migration steps:**
1. Create a KeyDocument conforming to v3.1.1 §13, referencing the existing authority's public key.
2. Publish the KeyDocument at `hiri://<authority>/key/main`.
3. Add `keyDocumentURI` to the `hiri:passport.holder` block in the next passport version update.
4. No re-signing of existing credential slots is required — KeyDocuments are independently resolved.

**Chain integrity:** The existing passport chain (previous manifest versions) remains valid. Verifiers resolving the KeyDocument for key lifecycle checks will find the document for the current key and any rotated predecessors.

### N.4 Migration: Registering with a Revocation Transparency Log (Pre-v1.6.0)

**What changes:** Issuers must register with a Revocation Transparency Log service and declare the log endpoint in their KeyDocument.

**Migration steps:**
1. Choose or operate a Revocation Transparency Log conforming to §16.
2. Authenticate with the log service using mTLS or signed JWT (§16.4.3).
3. For any credentials that have already been revoked via Tier 2 attestation chain updates: append retroactive `RevocationLogEntry` records for each revoked manifest hash. This backfills the log for pre-v1.6.0 revocations.
4. Update the issuer's KeyDocument `organizationalIdentity.revocationLogURI` field.
5. Publish a new KeyDocument version.

**Retroactive revocation entries:** Verifiers checking the revocation log for pre-migration credentials will find entries only if the issuer has backfilled them. Issuers SHOULD backfill all known revocations at migration time. Verifiers encountering credentials with a `revokedAt` timestamp predating the log's first checkpoint SHOULD treat the revocation log state as `"cached-checkpoint"` (trusting the Tier 2 attestation chain for the revocation evidence) rather than `"unknown"`.

### N.5 Migration: URDNA2015 Canonicalization (Passport-Interoperable)

**What changes:** Passport Manifests MUST use URDNA2015 canonicalization (§9.2). Pre-migration passports using JCS-canonicalized manifests remain verifiable but cannot claim Passport-Interoperable conformance.

**This is a breaking migration** — the new manifest has a different content hash from the old one.

**Migration steps:**
1. Create a new passport version with `hiri:content.canonicalization: "URDNA2015"`.
2. Recompute `hiri:content.hash` as `SHA-256(URDNA2015(holderContentPayload))`.
3. Sign the new manifest with the holder's current signing key.
4. Publish the new version; the `hiri:chain` block links to the previous JCS-canonicalized version.

**Chain continuity:** The chain walks correctly across the canonicalization boundary. A v3.1.1 chain integrity verifier checks each version against its declared canonicalization profile. The cross-version chain link (`hiri:chain.previous`) references the previous manifest's hash, which remains valid under its original JCS canonicalization.

**Credential slots:** Existing credential slot `attestationRef` entries do not need to change — they reference issuer-signed attestation manifests, which have their own independent canonicalization declarations.

### N.6 Migration Validation

After completing any migration, run the reference implementation conformance suite against the migrated passport:

```bash
npx hiri-passport-check \
  --passport hiri://key:ed25519:z<authority>/passport/main \
  --conformance-level interoperable \
  --report migration-validation.json
```

The report MUST show `"conformanceLevel": "Passport-Interoperable"` and no `warnings` entries for the migrated fields. Address any warnings before declaring migration complete.

---

## Document History

| Version | Date | Status | Notes |
|---------|------|--------|-------|
| 1.0.0 | 2026-03 | Draft | Initial specification |
| 1.1.0 | 2026-03 | Draft | withheldSlots default; Tier 2 override normative; signature algorithm registry; presentation slot blinding; nonce encoding normative; slot count limits |
| 1.2.0 | 2026-03 | Draft | Verifier authority binding in slot tokens; P-256 multicodec encoding corrected; coercion resistance moved to security considerations; temporal key lifecycle check at presentation verification |
| 1.3.0 | 2026-03 | Draft | Proxy Issuance appendix (INFORMATIVE); claim atomization guidance; ZK credential type forward reference |
| 1.4.0 | 2026-03 | Draft | Biometric network integration appendix (INFORMATIVE); `ProofOfUniqueHumanCredential` and `BiometricBoundCredential` added to credential type registry |
| 1.5.0 | 2026-03 | Draft | Split nullifier architecture (critical privacy fix); Oracle Notification Protocol for issuer-side revocation; `proofArtifactRef` for constrained transports; biometric modality mandatory disclosure clarified |
| 1.6.0 | 2026-03 | Draft | Revocation Transparency Log (§16, normative); Oracle Trust Governance (§17, normative); offline verifier decision table (§12.7, normative); KeyDocument MUST for Passport-Interoperable; tightened conformance levels; Appendices H, I, J |
| 1.7.0 | 2026-03 | Draft | HIRI as Integrity Layer (§18, normative); DID service endpoint formalized (§6.3); Identity Anchor registry (§10.5); JOSE/COSE algorithm cross-references; Standards Interoperability Bridges appendix (Appendix K) |
| 1.8.0 | 2026-03 | Draft | POST /append authentication hardened; Merkle canonicalization normative (§16.10); privacy-preserving revocation mode (§16.8); revocation acceptance windows (§16.9); oracle incident response (§17.7); staleness windows normative; Appendices H.6–H.8, L |
| **1.9.0** | **2026-03** | **Release Candidate** | Sign-off checklist (§1.5); interoperability test matrix (§H.9); Passport-Hardened test vectors (§H.10); machine-readable revocation status codes (§C.2); §16.10 3-leaf hex worked example; §16.8.2 selective-reveal access control normative; §6.4/§10.5 offline resolver behavior; Passport-Hardened summary in §15.6; Appendix L.2.4 acceptance criteria table; Appendix M OracleGovernanceDocument template + recovery notice; Appendix N migration guidance |

---

## License

**Specification:** CC0 1.0 Universal (Public Domain)
**Reference Implementations:** Apache 2.0

---

*A passport is not a platform. It belongs to its holder.*

*This specification treats identity portability as a security property, not a convenience.*
