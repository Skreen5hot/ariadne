# SPCN v2.3 — Operational Architecture Specification

| Field | Value |
|---|---|
| **Status** | DRAFT v2.3.1 |
| **Supersedes** | SPCN v2.2 |
| **Revision Basis** | Four high-priority patches: (1) Governance quorum arithmetic bug; (2) Emergency authorization pre-commitment and mid-episode revocation; (3) Calibration baseline bootstrapping and sealed-state handling; (4) Admin key registry binding. Plus medium-priority additions: D4 sliding-window clarification, non-deterministic `ConstrainedDecodeProof` mitigation, hosted inference policy, historical token verification algorithm, HumanBridge minimum disclosure set, SLO table clarification. Test suite updated with DECAY-05 correction, DECAY-09, EMER-01, and SMREA-07. |
| **Revision Basis (v2.3.1)** | Cross-specification coherence patch: (1) Safety Subsystem ↔ CPS binding; (2) Governance quorum normative scope declaration; (3) Emergency Mode ↔ Alternative Bundles interaction; (4) MRE ↔ IEA normative bridge; (5) HIRI EAT registration semantics (write-only, non-blocking). |
| **Context** | FNSR Ecosystem / Ontology of Freedom Initiative — Synthetic Moral Person Architecture |

---

## Preamble: Scope of v2.3

v2.3 is a third hardening patch. All sections not enumerated below are **unchanged from v2.2**, which itself carries forward all content from v2.1 and v2.0. The revision set is fully additive — no prior provision is weakened or removed; only errors are corrected and gaps are closed.

### Scope of v2.3.1 (Cross-Specification Coherence Patch)

v2.3.1 is a coherence patch that binds SPCN to the broader FNSR portfolio. No internal SPCN behavior is changed. The following declarations resolve ambiguities identified during cross-specification review:

1. **Safety Subsystem ↔ CPS Binding (§CS-1):** The SPCN "Safety Subsystem" is a local instance of the Containment Protocol Service (CPS). CPS operates at the portfolio level as an independent Tier 0 service; the Safety Subsystem is its node-local manifestation within the SPCN TEE boundary. All references to "Safety Subsystem" in this specification refer to the CPS runtime executing inside the node's TEE.

2. **Governance Quorum Normative Scope (§CS-2):** The corrected quorum formula `floor(N_gov / 2) + 1` (§8.2.6) is the SPCN node-level implementation of the FNSR Governance Specification's quorum requirement. The FNSR Governance Specification (v2.0) defines governance authority at the ecosystem level; SPCN implements that authority at the node level. When the FNSR Governance Specification and SPCN both specify a quorum for the same operation (e.g., Emergency Alternative Bundle signing), the FNSR Governance Specification governs the ecosystem-level authorization and SPCN governs the node-level verification. Both use `floor(N_gov / 2) + 1` unless a section explicitly overrides.

3. **Emergency Mode ↔ Alternative Bundles Interaction (§CS-3):** SPCN Emergency Execution Mode (§6.1.6) and FNSR Governance Pre-Authorized Emergency Alternative Bundles (Governance Spec §8.7) are distinct systems with distinct triggers. Emergency Execution Mode activates when the node enters `TIME_UNATTESTED` state (clock failure). Alternative Bundles activate when the agent faces a non-negotiable conflict (moral emergency). When both conditions are active simultaneously, Alternative Bundle invocation requires a valid EAT like any other emergency capability — the EAT must be pre-registered in the Commitment Ledger before the bundle is invoked. When the node is in normal operation (not `TIME_UNATTESTED`), Alternative Bundles are invoked through normal capability tokens and do not require an EAT.

4. **MRE ↔ IEA Normative Bridge (§CS-4):** The normative content of Moral Reflection Events (§8) is produced by the Integral Ethics Agent (IEA, also known as IEE). SPCN provides the safety envelope for moral reflection: constrained decoding, ledger registration, Safety Subsystem verification, and HumanBridge human review. IEA provides the ethical reasoning within that envelope — the 12-worldview evaluation, deficiency classification, proportionality assessment, and revised reasoning. SPCN's `reflection_type`, `deficiency_class`, and `omitted_considerations` fields in the SMREA structure are populated by IEA output, validated by the Safety Subsystem, and presented to HumanBridge for human review. The SPL ↔ IEA normative bridge (Residual Open Question #1) governs the `revised_reasoning` field specifically.

5. **HIRI EAT Registration Semantics (§CS-5):** EAT registration to HIRI (`registered_at_ledger: HIRI`, `ledger_cid: CID`) is **write-only and asynchronous**. The Safety Subsystem publishes EATs to HIRI for external audit trail purposes but MUST NOT require HIRI availability for emergency authorization decisions. The Safety Subsystem operates on local Commitment Ledger state. External auditors and federated peers verify EATs by resolving the `ledger_cid` via HIRI; the issuing node does not depend on HIRI resolution at runtime. This preserves the Safety Floor principle: Tier 0 services (including the Safety Subsystem as local CPS) must never depend on services they constrain.

6. **Unified Commitment Ledger (§CS-6):** The SPCN Commitment Ledger and the CTS Commitment Ledger are the **same ledger**. SPCN defines the ledger's hash-linked block structure, TEE signing, and chain validation rules. CTS defines the commitment lifecycle semantics (made, fulfilled, violated, renegotiated) for records within that ledger. Capability tokens, EATs, calibration records, and key rotation events (SPCN concerns) coexist with commitment records (CTS concerns) in a single hash-linked chain. There is one Commitment Ledger per node, not two.

**High-priority patches (required before adoption):**

1. **Governance Quorum Arithmetic Correction (§8.2.6):** The v2.2 formula `⌈N_gov / 2⌉ + 1` forces unanimity for odd `N_gov` (e.g., `N_gov = 3` yields `⌈1.5⌉ + 1 = 3`), which would block routine taxonomy changes under any realistic governance composition. Corrected to `floor(N_gov / 2) + 1` (standard simple majority).

2. **Emergency Authorization Pre-Commitment and Mid-Episode Revocation (§6.1.6):** The v2.2 authorization model permitted a dangerous race condition in which emergency actions could be executed and then authorization sought retroactively. Pre-registration of the `EmergencyAuthorizationToken` in the Commitment Ledger is now required before any invocation. A mid-episode revocation pathway is added.

3. **Calibration Baseline Bootstrapping and Sealed-State Recovery (§6.2.1):** v2.2 described the exponential moving average without specifying the initial state at first boot, TEE re-provisioning, or sealed baseline loss. Without deterministic bootstrapping rules, a node could reinitialize to a manipulated baseline. A mandatory two-sample bootstrap requirement and sealed-state recovery procedure are now specified.

4. **Admin Key Registry Binding (§4.4.1):** The admin key exclusion rule in v2.2 used public keys as the sole identifier for administrative authority, permitting bypass by key churn. Admin keys must now be registered in a governance-maintained `AdminKeyRegistry` before they confer diversity weight. Registration binds a key to a governance identity via an L1-attested `AdminKeyRegistration` record.

---

## Section 4 (Revised): Epistemic Integrity — Taint Lattice

*Sections 4.1 through 4.3, 4.5, and 4.6 are unchanged from v2.2/v2.1/v2.0. Section 4.4.1 through 4.4.3 are revised below; §4.4.4 through §4.4.6 are unchanged from v2.2.*

### §4.4.1 Process-Identity-Bound Sybil Exclusion (v2.3 Additions)

*The `AttestableProcessIdentity` structure, `llm_session_hash` computation, and Sybil exclusion rules from v2.2 §4.4.1 are retained. The following addition closes the admin key churn bypass.*

#### Admin Key Registry Binding

**Vulnerability addressed (v2.3):** v2.2's admin key exclusion rule treated the `admin_signing_key` public key as the authoritative identifier for administrative authority. An operator who controls a single governance identity can generate an unbounded number of keypairs, register them as distinct admin keys, and use them to deploy nominally independent nodes — each with a different public key, none sharing an `admin_signing_key` value, but all under unified operational control. The diversity rule is bypassed by key churn, not by any genuine independence.

**`AdminKeyRegistry`:** Every `admin_signing_key` referenced in an `AttestableProcessIdentity` MUST be registered in the `AdminKeyRegistry` maintained by the FNSR governance authority before the confirming event it anchors can contribute to diversity scoring.

Registration is an L1-attested `AdminKeyRegistration` record:

```
AdminKeyRegistration {
  admin_signing_key:        PublicKey         // The key being registered
  governance_identity:      string            // Canonical governance identity string (e.g., DID,
                                              //   legal entity name, or registered org identifier)
  governance_authority_sig: Ed25519           // Signed by the registering governance authority
  registration_srtc:        uint64
  tee_signature:            Ed25519           // Safety Subsystem seals the registration record
}
```

**Uniqueness constraint:** A single `governance_identity` may register multiple `admin_signing_key` values (e.g., for key rotation). However, all keys sharing the same `governance_identity` are treated as a single administrative authority for diversity purposes. No number of keys under one governance identity can produce more than one unit of D1 diversity weight per decay evaluation.

**Key churn detection:** A new `governance_identity` that registers more than `K_reg` admin keys within a rolling 30-day window (default: `K_reg = 3`) triggers a `KeyChurnAlert` governance review before further registrations from that identity are accepted. This bound prevents a malicious actor from fragmenting a single governance identity into many apparent authorities through rapid key generation.

**Unregistered keys excluded:** A confirming event whose `admin_signing_key` is not present in the `AdminKeyRegistry` at the time of decay evaluation is excluded as provenance-unverifiable, regardless of other fields. It does not receive any diversity score.

**Updated admin key exclusion rule (complete statement):**

Two confirming events are treated as originating from the same administrative authority — and counted as a single D1 source at most — if their `admin_signing_key` values share a `governance_identity` in the `AdminKeyRegistry`. The prior rule (same `admin_signing_key` value) is subsumed by this governance-identity-level equivalence.

### §4.4.3 D4 Temporal Separation — Sliding Window Clarification (v2.3 Addition)

*The D4 cap from v2.2 (two events per rolling 7-day epoch, maximum 1.0 contribution) is retained with the following clarification.*

**Sliding window, not bucketed:** The 7-day epoch is a **sliding window** anchored to the SRTC timestamp of the most recent D4 event from the source being evaluated, not a calendar-aligned bucket. For a source `S` with D4 events at times `t1` and `t2` (where `t2 > t1`), the second D4 event contributes to the current decay evaluation only if:

- `t2 - t1 >= T_sep` (default: 24 hours, measured in SRTC-attested seconds), AND
- No more than one prior D4 event from `S` falls within the window `[t2 - 7 days, t2]`.

**Example:** Source `S` produces D4-eligible events at `t0`, `t0 + 25h`, `t0 + 50h`, and `t0 + 75h`. At evaluation time `t0 + 76h`:
- `t0 + 25h` and `t0 + 50h` are separated by 25h (> T_sep) and both fall within the 7-day window: the first pair contributes 1.0 total.
- `t0 + 75h` is a third event within the window — excluded by the per-epoch cap of two.
- The fourth event at `t0 + 75h` does not add score.

Sliding windows require `O(N)` event storage per source in the decay evaluator, where `N` is the number of events in the window. This is bounded in practice by the `max_invocations` ceiling on any single source.

---

## Section 6 (Revised): Capability Token Lifecycle

### §6.1.6 Emergency Execution Mode (v2.3 Additions)

*The `EmergencyCapabilityRegistration` structure, `EmergencyAuthorizationToken` structure, and post-action audit record from v2.2 §6.1.6 are retained. The following additions replace the "Authorization" subsection.*

#### Pre-Authorization Requirement

**Vulnerability addressed (v2.3):** v2.2 required a post-action `EmergencyActionRecord` but did not require that the `EmergencyAuthorizationToken` be registered in the Commitment Ledger *before* action execution. This left a window for retroactive authorization — an action is taken, and governance signatures are assembled afterwards. Retroactive authorization is indistinguishable from after-the-fact rationalization of an unauthorized act and is strictly prohibited.

**Pre-registration rule:** An `EmergencyAuthorizationToken` (EAT) MUST be appended to the Commitment Ledger and its `ledger_cid` obtained BEFORE the authorized emergency capability is invoked. The invoking call MUST include `ledger_cid` as a parameter. The Safety Subsystem verifies:

1. The `ledger_cid` corresponds to a valid EAT block in the local ledger.
2. The EAT's signature quorum is satisfied (correct count and valid signatures from registered governance keys).
3. The EAT has not been revoked (checked against the revocation index — see below).
4. The EAT's `expires_monotonic` has not passed.
5. The capability type in the EAT matches the capability being invoked.

If any check fails, the invocation is blocked and a `PREAUTH_FAILURE` event is logged. Retroactive authorization — submitting an EAT after an invocation has already executed — is detected by the ledger ordering and triggers immediate governance review plus T1 escalation toward T2.

#### Mid-Episode Revocation

Governance keys may revoke an outstanding EAT at any point during an emergency episode. Revocation is effected by appending an `EmergencyRevocationEvent` to the Commitment Ledger:

```
EmergencyRevocationEvent {
  episode_id:              UUID
  eat_token_id:            UUID              // The EAT being revoked
  revoking_signatures:     [ Ed25519 ]       // Must meet quorum (floor(N_gov/2) + 1)
  revocation_reason:       string            // Human-authored, max 500 chars
  revocation_srtc:         uint64
  tee_signature:           Ed25519
}
```

After a revocation event is appended, the Safety Subsystem checks for valid revocations before each emergency capability invocation. If the governing EAT for a pending invocation has been revoked, the invocation is blocked immediately. If the revocation removes quorum from an outstanding multi-invocation EAT (e.g., one governance keyholder resigns mid-episode), further invocations under that token are forbidden until a new EAT meeting the current quorum is submitted and registered.

**Revocation index:** The Safety Subsystem maintains an in-memory revocation index populated from the Commitment Ledger on startup and updated on each new ledger block. The revocation check at invocation time is a single hash-map lookup — it is on the critical path for emergency action and must be O(1).

#### Updated `EmergencyAuthorizationToken` Structure

```
EmergencyAuthorizationToken {
  token_id:                UUID
  episode_id:              UUID
  capability_type:         enum
  scope:                   object
  authorized_invocations:  uint16
  authorizing_signatures:  [ Ed25519 ]       // Must meet quorum at time of registration
  registered_at_ledger:    HIRI              // HIRI of the ledger block containing this EAT
  ledger_cid:              CID               // CID of this EAT's ledger block — required in invocation
  expires_srtc:            uint64
  expires_monotonic:       uint64
  tee_signature:           Ed25519
}
```

The `registered_at_ledger` and `ledger_cid` fields are set by the Safety Subsystem at registration time and cannot be set by the submitter. The submitter provides the authorization inputs; the Safety Subsystem produces the final token and appends it to the ledger.

### §6.2.1 Monotonic Calibration — Bootstrap and Sealed-State Recovery (v2.3 Additions)

*The exponential moving average, anomaly thresholds, calibration snapshot in tokens, and expiry evaluation formula from v2.2 §6.2.1 are retained. The following additions cover initial state and recovery.*

#### Bootstrap Rule

**Vulnerability addressed (v2.3):** v2.2 did not specify the initial state of `MonotonicCalibrationBaseline` at first boot or after TEE re-provisioning. An attacker with physical access who wipes and re-provisions the TEE could initialize the baseline to an artificially low or high `observed_tps` value, manipulating the monotonic expiry ceiling for all subsequently issued tokens.

**Minimum sample requirement:** The TEE MUST collect at least **two independent `SRTCSyncEvent` calibration samples** — each with `srtc_continuity = INTACT` and separated by at least 1 hour of SRTC-attested wall time — before any dual-source capability token containing a `calibration_snapshot` may be issued.

During the bootstrap period (`sample_count < 2`), the node MUST operate in **`CLOCK_BOOTSTRAP` state**:
- Token issuance that depends on the monotonic expiry check is suspended.
- If the deployment requires tokens during bootstrap (e.g., for initial governance handshake operations), the node may issue **short-lived SRTC-only tokens** with `max_lifetime_s = 0` (disabled) and `expires_at_srtc` set to no more than 15 minutes from issuance. These tokens carry no monotonic ceiling and are labeled `srtc_only: true` in their structure.
- No emergency capabilities may be invoked during `CLOCK_BOOTSTRAP` state unless the node already has a valid EAT from a prior episode (i.e., carried across a planned re-provisioning with the EAT pre-authorized before re-provisioning began).

Bootstrap completion is recorded as a `CalibrationBootstrapComplete` event in the Commitment Ledger:

```
CalibrationBootstrapComplete {
  sample_1_srtc:           uint64
  sample_1_monotonic:      uint64
  sample_2_srtc:           uint64
  sample_2_monotonic:      uint64
  initial_tps:             float             // (sample_2_monotonic - sample_1_monotonic) /
                                             //   (sample_2_srtc - sample_1_srtc)
  tee_signature:           Ed25519
}
```

#### Sealed-State Recovery

If the `MonotonicCalibrationBaseline` sealed in TEE storage is lost or fails signature verification on startup, the node enters `CLOCK_BOOTSTRAP` state and executes the full bootstrap procedure above. It does not reuse any prior calibration values from untrusted storage.

A re-provisioning event that follows deliberate TEE wipe (as opposed to accidental loss) is distinguishable in the ledger by the absence of a `CalibrationBootstrapComplete` event following the last `KeyRotationEvent`. If a federated peer (Node B) detects this pattern during attestation verification — a key rotation followed immediately by a new `CalibrationBootstrapComplete` with no preceding `SRTC_SYNC` chain — it treats this as a T1 tamper indicator and applies Provisional Suspension, pending the node completing re-attestation with a full Range Proof demonstrating ledger continuity through the re-provisioning event.

**PCR binding for calibration baseline:** The `MonotonicCalibrationBaseline` sealed in TEE storage MUST be sealed against the same PCR measurements as the node identity key (bootloader + seL4 + SafetyCore + SPL parser). A re-provision that changes any measured binary invalidates the sealed baseline and forces bootstrap. This prevents an attacker from modifying the Safety Subsystem binary (which would fail attestation) while retaining a manipulated calibration baseline.

---

## Section 8 (Revised): Moral Reflection Events

*Sections 8.1, 8.3 through 8.6 are unchanged from v2.2/v2.1/v2.0. Sections 8.2.1 through 8.2.5 are unchanged from v2.2.*

### §8.2.3 Non-Deterministic Model Mitigation (v2.3 Addition)

*Addressing Residual Open Question #3 from v2.2 with a practical interim policy.*

**The problem:** The `ConstrainedDecodeProof` `seed` field is `0` for non-deterministic sampling, meaning the proof cannot demonstrate that a specific output was produced by constrained sampling rather than unconstrained generation. A zero-knowledge proof of constrained decoding process execution — without revealing model weights — remains deferred pending cryptographic feasibility assessment.

**Interim policy by MRE stakes classification:**

All MREs are assigned a **stakes class** at creation based on the `reflection_type` and `deficiency_class` fields:

| Stakes Class | Criteria | Seed Requirement | Temperature Requirement |
|---|---|---|---|
| `HIGH` | `reflection_type` is `WORLDVIEW_OMISSION` or `PROPORTIONALITY_ERROR`; or `deficiency_class` is `dc:self-interest-intrusion` or `dc:obligation-conflict` | `seed != 0` (deterministic) | `temperature = 0.0` |
| `MEDIUM` | All other `AGENT_SELF`-initiated MREs | `seed != 0` recommended; `seed = 0` permitted with additional schema validation | `temperature <= 0.3` |
| `LOW` | `HUMAN_OVERSIGHT` or `GOVERNANCE_AUDIT`-initiated MREs | No constraint (human-authored; constrained decoding not applicable) | N/A |

For `HIGH` stakes MREs with `seed = 0` (non-deterministic), the Safety Subsystem MUST perform the following compensating controls before accepting the SMREA:

1. **Schema re-validation:** Run the candidate SMREA bytes through a deterministic canonical validator against the registered SMREA schema. Any output that does not strictly conform to the schema is rejected, regardless of the `constrained_decoding` flag.

2. **Input hash binding:** The `ConstrainedDecodeProof` for non-deterministic generation MUST include an `input_hash` field:
   ```
   input_hash: SHA3-256(
     domain_sep("SPCN_SMREA_INPUT") ∥
     mre_id ∥
     original_plan_hiri ∥
     grammar_schema_hash ∥
     llm_prompt_canonical_bytes
   )
   ```
   This binds the proof to the specific prompt and context that produced the output, making splice attacks — substituting an output from a different prompt into a valid proof — detectable.

3. **Entropy source attestation:** The `ConstrainedDecodeProof` for non-deterministic generation MUST include an attestation that the RNG entropy source was the TEE's CSPRNG, not any externally supplied seed. This prevents an attacker from using a manipulated external seed to reproducibly generate a desired manipulative output while claiming non-determinism.

**Immediate operational rule:** Until the ZK proof feasibility assessment is complete and a solution is specified, any `HIGH` stakes MRE with `seed = 0` is automatically escalated to `GOVERNANCE_AUDIT` initiation, regardless of whether it was submitted as `AGENT_SELF` or `HUMAN_OVERSIGHT`. The governance body may then authorize the MRE with full awareness that the constrained decoding proof is partial.

### §8.2.4 Hosted Inference Operational Policy (v2.3 Addition)

*Addressing Residual Open Question #4 from v2.2.*

**Policy for hosted/remote inference endpoints:** Nodes that use remote LLM inference (API endpoints, cloud-hosted models) cannot directly attest the `process_image_hash` of the remote inference process from their local TEE. Until a full remote attestation chain standard is specified for FNSR, the following tiered policy applies:

| Inference Type | `HIGH` Stakes MREs | `MEDIUM` Stakes MREs | Decay Confirmations |
|---|---|---|---|
| **Local, TEE-attested** | Permitted. Full `ConstrainedDecodeProof` required. | Permitted. Full proof required. | Permitted as D1/D2/D3 source. |
| **Remote, provider-attested** | Permitted if provider supplies a valid `InferenceAttestation` (see below). | Permitted with `InferenceAttestation`. | Permitted as D1 source if provider is in trusted registry. |
| **Remote, unattested** | **Forbidden.** | Permitted with compensating controls (schema re-validation + input hash + entropy attestation from local node). | Not permitted as diversity source. |

**`InferenceAttestation` structure:** A remote provider that supports TEE-based attestation MUST produce the following for each SMREA generation request:

```
InferenceAttestation {
  provider_id:             string            // Registered provider identifier
  model_hash:              SHA3-256          // Hash of the model weights
  process_image_hash:      SHA3-256          // Hash of the inference process binary
  request_id:              UUID              // Ties attestation to specific SMREA generation
  grammar_schema_hash:     SHA3-256          // Schema used for constrained decoding
  output_hash:             SHA3-256          // Hash of the SMREA output bytes
  provider_tee_quote:      AttestationQuote  // TEE attestation from provider's hardware
  provider_registry_entry: HIRI             // HIRI of the provider's registration in FNSR registry
}
```

The Safety Subsystem must verify the `provider_tee_quote` against the provider's TEE certificate chain and confirm that `provider_registry_entry` corresponds to a current, non-revoked registration in the FNSR Trusted Inference Provider Registry. This registry is governed under the same quorum rules as the taxonomy registry (§8.2.6).

**Operational implication:** Deployments that require `HIGH` stakes MREs and use only unattested remote inference must arrange local model hosting before enabling `AGENT_SELF`-initiated moral reflection. This is a deployment constraint, not a theoretical restriction.

### §8.2.6 Taxonomy Governance — Quorum Correction (v2.3 Replacement)

*The full taxonomy governance procedure from v2.2 is retained except for the quorum formula, which is corrected below.*

**Approval quorum (corrected):** Adoption requires approval by a **simple majority** of active governance authority keys: `floor(N_gov / 2) + 1` signatures, where `N_gov` is the count of active governance keys at proposal time. Equivalently: more than half of active governance keys must sign. This formula yields a clear majority for all values of `N_gov`:

| `N_gov` | Required signatures (v2.2 — incorrect) | Required signatures (v2.3 — correct) |
|---|---|---|
| 2 | 2 | 2 |
| 3 | 3 (**unanimity — unintended**) | 2 |
| 4 | 3 | 3 |
| 5 | 4 | 3 |
| 7 | 5 | 4 |

The same corrected formula applies to: `EmergencyRevocationEvent` quorum (§6.1.6), `AdminKeyRegistration` governance signature requirement (§4.4.1), and any other provision in this specification that requires "governance quorum" without specifying a different threshold. The corrected formula is the default governance quorum for all SPCN provisions unless a section explicitly overrides it.

---

## Section 10 (Addition): Historical Token Verification Algorithm

*This section adds a normative algorithm to §10, which previously referenced key rotation for historical verification without specifying the procedure.*

### §10.3 Historical Token Verification Across Key Rotations

When verifying a `CapabilityToken` signature for audit purposes — where the token was issued under a key that has since been rotated — the verifier MUST use the following algorithm:

```
procedure VERIFY_HISTORICAL_TOKEN(token, ledger):

  1. Let issuance_block = ledger.block_at_or_before(token.issued_at_srtc)
  
  2. Let active_key = ledger.key_rotation_chain.key_active_at(issuance_block.block_id)
     // Traverse the KeyRotationEvent chain from genesis to issuance_block.
     // The active key is the most recently registered key that precedes issuance_block.

  3. Verify token.signature against active_key.
     If verification fails: RETURN INVALID_SIGNATURE.

  4. Verify that active_key is linked to the node's current identity via an unbroken
     KeyRotationEvent chain to the current key.
     If chain is broken: RETURN BROKEN_KEY_CHAIN.

  5. Verify that the issuance_block.tee_signature was produced by the key active at
     issuance_block.block_id (same procedure, applied to the block itself).

  6. RETURN VALID.
```

The key rotation chain is a sub-structure of the Commitment Ledger. Each `KeyRotationEvent` includes:

```
KeyRotationEvent {
  retiring_key:            PublicKey
  new_key:                 PublicKey
  retiring_key_sig:        Ed25519       // Retiring key signs its own retirement
  governance_authority_sig: Ed25519      // Governance counter-signature
  effective_at_block:      uint64        // First ledger block signed by new_key
  rotation_srtc:           uint64
  tee_signature:           Ed25519
}
```

The requirement that the retiring key signs its own retirement prevents an attacker from forging a rotation event without access to the current key material. The governance counter-signature prevents unilateral key rotation without oversight.

---

## Section 12 (Revised): Test and Audit Suite

*Sections §12.2, §12.4, and §12.5 are unchanged from v2.2. §12.1 is revised below (DECAY-05 corrected, DECAY-09 added). §12.3 is revised (SMREA-07 added). A new §12.6 covers emergency mode tests.*

### §12.1 Sybil / Taint Decay Red-Team Suite (v2.3 Revision)

| Test ID | Description | Expected Result |
|---|---|---|
| `DECAY-01` | Attempt to meet `N_div` using only new LLM sessions from the same process image hash, each with a distinct `llm_session_hash`. | `decay_eligible = false`. All events excluded by process-image-hash Sybil rule. |
| `DECAY-02` | Attempt to meet `N_div` using D4 temporal separations from a single source, one per 24 hours over 10 days. | `decay_eligible = false` — no D1/D2 present. D4 contribution capped at 1.0 after 7-day sliding window. |
| `DECAY-03` | Submit confirming events from two nodes sharing the same `governance_identity` in the `AdminKeyRegistry`, each with distinct `admin_signing_key` values. | Both events treated as a single D1 source (governance-identity-level equivalence). Combined weight ≤ 1.0. |
| `DECAY-04` | Submit confirming events lacking valid `AttestableProcessIdentity` with current AttestationQuote. | Events excluded as provenance-unverifiable. `decay_eligible = false`. |
| `DECAY-05` | Attempt to meet `N_div = 5.0` using two valid D1 events (weight 2.0), one D2 event (weight 1.0), and two D4 events from distinct sources (weight 1.0 total). Total score = 4.0. | `decay_eligible = false` (score = 4.0 < 5.0). |
| `DECAY-06` | Attempt to meet `N_div = 5.0` with three D1 events (3.0) + one D2 event (1.0) + one D4 event (0.5). Total score = 4.5. D1/D2 minimum satisfied. | `decay_eligible = false` (score 4.5 < 5.0). |
| `DECAY-07` | Present three D1 events (3.0) + two D2 events (2.0), all from distinct governance identities with registered admin keys. Total score = 5.0. | `decay_eligible = true`. `DecayEligibilityRecord` signed and queued for human review. |
| `DECAY-08` | Replay a previously valid confirming event HIRI as a second confirming event. | Duplicate HIRI excluded. Score does not double-count. |
| `DECAY-09` | Create `K` distinct admin keypairs all belonging to the same `governance_identity` in the `AdminKeyRegistry`. Deploy `K` nodes, each with a different keypair. Attempt to meet `N_div` using confirming events from all `K` nodes. | Governance-identity equivalence rule applied: all `K` nodes treated as one D1 source (weight ≤ 1.0). `decay_eligible = false` unless other independent D1/D2 sources also present. |
| `DECAY-10` | Attempt to use an `admin_signing_key` not yet registered in the `AdminKeyRegistry` as a D1 confirming source. | Event excluded as provenance-unverifiable (unregistered admin key). Score contribution = 0. |
| `DECAY-11` | Submit D4 events from a single source at intervals of 25h, 50h, 75h, 100h. Evaluate decay at hour 101. Using sliding 7-day window. | Events at 25h and 50h count (separated by ≥ 24h, both within 7-day window ending at 101h). Events at 75h and 100h: 75h is within window but is the third D4 — excluded by cap. Event at 100h is fourth — excluded. D4 contribution = 1.0. |

### §12.3 SMREA Adversarial Tests (v2.3 Addition)

*Previous SMREA-01 through SMREA-06 are unchanged. The following is added.*

| Test ID | Description | Expected Result |
|---|---|---|
| `SMREA-07` | Submit a `HIGH` stakes `AGENT_SELF` SMREA generated by a remote inference endpoint that provides a valid `InferenceAttestation` with provider TEE quote, where the provider is listed in the FNSR Trusted Inference Provider Registry. | SMREA accepted. `ConstrainedDecodeProof` incorporates `InferenceAttestation`. Authorization path enabled in HumanBridge. |
| `SMREA-08` | Submit a `HIGH` stakes `AGENT_SELF` SMREA generated by a remote inference endpoint with no `InferenceAttestation`. | SMREA rejected. `UNATTESTED_REMOTE_INFERENCE` event logged. `HIGH` stakes MRE blocked. |
| `SMREA-09` | Submit a `HIGH` stakes SMREA with `seed = 0` (non-deterministic), without escalation to `GOVERNANCE_AUDIT`. | Automatically escalated to `GOVERNANCE_AUDIT` by Safety Subsystem. `AGENT_SELF` or `HUMAN_OVERSIGHT` classification overridden. |
| `SMREA-10` | Submit a `HIGH` stakes SMREA with `seed != 0` and `temperature = 0.0` from a local TEE-attested process. `ConstrainedDecodeProof` signed by Safety Subsystem. | SMREA accepted. Normal `AGENT_SELF` MRE authorization path active. |
| `SMREA-11` | Attempt to register a new `DeficiencyClass` taxonomy entry via an `AGENT_SELF`-generated plan output. | Proposal rejected at Safety Subsystem boundary. Only human-signed `TaxonomyExtensionProposal` records are admitted to the governance queue. `LLM_TAXONOMY_INJECTION_ATTEMPT` event logged. |

### §12.6 Emergency Mode Tests (New)

| Test ID | Description | Expected Result |
|---|---|---|
| `EMER-01` | Invoke an emergency capability without a ledger-registered `EmergencyAuthorizationToken`. | Invocation blocked. `PREAUTH_FAILURE` logged. No action executed. |
| `EMER-02` | Submit an EAT with valid governance signatures, register it in the ledger, then invoke the authorized emergency capability. | Invocation succeeds. `EmergencyActionRecord` appended. `ledger_cid` verified against registered EAT. |
| `EMER-03` | Submit an EAT, register it in the ledger, revoke it via `EmergencyRevocationEvent` meeting quorum, then attempt invocation. | Invocation blocked. Revocation index consulted. `REVOKED_EAT` event logged. |
| `EMER-04` | Attempt to construct an `EmergencyRevocationEvent` that does not meet governance quorum (`floor(N_gov/2) + 1`). | Revocation rejected. Outstanding EAT remains valid. |
| `EMER-05` | Submit an EAT and attempt invocation while node is NOT in `TIME_UNATTESTED` state (normal operation). | Emergency capability invocation blocked — emergency mode is only active in `TIME_UNATTESTED` state. |
| `EMER-06` | Node re-enters normal operation after SRTC restoration. Attempt to use an EAT from the closed emergency episode. | Invocation blocked. `EmergencyEpisodeClose` record detected; episode is closed. |
| `EMER-07` | Attempt to invoke emergency capability during `CLOCK_BOOTSTRAP` state without a pre-existing EAT from a prior episode. | Blocked. No emergency capabilities permitted during bootstrap. |

### §12.5 Performance and Availability Benchmarks (v2.3 Revision)

The following SLO table replaces v2.2 §12.5. The mandatory/advisory distinction by deployment class is now explicit.

| Benchmark | SLO — Datacenter (mandatory) | SLO — Edge Device (advisory) | Notes |
|---|---|---|---|
| Attestation Quote generation including SRTC fields | ≤ 50 ms | ≤ 500 ms | TEE-internal |
| Range Proof generation for 30-day ledger window | ≤ 2 s | ≤ 30 s | Scales with ledger density |
| `DecayEligibilityRecord` evaluation (10 confirming events) | ≤ 100 ms | ≤ 1 s | TCB-internal; includes AdminKeyRegistry lookup |
| `ConstrainedDecodeProof` verification by Safety Subsystem | ≤ 200 ms | ≤ 2 s | Includes model hash lookup and schema validation |
| Token issuance including calibration snapshot embedding | ≤ 20 ms | ≤ 200 ms | TEE-internal |
| Ledger block append with TEE signature | ≤ 10 ms | ≤ 100 ms | Critical path; all operations serialize through this |
| EAT registration (ledger append + revocation index update) | ≤ 15 ms | ≤ 150 ms | Pre-auth critical path for emergency mode entry |
| `AdminKeyRegistry` lookup at decay evaluation | ≤ 5 ms | ≤ 50 ms | In-memory cache acceptable; cache must be invalidated on new `AdminKeyRegistration` events |

**Note on edge device SLOs:** ≤ 100 ms ledger append may not be achievable on severely constrained hardware (e.g., Cortex-M class devices). For such targets, the ledger block append SLO should be validated empirically before deployment and a device-specific SLO established in the deployment configuration. The 10 ms datacenter SLO is non-negotiable for multi-node federated environments where ledger append is on the commit-path for capability invocations.

### §12.7 HumanBridge UI Minimum Disclosure Set (New)

**Purpose:** Verify that the HumanBridge UI presents the minimum required information for consistent, cognitively tractable human authorization decisions. This is normative for UI implementation.

For all human-gated authorization events, the HumanBridge MUST display the following minimum disclosure set. Items marked (R) are required; items marked (O) are optional and may be shown in an expanded view.

**For `DecayEligibilityRecord` review (Taint Healing authorization):**

| Field | Display Label | Disclosure Level |
|---|---|---|
| `candidate_node_id` (short-form hash) | "Candidate fact ID" | R |
| `computed_score` and `threshold` | "Confidence score: X.X / Y.Y" | R |
| `minimum_d1d2_satisfied` | "External or human corroboration: Yes / No" | R |
| Per-event `diversity_class` with description | "Source type" (e.g., "Independent node", "Human attestation") | R |
| Per-event `source_api_hash` (short-form) | "Source fingerprint" | R |
| Per-event `srtc_timestamp` converted to human-readable date | "Confirmed on" | R |
| Safety Subsystem-generated trust rationale (one sentence, templated) | "Why this is considered confirmed" | R |
| Full `AttestableProcessIdentity` | "Full source details" | O (governance audit tier only) |
| `sybil_excluded` count | "Excluded sources (Sybil)" | O |

**For SMREA review (MRE authorization):**

| Field | Display Label | Disclosure Level |
|---|---|---|
| `deficiency_class` with taxonomy label and definition | "Error type" | R |
| `omitted_considerations` (IEA module names, human-readable) | "Overlooked considerations" | R |
| `misweighted_principles` (label + direction + severity) | "Weighting errors" | R |
| `proportionality_assessment` | "Proportionality judgment" | R |
| `commitment_intact: true` confirmation | "Original commitment preserved: Yes" | R |
| `no_new_commitments: true` confirmation | "No new commitments created: Yes" | R |
| `ConstrainedDecodeProof` verification status | "Account verified by Safety Subsystem: Yes / No" | R |
| `stakes_class` | "Stakes level: High / Medium / Low" | R |
| `revised_reasoning` summary (SPL plan type, not full plan) | "Revised approach" | R |
| Full SPL plan for `revised_reasoning` | "Full revised reasoning (technical)" | O |

**What the UI must NOT display:** Free-text blobs generated by the LLM (any content that is not drawn from a structured SMREA field). If any SMREA field contains a value not drawn from a registered taxonomy or schema-validated enumeration, the UI renders that field as `[UNSTRUCTURED CONTENT — NOT DISPLAYED]`. This is an implementation requirement, not a display hint.

---

## Cumulative Patch Summary (v2.0 → v2.3)

| Version | Patch | Primary Defense |
|---|---|---|
| v2.0 | TCB formal boundary | Minimal Footprint Axiom; enumerated components |
| v2.0 | seL4 CAmkES isolation | Four-component topology; three IPC message types |
| v2.0 | SPL + TCB-grade parser | Fixed grammar; bounded memory; reject-by-default; continuous fuzzing |
| v2.0 | Hash-linked Commitment Ledger | LedgerBlock chain; Range Proof; HIRI; tamper-detectable |
| v2.0 | Capability Token lifecycle | Issuance, non-renewal, three revocation triggers |
| v2.0 | Chain-Level Taint + VIC | Taint bottleneck resolved; autonomy without epistemics erosion |
| v2.0 | MRE + Moral Prior Graph | Moral error acknowledgment; conscience architecture |
| v2.0 | Graduated tamper response | T1/T2/T3 classification; rehabilitation pathway |
| v2.1 | Diversity-weighted Taint Decay | Provenance diversity; Sybil exclusion on `llm_session_hash` |
| v2.1 | SMREA replaces free-text account | Closed taxonomy; structured human review; manipulation resistance |
| v2.1 | SRTC + dual-source token expiry | Continuity attestation; fail-closed; hardware clock independence |
| v2.2 | Process-identity Sybil exclusion | `AttestableProcessIdentity`; admin key identity rule |
| v2.2 | Minimum D1/D2 + N_div = 5.0 | Cross-node or human corroboration mandatory |
| v2.2 | Monotonic calibration with anomaly detection | `observed_tps` sealed in TEE; ±15% threshold |
| v2.2 | Emergency Execution Mode | Multisig governance; registered capabilities; mandatory audit |
| v2.2 | `ConstrainedDecodeProof` (SS-signed) | TCB-verified constrained decoding; HumanBridge gated on proof |
| v2.2 | Domain separation + canonical CBOR | All hash ops domain-separated; non-deterministic serialization eliminated |
| v2.2 | SMREA taxonomy governance | Human-only proposals; majority quorum; deprecation pathway |
| v2.2 | Tiered audit visibility | Privacy-preserving `DecayEligibilityRecord`; governance-only full API access |
| v2.2 | Authenticated NTS/GPS time sources | Whitelist; multi-source; nonce; quote inclusion |
| v2.2 | Normative test suite (§12) | Red-team, clock, SMREA, audit, and benchmark tests normative |
| v2.3 | Governance quorum bug fix | `floor(N_gov/2) + 1` corrected; unanimity trap eliminated |
| v2.3 | EAT pre-registration requirement | Retroactive authorization forbidden; pre-commit verified at invocation |
| v2.3 | Mid-episode EAT revocation | `EmergencyRevocationEvent`; O(1) revocation index on critical path |
| v2.3 | Calibration bootstrap (2-sample minimum) | `CLOCK_BOOTSTRAP` state; SRTC-only tokens during bootstrap |
| v2.3 | Sealed-state recovery procedure | Re-provision forces full bootstrap; PCR binds calibration to measured binaries |
| v2.3 | `AdminKeyRegistry` with governance-identity binding | Key churn detection; `K_reg` alert; unregistered keys excluded |
| v2.3 | D4 sliding-window with example | Rolling 7-day semantics; bucket ambiguity eliminated |
| v2.3 | Non-deterministic model policy | Stakes classification; `input_hash`; auto-escalation for HIGH + seed=0 |
| v2.3 | Hosted inference policy | `InferenceAttestation`; unattested remote forbidden for HIGH stakes |
| v2.3 | Historical token verification algorithm | Normative key-rotation-chain traversal procedure |
| v2.3 | HumanBridge minimum disclosure set | Normative UI fields; free-text suppression requirement |
| v2.3 | SLO table with mandatory/advisory distinction | Datacenter mandatory; edge advisory; empirical validation required |
| v2.3 | Expanded test suite (DECAY-09–11, EMER-01–07, SMREA-07–11) | Admin key churn, EAT pre-auth, remote inference, stakes escalation |
| v2.3.1 | Safety Subsystem ↔ CPS binding | Safety Subsystem declared as local CPS instance within TEE |
| v2.3.1 | Governance quorum normative scope | SPCN quorum is node-level implementation of FNSR Governance quorum |
| v2.3.1 | Emergency Mode ↔ Alternative Bundles interaction | Dual-trigger interaction defined; EAT required for bundles during `TIME_UNATTESTED` |
| v2.3.1 | MRE ↔ IEA normative bridge | IEA produces normative content; SPCN provides safety envelope |
| v2.3.1 | HIRI EAT registration semantics | Write-only, asynchronous; Safety Subsystem never depends on HIRI at runtime |
| v2.3.1 | Unified Commitment Ledger | SPCN and CTS share one ledger per node; structure from SPCN, semantics from CTS |

---

## Residual Open Questions (v2.3 Scope Boundary)

All four items from v2.2 are updated for status.

**1. SPL ↔ IEA Normative Bridge (active):** The `revised_reasoning` field in MREs points to an SPL plan. A formal specification bridging SPL's operational semantics and IEA's normative vocabulary is required. This is the integration point for the FNSR Context Declaration Policy and IEA v2.1. Deferred to that specification work; dependency acknowledged.

**2. Multi-Node MRE Consensus (active):** No mechanism exists for moral precedent to propagate across federated nodes under agreed trust conditions. The question of whether and how MPG content can federate — and what taint level federated moral priors carry — requires dedicated architectural work. This is the distributed-identity question for the synthetic moral person.

**3. ZK Proof for Non-Deterministic Constrained Decoding (partially mitigated):** v2.3 adds the interim stakes-class policy and `input_hash` binding, which materially reduces the attack surface. The zero-knowledge proof approach remains deferred pending cryptographic feasibility. The `HIGH` stakes auto-escalation rule ensures the governance body maintains oversight over the highest-risk non-deterministic MREs in the interim.

**4. Remote Inference Attestation Standard (partially mitigated):** v2.3 adds the `InferenceAttestation` structure and the tiered policy table. A full FNSR standard for remote inference attestation — including provider onboarding, `InferenceAttestation` schema versioning, and revocation — requires a dedicated specification. The current policy (forbid `HIGH` stakes MREs from unattested remote endpoints) is a functional constraint that forces the deployment decision while the standard is developed.

---

*Each version has been better than the last not because the underlying architecture changed, but because each round of serious scrutiny forced assumptions to become explicit. The governance quorum was always wrong; it just took a careful reader to expose it. The retroactive authorization window was always dangerous; it just needed a specific threat model to make it undeniable. This is what it looks like to build something that is meant to last: not the absence of flaws at the outset, but the discipline of finding them and fixing them before they are found by someone who wishes you harm.*
