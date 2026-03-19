# Difftastic Review Playbook

## Triage template

For each touched file, capture:
- `intent`: what changed
- `type`: mechanical vs semantic vs mixed
- `risk`: low/medium/high
- `verification`: tests or manual checks needed

## Practical sequence

1. Run `difft` per high-priority file.
2. Mark semantic hunks.
3. Inspect call-site and interface changes first.
4. Verify config/flags/defaults changes explicitly.

## When to escalate

Escalate review depth when you see:
- condition/order changes
- retries/timeouts/backoff edits
- security/permission boundaries touched
- state migration or serialization format changes

## Traps

- Assuming formatter-only PRs are no-op.
- Ignoring changed default values hidden in long object literals.
- Missing subtle operator changes (`||` to `??`, `==` to `===`, etc.).
- Trusting visual similarity instead of execution path reasoning.
