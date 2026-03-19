# Comby Rewrite Playbook

## Match-template design

- Keep template minimally specific while preserving intent.
- Use placeholders for variable segments.
- Add surrounding anchors to avoid over-match.

## Rollout protocol

1. Match-only run.
2. Manual sample inspection.
3. Rewrite a small directory/file set.
4. Run checks.
5. Continue if clean.

## Example thought process

- Goal: migrate a repeated callback form to promise style.
- Constraint: keep call order and error handling intact.
- Risk: accidental rewrite of similarly named but semantically different blocks.

## Pitfalls

- Placeholder too broad causing unrelated captures.
- Rewrite changes whitespace-sensitive formats unexpectedly.
- Batch size too large to review meaningfully.

## Rollback heuristic

If uncertainty rises during review, stop rollout, revert the current batch, tighten template anchors, rerun on smaller scope.
