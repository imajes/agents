# SD Safe Rollout

## Recommended rollout sequence

1. Identify target files with ripgrep:

```bash
rg -n 'before' path/
```

2. Apply to one file/group:

```bash
sd 'before' 'after' path/file.txt
```

3. Inspect diff.
4. Run targeted tests/checks.
5. Scale to broader scope.

## Multi-file strategy

For many files, iterate deterministic lists from `rg --files` and avoid shell glob surprises.

## Edge cases

- Replacement text containing `$` or backslashes: verify shell quoting.
- Unintended replacements in generated/vendor files: exclude paths explicitly.
- Case-sensitive variants: treat each variant intentionally.

## Validation checklist

- All intended occurrences changed.
- No unrelated files modified.
- Build/test checks remain green.
