# Valkey Patterns

## Cache pattern

Use when expensive command output can be reused for a short window.

```bash
key="codex:${TASK}:cache:dependency-graph"
if ! valkey-cli EXISTS "$key" | grep -q '^1$'; then
  value="$(your_expensive_command)"
  valkey-cli SETEX "$key" 600 "$value" >/dev/null
fi
valkey-cli GET "$key"
```

## Lock pattern

Use `SETNX` + expiry for single-run sections.

```bash
lock_key="codex:${TASK}:lock:migration"
if valkey-cli SETNX "$lock_key" "$(date +%s)" | grep -q '^1$'; then
  valkey-cli EXPIRE "$lock_key" 120 >/dev/null
  # critical section
  valkey-cli DEL "$lock_key" >/dev/null
else
  echo "lock busy: $lock_key" >&2
fi
```

## Counter/rate-limit pattern

```bash
key="codex:${TASK}:counter:api-calls"
count="$(valkey-cli INCR "$key")"
valkey-cli EXPIRE "$key" 60 >/dev/null
printf 'count=%s\n' "$count"
```

## Dedup/idempotency token

```bash
token_key="codex:${TASK}:dedup:${PAYLOAD_HASH}"
if valkey-cli SETNX "$token_key" "1" | grep -q '^1$'; then
  valkey-cli EXPIRE "$token_key" 1800 >/dev/null
  # process payload once
else
  echo "duplicate payload skipped" >&2
fi
```

## Cross-agent handoff

Store status payloads with short TTL and deterministic keys:
- `codex:<task>:handoff:<agent-id>:status`
- `codex:<task>:handoff:<agent-id>:result`

## Failure modes

- Missing TTL: stale state and hidden deadlocks.
- Over-broad namespaces: accidental collisions.
- Large blob values: memory bloat and poor key hygiene.
- Silent lock steal behavior: include timestamps or owner ids in lock values.
