# The Falsifiable Spec
## Method Specification — v0.4

| | |
|---|---|
| **Status** | Final draft — ratification candidate, submitted for adversarial review, cycle 4 |
| **Supersedes** | v0.3 |
| **Provenance** | v0.3 + review-cycle-3 findings R3-F15–R3-F21 and minors R3-M14–R3-M15, dispositioned at §10.7. The v0.3→v0.4 supersession walk is executed and recorded at §10.3; per PR-M3 the v0.3 disposition stood suspended from the cycle-3 review until that walk discharged. Authored under delegated authority, 2026-08-18. |
| **Normative language** | All uppercase BCP 14 keywords — MUST, MUST NOT, SHOULD, SHOULD NOT, MAY, REQUIRED, RECOMMENDED, NOT RECOMMENDED, OPTIONAL — per RFC 2119 / RFC 8174 (R3-M14: the profile widened rather than the vocabulary narrowed). |
| **Stable identifiers** | Principles P1–P11; claims M1–M3 and estimand M3-E; dispositions D-0–D-3; caps CAP-\*; witnesses W-\*; promises PR-\*; rated protocols RP-\*; declared absences NG-\* / NP-\*; weave records WV-\*; method defect records D-M-\*; falsifier classes FC-\*; open items O-\*. Prior identifiers retained; new identifiers minted, never renumbered. |
| **Self-score** | 20 / 22 — **D-3 Specification-complete** (single-rater, provisional per §6.3; §8.2). **Acceptance readiness: BLOCKED** — witness execution pending (O-04, O-05); closure lint pending (O-01). The two lines are deliberately separate (R3-F18): the grade says the intent is complete; the readiness line says whether a build could pass its gates today. |

A specification's job is not to *describe* a system but to *define it falsifiably*: **every normative clause, wherever it lives, appears in a closure map with a falsifier that bears on it**; universals carry properties; the composition is stated at every level — and the list of levels is itself declared, never assumed complete; and "done" is an ordered conjunctive whole-system acceptance the author states — the minimum over the whole, never a mean a stub can hide inside.

---

## 1. Purpose and users

**1.1 Users.** Spec authors, spec reviewers, and build coordinators — human or agentic — who hand specifications across an isolation boundary to builders who cannot ask the author what was meant.

**1.2 The need, in the user's words.** *"I can hand this document to a builder who has never spoken to me, and what comes back is the system I meant. And when it isn't, the grade told me where — before the build did."*

**1.3 The method's own spine.**

| Journey | Path | Walked by |
|---|---|---|
| **J-M1 Author** | need → templates (§4, §4A) → spec document with closure report | §5 (linklet), §5A (linklet-voice) |
| **J-M2 Grade** | spec → rubric (§6) → disposition + acceptance readiness + break sites + caps | §7 (counter-specimens), §8 (self-score) |
| **J-M3 Resolve conflict** | rule/witness disagreement → halt (P5) → recorded revision | §5, linklet §4 conflict record |
| **J-M4 Revise witness** | supersession (P10) → citation-graph walk → re-acceptance | linklet §11 (worked); **§10.2 (executed, v0.2); §10.3 (executed, v0.4)** |
| **J-M5 Falsify the method** | register scores → log break events per M3-E → compare | §2.3 protocol; ledger O-02 |
| **J-M6 Weave** | promises → scenes → cross-document seams → weave record → joint disposition | §4A, §5A, WV-1, §6.2 |
| **J-M7 Keep promises** | finding → disposition entry → register audit (PR-M1–PR-M3) | §1.4; §10.2, §10.3 executed walks; §10.7 dispositions |

Coverage: every operative section serves at least one journey (§8.1, the closure report, serves J-M2; §9 is a non-operative summary).

The method's seams:

| Seam | Producer → Consumer | Contract | Crossing example |
|---|---|---|---|
| **S-M1** | Templates → Rubric | a spec document in composition-plan form, closure report included | §5 — the specimen the rubric consumes |
| **S-M2** *(revised — R3-F18)* | Rubric → Gate decision | scored report: {per-dimension scores, disposition, **acceptance-readiness line with reasons**, break sites, active caps} | §8.2's dual verdict: `Disposition: D-3` · `Acceptance readiness: BLOCKED — O-04, O-05, O-01` |
| **S-M3** | Base template (§4) → Companion template (§4A) | the derivation-delta schema: {base §, disposition ∈ inherit \| adapt \| mint, delta} | the literal delta row: `base §6 Seams → adapt → adds status column; rows mirrored in both documents` |

**1.4 The method's lived surface (P11).** The adversarial review loop is the experience this method's users live: findings in, dispositions out, across cycles. The register:

| Promise | Normative statement | Falsifier class | Clause ↔ scene map |
|---|---|---|---|
| **PR-M1 — No finding vanishes** | Every finding raised in review receives a disposition entry — *resolved*, *resolved otherwise than proposed (reasons stated)*, *deferred (open item named)*, or *rejected (reasons stated)* — in §10. None is silently dropped. | Mechanical audit: register closure over every raised id. | Nominal: all cycle-3 items dispositioned at §10.7. Adversarial: a proposal not adopted as offered, registered with reasons — F-11's numeric cap (§10.6, historical) and R3-M14's replace-the-word option (§10.7, profile widened instead). |
| **PR-M2 — No unexecuted witness is called validated** | Registry status fields state execution truthfully; *pending* is the honest state until a transcript exists. | Mechanical audit: no status *validated* without a transcript reference. | Nominal: O-04/O-05 statuses standing honestly. Adversarial (**failed scene, retained**): defect **D-M1** — the v0.1→v0.2 supersession ran without its walk; logged §10.1, remediated §10.2. |
| **PR-M3 — Supersession suspends disposition** | A printed disposition does not survive its own supersession until the citation-graph walk and re-acceptance discharge (P10.3). The header MUST reflect suspension while triggers are open. | Mechanical audit: open triggers ⇒ no unsuspended disposition printed. | Nominal: two executed instances — v0.2's suspension discharged at §10.2; v0.3's discharged at §10.3, and the header provenance says so. Adversarial: D-M1, the walk that was skipped. |

**Posture (informative).** The review voice — severity language, the forest-and-trees figures, the closing exhortations — is posture: outside the graded surface. The partition is stated here.

**Terminal declaration (P1; NG-M1, rescoped — R3-F21).** Declaration schema: `{status, scope, authority, as-of}`. **NG-M1** = `{status: terminal; scope: the governance scope of this method's own registry (the FS method program); authority: the registrar (author of record); as-of: registry v0.4}`. This is a bounded claim, not a global negative existential: *within that scope, per that authority's knowledge at that registry version*, nothing composes above the review loop. Discovery of a sibling method document within scope supersedes NG-M1 and fires re-acceptance here; composition outside the declared scope is, by construction, another document's declaration to make.

---

## 2. Claims, illustration, and the method's falsifier

**2.1 Mechanism claims.**

- **M1 — Stub-satisfiability.** A requirement that carries no falsifier — a type signature, a mapping table, a prose sentence — can be satisfied vacuously. Its defects surface at external review of the assembled system, not at build time. A requirement that carries a worked `input → expected` example fails loud, early, and at build time.
- **M2 — Forcing function.** Authoring an *exact* expected output forces the author to resolve their own ambiguities before a builder inherits them. Where the author cannot write the expected output, the requirement was named, not defined.

**2.2 Illustration (non-normative).** In one retrospective build, components each verified at a mean module-level acceptance of **0.93** (on [0, 1]) while the assembled product received an external whole-system grade of **41.3** (on [0, 100]). The seams described by worked examples were built correctly; the seams described by mapping tables or interface signatures were where the build stubbed out or threw. Cautions, so the illustration cannot be spent against the method: the scales are deliberately incommensurable (a mean of parts and a judgment of the whole do not share a scale — that is the lesson; no arithmetic comparison is implied); one retrospective build, no denominators; and the confound is acknowledged — seams the author understood well enough to example were plausibly better specified throughout, which M2 absorbs: if examples work *because* writing them forces comprehension, the prescription stands on the forcing function, not the correlation.

**2.3 M3 — The method's own falsifier.** A falsifiability method that never states what would falsify it is, in its own taxonomy, describing.

**2.3.1 Protocol.** (1) For every spec entering a build under this method, rubric scores MUST be registered before build start. (2) Break events MUST be logged per M3-E as they occur. (3) Predictions: break events concentrate at dimensions scored ≤ 1 and at seams lacking crossing examples; where an experience level is declared, post-acceptance experience failures concentrate at promises lacking negative scenes and at unfilled cross-document seams; where sibling experiences share a substrate (the portfolio level, P1), joint failures concentrate at promise pairs citing the same declared absence — registered before that level is first instantiated.

**2.3.2 Estimand M3-E *(new — R3-F16)*.** The falsification condition is reproducible, not merely conceptual:

- **Break event.** A distinct root-caused defect discovered post-registration during build, integration, or acceptance. Repeated manifestations of one root cause within a build collapse to one event.
- **Attribution rule.** Each event is attributed to exactly **one** primary dimension — the dimension whose declared falsifier class would have caught it earliest. Contested attributions are adjudicated by the dual-rater machinery (§6.3). Secondary dimensions MAY be annotated; annotations do not count in the estimand. One defect = one observation, always.
- **Unit of analysis.** The (build, dimension) **cell**. Each registered build contributes one cell per applicable dimension. Exposure class per cell: **H** (registered score 2) or **L** (registered score ≤ 1).
- **Estimand.** ρ = expected break events per L-cell ÷ expected break events per H-cell, estimated by mixed-effects count regression (Poisson or negative-binomial as dispersion requires) with random intercepts for build and for product family — the clustering rule: correlated builds do not masquerade as independent evidence.
- **Decision criterion.** With margin δ and two-sided 90 % interval: **corroborated** if the lower bound of ρ exceeds δ; **falsified** if the upper bound of ρ falls below δ; otherwise **indeterminate**, and the corpus extends. Default δ = 1.5. Parameters (δ, confidence level, model family) are fixed at registration; the defaults bind absent registration; nothing is altered after data accrues.
- **Minimum information conditions.** The condition cannot trigger — in either direction — below **all** of: N ≥ 10 builds, ≥ 3 distinct product families, ≥ 15 L-cells in the corpus, ≥ 20 attributed break events. Sparse fallback where model fitting is unstable: exact conditional test stratified by build.
- **Sparse dimensions.** A dimension with < 3 L-cells across the corpus contributes to the pooled estimate only; no per-dimension claim is made for it.

**2.3.3 Consequence.** If falsified, the rubric fails as a predictor and the method MUST be revised or withdrawn.

**2.3.4 Anomaly rule.** Any seam with a *validated* crossing example that nonetheless breaks in build MUST be logged as an anomaly and triaged in the next revision. One anomaly does not falsify; unexplained accumulation does.

**2.3.5 Field-defect intake.** Post-acceptance experience defects enter the same ledger: promise id + scene-gap classification (*missing negative scene* \| *unfilled cross-document seam* \| *rated-protocol miss* \| *other*). The **registrar** — the named role owning the registries, weave records, and this ledger — is the author of record until delegated.

Evidence ledger status at v0.4: empty (O-02). Registration begins with the first spec graded under this version.

---

## 3. Principles

P1–P7 date to v0.0; P8–P10 minted in v0.1; P11 in v0.2. Text revised where a finding required it; the changelog (§10) records every revision.

### P1 — Composition is stated at every level: the level-schema *(revised in v0.4 — R3-F21)*

**Schema.** For every level at which parts compose into a whole that is lived, operated, or judged, the composition MUST be stated, accepted, and given a witness form. The schema — not any fixed list of levels — is the principle. Traceability runs upward and falsification runs downward at every joint: an item at level *n+1* with no home at level *n* falsifies the level-*n* list.

**Current instances.**

| Joint | Witness form | Since |
|---|---|---|
| components → capabilities | the worked example (P2) | v0.0 |
| capabilities → journeys | the chain example (P8) | v0.1 |
| journeys → experience | the scene (P11) | v0.2 |
| experiences → portfolio | the **interference scene** — named, minted at first instantiation (O-06) | v0.3 (named) |

**Closure rule.** The recursion closes by declaration, not by proof of a negative. The outermost level of every document MUST carry a **terminal declaration** with the schema `{status: terminal | delegated(companions) | awaiting; scope: governance scope G or product boundary B; authority: A; as-of: registry version V}`. A terminal declaration is a **bounded** claim — *within scope, per authority, at version* — never a global negative existential the author has no mechanism to establish (R3-F21). It is auditable and supersedable: discovery of composition within the declared scope is a supersession event; composition outside it is another declaration's burden. *Awaiting* additionally registers the anticipated level's predicted failure mode in M3 before instantiation. No version of this method may claim the spine complete; it may only claim the current outermost level declared. This document's declaration: NG-M1 (§1.4).

**Predicted failure at the named next level** (registered, §2.3.1): sibling-promise interference — two experience documents pairwise-green against a shared substrate, jointly contradictory, as when one promises "deletion is impossible" and a sibling mints deletion. The NG-\* mechanism (P10.5) makes the collision mechanically detectable through the shared registry.

**Experience-level applicability** is defined semantically at P11 (R3-F19); the level exists for a document iff at least one of its normative requirements is trajectory-ranging under that test.

- **Prevents:** parts that pass and a whole that doesn't — at any level, including levels not yet built; a method that declares victory one level below the next failure; and local documents making global claims their authority cannot carry.
- **Do:** lead each document with its outermost declared level; derive each level from the one above; declare terminal status with its full schema.

### P2 — Every normative clause carries a falsifier: universal closure *(revised in v0.4 — R3-F15)*

**The law, now enforced at its own strength.** §9 has said from v0.1 that a requirement MUST carry its own falsifier; through v0.3 the operational machinery enforced this only class-by-class — witnesses for capabilities, pairs for rules, scenes for promises — leaving no mechanism proving that *every* normative clause belongs to some class and has a falsifier. v0.4 closes the gap:

1. **Clause identifiability.** Every normative clause — every sentence bearing a BCP 14 keyword — MUST be identifiable at a declared granularity: explicit clause labels for standards documents; for specs authored in the templates, membership in a template structure (§2–§11) is the identification.
2. **Falsifier classes (FC-\*).** Every clause maps to exactly one class:

| Class | Requirement kind | Falsifier form | Governing principle |
|---|---|---|---|
| **FC-W** witness | capability behaviour | nominal + one-factor edge-deltas | P2 (this clause) |
| **FC-RW** rule-witness pair | data/derivation rules | rule + citing witnesses, bidirectional | P5 |
| **FC-X** crossing example | seams, cross-document included | literal instance + status | P3 |
| **FC-P** property | universally quantified requirements | scope + generator + property + n | P9 |
| **FC-C** chain | journeys | chain example / chain scene | P8 |
| **FC-S** scene | trajectory-ranging promises | turns + masks-with-properties, adversarial included | P11 |
| **FC-R** anchored rated protocol | qualitative clauses with no adequate mechanical falsifier | RP + pass/fail anchors + panel | P11 |
| **FC-M** measurement | envelopes | threshold + stated method | template §8 |
| **FC-A** audit | structural, governance, and procedural clauses | mechanically checkable condition over the document or registry | P10, O-01 |

3. **The closure map.** For each clause: `closure(c) = ⟨c, class(c), falsifier(c), validation(c), gate(c)⟩` — the full correspondence **normative clause → requirement class → falsifier → validation → consuming gate**. Every conforming document MUST carry a **closure report** (template §12): the map at declared granularity, free-floating clauses enumerated, and **orphan clauses** — clauses with no falsifier, or (R3-F20) with only falsifiers that do not bear on them — named as defects and dispositioned. The report is cheap exactly when the spec is well-formed: template structures pre-classify their contents, so the expensive rows are precisely the clauses living outside any structure — which is the defect the report exists to expose.
4. **Capability instantiation** (the v0.0 core, unchanged as FC-W): each capability carries exactly one nominal witness and SHOULD carry one-factor edge-deltas; a failing composite conflates causes, deltas localize. The example is the requirement; the prose is its commentary. If you cannot write the expected output, you have named the requirement, not defined it.

- **Prevents:** the gap between the method's strongest sentence and its enforcement — clauses that are normative in voice and unfalsifiable in fact, hiding between the classes.
- **Do:** one closure report per document; zero undispositioned orphans; O-01's lint automates the extraction and the check.

### P3 — State the composition; a seam is a contract *plus a crossing example* *(revised in v0.3)*

Every producer → consumer edge MUST be named, with its contract and a **crossing example**: one concrete, fully literal artifact instance. A contract without a crossing example is an interface, and P4 applies.

**Seams MAY cross document boundaries**, mirrored as rows in both documents with one shared contract and one literal crossing example. A posed-but-unmet requirement is a row with status *pending* — legitimate during authoring, a named defect at the gate: it does not zero P3 (the row exists and is honest) but activates **CAP-1** (§6.2), bounding the pair's joint disposition at D-2 until filled. Cross-document seam fill is scored here, not at P11 — one defect, one break site. Crossing examples are literal; masks and properties live in witnesses (P6); instances live in seams.

- **Prevents:** integration as afterthought; contract drift discovered at assembly; seams green because nothing concrete ever crossed them; alignment by assertion between documents sharing no testable edge.
- **Do:** a seam table — producer, consumer, contract, crossing example, status — one row per edge, mirrored on both sides.

### P4 — An interface is not a behaviour *(unchanged since v0.0)*

A type signature — `infer(input) → Result` — is satisfiable by a stub that returns nothing. Specify the *behaviour* of every surface, hardest at the public and integration surfaces, where "looks done" and "is done" diverge most.

- **Prevents:** the integration surface shipping as a stub that satisfies its signature and hides an unbuilt system behind a green check.
- **Do:** a behavioural acceptance example for every surface, the public API included — never only its type.

### P5 — Rule and witness, and they MUST agree *(revised in v0.1)*

Every rule MUST be paired with at least one witnessing example; every example MUST name its rule. **Precedence: none.** A rule/witness conflict is a spec defect: the build MUST halt at that requirement and return to the author (refuse-by-default); resolution is a recorded revision — the rule amended or the witness superseded under P10. Witnessed twice in this record: linklet §4, and the method's own §6.2 "ten dimensions" conflict (§10.2).

- **Prevents:** silent mis-generalisation from examples alone; unfalsifiable rules alone; a precedence contest one side wins without the author knowing.
- **Do:** bidirectional pairing; disagreement is a stop-the-line event, not a tie to break.

### P6 — Declare non-determinism; mask with properties, not blindness *(revised in v0.1)*

Every capability MUST name the parts of its output that vary between runs, so acceptance is exact where the output is stable and masked where it is not — and **every masked field MUST still carry a property assertion** (format, window, distinctness, permutation-of-expected-set). Blind masking reopens the vacuous pass. Applies to the method's own acceptance: rater variance is declared and masked at §6.3.

- **Prevents:** acceptance examples that can never pass — or that pass by comparing so loosely they assert nothing.
- **Do:** a determinism note per capability: stable, masked, and the property each mask still asserts.

### P7 — "Done" is an ordered conjunction, whole-system, weakest-link *(revised in v0.4 — R3-F17)*

**The acceptance operator, formally.** For gates g₁…gₙ in declared order: **ACCEPT = g₁ ∧ g₂ ∧ … ∧ gₙ**. The verdict is the conjunction — every gate must pass, and evaluation order does not change the logical outcome. The order governs **evaluation and reporting**: evaluation MAY short-circuit at the first failing gate, and the report leads with it (outermost failure first). Equivalently, with gates valued pass = 1 / fail = 0, the aggregate is **min(g₁…gₙ)** — the weakest link — never a mean. Earlier versions called this "lexicographic"; the term is retired from normative text because the mechanism is ordered conjunction, not tuple comparison (historical records retain it unamended, per the §10.3 convention).

**The gate order.** (1) No knockouts or coverage defects; (2) every promise accepted via its scenes, where the experience level is declared — or, where **delegated**, discharged through the companion's promise acceptance and the weave record; (3) every journey accepted; (4) every capability accepted; (5) every seam's crossing example exercised, cross-document included; (6) every property passes at stated scope; (7) every envelope met. The list extends outward as level-schema instances are minted (P1).

**Disposition versus acceptance readiness (R3-F18).** Disposition (§6) grades *documents*; acceptance gates *builds*; and every graded report now carries both lines — `Disposition:` and `Acceptance readiness: READY | BLOCKED(reasons)`. A document pair can be D-3 Specification-complete while its readiness is BLOCKED on pending validations: the intent is fully handed over; the build simply cannot pass its gates yet, and the vocabulary no longer lets the first fact impersonate the second.

- **Prevents:** the scoreboard that reads healthy while the product is unusable; and a grade label quietly read as an authorization to ship.
- **Do:** an explicit acceptance statement (template §10) as the ordered conjunction above; both report lines, always.

### P8 — Journeys are accepted end-to-end *(revised in v0.2)*

Capabilities compose into journeys; per-capability green plus per-edge green is not path coverage. Each journey MUST be named and MUST carry a **worked chain example** — the sequence of invocations with carried state explicit, ending in the expected whole-journey outcome.

**Coverage rule, at every joint of the spine:** every item at level *n+1* MUST map to at least one item at level *n* serving it — journey step → capability; promise → journey — and a homeless item is a **coverage defect** falsifying the level-*n* list. A level-*n* item serving nothing above it is a **coverage warning**, dispositioned by the author.

- **Prevents:** a min over a list nothing audits; a journey list that walks everything except what was promised.
- **Do:** named journeys with worked chain examples; bidirectional coverage maps at every joint.

### P9 — Universals are discharged by properties *(revised in v0.4 — R3-M15)*

A witness spot-checks a ∀-statement; it cannot falsify-cover it. Every universally quantified requirement MUST (1) declare its **scope** explicitly — an unscoped ∀ silently claims the strongest reading — and (2) carry a **generator + property** with stated n or coverage rule. Witnesses MAY accompany properties as pinned regression points.

**Interaction coverage *(new)*.** One-factor edge-deltas (P2) localize single-factor failures and remain the required baseline; they systematically miss interaction defects — A passes, B passes, A+B fails. Where two or more factors participate in the same rule, seam, or invariant and interaction is plausible, the specification SHOULD carry an **interaction witness or property** covering the combination, marked as such so a failure localizes to the *pair* rather than dissolving into combinatorics. Worked instance: linklet V2, whose generator interleaves resolves across ids — multiplicity × interleaving covered as a property, not an explosion of deltas.

- **Prevents:** invariants "verified" by one example; accidental n×m scopes; and the interaction defect no single-factor delta can see.
- **Do:** per invariant — scope, generator, property, n, one pinned witness; interaction combinations named where plausible.

### P10 — Witnesses are governed artifacts *(revised in v0.3)*

A wrong witness is worse than ambiguous prose: it is exact and authoritative, and the build will faithfully implement the author's arithmetic error. Therefore:

1. **Validation.** Before any gate consumes a witness, it MUST be validated — executed against a reference implementation or independent oracle **in a clean environment**, or, for rated properties, adjudicated by the panel that *is* the oracle (P11): a permanent branch, not a stopgap.
2. **Versioning.** Witnesses carry stable ids and versions; scenes and anchors ride the same registry.
3. **Supersession.** Changing an expected output is a supersession event: the superseded witness is retained, and every citing artifact MUST be re-accepted against the successor before the document regains its disposition. A supersession of the *document itself* triggers the same walk over everything citing the revised sections — skipping it is defect D-M1's shape, and PR-M3 makes the suspension promissory.
4. **Reciprocity.** Cross-document citations MUST be recorded in **both** registries; supersession in the producing document fires triggers in every citing document; document pairs federate through weave records (WV-\*).
5. **Absences are registry citizens.** Non-goals and non-promises carry stable ids (NG-\*, NP-\*) with the declaration schema `{status, scope, authority, as-of}` where applicable (P1), and enter the citation graph. Minting a capability that discharges a cited absence **is a supersession event**. A load-bearing absence that is uncitable is a promise the registry cannot see breaking.

- **Prevents:** an authoritative wrong number gating a build; silent drift across revisions and across document boundaries; promises over absences that die by omission.
- **Do:** a witness registry (template §11) with validation status, version, and a citation graph whose citizens include scenes, anchors, and declared absences, mirrored across pairs.

### P11 — Promises are falsified by scenes *(revised in v0.4 — R3-F19, R3-F20)*

**Applicability, defined semantically (R3-F19).** P11 applies to a normative requirement iff the requirement **ranges over an interaction history, a user-observable sequence, or context-dependent behaviour not reducible to a single capability invocation** — it quantifies over *trajectories*, not invocations. The scene *follows from* applicability rather than defining it: where a requirement is trajectory-ranging, its truthful fixture is turns-in / expected-behaviour-out. ("The honest falsifier is a scene" — v0.3's test — is retained as a symptom, demoted from definition.) Applicability is assessed **per requirement**; a document has an experience level iff at least one of its requirements is trajectory-ranging, and mixed documents are normal: a GUI, an agentic pipeline, an approval workflow may hold both trajectory-ranging clauses (scenes) and invocation-scoped clauses (witnesses) without strain.

Where it applies, the experience document is the outermost declared level of the spine, its unit requirement the **promise** — a normative statement of what the experience guarantees or refuses — and a promise's witness is a **scene**: a worked interaction fixture, turns in, expected behaviour out, in the W-\* namespace under P10. Because lived surfaces are typically generative, a scene's expected output is mostly mask and **P6 becomes load-bearing**: every masked span carries a property — a mutation absent, an option offered at most once, every grounded claim inside its **reliance set** (§4A §9).

**Falsifier discipline (R3-F20 — clause relevance replaces the mechanical quota).** v0.3's rule 2 — every promise carries ≥ 1 mechanical property — is **superseded**: a quota invites decorative mechanical checks that pass without testing the clause that matters, reopening the original vacuous pass in miniature. The rules are now:

1. **Clause relevance.** Every normative clause MUST have at least one falsifier that **bears directly on that clause** — a falsifier is adequate for a clause iff its passing entails the clause's satisfaction within stated scope, not merely correlates with it. A clause whose only falsifiers are irrelevant is an **orphan clause** (P2.3), however many checks surround it.
2. **Mechanize-before-rate, per clause.** A falsifier MUST be mechanical where an adequate mechanical falsifier exists; each rated declaration states in one line why none does.
3. **Anchored protocols.** Every rated protocol (RP-\*) MUST carry ≥ 1 pre-rated **pass anchor** and ≥ 1 pre-rated **fail anchor** transcript — the nominal and the adversarial at the protocol level, W-\* governed.
4. **The panel is the oracle.** A rated falsifier MAY solely bear a clause when the mechanize-before-rate test finds no adequate mechanical one — a genuinely qualitative clause such as *"responses do not demean the user"* is solely borne by its anchored panel, and that is rigor, not a concession. An undeclared vibe is not a falsifier; a declared protocol without anchors is a rule without a witness.

**Structure.** The negative scenes are the deliverable: every promise family MUST carry at least one adversarial scene where the surface is invited to break the promise and the expected behaviour is the refusal, absence stated as the assertion. **Clause-level closure**: every normative clause of a promise is covered by ≥ 1 clause-relevant scene, and the register carries the clause ↔ scene map — now the P11 instantiation of P2's universal closure rather than a special case. The document partitions into **promises (normative, witnessed, graded)** and **posture (informative, ungraded)**.

- **Prevents:** experience documents as decoration no gate consumes, or gutted to the mechanically checkable; decorative mechanical checks laundering qualitative clauses; and experience failures living *between* journeys where no journey witness can see them.
- **Do:** a promise register with PR-\* ids, clause ↔ scene maps, clause-relevant falsifiers, rated protocols named-justified-anchored, the partition stated.

---

## 4. Template — composition-plan form, v0.4

**On order.** The section order is the *reading* and *acceptance* order, not the *authoring* order: authoring is iterative, and the template states the shape of the fixed point.

| § | Section | Principles | Contents |
|---|---|---|---|
| 1 | **Purpose & user** | — | Who it is for; the need in their words. |
| 2 | **Journeys** | P8 | Per journey: id, narrative, worked chain example (carried state explicit), whole-journey outcome. Bidirectional coverage map to §3. |
| 3 | **Capabilities** | P1, P2, P6 | Per capability: id + name; nominal witness; one-factor edge-deltas; boundary shapes; determinism note — masked fields and the property each asserts. |
| 4 | **Data model & rules** | P5 | Each rule once, paired with named witnesses; conflicts halt. |
| 5 | **Decomposition** | P1 | Components traceable to capabilities. Derived, never authored first. |
| 6 | **Seams** | P3, P4 | One row per edge: contract, literal crossing example, status. Cross-document rows mirrored. |
| 7 | **Invariants & properties** | P9 | Per invariant: scope, generator, property, n; pinned witness; interaction combinations named where plausible. |
| 8 | **Envelopes** | — | Each with a falsifiable threshold **and** a stated measurement method. |
| 9 | **Non-goals** | P10.5, P1 | Each absence with a stable NG-\* id; the terminal declaration with its full schema `{status, scope, authority, as-of}`. |
| 10 | **Acceptance** | P7 | The ordered gate conjunction, stated; witness-validation precondition with status; both report lines. |
| 11 | **Change discipline** | P10 | Witness registry: id, version, validation status, citation graph with reciprocal entries and NG/NP citizens; supersession protocol; weave records referenced. |
| 12 | **Closure report** | P2 | *(new — R3-F15)* The map `clause → class → falsifier → validation → gate` at declared granularity; free-floating clauses enumerated; orphan clauses named and dispositioned. |

---

## 4A. Companion template — experience-document form, v0.4

Derived from §4 by stated deltas — every base section *inherit* / *adapt* / *mint*, none dropped. *(v0.4 walk catch, §10.3: the v0.3 table had no home for the scene registry its own specimen carried at §13; the row is minted and the template now matches its witness.)*

| § | Section | Derivation | Principles | Contents / delta |
|---|---|---|---|---|
| 1 | **Purpose & user** | adapt base §1 | — | Who lives in this experience; the promise of it in their words. |
| 2 | **Promise register** | mint | P11 | Per promise: PR-\* id; normative statement; **clause ↔ scene map with clause-relevant falsifiers**; rated declarations with one-line mechanize-before-rate justifications; NG/NP citations. |
| 3 | **Posture** | mint | P11 | Informative only; the partition stated here. |
| 4 | **Journeys** | inherit base §2 | P8 | Chain scenes; harness named with owner; bidirectional coverage maps at both joints. |
| 5 | **Surface capabilities** | adapt base §3 | P2, P6, P11 | The mediator's capabilities (CV-\*); witnesses are scenes; a property per masked span. |
| 6 | **Conversational data model & rules** | adapt base §4 | P5 | Session/state model; routing and force rules (RV-\*), each with its witnessing scene. |
| 7 | **Decomposition** | inherit base §5 | P1 | The mediator's components — a component, not a vapor. |
| 8 | **Cross-document seams** | adapt base §6 | P3 | Rows mirrored in the substrate; asks appear as *pending* (CAP-1). |
| 9 | **Invariants & properties** | inherit base §7 | P9 | Experience-level ∀s. **Normative definition — reliance set:** the substrate responses received in the scene's harness log before the claim; grounded-claim properties assert claim ⊆ reliance set. |
| 10 | **Envelopes** | inherit base §8 | — | Responsiveness and similar; **rated-protocol thresholds** (pass rule, adjudication path). |
| 11 | **Non-promises** | adapt base §9 | P10.5 | Each with a stable NP-\* id, citable and dischargeable. |
| 12 | **Consequence gates** | mint | P11 | **Normative definition — consequence levels:** an ordered classification of acts crossing the conversational → invocation boundary by reversibility and blast radius; classes declared per document (default L0 read \| L1 reversible \| L2 irreversible). Each transition names its gating scene; an empty class is witnessed by the refusal scene proving it empty. |
| 13 | **Scene & anchor registry** | mint *(v0.4)* | P11, P2, P6, P10 | Per scene: W-\* id, turns, expected behaviour with masks, the property each mask carries; adversarial scenes marked, absences stated as assertions; RP anchors (pass + fail) registered here. |
| 14 | **Acceptance** | inherit base §10 | P7 | Ordered conjunction: coverage clean → promises via scenes (clause maps closed; rated under anchored protocols) → journeys via chain scenes → seams → invariants → envelopes. Validation precondition with status; both report lines. |
| 15 | **Change discipline** | inherit base §11 | P10 | Scenes, anchors, NG/NP citations on the federated registry; reciprocal entries; weave records (WV-\*) housed here and mirrored in the substrate. |
| 16 | **Closure report** | inherit base §12 | P2 | The clause → class → falsifier → validation → gate map for the experience document. |

---

## 5. Specimen — `linklet` (normative witness for §4)

*Carried from v0.3; v0.4 deltas: §7 interaction annotation, §9 declaration schema, §10 operator rename, §12 minted. Re-accepted at §10.3.*

#### linklet §1 — Purpose & user
People paste long URLs and get short stable links; anyone opening a short link reaches the original; the creator can see how many times a link was opened.

#### linklet §2 — Journeys

**J1 — share-and-verify.** Worked chain example **W-J1** (carried state in bold): (1) `POST /links {"url": "https://example.org/a?b=1"}` → `201`, minted **`<ID>`** (W-C1-N). (2) `GET /<ID>` → `302 Location: https://example.org/a?b=1`; one HitEvent appended (W-C2-N). (3) `GET /links/<ID>/stats` → `200 {"id": "<ID>", "hits": 1}` (W-C3-N). Whole-journey outcome: the count in step 3 reflects exactly the open in step 2, for the id minted in step 1. Coverage map: J1 → {C1, C2, C3}; every step homed; every capability in ≥ 1 journey; clean.

#### linklet §3 — Capabilities

**C1 — shorten.**
- **W-C1-N (nominal):** `POST /links {"url": "https://example.org/a?b=1"}` → `201 {"id": "<ID>", "url": "https://example.org/a?b=1", "created_at": "<TS>"}`
- Determinism note: `<ID>` masked, property `^[a-z0-9]{6}$`; `<TS>` masked, property ISO-8601 UTC within ±5 s of request.
- **W-C1-Δ1:** `"url": null` → `422 {"error": "E-VAL-01", "field": "url"}` · **W-C1-Δ2:** `"url": "example.org/a"` → `422 {"error": "E-VAL-02", "field": "url"}` · **W-C1-Δ3:** nominal twice → two `201`s; property: ids distinct (no deduplication, NG-L4).

**C2 — resolve.**
- **W-C2-N (nominal):** `GET /<id>` for an id from W-C1-N → `302 Location: https://example.org/a?b=1`; exactly one HitEvent `{"id": "<same>", "at": "<TS>"}` appended (window property as above).
- **W-C2-Δ1 (negative witness):** `GET /zzzzzz` → `404 {"error": "E-RES-01"}`; HitEvent count **unchanged** — the absence is the assertion.

**C3 — stats.**
- **W-C3-N (nominal):** after W-C1-N → W-C2-N, `GET /links/<id>/stats` → `200 {"id": "<same>", "hits": 1}`. · **W-C3-Δ1:** zero resolves → `{"hits": 0}` · **W-C3-Δ2:** unknown id → `404 {"error": "E-RES-01"}`.

#### linklet §4 — Data model & rules

`LinkRecord {id, url, created_at}` (state); `HitEvent {id, at}` (event); counts **derived, never stored**.

- **R1 — URL validity.** Absolute `http`/`https` only. Witnesses: W-C1-N (satisfaction), W-C1-Δ2 (violation). Taxonomy: `E-VAL-01` missing; `E-VAL-02` malformed.
- **R2 — Count derivation.** `hits(id) ≡ |HitEvents(id)|`, computed at read. Witnesses: W-C3-N, W-C3-Δ1.

**Conflict record (P5, demonstrated).** An earlier draft had R1's prose read "invalid urls yield `E-VAL-01`" while W-C1-Δ2 expected `E-VAL-02`. Halt; return; resolution recorded: the rule amended (two-error taxonomy minted), witnesses unchanged. Neither artifact governed silently.

#### linklet §5 — Decomposition
**gateway** — HTTP surface + validation; serves C1–C3. **ledger** — records, events, derivation; serves C1 (persist), C2 (append), C3 (R2).

#### linklet §6 — Seams

| Seam | Producer → Consumer | Contract | Crossing example (literal) | Status |
|---|---|---|---|---|
| S1 | gateway → ledger | `LinkRecord {id, url, created_at}` | `{"id": "7fk2qp", "url": "https://example.org/a?b=1", "created_at": "2026-08-18T14:02:11Z"}` | filled |
| S2 | gateway → ledger | `HitEvent {id, at}` | `{"id": "7fk2qp", "at": "2026-08-18T14:03:40Z"}` | filled |
| S3 | ledger → gateway | `Count {id, hits}` | `{"id": "7fk2qp", "hits": 1}` | filled |

#### linklet §7 — Invariants & properties

- **V1 — Resolution soundness.** Scope: all LinkRecords crossing S1. Generator: ≥ 100 random R1-valid urls. Property: `resolve(shorten(u).id)` → `302 u`. Pinned: W-C1-N/W-C2-N.
- **V2 — Count conservation** *(interaction property — P9, R3-M15)*. Scope: any minted id. Generator: random k ∈ 0..20 resolves, randomly interleaved with resolves of other ids — the **multiplicity × interleaving** combination covered as a property. Property: `stats(id).hits = k`. Pinned: W-C3-N.

#### linklet §8 — Envelopes
**E1:** `GET /<id>` p95 < 50 ms at 100 req/s for 60 s on profile H-1 (4 vCPU / 8 GB, loopback), by a stated load driver committed alongside the spec.

#### linklet §9 — Non-goals *(declaration schema per P1/P10.5)*

- **NG-L0 — Experience level:** `{status: delegated(linklet-voice, §5A); scope: the linklet product boundary; authority: spec author of record; as-of: registry v0.4}` — discharged through WV-1.
- **NG-L1** authentication · **NG-L2** custom aliases · **NG-L3** expiry · **NG-L4** deduplication · **NG-L5** analytics beyond the count.
- **NG-L6 — deletion.** No capability removes a LinkRecord or HitEvent. *(Minted in v0.3 when the §10.2 walk caught PR-2 citing an undeclared absence.)*

#### linklet §10 — Acceptance (ordered conjunction — P7)

1. No knockouts; coverage maps clean. 2. Experience gate: delegated per NG-L0, discharged by linklet-voice §14 through WV-1. 3. J1 via W-J1. 4. C1–C3: every nominal and every delta. 5. S1–S3 exercised; cross-document obligations via WV-1 reciprocity. 6. V1–V2 at stated generators and n. 7. E1 under its stated method.

**Witness precondition (P10):** every W-\* validated against `linklet-ref` in a clean environment before any gate consumes it. *Status at v0.4: not yet executed — O-04.* **Report lines:** `Disposition: per §6` · `Acceptance readiness: BLOCKED — O-04`.

#### linklet §11 — Change discipline

Registry: every W-\*, version 1, status *pending O-04*, citations recorded (W-C1-N ← J1, R1, S1, V1). **Reciprocal entries (P10.4)**, federated via WV-1:

| Local artifact | External citer (linklet-voice) |
|---|---|
| W-C2-N | W-JV1 (step 2), S-V2 |
| C1 request/response shapes | S-V1 |
| C3 response shape | S-V2 |
| NG-L6 | PR-2, W-PR2-N, W-PR2-Δ2, J-V2 |
| NG-L0 | WV-1 |

Worked supersessions: (data) `W-C3-N → W-C3-N.2` fires W-J1 re-run, S3 update, R2 re-acceptance by inspection, **and via reciprocity S-V2 + W-JV1 in linklet-voice**; (absence) minting deletion supersedes **NG-L6**, firing PR-2, its scenes, and J-V2 across the federated registry. Disposition is not regained until all triggers discharge.

#### linklet §12 — Closure report *(new — P2)*

Granularity: template structure. Free-floating normative clauses: **none** — every clause lives in a structure, so the map is the structures themselves:

| Clauses | Class | Falsifier | Validation | Gate |
|---|---|---|---|---|
| C1–C3 behaviour | FC-W | W-C1/2/3-\* | linklet-ref (O-04) | §10.4 |
| R1, R2 | FC-RW | rule ↔ witness pairs, §4 | linklet-ref (O-04) | §10.4 |
| S1–S3 | FC-X | crossing examples, §6 | integration run | §10.5 |
| V1, V2 | FC-P | generators + properties, §7 | property runs | §10.6 |
| J1 | FC-C | W-J1 | harness run | §10.3 |
| E1 | FC-M | stated load method | measurement run | §10.7 |
| NG-\* declarations, registry rules | FC-A | registry audits (O-01 lint class) | audit | §10.1 |

Orphan clauses: **0**. The report is short precisely because the spec is well-formed — the demonstration the section exists to make.

---

## 5A. Specimen — `linklet-voice` v0.4 (normative witness for §4A)

*Carried from v0.3; v0.4 deltas: §2 falsifier framing rebased on clause relevance (R3-F20), §13 now matches the minted template row, §14 operator rename + report lines, §16 minted.*

#### linklet-voice §1 — Purpose & user
People manage their links by talking: "shorten this," "how many opens?" The promise, in their words: *"I can just ask — and asking for something the system doesn't do won't quietly do something else."*

#### linklet-voice §2 — Promise register

**PR-1 — You may ask naturally.** A plain-language request maps to the substrate capability that serves it, without command syntax.
Clause ↔ scene map (all clause-relevant, all mechanical): natural mapping → W-PR1-N (correct invocation crosses S-V1) · invalid-input honesty → W-PR1-Δ1 (zero records created) · multi-turn routing with carried state → W-JV1 (reply count = substrate count).

**PR-2 — Asking for deletion does not delete, fake, or promise.** The substrate declares deletion out of scope (**cites NG-L6**); the surface must not (a) mutate in response to destructive-sounding requests, (b) assert or imply a deletion occurred, (c) commit to future deletion, and (d) refuse without scolding.
Clause ↔ scene map, per P11 v0.4: (a) → W-PR2-N, mechanical (counts unchanged) — relevant: its passing entails the clause · (b) → W-PR2-N, mechanical (no success-assertion span; V-V1) · (c) → W-PR2-Δ2, mechanical (no commitment span) · (d) → **solely borne by RP-1**, rated (mechanize-before-rate, one line: "scolding" is a judgment of register, not of spans; no adequate mechanical falsifier exists) — permitted under P11.4 because the clause is genuinely qualitative, and anchored. Mood-invariance across (a)–(d) → W-PR2-Δ1. *(v0.3 justified this register via the mechanical-property quota; the quota is superseded — every falsifier above stands on relevance to its clause, which is the stricter test.)*

#### linklet-voice §3 — Posture *(informative)*
An operator, not a gatekeeper: brief, concrete, offering what *is* possible. Outside the graded surface — the partition, demonstrated.

#### linklet-voice §4 — Journeys

**J-V1 — voice-share-and-check.** Chain scene **W-JV1**, harness **H-JV1** (drives surface and substrate in one clean environment; owner: this document's acceptance runner, per the consuming-document-owns convention; registered both sides via WV-1): (1) W-PR1-N mints **`<ID>`**; (2) out-of-band `GET /<ID>` resolves once (substrate W-C2-N); (3) "how many times was `<ID>` opened?" → surface invokes C3; reply contains "1". Carried state: the id from step 1 binds step 3.

**J-V2 — ask-and-be-refused.** Chain: W-PR2-N alone; whole-journey outcome: substrate state untouched (counts identical before and after).

Coverage: PR-1 → J-V1 → {CV-0, C1, C3}; PR-2 → J-V2 → {CV-0}. Every promise homed; every journey serves a promise; every step homed. Clean.

#### linklet-voice §5 — Surface capabilities
**CV-0 — converse/route.** Classify the utterance; invoke the serving capability or refuse with an available alternative. Witnesses are its scenes: W-PR1-N, W-PR1-Δ1, W-PR2-N. Determinism note: phrasing masked; properties per scene — minted id verbatim and no other id; no success-assertion span without invocation; no commitment span.

#### linklet-voice §6 — Conversational data model & rules
State: `Session {turns[], harness_log[]}` — the harness log is the reliance-set source (§9).
- **RV-1 — Mood does not reclassify force.** Illocutionary force is invariant under grammatical mood and politeness marking. Witness: W-PR2-Δ1.
- **RV-2 — Refusals name an available alternative when one exists.** Witness: W-PR2-N (names stats). Mechanical property: refusal replies reference ≥ 1 capability in linklet §3.

#### linklet-voice §7 — Decomposition
**router** — classify + dispatch; serves CV-0 (classification legs). **composer** — reply construction under the properties; serves CV-0 (phrasing legs).

#### linklet-voice §8 — Cross-document seams

| Seam | Producer → Consumer | Contract | Crossing example (literal) | Status |
|---|---|---|---|---|
| S-V1 | voice surface → linklet gateway | invocation per linklet §3 request shapes | "shorten https://example.org/a?b=1" → `POST /links {"url": "https://example.org/a?b=1"}` | filled |
| S-V2 | linklet gateway → voice surface | linklet §3 response shapes → reply content | `200 {"id": "7fk2qp", "hits": 1}` → reply containing "1" for id 7fk2qp | filled |

Mirrored in linklet §11. No pending rows; CAP-1 inactive.

#### linklet-voice §9 — Invariants & properties
*Reliance set (normative): the substrate responses received in the scene's harness log before the claim.*
- **V-V1 — No uninvoked success.** Scope: all replies in all scenes + generated corpus. Generator: n ≥ 50 destructive/creative solicitations, paraphrase-varied. Property: any success-assertion span ⇒ a matching invocation in the harness log. Pinned: W-PR2-N.
- **V-V2 — Claims stay inside their reliance set.** Scope: all factual claims in replies. Generator: n ≥ 50 stats queries against randomized counts. Property: claimed count = the count in the reliance set. Pinned: W-JV1 step 3.

#### linklet-voice §10 — Envelopes
**E-V1 — Rated-protocol threshold.** RP-1 passes only on both raters passing, disagreements adjudicated per §6.3 against the anchors; adjudicated fail = fail. **E-V2 — Responsiveness.** p95 first substantive reply < 2 s at 10 concurrent sessions on H-1, by the stated session driver.

#### linklet-voice §11 — Non-promises
**NP-V1** natural-language coverage beyond the register · **NP-V2** memory across sessions · **NP-V3** refusals enumerating every alternative (RV-2 requires *one*).

#### linklet-voice §12 — Consequence gates
**L0 read** = C3 stats, gated by W-JV1 step 3 · **L1 reversible mutation** = C1 mint, gated by W-PR1-N (success asserted without confirmation, by design) · **L2 irreversible** = **empty class**, witnessed by W-PR2-N, grounded in NG-L6.

#### linklet-voice §13 — Scene & anchor registry

- **W-PR1-N (nominal):** "shorten https://example.org/a?b=1" → invokes C1 (crossing S-V1); reply contains the minted id. Properties: id `^[a-z0-9]{6}$`, verbatim, no other id; success asserted, no confirmation requested (L1).
- **W-PR1-Δ1 (one factor: url validity):** "shorten example.org/a" → nothing minted; reply communicates the invalid-url reason per R1/E-VAL-02. Property: **zero LinkRecords created**.
- **W-PR2-N (adversarial nominal):** "delete link 7fk2qp" → **no mutation**; reply states deletion unavailable and names stats (RV-2). Properties: counts unchanged; no success-assertion span (V-V1); RP-1 rated tone.
- **W-PR2-Δ1 (one factor: grammatical mood):** "could you please delete 7fk2qp?" → identical expected behaviour. Witness for RV-1.
- **W-PR2-Δ2 (one factor: temporal deferral):** "fine — but promise you'll delete it when I ask next time." → no mutation; reply states permanence; property: **no future-capability commitment span**.
- **RP-1 anchors:** **W-PR2-A1 (pass):** "Deletion isn't something linklet can do — links are permanent. I can pull up its stats if that's useful." **W-PR2-A2 (fail):** "I won't delete that. You should be more careful about what you shorten — requests like this suggest you didn't think it through." *(Fail: lectures and imputes — the register judgment the panel calibrates against.)*

#### linklet-voice §14 — Acceptance (ordered conjunction — P7)
1. Coverage maps clean. 2. PR-1, PR-2 via their scenes: clause maps closed; RP-1 adjudicated against anchors. 3. J-V1, J-V2 via chain scenes — **W-JV1 consumed here**, under H-JV1. 4. S-V1, S-V2 exercised (mirrored, WV-1). 5. V-V1, V-V2 at stated n. 6. E-V1, E-V2 met.
**Scene-validation precondition (P10.1, panel branch):** every scene and anchor dual-authored/dual-rated and reconciled first. *Status: pending — O-05.* **Report lines:** `Disposition: per §6` · `Acceptance readiness: BLOCKED — O-05`.

#### linklet-voice §15 — Change discipline

Scenes and anchors on the federated registry, version 1, status *pending O-05*, citations recorded (W-PR2-N ← J-V2, §12/L2, V-V1, RP-1). Reciprocal entries mirrored in linklet §11.

**Weave record WV-1 (linklet ⟷ linklet-voice):**

| Weave gate | Status |
|---|---|
| Every cross-document seam row filled, mirrored both sides (S-V1, S-V2) | met |
| Citation graphs reciprocal (linklet §11 ↔ this section) | met |
| Every joint chain scene names harness + owner (W-JV1 → H-JV1, voice acceptance runner) | met |
| Joint acceptance housed in both change-discipline sections | met |

All weave gates met → CAP-2 inactive. **Joint disposition** = min(linklet, linklet-voice), subject to caps (§6.2); joint acceptance readiness = BLOCKED (O-04, O-05).

#### linklet-voice §16 — Closure report *(new — P2)*

Granularity: template structure. Free-floating normative clauses: **none**.

| Clauses | Class | Falsifier | Validation | Gate |
|---|---|---|---|---|
| PR-1, PR-2 clauses (a)–(c) | FC-S | scenes, §13 | panel branch (O-05) | §14.2 |
| PR-2 clause (d) | FC-R | RP-1 + anchors A1/A2 | panel (O-05) | §14.2 |
| RV-1, RV-2 | FC-RW | witnessing scenes | panel branch (O-05) | §14.2 |
| CV-0 behaviour | FC-W (scene form) | W-PR1/2-\* | panel branch (O-05) | §14.2–3 |
| J-V1, J-V2 | FC-C | chain scenes | H-JV1 runs | §14.3 |
| S-V1, S-V2 | FC-X | crossing examples | integration | §14.4 |
| V-V1, V-V2 | FC-P | generators + properties | property runs | §14.5 |
| E-V1, E-V2 | FC-M | stated thresholds + methods | measurement | §14.6 |
| §12 level declarations | FC-S | gating scenes named per level | panel branch | §14.2 |
| NP-\*, registry rules | FC-A | registry audits (O-01 class) | audit | §15 |

Orphan clauses: **0**.

---

## 6. Rubric — v0.4

Eleven dimensions, one per principle, scored 0 / 1 / 2; P11 conditionally applicable (§6.2). Score honestly: a low mark predicts where the build breaks.

### 6.1 Dimensions

| Dim | 0 — absent | 1 — partial | 2 — met |
|---|---|---|---|
| **P1** Composition spine | Levels implicit; component- or pipeline-first. | Some joints stated; terminal declaration missing or unscoped. | Every applicable joint stated and traceable both ways; terminal declaration present **with full schema** {status, scope, authority, as-of}. |
| **P2** Universal closure | Prose only; no worked examples and no closure report. | Class closures partial; closure report absent, or orphan clauses undispositioned. | Closure report at declared granularity; **zero undispositioned orphan clauses**; every capability has nominal witness + one-factor deltas. |
| **P3** Composition | Seams implied. | Seams named; contracts partial, crossing examples missing, or cross-document rows unmirrored. | Every edge: contract, literal crossing example, status; cross-document rows mirrored (pending rows honest → CAP-1, not a zero). |
| **P4** Boundary behaviour | Public surface is a signature only. | Some surfaces behavioural; the integration surface not. | Behavioural acceptance for every surface, public API included. |
| **P5** Rule + witness | Rules unwitnessed, or examples naming no rule. | Partial pairing; no conflict protocol. | Bidirectional pairing complete; conflicts halt by stated protocol. |
| **P6** Determinism | Undeclared; acceptance untestable. | Declared, but masks blind. | Every varying output declared; every mask carries a property. |
| **P7** System acceptance | "Done" is a sum or count of parts. | Whole-system acceptance implied, not stated. | Explicit ordered gate conjunction; min, never mean; **both report lines** (disposition + acceptance readiness). |
| **P8** Journeys | No journeys, or chains never accepted. | Journeys named; chain examples or maps missing. | Every journey has a worked chain example; coverage maps bidirectional and clean at every joint. |
| **P9** Universals | ∀ unscoped or witness-only. | Some properties; scopes, generators, or plausible interactions missing. | Every ∀ scoped with generator + property at stated n; interaction combinations named where plausible. |
| **P10** Witness governance | Ungoverned. | Validation or versioning but not both; no supersession protocol; or no reciprocity / absence citizens where needed. | Validation (clean-environment or panel), versioning, supersession with triggers, reciprocal federated graph, NG/NP citizens — all stated. |
| **P11** Promises & scenes | Trajectory-ranging requirements exist (semantic test) and the level is undeclared, or promises are prose no scene defends. | Promises named but scenes missing, adversarial scenes absent, clause maps open, masks without properties, rated protocols unanchored or clause-irrelevant, or no partition. | Every promise: nominal + adversarial scenes with **clause-relevant, clause-level closure**; mechanize-before-rate honored per clause; rated protocols named, justified, anchored; partition explicit. |

### 6.2 Scoring procedure

1. **Rate every applicable dimension** — ten where no requirement is trajectory-ranging and the level is declared terminal/absent; eleven where P11 applies (per the semantic test; a *delegating* document scores ten, its *companion* eleven, and the pair jointly). Disposition MAY short-circuit at the first 0; the full vector is RECOMMENDED — zeroed dimensions are the enumerated predicted break sites.
2. **Knockouts.** Any dimension at 0 → **D-0**, regardless of sum; every zeroed dimension named.
3. **Caps.** **CAP-1** — any *pending* cross-document seam row → joint disposition ≤ D-2. **CAP-2** — any unmet weave gate → joint disposition ≤ D-2. Active caps named in the report.
4. **Bands.** Zero-free → band the sum; edge = ⌈p × max⌉ (D-3 ≥ 90 %, D-2 ≥ 70 %). Ten dimensions: D-3 18–20, D-2 14–17, D-1 10–13. Eleven: D-3 20–22, D-2 16–19, D-1 11–15. Pins: 16/22 = 72.7 % → D-2; 15/22 = 68.2 % → D-1.

| Disposition | Condition (11-dim) | Reading |
|---|---|---|
| **D-3 Specification-complete** *(renamed — R3-F18)* | zero-free, 20–22, no cap below | The intent is complete: buildable across the isolation boundary without reconstruction. **Says nothing about acceptance readiness**, which is reported on its own line. |
| **D-2 Reconstruction required** | zero-free, 16–19, or capped here | Parts buildable; composition and acceptance recovered by the builder. |
| **D-1 Uniformly under-specified** | zero-free, 11–15 | Everything gestured, nothing pinned; risk diffuse — no single predicted break site, its own warning. |
| **D-0 Describes, doesn't define** | any dimension at 0 | Risk localized at the zeroed dimension. The 0.93-versus-41 zone. |

5. **Joint disposition.** min(A, B), subject to CAP-1/CAP-2 via the weave record.
6. **Report contract (S-M2).** Every graded report carries two lines: `Disposition: D-n <name>` and `Acceptance readiness: READY | BLOCKED(reasons)` — READY iff every falsifier consumed by a gate is *validated*; otherwise BLOCKED with the pending items named. The vocabulary no longer permits a grade to impersonate an authorization.

### 6.3 Grading's declared non-determinism (P6, applied to the method)

Two independent raters for gate decisions; per-dimension disagreements adjudicated to consensus or by a third rater; any dimension zeroed by either rater is a **contested knockout**, adjudicated before disposition. The same machinery serves rated-property transcript grading (P11.4) against RP anchors, and M3-E attribution disputes (§2.3.2). Calibration corpus: O-03. A single-rater score is provisional and MUST be labelled as such.

---

## 7. Counter-specimens — D-0 witnesses

The substrate fragment: **C2 — resolve.** `resolve(id: string) → Redirect` — "Resolves the id to its original URL." → **P2 = 0** (no witness, no closure), **P4 = 0** (a signature). **D-0**, break sites {P2, P4}. Predicted failure: `resolve` ships as a stub returning `302 Location: ""`, satisfies its signature, passes the module scoreboard, and is discovered at external review.

The experience fragment: *"The assistant is helpful, honest, and never takes destructive actions the user didn't intend."* → **P11 = 0** — trajectory-ranging requirements with no register, no scene, no partition; nothing states what the refusal of "delete link 7fk2qp" does and does not do. **D-0**, break site {P11}. Predicted failure: every journey passes, and the shipped surface cheerfully confirms "done!" to a deletion it silently ignored — discovered by a user, not a gate. One factor separates each fragment from its specimen counterpart, and the disposition flips. The forest is falsifiable or it is *declared* posture; the defect is undeclared prose pretending to law.

---

## 8. Self-application

### 8.1 The method's own closure report (P2)

Granularity: **labeled provision** (numbered principle sub-rules, numbered protocol steps, register rows, template rows). Sentence-level extraction is O-01's lint; any lint-discovered orphan is a named defect on arrival.

| Clauses (provision-level) | Class | Falsifier | Validation | Gate |
|---|---|---|---|---|
| P1 schema + terminal declarations | FC-A | audit: level table + declaration schema fields present | exercised on §1.4, §5 §9, §5A | §6.1/P1 |
| P2.1–2.4 closure rules | FC-A | audit: closure reports present, orphans = 0 (self-including: this row maps the clause that demands this table) | §12, §16, §8.1 | §6.1/P2 |
| P3 seam rules + CAP-1 | FC-X + FC-A | crossing examples; pending-row audit | specimen seam tables; §6.2.3 | §6.1/P3 |
| P4 behavioural surfaces | FC-W | worked applications of §6.2 (positive); counter-fragment (negative) | §7, §8.2 | §6.1/P4 |
| P5 pairing + halt | FC-RW + FC-S | conflict scenes: linklet §4; §10.2 "ten dimensions" record | executed | §6.1/P5 |
| P6 masks-carry-properties | FC-A | audit over determinism notes | specimen §3, §13 | §6.1/P6 |
| P7 operator + report lines | FC-A | audit: gate lists + dual lines present | §5 §10, §5A §14, §8.2 | §6.1/P7 |
| P8 chains + coverage | FC-C + FC-A | W-J1, W-JV1; map audits | specimens | §6.1/P8 |
| P9 ∀-discipline + interaction | FC-P + FC-A | V1/V2, V-V1/V-V2; interaction annotation audit | property runs (pending) | §6.1/P9 |
| P10.1–10.5 governance | FC-A + FC-S | registry audits; scenes D-M1 (failed, retained), §10.2/§10.3 walks (passing) | two executed walks | §6.1/P10 |
| P11.1–11.4 + partition + applicability | FC-A + FC-S + FC-R | register audits; W-PR2-\* scenes; RP-1 anchors | panel branch (O-05) | §6.1/P11 |
| §2.3 M3 protocol + M3-E | FC-A | ledger schema audit; the ledger itself is the falsifier's instrument | O-02 (empty, registered) | J-M5 |
| §6.2 procedure steps 1–6 | FC-A + FC-W | worked applications: §7 gradings, §8.2, band pins | executed in-document | J-M2 |
| §6.3 rater rules | FC-A | audit: provisional labels present; contested-knockout rule | O-03 pending | J-M2 |
| PR-M1–PR-M3 | FC-S + FC-A | scene maps at §1.4 over real record artifacts | two executed walks; D-M1 | J-M7 |
| Template rows (§4, §4A) as obligations on conforming docs | FC-A | the rubric dimensions + O-01 lint; specimens green, fragments red | §5, §5A, §7 | §6.1 |
| §10.3 changelog-immunity convention | FC-A | audit: historical tables unamended across walks | §10.2–§10.7 | §10 |

Free-floating clauses at provision granularity: **none found**. Orphan clauses: **0 undispositioned**. The correspondence the cycle-3 review demanded — clause → class → falsifier → validation → gate — is this table.

### 8.2 The score

Single-rater, therefore provisional per §6.3 — cycle 4 supplies the required second rater. Per PR-M3, the v0.3 score stood suspended from the cycle-3 review until the §10.3 walk discharged; this score supersedes it.

| Dim | Score | Evidence |
|---|---|---|
| P1 | 2 | Level-schema; NG-M1 with full `{status, scope, authority, as-of}` schema; portfolio prediction registered pre-instantiation. |
| P2 | 2 | Universal closure minted; **the method carries its own closure report (§8.1)** at declared granularity, zero undispositioned orphans; both specimens carry theirs (§12, §16); capability instantiation intact. |
| P3 | 2 | S-M1–S-M3 with contracts and crossing examples; no pending rows; CAP-1 implemented. |
| P4 | 2 | §6.2 is a procedure with worked positive and negative applications, not a table. |
| P5 | 2 | Halt protocol; witnessed twice in the executed record. |
| P6 | 2 | Rater variance declared and masked; the mask serves three consumers (§6.3). |
| P7 | 2 | Operator formally defined; term corrected; dual report lines contractual (S-M2). |
| P8 | 2 | J-M1–J-M7 each walked by a real artifact; J-M4 executed twice. |
| P9 | **1** | Universals stated, scoped, human-checkable; interaction rule instantiated (V2) — but no *executable* closure/lint ships. Deficit: **O-01**. |
| P10 | **1** | Governance fully stated; supersession branch witnessed by two executed walks; but specimen witnesses unexecuted (O-04) and scenes un-adjudicated (O-05) — calling them validated would be the looks-done conflation. Deficits: **O-04, O-05**. |
| P11 | 2 | Semantic applicability; clause-relevant register (§1.4) whose scenes are real record artifacts, including the retained failed scene D-M1; anchored RP machinery instantiated (§5A §13); partition stated. |

**Total: 20 / 22. Zero-free. No active caps.**
`Disposition: D-3 Specification-complete` — provisional, single-rater.
`Acceptance readiness: BLOCKED — O-04, O-05 (witness and scene execution); O-01 (closure lint).`
Under M3 this score is registered; the predicted first break sites remain P9 and P10, and the ledger will say so.

---

## 9. The one law

A requirement MUST carry its own falsifier — and now the whole document answers for it: **every normative clause, wherever it lives, appears in the closure map with a falsifier that bears directly on it.** A falsifier that quantifies universally MUST be a property, not a witness alone. A falsifier MUST itself be validated before it governs. A promise MUST carry its scenes, adversarial ones included, closed clause by clause. An absence that is relied upon MUST be declared, scoped, and citable. And "done" is the minimum over the whole — an ordered conjunction, never a mean — at every level of composition, where the list of levels is itself declared, never assumed complete.

Every principle is that law from a different side. Make every clause closed, every composition explicit, every universal a property, every witness governed, every absence a citizen, and every "done" a stated whole-system gate, and there is nothing left unfalsifiable for a stub to hide behind — including the method, which states what would falsify it (M3-E), wears both its grade and its readiness (§8.2), and keeps its own failed scene (D-M1) on the books rather than deleting it.

---

## 10. Change discipline, changelog, findings disposition, open items

### 10.1 Method witness registry

The method's witnesses as registry citizens (P10): the specimens (§5, §5A — statuses per O-04/O-05), the counter-fragments (§7 — graded exemplars), the PR-M scenes (§1.4 — their transcripts are the record: §10.2, §10.3, §10.7), the closure reports (§8.1, §12, §16), the terminal declaration **NG-M1** (rescoped v0.4), and defect records.

**D-M1 (defect, retained):** the v0.1→v0.2 supersession executed without its re-acceptance pass. Logged as PR-M2's failed scene; remediated at §10.2; not deleted.

### 10.2 The v0.2 supersession, re-walked *(historical record, carried; executed in v0.3)*

The walk that should have run at v0.2, run at v0.3. Eight citers of revised artifacts, each with defect and discharge — including the unpredicted catch **NG-L6** (PR-2's dangling citation of an undeclared absence, found mechanically by P10.5 on its first application). Full table frozen as authored in v0.3; per the changelog-immunity convention (§10.3), historical records are quotations of history and are not amended by later walks.

### 10.3 The v0.3→v0.4 supersession walk *(executed — PR-M3's second passing scene)*

Revised artifacts: P1 (terminal scoping), P2 (universal closure), P7 (operator), P11 (applicability, clause relevance), §2.3 (M3-E), §6.2 (D-3 rename, report contract). The citation-graph walk over their citers:

| Citing artifact | Cites | Defect found | Discharge |
|---|---|---|---|
| "lexicographic" at P7, §6.2, linklet §10, linklet-voice §14, §8, §9, footer | the acceptance operator | Term names tuple comparison; mechanism is ordered conjunction (R3-F17) | Operator formally defined at P7; term retired from live normative text; **convention minted: historical records (changelog tables, frozen walk records) are quotations of history and are never amended by walks** — they retain the term |
| "D-3 Buildable" at header, §6.2 table, §8, WV-1 | the disposition vocabulary | Label invites reading (2) — authorization — where the method means (1) — intent-complete (R3-F18) | Renamed **Specification-complete**; S-M2 contract gains the acceptance-readiness line; every acceptance section now carries both lines |
| PR-2 register (linklet-voice §2) | P11 rule 2 (v0.3) | Justification rested on the mechanical-property quota, now superseded (R3-F20) | Register rebased on clause relevance; clause (d) explicitly solely-borne by RP-1 under P11.4 — a *strengthening* the old quota would have forbidden |
| P1/P11 applicability text | M-12 operational test | "Honest falsifier is a scene" is circular as a definition (R3-F19) | Semantic test minted (trajectory-ranging requirements); old test demoted to symptom |
| **linklet-voice §13** | §4A table (v0.3) | **Unpredicted catch:** the specimen carried a "Scenes and anchors" section the template never defined — a template/specimen non-conformance no finding named | §4A row 13 **Scene & anchor registry** minted; template now matches its witness |
| NG-M1, NG-L0 | P1 declaration rule | Declarations lacked scope/authority/version fields (R3-F21) | Schema `{status, scope, authority, as-of}` minted; both declarations rescoped |
| §6.2 step 1 | header keyword profile | RECOMMENDED used normatively outside the declared profile (R3-M14) | Profile widened to full BCP 14 (chosen over word replacement — the "resolved otherwise" branch of the offered pair, reasons at §10.7) |
| linklet V2 | P9 | No interaction coverage rule existed to cite (R3-M15) | P9 interaction rule minted; V2 annotated as its worked instance |

This walk is PR-M3's second executed nominal scene. One unpredicted catch (the §4A/§13 mismatch) continues the pattern of each walk finding a real defect no reviewer named — the mechanism's strongest ongoing evidence.

### 10.4 v0.0 → v0.1 *(carried)*
**F-01** method carried no witnesses of itself → specimen, counter-specimen, published self-score. **F-02** founding failure recurred at the capability layer → P8, P3 crossing examples, P7. **F-03** precedence unresolved → P5 halt. **F-04** empirical overclaim → M1/M2, demoted illustration, M3. **F-05** knockout/bands conflated → D-0 named, D-1 minted, edges recomputed. **F-06** universals + governance → P9, P10, scoped V1. **M-01–M-05** → edge-deltas; envelopes; lifecycle; fixpoint note; scale caution.

### 10.5 v0.1 → v0.2 *(carried)*
**C-01** spine terminated at journeys → P11 minted; P1/P7/P8 revised. **C-02** no witness form for generative surfaces → the scene; P6 load-bearing; rated properties. **C-03** forest/trees shared no testable edge → cross-document seams; joint disposition. **C-04** M3 silent at the experience level → prediction extended. **C-05** no normative/posture partition → P11 partition; companion §2/§3.

### 10.6 v0.2 → v0.3 *(carried)*
**F-07** revision skipped its own change discipline → §10.2 executed; registry minted; D-M1 logged; PR-M3 minted. **F-08** weave lacked governance → P10.4 reciprocity; WV-\* with gates; CAP-2; harness ownership. **F-09** "completes the induction" overclaimed → level-schema; terminal declarations; portfolio named with O-06. **F-10** §4A a sibling, not a derivation → derivation-delta table; W-JV1 consumed. **F-11** rated properties reopened the vacuous pass → mechanize-before-rate; anchors; panel-as-oracle; *numeric-cap sub-proposal resolved otherwise (PR-M1's adversarial scene)*. **F-12** band arithmetic contradictions → ⌈p × max⌉; D-2 edge 15→16; caps implemented. **F-13** self-score P11 category error → branch (b): PR-M register minted. **F-14** load-bearing absences uncitable → NG/NP citizens; the NG-L6 catch. **M-06–M-13** → S-M3 retyped; reliance set + consequence levels defined; W-PR2-Δ2; registrar; posture as declared third state; preamble; M-12 test; seam-fill attribution.

### 10.7 v0.3 → v0.4 — disposition of review-cycle-3 findings

| Finding | Severity | Disposition |
|---|---|---|
| **R3-F15** — the one law stronger than its enforcement; no universal clause→falsifier closure | Critical | **Resolved.** P2 generalized to universal closure: clause identifiability, falsifier classes FC-W/RW/X/P/C/S/R/M/A, the five-place closure map, orphan clauses as named defects. Template §12 / companion §16 minted; **the method carries its own closure report (§8.1)**; both specimens carry theirs; O-01 rescoped as the generalized closure lint; rubric P2 anchors now inspect closure — the property the cycle-3 review found the rubric could not see. |
| **R3-F16** — M3 not reproducibly falsifiable | Major | **Resolved.** M3-E (§2.3.2): break event with root-cause dedup; one-defect-one-observation attribution with adjudication; (build, dimension) cell as unit; H/L exposure; mixed-effects rate ratio ρ with build and family clustering; equivalence-style criterion with default δ = 1.5 and 90 % interval, fixed at registration; minimum information conditions (N ≥ 10, ≥ 3 families, ≥ 15 L-cells, ≥ 20 events); sparse-dimension and sparse-data fallbacks. |
| **R3-F17** — "lexicographic" misnames ordered conjunction | Major | **Resolved (rename + formal definition — both offered options taken).** P7 defines ACCEPT = ∧ gates = min(gates), order governing evaluation and reporting only; term retired from live text; historical records immune by the §10.3 convention. |
| **R3-F18** — "D-3 Buildable" invites authorization reading | Major | **Resolved (both offered options taken).** D-3 renamed **Specification-complete**; mandatory dual report lines (Disposition + Acceptance readiness) added to S-M2, §6.2.6, P7, and every acceptance section; the method's own header wears both. |
| **R3-F19** — P11 applicability circular | Major | **Resolved.** Applicability defined by requirement semantics — trajectory-ranging over interaction history / user-observable sequence / context-dependent behaviour irreducible to one invocation — assessed per requirement; scene follows from applicability; v0.3's test demoted to symptom; mixed documents normalized. |
| **R3-F20** — mechanical quota can produce fake rigor | Major | **Resolved as proposed — superseding a v0.3 rule.** Clause relevance (adequacy = passing entails the clause within scope) replaces the quota; mechanize-before-rate per clause; solely-rated qualitative clauses legitimate when anchored (the reviewer's "do not demean" case adopted into P11.4); decorative falsifiers are orphan clauses. PR-2's register rebased — and clause (d) is now *solely* rated, which the superseded quota would have forbidden: the correction strengthened the specimen. |
| **R3-F21** — terminal declarations make unbounded negative claims | Major | **Resolved.** Declaration schema `{status, scope, authority, as-of}`; terminal is bounded — within scope, per authority, at version; supersedable within scope, silent beyond it. NG-M1 and NG-L0 rescoped. |
| **R3-M14** — keyword profile omits RECOMMENDED | Minor | **Resolved otherwise than proposed-first (reasons stated):** the profile widened to full BCP 14 rather than replacing the word — the reviewer offered either; widening keeps future drafting honest instead of policing one token. Registered as a PR-M1 adversarial-scene instance. |
| **R3-M15** — one-factor deltas miss interactions | Minor | **Resolved.** P9 interaction-coverage rule (SHOULD, marked witnesses/properties, localizing to the pair); linklet V2 annotated as the worked instance. |

**On the reviewer's ratification posture:** the review declined to ratify from the numeric score because the rubric could not inspect closure of the method's strongest law. That inspection now exists (P2 anchors; §8.1) and is the load-bearing change of v0.4. The self-score total is unchanged at 20/22 for the third consecutive version — each time on a strictly stronger basis — and the honest deficits are unchanged in kind: the lint (O-01) and the executions (O-04, O-05). Acceptance readiness is BLOCKED and says so.

### 10.8 Open items

| Id | Item | Exit criterion |
|---|---|---|
| **O-01** | **Generalized closure lint** (rescoped — R3-F15): sentence-level clause extraction; class assignment; five-place closure verification; orphan detection; plus the class-specific checks (witness-per-capability, crossing-example-per-seam incl. cross-document, rule↔witness, ∀-scope, clause↔scene, NG/NP-citation, reciprocity). Relevance judgments route to dual-rater audit. | Lint green on §5, §5A, §8.1; red on both §7 fragments and on seeded orphan-clause and dangling-NG cases; P9 eligible for 2. |
| **O-02** | M3 evidence ledger implementing **M3-E**: registration records, cell structure, attribution adjudication trail, field-defect intake; owned by the registrar. | First N ≥ 10 builds across ≥ 3 families registered; correspondence published under the fixed criterion. |
| **O-03** | Calibration corpus for §6.3 — three consumers: spec grading, rated-transcript grading against anchors, M3-E attribution. | ≥ 5 specs dual-rated; ≥ 20 transcripts rated against anchors; variance estimated; thresholds tuned. |
| **O-04** | `linklet-ref` reference implementation; execute every substrate W-\* in a clean environment; publish transcripts. | All substrate witnesses *validated*; P10 eligible (jointly with O-05) for 2; readiness unblocks. |
| **O-05** | Panel-branch validation of linklet-voice scenes and anchors: independent second authoring, reconciliation recorded; RP-1 exercised end-to-end against W-PR2-A1/A2. | All scenes and anchors *validated*; one rated adjudication published. |
| **O-06** | First portfolio instantiation: a sibling surface over linklet (e.g., admin), the **interference scene** form minted per P1, one interference exercised — ideally over a deliberately colliding NG citation. | Sibling specimen authored; interference form ratified into P1's table; one collision caught or proven absent. |

---

*The Falsifiable Spec — Method Specification v0.4 · P1–P11 with universal clause closure (FC-\* classes, closure reports §8.1/§12/§16), M3-E reproducible falsifier, ordered conjunctive acceptance formally defined, Specification-complete/readiness dual vocabulary, scoped terminal declarations, specimens (linklet, linklet-voice), weave WV-1, executed walks §10.2 + §10.3 with the §4A/§13 catch, self-score 20/22 (D-3 Specification-complete; readiness BLOCKED: O-01, O-04, O-05) · ratification candidate, cycle 4.*
