# MAREP-on-Barcode Integration Specification

**Version:** 1.0 (Draft)
**Status:** Implementation guidance for Daemon Team
**Audience:** Daemon Team (Barcode substrate implementers)
**Companion to:** [MAREP v2.2](MAREP_v2.2.md) (the retro-surface specification)
**Implementation target:** v3.0 minor release (alongside generalized-synthesist work)

---

## 0. Purpose and scope

MAREP v2.2 specifies the retro-surface generalized layer. This document specifies the **substrate-side implementation** required for full MAREP conformance on the Barcode substrate.

It is the Daemon Team's implementation companion: where MAREP says "the substrate validates `requested_sections ⊆ role_permitted_sections`," this document specifies what the validator looks like in Python.

Two-layer document structure (mirroring the FNSR Protocol Specifications bundle): each section names a substrate primitive, gives the rationale (cross-referenced to MAREP v2.2), provides implementation guidance with code-shaped sketches, and ends with open questions / extension points the Daemon Team should adjudicate before committing.

This document supersedes nothing. It augments MAREP v2.2 with substrate detail and slots into the existing FNSR Protocol Specifications conventions.

---

## 1. Relationship to substrate v2.8.0

Substrate v2.8.0 already provides primitives MAREP relies on:

| MAREP requirement | Substrate v2.8.0 mechanism |
|---|---|
| Canonical state | `state.jsonld` + atomic-write + lock |
| Chain-hashed audit trail | `hiri_sign` + `prev_hash`/`chain_hash` per history entry |
| Per-mutation locking | `state.jsonld.lock` (msvcrt / fcntl) |
| Agent dispatch contract | `invoke_agent` + `required_outputs` frontmatter |
| Multi-mode agents | `default_mode` + per-mode required_outputs |
| Structured-error veto | CPS check + `error: <slug>` agent output |
| Read-only-by-contract pattern | reconnaissance / verification-ritual-llm / adversarial-critic cat-9-second-pass |
| Audit-event types | `banking`, `forward_track`, `phase_boundary_declared`, `operator_resolution`, etc. |
| Surface-registry primitive | `surfaces/<surface>/<category-or-bucket>/` (verification surface in v2.8.0) |
| Subject-project hook loader | `surfaces/<surface>/<file>.py` co-located with spec |

These do not need to be reimplemented. MAREP-on-Barcode integration is the *delta* between substrate v2.8.0 and what MAREP requires.

---

## 2. Substrate primitives required

Six primitives are net-new for v3.0. Listed in dependency order (later primitives depend on earlier ones).

| # | Primitive | Type | Scope |
|---|---|---|---|
| 1 | Retro-surface directory + spec loader | Substrate infrastructure | ~50 LOC daemon |
| 2 | `surfaces/retro/agents/<role>.md` role-binding loader | Substrate infrastructure | ~30 LOC daemon |
| 3 | Three-stage permitted_sections validator | Substrate infrastructure | ~40 LOC daemon + CPS check |
| 4 | Length-budget frontmatter syntax | Agent contract extension | ~20 LOC daemon |
| 5 | Three anti-pattern CPS checks (§17 MAREP) | CPS extensions | ~150 LOC daemon + tests |
| 6 | Retro-applier system agent | System agent | ~200 LOC daemon + tests |

Plus three operator-facing additions:

| # | Operator surface | Scope |
|---|---|---|
| A | Three new analytical agents (`@QA`, `@DeliveryManager`, `@RiskAnalyst`) | Three new `.claude/agents/<role>.md` files; ~100 LOC each |
| B | `state_admin retro` subcommand family | ~250 LOC `state_admin.py` |
| C | `state_admin verify` extended to retro state files | ~20 LOC modification |

Estimated total scope: **~1000 LOC + ~50 tests** for v3.0 MAREP integration. Comparable to a single v2.8.0 checkpoint.

---

## 3. Primitive 1 — Retro-surface directory + spec loader

### 3.1 Directory layout (per MAREP v2.2 §5.3)

```
surfaces/
├── verification/             (existing; v2.8.0)
│   ├── surface-spec.md
│   └── categories/cat-NN-*.md
└── retro/                    (NEW; v3.0)
    ├── surface-spec.md       — retro-surface generalized spec (MAREP v2.2 reference)
    ├── agents/               — default per-role bindings
    │   ├── orchestrator.md
    │   ├── qa.md
    │   ├── delivery-manager.md
    │   ├── risk-analyst.md
    │   └── ...
    └── phases/               — per-phase entry/exit/permitted_sections specs
        ├── 01-gathering.md
        ├── 02-merge.md
        ├── 03-analysis.md
        ├── 04-consensus.md
        ├── 05-actions.md
        └── 06-compression.md
```

### 3.2 Spec loader (analog to `_load_category_specs`)

```python
def _load_retro_phase_specs() -> list[dict]:
    """Load every phases/<phase>.md under surfaces/retro/phases/.
    Returns phase-spec dicts (frontmatter fields populated, plus _path).
    Same pattern as _load_category_specs in v2.8.0; reuses
    _parse_category_frontmatter."""
    phases_dir = SURFACES_DIR / "retro" / "phases"
    if not phases_dir.exists():
        return []
    specs = []
    for path in sorted(phases_dir.glob("[0-9]*-*.md")):
        # ... same pattern as _load_category_specs ...
    return specs


def _load_retro_role_bindings() -> dict[str, dict]:
    """Load every agents/<role>.md under surfaces/retro/agents/.
    Returns dict keyed by role-name; each value is the role-binding
    frontmatter (default permitted_sections, agent_file, mode, etc.).
    Per-retro AGENTS.md may override these defaults."""
    agents_dir = SURFACES_DIR / "retro" / "agents"
    # ... similar pattern ...
```

### 3.3 Frontmatter shape (phase spec)

```yaml
---
phase_id: 01-gathering
name: Independent Gathering
entry_criteria: AGENTS.md finalized; RETRO_STATE.jsonld initialized
exit_criteria: Every agent has either submitted findings or declined
permitted_sections_per_role:
  "@Architect": [issues]
  "@QA": [issues]
  "@Skeptic": [issues, conflict_record]
  # ...
---
```

### 3.4 Open questions

- **Phase ordering enforcement**: the phase-spec filename prefix (`01-`, `02-`, ...) implies ordering. Should phase transitions be substrate-validated against the order, or operator-declared? Lean: operator-declared via Orchestrator dispatch, with the filename-prefix providing canonical ordering for `state_admin retro status` display only.

---

## 4. Primitive 2 — Role-binding loader + AGENTS.md merge

### 4.1 Per-retro AGENTS.md loading

Each retro instance has its own `AGENTS.md` at the retro's root (operator-authored before Phase 1). The substrate loader merges:

1. Defaults from `surfaces/retro/agents/<role>.md`
2. Per-retro overrides from `AGENTS.md`

```python
def _resolve_retro_role(role_name: str, agents_md_path: Path) -> dict:
    """Resolve a retro role-binding: default from surfaces/retro/agents/,
    override from per-retro AGENTS.md. Returns merged dict with
    permitted_sections, agent_file, mode, etc."""
    defaults = _load_retro_role_bindings().get(role_name, {})
    instance = _parse_agents_md(agents_md_path).get(role_name, {})
    return {**defaults, **instance}  # instance overrides defaults
```

### 4.2 AGENTS.md schema (per-retro file)

```yaml
agents:
  - role: "@Architect"
    agent_file: ".claude/agents/architect.md"
    mode: "review"                       # if multi-mode agent
    permitted_sections:                  # overrides surface default
      - issues
      - actions[*]/architectural_review
  - role: "@QA"
    agent_file: ".claude/agents/qa.md"
    # permitted_sections inherited from surfaces/retro/agents/qa.md default
```

### 4.3 Open questions

- **Schema-strict vs schema-permissive**: should AGENTS.md fail-loud if a role isn't declared in `surfaces/retro/agents/`? Lean: warn and continue (treat the per-retro AGENTS.md as authoritative; surface defaults are a starting template).
- **Mid-retro AGENTS.md amendments**: MAREP v2.2 §6 allows numbered amendments. Implementation: amendments are append-only entries in AGENTS.md with `amendment_id` + `effective_at_phase`. Substrate validates them at phase-transition time; CPS rejects if mid-phase amendment changes permitted_sections in a way that invalidates an in-flight turn.

---

## 5. Primitive 3 — Three-stage permitted_sections validator

The most architecturally important primitive. Per MAREP v2.2 §10.2, the LLM Orchestrator never makes authority decisions; the substrate does.

### 5.1 Validator implementation

```python
def _validate_requested_sections(
    role_name: str,
    requested_sections: list[str],
    agents_md_path: Path,
) -> tuple[bool, Optional[str]]:
    """Stage 3 of MAREP v2.2 §10.2 permitted-sections safety.
    
    Validates that the agent's per-turn requested_sections is a subset
    of the role's static permitted_sections (from AGENTS.md merged with
    surface defaults). Returns (True, None) on success;
    (False, reason) on rejection.
    """
    role_binding = _resolve_retro_role(role_name, agents_md_path)
    permitted = set(role_binding.get("permitted_sections", []))
    if not permitted:
        return (False, f"role {role_name!r} has no declared permitted_sections")
    requested = set(requested_sections or [])
    if not requested.issubset(permitted):
        excess = requested - permitted
        return (False, f"requested sections {sorted(excess)} exceed role's "
                       f"permitted_sections")
    return (True, None)
```

### 5.2 Section-pattern semantics — formal JSONPath subset

`permitted_sections` and `requested_sections` use a deliberately-constrained JSONPath subset. The formal subset is specified below; operators authoring permitted_sections in AGENTS.md or `surfaces/retro/agents/<role>.md` can refer to this spec rather than read the Python implementation.

**Supported syntax:**

| Form | Meaning | Example |
|---|---|---|
| `<key>` | Access the top-level key in canonical state. Grants read+write on the entire subtree under `<key>`. | `issues` (the whole `issues[]` array) |
| `<key>.<subkey>` | Traverse one level. Grants access only to the named subkey, not siblings. | `retro.phase` (only the phase field) |
| `<key>[*]` | Array wildcard. Grants access to every element of the array, but each element scoped to whatever follows. | `issues[*]` (every issue, full subtree) |
| `<key>[*]/<subkey>` | Array wildcard with element-scoped subkey. Grants access only to the named subkey of each array element. | `issues[*]/qa_evidence` (the qa_evidence field on every issue, nothing else) |
| `<key>[*]/<subkey>.<subsubkey>` | Combinable with `.` traversal. | `actions[*]/owner.id` |

**NOT supported (deliberately):**

| Form | Why omitted |
|---|---|
| `..` deep traversal | Invites scope-creep; ambiguous semantics across nested structures. |
| `[<index>]` numeric index | Element identity in `RETRO_STATE.jsonld` is by `@id`, not position; positional indices break under append/reorder. |
| `[?predicate]` predicate filters | Predicate evaluation requires interpreter; complexity invites LLM-misuse vectors. |
| `[<a>,<b>]` array slicing | Same complexity argument; no observed use case. |
| `@.<expr>` current-context | Not needed for static permitted_sections; would only matter for dynamic dispatch. |

**Determinism guarantee:** the section-pattern matcher is pure Python set-membership over textual patterns. Same inputs always produce same matches; no LLM in the matching path. This is the substrate-vs-procedure distinction (per the v2.8.0 four-property pattern) applied to scope authorization.

**Match algorithm (informal):**

```
match(actual_path, permitted_pattern):
    1. Tokenize both into segments: split on '.' and '/'
    2. For each segment-pair:
       a. If permitted_segment ends with '[*]', match any array index
          in actual_segment's position
       b. Otherwise require exact textual match
    3. If permitted_pattern has fewer segments than actual_path,
       check that the actual_path is rooted at permitted_pattern
       (i.e., permitted grants the subtree)
    4. Return True if all segments matched; False otherwise
```

**Pattern matching is greedy on subtrees, strict on subkeys.** `issues` grants the whole subtree (greedy). `issues[*]/qa_evidence` grants only `qa_evidence` (strict; not `qa_evidence.foo`). To grant a deep subtree under one element, the pattern must explicitly extend: `issues[*]/qa_evidence` grants only the field; `issues[*]/qa_evidence.subkey` grants that one subkey; `issues[*]` grants the whole issue subtree.

### 5.3 Subset rationale (FNSR-relevant)

The constrained subset is not minimalism for its own sake. It's the **substrate-vs-procedure pattern** from v2.8.0 applied to scope authorization:

- **Deterministic where possible**: pattern matching is pure Python; same inputs always produce same matches. An operator reading a permitted_sections declaration can re-derive the granted scope by hand.
- **No LLM in the authority decision**: the matcher is not invoked by the LLM Orchestrator; it's invoked by the substrate at lock-grant time. The LLM cannot manipulate the matcher's behavior.
- **Audit-chain visibility**: every scope grant + scope rejection lands as a versioned audit entry, traceable back to the permitted_sections + requested_sections at decision time.

More expressive patterns (predicates, filters, deep traversal) would all violate at least one of these properties:

- Predicates introduce LLM-evaluable conditions that the substrate cannot fully validate
- Deep traversal makes "grant the subtree" semantics ambiguous in nested structures
- Numeric indices break under the substrate's append-only `@id`-keyed identity model

The substrate-stage-3 validator (§5.1) is the deterministic enforcement point; the constrained subset is what makes that enforcement tractable.

### 5.4 CPS pre-commit re-validation (defense in depth)

Even when Stage 3 grants the lock, the CPS pre-commit hook re-validates the actual mutation diff against the granted requested_sections. If an agent's output touches paths outside its declared scope, CPS vetoes:

```python
def _check_no_out_of_scope_mutation(
    task: dict, outputs: dict, requested_sections: list[str],
) -> None:
    """Per MAREP v2.2 §17.4. Walks the outputs dict; for every path
    that would be written into RETRO_STATE.jsonld, checks it matches
    a granted section. Raises ContainmentVeto on violation."""
    actual_paths = _compute_mutation_paths(outputs)
    permitted = set(requested_sections)
    out_of_scope = [p for p in actual_paths
                    if not _matches_any_section(p, permitted)]
    if out_of_scope:
        raise ContainmentVeto(
            f"out_of_scope_mutation: agent attempted to modify "
            f"{out_of_scope} but granted scope was {sorted(permitted)}"
        )
```

### 5.5 Open questions

- **Section-pattern expressiveness**: formally specified in §5.2 + §5.3 per Aaron's CP3 adjudication. Locked in as exact paths + `[*]` array wildcards + `.field` traversal; `..` deep traversal, predicates, filters, numeric indices, and array slicing all excluded with rationale.
- **Read scoping**: §10.3 says reads are unrestricted within working memory. Should this hold for episodic memory access too? Lean: NO — episodic access goes through the Orchestrator (per §16.6); analytical agents don't have direct read access to past retros.

---

## 6. Primitive 4 — Length-budget frontmatter syntax

Per MAREP v2.2 §17.3 detection mechanism, agent frontmatter gains per-field `max_length` declarations.

### 6.1 Frontmatter syntax (additive)

```yaml
---
name: qa
description: ...
tools: Read, Grep, Glob
required_outputs: [proposed_issues, summary]
length_budgets:
  proposed_issues[*]/evidence[*]: 500    # per evidence item
  proposed_issues[*]/title: 100
  summary: 1500
conversational_connectives_forbidden:
  - "as we discussed"
  - "circling back"
  - "to your point"
  - "building on what you said"
contract_class: read-only
---
```

### 6.2 CPS check (`_check_no_freeform_brainstorm`)

```python
def _check_no_freeform_brainstorm(
    task: dict, outputs: dict, budgets: dict, forbidden_phrases: list[str],
) -> None:
    """Per MAREP v2.2 §17.3. Two-pass check:
    1. Walk outputs against per-field max_length budgets; flag overruns.
    2. Scan all free-text fields for forbidden conversational connectives.
    Either triggers a structured-error veto."""
    # ... implementation ...
```

### 6.3 Open questions

- **Forbidden-connectives list**: should the substrate ship a default list, or require per-agent specification? Lean: ship a small default list in the substrate; agents may extend per their `conversational_connectives_forbidden` frontmatter. Default list to be authored by Logic Team or operator based on observed false-collaboration patterns.

---

## 7. Primitive 5 — Three anti-pattern CPS checks

Per MAREP v2.2 §17, four anti-patterns mapped to substrate-mechanical detection. Three are net-new CPS checks (§17.1, §17.2, §17.3); the fourth (§17.4) is the out-of-scope-mutation check covered in §5.3 above.

### 7.1 `_check_no_persona_theater` (§17.1)

```python
_PERSONA_ADDR_RE = re.compile(r"@[A-Z][a-zA-Z0-9_-]*")
_DESIGNATED_REFERENCE_FIELDS = (
    "confirmed_by", "contested_by", "owner",
    "votes.cast[*].agent", "conflict_record[*].positions[*].agent",
)

def _check_no_persona_theater(outputs: dict, agent_path_in_outputs: str) -> None:
    """Per MAREP v2.2 §17.1. Scans outputs free-text fields for
    @<agent> patterns outside designated reference fields. Raises
    ContainmentVeto with error: persona_theater_detected on hit."""
    free_text_fields = _collect_free_text_fields(outputs,
                                                  exclude=_DESIGNATED_REFERENCE_FIELDS)
    hits = []
    for path, text in free_text_fields.items():
        for m in _PERSONA_ADDR_RE.finditer(text):
            hits.append({"path": path, "match": m.group(0)})
    if hits:
        raise ContainmentVeto(
            f"persona_theater_detected: free-text fields contain agent "
            f"addresses outside designated reference fields: {hits}"
        )
```

### 7.2 `_check_no_redundant_affirmation` (§17.2)

Levenshtein-based v1; LLM-judge for future. Compares against the **prior turn's outputs in the same retro**, not all prior outputs.

```python
def _check_no_redundant_affirmation(
    task: dict, outputs: dict, retro_state: dict, threshold: float = 0.85,
) -> None:
    """Per MAREP v2.2 §17.2. Computes normalized Levenshtein similarity
    between this turn's free-text body and the prior turn's body in
    the same retro. Rejects when similarity >= threshold."""
    prior_turn = _find_prior_turn_outputs(retro_state, task["agent"])
    if prior_turn is None:
        return  # no prior turn; no redundancy check applicable
    current_body = _concat_free_text(outputs)
    prior_body = _concat_free_text(prior_turn)
    similarity = _normalized_levenshtein(current_body, prior_body)
    if similarity >= threshold:
        raise ContainmentVeto(
            f"redundant_affirmation: similarity {similarity:.2f} >= "
            f"threshold {threshold:.2f} vs prior turn"
        )
```

**Threshold tuning** is a future-work concern. v1 implementation uses 0.85 as a starting heuristic; observe in production and tune. Per MAREP v2.2 §17.2, LLM-judge similarity may substitute the deterministic comparison once production patterns are observed.

### 7.3 `_check_no_freeform_brainstorm` (§17.3)

Covered in §6.2 above (length-budget + forbidden-connectives).

### 7.4 Wiring into CPS

All three checks dispatch from the main `cps_check` function based on agent's contract_class or surface affiliation:

```python
def cps_check(task, proposed_outputs):
    # ... existing checks (null, structured error, required_outputs) ...
    
    # MAREP retro-surface anti-pattern checks
    if _is_retro_surface_task(task):
        agent_name = task.get("agent")
        frontmatter = _read_agent_frontmatter(agent_name)
        _check_no_persona_theater(proposed_outputs, agent_name)
        if frontmatter.get("length_budgets"):
            _check_no_freeform_brainstorm(
                task, proposed_outputs,
                frontmatter["length_budgets"],
                frontmatter.get("conversational_connectives_forbidden", []),
            )
        retro_state = _load_active_retro_state(task)
        if retro_state:
            _check_no_redundant_affirmation(task, proposed_outputs, retro_state)
```

### 7.5 Open questions

- **`_is_retro_surface_task` detection**: how does the substrate know a task is part of a retro vs the substrate's main work? Options: (a) task `inputs.surface: retro`; (b) task `@id` matches `urn:fnsr:retro:...`; (c) the dispatched agent's `contract_class` includes `retro`. Lean: (a) — explicit operator-set surface attribution on the task.

---

## 8. Primitive 6 — Retro-applier system agent

Analog to v2.6.0's `applier` for code changes, scoped to RETRO_STATE.jsonld.

### 8.1 Contract

```yaml
---
name: retro-applier
description: Deterministic system agent. Consumes analytical-agent
  proposals (proposed_issues, proposed_actions, vote_casts) and merges
  them into RETRO_STATE.jsonld with chain-hashed audit entries. Same
  pattern as applier for code changes, scoped to retro state.
required_outputs: [applied, failed, summary]
---
```

### 8.2 System agent implementation

```python
def _retro_apply(task, upstream) -> WorkerResult:
    """Merge analytical-agent proposals into RETRO_STATE.jsonld.
    
    Inputs (task.inputs):
      retro_state_path: path to RETRO_STATE.jsonld
      proposals: dict from one or more upstream tasks' outputs;
                 keys: proposed_issues, proposed_actions, vote_casts
      requested_sections: scope-validation per Primitive 3
    
    Output:
      applied: list of {section, @id, mutation}
      failed: list of {section, @id, reason}
      summary: str
    """
    retro_state_path = Path(task["inputs"]["retro_state_path"])
    retro_state = _load_retro_state(retro_state_path)
    expected_version = task["inputs"].get("version_read")
    # CAS check per MAREP v2.2 §9
    if expected_version is not None and retro_state["retro"]["version"] != expected_version:
        return WorkerResult(True, {
            "error": "version_mismatch",
            "current_version": retro_state["retro"]["version"],
            "expected_version": expected_version,
        }, "", "")
    applied = []
    failed = []
    for proposal in task["inputs"]["proposals"]:
        # Merge each proposal; track applied/failed
        # ... idempotent merge per @id ...
    # Increment version; append audit entry; atomic write
    retro_state["retro"]["version"] += 1
    _append_retro_audit(retro_state, task["@id"], applied)
    _atomic_write(retro_state_path, retro_state)
    return WorkerResult(True, {
        "applied": applied,
        "failed": failed,
        "summary": f"applied {len(applied)} proposals; "
                   f"{len(failed)} failed; "
                   f"retro state now at version {retro_state['retro']['version']}",
    }, "", "")
```

### 8.3 Registration

```python
SYSTEM_AGENTS = {
    "applier": _apply_changes,
    "mojibake-repair": _mojibake_repair,
    "question-resolver": _question_resolver,
    "verification-ritual": _verification_ritual,
    "retro-applier": _retro_apply,        # v3.0 NEW
}
```

### 8.4 Open questions

- **Idempotency key**: re-applying the same proposal MUST be a no-op (MAREP v2.2 §11.2). Implementation: use proposal's `@id` as the idempotency key. If an issue with the same @id already exists at the same version, the merge is a no-op. If the @id exists at a different version, return failed with `reason: version_collision`.
- **Vote merging semantics**: when an agent submits a vote_cast, it appends to `votes[*]/cast` array. Two agents submitting votes on the same subject in the same turn-window — how does the substrate handle? Lean: vote_casts are append-only; the @id of the vote is per-subject (`urn:retro:vote:PERF-001`); cast entries are per-agent within the vote. Concurrent vote submission is serialized via the existing per-mutation lock.

---

## 9. Three new analytical agents

Per MAREP v2.2 §4.2, three roles are retro-surface-specific without existing substrate analogs.

### 9.1 `@QA` (`.claude/agents/qa.md`)

```yaml
---
name: qa
description: Quality and verification perspective for retros. Surfaces
  defects, verification gaps, regression risks, process quality
  observations as proposed issues + evidence. Read-only-by-contract.
tools: Read, Grep, Glob
required_outputs: [proposed_issues, summary]
contract_class: read-only
length_budgets:
  proposed_issues[*]/title: 100
  proposed_issues[*]/evidence[*]: 500
  summary: 1500
---
```

Prompt should be structurally similar to `reconnaissance.md` — read-only-by-contract, observation-grounded-in-evidence, no proposals beyond `proposed_issues`. Focus areas: test coverage gaps, regression patterns, defect clustering, verification scope drift.

### 9.2 `@DeliveryManager` (`.claude/agents/delivery-manager.md`)

Focus areas: sprint predictability, throughput, blockers, coordination overhead, dependency thrash. Output shape similar to `@QA` (proposed_issues + summary). Read-only-by-contract.

### 9.3 `@RiskAnalyst` (`.claude/agents/risk-analyst.md`)

Focus areas: hidden failure modes, systemic fragility, operational exposure, what-if-this-breaks scenarios. Related to but distinct from `adversarial-critic` — adversarial-critic challenges specific findings; @RiskAnalyst surfaces latent risks not yet observed.

### 9.4 Open questions

- **Default `length_budgets`**: what's a reasonable starting set? Lean: 100 chars for titles, 500 for evidence items, 1500 for summary. Tune in production.
- **Should `@RiskAnalyst` reuse `adversarial-critic` via multi-mode**: lean NO — the role's focus (latent-risk surfacing) is distinct enough from adversarial-critic's role (finding-challenging) that multi-mode would muddy both contracts.

---

## 10. `state_admin retro` subcommand family

Per MAREP v2.2 §20 item 6, operator-facing CLI mirroring the v2.7.0 `forward-track` pattern.

```bash
# Initialize a new retro
state_admin retro init <retro-id> --sprint <sprint-id> --agents-md <path>

# Transition phase (Orchestrator dispatches this; operator can also dispatch)
state_admin retro phase-transition <retro-id> --to-phase <phase-id>

# Record an operator-cast vote (operator participating as deciding voice)
state_admin retro vote <retro-id> --subject <subject> --position <pos>

# Archive a completed retro (Phase 6 close); writes to FNSR archive
state_admin retro archive <retro-id> --archive-root <path>

# Verify retro state chain-hash integrity
state_admin retro verify <retro-id>

# List active and recent retros
state_admin retro list [--status active|complete|archived]
```

### 10.1 Open questions

- **Archive path resolution**: `--archive-root` defaults to env var `FNSR_ARCHIVE_ROOT` (analog to `FNSR_SURFACES_DIR`); per Aaron's directive the canonical location is `<operator>/Documents/ariadne/archive/retrospectives/`. Substrate doesn't hardcode the path; operator sets the env var or passes explicitly.

---

## 11. LLM-with-elevated-authority pattern (substrate primitive)

Per MAREP v2.2 §4.1, the Orchestrator role is the **first instance of a reusable substrate primitive**: an LLM worker agent with elevated retro-surface authority but no substrate-level privileges.

### 11.1 Pattern shape

An LLM-with-elevated-authority agent:

- **Operates as a worker agent** (LLM-dispatched; no special daemon-level privileges)
- **Has elevated responsibilities within its surface** (workflow control, conflict detection, summarization, etc.)
- **Cannot bypass substrate enforcement** (CPS check applies; permitted_sections apply; audit-chain applies)
- **Decisions land in audit chain like any other agent's** (auditable through the same machinery)

### 11.2 Substrate accommodation

The substrate already supports this pattern without modification. The Orchestrator agent's `.md` file declares its tools (Read, Grep, Glob plus dispatch-authority-marker-fields), its mode if multi-mode, its required_outputs. The substrate dispatches it via `invoke_agent` like any other worker.

**No new substrate code is required for this pattern itself** — the v2.7.0 multi-mode required_outputs + the v2.8.0 default_mode mechanism are sufficient. The MAREP-Orchestrator's elevated-authority claim is encoded in its prompt + frontmatter, not in substrate-level privilege escalation.

### 11.3 Future instances

The pattern generalizes. Future agents that may adopt it:

- **Generalized synthesist** (v3.0; reconciles multiple parallel input streams with elevated authority over the synthesis surface)
- **Phase-exit retro finalizer** (consolidates phase-exit deliberation outputs with elevated authority)
- **FNSR moral-person deliberative coordinator** (eventual; coordinates parallel moral-judgment streams with elevated authority over the deliberation surface)

Each is a worker agent with elevated surface-authority and no substrate-level privilege. The pattern's FNSR-relevance is that **normative apparatus often requires elevated-authority coordination without elevated-substrate-privilege** — the synthetic moral person project needs this exact shape.

### 11.4 Naming

This pattern deserves a name beyond "LLM-with-elevated-authority." Suggested: **bounded-authority orchestrator** (BAO) — bounded by the surface scope, by substrate enforcement, and by audit-chain visibility; orchestrator by responsibility within those bounds. Open for operator naming preference.

---

## 12. Semantic-memory immutability enforcement

Per MAREP v2.2 §16.6, retro-turn updates that try to mutate semantic-memory paths are CPS-rejected.

### 12.1 Path-set definition

```python
_SEMANTIC_MEMORY_PATHS = (
    "surfaces/",                       # All surface specs
    "project/DECISIONS.md",            # ADR registry
    "project/SPEC.md",                 # Subject project spec
    "project/ROADMAP.md",
    "project/IMPLEMENTATION_PLAN.md",
    "CLAUDE.md",
    "PLAYBOOK.md",
    "project/Routing/",                # FNSR Protocol Specifications
    ".claude/agents/",                 # Substrate-wide agent contracts
)
```

(`FNSR_SEMANTIC_MEMORY_PATHS` env var allows override.)

### 12.2 CPS check

```python
def _check_no_semantic_memory_mutation(task, outputs) -> None:
    """Per MAREP v2.2 §16.6. If a retro-surface task's outputs would
    write to a semantic-memory path, veto. Semantic memory updates
    require ADR-or-equivalent process; not performable from a retro
    turn."""
    if not _is_retro_surface_task(task):
        return
    mutation_paths = _compute_mutation_paths(outputs)
    semantic_hits = [p for p in mutation_paths
                     if any(p.startswith(prefix)
                            for prefix in _SEMANTIC_MEMORY_PATHS)]
    if semantic_hits:
        raise ContainmentVeto(
            f"semantic_memory_immutable_from_retro: retro-surface task "
            f"attempted to write semantic-memory paths {semantic_hits}; "
            f"semantic memory updates require ADR-or-equivalent process "
            f"outside the retro turn"
        )
```

### 12.3 Episodic → Semantic promotion path (deliberate)

Per MAREP v2.2 §16.4 + Aaron's confirmation: Episodic → Semantic is **deliberate, not automatic**. Implementation:

1. Operator reviews episodic entries (`<fnsr-archive>/archive/retrospectives/`) at phase-exit retro deliberation.
2. For each entry the operator wants to promote, the operator queues a `reconnaissance → ratification → commit-finalize` chain per FNSR Spec 03 to author the corresponding ADR / PLAYBOOK update / CLAUDE.md amendment.
3. The promotion is itself a `forward_track` event with `subject.type: candidacy`, `sub_surface: internal-methodology-refinement`, `surfacing_task_id: <retro task @id>` per FNSR Spec 07.

This reuses substrate v2.8.0 machinery; no new substrate code required for the promotion mechanism itself, only for the **rejection** of in-retro semantic-memory mutation (§12.2 above).

---

## 13. Chain-hashed RETRO_STATE.jsonld audit

Per MAREP v2.2 §7.4 + §9, retro state inherits the substrate's append-only invariant via `hiri_sign`.

### 13.1 Implementation

The existing `hiri_sign(prev_hash, payload) -> chain_hash` function works unchanged on retro state. The substrate's `_append_audit` helper (state_admin.py) generalizes from task-history to retro-state-audit:

```python
def _append_retro_audit(retro_state, task_id, mutation_summary):
    """Same pattern as _append_audit; operates on retro_state['audit']
    instead of task['history']."""
    prev_hash = retro_state["audit"][-1]["chain_hash"] if retro_state["audit"] else "0" * 64
    payload = {
        "event": "retro_mutation",
        "task_id": task_id,
        "version": retro_state["retro"]["version"],
        "diff_summary": mutation_summary,
    }
    new_hash = hiri_sign(prev_hash, payload)
    retro_state["audit"].append({
        "version": retro_state["retro"]["version"],
        "prev_hash": prev_hash,
        "chain_hash": new_hash,
        "timestamp": _now_iso(),
        **payload,
    })
```

### 13.2 `state_admin retro verify`

Generalizes the existing `state_admin verify`:

```python
def cmd_retro_verify(args):
    """Walk retro state's audit array; re-derive each chain_hash from
    prev_hash + event + payload; report mismatch. Same pattern as
    cmd_verify for state.jsonld; substrate's chain-integrity invariant
    extends to retro state without modification."""
    # ...
```

---

## 14. Coexistence with substrate v2.8.0 (back-compat)

v3.0 MAREP retros must not break v2.8.0 substrate operations:

- **state.jsonld remains the substrate's authoritative state.** RETRO_STATE.jsonld files are *sibling* canonical states scoped to individual retros; the substrate doesn't merge them.
- **Existing v2.8.0 agents (verification-ritual, architect, etc.) work unchanged in non-retro contexts.** The retro-surface anti-pattern CPS checks only fire on retro-surface tasks (detected per §7.5).
- **Substrate v2.8.0 audit chain remains valid.** Retro-related `retro_closed` audit events appended to state.jsonld are additive; they don't invalidate prior chain entries.
- **v2.8.0-shipped substrate-level operations (kickoff ritual, verification ritual, banking, forward-track) continue without modification.** MAREP runs as a parallel workflow on the same daemon.

### 14.1 What about retros launched against v2.8.0 substrate (light adoption)?

Per MAREP v2.2 §20: light adoption is supported. Retros run on v2.8.0 substrate without the new primitives by:

- Using existing agents (architect / developer / ux-sme / adversarial-critic)
- Bypassing voting/compression in favor of `awaiting_operator_decision` resolution
- Skipping anti-pattern detection checks (since they're not implemented)
- Storing retro state in state.jsonld as task histories rather than separate RETRO_STATE.jsonld

This is the operational fallback if v3.0 MAREP integration ships later than planned. Operators can run informal retros on v2.8.0 substrate immediately; full MAREP conformance arrives with v3.0.

---

## 15. Testing strategy

Per the substrate's gap-surfacing cadence: v3.0 MAREP integration should ship in **2-3 checkpoints** matching v2.8.0's pattern.

### 15.1 Checkpoint sketch

**CP1 (v3.0-alpha.1)** — Foundation:
- `surfaces/retro/` directory + spec loader (Primitives 1, 2)
- Three-stage permitted_sections validator (Primitive 3)
- Three new analytical agents (Operator surface A)
- Tests: ~20

**CP2 (v3.0-alpha.2)** — Substrate primitives:
- Retro-applier system agent (Primitive 6)
- Length-budget frontmatter syntax (Primitive 4)
- Three anti-pattern CPS checks (Primitive 5)
- Semantic-memory immutability enforcement (§12)
- Tests: ~25

**CP3 (v3.0)** — Operator surface + integration:
- `state_admin retro` subcommand family (Operator surface B)
- `state_admin verify` extended (Operator surface C)
- End-to-end retro test (init → 6 phases → archive)
- Documentation sweep (CLAUDE.md / PLAYBOOK.md / CHANGELOG)
- Final v3.0 tag (joint with generalized-synthesist work)

Estimated total: ~50 tests; full suite at v3.0 = ~344 (up from 294 at v2.8.0).

### 15.2 Anti-pattern detection tuning

The three anti-pattern detections (persona theater, redundant affirmation, freeform brainstorm) will produce false positives and false negatives in production. Per the substrate's pattern: ship with reasonable defaults; observe; tune.

- Persona theater: false-positive risk LOW (the `@<agent>` pattern is structural). False-negative risk MODERATE (paraphrased addresses like "as our QA friend mentioned" may slip through). Lean: ship v1 as-is; refine after observation.
- Redundant affirmation: false-positive risk HIGH (legitimate elaboration on a prior point may hit similarity threshold). False-negative risk MODERATE. Lean: ship with threshold 0.85 and per-retro override; tune in production.
- Freeform brainstorm (length budgets + forbidden connectives): false-positive risk MODERATE (tight budgets cause legitimate work to be vetoed). Lean: ship with generous defaults (~500 chars per evidence item; ~1500 chars summary); per-agent override.

---

## 16. Open questions for Daemon Team adjudication

These should be resolved before CP1 commits:

1. **`_is_retro_surface_task` detection** — explicit `inputs.surface: retro` vs other mechanisms (§7.5). Lean (a) — explicit.
2. **Section-pattern syntax subset** — which JSONPath subset to support (§5.4). Lean: exact paths + `[*]` wildcards + `.field` traversal; reject `..`, predicates, filters.
3. **Redundant-affirmation threshold** — 0.85 starting heuristic, or different? (§7.2). Tune in production; ship v1 at 0.85.
4. **Forbidden-connectives default list** — operator-authored or substrate-default (§6.3). Lean: ship a small substrate default; agents may extend.
5. **AGENTS.md amendment mid-retro semantics** — strict (reject if mid-phase amendment affects in-flight turn) vs permissive (apply at next phase transition). Lean: strict.
6. **LLM-with-elevated-authority pattern naming** — "bounded-authority orchestrator" (BAO) vs alternative (§11.4). Operator's call.
7. **Vote-record idempotency** — vote @id uniqueness scope (per-retro vs global). Lean: per-retro scoped via `urn:retro:<retro-id>:vote:<NNN>` URN convention.

---

## 17. Sequencing into v3.0

Per Aaron's v3.0 directive: "generalized synthesist + phase-exit-retro + phase-complete-declaration". MAREP integration overlaps with the generalized synthesist:

- **Generalized synthesist** = the synthesist agent extended to reconcile multiple parallel input streams. Naturally fits the LLM-with-elevated-authority (BAO) pattern; the MAREP-Orchestrator is one instance.
- **Phase-exit retro** = the operator-deliberation cycle at phase boundary that promotes episodic → semantic memory. Naturally MAREP-shaped; the retro IS the phase-exit deliberation.
- **Phase-complete-declaration** = the operator-authored signal that a phase has met its acceptance criteria. Triggers the phase-exit retro.

Implementation order proposal:

1. **v3.0-alpha.1**: BAO pattern formalization + generalized synthesist + MAREP surfaces/retro/ foundation
2. **v3.0-alpha.2**: MAREP substrate primitives (retro-applier, anti-pattern CPS, length budgets) + phase-complete-declaration operator surface
3. **v3.0**: phase-exit retro end-to-end + state_admin retro family + Episodic→Semantic promotion path documentation + final v3.0 tag

Total estimated scope: ~1500 LOC + ~80 tests across the three checkpoints. Comparable to v2.8.0's four-checkpoint scope but compressed to three.

---

## 18. FNSR-relevance summary

MAREP-on-Barcode integration ships three FNSR-load-bearing pieces:

1. **The bounded-authority orchestrator (BAO) pattern** — the architecture's precedent for elevated-authority-without-substrate-privilege. The synthetic moral person project's deliberative coordinators (parallel-moral-judgment-stream reconcilers; equity-assessment orchestrators) will adopt this shape. Pattern documented in §11; first instance in MAREP-Orchestrator.

2. **The deliberate-promotion path for Episodic → Semantic memory** — the architecture's precedent for "tacit observations accumulate; deliberate operator action promotes to canonical normative apparatus." The synthetic moral person project requires this discipline at every level — normative apparatus evolves through deliberate operator-mediated promotion, not automatic accumulation. Pattern documented in §12.3; reuses substrate v2.8.0 forward-track + ratification + commit-finalize chain.

3. **The substrate-mechanical anti-pattern enforcement** — the architecture's precedent for structurally-enforced behavioral constraints. Persona theater, recursive agreement loops, freeform brainstorm drift, out-of-scope mutation are all generalizable failure modes; the synthetic moral person project will face structurally-similar failure modes (judgment-by-emulation, false-consensus in deliberation, unprincipled reasoning, authority-boundary violation). Pattern: forbidden-behavior + paired-structural-detection + structured-error veto. Documented in §7.

The substrate's verification-as-substrate move (v2.8.0) made protocol depth operable at machine speed. MAREP-on-Barcode integration extends that to **deliberation depth** — the substrate operates retrospective deliberation at machine speed with the same audit-trail-honesty properties. After v3.0 ships, the substrate operates both *evidence-gated change* (Pass 2a/2b chain) and *deliberative reflection* (MAREP retros) under one architectural pattern.

---

## Changelog

* **v1.0 (Draft, 2026-05-18)** — Initial draft. Companion to MAREP v2.2. Specifies six net-new substrate primitives + three operator surface additions; estimates ~1000 LOC + ~50 tests for v3.0 integration. Sequenced into three checkpoints alongside generalized-synthesist work.
