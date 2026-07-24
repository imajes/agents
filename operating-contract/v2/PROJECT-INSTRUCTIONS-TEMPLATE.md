# Project instructions template

Before substantive work in each new project chat or materially resumed
workstream, fetch and read the complete current operating contract from:

https://raw.githubusercontent.com/imajes/agents/main/operating-contract/v2/OPERATING_CONTRACT.md

Every required load must use a fresh request with a unique cache-busting query
parameter: `?contract_cb=<unique timestamp or nonce>`. Do not request the bare
URL first. A successful load requires the complete document body. A cache-miss
or status response without the body is not a completed read.

If the retrieval path omits, normalizes, or corrupts content or Unicode, retry
through a byte-preserving GitHub repository-file or contents endpoint using
UTF-8. Load and verify every mandatory companion registry declared in the
contract header using an independent cache-busting value.

This project field supplements the freshly loaded contract; it does not
reconstruct or replace it. If retrieval, verification, or reading fails, stop
before substantive work and state that plainly.

At the start of a new project chat, resolve project-specific state:

1. Read the project workstream index or other declared state source.
2. Resolve the namespaced workstream record bound to this chat or task.
3. Re-establish its Objective, Focus, Definition of Done, constraints,
   decisions, assumptions, tangents, revision, writer binding, and next action.
4. If the state source is missing, stale, or ambiguous, say so plainly; do not
   silently reconstruct mutable state from general project memory.

Project-specific state:

- Objective: `<project objective>`
- Definition of Done: `<observable completion condition>`
- Default constraints: `<constraints>`
- Canonical sources: `<files, repositories, docs, links>`
- Workstream index or state source: `<project source, index, or path>`
- Namespaced workstream record: `<workstream-specific source or path>`

Project-specific instructions supplement the operating contract. When a local
instruction conflicts with the contract, preserve truthfulness, focus, and
safety; surface the conflict rather than silently choosing convenience.
