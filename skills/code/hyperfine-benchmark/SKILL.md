---
name: hyperfine-benchmark
description: Use when evaluating performance claims; benchmark comparable before/after
  command variants with `hyperfine` and report measured results. This skill is for
  speed measurement, not functional testing.
metadata:
  short-description: Benchmark protocol for evidence-based perf claims
---

# Hyperfine Benchmark

Use `hyperfine` whenever performance claims need evidence.

## Quick start

```bash
hyperfine --warmup 3 'cmd_before' 'cmd_after'
hyperfine --export-markdown bench.md 'cmd_before' 'cmd_after'
```

## Trigger cues

Use this skill when:
- proposing speed improvements
- choosing between competing command/tool variants
- documenting performance in review notes

## Routing boundary

- Use `hyperfine-benchmark` for timing evidence.
- Use normal test/lint workflows to establish correctness separately.

## Workflow

1. Define comparable command variants.
2. Normalize environment assumptions (cache, data size, CPU noise where possible).
3. Run warmups.
4. Collect results and export artifact.
5. Report medians/variance and command definitions.

## Guardrails

- Do not claim perf gains without measured output.
- Keep commands equivalent in functional behavior before comparing speed.

## Read references only when needed

- Benchmark protocol and reporting template: `references/benchmark-protocol.md`
- Common confounders and mitigation: `references/benchmark-protocol.md#confounders`
