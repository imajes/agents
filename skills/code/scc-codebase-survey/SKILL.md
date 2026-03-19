---
name: scc-codebase-survey
description: Use at task start to survey repository composition (language mix, file
  counts, LOC) and shape planning. This skill is for orientation/scoping, not correctness
  or behavior validation.
metadata:
  short-description: Fast repo shape survey to de-risk planning
---

# SCC Codebase Survey

Use `scc` to get fast directional metrics about repository composition.

## Quick start

```bash
scc .
```

## Trigger cues

Use this skill when:
- entering unfamiliar repositories
- estimating breadth of likely impact
- choosing which toolchains/tests to prioritize

## Routing boundary

- Use `scc-codebase-survey` before deep edits in unfamiliar repos.
- Transition to task-specific edit/review/test skills after scope is set.

## Workflow

1. Run `scc` at repo root.
2. Identify dominant languages and file counts.
3. Map likely test/build surfaces from language mix.
4. Use output as orientation, then inspect concrete files.

## Guardrails

- Treat `scc` as planning input, not behavioral proof.
- Always follow with targeted source inspection.

## Read references only when needed

- Survey interpretation templates: `references/survey-template.md`
- Converting language mix into execution plan: `references/survey-template.md#planning-mapping`
