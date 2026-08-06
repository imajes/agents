# Agent Lifecycle Hooks

This directory contains user-level lifecycle hooks intended to work across durable agent
workstreams. Each hook is packaged with its runtime entrypoint, client registration examples,
policy documentation, and tests rather than existing as an opaque command in a settings file.

## Installed Hooks

- [`workstream-bootstrap/`](./workstream-bootstrap/) — on every conversation start, ensure a
  durable workspace is a Git repository, prime Beads when it is already present, automatically
  initialize new/unborn workstreams, and request James's approval before adding Beads to an
  established repository.

Client-specific settings should point into these packages. The canonical implementation remains
here so behavior can be reviewed, tested, and versioned independently of any one agent client.
