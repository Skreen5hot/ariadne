# Distributed Semantic Function Commons (DSFC)

**Version:** 1.2

**Status:** Draft Specification

**Audience:** Semantic engineers, ontology engineers, public digital infrastructure architects, policy technologists, social justice technologists

**Depends on:**

* Semantic Function Schema (SFS) v2.2
* APQC Process Classification Framework (PCF)
* BFO / CCO

---

## Changelog: v1.1 → v1.2

Version 1.2 incorporates refinements addressing gaps in decentralized authority, refusal accountability, registry transparency, and community governance. Key changes:

| Section | Change |
|---------|--------|
| §2.3 | Added Ontology Lineage as basis for decentralized alignment |
| §5.2 | Revised APQC mapping to target Goal Declarations, not functions directly |
| §6.3 | Added Registry Transparency Requirements with enforcement mechanisms |
| §7.4 | Strengthened RefusalEvent with required ontology grounding and categories |
| §8.3 | NEW: Community Governance Artifacts specification |
| §10 | Added Orchestrator/Planner conformance level |
| §13 | NEW: SFS v2.2 Integration Matrix |
| Appendix A | NEW: Threat Model |
| Appendix B | NEW: Refusal Reason Ontology (Reference) |

---

## 1. Purpose and Vision

The **Distributed Semantic Function Commons (DSFC)** is a public, open, and decentralized infrastructure for publishing, distributing, composing, and executing *pure semantic functions* as shared civic knowledge.

DSFC treats computational logic as **inspectable public reasoning**, not proprietary services. Its goals are:

* **Transparency:** All decision logic is visible, inspectable, and auditable.
* **Access:** Functions may be fetched and executed without centralized permission.
* **Justice:** Power over logic is decentralized; coercive or opaque automation is structurally discouraged.
* **Resilience:** No single institution controls execution, distribution, or semantic authority.

DSFC builds directly on **Semantic Function Schema (SFS) v2.2** for execution semantics, **APQC PCF** for shared process semantics, and **BFO/CCO** for ontological grounding.

### 1.1 Relationship to SFS

SFS defines *how* semantic functions work: purity, determinism, explicit effects, postconditions, and agent integration. DSFC defines *how semantic functions are shared*: distribution, discovery, execution rights, refusal, and community governance.

SFS is the execution contract. DSFC is the social contract.

---

## 2. Core Principles (Normative)

These principles are NORMATIVE. Any DSFC implementation that violates these principles is non-conformant.

### 2.1 Purity and Determinism

All executable artifacts in the commons MUST be valid SFS v2.2 semantic functions: pure, deterministic, side-effect-free, and explicitly effect-declaring.

### 2.2 Semantic Transparency

Every function MUST be semantically grounded in an ontology and accompanied by:

* Explicit preconditions
* Explicit postconditions
* Explicit effects
* Declared failure modes
* Discovery metadata

No hidden control flow, probabilistic reasoning, or ambient state is permitted.

### 2.3 Decentralized Authority

No registry, mirror, or execution environment may be considered authoritative. Authority derives solely from:

* **Cryptographic integrity** — Content addressing ensures artifact identity
* **Ontological alignment** — Artifacts declare their ontology lineage explicitly
* **Open verification** — Anyone can verify alignment claims

#### 2.3.1 Ontology Lineage (v1.2)

In a decentralized system, "the ontology" does not exist. Multiple communities may fork, extend, or diverge ontologies. Functions do not align to an abstract ontology—they align to a specific **Ontology Lineage**.

```typescript
type OntologyLineage = {
  readonly lineageId: IRI
  readonly rootOntologyIRI: IRI
  readonly versionCID: CID                    // Content-addressed ontology version
  readonly parentLineage?: OntologyLineage    // Fork source, if any
  readonly divergencePoint?: Timestamp        // When fork occurred
  readonly maintainerCommunity?: IRI          // Community responsible for this lineage
}
```

**Lineage Rules:**

1. Every semantic function MUST declare its ontology lineage, not just an ontology IRI.
2. Cross-lineage composition requires an explicit **Ontology Bridge Artifact** that maps terms between lineages.
3. Lineage forks MUST preserve the parent lineage reference for provenance.
4. Verification tools MUST check that function terms exist in the declared lineage version.

```typescript
type OntologyBridge = {
  readonly bridgeId: IRI
  readonly sourceLineage: OntologyLineage
  readonly targetLineage: OntologyLineage
  readonly termMappings: ReadonlyMap<IRI, IRI>  // Source term → Target term
  readonly semanticLoss: readonly SemanticLossDeclaration[]
  readonly bidirectional: boolean
}

type SemanticLossDeclaration = {
  readonly sourceTerm: IRI
  readonly lossType: 'NARROWING' | 'BROADENING' | 'APPROXIMATE' | 'UNMAPPABLE'
  readonly explanation: string
}
```

### 2.4 Right to Fork

Any published semantic function MAY be forked, re-versioned, or re-aligned by downstream communities, provided:

* Identifiers are changed (new IRI)
* Provenance is preserved (reference to source)
* Ontology lineage is declared

Forking is a feature, not a failure. It enables communities to adapt shared reasoning to local contexts without capturing the original.

### 2.5 Agent Neutrality

Following SFS v2.2 §2.7, DSFC makes no distinction between human and AI agents at the semantic layer. All agents—human developers, automated systems, AI models—are subject to the same constraints, entitled to the same transparency, and accountable through the same mechanisms.

---

## 3. Architectural Overview

DSFC is composed of five conceptual layers:

```
┌─────────────────────────────────────────────────────────────┐
│  5. Community Governance                                    │
│     Policies, authorization levels, refusal norms           │
├─────────────────────────────────────────────────────────────┤
│  4. Orchestration and Planning                              │
│     Goal satisfaction, plan construction, verification      │
├─────────────────────────────────────────────────────────────┤
│  3. Execution Environments                                  │
│     Local-first execution, effect interpretation, refusal   │
├─────────────────────────────────────────────────────────────┤
│  2. Registries and Discovery                                │
│     Non-authoritative indices, multi-source queries         │
├─────────────────────────────────────────────────────────────┤
│  1. Content-Addressed Storage                               │
│     Immutable artifacts, CID-based integrity                │
└─────────────────────────────────────────────────────────────┘
```

Each layer is independently replaceable and non-authoritative. Loss of any single component at any layer MUST NOT compromise the integrity of artifacts or the correctness of execution.

---

## 4. Semantic Artifacts

### 4.1 Semantic Functions

A **Semantic Function** in DSFC is a conformant SFS v2.2 artifact with:

* A stable IRI
* Semantic versioning
* Ontology lineage declaration
* Alignment manifest (content-addressed)
* Discovery metadata
* Zero runtime side effects

Semantic functions MAY be:

* **Primitive** (atomic computation)
* **Composite** (constructed from other semantic functions)

### 4.2 Goal Declarations

Goals are declarative artifacts that express desired world states. Goals use the SFS v2.2 `GoalDeclaration` type:

```typescript
type GoalDeclaration<G, S = unknown> = {
  readonly id: IRI
  readonly description: string
  readonly goalState: G
  readonly satisfiedWhen: ConditionSet<S>
  readonly priority?: number
  readonly deadline?: Timestamp
}
```

Goals:

* Are NOT executable
* Are consumed by planners or orchestration systems
* Reference semantic conditions from declared ontology lineage
* MAY be APQC-aligned (see §5)

### 4.3 Artifact Bundles

A complete DSFC artifact bundle includes:

| Component | Required | Content-Addressed |
|-----------|----------|-------------------|
| Function implementation | Yes | Yes |
| Alignment manifest | Yes | Yes |
| Ontology lineage declaration | Yes | Yes |
| Discovery metadata | Yes | Yes |
| Test vectors | RECOMMENDED | Yes |
| Provenance record | If forked | Yes |

All components MUST be independently verifiable by CID.

---

## 5. APQC Integration Model

### 5.1 Role of APQC

APQC PCF serves as a **semantic reference taxonomy** for business processes, not an execution model.

APQC elements:

* Define *what kind* of process outcome is desired
* Provide shared vocabulary across organizations
* Enable cross-domain comparability

APQC elements DO NOT:

* Define control flow
* Define execution order
* Specify implementation

### 5.2 Mapping Rules (Revised in v1.2)

APQC process categories map to **Goal Declarations**, not directly to functions. This reflects the reality that multiple functions (or function compositions) may achieve the same process outcome.

```
APQC Category                    DSFC Mapping
─────────────────────────────    ────────────────────────────
APQC 2.2.3 Develop Pricing       → GoalDeclaration
Strategy                            id: urn:dsfc:goals:apqc:2.2.3
                                    satisfiedWhen: { pricing strategy exists,
                                                    approved by stakeholders }
                                    
                                 → Function Registry Query
                                    "functions whose postconditions 
                                     can satisfy this goal"
```

**Mapping artifacts:**

```typescript
type APQCGoalMapping = {
  readonly apqcCode: string                    // e.g., "2.2.3"
  readonly apqcDescription: string
  readonly goalDeclaration: GoalDeclaration<unknown>
  readonly suggestedFunctions: readonly IRI[]  // Functions known to satisfy
  readonly ontologyLineage: OntologyLineage
}
```

### 5.3 Planner Integration

DSFC planners use APQC-mapped goals as inputs:

1. Accept APQC code or GoalDeclaration
2. Query registries for functions with matching postconditions
3. Construct execution plan using SFS v2.2 `ExecutionPlan` type
4. Verify plan satisfies goal via `PlanVerifier`
5. Execute with community-appropriate authorization levels

---

## 6. Distribution Model

### 6.1 Content-Addressed Semantic Artifacts

All DSFC artifacts MUST be distributed as immutable, content-addressed units.

Artifact identity consists of:

* **Logical IRI** — Human-meaningful identifier
* **Content Identifier (CID)** — Cryptographic hash of content

The CID is the authoritative integrity reference. The IRI is a convenience alias.

```typescript
type ArtifactReference = {
  readonly iri: IRI           // urn:dsfc:functions:validateEmail
  readonly cid: CID           // bafybeigdyrzt5sfp7udm7hu76uh7y26nf3...
  readonly version: Version
}
```

### 6.2 Content-Addressed Alignment Manifests

Alignment Manifests (SFS v2.2 §8.2) MUST themselves be content-addressed artifacts.

Manifests MUST:

* Reference ontology entities by IRI within declared lineage
* Reference code artifacts by CID
* Be immutable once published

This prevents the **semantic reassignment attack** where published function code is given new meaning by updating its manifest.

### 6.3 Registry Transparency Requirements (v1.2)

Registries serve as discovery indices only. They MUST NOT claim semantic authority.

#### 6.3.1 Registry Obligations

Registries MUST:

1. **Publish inclusion criteria** — What artifacts are accepted and why
2. **Publish exclusion criteria** — What artifacts are rejected and why
3. **Maintain audit logs** — All additions, removals, and modifications with timestamps
4. **Support CID queries** — Lookup by content identifier, not just IRI
5. **Declare their governance** — Who controls the registry and how decisions are made
6. **Federate willingly** — Respond to cross-registry synchronization requests

Registries MUST NOT:

1. Rewrite artifact content
2. Substitute alignment manifests
3. Imply semantic authority over indexed artifacts
4. Require exclusive listing agreements
5. Silently filter query results

#### 6.3.2 Client Obligations

Clients (executors, planners, developers) SHOULD:

1. **Query multiple registries** — Do not depend on single source
2. **Detect divergence** — Alert when registries return different CIDs for same IRI
3. **Verify independently** — Check CID integrity regardless of registry trust
4. **Cache locally** — Maintain local copies of critical artifacts

#### 6.3.3 Registry Transparency Artifact

Registries MUST publish a machine-readable transparency artifact:

```typescript
type RegistryTransparency = {
  readonly registryId: IRI
  readonly governingCommunity: IRI
  readonly inclusionPolicy: PolicyDocument
  readonly exclusionPolicy: PolicyDocument
  readonly auditLogCID: CID               // Content-addressed audit log
  readonly lastUpdated: Timestamp
  readonly federationPeers: readonly IRI[]
  readonly contactMethod: string
}

type PolicyDocument = {
  readonly policyCID: CID
  readonly humanReadableURL: string
  readonly effectiveDate: Timestamp
}
```

### 6.4 CDNs as Optional Accelerators

CDNs MAY cache artifacts but MUST NOT:

* Override integrity checks
* Act as identity providers
* Enforce access policy beyond caching

Loss of CDN access MUST NOT impact semantic correctness—only performance.

---

## 7. Execution Model

### 7.1 Local-First Semantic Execution

Semantic functions are fetched and executed locally by:

* Browsers
* Edge runtimes
* Servers
* Offline systems
* AI agents

**Execution requires only:**

* Function artifact (verified by CID)
* Input data
* Context (including AgentIdentity)

**Execution prohibits:**

* Network access during computation
* Registry consultation during computation
* Authority signals affecting computation

The semantic boundary is inviolable. What happens inside is determined solely by input, context, and the function's declared logic.

> **Clarification (v1.2):** *Fetching* an artifact may require network access. *Executing* it must not. Once an artifact is locally available and verified, execution is fully offline-capable.

### 7.2 Effect Lifecycle and Executor Agency

Effects emitted by functions are *descriptive intent*, not commands.

```
Function executes    →    Effects emitted    →    Executor interprets
(deterministic)           (data)                  (policy, law, ethics)
```

Executors have full agency over effect interpretation. They may:

* Execute effects immediately
* Queue effects for later
* Request human authorization (per SFS v2.2 EffectAuthorization)
* Refuse effects entirely

### 7.3 Executor Right of Refusal (Normative)

An executor MAY refuse to enact an effect even if the semantic function executed successfully.

**Refusal MUST NOT:**

* Modify the semantic result
* Retroactively change function meaning
* Be hidden or silent

**Refusal MUST:**

* Be explicit
* Be recorded as a RefusalEvent
* Be semantically classifiable
* Reference a reason from the Refusal Reason Ontology

### 7.4 RefusalEvent Specification (Revised in v1.2)

Effect refusal is modeled as a first-class semantic artifact with required ontological grounding.

```typescript
type RefusalEvent = {
  readonly id: IRI
  readonly timestamp: Timestamp
  readonly effectRef: IRI                      // The refused effect
  readonly effectCID: CID                      // Integrity proof
  readonly executorIdentity: AgentIdentity     // From SFS v2.2
  readonly reasonCategory: RefusalCategory     // REQUIRED
  readonly reasonOntologyRef: IRI              // REQUIRED - specific reason code
  readonly justification?: string              // Human-readable explanation
  readonly communityPolicy?: IRI               // Policy that mandated refusal
  readonly appealable: boolean
  readonly appealDeadline?: Timestamp
  readonly relatedRefusals?: readonly IRI[]    // Coordinated refusal detection
}

type RefusalCategory =
  | 'POLICY'       // Local or community policy prohibits
  | 'LEGAL'        // Jurisdiction prohibits
  | 'ETHICAL'      // Executor conscience objection
  | 'TECHNICAL'    // Cannot execute (resources, access, capability)
  | 'INTEGRITY'    // Artifact verification failed
  | 'COMMUNITY'    // Community norm or governance decision
  | 'AUTHORIZATION'// Required human approval not granted
```

**Refusal Recording:**

RefusalEvents MUST be recorded. Recording options:

1. **Local audit log** — Minimum requirement
2. **Community audit log** — If community membership claimed
3. **Public refusal registry** — For transparency-maximizing executors

RefusalEvents MAY be emitted as effects of kind `EMIT` targeting an audit system.

### 7.5 Coordinated Refusal Detection

To prevent silent executor collusion (see Threat Model, Appendix A), refusal monitoring systems SHOULD:

1. Aggregate RefusalEvents across executors
2. Detect statistical anomalies (function X refused by >N% of executors)
3. Require `relatedRefusals` field when executors are aware of coordinated action
4. Publish coordination reports for community review

---

## 8. Orchestration and Governance

### 8.1 Whigham-Style Governance Loops

Continuous improvement and governance loops (e.g., Define–Measure–Analyze–Improve–Control) operate **outside** the semantic boundary.

These loops:

* Select goals (potentially APQC-mapped)
* Choose semantic functions
* Construct and verify execution plans
* Interpret emitted effects
* Record refusals and outcomes
* Decide whether to continue, adapt, or halt

Governance is **not computation**. It is human (or human-delegated) judgment about what computation should occur.

### 8.2 Governance-to-Semantic Boundary

Governance systems MAY influence semantic execution **only** by injecting explicit, read-only Context.

**Context injection rules:**

1. Context MUST be immutable during execution
2. Context MUST be fully typed per SFS v2.2
3. Context MUST be inspectable by the function and any auditor
4. Context MUST NOT contain executable logic
5. Context SHOULD include AgentIdentity and delegationChain

This boundary ensures that governance decisions are visible inputs, not hidden tampering.

### 8.3 Community Governance Artifacts (v1.2)

"Communities decide" requires operationalization. DSFC v1.2 introduces Community Governance Artifacts that make community decisions explicit, versioned, and forkable.

```typescript
type CommunityPolicy = {
  readonly policyId: IRI
  readonly communityId: IRI
  readonly policyVersion: Version
  readonly policyCID: CID                      // Content-addressed
  readonly effectiveDate: Timestamp
  readonly expirationDate?: Timestamp
  
  // Authorization settings
  readonly effectAuthorizations: ReadonlyMap<EffectKind, AuthorizationLevel>
  readonly functionAuthorizations: ReadonlyMap<IRI, AuthorizationLevel>
  
  // Refusal settings  
  readonly mandatoryRefusals: readonly MandatoryRefusal[]
  readonly refusalAppealsEnabled: boolean
  
  // Context defaults
  readonly contextDefaults: Record<string, unknown>
  
  // Governance metadata
  readonly ratificationMethod: RatificationMethod
  readonly ratificationEvidence: RatificationEvidence
  readonly amendmentProcess: IRI              // Reference to amendment rules
  readonly forkableBy: 'ANYONE' | 'MEMBERS' | 'SUPERMAJORITY'
}

type MandatoryRefusal = {
  readonly effectPattern: EffectPattern       // Which effects must be refused
  readonly reasonCategory: RefusalCategory
  readonly reasonOntologyRef: IRI
  readonly justification: string
}

type EffectPattern = {
  readonly kind?: EffectKind
  readonly targetSystem?: string
  readonly targetResource?: string
  readonly payloadCondition?: Condition<unknown>
}

type RatificationMethod = 
  | 'FOUNDER_DECLARATION'
  | 'MEMBER_VOTE'
  | 'DELEGATED_AUTHORITY'
  | 'CONSENSUS'
  | 'SUPERMAJORITY'

type RatificationEvidence = {
  readonly method: RatificationMethod
  readonly participantCount?: number
  readonly approvalCount?: number
  readonly signaturesCID?: CID                // Aggregated signatures
  readonly deliberationRecordCID?: CID        // Discussion/debate record
}
```

**Community Policy Rules:**

1. Community policies MUST be content-addressed and versioned
2. Policy changes MUST follow the declared amendmentProcess
3. Members MAY exit communities whose policies they reject
4. Communities MAY fork, creating new policies from existing ones
5. Executors claiming community membership MUST enforce community policies

### 8.4 Community Membership

```typescript
type CommunityMembership = {
  readonly memberId: AgentIdentity
  readonly communityId: IRI
  readonly joinedAt: Timestamp
  readonly membershipProof: MembershipProof
  readonly roles: readonly CommunityRole[]
  readonly delegatedCapabilities: readonly AgentCapability[]
}

type MembershipProof =
  | { kind: 'SIGNATURE'; signatureCID: CID }
  | { kind: 'REGISTRY'; registryRef: IRI }
  | { kind: 'TOKEN'; tokenRef: IRI }

type CommunityRole =
  | 'MEMBER'           // Basic participation
  | 'CONTRIBUTOR'      // Can propose functions
  | 'REVIEWER'         // Can approve functions
  | 'GOVERNOR'         // Can propose policy changes
  | 'ARBITRATOR'       // Can resolve disputes
```

---

## 9. Ethics and Justice

### 9.1 Non-Capture Guarantees

DSFC is explicitly designed to resist capture through:

* **Forkability** — Any artifact can be forked with new identity
* **Open verification** — Anyone can verify any claim
* **Non-centralized identity** — No single authority over IRIs or meaning
* **Registry plurality** — Multiple registries prevent gatekeeping
* **Refusal rights** — Executors cannot be compelled

### 9.2 Justice Requirements

Implementations MUST:

1. Expose decision logic to affected parties upon request
2. Provide RefusalEvent access to affected parties
3. Support community-defined ethical policies
4. Record all AI agent actions per SFS v2.2 audit requirements

Implementations SHOULD:

1. Enable opt-out from effects by affected parties where feasible
2. Provide appeals processes for refusals
3. Detect and report coordinated refusal patterns
4. Support accessibility requirements in discovery interfaces

### 9.3 Preventing "The Algorithm Made Me Do It"

DSFC structurally prevents the excuse that automated systems compelled harmful action:

1. **Functions don't act** — They only compute and emit effect descriptions
2. **Executors choose** — Every effect execution is a choice with refusal rights
3. **Refusals are recorded** — Failure to refuse is visible
4. **Governance is explicit** — Community policies are public artifacts
5. **Delegation chains exist** — AI actions trace to human authorization

---

## 10. Conformance Levels

### 10.1 Artifact Conformance

An artifact is DSFC-conformant if it:

* Is valid SFS v2.2 (with postconditions)
* Declares ontology lineage (not just ontology reference)
* Is content-addressable (CID available)
* Includes discovery metadata
* Preserves provenance if forked

### 10.2 Registry Conformance

A registry is DSFC-conformant if it:

* Publishes transparency artifact (§6.3.3)
* Does not claim semantic authority
* Serves immutable artifacts
* Supports CID-based queries
* Maintains accessible audit logs
* Responds to federation requests

### 10.3 Executor Conformance

An executor is DSFC-conformant if it:

* Verifies artifact integrity before execution
* Preserves semantic boundary purity
* Treats effects as optional (refusal right)
* Records RefusalEvents with required fields
* Enforces claimed community policies
* Tracks agent identity per SFS v2.2

### 10.4 Planner/Orchestrator Conformance (v1.2)

A planner or orchestrator is DSFC-conformant if it:

* Constructs plans using SFS v2.2 ExecutionPlan type
* Verifies plans against goals using SFS v2.2 PlanVerifier
* Respects ontology lineage boundaries
* Uses OntologyBridge artifacts for cross-lineage composition
* Records PlanHandshake for accountability
* Obtains authorization per community policy before execution

### 10.5 Community Conformance

A community governance structure is DSFC-conformant if it:

* Publishes CommunityPolicy artifacts
* Follows declared ratification methods
* Provides membership verification
* Enables policy forking per declared rules
* Maintains dispute resolution processes

---

## 11. Non-Goals

DSFC explicitly does NOT aim to:

* Maximize computational performance
* Replace all enterprise BPM systems
* Enforce a single ontology or worldview
* Prevent all possible misuse
* Eliminate the need for human judgment

Its goal is **coherent, inspectable, shared reasoning** with **accountable human agency**.

---

## 12. SFS v2.2 Integration Matrix (v1.2)

DSFC v1.2 integrates with SFS v2.2 features as follows:

| SFS v2.2 Feature | DSFC Integration |
|------------------|------------------|
| **Postconditions** | Enable APQC-to-function bridging; planners query by postcondition satisfaction |
| **EffectAuthorization** | Maps to community policy authorization levels; CONFIRM/MULTI_PARTY become community consent |
| **AgentIdentity** | Required in RefusalEvents; tracks executor and delegation chains |
| **DiscoveryMetadata** | Primary substrate for registry indexing and natural language search |
| **ExecutionPlan** | Standard format for orchestration across community boundaries |
| **PlanHandshake** | Accountability record for all AI-generated plans |
| **PlanVerifier** | Used for cross-community and cross-lineage plan validation |
| **AuthorizationEnforcer** | Implemented by executors respecting community policies |
| **WorldState** | Bridges between APQC goals and function preconditions |

---

## 13. Closing Statement

The Distributed Semantic Function Commons treats computation as civic infrastructure.

Functions compute.
Goals declare.
Effects describe.
Executors choose.
Communities govern.
Refusals are recorded.

This specification makes reasoning *public, forkable, and accountable*. It does not prevent harm—no specification can. It makes harm *visible* and *attributable*.

When an AI agent executes a plan, the plan is verified. When an effect is refused, the refusal is recorded. When a community decides policy, the decision is an artifact. When someone claims "the algorithm made me do it," the audit trail shows who authorized what.

Build well. Build transparently. Build together.

---

## Appendix A: Threat Model

This appendix enumerates known threats to DSFC integrity and the mitigations the specification provides.

### A.1 Capture Threats

#### A.1.1 Registry Capture

**Threat:** A single registry becomes dominant through network effects, then uses its position to gatekeep functions or manipulate discovery.

**Mitigations:**
- §6.3 requires registry transparency artifacts
- §6.3.2 requires clients to query multiple registries
- Right to fork (§2.4) enables alternative registries
- CID-based integrity means registries cannot modify artifacts

**Residual Risk:** Social coordination may still concentrate on few registries.

#### A.1.2 Ontology Capture

**Threat:** Control over the "canonical" ontology enables semantic manipulation—changing what terms mean while code stays the same.

**Mitigations:**
- §2.3.1 introduces Ontology Lineage with content-addressed versions
- Ontology forks preserve parent lineage
- OntologyBridge artifacts make cross-lineage composition explicit

**Residual Risk:** Most users may use dominant lineage without understanding alternatives.

#### A.1.3 Community Capture

**Threat:** Community governance processes are captured by small groups who manipulate policies.

**Mitigations:**
- §8.3 requires ratification evidence
- Policies are content-addressed and auditable
- Members can exit and fork communities
- Deliberation records can be required

**Residual Risk:** Apathy may enable minority capture in low-participation communities.

### A.2 Coercion Threats

#### A.2.1 Registry Coercion

**Threat:** Legal or political pressure forces registries to delist functions.

**Mitigations:**
- Registry plurality reduces single points of coercion
- Content addressing enables distribution outside registries
- Delisting must be recorded in audit logs
- Other registries may continue serving

**Residual Risk:** Coordinated multi-jurisdiction pressure could affect major registries.

#### A.2.2 Executor Coercion

**Threat:** Executors are pressured to refuse or execute certain effects regardless of function output.

**Mitigations:**
- Refusal rights allow resistance to forced execution
- RefusalEvents create evidence of coercion patterns
- Community policies can mandate certain refusals
- Coordinated refusal detection (§7.5) surfaces collusion

**Residual Risk:** Coercion may be subtle or backed by overwhelming force.

### A.3 Manipulation Threats

#### A.3.1 Ethics Washing

**Threat:** Executors claim refusal rights but never actually refuse, creating false appearance of ethical agency.

**Mitigations:**
- RefusalEvents are auditable
- Absence of refusals for known-problematic effects is detectable
- Community policies can mandate specific refusals

**Residual Risk:** Requires active monitoring to detect.

#### A.3.2 Silent Executor Collusion

**Threat:** Executors coordinate to refuse certain functions without declaring coordination, effectively censoring through distributed action.

**Mitigations:**
- §7.5 coordinated refusal detection
- `relatedRefusals` field for transparency
- Statistical anomaly detection across executor population

**Residual Risk:** Sophisticated collusion may evade detection.

#### A.3.3 Semantic Reassignment Attack

**Threat:** Attacker publishes function, waits for adoption, then changes alignment manifest to alter semantic meaning while preserving code.

**Mitigations:**
- §6.2 requires content-addressed manifests
- Function references include manifest CID
- Manifest changes produce new CID, breaking references

**Residual Risk:** Effectively eliminated by content addressing.

#### A.3.4 Context Poisoning

**Threat:** Malicious governance layer injects misleading Context that technically complies with type constraints but produces harmful outcomes.

**Mitigations:**
- §8.2 requires Context to be inspectable
- Community policies define acceptable Context defaults
- Audit trails include Context snapshots

**Residual Risk:** Subtle poisoning may be hard to detect without domain expertise.

#### A.3.5 Ontology Drift Attack

**Threat:** Slow, incremental changes to ontology definitions gradually shift function meanings without triggering version changes.

**Mitigations:**
- Ontology Lineage includes content-addressed versions
- Any ontology change produces new CID
- Functions pin to specific lineage versions

**Residual Risk:** Requires vigilance in tracking ontology updates.

### A.4 Availability Threats

#### A.4.1 Refusal Flooding

**Threat:** Attacker generates spurious RefusalEvents to delegitimize specific functions or overwhelm audit systems.

**Mitigations:**
- RefusalEvents require executor identity
- Sybil attacks detectable through identity analysis
- Community policies can weight refusals by executor reputation

**Residual Risk:** High-volume attacks may still degrade signal quality.

#### A.4.2 Registry Denial of Service

**Threat:** Registries are overwhelmed, preventing discovery.

**Mitigations:**
- Local caching of critical artifacts
- CDN acceleration (§6.4)
- Registry federation enables failover
- Artifacts remain valid without registry access

**Residual Risk:** Discovery of new functions may be impaired.

---

## Appendix B: Refusal Reason Ontology (Reference)

This appendix provides a reference taxonomy for refusal reasons. Implementations MAY extend this taxonomy within their ontology lineage.

### B.1 Top-Level Categories

```
RefusalReason (urn:dsfc:ontology:refusal:Reason)
├── PolicyRefusal (urn:dsfc:ontology:refusal:Policy)
│   ├── OrganizationalPolicy
│   ├── CommunityPolicy
│   └── PersonalPolicy
├── LegalRefusal (urn:dsfc:ontology:refusal:Legal)
│   ├── JurisdictionalProhibition
│   ├── RegulatoryCompliance
│   ├── ContractualObligation
│   └── CourtOrder
├── EthicalRefusal (urn:dsfc:ontology:refusal:Ethical)
│   ├── ConscienceObjection
│   ├── HarmPrevention
│   ├── PrivacyProtection
│   └── AutonomyRespect
├── TechnicalRefusal (urn:dsfc:ontology:refusal:Technical)
│   ├── ResourceUnavailable
│   ├── CapabilityMissing
│   ├── DependencyFailure
│   └── RateLimitExceeded
├── IntegrityRefusal (urn:dsfc:ontology:refusal:Integrity)
│   ├── CIDMismatch
│   ├── SignatureInvalid
│   ├── LineageMismatch
│   └── ManifestTampered
├── CommunityRefusal (urn:dsfc:ontology:refusal:Community)
│   ├── NormViolation
│   ├── GovernanceDecision
│   ├── MembershipRequired
│   └── ReputationThreshold
└── AuthorizationRefusal (urn:dsfc:ontology:refusal:Authorization)
    ├── HumanApprovalDenied
    ├── HumanApprovalTimeout
    ├── InsufficientApprovers
    └── DelegationChainInvalid
```

### B.2 BFO Alignment

Refusal reasons are modeled as subclasses of `bfo:Quality` inhering in the refusal event (a `bfo:Process`).

```
bfo:Quality
└── dsfc:RefusalReason
    └── [taxonomy above]
```

### B.3 Usage Example

```typescript
const refusalEvent: RefusalEvent = {
  id: 'urn:dsfc:refusals:2024-01-15:executor-001:effect-xyz' as IRI,
  timestamp: { iso8601: '2024-01-15T14:30:00Z', epochMs: 1705329000000 },
  effectRef: 'urn:dsfc:effects:deleteUserData:12345' as IRI,
  effectCID: 'bafybeigdyrzt5sfp7udm7hu76uh7y26nf3...' as CID,
  executorIdentity: {
    agentId: 'executor-001',
    agentType: 'AUTOMATED',
    sessionId: 'session-abc',
    capabilities: ['EXECUTE'],
    delegationChain: [{ agentId: 'admin-jane', agentType: 'HUMAN', ... }]
  },
  reasonCategory: 'LEGAL',
  reasonOntologyRef: 'urn:dsfc:ontology:refusal:Legal:RegulatoryCompliance' as IRI,
  justification: 'GDPR Article 17 retention period not yet elapsed',
  communityPolicy: 'urn:dsfc:communities:eu-data-protection:policy:v2.3' as IRI,
  appealable: true,
  appealDeadline: { iso8601: '2024-01-22T14:30:00Z', epochMs: 1705933800000 }
}
```

---

## Appendix C: Example Artifacts

### C.1 Ontology Lineage Declaration

```typescript
const communityOntologyLineage: OntologyLineage = {
  lineageId: 'urn:dsfc:lineages:civic-tech-commons:2024' as IRI,
  rootOntologyIRI: 'urn:obo:bfo.owl' as IRI,
  versionCID: 'bafybeihkoviema7g3gxyt6la7vd5ho32...' as CID,
  parentLineage: {
    lineageId: 'urn:dsfc:lineages:civic-tech-commons:2023' as IRI,
    rootOntologyIRI: 'urn:obo:bfo.owl' as IRI,
    versionCID: 'bafybeigdyrzt5sfp7udm7hu76uh7y26nf3...' as CID,
  },
  divergencePoint: { iso8601: '2024-01-01T00:00:00Z', epochMs: 1704067200000 },
  maintainerCommunity: 'urn:dsfc:communities:civic-tech-commons' as IRI
}
```

### C.2 Community Policy

```typescript
const communityPolicy: CommunityPolicy = {
  policyId: 'urn:dsfc:communities:privacy-advocates:policy:v1.0' as IRI,
  communityId: 'urn:dsfc:communities:privacy-advocates' as IRI,
  policyVersion: { major: 1, minor: 0, patch: 0 },
  policyCID: 'bafybeihkoviema7g3gxyt6la7vd5ho32...' as CID,
  effectiveDate: { iso8601: '2024-01-01T00:00:00Z', epochMs: 1704067200000 },
  
  effectAuthorizations: new Map([
    ['DELETE', 'CONFIRM'],
    ['UPDATE', 'NOTIFY'],
    ['CREATE', 'AUTO'],
  ]),
  
  functionAuthorizations: new Map([
    ['urn:dsfc:functions:bulkDataExport', 'MULTI_PARTY'],
  ]),
  
  mandatoryRefusals: [
    {
      effectPattern: {
        kind: 'EMIT',
        targetSystem: 'advertising',
      },
      reasonCategory: 'COMMUNITY',
      reasonOntologyRef: 'urn:dsfc:ontology:refusal:Community:NormViolation' as IRI,
      justification: 'Community prohibits advertising-related data emissions'
    }
  ],
  
  refusalAppealsEnabled: true,
  contextDefaults: { privacyLevel: 'strict' },
  
  ratificationMethod: 'MEMBER_VOTE',
  ratificationEvidence: {
    method: 'MEMBER_VOTE',
    participantCount: 150,
    approvalCount: 142,
    deliberationRecordCID: 'bafybeigxyz...' as CID,
  },
  
  amendmentProcess: 'urn:dsfc:communities:privacy-advocates:amendment-rules' as IRI,
  forkableBy: 'ANYONE'
}
```

### C.3 APQC Goal Mapping

```typescript
const pricingStrategyGoal: APQCGoalMapping = {
  apqcCode: '2.2.3',
  apqcDescription: 'Develop pricing strategy',
  goalDeclaration: {
    id: 'urn:dsfc:goals:apqc:2.2.3' as IRI,
    description: 'A pricing strategy exists that has been validated and approved',
    goalState: { pricingStrategyDefined: true, approved: true },
    satisfiedWhen: {
      mode: 'ALL',
      conditions: [
        {
          id: 'urn:dsfc:conditions:pricingStrategyExists' as IRI,
          description: 'A pricing strategy document has been produced',
          predicate: { kind: 'expression', evaluate: (s) => s.pricingStrategy !== null }
        },
        {
          id: 'urn:dsfc:conditions:pricingStrategyApproved' as IRI,
          description: 'The pricing strategy has stakeholder approval',
          predicate: { kind: 'expression', evaluate: (s) => s.approvalStatus === 'APPROVED' }
        }
      ]
    }
  },
  suggestedFunctions: [
    'urn:dsfc:functions:analyzeCostStructure' as IRI,
    'urn:dsfc:functions:assessMarketPosition' as IRI,
    'urn:dsfc:functions:generatePricingOptions' as IRI,
    'urn:dsfc:functions:validatePricingStrategy' as IRI,
  ],
  ontologyLineage: communityOntologyLineage
}
```

---

## Appendix D: Glossary

| Term | Definition |
|------|------------|
| **AgentIdentity** | SFS v2.2 type identifying human or AI caller |
| **CID** | Content Identifier; cryptographic hash serving as artifact identity |
| **Community Policy** | Governance artifact defining authorization levels and refusal mandates |
| **DSFC** | Distributed Semantic Function Commons |
| **Effect** | SFS descriptor of intended state change |
| **Executor** | System that interprets and optionally enacts effects |
| **Goal Declaration** | SFS v2.2 specification of desired world state |
| **IRI** | Internationalized Resource Identifier |
| **Ontology Bridge** | Artifact mapping terms between ontology lineages |
| **Ontology Lineage** | Content-addressed version chain of an ontology |
| **Planner** | System that constructs execution plans from goals |
| **RefusalEvent** | Record of executor declining to enact an effect |
| **Registry** | Non-authoritative discovery index for artifacts |
| **Semantic Function** | SFS v2.2 pure, deterministic computation with explicit effects |

---

*End of DSFC v1.2 Specification*
