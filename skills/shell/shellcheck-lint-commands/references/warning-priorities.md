# ShellCheck Warning Priorities

## High-priority categories

- Unquoted expansions that can split or glob.
- Masked failures (`|| true`, unchecked pipeline status).
- Inconsistent test syntax in POSIX `sh` scripts.
- Command substitution with unsafe parsing assumptions.

## Common fixes

### Quote variables

Before:

```bash
rm -rf $target
```

After:

```bash
rm -rf "$target"
```

### Explicit failure tolerance

Before:

```bash
some_command || true
```

After:

```bash
if ! some_command; then
  echo "some_command failed; continuing intentionally" >&2
fi
```

### Safe reads

```bash
while IFS= read -r line; do
  printf '%s\n' "$line"
done < file.txt
```

## CI patterns

- Start scripts with strict mode appropriate to shell/runtime.
- Keep per-step failures visible in logs.
- Use explicit retries with backoff for flaky network calls.
- Avoid hidden stderr unless a policy requires suppression.
