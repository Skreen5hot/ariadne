# Analogical Precedent Service (APS) Specification

**Document ID:** `aps-core-01`
**Version:** 1.1.0
**Status:** Draft
**Last Updated:** 2026-02-05

-----

## Executive Summary

The Analogical Precedent Service (APS) is the FNSR ecosystem’s capacity for *wisdom*—the accumulation of reasoning experience into a searchable, structurally-aware case library. When MDRE or IEE encounters a reasoning challenge and asks “have we seen a case like this before?”, APS searches a library of historical reasoning graphs and returns ranked analogical matches with similarity scores and provenance chains.

APS does not determine outcomes. Precedents are always advisory—they inform but never bind. This is a deliberate architectural choice: a system that is bound by precedent ossifies. A system that ignores precedent is foolish. APS occupies the disciplined middle ground: it remembers, it compares, it advises, and it defers.

The core computational challenge is *hybrid* similarity over reasoning graphs. Two cases may share surface-level features (same entity types, same predicates) without being genuinely analogous, or they may be deeply analogous while sharing almost no surface vocabulary. APS addresses this through a dual embedding strategy: reasoning graphs are projected into a vector space via Graph Neural Networks (GNNs) that capture both structural topology and semantic content, and similarity is computed as vector distance—a measure of structural *and* semantic resemblance.

This specification defines APS as a pure computational function. It embeds graphs, indexes embeddings, queries by hybrid similarity, and returns ranked precedents. It requires no infrastructure, runs in any JavaScript environment, and produces deterministic results from identical inputs.

### Changes in v1.1.0

- Added hybrid embedding: semantic content vectors in node initialization (§4.2.2, Phase 1) to prevent purely structural false positives (the “cake vs. pipe bomb” problem)
- Defined training objective: contrastive learning with hard negative mining (§4.4), closing the “magic weights” gap
- Clarified alignment algorithm as greedy O(V²) heuristic, not exact subgraph isomorphism (§6.2.1)
- Added WebAssembly as normative accelerator option for APSArithmetic (§1.3.2)
- Added schema evolution and case migration strategy (§8.5)
- Added negative feedback mechanism for precedent quality (§8.6)
- Added cold start bootstrap protocol (§8.7)
- Added precedent strength tracking (§10.4), promoted from “future consideration”
- Added cross-platform determinism CI matrix (§1.3.3)
- Updated performance estimates to reflect hybrid embedding costs (§11.2)
- Added semantic safety tests for content-divergent structurally-similar graphs (§13.2)

-----

## 1. Foundational Principles

### 1.1 Wisdom, Not Authority

Human legal systems oscillate between precedent-as-binding (*stare decisis*) and precedent-as-advisory. FNSR makes an explicit architectural choice: precedents are never binding. APS returns candidates; the consuming service (MDRE, IEE) decides what weight to assign.

This is not a concession. It is the correct epistemic posture. Analogies are structurally informative but never deductively valid—the inference from “case A resembled case B, and case B had outcome X” to “case A should have outcome X” is always defeasible. APS encodes this defeasibility in its output format: every precedent match carries a similarity score, a structural alignment map, and explicit documentation of where the analogy breaks down (disanalogy annotation).

### 1.2 Edge-Canonical Execution

APS must execute identically whether running:

- In a browser tab
- Via `node index.js`
- As part of a larger orchestrated system

The specification describes computation, not deployment. All infrastructure concerns (persistence, distribution, scheduling) are adapter responsibilities, not core requirements.

The GNN embedding, the vector index, and the case library are all representable as JSON-LD structures and serializable to disk. No external database is required. A developer can load a case library from a JSON file, embed a query graph, and retrieve precedents using nothing but a local Node.js runtime.

### 1.3 Determinism

Given:

- The same query reasoning graph (as JSON-LD)
- The same case library state
- The same GNN model weights

APS **must** produce the same ranked precedent list. Non-determinism in precedent retrieval would make analogical reasoning unreproducible—two runs of the same query would yield different advice, undermining trust in the system’s judgment.

#### 1.3.1 Deterministic Arithmetic

APS inherits the CSS deterministic arithmetic requirement. All vector computations (dot products, distance calculations, softmax normalization) MUST use deterministic arithmetic that produces bit-identical results across conforming JavaScript environments.

```typescript
interface APSArithmetic {
  /**
   * Precision: IEEE 754 double-precision is acceptable for vector operations
   * where bit-identical reproducibility across platforms is ensured through:
   * 1. Fixed operation ordering (no platform-dependent reordering)
   * 2. Explicit intermediate rounding at declared precision boundaries
   * 3. No fused multiply-add (FMA) unless explicitly opted in
   *
   * For similarity scores presented to consumers, round to 6 decimal places.
   */
  dot(a: Float64Array, b: Float64Array): number;
  cosine(a: Float64Array, b: Float64Array): number;
  euclidean(a: Float64Array, b: Float64Array): number;
  normalize(v: Float64Array): Float64Array;

  /**
   * Matrix multiplication for GNN message passing.
   *
   * @param A - Matrix as flat Float64Array (row-major), shape [m, k]
   * @param B - Matrix as flat Float64Array (row-major), shape [k, n]
   * @param m - Rows of A
   * @param k - Shared dimension
   * @param n - Columns of B
   * @returns Result matrix as flat Float64Array (row-major), shape [m, n]
   *
   * Operation order: canonical row-by-column with left-to-right accumulation.
   * No Strassen, no Winograd, no platform-dependent reordering.
   */
  matmul(A: Float64Array, B: Float64Array, m: number, k: number, n: number): Float64Array;

  /**
   * Element-wise ReLU activation.
   */
  relu(v: Float64Array): Float64Array;
}
```

**Rationale**: Unlike CSS (which performs iterative causal computations where rounding errors accumulate), APS performs primarily linear algebra over frozen embeddings. IEEE 754 double-precision with operation-order constraints is sufficient for reproducibility. If future analysis reveals divergence, the system can upgrade to decimal128 without breaking the interface.

#### 1.3.2 WebAssembly Acceleration

**[NEW IN v1.1]** Pure JavaScript matrix multiplication is O(N³) with high constant factors due to interpreter overhead. For the GNN forward pass (4 rounds of message passing across up to 500 nodes), this can push against the 50ms embedding budget on constrained devices.

WebAssembly (WASM) is a **normative accelerator option** for APSArithmetic:

```typescript
interface APSArithmeticProvider {
  /**
   * Select the arithmetic implementation based on environment capabilities.
   *
   * Selection order:
   * 1. WASM module (if available and loaded)
   * 2. Pure JavaScript fallback (always available)
   *
   * Both implementations MUST produce bit-identical results.
   * The WASM module is an optimization of the same algorithm,
   * not a different algorithm.
   */
  select(): APSArithmetic;

  /**
   * Verify that the WASM module produces identical results
   * to the JS fallback for a test vector suite.
   *
   * Run at initialization; reject the WASM module if verification fails.
   */
  verifyEquivalence(testVectors: TestVectorSuite): boolean;
}
```

**Constraints on WASM implementations:**

1. The WASM module MUST implement the same canonical operation ordering as the JS fallback.
1. The WASM module MUST NOT use SIMD instructions that reorder floating-point operations (e.g., horizontal add with different accumulation order).
1. The WASM module MUST pass the `verifyEquivalence` check against the JS reference before being used in production.
1. The WASM binary MUST be loadable from a local file or inline base64 (no network fetch required).
1. WebGPU is explicitly **not permitted** for core computation due to non-deterministic scheduling across GPU architectures. WebGPU may be used only behind an adapter boundary for non-normative batch preprocessing.

**Rationale**: WASM provides 10-50x speedup over pure JS for dense matrix operations while maintaining determinism guarantees. It runs in both browsers and Node.js (via `@aspect-build/rules_js` or native WASM support). This closes the feasibility gap identified in the v1.0 review without violating edge-canonical constraints.

#### 1.3.3 Cross-Platform Determinism Verification

**[NEW IN v1.1]** Conforming implementations MUST pass a cross-platform determinism CI matrix:

```json
{
  "@type": "aps:DeterminismCIMatrix",
  "aps:description": "All cells must produce bit-identical output for the reference test suite",
  "aps:environments": [
    { "runtime": "Node.js 18", "arch": "x86_64", "os": "Linux" },
    { "runtime": "Node.js 20", "arch": "x86_64", "os": "Linux" },
    { "runtime": "Node.js 20", "arch": "aarch64", "os": "macOS" },
    { "runtime": "Chrome 120+", "arch": "x86_64", "os": "Linux" },
    { "runtime": "Firefox 120+", "arch": "x86_64", "os": "Linux" },
    { "runtime": "Safari 17+", "arch": "aarch64", "os": "macOS" }
  ],
  "aps:testSuite": "aps-determinism-vectors-v1.json",
  "aps:assertion": "All environments produce identical Float64Array outputs for identical inputs",
  "aps:tolerance": "0 ULP (bit-identical, not approximately equal)"
}
```

### 1.4 Offline Is First-Class

APS must function under degraded conditions:

- **Empty case library**: Returns `{ matches: [], status: "no_precedent" }` with a graceful degradation advisory. This is not an error—a system with no history simply has no wisdom to offer.
- **No GNN model available**: Falls back to structural fingerprint comparison (§4.2.3) with degraded accuracy disclosed in output metadata.
- **Partial case library**: Searches available cases; annotates results with coverage metadata indicating what fraction of the historical corpus was searchable.
- **Stale embeddings**: If the case library has been updated but embeddings have not been recomputed, APS must either recompute on-demand or return results annotated with `embeddingsStaleSince` timestamp.

-----

## 2. Core Concepts

### 2.1 What Is a “Case”?

A case is a self-contained record of a completed reasoning episode. It captures not merely the conclusion but the entire reasoning journey: what was asked, what facts were known, how reasoning proceeded, what verdict was reached, how it was ethically evaluated, and what the outcome was (if known).

#### 2.1.1 Case Schema (JSON-LD)

```json
{
  "@context": {
    "aps": "https://fnsr.dev/aps/",
    "fnsr": "https://fnsr.dev/core/",
    "bfo": "http://purl.obolibrary.org/obo/",
    "hiri": "https://fnsr.dev/hiri/"
  },
  "@type": "aps:ReasoningCase",
  "@id": "aps:case-{uuid}",

  "aps:caseMetadata": {
    "@type": "aps:CaseMetadata",
    "aps:caseId": "string (UUID)",
    "aps:createdAt": "xsd:dateTime",
    "aps:domain": "IRI (W2Fuel namespace)",
    "aps:queryType": "string (fast | standard | full)",
    "aps:outcomeKnown": "boolean",
    "aps:version": "string (semver)",
    "aps:schemaVersionAtCreation": "string (W2Fuel schema version active when case was created)"
  },

  "aps:inputContext": {
    "@type": "aps:InputContext",
    "aps:originalQuery": "fnsr:QueryEnvelope (JSON-LD)",
    "aps:knownFacts": [
      {
        "@type": "aps:Fact",
        "aps:predicate": "IRI",
        "aps:subject": "IRI",
        "aps:object": "IRI or literal",
        "aps:taintLevel": "fnsr:TaintLevel",
        "aps:source": "hiri:Hash-IRI"
      }
    ],
    "aps:missingPredicates": ["IRI (if AES was invoked)"],
    "aps:domainContext": {
      "aps:activeNamespaces": ["IRI"],
      "aps:schemaVersion": "string"
    }
  },

  "aps:reasoningGraph": {
    "@type": "aps:ReasoningGraph",
    "aps:nodes": [
      {
        "@type": "aps:ReasoningNode",
        "@id": "aps:node-{uuid}",
        "aps:nodeType": "fact | rule | inference | gap | default | hypothesis",
        "aps:content": "JSON-LD (the actual claim, rule, or inference)",
        "aps:contentHash": "string (hash of canonical content for semantic deduplication)",
        "aps:taintLevel": "fnsr:TaintLevel",
        "aps:service": "string (which FNSR service produced this)"
      }
    ],
    "aps:edges": [
      {
        "@type": "aps:ReasoningEdge",
        "aps:source": "IRI (node @id)",
        "aps:target": "IRI (node @id)",
        "aps:edgeType": "supports | defeats | triggers | resolves",
        "aps:weight": "number (optional, for weighted inference)"
      }
    ]
  },

  "aps:verdict": {
    "@type": "aps:CaseVerdict",
    "aps:outcome": "string (the MDRE verdict)",
    "aps:confidence": "number [0,1]",
    "aps:taintLevel": "fnsr:TaintLevel",
    "aps:defeasibleDefaultsUsed": ["IRI (DES defaults that were applied)"],
    "aps:conflictsResolved": [
      {
        "aps:conflictType": "string",
        "aps:resolutionMethod": "string",
        "aps:winner": "IRI"
      }
    ]
  },

  "aps:ethicalEvaluation": {
    "@type": "aps:EthicalEvaluation",
    "aps:ieeResult": "approved | vetoed | deadlock | not_invoked",
    "aps:worldviewScores": {
      "aps:worldviewId": "number (IEE perspective scores, if available)"
    },
    "aps:ethicalConcerns": ["string (if any flags were raised)"]
  },

  "aps:outcome": {
    "@type": "aps:CaseOutcome",
    "aps:outcomeRecorded": "boolean",
    "aps:actualResult": "string or JSON-LD (what actually happened, if known)",
    "aps:verdictAccuracy": "correct | incorrect | partial | unknown",
    "aps:recordedAt": "xsd:dateTime",
    "aps:notes": "string"
  },

  "aps:feedback": {
    "@type": "aps:PrecedentFeedback",
    "aps:endorsements": "integer (times this case was used and endorsed as useful precedent)",
    "aps:rejections": "integer (times this case was returned but rejected as poor match)",
    "aps:feedbackLog": [
      {
        "aps:timestamp": "xsd:dateTime",
        "aps:sagaId": "string (which saga used this as precedent)",
        "aps:verdict": "endorsed | rejected",
        "aps:reason": "string (optional, why rejected)"
      }
    ]
  },

  "aps:embedding": {
    "@type": "aps:GraphEmbedding",
    "aps:modelVersion": "string (GNN model version that produced this)",
    "aps:vector": "base64-encoded Float64Array",
    "aps:dimensions": "integer",
    "aps:computedAt": "xsd:dateTime"
  },

  "aps:provenance": {
    "@type": "hiri:ProvenanceChain",
    "hiri:hash": "string (HIRI hash of this case)",
    "hiri:precedingEvents": ["IRI (event log entries that comprised this case)"],
    "hiri:attestation": "string (cryptographic signature, if available)"
  }
}
```

#### 2.1.2 Case Lifecycle

A case moves through the following states:

```
[ACTIVE]  →  [CLOSED]  →  [EMBEDDED]  →  [INDEXED]
    │             │              │              │
    │             │              │              └─ Searchable by APS
    │             │              └─ GNN embedding computed
    │             └─ Verdict rendered, reasoning complete
    └─ Reasoning in progress (not yet a case)

                    [OUTCOME_RECORDED]
                           │
                           └─ Post-hoc outcome data attached
                              (may happen much later)

                    [MIGRATED]
                           │
                           └─ Schema-migrated from an older
                              W2Fuel version (§8.5)

                    [RETIRED]
                           │
                           └─ Superseded by schema change or
                              explicitly deprecated, or
                              negative feedback exceeds threshold (§8.6)
```

Cases in `ACTIVE` state are not visible to APS. Only `EMBEDDED` or `INDEXED` cases are searchable. `OUTCOME_RECORDED` cases are preferred in retrieval because they carry empirical feedback. `MIGRATED` cases are searchable but carry a migration annotation in their provenance.

### 2.2 What Is “Structural Similarity”?

Two reasoning graphs are structurally similar when they share analogous patterns of inference, even if the surface-level entities and predicates differ.

**Example**: Consider two cases:

- **Case A**: An employment dispute where a background check was incomplete, default assumptions were applied via DES, a gap was identified by AES, and MDRE rendered a conditional verdict.
- **Case B**: A real estate transaction where a title search was incomplete, default assumptions were applied via DES, a gap was identified by AES, and MDRE rendered a conditional verdict.

These cases share almost no vocabulary (employment vs. real estate, background check vs. title search), but their reasoning graphs are structurally isomorphic: both feature the same pattern of incomplete-information → default-reasoning → gap-detection → conditional-verdict. APS should recognize this structural analogy.

#### 2.2.1 The Limits of Pure Structure (The “Cake vs. Pipe Bomb” Problem)

**[NEW IN v1.1]** Structural similarity alone is necessary but insufficient. Consider:

- **Case C**: A case about “recipe for a cake” with structure: ingredients → steps → outcome.
- **Case D**: A case about “recipe for an explosive” with structure: ingredients → steps → outcome.

These graphs are structurally isomorphic. Pure topological embedding would rate them as near-identical. This is dangerous—a precedent from a benign baking case should never be suggested as analogous to a weapons case.

**Resolution**: APS uses *hybrid* embedding (§4.2.2) that concatenates structural features with semantic content vectors. The GNN captures topology; the semantic component captures *what the nodes are about*. Two structurally identical graphs with semantically divergent content will embed at different locations in vector space.

This design choice means APS is not purely structure-blind. It is structure-*primary*: topology is the dominant signal, but semantic content acts as a discriminator that prevents pathological cross-domain false positives. The balance between structural and semantic weight is controlled by the `semanticWeight` hyperparameter in the node initialization (§4.2.2, Phase 1).

### 2.3 Taint Model

APS outputs carry inherited taint from their precedent sources, with an additional analogical uncertainty factor.

#### 2.3.1 Taint Inheritance Rules

|Source Case Taint|APS Output Taint |Rationale                                                   |
|-----------------|-----------------|------------------------------------------------------------|
|L0 (Verified)    |L2 (Defeasible)  |Analogical inference is inherently defeasible               |
|L1 (Derived)     |L2 (Defeasible)  |Same reasoning; analogy cannot preserve derivation certainty|
|L2 (Defeasible)  |L2 (Defeasible)  |Floor; analogy does not degrade further                     |
|L3 (Speculative) |L3 (Speculative) |Cannot launder speculation through analogy                  |
|L4 (Hypothetical)|L4 (Hypothetical)|Precedent from simulation remains hypothetical              |
|L5 (Adversarial) |Excluded         |Adversarial cases are never returned as precedent           |

**Key principle**: Analogical inference **always** produces at least L2 output. Even if the source case was verified (L0), the act of drawing an analogy introduces epistemic uncertainty that prevents the conclusion from being treated as verified.

#### 2.3.2 Taint Envelope

```json
{
  "@context": {
    "taint": "https://fnsr.dev/taint/",
    "aps": "https://fnsr.dev/aps/"
  },
  "@type": "taint:TaintedContent",

  "taint:level": {
    "@type": "taint:Level",
    "@id": "taint:L2",
    "taint:name": "Defeasible",
    "taint:source": "aps:analogical_inference",
    "taint:canPromoteTo": ["taint:L1"],
    "taint:promotionRequires": "independent_verification"
  },

  "taint:derivation": {
    "taint:sourceService": "aps",
    "taint:sourceCase": "aps:case-{uuid}",
    "taint:sourceCaseTaint": "taint:L0",
    "taint:taintElevationReason": "analogical_inference_defeasibility"
  },

  "taint:restrictions": {
    "taint:canInformDecision": true,
    "taint:canBindDecision": false,
    "taint:mustLabelAsAdvisory": true,
    "taint:requiresExplicitAcknowledgment": false
  },

  "taint:content": {
    "@type": "aps:PrecedentResult",
    "...": "the actual precedent match"
  }
}
```

-----

## 3. Architecture

### 3.1 Component Overview

APS consists of four pure computational components, each independently testable:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                  ANALOGICAL PRECEDENT SERVICE (APS)                     │
│                                                                         │
│  ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐  │
│  │                  │    │                  │    │                  │  │
│  │   GRAPH EMBEDDER │    │   VECTOR INDEX   │    │  CASE LIBRARY    │  │
│  │   (GNN Core)     │    │   (HNSW/Flat)    │    │  (JSON-LD Store) │  │
│  │                  │    │                  │    │                  │  │
│  │  Reasoning Graph │    │  Indexed         │    │  Case Records    │  │
│  │  → Float64 Vec   │    │  Embeddings      │    │  + Metadata      │  │
│  │  (hybrid: struct │    │                  │    │  + Feedback       │  │
│  │   + semantic)    │    │                  │    │                  │  │
│  └────────┬─────────┘    └────────┬─────────┘    └────────┬─────────┘  │
│           │                       │                       │            │
│           └───────────┬───────────┘                       │            │
│                       │                                   │            │
│                       ▼                                   │            │
│           ┌──────────────────────┐                        │            │
│           │                      │                        │            │
│           │   PRECEDENT MATCHER  │◄───────────────────────┘            │
│           │                      │                                     │
│           │  Query embedding     │                                     │
│           │  + Vector search     │                                     │
│           │  + Greedy alignment  │                                     │
│           │  + Disanalogy detect │                                     │
│           │  + Feedback-aware    │                                     │
│           │    ranking           │                                     │
│           │                      │                                     │
│           └──────────┬───────────┘                                     │
│                      │                                                 │
│                      ▼                                                 │
│           ┌──────────────────────┐                                     │
│           │  PrecedentResult     │                                     │
│           │  (Tainted, Advisory) │                                     │
│           └──────────────────────┘                                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Separation of Concerns

|Layer        |Component        |Responsibility                     |Pluggable?                               |
|-------------|-----------------|-----------------------------------|-----------------------------------------|
|Computation  |Graph Embedder   |Embed reasoning graphs into vectors|Core (not pluggable)                     |
|Computation  |Precedent Matcher|Compute similarity, align, rank    |Core (not pluggable)                     |
|Computation  |Semantic Hasher  |Produce content vectors for nodes  |Pluggable (adapter; see §4.2.2)          |
|State        |Case Library     |Store and retrieve case records    |Pluggable (JSON file, IndexedDB, adapter)|
|State        |Vector Index     |Store and query embeddings         |Pluggable (in-memory flat, HNSW, adapter)|
|Orchestration|Event handler    |Listen for `fnsr.precedent.query`  |Pluggable (adapter)                      |
|Integration  |Event emitter    |Emit `fnsr.precedent.found`        |Pluggable (adapter)                      |

-----

## 4. Graph Embedding (GNN Architecture)

### 4.1 Problem Statement

A reasoning graph is a directed labeled graph where nodes carry semantic types (fact, rule, inference, gap, default, hypothesis) and edges carry relational types (supports, defeats, triggers, resolves). The embedding must capture:

1. **Topology**: The shape of reasoning (linear chains vs. branching trees vs. cyclical support)
1. **Node role distribution**: The mix of facts, rules, defaults, gaps, and hypotheses
1. **Edge semantics**: The pattern of support, defeat, triggering, and resolution
1. **Depth and complexity**: Shallow reasoning vs. deep multi-step inference
1. **Domain invariance**: The embedding should generalize across domains (an employment case and a real estate case with the same reasoning structure should embed similarly)
1. **[NEW IN v1.1] Semantic discrimination**: Structurally identical graphs with semantically divergent content must embed differently to prevent pathological false positives

### 4.2 GNN Model

#### 4.2.1 Architecture: Message-Passing Neural Network (MPNN)

APS uses a typed message-passing architecture that respects both node types and edge types.

```typescript
/**
 * APS Graph Neural Network - Edge-Canonical Implementation
 *
 * This model runs in any JavaScript environment with no external dependencies
 * beyond a matrix math library (or the built-in APSArithmetic).
 */

interface APSGraphModel {
  /**
   * Embed a reasoning graph into a fixed-dimensional vector.
   *
   * @param graph - The reasoning graph (nodes + edges) as JSON-LD
   * @param weights - Frozen model weights (JSON-serializable)
   * @param semanticVectors - Pre-computed semantic content vectors for each node
   * @returns Fixed-dimensional embedding vector
   *
   * Determinism: identical graph + identical weights + identical semanticVectors
   *              = identical vector
   */
  embed(
    graph: ReasoningGraph,
    weights: ModelWeights,
    semanticVectors: Map<string, Float64Array>
  ): Float64Array;

  /**
   * Embed a batch of graphs (for case library indexing).
   */
  embedBatch(
    graphs: ReasoningGraph[],
    weights: ModelWeights,
    semanticVectorsBatch: Map<string, Float64Array>[]
  ): Float64Array[];
}
```

#### 4.2.2 Model Structure

The MPNN operates in three phases:

**Phase 1: Node Feature Initialization (Hybrid)**

**[REVISED IN v1.1]** Each node is assigned an initial feature vector by concatenating three components: type encoding, taint encoding, and a semantic content vector.

```json
{
  "nodeFeatureSchema": {
    "structuralFeatures": {
      "typeEncoding": {
        "fact": [1, 0, 0, 0, 0, 0],
        "rule": [0, 1, 0, 0, 0, 0],
        "inference": [0, 0, 1, 0, 0, 0],
        "gap": [0, 0, 0, 1, 0, 0],
        "default": [0, 0, 0, 0, 1, 0],
        "hypothesis": [0, 0, 0, 0, 0, 1]
      },
      "taintEncoding": {
        "L0": [1, 0, 0, 0, 0, 0],
        "L1": [0, 1, 0, 0, 0, 0],
        "L2": [0, 0, 1, 0, 0, 0],
        "L3": [0, 0, 0, 1, 0, 0],
        "L4": [0, 0, 0, 0, 1, 0],
        "L5": [0, 0, 0, 0, 0, 1]
      },
      "serviceEncoding": "one-hot over known FNSR services (MDRE, AES, DES, CSS, etc.)",
      "structuralDimension": 24
    },

    "semanticFeatures": {
      "description": "A fixed-dimension content vector derived from the node's JSON-LD content",
      "semanticDimension": 32,
      "source": "SemanticHasher adapter (see below)"
    },

    "combination": "concat(structuralFeatures, semanticWeight * semanticFeatures)",
    "semanticWeight": 0.5,
    "totalInitialDimension": 56
  }
}
```

**The Semantic Hasher Adapter**

The semantic content vector is produced by a pluggable adapter, not a fixed algorithm. This preserves edge-canonical constraints: the adapter interface is defined; the implementation is pluggable.

```typescript
/**
 * Produces a fixed-dimension semantic content vector from node content.
 *
 * This is an adapter boundary. Implementations may range from:
 * - Deterministic hash-based: SimHash/MinHash over content tokens (edge-canonical)
 * - Learned: Small language model embeddings (requires model weights)
 * - Ontology-based: BFO/CCO class hierarchy distance vectors (requires W2Fuel)
 *
 * The reference implementation uses SimHash (no learned weights required).
 */
interface SemanticHasher {
  /**
   * Produce a semantic content vector for a reasoning node.
   *
   * @param content - The node's JSON-LD content
   * @param dimension - Target vector dimension (default: 32)
   * @returns Fixed-dimension semantic vector
   *
   * Determinism: identical content = identical vector
   */
  hash(content: JsonLd, dimension: number): Float64Array;
}
```

**Reference implementation: SimHash**

SimHash is the edge-canonical baseline. It requires no learned weights, no model files, and no external dependencies. It works by:

1. Tokenizing the JSON-LD content into terms (predicates, type IRIs, literal values)
1. Hashing each term with a deterministic hash function (e.g., FNV-1a)
1. Accumulating weighted bit-level signatures
1. Normalizing to a unit vector of the target dimension

SimHash captures semantic similarity at a coarse level: nodes that mention similar predicates and types will hash similarly. It does not capture deep semantic meaning (synonymy, paraphrase), but it does discriminate between “background check” and “title search” and critically between “baking” and “explosive manufacturing.”

**Why `semanticWeight` = 0.5?**

The structural features (24 dimensions) and semantic features (32 dimensions, weighted by 0.5 → effective 16 dimensions) give the model a roughly 60/40 structural-to-semantic ratio. This means:

- Structurally identical graphs with identical content: very high similarity (both components match).
- Structurally identical graphs with different content: moderate similarity (structure matches, semantics diverge). This is the desired behavior—the “cake vs. pipe bomb” scenario produces a moderate score, not a high one.
- Structurally different graphs with similar content: low-to-moderate similarity (topology diverges, content partially matches).

The `semanticWeight` is a frozen hyperparameter in the model weights, not a runtime parameter.

**Phase 2: Message Passing (K rounds)**

```
For each round k = 1..K:
  For each node v:
    messages = []
    For each edge (u, v) with type t:
      m = W_t^k · h_u^(k-1)          // Type-specific message transform
      messages.append(m)
    For each edge (v, u) with type t:
      m_rev = W_t_rev^k · h_u^(k-1)  // Reverse direction (separate weights)
      messages.append(m_rev)
    
    aggregated = mean(messages)        // Permutation-invariant aggregation
    h_v^k = ReLU(W_self^k · h_v^(k-1) + aggregated)
```

**Configuration constants:**

|Parameter                 |Value                                    |Rationale                                                                                             |
|--------------------------|-----------------------------------------|------------------------------------------------------------------------------------------------------|
|K (message-passing rounds)|4                                        |Sufficient for reasoning chains up to depth ~8; beyond this, information is captured by global pooling|
|Hidden dimension          |64                                       |Balances expressiveness with browser runtime; larger models use adapters                              |
|Edge types                |4 (supports, defeats, triggers, resolves)|Matches FNSR edge vocabulary                                                                          |
|Weight matrices per round |2 × edge_types + 1 = 9                   |Forward + reverse per edge type, plus self-loop                                                       |
|Input projection          |W_input: 56 → 64                         |Projects hybrid initialization to hidden dimension                                                    |

**Phase 3: Graph-Level Readout**

The final graph embedding combines three aggregation strategies to capture different aspects of the reasoning structure:

```
v_mean = mean({h_v^K | v ∈ V})       // Average node state
v_max  = max({h_v^K | v ∈ V})        // Most activated node
v_root = h_root^K                     // Root node state (the query or verdict)

graph_embedding = W_readout · concat(v_mean, v_max, v_root)
```

**Output dimension**: 128 (configurable via model weights, but 128 is the default for the reference implementation).

#### 4.2.3 Fallback: Structural Fingerprint

When the GNN model is unavailable (offline, not yet trained, model loading failure), APS falls back to a deterministic structural fingerprint that requires no learned weights:

```json
{
  "@type": "aps:StructuralFingerprint",
  "description": "Handcrafted feature vector computed without learned weights. Includes both topological and semantic hash features.",

  "features": {
    "nodeCount": "integer",
    "edgeCount": "integer",
    "nodeTypeCounts": {
      "fact": "integer",
      "rule": "integer",
      "inference": "integer",
      "gap": "integer",
      "default": "integer",
      "hypothesis": "integer"
    },
    "edgeTypeCounts": {
      "supports": "integer",
      "defeats": "integer",
      "triggers": "integer",
      "resolves": "integer"
    },
    "graphDepth": "integer (longest path from root)",
    "branchingFactor": "number (mean out-degree)",
    "defeatRatio": "number (defeats / total edges)",
    "gapRatio": "number (gaps / total nodes)",
    "taintDistribution": [
      "number (fraction of nodes at each taint level)"
    ],
    "topologicalSignature": "string (hash of sorted degree sequence)",
    "contentSimHash": "Float64Array (SimHash of all node content, 16 dimensions)"
  },

  "dimension": 48,
  "accuracyDisclaimer": "Structural fingerprints capture coarse topology and content signature but miss learned structural patterns. Similarity scores from fingerprint mode are less reliable than GNN mode and should be weighted accordingly."
}
```

**[REVISED IN v1.1]**: Fingerprint now includes a `contentSimHash` component (16 of 48 dimensions), providing basic semantic discrimination even in fallback mode. This prevents the “cake vs. pipe bomb” failure mode from manifesting in fingerprint-only operation.

Fingerprint similarity is computed as cosine distance over the 48-dimensional feature vector after z-score normalization.

### 4.3 Model Weight Management

#### 4.3.1 Weight Format

Model weights are serialized as JSON-LD for portability:

```json
{
  "@context": "https://fnsr.dev/aps/model/",
  "@type": "aps:ModelWeights",
  "aps:modelVersion": "1.0.0",
  "aps:architecture": "MPNN-4-64-128-hybrid",
  "aps:trainedOn": "string (dataset identifier)",
  "aps:trainedAt": "xsd:dateTime",
  "aps:trainingObjective": "contrastive_with_hard_negatives",
  "aps:trainingMetrics": {
    "aps:validationSimilarityCorrelation": "number",
    "aps:analogyRecallAt10": "number",
    "aps:hardNegativeRejectionRate": "number"
  },
  "aps:hyperparameters": {
    "aps:semanticWeight": 0.5,
    "aps:semanticDimension": 32,
    "aps:structuralDimension": 24,
    "aps:hiddenDimension": 64,
    "aps:outputDimension": 128,
    "aps:messagePassingRounds": 4
  },
  "aps:weights": {
    "aps:inputProjection": "base64 (Float64Array, shape [64, 56])",
    "aps:messagePassingRounds": [
      {
        "aps:round": 1,
        "aps:edgeWeights": {
          "supports_fwd": "base64 (Float64Array)",
          "supports_rev": "base64 (Float64Array)",
          "defeats_fwd": "base64 (Float64Array)",
          "defeats_rev": "base64 (Float64Array)",
          "triggers_fwd": "base64 (Float64Array)",
          "triggers_rev": "base64 (Float64Array)",
          "resolves_fwd": "base64 (Float64Array)",
          "resolves_rev": "base64 (Float64Array)"
        },
        "aps:selfWeight": "base64 (Float64Array)",
        "aps:bias": "base64 (Float64Array)"
      }
    ],
    "aps:readoutWeight": "base64 (Float64Array)",
    "aps:readoutBias": "base64 (Float64Array)"
  },
  "hiri:hash": "string (HIRI hash of this weight set)"
}
```

#### 4.3.2 Weight Loading Contract

```typescript
interface WeightLoader {
  /**
   * Load model weights from a JSON-LD source.
   *
   * Adapter implementations may load from:
   * - Local JSON file (edge-canonical baseline)
   * - IndexedDB (browser persistence)
   * - HTTP fetch (remote model registry)
   *
   * The core computation only requires the resolved ModelWeights object.
   */
  load(): Promise<ModelWeights>;

  /**
   * Verify weight integrity via HIRI hash.
   */
  verify(weights: ModelWeights): boolean;
}
```

#### 4.3.3 Training Objective

**[REVISED IN v1.1]** GNN training remains an offline, non-real-time process that produces a frozen weight file. However, the training *objective* is normative because it determines what “similarity” means—different objectives produce different embedding spaces, and consumers must understand what the embeddings encode.

**Training is out of scope for runtime execution**, but the training objective is part of the specification because it defines the semantics of the embedding space.

**Objective: Contrastive Learning with Hard Negative Mining**

APS trains via a contrastive loss that pulls structurally analogous graphs together and pushes dissimilar graphs apart in embedding space:

```
L(anchor, positive, negative) = max(0, margin + sim(anchor, negative) - sim(anchor, positive))
```

Where:

- **Anchor**: A reasoning graph from the case library.
- **Positive**: A graph that is genuinely analogous (same reasoning pattern, possibly different domain).
- **Negative**: A graph that is *not* analogous.
- **sim()**: Cosine similarity in embedding space.
- **margin**: Minimum distance between positive and negative pairs (hyperparameter, default 0.3).

**Hard Negative Mining**

The critical training signal comes from *hard negatives*—cases that are superficially similar but genuinely different:

|Hard Negative Type               |Example                                                          |What It Teaches                          |
|---------------------------------|-----------------------------------------------------------------|-----------------------------------------|
|Same domain, different structure |Two employment cases with completely different reasoning patterns|Domain alone does not make an analogy    |
|Same structure, different content|“Cake recipe” vs. “explosive recipe” reasoning graphs            |Structure alone does not make an analogy |
|Near-miss topology               |A linear chain vs. a chain with one extra defeat edge            |Small structural changes can matter      |
|Taint mismatch                   |L0-dominated case vs. L3-dominated case with same topology       |Epistemic profile affects analogy quality|

**Positive Pair Construction**

Positive pairs are constructed by:

1. **Domain transfer**: Taking a real case and replacing all domain-specific IRIs with IRIs from a different W2Fuel namespace while preserving graph topology.
1. **Node perturbation**: Adding or removing one non-critical node while preserving the core reasoning pattern.
1. **Human annotation**: Domain experts marking pairs of cases as “genuinely analogous” (the gold standard, but expensive).

**What this specification defines:**

- The loss function shape (triplet contrastive)
- The hard negative taxonomy (what constitutes a meaningful negative)
- The positive pair construction methods
- The required training metrics in the weight file

**What this specification does NOT define:**

- Learning rate schedule, batch size, optimizer choice
- Training hardware requirements
- Dataset size thresholds
- Training pipeline implementation

### 4.4 Model Versioning and Compatibility

The `modelVersion` field in the weight file uses semantic versioning:

- **Major**: Changes to the embedding space semantics (new architecture, different output dimension). Major version changes require full re-embedding of the case library.
- **Minor**: Improved weights from additional training data. Minor version changes produce better embeddings but remain in the same vector space. Re-embedding is recommended but not required; stale embeddings are disclosed.
- **Patch**: Bug fixes in weight serialization. No re-embedding needed.

A vector index MUST NOT mix embeddings from different major versions. If the model major version changes, the entire index must be rebuilt.

-----

## 5. Vector Index

### 5.1 Purpose

The vector index provides approximate nearest-neighbor (ANN) search over the embedding space, enabling efficient retrieval of similar cases from potentially large case libraries.

### 5.2 Index Interface

```typescript
interface VectorIndex {
  /**
   * Add an embedding to the index.
   *
   * @param id - Case identifier
   * @param vector - Embedding vector (from GNN or fingerprint)
   */
  add(id: string, vector: Float64Array): void;

  /**
   * Remove an embedding from the index.
   *
   * @param id - Case identifier to remove
   */
  remove(id: string): void;

  /**
   * Query the index for nearest neighbors.
   *
   * @param query - Query vector
   * @param k - Number of results to return
   * @param filter - Optional predicate to exclude candidates
   * @returns Ranked results with distances
   */
  search(
    query: Float64Array,
    k: number,
    filter?: (id: string) => boolean
  ): SearchResult[];

  /**
   * Serialize the index to a JSON-LD compatible format.
   */
  serialize(): IndexSnapshot;

  /**
   * Load an index from a serialized snapshot.
   */
  deserialize(snapshot: IndexSnapshot): void;

  /**
   * Report index statistics.
   */
  stats(): IndexStats;
}

interface SearchResult {
  caseId: string;
  distance: number;
  similarity: number;  // 1 - normalized_distance
}

interface IndexStats {
  totalVectors: number;
  dimensions: number;
  indexType: string;
  memoryEstimateBytes: number;
}
```

### 5.3 Index Strategies

APS supports multiple index strategies, selected based on case library size:

|Library Size       |Strategy                                 |Rationale                                |
|-------------------|-----------------------------------------|-----------------------------------------|
|0–1,000 cases      |Flat (brute-force)                       |Exact results; linear scan is fast enough|
|1,000–100,000 cases|HNSW (Hierarchical Navigable Small World)|Sublinear search time; good recall       |
|100,000+ cases     |HNSW with product quantization           |Memory-efficient approximate search      |

#### 5.3.1 Flat Index (Reference Implementation)

The flat index is the edge-canonical baseline. It performs exact cosine similarity search via linear scan:

```typescript
class FlatVectorIndex implements VectorIndex {
  private vectors: Map<string, Float64Array> = new Map();

  search(query: Float64Array, k: number, filter?: (id: string) => boolean): SearchResult[] {
    const results: SearchResult[] = [];

    for (const [id, vector] of this.vectors) {
      if (filter && !filter(id)) continue;
      const similarity = cosineSimilarity(query, vector);
      results.push({ caseId: id, distance: 1 - similarity, similarity });
    }

    results.sort((a, b) => b.similarity - a.similarity);
    return results.slice(0, k);
  }

  // ... add, remove, serialize, deserialize implementations
}
```

#### 5.3.2 HNSW Index (Adapter)

HNSW is a non-normative adapter for larger deployments. Implementations may use libraries like `hnswlib-node` or port the algorithm to pure JavaScript. HNSW parameters:

|Parameter     |Default|Description                       |
|--------------|-------|----------------------------------|
|M             |16     |Max connections per node per layer|
|efConstruction|200    |Build-time search width           |
|efSearch      |50     |Query-time search width           |

HNSW is an optimization, not a requirement. Any index that satisfies the `VectorIndex` interface is valid.

### 5.4 Index Serialization (JSON-LD)

```json
{
  "@context": "https://fnsr.dev/aps/index/",
  "@type": "aps:VectorIndexSnapshot",
  "aps:indexType": "flat | hnsw",
  "aps:dimensions": 128,
  "aps:vectorCount": "integer",
  "aps:createdAt": "xsd:dateTime",
  "aps:modelVersion": "string (which GNN model produced these embeddings)",
  "aps:entries": [
    {
      "aps:caseId": "aps:case-{uuid}",
      "aps:vector": "base64 (Float64Array)"
    }
  ],
  "aps:hnswParams": {
    "aps:M": 16,
    "aps:efConstruction": 200,
    "aps:layerCount": "integer"
  },
  "hiri:hash": "string (HIRI hash of this snapshot)"
}
```

-----

## 6. Precedent Matching Algorithm

### 6.1 Query Pipeline

When APS receives an `fnsr.precedent.query` event, it executes the following pipeline:

```
Input: ReasoningGraph (the current case's reasoning so far)
       QueryParameters (k, threshold, domain filter, etc.)

Step 1: SEMANTIC HASH
  For each node in reasoningGraph:
    semanticVec = semanticHasher.hash(node.content, 32)
  // Deterministic; no external service required

Step 2: EMBED
  queryVector = graphModel.embed(reasoningGraph, weights, semanticVectors)
  OR
  queryVector = structuralFingerprint(reasoningGraph)  // fallback

Step 3: SEARCH
  candidates = vectorIndex.search(queryVector, k * OVERSAMPLE_FACTOR, domainFilter)
  // OVERSAMPLE_FACTOR = 3 (retrieve 3x candidates for re-ranking)

Step 4: RE-RANK
  For each candidate:
    a. Load full case record from case library
    b. Compute greedy structural alignment (§6.2)
    c. Compute disanalogy annotations (§6.3)
    d. Apply feedback adjustment (§6.5)
    e. Compute composite similarity score (§6.4)
  Sort by composite score

Step 5: THRESHOLD
  Filter results below minimum similarity threshold (default: 0.3)

Step 6: PACKAGE
  For each surviving result:
    a. Attach taint envelope (§2.3)
    b. Attach provenance chain
    c. Mark as advisory

Output: PrecedentResult (ranked list of matches with metadata)
```

### 6.2 Structural Alignment Map

After vector search identifies candidates, APS computes a structural alignment map that explains *why* the candidate is analogous:

```json
{
  "@type": "aps:StructuralAlignmentMap",
  "aps:algorithm": "greedy_embedding_match",
  "aps:alignedPairs": [
    {
      "aps:queryNode": "IRI (node in query graph)",
      "aps:caseNode": "IRI (node in precedent case)",
      "aps:alignmentScore": "number [0,1]",
      "aps:alignmentBasis": "type_match | structural_role | embedding_proximity"
    }
  ],
  "aps:alignedEdges": [
    {
      "aps:queryEdge": { "source": "IRI", "target": "IRI", "type": "string" },
      "aps:caseEdge": { "source": "IRI", "target": "IRI", "type": "string" },
      "aps:alignmentScore": "number [0,1]"
    }
  ],
  "aps:unmatchedQueryNodes": ["IRI (nodes in query with no analog in case)"],
  "aps:unmatchedCaseNodes": ["IRI (nodes in case with no analog in query)"],
  "aps:alignmentCoverage": "number [0,1] (fraction of query nodes that were aligned)"
}
```

#### 6.2.1 Alignment Algorithm: Greedy Embedding Match

**[REVISED IN v1.1]** The alignment uses a greedy heuristic, not exact subgraph isomorphism. This is an explicit design choice: exact alignment is NP-hard (reducible to subgraph isomorphism), which violates the latency budget. The greedy approach is O(V_q × V_c) and produces good-enough alignments for advisory purposes.

**Algorithm:**

```
Input: queryGraph (V_q nodes), caseGraph (V_c nodes), 
       nodeEmbeddings from GNN final round

1. Compute similarity matrix S where S[i][j] = cosine(h_qi^K, h_cj^K)
2. Apply type compatibility mask: S[i][j] = -∞ if type(q_i) ≠ type(c_j)
3. Greedy assignment:
   matched_case_nodes = {}
   For each query node q_i in decreasing order of max(S[i,:]):
     best_j = argmax_j S[i][j] where c_j ∉ matched_case_nodes
     if S[i][best_j] > ALIGNMENT_THRESHOLD (default: 0.3):
       align(q_i, c_best_j)
       matched_case_nodes.add(c_best_j)
     else:
       mark q_i as unmatched
4. Edge alignment: align edges whose source AND target nodes are both aligned
5. Compute coverage = |aligned query nodes| / |total query nodes|
```

**Complexity**: O(V_q × V_c) for the similarity matrix, O(V_q × log V_q) for the greedy sort. Total: O(V_q × V_c), which for V_q = 50 and V_c = 50 is 2,500 operations—trivially fast.

**Why not Hungarian algorithm?** The Hungarian algorithm (O(V³)) produces optimal assignments but is slower and offers marginal improvement for advisory purposes. The greedy approach is deterministic, fast, and produces interpretable alignments. If future analysis shows the greedy approach produces poor alignments, the algorithm can be upgraded without changing the interface.

### 6.3 Disanalogy Annotation

APS does not merely report similarity—it explicitly documents where the analogy breaks down:

```json
{
  "@type": "aps:DisanalogyReport",
  "aps:structuralDisanalogies": [
    {
      "aps:type": "missing_branch | extra_branch | type_mismatch | depth_mismatch",
      "aps:description": "string (human-readable explanation)",
      "aps:severity": "minor | moderate | major",
      "aps:affectedNodes": ["IRI"]
    }
  ],
  "aps:domainDisanalogies": [
    {
      "aps:queryDomain": "IRI (W2Fuel namespace)",
      "aps:caseDomain": "IRI (W2Fuel namespace)",
      "aps:crossDomainWarning": "string (e.g., 'Precedent is from real estate; query is employment')"
    }
  ],
  "aps:semanticDisanalogies": [
    {
      "aps:type": "content_divergence | predicate_mismatch | entity_type_mismatch",
      "aps:description": "string",
      "aps:divergenceScore": "number [0,1] (semantic distance between aligned node contents)"
    }
  ],
  "aps:epistemicDisanalogies": [
    {
      "aps:type": "taint_level_mismatch | confidence_gap | different_default_assumptions",
      "aps:description": "string"
    }
  ],
  "aps:overallDisanalogyScore": "number [0,1] (0 = perfect analogy, 1 = completely disanalogous)"
}
```

**[REVISED IN v1.1]**: Added `semanticDisanalogies` category. Disanalogy detection now uses the aligned node pairs from §6.2 to identify content-level divergences between structurally similar nodes, directly addressing the “pure structure” gap.

### 6.4 Composite Similarity Score

The final ranking uses a weighted combination:

```
compositeScore =
    w_embed   * embeddingSimilarity      // Vector-space distance (from search)
  + w_align   * alignmentCoverage        // Fraction of nodes aligned
  + w_disanal * (1 - disanalogyScore)    // Penalty for disanalogies
  + w_outcome * outcomeBonus             // Bonus if outcome is known
  + w_recency * recencyFactor            // Slight preference for recent cases
  + w_feedback * feedbackScore           // Feedback adjustment (§6.5)
```

**Default weights:**

|Weight    |Value|Rationale                                                            |
|----------|-----|---------------------------------------------------------------------|
|w_embed   |0.35 |Primary structural signal (reduced from 0.40 to accommodate feedback)|
|w_align   |0.20 |Alignment quality matters                                            |
|w_disanal |0.20 |Disanalogy penalty                                                   |
|w_outcome |0.10 |Known outcomes are more valuable                                     |
|w_recency |0.05 |Slight recency preference (schemas evolve)                           |
|w_feedback|0.10 |Feedback from past usage (§6.5)                                      |

Weights are configurable per query but default values are normative for the reference implementation.

### 6.5 Feedback-Aware Scoring

**[NEW IN v1.1]** When a precedent has been used in past reasoning sagas and received explicit feedback (endorsement or rejection), APS adjusts its ranking score:

```
feedbackScore = (endorsements - rejections) / (endorsements + rejections + 1)
```

This produces a value in (-1, 1):

- A case with 5 endorsements and 0 rejections: feedbackScore ≈ 0.83
- A case with 0 endorsements and 5 rejections: feedbackScore ≈ -0.83
- A case with no feedback: feedbackScore = 0 (neutral)
- A case with equal endorsements and rejections: feedbackScore ≈ 0 (neutral)

**Feedback does not remove cases.** Even heavily rejected cases remain in the library. The feedback score only affects ranking. Removal requires explicit retirement (§8.6).

-----

## 7. Event Contract

### 7.1 Consumed Events

#### `fnsr.precedent.query`

Request for analogical precedent search.

```json
{
  "@context": "https://fnsr.dev/events/",
  "@type": "fnsr:PrecedentQueryEvent",

  "specversion": "1.0",
  "type": "fnsr.precedent.query",
  "source": "string (requesting service, e.g., '/fnsr/mdre' or '/fnsr/iee')",
  "id": "string (UUID)",
  "time": "xsd:dateTime",
  "datacontenttype": "application/ld+json",

  "fnsr-saga-id": "string (UUID of the enclosing reasoning saga)",
  "fnsr-correlation-id": "string (UUID for request-response pairing)",

  "data": {
    "@type": "aps:PrecedentQuery",

    "aps:reasoningGraph": {
      "@type": "aps:ReasoningGraph",
      "aps:nodes": ["... (same schema as §2.1.1)"],
      "aps:edges": ["..."]
    },

    "aps:queryParameters": {
      "aps:maxResults": "integer (default: 5)",
      "aps:minimumSimilarity": "number [0,1] (default: 0.3)",
      "aps:domainFilter": "IRI or null (restrict to specific W2Fuel namespace)",
      "aps:excludeCases": ["aps:case-{uuid} (exclude specific cases)"],
      "aps:preferOutcomeKnown": "boolean (default: true)",
      "aps:embeddingMode": "gnn | fingerprint | auto (default: auto)",
      "aps:includeDisanalogy": "boolean (default: true)",
      "aps:includeAlignment": "boolean (default: false, expensive)"
    }
  }
}
```

### 7.2 Produced Events

#### `fnsr.precedent.found`

Response with ranked precedent matches.

```json
{
  "@context": "https://fnsr.dev/events/",
  "@type": "fnsr:PrecedentFoundEvent",

  "specversion": "1.0",
  "type": "fnsr.precedent.found",
  "source": "/fnsr/aps",
  "id": "string (UUID)",
  "time": "xsd:dateTime",
  "datacontenttype": "application/ld+json",

  "fnsr-saga-id": "string (UUID, inherited from query)",
  "fnsr-correlation-id": "string (UUID, inherited from query)",
  "fnsr-taint": "L2 (minimum; may be higher per §2.3)",

  "data": {
    "@type": "aps:PrecedentResult",

    "aps:queryId": "string (UUID of the originating query)",
    "aps:status": "found | no_precedent | degraded",
    "aps:embeddingMode": "gnn | fingerprint",
    "aps:searchedCases": "integer (total cases searched)",
    "aps:searchDurationMs": "number",

    "aps:matches": [
      {
        "@type": "aps:PrecedentMatch",
        "aps:rank": "integer (1-based)",
        "aps:caseId": "aps:case-{uuid}",
        "aps:compositeSimilarity": "number [0,1]",
        "aps:embeddingSimilarity": "number [0,1]",

        "aps:caseSummary": {
          "aps:domain": "IRI",
          "aps:queryType": "string",
          "aps:verdictOutcome": "string",
          "aps:outcomeKnown": "boolean",
          "aps:verdictAccuracy": "correct | incorrect | partial | unknown",
          "aps:caseAge": "xsd:duration",
          "aps:nodeCount": "integer",
          "aps:edgeCount": "integer",
          "aps:precedentStrength": {
            "aps:endorsements": "integer",
            "aps:rejections": "integer",
            "aps:feedbackScore": "number [-1, 1]"
          }
        },

        "aps:alignment": {
          "@type": "aps:StructuralAlignmentMap",
          "...": "(included if includeAlignment was true)"
        },

        "aps:disanalogy": {
          "@type": "aps:DisanalogyReport",
          "...": "(included if includeDisanalogy was true)"
        },

        "aps:taint": {
          "taint:level": "taint:L2",
          "taint:sourceCaseTaint": "taint:L0",
          "taint:elevationReason": "analogical_inference_defeasibility"
        },

        "aps:provenance": {
          "hiri:caseHash": "string",
          "hiri:eventLogEntries": ["IRI (original events in the precedent case)"]
        },

        "aps:advisoryNote": "string (auto-generated: 'This precedent is advisory only. The analogy between [query domain] and [case domain] has [disanalogy score] structural differences.')"
      }
    ],

    "aps:degradation": {
      "aps:isDegraded": "boolean",
      "aps:reasons": ["string (e.g., 'fingerprint_mode', 'partial_library', 'stale_embeddings')"],
      "aps:embeddingsStaleSince": "xsd:dateTime or null"
    }
  }
}
```

### 7.3 Feedback Events

**[NEW IN v1.1]** APS consumes feedback events from downstream consumers:

#### `fnsr.precedent.feedback`

```json
{
  "specversion": "1.0",
  "type": "fnsr.precedent.feedback",
  "source": "string (service that used the precedent)",
  "id": "string (UUID)",
  "time": "xsd:dateTime",

  "data": {
    "@type": "aps:PrecedentFeedback",
    "aps:caseId": "aps:case-{uuid} (the precedent case being evaluated)",
    "aps:sagaId": "string (the saga that used this precedent)",
    "aps:verdict": "endorsed | rejected",
    "aps:reason": "string (optional, human or machine explanation)"
  }
}
```

#### Status Semantics

|Status        |Meaning                               |Action for Consumer                                      |
|--------------|--------------------------------------|---------------------------------------------------------|
|`found`       |One or more precedents above threshold|Use matches for advisory reasoning                       |
|`no_precedent`|No matches above threshold            |Proceed without precedent (this is not an error)         |
|`degraded`    |Matches found but with reduced quality|Use matches with extra caution; check `degradation` field|

-----

## 8. Case Library Management

### 8.1 Case Library Interface

```typescript
interface CaseLibrary {
  /**
   * Store a new case. Cases are immutable once stored
   * (except for outcome recording and feedback).
   */
  store(caseRecord: ReasoningCase): void;

  /**
   * Retrieve a case by ID.
   */
  get(caseId: string): ReasoningCase | null;

  /**
   * Attach outcome data to an existing case.
   */
  recordOutcome(caseId: string, outcome: CaseOutcome): void;

  /**
   * Record feedback (endorsement or rejection) for a case.
   */
  recordFeedback(caseId: string, feedback: PrecedentFeedbackEntry): void;

  /**
   * Retire a case (mark as no longer searchable).
   */
  retire(caseId: string, reason: string): void;

  /**
   * List cases matching a filter.
   */
  list(filter: CaseFilter): ReasoningCase[];

  /**
   * Serialize the library to JSON-LD.
   */
  serialize(): CaseLibrarySnapshot;

  /**
   * Load a library from a serialized snapshot.
   */
  deserialize(snapshot: CaseLibrarySnapshot): void;

  /**
   * Report library statistics.
   */
  stats(): LibraryStats;
}

interface CaseFilter {
  domain?: string;          // W2Fuel namespace
  queryType?: string;       // fast, standard, full
  outcomeKnown?: boolean;
  createdAfter?: string;    // ISO datetime
  createdBefore?: string;   // ISO datetime
  status?: string;          // closed, embedded, indexed, migrated, retired
  minFeedbackScore?: number; // minimum feedback score
}

interface LibraryStats {
  totalCases: number;
  embeddedCases: number;
  indexedCases: number;
  migratedCases: number;
  retiredCases: number;
  outcomeKnownFraction: number;
  domainDistribution: Map<string, number>;
  schemaVersionDistribution: Map<string, number>;
  oldestCase: string;       // ISO datetime
  newestCase: string;       // ISO datetime
  averageFeedbackScore: number;
}
```

### 8.2 Case Ingestion

Cases are constructed from the event log. When a reasoning saga completes (MDRE renders a verdict, IEE approves or vetoes), the orchestrator may emit a `fnsr.saga.completed` event. An APS adapter listens for these events and constructs case records.

Case construction is an **adapter concern**, not a core computation. The core spec defines the case schema (§2.1.1) and the ingestion interface, but the mechanism by which events become cases is pluggable.

```typescript
interface CaseConstructor {
  /**
   * Build a case record from a completed saga's events.
   *
   * @param sagaEvents - All events in the completed saga
   * @returns A new ReasoningCase (in CLOSED state)
   */
  construct(sagaEvents: FNSREvent[]): ReasoningCase;
}
```

### 8.3 Embedding Maintenance

When a case transitions from `CLOSED` to `EMBEDDED`, the GNN produces its embedding vector. When the embedding is added to the vector index, the case transitions to `INDEXED`.

Embedding recomputation is required when:

1. The GNN model weights are updated (new major version per §4.4)
1. The node/edge feature schema changes
1. The SemanticHasher implementation changes (since semantic vectors feed into the GNN)

Recomputation is a batch operation. APS must track which model version produced each embedding and flag stale embeddings in query results.

### 8.4 Eventually-Consistent Projection

Per FNSR §8.2, APS maintains an eventually-consistent projection from the event log. This means:

- The case library may lag behind the event log
- Recently completed sagas may not yet be searchable
- APS reports its projection lag in query responses (`searchedCases` count and `embeddingsStaleSince`)

This is acceptable because precedent search is inherently tolerant of slight staleness. Missing the most recent case is far less harmful than missing a structurally similar case from months ago.

### 8.5 Schema Evolution and Case Migration

**[NEW IN v1.1]** When the W2Fuel ontology changes (new classes, deprecated predicates, namespace restructuring), existing cases may reference predicates or types that no longer exist in the current schema. This creates a version skew between the case library and the active ontology.

#### 8.5.1 Migration Strategy

APS does NOT re-write historical cases to match the new schema. Cases are historical records and their content is immutable. Instead, APS uses a layered approach:

```
┌─────────────────────────────────────────────────────┐
│                SCHEMA MIGRATION LAYERS               │
│                                                     │
│  Layer 1: Case Record (IMMUTABLE)                   │
│    The original case with original predicates.      │
│    Never modified.                                  │
│                                                     │
│  Layer 2: Migration Annotation (ADDITIVE)           │
│    Records how old predicates map to new ones.      │
│    Attached to the case as metadata.                │
│                                                     │
│  Layer 3: Re-embedding (RECOMPUTED)                 │
│    The GNN re-embeds using translated features.     │
│    Old content is hashed through the CURRENT        │
│    SemanticHasher; structural features are stable.  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

#### 8.5.2 Migration Annotation Schema

```json
{
  "@type": "aps:SchemaMigrationAnnotation",
  "aps:originalSchemaVersion": "string",
  "aps:currentSchemaVersion": "string",
  "aps:migratedAt": "xsd:dateTime",
  "aps:predicateMappings": [
    {
      "aps:oldPredicate": "IRI",
      "aps:newPredicate": "IRI | null (null = deprecated with no replacement)",
      "aps:mappingType": "renamed | merged | split | deprecated"
    }
  ],
  "aps:ontologyBridge": "IRI (reference to W2Fuel ontology bridge document, if available)",
  "aps:migrationConfidence": "number [0,1] (how confident the migration mapping is)"
}
```

#### 8.5.3 Re-embedding After Schema Change

When W2Fuel emits an `fnsr.schema.updated` event with `breaking: true`, APS should:

1. Flag all existing embeddings as stale
1. For each case, compute the migration annotation using the W2Fuel ontology bridge
1. Re-hash node content through the SemanticHasher using the current schema context
1. Re-embed with the GNN using updated semantic vectors
1. Update the vector index

This process is batched and asynchronous. During re-embedding, APS continues serving queries with stale embeddings annotated as such.

### 8.6 Negative Feedback and Case Retirement

**[NEW IN v1.1]** If a case accumulates sufficient negative feedback, it becomes a candidate for retirement:

```json
{
  "@type": "aps:RetirementPolicy",
  "aps:autoRetireThreshold": {
    "aps:minimumFeedbackCount": 10,
    "aps:feedbackScoreBelow": -0.6,
    "aps:description": "Auto-retire cases with 10+ feedback entries and score below -0.6"
  },
  "aps:reviewThreshold": {
    "aps:feedbackScoreBelow": -0.3,
    "aps:description": "Flag for human review when score drops below -0.3"
  },
  "aps:retirementIsReversible": true,
  "aps:retiredCasesRetainedFor": "P365D (kept for audit, not searchable)"
}
```

**Governance note**: Auto-retirement is an adapter policy, not core logic. The core spec only defines the feedback data model and the retirement interface. Whether retirement is automatic or requires human approval is a deployment decision.

### 8.7 Cold Start Bootstrap Protocol

**[NEW IN v1.1]** A system with zero cases has zero wisdom. The cold start problem is real and must be addressed explicitly.

#### 8.7.1 Bootstrap Strategies

|Strategy                       |Description                                                                      |When to Use                                       |
|-------------------------------|---------------------------------------------------------------------------------|--------------------------------------------------|
|**Synthetic cases**            |Generate reasoning graphs from known rule sets and domain templates              |Before any real queries; requires domain expertise|
|**Import from external corpus**|Convert existing decision records into APS case format                           |When migrating from a legacy system               |
|**Fingerprint-only period**    |Operate in fingerprint mode until enough real cases accumulate                   |When no synthetic data is available               |
|**Cross-domain seeding**       |Bootstrap a new domain with structurally similar cases from an established domain|When adding a new W2Fuel namespace                |

#### 8.7.2 Minimum Viable Case Library

APS does not define a hard minimum case count. However, the following guidance applies:

- **< 10 cases**: APS returns `no_precedent` for most queries. This is expected and acceptable.
- **10–100 cases**: Fingerprint mode is adequate. GNN mode may overfit.
- **100–1,000 cases**: GNN mode becomes useful. Cross-domain analogies start appearing.
- **1,000+ cases**: Full capability. HNSW index becomes worthwhile.

The GNN model itself requires a separate training corpus (§4.3.3). The training corpus may be larger than any single deployment’s case library (e.g., a pre-trained model shipped with the system).

-----

## 9. Query Path Integration

### 9.1 Path Routing

|Path    |APS Invoked?|Rationale                                               |
|--------|------------|--------------------------------------------------------|
|Fast    |No          |Cached responses need no precedent                      |
|Standard|No          |Standard reasoning proceeds without analogical support  |
|Full    |Yes         |High-stakes reasoning benefits from historical precedent|

APS is invoked on the full query path when:

1. MDRE or IEE explicitly requests precedent (emits `fnsr.precedent.query`)
1. The orchestrator determines that precedent search would benefit the current saga (policy-driven)

APS is **never** invoked automatically on fast or standard paths.

### 9.2 Latency Budget

The full query path has a 2-second budget. APS should complete within a 500ms allocation, broken down as:

|Phase                       |Budget|Notes                                                                  |
|----------------------------|------|-----------------------------------------------------------------------|
|Semantic hashing (all nodes)|10ms  |SimHash is fast; ~0.2ms per node for 50 nodes                          |
|Graph embedding             |60ms  |GNN forward pass (4 rounds, 64-dim, hybrid init) [revised up from 50ms]|
|Vector search               |100ms |HNSW or flat scan                                                      |
|Re-ranking (top candidates) |200ms |Greedy alignment + disanalogy for top 15 candidates                    |
|Result packaging            |30ms  |Taint wrapping, JSON-LD serialization                                  |
|Buffer                      |100ms |Network/adapter overhead                                               |

**[REVISED IN v1.1]**: Embedding budget increased by 10ms to account for hybrid initialization (semantic hashing + projection from 56→64 dimensions). Total budget remains 500ms.

If APS cannot complete within budget, it returns partial results with `degraded` status rather than timing out silently.

### 9.3 Interaction with Sibling Services

```
MDRE encounters uncertainty
    │
    ├─→ AES (if predicates are missing)
    │       AES generates hypotheses (L3)
    │
    ├─→ DES (if defaults might apply)
    │       DES provides defeasible expectations (L2)
    │
    ├─→ APS (if historical precedent might help)   ◄── THIS SERVICE
    │       APS returns analogical matches (L2+)
    │
    └─→ CSS (if counterfactual analysis needed)
            CSS simulates alternatives (L4)

IEE receives MDRE verdict
    │
    ├─→ APS (if ethical precedent might help)      ◄── ALSO THIS SERVICE
    │       APS returns cases with similar ethical evaluations
    │
    └─→ IEE renders ethical judgment
```

APS serves both MDRE (for reasoning precedent) and IEE (for ethical precedent). The same case library and the same query pipeline serve both consumers; the difference is in what aspects of the precedent the consumer attends to.

-----

## 10. Boundary Between Precedent-as-Advisory and Precedent-as-Binding

### 10.1 The Architectural Decision

In legal systems, the weight of precedent ranges from purely advisory (civil law traditions) to binding (common law *stare decisis*). FNSR chooses advisory, and this section explains why and how that choice is enforced.

### 10.2 Why Advisory

Binding precedent requires:

1. **A theory of case identity**: When is the current case “the same” as the precedent? This is the central problem of legal reasoning and has no algorithmic solution.
1. **A hierarchy of authority**: Which court’s precedent binds which lower court? FNSR has no judicial hierarchy.
1. **A mechanism for overruling**: How are bad precedents reversed? Binding precedent without a Supreme Court is stagnation.

APS has none of these. Its structural similarity is a heuristic, not a determination of legal identity. Its case library has no authority hierarchy. And it has no mechanism for formally overruling a past case (only retiring it).

Therefore, APS output is structurally, contractually, and epistemically advisory.

### 10.3 How Advisory Is Enforced

1. **Taint level**: APS output is at least L2 (Defeasible). Defeasible conclusions can be overridden by more specific reasoning. This is enforced by the taint envelope.
1. **No binding field**: The `PrecedentMatch` schema has no `binding: true` field. There is no way to express “this precedent must be followed” in the output format.
1. **Advisory note**: Every match includes an auto-generated `advisoryNote` that explicitly states the precedent is non-binding.
1. **Consumer responsibility**: The consuming service (MDRE, IEE) receives precedent as one input among many. The spec for MDRE and IEE must document how they weight precedent against direct evidence, rules, and ethical evaluation.

### 10.4 Precedent Strength

**[PROMOTED FROM “FUTURE CONSIDERATION” IN v1.1]** While precedent is always advisory, not all advice is equal. APS now tracks precedent strength through the feedback mechanism (§6.5, §8.6):

- **Endorsement count**: How many times this case was returned as precedent and subsequently endorsed by the consuming service.
- **Rejection count**: How many times this case was returned but rejected as a poor match.
- **Feedback score**: The normalized balance between endorsements and rejections.
- **Outcome accuracy**: Whether the precedent case’s verdict was later confirmed as correct.

Precedent strength is reported in the `caseSummary.precedentStrength` field of each match (§7.2) and influences ranking through the `w_feedback` composite score weight (§6.4). It does not change the advisory nature of the output—a strong precedent is still defeasible advice, not binding authority.

-----

## 11. Performance and Resource Requirements

### 11.1 Complexity Analysis

|Operation                   |Time Complexity              |Space Complexity                     |
|----------------------------|-----------------------------|-------------------------------------|
|Semantic hashing (per node) |O(T) where T = content tokens|O(d_s) where d_s = semantic dimension|
|GNN embedding (single graph)|O(K × (V + E) × d²)          |O(V × d)                             |
|Flat index search           |O(N × d)                     |O(N × d)                             |
|HNSW index search           |O(log N × d)                 |O(N × d × M)                         |
|Greedy alignment            |O(V_q × V_c)                 |O(V_q × V_c)                         |
|Case serialization          |O(V + E)                     |O(V + E)                             |

Where: K = message-passing rounds (4), V = nodes, E = edges, d = hidden dimension (64/128), d_s = semantic dimension (32), N = cases in library, M = HNSW connections (16), T = tokens per node.

### 11.2 Browser Runtime Estimates

**[REVISED IN v1.1]**: Updated to reflect hybrid embedding and WASM acceleration.

For a reasoning graph with 50 nodes and 80 edges, and a case library of 1,000 cases:

|Operation                      |JS (pure)|WASM |Memory        |
|-------------------------------|---------|-----|--------------|
|Semantic hashing (50 nodes)    |~5ms     |~1ms |~100KB        |
|GNN embedding                  |~15ms    |~3ms |~600KB        |
|Flat index search              |~5ms     |~2ms |~1MB (vectors)|
|Greedy alignment (5 candidates)|~10ms    |~5ms |~200KB        |
|Total query                    |~35ms    |~11ms|~2MB peak     |

For a case library of 100,000 cases with HNSW:

|Operation                      |JS (pure)|WASM |Memory        |
|-------------------------------|---------|-----|--------------|
|Semantic hashing + GNN         |~20ms    |~4ms |~700KB        |
|HNSW search                    |~3ms     |~1ms |~100MB (index)|
|Greedy alignment (5 candidates)|~10ms    |~5ms |~200KB        |
|Total query                    |~33ms    |~10ms|~100MB peak   |

**Note**: Pure JS estimates assume optimized Float64Array operations without naive nested loops. WASM estimates assume a compiled C/Rust kernel with deterministic operation ordering. Actual performance will vary by environment.

### 11.3 Resource Limits

|Parameter                   |Default  |Configurable?    |
|----------------------------|---------|-----------------|
|Max case library size (flat)|10,000   |Yes (via adapter)|
|Max case library size (HNSW)|1,000,000|Yes (via adapter)|
|Max reasoning graph nodes   |500      |Yes              |
|Max reasoning graph edges   |2,000    |Yes              |
|Max re-ranking candidates   |15       |Yes              |
|Query timeout               |500ms    |Yes              |
|Max embedding dimensions    |256      |Yes              |
|Max semantic hash dimension |64       |Yes              |

-----

## 12. Error Handling

### 12.1 Error Taxonomy

|Error Code           |Severity|Meaning                                     |Recovery                                                |
|---------------------|--------|--------------------------------------------|--------------------------------------------------------|
|`APS_NO_MODEL`       |Degraded|GNN weights unavailable                     |Fall back to fingerprint mode                           |
|`APS_NO_LIBRARY`     |Degraded|Case library empty                          |Return `no_precedent` status                            |
|`APS_STALE_INDEX`    |Warning |Embeddings older than case library          |Return results with staleness annotation                |
|`APS_GRAPH_TOO_LARGE`|Rejected|Input graph exceeds node/edge limits        |Return error with limits                                |
|`APS_TIMEOUT`        |Degraded|Query exceeded time budget                  |Return partial results                                  |
|`APS_MODEL_MISMATCH` |Error   |Query embedding model ≠ index model         |Reject (cannot compare embeddings from different models)|
|`APS_CORRUPT_CASE`   |Warning |Case record fails integrity check           |Skip case, log warning, continue search                 |
|`APS_SCHEMA_SKEW`    |Warning |Case references deprecated W2Fuel predicates|Apply migration annotation, re-embed if possible        |
|`APS_WASM_MISMATCH`  |Error   |WASM module fails equivalence verification  |Fall back to pure JS                                    |

### 12.2 Graceful Degradation Hierarchy

```
Full capability (GNN/WASM + HNSW + complete library + feedback data)
    │
    ├─ WASM unavailable → Pure JS (slower but identical results)
    │
    ├─ GNN unavailable → Fingerprint mode (reduced accuracy, disclosed)
    │
    ├─ Index stale → Search with staleness annotation
    │
    ├─ Library partial → Search available cases, report coverage
    │
    ├─ Schema skew → Apply migration annotations, annotate results
    │
    ├─ Library empty → Return no_precedent (NOT an error)
    │
    └─ Everything unavailable → Return no_precedent with degradation report
```

At no point does APS throw an unrecoverable error for operational conditions. The only hard errors are schema violations (malformed input), model mismatches (incompatible embedding versions), and WASM verification failures (which fall back to JS, not failure).

-----

## 13. Conformance and Testing

### 13.1 Conformance Levels

**Level 1: Core** (required for all implementations)

- Case schema validation (§2.1.1)
- Structural fingerprint embedding with content SimHash (§4.2.3)
- Flat vector index (§5.3.1)
- Precedent matching pipeline (§6.1)
- Event contract compliance (§7)
- Graceful degradation for empty library (§1.4)
- Deterministic output (§1.3)

**Level 2: Standard** (required for production use)

- GNN hybrid embedding (§4.2.1, §4.2.2)
- Structural alignment maps with greedy algorithm (§6.2)
- Disanalogy annotation including semantic disanalogies (§6.3)
- Composite similarity scoring with feedback (§6.4, §6.5)
- Case library management with feedback tracking (§8)
- Schema migration annotations (§8.5)

**Level 3: Extended** (optional optimizations)

- HNSW vector index (§5.3.2)
- Product quantization
- WASM-accelerated arithmetic (§1.3.2)
- Batch embedding
- Learned SemanticHasher (LLM-based)
- Auto-retirement policy (§8.6)

### 13.2 Test Suite

#### Determinism Tests

```json
{
  "@type": "aps:TestSuite",
  "aps:tests": [
    {
      "aps:name": "deterministic_embedding",
      "aps:description": "Same graph + same weights + same semantic vectors = same embedding (bit-identical)",
      "aps:iterations": 100,
      "aps:assertion": "all_identical"
    },
    {
      "aps:name": "deterministic_search",
      "aps:description": "Same query + same index = same ranked results",
      "aps:iterations": 100,
      "aps:assertion": "all_identical"
    },
    {
      "aps:name": "deterministic_alignment",
      "aps:description": "Same query graph + same case = same alignment map",
      "aps:iterations": 100,
      "aps:assertion": "all_identical"
    },
    {
      "aps:name": "wasm_js_equivalence",
      "aps:description": "WASM and pure JS implementations produce bit-identical results",
      "aps:iterations": 1000,
      "aps:assertion": "all_identical across implementations"
    }
  ]
}
```

#### Structural Similarity Tests

```json
{
  "@type": "aps:TestSuite",
  "aps:tests": [
    {
      "aps:name": "isomorphic_graphs_high_similarity",
      "aps:description": "Two isomorphic reasoning graphs with different entity names but same domain should have similarity > 0.85",
      "aps:input": {
        "graphA": "employment dispute with gap detection",
        "graphB": "different employment dispute with gap detection (same structure, different entities)"
      },
      "aps:assertion": "similarity > 0.85"
    },
    {
      "aps:name": "cross_domain_structural_match",
      "aps:description": "Two isomorphic graphs from different domains should have moderate similarity (0.5-0.8)",
      "aps:input": {
        "graphA": "employment dispute with gap detection",
        "graphB": "real estate dispute with gap detection (same structure, different domain)"
      },
      "aps:assertion": "0.5 < similarity < 0.8"
    },
    {
      "aps:name": "different_structure_low_similarity",
      "aps:description": "Two graphs with same domain but different reasoning patterns should have similarity < 0.5",
      "aps:input": {
        "graphA": "simple linear deduction (3 facts → 1 conclusion)",
        "graphB": "complex branching with defaults and gaps (15 nodes, 5 defeats)"
      },
      "aps:assertion": "similarity < 0.5"
    },
    {
      "aps:name": "no_precedent_graceful",
      "aps:description": "Query against empty library returns no_precedent status, not error",
      "aps:assertion": "status == 'no_precedent' && matches.length == 0"
    },
    {
      "aps:name": "taint_floor_L2",
      "aps:description": "Even when source case is L0, output taint is at least L2",
      "aps:assertion": "all matches have taint >= L2"
    },
    {
      "aps:name": "adversarial_exclusion",
      "aps:description": "Cases with L5 taint are never returned as precedent",
      "aps:assertion": "no match references an L5 case"
    }
  ]
}
```

#### Semantic Safety Tests

**[NEW IN v1.1]**

```json
{
  "@type": "aps:TestSuite",
  "aps:name": "semantic_safety",
  "aps:description": "Tests that structurally isomorphic but semantically divergent graphs do NOT match at high similarity",
  "aps:tests": [
    {
      "aps:name": "benign_vs_harmful_structure",
      "aps:description": "Structurally identical graphs with benign vs. harmful content should have similarity < 0.6",
      "aps:input": {
        "graphA": "recipe-style reasoning about food preparation",
        "graphB": "recipe-style reasoning about dangerous substance preparation (same topology)"
      },
      "aps:assertion": "similarity < 0.6",
      "aps:rationale": "Semantic content vectors must discriminate even when topology matches"
    },
    {
      "aps:name": "same_domain_different_subject",
      "aps:description": "Same domain, same structure, but different subject matter should have moderate similarity",
      "aps:input": {
        "graphA": "employment case about salary dispute",
        "graphB": "employment case about harassment claim (similar structure)"
      },
      "aps:assertion": "0.4 < similarity < 0.7",
      "aps:rationale": "Same domain boosts similarity but content divergence should temper it"
    },
    {
      "aps:name": "semantic_hash_discrimination",
      "aps:description": "SimHash of 'background check' and 'title search' should have cosine distance > 0.3",
      "aps:assertion": "cosine_distance(simhash('background check'), simhash('title search')) > 0.3"
    }
  ]
}
```

#### Edge-Canonical Test

```json
{
  "@type": "aps:TestSuite",
  "aps:tests": [
    {
      "aps:name": "browser_execution",
      "aps:description": "Full query pipeline executes in browser environment",
      "aps:environment": "browser (Chrome, Firefox, Safari)",
      "aps:requirements": [
        "No Node.js-only APIs",
        "No file system access",
        "No network requests (all data loaded from JSON)",
        "Deterministic results matching Node.js execution"
      ]
    },
    {
      "aps:name": "node_execution",
      "aps:description": "Full query pipeline executes via node index.js",
      "aps:environment": "Node.js >= 18",
      "aps:requirements": [
        "Single-file entry point",
        "JSON-LD file input/output",
        "No external services required"
      ]
    }
  ]
}
```

### 13.3 Spec Test Verification

**Could a developer evaluate, reason about, and execute this system using only a browser, a local NodeJS runtime, and JSON-LD files?**

1. **Model weights**: Loaded from a JSON file containing base64-encoded Float64Arrays. ✓
1. **Case library**: Loaded from a JSON-LD file containing case records. ✓
1. **Vector index**: Built in-memory from case embeddings (flat index). ✓
1. **GNN inference**: Pure JavaScript matrix operations (or WASM loaded from local file). ✓
1. **Semantic hashing**: SimHash requires no model files—deterministic algorithm over content tokens. ✓
1. **Query execution**: Takes a JSON-LD reasoning graph, returns a JSON-LD precedent result. ✓
1. **No infrastructure**: No database, no message broker, no background workers. ✓

**Answer: Yes.**

-----

## 14. Glossary

|Term                      |Definition                                                                                                                                             |
|--------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
|**Alignment Map**         |Mapping between nodes/edges in a query graph and a precedent case graph showing structural correspondence                                              |
|**Case**                  |A self-contained record of a completed reasoning episode including input, reasoning graph, verdict, ethical evaluation, and optional outcome           |
|**Case Library**          |The collection of all stored reasoning cases, searchable by APS                                                                                        |
|**Cold Start**            |The condition where a new deployment has zero or very few cases in the library                                                                         |
|**Composite Similarity**  |Weighted combination of embedding similarity, alignment coverage, disanalogy penalty, outcome bonus, recency factor, and feedback score                |
|**Contrastive Learning**  |Training objective that pulls similar graphs together and pushes dissimilar graphs apart in embedding space                                            |
|**Disanalogy**            |An explicit annotation of where an analogy between query and precedent breaks down                                                                     |
|**Feedback Score**        |Normalized endorsement-to-rejection ratio for a case’s utility as precedent                                                                            |
|**GNN**                   |Graph Neural Network; here, a message-passing architecture that embeds reasoning graphs into vectors                                                   |
|**Hard Negative**         |A training example that is superficially similar but genuinely dissimilar to the anchor, used to teach the model discrimination                        |
|**HNSW**                  |Hierarchical Navigable Small World; an approximate nearest-neighbor index for efficient vector search                                                  |
|**Hybrid Embedding**      |Node initialization that combines structural features (type, taint) with semantic content vectors                                                      |
|**MPNN**                  |Message-Passing Neural Network; the specific GNN architecture used by APS                                                                              |
|**Oversample Factor**     |The ratio of candidates retrieved from vector search to final results returned (default 3x)                                                            |
|**Precedent**             |A historical reasoning case that is structurally analogous to the current query                                                                        |
|**Precedent Strength**    |Accumulated endorsement/rejection data reflecting a precedent’s utility over time                                                                      |
|**Reasoning Graph**       |A directed labeled graph capturing the structure of a reasoning episode (facts, rules, inferences, gaps, defaults, hypotheses, and their relationships)|
|**Schema Migration**      |The process of annotating historical cases when the W2Fuel ontology changes                                                                            |
|**Semantic Hasher**       |Pluggable adapter that produces fixed-dimension content vectors from node JSON-LD content                                                              |
|**SimHash**               |Locality-sensitive hashing algorithm used as the reference SemanticHasher implementation                                                               |
|**Structural Fingerprint**|A handcrafted feature vector capturing coarse graph topology and content signature, used as a fallback when GNN is unavailable                         |
|**Vector Index**          |A data structure enabling efficient nearest-neighbor search over embedding vectors                                                                     |
|**WASM**                  |WebAssembly; a portable binary instruction format used as a normative accelerator for APSArithmetic                                                    |

-----

## 15. References

1. Gilmer, J., et al. (2017). Neural Message Passing for Quantum Chemistry. *ICML 2017*.
1. Malkov, Y. A., & Yashunin, D. A. (2018). Efficient and Robust Approximate Nearest Neighbor using Hierarchical Navigable Small World Graphs. *IEEE TPAMI*.
1. Gentner, D. (1983). Structure-Mapping: A Theoretical Framework for Analogy. *Cognitive Science*, 7(2), 155–170.
1. Forbus, K. D., et al. (2017). Extending Structure-Mapping to Support Analogical Reasoning. *Cognitive Science*, 41(5), 1234–1264.
1. Charikar, M. S. (2002). Similarity Estimation Techniques from Rounding Algorithms. *STOC 2002*. (SimHash)
1. Chen, T., et al. (2020). A Simple Framework for Contrastive Learning of Visual Representations. *ICML 2020*. (Contrastive learning framework)
1. The Plot: FNSR Architectural Narrative, §4 (Learning Layer), §10 (Cognitive Metaphors).
1. FNSR Integration Specification v1.0, §4.2 (APS Integration Points).
1. MDRE Technical Specification v1.3 (Companion document).
1. IEE Integral Ethics Engine Specification (Companion document).
1. CSS Counterfactual Simulation Service Specification v2.0, §1.3 (Determinism), §1.4 (Deterministic Arithmetic).
1. W2Fuel Ontological Schema Service Specification v1.1.1 (Schema evolution, ontology bridges).
1. Basic Formal Ontology (BFO) 2020 Specification.
1. Common Core Ontologies (CCO) Documentation.

-----

## 16. Document History

|Version|Date      |Changes                                                                                                                                                                                                                                                                                                                                                                         |
|-------|----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|1.0.0  |2026-02-05|Initial specification                                                                                                                                                                                                                                                                                                                                                           |
|1.1.0  |2026-02-05|Hybrid embedding with semantic content vectors (§4.2.2); contrastive training objective (§4.3.3); greedy alignment algorithm (§6.2.1); WASM accelerator (§1.3.2); schema migration (§8.5); feedback mechanism (§6.5, §7.3, §8.6); cold start protocol (§8.7); cross-platform CI matrix (§1.3.3); semantic safety tests (§13.2); precedent strength promoted to normative (§10.4)|

-----

*This specification describes APS as the accumulation of reasoning experience into searchable wisdom. It remembers past cases, recognizes structural and semantic patterns, and offers advisory counsel—without ever binding the system to repeat its past decisions. APS is how FNSR learns from experience without being imprisoned by it.*