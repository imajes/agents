# Shell Hygiene Rules and Examples

## Anti-pattern: hidden failure

Before:

```bash
some_command 2>/dev/null || true
```

After:

```bash
if ! some_command; then
  echo "some_command failed; continuing intentionally" >&2
fi
```

## Anti-pattern: useless cat

Before:

```bash
cat file.txt | command
```

After:

```bash
command < file.txt
```

## CI-hardened patterns

- Surface all failed commands in logs.
- Use explicit retries instead of silent masking.
- Keep stderr unless a policy requires suppression and documents why.
- Keep command behavior readable for reviewers.
