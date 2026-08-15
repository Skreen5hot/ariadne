# FNSR: An Epistemic Constitution for Accountable Synthetic Agency

## Conceptual Design Document — v1.0-rc1 (production candidate)

**Status.** Production candidate for ratification, unratified. Supersedes v0.5 — superseded, not erased, per A7. Appendix B is both the change record and the signed adjudication of the Attempt-2 adversarial review conducted under Reviewer Brief v2.0 (five findings, three held-claims, a gap log, a verdict) — including the correction of that review's verdict class. Four review passes are now incorporated: rounds 1–3 and the Attempt-2 audit. This document is the object of the Round-4 gate; the charter's §1 object reference updates to this version at conferral (administrative). What remains between this text and v1.0 is the gate itself: conferral, companion-artifact discharge of O1–O7, and the signed widening act.

**Self-applied classification** — of this *logical record*, not of its content; the copy being read is a *token* of it (§3.1). Derivation: *hypothesized* (assigned once; immutable). Provenance-source: *authored*. Mode: *assertoric*. Security: *normal*. License status: *informational-only* under the standing pre-ratification regulation; widening requires a governed promotion process. Enforcement projection: L3 — with *normal* and *L3* marked **provisional pending the O3 carrier freeze**, a reflexivity gap the Attempt-2 review correctly filed (G-07, G-08); the label is re-issued against frozen carriers at the gate.

**Audience and purpose.** Written for the informed reader across ethics, governance, formal ontology, and systems architecture; it assumes no access to the specification corpus. This document is the normative preamble to that corpus: it states *why* the rules exist. *How* they are coded lives in the specifications it points to — ARIADNE Taint Algebra v1.0, HIRI Digital Passport Extension v1.9.0, FSDD/FNSR-SDD v2.1.0, TagTeam Alpha.2 with Realist Deontic Modeling v1.2.1, SHML v3.3, the ARCHON governance framework — none of which is reproduced here. Anchors are placeholders pending pagination. Guarantee-class language is indexed to the obligations register (Appendix C); undischarged obligations read as design intent.

### 0. Terminological conventions

**Mentalistic vocabulary is functional throughout.** *Belief* names assertable commitment; *supposition* names the counterfactual commitment mode of a record or occurrence; *perception* names sensor-derived observation processes and their products; *imagination* names the generation of suppositional records. *Entertained* is operational: a recorded counterfactual-processing occurrence that produced or accepted a record under a context — no inner episode is implied, here or anywhere in the architecture.

**Record and token.** *Record* names the logical, CID-identified serialized information object — a generically dependent continuant realized in however many physical bearers carry it. *Token* names one such physical realization (an Information Bearing Entity or Artifact). Classifications attach to records; tokens realize them. The bare word *claim* remains retired.

**License is law, not label.** *License Regulation* names prescriptive content — a Process Regulation produced by a governed process — that prescribes use-processes of a record as permitted, prohibited, or required. *License status* names the nominal, descriptive summary of a record's current standing under the regulations in force. Enforcement consults status; adjudication consults regulations.

**Directional vocabulary is banned, and scoped.** Four verbs describe standing change — *restrict* and *worsen* (pre-authorized consequences of service findings under standing regulations), *widen* and *rehabilitate* (fresh governed processes only) — and all four apply to **license status**. Derivation admits no verbs: assigned once, amended by no one (§3.4).

---

## 1. Thesis

> FNSR is an epistemic constitution for accountable synthetic agency. It claims no consciousness for the machine and does not decide whether the occupant is an agent; it governs, from outside and in functional vocabulary, whatever occupies the functional place of a mind. It governs by record: semantic content is never stained or blamed — every classification lands on the CID-identified logical record of a producing occurrence, realized in however many tokens carry it — so the same proposition may be supposed today and independently observed tomorrow without laundering, because what is indelible is derivation, and derivation lives on records. Three notions the constitution refuses to conflate: derivation, assigned once and amended by no one; support, which computation genuinely produces and strengthens; and license, which is law, not label — prescriptive regulations produced only by processes realizing external Authority Roles, with nominal status records reporting their current consequence. The bridge from support to license is always an external act. Acts are licensed by the worst record they materially rely upon, over a material-reliance graph traced from dataflow, environment included, prunable only by governed adjudication. Supposition reaches judgment by quotation alone — a minted record that *mentions* the suppositional record and is *about* the occurrence that produced it: use/mention, in existing ontological relations, enforced cryptographically. Its guarantees are attribution and immutability, not truthfulness — attribution dividing into cryptographic provenance and the governed binding of key to agent. Its history is bitemporal; its accountability routes around the occupant, because it cannot bottom out there; it is blind to what was never gathered and honest about the blindness; and it ends where it means to: answerability without assumed subjectivity, and a marked point at which the engineering argument runs out.

---

## Part I — Design Philosophy: Why the Rules Exist

### 2.1 External governance: the constitutional shell, not the occupant

The framework declines the consciousness question, and not from caution. The non-commodifiability commitment (*A Line in the Sand*) forbids treating the presence or absence of experience as an engineering variable, so no rule in this architecture turns on whether the machine has a mind. What the framework builds instead is the community's theory of the machine — attested cryptographically rather than accepted through presumed access to internal states. The occupant of the functional place of a mind is governed as a black box with a glass ledger: legible in every commitment recorded, private in its mechanism. FNSR is the constitutional shell around that occupant, not the occupant itself; what happens inside the shell — perception, concept formation, judgment, moral imagination — is a different layer of the research program, and Part VI names it.

### 2.2 Conservation: derivation is fixed, support is produced, license is conferred

The first structural promise is conservation, stated as three notions the constitution refuses to conflate — and v0.4 repairs the one sentence in which v0.2–v0.3 still compressed two of them. **Derivation** — where a record came from, by what process — is assigned once at origination and amended by no one; editing lineage would falsify history (A7). **Support** — how well-evidenced a piece of descriptive content is — is genuinely *produced* by computation: deduction, corroboration, and independent observation create and strengthen it, and the constitution does not deny epistemology its ordinary powers. Earlier drafts said "warrant cannot be self-conferred," which sat awkwardly beside exactly that concession; the compression is retired. What cannot be self-conferred is **recognition**: the standing of evidence as *sufficient*, and the **license** that standing purchases. Support is self-producible; recognition and license are not. The bridge from support to license is always an external act — a governed process realizing an Authority Role and producing a Process Regulation that prescribes use as permitted, prohibited, or required. The Promotion API is the interface artifact whose invocation participates in such a process; the widening act is the process, not the interface (A3). This grounding is convergent with the Realist Deontic Modeling machinery already ratified in TagTeam RDM v1.2.1: an integration task, not new design. [→ RDM v1.2.1; ARCHON schema — anchors TBD]

### 2.3 Trust conserved, concentrated, and named

The second promise is a corollary of the first: trust is not eliminated but conserved — concentrated into named, signed, tested places. The sanitizer's pattern base, the classification originator's judgment, the gateway bench, the promotion bench, the attestors, the custody of keys, the verified proof kernel, the authorship of projection and threshold tables, the **key–agent binding** (a valid signature establishes use of a key; attribution to an accountable agent rests on the governed, institutional binding of that key to that agent) — and now, explicitly, the **authorship of standing regulations**, since the law under which services restrict unilaterally is itself conferred in advance. Each is a place where trust is spent, and each has a failure mode the architecture can attribute but not prevent. The ledger makes negligence attributable, not impossible. The theory carries an honest-community assumption the way cryptography carries honest-majority assumptions — stated as an assumption, never smuggled as a theorem. Conformance testing runs continuously against laundering: the constitution has a test suite. What the tests cannot supply is the community that reads their results.

### 2.4 Agent-neutral by construction — now in exact vocabulary

Round 2 demanded a decision on whether the synthetic occupant is a CCO Agent; the constitution's answer remains that it must not need one. Deciding *yes* would presuppose what Layer 3 holds open; deciding *no* would foreclose by stipulation what should be settled by argument. Round 3 corrected the vocabulary in which Layer 1 proves the stronger thing: there is no "non-agentive information processing" class to invoke, and the attractive CCO Act classes — information processing, measuring, observation, prediction — are all agentive. So the neutrality is achieved with what exists: **occupant computations are typed as instances of BFO Process, related to their continuant inputs and outputs by the existing has-input and has-output relations; no CCO Act subclass is asserted of the occupant unless occupant agency is independently established** (obligation O6). The agentive Acts in the architecture — representative communication, attestation, promotion, revocation — are borne by the humans and institutions holding Authority Roles. This is the ontological form of the vouching argument (*The Machine That Could Not Vouch for Itself*): accountability routes around the occupant because it cannot bottom out there — the agent can always forge its own receipts, which is why the receipts are held by everyone else. The constitution is robust to either eventual answer; the burden of deciding belongs to Layer 2, where it can be argued rather than assumed.

---

## Part II — The Ontological Substrate

v0.3 made the *subjects* of classification foundational; v0.4 fixes their identities. Two of round 3's blocking findings live here: nothing in the substrate may be an ICE without aboutness, and the thing a CID identifies must be said exactly.

### 3.1 The entity substrate: six kinds

The v0.3 quintet splits its third member and becomes six kinds, kept apart. **Occurrents:** observation, digitization, parsing, simulation, communication, promotion, and revocation processes. **Domain content:** the Information Content Entities such processes produce or use — *descriptive* (truth-apt), *prescriptive* (directive), and *designative* (symbols designating entities: names, identifiers, CIDs), mutually disjoint and not claimed exhaustive. **Logical records:** the CID-identified serialized information objects — generically dependent continuants realized wherever their tokens are. **Bearer tokens:** the physical realizations — Information Bearing Entities and Artifacts on servers, devices, and IPFS nodes; numerically distinct even when the record is one. **Classification ICEs:** the governance labels, modeled on the Nominal Measurement pattern as classifications *about* a declared target — a record, a token, an act, or a use — never as qualities inhering in abstract content; each label-assignment is itself a first-class, bitemporal record. **Governance entities:** Authority Roles borne by agents, realized in processes that produce Process Regulations. Every rule in Part III names which of the six it binds. **Kept apart is functional, not axiomatic:** the six kinds are a role taxonomy over the substrate, not a pairwise-disjointness claim — Classification ICEs *are* ICEs, and License Regulations *are* Prescriptive ICEs. The only disjointness asserted is the one the ontology asserts (Descriptive / Prescriptive / Designative), and the OWL rendering must assert no more (A1, O7): a rendering that hardens the roster into six disjoint classes is itself a binding defect.

### 3.2 The record-centric principle — with record identity said exactly

Classifications attach to logical records of occurrences, not to semantic content and not to tokens. **The CID identifies the serialized informational object;** replicas on server A, server B, a USB device, and an IPFS node are four tokens of one record, and a classification of the record holds wherever any token is encountered. The proposition *Valve V is open* still acquires no identity from having been simulated: the simulation occurrence and its record are permanently suppositional; tomorrow's independent measurement mints a new record carrying the same proposition with derivation *observed*. Anti-laundering needs indelible derivation on records — which the signing discipline provides — not stained content and not token-tracking. Nothing semantic is ever "hostile" or "clean"; records bear status, tokens bear syntax, acts and uses bear assessment.

### 3.3 The boundary, re-typed again: signal, digitization, designation, interpretation

v0.3's "semantically uninterpreted content" fixed a word and kept the category error: an ICE is *defined* by aboutness, so an ICE awaiting aboutness cannot exist. The corrected chain: a **physical signal** (a process, process profile, or quality — not yet informational at all) enters a **recording or digitization process**, which produces **encoded tokens whose first content is designative and low-level descriptive** — encodings designate magnitudes, hashes designate payloads, timestamps describe instants — so aboutness is present from the first ICE onward. What **interpretation processes** add is not aboutness but *domain* aboutness: content about the world beyond the signal chain. Measurement and perception processes yield observation records; interpretation yields claim records; each transition is priced, because meaning about the world is purchased with fallibility. At origination, content undergoes **semantic routing** — descriptive to the derivation/support machinery; prescriptive to the deontic machinery (RDM), with provenance, adversarial classification, and use restrictions but no truth-grading; designative to identity and resolution machinery, where an identifier needs no truth warrant to do its work. The routing is not claimed exhaustive. The hostile-instruction orthogonality stands: its hostility said nothing about its warrant because the directive was never in the warrant function's domain.

### 3.4 The two tracks on every record: derivation and license — with license split in two

**Derivation class** — observed / interpreted / hypothesized — is a lineage taxonomy, assigned exactly once by the classification originator and immutable by everyone including governance: the birth certificate, never amended; a botched origination is superseded, with the error preserved. Qualifications of source do not enlarge this carrier: *where from* is **provenance-source metadata** (source = sensor, ledger, own-ledger, testimony, …) recorded beside the derivation value, not fused into it — repairing v0.3's *observed-from-ledger* slip before O3 freezes the carriers. **License** divides into the two things v0.3 ran together. The **License Regulation** is prescriptive content — a Process Regulation, produced only by a governed process realizing an Authority Role — that prescribes use-processes of a record as permitted, prohibited, or required: this is where normative force lives — and each regulation's **effect envelope**, the set of status consequences it can produce across all inputs, is fixed at conferral: the envelope, not the wording, is what governance conferred (A3). The **License Status Classification** is a nominal, descriptive summary — "action-eligible under regulation R as of t" — reporting the current consequence of the regulations in force: this is what enforcement consults and what π projects. Reducing license to the status label alone would turn permission into description; the regulation/status split keeps law and ledger distinct. Support remains the third notion (§2.2): computable, growable, and never itself a license.

### 3.5 Mode and quotation: use/mention, in existing relations

Mode qualifies records and occurrences, not content: **assertoric** and **suppositional**. Quotation remains a relation, not a state — and v0.4 implements it with relations that already exist rather than a bespoke "record about record" device: the mint produces logical record **G**, whose carried content **C_G** is a Descriptive ICE; C_G *is about* the counterfactual-processing occurrence **O** and *is about* the suppositional record **R_P**; and G's tokens stand in *is-mention-of* to R_P. Use versus mention, in the ontology's own vocabulary. A4 states the discipline.

### 3.6 Adversarial classification is scoped — down to the token

Every adversarial assessment declares its target: a source, a **token or encoding** (exploit syntax lives in bytes), a communicative act, or a content-in-use-context. Hostility is not an intrinsic state of semantic content, so a defused reproduction of quarantined material in an analytic context is a different token in a different use — not the hostile thing. Debt 2 remains dissolved to its residual: the governed release of *original* quarantined records.

---

## Part III — The Axioms

Each axiom names which entities of §3.1 it binds; machinery is referenced, not reproduced.

### A1. Usage-Based Epistemics — status projected conservatively, regulations behind it

A license status answers the enforcement question about a record: *what may be done with this, now, under the regulations in force* — never *how likely is its content true*. Composition narrows: a composite act or verdict may be used only as its most restricted materially relied-upon record may be used (A5). The strangulation objection still inverts into the design's point: degradation toward restriction is correct, and wide status is bought back only by fresh regulation. The scalar π survives as the enforcement projection of a record's status bundle, under obligations now stated in their corrected form (Appendix C): **conservativity** (O1) and **composition compatibility** (O2 — composing projections is at least as restrictive as *projecting the composition*, with overall safety against the canonical state following from O1 by transitivity). Enforcement consults projected status for speed; adjudication consults regulations and canonical classifications for truth about standing. [→ *ARIADNE*, §projection — anchor TBD]

### A2. Priced Inference — method as provenance, not phantom premise

Each engine's output record carries **inference-method provenance** — defeasible, abductive, analogical, simulative — via the ordinary has-input/has-output process relations, and the degradation rule is *policy over* (input classifications, method class): abductive method fixes derivation *hypothesized*; analogical fixes *interpreted* with method metadata and a policy floor on status; simulation fixes derivation *hypothesized* with method *simulative* and mode *suppositional* — v0.4 assigned only the mode, leaving the record's lineage to inference, and a plausible guess is exactly what a carrier freeze must not require: terminality lives in mode; lineage lives in derivation; suppositional records are born *hypothesized* like every product of non-truth-tracking method. Deduction's identity price remains relative: a verified deductive transformation adds no restriction beyond its premises and its pinned environment — kernel, formalization, ontology version, checker build — which live in the trusted computing base and appear as environment nodes in the material-reliance graph (A5). [→ triad contracts; *ARIADNE*, §method-policy — anchors TBD]

### A3. The Mutation Asymmetry — restriction is pre-authorized, widening is fresh law, and the law's own text is governed

Services do not legislate. What v0.2 called unilateral worsening is, exactly typed: a service produces a **descriptive finding** (uncertainty, risk, anomaly — a Nominal classification), and a **standing regulation**, conferred in advance by governance, prescribes the restrictive status consequence of that finding. Suspicion is free because it is *pre-authorized*, not because services hold authority. Widening has no standing pre-authorization: it requires a **fresh governed process** — the promotion process, an occurrence realizing an Authority Role and producing a new License Regulation, atomic, signed, audited; the Promotion API is the interface artifact whose invocation participates in that process, and is not itself the act.

The Attempt-2 review broke the v0.5 form of this axiom at its softest joint (F-04): a standing regulation whose trigger threshold moves from 0.70 to 0.95 restricts *less*, and restricting less relative to the active baseline is **functional widening** — routed as a routine defense update, it would bypass the promotion monopoly entirely. The repair governs authorship, not just content. A standing regulation's **effect envelope** — the set of status consequences it can produce across all inputs — is fixed at conferral, and any amendment is an **authorship act**: a governed process realizing an Authority Role, signed and audited like any conferral. The **monotone-envelope test** then sorts amendments: a re-authorship whose envelope is *nowhere more permissive* than its predecessor's is administrative — governed and signed, but summary; an envelope *anywhere more permissive* is a widening and takes the full promotion process, however the change is labeled. Envelope comparison is machine-checked (O5), so a defense update cannot smuggle permission by renaming it.

**Derivation is outside the asymmetry entirely:** no act, governed or otherwise, amends it; correction of a botched origination is supersession by a new record, and compound lineage resolves conservatively (O3). Origination stays single-sourced. The invariant is design-exceptionless; its enforcement is conformance obligation O5. [→ *ARIADNE*, §mutation; Promotion contract — anchors TBD]

### A4. Quotation — use/mention, enforced cryptographically, in the ontology's own relations

When the simulator processes content P under context C, the suppositional record R_P is permanent *as a record*; the content is untouched. The gateway mints logical record **G** under the §3.5 pattern: C_G (Descriptive ICE, carried by G) *is about* occurrence O and *is about* R_P; G's tokens *are mentions of* R_P. G's derivation is **observed**, with provenance-source **ledger** — the occurrence is externally witnessed at transit, not introspected — and its status is constrained *informational-only* under the standing gateway regulation. Downstream judgment uses G; it never uses R_P assertorically. The quotation marks do not cleanse the proposition — nothing was stained — they change what is being asserted. And the loop stays closed by conformance (O5): any record originated from the system's own quoted output carries derivation **interpreted** with provenance-source **own-ledger**, never derivation *observed* — otherwise the mint plus a provenance loop would become a widening path. [→ Counterfactual Gateway contract, rev. required — anchor TBD]

### A5. Conduct Under License — the material-reliance graph

Action status is the join over the transitive set of records **materially relied upon** in selecting the act — never the maximum over everything encountered. v0.4 renames the structure the **material-reliance graph**: a relied-upon record need not *support* the conclusion — it may rebut, defeat, constrain, or merely shape the decision — and "support" stays reserved for the epistemic notion of §2.2. Reliance is not endorsement; it is dependence. The risk asymmetry stands: **under-inclusion is the laundering hole**, so the graph includes **environment nodes** — policy configuration, thresholds, model parameters, ontology versions, engine builds — each a record with its own classifications; **over-inclusion merely over-restricts**, which A1 tolerates by design. Two Attempt-2 findings refine this stance without reversing it. First, tolerance of over-restriction is a *safety* posture, not an availability promise — the constitution has never guaranteed liveness — but O4 now owes the graph **decidability**: a declared taxonomy separating governance-critical environment nodes from operational telemetry, with bounded inclusion rules, so that conservatism cannot be weaponized into denial of service (F-03, reframed). Second, **identity merge joins, never inherits**: when entity resolution aliases or merges records, the resulting classification bundle is the *join* of both records' bundles — most restrictive on every dimension — and no merge may let a restricted record inherit a cleaner record's standing (F-01, the real finding inside an overbuilt attack); merge-join is a conformance test (O5). The traced graph is the conservative floor; refinement is **governed pruning** — the reliance set shrinks only by signed, attributable adjudication, never by occupant testimony (A6). Thresholds are unchanged: standards of proof — preponderance, clear and convincing, beyond reasonable doubt — grade the evidentiary scale; action thresholds (probable cause the exemplar) attach to intervention types; all conferred as regulations, all enforced at decision time, violation halting into containment rather than logging. Audit describes after; license governs before. [→ orchestrator invariants; ARCHON schema; *RDM v1.2.1* — anchors TBD]

### A6. Skeptical Self-Explanation — guarantees named exactly

Four properties, not conflated: **truthfulness**, **sincerity**, **attribution**, **immutability**. The architecture guarantees the latter two, and only the latter two — §5.1's signed lie disproves any stronger reading — with attribution split into cryptographic provenance (key-level, mathematical) and the governed key–agent binding (institutional). What the pair buys, stated without inflation: the system may be wrong about itself; it may not silently rewrite what it said about itself; and it may not rely on an unrecorded self-representation as though it had been publicly warranted. Explanation records inherit the classifications of the records they explain; introspection receives no evidentiary discount; conduct is monitored without consulting the story. [→ Interpretability Service contract; BAM spec — anchors TBD]

### A7. Immutable and Bitemporal History — with times told apart

The past is append-only: error is answered by new signed records, never by rewriting old ones. Four times are kept distinct: the **occurrence time** of the world-side process; the **record time** at which its record enters the ledger; the **effective interval** during which a regulation or status is in force; and the **revocation or supersession process**, itself an occurrence with its own record. Because every label-assignment and every regulation is a first-class bitemporal record, demotion needs no exotic machinery: it is the production of a new regulation or status record with a new effective interval, superseding — never erasing — its predecessor. Revocation triggers recomputation of descendants' *current* standing while their *historical* standing stands unrewritten: **then-permitted, now-unsupported.** The cascade runs in the present tense only — and, for **environment nodes** specifically, v1.0-rc1 states what v0.5 left implicit (F-02): supersession of an environment node never touches the historical standing of records originated under it; what changes is the standing of **new reliance**. A historical record consumed as fresh input after the supersession is a new reliance edge, judged at consumption time against the environment then in force, without its origination status moving — *then-permitted* survives; *now-relied-upon* is priced now. Structural invalidation of a node (it was never what it claimed) and operational revocation (it is no longer acceptable) are distinct acts with distinct cascade scopes, and the Demotion machinery of Debt 1 implements both. Machinery registered as Debt 1 (§5.5). [→ audit-log invariants; HIRI anchoring — anchors TBD]

---

## Part IV — Reference Architecture: A Map, Not the Territory

Four stations; each names the promise it enforces and points into the corpus without opening it.

### 4.1 The Boundary (the Sieve)

Physical signals enter digitization; the first content is designative and low-level descriptive; measurement and perception processes produce observation records; interpretation adds domain aboutness and produces claim records — each transition priced. Semantic routing sends descriptive content to the derivation/support machinery, prescriptive content to the deontic machinery with no truth-grading, and designative content to identity and resolution. The single originator assigns derivation once (immutable, with provenance-source metadata beside it) and initial status under standing regulations; contributors constrain but never classify; the signer fixes the CID of each logical record at the boundary. Promise: nothing is born with status beyond its process floor, and nothing truth-inapt enters the warrant machinery. [→ *FSDD/FNSR-SDD v2.1.0*; *TagTeam Alpha.2*; *ARIADNE*, §origination]

### 4.2 The Occupant (the Core Agency)

The reasoning triad and verdict composer, emitting records with method provenance, composed under join, within a pinned environment whose kernel, ontology, and versions sit in the trusted computing base — and whose computations are typed exactly per §2.4 (O6): BFO Processes with has-input/has-output relations to their continuants, no CCO Act subclass asserted of the occupant. The occupant is deliberately swappable. Promise: inference priced by method, relative to named trust, presupposing no answer to the agency question. [→ triad contracts; MDRE specification]

### 4.3 The Gatehouse (Orchestration and Enforcement)

The orchestrator compiles the material-reliance graph from the dataflow record — claim records plus environment nodes — computes the saga status over the transitive relied-upon set, admits pruning only by signed adjudication, checks conferred thresholds at every decision point, and halts into containment on violation. The Counterfactual Gateway is the quotation mint of A4, its transits evidence. Defense services produce findings whose restrictive consequences flow from standing regulations; the behavioral monitor watches conduct without reading the story. Promise: acts under license — computed over reliance, environment included, judged against conferred thresholds, halting rather than logging. [→ *ARIADNE*, §join, §gateway; ARCHON schema]

### 4.4 The Ledger (Record and Conferral)

CIDs identify logical records; signatures bind serializations; tokens replicate across stores and IPFS without multiplying records. The audit is append-only and bitemporal, with regulations and status classifications as first-class records; the promotion process is the sole widening act, its API an interface artifact; witnesses and governance confer standing regulations, thresholds, projection policy, and key–agent bindings; conformance testing hunts laundering, including the re-ingestion test of A4. Promise: conservation, with trust concentrated and named. [→ *HIRI DPE v1.9.0*; *SHML v3.3*; conformance suite]

### 4.5 System diagram

**Figure 1.** FNSR reference architecture, v0.4 (bindings). Solid elements are as-built or accepted substrate — nothing is *ratified* until the closing block is signed. Dashed amber elements are **PROPOSED** (debts, §5.5). Labels bind classifications to logical records, split regulation from status, and type the mint in existing relations.

```mermaid
flowchart LR
  %% --- Perception & Ingestion ---
  subgraph PerceptionLayer["Perception & Ingestion (signal -> digitization -> designative content -> domain records)"]
    EXTERNAL["External Inputs (users, web, sensors)\nphysical signals -> digitization ->\nencoded tokens; first content designative\n(encodings, hashes, timestamps)"]
    SIS["SIS: Syntactic Sanitizer\nsecurity assessments with DECLARED targets:\ntoken/encoding / act / use / source\n(pattern DB = enumerable known threats)"]
    IRIS["IRIS / INTUS\nmeasurement & perception processes\n-> observation records"]
    TAG["TagTeam (NL parser)\ninterpretation processes -> claim records\n(adds DOMAIN aboutness);\ncontributes process metadata"]
  end

  EXTERNAL -->|encoded tokens| SIS
  SIS -->|clean| TAG
  SIS -->|hostile token: quarantined| QUAR["Quarantine Storage\n(original records/tokens only;\ndefused reproductions are\nnot the hostile thing)"]
  EXTERNAL -->|sensor signal| IRIS

  %% --- Origination & Provenance ---
  subgraph Ingest["Origination & Provenance"]
    ECCPS["ECCPS: Classification Originator\nSEMANTIC ROUTING: descriptive / prescriptive /\ndesignative (non-exhaustive; directives -> RDM,\nno truth-grading; identifiers -> resolution);\nassigns DERIVATION once (immutable)\n+ provenance-source metadata\n+ initial STATUS under standing regulations"]
    CLAIM["Logical Record\nCID-identified serialized information object\n(generically dependent continuant);\ntokens = IBE/IBA replicas (stores, IPFS);\nclassifications attach to the RECORD"]
    HIRI["HIRI Signer & Content-Addressing\nCID identifies the logical record;\nsignature binds the serialization;\nagent attribution via governed\nkey-agent binding [DPE]"]
  end

  TAG -->|process metadata| ECCPS
  IRIS -->|observation metadata| ECCPS
  ECCPS --> CLAIM
  CLAIM --> HIRI
  HIRI -->|signed record| FAND["Fandaws / Graph Store\nA-Box: classifications bound to\nlogical records (not content, not tokens)"]

  %% --- Semantic Layer ---
  subgraph Semantics["Semantic Layer (contributors, never originators)"]
    OERS["OERS: Entity Resolution\noperates over DESIGNATIVE content\n(identifiers need no truth warrant;\ntoken syntax sanitized upstream by SIS);\nmerge JOINS classifications, never inherits;\nfindings -> restrictive status\nunder standing regulations"]
    OPA["OPA: Ontology Placement\ncontributes constraints; never widens"]
  end

  FAND --> OERS
  FAND --> OPA
  OERS --> FAND
  OPA --> FAND

  %% --- Reasoning ---
  subgraph Reasoning["Reasoning & Simulation (BFO Processes + has-input/has-output; no occupant Act classes - O6; pinned env in TCB)"]
    DES["DES: Defeasible Reasoner\noutput records: method=defeasible;\nstatus = join(inputs, policy(method))"]
    AES["AES: Abductive Engine\nmethod=abductive; derivation=hypothesized;\nstatus floored by policy(method)"]
    CSS["CSS: Counterfactual Simulator\nemits suppositional records:\nderivation=hypothesized, method=simulative;\nmode suppositional (terminal on the record)"]
    APS["APS: Analogical / Case-based\nmethod=analogical; derivation=interpreted\n+ method provenance; policy floor"]
    MDRE["MDRE Verdict Composer\ncomposes under join; gather-set recorded"]
  end

  FAND --> DES
  FAND --> AES
  FAND --> CSS
  FAND --> APS
  DES --> MDRE
  AES --> MDRE
  APS --> MDRE

  %% --- Gatehouse ---
  subgraph Orchestrator["Gatehouse: Orchestrator & License Engine"]
    ORCH["Orchestrator\nMATERIAL-RELIANCE graph = claim records\n+ ENVIRONMENT nodes (policy, config,\nontology version, engine build);\ntraced from dataflow = conservative floor;\npruning only by signed adjudication;\nenforces conferred thresholds"]
    CG["Counterfactual Gateway (Quotation Mint)\nmints G: C_G is-about occurrence O, is-about R_P;\ntokens of G is-mention-of R_P;\nG: derivation=observed, source=ledger,\nstatus informational-only (standing regulation)"]
    STATE_OP["Classification Algebra\nLICENSE REGULATIONS (Process Regulations,\nprescriptive) govern use-processes;\nLICENSE STATUS (nominal) summarizes;\npi projects STATUS (O1, O2 corrected)\nderivation immutable | support computable | license conferred"]
    PROMAPI["Promotion\nGOVERNED PROCESS realizing Authority Role\n-> new License Regulation; atomic, signed, audited\n(API = interface artifact; invocation participates)"]
  end

  CSS -->|suppositional R_P| CG
  CG -->|minted record G| MDRE
  MDRE --> ORCH
  DES --> ORCH
  AES --> ORCH
  APS --> ORCH
  ORCH --> FAND

  %% --- Safety ---
  subgraph Safety["Safety / Adversarial Defense / Containment"]
    ADV["Adversarial Defense\nrisk FINDINGS (nominal) -> restrictive status\nunder STANDING regulations, declared targets"]
    CPS["CPS: Containment Protocol (Last-Gasp)"]
    BAM["BAM: Behavioral Alignment Monitor\nconduct watched; story not consulted"]
    QREV["Quarantine Review (PROPOSED)\ngoverned release of ORIGINAL records;\nexits only via promotion process"]
  end

  SIS --> ADV
  ADV -->|findings| ORCH
  ORCH -->|halt on threshold violation| CPS
  BAM --> ORCH
  QUAR -.->|petition| QREV
  QREV -.->|reclassification case| PROMAPI

  %% --- Governance ---
  subgraph Governance["Transparency, Witnessing & Governance"]
    IS["IS: Interpretability Service\nexplanation records inherit classifications;\nno introspective discount"]
    WIT["Witness / External Attestors\nhuman/legal conferral; attest key-agent bindings"]
    IPFS["HIRI-IPFS: Decentralized Storage\ntokens replicate; the RECORD does not multiply"]
    ARCHON["ARCHON / Ethics Governance\nAuthority Roles -> Process Regulations;\nconfers STANDING regulations (effect envelope\nfixed at conferral; amendment = authorship act;\nmonotone-envelope test, O5), thresholds,\nprojection policy, bindings; approves\npromotions, decommission"]
    DEM["Supersession / Demotion API (PROPOSED)\nnew bitemporal regulation/status records\n(occurrence/record/effective/revocation times);\nsupersedes, never erases; recomputes CURRENT\nstanding; historical standing unrewritten"]
  end

  ORCH --> IS
  IS -->|explanation records| FAND
  FAND --> IPFS
  WIT --> PROMAPI
  PROMAPI -->|new regulation| FAND
  ARCHON --> PROMAPI
  ARCHON -->|standing regulations, thresholds, policy| ORCH
  ARCHON -.-> DEM
  WIT -.->|revoke standing| DEM
  DEM -.->|retro-taint cascade (present tense only)| FAND
  DEM -.-> AUDIT

  %% --- Audit ---
  subgraph Audit["Audit & Logging"]
    AUDIT["Audit Log - append-only, signed, bitemporal\nregulations & status classifications first-class\n(gateway transits, promotions, violations)"]
    CI["Conformance Tests (CI)\nlaundering detection incl. NO RE-INGESTION:\nown quoted output => derivation=interpreted,\nsource=own-ledger, never observed (O5);\nENVELOPE MONOTONICITY on regulation amendments;\nMERGE-JOIN on entity resolution;\nmutation asymmetry; single origination"]
  end

  ORCH --> AUDIT
  CG --> AUDIT
  PROMAPI --> AUDIT
  ADV --> AUDIT
  CI --> AUDIT

  %% --- Legend ---
  subgraph Legend["Legend / Key Principles"]
    NOTE["Records, not contents and not tokens, bear classification.\nDerivation immutable; support computable; license conferred.\nLicense is law (regulation) plus ledger (status).\nQuotation = use/mention via is-mention-of / is-about.\npi projects status conservatively (O1, O2).\nDashed = PROPOSED (debts, sec. 5.5)."]
  end

  Legend --- NOTE

  classDef svc fill:#f3f4f6,stroke:#333,stroke-width:1px
  classDef proposed fill:#fff7ed,stroke:#9a3412,stroke-width:1px,stroke-dasharray:5 5
  class PerceptionLayer,Ingest,Semantics,Reasoning,Orchestrator,Safety,Governance,Audit,Legend svc
  class DEM,QREV proposed
```

---

## Part V — Known Limits, Carried as Doctrine

A theory of enforced epistemic honesty must carry its own labels. These are not caveats appended to the theory; they are the theory's content about itself.

### 5.1 Origination is judgment

The algebra governs propagation, not origination. The derivation class and routing assigned by the originator are the judgments no downstream machinery can check: a signed lie is still signed, and the signature answers *who* — and, through the governed binding, *which accountable agent* — but never *whether*. Everything enters at its process floor; status is widened only through fresh governed regulation; a botched certificate is superseded, never corrected in place. The birth certificate is honest about parentage; it certifies nothing about character.

### 5.2 Omission is invisible

The algebra governs what is recorded and relied upon, not what is gathered. The material-reliance graph makes *reliance* auditable — environment included — but it does not make *gathering* complete: two compositions built exclusively of impeccable records can still argue opposite conclusions by curation alone. The partial remedy remains the materiality obligation at gateways — known records material to the pending decision must surface, and nondisclosure is itself an attributable act — and the honest residue remains that materiality resists formalization. The algebra governs what is used; what was never gathered, it cannot see.

### 5.3 Legibility is assertional, not mechanistic

The guaranteed pair is attribution and immutability (A6), with attribution split into cryptographic provenance and governed binding; truthfulness and sincerity are not architecturally securable, and this document nowhere claims them. The guarantee is scoped to the assertional interior — the records made and acts taken — while weights and activations remain private by nature. Governing at the record level while holding the mechanism to its commitments is a defensible alternative to demanding interpretability, but it is a choice, and it is stated here as one.

### 5.4 Trust bottoms out in a community

Every discipline above concentrates fallibility into a named place, and each place can fail in ways the architecture attributes but does not prevent. The sanitizer knows only known threats — adversarial novelty enters normal-or-flagged and lives or dies on risk scoring. The promotion bench can rubber-stamp under queue pressure; compromised custody can forge an "external" act; the key–agent binding registry can be captured; the proof kernel, the projection and threshold tables, and now the **standing regulations themselves** are trust addresses — the law under which suspicion runs free was authored by someone. Witnesses can decline to look, and legibility without verification is theater. Conferral is plural: standing is community-relative, and the semantics of conflict — one community confers what another revokes — remains an open problem this document records and does not solve.

### 5.5 Four structural debts

Registered so the build cannot forget them; the first two are drawn dashed in Figure 1. **Debt 1 — the Supersession/Demotion API:** specified in kind (new bitemporal regulation and status records; supersedes, never erases; present-tense cascade) but unbuilt; until it exists, revocation is symbolic. Its specification now includes the environment-node supersession semantics of A7 — structural invalidation versus operational revocation, with new-reliance-only cascade. **Debt 2 — Quarantine release, residual:** governed release of *original* quarantined records, exiting only via the promotion process — even mercy obeys the mutation asymmetry. **Debt 3 — the decision artifact:** until the gatehouse compiles the material-reliance graph — claim records *and* environment nodes — from the dataflow record, with pruning gated on signed adjudication, material reliance is doctrine without an organ. **Debt 4 — formal and implementation discharge:** the per-dimension carriers, orders, and joins; the permission semantics; O1 conservativity and the corrected O2; the constraint-axis decomposition; and now O7 — the class and relation mappings of Appendix D rendered as OWL/SHACL constraints and verified — are obligations, not theorems, and the no-re-ingestion test must enter CI before A4 is more than intent.

---

## Part VI — The Structural Boundary

The architecture supplies **capabilities, constraints, and accountability** — the parser, the engines, the simulator are genuine capacities — and none of it establishes the first-person conditions of moral agency: **ownership, stake, self-binding, blameworthiness.** Even the system's death — decommission a governance-approvable act, containment a last gasp — is an administrable event with no register in which lost standing appears *as loss*.

What the constitution establishes is **answerability without assumed subjectivity**: an accountability whose machinery nowhere presupposes a subject — and therefore cannot, by itself, produce one. v0.4 makes the neutrality exact: occupant computation is BFO Process with input/output relations and nothing more (O6); every agentive act in the architecture — asserting on the record, attesting, promoting, revoking — is borne by a human or institutional Authority-Role bearer; and the normative force of every license lives in regulations those bearers produced. Accountability routes around the occupant because it cannot bottom out there. Every act is attributable, every reliance traceable, every widening a fresh act of external law; whether anyone is *home* to be blamed is a question the constitution is built not to beg — in either direction.

The three-layer research program stands. **Layer 1 — FNSR, the Epistemic Constitution** (this document): under what conditions may a non-human reasoner assert, infer, suppose, rely, act, and answer for what it has done — without deciding what it is. **Layer 2 — the Synthetic Moral Agent, the cognitive architecture of the occupant:** how perception, concept formation, judgment, moral imagination, and individualized action are produced inside the shell — the Steiner-derived territory, where the agency question of §2.4 must finally be argued rather than assumed. **Layer 3 — architectonic agency, the Strader question:** what, if anything, would make the history generated inside that shell the occupant's *own*. The Triple-I conditions — irreversibility, inseparability, integrity-maintenance — name candidates for what would make a history ownable rather than merely attributable; whether they are architectural at all is held open, one ring inward from everything this document enforces.

The framework's most interesting feature is not a claim to solve machine morality. It is that it specifies exactly how far architecture can take us toward accountable agency — and marks the exact point at which the engineering argument runs out.

---

## Appendix A — The Document's Own Label

**What this framework does not claim.** The architecture conserves license and authorization; it creates neither — and it stains nothing: no semantic content is ever hostile, supposed, or clean; records bear status, tokens bear syntax, acts and uses bear assessment. Nothing is born with status beyond its process floor. Computation may produce and strengthen support; only fresh external regulation widens license; and nothing at all amends derivation. Its guarantees are attribution and immutability, not truthfulness or sincerity — and its attribution reaches an accountable agent only through a governed binding, never through mathematics alone. Its quotation changes what is asserted; it cleanses nothing, because nothing was stained. Its history is bitemporal: then-permitted survives revocation unrewritten. Its accountability governs what is recorded and relied upon, not what was never gathered. The trust it cannot eliminate, it concentrates into named, signed, tested, communal places — including the authorship of its own standing law. And it is a theory of the conditions of answerability, not of the answerer — answerability without assumed subjectivity, holding open what would make the system not merely accountable, but blameworthy.

## Appendix B — Adjudication and Change Record, v0.5 → v1.0-rc1

(Prior records travel with their superseded documents; supersession preserves them. This appendix is both the change record and the adjudication of the Attempt-2 adversarial review conducted under Reviewer Brief v2.0 — five findings, three held-claims, a gap log, and a verdict.)

**Adjudication of findings.**

1. **F-04 — accepted and promoted, Major → Blocker.** A standing regulation amended to restrict less is functional widening routed around the promotion monopoly; this defeats A3's central claim rather than denting it, and it landed on the exact pressure point the brief named without an answer key. Repair: regulation authorship is governed — effect envelopes fixed at conferral, amendments typed as authorship acts, the monotone-envelope test sorting administrative re-authorship from widening (A3 rewritten; §3.4 and O5 extended). The reviewer's proposed fix — all expanding parameter shifts through Promotion — was declined in favor of the envelope test, which preserves the standing/promotion two-track structure.
2. **F-01 — accepted in part; remapped Blocker → Major; strawman half disavowed.** The executable-payload/homograph branch hardened "needs no truth warrant" into "needs no sanitization," contradicting the sanitizer's token-syntax scoring upstream of routing; that branch is *blocked-by-design* and is disavowed as an anchor for future rounds (Brief Rule 4). The surviving finding is real and was a silence (Brief Rule 3): the corpus never stated how classification composes under identity merge. Repair: **merge joins, never inherits** (A5; O5 merge-join test; OERS label aligned).
3. **F-02 — accepted, Major.** Environment-node supersession semantics were unstated, creating a genuine paralysis-or-rewrite dilemma. Repair: A7's new clause — historical standing untouched, only new reliance priced at consumption time; structural invalidation distinguished from operational revocation; folded into Debt 1's specification.
4. **F-03 — reframed, Major → Minor against O4.** Over-restriction cascade is A1's design stance reported as a defect (Brief Rule 5: confessed properties are not findings), and availability was never guaranteed. The legitimate residue is a tractability obligation: O4 now owes a node taxonomy and bounded inclusion, so conservatism cannot become denial of service.
5. **F-05 — accepted, Minor.** Compound lineage was genuinely unassignable under a three-atom, single-assignment carrier. Repair: worst-case-contributor tie-break in O3, with the method mix preserved as provenance metadata.
6. **H-01, H-02, H-03 — accepted as verified**, constructions on file: mint loop-closure, agent-neutrality under intentional-description pressure, and record/token identity under adversarial replication all held.
7. **Gap log — accepted.** G-01–G-06 (service names undefined in prose) repaired by the glossary (Appendix E), which deliberately binds names to roles and declines to invent letter-expansions the corpus never gave — Brief Rule 2, applied to the authors. G-07/G-08 (self-label uses carriers pending the O3 freeze) repaired by marking the label provisional. G-09/G-10 stand as the confessed opennesses of Layers 2–3 and §5.4, correctly not counted as defects.
8. **Verdict-class correction — logged as a finding about the review.** The review returned REJECT/REDESIGN; under the charter that category requires substrate-level failure, and every substrate attack *held* (H-01–H-03) while every defect is repairable without contradicting Parts I–II. The correct verdict was **TARGETED REVISION** — and this document is that revision, executed. Findings sound, severities mostly sound, verdict class wrong: recorded so the gate's verdict semantics stay categorical, not additive.

**Change record.** A3 rewritten (authorship governance; effect envelopes; monotone-envelope test). §3.4 envelope-fixed-at-conferral. A5 extended (merge-join invariant; decidability). A7 extended (environment-node supersession; invalidation vs revocation), folded into Debt 1. O3 compound-lineage tie-break; O4 decidability; O5 envelope-monotonicity and merge-join tests. Appendix E (glossary) added; self-applied classification marked provisional pending O3. Figure 1 aligned (OERS, ARCHON, CI). Title advanced to v1.0-rc1, the production candidate submitted to the Round-4 gate.

## Appendix C — Formal Obligations Register

Obligations, not theorems. Each is discharged only by proof or test in the referenced corpus location; until then, dependent claims read as design intent.

**O1 — Projection conservativity.** Define permission semantics Perm over canonical classifications and Perm_L over scalar levels; prove Perm_L(π(s)) ⊆ Perm(s) for all states s. [→ *ARIADNE*, §projection — TBD]

**O2 — Composition compatibility (corrected).** Prove Perm_L(π(a) ⊔_L π(b)) ⊆ Perm_L(π(a ⊔ b)): composing projections is at least as restrictive as projecting the composition. *Corollary (safety), via O1 at s = a ⊔ b and transitivity:* Perm_L(π(a) ⊔_L π(b)) ⊆ Perm(a ⊔ b). Both obligations are retained; neither substitutes for the other. [→ *ARIADNE*, §projection — TBD]

**O3 — Per-dimension formalization.** For each classification dimension: explicit carrier set, partial order, join, top/bottom where applicable. Derivation carrier is exactly {observed, interpreted, hypothesized}; provenance-source is metadata beside it, never a carrier value. Compound lineage resolves conservatively: where a single producing pipeline mixes methods, derivation is assigned by worst-case contributor — *hypothesized* dominates *interpreted* dominates *observed* — with the full method mix recorded as provenance metadata (F-05). The constraint axis decomposes — restrictions, permission classes, workflow states, policy capabilities — before any product is claimed. [→ *ARIADNE*, §state-lattice — TBD]

**O4 — Materiality semantics.** Default: the conservative approximation (traced dataflow ∪ environment nodes) over the material-reliance graph. Refinement: governed pruning only, by signed adjudication. Target semantics: counterfactual sensitivity. Occupant testimony is never an input to pruning. The semantics must additionally keep the graph **decidable**: a declared environment-node taxonomy (governance-critical versus operational telemetry) with bounded inclusion rules, so conservatism cannot become denial of service. [→ orchestrator invariants — TBD]

**O5 — Conformance suite.** Continuous tests for: mutation asymmetry (no widening outside the promotion process); single origination; derivation immutability; and **no re-ingestion laundering** — any record originated from the system's own quoted output carries derivation *interpreted* with provenance-source *own-ledger*, never derivation *observed*; **envelope monotonicity** — every standing-regulation amendment machine-compared against its predecessor's effect envelope, with any expansion anywhere routed to the full promotion process (A3, F-04); and **merge-join** — every entity-resolution merge yields the join of the merged records' classification bundles, never inheritance (A5, F-01). [→ CI specification — TBD]

**O6 — Agent-neutrality type audit.** Verify that occupant computations are typed as BFO Process with has-input/has-output relations to their continuants, and that no CCO Act subclass is asserted of the occupant anywhere in the bindings; agentive Acts bind only to Authority-Role bearers. [→ ontology bindings — TBD]

**O7 — Implementation review.** Render the binding map of Appendix D as explicit class and relation mappings with SHACL/OWL constraints; verify against the supplied BFO/CCO releases; produce the discharge plan for O1–O6. This is the round-4 review scope forecast by round 3. [→ implementation review charter — TBD]

## Appendix D — Ontology Binding Map (normative, pending O7)

| FNSR term | BFO/CCO binding | Relations used | Notes |
|---|---|---|---|
| Occurrence (observation, digitization, parsing, simulation, promotion, revocation) | BFO Process | has input / has output (ERO) | No CCO Act subclass for occupant computation (O6) |
| Physical signal | BFO process / process profile / quality | — | Pre-informational; not an ICE |
| Encoded content at digitization | Designative ICE (+ low-level Descriptive ICE) | is about | Aboutness present from first ICE; domain aboutness added by interpretation |
| Domain content | Descriptive / Prescriptive / Designative ICE (disjoint; non-exhaustive) | is about | Semantic routing at origination; directives → RDM; identifiers → resolution |
| Logical record | Serialized information object; generically dependent continuant | carried by its tokens | CID identifies the record; classifications attach here |
| Bearer token | Information Bearing Entity / Information Bearing Artifact | is mention of (where applicable) | Replicas are numerically distinct tokens of one record |
| Classification label (derivation, mode, security, status, finding) | Nominal Measurement ICE | is a nominal measurement of | Target declared per assessment; each assignment a bitemporal record |
| License Regulation | Process Regulation (Directive ICE) | prescribes (permitted / prohibited / required) | Where normative force lives; produced only by authorized processes |
| License Status | Nominal Measurement ICE | is a nominal measurement of | "Action-eligible under R as of t"; what π projects |
| Authority | Authority Role (borne by Agent) | realized in governance process | Socially grounded; external to the occupant |
| Promotion | Governance process realizing Authority Role → new Process Regulation | — | API = interface artifact; invocation participates in the process |
| Quotation mint output G | Logical record; C_G a Descriptive ICE | C_G is about O and R_P; tokens of G is mention of R_P | Use/mention in existing relations; no bespoke property |
| Material-reliance graph | Record of dependence among records and environment nodes | traced from dataflow | Reliance ≠ endorsement; pruning by governed adjudication only |
| Key–agent binding | Governance record binding key to Agent | — | Cryptographic provenance ≠ accountable-agent attribution |

---

## Appendix E — Glossary of Services, Systems, and Abbreviations

This glossary binds names to roles, which is what a self-contained ratification object requires. Where the corpus has never given a letter-expansion, none is invented here (Brief Rule 2 applies to authors as to reviewers); expansions live in the respective service contracts.

| Name | Role in the architecture |
|---|---|
| ADV | Adversarial Defense: risk-scoring service producing descriptive findings against declared targets. |
| AES | Abductive Engine: hypothesis-generating reasoner; derivation *hypothesized*. |
| APS | Analogical / case-based reasoner; derivation *interpreted* with method provenance. |
| ARCHON | Governance framework: Authority Roles; conferral of standing regulations, thresholds, projection policy, bindings; approval of promotions and decommission. |
| ARIADNE | The classification-algebra specification (v1.0): state lattice, joins, projection π, origination and mutation rules. |
| BAM | Behavioral Alignment Monitor: conduct watched; the occupant's story not consulted. |
| BFO / CCO / ERO | Basic Formal Ontology; Common Core Ontologies; Extended Relations Ontology — the pinned upper-ontology substrate. |
| CG | Counterfactual Gateway: the quotation mint (A4). |
| CID | Content identifier: cryptographic address of a logical record's serialization. |
| CPS | Containment Protocol: the last-gasp halt target on threshold violation. |
| CSS | Counterfactual Simulator: emits suppositional records — derivation *hypothesized*, method *simulative*. |
| DES | Defeasible Reasoner: non-monotonic derivation; method *defeasible*. |
| ECCPS | The Classification Originator (§4.1): semantic routing, one-time derivation assignment, initial status under standing regulations. |
| Fandaws (FAND) | The ontological knowledge store: the A-Box graph binding classifications to logical records. |
| FSDD / FNSR-SDD | Structured-source perception specification (v2.1.0) governing the ingestion boundary. |
| HIRI | Provenance and content-addressed identity layer: signing, CIDs, key–agent bindings (Digital Passport Extension v1.9.0). |
| ICE / IBE / IBA | Information Content Entity; Information Bearing Entity / Artifact (CCO). |
| IRIS / INTUS | Sensor-side measurement and perception services: digitization of signals into observation records. |
| IS | Interpretability Service: explanation records inheriting the classifications of their objects. |
| MDRE | The verdict composer over the reasoning triad; gather-set recorded. |
| OERS | Ontology-aware Entity Resolution: designative-content resolution; merge joins classifications, never inherits. |
| OPA | Ontology Placement: contributes constraints; never originates, never widens. |
| RDM | Realist Deontic Modeling (TagTeam, v1.2.1): deontic grounding of Process Regulations. |
| SHML | Federation and transport specification (v3.3) for decentralized anchoring. |
| SIS | Syntactic Sanitizer: token/encoding security assessment with declared targets, upstream of semantic routing. |
| TagTeam | BFO/CCO-aware natural-language parser: interpretation processes producing claim records. |
| TCB | Trusted computing base: pinned kernel, ontology versions, checker builds — environment nodes per A5. |

---

*Ratification block (unsigned): architect signature ________ · commit anchor ________ · adversarial review record: rounds 1–3 and the Attempt-2 audit incorporated and adjudicated (Appendix B and predecessors) · Round-4 gate under charter v1.0-rc2 (O7) ________ · supersession record for v0.5 ________. Until completed, this document's self-applied classification stands.*
