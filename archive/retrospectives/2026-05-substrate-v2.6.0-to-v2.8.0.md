# FNSR Substrate Retrospective: v2.6.0 → v2.8.0

**Audience:** FNSR-internal. Not public; not marketing.
**Scope:** What three substrate moves demonstrated, the architecture pattern that crystallized, the coordination pattern that produced it, and the FNSR-relevance of each.
**Date:** 2026-05-18

---

## 1. What shipped, in three substrate moves

The substrate moved three times across the v2.6.0 → v2.8.0 arc. Each move was a qualitative change in what the substrate could do, not just an increment in feature count.

### v2.6.0 — Verbal discipline → audit events

Before v2.6.0, the substrate was a thin coordinator: a deterministic Python orchestrator dispatching Claude Code subagents, with state in `state.jsonld` and a chained-hash audit trail per task. Bankings (operator observations about the protocol) existed only as verbal practice. Forward-tracks (commitments to future deliberation) lived only in markdown.

v2.6.0 made these first-class:

- **ADR-citation CPS check** — vetoed canonical-doc proposals citing ADR-NNN values not registered in `project/DECISIONS.md`. Configurable canonical-doc list via env var; scoped to authored protocol content only.
- **`awaiting_operator_decision` status** — the daemon's first explicit handoff back to the operator. Agents emitting `{status, options[], recommendation}` were committed in this state; operators resolved via `state_admin resolve <task-id> <option-index>`.
- **`forward_track` audit event** (later renamed to `banking` in v2.7.0 per Spec 05/07 separation) — operator observations recorded against an anchor task, chain-hashed into the audit trail.
- **`state_admin resolve` + `bank` subcommands** — the operator CLI gained first-class commands for the handoff and the banking surface.

**What this demonstrated:** Tacit operator discipline can be encoded as substrate primitives without losing the operator-in-the-loop pattern. The substrate didn't replace operator judgment; it made operator judgment auditable in the same chain as agent dispatches.

**Test count delta:** 119 → 151 (+32). One v2.6.1 patch added 5 more tests (the ADR-012 ghost fixture from FNSR Spec 06).

### v2.7.0 — Pass 2a discipline chain

The v1.1 FNSR Protocol Specifications bundle arrived after v2.6.0 with eight artifacts: meta-principle (Spec 01), verification ritual (Spec 02), Pass 2a/2b sequencing (Spec 03), cycle counter (Spec 04), banking lifecycle (Spec 05), ADR-012 ghost fixture (Spec 06), and Forward-Track Surface (Spec 07).

v2.7.0 implemented the discipline-chain pieces:

- **`reconnaissance` worker agent** — the first instance of the **read-only-by-contract agent pattern**. Tools: Read/Grep/Glob only; no Edit/Write/Bash. Outputs `findings`, `summary`, `evidence_paths`. Refuses scope-violation requests via structured error. The contract is defined by what the agent CANNOT do, not just what it does.
- **`architect` extended to two modes** — `review` (existing v2.5.0 contract) and `ratification` (new Pass 2a per Spec 03). Six-field ruling payload: `ruling`, `editorial_verdict`, `editorial_verdict_reason`, `rationale`, `referenced_evidence`, `bankings`. Refusal contract: substantive changes without UPSTREAM reconnaissance produce `ruling: denied, rationale: reconnaissance_required`. The `editorial_verdict_reason` field was a Gap 3 refinement — surfaces the LLM's classification rationale separately from the overall ruling, making misclassifications auditable.
- **Multi-mode `required_outputs` parsing** — daemon-side substrate extension supporting both flat-list and per-mode dict frontmatter. Critical for the architect's two modes and seeded the pattern that v2.8.0's verification-ritual-llm and adversarial-critic later reused.
- **Banking lifecycle (Spec 05)** — three-state lifecycle (verbal-pending → partially-committed → formalized) with substrate-neutral implicit-vs-explicit operation. `state_admin bank --category --state`; `state_admin transition-banking <id> --to-state`. Logic Team's actual practice (implicit reconciliation at phase-exit doc-pass) and explicit-mode (per-transition audit events) are both first-class.
- **Forward-Track Surface (Spec 07)** — structurally distinct from bankings per Logic Team's v1.1 review pushback (which Aaron folded in BEFORE v2.7.0 implementation began). Forward-tracks record commitments to FUTURE deliberation; bankings record observations ABOUT the protocol. Different lifecycle (candidate → deliberated → resolved), different audience structure (consumer-closure-path vs internal-methodology-refinement), different audit-trail unity. `state_admin forward-track create / inherit`.
- **`state_admin phase-boundary <from> <to>`** — operator-emitted phase-boundary audit events. Substrate is phase-schema-neutral; the operator declares.

**What this demonstrated:** The Pass 2a discipline (substantive changes require evidence-gated reconnaissance; ratification rulings are auditable with separable reasoning fields) is implementable mechanically. The substrate enforces the contract; the LLM judgment lives at the boundary the contract delegates to.

**Test count delta:** 156 → 190 (+34 in v2.7.0 itself; plus 5 from v2.6.1 ghost fixture).

### v2.8.0 — Verification-as-substrate

The biggest single-version delta in the substrate's history. v2.8.0 implemented FNSR Spec 02 (verification ritual) in four checkpoints (alpha.1 through final), closing the Pass 2a/Pass 2b chain per Spec 03.

#### CP1: Foundation
- `surfaces/` directory layout — first explicit use of Spec 01's surface-registry primitive
- `surfaces/verification/categories/cat-NN-*.md` — per-category spec files; the substrate primitive
- Cat 1–7 deterministic predicates (structural lookups against frozen contracts)
- `verification-ritual` system agent (orchestrator)
- Category-spec loader + predicate resolver

#### CP2: Hybrid + hook framework
- Cat 8 hybrid two-cadence (pre-routing structural + activation-time strict-equality + `semantic_equivalence_acceptable: {reason, scope}` deferral)
- Cat 10 candidacy with subject-project hook framework (sibling .py file pattern; per-surface sandbox namespace `subject.<surface>.<module>`)
- `PredicateMetadata` dataclass — typed substrate-supplied context (`self_path`, `task_id`, `cycle_id`, `phase_context`, `cadence`) threaded to predicates
- Three-class miss taxonomy (`malformed_spec`, `unresolved_predicate`, `categorical_coverage_miss`)

#### CP3: LLM side
- Cat 9 LLM candidacy (cited-content consistency) — category-agnostic prompt with ADR-012 ghost AND Q-4-Step5-A spec §3.4.1 case as parallel examples
- `verification-ritual-llm` worker agent — second instance of the read-only-by-contract pattern; two modes (`cat-9-judge`, `cat-8-semantic-equivalence`)
- `adversarial-critic` cat-9-second-pass mode — third instance of read-only-by-contract; fires on Cat 9 vetoes only (verdicts that change downstream state); `default_mode: review-second-pass` for back-compat
- Fourth miss class split: `missing_canonical_source` (Gap I)
- `default_mode` frontmatter mechanism — single→multi-mode agent migrations preserve back-compat

#### CP4: Operating surface + chain closure
- `state_admin forward-track transition / list / aging` — full Spec 07 operating surface
- Forward-track aging warnings as audit events (`forward_track_aging_warning`), not just CLI output
- `commit-finalize` task type documented as canonical Pass 2b consumer
- Read-compat with v2.7.0 operator-applier chains preserved (append-only invariant)

**What this demonstrated:** Protocol depth survives substrate translation across a meaningful capability surface (ten categories, LLM judgment with adversarial mitigation, full Pass 2a/2b chain). The substrate operates evidence-gated discipline at machine speed without losing audit-trail honesty.

**Test count delta across v2.8.0:** 190 → 294 (+104 across four checkpoints).

---

## 2. The architecture pattern that crystallized

Across v2.8.0's four checkpoints, the substrate's operating architecture settled into a four-property pattern:

1. **Deterministic where possible.** Cat 1–7 + Cat 10 are structural lookups against frozen contracts. The predicate is a Python function; the verdict is verifiable by the operator reading code. No LLM in the loop.
2. **LLM where necessary.** Cat 9 (cited-content consistency) is semantic comparison between citing framing and canonical content. No deterministic predicate suffices; the LLM judgment is irreducible. Cat 8's activation-time semantic-equivalence is the same.
3. **Adversarial-critic where verdict changes state.** Cat 9 vetoes block downstream routing (they change state). The `adversarial-critic` cat-9-second-pass mode runs only on vetoes — passes don't need second opinion because they don't uniquely change state. The second-pass produces an independent verdict (confirm / dispute / extend); paired-verdict audit history records both verdicts in the chain.
4. **Audit-chain for all of it.** Every verdict (Cat 1–10), every LLM judgment, every adversarial-critic stance, every Cat 9 disputed-veto outcome lives in the chain-hashed audit history. The chain is append-only; the audit trail is the canonical record.

### Why the third property is the substrate-vs-procedure distinguisher

A procedure can produce verdicts and even produce challenges. What a procedure cannot do is record verdicts AND their challenges in a way that survives the verdict being later questioned. The audit chain is what makes that recording trustworthy. When Cat 9 vetoes a routing change, the chain contains: the LLM's veto verdict + rationale; the adversarial-critic's stance (confirm or dispute) + independent rationale; the operator's final decision (honor or override) if dispute surfaces.

A future operator reading this chain six months later doesn't have to trust that Cat 9 was right. They have evidence — the paired verdicts and the operator's resolution — to re-derive whether the routing decision was sound. That's the property the substrate provides. Procedures can produce decisions; substrates produce decisions that are auditable against themselves.

### How the architecture survives translation

The pattern is substrate-neutral. The verification surface is one instance of Spec 01's surface-registry primitive; future surfaces (cycle, commit, bankings, forward-track, and surfaces not yet emerged) follow the same `surfaces/<surface>/<bucket-or-category>/` layout. Adding a new category is a file-drop, not a substrate release. Adding a new LLM-judged predicate that changes state automatically inherits the adversarial-critic mitigation pattern.

This is why v2.8.0 is the change rather than just an incremental release. The substrate is no longer adding features under a single fixed architecture; the substrate is providing primitives a future operator can use to add features under the same architecture. The capability set is extensible without changing the substrate.

---

## 3. The cross-team coordination pattern

v2.8.0 didn't ship from a single team's work. The pattern that produced it had four moving parts:

### Parallel teams with orchestrator brokerage

The **Logic Team** developed protocol depth in their subject project, surfacing patterns (the eight ritual categories; two-cadence operation; banking lifecycle; forward-track surface; cited-content consistency as a Cat 9 candidacy). The **Daemon Team** built substrate. Aaron, as orchestrator, sat between — translating Logic Team observations into substrate specifications, routing instance-layer review back to Logic Team before implementation began, then dispatching adjudicated specifications to Daemon Team.

This is not a team-of-teams pattern where outputs flow downstream. It's a **brokerage pattern**: the orchestrator negotiates contracts between teams that don't share a working surface, with both teams operating on their own cadence and the orchestrator absorbing translation cost.

The cost is real. The orchestrator does the work that makes parallel teams coherent. From the outside, the release looks like "Daemon Team shipped v2.8.0"; from the inside, every checkpoint involved orchestrator-mediated triage between specification questions (Logic Team's domain) and implementation questions (Daemon Team's domain).

### Two-layer specifications

The v1.1 bundle's eight artifacts each contained two layers: a **generalized layer** (substrate-neutral; Daemon-Team-implementable) and an **instance layer** (Logic Team's specific protocol as a worked example). This shape was load-bearing.

The generalized layer is what the substrate implements; the instance layer is what evidence-grounds the generalization. Implementation without the generalized layer would have over-fit to Logic Team's specifics. Specification without the instance layer would have been unfalsifiable — no production cases to cite.

The shape also made instance-layer review feasible. Logic Team reviewed each spec for whether the instance layer accurately reflected their protocol (this surfaced the v1 → v1.1 correction: forward-tracks promoted from sub-surfaces of bankings to their own surface). The generalized layer was then anchored on a reviewed instance layer.

### Instance-layer review folded in BEFORE implementation

The v1 → v1.1 correction happened pre-Daemon-Team. If the v1 bundle had shipped to implementation, the bankings-lifecycle model would have collided with itself at every cross-phase forward-track inheritance event. Logic Team's review caught it; the corrected bundle was what Daemon Team received.

This is the right ordering. Substrate releases are expensive to undo (append-only audit chain); specification errors caught at instance-layer review cost hours, the same errors caught after substrate implementation cost a substrate release. The pattern: review at the layer where the cost is lowest, before propagating to the layer where the cost is highest.

### On-demand transition after stable substrate emerged

Logic Team's engagement transitioned to on-demand once the bundle was delivered. They did not need to be continuously available; the bundle's "open questions / extension points" sections at the bottom of each spec named what was known-incomplete. Daemon Team operated against the bundle plus orchestrator brokerage; Logic Team responded to specific questions when implementation surfaced ambiguities the bundle didn't resolve.

This is sustainable. Continuous-engagement coordination patterns burn out the participants who must remain available; on-demand coordination preserves their attention for the cases that genuinely require it.

### Why this matters for FNSR

The synthetic moral person project requires substrate work spanning years rather than weeks. No single team can sustain continuous-engagement coordination at that scale. The brokerage pattern + two-layer specifications + instance-layer-review-before-implementation + on-demand-transition is the coordination architecture FNSR needs.

v2.6.0 → v2.8.0 demonstrated it works at a small scale (one orchestrator + two teams + ~3 weeks of intensive substrate development). The pattern's scalability to FNSR's longer time horizons is an open question but the architecture is right.

---

## 4. The gap-surfacing cadence as stable substrate process

Each of v2.8.0's four checkpoints surfaced gaps that the next checkpoint folded in. The cadence:

- **CP1 → Gaps F, G, H** (per-category .py hook loader; three-class miss taxonomy; PredicateMetadata)
- **CP2 → Gap I** (4th miss class: `missing_canonical_source`)
- **CP3 → orchestrator-ordering catch** (LLM categories shouldn't defer when their inputs are absent)
- **CP4 → ready to ship**

What stabilized was not the gaps themselves (those are release-specific) but the **process**:

- Implementation surfaces an under-specification
- The team triages: blocking-vs-clarifying-vs-mechanical
- The orchestrator adjudicates with default-proposed-and-reasoned
- The refinement folds into the next checkpoint additively (no substrate release for the refinement itself; the next checkpoint absorbs it)

This is the operating mode that replaces "ship complete release, discover gap, ship patch." Patches are reactive; the gap-surfacing cadence is proactive. Each checkpoint is a deliberate inspection point built into the release shape.

### Why this is substrate, not procedure

A procedure that surfaces gaps at checkpoint cadence is just a process. What makes the cadence substrate is that **the gap-surfacing itself accumulates in the audit chain**. Every CP carried `forward_track` events documenting observations during implementation; every CHANGELOG carried "open observation surfacing for next CP adjudication" sections; every refinement was a citable historical decision.

A future team picking up the substrate doesn't have to re-derive why `MISS_MISSING_CANONICAL_SOURCE` is its own class rather than collapsed under `MISS_UNRESOLVED_PREDICATE`. The history is in the audit chain: Gap I surfaced post-CP2; Aaron's CP3 adjudication confirmed the split; the four-class taxonomy locked in CP3. The decision-history is substrate, not folklore.

### Why this matters for FNSR

The synthetic moral person project will accumulate decision-history across years. Decisions made early will be reviewed and possibly revised years later by people who weren't present at the original adjudication. The audit-trail-honesty property is what lets that future review happen rigorously rather than reconstructively.

The gap-surfacing cadence demonstrates the property scales — every CP's open observations are now permanent record. The pattern was stable across four CPs; nothing prevents it from being stable across forty CPs spanning multiple FNSR substrate releases.

---

## 5. FNSR-relevance of each move

### Substrate-discipline encoding portable across subject projects

The substrate ships at `Skreen5hot/AgenticDev` as a template. GraphWrite is one subject project; barcode-template is the bare scaffold. Both consume the same substrate via three-way sync.

What survives the sync is the substrate's contract — agent frontmatter format, multi-mode `required_outputs`, category spec layout, `PredicateMetadata` dataclass, miss-class taxonomy, audit event structure. What differs is the subject content (`project/SPEC.md`, `project/ROADMAP.md`, etc.) and subject-project hooks (`cat-10-type-field-structure.py` stub vs real implementation).

This is the FNSR-relevant portability claim: substrate-discipline encoding survives substrate translation across subject projects. The synthetic moral person project will need this property at every level — normative apparatus authored once, applicable across multiple substrate-translation domains.

The proof in v2.6.0 → v2.8.0: three-way diff identical across GraphWrite / AgenticDev / barcode-template on every shared file at every release. 294/294 tests green in all three repos. The substrate didn't fork; the substrate replicated.

### Non-deterministic-but-auditable normative judgment pattern

Cat 9 + adversarial-critic cat-9-second-pass is the first concrete implementation. The pattern's three properties (verdict produced; verdict challengeable; verdict recorded with its challenge) generalize to any normative surface where deterministic rule-checking is insufficient.

The synthetic moral person project's reasoning apparatus will face this boundary repeatedly:
- Equity assessments between competing reasonable positions
- Novel-case interpretations where the rule predates the case
- Normative judgments under genuine uncertainty
- Moral judgments where rule-application yields contradictory verdicts

In each, deterministic predicates can rule out some answers but cannot select among the remaining ones. An LLM verdict is the mechanism by which selection happens; the verdict is challengeable; the challenge becomes part of the audit chain.

The architecture pattern v2.8.0 ships is exactly the shape this needs. Future FNSR work doesn't have to re-invent the pattern; it draws on the precedent.

### Tacit-knowledge → documented-specification as formalization work

The v1.1 bundle is the formalization artifact for Logic Team's tacit operating discipline. Before the bundle, the discipline existed as practice — Logic Team operated the eight categories without ever having declared them as a category set; operated the banking lifecycle implicitly without ever having transitioned a banking explicitly; surfaced Cat 9 and Cat 10 candidacies as production misses that nobody had named.

The bundle named them. Once named, they were implementable. Once implementable, the substrate could carry them.

This formalization is FNSR-load-bearing in a way that's worth being explicit about: **the synthetic moral person project requires moving normative apparatus from tacit practice to documented specification to substrate-implementation**. Each move loses something (specificity, contextual judgment) and gains something (portability, scalability, audit-trail honesty). The gains have to outweigh the losses, and the formalization work has to be done by people who can recognize when over-formalization is happening.

v2.6.0 → v2.8.0 demonstrates the gains can outweigh the losses for the verification-ritual surface. That's evidence for the broader claim; not proof for normative apparatus in general, but evidence the methodology can produce sound formalization in at least one case.

### Pattern survives sustained development without losing audit-trail honesty

Five releases in three weeks (v2.6.0, v2.6.1, v2.7.0, v2.8.0-alpha.1/2/3, v2.8.0). 138 new tests. Every release green at the suite level. Every release surfacing gaps the next folded in. Backward compatibility preserved across every shape change.

This is the development-velocity claim: the substrate can grow at intensive pace without the audit-trail honesty degrading. The append-only invariant held across every release; chain integrity verified at every checkpoint; v2.6.0 audit chains remain valid in v2.8.0 state files.

The synthetic moral person project will involve sustained development at scales that make three weeks look brief. The fact that the gap-surfacing cadence + audit-trail honesty hold at three-week pace is evidence they hold at three-year pace — not proof, but evidence the architecture's intrinsic constraints (append-only audit chain; explicit operator-fix paths per miss class; four-property verdict architecture) keep the substrate sound under development pressure rather than under development pressure causing the substrate to compromise.

---

## 6. What this is evidence for

The synthetic moral person project requires substrates that:

1. **Encode normative discipline portably** — apparatus authored once, applicable across substrate-translation domains. v2.6.0 → v2.8.0 demonstrates the encoding survives 3-way sync (GraphWrite + AgenticDev + barcode-template).
2. **Support non-deterministic-but-auditable judgment** — LLM verdicts that an operator can disagree with but cannot re-derive deterministically, made trustworthy by paired-verdict machinery. The Cat 9 + adversarial-critic pattern is the precedent.
3. **Accumulate decision-history across years** — every refinement, gap-surfacing, adjudication preserved in audit chain. The gap-surfacing cadence stability across four CPs is the precedent.
4. **Grow under development pressure without losing audit-trail honesty** — append-only invariant + backward compatibility + chain integrity hold across intensive development. Five releases in three weeks demonstrates the property.

v2.6.0 → v2.8.0 is the first capability-surface evidence the methodology can produce a substrate with these properties. It's not proof for the synthetic moral person project's needs — that requires demonstration at much larger scope. But it's evidence the foundational architecture is right.

The build-order from v2.9.0+ (test-runner + git-committer + template-sync; generalized synthesist + phase-exit-retro + phase-complete-declaration; surface_audience) extends the substrate but doesn't change its fundamental nature. The fundamentals were set across v2.6.0 → v2.8.0. Future releases inherit them.

---

## 7. What's worth noting that isn't in the changelogs

Three things this retrospective records that won't make it into release notes:

### The coordination cost the orchestrator absorbed

The Daemon Team's CHANGELOGs document what shipped. They don't document the labor of routing instance-layer reviews back to Logic Team, adjudicating gaps with default-proposed-and-reasoned defaults, holding parallel teams aligned without continuous-engagement burnout. That labor is the load-bearing coordination work; it's invisible from outside the conversation; it's worth being named.

### The pattern Aaron ratified across CP adjudications

Every CP closed with Aaron adjudicating gaps before the next CP began. The pattern: blocking-vs-clarifying-vs-mechanical triage; defaults proposed with reasoning; refinements folded additively; meta-observations on FNSR-relevance integrated alongside substrate decisions. The pattern's consistency is what made the gap-surfacing cadence stable. A different orchestrator might have produced different gap-adjudications; this orchestrator's pattern is the one that produced v2.8.0's specific architecture.

### The bridge between substrate work and FNSR work

Substrate work and FNSR work look separate from the outside — one is a software engineering project, the other is a synthetic-moral-person project. From the inside, they're connected by the architecture pattern. The substrate work produces the patterns FNSR needs; FNSR's eventual normative apparatus draws on the substrate's audit-chain machinery; the patterns survive substrate translation because the substrate was built to make them survive. The bridge is what makes the substrate work FNSR-load-bearing rather than incidental.

---

## Closing

v2.8.0 shipped a substrate that operates protocol depth at machine speed without losing audit-trail honesty, across a meaningful capability surface, via a coordination pattern that scales beyond the current participants. That's the milestone.

The build-order continues. v2.9.0 extends; v3.0.0 generalizes; v3.1.0 deferred. None of those releases change what v2.6.0 → v2.8.0 demonstrated.

The retrospective sits in the FNSR archive as evidence for the larger project's substrate requirements. Future participants reviewing the moment when the substrate crossed from thin-coordinator to operates-protocol-depth-at-machine-speed have this document as the anchor.

— Daemon Team, drafted from the v2.6.0 → v2.8.0 conversation arc
— For Aaron's FNSR archive
