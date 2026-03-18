# Counterfactual Simulation Service (CSS) Specification

**Document ID:** `css-core-01`
**Version:** 2.0.0
**Status:** Final
**Last Updated:** 2025-02-03

---

## Executive Summary

The Counterfactual Simulation Service (CSS) is the FNSR ecosystem's capacity for disciplined imagination. It answers "what if?" questions by forking the known world into isolated hypothetical sandboxes, applying causal interventions, and tracing consequences—all without contaminating verified knowledge.

CSS operates under a fundamental architectural constraint: **hypothetical reasoning must never masquerade as fact**. Every simulation output carries L4 (Hypothetical) taint that cannot be removed, stripped, or downgraded. This is not a policy decision but a structural impossibility enforced by the representation format itself.

This specification defines CSS as a pure computational function that transforms intervention requests into consequence traces. It requires no infrastructure, runs in any JavaScript environment, and produces deterministic results from identical inputs.

### Changes in v2.0.0

- Added cross-platform determinism requirements and CI matrix (§1.4.6)
- Defined formal seed derivation policy using HKDF (§1.4.7)
- Made abduction fallbacks normative with quality metrics (§4.3.4)
- Added global sensitivity methods (Sobol, Morris) and adjoint mode (§3.3.3)
- Added taint enforcement specification for adapters (§5.5)
- Added streaming/partial result event semantics (§6.1.3)
- Added security and privacy section with redaction policies (§10)
- Defined numeric constants (MAX_ENUMERATION_SIZE, etc.) (§4.3.3)
- Added variable normalization for equilibrium detection (§4.5.5)
- Editorial: aligned filename references to CSS

### Changes in v1.2.0

- Added sensitivity analysis resource limits (§8.1.1)
- Defined formal equilibrium detection metric (§4.5.4)
- Added trajectory compression (§3.3.2)

### Changes in v1.1.0

- Added deterministic arithmetic specification (§1.4)
- Clarified decision horizon and taint propagation (§5.4)
- Added temporal causal models with feedback loops (§4.5)
- Added abduction tractability constraints (§4.3.3)
- Added sensitivity analysis (§3.3.1)

---

## 1. Foundational Principles

### 1.1 The Imagination Constraint

CSS embodies a careful distinction: the difference between *what is* and *what might be*. Human cognition blurs this boundary constantly—we imagine, confuse our imaginings with memory, and act on counterfactual reasoning as if it were established fact. CSS exists precisely to prevent this confusion in artificial reasoning systems.

The architectural guarantee is simple: **L4 outputs cannot become L1-L3 inputs**. A simulation result can inform decisions, but it cannot retroactively become evidence. The taint is indelible.

### 1.2 Edge-Canonical Execution

CSS must execute identically whether running:
- In a browser tab
- Via `node index.js`
- As part of a larger orchestrated system

The specification describes computation, not deployment. All infrastructure concerns (persistence, distribution, scheduling) are adapter responsibilities, not core requirements.

### 1.3 Determinism

Given:
- The same world state (as JSON-LD)
- The same intervention specification
- The same simulation parameters

CSS **must** produce the same result. Non-determinism would make counterfactual reasoning meaningless—we could not compare scenarios or reproduce analyses.

### 1.4 Deterministic Arithmetic Specification

**Problem**: JavaScript's native `number` type (IEEE 754 double-precision) can produce subtly different results across browser engines (V8, SpiderMonkey, JavaScriptCore) and CPU architectures (x86, ARM) due to differences in optimization levels, extended precision registers, and fused multiply-add operations.

**Requirement**: CSS implementations MUST use deterministic arithmetic that produces bit-identical results across all conforming JavaScript environments.

**Performance Trade-off**: Decimal arithmetic is 10-100x slower than native floating-point. This is an acceptable trade-off for a reasoning engine where **correctness and reproducibility take precedence over raw speed**. For exploratory use cases, see §1.4.8 on execution modes.

#### 1.4.1 Canonical Arithmetic Library

CSS defines a canonical arithmetic interface that all implementations must use:

```typescript
/**
 * Deterministic decimal arithmetic for CSS.
 * 
 * All numerical computations in simulation MUST use this interface,
 * NOT native JavaScript number operations.
 */
interface CSSArithmetic {
  /**
   * Precision: 34 significant decimal digits (IEEE 754-2008 decimal128)
   * Rounding: ROUND_HALF_EVEN (banker's rounding)
   * These parameters are FIXED and not configurable.
   */
  readonly PRECISION: 34;
  readonly ROUNDING: 'ROUND_HALF_EVEN';
  
  // Construction
  fromNumber(n: number): Decimal;
  fromString(s: string): Decimal;
  fromFraction(numerator: bigint, denominator: bigint): Decimal;
  
  // Basic operations
  add(a: Decimal, b: Decimal): Decimal;
  subtract(a: Decimal, b: Decimal): Decimal;
  multiply(a: Decimal, b: Decimal): Decimal;
  divide(a: Decimal, b: Decimal): Decimal;
  abs(a: Decimal): Decimal;
  
  // Advanced operations
  pow(base: Decimal, exponent: Decimal): Decimal;
  sqrt(a: Decimal): Decimal;
  ln(a: Decimal): Decimal;
  exp(a: Decimal): Decimal;
  
  // Comparison
  compare(a: Decimal, b: Decimal): -1 | 0 | 1;
  
  // Conversion
  toNumber(d: Decimal): number;  // Lossy, for display only
  toString(d: Decimal): string;  // Lossless canonical form
}
```

#### 1.4.2 Reference Implementation

```typescript
// css-arithmetic.ts - Reference Implementation

import Decimal from 'decimal.js';

// MANDATORY configuration - do not modify
Decimal.set({
  precision: 34,
  rounding: Decimal.ROUND_HALF_EVEN,
  toExpNeg: -9e15,
  toExpPos: 9e15,
  maxE: 9e15,
  minE: -9e15,
  crypto: false  // Deterministic, NOT cryptographically secure
});

export const CSSMath: CSSArithmetic = {
  PRECISION: 34,
  ROUNDING: 'ROUND_HALF_EVEN',
  
  fromNumber: (n) => new Decimal(n),
  fromString: (s) => new Decimal(s),
  fromFraction: (num, den) => new Decimal(num.toString()).div(den.toString()),
  
  add: (a, b) => a.plus(b),
  subtract: (a, b) => a.minus(b),
  multiply: (a, b) => a.times(b),
  divide: (a, b) => a.div(b),
  abs: (a) => a.abs(),
  
  pow: (base, exp) => base.pow(exp),
  sqrt: (a) => a.sqrt(),
  ln: (a) => a.ln(),
  exp: (a) => a.exp(),
  
  compare: (a, b) => a.comparedTo(b) as -1 | 0 | 1,
  
  toNumber: (d) => d.toNumber(),
  toString: (d) => d.toFixed()
};

Object.freeze(CSSMath);
```

#### 1.4.3 Deterministic Random Number Generation

For probabilistic simulations, CSS requires a seeded PRNG. The PRNG is for **reproducibility only** and MUST NOT be used where cryptographic randomness is required.

```typescript
/**
 * Deterministic PRNG for Monte Carlo simulation.
 * Uses xoshiro256** algorithm.
 * 
 * WARNING: This is NOT cryptographically secure. Do not use for
 * key generation, nonces, or any security-sensitive purpose.
 */
interface CSSPRNG {
  fromSeed(seed: Uint8Array): PRNGState;
  next(state: PRNGState): [Decimal, PRNGState];
  normalSample(state: PRNGState): [Decimal, PRNGState];
  sampleDistribution(state: PRNGState, dist: Distribution): [Decimal, PRNGState];
}
```

#### 1.4.4 Serialization Determinism

All intermediate values MUST be serialized using canonical string form:

```json
{
  "value": {
    "@type": "css:DecimalValue",
    "css:canonicalForm": "3.141592653589793238462643383279503",
    "css:displayForm": "3.14159"
  }
}
```

#### 1.4.5 Conformance Testing

CSS implementations MUST pass the determinism test suite:

```typescript
describe('Arithmetic Determinism', () => {
  const testCases = loadCanonicalTestVectors('css-arithmetic-vectors.json');
  
  for (const tc of testCases) {
    it(`${tc.operation}: ${tc.description}`, () => {
      const result = CSSMath[tc.operation](...tc.inputs.map(CSSMath.fromString));
      expect(CSSMath.toString(result)).toBe(tc.expectedOutput);
    });
  }
});
```

#### 1.4.6 Cross-Platform Determinism Requirements

**Normative Requirement**: CSS implementations MUST produce bit-identical outputs across all supported platforms. This is verified through mandatory CI testing.

**Runtime Matrix**: The following platforms MUST produce identical results for all test vectors:

| Engine | Versions | Architectures |
|--------|----------|---------------|
| V8 (Node.js) | 18.x, 20.x, 22.x | x86_64, ARM64 |
| V8 (Chrome) | Latest stable | x86_64, ARM64 |
| SpiderMonkey (Firefox) | Latest stable | x86_64, ARM64 |
| JavaScriptCore (Safari) | Latest stable | ARM64 |

**CI Configuration** (GitHub Actions reference):

```yaml
# .github/workflows/determinism.yml
name: Cross-Platform Determinism

on: [push, pull_request]

jobs:
  node-determinism:
    strategy:
      matrix:
        node: [18, 20, 22]
        os: [ubuntu-latest, macos-latest, windows-latest]
        include:
          - os: ubuntu-latest
            arch: x64
          - os: macos-latest
            arch: arm64
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
      - run: npm ci
      - run: npm run test:arithmetic-vectors
      - name: Compare golden outputs
        run: |
          npm run generate:golden-trace -- --output trace-${{ matrix.os }}-${{ matrix.node }}.json
          diff trace-${{ matrix.os }}-${{ matrix.node }}.json golden/canonical-trace.json

  browser-determinism:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npx playwright install
      - name: Run vectors in Chrome
        run: npx playwright test --project=chromium tests/arithmetic-vectors.spec.ts
      - name: Run vectors in Firefox
        run: npx playwright test --project=firefox tests/arithmetic-vectors.spec.ts
      - name: Run vectors in WebKit
        run: npx playwright test --project=webkit tests/arithmetic-vectors.spec.ts
      - name: Verify cross-browser consistency
        run: npm run verify:browser-determinism
```

**Golden Trace Artifacts**: The repository MUST maintain golden trace files that serve as the canonical reference. Any divergence from golden traces fails the build.

**WASM Bindings**: For performance-critical deployments, implementations MAY use WASM-compiled decimal libraries (e.g., `rust_decimal` compiled to WASM) provided they pass the same conformance suite with bit-identical outputs.

#### 1.4.7 Seed Derivation Policy

**Problem**: When multiple components compose sources of randomness, naive seeding can cause correlation between supposedly independent random streams.

**Normative Requirement**: PRNG seeds MUST be derived using HKDF to ensure independence across components while maintaining reproducibility.

```typescript
/**
 * Derive a deterministic, independent seed for a specific component/step.
 * 
 * Uses HKDF-SHA256 to derive seeds that are:
 * - Deterministic: same inputs = same seed
 * - Independent: different components get uncorrelated streams
 * - Reproducible: can recreate exact sequence from requestId
 */
async function deriveSeed(
  requestId: string,
  namespace: string,
  componentId: string
): Promise<Uint8Array> {
  const encoder = new TextEncoder();
  
  // Import request ID as key material
  const keyMaterial = await crypto.subtle.importKey(
    'raw',
    encoder.encode(requestId),
    'HKDF',
    false,
    ['deriveBits']
  );
  
  // Salt includes service namespace for domain separation
  const salt = encoder.encode(`css:${namespace}`);
  
  // Info includes component identifier
  const info = encoder.encode(componentId);
  
  // Derive 32 bytes (256 bits) for xoshiro256** state
  const derivedBits = await crypto.subtle.deriveBits(
    {
      name: 'HKDF',
      hash: 'SHA-256',
      salt: salt,
      info: info
    },
    keyMaterial,
    256
  );
  
  return new Uint8Array(derivedBits);
}

// Usage examples:
// Main simulation PRNG
const mainSeed = await deriveSeed(requestId, 'simulation', 'main');

// Monte Carlo sampling (each sample gets independent stream)
const sampleSeed = await deriveSeed(requestId, 'montecarlo', `sample-${i}`);

// Sensitivity perturbation
const sensitivitySeed = await deriveSeed(requestId, 'sensitivity', `var-${variableId}`);
```

**Seed Derivation Requirements**:

1. The `requestId` MUST be the root entropy source
2. Each component MUST use a unique `(namespace, componentId)` pair
3. Implementations MUST NOT reuse seeds across components
4. The derivation algorithm MUST be HKDF-SHA256 as specified

**Conformance Test**:

```typescript
describe('Seed Derivation', () => {
  it('produces identical seeds for identical inputs', async () => {
    const seed1 = await deriveSeed('req-123', 'simulation', 'main');
    const seed2 = await deriveSeed('req-123', 'simulation', 'main');
    expect(seed1).toEqual(seed2);
  });
  
  it('produces different seeds for different components', async () => {
    const seed1 = await deriveSeed('req-123', 'simulation', 'main');
    const seed2 = await deriveSeed('req-123', 'montecarlo', 'sample-0');
    expect(seed1).not.toEqual(seed2);
  });
  
  it('matches canonical test vectors', async () => {
    const seed = await deriveSeed('test-request-id', 'simulation', 'main');
    expect(Buffer.from(seed).toString('hex')).toBe(CANONICAL_SEED_HEX);
  });
});
```

#### 1.4.8 Execution Modes

CSS supports two execution modes to balance correctness with exploration speed:

| Mode | Arithmetic | PRNG | Use Case | Output Label |
|------|------------|------|----------|--------------|
| **Exact** | Decimal128 | Seeded xoshiro256** | Audits, canonical runs, production | `L4` |
| **Fast** | IEEE 754 double | Seeded xoshiro256** | Exploration, prototyping | `L4-fast` |

**Fast Mode Constraints**:

1. Fast mode outputs MUST be labeled `L4-fast` (not `L4`)
2. Fast mode outputs MUST include a warning in diagnostics
3. Fast mode outputs MUST NOT be used for:
   - Audit trails
   - Regulatory compliance
   - Cross-platform comparison
   - Reproducibility claims
4. Fast mode is OPT-IN only via explicit request flag

```json
{
  "requestMetadata": {
    "executionMode": "fast",
    "fastModeAcknowledgment": true
  }
}
```

**Fast Mode Output Warning**:

```json
{
  "taint:level": "L4-fast",
  "diagnostics": {
    "executionMode": "fast",
    "fastModeWarning": "Results computed using IEEE 754 arithmetic. Not suitable for audits, cross-platform comparison, or reproducibility claims. Re-run in exact mode for canonical results."
  }
}
```

---

#### 1.4.9 Relationship to Causal OS Kernel Deterministic Numerics Contract

The Causal OS Kernel (v1.6 §3.6) defines a three-level Deterministic Numerics Contract (`wasm-deterministic` / `softfloat` / `engine-scoped`) governing floating-point reproducibility in the ONNX inference path (LatentBridge neural-symbolic interface). CSS's decimal128 arithmetic (this section) and the Kernel's MathKernelSpec govern **different computation scopes** within the same execution pipeline:

| Scope | Arithmetic | Governed By | Purpose |
|---|---|---|---|
| **Symbolic causal computation** — SCM graph evaluation, do-calculus interventions, counterfactual probability, sensitivity analysis, equilibrium detection | Decimal128 (34 digits, ROUND_HALF_EVEN) via `CSSArithmetic` | CSS §1.4 (this section) | Exact reproducibility of causal reasoning across all platforms |
| **Neural inference** — ONNX model execution in LatentBridge encode/decode, surrogate causal mechanism evaluation | IEEE 754 float32/float64 under declared `MathKernelSpec` compliance level | Kernel §3.6 | Bit-identical neural inference within declared compliance level |

**Boundary rule:** When LatentBridge inference results (Kernel-governed, IEEE 754) feed back into CSS symbolic computation, they MUST be converted to `Decimal` at the boundary via `CSSArithmetic.fromNumber()`. The conversion is lossy (IEEE 754 double has ~15.9 significant digits vs decimal128's 34), but this is acceptable because the neural surrogate's precision is inherently limited by model training — the decimal128 representation preserves the surrogate's output exactly as received, preventing further precision loss in downstream symbolic operations.

**Fast mode exception:** When CSS operates in Fast mode (§1.4.8, `L4-fast`), symbolic computation uses IEEE 754 double, which aligns naturally with the Kernel's L1/L3 precision. The boundary conversion is a no-op in this mode. Fast mode outputs remain unsuitable for audits regardless.

---

## 2. Conceptual Model

### 2.1 Worlds, Interventions, and Traces

CSS operates on three fundamental concepts:

**World State**: A JSON-LD knowledge graph representing everything known at simulation time. This includes entities, relationships, temporal facts, and uncertainty markers. The world state is immutable—CSS never modifies it.

**Intervention**: A formal specification of what to change in the hypothetical world. Interventions are expressed using Pearl's do-calculus notation: `do(X = x)` means "set variable X to value x, regardless of its natural causes."

**Consequence Trace**: The simulation output—a structured record of what follows from the intervention.

### 2.2 Causal Models

CSS requires explicit causal structure to reason about interventions. This structure comes from:

1. **Ontological Causation**: Relations in the knowledge graph that carry causal semantics
2. **Declared Causal Models**: Explicit DAGs or temporal models submitted with requests

### 2.3 Simulation as Graph Traversal

1. **Fork**: Create an isolated copy of relevant world state subgraph
2. **Intervene**: Apply `do(X = x)` via graph surgery
3. **Propagate**: Traverse outgoing causal edges, computing new values
4. **Bound**: Stop when reaching thresholds or limits
5. **Analyze**: Compute sensitivity of results to perturbations
6. **Collect**: Gather all changes into the consequence trace

---

## 3. Data Structures

### 3.1 Simulation Request

```json
{
  "@context": {
    "@vocab": "https://fnsr.dev/css/",
    "fnsr": "https://fnsr.dev/ontology/",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
  },
  "@type": "SimulationRequest",
  "@id": "urn:uuid:simulation-request-id",
  
  "requestMetadata": {
    "requestId": "string (UUID)",
    "requestedAt": "xsd:dateTime",
    "requestedBy": "IRI of requesting service/agent",
    "correlationId": "string",
    "priority": "low | normal | high | critical",
    "timeoutMs": "integer",
    "maxSteps": "integer",
    "randomSeed": "string (optional, defaults to requestId)",
    "executionMode": "exact | fast (default: exact)"
  },
  
  "worldState": {
    "@type": "WorldStateReference",
    "method": "inline | reference | snapshot",
    "content": "JSON-LD graph (if inline)",
    "reference": "IRI (if reference)",
    "snapshotId": "string (if snapshot)",
    "asOf": "xsd:dateTime"
  },
  
  "causalModel": {
    "@type": "CausalModelReference",
    "method": "inline | reference | derive",
    "content": "CausalModel (if inline)",
    "reference": "IRI (if reference)",
    "derivationScope": "IRI[] (if derive)",
    "modelType": "static | temporal"
  },
  
  "interventions": [
    {
      "@type": "Intervention",
      "target": "IRI",
      "operator": "do | observe | counterfactual",
      "value": "new value",
      "priorValue": "original value (for counterfactual)",
      "rationale": "string",
      "temporalIndex": "integer (for temporal models)"
    }
  ],
  
  "queries": [
    {
      "@type": "SimulationQuery",
      "queryId": "string",
      "target": "IRI",
      "queryType": "value | probability | distribution | path | sensitivity | trajectory",
      "conditions": "optional conditioning",
      "temporalRange": "[startStep, endStep]",
      "trajectoryOptions": {
        "downsampleFactor": "integer (default 1)",
        "compression": "none | delta | sparse"
      }
    }
  ],
  
  "sensitivityAnalysis": {
    "enabled": "boolean (default: false)",
    "method": "one-at-a-time | sobol | morris | adjoint",
    "perturbationMagnitude": "number 0-1 (default: 0.1)",
    "perturbationType": "relative | absolute",
    "variablesToAnalyze": "IRI[]",
    "variablePriority": "IRI[] (ordering for truncation)"
  },
  
  "constraints": {
    "propagationDepth": "integer",
    "uncertaintyThreshold": "number 0-1",
    "excludeEntities": "IRI[]",
    "requireEntities": "IRI[]",
    "temporalBound": "duration",
    "temporalSteps": "integer"
  }
}
```

### 3.2 Causal Model

```json
{
  "@type": "CausalModel",
  "@id": "urn:uuid:causal-model-id",
  
  "metadata": {
    "name": "string",
    "version": "semver",
    "domain": "IRI",
    "modelType": "static | temporal",
    "assumptions": ["string"],
    "limitations": ["string"],
    "sources": ["IRI"],
    "abductionComplexity": "tractable | expensive | intractable"
  },
  
  "variables": [
    {
      "@type": "CausalVariable",
      "@id": "IRI",
      "name": "string",
      "datatype": "numeric | categorical | boolean",
      "domain": "value constraints",
      "domainFinite": "boolean",
      "domainSize": "integer (if finite)",
      "observable": "boolean",
      "manipulable": "boolean",
      "equationInvertible": "boolean",
      "scale": "number (for normalization, default 1.0)",
      "normalizationMethod": "none | zscore | minmax | custom"
    }
  ],
  
  "edges": [
    {
      "@type": "CausalEdge",
      "from": "IRI",
      "to": "IRI",
      "edgeType": "deterministic | probabilistic | enabling | preventing",
      "strength": "number or distribution",
      "mechanism": "IRI",
      "confidence": "number 0-1",
      "temporalLag": "integer"
    }
  ],
  
  "structuralEquations": [
    {
      "@type": "StructuralEquation",
      "variable": "IRI",
      "equation": "string (functional form)",
      "equationType": "linear | polynomial | invertible-nonlinear | general",
      "differentiable": "boolean",
      "noiseDistribution": "distribution specification",
      "inverseEquation": "string (optional)"
    }
  ],
  
  "temporalStructure": {
    "timeStepDuration": "duration",
    "maxLag": "integer",
    "equilibriumDetection": "boolean",
    "equilibriumThreshold": "number",
    "equilibriumMetric": "euclidean | chebyshev | relative-change",
    "equilibriumWindow": "integer",
    "variableNormalization": {
      "method": "none | scale | zscore",
      "scaleFactors": "map of variable IRI -> scale"
    }
  }
}
```

### 3.3 Simulation Result

```json
{
  "@type": "SimulationResult",
  "@id": "urn:uuid:simulation-result-id",
  
  "taint:level": "L4 | L4-fast",
  "taint:source": "css",
  "taint:immutable": true,
  "taint:canPromote": false,
  
  "resultMetadata": {
    "requestId": "string",
    "correlationId": "string",
    "simulatedAt": "xsd:dateTime",
    "durationMs": "integer",
    "executionMode": "exact | fast",
    "stepsExecuted": "integer",
    "temporalStepsSimulated": "integer",
    "entitiesModified": "integer",
    "terminationReason": "completed | timeout | depthLimit | uncertaintyThreshold | resourceLimit | equilibrium",
    "sensitivityComputationMs": "integer"
  },
  
  "consequenceTrace": {
    "@type": "ConsequenceTrace",
    "directEffects": ["CausalEffect"],
    "indirectEffects": ["CausalEffect"],
    "blockedEffects": ["BlockedEffect"],
    "uncertainEffects": ["UncertainEffect"],
    "temporalTrajectory": "TemporalTrajectory (compressed)"
  },
  
  "sensitivityAnalysis": {
    "@type": "SensitivityReport",
    "computationMethod": "one-at-a-time | sobol | morris | adjoint",
    "perturbationMagnitude": "number",
    "variablesAnalyzed": "integer",
    "variablesSensitivities": ["SensitivityMetric"],
    "globalSensitivityIndices": "GlobalIndices (for sobol/morris)",
    "overallRobustness": "number 0-1",
    "criticalInputs": ["IRI"],
    "stableConclusions": ["string"],
    "unstableConclusions": ["string"],
    "truncated": "boolean",
    "truncationReason": "string"
  },
  
  "queryResults": ["QueryResult"],
  "worldDiff": "WorldStateDiff",
  "diagnostics": "Diagnostics"
}
```

#### 3.3.1 Sensitivity Analysis Details

**One-at-a-Time (OAT)**: Perturbs each variable independently. Cost: 2n+1 simulations.

**Morris Method**: Screens for important variables using elementary effects. Cost: r(k+1) simulations where r=trajectories, k=variables. Default r=10.

**Sobol Indices**: Computes first-order and total-order variance-based sensitivity. Cost: n(k+2) simulations where n=samples. Default n=1024.

**Adjoint Method**: For models with differentiable structural equations, computes exact gradients in a single backward pass. Cost: 2 simulations (forward + backward). Requires `differentiable: true` on all equations.

```typescript
interface SensitivityConfig {
  method: 'one-at-a-time' | 'sobol' | 'morris' | 'adjoint';
  
  // OAT parameters
  perturbationMagnitude?: Decimal;  // Default 0.1
  perturbationType?: 'relative' | 'absolute';  // Default 'relative'
  
  // Morris parameters
  morrisTrajectories?: number;  // Default 10
  morrisLevels?: number;  // Default 4
  
  // Sobol parameters
  sobolSamples?: number;  // Default 1024
  sobolOrder?: 'first' | 'total' | 'both';  // Default 'both'
  
  // Variable selection
  variablesToAnalyze: IRI[];
  variablePriority?: IRI[];  // For truncation ordering
}

interface GlobalSensitivityIndices {
  // Sobol indices
  firstOrder?: Map<IRI, Decimal>;  // S_i: main effect
  totalOrder?: Map<IRI, Decimal>;  // S_Ti: total effect including interactions
  
  // Morris indices  
  morrisMu?: Map<IRI, Decimal>;  // μ: mean elementary effect
  morrisMuStar?: Map<IRI, Decimal>;  // μ*: mean absolute elementary effect
  morrisSigma?: Map<IRI, Decimal>;  // σ: std dev of elementary effects
}
```

**Cost Budget Table**:

| Method | Variables | Cost Formula | Example (5 vars) |
|--------|-----------|--------------|------------------|
| OAT | k | 2k + 1 | 11 simulations |
| Morris | k | r(k + 1), r=10 | 60 simulations |
| Sobol | k | n(k + 2), n=1024 | 7168 simulations |
| Adjoint | k | 2 | 2 simulations |

**Method Selection Guidance**:

| Scenario | Recommended Method |
|----------|-------------------|
| Quick screening, few variables | OAT |
| Identify important variables from many | Morris |
| Quantify interactions, variance decomposition | Sobol |
| Differentiable model, need exact gradients | Adjoint |
| Resource-constrained | OAT or Adjoint |

#### 3.3.2 Temporal Trajectory Compression

*(Unchanged from v1.2)*

**Compression Strategies**:

| Strategy | Records | Use Case |
|----------|---------|----------|
| `none` | Full state each step | Debugging |
| `delta` | Changed values only | Standard analysis |
| `sparse` | Significant changes only | Long simulations |

#### 3.3.3 Sensitivity Categorization

| Category | Elasticity Range | Interpretation |
|----------|------------------|----------------|
| Negligible | \|ε\| < 0.01 | Input has virtually no effect |
| Low | 0.01 ≤ \|ε\| < 0.1 | Minor influence |
| Moderate | 0.1 ≤ \|ε\| < 0.5 | Notable influence |
| High | 0.5 ≤ \|ε\| < 1.0 | Strong influence |
| Critical | \|ε\| ≥ 1.0 | Output changes faster than input |

### 3.4 Taint Envelope

```json
{
  "@context": {
    "taint": "https://fnsr.dev/taint/",
    "css": "https://fnsr.dev/css/",
    "@protected": true
  },
  "@type": "taint:TaintedContent",
  
  "taint:level": {
    "@type": "taint:Level",
    "@id": "taint:L4",
    "taint:name": "Hypothetical",
    "taint:canPromoteTo": [],
    "taint:isTerminal": true
  },
  
  "taint:source": {
    "taint:service": "css",
    "taint:operation": "simulate",
    "taint:timestamp": "xsd:dateTime",
    "taint:requestId": "string"
  },
  
  "taint:restrictions": {
    "taint:canMergeToMainLog": false,
    "taint:canBecomeEvidence": false,
    "taint:canInformDecision": true,
    "taint:mustLabelAsHypothetical": true
  },
  
  "taint:content": {
    "@type": "css:SimulationResult"
  }
}
```

---

## 4. Core Algorithm

### 4.1 Simulation Engine Interface

```typescript
interface CSSEngine {
  simulate(request: SimulationRequest): Promise<TaintedResult<SimulationResult>>;
  validate(request: SimulationRequest): ValidationResult;
  estimate(request: SimulationRequest): ResourceEstimate;
  assessAbductionTractability(model: CausalModel): AbductionAssessment;
}

interface TaintedResult<T> {
  readonly taintLevel: 'L4' | 'L4-fast';
  readonly taintSource: 'css';
  readonly canPromote: false;
  readonly content: T;
  
  acknowledgeHypothetical(): T;
  map<U>(fn: (t: T) => U): TaintedResult<U>;
}
```

### 4.2 The Simulation Algorithm

```
FUNCTION simulate(request: SimulationRequest) -> TaintedResult<SimulationResult>:
  
  // Phase 1: Validation
  validation = validate(request)
  IF validation.hasErrors:
    RETURN TaintedResult.error(validation.errors)
  
  // Phase 2: Resolve inputs
  worldState = resolveWorldState(request.worldState)
  causalModel = resolveCausalModel(request.causalModel, worldState)
  
  // Phase 3: Tractability check for counterfactual
  IF request.interventions.any(i => i.operator == 'counterfactual'):
    tractability = assessAbductionTractability(causalModel)
    IF tractability.complexity == 'intractable':
      RETURN TaintedResult.error({code: 'ABDUCTION_INTRACTABLE'})
  
  // Phase 4: Create sandbox
  sandbox = createSandbox(worldState, request.constraints)
  
  // Phase 5: Initialize PRNG with derived seed
  baseSeed = await deriveSeed(
    request.requestMetadata.randomSeed ?? request.requestMetadata.requestId,
    'simulation',
    'main'
  )
  prng = CSSPRNG.fromSeed(baseSeed)
  
  // Phase 6: Apply interventions
  FOR EACH intervention IN request.interventions:
    prng = applyIntervention(sandbox, causalModel, intervention, prng)
  
  // Phase 7: Propagate
  IF causalModel.modelType == 'temporal':
    trace = propagateTemporal(sandbox, causalModel, request.constraints, prng)
  ELSE:
    trace = propagateStatic(sandbox, causalModel, request.constraints, prng)
  
  // Phase 8: Evaluate queries
  queryResults = evaluateQueries(request.queries, sandbox, trace)
  
  // Phase 9: Sensitivity analysis (bounded)
  IF request.sensitivityAnalysis.enabled:
    sensitivity = computeSensitivityBounded(request, sandbox, trace, LIMITS)
  
  // Phase 10: Compress trajectory
  IF trace.hasTemporalTrajectory:
    trace.temporalTrajectory = compressTrajectory(trace.temporalTrajectory, request)
  
  // Phase 11: Assemble result
  result = assembleResult(request, trace, queryResults, sensitivity, sandbox.getDiff())
  
  // Phase 12: Taint wrap
  taintLevel = request.requestMetadata.executionMode == 'fast' ? 'L4-fast' : 'L4'
  RETURN TaintedResult.wrap(result, {level: taintLevel, source: 'css', canPromote: false})
```

### 4.3 Intervention Operators

#### 4.3.1 The `do` Operator

```
FUNCTION applyDoIntervention(sandbox, causalModel, intervention, prng):
  variable = intervention.target
  value = intervention.value
  
  // Graph surgery: sever incoming edges
  FOR EACH edge IN causalModel.getIncomingEdges(variable):
    causalModel.severEdge(edge)
    sandbox.recordSeveredEdge(edge)
  
  sandbox.setValue(variable, value)
  sandbox.markAsIntervened(variable)
  
  RETURN prng
```

#### 4.3.2 The `observe` Operator

```
FUNCTION applyObserveIntervention(sandbox, causalModel, intervention, prng):
  variable = intervention.target
  value = intervention.value
  
  // Conditioning: no graph surgery
  sandbox.setConditionedValue(variable, value)
  sandbox.markAsObserved(variable)
  
  RETURN prng
```

#### 4.3.3 The `counterfactual` Operator

**Numeric Constants**:

| Constant | Value | Description |
|----------|-------|-------------|
| `MAX_ENUMERATION_SIZE` | 10,000 | Maximum domain size for exact enumeration |
| `MAX_VARIATIONAL_ITERATIONS` | 1,000 | Maximum iterations for variational inference |
| `VARIATIONAL_CONVERGENCE_THRESHOLD` | 1e-6 | ELBO convergence criterion |
| `MIN_EFFECTIVE_SAMPLE_SIZE` | 100 | Minimum ESS for sampling methods |

**Tractability Table**:

| Model Property | Complexity | CSS Support | Quality Metric |
|----------------|-----------|-------------|----------------|
| Linear SEMs, Gaussian noise | O(n³) exact | ✓ Full | Exact (1.0) |
| Polynomial, finite domain ≤ 10k | O(d^n) enum | ✓ Full | Exact (1.0) |
| Invertible nonlinear, inverse provided | Varies | ✓ Full | Exact (1.0) |
| General nonlinear | NP-hard | ⚠ Variational | ELBO-normalized |
| Non-invertible | Intractable | ✗ Rejected | N/A |

#### 4.3.4 Abduction Quality Metrics

**Normative Requirement**: Any non-exact abduction MUST report quality metrics in the result.

```typescript
interface AbductionResult {
  method: 'exact' | 'variational' | 'sampling';
  noiseValues: Map<IRI, Decimal>;
  
  // Quality metrics (required for non-exact methods)
  quality?: {
    // For variational: ELBO normalized to [0, 1]
    // For sampling: effective sample size / total samples
    score: Decimal;  // Range [0, 1], higher is better
    
    // Method-specific metrics
    elbo?: Decimal;  // Evidence lower bound (variational)
    effectiveSampleSize?: number;  // ESS (sampling)
    convergenceIterations?: number;  // Iterations to converge
    
    // Confidence assessment
    confidence: 'high' | 'medium' | 'low';
    confidenceReason: string;
  };
  
  // Required warning for approximate methods
  warning?: string;
}

function assessAbductionQuality(result: AbductionResult): QualityAssessment {
  if (result.method === 'exact') {
    return { confidence: 'high', score: CSSMath.fromNumber(1.0) };
  }
  
  if (result.method === 'variational') {
    // ELBO should be close to 0 (log-likelihood) for good fit
    // Normalize: score = exp(ELBO) for negative ELBO, capped at 1
    const score = CSSMath.exp(CSSMath.min(result.quality.elbo, CSSMath.fromNumber(0)));
    const confidence = 
      CSSMath.compare(score, CSSMath.fromString('0.9')) >= 0 ? 'high' :
      CSSMath.compare(score, CSSMath.fromString('0.7')) >= 0 ? 'medium' : 'low';
    
    return {
      score,
      confidence,
      confidenceReason: `ELBO = ${result.quality.elbo}, normalized score = ${score}`
    };
  }
  
  if (result.method === 'sampling') {
    const essRatio = result.quality.effectiveSampleSize / totalSamples;
    const score = CSSMath.fromNumber(Math.min(essRatio, 1.0));
    const confidence = 
      essRatio >= 0.5 ? 'high' :
      essRatio >= 0.1 ? 'medium' : 'low';
    
    return {
      score,
      confidence,
      confidenceReason: `ESS = ${result.quality.effectiveSampleSize}, ratio = ${essRatio}`
    };
  }
}
```

**Graceful Degradation Path**:

```
FUNCTION abduceNoiseValues(sandbox, causalModel, variable, priorValue, prng):
  
  // Try exact methods first
  IF allEquationsLinear(causalModel):
    RETURN exactLinearAbduction(sandbox, causalModel, priorValue)
  
  IF allDomainsFinite(causalModel) AND totalDomainSize <= MAX_ENUMERATION_SIZE:
    RETURN exactEnumerationAbduction(sandbox, causalModel, priorValue)
  
  IF allEquationsHaveInverse(causalModel):
    RETURN exactInverseAbduction(sandbox, causalModel, priorValue)
  
  // Fall back to approximate methods
  IF causalModel.metadata.abductionComplexity != 'intractable':
    result = variationalAbduction(
      sandbox, causalModel, priorValue,
      maxIterations = MAX_VARIATIONAL_ITERATIONS,
      convergenceThreshold = VARIATIONAL_CONVERGENCE_THRESHOLD
    )
    
    quality = assessAbductionQuality(result)
    
    IF quality.confidence == 'low':
      result.warning = 'Variational abduction converged with low confidence. ' +
        'Results may be unreliable. Consider simplifying the model or using do() operator.'
    
    RETURN result
  
  // Model is intractable
  THROW AbductionIntractableError({
    reason: 'Model contains non-invertible equations with infinite domains',
    recommendation: 'Use do() operator instead of counterfactual, or provide inverse equations'
  })
```

**Result Reporting**:

```json
{
  "diagnostics": {
    "abductionPerformed": true,
    "abductionMethod": "variational",
    "abductionQuality": {
      "score": "0.847",
      "elbo": "-0.166",
      "convergenceIterations": 342,
      "confidence": "medium",
      "confidenceReason": "ELBO = -0.166, normalized score = 0.847"
    },
    "abductionWarning": "Approximate abduction used. Quality score 0.847 (medium confidence)."
  }
}
```

### 4.4 Propagation Strategies

#### 4.4.1 Deterministic Propagation

```
FUNCTION propagateDeterministic(sandbox, causalModel, frontier):
  FOR EACH variable IN topologicalOrder(frontier, causalModel):
    equation = causalModel.getStructuralEquation(variable)
    parentValues = getParentValues(variable, sandbox, causalModel)
    
    newValue = equation.evaluate(parentValues, CSSMath)
    sandbox.setValue(variable, newValue)
    
    YIELD Effect(variable, oldValue, newValue, confidence=1.0)
```

#### 4.4.2 Probabilistic Propagation

```
FUNCTION propagateProbabilistic(sandbox, causalModel, frontier, nSamples, prng):
  samples = []
  
  FOR i IN 1..nSamples:
    // Derive independent seed for this sample
    sampleSeed = await deriveSeed(prng.requestId, 'montecarlo', `sample-${i}`)
    samplePrng = CSSPRNG.fromSeed(sampleSeed)
    sampleSandbox = sandbox.clone()
    
    FOR EACH variable IN topologicalOrder(frontier, causalModel):
      equation = causalModel.getStructuralEquation(variable)
      parentValues = getParentValues(variable, sampleSandbox, causalModel)
      
      [noise, samplePrng] = CSSPRNG.sampleDistribution(samplePrng, equation.noiseDistribution)
      newValue = equation.evaluate(parentValues, noise, CSSMath)
      sampleSandbox.setValue(variable, newValue)
    
    samples.add(sampleSandbox.getState())
  
  // Aggregate
  FOR EACH variable IN allVariables:
    distribution = computeDistribution(samples, variable, CSSMath)
    YIELD Effect(variable, sandbox.getValue(variable), distribution, computeConfidence(distribution))
```

### 4.5 Temporal Causal Models

#### 4.5.1 Temporal Model Structure

```json
{
  "@type": "TemporalCausalModel",
  "modelType": "temporal",
  
  "temporalStructure": {
    "timeStepDuration": "PT1H",
    "maxLag": 3,
    "equilibriumDetection": true,
    "equilibriumThreshold": "0.001",
    "equilibriumMetric": "relative-change",
    "equilibriumWindow": 3,
    "variableNormalization": {
      "method": "scale",
      "scaleFactors": {
        "urn:var:price": "100.0",
        "urn:var:panic": "1.0",
        "urn:var:volume": "10000.0"
      }
    }
  }
}
```

#### 4.5.2 Temporal Propagation

```
FUNCTION propagateTemporal(sandbox, causalModel, constraints, prng):
  trace = TemporalTrace()
  currentState = sandbox.getTemporalState(t=0)
  trace.recordSnapshot(0, currentState)
  
  recentStates = CircularBuffer(size=equilibriumWindow)
  recentStates.push(currentState)
  
  FOR t IN 1..constraints.temporalSteps:
    IF exceededLimits(t, trace, constraints):
      trace.terminationReason = 'resourceLimit'
      BREAK
    
    nextState = computeNextState(currentState, causalModel, t, prng)
    trace.recordSnapshot(t, nextState, computeTransitions(currentState, nextState))
    
    IF causalModel.temporalStructure.equilibriumDetection:
      recentStates.push(nextState)
      IF recentStates.isFull() AND isAtEquilibrium(recentStates, causalModel.temporalStructure):
        trace.terminationReason = 'equilibrium'
        trace.equilibriumReachedAt = t
        BREAK
    
    currentState = nextState
  
  RETURN trace
```

#### 4.5.4 Equilibrium Detection

**Definition**: Equilibrium is reached when the normalized state vector remains stable within threshold for `equilibriumWindow` consecutive steps.

**Formal Specification**:

Let $S_t = (v_1^t, v_2^t, \ldots, v_n^t)$ be the state at time $t$.

Let $\hat{S}_t = (v_1^t/s_1, v_2^t/s_2, \ldots, v_n^t/s_n)$ be the normalized state where $s_i$ is the scale factor for variable $i$.

Equilibrium at time $t$ iff:
$$\forall k \in [t-w+1, t]: d(\hat{S}_k, \hat{S}_{k-1}) < \theta$$

**Supported Metrics**:

| Metric | Formula | Use Case |
|--------|---------|----------|
| `euclidean` | $\sqrt{\sum_i (\hat{v}_i^t - \hat{v}_i^{t-1})^2}$ | General purpose |
| `chebyshev` | $\max_i |\hat{v}_i^t - \hat{v}_i^{t-1}|$ | All variables must stabilize |
| `relative-change` | $\max_i \frac{|\hat{v}_i^t - \hat{v}_i^{t-1}|}{|\hat{v}_i^{t-1}| + \epsilon}$ | Scale-invariant |

#### 4.5.5 Variable Normalization

**Problem**: For mixed-scale variables (e.g., price=100, panic=0.5, volume=10000), euclidean distance is dominated by large-scale variables.

**Solution**: Normalize variables before distance computation.

```typescript
interface VariableNormalization {
  method: 'none' | 'scale' | 'zscore';
  
  // For 'scale': divide by these factors
  scaleFactors?: Map<IRI, Decimal>;
  
  // For 'zscore': use these parameters (from historical data or model)
  zscoreParams?: Map<IRI, { mean: Decimal; std: Decimal }>;
}

function normalizeState(
  state: State,
  config: VariableNormalization,
  model: CausalModel
): State {
  const normalized: State = {};
  
  for (const [varId, value] of Object.entries(state)) {
    const variable = model.variables.find(v => v['@id'] === varId);
    
    // Skip non-numeric variables
    if (variable.datatype !== 'numeric') {
      normalized[varId] = value;
      continue;
    }
    
    switch (config.method) {
      case 'none':
        normalized[varId] = value;
        break;
        
      case 'scale':
        const scale = config.scaleFactors?.get(varId) ?? 
                      variable.scale ?? 
                      CSSMath.fromNumber(1);
        normalized[varId] = CSSMath.divide(value, scale);
        break;
        
      case 'zscore':
        const params = config.zscoreParams?.get(varId);
        if (params) {
          normalized[varId] = CSSMath.divide(
            CSSMath.subtract(value, params.mean),
            params.std
          );
        } else {
          normalized[varId] = value;
        }
        break;
    }
  }
  
  return normalized;
}
```

**Handling Non-Numeric Variables**:

- **Categorical**: Excluded from distance computation by default, or use Hamming distance if `includeCategorical: true`
- **Boolean**: Treated as 0/1 numeric
- **Missing/Uncertain**: Use last known value, or exclude from distance with warning

---

## 5. Taint Architecture

### 5.1 The L4 Guarantee

CSS outputs carry L4 (or L4-fast) taint that cannot be removed or promoted.

### 5.2 Taint Interaction Rules

| Source | Operation | Result |
|--------|-----------|--------|
| L4 | Any computation | L4 |
| L4 + L1/L2/L3 | Merge | L4 |
| L4 | Strip attempt | Error |
| L4 | Promote attempt | Error |
| L4-fast | Any | L4-fast |

### 5.3 Cross-Service Taint Flow

```
IEE can:
  ✓ Read simulation for ethical analysis
  ✓ Include in decision rationale
  ✓ Compare simulations
  ✓ Reject scenarios based on simulation

IEE cannot:
  ✗ Treat simulation as evidence
  ✗ Store in verified knowledge base
  ✗ Assert results as facts
  ✗ Remove L4 taint
```

### 5.4 Decision Horizon

The decision acts as a **taint diode**:

```
L4 SimulationResult → Decision Boundary → L1 Decision Record
                                          └─ L4 Reference (preserved)
```

- Decision itself is L1 (observable fact)
- Rationale links to L4 evidence via reference
- Simulation remains L4 (never promoted)
- Audit trail preserves both

### 5.5 Taint Enforcement for Adapters

**Normative Requirement**: All adapters (event bus, storage, analytics) MUST enforce taint restrictions at the protocol level, not just application level.

#### 5.5.1 Event Bus Enforcement

Event adapters MUST reject publish attempts that would place tainted content into L1 persistent stores.

**JSON Schema for Event Validation**:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://fnsr.dev/schemas/taint-validation.json",
  
  "definitions": {
    "L4Content": {
      "type": "object",
      "required": ["taint:level"],
      "properties": {
        "taint:level": {
          "enum": ["L4", "L4-fast"]
        }
      }
    },
    
    "L1Store": {
      "type": "object",
      "properties": {
        "content": {
          "not": { "$ref": "#/definitions/L4Content" }
        }
      }
    }
  },
  
  "type": "object",
  "if": {
    "properties": {
      "destination": { "const": "verified-knowledge-base" }
    }
  },
  "then": {
    "$ref": "#/definitions/L1Store"
  }
}
```

**Adapter Implementation**:

```typescript
class TaintEnforcingEventAdapter implements CSSEventAdapter {
  async publish(event: FNSREvent): Promise<void> {
    // Check if content is tainted
    const taintLevel = extractTaintLevel(event.payload);
    
    if (taintLevel === 'L4' || taintLevel === 'L4-fast') {
      // Verify destination allows L4
      if (!this.destinationAllowsL4(event.destination)) {
        throw new TaintViolationError({
          code: 'L4_TO_L1_STORE_BLOCKED',
          message: `Cannot publish L4 content to ${event.destination}`,
          taintLevel,
          destination: event.destination
        });
      }
      
      // Ensure taint marker is preserved
      if (!event.payload['taint:level']) {
        throw new TaintViolationError({
          code: 'TAINT_MARKER_MISSING',
          message: 'L4 content must include taint:level marker'
        });
      }
    }
    
    await this.underlyingAdapter.publish(event);
  }
  
  private destinationAllowsL4(destination: string): boolean {
    const l4AllowedDestinations = [
      'css-results',
      'simulation-archive',
      'l4-analytics',
      'decision-rationale'
    ];
    return l4AllowedDestinations.includes(destination);
  }
}
```

#### 5.5.2 Storage Adapter Enforcement

Storage adapters MUST:
1. Reject attempts to store L4 content in L1 collections
2. Enforce immutable L4 flags
3. Deny promotion operations

```typescript
class TaintEnforcingStorageAdapter implements CSSStateAdapter {
  async save(content: any, collection: string): Promise<string> {
    const taintLevel = extractTaintLevel(content);
    
    // Check collection compatibility
    const collectionTier = this.getCollectionTier(collection);
    
    if (taintLevel === 'L4' && collectionTier < 4) {
      throw new TaintViolationError({
        code: 'L4_TO_VERIFIED_STORE_BLOCKED',
        message: `Cannot save L4 content to L${collectionTier} collection "${collection}"`,
        allowedCollections: this.getL4Collections()
      });
    }
    
    // Ensure taint is preserved in storage
    if (taintLevel) {
      content = this.ensureTaintPersisted(content, taintLevel);
    }
    
    return await this.underlyingAdapter.save(content, collection);
  }
  
  async promote(id: string, fromTier: number, toTier: number): Promise<void> {
    if (fromTier === 4) {
      throw new TaintViolationError({
        code: 'L4_PROMOTION_BLOCKED',
        message: 'L4 (hypothetical) content cannot be promoted to any tier',
        documentId: id
      });
    }
    
    // Allow other promotions
    await this.underlyingAdapter.promote(id, fromTier, toTier);
  }
}
```

#### 5.5.3 Audit Logging Requirements

Any decision that references L4 content MUST be logged with:

```json
{
  "@type": "L4ReferenceAuditEntry",
  "timestamp": "2025-02-03T14:30:00Z",
  "decisionId": "urn:decision:d-123",
  "l4ReferenceId": "urn:simulation:sim-456",
  "l4TaintLevel": "L4",
  "operatorId": "urn:agent:review-bot",
  "operatorAcknowledgment": true,
  "acknowledgmentMethod": "api-call-with-flag",
  "accessContext": "ethical-review"
}
```

**Log Separation**: Full L4 payloads MUST be stored in separate L4-designated log streams, not mixed with primary operational logs. Primary logs contain only references.

---

## 6. Integration Points

### 6.1 Event Protocol

#### 6.1.1 Request Event: `fnsr.simulation.requested`

```json
{
  "@type": "SimulationRequestedEvent",
  "eventId": "uuid",
  "timestamp": "xsd:dateTime",
  "source": "mdre | iee | user-agent",
  "correlationId": "uuid",
  "payload": {"@type": "SimulationRequest"}
}
```

#### 6.1.2 Result Event: `fnsr.simulation.result`

```json
{
  "@type": "SimulationResultEvent",
  "eventId": "uuid",
  "timestamp": "xsd:dateTime",
  "source": "css",
  "correlationId": "uuid",
  "payload": {
    "@type": "TaintedContent",
    "taint:level": "L4",
    "taint:content": {"@type": "SimulationResult"}
  }
}
```

#### 6.1.3 Progress Event: `fnsr.simulation.progress`

For long-running simulations, CSS emits progress events to enable streaming partial results and responsive UX.

```json
{
  "@type": "SimulationProgressEvent",
  "eventId": "uuid",
  "timestamp": "xsd:dateTime",
  "source": "css",
  "correlationId": "uuid",
  
  "progress": {
    "phase": "validating | resolving | propagating | analyzing | completing",
    "percentComplete": 0.45,
    "stepsCompleted": 450,
    "stepsTotal": 1000,
    "elapsedMs": 1200,
    "estimatedRemainingMs": 1500,
    "estimatedCompletionTime": "xsd:dateTime"
  },
  
  "partialResult": {
    "@type": "PartialSimulationResult",
    "taint:level": "L4",
    "isPartial": true,
    "availableData": {
      "interventionsApplied": true,
      "directEffectsAvailable": true,
      "indirectEffectsAvailable": false,
      "sensitivityAvailable": false
    },
    "consequenceTrace": {
      "directEffects": ["available effects so far"],
      "indirectEffects": "pending"
    }
  },
  
  "resourceUsage": {
    "memoryMb": 128,
    "memoryLimitMb": 256,
    "entitiesModified": 2500,
    "entitiesLimit": 5000
  },
  
  "warnings": [
    "Approaching memory limit (50%)",
    "Estimated completion exceeds timeout by 500ms"
  ],
  
  "gracefulMode": {
    "enabled": false,
    "reason": null,
    "reducedScope": null
  }
}
```

**Progress Event Semantics**:

| Condition | Behavior |
|-----------|----------|
| Normal progress | Emit every 500ms or every 10% completion |
| Approaching timeout | Set `gracefulMode.enabled = true`, reduce scope |
| Approaching memory limit | Emit warning, consider early termination |
| Partial results useful | Include `partialResult` with available data |

**Graceful Degradation**:

When resource limits are approaching, CSS can enter graceful mode:

```json
{
  "gracefulMode": {
    "enabled": true,
    "reason": "timeout-approaching",
    "reducedScope": {
      "sensitivitySkipped": true,
      "trajectoryDownsampled": 10,
      "propagationDepthReduced": 50
    },
    "guaranteedDelivery": [
      "directEffects",
      "queryResults"
    ]
  }
}
```

**Client Handling**:

```typescript
// Example client subscription
cssClient.onProgress(correlationId, (progress) => {
  updateProgressBar(progress.percentComplete);
  
  if (progress.partialResult?.availableData.directEffectsAvailable) {
    renderPartialResults(progress.partialResult.consequenceTrace.directEffects);
  }
  
  if (progress.gracefulMode.enabled) {
    showWarning(`Simulation scope reduced: ${progress.gracefulMode.reason}`);
  }
});
```

### 6.2 Adapter Interfaces

```typescript
interface CSSStateAdapter {
  saveSnapshot(worldState: WorldState): Promise<SnapshotId>;
  loadSnapshot(id: SnapshotId): Promise<WorldState>;
  listSnapshots(filter?: SnapshotFilter): Promise<SnapshotMetadata[]>;
}

interface CSSModelAdapter {
  registerModel(model: CausalModel): Promise<ModelId>;
  getModel(id: ModelId): Promise<CausalModel>;
  deriveModel(scope: IRI[], ontology: Ontology): Promise<CausalModel>;
}

interface CSSEventAdapter {
  subscribe(eventType: string, handler: EventHandler): Subscription;
  publish(event: FNSREvent): Promise<void>;
  // Taint enforcement is mandatory
  validateTaint(event: FNSREvent): TaintValidationResult;
}
```

### 6.3 Query Path Placement

```
Fast Path (< 200ms):     [CSS bypassed]
Standard Path (< 1s):    [CSS bypassed]
Full Path (< 2s+):       IRIS → W2Fuel → Assay → MDRE/IEE → CSS → Response
```

### 6.4 Causal Model Derivation

**Status**: ⚠️ **EXPERIMENTAL**

Derivation from ontology is experimental. Explicitly authored models are strongly preferred.

---

## 7. Offline and Degraded Operation

### 7.1 Offline-First Design

| Dependency | Offline Behavior |
|------------|------------------|
| World State | Must be inline or cached |
| Causal Models | Must be inline or cached |
| Event Bus | Queue locally |

### 7.2 Explicit Uncertainty

All uncertainty sources are surfaced in results.

---

## 8. Resource Limits and Decidability

### 8.1 Bounded Computation

```json
{
  "@type": "ResourceLimits",
  
  "time": {
    "maxWallClockMs": 30000,
    "maxCpuMs": 10000,
    "warningThresholdMs": 5000,
    "progressIntervalMs": 500
  },
  
  "space": {
    "maxMemoryMb": 256,
    "maxSandboxEntities": 10000,
    "maxCausalEdges": 50000,
    "maxModifiedEntities": 5000
  },
  
  "computation": {
    "maxPropagationSteps": 1000,
    "maxMonteCarloSamples": 10000,
    "maxRecursionDepth": 100,
    "maxTemporalSteps": 1000,
    "maxAbductionIterations": 1000
  },
  
  "sensitivity": {
    "maxVariablesOAT": 10,
    "maxVariablesMorris": 20,
    "maxVariablesSobol": 10,
    "maxTotalSimulations": 100,
    "morrisTrajectories": 10,
    "sobolSamples": 1024
  },
  
  "output": {
    "maxResultSizeKb": 1024,
    "maxEffectsReported": 500,
    "maxTrajectorySnapshots": 200,
    "truncationStrategy": "priority | recency | magnitude"
  }
}
```

### 8.2 Decidability Guarantees

1. Static models must be DAGs
2. Temporal models bounded by `maxTemporalSteps`
3. Probabilistic bounded by `maxMonteCarloSamples`
4. Abduction bounded by tractability assessment
5. Sensitivity bounded by method-specific limits
6. Watchdog enforces wall-clock timeout

---

## 9. Conformance Testing

### 9.1 Test Categories

| Category | Description | Required |
|----------|-------------|----------|
| Arithmetic | Test vectors from Appendix A | ✓ |
| Cross-platform | Same results across engines | ✓ |
| Seed derivation | HKDF produces canonical seeds | ✓ |
| Taint enforcement | L4 cannot escape | ✓ |
| Resource limits | Termination within bounds | ✓ |
| Equilibrium | Correct detection | ✓ |
| Compression | Lossless reconstruction | ✓ |
| Abduction quality | Metrics reported | ✓ |

### 9.2 Golden Trace Artifacts

Repository maintains golden traces for regression testing:

```
golden/
  canonical-trace.json          # Reference simulation output
  arithmetic-vectors.json       # Decimal arithmetic test cases
  seed-derivation-vectors.json  # HKDF test cases
  equilibrium-traces/           # Various equilibrium scenarios
  compression-traces/           # Compression round-trip tests
```

### 9.3 Stress Tests

- Large graphs (near `maxCausalEdges`)
- Many Monte Carlo samples
- Long temporal simulations
- Counterfactual edge cases
- Concurrent simulation requests

---

## 10. Security and Privacy

### 10.1 Threat Model

| Threat | Mitigation |
|--------|------------|
| L4 content pollutes knowledge base | Taint enforcement at adapter level |
| Sensitive data in world diffs | Redaction policies |
| Simulation results leak PII | Access control, data minimization |
| Timing attacks via simulation | Resource limits, no early termination on secret data |

### 10.2 Redaction Policies

**Normative Requirement**: When world state contains PII or sensitive data, CSS MUST support redaction in outputs.

```typescript
interface RedactionPolicy {
  // Fields to always redact from worldDiff
  alwaysRedact: IRI[];
  
  // Patterns to detect and redact (regex)
  patterns: {
    ssn: /\d{3}-\d{2}-\d{4}/,
    email: /[\w.-]+@[\w.-]+/,
    creditCard: /\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}/
  };
  
  // Role-based visibility
  roleBasedAccess: {
    'analyst': ['summary', 'queryResults'],
    'auditor': ['full'],
    'dashboard': ['aggregates']
  };
  
  // Redaction method
  method: 'remove' | 'hash' | 'mask' | 'generalize';
}
```

**Applying Redaction**:

```typescript
function applyRedaction(
  result: SimulationResult,
  policy: RedactionPolicy,
  accessorRole: string
): SimulationResult {
  const allowedFields = policy.roleBasedAccess[accessorRole];
  
  // Deep clone and redact
  const redacted = structuredClone(result);
  
  // Remove disallowed fields
  if (!allowedFields.includes('full')) {
    if (!allowedFields.includes('worldDiff')) {
      delete redacted.worldDiff;
    }
    if (!allowedFields.includes('consequenceTrace')) {
      redacted.consequenceTrace = { redacted: true };
    }
  }
  
  // Apply pattern-based redaction to remaining content
  redactPatterns(redacted, policy.patterns, policy.method);
  
  // Remove explicitly listed fields
  for (const field of policy.alwaysRedact) {
    removeField(redacted, field);
  }
  
  redacted.diagnostics.redactionApplied = true;
  redacted.diagnostics.redactionPolicy = policy.id;
  
  return redacted;
}
```

### 10.3 Data Minimization

For analytics and dashboards, use trajectory downsampling and aggregation:

```json
{
  "trajectoryOptions": {
    "downsampleFactor": 100,
    "aggregation": "summary",
    "excludeFromAnalytics": ["urn:var:sensitive-*"]
  }
}
```

### 10.4 Access Control

L4 payloads require explicit access grants:

```typescript
interface L4AccessGrant {
  grantId: string;
  simulationId: string;
  grantedTo: string;  // Role or principal
  grantedBy: string;  // Authorizing principal
  scope: 'full' | 'summary' | 'reference-only';
  expiresAt: Date;
  purpose: string;  // Required justification
}
```

---

## 11. Reference Implementation

### 11.1 Entry Point

```typescript
// css.ts - Main entry point

import { CSSMath, CSSPRNG, deriveSeed } from './css-arithmetic';
import { TaintedResult } from './taint';
import { DEFAULT_LIMITS } from './limits';

export class CSS implements CSSEngine {
  constructor(
    private limits: ResourceLimits = DEFAULT_LIMITS,
    private adapters: CSSAdapters = {}
  ) {}
  
  async simulate(request: SimulationRequest): Promise<TaintedResult<SimulationResult>> {
    // Implementation follows §4.2 algorithm
  }
}

// Browser-compatible export
export { CSS, CSSMath, CSSPRNG, TaintedResult };
```

### 11.2 Package Structure

```
css/
├── src/
│   ├── css.ts                 # Main engine
│   ├── css-arithmetic.ts      # Deterministic math
│   ├── css-prng.ts           # Seeded PRNG
│   ├── seed-derivation.ts    # HKDF implementation
│   ├── taint.ts              # Taint types and enforcement
│   ├── propagation/
│   │   ├── static.ts
│   │   ├── temporal.ts
│   │   └── equilibrium.ts
│   ├── intervention/
│   │   ├── do.ts
│   │   ├── observe.ts
│   │   └── counterfactual.ts
│   ├── sensitivity/
│   │   ├── oat.ts
│   │   ├── morris.ts
│   │   ├── sobol.ts
│   │   └── adjoint.ts
│   └── adapters/
│       ├── event.ts
│       └── storage.ts
├── test/
│   ├── conformance/
│   │   ├── arithmetic.test.ts
│   │   ├── cross-platform.test.ts
│   │   ├── seed-derivation.test.ts
│   │   └── taint.test.ts
│   ├── golden/
│   │   └── *.json
│   └── stress/
├── golden/
│   ├── canonical-trace.json
│   └── arithmetic-vectors.json
└── package.json
```

---

## 12. Glossary

| Term | Definition |
|------|------------|
| **Abduction** | Inferring hidden variables from observed outcomes |
| **Adjoint Method** | Gradient computation via backward pass |
| **Causal Model** | Directed graph specifying causal relationships |
| **Decision Horizon** | Boundary where L4 informs L1 without taint leakage |
| **ELBO** | Evidence Lower Bound (variational inference quality) |
| **ESS** | Effective Sample Size |
| **HKDF** | HMAC-based Key Derivation Function |
| **L4 Taint** | Indelible marker for hypothetical content |
| **Morris Method** | Elementary effects sensitivity screening |
| **OAT** | One-at-a-time sensitivity analysis |
| **Sobol Indices** | Variance-based global sensitivity measures |
| **Taint Diode** | One-way information flow preserving taint |

---

## 13. References

1. Pearl, J. (2009). *Causality* (2nd ed.). Cambridge.
2. Saltelli, A. et al. (2008). *Global Sensitivity Analysis*. Wiley.
3. Murphy, K. P. (2002). *Dynamic Bayesian Networks*. UC Berkeley.
4. RFC 5869: HKDF (HMAC-based Key Derivation Function)
5. IEEE 754-2008: Floating-Point Arithmetic

---

## Appendix A: Canonical Test Vectors

### A.1 Arithmetic Vectors

```json
{
  "version": "2.0",
  "vectors": [
    {"op": "add", "a": "0.1", "b": "0.2", "expected": "0.3"},
    {"op": "divide", "a": "1", "b": "3", "expected": "0.3333333333333333333333333333333333"},
    {"op": "sqrt", "a": "2", "expected": "1.414213562373095048801688724209698"},
    {"op": "exp", "a": "1", "expected": "2.718281828459045235360287471352662"},
    {"op": "ln", "a": "2.718281828459045235360287471352662", "expected": "1.000000000000000000000000000000000"},
    {"op": "pow", "a": "2", "b": "0.5", "expected": "1.414213562373095048801688724209698"}
  ]
}
```

### A.2 Seed Derivation Vectors

```json
{
  "version": "1.0",
  "vectors": [
    {
      "requestId": "test-request-id",
      "namespace": "simulation",
      "componentId": "main",
      "expectedHex": "a1b2c3d4e5f6..."
    }
  ]
}
```

---

## Appendix B: Default Resource Limits

```typescript
const DEFAULT_LIMITS: ResourceLimits = {
  time: { maxWallClockMs: 30000, maxCpuMs: 10000, warningThresholdMs: 5000, progressIntervalMs: 500 },
  space: { maxMemoryMb: 256, maxSandboxEntities: 10000, maxCausalEdges: 50000, maxModifiedEntities: 5000 },
  computation: { maxPropagationSteps: 1000, maxMonteCarloSamples: 10000, maxTemporalSteps: 1000, maxAbductionIterations: 1000 },
  sensitivity: { maxVariablesOAT: 10, maxVariablesMorris: 20, maxVariablesSobol: 10, maxTotalSimulations: 100 },
  output: { maxResultSizeKb: 1024, maxEffectsReported: 500, maxTrajectorySnapshots: 200 }
};
```

---

## Appendix C: Numeric Constants

| Constant | Value | Section |
|----------|-------|---------|
| `MAX_ENUMERATION_SIZE` | 10,000 | §4.3.3 |
| `MAX_VARIATIONAL_ITERATIONS` | 1,000 | §4.3.3 |
| `VARIATIONAL_CONVERGENCE_THRESHOLD` | 1e-6 | §4.3.3 |
| `MIN_EFFECTIVE_SAMPLE_SIZE` | 100 | §4.3.3 |
| `DEFAULT_EQUILIBRIUM_THRESHOLD` | 0.001 | §4.5.4 |
| `DEFAULT_EQUILIBRIUM_WINDOW` | 3 | §4.5.4 |
| `DEFAULT_PERTURBATION_MAGNITUDE` | 0.1 | §3.3.1 |

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-02-02 | Initial specification |
| 1.1.0 | 2025-02-03 | Deterministic arithmetic, temporal models, sensitivity |
| 1.2.0 | 2025-02-03 | Resource limits, equilibrium, compression |
| 2.0.0 | 2025-02-03 | Cross-platform CI, HKDF seeds, abduction quality, global sensitivity, taint enforcement, streaming, security |

---

*CSS is how FNSR dreams responsibly. It imagines possibilities without confusing them with facts. The L4 taint is not a limitation but a liberation—it permits exploration of any scenario because hypotheticals cannot contaminate knowledge.*