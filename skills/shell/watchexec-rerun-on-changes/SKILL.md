---
name: watchexec-rerun-on-changes
description: Use when fast edit-feedback loops are needed; rerun tests/lints/builds
  on file changes with `watchexec`. Prefer this for repeated local iteration, not
  one-off command execution.
metadata:
  short-description: Watch-loop recipes for faster edit/verify cycles
---

# Watchexec Loop

Use `watchexec` to maintain rapid edit-check loops.

## Quick start

```bash
watchexec --restart --exts rs -- cargo test
watchexec --restart --exts js,ts -- npm test
```

## Trigger cues

Use this skill when:
- editing code in short iterative cycles
- repeatedly rerunning tests/lints/builds manually
- needing faster feedback on correctness regressions

## Routing boundary

- Use `watchexec-rerun-on-changes` for continuous iteration loops.
- Use direct command execution for single-run checks.

## Workflow

1. Choose minimal watched extension/path set.
2. Pick one command with fast, deterministic feedback.
3. Use `--restart` for current-state validation.
4. Tune scope to reduce noisy reruns.

## Guardrails

- Avoid overly broad watch roots in large repos.
- Prefer one stable watch loop over many overlapping loops.

## Read references only when needed

- Command recipes for common stacks: `references/loop-recipes.md`
- Noise reduction and loop stability guidance: `references/loop-recipes.md#stability`
