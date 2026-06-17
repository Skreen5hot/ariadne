# SHML Edge Compiler

## Revised Architecture and Service Specification v0.3.0

| Attribute | Value |
|---|---|
| Version | 0.3.0 |
| Status | Revised Draft |
| Replaces | SHML Compiler v0.2 |
| Conforms to | SHML v3.3 |
| Namespace | `shml:` → `http://fnsr.org/shml/` (canonical; repointed from the v0.2 placeholder) |

---

## Changes in v0.3.0

This revision aligns the compiler with the SHML v3.3 specification. The compiler's generic core is preserved; every addition is backward-compatible — when fed a plain graph with no Assertion Events and no Belief Scopes, the compiler behaves exactly as v0.2.

**Reframed**
- **Identity (§3).** The compiler is now specified as the **Edge-Canonical execution engine for the SHML v3.3 Scope Declaration**. The manifest is *generated from* a Scope Declaration (SHML v3.3 §8.1), which is the single source of truth. SPARQL is the adapter execution target, not the engine — resolving the tension between SHML v3.3 §8.3 (which uses SPARQL CONSTRUCT) and the Edge-Canonical Spec Test (§2.7).

**Added**
- **§4.3 ECP-SC boundary resolution.** ECP-SC is defined as the SPARQL/triplestore execution target — the realization of the non-core `@shml/sparql` adapter — with an equivalence guarantee binding it and this compiler to the same Scope Declaration.
- **§7.6.1 Derivation Rules.** A declared, pure, traced field-derivation construct for SHML v3.3 Appendix B.5 *rule-derived* fields (e.g., a status computed by a state machine over process membership), which are not expressible as path reads.
- **§7.11 Scope Filtering.** Belief Scope binding (manifest-level) and `scopeFilter` (rule-level), per SHML v3.3 §4.3 and §8.5.
- **§7.8 Assertion Event trace pass-through.** An optional `derivedFrom` field on `FieldTrace`, populated when the input graph carries Provenance Index linkage (SHML v3.3 §4.2). These identifiers are content-addresses (CIDs) when the federation adapter is present (SHML v3.3 §4.4).
- **§6 Projection output envelope.** `_contract`, `_generated_at`, `_derived_from`, `_scope_bounded_to`, `_excluded_scopes`, per SHML v3.3 §8.5.
- **Appendix A: Conformance to SHML v3.3** — a mapping of compiler constructs to SHML v3.3 sections and conformance IDs.

**Amended**
- **§7.7 Collision emission.** The `emit-conflict-object` policy's object shape is pinned to the SHML v3.3 §8.6 schema.
- **§7.9 Loss model.** Categories reconciled with SHML v3.3 Appendix B, including the new derived-by-rule category (B.5).
- **§18 Worked example.** Aligned to the canonical `is_tokenized_by` projection pattern.

**Resolved**
- ECP-SC is the realization of the SPARQL adapter boundary. The core compiler MUST NOT depend on it; ECP-SC MUST NOT be part of the SHML Compiler core. The two are interchangeable execution targets of one Scope Declaration, bound by an equivalence guarantee (§4.3).

---

## 1. Purpose

The SHML Compiler is an **edge-canonical semantic projection engine** and the **Edge-Canonical execution engine for the SHML v3.3 Compression Layer** (SHML v3.3 §8).

It transforms valid RDF / JSON-LD knowledge structures into compact, semantically honest JSON-LD projections while preserving:

* field-level traceability — to source statements and, when present, to the Assertion Events that produced them (SHML v3.3 §4.1),
* projection rules,
* source paths,
* belief-scope bounding (SHML v3.3 §4.3),
* uncertainty,
* loss model declarations (SHML v3.3 Appendix B),
* and optional rehydration paths back to the fuller graph (the inverse of the projection — the SHML v3.3 §8 forward transform).

The compiler is not primarily a web service, database application, graph server, ETL pipeline, or deployment topology. It is a deterministic computation over JSON-LD inputs.

The canonical execution model is:

```text
browser
or
node index.js
```

Any cloud, server, database, message broker, registry, worker, queue, endpoint, or enterprise platform is an optional adapter. None is part of the core specification.

> **Relationship to the SHML v3.3 Scope Declaration.** The manifest the compiler consumes (§8) is *generated from* a SHML v3.3 Scope Declaration, which is the single source of truth (SHML v3.3 §8.1). The compiler does not replace the Scope Declaration; it executes one of the artifacts generated from it. See §3 for the generation picture and §4.3 for the relationship to the SPARQL execution target (ECP-SC).

---

## 2. Architectural First Principles

### 2.1 Edge-Canonical First Principle

All core SHML/SHAML components MUST be able to run, unmodified, in:

```text
1. a browser runtime
2. a local NodeJS runtime via node index.js
```

If a component cannot operate under this constraint, it is not core logic. It is infrastructure and MUST be isolated behind an adapter boundary.

> This principle is the reason the compiler exists alongside the SHML v3.3 §8.3 SPARQL CONSTRUCT. SPARQL requires a query engine, which fails the Spec Test (§2.7). The compiler materializes projections by path-walking in pure JS, with no engine — making the SHML projection contract executable under Edge-Canonical First. SPARQL execution is the adapter path (§4.3).

### 2.2 No Required Infrastructure

The core compiler MUST NOT require:

* databases,
* message brokers,
* service registries,
* background workers,
* addressable servers,
* deployment topologies,
* cloud services,
* network access,
* persistent daemons,
* external APIs.

These MAY exist only as optional adapters.

### 2.3 Determinism Over Deployment

Given the same JSON-LD inputs, manifest, options, and declared local resolution context, the compiler SHOULD produce the same outputs.

Hidden state, ambient services, system clocks, network lookups, environment variables, and undeclared caches MUST NOT affect core computation.

If nondeterminism is unavoidable, it MUST be declared as an adapter behavior, not core behavior.

> Derivation rules (§7.6.1) MUST be pure and deterministic for this reason. A derivation function that consults the system clock, the network, or hidden state is an adapter behavior, not core computation.

### 2.4 Mandatory Separation of Concerns

The specification distinguishes four concerns:

| Concern       | Meaning                                                     | Core? |
| ------------- | ----------------------------------------------------------- | ----- |
| Computation   | What is derived, projected, flattened, traced, or validated | Yes   |
| State         | How intermediate results are stored or resumed              | No    |
| Orchestration | How and when computation is invoked                         | No    |
| Integration   | How the external world is contacted                         | No    |

Only computation is core. State, orchestration, and integration are pluggable.

> This separation is what lets the SHML v3.3 §4.4 federation layer (content-addressing over IPFS) live in the **state/integration adapter**, not in core compute. The compiler core does not content-address anything. Its output packages are what the federation adapter content-addresses, and the Assertion Event identifiers that flow through its trace (§7.8) *are* CIDs when that adapter is present. The compiler therefore needs no content-addressing feature — only the trace slot that carries the identifiers through.

### 2.5 JSON-LD as Canonical Representation

JSON-LD is the authoritative representation for: inputs, outputs, manifests, projection rules, trace maps, loss models, conformance reports, rehydration templates, and inter-component contracts.

Alternative internal forms such as RDFJS datasets, quads, maps, indexes, tables, or property-graph-like structures are permitted only as implementation optimizations. They MUST be losslessly derivable from the canonical JSON-LD representation.

### 2.6 Offline Is First-Class

Inability to reach an external system is not an error in the core model. The compiler MUST define valid behavior for: partial information, unresolved IRIs, missing remote contexts, deferred resolution, degraded execution, and explicit uncertainty.

Network resolution is an adapter concern.

### 2.7 Spec Test

A SHML/SHAML draft is not acceptable unless the answer is yes to this question:

> Could a developer evaluate, reason about, and execute this system using only a browser, a local NodeJS runtime, and JSON-LD files?

If not, the draft has leaked infrastructure into the core.

### 2.8 Relationship to SHML v3.3 (informative)

The compiler is one execution target generated from the SHML v3.3 Scope Declaration. Three principles govern the relationship:

1. **The Scope Declaration is upstream.** The manifest is generated from it; the compiler does not author projection policy, it executes it.
2. **Genericity is preserved.** The core projects any valid JSON-LD graph and invents no domain meaning (§7.6). SHML-conformant output arises from feeding it SHML-shaped manifests and provenance-linked inputs — not from hard-coding SHML semantics into the core. The compiler is therefore simultaneously a generic projection engine and the SHML execution engine.
3. **Additions are no-ops on plain graphs.** Assertion Event trace (§7.8) and Belief Scope filtering (§7.11) activate only when the input carries the corresponding structure. On a plain graph they do nothing, and the compiler behaves as v0.2.

---

## 3. Revised System Identity

The compiler is a pure function:

```text
compileSHML(inputPackage) → outputPackage
```

Where both the input and output packages are JSON-LD documents.

```ts
type CompileSHML = (
  inputPackage: JsonLdDocument
) => JsonLdDocument;
```

### 3.1 Position in the SHML v3.3 Generation Picture

The compiler is **one of two execution targets** generated from the SHML v3.3 Scope Declaration:

```text
Scope Declaration                      (SHML v3.3 §8.1 — single source of truth)
   │  generates
   ├──→ Compiler Manifest              (Edge-Canonical execution target — THIS SPEC)
   │       ├─ compileSHML executes  → projection + traceMap + lossModel + report
   │       └─ inverse template       → rehydration (= SHML v3.3 §8 forward transform)
   │
   ├──→ JSON-LD Context               (graph → flat framing; SHML v3.3 §8.2)
   │
   └──→ Parametric SPARQL CONSTRUCT   (triplestore execution target — ECP-SC; §4.3)
           └─ ECP-SC executes        → projection + traceMap + lossModel + report
```

Both execution targets are bound by the **equivalence guarantee** of §4.3: the same Scope Declaration, applied to the same underlying knowledge, MUST yield semantically equivalent projection, trace, and loss model regardless of which executor ran.

### 3.2 Conceptual Pipeline

```text
JSON-LD Input Package
  ↓
normalize declared graph
  ↓
resolve manifest                       (generated from Scope Declaration)
  ↓
apply scope binding                    (§7.11 — no-op if input carries no scopes)
  ↓
select anchors
  ↓
apply projection rules                 (flattening §7.5 + derivation §7.6.1)
  ↓
flatten eligible structures
  ↓
construct trace map                    (incl. Assertion Event pass-through §7.8)
  ↓
declare loss model                     (reconciled with SHML v3.3 Appendix B)
  ↓
assemble output envelope               (§6 — SHML v3.3 §8.5)
  ↓
emit compressed JSON-LD output package
```

No server, database, queue, or endpoint is implied.

---

## 4. Project Boundary

### 4.1 Project 1: SHML Edge Compiler (this specification)

This project produces compact, traceable semantic projections under Edge-Canonical First.

```text
Full RDF / JSON-LD
  → SHML compiler
  → compressed JSON-LD projection
```

### 4.2 Project 2: RDF-to-i2 / ANX Compiler

This later project consumes SHML/SHAML output.

```text
Compressed SHML / JSON-LD
  → i2 chart intermediate representation
  → ANX
```

The ANX compiler MUST NOT be part of the SHML core.

### 4.3 Resolution: Relationship to ECP-SC

> **Provenance of this resolution.** This boundary is defined from the ECP-SC name (**E**dge-**C**anonical **P**arametric **S**PARQL **C**ompiler) and the SHML v3.3 generation architecture, not from the ECP-SC v0.2.0 text. If ECP-SC's actual scope differs, reconcile this section against it; the equivalence guarantee and the non-dependency rule are the load-bearing parts and should hold under any reconciliation.

**ECP-SC is the SPARQL/triplestore execution target.** It is the realization of this compiler's own non-core `@shml/sparql` adapter (§16), elevated to its own specification because parametric SPARQL compilation is substantial enough to warrant one. Where this compiler executes the **manifest** path (pure JS, browser/node, offline), ECP-SC executes the **SPARQL CONSTRUCT** path against a triplestore.

**Division of labor — by data residence:**

| Where the knowledge lives | Execution target | Why |
|---|---|---|
| Local JSON-LD files, in-browser, offline, no infrastructure | **SHML Edge Compiler** (this spec) | Edge-Canonical First; no engine required |
| A triplestore or SPARQL endpoint | **ECP-SC** | The data already lives behind SPARQL; round-tripping it to JSON-LD files to use the Edge compiler would be wasteful |

Both are generated from the **same Scope Declaration**. Neither is redundant: they serve different *deployment substrates* of the same logical operation — exactly the core/adapter philosophy this specification already espouses (§2.4).

**Equivalence guarantee (normative).** For a given Scope Declaration `S` and a body of knowledge `K` (whether `K` is presented as local JSON-LD to this compiler or as triplestore contents to ECP-SC):

```text
project(SHML-Edge-Compiler, manifest(S), K)
  ≡_semantic
project(ECP-SC, sparql(S), K)
```

The two projections MUST be semantically equivalent: same projected fields, same values, same collision outcomes, same loss-model categories, and trace metadata that resolves to the same source statements and the same Assertion Events. Differences permitted: identifier minting, ordering, and serialization detail. Differences NOT permitted: a field present in one and absent in the other, divergent collision resolution, or divergent loss categorization. This guarantee is the interface contract that prevents the two executors from drifting.

**Shared output contract (normative).** Both executors MUST emit the `CompileOutputPackage` shape of §6, including the projection output envelope (§6 / SHML v3.3 §8.5), the field-level trace schema (§7.8), and the loss model (§7.9). A consumer MUST NOT be able to tell, from the output package alone, which executor produced it (modulo the permitted differences above).

**Non-dependency (normative).**
- The SHML Edge Compiler core MUST NOT depend on ECP-SC. ECP-SC is invoked only when the knowledge lives in a triplestore.
- ECP-SC MUST NOT be part of the SHML Edge Compiler core.
- A federation MAY run both, choosing per node by data residence, with HIRI bridging entity identity across nodes (SHML v3.3 §3.4, §12).

---

## 5. Core Input Package

The compiler accepts a single JSON-LD input package containing all information needed for deterministic local execution.

```json
{
  "@context": {
    "shml": "http://fnsr.org/shml/",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#"
  },
  "@type": "shml:CompileInputPackage",
  "inputGraph": {
    "@id": "graph:input",
    "@graph": []
  },
  "manifest": {
    "@id": "manifest:default",
    "@type": "shml:ProjectionManifest",
    "generatedFrom": "scope-declaration:<id>"
  },
  "provenanceIndex": {
    "@id": "provindex:input",
    "@graph": [],
    "_note": "Optional. SHML v3.3 §4.2 linkage: maps input statements to the Assertion Events that produced them. When present, drives §7.8 trace pass-through. When absent, trace resolves to source statements only."
  },
  "scopeContext": {
    "@id": "scopes:input",
    "knownScopes": [],
    "_note": "Optional. SHML v3.3 §4.3 Belief Scopes referenced by the manifest's scopeBinding. When absent, scope binding is a no-op."
  },
  "options": {
    "mode": "traceable",
    "reasoning": "declared-types-only",
    "offline": true
  },
  "resolutionContext": {
    "remoteResolution": "disabled",
    "knownContexts": [],
    "knownOntologies": []
  }
}
```

The input package MAY contain compacted JSON-LD, expanded JSON-LD, or JSON-LD-compatible RDF graph structures.

If Turtle, RDF/XML, N-Triples, CSV, or external records are used, they must be converted into the JSON-LD input package before entering the core compiler, or handled by optional adapters.

> **`provenanceIndex` and `scopeContext` are optional.** They are the carriers for SHML v3.3 awareness. When present, the compiler produces SHML-conformant trace (§7.8) and scope-bounded projections (§7.11). When absent, the compiler projects a plain graph exactly as v0.2 did. This is how genericity and SHML-conformance coexist.

---

## 6. Core Output Package

The compiler emits a JSON-LD output package with a **projection output envelope** (SHML v3.3 §8.5).

```json
{
  "@context": {
    "shml": "http://fnsr.org/shml/"
  },
  "@type": "shml:CompileOutputPackage",

  "envelope": {
    "_contract": "scope-declaration:<id>",
    "_generated_at": "<timestamp — adapter-supplied; see note>",
    "_derived_from": [],
    "_scope_bounded_to": [],
    "_excluded_scopes": []
  },

  "projection": {
    "@id": "projection:local",
    "@graph": []
  },
  "traceMap": {
    "@id": "trace:local",
    "@graph": []
  },
  "lossModel": {
    "@id": "loss:local"
  },
  "report": {
    "@id": "report:local"
  }
}
```

The envelope fields:

| Field | Content | Source |
|---|---|---|
| `_contract` | Identifier of the producing Scope Declaration | manifest `generatedFrom` |
| `_generated_at` | Timestamp of materialization | adapter-supplied |
| `_derived_from` | Assertion Event identifiers (CIDs when federated) that produced the emitted fields | `provenanceIndex` |
| `_scope_bounded_to` | Belief Scopes this projection is bounded to | manifest `scopeBinding` |
| `_excluded_scopes` | Belief Scopes deliberately excluded | manifest `scopeBinding` |

> **Determinism note.** `_generated_at` is a timestamp and therefore MUST be supplied by an adapter, not read from the system clock in core (§2.3). Core computation that must remain deterministic excludes `_generated_at` from any hash or equivalence comparison.

The output package MUST be understandable without a running server. It MAY contain references to external graphs or contexts, but unresolved references MUST be represented as unresolved, not silently fetched.

---

## 7. Core Computation

The core compiler consists only of computation modules.

### 7.1 JSON-LD Normalization

The compiler normalizes the declared input graph into an internal graph view. This module MAY use indexes internally, but the canonical source remains the JSON-LD input package.

Responsibilities: expand compacted terms using declared local contexts; preserve IRIs; preserve blank node identity where possible; preserve literals, datatypes, and language tags; preserve named graph information if present; preserve unresolved references explicitly.

Remote context fetching MUST NOT occur in core computation. If a referenced context is unavailable locally, the compiler MUST emit a deferred-resolution warning.

### 7.2 Manifest Resolution

The compiler resolves the projection manifest from the input package. The manifest declares the Scope Declaration it was generated from (`generatedFrom`). The manifest MAY extend another manifest only if the parent is included locally in the input package or declared in the local resolution context. Network retrieval of parent manifests is not core behavior.

### 7.3 Type and Class Awareness

The compiler MAY use the following local reasoning modes:

```text
none
declared-types-only
local-rdfs-subclass
local-rule-closure
```

Full OWL reasoning is optional and MUST be isolated as an adapter or replaceable computation module. The default mode SHOULD be `declared-types-only`, or `local-rdfs-subclass` when the relevant subclass axioms are present in the input package.

### 7.4 Anchor Selection

An anchor is a source graph node selected as a projection subject. Anchor rules are manifest-defined.

```json
{
  "@id": "rule:select-government-orgs",
  "@type": "shml:AnchorRule",
  "sourceClass": "cco:ont00000408",
  "targetKind": "shml:ProjectedEntity"
}
```

Anchor selection MUST be deterministic over the provided graph and manifest. If a class hierarchy required to identify anchors is not locally available, the compiler MUST degrade gracefully by using declared types only and reporting reduced certainty.

### 7.5 Projection Rule Application (Flattening)

A flattening rule **reads** a value from a path. Projection rules transform full graph patterns into compact JSON-LD fields or structures.

A flattening rule MUST declare: its identifier, its source pattern (path), its target field or structure, its cardinality expectation, its collision policy, its trace policy, and its rehydration policy if any. It MAY declare a `scopeFilter` (§7.11).

```json
{
  "@id": "rule:flatten-status",
  "@type": "shml:FlatteningRule",
  "ownerKind": "shml:ProjectedEntity",
  "path": [
    "obo:RO_0000053",
    "cco:ont00001761"
  ],
  "field": "status",
  "cardinality": "single",
  "collisionPolicy": "emit-conflict-object",
  "tracePolicy": "field-level"
}
```

This is the canonical SHML projection pattern: walk `bearer_of` (`obo:RO_0000053`) to the Quality instance, then read `is_tokenized_by` (`cco:ont00001761`). It is generated from the corresponding capture clause of the Scope Declaration.

### 7.6 Generic Fallback Projection

Because the compiler cannot assume CCO, SHACL, or modeler-specific conventions, it MUST support generic fallback behavior. Fallback rules MAY include direct literal flattening, bounded object-to-literal flattening, generic object relation links, and trace-only preservation of unknown structures.

Fallback projection MUST NOT invent domain meaning.

Given:

```turtle
ex:a ex:foo ex:b .
ex:b ex:bar "123" .
```

The compiler MAY emit `{ "properties": { "ex:foo.ex:bar": "123" } }`. It MUST NOT emit `{ "status": "123" }` unless a manifest rule declares that mapping.

### 7.6.1 Derivation Rules

A flattening rule reads a value from a path. A **derivation rule computes a value from a declared pure function over matched graph patterns.** This construct exists for SHML v3.3 Appendix B.5 *rule-derived* fields — values that are present in neither the source data nor any single path, but are computed by a rule (e.g., a shipment `status: "In Transit"` computed by a state machine over process membership). These are not expressible as path reads, and v3.3 B.5 flags them as the most dangerous fields in a projection precisely because they carry the appearance of a directly-observed value.

A derivation rule MUST declare:

* its identifier,
* its inputs — the patterns or paths it consumes,
* a reference to its derivation function,
* its output field,
* its trace policy,
* a `scopeFilter` if any (§7.11).

Constraints (normative):

* The derivation function MUST be **pure and deterministic** (§2.3). It MUST NOT consult the clock, network, environment, or hidden state.
* The core MUST NOT define domain derivation logic. The function's content is supplied by the manifest author (as a registered pure function or a declarative spec). The core invokes it, sandboxes it, and guarantees its inputs are traced.
* A derived field MUST be traced to the derivation rule AND to the source patterns — and, when `provenanceIndex` is present, to the Assertion Events — it consumed (§7.8).
* A derived field MUST be flagged in the loss model as `derivedByRule` (§7.9).
* A derived field MUST NOT be presented as if read directly from a path. (SHML v3.3 §11(9).)

```json
{
  "@id": "rule:derive-shipment-status",
  "@type": "shml:DerivationRule",
  "ownerKind": "shml:ProjectedEntity",
  "inputs": [
    { "path": ["ex:hasTransportProcess", "ex:processState"] },
    { "path": ["ex:hasReceivingProcess", "ex:processState"] }
  ],
  "derivationFunction": "fn:shipment-status-state-machine",
  "field": "status",
  "tracePolicy": "field-level"
}
```

> **Why this stays in core but the function does not.** The *mechanism* — invoke a declared pure function, sandbox it, trace its inputs, flag it in the loss model — is generic and belongs in core. The *content* — what state machine governs shipment status — is domain logic and belongs with the manifest author. This preserves the compiler's "MUST NOT invent domain meaning" principle while making B.5 expressible.

### 7.7 Collision Resolution

The compiler MUST NOT silently discard conflicting projected values. Collision policies include:

```text
error
warning
emit-array
emit-conflict-object
select-first-by-declared-priority
select-by-source-authority
select-by-timestamp
trace-only
```

If the required information for a selected collision policy is unavailable, the compiler MUST report degraded resolution and use the manifest's fallback collision policy.

**`emit-conflict-object` schema (normative, SHML v3.3 §8.6).** When the policy is `emit-conflict-object`, the projected field value MUST be `null`, and the conflict MUST be emitted as a `_conflicts` entry with this shape:

```json
{
  "field": "<field name>",
  "reason": "<why this is a conflict>",
  "candidates": [
    {
      "value": "...",
      "scope": "<belief scope, if scope-bounded>",
      "asserted_by": "<agent>",
      "via": "<Assertion Event identifier>"
    }
  ]
}
```

`scope`, `asserted_by`, and `via` are populated when `scopeContext` and `provenanceIndex` are present; they are omitted otherwise. A consuming system that requires a single value MUST resolve the conflict by narrowing the scope binding or applying a declared selection policy — never by reading one candidate arbitrarily.

### 7.8 Trace Construction

The compiler MUST produce field-level trace metadata for every projected field when operating in traceable mode.

A field trace SHOULD include: source node, source path, source value, projection rule, source graph, local statement references, collision resolution behavior, uncertainty status, rehydration rule if available, and — when the input carries Provenance Index linkage — `derivedFrom`.

**Assertion Event pass-through (normative, SHML v3.3 §4.1).** `FieldTrace` MAY include a `derivedFrom` field: the list of Assertion Event identifiers that produced the source statement(s) the field was projected from.

* When `provenanceIndex` is present in the input package (SHML v3.3 §4.2), the compiler MUST populate `derivedFrom`.
* When it is absent, `derivedFrom` is omitted and the trace resolves to source statements only.
* When the federation adapter is present, these identifiers are content-addresses (CIDs, SHML v3.3 §4.4).
* The compiler MUST NOT synthesize Assertion Events. It passes through those present in the input. This preserves the "invent nothing" principle: the compiler does not fabricate provenance, it propagates it.

```json
{
  "@id": "trace:org1/status",
  "@type": "shml:FieldTrace",
  "projectedEntity": "ex:org1",
  "field": "status",
  "value": "ACTIVE",
  "sourcePath": [
    "obo:RO_0000053",
    "cco:ont00001761"
  ],
  "sourceNode": "ex:statusNode1",
  "projectionRule": "rule:flatten-status",
  "scope": "ex:Scope_CountyGIS_Current",
  "derivedFrom": [ "ae:cid:bafy...status-assert" ],
  "certainty": "resolved-local"
}
```

### 7.9 Loss Model Construction

Every output package MUST include a loss model declaring what happened during projection. Its categories are reconciled with SHML v3.3 Appendix B:

| Loss model category | SHML v3.3 Appendix B |
|---|---|
| `preserved` | B.1 Fields preserved |
| `flattened` | B.1 (collapsed ICE/IBE chain) |
| `omitted` (derivable) | B.2 Fields intentionally dropped |
| `notInSource` | B.3 Information not in source data |
| `ambiguous` | B.4 Collision |
| `derivedByRule` | **B.5 Derived-by-rule fields** |
| `traceOnly` | (compiler extension — unmapped relations retained for trace) |
| `unresolved` | (compiler extension — offline/deferred, SHML v3.3 §9 of compiler) |

```json
{
  "@id": "loss:local",
  "@type": "shml:ProjectionLossModel",
  "preserved": [ "selected anchors", "selected literal values" ],
  "flattened": [ "bounded object-to-literal paths", "collapsed ICE nodes via is_tokenized_by" ],
  "omitted": [ "level (derivable from part_of depth)" ],
  "notInSource": [ "temporal extent of status (no timestamps in source)" ],
  "derivedByRule": [ "status (via fn:shipment-status-state-machine)" ],
  "traceOnly": [ "unmapped object relations" ],
  "ambiguous": [],
  "unresolved": [ "remote context not available" ],
  "requiresFullGraphForRehydration": true
}
```

The loss model MUST distinguish between: not present; present but not projected; present but trace-only; present but unresolved; present but ambiguous; present but derived-by-rule; and present and projected.

### 7.10 Rehydration Metadata

The compiler MAY support rehydration modes:

```text
none
traceable-with-source-graph
template-rehydratable
self-contained
```

The default SHOULD be `traceable-with-source-graph`. In this mode the compressed projection does not contain the entire full graph, but preserves enough local identifiers and source paths to trace back if the full graph is provided later.

> **`template-rehydratable` is the SHML v3.3 §8 forward transform.** In this mode the rehydration template — generated from the same manifest, which is generated from the same Scope Declaration — is the inverse of the flattening rules and reconstructs the full graph from the flat payload. This is precisely the SHML v3.3 §8.1 forward transform that holds the field-to-ICE-type mapping the JSON-LD context cannot carry. The compiler's `template-rehydratable` mode and the v3.3 forward transform are the same artifact under two names.

Rehydration MUST NOT require a database. A rehydration operation is another pure computation:

```text
rehydrateSHML(projectionPackage, manifestPackage, optionalSourceGraphPackage)
  → JSON-LD graph package
```

### 7.11 Scope Filtering

Belief Scopes (SHML v3.3 §4.3) bound a projection to specific agents' interpretations. The compiler supports scope binding at the manifest level and scope filtering at the rule level.

* The manifest MAY declare `scopeBinding`: `{ scopesIncluded: [...], scopesExcluded: [...] }` (SHML v3.3 §8.5). These populate the output envelope's `_scope_bounded_to` and `_excluded_scopes`.
* A flattening or derivation rule MAY declare `scopeFilter`: a named scope restricting the rule to Assertion Events `in_scope` that scope.

Behavior (normative):

* When the input carries scope membership — Assertion Events tagged `in_scope` via `scopeContext` and `provenanceIndex` (SHML v3.3 §4.3) — the compiler MUST honor scope binding and `scopeFilter`. Statements produced only by Assertion Events outside the bound scopes MUST NOT be projected.
* When the input carries no scope membership, scope binding is a **no-op**: the compiler projects the whole graph, and `_scope_bounded_to` / `_excluded_scopes` are recorded as declared but unenforced.
* Cross-scope behavior MUST NOT be implicit. A projection that draws on more than one scope binds them explicitly via `scopesIncluded`; the compiler does not silently merge scopes (SHML v3.3 §4.3, §10.3).

```json
{
  "scopeBinding": {
    "scopesIncluded": [ "ex:Scope_CountyGIS_Current", "ex:Scope_ZoningCurrent" ],
    "scopesExcluded": [ "ex:Scope_USPS", "ex:Scope_RezoningProposal_2026" ]
  }
}
```

---

## 8. Canonical Manifest Model

The manifest is a JSON-LD document, **generated from a SHML v3.3 Scope Declaration**.

```json
{
  "@context": {
    "shml": "http://fnsr.org/shml/"
  },
  "@id": "manifest:default-edge-shml-v1",
  "@type": "shml:ProjectionManifest",
  "generatedFrom": "scope-declaration:<id>",

  "inputContract": {
    "required": [ "valid JSON-LD input package" ],
    "optional": [ "provenanceIndex (SHML v3.3 §4.2)", "scopeContext (SHML v3.3 §4.3)" ],
    "notAssumed": [
      "network access", "database", "server",
      "CCO", "SHACL", "specific predicates",
      "unique labels", "complete provenance"
    ]
  },

  "executionContract": {
    "canonicalRuntime": [ "browser", "node index.js" ],
    "remoteResolution": "adapter-only",
    "determinism": "same-inputs-same-outputs",
    "sparqlTarget": "ECP-SC (optional, §4.3)"
  },

  "scopeBinding": {
    "scopesIncluded": [],
    "scopesExcluded": []
  },

  "anchorRules": [],
  "labelRules": [],
  "typeRules": [],
  "flatteningRules": [],
  "derivationRules": [],
  "linkRules": [],

  "fallbackRules": {
    "directLiteralFlattening": true,
    "boundedLiteralFlattening": true,
    "boundedLiteralFlatteningDepth": 2,
    "genericAnchorLinks": true,
    "preserveUnknownPredicatesInTrace": true
  },

  "collisionRules": {
    "default": "emit-conflict-object"
  },

  "traceRules": {
    "fieldLevelTrace": true,
    "includeSourcePath": true,
    "includeProjectionRule": true,
    "includeSourceGraph": true,
    "includeAssertionEvents": true
  },

  "rehydrationPolicy": {
    "mode": "traceable-with-source-graph"
  }
}
```

---

## 9. Offline and Deferred Resolution

Offline operation is not exceptional. The compiler MUST continue when possible if remote JSON-LD contexts, ontology imports, external manifests, source documents, provenance systems, or remote identifiers are unavailable. The output MUST explicitly represent unresolved dependencies.

```json
{
  "@id": "warning:missing-context",
  "@type": "shml:DeferredResolution",
  "resource": "https://example.org/context.jsonld",
  "effect": "Terms using this context were not expanded beyond local declarations.",
  "severity": "warning"
}
```

Allowed certainty values include:

```text
resolved-local
resolved-by-manifest
resolved-by-local-context
partially-resolved
unresolved-remote
ambiguous
trace-only
```

---

## 10. State Model

State is not core. The core compiler operates on an input package and returns an output package.

A state adapter MAY provide local file persistence, browser IndexedDB persistence, in-memory session state, database persistence, object storage, or Git-backed versioning. These adapters MUST NOT change compiler semantics. State adapters store JSON-LD packages; they do not define the meaning of the computation.

> **Federation adapter (SHML v3.3 §4.4).** The content-addressed storage adapter (IPFS) is a state/integration adapter. It content-addresses the compiler's output packages and the Assertion Events referenced in their trace. When this adapter is present, the `derivedFrom` identifiers (§7.8) and the envelope's `_derived_from` (§6) are CIDs, and the Provenance Index is the Merkle-DAG over them. The compiler core remains unchanged: it carries identifiers, it does not address content.

---

## 11. Orchestration Model

Orchestration is not core. The same compiler may be invoked by `node index.js`, a browser button click, a CLI wrapper, a test runner, an HTTP endpoint, a workflow engine, a serverless function, or a desktop app. All invoke the same pure computation.

The normative invocation is:

```js
import { compileSHML } from "./shml-core.js";

const outputPackage = await compileSHML(inputPackage);
```

A CLI wrapper is optional:

```bash
node index.js compile input-package.jsonld > output-package.jsonld
```

An HTTP API is optional and non-normative.

---

## 12. Integration Model

Integration is not core. Adapters MAY exist for SPARQL endpoints, triplestores, graph databases, file systems, web APIs, Git repositories, i2 / ANX pipelines, enterprise catalogs, and ontology registries. Adapters must convert external resources into local JSON-LD packages before core computation begins.

```text
external system
  → adapter
  → JSON-LD input package
  → core compiler
  → JSON-LD output package
  → adapter
  → external system
```

Core computation never contacts the external system directly.

> **ECP-SC realizes the SPARQL adapter boundary (§4.3).** Where the SPARQL adapter would convert triplestore contents into a JSON-LD input package and run this compiler, ECP-SC instead compiles the Scope Declaration to parametric SPARQL and executes the projection in the triplestore directly — appropriate when the knowledge already lives there. Both paths honor the equivalence guarantee of §4.3.

---

## 13. Browser Execution

A conformant browser implementation MUST be able to: load a JSON-LD input package from a local file, text area, drag/drop, or embedded object; run the compiler without network access; produce a JSON-LD output package; and display or download the result. It MUST NOT require a server.

---

## 14. Node Execution

A conformant NodeJS implementation MUST be able to run with `node index.js` or equivalent local execution. It MUST NOT require a database process, a web server, a broker, a background worker, or a remote endpoint.

---

## 15. Internal Representation

Implementations MAY use internal structures such as RDFJS Datasets, quad arrays, term indexes, path indexes, maps, tables, or property graph views. These are optimizations only. The authoritative representation remains JSON-LD. An implementation MUST be able to serialize relevant internal state back into the JSON-LD package model without semantic loss.

---

## 16. Minimal Core Modules

The core implementation SHOULD be organized as pure modules:

```text
@shml/core
  compileSHML(inputPackage)

@shml/jsonld
  expandLocal()
  compactLocal()
  frameLocal()

@shml/manifest
  resolveManifestLocal()
  validateManifest()

@shml/rules
  applyAnchorRules()
  applyFlatteningRules()
  applyLinkRules()

@shml/derive
  applyDerivationRules()          # §7.6.1 — sandboxed pure functions, traced inputs

@shml/scope
  applyScopeBinding()             # §7.11 — no-op when input carries no scopes

@shml/trace
  buildTraceMap()                 # incl. Assertion Event pass-through §7.8

@shml/loss
  buildLossModel()

@shml/rehydrate
  rehydrateSHML()
```

The following are non-core adapters:

```text
@shml/cli
@shml/http
@shml/fs
@shml/sparql        # realized by ECP-SC (§4.3)
@shml/browser-ui
@shml/indexeddb
@shml/triplestore
@shml/ipfs          # federation / content-addressing (SHML v3.3 §4.4)
@shml/i2-anx
```

---

## 17. MVP Scope

The MVP core MUST support: JSON-LD input package; JSON-LD manifest (generated from a Scope Declaration); local context handling; anchor selection by declared type; optional local subclass closure; direct literal flattening; bounded object-to-literal flattening; generic anchor-to-anchor links; field-level trace **with optional Assertion Event pass-through**; **scope binding (no-op when absent)**; collision reporting **in the §8.6 conflict-object schema**; **derivation rules**; loss model output **including the derived-by-rule category**; the **projection output envelope**; degraded offline behavior; deterministic local execution; browser execution; NodeJS execution.

The MVP MUST NOT require: HTTP; database; SPARQL endpoint; triplestore; graph database; background worker; cloud deployment; remote JSON-LD context fetch; full OWL reasoning; ECP-SC; or content-addressed storage.

---

## 18. Example Edge Invocation

Input package (canonical `is_tokenized_by` pattern, with optional provenance and scope):

```json
{
  "@context": {
    "shml": "http://fnsr.org/shml/",
    "ex": "https://example.org/",
    "obo": "http://purl.obolibrary.org/obo/",
    "cco": "https://www.commoncoreontologies.org/"
  },
  "@type": "shml:CompileInputPackage",
  "inputGraph": {
    "@id": "graph:example",
    "@graph": [
      {
        "@id": "ex:org1",
        "@type": "cco:ont00000408",
        "obo:RO_0000053": { "@id": "ex:status1" }
      },
      {
        "@id": "ex:status1",
        "@type": "ex:OperationalStatus",
        "cco:ont00001761": "ACTIVE"
      }
    ]
  },
  "provenanceIndex": {
    "@id": "provindex:example",
    "@graph": [
      {
        "@id": "ae:status1-active",
        "@type": "shml:AssertionEvent",
        "shml:subject": "ex:status1",
        "shml:predicate": "cco:ont00001761",
        "shml:object": "ACTIVE",
        "shml:asserted_by": "ex:CountyGIS",
        "shml:in_scope": "ex:Scope_CountyGIS_Current"
      }
    ]
  },
  "manifest": {
    "@id": "manifest:example",
    "@type": "shml:ProjectionManifest",
    "generatedFrom": "scope-declaration:place-summary-v1",
    "scopeBinding": {
      "scopesIncluded": [ "ex:Scope_CountyGIS_Current" ],
      "scopesExcluded": []
    },
    "anchorRules": [
      {
        "@id": "rule:select-orgs",
        "@type": "shml:AnchorRule",
        "sourceClass": "cco:ont00000408",
        "targetKind": "shml:ProjectedEntity"
      }
    ],
    "flatteningRules": [
      {
        "@id": "rule:flatten-status",
        "@type": "shml:FlatteningRule",
        "path": [ "obo:RO_0000053", "cco:ont00001761" ],
        "field": "status",
        "collisionPolicy": "emit-conflict-object"
      }
    ],
    "traceRules": { "fieldLevelTrace": true, "includeAssertionEvents": true }
  },
  "options": { "offline": true, "mode": "traceable" }
}
```

Output package:

```json
{
  "@context": {
    "shml": "http://fnsr.org/shml/",
    "ex": "https://example.org/"
  },
  "@type": "shml:CompileOutputPackage",
  "envelope": {
    "_contract": "scope-declaration:place-summary-v1",
    "_derived_from": [ "ae:status1-active" ],
    "_scope_bounded_to": [ "ex:Scope_CountyGIS_Current" ],
    "_excluded_scopes": []
  },
  "projection": {
    "@id": "projection:example",
    "@graph": [
      {
        "@id": "ex:org1",
        "@type": "shml:ProjectedEntity",
        "properties": { "status": "ACTIVE" }
      }
    ]
  },
  "traceMap": {
    "@id": "trace:example",
    "@graph": [
      {
        "@id": "trace:ex-org1-status",
        "@type": "shml:FieldTrace",
        "projectedEntity": "ex:org1",
        "field": "status",
        "value": "ACTIVE",
        "sourcePath": [ "obo:RO_0000053", "cco:ont00001761" ],
        "sourceNode": "ex:status1",
        "projectionRule": "rule:flatten-status",
        "scope": "ex:Scope_CountyGIS_Current",
        "derivedFrom": [ "ae:status1-active" ],
        "certainty": "resolved-local"
      }
    ]
  },
  "lossModel": {
    "@id": "loss:example",
    "@type": "shml:ProjectionLossModel",
    "preserved": [ "ex:org1" ],
    "flattened": [ "obo:RO_0000053/cco:ont00001761 (collapsed status ICE)" ],
    "derivedByRule": [],
    "requiresFullGraphForRehydration": true
  },
  "report": {
    "@id": "report:example",
    "@type": "shml:CompileReport",
    "status": "completed",
    "warnings": []
  }
}
```

---

## 19. Revised Service Philosophy

The SHML Compiler is not a service first. It is a deterministic semantic computation that services may wrap, and the Edge-Canonical execution engine for the SHML v3.3 Compression Layer.

The center of the architecture is not an endpoint, database, queue, or graph server. The center is the Scope Declaration and this contract:

```text
Scope Declaration in (as a generated manifest)
JSON-LD package in
JSON-LD package out
same inputs, same outputs
offline valid
traceable projection — to source statements and Assertion Events
scope-bounded when the input carries scopes
equivalent to the ECP-SC SPARQL path (§4.3)
```

---

## 20. Conformance Requirements

A conformant core implementation MUST satisfy the following:

1. It MUST run in a browser.
2. It MUST run via local NodeJS execution.
3. It MUST accept JSON-LD as the canonical input representation.
4. It MUST emit JSON-LD as the canonical output representation.
5. It MUST NOT require network access.
6. It MUST NOT require a database.
7. It MUST NOT require an addressable server.
8. It MUST NOT require background workers.
9. It MUST isolate external integrations behind adapters.
10. It MUST distinguish computation from state, orchestration, and integration.
11. It MUST produce deterministic output for identical declared inputs.
12. It MUST represent unresolved external dependencies explicitly.
13. It MUST produce a loss model, including the derived-by-rule category where applicable (SHML v3.3 Appendix B.5).
14. It SHOULD produce field-level trace metadata.
15. It MUST NOT invent semantic meaning for unknown graph patterns.
16. It MUST accept the manifest's `generatedFrom` linkage to a Scope Declaration and MUST emit the projection output envelope (SHML v3.3 §8.5).
17. When the input carries Provenance Index linkage, it MUST populate `derivedFrom` on field traces with the producing Assertion Event identifiers (SHML v3.3 §4.1–§4.2); it MUST NOT synthesize Assertion Events.
18. When the input carries Belief Scope membership, it MUST honor scope binding and `scopeFilter`; when it does not, scope binding MUST be a no-op (SHML v3.3 §4.3, §8.5).
19. It MUST emit conflicts in the §8.6 conflict-object schema; it MUST NOT silently choose among conflicting values (SHML v3.3 §8.6).
20. Derivation functions MUST be pure and deterministic; derived fields MUST be traced to their inputs and flagged in the loss model (SHML v3.3 §11(9), Appendix B.5).
21. A projection it produces MUST be semantically equivalent to the projection ECP-SC produces from the same Scope Declaration (§4.3 equivalence guarantee).

---

## 21. Relationship to Infrastructure

Infrastructure is allowed only after the core is complete.

Valid infrastructure adapters: HTTP API wrapping `compileSHML()`; SPARQL adapter producing input packages; **ECP-SC executing the SPARQL projection path (§4.3)**; database adapter storing output packages; **IPFS adapter content-addressing output packages and Assertion Events (SHML v3.3 §4.4)**; browser UI invoking `compileSHML()`; workflow adapter invoking the compiler on a schedule; enterprise adapter publishing results to a catalog.

Invalid core assumptions: the compiler reads from a triplestore; the compiler writes to a database; the compiler calls a server to resolve contexts; the compiler requires a queue; the compiler depends on a running API; the compiler depends on ECP-SC; the compiler assumes a deployment topology.

---

## 22. Final Spec Test

Before accepting any feature into the core, ask:

```text
Can this be evaluated, reasoned about, and executed with only:
  - a browser,
  - local NodeJS,
  - JSON-LD files?
```

If yes, it may be core. If no, it is an adapter, optimization, or out-of-scope.

---

## Appendix A: Conformance to SHML v3.3

This appendix maps compiler constructs to the SHML v3.3 specification.

| Compiler construct | SHML v3.3 reference | Notes |
|---|---|---|
| Manifest `generatedFrom` | §8.1 Scope Declaration as source of truth | Manifest is a generated artifact |
| `compileSHML` manifest path | §8.3 (Edge-Canonical alternative to SPARQL CONSTRUCT) | Resolves the §8.3/§2.7 tension |
| ECP-SC SPARQL path | §8.3 SPARQL CONSTRUCT target | The triplestore execution target (§4.3) |
| Output envelope | §8.5 Projection Output Envelope | `_contract`, `_generated_at`, `_derived_from`, `_scope_bounded_to`, `_excluded_scopes` |
| `emit-conflict-object` schema | §8.6 Conflict Emission | `candidates: [{value, scope, asserted_by, via}]` |
| `FieldTrace.derivedFrom` | §4.1 Assertion Event Log, §4.2 Provenance Index | Pass-through; CIDs when federated (§4.4) |
| `scopeBinding` / `scopeFilter` | §4.3 Belief Scope Registry, §8.5 | No-op when input carries no scopes |
| `DerivationRule` | Appendix B.5 Derived-by-Rule Fields, §11(9) | Pure, traced, flagged in loss model |
| Loss model categories | Appendix B (B.1–B.5) | See §7.9 mapping table |
| `template-rehydratable` mode | §8.1 forward transform | Same artifact, two names |
| Generic fallback "invent nothing" | §11(15) | Compiler asset; predates and matches the spec |
| IPFS adapter | §4.4 Federation and Content-Addressing | State/integration adapter, not core |
| Equivalence guarantee | §3.4 layered/flat coexistence; §8 contract | Binds the two execution targets |

**Constructs intentionally NOT in the compiler core:**

| Not in core | Why | Where it lives |
|---|---|---|
| Content-addressing / CID minting | Storage concern, not computation (§2.4) | `@shml/ipfs` adapter (SHML v3.3 §4.4) |
| Assertion Event creation | Compiler propagates provenance, does not author it | Upstream ingestion / Middle Layer |
| Belief Scope creation | Scopes are declared upstream | SHML v3.3 §4.3 Belief Scope Registry |
| Domain derivation logic | Domain meaning, not generic mechanism (§7.6.1) | Manifest author's pure functions |
| SPARQL execution | Requires an engine; fails the Spec Test (§2.7) | ECP-SC (§4.3) |

---

*End of SHML Edge Compiler Specification v0.3.0 · conforms to SHML v3.3 · Fandaws Ontology Service · Ontology of Freedom Initiative*
