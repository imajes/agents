# SCC Survey Template

## Output interpretation

Capture:
- Top languages by LOC
- Count of files per major language
- Presence of config-heavy vs code-heavy footprint

## Planning mapping

Use language mix to prioritize:
- tooling (`npm`, `cargo`, `go`, `pytest`, etc.)
- likely test command families
- expected linters/formatters

## Example summary format

- "Repo is 65% TypeScript, 20% JSON/YAML, 10% shell, 5% docs."
- "Primary risk surface is TS app/runtime config; shell scripts are secondary."
- "First checks: typecheck + targeted unit tests + workflow YAML review."

## Pitfalls

- High LOC does not equal high change risk.
- Generated code can skew counts.
- Config files can have outsized operational impact despite low LOC.
