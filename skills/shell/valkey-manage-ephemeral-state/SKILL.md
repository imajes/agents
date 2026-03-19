---
name: valkey-manage-ephemeral-state
description: Use for ephemeral/shared state coordination (cache, queue, lock, counter,
  dedup key, cross-agent handoff). Use this instead of scratch files for short-lived
  state; do not use for durable/auditable file persistence.
metadata:
  short-description: Local Valkey patterns for ephemeral coordination
---

# Valkey Ephemeral State

Use local Valkey (Redis-compatible) as the default primitive for short-lived shared state.

## Quick start

```bash
valkey-cli ping
redis-cli -h 127.0.0.1 -p 6379 ping
```

Use namespaced keys with TTLs:

```bash
valkey-cli SETEX codex:<task>:cache:artifact 900 "<value>"
valkey-cli SETNX codex:<task>:lock:step1 "$(date +%s)"
valkey-cli EXPIRE codex:<task>:lock:step1 120
```

## Trigger cues

Use this skill when you need:
- temporary caching for expensive commands or API calls
- cross-agent or cross-process handoff
- lightweight queues, locks, counters, or idempotency keys

Do not use this skill when the requirement is durable/auditable file persistence.

## Routing boundary

- Choose `valkey-manage-ephemeral-state` for transient coordination state.
- Choose normal files/datastores when persistence beyond task lifetime is required.

## Workflow

1. Choose key namespace before writing any keys.
2. Define TTL by data class (cache, lock, queue marker, dedup token).
3. Write values atomically where possible (`SETEX`, `SETNX`, `INCR`).
4. Validate cleanup behavior by checking expiry and stale key paths.
5. Expose only the minimal key contract needed by collaborating processes.

## Defaults

- Endpoint: `127.0.0.1:6379` (or `VALKEY_URL`/`REDIS_URL` when set)
- Namespace: `codex:<task>:<scope>:<name>`
- TTL rule: default all ephemeral keys to finite expiry

## Read references only when needed

- For pattern-by-pattern recipes and command snippets: `references/patterns.md`
- For failure modes and stale-key mitigation: `references/patterns.md#failure-modes`
