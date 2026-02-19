# W2Fuel Ontological Schema Service — Core Specification

**Document ID:** `w2fuel-core-01`
**Version:** 2.0.0
**Status:** DRAFT
**Classification:** FNSR Core Memory/Identity Layer Component
**Supersedes:** `w2fuel-core-01` v1.3.1

---

## Version 2.0.0 Summary: Architectural Alignment

> **MAJOR CHANGE:** This version refactors the W2Fuel specification to comply with the FNSR Architectural Principles. All infrastructure assumptions have been removed from the normative specification. What remains is *pure computation*: deterministic functions that take JSON-LD in and produce JSON-LD out, executable in a browser or via `node index.js` with no required infrastructure.
>
> The Rust/Oxigraph/Nemo stack from v1.3.1 is preserved as a **non-normative deployment optimization** in the companion document `w2fuel-deploy-01`. Consumer semantics, event contracts, and all downstream-visible behavior are unchanged.

### What Changed from v1.3.1

| Area | v1.3.1 | v2.0.0 | Impact |
|------|--------|--------|--------|
| **Scope** | Computation + infrastructure unified | Computation only (normative) | Clean separation of concerns |
| **Execution model** | Assumes Oxigraph, Redis, Kafka, K8s | Runs in browser or `node index.js` | Edge-canonical |
| **Data format** | Mixed (Turtle, YAML, bare JSON, N-Quads) | JSON-LD canonical for all I/O | Single authoritative format |
| **Infrastructure** | Normative requirements | Adapter boundaries (pluggable) | No required infrastructure |
| **Offline behavior** | Undefined | Explicit contracts per function | First-class offline mode |
| **Reasoning engine** | Nemo (Rust) required | Abstract Datalog semantics | Any conforming engine |
| **Graph store** | Oxigraph required | Abstract GraphStore adapter | Any conforming store |

### What Did NOT Change

- T-Box / A-Box architecture
- Ontological foundations (BFO/CCO alignment)
- OWL 2 RL profile selection and rationale
- OWL → Datalog transpilation semantics
- OWL → SHACL generation mappings
- Namespace disambiguation logic
- Event semantic content (what changed, sequence_id)
- Consumer behavioral contracts
- Governance change classification
- RBAC role model
- SHACL dual-semantics (OWA/CWA)
- Golden-rule translation tests
- Inference parity comparison logic

---

## 1. Executive Summary

W2Fuel is the **Terminological Box (T-Box)** service for the FNSR architecture. It manages the class definitions, property schemas, and ontological structure that give meaning to all instance data stored in Fandaws (A-Box). W2Fuel defines *what kinds of things exist*; Fandaws stores *which things exist*. MDRE joins both when reasoning.

This specification defines W2Fuel's **computation**: the deterministic, stateless functions that validate ontologies, transpile OWL to Datalog and SHACL, disambiguate namespace references, classify hierarchies, and produce signed validation bundles. All functions accept JSON-LD input and produce JSON-LD output. All functions are executable in a browser, via Node.js, or in any environment that can process JSON-LD.

**This specification does not define** how these functions are deployed, what storage backends persist their results, what message brokers distribute their events, or what CI/CD systems orchestrate their execution. Those concerns belong to adapter implementations and deployment guides, which are non-normative with respect to W2Fuel's architecture.

### Concern Separation

This specification observes strict separation of concerns. Every element is classified as exactly one of:

| Concern | Definition | Normative Status | Location |
|---------|-----------|------------------|----------|
| **Computation** | What is being derived or reasoned | **NORMATIVE** | This document |
| **State** | How intermediate results are stored or resumed | Pluggable | Adapter interfaces (§12) |
| **Orchestration** | How and when computation is invoked | Pluggable | Adapter interfaces (§12) |
| **Integration** | How the external world is contacted | Pluggable | Adapter interfaces (§12) |

Only Computation is core. State, Orchestration, and Integration are defined as adapter interfaces with minimal default implementations suitable for browser and Node.js execution.

### Spec Test

> *Could a developer evaluate, reason about, and execute this system using only a browser, a local Node.js runtime, and JSON-LD files?*

**Yes.** A developer can:

1. Load OWL ontologies as JSON-LD files from disk or URL
2. Call `validateOwlRl()` — pure function, no dependencies
3. Call `owlToDatalog()` — pure function, produces JSON-LD rules
4. Call `owlToShacl()` — pure function, produces JSON-LD shapes
5. Call `disambiguate()` with a JSON-LD registry — pure function
6. Call `materialize()` with an in-memory graph — pure function
7. Evaluate golden-rule tests with `evaluateGoldenRules()` — pure assertions
8. Verify inference parity with `compareInferenceSets()` — pure diff

All I/O is JSON-LD. All computation is deterministic. No servers, databases, brokers, or network access required.

### Architectural Position

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         T-BOX / A-BOX ARCHITECTURE                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                     W2Fuel (This Specification)                     │   │
│   │                         Terminological Box                          │   │
│   │                      "Laws of Physics for Data"                     │   │
│   │                                                                     │   │
│   │  "What kinds of things CAN exist in this domain?"                   │   │
│   │                                                                     │   │
│   │  COMPUTATION (normative):                                           │   │
│   │  • Validate OWL 2 RL ontologies                                     │   │
│   │  • Transpile OWL → Datalog rules                                    │   │
│   │  • Generate SHACL shapes from OWL                                   │   │
│   │  • Disambiguate namespace references                                │   │
│   │  • Classify and traverse hierarchies                                │   │
│   │  • Compare inference sets                                           │   │
│   │  • Sign and verify SHACL bundles                                    │   │
│   │                                                                     │   │
│   │  STATE / ORCHESTRATION / INTEGRATION (pluggable):                   │   │
│   │  • GraphStore, Cache, EventEmitter, etc. (§12)                      │   │
│   │                                                                     │   │
│   └───────────────────────────────────────────────────────────────────┬─┘   │
│                                                                       │     │
│                                instantiates + validates               │     │
│                                                                       ▼     │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                           Fandaws                                   │   │
│   │                         Assertion Box                               │   │
│   │                                                                     │   │
│   │  "Which specific things DO exist?"                                  │   │
│   │                                                                     │   │
│   │  • Instance data, asserted facts, provenance chains                 │   │
│   │  • Taint levels (L0-L5 per fact)                                    │   │
│   │  • LOCAL SHACL validation (shapes downloaded from W2Fuel)           │   │
│   │                                                                     │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│   MDRE queries both via unified interface; joins happen at MDRE level       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Ontological Foundations

### 2.1 BFO Alignment

W2Fuel maintains the **Basic Formal Ontology (BFO)** as its upper-level framework. All domain classes must align with BFO categories:

```
BFO Upper Level (maintained by W2Fuel)
══════════════════════════════════════

                           entity
                              │
              ┌───────────────┴───────────────┐
              │                               │
          continuant                      occurrent
       (exists in full                  (unfolds in
        at any moment)                     time)
              │                               │
    ┌─────────┼─────────┐           ┌────────┼────────┐
    │         │         │           │        │        │
independent dependent  spatial   process  temporal  spatiotemporal
continuant  continuant region             region      region
    │         │
  ┌─┴─┐     ┌─┴─┐
  │   │     │   │
material    quality  role  function  disposition
entity
```

### 2.2 CCO Integration

The **Common Core Ontologies (CCO)** provide intermediate abstractions between BFO and domain-specific classes:

| CCO Module | Typical Content | Example Domain Use |
|------------|-----------------|-------------------|
| Agent Ontology | Person, Organization, Role | Identity resolution |
| Artifact Ontology | Document, Instrument | Contract processing |
| Event Ontology | Act, Process, State | Workflow tracking |
| Information Entity | Information Content Entity | Knowledge graphs |
| Geospatial Ontology | Site, Region, Location | Property management |

### 2.3 Domain Ontologies

Domain-specific ontologies extend CCO for particular use cases:

```
Domain Ontology Structure
═════════════════════════

BFO (Upper)
    │
    └── CCO (Mid-level)
            │
            ├── RealEstate Ontology
            │     ├── Lease (extends cco:Agreement)
            │     ├── Property (extends cco:Facility)
            │     └── Tenant (extends cco:AgentRole)
            │
            ├── Automotive Ontology
            │     ├── Vehicle (extends cco:Artifact)
            │     ├── Financing (extends cco:Agreement)
            │     └── Dealership (extends cco:Organization)
            │
            └── Network Ontology
                  ├── NetworkDevice (extends cco:Artifact)
                  ├── IPAllocation (extends cco:InformationContentEntity)
                  └── DHCPLease (extends cco:Agreement)
```

---

## 3. OWL 2 RL Profile

### 3.1 Profile Selection Rationale

W2Fuel adopts **OWL 2 RL** as the normative profile.

| Profile | Complexity | Reasoning Strategy | W2Fuel Use |
|---------|------------|-------------------|------------|
| OWL 2 Full | Undecidable | N/A | ❌ |
| OWL 2 DL | NExpTime | Tableau | ❌ Authoring only |
| **OWL 2 RL** | **Polynomial** | **Datalog materialization** | **✅ Normative** |
| OWL 2 EL | Polynomial | Completion | ❌ Too limited |
| OWL 2 QL | Polynomial | Query rewriting | ❌ Wrong focus |

**Why OWL 2 RL:**

- Polynomial-time reasoning (tractable at any scale)
- Aligns with SHACL's Closed World semantics
- Supports rule-based inference via Datalog materialization
- Covers 95%+ of real-world ontology patterns
- **Deterministic**: same axioms always produce same inferences (no tableau non-determinism)

### 3.2 Supported Constructs

| Construct | OWL 2 RL Support | Notes |
|-----------|------------------|-------|
| `rdfs:subClassOf` | ✅ Full | Core hierarchy |
| `rdfs:subPropertyOf` | ✅ Full | Property hierarchy |
| `owl:equivalentClass` | ✅ Full | Class equivalence |
| `owl:disjointWith` | ✅ Full | Disjointness |
| `owl:allValuesFrom` | ✅ Full | Universal restrictions |
| `owl:hasValue` | ✅ Full | Value restrictions |
| `owl:maxCardinality 0/1` | ✅ Full | Limited cardinality |
| `owl:someValuesFrom` | ⚠️ Superclass only | RL restriction |
| `owl:unionOf` | ⚠️ Superclass only | RL restriction |
| `owl:cardinality > 1` | ❌ Not in OWL | Use SHACL instead |
| `owl:complementOf` | ❌ Not in OWL | Use SHACL instead |

### 3.3 Authoring in OWL 2 DL, Deploying as OWL 2 RL

Ontology authors may use full OWL 2 DL expressivity during design (e.g., Protégé with HermiT). The `validateOwlRl` function (§5.1) detects non-RL constructs and the `owlToShacl` function (§5.4) generates SHACL alternatives for them.

```
AUTHORING (design-time)           DEPLOYMENT (runtime)
═══════════════════════           ════════════════════

Write in OWL 2 DL          ──►   OWL 2 RL (for inference)
Use Protégé + HermiT              + Datalog rules
Full expressivity                  + SHACL shapes (for CWA validation)
                                   All generated by core functions
```

### 3.4 Non-RL Construct Handling

| Construct | Validation Behavior | SHACL Alternative |
|-----------|--------------------|--------------------|
| `owl:someValuesFrom` in subclass | WARN | `sh:qualifiedMinCount` |
| `owl:cardinality > 1` | WARN | `sh:minCount` / `sh:maxCount` |
| `owl:complementOf` | FAIL unless manual SHACL exists | Manual `sh:not` |
| `owl:unionOf` in subclass | WARN | `sh:or` |

---

## 4. Namespace Federation

### 4.1 The Disambiguation Problem

Different domains may use the same term for different concepts. W2Fuel provides context-aware disambiguation as a pure function over a namespace registry.

```
"Lease" can mean:

  RealEstate:Lease        Automotive:Lease       Network:Lease
  (rental agreement)      (financing)            (DHCP allocation)

  disambiguate("Lease", context, registry) → ranked candidates
```

### 4.2 Namespace Registry (JSON-LD Canonical Form)

The namespace registry is a JSON-LD document. It is loaded as input to disambiguation functions; it is not an ambient service.

```json
{
  "@context": {
    "w2fuel": "https://fnsr.spec/v2/w2fuel/",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
  },
  "@type": "w2fuel:NamespaceRegistry",
  "w2fuel:namespaces": [
    {
      "@type": "w2fuel:NamespaceEntry",
      "w2fuel:prefix": "realestate",
      "w2fuel:iri": "https://ontology.example.org/realestate#",
      "w2fuel:domainKeywords": ["property", "rental", "tenant", "landlord", "apartment", "housing"],
      "w2fuel:disambiguationHints": [
        {
          "@type": "w2fuel:Hint",
          "w2fuel:pattern": "rent|tenant|landlord|property management",
          "w2fuel:weight": 0.9
        },
        {
          "@type": "w2fuel:Hint",
          "w2fuel:pattern": "real estate|housing|apartment",
          "w2fuel:weight": 0.8
        }
      ]
    },
    {
      "@type": "w2fuel:NamespaceEntry",
      "w2fuel:prefix": "auto",
      "w2fuel:iri": "https://ontology.example.org/automotive#",
      "w2fuel:domainKeywords": ["vehicle", "car", "financing", "dealership", "monthly payment"],
      "w2fuel:disambiguationHints": [
        {
          "@type": "w2fuel:Hint",
          "w2fuel:pattern": "vehicle|car|automobile|dealership",
          "w2fuel:weight": 0.9
        }
      ]
    },
    {
      "@type": "w2fuel:NamespaceEntry",
      "w2fuel:prefix": "network",
      "w2fuel:iri": "https://ontology.example.org/networking#",
      "w2fuel:domainKeywords": ["DHCP", "IP address", "router", "configuration", "network"],
      "w2fuel:disambiguationHints": [
        {
          "@type": "w2fuel:Hint",
          "w2fuel:pattern": "DHCP|IP|router|network configuration",
          "w2fuel:weight": 0.95
        }
      ]
    }
  ]
}
```

### 4.3 Human-in-the-Loop Disambiguation

When automated confidence is below threshold (< 0.60), the disambiguation function returns a review request rather than a resolved result. How that review request is routed (ticketing system, email, UI prompt) is an integration concern handled by adapters.

```json
{
  "@type": "w2fuel:DisambiguationResult",
  "w2fuel:status": "review_required",
  "w2fuel:term": "Lease",
  "w2fuel:confidence": 0.45,
  "w2fuel:candidates": [
    { "w2fuel:class": "realestate:Lease", "w2fuel:confidence": 0.45 },
    { "w2fuel:class": "auto:Lease", "w2fuel:confidence": 0.38 }
  ],
  "w2fuel:reviewRequest": {
    "@type": "w2fuel:ReviewRequest",
    "w2fuel:requestId": "urn:uuid:...",
    "w2fuel:term": "Lease",
    "w2fuel:contextText": "...",
    "w2fuel:suggestedExpiry": "P7D"
  }
}
```

---

## 5. Core Computation Functions

All functions defined in this section are **deterministic** and **stateless**. Given the same inputs, they produce the same outputs. They require no network access, no databases, no ambient services. They are the normative core of W2Fuel.

All inputs and outputs use **JSON-LD** as the canonical representation. Internal representations (Turtle, N-Triples, native RDF objects) are permitted as implementation optimizations and must be losslessly derivable from the JSON-LD form.

### 5.1 Schema Validation

#### `validateOwlRl`

Validates an ontology graph for OWL 2 RL compliance.

**Signature:**
```
validateOwlRl(ontologyGraph: JSON-LD) → ValidationResult (JSON-LD)
```

**Input — `ontologyGraph`:**
A JSON-LD document containing OWL axioms. May be a single ontology or a merged graph with imports resolved.

**Output — `ValidationResult`:**
```json
{
  "@context": "https://fnsr.spec/v2/w2fuel/",
  "@type": "w2fuel:ValidationResult",
  "w2fuel:valid": true,
  "w2fuel:axiomCount": 142,
  "w2fuel:diagnostics": [],
  "w2fuel:nonRlConstructs": [
    {
      "@type": "w2fuel:NonRlReport",
      "w2fuel:axiomId": "realestate:Lease_someValuesFrom_1",
      "w2fuel:construct": "owl:someValuesFrom",
      "w2fuel:position": "subclass",
      "w2fuel:severity": "warning",
      "w2fuel:shaclAlternative": "sh:qualifiedMinCount 1",
      "w2fuel:sourceLocation": { "w2fuel:line": 45 }
    }
  ]
}
```

**Determinism guarantee:** Same `ontologyGraph` always produces same `ValidationResult`.

**Offline behavior:** Fully offline. No external dependencies.

#### `checkBfoCompliance`

Verifies that all classes in a domain ontology are properly anchored to BFO categories.

**Signature:**
```
checkBfoCompliance(ontologyGraph: JSON-LD, bfoGraph: JSON-LD) → ComplianceResult (JSON-LD)
```

**Output — `ComplianceResult`:**
```json
{
  "@type": "w2fuel:ComplianceResult",
  "w2fuel:compliant": true,
  "w2fuel:unanchoredClasses": [],
  "w2fuel:alignmentReport": [
    {
      "w2fuel:class": "realestate:Lease",
      "w2fuel:bfoAnchor": "bfo:BFO_0000015",
      "w2fuel:anchorLabel": "process",
      "w2fuel:pathLength": 3
    }
  ]
}
```

**Offline behavior:** Both graphs must be provided as input. If `bfoGraph` is absent or empty, returns `{ compliant: null, reason: "bfo_unavailable" }`.

#### `checkCcoAlignment`

Verifies CCO module alignment for a domain ontology.

**Signature:**
```
checkCcoAlignment(ontologyGraph: JSON-LD, ccoGraphs: JSON-LD[]) → AlignmentResult (JSON-LD)
```

**Offline behavior:** If any `ccoGraphs` entry is absent, reports `partial: true` and validates against available modules only.

### 5.2 Transpilation: OWL → Datalog

#### `owlToDatalog`

Transpiles OWL 2 RL axioms into Datalog rules suitable for materialization by any conforming Datalog engine.

**Signature:**
```
owlToDatalog(ontologyGraph: JSON-LD) → DatalogRuleSet (JSON-LD)
```

**Output — `DatalogRuleSet`:**
```json
{
  "@context": "https://fnsr.spec/v2/w2fuel/",
  "@type": "w2fuel:DatalogRuleSet",
  "w2fuel:generatedFrom": "realestate-v1.0",
  "w2fuel:rules": [
    {
      "@type": "w2fuel:DatalogRule",
      "@id": "w2fuel:rule_subclass_Employee_Person",
      "w2fuel:head": {
        "w2fuel:predicate": "rdf:type",
        "w2fuel:args": ["?x", "ex:Person"]
      },
      "w2fuel:body": [
        {
          "w2fuel:predicate": "rdf:type",
          "w2fuel:args": ["?x", "ex:Employee"]
        }
      ],
      "w2fuel:sourceAxiom": "ex:Employee rdfs:subClassOf ex:Person",
      "w2fuel:humanReadable": "Person(?x) :- Employee(?x) ."
    }
  ],
  "w2fuel:warnings": [],
  "w2fuel:ruleCount": 47
}
```

**Transpilation rules (normative):**

| OWL 2 RL Axiom | Datalog Rule |
|----------------|-------------|
| `A rdfs:subClassOf B` | `B(?x) :- A(?x) .` |
| `P rdfs:subPropertyOf Q` | `Q(?x,?y) :- P(?x,?y) .` |
| `A owl:equivalentClass B` | `B(?x) :- A(?x) .` and `A(?x) :- B(?x) .` |
| `P rdfs:domain C` | `C(?x) :- P(?x,?y) .` |
| `P rdfs:range C` | `C(?y) :- P(?x,?y) .` |
| `A rdfs:subClassOf (allValuesFrom P C)` | `C(?y) :- A(?x), P(?x,?y) .` |
| `A rdfs:subClassOf (hasValue P v)` | `P(?x, v) :- A(?x) .` |
| `P a owl:FunctionalProperty` | `sameAs(?y1,?y2) :- P(?x,?y1), P(?x,?y2) .` |
| `P owl:inverseOf Q` | `Q(?y,?x) :- P(?x,?y) .` and `P(?x,?y) :- Q(?y,?x) .` |
| `P a owl:TransitiveProperty` | `P(?x,?z) :- P(?x,?y), P(?y,?z) .` |

**Determinism guarantee:** Same `ontologyGraph` always produces same `DatalogRuleSet`. Rule ordering is lexicographic by rule `@id`.

**Offline behavior:** Fully offline. If the ontology contains unresolved imports, generates rules for resolved axioms only and sets `w2fuel:incomplete: true`.

### 5.3 Transpilation: OWL → SHACL

#### `owlToShacl`

Generates SHACL validation shapes from OWL 2 RL axioms, plus SHACL alternatives for non-RL constructs.

**Signature:**
```
owlToShacl(ontologyGraph: JSON-LD, manualShacl?: JSON-LD) → ShaclShapesResult (JSON-LD)
```

**Input — `manualShacl` (optional):**
Hand-authored SHACL shapes for constructs that require manual specification (e.g., `owl:complementOf` → `sh:not`). When provided, these are merged with generated shapes.

**Output — `ShaclShapesResult`:**
```json
{
  "@context": "https://fnsr.spec/v2/w2fuel/",
  "@type": "w2fuel:ShaclShapesResult",
  "w2fuel:shapesGraph": { "... JSON-LD SHACL shapes ..." },
  "w2fuel:generationMap": [
    {
      "w2fuel:shapeIri": "realestate:LeaseShape",
      "w2fuel:sourceAxioms": ["realestate:Lease rdfs:subClassOf cco:Agreement"]
    }
  ],
  "w2fuel:manualRequired": [],
  "w2fuel:shapeCount": 23
}
```

**OWL 2 RL → SHACL mapping (normative):**

| OWL 2 RL Construct | SHACL Output |
|--------------------|-------------|
| `rdfs:subClassOf` | `sh:targetClass` on superclass |
| `rdfs:range` (class) | `sh:class` |
| `rdfs:range` (datatype) | `sh:datatype` |
| `owl:allValuesFrom C` | `sh:class C` on property |
| `owl:hasValue v` | `sh:hasValue v` |
| `owl:maxCardinality 1` | `sh:maxCount 1` |
| `owl:FunctionalProperty` | `sh:maxCount 1` |

**Non-RL → SHACL mapping (normative):**

| Non-RL Need | SHACL Output |
|-------------|-------------|
| "At least one" (`owl:someValuesFrom`) | `sh:minCount 1` |
| "Exactly N" (`owl:cardinality N`) | `sh:minCount N` + `sh:maxCount N` |
| "Not a" (`owl:complementOf`) | `sh:not` (manual only) |
| "A or B" (`owl:unionOf`) | `sh:or` |

**Determinism guarantee:** Same inputs always produce same shapes graph. Shape ordering is lexicographic by shape IRI.

**Offline behavior:** Fully offline.

### 5.4 Reasoning: Datalog Materialization

#### `materialize`

Applies Datalog rules to a set of asserted facts, producing inferred triples. This function defines the **semantics** of materialization. Any conforming Datalog engine (Nemo, Datalog.js, a hand-written fixpoint loop) may implement it.

**Signature:**
```
materialize(rules: DatalogRuleSet (JSON-LD), facts: JSON-LD) → MaterializationResult (JSON-LD)
```

**Output — `MaterializationResult`:**
```json
{
  "@type": "w2fuel:MaterializationResult",
  "w2fuel:inferred": { "... JSON-LD inferred triples ..." },
  "w2fuel:inferredCount": 312,
  "w2fuel:ruleTrace": [
    {
      "w2fuel:inferredTriple": "ex:fido rdf:type ex:Animal",
      "w2fuel:byRules": ["w2fuel:rule_subclass_Dog_Animal"]
    }
  ],
  "w2fuel:partial": false,
  "w2fuel:fixpointReached": true
}
```

**Semantics:** Materialization proceeds by fixpoint iteration. Rules are applied until no new triples are derived. The result is the minimal model of the rules applied to the facts.

**Determinism guarantee:** Same rules + same facts always produce same inferred triples (modulo blank node identifiers, which are compared structurally).

**Offline behavior:** Fully offline. If `rules` has `w2fuel:incomplete: true`, the result carries `w2fuel:partial: true` to signal that additional inferences may exist.

### 5.5 Namespace Disambiguation

#### `disambiguate`

Resolves an ambiguous term to a namespace-qualified class using pattern matching and contextual signals.

**Signature:**
```
disambiguate(
  term: string,
  context: DisambiguationContext (JSON-LD),
  registry: NamespaceRegistry (JSON-LD)
) → DisambiguationResult (JSON-LD)
```

**Input — `DisambiguationContext`:**
```json
{
  "@type": "w2fuel:DisambiguationContext",
  "w2fuel:contextText": "The property management company said my lease expires next month",
  "w2fuel:contextEntities": [
    {
      "w2fuel:entity": "property management company",
      "w2fuel:resolvedType": "realestate:PropertyManager"
    }
  ]
}
```

**Output — `DisambiguationResult`:**
```json
{
  "@type": "w2fuel:DisambiguationResult",
  "w2fuel:status": "resolved",
  "w2fuel:term": "Lease",
  "w2fuel:resolvedClass": "realestate:Lease",
  "w2fuel:confidence": 0.94,
  "w2fuel:confidenceTier": "high",
  "w2fuel:reasoning": {
    "w2fuel:keywordMatch": 0.8,
    "w2fuel:entityContext": 0.95,
    "w2fuel:combined": 0.94
  },
  "w2fuel:alternatives": [
    { "w2fuel:class": "auto:Lease", "w2fuel:confidence": 0.12 },
    { "w2fuel:class": "network:Lease", "w2fuel:confidence": 0.02 }
  ]
}
```

**Confidence tiers:**

| Tier | Range | Behavior |
|------|-------|----------|
| `high` | ≥ 0.80 | Resolved automatically |
| `medium` | 0.60–0.79 | Resolved with advisory |
| `low` | < 0.60 | Returns `review_required` (see §4.3) |

**Determinism guarantee:** Same (term, context, registry) always produces same result.

**Offline behavior:** If `registry` is null or empty, returns `{ status: "unavailable", reason: "registry_not_loaded" }`. This is not an error — it is an explicit representation of uncertainty.

### 5.6 Schema Query Functions

These functions extract information from a loaded ontology graph. They are pure projections — no side effects, no state modification.

#### `resolveClass`

```
resolveClass(classIri: IRI, ontologyGraph: JSON-LD) → ClassDefinition (JSON-LD)
```

Returns the full definition of a class: its superclasses, properties, annotations, and associated SHACL shape (if shapes have been generated).

**Offline behavior:** If `classIri` is not found, returns `{ found: false, searchedGraph: "..." }`.

#### `resolveProperty`

```
resolveProperty(propertyIri: IRI, ontologyGraph: JSON-LD) → PropertyDefinition (JSON-LD)
```

Returns domain, range, superproperties, and characteristics (functional, transitive, etc.).

#### `getHierarchy`

```
getHierarchy(rootIri: IRI, ontologyGraph: JSON-LD, depth?: number) → HierarchyTree (JSON-LD)
```

Returns the class hierarchy rooted at `rootIri`, traversing `rdfs:subClassOf` relations. Optional `depth` parameter limits traversal.

### 5.7 Comparison & Testing Functions

#### `compareInferenceSets`

Compares two sets of inferred triples to detect semantic drift.

**Signature:**
```
compareInferenceSets(
  setA: JSON-LD,
  setB: JSON-LD,
  criticalInferences: Assertion[]
) → ParityReport (JSON-LD)
```

**Output — `ParityReport`:**
```json
{
  "@type": "w2fuel:ParityReport",
  "w2fuel:equivalent": false,
  "w2fuel:inANotB": ["..."],
  "w2fuel:inBNotA": ["..."],
  "w2fuel:criticalStatus": [
    {
      "w2fuel:assertion": "Every Continuant is an Entity",
      "w2fuel:status": "present"
    },
    {
      "w2fuel:assertion": "Property has exactly one address",
      "w2fuel:status": "moved_to_shacl"
    }
  ]
}
```

**Use case:** Validating that a migration (e.g., HermiT → Nemo, or OWL 2 DL → OWL 2 RL) preserves critical inferences.

#### `evaluateGoldenRules`

Runs canonical OWL→Datalog translation tests.

**Signature:**
```
evaluateGoldenRules(testCases: GoldenRuleTest[]) → TestReport (JSON-LD)
```

**Normative test cases:**

| Name | OWL Input | Expected Datalog | Round-Trip Validation |
|------|-----------|-----------------|----------------------|
| `subclass_simple` | `ex:Dog rdfs:subClassOf ex:Animal` | `Animal(?x) :- Dog(?x) .` | `ex:fido a ex:Dog` → infers `ex:fido a ex:Animal` |
| `subclass_chain` | `Poodle ⊂ Dog ⊂ Animal` | Two rules | `ex:p a ex:Poodle` → infers `ex:p a ex:Animal` |
| `domain_inference` | `ex:owns rdfs:domain ex:Person` | `Person(?x) :- owns(?x,?y) .` | `ex:j ex:owns ex:c` → infers `ex:j a ex:Person` |
| `range_inference` | `ex:owns rdfs:range ex:Asset` | `Asset(?y) :- owns(?x,?y) .` | `ex:j ex:owns ex:c` → infers `ex:c a ex:Asset` |
| `equivalent_class` | `ex:Human owl:equivalentClass ex:Person` | Bidirectional rules | Both directions infer |
| `all_values_from` | `VeganRestaurant ⊂ ∀servesFood.VeganFood` | `VeganFood(?y) :- VeganRestaurant(?x), servesFood(?x,?y) .` | Applied correctly |
| `has_value` | `USCitizen ⊂ ∃nationality.{USA}` | `nationality(?x, ex:USA) :- USCitizen(?x) .` | Applied correctly |
| `functional_property` | `ex:hasMother a owl:FunctionalProperty` | `sameAs(?y1,?y2) :- hasMother(?x,?y1), hasMother(?x,?y2) .` | Applied correctly |
| `inverse_property` | `ex:hasChild owl:inverseOf ex:hasParent` | Bidirectional rules | Both directions infer |
| `transitive_property` | `ex:ancestorOf a owl:TransitiveProperty` | `ancestorOf(?x,?z) :- ancestorOf(?x,?y), ancestorOf(?y,?z) .` | Chain infers |

### 5.8 Integrity Functions

#### `signShaclBundle`

Signs a SHACL shapes graph with an Ed25519 private key.

**Signature:**
```
signShaclBundle(shapesGraph: JSON-LD, privateKey: Uint8Array) → SignedBundle (JSON-LD)
```

**Output — `SignedBundle`:**
```json
{
  "@type": "w2fuel:SignedShaclBundle",
  "w2fuel:shapesGraph": { "..." },
  "w2fuel:signature": "ed25519:abc123def456...",
  "w2fuel:signedBy": "key:ed25519:w2fuel-signing-key-2026",
  "w2fuel:signedAt": "2026-02-01T15:30:00Z",
  "w2fuel:schemaVersion": "realestate-v1.0.3",
  "w2fuel:contentHash": "sha256:a1b2c3d4..."
}
```

**Determinism guarantee:** Same (shapesGraph, privateKey) always produces same signature bytes. Timestamp is an input parameter, not read from the environment.

Note: Key management (rotation, storage, revocation) is an integration concern. This function only performs the signing computation.

#### `verifyShaclSignature`

Verifies the signature on a signed SHACL bundle.

**Signature:**
```
verifyShaclSignature(signedBundle: SignedBundle (JSON-LD), publicKey: Uint8Array) → VerificationResult (JSON-LD)
```

**Offline behavior:** If the public key is unavailable (e.g., key server unreachable), returns `{ valid: null, reason: "key_unavailable" }`. This is not an error — it is explicit uncertainty. Consumers must decide their own policy for unverifiable bundles.

---

## 6. SHACL Dual Semantics

W2Fuel generates both OWL 2 RL rules (for inference) and SHACL shapes (for validation). These operate under complementary semantics:

```
OWL 2 RL (Open World)             SHACL (Closed World)
═══════════════════════           ═══════════════════════

"What COULD be true?"             "What MUST be present?"

• Inference rules                 • Validation rules
• If data missing → unknown       • If data missing → violation
• Used by: MDRE, materialization  • Used by: Fandaws, TagTeam (edge)

With OWL 2 RL, the semantics are MORE ALIGNED:
• RL rules produce deterministic inferences
• SHACL validates those inferences
• No "what could theoretically exist" uncertainty
```

**Consumers download SHACL bundles and validate locally.** The shapes graph is the contract between W2Fuel (T-Box) and edge validators (Fandaws, TagTeam). Consumers **MUST** verify bundle signatures before use (§5.8).

---

## 7. Event Semantic Contract

This section defines the **semantic content** of W2Fuel's schema update event — what information it carries about what changed. How the event is transported (Kafka, postMessage, file write, webhook) is an integration concern handled by the EventEmitter adapter (§12).

### 7.1 Schema Updated Event (Normative)

```json
{
  "@context": {
    "fnsr": "https://fnsr.spec/v2/",
    "w2fuel": "https://fnsr.spec/v2/w2fuel/",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
  },
  "@type": "fnsr:SchemaUpdatedEvent",
  "@id": "urn:uuid:550e8400-e29b-41d4-a716-446655440000",

  "fnsr:sequenceId": 42,
  "fnsr:timestamp": "2026-02-01T15:30:00Z",

  "w2fuel:updateType": "minor",
  "w2fuel:breaking": false,
  "w2fuel:affectedNamespaces": ["realestate"],

  "w2fuel:versionInfo": {
    "@type": "w2fuel:VersionTransition",
    "w2fuel:previousVersion": "1.0.0",
    "w2fuel:newVersion": "1.1.0",
    "w2fuel:sourceIdentifier": "abc123def456"
  },

  "w2fuel:verificationStatus": "verified",
  "w2fuel:shaclBundleHash": "sha256:a1b2c3d4e5f6789..."
}
```

**What is NOT in this event:** Infrastructure state (database committed, cache invalidated, broker acked). Those are orchestration concerns that belong in adapter-layer telemetry, not in the semantic event. Consumers react to *what changed*, not to *how it was deployed*.

### 7.2 Verification Status

| Status | Meaning |
|--------|---------|
| `verified` | Full Datalog classification passed, SHACL generated |
| `lite` | Syntax-only validation (classification disabled for this namespace) |
| `partial` | Ontology had unresolved imports; verified against available content |

### 7.3 Consumer Semantics

| Status | TagTeam | MDRE | Fandaws |
|--------|---------|------|---------|
| `verified` | Extract entities normally | Load schema, materialize via Datalog | Validate with SHACL, reject non-conformant |
| `lite` | Extract normally | Load schema, explicit axioms only (no inference) | Validate with SHACL normally |
| `partial` | Extract with caution flag | Load schema, `partial: true` on inferences | Validate with available SHACL |

### 7.4 Idempotent Event Processing

Consumers process events idempotently using `sequenceId`:

| Rule | Behavior |
|------|----------|
| R1 | If `sequenceId` ≤ last processed → IGNORE (duplicate) |
| R2 | If `sequenceId` == last processed + 1 → PROCESS normally |
| R3 | If `sequenceId` > last processed + 1 → PROCESS, log gap warning |
| R4 | Store `lastProcessedSequenceId` durably before processing |
| R5 | On restart, sync from authoritative source |

How `lastProcessedSequenceId` is stored (Redis, file, localStorage, in-memory) is a State adapter concern.

### 7.5 Event Construction Function

Event construction is itself a pure function:

```
constructSchemaEvent(
  previousVersion: SemVer,
  newVersion: SemVer,
  affectedNamespaces: string[],
  verificationResult: ValidationResult,
  shaclBundleHash: string,
  sequenceId: number,
  timestamp: string,
  sourceIdentifier: string
) → SchemaUpdatedEvent (JSON-LD)
```

**Determinism guarantee:** Same inputs always produce same event. `timestamp` and `sequenceId` are explicit parameters, not read from the environment.

---

## 8. Governance

### 8.1 Change Classification (Computation)

Change classification is a deterministic function over the ontology diff:

```
classifyChange(previousGraph: JSON-LD, newGraph: JSON-LD) → ChangeClassification (JSON-LD)
```

| Change Type | Detection Rule | Required Approval |
|-------------|---------------|-------------------|
| `patch` | Annotations only; no axiom changes | Auto |
| `minor` | New classes/properties; no removals; no axiom modifications | Domain Steward |
| `major` | Removed classes/properties; modified axioms; breaking changes | Governance Body |

**Output:**
```json
{
  "@type": "w2fuel:ChangeClassification",
  "w2fuel:changeType": "minor",
  "w2fuel:breaking": false,
  "w2fuel:addedClasses": ["realestate:SubLease"],
  "w2fuel:removedClasses": [],
  "w2fuel:modifiedAxioms": [],
  "w2fuel:requiredApproval": "domain_steward"
}
```

How approval is obtained (GitHub PR review, email chain, governance meeting) is an orchestration concern.

### 8.2 Bridge Ontologies

Version migration bridges are OWL equivalence mappings:

```json
{
  "@context": { "owl": "http://www.w3.org/2002/07/owl#" },
  "@type": "w2fuel:BridgeOntology",
  "w2fuel:from": "realestate-v1",
  "w2fuel:to": "realestate-v2",
  "w2fuel:mappings": [
    {
      "owl:equivalentClass": [
        { "@id": "realestate-v1:RentalProperty" },
        { "@id": "realestate-v2:ResidentialLease" }
      ]
    },
    {
      "owl:equivalentProperty": [
        { "@id": "realestate-v1:monthlyRent" },
        { "@id": "realestate-v2:rentAmount" }
      ]
    }
  ]
}
```

Bridge ontologies are processed by the same `owlToDatalog` and `owlToShacl` functions as any other ontology.

### 8.3 RBAC Model

The role model defines *what operations exist* and *who can perform them*. How authentication is implemented (OAuth, JWT, API key, local trust) is an integration adapter concern.

| Role | Permissions |
|------|-------------|
| `anonymous` | Health/status queries only |
| `authenticated_service` | Read, query, SHACL download |
| `schema_author` | Submit schema change proposals |
| `domain_steward` | Approve `minor` changes within their namespace |
| `ontology_steward` | Cross-namespace changes |
| `operator` | Administrative operations |
| `governance_body` | All permissions |

---

## 9. Validation Pipeline (Computation)

The validation pipeline is a **composition of core functions** applied in sequence. This section defines the logical ordering and pass/fail semantics. How the pipeline is triggered (CI/CD, manual invocation, file watcher) is an orchestration concern.

### 9.1 Pipeline Stages

```
INPUT: ontologyGraph (JSON-LD), bfoGraph (JSON-LD), ccoGraphs (JSON-LD[])
       previousGraph? (JSON-LD), manualShacl? (JSON-LD)

STAGE 1: Syntax Validation
  validateOwlRl(ontologyGraph)
  → If not valid: FAIL with diagnostics

STAGE 2: Compliance
  checkBfoCompliance(ontologyGraph, bfoGraph)
  checkCcoAlignment(ontologyGraph, ccoGraphs)
  → If not compliant: FAIL with report

STAGE 3: Transpilation
  owlToDatalog(ontologyGraph)
  owlToShacl(ontologyGraph, manualShacl)
  → Produces DatalogRuleSet and ShaclShapesResult

STAGE 4: Classification
  materialize(datalogRules, ontologyGraph)
  → Check: no unsatisfiable classes in result
  → If inconsistent: FAIL

STAGE 5: Golden-Rule Tests
  evaluateGoldenRules(canonicalTestCases)
  → If any fail: FAIL (transpilation bug)

STAGE 6: Inference Parity (if previousGraph provided)
  materialize(previousRules, ontologyGraph)  → setA
  materialize(newRules, ontologyGraph)        → setB
  compareInferenceSets(setA, setB, criticalInferences)
  → If critical inferences lost: FAIL

STAGE 7: Change Classification (if previousGraph provided)
  classifyChange(previousGraph, ontologyGraph)
  → Produces ChangeClassification for governance routing

STAGE 8: Bundle Signing
  signShaclBundle(shapesGraph, signingKey)
  → Produces SignedBundle

STAGE 9: Event Construction
  constructSchemaEvent(...)
  → Produces SchemaUpdatedEvent (JSON-LD)

OUTPUT: PipelineResult containing all intermediate artifacts
```

Every stage is a pure function call. The pipeline itself is a pure composition. No network access, no database writes, no event emission occurs *within* the pipeline. The resulting artifacts (DatalogRuleSet, SignedBundle, SchemaUpdatedEvent) are returned as JSON-LD and can then be handed to adapters for persistence, distribution, and notification.

### 9.2 Pipeline as Function

```
runValidationPipeline(
  ontologyGraph: JSON-LD,
  bfoGraph: JSON-LD,
  ccoGraphs: JSON-LD[],
  previousGraph?: JSON-LD,
  manualShacl?: JSON-LD,
  signingKey?: Uint8Array,
  sequenceId: number,
  timestamp: string,
  sourceIdentifier: string
) → PipelineResult (JSON-LD)
```

**Output — `PipelineResult`:**
```json
{
  "@type": "w2fuel:PipelineResult",
  "w2fuel:status": "passed",
  "w2fuel:stages": [
    { "w2fuel:stage": "syntax_validation", "w2fuel:status": "passed", "w2fuel:durationMs": 45 },
    { "w2fuel:stage": "compliance", "w2fuel:status": "passed", "w2fuel:durationMs": 23 },
    { "w2fuel:stage": "transpilation", "w2fuel:status": "passed", "w2fuel:durationMs": 78 },
    { "w2fuel:stage": "classification", "w2fuel:status": "passed", "w2fuel:durationMs": 120 },
    { "w2fuel:stage": "golden_rules", "w2fuel:status": "passed", "w2fuel:durationMs": 15 },
    { "w2fuel:stage": "inference_parity", "w2fuel:status": "passed", "w2fuel:durationMs": 230 },
    { "w2fuel:stage": "change_classification", "w2fuel:status": "passed", "w2fuel:durationMs": 12 },
    { "w2fuel:stage": "bundle_signing", "w2fuel:status": "passed", "w2fuel:durationMs": 5 },
    { "w2fuel:stage": "event_construction", "w2fuel:status": "passed", "w2fuel:durationMs": 1 }
  ],
  "w2fuel:artifacts": {
    "w2fuel:validationResult": { "..." },
    "w2fuel:datalogRuleSet": { "..." },
    "w2fuel:shaclShapesResult": { "..." },
    "w2fuel:signedBundle": { "..." },
    "w2fuel:changeClassification": { "..." },
    "w2fuel:schemaUpdatedEvent": { "..." },
    "w2fuel:parityReport": { "..." }
  }
}
```

---

## 10. Offline Behavior Summary

Inability to reach external systems is not an error state. Every core function defines explicit behavior for degraded conditions:

| Function | Degraded Condition | Behavior |
|----------|-------------------|----------|
| `validateOwlRl` | Unresolved imports | Validate available axioms; report `unresolvedImport` |
| `checkBfoCompliance` | BFO graph absent | Return `{ compliant: null, reason: "bfo_unavailable" }` |
| `checkCcoAlignment` | Some CCO modules absent | Validate against available; `partial: true` |
| `owlToDatalog` | Incomplete ontology | Generate available rules; `incomplete: true` |
| `owlToShacl` | Missing manual SHACL | Generate auto shapes; report `manualRequired` |
| `materialize` | Incomplete rules | Materialize available; `partial: true` |
| `disambiguate` | Registry not loaded | Return `{ status: "unavailable", reason: "registry_not_loaded" }` |
| `resolveClass` | Class not in graph | Return `{ found: false }` |
| `verifyShaclSignature` | Key unavailable | Return `{ valid: null, reason: "key_unavailable" }` |
| `constructSchemaEvent` | Missing fields | Construct with available; `partial: true` |

**Principle:** Every function returns a well-typed JSON-LD result even under degraded conditions. Null, undefined, and thrown exceptions are replaced with explicit uncertainty representations. Consumers decide their own tolerance policy.

---

## 11. JSON-LD Canonical Representation

### 11.1 Principle

JSON-LD is the authoritative format for all inputs, outputs, configuration, and inter-component contracts. Alternative representations (Turtle, N-Triples, SPARQL result sets, Datalog text) are permitted as internal optimizations and must be losslessly derivable from the JSON-LD form.

### 11.2 Base Context

All W2Fuel JSON-LD documents share a base context:

```json
{
  "@context": {
    "w2fuel": "https://fnsr.spec/v2/w2fuel/",
    "fnsr": "https://fnsr.spec/v2/",
    "bfo": "http://purl.obolibrary.org/obo/BFO_",
    "cco": "http://www.ontologyrepository.com/CommonCoreOntologies/",
    "owl": "http://www.w3.org/2002/07/owl#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "sh": "http://www.w3.org/ns/shacl#",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
  }
}
```

### 11.3 Format Derivation Table

| Format | Canonical JSON-LD Type | Derivation |
|--------|----------------------|------------|
| OWL/Turtle ontology | JSON-LD `@graph` with OWL vocabulary | Standard RDF serialization conversion |
| SHACL/Turtle shapes | JSON-LD `@graph` with SHACL vocabulary | Standard RDF serialization conversion |
| Datalog rules (text) | `w2fuel:DatalogRuleSet` with `humanReadable` per rule | `humanReadable` is a text projection of the JSON-LD rule structure |
| Namespace registry (YAML) | `w2fuel:NamespaceRegistry` (see §4.2) | Direct structural mapping |
| Schema event (bare JSON) | `fnsr:SchemaUpdatedEvent` (see §7.1) | Add `@context` and `@type` |
| SPARQL result set | JSON-LD per W3C SPARQL Results JSON format | Standard mapping |

---

## 12. Adapter Boundaries

This section defines the **interfaces** through which W2Fuel's core computation connects to state, orchestration, and integration concerns. Each adapter has a minimal interface and a **default implementation** suitable for browser and Node.js execution. Server-optimized implementations are non-normative.

### 12.1 Design Principle

Core computation functions (§5) never call adapters directly. Orchestration code wires computation outputs to adapter inputs. This ensures that all core functions remain testable in isolation with no mocking required.

```
ORCHESTRATION wires:
  computation output ──► state adapter (persist)
  computation output ──► integration adapter (distribute)
  state adapter output ──► computation input (resume)
```

### 12.2 State Adapters

#### GraphStore

Stores and queries RDF graph data.

| Method | Signature | Purpose |
|--------|-----------|---------|
| `load` | `(graph: JSON-LD) → void` | Load triples into store |
| `query` | `(sparqlOrPattern: string) → JSON-LD` | Query stored triples |
| `update` | `(additions: JSON-LD, removals: JSON-LD) → void` | Atomic update |
| `export` | `() → JSON-LD` | Export all triples |

| Implementation | Environment | Notes |
|---------------|-------------|-------|
| **In-memory (default)** | Browser, Node.js | Uses rdf-ext, N3.js, or Oxigraph-WASM |
| Oxigraph server | Server | RocksDB-backed, persistent |
| Apache Jena Fuseki | Server (legacy) | Java-based |

#### Cache

Caches computation results to avoid redundant work.

| Method | Signature | Purpose |
|--------|-----------|---------|
| `get` | `(key: string) → JSON-LD \| null` | Retrieve cached value |
| `set` | `(key: string, value: JSON-LD, ttlMs?: number) → void` | Store with optional TTL |
| `invalidate` | `(prefix: string) → void` | Remove entries by key prefix |

| Implementation | Environment | Notes |
|---------------|-------------|-------|
| **`Map` (default)** | Browser, Node.js | In-memory, no TTL enforcement |
| Redis | Server | Persistent, TTL, distributed |

#### SequenceStore

Maintains the monotonically increasing sequence counter for events.

| Method | Signature | Purpose |
|--------|-----------|---------|
| `getCurrent` | `() → number` | Current sequence value |
| `getNext` | `() → number` | Atomically increment and return |

| Implementation | Environment | Notes |
|---------------|-------------|-------|
| **Counter variable (default)** | Browser, Node.js | In-memory, resets on restart |
| Redis INCR | Server | Persistent, atomic |
| File-based | Node.js | Persistent, single-process |

### 12.3 Integration Adapters

#### EventEmitter

Distributes schema update events to downstream consumers.

| Method | Signature | Purpose |
|--------|-----------|---------|
| `emit` | `(event: JSON-LD) → Ack` | Publish event to consumers |

| Implementation | Environment | Notes |
|---------------|-------------|-------|
| **Callback / `postMessage` (default)** | Browser, Node.js | In-process or cross-frame |
| Kafka | Server | Distributed, persistent |
| NATS | Server | Lightweight |
| File append | Node.js | Append JSON-LD to newline-delimited file |

#### AuthProvider

Authenticates and authorizes requests.

| Method | Signature | Purpose |
|--------|-----------|---------|
| `authenticate` | `(credentials: any) → Identity` | Verify identity |
| `authorize` | `(identity: Identity, action: string) → boolean` | Check permission |

| Implementation | Environment | Notes |
|---------------|-------------|-------|
| **No-op / local trust (default)** | Browser, Node.js | All actions permitted |
| OAuth 2.0 + JWT | Server | Production auth |

#### SecretsProvider

Provides cryptographic keys and other secrets.

| Method | Signature | Purpose |
|--------|-----------|---------|
| `getSigningKey` | `() → Uint8Array` | Private key for SHACL signing |
| `getVerificationKeys` | `() → Uint8Array[]` | Public keys for verification |

| Implementation | Environment | Notes |
|---------------|-------------|-------|
| **Environment variable / file (default)** | Node.js | Load from `process.env` or file |
| **Hardcoded test key (default)** | Browser | For development only |
| HashiCorp Vault | Server | Production secrets management |

#### NotificationSink

Emits operational alerts.

| Method | Signature | Purpose |
|--------|-----------|---------|
| `notify` | `(alert: JSON-LD) → void` | Send alert |

| Implementation | Environment | Notes |
|---------------|-------------|-------|
| **`console.warn` (default)** | Browser, Node.js | Log to console |
| Slack / PagerDuty | Server | Production alerting |

#### MetricsSink

Records performance and health metrics.

| Method | Signature | Purpose |
|--------|-----------|---------|
| `record` | `(metric: string, value: number, tags?: object) → void` | Record metric |

| Implementation | Environment | Notes |
|---------------|-------------|-------|
| **No-op (default)** | Browser, Node.js | Discard metrics |
| Prometheus / Datadog | Server | Production observability |

### 12.4 Orchestration Adapters

#### Pipeline

Executes a sequence of computation stages.

| Method | Signature | Purpose |
|--------|-----------|---------|
| `run` | `(stages: Stage[]) → PipelineResult` | Execute pipeline |

| Implementation | Environment | Notes |
|---------------|-------------|-------|
| **Sequential `await` (default)** | Browser, Node.js | Simple loop |
| GitHub Actions / GitLab CI | Server | CI/CD integration |

#### TransactionManager

Provides atomicity guarantees for multi-step state updates.

| Method | Signature | Purpose |
|--------|-----------|---------|
| `begin` | `() → Transaction` | Start transaction |
| `commit` | `(tx: Transaction) → void` | Commit |
| `rollback` | `(tx: Transaction) → void` | Rollback |

| Implementation | Environment | Notes |
|---------------|-------------|-------|
| **No-op (default)** | Browser, Node.js | In-memory state is inherently atomic |
| Oxigraph transactions | Server | ACID guarantees |

---

## 13. Open Design Decisions

The following decisions were made during this refactor. They are recorded here for governance review and may be revisited.

### 13.1 Engine Abstraction

**Decision:** Core specifies Datalog *semantics* abstractly. Nemo, Oxigraph-WASM, Datalog.js, or any conforming engine may implement `materialize()`.

**Rationale:** The Edge-Canonical principle requires that core logic run in a browser. Nemo-WASM and Oxigraph-WASM exist but binding the spec to specific Rust toolchains creates a coupling between core logic and a deployment choice. The computation is the Datalog fixpoint semantics, not the engine.

**Trade-off:** Conformance testing across engines is required to ensure equivalent results. The `evaluateGoldenRules` and `compareInferenceSets` functions provide this.

### 13.2 SPARQL as Adapter, Not Core

**Decision:** SPARQL is the query language for the GraphStore adapter, not a core computation format. Core functions accept and return JSON-LD. SPARQL queries appear only in adapter implementations.

**Rationale:** SPARQL assumes a queryable graph store, which is infrastructure. Core functions operate over JSON-LD graphs directly. If an implementation uses SPARQL internally (e.g., Oxigraph adapter), that is an optimization.

### 13.3 Event Infrastructure Fields Removed

**Decision:** The `infrastructure_state` and `ci_verification` fields from v1.3.1's event contract are removed from the normative event schema. They belong in adapter-layer telemetry.

**Rationale:** The Separation of Concerns principle requires that events carry semantic content only. Consumers react to *what changed*, not to *how it was deployed*. Adapter-layer enrichment is permitted for operational visibility.

### 13.4 Governance Classification as Computation

**Decision:** `classifyChange()` is a core computation function. Approval routing is an orchestration concern.

**Rationale:** The classification itself (PATCH/MINOR/MAJOR) is a deterministic function of the diff. How approval is obtained is deployment-specific. Separating these allows the same classification logic to be used in CI/CD, local development, and manual review.

### 13.5 Signing Timestamp as Parameter

**Decision:** `signShaclBundle()` takes `timestamp` as an explicit parameter rather than reading `Date.now()`.

**Rationale:** The Determinism Over Deployment principle requires that same inputs produce same outputs. Reading system time is environment-coupled behavior. The orchestration layer provides the timestamp.

---

## Appendix A: OWL 2 RL Compliance Checker

A reference implementation of `validateOwlRl` as a command-line tool:

```
w2fuel-rl-check ontology.jsonld

# Output:
# ✓ 142 axioms checked
# ✓ 138 axioms are OWL 2 RL compliant
# ⚠ 4 axioms require SHACL alternative:
#   - owl:someValuesFrom in subclass → use sh:minCount 1
#   - owl:cardinality 2 → use sh:minCount 2 + sh:maxCount 2
#   - owl:unionOf in subclass → use sh:or
#   - owl:complementOf → use sh:not
```

The checker consumes JSON-LD and produces a `ValidationResult` (§5.1).

---

## Appendix B: Manual SHACL Cookbook

Templates for constructs that require hand-authored SHACL (merged via the `manualShacl` parameter of `owlToShacl`):

**Complement (NOT):**
```json
{
  "@type": "sh:NodeShape",
  "sh:targetClass": { "@id": "ex:NonEmployee" },
  "sh:not": {
    "sh:class": { "@id": "ex:Employee" }
  }
}
```

**Disjunction (OR):**
```json
{
  "@type": "sh:NodeShape",
  "sh:targetClass": { "@id": "ex:StaffMember" },
  "sh:or": {
    "@list": [
      { "sh:class": { "@id": "ex:FullTime" } },
      { "sh:class": { "@id": "ex:PartTime" } }
    ]
  }
}
```

**Exact cardinality:**
```json
{
  "@type": "sh:PropertyShape",
  "sh:path": { "@id": "ex:hasAddress" },
  "sh:minCount": 1,
  "sh:maxCount": 1
}
```

---

## Appendix C: Companion Documents

This specification is the normative core. Two companion documents provide additional guidance:

| Document | Content | Status |
|----------|---------|--------|
| **`w2fuel-adapters-01`** | Detailed adapter implementation guides; reference implementations for browser, Node.js, and server environments; conformance test suites | Planned |
| **`w2fuel-deploy-01`** | Production deployment guide covering Oxigraph, Redis, Kafka, Kubernetes, HA/DR, monitoring, CI/CD pipeline configuration, migration procedures, and operational runbooks. Contains all infrastructure content from v1.3.1. | Planned |

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0-draft | 2026-02-01 | Aaron / Claude | Initial specification |
| 1.1.0 | 2026-02-01 | Aaron / Claude | SHACL, CI/CD, bridges, disambiguation |
| 1.2.0 | 2026-02-01 | Aaron / Claude | Production hardening |
| 1.2.3 | 2026-02-02 | Aaron / Claude | Final v1.2.x (Java stack) |
| 1.3.0-draft | 2026-02-02 | Aaron / Claude | Rust stack adoption (Oxigraph/Nemo) |
| 1.3.1 | 2026-02-02 | Aaron / Claude | HA/DR, inference parity, runbooks |
| **2.0.0** | **2026-02-19** | **Aaron / Claude** | **Architectural alignment refactor: separated computation from infrastructure; JSON-LD canonical; edge-canonical execution; offline behavior contracts; adapter boundaries** |

---

*End of Core Specification*
