# Watchexec Loop Recipes

## Rust

```bash
watchexec --restart --exts rs -- cargo test
```

## JS/TS

```bash
watchexec --restart --exts js,ts -- npm test
```

## Python

```bash
watchexec --restart --exts py -- pytest -q
```

## Mixed stack example

Watch only app-relevant paths to reduce churn:

```bash
watchexec --restart --watch src --watch tests --exts ts,tsx -- npm test
```

## Stability

- Keep command runtime short.
- Avoid watching generated/build output directories.
- Prefer explicit `--watch` paths for large mono-repos.
