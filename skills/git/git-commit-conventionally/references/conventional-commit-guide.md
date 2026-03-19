# Conventional Commit Guide

## Type selection

- `feat`: user-visible functionality added
- `fix`: bug fix or behavior correction
- `refactor`: internal change without external behavior change
- `perf`: performance improvement
- `test`: test-only additions/changes
- `docs`: documentation-only updates
- `chore`: maintenance or tooling work
- `ci`: CI/CD pipeline/workflow changes
- `build`: build/dependency/package changes

## Scope guidance

Use narrow, stable scopes when useful:
- component (`auth`, `billing`, `ui`)
- package/module name
- subsystem (`api`, `worker`, `cli`)

If scope adds noise, omit it.

## Message template

```text
<type>(<scope>): <summary>

- Group A:
  - change detail
  - change detail
- Group B:
  - change detail
- Tests:
  - coverage or validation updates
```

## Quality rubric

- Subject is actionable and specific.
- Bullets are grouped logically, not random file lists.
- Narrative explains intent/outcome, not only mechanics.
- Message reflects the full commit scope without exaggeration.

## Anti-patterns

- Vague subjects: "update stuff", "fix things"
- Giant unstructured bullet list
- Literal `\n` escapes in final commit content
- Missing `git -C <repo>` prefix in commit commands
