---
name: pushover-notify
description: Send focused Pushover notifications through the skill-local `scripts/pushover-notify` helper with validated message limits, optional formatting flags, and conservative API behavior. Use when Codex needs to notify the user through Pushover about task completion, failures, review results, long-running checkpoints, or other high-signal events without using the generic notify hook.
---

# Pushover Notify

Use the local helper instead of hand-writing `curl` each time. It enforces the main Pushover message constraints, reads credentials from environment variables, supports stdin for multiline payloads, and avoids unsafe retry behavior.

## Quick Start

- Ensure `PUSHOVER_APP_TOKEN` and `PUSHOVER_USER_KEY` are set in the environment.
- Send a short message from arguments:
  ```bash
  /Users/james/.codex/skills/pushover-notify/scripts/pushover-notify "Frontend checks passed"
  ```
- Preserve newlines by piping stdin:
  ```bash
  printf 'Build finished\nbranch: %s\nsha: %s\n' "$branch" "$sha" | /Users/james/.codex/skills/pushover-notify/scripts/pushover-notify --title "Codex"
  ```
- Use formatting features only when they add value:
  ```bash
  /Users/james/.codex/skills/pushover-notify/scripts/pushover-notify --html --title "Codex" '<b>CI failed</b><br><i>Check GitHub Actions</i>'
  /Users/james/.codex/skills/pushover-notify/scripts/pushover-notify --monospace --title "Codex" "$(git status --short)"
  ```

## Workflow

1. Build the exact message content first.
2. Prefer stdin when preserving line breaks matters.
3. Set `--title`, `--priority`, `--sound`, `--url`, or `--url-title` only when needed.
4. Use `--html` or `--monospace`, never both.
5. If you want to validate without sending, run `--dry-run`.
6. If the command fails with a 4xx response, fix the payload or credentials instead of retrying.
7. If the command fails with a 5xx response or transport failure, wait at least 5 seconds before retrying.

## Output Expectations

- On success, the helper prints a queued confirmation and the request id, plus remaining quota headers when Pushover returns them.
- On 4xx failure, the helper exits non-zero and prints the API error text. Treat that as non-retryable until the input changes.
- On 5xx or transport failure, the helper exits non-zero and tells you to wait before retrying.

## Reference

- Read [references/api-notes.md](references/api-notes.md) when you need the exact limit values, formatting options, or retry semantics behind the helper.
- Use the implementation at `scripts/pushover-notify` instead of creating an ad hoc `curl` call.
