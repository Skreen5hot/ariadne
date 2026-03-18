# Technical Specification v1.6: Causal OS Kernel
## BFO 2020–Aligned Edge-Canonical Causal Prediction Runtime

> **Changelog from v1.5 — v1.0 release hardening:**
>
> *Must items (correctness and auditability blockers):*
> - Surrogate Causal Validity Contract added: synthetic SCM test suite, `causal:Surrogate_Causal_Mismatch` status, production pass-rate threshold (§2.5)
> - ONNX→WASM compilation pipeline formally specified: toolchain, flags, signing, and backend-delegation prohibition (§3.6.3)
> - Reference test vectors defined with canonical input/output/hash triples for all critical FP operations (§3.6.5)
> - Halting criterion hardened: dual test — variance AND bimodality coefficient $b$; `nonConvergentReason` added to halt record (§4.3)
>
> *Should items (production safety and trust):*
> - WASM module security contract: signed binaries, cert chain verification, sandbox resource caps for all learned modules (§3.7)
> - Policy network training regime specified: data contract, convergence criteria, minimum synthetic SCM pass rate (§4.2)
> - MEDR SHACL complexity budget: `max_shacl_calls` counter added to algorithm and `ExecutionContext` (§3.2, §5.3.2)
> - Attribution method defaults enforced: `"structural"` required for online inference; Shapley requires explicit opt-in (§6.6.2)
> - `ExecutionContext`, `ExecutionBundle`, epistemic registry, `context.jsonld`, Output Contract, and Appendix A updated throughout
>
> **Inherited from v1.5:**
> - Deterministic Numerics Contract (§3.6)
> - `ExecutionContext` with `encoderProfile`, `mathKernel`, `repairProposerRef` (§3.2)
> - MCTS policy/value prior term (§4.2)
> - RepairProposer abstract API; MEDR with learned candidates (§5.3)
> - `alternateRepairs` in RepairProvenance (§5.4)
> - MEDR Domain Policy Registry (§5.5)
> - `edge-rich` encoder profile (§6.5)
> - Causal Attribution layer (§6.6)
>
> **Inherited from v1.4:**
> - `CausalEdge.relation` string literals replaced with canonical RO causal IRIs (§3.4)
> - MEDR greedy loop hardened with `max_edits` guard; `causal:Repair_Failed` status added (§5.3, §7.2)
> - `LatentBridge` encode step formally specifies entity-count aggregation via max-pooling with `MAX_ENTITIES` cap (§6.2)
>
> **Inherited from v1.3:**
> - All equations restored and formally stated
> - BFO version pinned to BFO 2020 throughout
> - SHACL shapes corrected to target domain subclasses, not BFO base classes
> - L₂ projection replaced with Minimum-Edit Discrete Repair (MEDR) algorithm
> - MCTS and do-calculus integration formally specified via Causal State Nodes
> - Causal DAG representation and lifecycle formally defined
> - `BfoTemporalRegion` snapshot replaced with `ContinuantSlice` pattern
> - Resolver contract hardened: pre-fetch isolation eliminates async non-determinism
> - Halting condition renamed `Non_Convergent_Rollout`; Wolfram term retired
> - Epistemic status values assigned canonical IRIs under `causal:` namespace
> - Repair provenance record added to `Repaired_Inference` outputs
> - Neural-symbolic interface (`LatentBridge`) formally specified

---

## 1. Architectural Philosophy: The Causal OS Kernel

The system acts as a **Causal Operating System**. It does not manage hardware; it manages epistemic state, temporal transitions, and causal interventions. Its purpose is to reason about what will happen, what would have happened under different conditions, and how confident it can be in either answer.

In strict adherence to the **Edge-Canonical First Principle**, the core system is a **deterministic pure function library**. It possesses no native concept of a database, network, or persistent infrastructure. All inputs are injected as valid JSON-LD graphs bounded by SHACL shapes. All outputs are yielded as JSON-LD projections with explicit provenance, cryptographic seeds, and epistemic uncertainty bounds.

The kernel operates in two well-separated phases:

1. **Pre-execution phase**: All external resources (SHACL shapes, ontology fragments, resolver results) are fetched, validated, and frozen into an immutable `ExecutionBundle`. This phase is inherently async and may be stateful.
2. **Execution phase**: A fully deterministic, synchronous computation over the sealed `ExecutionBundle`. No I/O is permitted. Reproducibility is guaranteed by the cryptographic seed and the `model_hash`.

This separation is the architectural enforcement of the Edge-Canonical First Principle. The word "pure" in "pure function library" refers exclusively to the execution phase.

**Ontology baseline:** All BFO references in this specification conform to **BFO 2020** (IRI prefix `http://purl.obolibrary.org/obo/BFO_`). Implementers must not silently substitute BFO 2.0, which has incompatible class hierarchies and IRI patterns for several continuant categories.

**Deterministic numerics baseline:** Reproducibility of the execution phase is not solely a matter of CSPRNG seeding. Floating-point operations in JS engines and WASM runtimes are subject to platform-dependent rounding behaviour in edge cases. This specification therefore mandates a **Deterministic Numerics Contract** (Section 3.6) governing all floating-point computation within the execution phase. The word "deterministic" in this specification means bit-identical outputs given the same `ExecutionBundle`, not merely statistically equivalent outputs.

---

## 2. Formal Mathematical Foundation

The kernel relies on explicit mathematical contracts for process transitions, interventions, system halting, and constraint repair. All contracts are stated here prior to their algorithmic expression in later sections.

### 2.1 Ontological Primitives

Let the state of the world at temporal instant $t$ be represented by a **ContinuantSlice** $\mathcal{S}_t$ (see Section 3.3 for its formal type definition). This slice comprises:

- $\mathbf{C}_t$: the set of **independent continuants** (material entities, objects) present and participating
- $\mathbf{Q}_t$: the set of **specifically dependent continuants** (qualities) inhering in members of $\mathbf{C}_t$
- $\mathbf{D}_t$: the set of **dispositions** inhering in members of $\mathbf{C}_t$, which may or may not be realized

A **Process** $P$ occupies a temporal interval $[t_0, t_1]$, bounded by temporal instants $t_0$ (process boundary, start) and $t_1$ (process boundary, end), and has participants drawn from $\mathbf{C}_{t_0}$.

### 2.2 Process Transition and Structural Equations

The generation of new quality values $\mathbf{Q}_{t_1}$ resulting from Process $P$ is governed by a **Structural Causal Equation (SCE)**:

$$\mathbf{Q}_{t_1} = f_P\!\left(\mathbf{Q}_{t_0},\, \mathbf{D}_{t_0},\, \mathbf{C}_{t_0};\, \theta_P\right) + \mathbf{U}_P$$

Where:

| Symbol | Meaning |
|---|---|
| $f_P$ | The causal mechanism function for Process $P$; may be a closed-form model or a neural surrogate |
| $\theta_P$ | Known or learned causal mechanism parameters (weights of the SCM edge for $P$) |
| $\mathbf{U}_P$ | Exogenous noise / unobserved confounders entering the equation at $P$; assumed independent of $\mathbf{C}_{t_0}$ under the no-hidden-common-cause assumption for the identified subgraph |

When $f_P$ is a neural surrogate, $\theta_P$ corresponds to the weights of the `LatentBridge` network (Section 6). When $f_P$ is a symbolic mechanism, $\theta_P$ is an explicit parameter vector drawn from the causal DAG annotation.

The full collection of SCEs for all processes in the causal DAG $\mathcal{G}$ constitutes the **Structural Causal Model (SCM)**:

$$\mathcal{M} = \langle \mathbf{V},\, \mathbf{U},\, \mathcal{F},\, P(\mathbf{U}) \rangle$$

Where $\mathbf{V}$ is the set of endogenous variables (qualities and dispositions indexed to process nodes), $\mathcal{F}$ is the set of structural equations $\{f_P\}$, and $P(\mathbf{U})$ is the joint distribution over exogenous noise terms.

### 2.3 Counterfactual Interventions (do-calculus)

When evaluating a counterfactual that forces Process $P$ to take value $p^*$, we perform a **do-intervention**: all incoming edges to $P$ in $\mathcal{G}$ are severed, replacing $P$'s structural equation with the constant $P := p^*$. The resulting mutilated graph is denoted $\mathcal{G}_{\overline{P}}$.

The **interventional distribution** over post-process qualities is:

$$P\!\left(\mathbf{Q}_{t_1} \mid do(P = p^*)\right) = \int P\!\left(\mathbf{Q}_{t_1} \mid P = p^*,\, \mathbf{C}_{t_0} = \mathbf{c},\, \mathbf{U}_P = \mathbf{u}\right) P(\mathbf{c})\, P(\mathbf{u})\; d\mathbf{c}\; d\mathbf{u}$$

When the target quantity is identifiable from observational data via the **backdoor criterion**, the estimator simplifies to:

$$P\!\left(\mathbf{Q}_{t_1} \mid do(P = p^*)\right) = \sum_{\mathbf{z}} P\!\left(\mathbf{Q}_{t_1} \mid P = p^*,\, \mathbf{Z} = \mathbf{z}\right) P(\mathbf{Z} = \mathbf{z})$$

Where $\mathbf{Z}$ is any valid adjustment set satisfying the backdoor criterion relative to $(P, \mathbf{Q}_{t_1})$ in $\mathcal{G}$.

When the backdoor criterion fails but the **front-door criterion** is satisfied via a mediator set $\mathbf{M}$:

$$P\!\left(\mathbf{Q}_{t_1} \mid do(P = p^*)\right) = \sum_{\mathbf{m}} \left[\sum_{\mathbf{p}} P(\mathbf{m} \mid \mathbf{p})\, P(\mathbf{p})\right] P\!\left(\mathbf{Q}_{t_1} \mid \mathbf{m},\, p^*\right)$$

### 2.4 Epistemic Uncertainty and Hidden Confounding

If no valid identification strategy exists (neither backdoor, front-door, nor do-calculus derivation via the **ID algorithm**), the kernel does not fail silently. It computes a **sensitivity interval** using Rosenbaum bounds parametrized by $\Gamma \geq 1$, which quantifies the degree of departure from unconfoundedness required to explain away an effect:

$$\frac{1}{1+\Gamma} \leq \frac{P(\text{treated} \mid X_i,\, U_i)}{P(\text{treated} \mid X_j,\, U_j)} \leq \frac{\Gamma}{1+\Gamma}$$

The output yields a probability interval $[p^{-}(\Gamma),\, p^{+}(\Gamma)]$ at the analyst-specified $\Gamma$, together with the critical $\Gamma^*$ at which the estimated effect crosses the null. This is surfaced with:

```
EpistemicStatus: causal:Unidentifiable_Confounding
causal:sensitivityGamma: <value>
causal:effectInterval: [lower, upper]
causal:criticalGamma: <Gamma*>
```

### 2.5 Surrogate Causal Validity Contract

This section addresses the deepest correctness vulnerability in the system. Neural surrogates trained on observational data learn the conditional distribution $P(\mathbf{Q}_{t_1} \mid \mathbf{Q}_{t_0}, P)$. This is **not** the same as the interventional distribution $P(\mathbf{Q}_{t_1} \mid do(P = p^*))$ required by the SCM. A surrogate that passes SHACL validation and hash verification may still produce systematically biased counterfactual estimates if it has not been tested against known causal ground truth.

This contract specifies the required test suite and acceptance criteria that must be satisfied before a surrogate's `model_hash` is admitted to production.

#### 2.5.1 Synthetic SCM Test Suite

A **Synthetic SCM Test Suite** is a collection of $T$ test cases, each of the form:

$$\tau_i = \langle \mathcal{M}_i^{\text{syn}},\, \text{query}_i,\, P^*_i(\mathbf{Q}_{t_1} \mid do(\cdot)) \rangle$$

Where:
- $\mathcal{M}_i^{\text{syn}}$ is a synthetic SCM with fully known causal mechanisms and no hidden confounders
- $\text{query}_i$ is a do-intervention or counterfactual query applied to $\mathcal{M}_i^{\text{syn}}$
- $P^*_i$ is the analytically derived ground-truth interventional distribution

The suite must include at minimum the following SCM structural classes:

| SCM class | Minimum test cases | What is tested |
|---|---|---|
| Linear Gaussian chain ($A \to B \to C$) | 10 | Do-calculus correctness on direct and mediated paths |
| Confounded fork ($A \leftarrow U \to B$, $A \to B$) | 10 | Surrogate bias under unobserved confounder |
| V-structure / collider ($A \to C \leftarrow B$) | 5 | Collider conditioning error |
| Non-linear monotone ($f_P$ is sigmoid or ReLU) | 10 | Non-linear causal mechanism approximation |
| Multi-process chain (length $\geq 4$) | 5 | Compounding error over horizon |

The suite is serialized as a JSON-LD document, hash-verified as `context.surrogate_suite_hash`, and loaded into the `ExecutionBundle` as `surrogateSuiteBytes`.

#### 2.5.2 Causal Mismatch Metric

For each test case $\tau_i$, the surrogate's interventional estimate $\hat{P}_i$ is compared to ground truth $P^*_i$ using the **Maximum Mean Discrepancy (MMD)** between $M = 1000$ samples from each:

$$\text{MMD}^2(\hat{P}_i, P^*_i) = \mathbb{E}_{x,x' \sim \hat{P}_i}\!\left[k(x,x')\right] - 2\,\mathbb{E}_{x \sim \hat{P}_i, y \sim P^*_i}\!\left[k(x,y)\right] + \mathbb{E}_{y,y' \sim P^*_i}\!\left[k(y,y')\right]$$

using a Gaussian RBF kernel $k(x,y) = \exp(-\|x-y\|^2 / 2\sigma^2)$ with bandwidth $\sigma$ set to the median heuristic over the combined sample.

The **surrogate causal error rate** is:

$$\text{SCE} = \frac{1}{T} \sum_{i=1}^{T} \mathbf{1}\!\left[\text{MMD}^2(\hat{P}_i, P^*_i) > \delta\right]$$

where $\delta$ is the MMD threshold, defaulting to $\delta = 0.05$.

#### 2.5.3 Production Acceptance Threshold

A surrogate is admitted to production if and only if:

$$\text{SCE} \leq \tau_{\text{max}}$$

where $\tau_{\text{max}} = 0.10$ by default (no more than 10% of test cases exceed the MMD threshold). This threshold may be tightened by domain policy but must never be relaxed above 0.10 for production deployment.

If a surrogate fails this threshold, execution is aborted and all outputs are flagged:

```
EpistemicStatus: causal:Surrogate_Causal_Mismatch
causal:surrogateErrorRate: <SCE>
causal:surrogateThreshold: <τ_max>
causal:failingTestCases: [<τ_i.id>, ...]
```

This is not a recoverable error. A failing surrogate must be retrained or replaced.

#### 2.5.4 Validation Lifecycle

The surrogate validation suite is run once during the **pre-execution phase** by the `ResourceCollector`, after `model_hash` verification and before the `ExecutionBundle` is sealed. The pass/fail result and the full per-test-case MMD scores are embedded in the sealed bundle as `surrogateValidationReport`. The kernel reads this report at execution start; if the report is absent or records a failure, execution is aborted.

---

## 3. The Edge Contract and Deterministic Execution

Execution must be perfectly reproducible across any standard V8/SpiderMonkey runtime at the same engine version. Reproducibility is a **contract**, not a best-effort property.

### 3.1 Pre-Execution Phase: Resource Isolation

Before the kernel executes, the **ResourceCollector** performs all async operations and seals results into an immutable `ExecutionBundle`. The kernel receives only the sealed bundle. This is the only place where async, network, or file I/O is permitted.

```typescript
type ResourceCollector = (
  query: CausalQuery,
  resolvers: ResolverPool,
  timeoutMs: number
) => Promise<ExecutionBundle>;

type ExecutionBundle = Readonly<{
  snapshot:                 ContinuantSlice;          // Frozen world-state (see §3.3)
  causalDag:                FrozenCausalDag;           // Sealed graph (see §3.4)
  shapes:                   ReadonlyMap<IRI, string>;  // All SHACL shapes, pre-fetched
  modelBytes:               Uint8Array;                // Primary ONNX/WASM encoder binary
  repairProposerBytes:      Uint8Array | null;         // RepairProposer WASM module, or null
  policyModelBytes:         Uint8Array | null;         // Policy/value network WASM module, or null
  surrogateSuiteBytes:      Uint8Array;                // Synthetic SCM test suite (§2.5); required
  surrogateValidationReport: SurrogateValidationReport; // Pre-computed by ResourceCollector (§2.5.4)
  domainRepairPolicies:     ReadonlyArray<DomainRepairPolicy>; // §5.5 registry
  context:                  ExecutionContext;           // Seeds, caps, hashes, profiles
}>;
```

No field of `ExecutionBundle` may be mutated during execution. Implementers must use `Object.freeze` recursively or an equivalent structural freeze before passing the bundle to the kernel.

### 3.2 Predictor Signature

The kernel entry point is a **pure synchronous function** over a sealed bundle:

```typescript
// Encoder profile selection (see §6.5 for edge-rich specification)
type EncoderProfile = "edge-default" | "edge-rich";

// Math kernel compliance level (see §3.6)
type MathKernelSpec =
  | { mode: "wasm-deterministic"; wasmRuntime: string; runtimeVersion: string }
  | { mode: "softfloat";          libraryHash: string }
  | { mode: "engine-scoped";      engineName: string; engineVersion: string };

type ExecutionContext = {
  random_seed:          string;          // Hex string; initializes CSPRNG (ChaCha20)
  model_hash:           string;          // SHA-256 of modelBytes; verified on entry
  max_memory_mb:        number;          // WASM heap cap; kernel aborts if exceeded
  encoderProfile:       EncoderProfile;  // "edge-default" (max-pool) or "edge-rich" (GNN/attention)
  mathKernel:           MathKernelSpec;  // Deterministic numerics declaration (§3.6)
  repairProposerRef:    string | null;   // SHA-256 of RepairProposer WASM module, or null
  max_edits:            number;          // MEDR edit ceiling; default = 3 × |V₀|; must be finite
  max_shacl_calls:      number;          // MEDR SHACL validation budget; default = 10 × |V₀|
  surrogate_suite_hash: string;          // SHA-256 of surrogateSuiteBytes; required for production
  policy_model_hash:    string | null;   // SHA-256 of policyModelBytes; null if no policy model
  signer_cert_hash:     string | null;   // SHA-256 of signing certificate (§3.7); null for dev only
};

type Predictor = (
  bundle:  ExecutionBundle,
  query:   CausalQuery,
  horizon: number
) => PredictionTree;
```

The kernel **must not** use `Math.random()`, `Date.now()`, `performance.now()`, or any API that reads ambient non-deterministic state. All randomness flows from the CSPRNG seeded by `random_seed`. The implementation must use a seedable CSPRNG (ChaCha20 recommended) for all stochastic sampling.

### 3.3 ContinuantSlice: Replacing BfoTemporalRegion as Snapshot

In BFO 2020, a `TemporalRegion` is the **time at which** processes and states obtain — it is not a carrier of state. Using it as a world-state snapshot was a type error in v1.2.

The correct representation is a **ContinuantSlice**: the set of continuants together with the qualities and dispositions inhering in them, all indexed to a specific temporal instant.

```typescript
type ContinuantSlice = {
  "@type":          "causal:ContinuantSlice";
  atInstant:        TemporalInstantIRI;         // bfo:TemporalInstant
  participants:     IndependentContinuant[];
  qualityAssignments: QualityBinding[];         // Q inhering in C at t
  dispositionAssignments: DispositionBinding[]; // D inhering in C at t
};

type QualityBinding = {
  quality:   IRI;   // subclass of bfo:0000019
  inheres_in: IRI;  // reference to IndependentContinuant IRI
  value:     number | string | boolean;
  unit?:     IRI;
};

type DispositionBinding = {
  disposition: IRI;   // subclass of bfo:0000016
  inheres_in:  IRI;
  realized:    boolean;
};
```

### 3.4 Causal DAG: Representation and Lifecycle

The SCM requires an explicit causal DAG. In v1.2 this was assumed present but never specified. The `FrozenCausalDag` type defines both its structure and its validation contract.

```typescript
type CausalNode =
  | { kind: "quality";     iri: IRI; description: string }
  | { kind: "process";     iri: IRI; mechanismRef: MechanismRef }
  | { kind: "disposition"; iri: IRI; description: string };

// CausalRelation uses canonical RO IRIs for all edge types.
// String aliases are forbidden as CausalEdge.relation values.
// See mapping table below.
type CausalRelationIRI =
  | "http://purl.obolibrary.org/obo/RO_0002410"  // causally related to (symmetric; use when direction unknown)
  | "http://purl.obolibrary.org/obo/RO_0002411"  // causally upstream of (strict; source generates downstream effect)
  | "http://purl.obolibrary.org/obo/RO_0002418"  // causally upstream of or within (includes intra-process causation)
  | "http://purl.obolibrary.org/obo/RO_0002566"  // causally downstream of (inverse of RO_0002411; for reverse edges)
  | "http://purl.obolibrary.org/obo/RO_0002304"; // causally upstream of, positive effect (positive modulation)

type CausalEdge = {
  from:      IRI;               // Source node IRI
  to:        IRI;               // Target node IRI
  relation:  CausalRelationIRI; // Must be a canonical RO IRI from the type above
  strength?: number;            // Optional prior effect strength ∈ [-1, 1]
};

type FrozenCausalDag = Readonly<{
  nodes: ReadonlyMap<IRI, CausalNode>;
  edges: ReadonlyArray<CausalEdge>;
  adjacency: ReadonlyMap<IRI, ReadonlySet<IRI>>; // Pre-computed for performance
  topologicalOrder: ReadonlyArray<IRI>;           // Pre-computed; verified acyclic
}>;
```

**DAG Validity Contract (enforced in pre-execution phase):**

1. The graph must be a **DAG** — verified by topological sort during `ResourceCollector` execution. If a cycle is detected, execution is aborted with `EpistemicStatus: causal:Invalid_Dag_Cycle`.
2. Every `mechanismRef` in a process node must resolve to either a symbolic parameter vector $\theta_P$ or a reference to the `LatentBridge` neural surrogate (Section 6).
3. All node IRIs must resolve to a class in BFO 2020 or a registered domain subclass.
4. Every `CausalEdge.relation` must be one of the five `CausalRelationIRI` values. A validator must reject any edge carrying a bare string label such as `"generates"` or `"enables"`.

**CausalRelation IRI Reference Table:**

| Semantic intent | RO IRI | RO label | Notes |
|---|---|---|---|
| Symmetric causal link (direction unresolved) | `ro:0002410` | causally related to | Use only when causal direction is genuinely unknown; prefer directed IRIs |
| Source drives downstream outcome | `ro:0002411` | causally upstream of | Primary relation for DAG forward edges |
| Causal effect contained within same process | `ro:0002418` | causally upstream of or within | Use for intra-process modulation (replaces "modulates") |
| Inverse of upstream; effect precedes cause in representation | `ro:0002566` | causally downstream of | Used when encoding reverse-edge perspective; avoid in primary DAG construction |
| Upstream with confirmed positive valence | `ro:0002304` | causally upstream of, positive effect | Use when effect sign is known positive (replaces "enables") |

**Migration note:** The informal string aliases from earlier drafts map as follows: `"generates"` → `ro:0002411`; `"enables"` → `ro:0002304`; `"modulates"` → `ro:0002418`; `"blocks"` has no direct RO equivalent — model as `ro:0002411` with `strength` set to a negative value in $[-1, 0)$.

### 3.5 The Resolver Contract

All resolvers are executed exclusively in the **pre-execution phase**. The execution phase receives only their frozen, validated results. This eliminates all async non-determinism from the pure kernel.

Resolvers must satisfy:

- **Idempotency**: For a given URI and `ExecutionContext.random_seed`, the resolver must return the exact same JSON-LD or Turtle string on every invocation. This is a content-addressed contract, not a caching suggestion.
- **Side-effect freedom**: Resolvers must not mutate any shared ambient state. They operate on their input URI and return a string. They may read from read-only caches.
- **Latency bound**: If a resolver does not return within the configured `timeoutMs`, the `ResourceCollector` records the failure and the corresponding resource slot is set to `null`. The kernel execution proceeds with the degraded bundle, and any output that depended on the missing resource is flagged:

```
EpistemicStatus: causal:Degraded_Offline
causal:missingResource: <uri>
```

### 3.6 Deterministic Numerics Contract

Reproducibility across runtimes is undermined by IEEE 754 floating-point non-associativity and engine-specific optimisations (FMA fusion, SIMD rounding). A kernel that claims bit-identical outputs must make an explicit and enforceable commitment about its floating-point model. This section defines that commitment.

#### 3.6.1 The Problem

JS engines (V8, SpiderMonkey) and WASM runtimes may differ in:
- Intermediate precision (x87 80-bit FP on some platforms)
- Fused multiply-add (FMA) emission, which changes rounding vs separate `mul` + `add`
- SIMD reductions (e.g., pairwise summation ordering)
- Transcendental function (`sin`, `exp`, `log`) implementation accuracy

Any of these can produce different low-order bits in accumulated sums, which will cascade through softmax, normalisation, and other operations in the ONNX inference path. The CSPRNG guarantee (ChaCha20) is unaffected, but the ONNX model's floating-point path is not.

#### 3.6.2 Compliance Levels

The `MathKernelSpec` in `ExecutionContext` must declare one of three compliance levels. These are listed in descending order of reproducibility guarantee strength:

| Level | `mode` value | Guarantee | Tradeoff |
|---|---|---|---|
| **L1 — WASM Deterministic** | `"wasm-deterministic"` | Bit-identical across all compliant engines on all platforms | Requires a WASM runtime that enforces strict IEEE 754 with no FMA and no platform-specific SIMD reductions. Recommended: [wasm-micro-runtime](https://github.com/bytecodealliance/wasm-micro-runtime) with `--disable-simd` or equivalent. Performance impact: ~10–20% vs native FP. |
| **L2 — Softfloat** | `"softfloat"` | Bit-identical on any platform, including heterogeneous edge clusters | Requires a software float library compiled to WASM (e.g., Berkeley SoftFloat). Performance impact: ~3–10× slower than hardware FP. Acceptable for offline or low-frequency inference. |
| **L3 — Engine-Scoped** | `"engine-scoped"` | Bit-identical only within the same JS engine at the same version | The weakest guarantee; acceptable for development and single-engine deployments. The `engineName` and `engineVersion` must be declared and must appear in the output provenance. Auditors must note this limitation. |

#### 3.6.3 Enforcement and ONNX→WASM Compilation Pipeline

**Runtime enforcement:**
- The `ResourceCollector` must verify that the declared `mathKernel.mode` is compatible with the runtime environment before sealing the `ExecutionBundle`. If not, it must abort with a configuration error before any execution begins.
- All ONNX inference in the `LatentBridge` (Section 6) must execute within the declared math kernel context. Implementations must not permit the ONNX runtime to escape the kernel's FP constraints via native backend delegation (e.g., CUDA, OpenBLAS) unless those backends are themselves proven bit-identical under the declared mode.
- All outputs must include the `mathKernelMode` in their provenance record (Section 8). Consumers comparing two `PredictionResult` objects must verify that their `mathKernelMode` values are identical before treating a difference as meaningful.

**ONNX→WASM compilation pipeline (required for L1 compliance):**

The compilation pipeline that converts an ONNX model to a compliant WASM binary must be reproducible and pinned. The reference pipeline is:

```
ONNX model (.onnx)
  → onnx-mlir (version ≥ 0.4.0) with flags:
      --EmitLib --mcpu=generic --disable-fma --no-vector-ops
  → wasm-ld (LLVM ≥ 17) targeting wasm32-unknown-unknown
  → wasm-micro-runtime (WAMR ≥ 2.0.0) with interpreter mode
      (not JIT; JIT may reintroduce platform-specific FP optimizations)
  → signed WASM binary (see §3.7)
```

The `--disable-fma` flag is mandatory. Its absence is the single most common source of cross-platform float divergence. The `--no-vector-ops` flag disables SIMD reductions, which have platform-specific summation orders.

The flags `--mcpu=generic` and interpreter mode (not JIT) together ensure the resulting WASM executes identically across x86-64, ARM64, and RISC-V targets under WAMR.

The exact compiler invocation, including all flags, must be recorded in the repository alongside the `model_hash`. Any change to compiler version or flags produces a new binary and therefore a new `model_hash`.

#### 3.6.4 Recommended Configuration

For production edge deployments: **L1 (wasm-deterministic)** with wasm-micro-runtime interpreter mode. For resource-constrained devices where overhead is prohibitive: **L3 (engine-scoped)** with Node.js version pinned in the deployment manifest and the limitation disclosed in all audit trails.

#### 3.6.5 Reference Test Vectors

The repository must ship a canonical test vector file (`/runtime/deterministic-test-vectors.json`) containing expected SHA-256 hashes of the outputs of the following floating-point operations, computed under L1 compliance with a fixed seed `0xDEADBEEF00000001`. All values are IEEE 754 float32 stored as hex strings.

| Operation | Input specification | Expected output hash |
|---|---|---|
| Vector dot product | `a = [0.1, 0.2, 0.3, ..., 1.0]` (10 elements), `b = [1.0, 0.9, ..., 0.1]` | Computed at build time; recorded in vector file |
| Softmax | Input vector of 100 elements, values from ChaCha20 seed `0xDEADBEEF00000001`, first 100 outputs normalized to [-5, 5] | Computed at build time; recorded in vector file |
| Reduce sum (pairwise) | 1024-element vector, all values = `1.0 / 1024.0` | Must equal `1.0` exactly under L1; any deviation signals FMA or SIMD error |
| exp/log round-trip | $y = \exp(\ln(x))$ for $x \in \{0.001, 0.01, 0.1, 1.0, 10.0, 100.0\}$ | Must satisfy $|y - x| < 2^{-20}$ (single-precision ULP bound) |
| Accumulation (worst case) | Sum of 10000 values alternating $+1$ and $-1/10000$ | Sensitive to summation order; L1 must produce identical result on all platforms |

**Test pass criteria:** A runtime passes L1 certification if and only if SHA-256 of its output for every row in the test vector file matches the expected hash recorded at build time. Test failures must produce a human-readable error naming the failing operation and the observed vs expected hash. These tests must run as part of CI on every commit that modifies the ONNX compilation pipeline or the WASM runtime configuration.

#### 3.6.6 Relationship to CSS Deterministic Arithmetic

The Counterfactual Simulation Service (CSS v2.0 §1.4) specifies decimal128 software arithmetic (34 significant decimal digits, ROUND_HALF_EVEN via `decimal.js`) for all symbolic causal computation — SCM graph evaluation, do-calculus interventions, counterfactual probability, and sensitivity analysis. The Kernel's Deterministic Numerics Contract (this section) governs a different computation scope: the IEEE 754 floating-point path used by ONNX models in the LatentBridge neural-symbolic interface.

These two numerics regimes are **complementary, not conflicting**:

- **Kernel MathKernelSpec** → governs `LatentBridge` encode/decode, surrogate mechanism inference, and all ONNX execution. Compliance level (L1/L2/L3) is declared per `ExecutionContext`.
- **CSS CSSArithmetic** → governs all symbolic computation that consumes or produces causal graph values. Uses decimal128 regardless of the Kernel's declared compliance level.

**Boundary contract:** LatentBridge outputs (IEEE 754 float under declared MathKernelSpec) are converted to CSS `Decimal` via `CSSArithmetic.fromNumber()` at the symbolic/neural boundary. The Kernel is not required to produce decimal128 outputs — it produces IEEE 754 outputs at its declared compliance level, and CSS accepts the inherent precision ceiling of the neural surrogate.

### 3.7 WASM Module Security: Signed Binaries and Sandbox Policy

The kernel loads up to four external WASM binaries: the primary encoder (`modelBytes`), the policy model (`policyModelBytes`), the repair proposer (`repairProposerBytes`), and the surrogate test suite runner (embedded in `surrogateSuiteBytes`). Hash verification (§6.4) proves integrity at load time but says nothing about what a module is permitted to do at runtime or whether it came from a trusted source. This section closes both gaps.

#### 3.7.1 Signing Requirements

Every WASM binary loaded into the kernel must carry a detached Ed25519 signature over its canonical byte content. The signing public key must be declared in the deployment manifest. The `ResourceCollector` must:

1. Verify the Ed25519 signature of each WASM binary against the declared key before adding it to the bundle.
2. Compute SHA-256 of the binary and compare to the corresponding `*_hash` field in `ExecutionContext`.
3. Reject any binary that fails either check with a non-recoverable configuration error, logged with the binary's role name (`"encoder"`, `"policy"`, `"repairProposer"`, `"surrogateSuite"`).

The signing key pair must be managed under a documented key lifecycle policy. Key rotation must produce a new deployment manifest version. A `signer_cert_hash` of `null` in `ExecutionContext` is permitted **only** for development and test environments; any output produced in this mode must include `"signingStatus": "unsigned"` in its provenance and must not be used in production audits.

#### 3.7.2 Sandbox Resource Caps

The `repairProposerBytes` and `policyModelBytes` modules execute as guests within the WASM runtime. Unlike the primary encoder (which has a known, fixed execution profile), learned proposer and policy modules may have unbounded execution times or memory usage if trained carelessly. The following caps are enforced by the WASM runtime host, not by the module itself:

| Module | Max heap allocation | Max instructions per call | Behaviour on exceed |
|---|---|---|---|
| `repairProposerBytes` | 32 MB | 10,000,000 | Call returns empty proposal list; heuristic fallback activates |
| `policyModelBytes` | 64 MB | 50,000,000 | Call returns uniform prior; $\lambda_\pi$ is zeroed for that node |
| `surrogateSuiteBytes` (per test case) | 128 MB | 500,000,000 | Test case marked as `timeout`; counts against SCE numerator |

These caps are not configurable at runtime. They are fixed in this specification to prevent a learned module from exhausting the WASM heap and triggering a false `max_memory_mb` abort in the primary encoder path.

#### 3.7.3 Capability Isolation

Learned WASM modules must be instantiated with the **minimal WASI capability set**: no file system access, no network access, no clock access. The host must not grant any WASI capabilities beyond linear memory read/write and the call stack. This is enforced by passing an empty capability set to the WASM runtime instantiation call.

A module that attempts to invoke a disallowed WASI function must be terminated immediately; its output is treated as if the resource cap was exceeded (empty proposals / uniform prior / test case timeout).

---

## 4. Causal DAG and MCTS Integration

This section resolves the central structural gap in v1.2: the relationship between the Pearl causal calculus (Section 2) and the Monte Carlo Tree Search expansion (Section 4.1). They are not parallel systems. The MCTS traverses the causal DAG in topological order; each MCTS node **is** a causal state node; each edge **is** a causal edge annotated with mechanism type and estimated effect.

### 4.1 Causal State Nodes

Each node $n$ in the MCTS tree corresponds to a **CausalStateNode**:

$$n = \langle \mathcal{S}^{(n)},\, \mathcal{G}^{(n)},\, e^{(n)} \rangle$$

Where:
- $\mathcal{S}^{(n)}$ is the `ContinuantSlice` at the temporal instant represented by node $n$
- $\mathcal{G}^{(n)}$ is the active causal DAG at $n$ (may be a mutilated subgraph under `do`-intervention)
- $e^{(n)}$ is the epistemic status tag accumulated to this node

An edge from $n$ to child $n'$ corresponds to the realization of a specific Process $P$, advancing the temporal instant from $t^{(n)}$ to $t^{(n')}$ and applying the structural equation $f_P$ to produce $\mathcal{S}^{(n')}$.

### 4.2 Guided MCTS Scoring

For node $n$ during UCT (Upper Confidence Bound for Trees) selection, the value function $V(n)$ is extended in v1.5 with a fourth term representing a learned policy prior $\pi_\theta$:

$$V(n) = \underbrace{\hat{Y}(n)}_{\text{causal estimate}} + \underbrace{\lambda_U \cdot \sqrt{\frac{\ln N_{\text{parent}(n)}}{N(n)}}}_{\text{exploration (UCB1)}} + \underbrace{\lambda_R \cdot R_{\mathcal{B}}(n)}_{\text{constraint reward}} + \underbrace{\lambda_\pi \cdot \pi_\theta\!\left(a^{(n)} \mid \mathcal{S}^{(n)}\right)}_{\text{policy prior}}$$

Where:

| Symbol | Meaning |
|---|---|
| $\hat{Y}(n)$ | The rollout-averaged causal estimate of the query variable at node $n$, computed via the SCM structural equations |
| $N(n)$ | Visit count of node $n$ |
| $N_{\text{parent}(n)}$ | Visit count of $n$'s parent |
| $\lambda_U$ | Exploration coefficient; default $\lambda_U = \sqrt{2}$ |
| $\lambda_R$ | Constraint reward coefficient; a hyperparameter ∈ [0, 1] |
| $R_{\mathcal{B}}(n)$ | Binary reward: 1 if $\mathcal{S}^{(n)}$ satisfies all SHACL shapes in $\mathcal{B}$, else 0 |
| $\lambda_\pi$ | Policy prior weight; default $\lambda_\pi = 0$ when `policyModelBytes` is `null` |
| $\pi_\theta\!\left(a^{(n)} \mid \mathcal{S}^{(n)}\right)$ | The probability assigned by the learned policy network to the action $a^{(n)}$ (the specific Process $P$ edge) that led to node $n$, conditioned on the parent state $\mathcal{S}^{(n)}$ |

**Policy network specification:** When `policyModelBytes` is non-null, the policy model is a small ONNX binary that accepts the latent encoding $\mathbf{z}$ of the parent `ContinuantSlice` and returns a probability vector over the outgoing process edges in the causal DAG. The policy model must be hash-verified analogously to the primary `model_hash` check (Section 6.4). Its hash is declared as `context.policy_model_hash`.

**Value network (optional):** A separate value head $V_\theta(\mathcal{S}^{(n)})$ may be included in the same ONNX binary, accessed via a named output. When present, it replaces rollout-based $\hat{Y}(n)$ with a direct value estimate, reducing the number of rollouts required for convergence. If value head output is absent, $\hat{Y}(n)$ defaults to rollout averaging.

**Graceful degradation:** When `policyModelBytes` is `null`, $\lambda_\pi = 0$ is enforced at the type level and the policy term vanishes from $V(n)$, yielding the v1.4 scoring function exactly. No code path should require special-casing; the term's coefficient forces it to zero.

**Policy network training regime:** A policy model whose weights are random or poorly trained will pass hash verification and signature checks while actively degrading search quality. The following data contract and acceptance criteria must be satisfied before a policy model's `policy_model_hash` is admitted to production:

- **Training data**: The policy must be trained on a corpus of at minimum 10,000 MCTS rollouts executed against the same SCM domain, with rollout quality labeled by terminal causal estimate accuracy (measured against held-out test interventions from the Surrogate Causal Validity suite, §2.5).
- **Training objective**: Cross-entropy loss between the policy's predicted action distribution and the empirical visit count distribution $N(n) / N_{\text{parent}(n)}$ from high-quality rollouts (those where the terminal node's $\hat{Y}$ was within 10% of ground truth on held-out test cases).
- **Convergence criterion**: Training is considered converged when the validation cross-entropy loss has not improved by more than $10^{-4}$ over 500 consecutive gradient steps.
- **Production acceptance test**: The trained policy must be evaluated on the synthetic SCM test suite (§2.5). It must achieve a mean reduction in MCTS branches-to-convergence of at least 20% relative to the uniform prior baseline ($\lambda_\pi = 0$). A policy that fails this test must not be shipped; it is better to run without a policy prior than to run with one that misdirects search.
- **Policy model hash binding**: The `policy_model_hash` in `ExecutionContext` must correspond to the specific trained checkpoint that passed the acceptance test. Any retraining, fine-tuning, or architectural change produces a new checkpoint and requires a new acceptance test.

**Integration with do-calculus:** When evaluating a counterfactual query $do(P = p^*)$ at tree depth $d$, the edge in $\mathcal{G}^{(n)}$ corresponding to $P$'s incoming edges is severed at the MCTS node where $P$ is first realized. All child nodes of that node inherit the mutilated DAG $\mathcal{G}^{(n)}_{\overline{P}}$ and use the constant mechanism $P := p^*$ in their structural equations. The UCT scoring function is unchanged; only the mechanism function $f_P$ changes.

### 4.3 Non-Convergent Rollout Halting

The v1.5 halting criterion used variance alone. A single variance threshold is fragile: a bimodal distribution (two tight clusters representing genuinely distinct causal futures) will have high variance while being informative. Halting on it discards a valid bifurcation. v1.6 introduces a **dual criterion**: both variance AND a bimodality test must be evaluated, with the halt record identifying which criterion triggered.

#### 4.3.1 Variance Criterion

If the sample variance of a critical quality $Q^{\text{crit}}$ across $K$ rollouts from node $n$ exceeds the threshold $\varepsilon$:

$$\widehat{\text{Var}}_K\!\left(Q^{\text{crit}}\right) = \frac{1}{K-1} \sum_{k=1}^{K} \left(Q^{\text{crit}}_k - \bar{Q}^{\text{crit}}\right)^2 > \varepsilon$$

the variance criterion is flagged. This alone does not halt expansion; the bimodality criterion is evaluated next.

#### 4.3.2 Bimodality Criterion

The **bimodality coefficient** $b$ is computed from the same $K$ rollout samples using the sample skewness $\hat{S}$ and excess kurtosis $\hat{K}$:

$$b = \frac{\hat{S}^2 + 1}{\hat{K} + \dfrac{3(K-1)^2}{(K-2)(K-3)}}$$

where:
$$\hat{S} = \frac{\frac{1}{K}\sum_k (Q_k - \bar{Q})^3}{\left(\frac{1}{K}\sum_k (Q_k - \bar{Q})^2\right)^{3/2}}, \qquad \hat{K} = \frac{\frac{1}{K}\sum_k (Q_k - \bar{Q})^4}{\left(\frac{1}{K}\sum_k (Q_k - \bar{Q})^2\right)^2} - 3$$

The bimodality coefficient of a uniform distribution is $b = 5/9 \approx 0.555$. A value $b > 0.555$ is a conservative indicator of potential multimodality or heavy bimodality.

The bimodality criterion is flagged when $b \leq 0.555$ — i.e., the distribution is **not** detectably multimodal. If variance is high but bimodality is absent, the branch is genuinely non-convergent and halt is warranted.

**Note:** This is $O(K)$ to compute from the same rollout samples already collected and adds no additional WASM memory cost.

#### 4.3.3 Halt Decision Logic

```
if variance_criterion AND NOT bimodality_criterion:
  // High variance, unimodal distribution: genuinely non-convergent
  HALT branch with nonConvergentReason = "high_variance_unimodal"

if variance_criterion AND bimodality_criterion:
  // High variance, bimodal distribution: may be a genuine causal bifurcation
  // Do NOT halt; continue expansion with reduced rollout budget
  // Surface a warning: causal:Potential_Bifurcation
  FLAG node with EpistemicStatus: causal:Potential_Bifurcation

if NOT variance_criterion:
  // Variance within threshold: expansion proceeds normally
  CONTINUE
```

#### 4.3.4 Halt Record

When the branch halts, the kernel yields:

```
Result: causal:Non_Convergent_Rollout
causal:criticalQuality: <IRI>
causal:observedVariance: <value>
causal:varianceThreshold: <ε>
causal:bimodalityCoefficient: <b>
causal:bimodalityThreshold: 0.555
causal:nonConvergentReason: "high_variance_unimodal" | "high_variance_bimodal_budget_exhausted"
causal:rolloutCount: <K>
EpistemicStatus: causal:Non_Convergent_Rollout
```

The `nonConvergentReason` field is mandatory; it must not be absent from any halt record.

---

## 5. Constraint Projection: Minimum-Edit Discrete Repair (MEDR)

Section 4.3 of v1.2 specified an L₂ projection of latent vector $\mathbf{z}$ onto a constraint manifold $\mathcal{B}$. This formulation was geometrically incorrect: SHACL shapes define discrete class membership and cardinality constraints over an RDF graph, not a smooth differentiable manifold. Gradient-based projection has no well-defined meaning here.

v1.3 replaces this with the **Minimum-Edit Discrete Repair (MEDR)** algorithm.

### 5.1 MEDR: Problem Formulation

Let $G$ be the RDF graph representing the current ContinuantSlice $\mathcal{S}^{(n)}$, and let $\mathcal{B}$ be the SHACL shapes graph. A validation report $\mathcal{V}$ is produced by a conformant SHACL processor:

$$\mathcal{V} = \text{SHACL-Validate}(G, \mathcal{B})$$

$\mathcal{V}$ yields a set of **violation records** $\{v_1, \ldots, v_m\}$, each of the form:

$$v_i = \langle \text{focusNode}_i,\, \text{resultPath}_i,\, \text{constraintComponent}_i,\, \text{message}_i \rangle$$

The repair problem is: find the minimum-cardinality set of **atomic graph edits** $\mathcal{E} = \{e_1, \ldots, e_r\}$ such that:

$$\text{SHACL-Validate}\!\left(\text{Apply}(\mathcal{E}, G),\, \mathcal{B}\right) = \emptyset$$

This is in general NP-hard (equivalent to weighted set cover over edit operations). The kernel uses a **greedy prioritized heuristic** that is sound (always produces a valid repair) but not guaranteed optimal:

### 5.2 MEDR: Repair Operation Taxonomy

The edit algebra supports four atomic operations:

| Operation | Formal definition | Trigger constraint |
|---|---|---|
| `AddTriple(s, p, o)` | $G' = G \cup \{(s, p, o)\}$ | `sh:minCount` violation |
| `RemoveTriple(s, p, o)` | $G' = G \setminus \{(s, p, o)\}$ | `sh:maxCount` violation |
| `AssertType(n, C)` | $G' = G \cup \{(n, \text{rdf:type}, C)\}$ | `sh:class` violation |
| `ReplaceValue(s, p, o_old, o_new)` | $G' = (G \setminus \{(s, p, o_{\text{old}})\}) \cup \{(s, p, o_{\text{new}})\}$ | `sh:datatype` or `sh:pattern` violation |

### 5.3 MEDR: Greedy Algorithm

#### 5.3.1 RepairProposer Abstract API

The `generate_candidates(v)` call in the MEDR loop is seeded by a **RepairProposer**, which may be either a heuristic rule engine (always available) or a learned WASM model (available when `repairProposerBytes` is non-null in the bundle).

```typescript
type RepairProposal = {
  candidateEdit: MEDREdit;      // One of the four atomic operations from §5.2
  confidence:    number;        // ∈ [0, 1]; heuristic proposals use confidence = 0.5
  source:        "learned" | "heuristic";
};

// The proposer is a pure function: same violation + context → same proposals
type RepairProposer = (
  violation:  ViolationRecord,
  graphSlice: ContinuantSlice,
  shapes:     ReadonlyMap<IRI, string>
) => ReadonlyArray<RepairProposal>;
```

When `repairProposerBytes` is non-null, the bundle contains a learned proposer WASM module. The kernel instantiates it once and calls it for each violation. Its outputs are merged with heuristic fallback proposals, sorted by descending confidence, and deduplicated before passing to `argmin` cost selection. This preserves the MEDR cost function as the final arbiter while improving candidate quality.

When `repairProposerBytes` is null, `generate_candidates` falls back to the heuristic-only path, producing candidates solely from the constraint component type (as in v1.4).

#### 5.3.2 Hardened Algorithm

The algorithm accepts both `max_edits` and `max_shacl_calls` scalars. The `max_shacl_calls` budget counts SHACL validation invocations, which are the primary computational cost in the loop. Budgeting in SHACL calls (not wall-clock milliseconds) preserves the execution phase's non-temporal determinism contract.

```
function MEDR(G, V_initial, max_edits, max_shacl_calls, proposer, domainPolicies):
  edits_applied = []
  unresolvable  = []
  V             = V_initial
  shacl_calls   = 1              // count the initial validation that produced V_initial

  while V is not empty:

    // Runaway-bloat guard: hard ceiling on edit count
    if length(edits_applied) >= max_edits:
      unresolvable.extend(V)
      break

    // SHACL complexity budget guard
    if shacl_calls >= max_shacl_calls:
      unresolvable.extend(V)
      break

    v = highest_priority_violation(V)   // prioritize by sh:severity

    // Merge learned + heuristic proposals, sorted by confidence desc
    proposed       = proposer(v, G, shapes)
    heuristic      = heuristic_candidates(v)
    all_candidates = deduplicate(sort_by_confidence_desc(proposed + heuristic))

    // Apply domain policy cost adjustments (§5.5)
    all_candidates = apply_domain_policies(all_candidates, domainPolicies, v.focusNode)

    if all_candidates is empty:
      unresolvable.append(v)
      V = V \ {v}              // skip; do not retry
      continue

    best_edit = argmin_{e ∈ all_candidates} adjusted_cost(e)
    G = Apply(best_edit, G)
    edits_applied.append(best_edit)
    V = SHACL-Validate(G, B)  // re-validate after each edit
    shacl_calls += 1

  if unresolvable is empty:
    return (G, edits_applied, shacl_calls, status=Repaired_Inference)
  else if length(edits_applied) > 0:
    return (G, edits_applied, unresolvable, shacl_calls, status=Partially_Repaired)
  else:
    return (G_original, [], unresolvable, shacl_calls, status=Repair_Failed)
```

**Cost function:** $\text{cost}(e)$ counts the number of existing triples removed by edit $e$. `AddTriple` and `AssertType` have cost 0. `RemoveTriple` has cost 1. `ReplaceValue` has cost 1.

**Budget sizing guidance:**
- `max_edits` default: $3 \times |\mathcal{V}_0|$ where $|\mathcal{V}_0|$ is the initial violation count
- `max_shacl_calls` default: $10 \times |\mathcal{V}_0|$ — allows on average ten validation passes per violation before budget exhaustion, which is sufficient for all known domain shapes

Both values are exposed in `ExecutionContext` (§3.2). `max_shacl_calls` must not be `∞` or unset. The `shacl_calls` counter is included in the `RepairProvenance` record for auditability.

### 5.4 Repair Provenance Record

Every repaired output must carry a complete **RepairProvenance** record. Epistemic consumers downstream must know not just that a repair occurred, but which constraints were violated, what edits resolved them, and what alternatives were considered.

```json
{
  "@type": "causal:RepairProvenance",
  "EpistemicStatus": "causal:Repaired_Inference",
  "violations": [
    {
      "focusNode": "causal:Shipment_XY42",
      "constraintShape": "causal:TransitProcessShape",
      "constraintComponent": "sh:MinCountConstraintComponent",
      "resultPath": "ro:0000057",
      "message": "A transit process cannot occur without a participating material entity.",
      "severity": "sh:Violation"
    }
  ],
  "editsApplied": [
    {
      "operation": "AddTriple",
      "subject": "causal:Shipment_XY42",
      "predicate": "ro:0000057",
      "object": "causal:Vehicle_DefaultCarrier",
      "justification": "Minimum cardinality repair: sh:minCount 1 on ro:0000057",
      "proposerSource": "learned",
      "proposerConfidence": 0.91
    }
  ],
  "repairCost": 0,
  "repairComplete": true,
  "alternateRepairs": [
    {
      "rank": 2,
      "posteriorWeight": 0.23,
      "editsApplied": [
        {
          "operation": "AddTriple",
          "subject": "causal:Shipment_XY42",
          "predicate": "ro:0000057",
          "object": "causal:Vehicle_AuxCarrier",
          "justification": "Alternative minimum cardinality repair",
          "proposerSource": "learned",
          "proposerConfidence": 0.61
        }
      ],
      "repairCost": 0
    }
  ]
}
```

**`alternateRepairs` semantics:** This array contains up to `max_alternate_repairs` alternative repaired graphs (default 3), each representing a distinct valid repair path with lower confidence or higher cost than the primary. The `posteriorWeight` values sum to less than 1.0 (the remainder belongs to the primary repair). Downstream tools may use these alternatives to reason over multiple plausible futures rather than committing to a single canonical repair. When `repairProposerBytes` is null, `alternateRepairs` is always an empty array since heuristic proposals do not produce ranked alternatives.

If `repairComplete` is `false`, the output is additionally flagged `EpistemicStatus: causal:Partially_Repaired` and the unresolvable violations are listed.

### 5.5 MEDR Domain Policy Registry

The base MEDR cost function (Section 5.3) is domain-agnostic. In practice, domain owners have well-founded preferences about which repair operations are appropriate for specific entity classes. A logistics operator may prefer that a missing vehicle participant is always resolved by `AssertType` (asserting an existing entity is a vehicle) rather than `AddTriple` (conjuring a new vehicle entity). A healthcare domain may forbid `RemoveTriple` on any triple involving `bfo:0000040` (material entities representing patients).

The `DomainRepairPolicy` type allows these preferences to be registered as first-class data, injected into the `ExecutionBundle`, and applied during the MEDR `adjusted_cost` computation.

```typescript
type DomainRepairPolicy = {
  "@type":              "causal:DomainRepairPolicy";
  targetClass:          IRI;                // Apply this policy when focusNode is rdf:type this class
  preferredOperation:   MEDROperationType;  // "AddTriple" | "AssertType" | "RemoveTriple" | "ReplaceValue"
  costMultiplier:       number;             // Multiplies base cost for preferredOperation; < 1 makes it cheaper
  forbiddenOperations:  MEDROperationType[]; // Operations that must never be applied to this class
  justification:        string;             // Human-readable rationale; required for audit trails
};
```

**`adjusted_cost` computation:**

For an edit $e$ targeting a focus node of class $C$, let $\mathcal{P}(C)$ be the set of registered domain policies matching $C$ (including superclass matches via RDFS entailment):

$$\text{adjusted\_cost}(e) = \text{base\_cost}(e) \times \prod_{p \in \mathcal{P}(C),\; p.\text{preferredOperation} = e.\text{operation}} p.\text{costMultiplier}$$

If any policy in $\mathcal{P}(C)$ lists $e.\text{operation}$ in `forbiddenOperations`, the edit is removed from the candidate set entirely before `argmin` evaluation. A forbidden edit is never applied regardless of cost.

**Example policy (logistics domain):**

```json
{
  "@type": "causal:DomainRepairPolicy",
  "targetClass": "causal:Vehicle",
  "preferredOperation": "AssertType",
  "costMultiplier": 0.1,
  "forbiddenOperations": ["RemoveTriple"],
  "justification": "Prefer asserting existing entities as vehicles over creating phantom vehicle nodes. Never delete vehicle-related triples during repair as this may mask real data errors."
}
```

Policies are pre-loaded and frozen into `ExecutionBundle.domainRepairPolicies` during the pre-execution phase. They are read-only during the execution phase.

---

## 6. Neural-Symbolic Interface: The LatentBridge

v1.2 included a `model_hash` referencing an ONNX/WASM binary but never specified how the neural model and the symbolic BFO constraint layer communicate. This section defines that interface.

### 6.1 Architectural Role

The `LatentBridge` is the adapter between:
- The **symbolic layer**: structured `ContinuantSlice` objects, BFO-typed IRIs, and SHACL constraints
- The **neural layer**: dense latent vectors $\mathbf{z} \in \mathbb{R}^d$ processed by the ONNX/WASM surrogate model

The `LatentBridge` exposes two operations, dispatching internally on `ExecutionContext.encoderProfile`:

```typescript
type LatentBridge = {
  encode: (slice: ContinuantSlice, profile: EncoderProfile) => Float32Array;
  decode: (z: Float32Array,        profile: EncoderProfile) => ContinuantSlice;
};
```

When `profile = "edge-default"`, the `encode` path follows Section 6.2 (max-pool aggregation, `MAX_ENTITIES` cap). When `profile = "edge-rich"`, the `encode` path follows Section 6.5 (per-entity matrix input with internal GNN/attention aggregation). The `decode` path in Section 6.3 is profile-agnostic; both profiles decode from the same latent space $\mathbb{R}^d$. The dimensionality $d$ is fixed for a given `model_hash` and must be consistent across both profiles when the same ONNX binary serves both — that is, the `edge-rich` encoder must produce a latent vector of the same dimension $d$ as the `edge-default` encoder, enabling use of a single shared decoder.

### 6.2 Encode: Symbolic → Latent

`encode` maps a `ContinuantSlice` to a fixed-dimensional latent vector via a deterministic serialization followed by a learned embedding:

**Step 1 — Canonical serialization:** The `ContinuantSlice` is serialized to a canonical N-Quads string (IRI-sorted, blank-node stable via Skolemization with the `random_seed`).

**Step 2 — Per-entity feature extraction:** For each independent continuant $c_i \in \mathbf{C}_t$, a local feature vector is constructed:

$$\mathbf{x}_i = \phi(c_i) \in \mathbb{R}^{d_{\text{ent}}}$$

where $\phi$ extracts the quality values and disposition states inhering in $c_i$ according to the fixed feature schema registered in `context.jsonld`. The schema defines exactly $d_{\text{ent}}$ feature slots; qualities not present in a given continuant are zero-padded.

**Step 3 — Entity-count aggregation (the variable-size problem):** A `ContinuantSlice` may contain any number of participants across rollouts. A strictly fixed $\mathbb{R}^{d_{\text{in}}}$ input cannot accommodate unbounded entity counts without a defined aggregation policy. The kernel specifies **max-pool aggregation over a capped entity set**:

$$\mathbf{x}_{\text{agg}} = \text{MaxPool}\!\left(\mathbf{x}_1, \mathbf{x}_2, \ldots, \mathbf{x}_{N'}\right) \in \mathbb{R}^{d_{\text{ent}}}$$

where $N' = \min(N,\, \texttt{MAX\_ENTITIES})$ and $N = |\mathbf{C}_t|$.

Max-pooling is applied component-wise: for each feature dimension $j$, $(\mathbf{x}_{\text{agg}})_j = \max_{i \leq N'} (\mathbf{x}_i)_j$.

The constant `MAX_ENTITIES` is a compile-time configuration parameter with a default of **32**. When $N > \texttt{MAX\_ENTITIES}$, entities are ranked by a deterministic priority function $\pi$ (descending quality magnitude, tie-broken by IRI lexicographic order) and the top-$\texttt{MAX\_ENTITIES}$ are retained. The truncation is recorded in the encode provenance:

```
causal:encodeTruncation: {
  totalEntities: <N>,
  retainedEntities: MAX_ENTITIES,
  truncated: true,
  priorityFunction: "quality_magnitude_iri_tiebreak"
}
```

**Step 4 — Embedding:** $\mathbf{z} = E_\theta(\mathbf{x}_{\text{agg}})$ where $E_\theta$ is the encoder network in the ONNX binary identified by `model_hash`. The input dimension of $E_\theta$ is $d_{\text{ent}}$, which must match the feature schema's slot count exactly. A mismatch is a hard error caught during `ResourceCollector` bundle validation.

**Design rationale — why max-pooling over alternatives:**

| Approach | Verdict |
|---|---|
| Padding to fixed length $\texttt{MAX\_ENTITIES} \times d_{\text{ent}}$ | Retains per-entity structure but scales input size as $O(\texttt{MAX\_ENTITIES})$; increases encoder weight count; entity ordering introduces positional bias |
| Mean-pooling | Dilutes dominant entity signals; poor for sparse quality distributions |
| Max-pooling | Preserves the most salient quality value per dimension across all entities; permutation-invariant; fixed output size $d_{\text{ent}}$ regardless of $N'$ |
| Graph neural network (GNN) aggregation | Architecturally correct but requires a GNN layer in the ONNX model, which exceeds the edge-canonical complexity budget for this release |

Max-pooling is therefore the required default. Implementers requiring richer aggregation (e.g., attention-weighted pooling) must register a custom ONNX model that performs the aggregation internally, accepting the raw sorted per-entity matrix as input.

### 6.3 Decode: Latent → Symbolic and SHACL Validation

`decode` maps a latent vector $\mathbf{z}$ back to a candidate `ContinuantSlice`:

1. **Decoding**: $\hat{\mathbf{x}} = D_\theta(\mathbf{z})$ where $D_\theta$ is the decoder network.
2. **Symbolic reconstruction**: $\hat{\mathbf{x}}$ is mapped back to `ContinuantSlice` fields via the inverse of the feature schema.
3. **Validation**: The reconstructed slice is immediately validated against $\mathcal{B}$ via `SHACL-Validate`. If violations exist, MEDR is invoked (Section 5.3).
4. **Return**: The (possibly repaired) `ContinuantSlice` is returned with its `RepairProvenance` attached if repair occurred.

### 6.4 Model Hash Verification

On kernel entry, before any inference, the kernel computes:

$$h = \text{SHA-256}(\text{modelBytes})$$

and asserts $h = \text{context.model\_hash}$. If the assertion fails, execution is aborted with `EpistemicStatus: causal:Model_Hash_Mismatch`. This is not a recoverable error.

### 6.5 Edge-Rich Encoder Profile

The `"edge-rich"` profile addresses the information loss inherent in max-pool aggregation when a `ContinuantSlice` contains many heterogeneous entities. Rather than compressing the entity set to a single $\mathbb{R}^{d_{\text{ent}}}$ vector before the ONNX model sees it, the `edge-rich` encoder passes the **full per-entity feature matrix** into the ONNX model and delegates aggregation to an internal GNN or attention mechanism.

#### 6.5.1 Input Format

The per-entity matrix $\mathbf{X} \in \mathbb{R}^{N \times d_{\text{ent}}}$ is constructed from all $N = |\mathbf{C}_t|$ entities without truncation:

$$\mathbf{X} = \begin{bmatrix} \phi(c_1) \\ \phi(c_2) \\ \vdots \\ \phi(c_N) \end{bmatrix}$$

where $\phi(c_i) \in \mathbb{R}^{d_{\text{ent}}}$ is the per-entity feature extraction from Section 6.2 Step 2. Entities are sorted by the same deterministic priority function $\pi$ used in `edge-default` (descending quality magnitude, IRI tiebreak), establishing a canonical row ordering.

The matrix is passed to the ONNX model as a 2D tensor with shape `[N, d_ent]`. The ONNX model must declare a dynamic first dimension for this input (ONNX `dim_param` = `"N"`). The `edge-rich` ONNX binary is responsible for all internal aggregation.

#### 6.5.2 ONNX Model Requirements for edge-rich

A model serving the `edge-rich` profile must:
1. Accept input shape `[N, d_ent]` with dynamic `N`
2. Produce output latent vector of shape `[d]` — identical dimensionality $d$ to the `edge-default` encoder, ensuring decoder compatibility
3. Implement internally either: (a) multi-head self-attention over entity rows, or (b) a message-passing GNN where entity rows are nodes and DAG adjacency provides edges
4. Be registered under the same `model_hash` as the `edge-default` path if served from a unified binary, or under a separate hash declared as `context.rich_model_hash`

#### 6.5.3 Adjacency Injection

When the `edge-rich` ONNX model implements a GNN, the causal DAG adjacency matrix $\mathbf{A} \in \{0,1\}^{N \times N}$ is passed as a second ONNX input with shape `[N, N]`. It is derived from `FrozenCausalDag.adjacency` restricted to the $N$ entities in $\mathbf{X}$, using the same sort order.

#### 6.5.4 Device Compatibility

`edge-rich` is intended for **server-class and edge+ devices** with sufficient WASM heap to hold $\mathbf{X}$ for realistic $N$. For devices where $N \leq 32$ and memory is constrained, `edge-default` is the required profile. The `ResourceCollector` should warn (but not abort) if `edge-rich` is requested and `max_memory_mb < 256`.

### 6.6 Causal Attribution Layer

When the primary prediction is returned, the kernel optionally computes a **causal attribution** for each predicted quality in $\mathbf{Q}_{t_1}$. Attribution identifies which upstream DAG nodes contributed most to the prediction, providing human-interpretable explanations and a debugging signal for model trust assessment.

#### 6.6.1 CausalAttribution Type

```typescript
type ContributorRecord = {
  sourceNodeIRI:   IRI;               // DAG node (quality or process) that contributed
  edgeRelation:    CausalRelationIRI; // RO IRI of the contributing edge
  absoluteEffect:  number;            // Estimated ΔQ from this contributor; signed
  relativeEffect:  number;            // |absoluteEffect| / Σ|absoluteEffect| across all contributors
  direction:       "positive" | "negative" | "ambiguous";
};

type CausalAttribution = {
  "@type":          "causal:CausalAttribution";
  targetQualityIRI: IRI;                  // The quality being explained
  targetValue:      number;               // The predicted value
  contributors:     ContributorRecord[];  // Sorted by |absoluteEffect| descending
  attributionMethod: "structural" | "gradient" | "shapley";
  coveredVariance:  number;               // Fraction of total variance explained by listed contributors
};
```

#### 6.6.2 Attribution Methods

Three methods are supported, declared in `attributionMethod`. The default method is enforced by query type to prevent accidental expensive Shapley runs during online inference.

**`"structural"` — required default for online inference.** Uses the SCM structural equations directly. For each upstream quality $Q_j$ in the adjustment set for $(P, Q_{t_1})$, the absolute effect is estimated as:

$$\Delta Q_{t_1}^{(j)} = \hat{Q}_{t_1} - \hat{Q}_{t_1}\big|_{Q_j = \mathbb{E}[Q_j]}$$

i.e., the change in prediction when $Q_j$ is replaced by its marginal mean. Computationally $O(|\text{adj set}|)$; available in both `edge-default` and `edge-rich` profiles. When `includeAttribution: true` is set in the query without specifying `attributionMethod`, the kernel must default to `"structural"`. Implementations must not default to Shapley for online use; doing so will exceed WASM heap budgets for large DAGs.

**`"gradient"` — opt-in, edge-rich only.** Computes $\partial \mathbf{z} / \partial \mathbf{x}_i$ via ONNX gradient operators on the encoder. Maps input feature sensitivity back to per-entity quality attributions. Requires the ONNX binary to expose gradient outputs. Only available with `encoderProfile = "edge-rich"`. A query requesting `"gradient"` attribution with `"edge-default"` profile must be rejected with a configuration error during query validation, not silently downgraded.

**`"shapley"` — explicit opt-in only; offline use strongly recommended.** Estimates Shapley values over the set of contributing process nodes via a Monte Carlo approximation over $M$ coalition samples:

$$\hat{\phi}_j = \frac{1}{M} \sum_{m=1}^{M} \left[\hat{Q}_{t_1}(S_m \cup \{j\}) - \hat{Q}_{t_1}(S_m)\right]$$

where $S_m$ is a random coalition of processes excluding $j$. The default value of $M$ is 200 for online use and 2000 for offline analysis; implementers must not increase $M$ beyond 500 in online inference without verifying that the resulting compute time fits within the WASM time budget.

To request Shapley attribution, the query must explicitly set both `"attributionMethod": "shapley"` and `"shapleyBudget": <M>`. A Shapley request without an explicit budget must be rejected. This double-opt-in prevents accidental $O(M \cdot |\mathcal{G}|)$ computation during production inference.

| Method | Requires explicit opt-in | Profile restriction | Complexity | Use case |
|---|---|---|---|---|
| `structural` | No (default) | Both | $O(\|\text{adj}\|)$ | All online inference |
| `gradient` | Yes | `edge-rich` only | $O(d_{\text{ent}})$ | Feature sensitivity analysis |
| `shapley` | Yes + explicit budget | Both | $O(M \cdot \|\mathcal{G}\|)$ | Offline audit and explanation |

#### 6.6.3 Integration with PredictionTree

Each leaf node of the `PredictionTree` may carry an optional `attribution` field:

```typescript
type PredictionTreeNode = {
  causalStateNode:  CausalStateNode;
  value:            number;
  epistemicStatus:  EpistemicStatusIRI;
  children:         PredictionTreeNode[];
  attribution?:     CausalAttribution[];  // One per predicted quality; absent if not requested
};
```

Attribution is computed only when the query includes `"includeAttribution": true`. It is never computed during MCTS expansion (too expensive per node); it is computed once on the final selected leaf after tree search completes.

### 7.1 BFO Version Declaration

All ontology resources in this system conform to **BFO 2020**. Implementations must declare this explicitly in their resource manifest:

```json
{
  "bfoVersion": "2020",
  "bfoBaseIRI": "http://purl.obolibrary.org/obo/BFO_",
  "roVersion": "2023-09-15",
  "roBaseIRI": "http://purl.obolibrary.org/obo/RO_"
}
```

### 7.2 Epistemic Status IRI Registry

All epistemic status values are assigned canonical IRIs under the `causal:` namespace. String literals are not acceptable as epistemic status values; they cannot be reasoned over, versioned, or aligned.

| Status | IRI | Meaning |
|---|---|---|
| Confident | `causal:Confident` | All identification criteria met; result is point-estimated |
| Unidentifiable_Confounding | `causal:Unidentifiable_Confounding` | No valid identification strategy; Rosenbaum bounds returned |
| Degraded_Offline | `causal:Degraded_Offline` | One or more resolvers failed; result computed on partial bundle |
| Repaired_Inference | `causal:Repaired_Inference` | MEDR was applied; RepairProvenance record attached |
| Partially_Repaired | `causal:Partially_Repaired` | MEDR applied; some violations remain unresolvable |
| Repair_Failed | `causal:Repair_Failed` | MEDR `max_edits` limit reached before any violations resolved; output is the original unrepaired graph |
| Non_Convergent_Rollout | `causal:Non_Convergent_Rollout` | Rollout variance exceeded threshold and distribution is unimodal; branch halted |
| Potential_Bifurcation | `causal:Potential_Bifurcation` | High variance with bimodal distribution detected; expansion continues with warning |
| Surrogate_Causal_Mismatch | `causal:Surrogate_Causal_Mismatch` | Surrogate failed causal validity test suite; execution aborted |
| Invalid_Dag_Cycle | `causal:Invalid_Dag_Cycle` | Cycle detected in causal DAG; execution aborted |
| Model_Hash_Mismatch | `causal:Model_Hash_Mismatch` | ONNX/WASM binary does not match declared hash |

### 7.3 Canonical context.jsonld

```json
{
  "@context": {
    "bfo":    "http://purl.obolibrary.org/obo/BFO_",
    "ro":     "http://purl.obolibrary.org/obo/RO_",
    "causal": "https://prediction-engine.local/ontology#",
    "sh":     "http://www.w3.org/ns/shacl#",
    "xsd":    "http://www.w3.org/2001/XMLSchema#",

    "MaterialEntity":       "bfo:0000040",
    "Process":              "bfo:0000015",
    "Disposition":          "bfo:0000016",
    "Quality":              "bfo:0000019",
    "TemporalInstant":      "bfo:0000148",
    "ContinuantSlice":      "causal:ContinuantSlice",

    "has_participant":      "ro:0000057",
    "realizes":             "ro:0000055",
    "bearer_of":            "ro:0000053",
    "inheres_in":           "ro:0000052",
    "participates_in":      "ro:0000056",

    "EpistemicStatus":      "causal:epistemicStatus",
    "RepairProvenance":     "causal:RepairProvenance",
    "atInstant":            { "@id": "causal:atInstant", "@type": "@id" },

    "Confident":                  "causal:Confident",
    "Unidentifiable_Confounding": "causal:Unidentifiable_Confounding",
    "Degraded_Offline":           "causal:Degraded_Offline",
    "Repaired_Inference":         "causal:Repaired_Inference",
    "Partially_Repaired":         "causal:Partially_Repaired",
    "Non_Convergent_Rollout":     "causal:Non_Convergent_Rollout",
    "Potential_Bifurcation":      "causal:Potential_Bifurcation",
    "Surrogate_Causal_Mismatch":  "causal:Surrogate_Causal_Mismatch",
    "Invalid_Dag_Cycle":          "causal:Invalid_Dag_Cycle",
    "Model_Hash_Mismatch":        "causal:Model_Hash_Mismatch",
    "Repair_Failed":              "causal:Repair_Failed",

    "surrogateValidationReport":  "causal:surrogateValidationReport",
    "surrogateErrorRate":         "causal:surrogateErrorRate",
    "nonConvergentReason":        "causal:nonConvergentReason",
    "bimodalityCoefficient":      "causal:bimodalityCoefficient",
    "bimodalityThreshold":        "causal:bimodalityThreshold",
    "shalcCallsUsed":             "causal:shacl_calls_used",
    "signingStatus":              "causal:signingStatus",
    "surrogate_suite_hash":       "causal:surrogateSuiteHash",
    "SurrogateValidationReport":  "causal:SurrogateValidationReport"
    "MathKernelSpec":        "causal:mathKernelSpec",
    "mathKernelMode":        "causal:mathKernelMode",
    "DomainRepairPolicy":    "causal:DomainRepairPolicy",
    "RepairProposal":        "causal:RepairProposal",
    "alternateRepairs":      { "@id": "causal:alternateRepairs", "@container": "@list" },
    "posteriorWeight":       "causal:posteriorWeight",
    "proposerSource":        "causal:proposerSource",
    "proposerConfidence":    "causal:proposerConfidence",
    "CausalAttribution":     "causal:CausalAttribution",
    "ContributorRecord":     "causal:ContributorRecord",
    "targetQualityIRI":      { "@id": "causal:targetQualityIRI", "@type": "@id" },
    "absoluteEffect":        "causal:absoluteEffect",
    "relativeEffect":        "causal:relativeEffect",
    "attributionMethod":     "causal:attributionMethod",
    "coveredVariance":       "causal:coveredVariance",
    "policy_model_hash":     "causal:policyModelHash",
    "rich_model_hash":       "causal:richModelHash"
  }
}
```

### 7.4 SHACL Shapes (shapes.ttl)

The shapes in v1.2 targeted `bfo:0000015` (all Processes) and `bfo:0000040` (all MaterialEntities). This was incorrect: those constraints apply only to domain-specific subclasses `causal:TransitProcess` and `causal:Vehicle`. Targeting BFO base classes would reject any BFO-conformant graph that includes non-transit processes or non-vehicle material entities.

```turtle
@prefix sh:     <http://www.w3.org/ns/shacl#> .
@prefix bfo:    <http://purl.obolibrary.org/obo/BFO_> .
@prefix ro:     <http://purl.obolibrary.org/obo/RO_> .
@prefix causal: <https://prediction-engine.local/ontology#> .
@prefix rdfs:   <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl:    <http://www.w3.org/2002/07/owl#> .

# --- Domain Subclass Declarations ---
# causal:TransitProcess is a subclass of bfo:Process.
# Targeting this shape at bfo:Process would constrain ALL processes.
# Only causal:TransitProcess requires a vehicle participant.
causal:TransitProcess
    a owl:Class ;
    rdfs:subClassOf bfo:0000015 ;
    rdfs:label "Transit Process" .

# causal:Vehicle is a subclass of bfo:MaterialEntity.
# Targeting VehicleShape at bfo:MaterialEntity would require ALL
# material entities to bear a disposition — ontologically absurd.
causal:Vehicle
    a owl:Class ;
    rdfs:subClassOf bfo:0000040 ;
    rdfs:label "Vehicle" .

causal:LoadCapacityDisposition
    a owl:Class ;
    rdfs:subClassOf bfo:0000016 ;
    rdfs:label "Load Capacity Disposition" .

causal:MotilityDisposition
    a owl:Class ;
    rdfs:subClassOf bfo:0000016 ;
    rdfs:label "Motility Disposition" .


# --- Shape 1: TransitProcess ---
# A TransitProcess must have at least one participating Vehicle
# and must realize at least one MotilityDisposition.
# Scope: causal:TransitProcess only — NOT all BFO Processes.

causal:TransitProcessShape
    a sh:NodeShape ;
    sh:targetClass causal:TransitProcess ;
    sh:severity sh:Violation ;

    sh:property [
        sh:path ro:0000057 ;              # has_participant
        sh:minCount 1 ;
        sh:class causal:Vehicle ;
        sh:name "vehicle-participant" ;
        sh:message "A TransitProcess must have at least one participating Vehicle." ;
    ] ;

    sh:property [
        sh:path ro:0000055 ;              # realizes
        sh:minCount 1 ;
        sh:class causal:MotilityDisposition ;
        sh:name "motility-realization" ;
        sh:message "A TransitProcess must realize at least one MotilityDisposition." ;
    ] .


# --- Shape 2: Vehicle ---
# A Vehicle must bear at least one LoadCapacityDisposition.
# Scope: causal:Vehicle only — NOT all BFO MaterialEntities.

causal:VehicleShape
    a sh:NodeShape ;
    sh:targetClass causal:Vehicle ;
    sh:severity sh:Violation ;

    sh:property [
        sh:path ro:0000053 ;              # bearer_of
        sh:minCount 1 ;
        sh:class causal:LoadCapacityDisposition ;
        sh:name "load-capacity" ;
        sh:message "A Vehicle must bear at least one LoadCapacityDisposition." ;
    ] .


# --- Shape 3: ContinuantSlice integrity ---
# Every ContinuantSlice must reference a temporal instant.

causal:ContinuantSliceShape
    a sh:NodeShape ;
    sh:targetClass causal:ContinuantSlice ;
    sh:severity sh:Violation ;

    sh:property [
        sh:path causal:atInstant ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:class bfo:0000148 ;            # TemporalInstant
        sh:name "temporal-anchor" ;
        sh:message "A ContinuantSlice must be anchored to exactly one TemporalInstant." ;
    ] .
```

---

## 8. Output Contract

Every output from the kernel, whether a full prediction or a halted branch, must conform to the following structure:

```json
{
  "@context": "<IRI of context.jsonld>",
  "@type": "causal:PredictionResult",
  "query": { ... },
  "horizon": 12,
  "random_seed": "0xA1B2C3...",
  "model_hash": "sha256:...",
  "encoderProfile": "edge-default",
  "mathKernelMode": "wasm-deterministic",
  "signingStatus": "signed",
  "surrogateValidation": {
    "passed": true,
    "surrogateErrorRate": 0.04,
    "testCasesRun": 40,
    "threshold": 0.10
  },
  "epistemicStatus": "causal:Confident",
  "result": {
    "predictedSlice": { ... },
    "probabilityEstimate": 0.73,
    "confidenceInterval": [0.61, 0.84]
  },
  "repairProvenance": null,
  "sensitivityAnalysis": null,
  "haltReason": null,
  "causalAttribution": null,
  "branchesExplored": 847,
  "wallClockMs": 312
}
```

All fields are required unless marked optional. `signingStatus` must be `"signed"` in production; `"unsigned"` is permitted only in development and must never appear in audit trails. `surrogateValidation` is always present and non-null; a result produced without running the validation suite must have `"passed": false` and `"surrogateErrorRate": null`. `encoderProfile` and `mathKernelMode` are always present and non-null.

All non-null values in `epistemicStatus` must be IRIs from the registry in Section 7.2. `repairProvenance.alternateRepairs` is an array (possibly empty) when `repairProvenance` is non-null.

---

## Appendix A: Constraint between Sections (Traceability Matrix)

### Issues resolved in v1.2 → v1.3

| Gap identified in v1.2 critique | Resolved in |
|---|---|
| Equations missing | §2.2, §2.3, §2.4, §4.2, §4.3 |
| SHACL targets BFO base classes | §7.4 |
| L₂ projection onto discrete constraint space | §5 (MEDR replaces it entirely) |
| MCTS and do-calculus unintegrated | §4.1, §4.2 |
| Causal DAG unspecified | §3.4 |
| `BfoTemporalRegion` as snapshot is a BFO type error | §3.3 |
| Async resolver undermines determinism | §3.1 |
| "Computational Irreducibility" term misused | §4.3 |
| Epistemic status values lack IRIs | §7.2, §7.3 |
| BFO version unspecified | §1, §7.1 |
| Repair outputs lack provenance | §5.4 |
| `model_hash` integration unexplained | §6 |

### Issues resolved in v1.3 → v1.4

| Gap identified in v1.3 review | Resolved in |
|---|---|
| `CausalEdge.relation` uses informal string literals; not machine-readable or RO-aligned | §3.4 (`CausalRelationIRI` type, RO IRI table, migration note) |
| MEDR greedy loop unbounded; zero-cost `AddTriple` can cause infinite graph bloat on unsatisfiable constraints | §5.3 (`max_edits` guard, three-way return status, sizing guidance) |
| `LatentBridge` encode assumes fixed entity count; variable-size `ContinuantSlice` causes silent truncation or dimension mismatch | §6.2 (per-entity $\phi$ extraction, max-pool aggregation, `MAX_ENTITIES` cap, truncation provenance, design rationale table) |
| `causal:Repair_Failed` status needed for total MEDR failure (distinct from partial repair) | §5.3, §7.2, §7.3 |

### Issues resolved in v1.4 → v1.5

| Gap identified in v1.4 SME review | Resolved in |
|---|---|
| IEEE 754 FP non-determinism across JS engines and WASM runtimes undermines reproducibility guarantee | §1 (deterministic numerics baseline declared), §3.6 (Deterministic Numerics Contract: three compliance levels, enforcement rules, recommended configuration) |
| `ExecutionContext` has no mechanism to declare encoder profile, math kernel, repair proposer, or edit ceiling | §3.2 (`encoderProfile`, `mathKernel`, `repairProposerRef`, `max_edits` added to `ExecutionContext`; `ExecutionBundle` extended with `repairProposerBytes`, `policyModelBytes`, `domainRepairPolicies`) |
| MCTS expansion has no learned prior; all branches treated equally regardless of historical quality | §4.2 (policy/value prior term $\lambda_\pi \cdot \pi_\theta$ added to $V(n)$; policy network spec, value head, graceful $\lambda_\pi = 0$ degradation) |
| MEDR `generate_candidates` is heuristic-only; no learned repair proposals; no way to plug in domain knowledge | §5.3 (`RepairProposer` abstract API, learned/heuristic merge, confidence-sorted candidate list) |
| Greedy MEDR selects a single repair; no ranked alternatives for downstream uncertainty reasoning | §5.4 (`alternateRepairs` array in `RepairProvenance`, `posteriorWeight`, `proposerSource`, `proposerConfidence` provenance fields) |
| MEDR cost function is domain-agnostic; cannot express domain-specific repair preferences or prohibitions | §5.5 (MEDR Domain Policy Registry: `DomainRepairPolicy` type, `adjusted_cost` formula, `forbiddenOperations`, example) |
| `edge-default` max-pool aggregation loses per-entity structure in multi-entity domains | §6.5 (`edge-rich` encoder profile: per-entity matrix $\mathbf{X}$, ONNX dynamic shape, GNN/attention delegation, adjacency injection, device compatibility guidance) |
| No mechanism to explain which upstream variables drove a prediction | §6.6 (Causal Attribution layer: `CausalAttribution` type, `ContributorRecord`, three attribution methods — structural/gradient/Shapley — `PredictionTreeNode.attribution` integration) |
| Output contract missing `encoderProfile`, `mathKernelMode`, `causalAttribution`, `alternateRepairs` | §8 (output schema updated; auditor comparison requirements stated) |

### Issues resolved in v1.5 → v1.6

| Gap identified in v1.5 review | Priority | Resolved in |
|---|---|---|
| Neural surrogates may learn observational $P(Y\|X)$ rather than interventional $P(Y\|do(X))$; no mechanism to detect or reject biased surrogates | Must | §2.5 (Surrogate Causal Validity Contract: synthetic SCM suite, MMD metric, 10% SCE threshold, `causal:Surrogate_Causal_Mismatch` status, pre-execution validation lifecycle) |
| §3.6 compliance levels are defined but ONNX→WASM pipeline is unspecified; L1 claim is unfalsifiable without a reference build | Must | §3.6.3 (onnx-mlir pipeline, `--disable-fma`, `--no-vector-ops`, WAMR interpreter mode, compiler flag recording requirement) |
| No reference test vectors; bit-identical claims cannot be verified by CI | Must | §3.6.5 (five test vector categories, SHA-256 expected hashes, ULP bound for transcendentals, CI integration requirement) |
| Single variance threshold halts on genuinely bifurcated causal distributions, discarding valid futures | Must | §4.3 (dual criterion: variance + bimodality coefficient $b$; `nonConvergentReason` field; `causal:Potential_Bifurcation` for bimodal high-variance branches) |
| Learned WASM modules (proposer, policy) have no integrity provenance beyond hash; no runtime sandbox prevents heap exhaustion | Should | §3.7 (Ed25519 signing, cert chain verification, per-module heap/instruction caps, WASI capability isolation) |
| Policy network training regime unspecified; a random-weight policy passes hash/signature checks while degrading search | Should | §4.2 (data contract, training objective, convergence criterion, 20% branch reduction acceptance test, policy_model_hash binding) |
| MEDR SHACL loop cost budgeted in wall-ms, which reintroduces timing non-determinism | Should | §5.3.2 (`max_shacl_calls` counter; budget in SHACL calls not milliseconds; `shacl_calls_used` in RepairProvenance) |
| Attribution defaults unspecified; a query with `includeAttribution: true` could accidentally trigger $O(M \cdot \|\mathcal{G}\|)$ Shapley on online hardware | Should | §6.6.2 (`"structural"` required default; gradient requires opt-in; Shapley requires double opt-in with explicit `shapleyBudget`; gradient restricted to `edge-rich`) |
| Output contract missing `surrogateValidation` and `signingStatus` fields | Should | §8 (both fields added, required semantics stated) |
