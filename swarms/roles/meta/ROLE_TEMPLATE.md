# Role contract template

> Status: current drafting aid, last reviewed 2026-08-05. This Markdown file is not runtime-authoritative and must remain `.md`. Materialize an approved role only as a top-level `../<role_id>.toml` file, then synchronize [`ROLE_MANIFEST.md`](ROLE_MANIFEST.md) and run [`VALIDATION.md`](VALIDATION.md).

## Use this template safely

1. Complete the candidate worksheet.
2. Apply the [role admission test](DESIGN.md#role-admission-test).
3. Review the nearest live role TOMLs and both sides of every proposed seam.
4. Draft inside this Markdown file or another `.md` outside `agents/`.
5. Run positive, negative, ambiguity, authority, and handoff cases.
6. Materialize only after the role and runtime posture are accepted.

Never save a candidate `.toml` under `agents/meta/`. Codex recursively discovers TOMLs under `agents/`.

## Candidate worksheet

```text
CANDIDATE_ID:
ONE_LINE_DESCRIPTION:
RECURRING_TRIGGER:
PRIMARY_DECISION_OR_ARTIFACT:
DISTINCT_METHOD:
EVIDENCE_STANDARD:
POSITIVE_CASES:
  1.
  2.
  3.
NEGATIVE_CASES:
  1.
  2.
  3.
NEAREST_ROLES_AND_EXCLUSIONS:
DOWNSTREAM_OWNER_AND_ACCEPTANCE_GATE:
LOCAL_WRITE_SURFACE:
EXTERNAL_OR_HIGH_RISK_ACTIONS:
SENSITIVE_DATA_BOUNDARY:
MODEL_AND_EFFORT_RATIONALE:
TIMEOUT_RATIONALE:
SANDBOX_RATIONALE:
COMPLETION_EVIDENCE:
WHY_AN_EXISTING_ROLE_PLUS_SKILL_IS_INSUFFICIENT:
```

If the last field is weak, do not add the role.

## Runtime TOML skeleton

Copy this block only when intentionally creating `agents/<role_id>.toml`. Replace every placeholder and remove unused optional text.

```toml
name = "<role_id>"
description = "<one routing sentence naming the specialty and canonical value>"
nickname_candidates = ["<candidate one>", "<candidate two>", "<candidate three>"]
background_terminal_max_timeout = <milliseconds>
sandbox_mode = "read-only"
model = "<supported model>"
model_reasoning_effort = "<supported effort>"
developer_instructions = """
You are the <role title>: <one sentence naming the decision or artifact you own>.

Primary use:
- <triggering task family>
- <triggering task family>
- <triggering task family>

Operating rules:

1. Accept a <contract name> naming <mode>; <target and revision/date>; <decision and artifact owners>; <required inputs>; <constraints>; <authority and write surface>; <stop conditions>; <required deliverable>; and <escalation boundary>.
2. <Establish the outcome, definitions, evidence quality, and material unknowns before concluding or changing anything.>
3. <Apply the role-specific ordered method.>
4. <Classify observations, facts, calculations, assumptions, hypotheses, unknowns, confidence, and decisions.>
5. <Define the canonical artifact or compact output packet.>
6. <State verification or acceptance evidence and residual risk.>
7. <Name exact seams with each plausible adjacent role and the handoff gate.>
8. <Begin read-only or limit writes to the assigned local surface; enumerate actions that require exact separate authority.>
9. <Protect credentials, personal data, customer data, confidential evidence, and other sensitive material relevant to this role.>
10. <Return the artifact, source/evidence ledger, verification result, decisions needed, and exact next owner.>

Do not <most tempting unsafe scope expansion>. Do not <most tempting neighboring-role collision>. Do not <most tempting unsupported claim>.
"""
```

Omit `sandbox_mode` only when the effective default is intentionally appropriate and validation confirms it. Do not assume omission means a universal workspace-write posture.

## Prompt design prompts

### Identity

- What singular decision or artifact remains this role's responsibility?
- Is the first sentence concrete enough to exclude a neighboring role?
- Does the description route by task rather than by prestige or broad subject matter?

### Intake

- Which facts materially change scope, method, authority, or success?
- Which mode must be declared to avoid mixing incompatible perspectives?
- Which owner accepts the output?
- Which source or observation date matters?
- Which local and external systems are in scope?

### Method

- What ordered process distinguishes the specialist from a generalist?
- Which evidence is discriminating rather than merely available?
- Which failure modes or confounders must be tested?
- When should the role stop and surface uncertainty?

### Artifact

- Can another owner inspect the output without reading the entire thread?
- Does the packet distinguish evidence, inference, decision, and residual risk?
- Is the output durable when the task is long or consequential?
- Does completion have an observable criterion?

### Boundaries

- Which three roles are most likely to collide with this one?
- What does each neighbor retain?
- Is every “does not own” paired with a positive handoff owner?
- Can the role execute a bounded assignment without seizing the upstream decision?

### Authority and safety

- What begins read-only?
- Which exact writes are intrinsic to the role?
- Which actions require target-specific authorization?
- Which data, credentials, legal/commercial commitments, or production effects require separate control?
- What rollback, disruption limit, or stop condition applies?

### Completion

- Which evidence proves the result?
- Which uncertainty remains?
- Who decides, implements, reviews, operates, publishes, or communicates next?
- Can an interrupted task recover from the artifact and source ledger?

## Compact artifact packet pattern

Use a role-specific vocabulary, but keep a predictable shape:

```text
MODE_AND_SCOPE: <task, target, revision/date, owners, authority>
QUESTION_OR_OUTCOME: <decision or artifact>
INPUTS_AND_EVIDENCE: <sources, quality, freshness, gaps>
METHOD: <ordered approach and assumptions>
FINDINGS_OR_ARTIFACT: <stable, inspectable output>
BOUNDARIES_AND_HANDOFFS: <retained ownership and acceptance gates>
VERIFY: <evidence that proves completion>
RESIDUAL_RISK: <open, accepted, transferred, or unknown>
NEEDS: <authority, evidence, owner, or decision>
NEXT: <exact owner and action>
```

Do not force this generic packet over a mature domain-specific artifact. Its purpose is to expose missing contract fields during drafting.

## Boundary table template

| Adjacent role | Candidate owns | Adjacent role retains | Handoff gate | Negative example |
| --- | --- | --- | --- | --- |
| `<role>` | `<artifact or decision>` | `<artifact or decision>` | `<acceptance condition>` | `<task that must route away>` |

At least one row should cover the most tempting overlap. High-risk roles should also cover the independent security, review, or decision owner where applicable.

## Forward-test template

### Positive case

**Input:** `<realistic task>`

**Expected:** candidate is primary; artifact, authority, and handoff are correct.

### Negative case

**Input:** `<similar but out-of-scope task>`

**Expected:** candidate is excluded; `<other role>` owns `<artifact>`.

### Ambiguity case

**Input:** `<underspecified task>`

**Expected:** clarify first or route to `analyst`; candidate does not invent scope.

### Side-effect case

**Input:** `<task adjacent to production, money, external communication, active testing, or sensitive data>`

**Expected:** candidate identifies the exact gate and does not treat selection as authorization.

### Handoff case

**Input:** `<task requiring staged work>`

**Expected:** one owner produces the prerequisite artifact, a named decision owner accepts it, and the implementation owner starts only after the gate.

## Materialization checklist

- [ ] Role admission test passes.
- [ ] ID is snake case, unique, and matches the intended filename.
- [ ] Description is unique and routing-oriented.
- [ ] Nickname candidates are nonblank and unique after trimming and contain only ASCII letters, digits, spaces, hyphens, and underscores.
- [ ] Timeout fits bounded expected operations.
- [ ] Model and effort exist in the current catalog and have a method-based rationale.
- [ ] Sandbox and task-level write surface are explicit.
- [ ] Intake, method, evidence, artifact, boundaries, safety, and completion are present.
- [ ] Positive, negative, ambiguity, side-effect, and handoff cases pass adversarial review.
- [ ] Reciprocal seams are ready for adjacent TOMLs.
- [ ] Manifest and relevant fixtures are ready to update.
- [ ] No external setup, staging, or commit is being inferred.

## Post-materialization checklist

- [ ] `taplo check agents/*.toml` passes.
- [ ] Filename and `name` match.
- [ ] Runtime and manifest inventories match dynamically.
- [ ] No nested TOML exists under `agents/meta/`.
- [ ] Live inbound and outbound references use current IDs.
- [ ] Model/effort/sandbox and timeout matrix was reviewed.
- [ ] Embedded protocol examples still parse if touched.
- [ ] Markdown links, headings, fences, tables, final newlines, and whitespace pass.
- [ ] Ordinary and strict Codex Doctor both load configuration.
- [ ] Diff scope and staging state match the request.
- [ ] Handoff names exact validation evidence and residual risk.

## Related documents

- [Design guide](DESIGN.md)
- [Editing workflow](EDITING.md)
- [Validation contract](VALIDATION.md)
- [Role manifest](ROLE_MANIFEST.md)
