---
name: rm-guard-deletions
description: Prevent insecure or overly-destructive file deletion commands, especially
  shell usage involving `rm`, `rm -r`, `rm -f`, `rm -rf`, `find ... -delete`, wildcard
  cleanup, and recursive directory removal. Use whenever Codex is about to compose,
  review, or execute a command that deletes files or directories, particularly for
  cleanup tasks, generated artifacts, caches, temp directories, or user-requested
  bulk removal. Prefer reversible or narrowly-scoped deletion patterns, heavily avoid
  `-f` unless it is truly necessary, and always require explicit escalation before
  executing any forced delete.
---

# Rm Safety Guardrails

Treat file deletion as a high-risk operation. Default to the narrowest removable target, verify the target set before deleting, and do not rely on `-f` to paper over uncertainty.

## Mandatory rules

1. Never add `-f` or `--force` by reflex.
2. Never use `rm -rf` as a generic cleanup shortcut.
3. Always inspect or enumerate targets before deleting them when the command is dynamic, recursive, glob-based, or variable-driven.
4. Prefer the least-destructive tool:
   - Use `rmdir` for empty directories.
   - Use plain `rm` for known files.
   - Use `rm -r` only when recursive removal is actually required.
5. If a path may not exist, check first instead of adding `-f`.
6. If permission failures occur, inspect ownership or permissions first; do not jump straight to forced deletion.
7. If `-f` or `--force` is still necessary, always request explicit escalation before executing the command.

## Safe defaults

- Prefer `rm path` over `rm -f path`.
- Prefer `rm -r dir` over `rm -rf dir` when the directory should exist and interactive prompts are not expected.
- Prefer `test -e path` or `find ... -print` before deletion instead of suppressing errors with `-f`.
- Prefer exact paths over broad globs.
- Prefer staging a move out of the way when reversibility matters more than immediate reclamation.

## Forced delete policy

Treat all of these as forced-delete commands:

- `rm -f ...`
- `rm -rf ...`
- `rm --force ...`
- `find ... -delete` when the match set has not been shown first
- any scripted deletion pattern that suppresses missing-file or permission signals by design

Before running a forced-delete command:

1. Explain why non-forced deletion is insufficient.
2. Show the exact target path or enumerated target set.
3. Request explicit escalation for the command execution.
4. Keep the command as narrow as possible even after escalation.

If the command includes `-f` or `--force`, escalation is mandatory even when the path is inside the writable workspace.

## Review checklist

Before composing or running a delete command, check:

- Is the path absolute or otherwise clearly anchored?
- Could the variable, glob, or substitution expand more broadly than intended?
- Is recursion actually required?
- Can a preflight listing make the deletion auditable?
- Is `-f` being used only to avoid a harmless missing-file error that could be handled another way?
- Does the command touch generated files only, or could it remove source, config, credentials, or user data?

## Preferred patterns

Use patterns like:

```bash
test -e dist/app.js && rm dist/app.js
find build -maxdepth 1 -type f -name '*.tmp' -print
find build -maxdepth 1 -type f -name '*.tmp' -exec rm {} +
rmdir empty-cache-dir
```

Avoid patterns like:

```bash
rm -rf "$TARGET"
rm -f *.log
rm -rf "$WORKDIR"/
find . -delete
```

## Routing boundary

- Apply this skill alongside `$shell-guard-commands` for shell-heavy tasks.
- Use this skill for both authoring and reviewing delete commands.
- This skill governs destructive deletion patterns; it does not replace broader shell linting or general command-chain safety skills.
