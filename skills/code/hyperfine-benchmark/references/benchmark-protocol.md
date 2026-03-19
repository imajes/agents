# Benchmark Protocol

## Preflight checklist

- Commands are functionally equivalent.
- Inputs are identical.
- Warmup count is defined.
- Output side effects are controlled.

## Suggested command patterns

```bash
hyperfine --warmup 3 'cmd_before' 'cmd_after'
hyperfine --runs 20 'cmd_a' 'cmd_b'
hyperfine --export-markdown bench.md 'cmd_a' 'cmd_b'
```

## Reporting format

Include:
- exact commands
- run count/warmups
- median time
- relative speedup/slowdown
- known caveats

## Confounders

- file-system cache variance
- network jitter
- background CPU load
- nondeterministic input generation

Mitigate by repeating runs, isolating workloads, and documenting constraints.
