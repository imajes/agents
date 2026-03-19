---
name: markdown-modernize
description: Light-touch Markdown cleanup that improves readability, structure, and
  formatting without changing meaning. Use when asked to reformat existing Markdown,
  modernize headings or lists, fix broken fences or spacing, or make documentation
  easier to scan while preserving content fidelity.
---

# Markdown Modernize

## Workflow

1. Read applicable `AGENTS.md` files before editing.
2. Preserve meaning, factual claims, links, and intent. Treat this as editorial cleanup, not a rewrite.
3. Normalize only what is safe:
   - heading levels and heading spacing
   - list indentation, numbering, and blank lines
   - code fences and language tags when obvious
   - blockquotes, tables, and task lists when clearly malformed or inconsistent
4. Keep the smallest diff that materially improves scanability.
5. Stop and ask if a change would require paraphrasing, deleting ambiguous text, or inventing missing structure.

## Guardrails

- Do not add new claims, examples, or conclusions.
- Do not change tone unless the user explicitly asks for a stylistic rewrite.
- Preserve anchor targets, reference-style links, and fenced code contents unless they are clearly broken.
- Avoid reflowing generated sections or large code blocks unless the file is invalid as written.

## Validation

- Re-read the rendered structure after editing.
- Check for unbalanced fences, accidental list renumbering, and broken tables.
- Call out any awkward source text that had to remain in place to preserve fidelity.
