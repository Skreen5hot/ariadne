# Semantic Function Schema (SFS)

**Version:** 2.2 — AI-Readiness Foundation

**Status:** Draft

**Supersedes:** v2.1

**Audience:** Semantic engineers, AI/ML engineers, ontology engineers, system architects

**Scope:** Pure, composable semantic functions with AI agent integration support

---

## Changelog: v2.1 → v2.2

Version 2.2 introduces AI-Readiness features that enable autonomous agents to discover, reason about, compose, and safely execute semantic functions. These additions do not alter existing runtime semantics—they provide the metadata and structural foundations required for human-AI collaboration.

### Design Philosophy

AI agents are not special. They are callers that must honor the same semantic constraints as human developers. v2.2 provides better tooling for agents to:
- Discover functions via natural language
- Reason about composition via postconditions
- Prove correctness via verification interfaces
- Accept accountability via plan handshakes
- Defer to humans via authorization gates

### Summary of Changes

| Section | Change |
|---------|--------|
| §3.4.5 | Effect Authorization (NEW) — Human-in-the-loop gates for effect execution with approval levels |
| §3.8 | Postconditions (NEW) — What becomes true after function execution, enabling forward reasoning |
| §3.9 | Semantic Function Signature (REVISED) — Now includes postconditions field |
| §8.5 | Discovery Metadata (NEW) — Natural language intent labels and semantic domain tags for AI search |
| §15 | Agent Integration (NEW) — Plan handshakes, agent identity, execution plans, and verification interfaces |
| §16 | Human-AI Collaboration (NEW) — Authorization enforcement, delegation chains, and audit requirements |

---

## 1. Executive Summary

Semantic Function Schema (SFS) v2.2 formalizes a model for pure, deterministic semantic functions whose effects are expressed as data and whose meaning is formally aligned with ontology artifacts. This specification provides the complete formal foundation for building semantically grounded, composable computational systems that support both human developers and autonomous AI agents.

SFS defines three distinct but related concerns:
1. **Semantic execution calculus** — How pure functions compose
2. **Portable effect protocol** — How state changes are described without being performed
3. **Code-ontology co-evolution contract** — How computational artifacts stay aligned with their formal representations

Version 2.2 extends v2.1 with AI-Readiness features that enable agents to participate in the semantic ecosystem as first-class citizens. These features include:
- Discovery metadata for natural language function search
- Postconditions for forward reasoning and plan construction
- Plan handshakes for accountability and traceability
- Authorization gates for human-in-the-loop safety

The core architectural insight remains:

```
Functions compute.
Goals declare.
Effects describe.
Planners orchestrate.
```

Each concern has its proper place, and every boundary is explicit. AI agents operate within these same boundaries—they gain no special privileges, only better tooling for discovery and composition.

---

## 2. Normative Principles

The following principles are NORMATIVE and define compliance with SFS v2.2. Implementations violating any normative requirement are non-compliant.

### 2.1 Purity

All executable semantic functions MUST be pure. A function is pure if and only if:
- (a) Given identical inputs and context, it always produces identical outputs, effects, and errors
- (b) It performs no observable mutation of external state during execution
- (c) Its return value depends only on its explicit inputs and context

### 2.2 Determinism

All executable semantic functions MUST be deterministic. Determinism requires that function execution follows a single, predictable path determined entirely by inputs and context. Non-deterministic constructs (random number generation, system time access, concurrent state observation) are prohibited within function bodies.

### 2.3 Explicit Effects

No semantic function MAY perform side effects. All intended state changes MUST be returned as Effect descriptors. The execution environment is responsible for interpreting and executing Effect descriptors; the function itself never causes state change.

### 2.4 Semantic Completeness

Every semantic function MUST declare:
- **Inputs** — Typed parameters
- **Preconditions** — Required invariants
- **Postconditions** — Guaranteed outcomes
- **Outputs** — Typed return values
- **Failure modes** — Typed domain errors with identifiers
- **Effects** — Typed state change descriptors

Omission of any declaration element renders the function non-compliant.

### 2.5 Compositional Closure

Compositions of valid semantic functions MUST themselves satisfy this schema. No composition may introduce impurity, non-determinism, or implicit effects. The composition of compliant functions is compliant.

### 2.6 Ontology Parity

Ontology artifacts MUST be verifiably consistent with their computational counterparts. This consistency MUST be machine-testable. Advisory alignment is insufficient; parity is a testable invariant.

### 2.7 Agent Neutrality (v2.2)

The specification makes no distinction between human and AI callers at the semantic layer. All callers—human developers, automated systems, and AI agents—MUST satisfy the same preconditions, receive the same postcondition guarantees, and respect the same authorization requirements. Agent-specific metadata exists for traceability, not privilege.

---

## 3. Type Definitions

This section provides the complete, normative type definitions for SFS v2.2. All types are expressed in TypeScript notation with semantic annotations.

### 3.1 Foundational Types

#### 3.1.1 Timestamp

```typescript
type Timestamp = {
  readonly iso8601: string
  readonly epochMs: number
}
```

Timestamps represent moments in logical or wall-clock time. Both representations MUST be consistent.

#### 3.1.2 IRI (Internationalized Resource Identifier)

```typescript
type IRI = string & { readonly __brand: 'IRI' }
```

IRIs serve as ontology entity references. The brand ensures nominal typing.

#### 3.1.3 Version

```typescript
type Version = {
  readonly major: number
  readonly minor: number
  readonly patch: number
  readonly prerelease?: string
}
```

#### 3.1.4 Duration (v2.2)

```typescript
type Duration = {
  readonly milliseconds: number
  readonly iso8601?: string  // e.g., 'PT5M' for 5 minutes
}
```

Durations represent time spans, used for timeouts and deadlines in authorization flows.

### 3.2 Context Type

Context represents read-only environmental data passed explicitly to functions. Context preserves purity by making environmental dependencies explicit rather than ambient.

```typescript
type Context<T extends Record<string, unknown> = Record<string, never>> = {
  readonly [K in keyof T]: T[K]
} & {
  readonly __contextBrand: unique symbol
}

type EmptyContext = Context<Record<string, never>>
```

#### 3.2.1 Context Constraints

- Context values MUST be serializable to JSON without loss
- Context MUST NOT contain live handles (file descriptors, database connections, network sockets)
- Context MUST NOT contain functions or closures
- Context MUST be deeply immutable
- Context MUST be explicitly typed at function declaration

#### 3.2.2 Standard Context Fields

The following context fields are RECOMMENDED for common use cases:

| Field | Type | Purpose |
|-------|------|---------|
| `logicalClock` | `number` | Monotonic sequence for ordering |
| `authSnapshot` | `AuthState` | Frozen authorization state |
| `correlationId` | `string` | Request tracing identifier |
| `tenantId` | `string` | Multi-tenant isolation key |
| `agentIdentity` | `AgentIdentity` | v2.2: Identity of the calling agent |

#### 3.2.3 Context Schema Versioning

Contexts evolve over time. A function compiled against AuthState v1 may receive AuthState v2 at runtime. To surface this concern explicitly, context types MAY include schema version information.

```typescript
type VersionedContext<T extends Record<string, unknown>> = Context<T> & {
  readonly __contextSchemaVersion: Version
  readonly __contextSchemaIRI?: IRI
}
```

> **Note:** Context versioning is OPTIONAL but RECOMMENDED for contexts that are likely to evolve.

### 3.3 Condition Type

Conditions represent testable predicates over state. They are the fundamental building block for preconditions, postconditions, and goal satisfaction criteria.

```typescript
type Condition<S = unknown> = {
  readonly id: IRI
  readonly description: string
  readonly predicate: ConditionPredicate<S>
  readonly negation?: Condition<S>
}

type ConditionPredicate<S> =
  | { kind: 'expression'; evaluate: (state: S) => boolean }
  | { kind: 'reference'; conditionId: IRI }
  | { kind: 'composite'; operator: LogicalOperator; operands: Condition<S>[] }
```

#### 3.3.1 Logical Operators

```typescript
type LogicalOperator = 'AND' | 'OR' | 'NOT' | 'IMPLIES' | 'IFF'
```

- **AND:** All operands must hold
- **OR:** At least one operand must hold
- **NOT:** Single operand must not hold
- **IMPLIES:** If first operand holds, second must hold
- **IFF:** Both operands have same truth value

#### 3.3.2 Condition Composition

```typescript
function and<S>(...conditions: Condition<S>[]): Condition<S>
function or<S>(...conditions: Condition<S>[]): Condition<S>
function not<S>(condition: Condition<S>): Condition<S>
function implies<S>(antecedent: Condition<S>, consequent: Condition<S>): Condition<S>
```

#### 3.3.3 Condition Evaluation

Condition evaluation MUST be pure and deterministic:
- A condition with kind `'expression'` is evaluated by invoking its `evaluate` function
- A condition with kind `'reference'` is resolved by looking up the referenced condition and evaluating it
- A condition with kind `'composite'` is evaluated according to its logical operator

#### 3.3.4 Condition Purity Constraints

Condition predicates of kind `'expression'` carry inherent purity risk. Condition predicates MUST be:
- **Total** — Must return a boolean for all valid inputs
- **Side-effect free** — Must not mutate external state
- **Deterministic** — Same state yields same result
- **State-dependent only** — Must not access ambient context, time, or randomness

> **Warning:** Teams will accidentally introduce impurity through time access, randomness, or external cache reads. Test harnesses SHOULD include condition purity verification.

```typescript
// Enforcement strategies for production systems:

// Strategy 1: Restricted DSL compilation
type SafePredicate<S> = {
  kind: 'dsl'
  ast: PredicateAST  // Restricted to property access, comparison, boolean ops
}

// Strategy 2: Property-path predicates
type PropertyPredicate<S> = {
  kind: 'property'
  path: readonly string[]
  operator: 'eq' | 'neq' | 'gt' | 'lt' | 'gte' | 'lte' | 'in' | 'contains'
  value: unknown
}
```

### 3.4 Effect Type

Effects represent intended state changes as data. They are descriptors, not executors.

```typescript
type Effect<T = unknown> = {
  readonly id: IRI
  readonly kind: EffectKind
  readonly target: EffectTarget
  readonly payload: T
  readonly timestamp: Timestamp
  readonly idempotencyKey?: string
  readonly authorization?: EffectAuthorization  // v2.2: HITL gates
}

type EffectKind =
  | 'CREATE' | 'UPDATE' | 'DELETE'  // Entity mutations
  | 'EMIT'                           // Event publication
  | 'NOTIFY'                         // User notification
  | 'SCHEDULE'                       // Deferred execution
  | 'CANCEL'                         // Scheduled task cancellation
  | 'CUSTOM'                         // Domain-specific extension

type EffectTarget = {
  readonly system: string
  readonly resource: string
  readonly identifier?: string
}
```

#### 3.4.1 Effect Ontology Alignment

Every Effect MUST have an ontology counterpart. The Effect IRI MUST resolve to an ontology entity of type `obo:BFO_0000015` (Process) or a subclass thereof.

#### 3.4.2 Effect Algebra

Effects form a monoid under concatenation with the empty list as identity.

```typescript
type EffectList<Fx> = readonly Fx[]

const emptyEffects: EffectList<never> = []

function concatEffects<Fx>(
  left: EffectList<Fx>,
  right: EffectList<Fx>
): EffectList<Fx> {
  return [...left, ...right]
}
```

#### 3.4.3 Effect Type Aliases

```typescript
type NoEffect = never
type Effects<Fx extends Effect> = EffectList<Fx>
```

#### 3.4.4 Declared vs Emitted Effects

`effectTypes` declares the upper bound of effects a function may emit. Every emitted effect MUST have an IRI that appears in `effectTypes`. Emitting an undeclared effect type is a compliance violation.

#### 3.4.5 Effect Authorization (v2.2)

Effect authorization enables human-in-the-loop safety gates. When an AI agent or automated system triggers effects, certain operations may require human confirmation before execution.

> **AI-Ready:** This is the primary safety mechanism for AI agent integration. It ensures the semantic boundary remains inviolable even when AI is triggering effects.

```typescript
type EffectAuthorization = {
  readonly level: AuthorizationLevel
  readonly reason?: string
  readonly requiredRoles?: readonly string[]
  readonly timeout?: Duration
  readonly fallbackAction?: 'REJECT' | 'QUEUE' | 'ESCALATE'
}

type AuthorizationLevel =
  | 'AUTO'        // Execute without human intervention
  | 'NOTIFY'      // Execute but notify humans
  | 'CONFIRM'     // Pause until single human confirms
  | 'MULTI_PARTY' // Pause until multiple humans confirm
```

Authorization levels form a hierarchy: `AUTO < NOTIFY < CONFIRM < MULTI_PARTY`. Effect executors MUST enforce the declared level. If authorization times out, the `fallbackAction` determines behavior.

| Level | Behavior | Typical Use Case |
|-------|----------|------------------|
| `AUTO` | Immediate execution | Low-risk operations: logging, notifications, reads |
| `NOTIFY` | Execute + alert | Audit-worthy operations: user data access, config changes |
| `CONFIRM` | Pause for approval | Destructive operations: DELETE, financial transactions |
| `MULTI_PARTY` | Multiple approvals | Critical operations: production deployments, large transfers |

```typescript
// Example: DELETE effect requiring human confirmation
const deleteUserEffect: Effect<{ userId: string }> = {
  id: 'urn:sfs:effects:deleteUser' as IRI,
  kind: 'DELETE',
  target: { system: 'identity', resource: 'user', identifier: '12345' },
  payload: { userId: '12345' },
  timestamp: { iso8601: '2024-01-15T10:00:00Z', epochMs: 1705312800000 },
  authorization: {
    level: 'CONFIRM',
    reason: 'Permanent user deletion requires human approval',
    requiredRoles: ['admin', 'data-protection-officer'],
    timeout: { milliseconds: 86400000, iso8601: 'P1D' },  // 24 hours
    fallbackAction: 'REJECT'
  }
}
```

### 3.5 Error Types

#### 3.5.1 Domain Error

```typescript
type DomainError<E extends string = string> = {
  readonly code: E
  readonly message: string
  readonly category: ErrorCategory
  readonly recoverable: boolean
  readonly ontologyRef: IRI
  readonly failureModeId?: IRI
}

type ErrorCategory =
  | 'PRECONDITION'     // Readiness failure
  | 'VALIDATION'       // Input constraint violation
  | 'DOMAIN'           // Business rule violation
  | 'INTEGRATION'      // External system failure
  | 'INVARIANT'        // Internal consistency violation
  | 'AUTHORIZATION'    // v2.2: Human approval denied or timed out
```

#### 3.5.2 Precondition Errors

```typescript
type PreconditionError<E extends string = string> = DomainError<E> & {
  readonly category: 'PRECONDITION'
  readonly failedCondition: IRI
}
```

#### 3.5.3 Authorization Errors (v2.2)

Authorization errors occur when human approval is required but not granted.

```typescript
type AuthorizationError<E extends string = string> = DomainError<E> & {
  readonly category: 'AUTHORIZATION'
  readonly effectId: IRI
  readonly denialReason: 'TIMEOUT' | 'REJECTED' | 'INSUFFICIENT_APPROVALS'
  readonly requestedBy: AgentIdentity
  readonly reviewedBy?: readonly AgentIdentity[]
}
```

#### 3.5.4 Metadata Container

```typescript
const MetaSymbol: unique symbol = Symbol('SemanticFunctionMeta')

type MetaContainer = {
  readonly [MetaSymbol]: {
    readonly trace?: readonly string[]
    readonly timing?: { startMs: number; endMs: number }
    readonly debug?: Record<string, unknown>
    readonly agentTrace?: readonly AgentIdentity[]  // v2.2: Agent chain
  }
}
```

### 3.6 Result Type

```typescript
type SemanticResult<O, E extends string, Fx> =
  | SuccessResult<O, Fx>
  | FailureResult<E>

type SuccessResult<O, Fx> = {
  readonly ok: true
  readonly value: O
  readonly effects: EffectList<Fx>
} & Partial<MetaContainer>

type FailureResult<E extends string> = {
  readonly ok: false
  readonly error: DomainError<E>
} & Partial<MetaContainer>
```

### 3.7 Failure Mode Specification

```typescript
type FailureMode<E extends string> = {
  readonly id: IRI
  readonly error: DomainError<E>
  readonly triggerCondition: Condition<unknown>
  readonly mitigations: readonly Mitigation[]
}

type Mitigation = {
  readonly strategy: 'RETRY' | 'FALLBACK' | 'ESCALATE' | 'COMPENSATE'
  readonly description: string
  readonly automatable: boolean
}
```

### 3.8 Postconditions (v2.2)

Postconditions specify what becomes true after successful function execution. They are the complement to preconditions and enable AI agents to reason forward: "If I run Function A, its postcondition may satisfy the precondition of Function B."

> **AI-Ready:** Postconditions are essential for AI planning. Without them, agents cannot construct valid execution plans toward goals.

```typescript
type Postcondition<O, S = unknown> = {
  readonly id: IRI
  readonly description: string
  readonly appliesWhen: PostconditionScope
  readonly guarantees: Condition<S>
  readonly outputBinding?: OutputBinding<O, S>
}

type PostconditionScope =
  | 'SUCCESS'   // Applies only when function succeeds
  | 'FAILURE'   // Applies only when function fails
  | 'ALWAYS'    // Applies regardless of outcome

type OutputBinding<O, S> = {
  readonly description: string
  readonly bind: (output: O, priorState: S) => S  // How output changes world state
}
```

Postconditions may be conditional on the result. A validation function has different postconditions for success (input is valid) versus failure (input is invalid but now we know why).

```typescript
// Example: Email validation postconditions
const emailValidationPostconditions: Postcondition<
  { valid: boolean; normalized: string },
  EmailState
>[] = [
  {
    id: 'urn:sfs:example:validateEmail:post:valid' as IRI,
    description: 'Email is confirmed valid and normalized',
    appliesWhen: 'SUCCESS',
    guarantees: {
      id: 'urn:sfs:conditions:emailIsValid' as IRI,
      description: 'The email address conforms to RFC 5322',
      predicate: { kind: 'expression', evaluate: (s: EmailState) => s.isValidated }
    },
    outputBinding: {
      description: 'Sets normalized email in world state',
      bind: (output, prior) => ({
        ...prior,
        normalizedEmail: output.normalized,
        isValidated: true
      })
    }
  },
  {
    id: 'urn:sfs:example:validateEmail:post:invalid' as IRI,
    description: 'Email is confirmed invalid with reason',
    appliesWhen: 'FAILURE',
    guarantees: {
      id: 'urn:sfs:conditions:emailValidationAttempted' as IRI,
      description: 'Email validation has been attempted',
      predicate: { kind: 'expression', evaluate: (s: EmailState) => s.validationAttempted }
    }
  }
]
```

#### 3.8.1 Postcondition Chaining

The power of postconditions emerges in composition. Given functions `f` and `g`, if `f`'s postcondition guarantees a condition that `g` requires as a precondition, then `f >>> g` is a valid composition.

```typescript
// Postcondition chaining enables automated plan construction
//
// validateEmail postcondition: { emailIsValid: true }
// sendWelcomeEmail precondition: { emailIsValid: true }
//
// Therefore: validateEmail >>> sendWelcomeEmail is valid
// An AI planner can discover this automatically
```

### 3.9 Semantic Function Signature (Revised in v2.2)

The semantic function signature now includes postconditions, completing the pre/post contract model required for AI planning.

```typescript
type SemanticFunction<
  I,
  O,
  E extends string,
  Fx extends Effect,
  Ctx extends Context = EmptyContext
> = {
  readonly id: IRI
  readonly version: Version
  readonly preconditions: readonly Condition<I & Ctx>[]
  readonly postconditions: readonly Postcondition<O>[]  // v2.2: NEW
  readonly failureModes: readonly FailureMode<E>[]
  readonly effectTypes: readonly IRI[]
  readonly execute: (input: I, context: Ctx) => SemanticResult<O, E, Fx>
}
```

---

## 4. Function Categories

### 4.1 Primitive Functions

A primitive function is an atomic unit of semantic computation. It is not composed of other semantic functions.

```typescript
type PrimitiveFunction<I, O, E extends string, Fx extends Effect, Ctx> =
  SemanticFunction<I, O, E, Fx, Ctx> & {
    readonly kind: 'primitive'
  }
```

### 4.2 Composite Functions

A composite function is constructed from other semantic functions through composition operators.

```typescript
type CompositeFunction<I, O, E extends string, Fx extends Effect, Ctx> =
  SemanticFunction<I, O, E, Fx, Ctx> & {
    readonly kind: 'composite'
    readonly constituents: readonly IRI[]
    readonly compositionStrategy: CompositionStrategy
  }

type CompositionStrategy =
  | 'sequential'    // f then g
  | 'parallel'      // f and g independently
  | 'conditional'   // if p then f else g
  | 'iterative'     // f until condition
```

### 4.3 Goal Declarations

A Goal Declaration specifies a desired world state and the conditions under which that state is satisfied. Goal Declarations are NOT executable—they are consumed by planners.

```typescript
type GoalDeclaration<G, S = unknown> = {
  readonly id: IRI
  readonly description: string
  readonly goalState: G
  readonly satisfiedWhen: ConditionSet<S>
  readonly priority?: number
  readonly deadline?: Timestamp
}

type ConditionSet<S> = {
  readonly mode: 'ALL' | 'ANY' | 'WEIGHTED'
  readonly conditions: readonly Condition<S>[]
  readonly weights?: readonly number[]
}
```

#### 4.3.1 Goal vs. Function Distinction

| Aspect | Goal Declaration | Semantic Function |
|--------|------------------|-------------------|
| Nature | Declarative | Computational |
| Execution | Not executable | Executable |
| Output | None | Result + Effects |
| Consumer | Planner/Solver/AI | Runtime |
| Ontology Type | State/Quality | Process |

---

## 5. Preconditions and Failure Modes

### 5.1 Precondition Specification

```typescript
type Precondition<I, Ctx> = Condition<I & Ctx> & {
  readonly enforcement: 'CALLER' | 'FUNCTION' | 'BOTH'
  readonly violationError: IRI
}
```

- **CALLER:** Caller ensures precondition
- **FUNCTION:** Function validates
- **BOTH:** Both validate

### 5.2 Error Category Semantics

| Category | Meaning | Typical Response |
|----------|---------|------------------|
| `PRECONDITION` | Function invoked when invariants did not hold | Fix caller, do not retry |
| `VALIDATION` | Input failed structural or semantic validation | Correct input, may retry |
| `DOMAIN` | Business rule prevented operation | Change approach or data |
| `INTEGRATION` | External system unavailable or failed | Retry with backoff |
| `INVARIANT` | Internal consistency violation (bug) | Alert, investigate |
| `AUTHORIZATION` | Human approval denied or timed out | Re-request or escalate |

---

## 6. Effect Model

### 6.1 Effect Semantics

Effects are first-class values representing intended state changes. A semantic function does not cause state change; it returns descriptions of desired state changes.

#### 6.1.1 Effect Lifecycle

An effect progresses through stages:
1. **Declared** — In signature
2. **Emitted** — In result
3. **Pending** — Awaiting execution
4. **Authorized** — v2.2: Human approval if required
5. **Executed** — Applied to state
6. **Confirmed** — Acknowledged by target

#### 6.1.2 Effect Ordering Semantics

Effect ordering represents intentional sequencing, not causal dependency. Executors MAY reorder effects only if semantic independence is proven.

> **Warning:** Naive executors may attempt to "optimize" by reordering. This is only safe when independence is guaranteed. When in doubt, preserve order.

### 6.2 Effect Accumulation Rules

```typescript
// Sequential: effects(f >>> g) = concat(effects(f), effects(g))
// Parallel:   effects(f &&& g) = concat(effects(f), effects(g))
// Short-circuit: only completed function effects are included
```

### 6.3 Effect Deduplication

Automatic deduplication is NOT performed by the semantic layer. Use `idempotencyKey` for executor-level deduplication.

### 6.4 Effect Authorization Flow (v2.2)

When an effect has authorization requirements, the executor MUST pause and obtain approval before proceeding.

```typescript
// Effect Authorization Flow
//
// 1. Function emits effect with authorization: { level: 'CONFIRM', ... }
// 2. Executor detects authorization requirement
// 3. Executor notifies approval system (human dashboard, Slack, etc.)
// 4. Executor waits for approval or timeout
// 5a. If approved: execute effect, continue
// 5b. If rejected: emit AuthorizationError, halt
// 5c. If timeout: apply fallbackAction (REJECT | QUEUE | ESCALATE)
```

---

## 7. Composition Rules

### 7.1 Result Monad

```typescript
function pure<O, Fx extends Effect>(value: O): SemanticResult<O, never, Fx> {
  return { ok: true, value, effects: [] }
}

function bind<
  A, B,
  E1 extends string, E2 extends string,
  Fx1 extends Effect, Fx2 extends Effect
>(
  result: SemanticResult<A, E1, Fx1>,
  fn: (a: A) => SemanticResult<B, E2, Fx2>
): SemanticResult<B, E1 | E2, Fx1 | Fx2> {
  if (!result.ok) return result
  const next = fn(result.value)
  if (!next.ok) return next
  return {
    ok: true,
    value: next.value,
    effects: [...result.effects, ...next.effects]
  }
}
```

### 7.2 Monad Laws

Implementations MUST satisfy:
- **Left identity:** `bind(pure(a), f) ≡ f(a)`
- **Right identity:** `bind(m, pure) ≡ m`
- **Associativity:** `bind(bind(m, f), g) ≡ bind(m, x => bind(f(x), g))`

### 7.3 Composition Operators

```typescript
// Sequential composition: f >>> g
function seq<A, B, C, E, Fx, Ctx>(
  f: SemanticFunction<A, B, E, Fx, Ctx>,
  g: SemanticFunction<B, C, E, Fx, Ctx>
): SemanticFunction<A, C, E, Fx, Ctx>

// Parallel composition: f &&& g
function par<A, B, C, E, Fx, Ctx>(
  f: SemanticFunction<A, B, E, Fx, Ctx>,
  g: SemanticFunction<A, C, E, Fx, Ctx>
): SemanticFunction<A, [B, C], E, Fx, Ctx>

// Fallback composition: f orElse g
function orElse<I, O, E1, E2, Fx, Ctx>(
  primary: SemanticFunction<I, O, E1, Fx, Ctx>,
  fallback: SemanticFunction<I, O, E2, Fx, Ctx>
): SemanticFunction<I, O, E2, Fx, Ctx>
```

### 7.4 Postcondition Composition (v2.2)

When functions compose, postconditions chain. The composed function's postconditions are the union of constituent postconditions, with output bindings applied sequentially.

```typescript
// For f >>> g:
// - f's SUCCESS postconditions apply after f succeeds
// - g's SUCCESS postconditions apply after g succeeds
// - Final world state reflects both bindings
//
// This enables planners to reason about multi-step transformations
```

---

## 8. Ontology Alignment

### 8.1 Required Ontology Elements

| Element | BFO Type | Description |
|---------|----------|-------------|
| Function | `BFO:0000015` | Process representing computation |
| Input | `BFO:0000031` | Generically dependent continuant |
| Output | `BFO:0000031` | Generically dependent continuant |
| Effect | `BFO:0000015` | Process representing state change |
| Precondition | `BFO:0000019` | Quality inhering in process |
| Postcondition | `BFO:0000019` | Quality guaranteed by process |
| FailureMode | `CCO:ont00000958` | Information content entity |

### 8.2 Alignment Manifest

```typescript
type AlignmentManifest = {
  readonly schemaVersion: '2.2'
  readonly ontologyIRI: IRI
  readonly functions: readonly FunctionAlignment[]
  readonly effects: readonly EffectAlignment[]
  readonly errors: readonly ErrorAlignment[]
  readonly failureModes: readonly FailureModeAlignment[]
  readonly discoveryMetadata: readonly DiscoveryMetadata[]  // v2.2
}

type FunctionAlignment = {
  readonly functionId: IRI
  readonly typescriptPath: string
  readonly typescriptExport: string
  readonly inputAlignment: TypeAlignment
  readonly outputAlignment: TypeAlignment
  readonly postconditionAlignments: readonly PostconditionAlignment[]  // v2.2
  readonly versionConsistency: boolean
}

type PostconditionAlignment = {
  readonly postconditionId: IRI
  readonly guaranteedConditionId: IRI
  readonly scope: PostconditionScope
}
```

### 8.3 Verification Semantics

- **Structural alignment:** Parameters match ontology roles
- **Semantic alignment:** Descriptions match definitions
- **Version consistency:** Versions match across code and ontology
- **Failure mode traceability:** All modes have ontology counterparts

### 8.4 Verification Implementation

```typescript
interface AlignmentVerifier {
  verify(manifest: AlignmentManifest): VerificationResult
  verifyPlan(
    plan: ExecutionPlan,
    goal: GoalDeclaration<unknown>
  ): PlanVerificationResult  // v2.2
}

type VerificationResult = {
  readonly valid: boolean
  readonly violations: readonly AlignmentViolation[]
  readonly warnings: readonly AlignmentWarning[]
}
```

### 8.5 Discovery Metadata (v2.2)

Discovery metadata enables AI agents to find functions using natural language queries. It bridges the gap between human intent and formal IRIs.

> **AI-Ready:** This is how AI agents search for functions. Without discovery metadata, agents cannot map natural language requests to semantic functions.

```typescript
type DiscoveryMetadata = {
  readonly functionId: IRI
  readonly intentLabels: readonly string[]        // Natural language aliases
  readonly bfoDefinition: string                  // Ontology-aligned description
  readonly exampleInvocations: readonly string[]  // 'validate that aaron@example.com is valid'
  readonly semanticDomain: readonly IRI[]         // Which ontology branches this touches
  readonly keywords: readonly string[]            // Search optimization
  readonly relatedFunctions: readonly IRI[]       // Functions often used together
}

// Example: Discovery metadata for email validation
const emailValidationDiscovery: DiscoveryMetadata = {
  functionId: 'urn:sfs:example:validateEmail' as IRI,
  intentLabels: [
    'verify email',
    'check email address',
    'validate email format',
    'is this email valid',
    'email verification'
  ],
  bfoDefinition: 'A validation process that determines whether an email address ' +
                 'conforms to RFC 5322 syntax and produces a normalized form.',
  exampleInvocations: [
    'validate that aaron@example.com is a real email',
    'check if user@domain.org is properly formatted',
    'verify the email address before sending'
  ],
  semanticDomain: [
    'urn:obo:IAO_0000030' as IRI,  // Information content entity
    'urn:sfs:domain:identity' as IRI,
    'urn:sfs:domain:validation' as IRI
  ],
  keywords: ['email', 'validation', 'RFC5322', 'format', 'address'],
  relatedFunctions: [
    'urn:sfs:example:sendEmail' as IRI,
    'urn:sfs:example:normalizeEmail' as IRI
  ]
}
```

#### 8.5.1 Intent Matching

AI agents use discovery metadata to resolve natural language to IRIs. The matching process considers:
- `intentLabels` — Exact and fuzzy match
- `exampleInvocations` — Semantic similarity
- `keywords` — Term frequency
- `semanticDomain` — Ontology navigation

```typescript
// Intent resolution interface
interface IntentResolver {
  resolve(naturalLanguageQuery: string): readonly FunctionMatch[]
}

type FunctionMatch = {
  readonly functionId: IRI
  readonly confidence: number  // 0.0 to 1.0
  readonly matchedOn: 'intentLabel' | 'example' | 'keyword' | 'domain'
  readonly explanation: string
}
```

---

## 9. Metadata Isolation

### 9.1 Isolation Mechanism

Metadata is isolated via Symbol-keyed properties, inaccessible through normal enumeration.

### 9.2 Metadata Access Rules

- Semantic function logic MUST NOT access metadata
- Only infrastructure code MAY access metadata

### 9.3 Metadata Propagation

Implementations SHOULD default to `merge` policy to prevent trace loss.

| Policy | Behavior |
|--------|----------|
| `merge` | Combine traces from both results (RECOMMENDED default) |
| `replace` | Keep only final result metadata |
| `drop` | Discard all metadata at composition boundaries |

---

## 10. Testing Requirements

### 10.1 Required Test Categories

1. Purity
2. Preconditions
3. Postconditions (v2.2)
4. Effects
5. Failure Modes
6. Condition Purity
7. Context Variation
8. Composition
9. Ontology Alignment
10. Authorization Flow (v2.2)

### 10.2 Test Infrastructure

```typescript
interface SFSTestHarness<
  I, O, E extends string,
  Fx extends Effect,
  Ctx extends Context
> {
  assertPure(fn: SemanticFunction<I, O, E, Fx, Ctx>, input: I, ctx: Ctx): void
  assertPreconditionEnforced(fn, input: I, ctx: Ctx, expectedError: E): void
  assertPostconditionHolds(fn, input: I, ctx: Ctx, worldState: unknown): void  // v2.2
  assertEffectsEmitted(fn, input: I, ctx: Ctx, expectedEffects: Fx[]): void
  assertAuthorizationRequired(fn, input: I, ctx: Ctx, effectId: IRI): void  // v2.2
  assertConditionPure<S>(condition: Condition<S>, testStates: S[]): void
  assertAllFailureModesReachable(
    fn,
    testCases: Array<{ input: I; ctx: Ctx; expectedFailureMode: IRI }>
  ): void
}
```

---

## 11. Versioning Rules

SFS artifacts follow Semantic Versioning 2.0.0.

**Breaking (Major):**
- Removing inputs/outputs/effects/postconditions
- Stricter preconditions
- Removing failure modes

**Additions (Minor):**
- Optional inputs
- New outputs/effects/postconditions
- New failure modes
- Relaxing preconditions

**Fixes (Patch):**
- Bug fixes
- Documentation
- Performance

---

## 12. Deployment Constraints

- Semantic functions MUST be deployable in any JavaScript/TypeScript runtime
- All types MUST be JSON-serializable
- Functions MAY be distributed across network boundaries

---

## 13. Visual Mental Model

```
+-------------------------------------------------------------+
|                    SEMANTIC BOUNDARY                        |
|  +-----------+     +------------------+                     |
|  |   Input   |---->|                  |                     |
|  +-----------+     |    Semantic      |     +--------+      |
|  +-----------+     |    Function      |---->| Result |      |
|  |  Context  |---->|                  |     +--------+      |
|  +-----------+     |  (Pure, Det.)    |     +--------+      |
|  +-----------+     |                  |---->|Effects |      |
|  |Agent ID   |---->| Pre -> Post      |     +--------+      |
|  +-----------+     +------------------+          |          |
|                             |                    v          |
|                       +----------+      +--------------+    |
|                       |  Error   |      | Auth Gate?   |    |
|                       +----------+      +--------------+    |
+-------------------------------------------------------------+
           NO ARROWS EXIT THE BOUNDARY (until authorized)
```

---

## 14. Conformance Levels

### 14.1 Full Conformance

- All functions pure and deterministic
- All condition predicates satisfy purity
- All goals declarative
- All context explicit and read-only
- All functions have pre/postconditions
- All failure modes identified and traceable
- Ontology parity verifiable
- Composition satisfies monad laws
- Metadata isolated
- Authorization gates enforced
- All tests pass

### 14.2 Partial Conformance

Satisfies normative principles but lacks full verification infrastructure. MUST be explicitly declared.

### 14.3 Non-Conformance

Violates any normative principle. MUST NOT claim SFS compatibility.

---

## 15. Agent Integration (v2.2)

This section defines the types and interfaces required for AI agents to participate in the SFS ecosystem. Agents are first-class citizens that must honor the same semantic constraints as human developers.

> **AI-Ready:** This section is the core of AI-readiness. It defines how agents identify themselves, construct plans, and accept accountability.

### 15.1 Agent Identity

Every caller—human or AI—has an identity. Agent identity enables traceability and accountability.

```typescript
type AgentIdentity = {
  readonly agentId: string
  readonly agentType: AgentType
  readonly modelId?: string           // e.g., 'claude-3-opus-20240229'
  readonly sessionId: string
  readonly capabilities: readonly AgentCapability[]
  readonly delegationChain?: readonly AgentIdentity[]  // Who authorized this agent?
}

type AgentType =
  | 'HUMAN'           // Human developer or operator
  | 'AI_MODEL'        // Autonomous AI model
  | 'AUTOMATED'       // Non-AI automation (scripts, cron)
  | 'HYBRID'          // Human-AI collaboration

type AgentCapability =
  | 'DISCOVER'        // Can search for functions
  | 'PLAN'            // Can construct execution plans
  | 'EXECUTE'         // Can trigger function execution
  | 'APPROVE'         // Can approve authorization requests
  | 'DELEGATE'        // Can authorize other agents
```

#### 15.1.1 Delegation Chains

When an AI agent operates on behalf of a human, the delegation chain records the authorization path. This enables audit: "Who authorized this AI to perform this action?"

```typescript
// Example: AI agent operating under human delegation
const aiAgent: AgentIdentity = {
  agentId: 'agent-claude-001',
  agentType: 'AI_MODEL',
  modelId: 'claude-3-opus-20240229',
  sessionId: 'session-abc123',
  capabilities: ['DISCOVER', 'PLAN', 'EXECUTE'],
  delegationChain: [
    {
      agentId: 'user-aaron',
      agentType: 'HUMAN',
      sessionId: 'session-xyz789',
      capabilities: ['DISCOVER', 'PLAN', 'EXECUTE', 'APPROVE', 'DELEGATE']
    }
  ]
}
```

### 15.2 Execution Plans

An Execution Plan is a sequence of semantic function invocations designed to achieve a goal. Plans are constructed by planners (AI or algorithmic) and verified before execution.

```typescript
type ExecutionPlan = {
  readonly planId: IRI
  readonly goalRef: IRI
  readonly steps: readonly PlannedStep[]
  readonly assumptions: readonly WorldStateAssertion[]
  readonly estimatedEffects: readonly IRI[]
  readonly requiredAuthorizations: readonly AuthorizationRequirement[]
}

type PlannedStep = {
  readonly stepNumber: number
  readonly functionId: IRI
  readonly functionVersion: Version
  readonly inputMapping: InputMapping
  readonly expectedPreconditions: readonly IRI[]
  readonly expectedPostconditions: readonly IRI[]
  readonly dependsOn: readonly number[]  // Prior step numbers
}

type InputMapping = {
  readonly source: 'LITERAL' | 'PRIOR_OUTPUT' | 'WORLD_STATE' | 'USER_INPUT'
  readonly value?: unknown
  readonly stepRef?: number
  readonly path?: readonly string[]
}

type WorldStateAssertion = {
  readonly conditionId: IRI
  readonly assumedValue: boolean
  readonly justification: string
}

type AuthorizationRequirement = {
  readonly stepNumber: number
  readonly effectId: IRI
  readonly level: AuthorizationLevel
}
```

### 15.3 Plan Handshake

The Plan Handshake is the accountability record. It captures who generated a plan, when, with what assumptions, and what verification was performed.

```typescript
type PlanHandshake = {
  readonly handshakeId: IRI
  readonly planId: IRI
  readonly generatedBy: AgentIdentity
  readonly generatedAt: Timestamp
  readonly goalRef: IRI
  readonly goalDescription: string
  readonly functionVersionSnapshot: ReadonlyMap<IRI, Version>
  readonly verificationStatus: VerificationStatus
  readonly verificationResult?: PlanVerificationResult
  readonly executionStatus: ExecutionStatus
  readonly executionResult?: ExecutionResult
}

type VerificationStatus =
  | 'UNVERIFIED'
  | 'VERIFIED'
  | 'REJECTED'
  | 'VERIFICATION_FAILED'

type ExecutionStatus =
  | 'PENDING'
  | 'IN_PROGRESS'
  | 'AWAITING_AUTHORIZATION'
  | 'COMPLETED'
  | 'FAILED'
  | 'ABORTED'
```

### 15.4 Plan Verification

Plan verification proves that an execution plan, if executed successfully, will satisfy its goal. This is the bridge between AI-generated plans and semantic correctness.

```typescript
interface PlanVerifier {
  verifyPlan(
    plan: ExecutionPlan,
    goal: GoalDeclaration<unknown>,
    currentWorldState: WorldState
  ): PlanVerificationResult
}

type PlanVerificationResult = {
  readonly valid: boolean
  readonly satisfiesGoal: boolean
  readonly preconditionAnalysis: readonly PreconditionAnalysis[]
  readonly postconditionChain: readonly PostconditionChainLink[]
  readonly unsatisfiedConditions: readonly UnsatisfiedCondition[]
  readonly warnings: readonly PlanWarning[]
  readonly proof?: FormalProof
}

type PreconditionAnalysis = {
  readonly stepNumber: number
  readonly functionId: IRI
  readonly preconditionId: IRI
  readonly satisfiedBy: 'WORLD_STATE' | 'PRIOR_POSTCONDITION' | 'ASSUMPTION'
  readonly satisfyingSource?: number | IRI
}

type PostconditionChainLink = {
  readonly stepNumber: number
  readonly postconditionId: IRI
  readonly guarantees: IRI
  readonly enablesSteps: readonly number[]
}

type UnsatisfiedCondition = {
  readonly stepNumber: number
  readonly conditionId: IRI
  readonly reason: string
}

type PlanWarning = {
  readonly kind: 'ASSUMPTION_RISK' | 'VERSION_DRIFT' | 'AUTHORIZATION_BOTTLENECK'
  readonly message: string
  readonly stepNumber?: number
}
```

The verification algorithm works as follows:

1. Initialize world state from current state + assumptions
2. For each step in order:
   - Check preconditions against world state
   - If satisfied: apply postcondition bindings to world state
   - If not satisfied: record unsatisfied condition
3. After all steps: check goal conditions against final world state
4. Return result with full analysis chain

### 15.5 World State

World State is the abstract representation of relevant state that conditions evaluate against.

```typescript
type WorldState = {
  readonly stateId: IRI
  readonly timestamp: Timestamp
  readonly assertions: ReadonlyMap<IRI, boolean>  // Condition IRI -> truth value
  readonly entities: ReadonlyMap<IRI, unknown>    // Entity IRI -> value
}

// World state evolution during plan execution
function applyPostcondition<O, S>(
  worldState: WorldState,
  postcondition: Postcondition<O, S>,
  output: O
): WorldState {
  // Apply output binding to update world state
  // Mark guaranteed condition as true
  // Return new immutable world state
}
```

---

## 16. Human-AI Collaboration (v2.2)

This section defines the protocols for safe human-AI collaboration within the SFS ecosystem.

### 16.1 Authorization Enforcement

Authorization enforcement is mandatory. Effect executors MUST check authorization requirements and pause for human approval when required.

```typescript
interface AuthorizationEnforcer {
  checkAuthorization(
    effect: Effect<unknown>,
    requestingAgent: AgentIdentity
  ): AuthorizationCheckResult

  requestApproval(
    effect: Effect<unknown>,
    requestingAgent: AgentIdentity,
    approvers: readonly AgentIdentity[]
  ): Promise<ApprovalResult>
}

type AuthorizationCheckResult =
  | { authorized: true }
  | { authorized: false; reason: 'REQUIRES_APPROVAL'; level: AuthorizationLevel }
  | { authorized: false; reason: 'INSUFFICIENT_CAPABILITY' }
  | { authorized: false; reason: 'DELEGATION_CHAIN_INVALID' }

type ApprovalResult =
  | { approved: true; approvedBy: readonly AgentIdentity[]; timestamp: Timestamp }
  | { approved: false; reason: 'REJECTED'; rejectedBy: AgentIdentity }
  | { approved: false; reason: 'TIMEOUT' }
  | { approved: false; reason: 'INSUFFICIENT_APPROVERS' }
```

### 16.2 Audit Requirements

All AI agent actions MUST be auditable. Implementations MUST record:

- Agent identity for every function invocation
- Full delegation chain at time of invocation
- Plan handshake ID linking invocation to plan
- Authorization decisions and approver identities
- World state snapshots at key decision points

```typescript
type AuditRecord = {
  readonly recordId: IRI
  readonly timestamp: Timestamp
  readonly eventType: AuditEventType
  readonly agent: AgentIdentity
  readonly planHandshakeId?: IRI
  readonly functionId?: IRI
  readonly effectId?: IRI
  readonly authorizationDecision?: AuthorizationCheckResult
  readonly worldStateSnapshot?: IRI
  readonly outcome: 'SUCCESS' | 'FAILURE' | 'PENDING'
  readonly details: Record<string, unknown>
}

type AuditEventType =
  | 'PLAN_GENERATED'
  | 'PLAN_VERIFIED'
  | 'PLAN_REJECTED'
  | 'FUNCTION_INVOKED'
  | 'EFFECT_EMITTED'
  | 'AUTHORIZATION_REQUESTED'
  | 'AUTHORIZATION_GRANTED'
  | 'AUTHORIZATION_DENIED'
  | 'EXECUTION_COMPLETED'
  | 'EXECUTION_FAILED'
```

### 16.3 Safety Principles

The following safety principles govern human-AI collaboration:

1. **Semantic Boundary Integrity:** AI agents cannot bypass the semantic boundary. Effects remain descriptors until authorized and executed.

2. **Human Override:** Humans with `APPROVE` capability can halt any AI-initiated action at any authorization gate.

3. **Delegation Accountability:** AI agents inherit restrictions from their delegation chain. An AI cannot authorize itself to do what its delegator cannot do.

4. **Verification Before Execution:** Plans SHOULD be verified before execution. Unverified plans MUST be flagged.

5. **Audit Completeness:** Every AI action must be traceable to a human authorization decision.

---

## Appendix A: Complete Type Definitions

Consolidated v2.2 type definitions for reference implementation.

```typescript
// === SFS v2.2 Complete Type Definitions ===

// --- Foundational ---
type IRI = string & { readonly __brand: 'IRI' }
type Timestamp = { readonly iso8601: string; readonly epochMs: number }
type Version = {
  readonly major: number
  readonly minor: number
  readonly patch: number
  readonly prerelease?: string
}
type Duration = { readonly milliseconds: number; readonly iso8601?: string }

// --- Context ---
type Context<T extends Record<string, unknown> = Record<string, never>> =
  { readonly [K in keyof T]: T[K] } & { readonly __contextBrand: unique symbol }
type EmptyContext = Context<Record<string, never>>
type VersionedContext<T extends Record<string, unknown>> = Context<T> & {
  readonly __contextSchemaVersion: Version
  readonly __contextSchemaIRI?: IRI
}

// --- Conditions ---
type LogicalOperator = 'AND' | 'OR' | 'NOT' | 'IMPLIES' | 'IFF'
type ConditionPredicate<S> =
  | { kind: 'expression'; evaluate: (state: S) => boolean }
  | { kind: 'reference'; conditionId: IRI }
  | { kind: 'composite'; operator: LogicalOperator; operands: Condition<S>[] }
type Condition<S = unknown> = {
  readonly id: IRI
  readonly description: string
  readonly predicate: ConditionPredicate<S>
  readonly negation?: Condition<S>
}

// --- Effects ---
type EffectKind =
  | 'CREATE' | 'UPDATE' | 'DELETE'
  | 'EMIT' | 'NOTIFY' | 'SCHEDULE' | 'CANCEL' | 'CUSTOM'
type EffectTarget = {
  readonly system: string
  readonly resource: string
  readonly identifier?: string
}
type AuthorizationLevel = 'AUTO' | 'NOTIFY' | 'CONFIRM' | 'MULTI_PARTY'
type EffectAuthorization = {
  readonly level: AuthorizationLevel
  readonly reason?: string
  readonly requiredRoles?: readonly string[]
  readonly timeout?: Duration
  readonly fallbackAction?: 'REJECT' | 'QUEUE' | 'ESCALATE'
}
type Effect<T = unknown> = {
  readonly id: IRI
  readonly kind: EffectKind
  readonly target: EffectTarget
  readonly payload: T
  readonly timestamp: Timestamp
  readonly idempotencyKey?: string
  readonly authorization?: EffectAuthorization
}
type EffectList<Fx> = readonly Fx[]
type NoEffect = never

// --- Errors ---
type ErrorCategory =
  | 'PRECONDITION' | 'VALIDATION' | 'DOMAIN'
  | 'INTEGRATION' | 'INVARIANT' | 'AUTHORIZATION'
type DomainError<E extends string = string> = {
  readonly code: E
  readonly message: string
  readonly category: ErrorCategory
  readonly recoverable: boolean
  readonly ontologyRef: IRI
  readonly failureModeId?: IRI
}

// --- Postconditions (v2.2) ---
type PostconditionScope = 'SUCCESS' | 'FAILURE' | 'ALWAYS'
type OutputBinding<O, S> = {
  readonly description: string
  readonly bind: (output: O, priorState: S) => S
}
type Postcondition<O, S = unknown> = {
  readonly id: IRI
  readonly description: string
  readonly appliesWhen: PostconditionScope
  readonly guarantees: Condition<S>
  readonly outputBinding?: OutputBinding<O, S>
}

// --- Failure Modes ---
type Mitigation = {
  readonly strategy: 'RETRY' | 'FALLBACK' | 'ESCALATE' | 'COMPENSATE'
  readonly description: string
  readonly automatable: boolean
}
type FailureMode<E extends string> = {
  readonly id: IRI
  readonly error: DomainError<E>
  readonly triggerCondition: Condition<unknown>
  readonly mitigations: readonly Mitigation[]
}

// --- Results ---
declare const MetaSymbol: unique symbol
type MetaContainer = {
  readonly [MetaSymbol]: {
    readonly trace?: readonly string[]
    readonly timing?: { startMs: number; endMs: number }
    readonly debug?: Record<string, unknown>
    readonly agentTrace?: readonly AgentIdentity[]
  }
}
type SuccessResult<O, Fx> = {
  readonly ok: true
  readonly value: O
  readonly effects: EffectList<Fx>
} & Partial<MetaContainer>
type FailureResult<E extends string> = {
  readonly ok: false
  readonly error: DomainError<E>
} & Partial<MetaContainer>
type SemanticResult<O, E extends string, Fx> =
  | SuccessResult<O, Fx>
  | FailureResult<E>

// --- Semantic Function (v2.2 revised) ---
type SemanticFunction<
  I, O, E extends string,
  Fx extends Effect,
  Ctx extends Context = EmptyContext
> = {
  readonly id: IRI
  readonly version: Version
  readonly preconditions: readonly Condition<I & Ctx>[]
  readonly postconditions: readonly Postcondition<O>[]  // v2.2
  readonly failureModes: readonly FailureMode<E>[]
  readonly effectTypes: readonly IRI[]
  readonly execute: (input: I, context: Ctx) => SemanticResult<O, E, Fx>
}

// --- Goals ---
type ConditionSet<S> = {
  readonly mode: 'ALL' | 'ANY' | 'WEIGHTED'
  readonly conditions: readonly Condition<S>[]
  readonly weights?: readonly number[]
}
type GoalDeclaration<G, S = unknown> = {
  readonly id: IRI
  readonly description: string
  readonly goalState: G
  readonly satisfiedWhen: ConditionSet<S>
  readonly priority?: number
  readonly deadline?: Timestamp
}

// --- Agent Integration (v2.2) ---
type AgentType = 'HUMAN' | 'AI_MODEL' | 'AUTOMATED' | 'HYBRID'
type AgentCapability = 'DISCOVER' | 'PLAN' | 'EXECUTE' | 'APPROVE' | 'DELEGATE'
type AgentIdentity = {
  readonly agentId: string
  readonly agentType: AgentType
  readonly modelId?: string
  readonly sessionId: string
  readonly capabilities: readonly AgentCapability[]
  readonly delegationChain?: readonly AgentIdentity[]
}

// --- Discovery Metadata (v2.2) ---
type DiscoveryMetadata = {
  readonly functionId: IRI
  readonly intentLabels: readonly string[]
  readonly bfoDefinition: string
  readonly exampleInvocations: readonly string[]
  readonly semanticDomain: readonly IRI[]
  readonly keywords: readonly string[]
  readonly relatedFunctions: readonly IRI[]
}

// --- Execution Plans (v2.2) ---
type InputMapping = {
  readonly source: 'LITERAL' | 'PRIOR_OUTPUT' | 'WORLD_STATE' | 'USER_INPUT'
  readonly value?: unknown
  readonly stepRef?: number
  readonly path?: readonly string[]
}
type PlannedStep = {
  readonly stepNumber: number
  readonly functionId: IRI
  readonly functionVersion: Version
  readonly inputMapping: InputMapping
  readonly expectedPreconditions: readonly IRI[]
  readonly expectedPostconditions: readonly IRI[]
  readonly dependsOn: readonly number[]
}
type WorldStateAssertion = {
  readonly conditionId: IRI
  readonly assumedValue: boolean
  readonly justification: string
}
type AuthorizationRequirement = {
  readonly stepNumber: number
  readonly effectId: IRI
  readonly level: AuthorizationLevel
}
type ExecutionPlan = {
  readonly planId: IRI
  readonly goalRef: IRI
  readonly steps: readonly PlannedStep[]
  readonly assumptions: readonly WorldStateAssertion[]
  readonly estimatedEffects: readonly IRI[]
  readonly requiredAuthorizations: readonly AuthorizationRequirement[]
}

// --- Plan Handshake (v2.2) ---
type VerificationStatus =
  | 'UNVERIFIED' | 'VERIFIED' | 'REJECTED' | 'VERIFICATION_FAILED'
type ExecutionStatus =
  | 'PENDING' | 'IN_PROGRESS' | 'AWAITING_AUTHORIZATION'
  | 'COMPLETED' | 'FAILED' | 'ABORTED'
type PlanHandshake = {
  readonly handshakeId: IRI
  readonly planId: IRI
  readonly generatedBy: AgentIdentity
  readonly generatedAt: Timestamp
  readonly goalRef: IRI
  readonly goalDescription: string
  readonly functionVersionSnapshot: ReadonlyMap<IRI, Version>
  readonly verificationStatus: VerificationStatus
  readonly verificationResult?: PlanVerificationResult
  readonly executionStatus: ExecutionStatus
  readonly executionResult?: ExecutionResult
}
```

---

## Appendix B: Future Directions

The following features are planned for v3.0 (Agent Architecture):

### B.1 v3.0 Planned Features

1. **Full PlanVerifier Implementation:** Mathematical proof generation for plan correctness
2. **Postcondition Enforcement:** Runtime validation that postconditions actually hold after execution
3. **WorldState Service:** Standardized interface for world state queries and updates
4. **Intent Resolution Service:** Reference implementation of AI function discovery
5. **Authorization Workflow Engine:** Complete HITL workflow management
6. **Audit Service:** Standardized audit record storage and query interface

### B.2 Implementation Milestones

| Milestone | Deliverable |
|-----------|-------------|
| 1 | Minimal reference runtime with effect executor and alignment verifier |
| 2 | Real application slice (auth, validation, deferred submission) |
| 3 | Planner interface that consumes Goal Declarations |
| 4 | Full plan verification with formal proofs |
| 5 | Production-ready AI agent integration |

---

## Closing Statement

SFS v2.2 transforms the Semantic Function Schema from a pure computational specification into a foundation for human-AI collaboration. By adding postconditions, discovery metadata, plan handshakes, and authorization gates, this specification enables AI agents to participate as first-class citizens in the semantic ecosystem.

The core principle remains: **AI agents are not special.** They must honor the same semantic constraints as human developers. They gain no magical privileges—only better tooling for discovery, composition, and verification. The semantic boundary remains inviolable.

What changes is accountability. Every AI action is now traceable through delegation chains, plan handshakes, and audit records. Every destructive effect can require human approval. Every plan can be mathematically verified before execution.

This is the architecture for a world where AI and humans collaborate safely: shared semantics, explicit constraints, verifiable reasoning, and human oversight where it matters.

The path from here: implement the runtime, build a real application, and prove this works. At that point, SFS stops being a specification and becomes the way things are built.

---

*Build well. Build safely. Build together.*
