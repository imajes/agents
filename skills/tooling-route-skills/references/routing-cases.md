# Routing Cases

## Case 1: "Replace old API call signature across TS"

- Primary: `ast-grep-refactor`
- Secondary: `difftastic-review`
- Why: syntax-aware call-shape rewrite with semantic review pass.

## Case 2: "Update YAML image tags and env vars"

- Primary: `yq-yaml-edit`
- Secondary: `difftastic-review` (optional for high-risk config)
- Why: deterministic path-based YAML edits.

## Case 3: "Replace literal token in docs and config text"

- Primary: `sd-find-replace`
- Why: lexical substitution only, no syntax semantics required.

## Case 4: "Shell script keeps failing in CI"

- Primary: `shellcheck-lint-commands`
- Secondary: `shell-guard-commands`
- Why: lint diagnosis plus runtime safety normalization.

## Case 5: "Need to coordinate handoff among agents"

- Primary: `valkey-manage-ephemeral-state`
- Why: ephemeral coordination should avoid ad-hoc temporary files.

## Case 6: "Commit this"

- Primary: `git-commit-conventionally`
- Why: commit requests should default to Conventional Commit formatting and `git -C /path/to/repo` command prefixes.

## Misrouting recovery

If outcomes look wrong:
1. Stop rollout.
2. Re-classify operation category.
3. Switch to the next more-specific skill.
4. Re-run on smaller scope.

## Anti-patterns

- Using `sd` for syntax-sensitive code rewrites.
- Using `comby` when `ast-grep` is available and appropriate.
- Manually editing YAML for repeatable nested updates.
- Claiming performance gains without `hyperfine` measurements.
