# FNSR Ontological Possibility Space (OPS)

## Manifest-Indexed Concept Addressing, Bounded Navigation, and Grounded Completion

### Formal Research Specification

| Field | Value |
|---|---|
| Document ID | FNSR-OPS-SPEC |
| Version | **v0.6 — RATIFICATION CANDIDATE (third issue)** |
| Date | 2026-08-26 |
| Drafted by | Claude, under delegated authoring |
| Ratification authority | Ratifying Architect, FNSR |
| Methodology | Falsifiable Spec (house standard) |
| Normative language | RFC 2119 (SHALL / SHOULD / MAY) |
| Supersedes | FNSR-OPS-SPEC v0.5 and all prior versions; informal proposal *"A Universal Ontological Possibility Space"* |
| Review state | BFO-ontologist sign-off conditional on the four v0.5 repairs — incorporated herein; submitted to the original reviewer for final sign-off |

**Terminology notes.** *Signature* unqualified always means the logical signature Σ; cryptographic signatures are always so qualified. OPS-generated nodes are **logical class-expression equivalence classes**; the words *concept*, *universal*, and *category* are reserved for entities carrying an assertion per §8 — see the object discipline of §1.3.

### Change Record

| Version | Date | Change |
|---|---|---|
| v0.1–v0.4 | 2026-08-26 | Initial formal recut and three external review rounds. Findings R-01–R-40. |
| v0.5 | 2026-08-26 | Fourth external review incorporated; OI-6a CCO verification executed (Appendix B). Findings R-41–R-44. |
| v0.6 | 2026-08-26 | **Fifth review (BFO ontologist, final pass on v0.5) incorporated; third-issue ratification candidate. Findings R-45–R-48: all four accepted (Appendix A).** Headline repairs: **INV-9 operative-theory consistency** — no manifest becomes operative, issues addresses, or serves as a migration target unless T is consistent; the Consequence Preview and consistency gate now govern *every* candidate successor manifest, retirements included; the false "role axioms become vacuous" claim is withdrawn, with the reflexivity counterexample and subrole-emptiness propagation recorded (D-2.1(3), §9.3, FC-1(vi)). **FP re-founded** — the v0.2–v0.5 collision story was backwards: because the record embedded the TBox-free reduced form, cross-class FP collision was provably impossible, while one T-class could carry many FPs; FP is now $H(fid \| nfv \| TheoryID \| reduce_{\emptyset}(C))$, a stable **expression locator** with an explicit aliasing (not collision) model, and the classification-signature record becomes a separate, snapshot-indexed contextual artifact (D-6.1, D-6.2, FC-1(iii) recast as an alias-multiplicity metric, §7.5). **Identity epochs** — fid and nfv are now first-class continuity constituents: added to the manifest envelope and PinnedRef; NORMAL_FORM_REINDEX and FRAGMENT_MIGRATION defined; EQUIVALENT_REAXIOMATIZATION's 1:1 implication scope-conditioned on an unchanged epoch (§7.4, D-3.2, D-9, RP-16). **D-1.1 patched** to name the OWL 2 EL-specific property-chain/range restriction. Phase-1 entry set: RP-2A, RP-8–RP-13, RP-15, **RP-16**. |

---

## 1. Purpose and Scope

### 1.1 Mission statement

This specification defines a research program and candidate FNSR component for constructing, addressing, and navigating the space of satisfiable class descriptions expressible in a restricted, decidable ontology fragment, relative to a fixed signature and a versioned background theory.

The mission of OPS is **completion and alignment**, not discovery of new ontological primitives:

- **Completion.** Surface satisfiable, currently unnamed class-expression equivalence classes — meets, intermediate abstractions, bounded refinements — within an existing signature, ranked for plausible meaningfulness, and submitted to the Ontology Admission Gate (§8.4) for human ratification and naming.
- **Alignment.** Provide stable, manifest-indexed canonical addresses such that classes from independent ontologies sharing a canonical manifest (or manifests certified equivalent, D-3.2) resolve to common locations, and provide a governed pipeline for proposing, previewing, ratifying, and coalescing the bridge axioms that address coalescence requires.
- **Manifest-indexed identity, explicit continuity under drift.** Provide identity that is honest about its index: addresses bound to a versioned canonical manifest within an identity epoch (§7.4), plus migration semantics that make semantic continuity — and its failures (MERGE_WITNESSED, SPLIT_WITNESSED, BECAME_UNSATISFIABLE, NON_REGROUNDABLE) — explicit and auditable. OPS does not claim that identity always survives change; it claims that what happened to identity is always demonstrable, and that what is *not* demonstrable is always marked as such. This is the substrate requirement of §2.3.

### 1.2 Scope exclusions

The following are explicitly out of scope. These exclusions are normative; marketing or downstream documentation SHALL NOT contradict them.

- **SE-1 (No enumeration of reality).** OPS characterizes what a formal theory permits, never what the universe contains. Logical satisfiability confers Logical status *SATISFIABLE* (§8) and nothing more.
- **SE-2 (No primitive discovery).** The space contains only constructor-closures of the chosen signature Σ. OPS cannot originate a missing primitive; it can at most report, after differential diagnosis, that grounding evidence resists Σ-expression (§5.3). The naming of new primitives remains human ontological work.
- **SE-3 (No probabilistic structure).** Embedding-based and statistical components are advisory only. They SHALL NOT create, delete, or modify nodes, edges, addresses, or overlay assertions (INV-2).
- **SE-4 (Address ≠ endorsement).** Possession of a canonical address or fingerprint confers no ontological, scientific, or FNSR-governance standing.
- **SE-5 (No automatic classhood).** No OPS process — generation, ranking, grounding, or co-location — confers OPS assertion; only the Ontology Admission Gate (§8.4) does, and it governs exactly the transition UNNAMED → OPS_ASSERTED. Source assertions are *observed* via faithful projection (§8): never conferred, never gated, and never revoked by OPS.

### 1.3 Object discipline

OPS traffics in five distinct kinds of thing, and no interface, report, or document SHALL conflate them:

| # | Object | What establishes it | OPS construct |
|---|---|---|---|
| 1 | A satisfiable class description | The reasoner, relative to a manifest | An expression with Logical = SATISFIABLE |
| 2 | A logical class-expression equivalence class | Canonicalization under the manifest | A node of 𝒰 (D-4) |
| 3 | An empirically instantiated description | The evidence layer, under admission criteria | Grounding = EVIDENCE_SUPPORTED (§8) |
| 4 | Information artifacts standing for a class | The Canonicalizer | ADDR (designates the canonical representative N(C)); FP (designates the ∅-reduced expression, an alias-prone locator); the classification-signature record (snapshot-indexed description) — per §7.5 |
| 5 | A class asserted in an ontology | A source ontology's own assertion, faithfully projected; or the Ontology Admission Gate | Naming = SOURCE_ASSERTED or OPS_ASSERTED (§8) |

Movement rightward down this table is never automatic. A conjunction can be satisfiable, instantiated, useful to a classifier, and still pick out an accidental collection rather than anything warranting a named class; objects 1–4 SHALL NOT be called concepts, universals, or categories.

---

## 2. Position within FNSR

### 2.1 Inherited commitments

OPS inherits and SHALL conform to the standing FNSR commitments:

1. **BFO 2020 / CCO grounding.** BFO 2020 is the primary projection target (Phase 4); CCO's Extended Relations Ontology enters the Phase 0 audit (§9.1, RP-13), with broader CCO scaling under OI-4. This commitment is reflexive: OPS's own artifacts are characterized within CCO's information-entity machinery (§7.5, INV-8), against verified IRIs (Appendix B).
2. **Edge-Canonical First.** The reasoner core, canonicalizer, and frontier generator SHALL run unmodified in browser and Node.js. Consequence: no dependence on JVM reasoners (e.g., ELK). An edge-canonical EL-family reasoning core is therefore a first-class deliverable, not an integration detail (OI-1).
3. **HIRI conventions.** Theory manifests, migration artifacts, and pinned reference records are content-addressed, Ed25519-signed artifacts (§7), with digest values self-describing per D-10 — the same multihash convention that underlies the SHML/IPFS federation layer.
4. **Falsifiable Spec methodology.** Every load-bearing claim in this document is bound to a falsification condition with an operational threshold (§15). Thresholds marked ⚠ are calibrated at the phase gates named in OI-3.

### 2.2 Candidate consumers

The following integrations are identified as candidates. None is binding until the respective spec owner ratifies an interface.

- **OCE (Ontological Constraint Engine):** constraint queries keyed by canonical address rather than IRI, eliminating label-dependence in constraint targeting.
- **BCCS:** the signature-normalization problem under ratification there and the OPS normal form (§6.2) are the same species of problem (RP-7); additionally, the Ontology Admission Gate criteria (§8.4) are candidate material for BCCS-adjacent conformance rules.
- **TagTeam.js:** candidate verbalization/parsing bridge for the round-trip requirement of §10.4.
- **SHML / IPFS federation:** transport and federation of addresses, manifests, migration artifacts, and reference records; D-10's self-describing digests are chosen for direct compatibility.
- **CTS (Commitment Tracking Service):** re-grounding of commitments across theory evolution. **Doubly gated:** CTS integration requires ADDR-grade identity (§6.2, RP-2A/2B) *and* continuity-grade references (D-9); it SHALL remain disabled under FP-only operation or over locator-grade pins.

### 2.3 Rationale relative to the singular project

A synthetic moral person under the Triple-I Standard must maintain the integrity of its commitments over time. A commitment is only as determinate as the concepts it quantifies over. If those concepts are identified by mutable labels, or by addresses that silently change meaning when the background theory evolves, then Integrity-Maintenance is unverifiable in principle: the person cannot demonstrate that the commitment it honors today is the commitment it made.

OPS does not promise that identity *persists* under theory drift — witnessed merges, witnessed splits, and expressions that become unsatisfiable are precisely the documented cases where it does not. OPS promises **traceable semantic continuity**: manifest-indexed identity within a declared epoch (§7.1, §7.4), provenance-bearing references (§7.3), and migration semantics whose honest outcomes include NON_REGROUNDABLE and whose event annotations are explicitly witness-qualified. Integrity is served not by pretending persistence but by being able to demonstrate, for every commitment, exactly what happened to its conceptual content when the theory changed — including the cases where the only true answer is that continuity could not be established, and the cases where the only honest event label is *no change witnessed*. A moral person that can show where its commitments' contents changed, and where its knowledge of those changes runs out, is more integral, not less, than one whose identity substrate papers over drift. FC-7 makes this claim falsifiable against CTS scenarios — split scenarios mandatory — before any consumer integration.

---

## 3. Invariants

- **INV-1 (Determinism).** Given identical inputs (fid, Σ registry state, TheoryID, C, bounds, mode, strategy version), a conformant implementation SHALL produce byte-identical canonical output on every conformant host, including deterministic EXP expansion and tie-breaking per the canonical total order. Conformance is demonstrated by the dual-host equivalence suite (§11.3).
- **INV-2 (Reasoning authority).** Only the deterministic reasoning core determines satisfiability, equivalence, and subsumption. Probabilistic components order candidates and propose bridges; they SHALL NOT alter structure.
- **INV-3 (Manifest indexing).** Every address SHALL bind a TheoryID. An address lacking TheoryID binding is invalid and SHALL be rejected by all conformant consumers. TheoryID is manifest identity, not semantic theory identity (§7.1); no component SHALL present it otherwise.
- **INV-4 (Coalescence by ratified bridge only).** No two previously distinct canonical addresses SHALL be made equivalent on the basis of overlay, lexical, embedding, or evidence similarity alone. Address coalescence requires ratified bridge axioms incorporated into a new theory manifest, and is executed as a witnessed-merge migration under §7.3. Ordinary **co-location** — two overlays' formal definitions over the shared manifest canonicalizing to the same existing address — is not coalescence, requires no bridge, and is graded per D-8.
- **INV-5 (Status discipline).** Every node surfaced by any interface SHALL carry its full epistemic status tuple (§8), including assertion provenance. No interface SHALL present a SATISFIABLE node in a manner suggesting asserted or EVIDENCE_SUPPORTED standing, and no dimension of the tuple SHALL be suppressed in presentation.
- **INV-6 (Edge-canonical core).** Per §2.1(2).
- **INV-7 (Grade separation).** A fingerprint (FP, D-6.1) SHALL NOT be presented as, converted into, or consumed in place of a canonical address (ADDR, D-6). FP and ADDR values SHALL be syntactically distinguishable per the D-10 value grammar. Identity-dependent consumers SHALL reject FP-grade inputs.
- **INV-8 (Ontological self-conformance).** OPS meta-artifacts — addresses, fingerprints, signature records, manifests, reference records, migration artifacts, reports — SHALL be characterized within BFO/CCO using existing CCO relations per §7.5, with each artifact's characterization consistent with its formal role. No new object properties SHALL be minted for meta-description.
- **INV-9 (Operative-theory consistency) *(new v0.6)*.** A SignedTheoryManifest SHALL NOT become operative unless T is consistent — mechanically checkable in EL⊥ as $T \not\models \top \sqsubseteq \bot$, a polytime entailment test. Inconsistent candidate successor theories MAY be analyzed diagnostically (including justification extraction for the entailment of $\top \sqsubseteq \bot$) but SHALL NOT issue addresses, serve as migration targets, or be presented as operative. Every candidate successor manifest — bridge incorporation, symbol retirement, or ordinary axiom change — passes the Consequence Preview and this consistency gate before activation (§9.3, D-2.1(3)). Gated at FC-1(vi).

---

## 4. Definitions

- **D-1 (Fragment F — concept language).** Default: **EL⊥** — conjunction, existential restriction, ⊤, ⊥ — with general concept inclusions (GCIs), supporting disjointness via axioms of the form $A \sqcap B \sqsubseteq \bot$. Subsumption in this family is polynomial-time w.r.t. general TBoxes. Escalation to ELI (inverse roles) is a ratification decision (RP-1) because it forfeits tractability: subsumption in ELI w.r.t. GCIs is ExpTime-complete.
- **D-1.1 (Fragment F — role-axiom sub-fragment) *(rev. v0.6)*.** The fragment is not a concept language alone; the role-axiom sub-fragment SHALL be specified with the same precision, because CCO's semantics are heavily role-axiom-dependent. Default admitted role axioms, per the OWL 2 EL profile: role hierarchy ($r \sqsubseteq s$), property chains ($r \circ s \sqsubseteq t$, **subject to the OWL 2 global restrictions, including the OWL 2 EL-specific property-chain/range restriction**, transitivity as the special case), and domain/range in their EL-encodable forms. Excluded pending RP-1: inverse role declarations. The Phase 0 audit SHALL report role-axiom survival per axiom type with the same discipline as concept-axiom survival (§9.1). Preserving CCO's class syntax while silently destroying its relational semantics is a named failure mode, gated by FC-4.
- **D-2 (Signature Σ).** A finite, versioned vocabulary of primitive concept names and role names. Σ is a human artifact and is declared as such (§5). Every primitive symbol carries an **opaque, stable symbol identifier**; human-readable labels are annotations on symbols (§7.2). Renaming a label never changes a symbol; a new symbol is a new identifier.
- **D-2.1 (Symbol registry lifecycle) *(rev. v0.6 — retirement as governed theory change)*.** The logical symbol registry is **append-only**:

  1. A symbol identifier, once registered, is never removed from the operative signature, and never changes kind — a concept-to-role change (or the reverse) is a *new* identifier.
  2. Lifecycle governance is annotation-level: a symbol MAY be marked **deprecated** by a signed governance event, which affects presentation, ranking, and Admission Gate warrant judgments — never well-formedness.
  3. **Semantic retirement is a governed theory-change proposal, typed by symbol kind.** For a **concept symbol** S: propose $S \sqsubseteq \bot$. For a **role symbol** r: propose $\exists r.\top \sqsubseteq \bot$, which forces the role's extension empty; this is an ordinary GCI admitted by the default EL⊥ fragment. In EL every occurrence of a symbol is positive, so under either retirement axiom every expression containing the retired symbol becomes unsatisfiable and flows through the *existing* migration machinery as BECAME_UNSATISFIABLE, with full successor/event discipline. **Retirement propagates through T and can render a candidate theory inconsistent** — the v0.5 claim that role axioms mentioning a retired role become vacuous is **withdrawn**: a subrole $s \sqsubseteq r$ is forced empty alongside r (a real downstream consequence, not vacuity), and a reflexivity axiom on r yields outright inconsistency, since every individual would require the r-successor that retirement forbids. Accordingly, every retirement proposal SHALL pass the Consequence Preview — surfacing forced emptiness, newly unsatisfiable classes, and competency-set impact — and the INV-9 consistency gate before the successor manifest activates; a retirement that entails $\top \sqsubseteq \bot$ (as the reflexivity case does, unless the conflicting axiom is removed in the same change) SHALL NOT activate. **Conditional-support clause:** under any ratified fragment variant that does not admit the $\exists r.\top \sqsubseteq \bot$ pattern, semantic retirement of role symbols is unsupported — only deprecation is available — and that fragment's ratification SHALL state so explicitly. Under the default fragment, signature drift thereby reduces to *governed* theory drift, for both symbol kinds, and §7.3 and INV-9 together govern it.
  4. A **SigmaID** — the D-10 digest of the registry state (the ordered set of symbol identifiers and kinds) — is bound into the SignedTheoryManifest *envelope*, not into TheoryID or ADDR, preserving D-3.1's conservative-extension stability while making every manifest explicit about its operative registry.
  5. **Consequence:** a continuity-grade sourceExpression is well-formed over every later registry state; conformant signature evolution cannot orphan a reference syntactically. **Defensive outcome:** a conformant system encountering an expression containing an identifier absent from its operative registry SHALL classify it **NON_EXPRESSIBLE_UNDER_SIGNATURE** in the successor field — flagged, never silently repaired — an outcome unreachable through conformant operation but specified so that non-conformant states fail loudly.
- **D-3 (Theory T, TheoryID, and signed manifest) *(rev. v0.6)*.** T is a finite set of F-axioms over Σ (concept and role axioms alike). The **canonical theory payload** is exactly: the axioms of T in normal form, sorted under the canonical total order, with imports pinned by content hash — and nothing else. No cryptographic material, no signer metadata, no bare Σ declarations (D-3.1).

$$
TheoryID = H(\text{canonical theory payload})
$$

  with H per D-10. The **SignedTheoryManifest** is the envelope: { TheoryID, SigmaID, **fid, nfv**, signerID, Ed25519 cryptographic signature, metadata } — the epoch constituents fid and nfv are named explicitly (§7.4). Cryptographic signatures authenticate a manifest; they never constitute address content. Per INV-9, a manifest SHALL NOT become operative unless its theory is consistent.
- **D-3.1 (Σ binding).** Bare signature declarations are excluded from the canonical theory payload. In EL⊥, extending Σ with new symbols and no axioms is a conservative extension: it cannot change equivalence or subsumption among existing concepts, and SHALL NOT perturb existing addresses. Axioms mentioning new symbols enter the payload as axioms and change TheoryID in the ordinary way. Registry evolution beyond extension is governed by D-2.1.
- **D-3.2 (Manifest-equivalence certificate) *(rev. v0.6 — epoch-conditioned)*.** TheoryID identifies a canonical manifest, **not** a logical theory up to semantic equivalence: adding a redundant axiom, or re-presenting T in a logically equivalent axiomatization, changes TheoryID — and therefore every ADDR — while leaving the equivalence relation over the operative concept language untouched. OPS does not hide this; it certifies it. Because mutual TBox entailment is decidable in polynomial time in EL⊥, the Theory Manifest Service SHALL compute a **manifest-equivalence certificate** on every migration. **When the certificate holds *and the identity epoch (fid, nfv, hv) is unchanged*** (§7.4), the migration is classified **EQUIVALENT_REAXIOMATIZATION**: every address re-indexes 1:1, every event annotation is *definitively* NO_CHANGE, and consumers MAY follow the re-indexing automatically. When the certificate holds but an epoch constituent also changes, the migration decomposes into the epoch transition plus the certified theory step, each with its own record (§7.4). The stronger notion — a canonical representative of a theory *up to logical equivalence* — is deferred (OI-8) and never implied as solved.
- **D-4 (The space 𝒰).**

$$
\mathcal{U}_{F,\Sigma,T} \;=\; \bigl\{\, [C]_{\equiv_T} \;:\; C \in \mathcal{C}(F,\Sigma),\; C \not\equiv_T \bot \,\bigr\}
\quad\text{ordered by}\quad
[C] \preceq [D] \iff T \models C \sqsubseteq D .
$$

  This is the satisfiable fragment of the **Lindenbaum–Tarski algebra** of T over 𝒞(F,Σ). Its elements are **logical class-expression equivalence classes** — object 2 of §1.3 — and nothing more.
- **D-5 (Order-structure caveat).** Under nonempty T with GCIs, (𝒰, ⪯) is a partial order and **is not in general a lattice**: least common subsumers need not exist under general GCIs. Role-depth-bounded common subsumers exist at each bound, but they are approximations relative to that bound — they need not converge to a join as the bound grows, and no claim of "recovering" lattice structure is made. Distributivity, grading, and neighborhood results for EL concept descriptions (the Kriegel line) are **TBox-free** results and SHALL NOT be assumed for nonempty T.
- **D-6 (Canonical address — identity grade).**

$$
ADDR(C) \;=\; H\bigl(\, fid \;\|\; nfv \;\|\; TheoryID \;\|\; N_{F,\Sigma,T}(C) \,\bigr)
$$

  with H and framing per D-10, where N is the **globally canonical** representative of $[C]_{\equiv_T}$ under the normative well-order (§6.2, property 5) — an intrinsic object, independent of any search, frontier, or canonicalization envelope. **Issuance rule:** ADDR SHALL be issued only where global canonicality has been *certified* (§6.2); expressions beyond the certifiable size threshold receive FP only. An issued ADDR can never change under envelope growth — bound-invariance holds by construction, gated at FC-1(iv). Uniqueness of *identification* is governed by D-10: it holds under the collision-resistance assumption, fail-closed, never as mathematical injectivity. ADDR is the sole identity-grade object in OPS, it is **manifest-indexed identity within its epoch** (D-3.2, §7.4), and ontologically it is a designator of the canonical representative ICE (§7.5).
- **D-6.1 (Fingerprint — expression locator, re-founded) *(rev. v0.6)*.** The fingerprint of an expression C is the digest of its **TBox-free reduced form**:

$$
FP(C) \;=\; H\bigl(\, fid \;\|\; nfv \;\|\; TheoryID \;\|\; reduce_{\emptyset}(C) \,\bigr)
$$

  with H and framing per D-10 (domain tag `ops/fp`), where $reduce_{\emptyset}$ is the canonical ∅-reduced normal form under the §6.2 well-order. Two properties follow, and they **invert the collision story this specification carried from v0.2 through v0.5**:

  1. **No cross-class collision.** For EL⊥, reduced forms are canonical for empty-TBox equivalence: $reduce_{\emptyset}(C) = reduce_{\emptyset}(D) \Rightarrow C \equiv_{\emptyset} D \Rightarrow C \equiv_T D$ for every T. One FP therefore maps into exactly one T-equivalence class; two genuinely non-equivalent classes **cannot** share an FP (setting aside D-10 digest collisions, which are fail-closed).
  2. **Aliasing, not collision.** The failure direction is the opposite one: $C \equiv_T D$ with $C \not\equiv_{\emptyset} D$ yields $FP(C) \neq FP(D)$ — **one T-class may carry many FPs**, because T makes ∅-distinct expressions equivalent. FP is thus a stable **noncanonical expression locator**: an alias-prone handle on a particular reduced expression, never class identity. INV-7 stands, now for the correct reason. Consequence for FP-only operation: merge detection SHALL use reasoner equivalence, with FP equality as a sufficient-but-not-necessary fast path.

  FP quality in FP-only mode is measured as **alias multiplicity** (FC-1(iii)) — the distribution of distinct FPs per T-class — not as a collision rate; the retired collision metric measured a provably impossible event. Where the FP's preimage payload ($reduce_{\emptyset}(C)$) is retained in the content-addressed store, an FP-bearing pin MAY be upgraded to continuity-grade by payload retrieval; retention is not guaranteed, so continuity-grade status still requires the embedded sourceExpression (D-9).
- **D-6.2 (Classification-signature record — contextual artifact) *(new v0.6)*.** The classification of an expression against currently named classes is **not** part of FP, because assertion sets change without TheoryID changing — a new overlay projection or a gate admission would otherwise silently alter fingerprints. The **classification-signature record** is a separate, signed, content-addressed artifact (domain tag `ops/csr`), indexed by

$$
\langle\, FP,\; ReferenceSetID,\; bounds,\; AssertionSnapshotID \,\rangle
$$

  whose content is the set of subsumption statements locating the FP's reduced expression relative to the reference class set at that snapshot. **AssertionSnapshotID** is the D-10 digest of the ordered active assertion-record identifiers at issue time; **ReferenceSetID** identifies the chosen reference class set (default: all active assertions at the snapshot). Records are reissued under new snapshots, never retroactively edited. The three-tier model, stated once: **ADDR** — canonical identity of the T-class; **FP** — stable locator of a particular reduced expression, possibly one of several aliases for the class; **classification-signature record** — mutable-by-reissue, context-indexed description of where that expression lies among currently named classes.
- **D-7 (Bounded frontier — two modes).** For direction ↓ (specializations; ↑ symmetric): $Frontier_{\downarrow}(C;\, d, s, c, b, k)$ with **d** = maximum role depth, **s** = maximum normalized expression size, **c** = maximum conjunct count, **b** = maximum candidate evaluations, **k** = maximum returned results. k bounds output; b bounds work; d, s, c bound the candidate grammar. Two modes: **EXH (exhaustive-bounded)** — complete enumeration of the finite grammar $\mathcal{C}(F, \Sigma', d, s, c)$, permitted only within the ratified EXH envelope (OI-7); a completeness claim is licensed in this mode and only in this mode. **EXP (exploratory)** — deterministic best-first refinement search under budget b, expansion and tie-breaking per the canonical total order (INV-1); returns the best k found within b; **no completeness claim**; results labeled with (b, strategy version). In both modes, every returned node is satisfiable and every returned edge entailed; returned nodes are maximal under ⪯ **among evaluated candidates**. Frontiers are never claimed covers (§6.3). Frontier envelopes are *operational* bounds and play no role in identity (D-6).
- **D-8 (Overlay — with projection grades).** A mapping

$$
P_O : Classes(O) \rightarrow \mathcal{U}_{F,\Sigma,T}
$$

  from an ontology's named classes **into class-expression equivalence classes** — the codomain is 𝒰, per §1.3; the corresponding designator is $ADDR(P_O(X))$ (or FP in FP-only mode), supplied by the Canonicalizer. Overlays carry names, IRIs, definitions, and multilingual labels as annotations, and record the source's assertion as SOURCE-provenance Naming events (§8). Overlays never create locations; but "formal definitions determine locations" holds only as strongly as the source class's axiomatization warrants. Every projected class SHALL carry a **projection grade**: **PG-DEF** (necessary-and-sufficient definition: located by its definition's canonical form), **PG-PART** (necessary conditions only: located as its own primitive symbol, constrained by its axioms), **PG-PRIM** (primitive: a Σ atom), **PG-FORM** (human formalization of a textual definition: a new modeling assertion, requiring ratification, flagged, with provenance to the formalizer). Co-location claims are graded accordingly: only PG-DEF × PG-DEF co-location is machine-certified formal agreement; anything involving PG-FORM is ratified-interpretation agreement and SHALL be labeled so.
- **D-9 (Pinned reference — with continuity grades) *(rev. v0.6)*.** The unit of longitudinal continuity:

$$
PinnedRef = \langle\, refID,\; consumerID,\; ADDR\!\mid\!FP,\; sourceExpression,\; \mathbf{fid},\; nfv,\; TheoryID \,\rangle
$$

  cryptographically signed per HIRI conventions — **fid is now an explicit field** alongside nfv and TheoryID, completing the identity binding set in the reference itself (hv needs no field: every ADDR/FP value is self-describing per D-10). A PinnedRef is **continuity-grade** iff it carries its *sourceExpression*, since successor resolution is computed from the expression (§7.3) and works in both ADDR and FP-only modes; under D-2.1 that expression remains well-formed over every later registry state. A pin without a sourceExpression is **locator-grade**: permitted, but NON_REGROUNDABLE-eligible over any witnessed split. CTS and all identity-dependent consumers require continuity-grade pins (§2.2).
- **D-10 (Hash and serialization discipline).** All digests in this specification — TheoryID, SigmaID, ADDR, FP, AssertionSnapshotID, and content-addressing of artifacts — are governed by one discipline:

  1. **Algorithm.** The ratified hash function is **SHA-256** (hash-version hv = 1). Hash agility is provided by versioning, not by ambiguity: every digest **value is self-describing**, carrying its hash-function code and digest length as a prefix, per the multihash convention already native to the SHML/IPFS federation layer.
  2. **Framed canonical serialization.** Every hashed payload is serialized as: a versioned ASCII **domain-separation tag** naming the artifact family (`ops/theory/1`, `ops/sigma/1`, `ops/addr/1`, `ops/fp/1`, `ops/csr/1`, …), followed by its fields, each **length-prefixed** (unsigned-varint length, then bytes). Text is UTF-8, Unicode-NFC; symbol identifiers and axioms are ordered by the canonical total order. Distinct value prefixes for ADDR and FP realize INV-7's syntactic distinguishability normatively.
  3. **No injectivity claim.** A finite digest is not an injection; collision resistance is a cryptographic assumption, not a mathematical guarantee. All uniqueness language in this specification — including §7.5's conformance to CCO *designates* — is to be read as: unique identification **under the collision-resistance assumption of the ratified function, with fail-closed handling**.
  4. **Fail-closed collision policy.** If one digest is ever observed for two distinct canonical payloads within a domain tag: the digest is **immediately quarantined** from identity use; a signed **collision-incident artifact** is published and affected consumers notified; resolution is an hv migration — **DIGEST_REINDEX**: all values recomputed under the successor function, a payload-identical 1:1 re-index published through the standard migration-artifact machinery with definitive NO_CHANGE events, which consumers MAY follow automatically. Continued identity use of a quarantined digest is an FC-1(v) violation, zero tolerance.

---

## 5. The Σ-Boundary

### 5.1 Formal statement

Every element of 𝒰 is a constructor-combination of Σ under F. Therefore OPS surfaces unnamed **recombinations** of existing primitives; it cannot surface a missing **primitive**. One cannot conjoin one's way from *object* and *quality* to *disposition*. This is a hard boundary of the method, not an engineering gap, and it is the reason for the mission statement of §1.1 and exclusion SE-2.

### 5.2 Lineage as inherited risk

The program is a formally disciplined descendant of the combinatorial *ars* — Llull's Ars Magna, Leibniz's characteristica universalis. The historical failure mode of that lineage is precisely the Σ-Boundary: the alphabet is where the ontology actually lives, and the combinatorial machinery inherits the alphabet's adequacy. This specification records the lineage in order to inherit the risk register knowingly rather than rediscover it. The disanalogy with Mendeleev is likewise recorded: the periodic table's gaps predicted unseen *elements* because the grid was ordered by an empirical coordinate; OPS gaps predict unseen *conjunctions* because the grid is ordered by entailment over chosen atoms. Claims of empirical prediction SHALL NOT be made on the periodic-table model.

### 5.3 Representation Insufficiency Reports and the Σ-insufficiency verdict

Failure to express an evidence cluster is over-determined: it does not, by itself, demonstrate that Σ lacks a primitive. When the evidence layer (§11.1) holds an evidence cluster E for which no candidate expression within the operative bounds achieves match score ≥ θ, the engine SHALL emit a **Representation Insufficiency Report (RIR)** — a signed artifact recording the failure with candidate diagnoses drawn from:

$$
\{\, Bound,\; Fragment,\; Signature,\; Matcher,\; Evidence,\; Theory \,\}
$$

The verdict `candidate_signature_insufficiency = true` SHALL be emitted only after a documented differential procedure eliminates the alternatives: bounds widened (d, s, c, b) with the failure persisting; matcher round-trip checks passing (§10.4); evidence admission criteria re-verified; and a bounded richer-constructor probe (offline, non-production) failing to express E. An SIS so established is a *candidate indicator* that a new primitive is needed. Formulating and naming that primitive is human work; producing the disciplined indicator is an OPS deliverable (Phases 5–6, RP-5).

---

## 6. Formal Construction

### 6.1 Equivalence and classification

Deciding $C \equiv_T D$ in EL⊥ is polynomial (subsumption both directions w.r.t. T). Classification of candidates against named overlay classes is therefore cheap. This is the easy half of canonicalization.

### 6.2 Canonicalization — five algorithm properties

**The normative well-order.** The canonical total order $\leq_{can}$ SHALL be **length-first**: expressions ordered by normalized size, ties broken lexicographically under the symbol-identifier order. Under a length-first order, every expression preceding C has size ≤ |C| — so the global minimum of an equivalence class is certifiable by a *finite, intrinsic* search whose bound depends only on C, never on any operational envelope.

Phase 1 SHALL specify a canonicalization procedure and demonstrate that it is:

1. **Total** over the operative regime;
2. **Equivalence-complete** — $C \equiv_T D \Rightarrow N(C) = N(D)$;
3. **Confluent and host-deterministic** — one output, byte-identical across conformant hosts, independent of derivation order (INV-1);
4. **Feasible** — within the FC-2 envelope at the scales Phase 3 requires;
5. **Globally canonical (bound-invariant)** — $N(C)$ is the $\leq_{can}$-least member of $[C]_{\equiv_T}$ over the *full* $\mathcal{C}(F,\Sigma)$, certified by completed enumeration of all expressions $\leq_{can}$-preceding the candidate representative, each checked for equivalence (polytime per check in EL⊥). For issued ADDRs, property 2 follows from property 5: equivalent expressions share one global least element.

**Certified issuance.** ADDR SHALL be issued for C only when the property-5 certification completes within the operative resources; the feasible size threshold $s_{ADDR}$ is calibrated at OI-11, and any expression beyond it receives FP only. The alternative — binding the canonicalization envelope into the identity — is recorded as **rejected**: it would make identity envelope-relative, which is the disease itself.

**Failure consequence.** If the five properties are not demonstrated at Phase 1 exit: no fingerprint-grade addresses. OPS operates in **FP-only mode** — navigation, completion, projection, and ranking proceed on locator-grade fingerprints (D-6.1, INV-7) — and every identity-dependent consumer remains disabled until the properties are demonstrated. The criterion is ratified pre-Phase-1 as RP-2A; the demonstrated specification is ratified at Phase 1 exit as RP-2B (§13).

### 6.3 Fragility of the covering relation

"Immediate specialization" presupposes a Hasse diagram that general TBoxes do not guarantee. Example: for $A \sqsubseteq \exists r.A \in T$ — a shape realist ontologies legitimately contain — T entails $A \sqsubseteq \exists r^{n}.\top$ for all n, and the $\exists r^{n}.\top$ form an infinite strictly descending chain of subsumers lying entirely above A. An immediate subsumer of A need not exist. Consequently the engine exposes **bounded frontiers** (D-7), never claimed covers, and interface language SHALL read "bounded unnamed frontier below X," never "all immediate specializations of X."

### 6.4 Satisfiability filters almost nothing

The informativeness of 𝒰 is proportional to the strength of T's *negative* axioms. Under an axiom-light T, nearly every conjunction of primitives with modest existential nesting is satisfiable: thirty primitive concepts yield $2^{30} \approx 1.1 \times 10^{9}$ conjunction candidates before a single role is introduced, and the count of semantically distinct bounded-depth concepts grows tower-like with depth. The pipeline step "discard ⊥" is therefore expected to remove little below BFO's top-level disjointness. The meaningfulness burden falls on ranking (§10, H2, FC-3), and the classhood burden falls on the Admission Gate (§8.4, FC-9).

### 6.5 Why two frontier modes

EXH mode makes an honest completeness claim over a deliberately tiny, ratified grammar; EXP mode makes an honest budget claim over realistic configurations and no completeness claim at all. On EXH-feasible configurations, EXP's recall@k against EXH ground truth quantifies search adequacy (FC-8). **Scope caution:** FC-8 certifies search behavior on small regimes as a unit test; it is explicitly *not* evidence that EXP achieves equivalent recall in the much larger regimes where exhaustive comparison is impossible. At scale, EXP output's only warranty is its (b, strategy version) label.

---

## 7. Addressing, Signing, and Continuity

### 7.1 Manifest-indexed identity

There is no theory-independent address, and no semantically theory-relative address either. ADDR and FP bind TheoryID, which identifies a canonical manifest (D-3, D-3.2). Equivalent re-axiomatizations receive different TheoryIDs; what OPS provides at the semantic level is the polytime equivalence *certificate* and the 1:1 EQUIVALENT_REAXIOMATIZATION migration (epoch-conditioned, D-3.2), not equivalence-invariant addresses. "Stable logical address" SHALL therefore always be read as *stable relative to (fid, nfv, TheoryID)* — **manifest-indexed logical identity within its epoch** (§7.4) — with Σ participating through stable symbol identifiers inside expressions, its registry state recorded as SigmaID in the manifest envelope (D-2.1), never as a hashed declaration block in the identity (D-3.1, RP-9). Prose in any OPS document claiming ontologies "share a theory" SHALL mean: share a canonical manifest, or hold manifests certified equivalent under D-3.2.

### 7.2 Names as annotations

Human-readable names, ontology IRIs, definitions, and multilingual labels are mutable annotations pointing at addresses, never constituents of them. The doctrine extends to Σ itself: primitive symbols are opaque stable identifiers; their labels are annotations (D-2). Precedent that this model is workable at production scale: the Unison language content-addresses every definition by a hash of its normalized syntax tree, with names as metadata. OPS applies the same inversion to class expressions and to the vocabulary they are built from.

### 7.3 Provenance-bearing references and relational migration

If $C \equiv_T D$, canonicalization assigns one address and, by design, destroys the distinction between them. If under T′ the class splits, no cell of the resulting partition has a privileged claim to be *the* successor. Migration is therefore a relation, $migrate : ADDR_{T} \rightarrow \mathcal{P}(ADDR_{T'})$, and resolving a particular reference across a split requires the reference's own provenance:

> **Collapse–Reversal Principle.** Canonical identity licenses equivalence collapse; longitudinal continuity additionally requires provenance sufficient to reverse that collapse when the governing theory weakens. Continuity is a property of provenance-bearing references, not of bare addresses.

Every reference-level migration record carries two fields with different epistemic warrants:

**Field 1 — Successor (definitive).** Computed from the reference's own sourceExpression under T′: a successor ADDR′ (or FP′ in FP-only mode); **BECAME_UNSATISFIABLE** ($e \equiv_{T'} \bot$; definitive — and per D-2.1(3) the outcome by which *governed semantic retirement of a symbol, concept or role,* reaches references that used it); **NON_REGROUNDABLE** (locator-grade pin over a witnessed split; flagged, never silently defaulted — emitting this is correct behavior, failing to emit it is an FC-7 violation); **NON_EXPRESSIBLE_UNDER_SIGNATURE** (defensive, D-2.1(5)); **NON_EXPRESSIBLE_UNDER_FRAGMENT** (fragment restriction, §7.4 — flagged, never silently repaired).

**Field 2 — Event annotation (witness-qualified).** A class-history annotation for the reference's old class, always carrying its witness basis: **EQUIVALENT_REAXIOMATIZATION** (the D-3.2 certificate holds within an unchanged epoch — *the one definitive event label*); **NO_CHANGE_WITNESSED** (explicitly not a guarantee that none occurred); **MERGE_WITNESSED** (with partners); **SPLIT_WITNESSED** (with the witness pair); **CLASS_BECAME_UNSATISFIABLE**.

**Mechanics.** Continuity is computed at the reference level over the PinnedRef registry (D-9); the address-level relation, the reference-level records (both fields), and all witness bases are published together as the signed, content-addressed **migration artifact** alongside the new SignedTheoryManifest — which, per INV-9, has passed the consistency gate before becoming a migration target. The engine SHALL search pinned expressions and stored representatives for witnesses; absence of a witness is recorded as exactly that. Consumers re-ground through their own references, never through the address relation alone. Epoch-constituent evolution (fid, nfv, hv) is governed by §7.4 and publishes through this same machinery. FC-7 tests the whole path before any consumer integration.

### 7.4 Identity epochs and constituent evolution *(new v0.6)*

The identity binding set of every ADDR and FP is (fid, nfv, TheoryID) with hv riding inside the self-describing value (D-10). TheoryID evolution is §7.3's subject; the remaining constituents define the **identity epoch** = (fid, nfv, hv). Within an epoch, only theory migrations occur. Epoch transitions are first-class governed migrations, published through the §7.3 artifact machinery:

- **NORMAL_FORM_REINDEX (nfv change, fid fixed).** A normal-form specification change alters representatives, never equivalence classes: $\equiv_T$ is model-theoretic and untouched. Every value recomputes; the migration is 1:1 at the class level with definitive NO_CHANGE events. Global-canonicality certification is re-run under the successor normal form; any expression whose certification is infeasible under it degrades to FP′ and is flagged as such — never silently.
- **FRAGMENT_MIGRATION (fid change).** *Expansion* (e.g., EL⊥ → ELI) with the theory payload unchanged is an injective 1:1 embedding of the old classes: every old expression remains expressible and $\equiv_T$ over old expressions is model-theoretic and unchanged — definitive. A fragment change *bundled with* a theory change (the usual motive for escalation: richer axioms) SHALL be decomposed into the fragment step and the theory step, each with its own record and, for the theory step, the full §7.3 and INV-9 discipline. *Restriction* to a smaller fragment triggers a per-reference expressibility check; orphaned expressions receive **NON_EXPRESSIBLE_UNDER_FRAGMENT** — flagged, never silently repaired.
- **DIGEST_REINDEX (hv change).** Per D-10(4): payload-identical, 1:1, definitive NO_CHANGE.

fid and nfv are carried explicitly in the SignedTheoryManifest envelope (D-3) and in every PinnedRef (D-9), so cross-epoch re-grounding is computable from the reference itself. EQUIVALENT_REAXIOMATIZATION's automatic 1:1 implication holds only within an unchanged epoch (D-3.2). No epoch transition SHALL be bundled implicitly: a migration artifact declares exactly which constituents changed.

### 7.5 Ontological status of OPS artifacts *(rev. v0.6 — FP designatum corrected to the reduced-form expression)*

Per INV-8, OPS characterizes its own artifacts in the vocabulary it expects of its consumers, reusing CCO relations verified against the pinned CCO Information Entity Ontology artifact (Appendix B), minting no new object properties. One uniform discipline governs the table: **every asserted CCO relation targets an Information Content Entity**; every relation toward a class-expression equivalence class is held at the formal-system level (the OI-10 discipline, without exception). The three-tier model of D-6.2 applies: ADDR for class identity, FP for expression location, the classification-signature record for snapshot-indexed description.

| OPS artifact | CCO characterization | Relation to subject |
|---|---|---|
| ADDR | Non-Name Identifier (cco:ont00000649, a Designative ICE — its verified definition covers automatically generated character strings, which a digest is exactly) | *designates* (cco:ont00001916, range: BFO entity) — uniquely within the context (fid, nfv, TheoryID) **under the D-10 collision-resistance assumption with fail-closed quarantine** — the canonical representative **N(C)**, itself an ICE |
| Canonical representative N(C) | Information Content Entity (cco:ont00000958) | Its least-member relation to $[C]$ is maintained at the **formal-system level**; no CCO property is asserted toward the equivalence class |
| FP | Non-Name Identifier (cco:ont00000649) | *designates* — uniquely under D-10 — **the ∅-reduced expression** $reduce_{\emptyset}(C)$, itself an ICE. **FP never designates a class**: one class may carry many FP aliases (D-6.1), and the class-relationship is held at the formal-system level. This is INV-7's ontological form |
| Classification-signature record | Descriptive Information Content Entity (cco:ont00000853 — verified definition: an ICE that describes some Entity) | *describes* (cco:ont00001982) the reduced-form expression ICE whose bounded classification its statements give, indexed to its assertion snapshot (D-6.2). Its correspondence to the class(es) matching that classification is held at the formal-system level and is explicitly non-unique — consonant with CCO's own scope note declining to make *describes* functional |
| SignedTheoryManifest | Descriptive Information Content Entity | *describes* the canonical theory payload, registry state, and epoch constituents (ICEs) it fixes |
| PinnedRef | Descriptive Information Content Entity (provenance record, HIRI-conventional) | *is about* (cco:ont00001808) the referring consumer's use of a designator |
| Migration artifact, RIR | Descriptive Information Content Entity | *describes* the migration record set / representation-failure report contents |

OI-10 (the BFO treatment of the class-expression equivalence class itself) remains open and remains **non-load-bearing**: no asserted CCO relation anywhere in this table targets an equivalence class. **Variance note:** the ontological reviews' attached materials render the Descriptive ICE definition as "consists of a set of propositions"; the pinned develop-branch artifact reads "an ICE that describes some Entity" (Appendix B). The repair holds under either reading, and the operative CCO release for FNSR is pinned at Phase 0 under OI-6b.

---

## 8. Epistemic Status Model

The state of a node is a tuple of orthogonal dimensions:

$$
Status(C) = \langle\, Logical,\; Naming,\; Grounding \,\rangle
$$

- **Logical ∈ { UNSATISFIABLE, SATISFIABLE }.** Authority: the reasoner. Indexed to TheoryID — recomputed under migration, never "upgraded." UNSATISFIABLE nodes are excluded from 𝒰 and representable only as diagnostics. **Caution (normative):** SATISFIABLE is relative to T and nearly vacuous under weak T (§6.4); consumers SHALL NOT treat it as evidence of anything beyond formal consistency.
- **Naming — provenance-qualified.** Naming is determined by the set of active, signed assertion records at a location, each carrying a provenance qualifier: **SOURCE** — a faithful overlay projection records that an *external ontology* asserts this class (projection grade attached, D-8); observation, not conferral: the Admission Gate does not apply, and OPS neither ratifies nor can revoke the source's content. **OPS** — an OPS-surfaced candidate passed the Ontology Admission Gate (§8.4). Displayed values: **UNNAMED**, **SOURCE_ASSERTED**, **OPS_ASSERTED**, both where both hold, **DEPRECATED** (only deprecated records remain). The gate governs exactly one transition: UNNAMED → OPS_ASSERTED (SE-5).
- **Grounding ∈ { UNGROUNDED, CANDIDATE, EVIDENCE_SUPPORTED, DISPUTED, RETRACTED }.** Authority: the evidence layer, under its admission criteria. CANDIDATE is the natural output of RS-4 signals awaiting admission; DISPUTED and RETRACTED are legitimate states, not anomalies.

Global monotonicity is repealed: deprecation, dispute, and retraction are ordinary lifecycle events. Every status transition is a signed, auditable event issued by the authority for its dimension. INV-5 requires the full tuple — provenance included — in every presentation. Assertion events also advance the AssertionSnapshotID against which classification-signature records are indexed (D-6.2).

**The completion quarry.** The query pattern of Phases 5–6 is

$$
\langle\, SATISFIABLE,\; UNNAMED,\; CANDIDATE \,\rangle
\quad\text{and}\quad
\langle\, SATISFIABLE,\; UNNAMED,\; EVIDENCE\_SUPPORTED \,\rangle
$$

— formally admissible, humanly unnamed, empirically live. But quarry is not catch: between this pattern and OPS_ASSERTED stands the gate of §8.4, without exception (SE-5). SOURCE_ASSERTED nodes, meanwhile, are the named reference points against which frontiers, baselines, and Phase 4 projection metrics are computed — observed, not gated.

### 8.4 The Ontology Admission Gate

**Scope: the gate applies to OPS-surfaced candidates seeking OPS_ASSERTED status, and to nothing else.** Imported source assertions are outside its jurisdiction (§8).

A satisfiable, instantiated, high-ranked class expression can still pick out an accidental collection. Empirical evidence that instances happen to satisfy $A \sqcap B$ does not make *A-and-B* a genuine category. Between EVIDENCE_SUPPORTED candidacy and OPS_ASSERTED classhood, every candidate SHALL pass a human-ratified admission review answering, at minimum:

1. **Definition.** Does the candidate support a genus–differentia definition of the house form — *"b is a c that d's"* — with *c* the closest appropriate BFO/CCO parent and *d* genuinely distinguishing the intended referents?
2. **Clarity.** Is the definition clear to a competent curator without access to the generation trace?
3. **Inclusiveness.** Does it include the paradigmatic instances of the intended referents?
4. **Exclusiveness.** Does it exclude clear non-referents?
5. **Categorization.** Is the BFO parentage correct?
6. **Relation discipline.** Is the candidate expressible with existing BFO/CCO relations, without minting unnecessary object properties?
7. **Non-accidentality.** Is there reason to regard the class as non-accidental rather than a coincidental intersection?
8. **Warrant.** Is the class useful enough to justify assertion and maintenance?

The gate is process-level: it requires no new object properties and no OPS machinery beyond the recording of its verdicts as signed events on the Naming dimension. Gate criteria are ratified at RP-12; gate yield is measured at FC-9; the criteria are candidate material for BCCS-adjacent conformance rules (§2.2).

---

## 9. Projection and Alignment

### 9.1 Phase 0 — Expressivity audit (program gate)

Before any construction, the program SHALL measure how much of the target ontologies survives translation into the chosen fragment:

**Scope.** BFO 2020 (OWL artifact and CLIF axiomatization separately) **and CCO's Extended Relations Ontology, together with the property-chain machinery of CCO's information-entity module — before Phase 1** (RP-13). Known obstructions to record: BFO's relation set is inverse-paired and inverse declarations fall outside OWL 2 EL; CCO's mid-level relations carry inverse/subproperty structure and property chains; the CLIF axiomatization's full first-order content lies beyond any OWL profile.

**Dimensions.** Survival reported per axiom type for **concept axioms and role axioms alike** (D-1.1), plus a **projection-grade census** of the audit targets (PG-DEF / PG-PART / PG-PRIM counts, D-8).

**Measures.** Two, because ten trivial axioms and one consequential axiom are not naturally 10/11 of a theory's semantics:

- **Syntactic survival** — the proportion of source axioms exactly translatable, per axiom category (concept and role). Explanatory: it says why content is lost.
- **Consequence survival** — the gating measure, over a ratified competency-query set Q that SHALL include role-dependent entailments (drafted during Phase 0, ratified at Phase 0 exit; source-side entailments for CLIF content evaluated with first-order tooling):

$$
Survival_Q \;=\;
\frac{\bigl|\{\, q \in Q : T_{source} \models q \;\wedge\; T_{OPS} \models q \,\}\bigr|}
     {\bigl|\{\, q \in Q : T_{source} \models q \,\}\bigr|}
$$

FC-4 operates on $Survival_Q$; the syntactic tables contextualize it. Two failure shapes remain anticipated and gated: **trivial success** (taxonomy-plus-disjointness projection proves little) and **fragment artifacts** (equivalences and gaps that are artifacts of the fragment, with silent destruction of relational semantics a named instance, D-1.1). Every Phase 4–5 result SHALL carry the audit's $Survival_Q$ figure as a header caveat. The audit output feeds RP-1, which covers the concept fragment *and* the role-axiom sub-fragment.

### 9.2 Projection experiments (Phase 4)

For the ratified fragment: map the expressible BFO subset; evaluate unique-mapping rate, correctness of equivalence collapse, agreement between asserted and derived subsumption, and the census of unnamed nodes adjacent to SOURCE_ASSERTED ones — all reported per projection grade (D-8). Broader CCO scaling follows under OI-4.

### 9.3 Co-location, coalescence, and manifest transitions *(rev. v0.6)*

**Co-location** requires no governance beyond ordinary canonicalization: when two overlays' class definitions are both expressions over the shared manifest and canonicalize identically, they resolve to the same existing address. Co-location claims carry projection grades (D-8): PG-DEF × PG-DEF is machine-certified formal agreement; anything involving PG-FORM is ratified-interpretation agreement.

**Manifest transitions generally.** The Consequence Preview and the INV-9 consistency gate govern **every** candidate successor manifest — bridge incorporation, symbol retirement (D-2.1(3)), and ordinary axiom changes alike. No successor manifest becomes operative, issues addresses, or serves as a migration target without passing both.

**Coalescence** is the governed operation of making two previously distinct addresses equivalent. Two primitives from distinct namespaces never become equivalent absent bridge axioms in T — OPS *records* alignment; establishing it is empirical and terminological work outside logic's jurisdiction. Consistency does not establish that a bridge is *true* — a false bridge can be perfectly consistent — so the reasoner serves as decision support before the human, not as verifier after:

1. **Propose.** Embedding and evidence layers nominate candidate bridge axioms (A ≡ B, A ⊑ B) with supporting signals.
2. **Consequence Preview.** The reasoner computes, for the candidate successor theory: consistency (INV-9); the **entailment diff** — all new subsumptions and equivalences among asserted classes the change would introduce, including forced role and class emptiness in retirement cases; and impact on the ratified competency set Q. The preview is a signed artifact.
3. **Ratify.** A human authority — for FNSR-internal overlays, the Ratifying Architect — accepts or rejects each change *with the preview in hand*. The semantic burden lies here, explicitly: ratification asserts truth; the reasoner only ever asserted consequences.
4. **Activate.** The ratified axioms are incorporated into a new theory manifest (with a final mechanical re-verification, including the INV-9 gate, if the theory changed since preview), producing a new TheoryID whose migration artifact records the outcome (§7.3).

INV-4 forbids any other coalescence path. Pipeline quality is measured by the decomposed FC-5 family.

---

## 10. Salience and Ranking — the Headline Problem

### 10.1 Default expectation

Per §6.4, the expected default output of unranked frontier generation is overwhelmingly meaningless construction. This is the *anticipated baseline*; beating it is the central empirical question (H2) — and beating it still only produces candidates for the Admission Gate, never classes (SE-5).

### 10.2 Ranking stack

Candidate rankers, evaluated separately and in hybrid: **RS-1 Parsimony** (description-length / MDL priors over canonical forms); **RS-2 Structural priors** (proximity to named nodes; being a bounded common subsumer of named pairs; participation in short paths between overlay classes); **RS-3 Naturalness prior** (embedding-space coherence of the *verbalized* candidate with the target corpus — ranking generated nodes, not merely retrieving regions, is the principal legitimate use of the universal-embedding-geometry results within OPS); **RS-4 Evidence prior** (signal from the grounding layer that observations plausibly instantiate the candidate; RS-4 signals feed the Grounding dimension as CANDIDATE pending evidence-layer admission).

INV-2 applies throughout: rankers order; they never restructure. In EXP mode, rankers additionally steer the deterministic best-first expansion (D-7); the determinism requirement of INV-1 extends to any ranker so used.

### 10.3 The structural tension of embedding navigation

Embedding retrieval finds what language already talks about; the genuinely unnamed nodes — the novel target — are precisely where linguistic signal is weakest. Evaluation SHALL therefore stratify embedding-navigation recall by the target's lexical support in the corpus (FC-6). The shared-geometry results motivating RS-3 (the vec2vec / Platonic Representation Hypothesis line) describe geometry of *linguistic usage* — the very label-driven similarity the addressing layer exists to escape. Advisory use is licensed; structural use is forbidden (SE-3).

### 10.4 Verbalization as an evaluated dependency

RS-3 and all natural-language search paths depend on rendering formal expressions into language. Verbalization quality SHALL be evaluated in its own right, with a round-trip requirement: verbalize(C) → parse → same address (or same FP under FP-only mode, with reasoner-equivalence fallback per D-6.1's aliasing model), measured over the test corpus. TagTeam.js is the candidate bridge (§2.2). Round-trip results also serve the Matcher arm of the RIR differential procedure (§5.3).

### 10.5 Baseline obligation

Every ranking claim SHALL be reported against the baselines of §14.1; lift is claimed only relative to B-1 through B-3, never in absolute terms. Additionally, on EXH-feasible configurations, EXP output SHALL be scored for recall@k against EXH ground truth (§6.5, FC-8), so that ranking evaluation and search-adequacy evaluation are never conflated — with §6.5's scope caution: small-regime recall certifies search behavior, not large-regime recall.

---

## 11. Architecture

### 11.1 Components *(rev. v0.6)*

| Component | Responsibility |
|---|---|
| Theory Manifest Service | Canonical payload serialization per D-10, TheoryID and SigmaID computation, epoch-constituent declaration (fid, nfv), manifest signing and publication; **INV-9 consistency gate at activation**; manifest-equivalence certification (D-3.2); migration-artifact assembly and publication, including epoch transitions and DIGEST_REINDEX (§7.3, §7.4, D-10(4)); collision-incident artifacts |
| Symbol Registry | Append-only custody of symbol identifiers and kinds (D-2.1); deprecation events; SigmaID state |
| Reference Registry | Registration and custody of PinnedRefs with continuity grades and full binding set (D-9); reference-level successor resolution and event annotation; witness search (§7.3); cross-epoch re-grounding (§7.4) |
| Reasoner Core | Deterministic EL⊥ satisfiability, equivalence, subsumption, classification — concept and role axioms per D-1/D-1.1; theory-consistency checking for INV-9; edge-canonical (INV-6) |
| Canonicalizer | Normal form N with global-canonicality certification per §6.2(5), ADDR issuance under the certified-issuance rule (identity grade), ∅-reduction and FP computation (locator grade, D-6.1), classification-signature record issuance under assertion snapshots (D-6.2), grade tagging per INV-7 and D-10 value grammar |
| Frontier Generator | Bounded candidate generation per D-7 in EXH or EXP mode; generate → normalize → reason → merge/discard → rank; FP-only merge detection via reasoner equivalence with FP-equality fast path |
| Ranking Layer | RS-1 through RS-4; advisory only (INV-2); deterministic where used to steer EXP expansion |
| Overlay Registry | Ontology projections as annotation layers with projection grades (D-8); recording of SOURCE-provenance assertion events; custody of the Ontology Admission Gate's verdicts as signed OPS-provenance Naming events (§8, §8.4); AssertionSnapshotID advancement (D-6.2) |
| Evidence Layer | Grounding-dimension authority (§8); RIR emission and differential procedure custody (§5.3); evidence priors (RS-4) |
| Alignment Service | Propose → Consequence Preview → Ratify → Activate pipeline for all manifest transitions (§9.3); preview artifact production |

### 11.2 Pipeline invariant

Generate → Normalize → Reason → (⊥? discard) → (≡? merge, by reasoner equivalence) → Order by ⪯ → Rank → Present with full status tuple. Structure is fixed before ranking begins; presentation carries the tuple — assertion provenance included — per INV-5 and grade per INV-7.

### 11.3 Determinism and dual-host equivalence

Conformance to INV-1 — including deterministic EXP expansion order, the global-canonicality certification procedure, ∅-reduction, and byte-exact D-10 framing — is demonstrated by a dual-host equivalence suite executing identical inputs in browser and Node.js and diffing byte-level canonical outputs, per house precedent. The suite is a Phase 2 exit gate. Dependency pinning per OI-1 precedes any executable release.

---

## 12. Hypotheses *(rev. v0.6)*

- **H1 (Bounded constructibility).** For F = EL⊥ with the Phase 0 signature: (a) EXH mode is sound, complete over $\mathcal{C}(F,\Sigma',d,s,c)$, and deterministic on configurations within the ratified EXH envelope; (b) EXP mode is sound, deterministic, and operates within the FC-2 envelope at |Σ| ≤ 50 under budget b, achieving recall@k against EXH ground truth at or above the FC-8 threshold on EXH-feasible configurations; (c) ADDR issuance under the certified-issuance rule is achievable within the FC-2 envelope for expressions up to the calibrated size threshold $s_{ADDR}$ (OI-11). *Falsified by FC-1, FC-2, or FC-8.*
- **H2 (Salience).** The hybrid ranker (RS-1..4) exceeds each single-component ranker and exceeds the B-1 baseline on Instrument-A meaningfulness by the FC-3 margins. *Falsified by FC-3.*
- **H3 (Alignment utility).** On at least two real ontology pairs sharing BFO grounding, the pipeline of §9.3 achieves: proposal precision ≥ the FC-5a threshold; Consequence Previews complete per FC-5b; and post-integration semantic error ≤ the FC-5c threshold. *Falsified by any member of the FC-5 family.*
- **H4 (Traceable continuity) *(rev. v0.6)*.** Across a nontrivial evolution whose pilot scenario set includes genuine splits, one certified equivalent re-axiomatization, one **concept** retirement, one **role** retirement, one retirement proposal **correctly blocked** by the INV-9 gate (the reflexivity interaction), and one **NORMAL_FORM_REINDEX**: every continuity-grade reference receives the correct successor (definitive field); every event annotation is consistent with its witness basis, with no unwitnessed-definitive claim; every locator-grade reference over a witnessed split is flagged NON_REGROUNDABLE; activated retirements reach affected references as BECAME_UNSATISFIABLE with downstream emptiness shown in the preview; the blocked retirement never activates; the reindex is 1:1 at class level with degradations flagged; and under the equivalence certificate within an unchanged epoch, all addresses re-index 1:1 with definitive NO_CHANGE. Zero errors against manual adjudication. *Falsified by FC-7.*
- **H5 (Admission yield).** Phase 5 studies produce at least the FC-9 minimum of candidates that reach, or are adjudicated admissible-pending-definition at, OPS_ASSERTED via the Ontology Admission Gate. *Falsified by FC-9.* This is the hypothesis that OPS is a BFO/CCO completion mechanism and not merely a description-logic possibility explorer.

The informal proposal's original central hypothesis — that navigation without global materialization is possible — remains retired: refinement-operator research has performed lazy traversal for years (§16).

---

## 13. Research Phases *(rev. v0.6 — entry set includes RP-16)*

**Entry gate: Phase 1 SHALL NOT begin until RP-2A, RP-8, RP-9, RP-10, RP-11, RP-12, RP-13, RP-15, and RP-16 are ratified.** **RP-2B is ratified at Phase 1 exit.**

**Phase 0 — Expressivity audit.** *Entry:* this spec ratified to working status. *Exit:* syntactic-survival tables (concept and role axioms), projection-grade census, and $Survival_Q$ over ratified competency set Q (role-dependent entailments included) for BFO 2020 and CCO's Extended Relations Ontology; the operative CCO release pinned and OI-6b full-pinning pass complete; fragment decision — concept language and role-axiom sub-fragment — ratified (RP-1). *Gate:* FC-4.

**Phase 1 — Fragment and canonicalization.** Specify the smallest useful language (constructors, role axioms, GCI regime, normalization rules); demonstrate the five algorithm properties of §6.2 — global canonicality included — or invoke FP-only mode with identity-dependent consumers disabled. *Exit:* canonicalization specification ratified (**RP-2B**). *Gate:* FC-1 (algorithm-properties arm).

**Phase 2 — Canonicalizer and addressing.** Edge-canonical implementation of reasoner core (concept and role reasoning, consistency checking), canonicalizer with certified issuance, ∅-reduction, and D-10 framing, Theory Manifest Service with equivalence certification, epoch declaration, and the INV-9 activation gate, Symbol Registry, Reference Registry. *Exit:* dual-host equivalence suite green; dependencies pinned (OI-1). *Gate:* FC-1 (stability, grade-separation, bound-invariance, collision-policy, and consistency-gate arms).

**Phase 3 — Bounded frontier generation.** Implement D-7 in both modes; calibrate the EXH envelope (OI-7) and $s_{ADDR}$ (OI-11); measure the EXP performance envelope across |Σ|, d, s, c, b, and axiom count; measure EXP recall@k against EXH ground truth; measure FP alias multiplicity on the test corpus. *Exit:* envelope, search-adequacy, and alias reports. *Gates:* FC-2, FC-8.

**Phase 4 — Projection.** BFO 2020 expressible-subset projection per §9.2, reported per projection grade against SOURCE_ASSERTED reference points; ERO relational semantics verified against Q; broader CCO scaling per OI-4. *Exit:* projection report carrying the $Survival_Q$ caveat. *Gate:* FC-4 (artifact-content arm).

**Phase 5 — Completion studies.** Frontier generation around SOURCE_ASSERTED BFO/CCO nodes; ranking evaluation against B-1..3 under the two-instrument expert protocol (§14.2); Admission Gate reviews of top grounded candidates; RIR instrumentation live with the differential procedure. *Exit:* salience and admission-yield reports. *Gates:* FC-3, FC-9.

**Phase 6 — Navigation, alignment, and drift.** Stratified embedding-navigation evaluation; alignment pipeline pilots on two ontology pairs with Consequence Previews; migration trial against CTS scenarios per the H4 scenario set — splits, certified equivalent re-axiomatization, both retirement kinds, one blocked retirement, one NORMAL_FORM_REINDEX. *Exit:* pipeline quality and continuity reports. *Gates:* FC-5 family, FC-6, FC-7.

---

## 14. Evaluation and Baselines

### 14.1 Baselines

- **B-1 Random-satisfiable.** Draws from the bounded satisfiable grammar by a **specified, seeded, deterministic sampler**: on EXH-feasible configurations, exact uniform draws over the enumerated space; on larger configurations, uniform generation over the syntax of $\mathcal{C}(F,\Sigma',d,s,c)$ under a documented distribution, satisfiability-filtered. Uniformity over *semantic equivalence classes* is explicitly not claimed for the large regime — the baseline's role is a reproducible, unranked floor, and its distribution is part of the record.
- **B-2 Refinement operators.** Generation via DL refinement operators of the concept-learning tradition (the DL-Learner / CELOE family) — the nearest existing navigation machinery and the first comparator any informed reviewer will demand.
- **B-3 FCA completion.** Candidates from Formal Concept Analysis–based knowledge-base completion (the Baader–Ganter–Sertkaya attribute-exploration line; Kriegel's exploration work in EL) — the nearest existing *gap-discovery* machinery, with its own completeness theory.

### 14.2 Expert protocol — two instruments

Blinded review by ≥ 3 ontologists of shuffled candidate sets mixing top-ranked OPS output, B-1..3 output, and verbalized SOURCE_ASSERTED classes as attention checks; inter-rater agreement reported (Fleiss' κ); disagreements adjudicated and logged. Two instruments, kept separate: **Instrument A — Meaningfulness** (binary judgment plus free annotation; gates FC-3; exploratory — salience lift, not classhood). **Instrument B — Ontological admissibility** (the §8.4 criteria as a structured checklist; feeds the gate and FC-9). A candidate can pass A and fail B; that divergence is itself a reported metric. Protocol details are a ratification point (RP-4).

### 14.3 Criteria

Logical correctness (soundness of nodes and edges — zero tolerance); canonical stability, grade separation, bound-invariance of issued ADDRs, collision-policy conformance, and consistency-gate conformance (FC-1); reproducibility across hosts including EXP determinism, ∅-reduction, and D-10 framing (INV-1); scalability envelope (FC-2); search adequacy on EXH-feasible regimes with the §6.5 scope caution (FC-8); FP alias multiplicity (FC-1(iii)); projection fidelity under the $Survival_Q$ caveat, per projection grade, against SOURCE_ASSERTED reference points (§9.2); salience lift vs. baselines (FC-3); admission yield (FC-9); alignment pipeline quality by the decomposed FC-5 family; traceable continuity per the full H4 scenario set (FC-7).

---

## 15. Falsification Conditions *(rev. v0.6)*

Thresholds marked ⚠ are provisional pending pilot calibration (OI-3); the *shape* of each condition is fixed now.

- **FC-1 (Identity integrity).** (i) Any ADDR divergence across conformant hosts on identical inputs → fail, zero tolerance. (ii) Any instance of an FP presented as, converted into, or consumed as identity → fail (INV-7 breach), zero tolerance. (iii) If the §6.2 algorithm properties are not demonstrated at Phase 1 exit: ADDR does not ship; OPS proceeds FP-only with identity-dependent consumers disabled; FP quality is reported as **alias multiplicity** — the distribution of distinct FPs per T-class on the test corpus (target: median 1; tail distribution reported ⚠) — replacing the retired collision metric, which measured a provably impossible event (D-6.1). (iv) Bound-invariance: issuing an ADDR without a completed global-canonicality certificate, or any case of the same (fid, nfv, TheoryID, $[C]$) yielding two ADDRs under different operational envelopes → fail, zero tolerance. (v) Collision policy: any observed digest collision not met with immediate quarantine and a signed collision-incident artifact, or any identity use of a quarantined digest, or any resolution path other than a DIGEST_REINDEX hv migration → fail, zero tolerance. **(vi) Consistency gate *(new v0.6)*:** any manifest activated, address issued, or migration targeted against an inconsistent theory (INV-9) → fail, zero tolerance.
- **FC-2 (Tractability envelope — EXP mode).** With |Σ| ≤ 50, d ≤ 3, s ≤ s₀ ⚠, c ≤ c₀ ⚠, b ≤ 10⁵ ⚠ candidate evaluations: frontier generation exceeding 60 s wall-clock or 1 GB memory ⚠ on the reference edge host (browser profile, OI-2) → fail Phase 3. EXH-mode configurations exceeding their ratified envelope (OI-7) are rejected as configurations, not counted as program failure.
- **FC-3 (Salience — Instrument A).** Top-20 Instrument-A meaningful rate of the hybrid ranker fails to reach 2× B-1 and 1.25× the best of B-2/B-3 ⚠ → H2 falsified; ranking research redirected before Phase 6.
- **FC-4 (Projection substance).** $Survival_Q$ < 30% ⚠ over the ratified competency set — which includes role-dependent entailments — for the chosen fragment (concept language plus role-axiom sub-fragment), *or* OWL-artifact projection adds no non-taxonomic content beyond disjointness → halt for fragment escalation decision (RP-1 revisited); Phases 4–5 do not proceed on the failing fragment.
- **FC-5 (Alignment pipeline family).** **FC-5a (Proposal precision):** human acceptance rate of proposed bridges < 0.5 ⚠ on the pilot pairs → proposer revision (measures the proposer, not safety). **FC-5b (Preview completeness):** any post-activation entailment among asserted classes not shown in the Consequence Preview → fail, zero tolerance. **FC-5c (Post-integration error):** rate of coalesced bridges reverted or adjudicated semantically wrong within the pilot horizon > 0.05 ⚠ → pipeline revision before any production coalescence.
- **FC-6 (Embedding lift).** Stratified recall shows no lift over lexical search on low-lexical-support targets → RS-3 and embedding navigation demoted to OPTIONAL; SE-3 unchanged.
- **FC-7 (Continuity integrity) *(rev. v0.6)*.** The pilot scenario set SHALL include genuine splits, one certified equivalent re-axiomatization, one **concept** retirement, one **role** retirement, one retirement proposal **correctly blocked** by the INV-9 gate, and one **NORMAL_FORM_REINDEX**; FRAGMENT_MIGRATION scenarios are mandatory before any fid change becomes operative. Any successor-field error; any event annotation inconsistent with its witness basis; any unwitnessed-definitive event claim; any failure to flag NON_REGROUNDABLE for a locator-grade reference over a witnessed split; any failure to route an activated retirement through BECAME_UNSATISFIABLE with previewed downstream emptiness; any activation of a retirement that should have been blocked; any silent repair where NON_EXPRESSIBLE_UNDER_SIGNATURE or NON_EXPRESSIBLE_UNDER_FRAGMENT is required; any unflagged degradation under a reindex; or any failure to certify and 1:1-re-index the equivalent re-axiomatization within an unchanged epoch → migration semantics revision; no consumer integration until a clean pass.
- **FC-8 (Search adequacy).** On EXH-feasible configurations, EXP recall@k against EXH ground truth < 0.8 ⚠ → search-strategy revision before Phase 5 relies on EXP output. Per §6.5, passing FC-8 certifies small-regime search behavior only.
- **FC-9 (Admission yield).** Across the Phase 5 studies, fewer than 3 ⚠ candidates reach, or are adjudicated admissible-pending-definition at, OPS_ASSERTED via the Ontology Admission Gate → H5 falsified: OPS as configured is a description-logic possibility explorer but not a BFO/CCO completion mechanism for the audited signature and theory; program pivots or halts per RP-12 review.

---

## 16. Related Work and Lineage

**Tractable description logics.** EL-family tractability under GCIs (the Baader–Brandt–Lutz "EL envelope" line) motivates D-1; the OWL 2 EL profile is the implementation-facing statement of the same trade — including its admitted role axioms, the EL-specific property-chain/range restriction, and its exclusion of inverses — and drives the Phase 0 audit. ELI's ExpTime-completeness prices the escalation path.

**Concept-space structure.** Kriegel's results on reduced EL concept descriptions and the distributive, graded lattice of EL concept descriptions ground both the TBox-free case (D-5) and the canonicality of ∅-reduced forms on which D-6.1's no-cross-class-collision property rests. The LCS/MSC literature (Baader, Küsters, Molitor and successors) bounds what bounded common subsumers can promise under GCIs.

**Lazy navigation.** Refinement operators in DL concept learning (Lehmann–Hitzler; DL-Learner, CELOE) constitute fifteen years of practice in traversing concept spaces without materialization, with reasoning in the loop. OPS's novelty claim is accordingly *not* navigation but the addressing scheme, the grade discipline, the overlay model, the continuity semantics, the admission gate, and the grounding pipeline. B-2 makes this positioning testable.

**Completion.** FCA-based knowledge-base completion (Baader–Ganter–Sertkaya; Kriegel's EL exploration) is the nearest prior program to gap discovery, with a mathematical theory of when exploration is complete. B-3 makes the comparison mandatory.

**Ontology admission practice.** The Admission Gate criteria encode established BFO/OBO discipline: genus–differentia definitions of the form *"b is a c that d's,"* clarity/inclusiveness/exclusiveness refinement, correct upper-level categorization, and relation reuse over relation minting — per house practice and the CCO refinement rules supplied with the ontological reviews.

**Evaluation practice.** The consequence-survival metric of §9.1 follows established competency-question and entailment-preservation practice in ontology evaluation; the ratified query set Q makes the practice auditable here.

**Content-addressed identity.** Unison's production practice of hashing normalized syntax trees with names as metadata is the working precedent for §7.2, extended to the symbol-identifier doctrine of D-2 and the append-only registry of D-2.1; the multihash convention of D-10 is the working precedent for self-describing digests, shared with the IPFS substrate of SHML.

**Universal embedding geometry.** The vec2vec-style translation results and the Platonic Representation Hypothesis motivate RS-3 as a naturalness prior and nothing stronger; §10.3 records why.

**Lineage.** Llull and Leibniz, per §5.2 — cited as inherited risk, not ornament.

*Citation pinning:* load-bearing CCO IRIs are verified and pinned in **Appendix B** (OI-6a, closed; independently spot-checked by the fifth review); the full source-pinning pass is OI-6b, **SHALL be complete before Phase 0 exit**.

---

## 17. Open Issues

- **OI-1.** Edge-canonical EL⊥ reasoning core (including the D-1.1 role axioms and consistency checking): build vs. port; dependency pinning required before any executable release.
- **OI-2.** Reference edge host definition for FC-2 (browser and Node profiles).
- **OI-3.** Calibration pass for all ⚠ thresholds at the named phase gates (now including the FP alias-multiplicity tail).
- **OI-4.** Broader CCO projection scope and sequencing after the Phase 0 ERO audit and Phase 4 BFO projection.
- **OI-5.** Whether the BCCS signature-normalization work and the OPS normal form (§6.2) unify into one shared specification (see RP-7).
- **OI-6a *(closed)*.** Load-bearing CCO IRI verification for §7.5 — executed against the pinned develop-branch artifact; results in Appendix B; independently confirmed by the fifth review. Residual items folded into OI-6b.
- **OI-6b.** Full source-pinning pass (SHA-256 where retrievable) for all §16 sources, plus operative CCO release selection and repo-commit capture. **SHALL be complete before Phase 0 exit.**
- **OI-7.** EXH envelope calibration: the ratified set of (|Σ′|, d, s, c) configurations for which exhaustive enumeration is feasible on the reference edge host.
- **OI-8.** Semantic theory identity: a canonical representative of a theory up to logical equivalence. Deferred research; D-3.2 certificates are the interim mechanism.
- **OI-9.** Conservativity certificates for migrations whose new axioms mention only new symbols; would upgrade such migrations to definitive wholesale-PRESERVED.
- **OI-10.** BFO treatment of the class-expression equivalence class itself. Non-load-bearing (no asserted CCO relation targets it, §7.5); retained for the BCCS-adjacent review.
- **OI-11.** Calibration of $s_{ADDR}$: the maximum expression size for which global-canonicality certification (§6.2(5)) is feasible on the reference edge host; expressions beyond it receive FP only.

---

## 18. Ratification Points *(rev. v0.6)*

### Ratification status summary

| RP | Subject | Ext. 5 disposition on v0.5 | v0.6 action | Drafter recommendation |
|---|---|---|---|---|
| RP-1 | Fragment (concept + role sub-fragment) | Signed off in principle | D-1.1 chain/range wording patched (R-48) | Ratify at Phase 0 exit |
| RP-2A / RP-2B | Canonicalization criterion / specification | Signed off ("mathematically coherent") | Unchanged | Ratify pre-Phase-1 / at Phase 1 exit |
| RP-3 | Mission, object discipline, SE-1..5 | Signed off | §1.3 row 4 updated to the three-tier model | Ratify |
| RP-4 | Evaluation protocol | Signed off | Unchanged | Ratify |
| RP-5 | RIR/SIS deliverable | Signed off | Unchanged | Ratify |
| RP-6 | Naming of OPS | — | Unchanged | Decide after Phase 0 |
| RP-7 | Shared normal form with BCCS | — | Unchanged | Joint review before Phase 1 exit |
| RP-8 | Frontier semantics | Signed off | Unchanged | Ratify |
| RP-9 | Address binding set + Σ lifecycle | **BREAKING** (vacuity claim false; consistency invariant needed) | **Revised: INV-9; retirement as governed theory change through Consequence Preview + consistency gate; vacuity claim withdrawn with reflexivity counterexample recorded** | Ratify as revised |
| RP-10 | Status model | Signed off | Unchanged | Ratify |
| RP-11 | Continuity semantics | **BREAKING** (retirement consequence handling; via RP-9) | **Revised: blocked-retirement scenario in H4/FC-7; previewed downstream emptiness mandatory** | Ratify as revised |
| RP-12 | Ontology Admission Gate | Signed off | Unchanged | Ratify |
| RP-13 | Phase 0 role-audit scope | Signed off (with R-48 patch) | D-1.1 patched | Ratify |
| RP-14 | Meta-artifact grounding | **BREAKING** (FP's formal definition contradicted its collision semantics) | **Revised: FP re-founded over $reduce_{\emptyset}(C)$ with the aliasing model; classification-signature record separated as a snapshot-indexed contextual artifact; FP designatum = the reduced-form ICE; FC-1(iii) recast as alias multiplicity** | Ratify as revised |
| RP-15 | Hash and serialization discipline | Signed off ("correctly abandons mathematical injectivity") | AssertionSnapshotID and `ops/csr` tag added | Ratify |
| RP-16 | Identity epochs and constituent evolution | **NEW (from Ext. 5 breaking issue 3)** | **§7.4: epoch = (fid, nfv, hv); NORMAL_FORM_REINDEX; FRAGMENT_MIGRATION with expansion-embedding, decomposition, and restriction semantics; fid added to manifest envelope and PinnedRef; D-3.2 epoch-conditioned** | Ratify; gates Phase 1 |

### Ratification points in full

- **RP-1 (Fragment).** The concept language *and* the role-axiom sub-fragment (D-1, D-1.1, chain/range restriction named), decided on the Phase 0 audit. *Recommendation:* retain the default unless FC-4 fires.
- **RP-2A / RP-2B (Canonicalization).** The five-property criterion pre-Phase-1; the demonstrated specification at Phase 1 exit. *Recommendation:* ratify per phase.
- **RP-3 (Mission statement).** §1.1, §1.3, SE-1..5. *Recommendation:* ratify.
- **RP-4 (Evaluation protocol).** *Recommendation:* ratify with B-2, B-3, and Instrument B mandatory.
- **RP-5 (RIR/SIS deliverable).** *Recommendation:* ratify.
- **RP-6 (Naming).** *Recommendation:* decide after Phase 0.
- **RP-7 (Shared normal form with BCCS).** *Recommendation:* joint review before Phase 1 exit.
- **RP-8 (Frontier semantics).** *Recommendation:* ratify.
- **RP-9 (Address binding set and Σ lifecycle — REVISED v0.6).** As before, plus: INV-9 operative-theory consistency; semantic retirement as a governed theory-change proposal passing Consequence Preview and the consistency gate; the "vacuous" claim withdrawn, with subrole-emptiness propagation and the reflexivity inconsistency recorded as the canonical cases. *Recommendation:* ratify as revised; the fifth review's counterexample was decisive — one ungated retirement could have collapsed every class in 𝒰.
- **RP-10 (Status model).** *Recommendation:* ratify.
- **RP-11 (Continuity semantics — REVISED v0.6).** The H4/FC-7 scenario set now includes a correctly blocked retirement and a NORMAL_FORM_REINDEX. *Recommendation:* ratify as revised.
- **RP-12 (Ontology Admission Gate).** *Recommendation:* ratify.
- **RP-13 (Phase 0 role-audit scope).** *Recommendation:* ratify with the R-48 wording.
- **RP-14 (Meta-artifact grounding — REVISED v0.6).** §7.5 under the re-founded FP: ADDR designates N(C); FP designates the ∅-reduced expression; the classification-signature record, now a separate snapshot-indexed artifact, bears *describes* toward the reduced-form ICE; every asserted relation targets an ICE. *Recommendation:* ratify as revised; the fifth review's inversion of the FP collision story corrects a defect this specification carried from v0.2 onward, and the resulting three-tier model is cleaner than what it replaces.
- **RP-15 (Hash and serialization discipline).** *Recommendation:* ratify.
- **RP-16 (Identity epochs and constituent evolution — NEW v0.6).** §7.4 in full: the epoch triple; NORMAL_FORM_REINDEX with flagged degradations; FRAGMENT_MIGRATION with expansion-embedding, mandatory decomposition of bundled changes, and NON_EXPRESSIBLE_UNDER_FRAGMENT on restriction; fid in the manifest envelope and PinnedRef; the epoch condition on EQUIVALENT_REAXIOMATIZATION. *Recommendation:* ratify; a continuity system that governed theory drift while leaving its own normal-form and fragment versions ungoverned would have failed its headline claim at the first nfv bump, and the review was right to require this before ratification.

---

## Appendix A — Review Finding Register

R-01–R-12: ratification-track review of the informal proposal. R-13–R-21: first external review (v0.1). R-22–R-33: BFO ontologist review (v0.2). R-34–R-40: third external review (v0.3). R-41–R-44: fourth external review (v0.4). R-45–R-48: fifth review — BFO ontologist final pass (v0.5); all four accepted, refined in the accepting where noted; conditional sign-off satisfied by this revision.

| ID | Source | Finding | Disposition |
|---|---|---|---|
| R-01 | Rev. 0 | Space cannot transcend its signature; Llull/Leibniz lineage | §5, SE-2, RP-3; RIR/SIS (§5.3, RP-5) |
| R-02 | Rev. 0 | Addresses are theory-indexed | D-6, INV-3, §7.1, §7.3 |
| R-03 | Rev. 0 | Construction is the Lindenbaum–Tarski algebra | D-4 |
| R-04 | Rev. 0 | BFO won't fit through the EL keyhole | §9.1, FC-4, RP-1 |
| R-05 | Rev. 0 | Satisfiability filters almost nothing; ranking is the real problem | §6.4, §10, H2, FC-3 |
| R-06 | Rev. 0 | Covering relation fragile under cyclic GCIs | §6.3, D-7 |
| R-07 | Rev. 0 | Canonical representative selection is the hard half | §6.2, RP-2A/2B, FC-1 |
| R-08 | Rev. 0 | Alignment recorded, not discovered | §9.3, INV-4, FC-5 |
| R-09 | Rev. 0 | Embedding blindness; verbalization dependency | §10.3, FC-6; §10.4 |
| R-10 | Rev. 0 | Missing prior art; hypothesis trivially satisfiable | §16; B-2/B-3; §12 |
| R-11 | Rev. 0 | Phase numbering | §13 |
| R-12 | Rev. 0 | Falsification thresholds absent | §15 |
| R-13 | Ext. 1 | H1/FC-2 contradicted §6.4 | D-7 two modes; §6.5; FC-8; RP-8 |
| R-14 | Ext. 1 | Fingerprints must not serve as identity | D-6/D-6.1; INV-7; FP-only mode |
| R-15 | Ext. 1 | SPLIT unrecoverable from a bare address | §7.3; D-9; Collapse–Reversal Principle |
| R-16 | Ext. 1 | Status ladder inexpressive | §8 tuple; RP-10 |
| R-17 | Ext. 1 | SIS over-attributed | §5.3 RIR; RP-5 |
| R-18 | Ext. 1 | Cryptographic signature inside hashed payload; Σ-binding | D-3, D-3.1; RP-9 |
| R-19 | Ext. 1 | "Semantic survival" lacked a denominator | §9.1 Survival_Q; FC-4 |
| R-20 | Ext. 1 | Co-location vs coalescence conflated | INV-4; §9.3 |
| R-21 | Ext. 1 | "Identity under drift" overclaims | §1.1, §2.3 continuity wording |
| R-22 | Ext. 2 | TheoryID is manifest identity, not semantic theory identity | Manifest-indexed identity; D-3.2; OI-8 |
| R-23 | Ext. 2 | Satisfiable + instantiated ≠ ontologically admissible | §1.3; SE-5; §8.4 Gate; H5/FC-9; RP-12 |
| R-24 | Ext. 2 | "Definitive" outcomes vs witness-relative detection inconsistent | §7.3 successor/event separation |
| R-25 | Ext. 2 | Role-axiom fragment unspecified; CCO relation-heavy | D-1.1; §9.1 scope; RP-13 |
| R-26 | Ext. 2 | D-8 over-optimistic about "formal definitions" | D-8 projection grades |
| R-27 | Ext. 2 | RP-2 conflated existence with computability | §6.2 algorithm properties |
| R-28 | Ext. 2 | Consistency check verifies too little; FC-5 circular | §9.3 Consequence Preview; FC-5a/b/c |
| R-29 | Ext. 2 | Meta-artifacts should be BFO/CCO-grounded | §7.5; INV-8; RP-14 |
| R-30 | Ext. 2 | POSSIBLE and GROUNDED overload | SATISFIABLE; EVIDENCE_SUPPORTED |
| R-31 | Ext. 2 | D-5 "recovered under bounds" too strong | D-5 corrected |
| R-32 | Ext. 2 | FP in PinnedRef vs continuity presumption | D-9 continuity grades |
| R-33 | Ext. 2 | B-1 sampler unspecified; FC-8 extrapolation | §14.1 sampler; §6.5 caution |
| R-34 | Ext. 3 | RP-2 circular Phase-1 gate | RP-2A / RP-2B split; §13 |
| R-35 | Ext. 3 | ADDR not bound-invariant across canonicalization envelopes | §6.2 property 5; certified issuance; FC-1(iv) |
| R-36 | Ext. 3 | Σ lifecycle unspecified | D-2.1 append-only registry; SigmaID; defensive outcome |
| R-37 | Ext. 3 | FP cannot designate a class as then asserted | Superseded twice over: R-43's two-artifact repair, then R-46's re-founding |
| R-38 | Ext. 3 | *designates* asserted before its range condition was established | §7.5: all designata are ICEs; OI-10 demoted |
| R-39 | Ext. 3 | Admission Gate de-asserted imported classes | §8 provenance-qualified Naming; gate scope narrowed |
| R-40 | Ext. 3 | D-8 codomain type error | D-8 corrected: $P_O$ into 𝒰 |
| R-41 | Ext. 4 | No normative hash spec; injectivity overclaim; no collision policy | D-10; FC-1(v); RP-15 |
| R-42 | Ext. 4 | Semantic retirement ill-typed for role symbols | D-2.1(3) typed per kind; superseded in part by R-45's governance |
| R-43 | Ext. 4 | FP mistyped as Descriptive ICE; §1.3 stale | Two-artifact separation; superseded in part by R-46's re-founding |
| R-44 | Ext. 4 | OI-6's circulation SHALL self-blocked handoff | OI-6a executed (Appendix B); OI-6b re-gated to Phase 0 exit |
| R-45 | Ext. 5 | **"Role axioms become vacuous" is false**: Reflexive(r) + $\exists r.\top \sqsubseteq \bot$ has no model (nonempty domains); subroles are forced empty — real propagation, not vacuity; one ungated retirement could collapse 𝒰 | **INV-9** operative-theory consistency; Consequence Preview + consistency gate generalized to *all* manifest transitions (§9.3); D-2.1(3) rewritten with the counterexample recorded; FC-1(vi); blocked-retirement scenario in H4/FC-7. Refinement in accepting: EL⊥ consistency is the polytime test $T \not\models \top \sqsubseteq \bot$, so the gate is mechanically enforceable at activation, with justification extraction for diagnostics |
| R-46 | Ext. 5 | **FP's formal definition contradicted its collision semantics**: embedding the ∅-reduced form makes cross-class collision impossible ($R(C){=}R(D) \Rightarrow C \equiv_{\emptyset} D \Rightarrow C \equiv_T D$); the true failure mode is aliasing (many FPs per T-class); and hashing assertion-dependent classification made FP unstable under Naming events with TheoryID fixed | **FP re-founded**: $FP(C) = H(fid \| nfv \| TheoryID \| reduce_{\emptyset}(C))$ with the two-property statement (no cross-class collision; aliasing) in D-6.1; classification-signature record separated as ⟨FP, ReferenceSetID, bounds, AssertionSnapshotID⟩ (D-6.2); FC-1(iii) recast as alias multiplicity, the collision metric retired as measuring an impossible event; FP-only merge detection via reasoner equivalence; §7.5 FP designatum = the reduced-form ICE. **This corrects a defect present since v0.2 and carried through four review rounds, the drafter's included** — this round's principal catch. Refinement in accepting: retained ∅-reduced payloads MAY upgrade FP-only pins toward continuity by retrieval, without weakening the sourceExpression requirement |
| R-47 | Ext. 5 | **fid/nfv continuity absent**: PinnedRef omitted fid; no migration semantics for normal-form or fragment evolution; EQUIVALENT_REAXIOMATIZATION over-implied 1:1 across constituent changes | **§7.4 identity epochs** = (fid, nfv, hv); NORMAL_FORM_REINDEX (1:1 at class level, flagged degradations); FRAGMENT_MIGRATION (expansion = injective embedding under unchanged T-payload; bundled changes decomposed; restriction → NON_EXPRESSIBLE_UNDER_FRAGMENT); fid added to the manifest envelope (D-3) and PinnedRef (D-9); D-3.2 epoch-conditioned; RP-16. Refinement in accepting: hv needs no PinnedRef field — it rides inside every self-describing value per D-10 |
| R-48 | Ext. 5 | D-1.1's chain clause omitted the OWL 2 EL-specific property-chain/range restriction | D-1.1 wording patched per the W3C profile |

---

## Appendix B — OI-6a Verification Annex (pinned CCO artifact)

**Source artifact.** `raw.githubusercontent.com/CommonCoreOntology/CommonCoreOntologies/develop/src/cco-modules/InformationEntityOntology.ttl`, retrieved 2026-08-26. **SHA-256:** `294f81969d05af6d941625e08636d7f1289a1e36908aae22ca48d6176417571b`. Content is pinned by file hash; repo-commit capture and operative-release selection are folded into OI-6b. Definitions below are paraphrased; the file hash pins the exact text. **The fifth review independently spot-checked this annex against the current develop artifact and confirmed the load-bearing IRIs and meanings.**

| Term (label) | IRI | Verified characteristics |
|---|---|---|
| designates | `cco:ont00001916` | ObjectProperty; subPropertyOf *is about*; domain Designative ICE (ont00000686); **range `obo:BFO_0000001` (Entity)**; definition: given a context, the designator uniquely distinguishes its target entity from others |
| is about | `cco:ont00001808` | ObjectProperty; domain ICE (ont00000958); range Entity |
| describes | `cco:ont00001982` | ObjectProperty; subPropertyOf *is about*; domain Descriptive ICE (ont00000853); range Entity; **scope note: deliberately not declared functional, because one description may describe multiple entities** |
| Non-Name Identifier | `cco:ont00000649` | Class; subClassOf Designative ICE; definition: a character string designating an entity within a specified namespace or context, possibly automatically or randomly generated, typically without preexisting cultural or social significance |
| Descriptive Information Content Entity | `cco:ont00000853` | Class; subClassOf ICE; **definition in this artifact: an ICE that describes some Entity**; disjoint with Prescriptive ICE (ont00000965) |
| Designative Information Content Entity | `cco:ont00000686` | Class (domain of *designates*) |
| Information Content Entity | `cco:ont00000958` | Class; subClassOf `obo:BFO_0000031` (generically dependent continuant) |

**Load-bearing confirmations for §7.5:** the range of *designates* is BFO Entity, satisfied by ICE designata (N(C), the ∅-reduced expression); the non-functionality scope note on *describes* directly licenses the classification-signature record's non-unique correspondence to classes; and the Non-Name Identifier definition's coverage of automatically generated strings fits digest values. **Variance:** this artifact's Descriptive-ICE definition differs in phrasing from the reviews' attached materials ("set of propositions"); §7.5's repair holds under either reading, and release selection is OI-6b.

---

*End of FNSR-OPS-SPEC v0.6 — ratification candidate, third issue. The fifth review's conditional sign-off is satisfied by findings R-45–R-48; the Phase-1 entry set is RP-2A, RP-8–RP-13, RP-15, and RP-16. Submitted to the original reviewer for final sign-off; RP decisions rest with the Ratifying Architect.*
