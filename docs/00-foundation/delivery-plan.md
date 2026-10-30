# FNSR Delivery Plan: Slices, Rules, and Why

**Version:** 1.0
**Date:** 2026-10-30
**Owner:** Aaron Damiano
**Status:** Ratified 2026-10-30. In force (§9).
**Supersedes:** the phased roadmap (§5) of Portfolio Planning v3.6. The architecture in that document (§3 and §4: the Minimum Viable Epistemic Loop, the Safety Floor, the Subjectivity Stack) is kept unchanged.
**Evidence:** `docs/05-evidence-audit/audit.md`, computed from collected evidence on 2026-10-29.

---

## 1. Purpose

This plan says what gets built next, in what order, and under what rules, so that the work reaches a
running synthetic moral agent instead of a growing library of specifications. It does not change what
FNSR is for. The goal, the thesis and the commitments in *The Plot* stand as written.

## 2. Why this plan is necessary

### 2.1 What the evidence shows

The evidence audit measured the portfolio rather than reading its documents. As of 2026-10-29:

| Measure | Value |
| --- | --- |
| Repositories on GitHub | 94 |
| Repositories touched in the last 90 days | 23 |
| Buildable specifications in the spec index | 62 |
| Specifications with no code in any repository | 47 |
| Specifications whose status claims maturity (Final, Hardened, Stable, Candidate, Ready, Normative) but have no code | 22 of 27 |
| Specifications resting on passing tests | 11 (10 at L3, HIRI Protocol at L5) |
| Specifications whose code is used by another repository and deployed | 1 (HIRI Protocol) |

Three patterns explain these numbers.

1. **Dependency descent.** Work on one service reveals that it needs another service as complex as
   itself. The first is paused, the second is stubbed and then built, and the same happens again
   one level down. A depth-first walk through a dependency graph this large does not return for one
   person in any useful time.
2. **Parallel copies.** The same specification has been built several times to test build
   techniques: BIBSS exists in at least five repositories, and the SNP, BIBSS and SAS pipeline exists
   twice. Each copy looks like progress in a repository list. None of them is used by anything else.
3. **Status by document.** "Hardened" and "Final" were written into documents that have no code
   behind them. *The Plot* already names this error for the system itself: a validated status is
   not truth, and promoting one to the other is "No Oracle Claims violated through the back door"
   (§2.1, normative note of 2026-05-15). The portfolio did to itself what the system must never do.

The repositories that are finished (mermaid, wastewatch, MeetingGraph) all have something in
common: someone uses them. The work ships when it has a user and stalls when its only user is the
next service down.

### 2.2 Why the existing roadmap could not fix this

Portfolio Planning v3.6 is logically sound. Its dependency analysis is correct: you cannot have
narrative identity without a self-model, and containment must exist before action. Its error is one
of execution. It orders work **bottom-up and breadth-first**: lay each layer before the one above
it. For a team, that schedule is slow. For one person it is the dependency descent of §2.1, written
down as a plan. Every phase starts with services whose own prerequisites are unbuilt.

This plan keeps the dependency analysis and changes the order of construction: **end to end first,
then deeper.**

## 3. Why this is not an abandonment of the synthetic moral agent

**The goal does not move.** The target remains an accountable synthetic agent that reasons, judges
and acts while staying semantically honest, epistemically bounded and morally answerable. Nothing in
*The Plot*, the philosophy layer or the architecture is withdrawn.

**Every part of the agent stays present from the first running version.** The plan builds a
*walking skeleton*: one thin path that runs from a situation in to an accountable judgment out, with
every service on the full architecture represented. Services not yet built are present as stubs,
with their real interfaces and fixed answers. Abandoning a part of the design would mean deleting
its place. A stub keeps the place, the interface and the obligation to fill it.

**Running code is the only thing the thesis can be tested on.** The thesis makes claims about what
a system can do: trace its reasoning, bound its claims, answer for its judgments. A specification
cannot fail those tests and a running system can. Fifty specifications with no code are not closer
to a synthetic moral agent than five with code, because none of their claims has yet met reality. The ethics experiment (E-PC) already applies this standard to the perspective method.
This plan applies it to the whole agent.

**The specifications are kept as design capital.** Paused specifications are not discarded and are
not counted as failures. They are the design the skeleton grows into. What changes is that a
specification is built when a user of the running agent needs it, not before.

**The first slices are on the path, not off it.** Slice 1 builds the agent's ability to turn real
institutional data into a knowledge graph, which is the *Remember* leg of the Minimum Viable
Epistemic Loop (Portfolio Planning v3.6, §4.1) and the Semantic Data Platform made concrete, on real
data for the first time. Slice 2 decides whether the perspective method at the heart of the Integral
Ethics Agent survives a pre-registered test before anything is built on it. Slice 3 is the agent's
first end-to-end run.

**The Safety Floor is preserved, not stubbed.** The first running agent has no means to act: it
produces judgments for a human reader and nothing else, so *Human Override* holds by construction.
Rule R6 forbids stubbing any safety service once a slice gives the agent a capability to act.

## 4. The plan

Work proceeds in **slices**. A slice is the thinnest piece of work that delivers a usable result to
a named user. One slice is active at a time (R1).

### Slice 1: real data to a knowledge graph

| | |
| --- | --- |
| **Window** | 2026-10-30 to 2026-11-26 |
| **User** | Aaron's employer's data team, named privately, not in this repository |
| **Outcome** | A Jira schema is mapped to a realist BFO/CCO model through the Semantic Data Dictionary, exported as RML, and executed by an existing RML engine into a knowledge graph that passes the SDD's SHACL shapes. |
| **In scope** | SemanticDataDictionary: release verification on a real schema; an RML export module. Schema clean-up, if needed, as a script inside the SDD repository. An off-the-shelf RML engine. |
| **Out of scope** | A separate normalization service. Building an RML engine or a triple store. Fandaws, HIRI, SAS, BIBSS. |
| **Done** | The user has the knowledge graph and has used it for their purpose. |
| **Weekly targets** | Week 1: definition of done agreed with the user, SDD run on a real schema, decision on clean-up. Week 2: RML export. Week 3: knowledge graph produced and validated. Week 4: buffer and hand-off; nothing new. |
| **Data rule** | Employer data and schemas never enter a public repository. The SDD runs offline in the browser and the LLM step uses the employer's own LLM. |

### Slice 2: complete the ethics experiment (E-PC)

| | |
| --- | --- |
| **Window** | Opens after Slice 1 is done. Its end depends on the annotators' and raters' work; the timebox for Aaron's own tasks is set when it opens. |
| **User** | Aaron and the experiment's annotators and raters. |
| **Outcome** | A verdict on the perspective method under the pre-registered protocol and kill conditions (`experiments/e-pc/PREREG.md`). |
| **Done** | `results/<run_id>/report.md` exists for the credited run. |
| **Gate** | The verdict decides the deliberation step of Slice 3. If the method fails, Slice 3 uses the alternative the result points to, and the IEA specification is revised before it is built on. |
| **Note** | Annotation that other people do during Slice 1 does not count as a second active slice (R1). |

### Slice 3: FNSR v0, the walking skeleton

| | |
| --- | --- |
| **Window** | Opens after Slice 2. Timebox set when it opens; eight weeks is the starting proposal. |
| **User** | An academic collaborator who reads the deliberations and did not write the cases. Named privately, not in this repository. |
| **Outcome** | A moral case goes in as text; a traced, multi-perspective deliberation comes out, recorded in a hash-chained log that an independent verifier accepts. |
| **Chain** | TagTeam.js (read the situation) → ValueNet (name the values at stake) → Integral Ethics Agent, as shaped by the E-PC verdict (deliberate) → hash-chained log checked by FNSR_ChainVerifier (account for it). |
| **Stubbed** | Self-Model, Commitment Tracking, Affective Valence, Narrative Identity, Social Modeling, Governance, Fandaws, HIRI privacy, and every other service on the path. Each stub has its real interface and returns fixed, hand-written answers. |
| **Not present** | Any capability to act. v0 produces text for a human reader. |
| **Done** | The named user has used it on cases they did not write, and the log verifies. |

### After v0: grow by pull

After v0, each slice replaces **one** stub with a real service, chosen because the skeleton's user
hit a limit the stub cannot meet. The choice of which stub to replace is made between slices and
recorded with the reason. When a slice would give the agent any capability to act, the next slices
are the Safety Floor services (Containment, Behavioral Alignment Monitor), built for real and
independent of what they constrain, before that capability ships.

## 5. The rules

These rules are binding while this plan is in force. "MUST" means the rule is not a guideline.

**R1. One active slice.** Aaron MUST NOT build on more than one slice at a time. Work other people do
for a later slice may continue.

**R2. A named user.** A slice MUST have a named user before it opens. If no user can be named, the
slice is the wrong slice and another is chosen. Users are named privately; this repository records
their role, never their name.

**R3. Done means used.** A slice is done when its named user has used its outcome for a real task.
Passing tests, finished specifications and green CI are evidence along the way. None of them is done.

**R4. Timebox, then cut scope.** A slice has a fixed end date set when it opens. When time runs short,
scope is cut. The date does not move.

**R5. The stub rule.** When a slice turns out to need another service, Aaron MUST:
1. write a stub with the service's interface that returns fixed, hand-written answers;
2. add one line to `LATER.md` in the slice's repository: what was needed, and why;
3. continue the slice.

The stubbed service's repository MUST NOT be opened for work during the slice. A stub stays a stub
until a later slice is chosen, between slices, to replace it.

**R6. The Safety Floor is never stubbed for action.** No slice may give the agent a capability to act
while any Safety Floor service is a stub. Safety services MUST NOT depend on the services they
constrain (*The Plot*, §2.3).

**R7. No new repositories, no parallel copies.** No repository is created during a slice. No
specification is built a second time. Experiments in build technique (including the IntegratedAgent
factory) happen only as a declared research slice, chosen between slices like any other.

**R8. Specification freeze.** No new specification is written, and no paused specification is
revised, unless the active slice's user needs it. Ideas for specifications go to `LATER.md`.

**R9. Evidence, not status.** Progress is reported only from the evidence audit's computed levels and
from users' use. A status written in a document ("Hardened", "Final", "Ready") is a claim and is not
reported as progress.

**R10. The plan changes only between slices.** An amendment is written into this file with its date
and reason, and ratified by Aaron. An idea that arrives during a slice goes to `LATER.md`, and the
slice continues.

**R11. A weekly check of fifteen minutes.** Once a week: rerun the evidence audit on the active
slice's repositories only; confirm the slice is on its weekly target; read `LATER.md`, adding to it
but not acting on it. The audit tooling itself is not extended during a slice.

## 6. Paused, by name

Paused means not worked on until a slice chooses it. Paused is not failed: these repositories are the
research and design that taught the skeleton what it needs.

- **Semantic data line:** SemanticNormalization, SchemaService, SchemaAlignment, chartcraft,
  Percept-Formation-Pipeline, BIBS, BIBS2, BIBSS3, SemanticFunctionSchema,
  Sanitization-and-Ingestion-Service.
- **Knowledge and identity:** fandaws, fanlink, Fandaws-Sentinel, zenith-graph, term_relations, HIRI,
  HIRI-Passport, HIRI-Directory, HIRI-Conversation-Protocol, FNSRBridgeOntology.
- **Ethics and values (until Slices 2 and 3 open):** GNOMON, Ontology-of-Freedom,
  wrm-e2-independent-library-test.
- **Ontology content:** Business-and-Agent-Capabilities-Ontology, BusinessProcessOntology,
  BPO-Template-Port, EntityResolutionService.
- **Build-technique research and tooling:** IntegratedAgent, AgenticDev, assay,
  Specification-Refinement-System, HIRI-Review-and-Signoff, and the remaining supporting tools in
  `docs/05-evidence-audit/inventory.yaml`.
- **Specifications:** the 47 buildable specifications with no code, and every specification not on
  the active slice.

**Active or queued:** SemanticDataDictionary (Slice 1); ariadne and `experiments/e-pc` (Slice 2);
TagTeam.js, ValueNet, worldview-realization-model, Integral-Ethics-Engine and FNSR_ChainVerifier
(Slice 3).

Repositories with users outside FNSR (mermaid, wastewatch, MeetingGraph) are outside this plan's
scope and keep their own rhythm.

## 7. How progress is measured

| Question | Where the answer comes from |
| --- | --- |
| Is the active slice on track? | Its weekly target (§4) and the weekly check (R11). |
| Is it done? | Its named user's use (R3). |
| What level has a component reached? | `docs/05-evidence-audit/audit.md`, computed from collected evidence. |
| What has been deferred, and why? | `LATER.md` in each slice's repository. |

## 8. Relation to other documents

- *The Plot*: unchanged. This plan serves it, and its §2.1 normative note is the reason for R9.
- Portfolio Planning v3.6: its architecture (§3, §4) is kept. Its phased roadmap (§5) is superseded
  by this plan. Its status should be amended to say so when this plan is ratified.
- The spec index: unchanged. Specifications keep their document status; the audit reports the
  evidence beside it.
- `docs/05-evidence-audit/`: the measuring instrument for this plan (R9, R11).

## 9. Ratification

This plan comes into force when Aaron records below the date of ratification and any amendments
made at ratification.

| Field | Value |
| --- | --- |
| Ratified by | Aaron Damiano |
| Date | 2026-10-30 |
| Amendments at ratification | None. Before ratification, users were changed to be named privately, never in this repository (R2). |
