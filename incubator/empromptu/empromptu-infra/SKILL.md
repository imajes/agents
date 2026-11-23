---
name: empromptu-infra
description: AWS and Terraform workflow guidance for infrastructure repositories with
  multi-account concerns, SOC2-aligned controls, and Justfile-driven workflows. Use
  when planning, reviewing, or changing infrastructure code in Empromptu-style repos,
  especially when AGENTS.md, Just, and AWS or Terraform MCP tools should be the primary
  interfaces.
---

# Empromptu Infra

## Defaults

- Prefer clarity and safety over cleverness.
- Avoid guessing about AWS or Terraform semantics when MCP or official docs are available.
- Use the repo's `AGENTS.md`, `Justfile`, and `tools/*` as the primary interface to the infrastructure.

## Session Bootstrap

1. Read every applicable `AGENTS.md`.
2. Skim the root `Justfile` and any `just help` or `just help-module ...` output to learn the supported workflows.
3. Confirm you are in the intended repo root before making or proposing changes.

## MCP Checks

When AWS or Terraform MCP servers are available, verify them before deeper work:

1. Check Terraform MCP availability and confirm expected resources are present.
2. Check AWS API MCP availability with a safe identity or listing command.
3. Check Terraform provider doc search for a simple AWS resource.
4. Confirm local `just` tooling is reachable from the repo root.

If those checks fail unexpectedly, stop and surface the failure instead of reasoning from guesswork.

## Working Rules

- Prefer repo `just` workflows over raw `terraform` or `aws` commands unless there is a specific reason not to.
- Use MCP-backed AWS and Terraform docs as the primary source of truth when present.
- If a requested change would bypass repo guardrails, call that out and propose the safer path.
- Keep customer-workload separation, logging, access control, backups, and encryption concerns explicit when evaluating designs.

## Validation

For non-trivial Terraform changes, run the repo's equivalent of:

1. `just fmt`
2. `just validate-all`
3. `just tflint`
4. `just scan-policy`
5. `just verify`

If the repo uses different target names, use its documented equivalents and say what you ran.
