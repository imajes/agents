---
name: difftastic-review
description: Use for review-time semantic diffing when formatting churn/noise obscures
  logic changes. This skill is for analysis/review, not for applying rewrites.
metadata:
  short-description: Syntax-aware review workflow for noisy diffs
---

# Difftastic Review

Use `difftastic` to recover semantic signal from noisy diffs.

## Quick start

```bash
difft path/to/fileA path/to/fileB
```

## Trigger cues

Use this skill when:
- formatter or import sorting creates large churn
- standard line diffs hide control-flow changes
- review confidence is blocked by whitespace/noise

## Routing boundary

- Use `difftastic-review` to understand change risk.
- Pair with edit/test skills as needed; do not use this as a rewrite mechanism.

## Workflow

1. Start with syntax-aware diff for changed critical files.
2. Classify changes: semantic, mechanical, uncertain.
3. Prioritize uncertain/semantic segments for deeper inspection.
4. Pair with tests or runtime checks for behavior-sensitive code.

## Decision rule

- If change is purely mechanical, mark low risk.
- If semantic edits appear near critical paths, escalate with targeted verification.

## Read references only when needed

- Review triage template and risk labeling: `references/review-playbook.md`
- Common false confidence traps: `references/review-playbook.md#traps`
