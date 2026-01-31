# Architecture Specification v1.1

**Spec-Driven Service Discovery, Conformance, and Topology Audit**

**Status:** Draft
**Version:** 1.1
**Supersedes:** v1.0
**Audience:** Architecture, Platform Engineering, Knowledge Engineering
**Primary Goal:** Enable machine-assisted verification that all architecturally required services exist, conform, and integrate correctly within a repository.

---

## ARIADNE Alignment

This spec operationalizes two risks from The Plot §6 (Risk Register):
- **Specification Drift** — "Components evolve inconsistently"
- **Complexity Overwhelm** — "Too many specs to keep aligned"

It provides **machine-assisted tooling** for the manual coherence work currently performed by the ARIADNE review process. Specifically:

| Spec-Driven Concept | ARIADNE Equivalent | Relationship |
|---------------------|-------------------|-------------|
| Drift Audit (§7) | ARIADNE Checks 3–4 (Tension Consistency, Cross-Spec Consistency) | Automates detection; ARIADNE provides the evaluation criteria |
| New Service Proposal (§8) | ARIADNE Round 6 (Fill Specification Gaps) | Automates discovery; ARIADNE provides the review process |
| Topology Analysis (§9) | Integration Spec §4.2 (Event Registry) | Extends the registry with graph reasoning and visualization |
| Service Registry (§3) | spec-index.md + Integration Spec §4.2 | Structured machine-readable complement to existing human-readable indexes |

**Constraint:** This spec governs *discovery and audit tooling*. It does NOT replace the ARIADNE 7-check validation process, which evaluates philosophical alignment, non-negotiable preservation, and tension consistency — dimensions that require human judgment.

**Existing Baseline:** The FNSR Integration Spec §4.2 already defines 15 services with event contracts. The Plot §4 maps all components to thesis contributions. These are the authoritative baselines that this audit system reconciles against.

---

## 1. Purpose and Scope

This specification defines a **spec-driven architectural audit system** that reconciles:

* **Unstructured human-authored specifications (Markdown)**
* **Structured service registry artifacts (`service.yaml`)**

The system does **not** treat agents as autonomous builders. Instead, it treats them as **state reconciliation engines** that:

1. Extract implied architectural intent from specs
2. Resolve that intent against a canonical service registry
3. Detect omissions, drift, and contradictions
4. Produce actionable artifacts for human review

This spec governs:

* Service identity resolution
* Service conformance auditing
* Inter-service topology verification
* Machine-first generation of architectural artifacts

It explicitly **does not** govern:

* Runtime orchestration
* Implementation details
* Programming language or framework choices

---

## 2. Design Principles

### 2.1 Spec as Source of Truth

Markdown specifications are the **authoritative expression of architectural intent**.
Registry artifacts (`service.yaml`) are **compiled outputs**, not primary sources.

### 2.2 Machine-First, Human-Governed

Machines:

* Extract
* Compare
* Propose
* Visualize

Humans:

* Review
* Approve
* Merge

### 2.3 Identity Before Existence

A service **exists** only if it can be **semantically resolved** to a canonical identity.
Folder presence alone is insufficient.

### 2.4 Topology Over Enumeration

Services are defined by:

* What they consume
* What they produce
* Who they interact with

Isolated services are treated as architectural smells.

---

## 3. Canonical Service Contract (`service.yaml`)

### 3.1 Required Structure

All services **MUST** be represented by a `service.yaml` adhering to the following schema.

```yaml
apiVersion: architecture.io/v1
kind: Service

metadata:
  name: Abductive Elicitation Service
  id: aes-core-01        # Stable, immutable identifier
  aliases:
    - AES
    - Detective
    - Abduction Engine

spec:
  status: active         # active | draft | deprecated | proposed
  tier: 1                # Architectural criticality

  interfaces:
    consumed:
      - name: DeductionFailed
        source: mdre
    produced:
      - name: StructuredQueryObject
        target: orchestration

  responsibilities:
    - Identify minimal missing predicates
    - Enforce bounded abductive search
```

### 3.2 Rationale

This structure enables:

| Problem          | Resolution                               |
| ---------------- | ---------------------------------------- |
| Naming ambiguity | `aliases` + stable `id`                  |
| Drift detection  | Explicit responsibilities and interfaces |
| Graph reasoning  | Declared producers and consumers         |

---

## 4. Architecture Audit Pipeline

### 4.1 High-Level Flow

```
Spec → Service Extraction → Identity Resolution
     → Existence Check
        → NEW → Draft Proposal
        → EXISTING → Drift Audit
     → Topology Analysis
     → Reports & Visualizations
```

---

## 5. Spec Parsing and Service Extraction

### 5.1 Extraction Criteria

A **service candidate** is any construct in a spec that:

* Performs non-trivial processing
* Accepts defined inputs
* Produces defined outputs
* Has bounded responsibilities

Excluded:

* UI components
* Passive data schemas
* Libraries without behavior

### 5.2 Extraction Output (Intermediate)

```json
{
  "service_name": "The Ingestor",
  "location": "Ingestion Spec §2.1",
  "responsibilities": ["Normalize inbound payloads"],
  "implied_inputs": ["RawEvent"],
  "implied_outputs": ["NormalizedEvent"]
}
```

---

## 6. Identity Resolution (Solving the Naming Problem)

### 6.1 Canonical Registry Load

At runtime, the audit tool **MUST** load all existing services into a registry.

**Baseline sources (in priority order):**

1. **FNSR Integration Spec §4.2** — Authoritative service event contracts (15+ services with consume/produce declarations)
2. **The Plot §4** — Component-to-thesis mapping (defines *why* each service exists)
3. **spec-index.md** — Review status and version tracking
4. **`service.yaml` files** (when they exist) — Structured machine-readable contracts

The registry is populated by merging these sources. Conflicts between sources are flagged for human review, not auto-resolved.

**Example registry entry:**

```python
{
  "aes-core-01": [
    "Abductive Elicitation Service",
    "AES",
    "Detective",
    "Abduction Engine"
  ],
  "ingest-core-01": [
    "Ingestion Service",
    "Ingestor",
    "Pipeline Ingest"
  ]
}
```

### 6.2 Resolution Algorithm

1. Exact alias match (case-insensitive)
2. If unresolved, perform LLM-assisted semantic mapping (see §6.3 for epistemic constraints)
3. If still unresolved, mark as `NEW`

Resolution **MUST** return:

* Canonical service ID
  **or**
* Literal string `"NEW"`

No heuristic string normalization is permitted.

### 6.3 Epistemic Constraints on LLM-Assisted Resolution

Per The Plot §2.1 (No Oracle Claims, Uncertainty Visible), LLM-assisted semantic mapping in step 2 **MUST**:

* Carry a **confidence score** (0.0–1.0) on every mapping
* Be classified as **L1-INTERNAL** per the Epistemic Vocabulary Mapping — this is a model-mediated interpretation, not a verified fact
* Be classified as **Epistemic uncertainty** per PFCF — the LLM introduces model uncertainty
* **Never auto-accept** mappings below a configurable confidence threshold (default: 0.90)
* Present sub-threshold mappings as **proposals for human review**, not as resolved identities

LLM resolution that incorrectly maps a service name is a source of false confidence. The system must not grant itself certainty about its own interpretations (per IRIS-T-002: Self-Knowledge Certainty).

---

## 7. Conformance Audit (Solving the Drift Problem)

### 7.1 Trigger Condition

A **drift audit** is mandatory when:

* A spec-implied service resolves to an existing service ID

### 7.2 Drift Dimensions

The audit compares:

* Responsibilities
* Inputs
* Outputs
* Interface directionality

### 7.3 Drift Output Schema

```json
{
  "compliant": false,
  "drift_score": 72,
  "gaps": [
    {
      "type": "MISSING_RESPONSIBILITY",
      "description": "Bounded abductive search not declared"
    }
  ]
}
```

### 7.4 Interpretation

* `compliant: true` → no action required
* `drift_score < 100` → update required
* Gaps MUST be human-reviewable and actionable

---

## 8. New Service Proposal Workflow

When a service is marked `NEW`, the system **MUST**:

1. Generate a **draft `service.yaml`**
2. Populate:

   * Name
   * Proposed ID
   * Interfaces (inferred)
   * Responsibilities
3. Mark status as `proposed`

These drafts are **never auto-merged**.

---

## 9. Topology Analysis (Solving the Graph Problem)

### 9.1 Architectural Graph Model

Each service is a node.
Each interface (produced → consumed) is a directed edge.

### 9.2 Mermaid Output

The audit tool **SHOULD** generate a Mermaid diagram:

* Existing services: normal styling
* Missing services: highlighted
* Broken links: emphasized

This visualization represents:

* Completeness
* Integration gaps
* Architectural choke points

---

## 10. Outputs and Artifacts

Each audit run **MUST** produce:

| Artifact                 | Purpose                             |
| ------------------------ | ----------------------------------- |
| `service_inventory.json` | All extracted services + resolution |
| `missing_services.json`  | Canonical list of NEW services      |
| `drift_report.md`        | Human-readable conformance gaps     |
| `architecture.mmd`       | Visual topology                     |

**Provenance (HIRI Integration):** All audit artifacts SHOULD be content-addressed via HIRI v2.1 Resolution Manifests, consistent with the "Provenance Always" non-negotiable (The Plot §2.1). This ensures audit results are versioned, tamper-evident, and traceable to the specific spec versions they were derived from. At minimum, each artifact MUST include a `sha256` hash and a timestamp.

---

## 11. CI Integration

A repository **MAY** enforce:

* Failure if NEW services exist without proposals
* Failure if drift_score < threshold
* Failure if interfaces reference non-existent services

This enables **architecture-as-code enforcement**.

---

## 12. Machine-First Reasoning Model

This system treats the repository as a **compiler**:

| Layer          | Role            |
| -------------- | --------------- |
| Markdown Specs | Source Code     |
| Audit Tool     | Compiler        |
| service.yaml   | Build Artifacts |
| Mermaid Graph  | Linker Map      |
| CI             | Type Checker    |

The agent does not “decide architecture.”
It enforces **coherence between intent and reality**.

---

## 13. Versioning Notes

v1.1 introduces:

* Canonical service identity
* Drift auditing
* Topology awareness
* Machine-generated registry proposals

v1.0 mechanisms remain valid but insufficient alone.

---

### Closing Note

This spec intentionally shifts architectural authority **upstream** to human-authored intent while using machines to enforce discipline, consistency, and completeness.

This is not agentic automation.
This is **architectural rigor at scale**.

