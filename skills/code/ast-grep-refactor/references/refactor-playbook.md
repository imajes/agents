# ast-grep Refactor Playbook

## Search-first protocol

1. Write the smallest viable pattern.
2. Run search with language constrained.
3. Inspect at least 10 representative hits before rewrite.
4. Confirm non-target contexts are excluded.

## Rewrite rollout

1. Apply rewrite on one directory.
2. Run lint/typecheck/tests.
3. Evaluate diff shape (semantic vs formatting churn).
4. Roll forward to adjacent directories.

## Pattern design tips

- Prefer explicit anchors around the target expression.
- Use captures for dynamic segments, literals for invariant context.
- Avoid patterns that can match comments/strings unless intentional.

## Example: optional chaining migration

Search:

```bash
sg -p '$OBJ && $OBJ.$METHOD()' -l ts
```

Rewrite:

```bash
sg -p '$OBJ && $OBJ.$METHOD()' --rewrite '$OBJ?.$METHOD()' -l ts
```

Then manually review for side-effect-sensitive `$OBJ` expressions.

## Pitfalls

- Over-match due to missing context tokens.
- Under-match due to overly strict literal assumptions.
- Language mismatch (`-l` omitted or wrong).
- Rewrites that alter evaluation order.

## Validation checklist

- Build succeeds.
- Test suite passes or targeted tests pass.
- No unintended file classes changed.
- Diff count aligns with expected surface area.
