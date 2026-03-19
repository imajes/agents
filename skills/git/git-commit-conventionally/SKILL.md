---
name: git-commit-conventionally
description: 'Use when the user asks to commit changes or write a commit message (for
  example: ''commit this'', ''make a commit'', ''write the commit message''). Review
  the current work, then produce a Conventional Commit subject and a structured, GitHub-friendly
  markdown body that explains what changed and why it matters. Run git commands with
  a `git -C /path/to/repo` prefix.'
metadata:
  short-description: Conventional commit workflow with grouped narrative body
---

# Git Conventional Commits

Use this skill whenever the task includes creating a commit.

## Trigger cues

Use for prompts like:
- "commit this"
- "make a commit"
- "commit the changes"
- "create the commit message"

This skill should be the default commit workflow unless the user explicitly requests a different format.

## Output requirements

1. Subject must follow Conventional Commits:
   - `<type>(<scope>): <summary>` or `<type>: <summary>`
2. Ask whether the message should consider staged changes only or the full working tree before inspecting diffs.
3. Review only the scope the user selected before drafting the message.
4. Body must be multi-line markdown bullets grouped by area with clear narrative.
5. No literal `\n` escape text in commit message output.
6. Git commands must use `git -C <repo>` prefix.

## Quick start

1. Ask whether to inspect staged changes only or all current changes in the repo.
2. Inspect the selected scope:
   - staged only: `git -C <repo> diff --cached`
   - all changes: `git -C <repo> status --short` and `git -C <repo> diff`, plus `git -C <repo> diff --cached` if staged changes exist
3. Choose type/scope from changed files and intent.
4. Build a grouped bullet body that explains both the change and its purpose.
5. Commit with clean multiline message (prefer one of the patterns below).

## Commit command patterns

Preferred (clean and low noise):

```bash
git -C <repo> commit -F - <<'MSG'
feat(scope): concise summary

- Area A:
  - meaningful change 1
  - meaningful change 2
- Tests:
  - what was added/updated
MSG
```

Alternative when needed:

```bash
git -C <repo> commit -m "feat(scope): concise summary" -m "- Area: detail\n- Tests: detail"
```

## Grouping guidance

- Group bullets by subsystem or concern.
- Keep bullets specific and outcome-oriented.
- Keep narrative clean: what changed, where, and why it matters.

## Routing boundary

- This skill governs commit-message creation and commit execution style.
- It does not replace implementation/testing workflows.

## Read references only when needed

- Type/scope selection and examples: `references/conventional-commit-guide.md`
- Message quality rubric and anti-patterns: `references/conventional-commit-guide.md#quality-rubric`
