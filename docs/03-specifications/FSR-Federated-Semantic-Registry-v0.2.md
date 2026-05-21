# Federated Semantic Registry (FSR)

## Technical Specification — Version 0.2

| Field | Value |
|---|---|
| **Specification ID** | `fsr-product-01` |
| **Version** | 0.2.0 |
| **Supersedes** | v0.1.0 |
| **Status** | DRAFT — Architectural Review Hardening |
| **Date** | March 2026 |
| **Tier** | Application / Product Layer |
| **Phase** | 1 (MVP demoable in ~3 months with explicit stubbing strategy) |
| **Authors** | Aaron Damiano / Claude |
| **Dependencies (corpus specs)** | HIRI Protocol v3.1.1, SHML v3.2, W2Fuel Core v1.3.1, SNP v1.3, BIBSS v1.3, SAS v2.0 (optional), OPA v1.2 (optional); references the-plot.md, ariadne-readme.md |

---

## Revision History

### v0.1.0 → v0.2.0

v0.2.0 closes six findings from the v0.1.0 architectural review. The architectural commitments (No-Data Invariant, Human-In-The-Loop Invariant, Pluralism Invariant) are unchanged; the revisions resolve operational paradoxes that would have blocked the MVP timeline or violated invariants under realistic usage.

| ID | Category | Change | Section |
|---|---|---|---|
| R-1 | Critical | **Schema-drift architectural answer.** Alignment claims are bound to *column-level* content addresses, not schema-level. New §5.4 (Schema Evolution and Alignment Inheritance) defines `InheritedAlignmentSuggestion` and the `BulkTrustPolicy` pattern. Resolves the v0.1.0 paradox where adding one column would have forced re-alignment of 199 unchanged columns. | §5.4 (new), §6.3 cross-ref |
| R-2 | Critical | **Phase 1 timeline made achievable.** Explicit stubbing strategy for SNP and BIBSS; full corpus-spec implementations deferred to v1.1. Phase 1 focuses on FSR-specific surface area (workbench, signing, publication, minimal planner). | §12 |
| R-3 | High | **Read-only query planner pulled into Phase 1.** A registry without a planner cannot demonstrate the value proposition in §1.1. Phase 1 includes a minimal single-scope read-only planner that answers "which sources have aligned to class X?" | §12, §7.4 (new) |
| R-4 | High | **Active Routing Profile** introduced. Resolves the UX paradox where strict pluralism would force every consumer query to enumerate belief scopes. The profile is itself a signed, volatile, supersedable claim — preserving the anti-Oracle stance while restoring usability. | §10.2 (new) |
| R-5 | High | **Column-name obfuscation mandated for Phase 1.** Optional client-side hashing of column names before upload, for high-sensitivity environments. Resolves FSR-OQ-02 with a Phase 1 deliverable rather than a Phase 2 deferral. | §2.4 (new) |
| R-6 | Medium | **`IntentionalIgnoreClaim` introduced.** Distinguishes neglected columns from system-metadata columns explicitly excluded from semantic interpretation. Resolves the "gap report drowned in technical boilerplate" risk. | §5.2 |

---

## ARIADNE Preamble

This specification defines the Federated Semantic Registry (FSR), an application-layer product that serves the ARIADNE thesis by ensuring:

1. **Epistemic honesty** — Alignments are claims with sources, confidence, and supersession lineage. No alignment is asserted as world-truth.
2. **Value pluralism** — Multiple alignments can coexist via SHML belief scopes. The system does not impose a single canonical interpretation; it tracks divergence.
3. **Auditability** — Every alignment claim is HIRI-signed, content-addressed, and traceable to a human author with a timestamp and a justification.
4. **Human override** — Alignment is a human act. The system records and publishes; it does not decide.

FSR is not an inference engine. It is a **publication and routing surface** over schema-to-ontology alignment claims authored by humans, optionally assisted by deterministic suggestion services. The tool does not store, copy, or process the underlying data described by the schemas it aligns.

---

## 0. Orientation

### 0.1 What FSR Is

FSR is a federated semantic metadata registry. It collects schema descriptors from source systems, accepts human-authored alignment claims mapping those schemas to canonical ontology classes, signs and publishes those claims as content-addressed artifacts, and exposes a query planner that tells consumers *which source systems they would need to query* to answer a given semantic question.

The product positioning is **"Schema Registry meets Ontology Workbench"** — distinct from data catalogs (which inventory data without semantic rigor) and from ontology editors (which model concepts without source-system binding).

### 0.2 What FSR Is Not

FSR does **not**:

- Store, ingest, mirror, or process the data described by the schemas it aligns
- Execute federated queries (it tells you where to query; it does not query)
- Resolve entity identity across sources (no A-Box, no entity merging)
- Author alignments autonomously (alignment is a human act; machine suggestions are SHOULD, never MUST)
- Mediate trust between source systems (it publishes signed claims; consumer trust policies are downstream)
- Maintain a single canonical ontology by authority (the canonical T-Box is one belief scope among many; customers may fork)

This is the **No-Data Invariant** (§2), the **Human-In-The-Loop Invariant** (§5.2), and the **Pluralism Invariant** (§10).

### 0.3 Document Scope

This specification defines:

- The No-Data Invariant and its operational implications, including Phase 1 column-name obfuscation
- The three-layer architecture (defers to SHML v3.2 for the model)
- The alignment workflow and its conformance requirements
- The schema evolution and alignment inheritance model
- The publication model (signed claims, retrieval patterns, supersession semantics)
- The query planner contract, including the Phase 1 minimal-planner scope
- The Active Routing Profile mechanism
- Adapter interfaces (schema source, ontology source, publication target)
- Non-claims explicitly disclaimed by the architecture

This specification does **not** define:

- The UI for the alignment workbench (product-design concern, separable)
- Pricing, packaging, or licensing
- Specific BFO/CCO concept mappings (those live in W2Fuel-hosted ontology modules)
- Customer-specific belief scopes (customer-owned)

### 0.4 Assumptions and Limits

FSR's correctness claims hold under the following assumptions. When an assumption fails, the corresponding architectural property is reduced or withdrawn.

#### 0.4.1 Assumed alignment authority

FSR assumes that the humans authoring alignment claims have legitimate authority to do so for the schemas they align. The system records *who* aligned *what* and *when*, but does not verify that the aligner had organizational authority to make the claim. Authority verification is a governance concern outside this specification.

#### 0.4.2 Assumed schema fidelity

FSR assumes that uploaded schemas faithfully represent the source system. Drift between the schema submitted to FSR and the schema actually in production at the source system is a deployment concern, not an FSR concern. Schema-versioning and freshness governance are deferred to the integration layer.

#### 0.4.3 Assumed cryptographic primitive integrity

Ed25519, SHA-256, and the HIRI canonicalization profiles are assumed to function as specified. Their compromise is out of scope.

#### 0.4.4 Assumed customer ontology governance

If a customer forks or extends the default canonical ontology, governance of that fork is the customer's responsibility. FSR tracks divergence; it does not adjudicate it.

#### 0.4.5 What this specification provides under the above assumptions

Given the assumptions above, FSR guarantees:

- Every published alignment claim is content-addressed, HIRI-signed, and traceable to its human author
- No customer data is ever transmitted to, stored in, or processed by FSR
- Multiple competing alignments for the same schema-to-ontology mapping coexist as separable belief scopes
- The Provenance Index supports deterministic query planning: given a semantic question, return the set of source schemas that have aligned claims matching the question's ontology terms
- Schema evolution does not force re-alignment of unchanged schema elements (§5.4)

---

## 1. Purpose

### 1.1 The Tool

An organization with N source systems (CRM, ERP, HRIS, EHR, regulatory filings, vendor data feeds, etc.) has N schemas, none of which share a common semantic model. The question "where do we hold information about Persons?" is unanswerable without inspecting each source. The question "what qualities do we track about Persons?" requires a human to read all N schemas and synthesize.

FSR transforms this problem. The customer uploads each source's schema. A domain expert aligns each schema's columns to canonical ontology classes (Person, Organization, Account, etc.). FSR signs and publishes the alignments. Downstream queries become:

> *"Which of my source systems have aligned to BFO:Person? What qualities have they aligned for Persons?"*

The answer is computable from the alignment claims alone, without touching any customer data.

### 1.2 Architectural Position

FSR sits at the application layer, consuming corpus services for its primitives:

```
┌─────────────────────────────────────────────────────────┐
│              Federated Semantic Registry                │
│  (alignment workbench + publication + query planner)    │
└────────────┬───────────────────────────────────┬────────┘
             │ uses                              │ publishes
             ▼                                   ▼
┌────────────────────────────┐    ┌─────────────────────────────┐
│  SNP → BIBSS → SAS → OPA   │    │   HIRI-signed claims        │
│  (schema processing)        │    │   addressable via CID       │
└────────────────────────────┘    │   retrievable by consumers  │
                                  └─────────────────────────────┘
             │ canonical ontology hosted by
             ▼
        W2Fuel Core
             │ three-layer model from
             ▼
          SHML v3.2
```

FSR does not invent new primitives. It composes existing corpus services into a vertical product.

---

## 2. The No-Data Invariant

### 2.1 What Never Lives in FSR

The following MUST NOT be transmitted to, stored in, cached by, or processed by any FSR component:

- Source system row data (the actual records described by the schemas)
- Sample data from source systems (even one row)
- Decrypted customer data of any kind
- Credentials or connection strings for source systems
- API tokens or other source-system access material

### 2.2 What Lives in FSR

The following MAY be stored, processed, and published by FSR:

- Schema descriptors: column names, types, structural relationships (the *shape* of source data, not its content)
- Source system identifiers and human-readable labels (e.g., "CRM-Production", not "https://crm.prod/api with token X")
- Canonical ontology modules hosted by W2Fuel
- Alignment claims (mappings from schema columns to ontology classes) with provenance
- Belief scope metadata (which alignments belong to which interpretive framework)
- Aggregated, non-PII metadata about alignment activity (counts, timing, authors at role level)

### 2.3 Conformance Test

A conformant FSR implementation MUST publish an auditable inventory of all data ingress paths, and each path MUST be demonstrable as schema-only. The "no data" promise is an invariant, not a policy. Implementations that cannot demonstrate this invariant on demand are non-conformant regardless of marketing claims.

This conformance requirement directly serves the Plot §2.1 *No Oracle Claims* commitment as sharpened in the 2026-05-15 normative note: FSR makes claims about *schema-to-ontology alignment*, not about the world described by the schemas.

### 2.4 Column-Name Obfuscation (Phase 1 Mandate)

Column names themselves can reveal sensitive information. The string `healthcare_incident_type_hiv` discloses a category and a sensitive attribute even when no row data accompanies it. The string `customer_default_risk_score` reveals a business practice. The No-Data Invariant alone does not protect against this metadata leak.

A Phase 1 conformant implementation MUST support **optional client-side column-name obfuscation**:

1. The customer's local agent computes a salted hash of each column name before upload using `HMAC-SHA256(orgSalt, columnName)`.
2. FSR receives and stores only the hashed identifier. The hash is content-addressable like any other column identifier; alignment claims target it.
3. The customer's local agent maintains the salt-to-name mapping locally. FSR never holds the mapping.
4. For display in the alignment workbench, the customer's local agent decodes hashed identifiers back to human-readable names *client-side* before rendering. FSR-server-side rendering never sees plaintext column names for obfuscated schemas.

Obfuscation is per-schema-element granularity: a customer MAY obfuscate only sensitive columns and leave operational metadata columns (`created_at`, `row_id`) in plaintext, or obfuscate everything.

**Conformance:** An FSR implementation that cannot demonstrate end-to-end obfuscated operation for at least one synthetic schema is non-conformant for high-sensitivity deployments (regulated healthcare, defense, financial compliance).

---

## 3. Three-Layer Architecture

FSR's data model is the SHML v3.2 three-layer architecture, applied to schema metadata rather than knowledge graph instances. The full model is defined in [SHML v3.2](SHML-v3.2.md); FSR's specialization is below.

### 3.1 Reality Layer

The canonical class hierarchy. Hosted by W2Fuel Core. BFO 2020 + CCO 2.0 + domain extensions provided by FSR's default ontology module or customer-defined extensions.

The Reality Layer makes no claims about specific customer schemas. It defines what kinds of things exist in the world that schemas might describe.

### 3.2 Middle Layer

The assertion event log. Each alignment claim, ignore claim, inheritance claim, profile claim, and supersession is a Middle Layer event. Each event records:

- The schema column or structure being aligned (as a *column-level* content-addressed reference; see §5.4)
- The Reality Layer class to which it is aligned (where applicable)
- The human author of the alignment
- The timestamp
- The belief scope under which the alignment is claimed
- The confidence (where machine-assisted)
- The justification text (free-form, recorded for audit)
- HIRI signature over the canonicalized claim

The Middle Layer is the **authoritative event log**. All Logic Layer publications derive from it. The Middle Layer is append-only; corrections take the form of new claims that supersede prior claims.

### 3.3 Logic Layer

Published projections of the Middle Layer, scoped to a belief context. A customer may publish:

- The "production" Logic Layer projection (the alignments currently active under the organization's primary belief scope)
- A "regulatory" projection (alignments active under a specific compliance interpretation)
- A "research" projection (alignments active under exploratory interpretations)

Multiple Logic Layer projections coexist over the same Middle Layer. Consumers select the projection appropriate to their use case, optionally via the Active Routing Profile (§10.2).

---

## 4. Component Dependencies

FSR composes the following corpus services. Each is referenced, not redefined.

| Component | Spec | Role in FSR |
|---|---|---|
| **HIRI Protocol** | [v3.1.1](HIRI-Protocol-Spec-v3.1.1.md) | Signs and content-addresses every alignment claim. Verification primitive — never trust authority. |
| **SHML** | [v3.2](SHML-v3.2.md) | Three-layer architecture (Reality/Middle/Logic). The Middle Layer assertion event model is FSR's core data structure. |
| **W2Fuel Core** | [v1.3.1](w2fuel-core-01-v1.3.1.md) | T-Box service. Hosts the canonical ontology and any customer forks. Provides class hierarchy queries to the alignment workbench. |
| **SNP** | [v1.3](snp-v1.3.md) | Format cleaning of uploaded schema descriptors. CSV/JSON schemas in, cleaned in same format out. Phase 1 may use a stub (§12). |
| **BIBSS** | [v1.3](BIBSS-V1.3-SPEC.md) | Structural inference. Produces the CISM (Canonical Internal Schema Model) for display in the alignment workbench. Phase 1 may use a stub (§12). |
| **SAS** | [v2.0](sas-v2.0.md) (standalone mode) | Optional, Phase 2+: surfaces machine-suggested alignments for human review. Standalone mode (static rules) is sufficient; Enriched mode (Fandaws-assisted) deferred. |
| **OPA** | [v1.2](opa-v1.2.md) | Optional, Phase 2+: in **recorder mode**, OPA produces the two-layer Universal/ConceptDesignation graph output from human-authorized alignment commits. Autonomous placement mode (Stages 1–6) is out of scope. |

FSR does **not** depend on:

- Fandaws (no A-Box — no instance data is ever held)
- OERS (no entity resolution — no instances to resolve)
- HQL / WEAVER (no query execution — only query planning)
- TagTeam (no natural-language source ingestion at MVP; schemas only)
- IEE, ARCHON, CPS, BAM, IS, SMS, AVS, NIS, SoMS, CTS (no moral architecture — FSR is purely epistemic infrastructure)

---

## 5. The Alignment Workflow

### 5.1 Collection

A customer uploads schema descriptors via one of the supported source adapter interfaces (§8.1). For each schema:

1. SNP (or its Phase 1 stub) cleans format-level artifacts (BOMs, currency strings, locale-specific dates). Pure function, no semantic interpretation.
2. BIBSS (or its Phase 1 stub) performs structural inference, producing a CISM. The CISM is displayed in the alignment workbench as the *source-side view*.
3. FSR canonicalizes each schema element (column or sub-structure) *independently* and assigns each its own content address. See §5.4.
4. FSR persists the schema descriptor and its constituent column descriptors in the Middle Layer as a `SchemaIngestEvent`. No row data, no samples, no credentials.

Re-uploading a schema in which most columns are unchanged produces the same content addresses for those unchanged columns and the same alignment bindings.

### 5.2 Alignment (Human-Driven)

A human aligner (typically a domain expert from the customer's organization) opens the alignment workbench. For each column or structural element in the CISM, the aligner takes one of three actions:

**Action A: Align**

1. Select a candidate Reality Layer class (from the canonical ontology or a customer-defined extension).
2. Optionally consult SAS-suggested alignments (Phase 2+). SAS standalone mode produces machine suggestions with confidence scores. The human MUST explicitly accept, modify, or reject each suggestion. SAS suggestions are SHOULD, never MUST. Auto-acceptance is forbidden.
3. Provide justification (free-form text recording why this alignment is appropriate).
4. Commit. FSR canonicalizes the claim, signs it with the aligner's HIRI authority, assigns a content address, and writes a `SchemaAlignmentClaim` event to the Middle Layer.

**Action B: Intentionally Ignore**

Some columns are operationally meaningful but semantically uninteresting: `created_at`, `updated_at`, `row_id`, `version_number`, soft-delete flags, audit trail columns. Aligning them to BFO classes would be either trivial (`bfo:TemporalRegion` for every timestamp) or noisy. The aligner MAY mark a column with an `IntentionalIgnoreClaim`:

1. Select the column.
2. Provide a reason category: `system_metadata`, `audit_trail`, `transport_only`, `deprecated`, or `other` (with free-form justification).
3. Commit. FSR writes an `IntentionalIgnoreClaim` event to the Middle Layer, HIRI-signed, content-addressed.

`IntentionalIgnoreClaim` is a first-class claim type. It is distinct from "not yet aligned" — the gap report (§7.3) explicitly separates the two. A column marked `IntentionallyIgnored` does not appear in alignment-gap reports; an unmarked, unaligned column does.

**Action C: Leave Unaligned (Deferred)**

The aligner MAY leave columns without any claim at all. These appear in alignment-gap reports as `unmarked_pending`. They are first-class: the publication MUST disclose them as gaps, not silently omit them.

---

This workflow is the **Human-In-The-Loop Invariant**. No alignment, ignore, or inheritance claim enters the Middle Layer without a HIRI signature from a human author. Machine-only commits are forbidden.

### 5.3 Publication

A claim becomes part of a Logic Layer projection when the customer publishes a belief scope. Publication is:

1. **Explicit** — a customer action, not automatic.
2. **Versioned** — each publication is a content-addressed snapshot of the projection.
3. **Signed** — the publication itself is HIRI-signed by the publishing authority (typically a role identity, not an individual aligner).
4. **Retractable via supersession** — a published claim is never deleted; a superseding claim is added and the projection is republished.

### 5.4 Schema Evolution and Alignment Inheritance

Schemas drift continuously. A production database may add a tracking column weekly. A new field appears in an API response. A column type widens. Without an architectural answer to schema evolution, the No-Data Invariant becomes irrelevant because no human aligner will keep up.

FSR's answer rests on **column-level content addressing** plus **machine-suggested inheritance with human commit**.

#### 5.4.1 Column-Level Content Addressing

Each schema element (column, nested structure) has its own canonical representation and its own content address, computed independently of the containing schema descriptor. The canonical form of a column includes:

- The column name (or its obfuscated hash, per §2.4)
- The column type as inferred by BIBSS
- The column's structural position only insofar as required for disambiguation of identically-named columns at different nesting levels
- The column's null/required status as inferred by BIBSS

The canonical form does **not** include:

- The containing schema descriptor's identity (so unrelated changes elsewhere do not perturb this column's CID)
- The column's row count, value distribution, or any sample
- The column's ordinal position within the schema (so column reordering does not perturb the CID)

**Consequence:** Adding a new column to a schema does not change the content addresses of the existing columns. Their alignment claims remain valid by content-address binding. No human action is required.

The schema descriptor itself is a *containing reference* that points to a set of column CIDs. The schema descriptor's CID changes when the set of contained column CIDs changes, but the column CIDs and their alignment bindings are stable.

#### 5.4.2 Inherited Alignment Suggestions

When a column's canonical form *does* change (rename, type change, structural reorganization), its content address changes. The previously-bound alignment is now bound to the old (no-longer-present) column CID.

FSR detects this on ingest and produces an `InheritedAlignmentSuggestion`:

```json
{
  "@type": "fsr:InheritedAlignmentSuggestion",
  "fsr:newColumnCid": "cid:abc...",
  "fsr:priorColumnCid": "cid:xyz...",
  "fsr:priorAlignmentCid": "cid:def...",
  "fsr:similarityBasis": "structural_match | name_similarity | position_match | bibss_type_match",
  "fsr:confidence": 0.87,
  "fsr:generatedBy": "fsr:inheritance-suggester-v1"
}
```

`InheritedAlignmentSuggestion` is a machine-generated suggestion, *not a claim*. It does not enter the Logic Layer projection. It surfaces in the alignment workbench for human action. The aligner MUST explicitly accept, modify, or reject the suggestion. Accepting produces a new `SchemaAlignmentClaim` for the new column CID, with a `fsr:derivedFrom` reference to the prior alignment for audit trail continuity.

This preserves the Human-In-The-Loop Invariant: every claim still carries a human signature. The system has made the human's job a confirmation rather than a fresh authoring decision, but the human's role remains constitutive.

#### 5.4.3 Inheritance Across Renames

When a column is *renamed* (e.g., `cust_id` → `customer_id`), structural matching may detect the link even though CIDs differ. The aligner MAY explicitly invoke an `InheritanceAcrossRename` workflow:

1. The aligner identifies the rename by pointing to the prior column.
2. FSR generates an `InheritedAlignmentSuggestion` with `similarityBasis: rename_by_aligner_assertion`.
3. The aligner confirms; a new `SchemaAlignmentClaim` is committed.

The rename assertion is itself a claim: it records that *this aligner asserted* that these two columns refer to the same conceptual thing. Disputed renames produce supersession chains in the normal way.

#### 5.4.4 Bulk Trust Policy

For organizations with high schema-change velocity, individual confirmation of every `InheritedAlignmentSuggestion` is operationally infeasible. FSR adopts the **Bulk Trust Policy** pattern from [Fandaws Type Agent §17](fandaws-type-agent-v2.3.md):

A customer MAY configure a `BulkTrustPolicy` claim that authorizes automatic acceptance of `InheritedAlignmentSuggestion`s above a configurable confidence threshold, subject to two constraints:

1. **Each auto-accepted claim carries `fsr:pendingReview: true`**. The flag is cleared only by individual human review.
2. **Claims with `pendingReview: true` do NOT contribute to the Active Routing Profile (§10.2) by default.** Only individually-reviewed claims contribute to default routing. Bulk-accepted claims are visible to consumers who explicitly opt into them via belief scope selection.

The `BulkTrustPolicy` claim is itself HIRI-signed by an organizational role authority. The policy is auditable, revisable, and revocable. Adopting a bulk-trust workflow is an organizational decision recorded as a first-class claim, not a system-level default.

This pattern preserves Human-In-The-Loop in spirit: the human signature on the BulkTrustPolicy IS a meta-signature authorizing the auto-acceptances under stated conditions. The trade-off is explicit, the audit trail is complete, and the default routing profile remains conservative.

---

## 6. Publication Model

### 6.1 Signed Alignment Claims

Every published alignment claim is a HIRI-signed artifact. The signature attests:

- Who authored the alignment (HIRI authority)
- When the alignment was committed (timestamp)
- What schema element was aligned (column-level content-addressed reference)
- What Reality Layer class was selected (content-addressed reference)
- Under what belief scope (content-addressed reference)
- Whether the claim was inherited from a prior alignment, and if so, the prior claim's CID (§5.4)

A consumer verifying an FSR publication MUST be able to:

1. Verify the signature without contacting FSR
2. Retrieve the schema descriptor and ontology module by content address
3. Reconstruct the alignment justification text
4. Walk the supersession chain to determine the active claim under any past or present projection
5. Walk the `derivedFrom` inheritance chain to trace the alignment back to its originally-authored ancestor

### 6.2 Retrieval Patterns

FSR supports four retrieval patterns. Implementations MUST support at least patterns (a) and (b); patterns (c) and (d) are RECOMMENDED.

| Pattern | Description | Use Case |
|---|---|---|
| (a) **Pull by CID** | Consumer fetches a specific alignment claim by content address | Verification, citation, audit trail reconstruction |
| (b) **Pull by query** | Consumer queries a registry endpoint: "all claims for schema X under belief scope Y" | Operational integration, ETL configuration |
| (c) **Push via webhook** | FSR notifies registered consumers when a Logic Layer publication changes | Live integration, change propagation |
| (d) **Subscribe via feed** | Consumer subscribes to a change feed for a belief scope | Continuous integration, anomaly detection |

All retrieval patterns return signed artifacts. A consumer MUST NOT trust an unsigned response, regardless of transport.

### 6.3 Update Semantics

Alignment claims are immutable. Updates take three forms:

1. **Supersession** — a new claim explicitly supersedes a prior claim. The prior claim remains in the Middle Layer and Logic Layer history; only the active projection reflects the supersession.
2. **Annotation** — a new claim references and qualifies a prior claim without superseding it (e.g., "this alignment is correct but only under temporal scope T").
3. **Withdrawal** — a new claim records that the prior claim should not be considered active. Withdrawal is itself a claim with a HIRI signature.

There is no "delete" operation. The Middle Layer is append-only by architectural commitment.

Schema-evolution-driven updates use the `derivedFrom` mechanism from §5.4, which is *additive* (a new claim for a new column CID) rather than superseding (a new claim that replaces a prior claim for the same CID). Both flows coexist.

### 6.4 Supersession Chains

A consumer querying for the "current alignment" of a schema element under a belief scope receives the latest non-superseded, non-withdrawn claim. Supersession chains are linear within a belief scope but may diverge across belief scopes.

A conformant implementation MUST expose the full supersession chain on request. Hiding superseded claims is forbidden by the Plot §2.3 *Auditability* commitment.

---

## 7. Query Planner

### 7.1 The "Where Does the Answer Live" Question

Consumers do not ask FSR for data. They ask FSR for *routing*. The canonical query forms are:

| Query | FSR Returns |
|---|---|
| "Which source systems have aligned to `bfo:Person`?" | List of source schemas with at least one alignment to `bfo:Person` or its subclasses, with content addresses for each alignment |
| "What qualities are aligned for `bfo:Person` across my sources?" | Set of Reality Layer classes aligned as qualities of `bfo:Person`, grouped by source schema |
| "What source schemas are aligned under belief scope X?" | List of schemas with at least one alignment in the named belief scope |
| "What schema elements are unaligned in source Y?" | List of CISM nodes in source Y's schema that have no alignment claim and no `IntentionalIgnoreClaim` |

### 7.2 Implementation

The query planner is a thin layer over the SHML Provenance Index (Subcomponent 2 of the SHML Middle Layer). For each alignment claim, the Provenance Index records:

- Source schema (content address)
- Column-level reference (content address)
- Reality Layer class (content address)
- Belief scope (content address)
- Author authority (HIRI authority)
- Active status (whether superseded or withdrawn)
- `pendingReview` flag (from §5.4 BulkTrustPolicy)

Query planning is deterministic graph traversal over the Provenance Index. The planner does not infer; it reports.

### 7.3 The Distinguishing Feature

Most data catalog products tell consumers what data they have. FSR also tells them what they are **missing** — which sources have not been aligned, which Reality Layer classes have no aligned sources, where the canonical ontology has been extended without being mapped. This honest gap reporting is a feature, not a defect, and follows the Plot's *Uncertainty Visible* commitment.

The gap report distinguishes:

- **`unmarked_pending`**: columns with no alignment and no ignore claim — true semantic gaps
- **`intentionally_ignored`**: columns explicitly marked under §5.2 Action B — excluded from gap reports by default but available on opt-in
- **`pending_review`**: columns with bulk-trust-accepted alignments awaiting individual review — excluded from default routing but visible in gap reports as a separate category

### 7.4 Phase 1 Read-Only Single-Scope Planner

To prove the value proposition in §1.1 within the Phase 1 MVP, the following minimal planner is in scope for Phase 1:

| Query | Phase 1 Support |
|---|---|
| "Which source systems have aligned to class C?" | **YES** — graph traversal over the Provenance Index, single-scope (the customer's default profile) |
| "What classes are aligned in schema S?" | **YES** — inverse traversal |
| "What columns in schema S are unaligned?" | **YES** — gap report against the schema's CISM |
| Multi-scope queries enumerating belief scope variations | Deferred to Phase 2 |
| Cross-customer or federated queries | Deferred to Phase 3 |
| Push/webhook retrieval | Deferred to Phase 2 |

Phase 1's planner answers the questions used to justify FSR's existence (§1.1). It does so under a single belief scope (the Active Routing Profile default, §10.2). Multi-scope routing UI is a Phase 2 enrichment.

---

## 8. Adapter Interfaces

Per ARIADNE Pattern 3 (*Pluggable Doesn't Mean Unowned*), every adapter has a contract, a default, conformance tests, and a named owner.

### 8.1 Schema Source Adapter

**Contract:** Accepts a schema descriptor in some external format and produces a normalized schema document compatible with SNP input.

**Default:** A CSV / JSON upload adapter implemented within FSR. Accepts files via HTTP POST or local filesystem. The default adapter MUST also support the optional client-side column-name obfuscation pipeline defined in §2.4.

**Conformance:** MUST never transmit, request, or accept row data. MUST verify schema-only ingest via a publicly auditable check. MUST support obfuscated and non-obfuscated upload paths.

**Owner:** FSR product team.

**Extensions (community-owned):** JDBC introspection adapter, Avro adapter, Protocol Buffers adapter, GraphQL introspection adapter, OpenAPI adapter, dbt manifest adapter. Each extension MUST satisfy the same no-data conformance test.

### 8.2 Ontology Source Adapter

**Contract:** Accepts an ontology module (OWL, JSON-LD, or W2Fuel-native) and registers it as a Reality Layer source available to the alignment workbench.

**Default:** A BFO 2020 + CCO 2.0 starter ontology shipped with FSR, hosted via W2Fuel.

**Conformance:** MUST sign all registered ontology modules with HIRI authority. MUST track customer-authored extensions as separate belief scopes from the FSR-shipped default.

**Owner:** FSR product team for the default; customer ontology stewards for forks.

### 8.3 Publication Adapter

**Contract:** Accepts a Logic Layer projection snapshot and publishes it via a transport mechanism.

**Default:** HTTP registry endpoint with pull-by-CID and pull-by-query support.

**Conformance:** MUST publish only signed claims. MUST expose supersession chains on request. MUST NOT modify claim content during transport.

**Owner:** FSR product team for the default; consumer infrastructure teams for custom transports (IPFS gateway, message queue, webhook receiver, etc.).

---

## 9. Non-Claims

Per ARIADNE Pattern 4 (*Non-Claims Enumeration*), the following are explicit non-claims:

1. **Signed alignments do not make alignments true.** A signature attests *that* someone authored the alignment; not that the alignment is correct. Correctness is a community judgment, expressed through supersession and dispute.

2. **The canonical ontology is not the canonical ontology.** It is *one* belief scope shipped as a default. Customers MAY fork. Multiple canonical ontologies coexist; FSR tracks the divergence rather than imposing convergence.

3. **Machine-suggested alignments are not pre-approved.** SAS standalone mode and `InheritedAlignmentSuggestion` produce suggestions for human review. Auto-acceptance is forbidden outside of the explicit `BulkTrustPolicy` workflow (§5.4.4), and even there, auto-accepted claims carry `pendingReview: true` and do not contribute to default routing.

4. **A query planner result is not an answer.** It is a routing recommendation. The consumer must still query the named source systems and reconcile the results. FSR does not execute the queries it plans.

5. **The Provenance Index is not a knowledge graph.** It is a metadata index over alignment claims. It records *what was aligned*, not *what the data says*. Consumers tempted to use the Provenance Index as a pseudo-A-Box are reading the system wrong.

6. **Schema fidelity is not architecturally enforced.** FSR records what schemas customers upload; it does not verify that those schemas reflect production reality. Schema-drift detection is downstream.

7. **The "no data" invariant is not a privacy compliance attestation.** It is an architectural commitment that reduces the surface area where compliance applies. Customers remain responsible for compliance of their source systems under the regulatory regimes that govern them.

8. **Publication is not endorsement.** FSR publishes alignment claims authored by customers under their own authority. A claim's publication via FSR does not imply that FSR's vendor endorses the claim's substance.

9. **The Active Routing Profile (§10.2) is not the canonical answer.** It is *one* customer-designated default for routing convenience. A profile claim is itself a claim — auditable, supersedable, and overrideable by consumers who specify a different belief scope. The profile pointer does not collapse pluralism; it provides a convenient default.

10. **An `IntentionalIgnoreClaim` does not assert that a column is unimportant.** It asserts that the column is excluded from *semantic* alignment under the current understanding. The column may still be operationally critical; the claim simply records the aligner's judgment that no Reality Layer class is the appropriate mapping.

---

## 10. Pluralism and Belief Scopes

### 10.1 The Architectural Commitment

The most consequential architectural commitment in FSR is that **multiple legitimate alignments can coexist**. Two domain experts in the same organization may disagree about whether an `emp_id` column aligns to `bfo:Person` or to `cco:EmployeeRole`. A regulatory body may require alignment X while an analyst's preferred interpretation requires alignment Y.

FSR represents this directly via SHML belief scopes:

- Each belief scope is a named, signed, immutable interpretive framework.
- An alignment claim is always made *under* a belief scope.
- Multiple belief scopes may coexist over the same Middle Layer events.
- Logic Layer projections are belief-scope-specific.

The product MUST surface belief scope as a first-class concern in the API and in administrator-facing UI. Hiding belief scope in service of "simpler" UX would silently collapse the pluralism that the architecture exists to preserve.

### 10.2 Active Routing Profile

Strict pluralism creates a UX failure mode: every consumer query forced to enumerate belief scope variations before resolving even a simple routing question. The Active Routing Profile resolves this without sacrificing the architectural commitment.

An organization MAY designate one or more `ActiveRoutingProfile` claims. Each profile is:

- A first-class HIRI-signed claim authored by an organizational role authority
- A binding from a named context (e.g., `"default"`, `"regulatory"`, `"operational"`) to a specific belief scope
- Itself versioned and supersedable; profile changes produce supersession events in the normal way
- Auditable: every prior version of the profile remains in the Middle Layer

**Semantics of API queries:**

| Consumer request | FSR returns |
|---|---|
| Query with no scope specified | Routing under the `"default"` Active Routing Profile, with the profile CID returned alongside the result |
| Query specifying scope `S` | Routing under scope `S` directly; the profile is bypassed |
| Query for "all available scopes" | List of all belief scopes with at least one published projection |
| Query for "current profile bindings" | The full set of `ActiveRoutingProfile` claims and their belief-scope targets |

**Why this is not an Oracle Claim:**

The Active Routing Profile is a claim about *which scope the organization has currently designated as its default routing context* — not a claim about the world. The system is asserting:

> *"The organizational role authority `Customer-Admin` has, as of timestamp T, designated belief scope `B` as the routing default for context `default`. This claim is HIRI-signed and will remain active until superseded."*

This satisfies the Plot §2.1 chain (content-address → claim → validation → truth-policy → active-state) without breaking any link. The profile *is* the truth-policy decision, recorded as a claim with provenance, revisable on demand.

A consumer that wants strict pluralism opts in: explicit scope enumeration is always available, the profile is never imposed.

**UI requirement (Phase 1):**

The administrator UI MUST surface the Active Routing Profile as an explicit, named, editable setting. Consumers MUST be able to inspect the current profile via API. Hiding the profile or making it opaque is forbidden.

---

## 11. Conformance

A conformant FSR implementation MUST satisfy the following invariants. Conformance test vectors are deferred to a future Test Vectors appendix.

| ID | Invariant | Source |
|---|---|---|
| FSR-INV-01 | No customer row data is transmitted to, stored in, or processed by any FSR component | §2 |
| FSR-INV-02 | Every alignment claim is HIRI-signed by a human author (directly or via a Bulk Trust Policy meta-signature) | §5.2, §5.4.4 |
| FSR-INV-03 | Machine suggestions are SHOULD-level; auto-acceptance outside an explicit Bulk Trust Policy is forbidden | §5.2 |
| FSR-INV-04 | Alignment claims are append-only; updates take supersession, annotation, or withdrawal form | §6.3 |
| FSR-INV-05 | Supersession chains MUST be exposed on request | §6.4 |
| FSR-INV-06 | The Provenance Index is queryable; query planning returns routing, not data | §7.2 |
| FSR-INV-07 | Multiple belief scopes coexist; belief scope is surfaced in UI and API | §10 |
| FSR-INV-08 | All adapters MUST satisfy the no-data conformance test | §8.1 |
| FSR-INV-09 | Unaligned schema elements are disclosed, not hidden; gap report distinguishes `unmarked_pending`, `intentionally_ignored`, and `pending_review` | §5.2, §7.3 |
| FSR-INV-10 | Publication is explicit, customer-triggered, and reversible via supersession | §5.3 |
| FSR-INV-11 | Schema elements are content-addressed at column granularity; unchanged columns retain their CIDs across schema-descriptor changes | §5.4.1 |
| FSR-INV-12 | `InheritedAlignmentSuggestion` is machine-generated; it does not enter Logic Layer publication without a human commit (direct or via Bulk Trust Policy) | §5.4.2 |
| FSR-INV-13 | `BulkTrustPolicy` auto-accepted claims carry `pendingReview: true` and do not contribute to default routing | §5.4.4 |
| FSR-INV-14 | Column-name obfuscation MUST be supported in Phase 1; obfuscated names are stored only as salted hashes | §2.4 |
| FSR-INV-15 | The Active Routing Profile is itself a HIRI-signed, supersedable claim; consumers MAY override it by explicit scope selection | §10.2 |
| FSR-INV-16 | `IntentionalIgnoreClaim` is a distinct claim type; ignored columns are excluded from `unmarked_pending` gap reports | §5.2 |

---

## 12. Build Phases

### Phase 1: Stubbed-Boundary MVP (~3 months)

**Goal:** Single-source schema alignment with publication AND minimal query planning, demoable end-to-end.

The Phase 1 build budgets engineering effort to the FSR-specific surface area: workbench UX, claim signing, publication endpoint, profile management, and the minimal planner. Upstream corpus services (SNP, BIBSS) are *stubbed* — minimal implementations sufficient to feed the alignment workbench, with full corpus-spec compliance deferred to v1.1.

**Stubbing strategy:**

| Corpus dependency | Phase 1 Stub | Phase 1.1 Replacement Plan |
|---|---|---|
| **SNP v1.3** | Minimal CSV/JSON parser. Strips BOM, normalizes line endings. Does not implement full ECVE Appendix A.6/A.7 patterns. | Full SNP v1.3 implementation when ECVE dependencies are available. |
| **BIBSS v1.3** | Minimal column-type detection: string/integer/number/boolean/date/null. Per-column distribution counts. Does not implement full property-merge or three-tier kind/type classification. | Full BIBSS v1.3 implementation. |
| **W2Fuel Core v1.3.1** | Read-only hosting of a small BFO 2020 + CCO 2.0 starter ontology (~50 classes). No customer fork support. No T-Box update protocol. | Full W2Fuel implementation with adapter contracts. |

**FSR-specific Phase 1 builds (full implementation, not stubbed):**

- Alignment workbench UI (column display, class selection, justification field, IntentionalIgnore action, commit button)
- HIRI signing integration for all five claim types: `SchemaIngestEvent`, `SchemaAlignmentClaim`, `IntentionalIgnoreClaim`, `ActiveRoutingProfile`, supersession
- Column-level content addressing per §5.4.1
- Inherited Alignment Suggestion engine (structural match only at Phase 1; name-similarity and BIBSS-type-match deferred to Phase 2)
- Bulk Trust Policy claim definition and enforcement of `pendingReview` flag semantics
- Logic Layer publication endpoint with pull-by-CID and pull-by-query
- Active Routing Profile administration (one default profile per customer)
- Read-only single-scope query planner (§7.4)
- Optional client-side column-name obfuscation (§2.4)
- Gap report distinguishing `unmarked_pending`, `intentionally_ignored`, `pending_review`

**Out of scope for Phase 1:** SAS suggestions, OPA recorder mode, multi-scope query enumeration UI, push/webhook retrieval, customer ontology forks, federated queries.

**Conformance for Phase 1:** Invariants FSR-INV-01 through FSR-INV-16 MUST all hold at Phase 1, even where upstream services are stubbed. Invariants are about *FSR's behavior*, not about upstream-service feature completeness.

### Phase 2: Federation + Suggestions (~3 additional months)

**Goal:** Multi-source schema federation with machine-assisted alignment.

**Builds:**

- Full SNP v1.3 implementation
- Full BIBSS v1.3 implementation
- SAS v2.0 standalone mode (machine alignment suggestions)
- OPA v1.2 in recorder mode (two-layer Universal/ConceptDesignation output)
- Multi-scope query enumeration UI
- Webhook publication adapter
- Inherited Alignment Suggestion enrichment (name-similarity, BIBSS-type-match, position-match heuristics)

### Phase 3: Enrichment and Scale (~6+ months)

**Goal:** Customer ontology forks, advanced retrieval, change feeds.

**Builds:**

- Customer ontology fork and merge tooling (W2Fuel extension)
- Subscribe-via-feed retrieval pattern
- Cross-customer alignment patterns (with explicit privacy guarantees)
- SAS Enriched mode (requires Fandaws unblocked)

---

## 13. Open Questions

| ID | Question | Status | Resolution |
|---|---|---|---|
| FSR-OQ-01 | How does FSR handle schema versioning when source systems evolve? | **RESOLVED in v0.2** | §5.4 — column-level content addressing + InheritedAlignmentSuggestion + Bulk Trust Policy |
| FSR-OQ-02 | What is the privacy story for column *names* that themselves reveal sensitive information? | **RESOLVED in v0.2** | §2.4 — optional client-side obfuscation mandated for Phase 1 |
| FSR-OQ-03 | How are role identities distinguished from individual identities? | Open | Adopt HIRI Digital Passport v1.9.0 patterns; alignment claims signed by role authority, role membership tracked by customer IAM |
| FSR-OQ-04 | What is the legal and contractual status of published alignment claims? | Open | Out of architectural scope; product/legal concern |
| FSR-OQ-05 | How do customer ontology forks interact with FSR-shipped ontology version upgrades? | Open | Likely: customer fork pins its parent version; upgrades are explicit. Defer to Phase 3 |
| FSR-OQ-06 | Should the Provenance Index support cross-customer queries? | Open | Out of Phase 1-2 scope. Phase 3 may explore federated registries |
| FSR-OQ-07 | What is the conformance test for the No-Data Invariant? | Open | Phase 1 deliverable: publicly-auditable data-ingress inventory + automated test suite that exercises every ingress path with synthetic data and verifies no row content is retained |
| FSR-OQ-08 | How are `InheritedAlignmentSuggestion` confidence thresholds calibrated? | Open | Likely: organizational policy parameter on the BulkTrustPolicy claim, with default conservative threshold (e.g., 0.95) |

---

## Appendix A: Mapping to ARIADNE Process Patterns

| Pattern | Where Used |
|---|---|
| ARIADNE Preamble (Pattern 1) | Top of this document, binding to four commitments |
| Assumptions and Limits (Pattern 2) | §0.4 |
| Pluggable Doesn't Mean Unowned (Pattern 3) | §8 |
| Non-Claims Enumeration (Pattern 4) | §9 |

---

## Appendix B: Plot-Alignment Verification

A spec is in plot when each non-negotiable can be evidenced. FSR's evidence:

| Commitment | Evidence in FSR |
|---|---|
| No Oracle Claims | §6.1 (claims, not truths); §10.2 (Active Routing Profile as claim, not oracle); §9 non-claims 1, 4, 9 |
| Provenance Always | §6.1 (every claim signed); §5.2 (author, timestamp, justification mandatory); §5.4 (derivedFrom inheritance chain) |
| Uncertainty Visible | §5.2 (machine confidence surfaced); §7.3 (gap reporting with three categories); §13 (open questions) |
| Speculation Firewalled | N/A — FSR has no inference chain to taint |
| No Final Ethics | N/A — FSR is not a moral agent |
| Guardian Not Sovereign | §5.2 Human-In-The-Loop Invariant; §5.4.4 Bulk Trust as explicit human meta-signature; §9 non-claim 3 |
| Moral Injury Real | N/A — FSR is not a moral agent |
| Pluralism Respected | §10.1 belief scopes as first-class; §10.2 Active Routing Profile preserves both default UX and scope override; §9 non-claim 2, 9 |
| Auditability | §6.4 supersession chain exposure mandatory; §7.2 deterministic planner; §5.4 derivedFrom chain |
| Decidability | §7.2 query planning is graph traversal, not inference; terminates |
| Separation of Concerns | §3 Reality / Middle / Logic; §5.4.1 column-level vs schema-level addressing; §9 non-claims 4, 5 |
| Human Override | §5.2; §5.4.4; alignment is a human act by architectural commitment |
| Safety Floor Principle | N/A — FSR has no safety-critical layer |

---

## Appendix C: Phase 1 Timeline Sanity Check

The v0.1 critique correctly identified that "implement SNP + BIBSS + W2Fuel + alignment workbench in 90 days" was an illusion. v0.2's response:

| Phase 1 Effort | Sized For |
|---|---|
| Stubbed SNP (CSV/JSON parsing only) | ~1 week (one engineer) |
| Stubbed BIBSS (basic type detection only) | ~2 weeks (one engineer) |
| Starter ontology loaded into W2Fuel-stub | ~1 week (one engineer + one ontologist) |
| Column-level canonicalization and CID assignment | ~2 weeks |
| Alignment workbench UI | ~4-6 weeks (one full-time UI engineer) |
| HIRI signing integration | ~2 weeks (leverages existing HIRI Protocol implementation) |
| Logic Layer publication endpoint | ~2 weeks |
| Bulk Trust Policy + pendingReview semantics | ~1 week |
| InheritedAlignmentSuggestion (structural match only) | ~2 weeks |
| Active Routing Profile administration | ~1 week |
| Read-only single-scope planner | ~2 weeks |
| Optional column-name obfuscation pipeline | ~1 week (client-side library + server-side hash storage) |
| Gap report (three categories) | ~1 week |
| **Total (with parallelism)** | **~10-12 weeks for ~2-3 engineers + 1 ontologist + 1 designer** |

This is a credible 3-month MVP scope for a small product team. The stubbing strategy is the load-bearing element: building real SNP and real BIBSS in parallel with the workbench would not fit.

---

*End of Federated Semantic Registry Specification v0.2 · FNSR Application Layer · Ontology of Freedom Initiative*
