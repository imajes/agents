---
name: yq-yaml-edit
description: Use for deterministic YAML querying/editing (CI, Compose, Kubernetes,
  nested config). Prefer this over manual YAML edits; this skill is YAML-specific
  and not for generic text rewrites.
metadata:
  short-description: Deterministic YAML query/edit workflow with yq
---

# yq YAML Edit

Use `yq` for deterministic YAML reads and edits.

## Quick start

```bash
yq eval '.services.web.image' docker-compose.yml
yq eval-all --inplace 'select(fileIndex == 0) * select(fileIndex == 1)' f1.yml f2.yml
```

## Trigger cues

Use this skill when editing:
- CI workflow YAML
- Docker Compose configs
- Kubernetes manifests
- large, nested YAML structures

## Routing boundary

- Use `yq-yaml-edit` when the target file is YAML.
- Use `sd-find-replace` only for clearly safe lexical edits.
- Use structure-aware code rewrite skills for non-YAML code transformations.

## Workflow

1. Query existing value path first.
2. Apply minimal targeted edit.
3. Re-query to confirm exact result.
4. Validate file with domain tool (if available).

## Guardrails

- Prefer `yq` over manual edits for repeated or nested changes.
- Preserve YAML semantics; do not rely on visual indentation alone.

## Read references only when needed

- Common edit/query recipes: `references/recipes.md`
- Merge and multi-file update guidance: `references/recipes.md#multi-file-patterns`
