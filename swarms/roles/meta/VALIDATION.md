# Agent system validation contract

> Status: current reusable validation contract, last reviewed 2026-08-05. Commands assume the repository root is `/Users/james/.codex` and a zsh-compatible shell. The live TOMLs and effective Codex loader are authoritative; a passing documentation check cannot compensate for a runtime-load failure.

## Validation philosophy

Validation is layered so a failure identifies the class of defect:

1. **Repository boundary:** did the patch touch only authorized files and preserve staging state?
2. **Runtime syntax and identity:** can every discovered TOML parse, and does each file identify itself correctly?
3. **Taxonomy consistency:** does the human inventory exactly match the runtime inventory?
4. **Contract invariants:** are models, efforts, sandboxes, references, and embedded examples coherent?
5. **Documentation integrity:** do links, headings, fences, tables, whitespace, and freshness notices remain sound?
6. **Real loader:** does Codex load ordinary and strict configuration?

Run the narrowest relevant checks during editing and the complete affected set before handoff. Record exact commands and outcomes.

## Current baseline

As of 2026-08-05:

- 32 top-level runtime role TOMLs exist.
- `commander`, `lieutenant`, and `chief` are the only Ultra roles.
- The manifest inventory matches all 32 runtime IDs.
- `agents/meta/` is Markdown-only and not ignored.
- The future router is documentation only.

Counts and exact matrices are snapshots, not eternal constants. A deliberate taxonomy change updates the expected baseline and explains why.

## 1. Repository and staging boundary

Inspect the complete tree before and after the change:

```sh
git -C /Users/james/.codex status --short --branch
git -C /Users/james/.codex diff --name-status
git -C /Users/james/.codex diff --cached --name-status
```

Expected:

- every touched file belongs to the declared scope;
- unrelated pre-existing files retain their prior state;
- no agent or handbook file is staged unless James explicitly requested staging;
- untracked runtime TOMLs are included in later checks.

The current working tree can legitimately be dirty. “Clean” is not the invariant; preserved ownership and intentional scope are.

## 2. TOML syntax

```sh
taplo check agents/*.toml
```

Expected: zero parse or schema-independent TOML errors for every top-level runtime role.

A top-level glob is intentional. Runtime roles belong at the top level; the separate meta check catches accidental nested TOMLs.

## 3. Runtime identity

Run this from the repository root:

```zsh
failed=0
for file in agents/*.toml; do
  expected="$(basename "$file" .toml)"
  actual="$(sed -n 's/^name = "\([^"]*\)"$/\1/p' "$file")"
  if [[ -z "$actual" || "$actual" != "$expected" ]]; then
    print -r -- "$file: expected name=$expected, found name=${actual:-<missing>}"
    failed=1
  fi
done
(( failed == 0 ))
```

Expected: no output and exit zero.

Also inspect required metadata and duplicates:

```zsh
for file in agents/*.toml; do
  for field in name description nickname_candidates background_terminal_max_timeout model model_reasoning_effort developer_instructions; do
    taplo get -f "$file" "$field" >/dev/null ||
      print -r -- "$file: missing or unreadable $field"
  done
done

for field in name description; do
  for file in agents/*.toml; do
    taplo get -s -f "$file" "$field"
  done | sort | uniq -d | sed "s/^/$field duplicate: /"
done
```

Expected: no output. Codex Doctor remains the authoritative check for loader normalization rules such as nonempty, trimmed, unique nickname candidates containing only ASCII letters, digits, spaces, hyphens, and underscores.

## 4. Runtime inventory versus manifest

```zsh
comm -3 \
  <(for file in agents/*.toml; do basename "$file" .toml; done | sort) \
  <(sed -n '/^## Role inventory$/,/^## Specialist decision routing$/p' agents/meta/ROLE_MANIFEST.md |
      sed -n 's/^| `\([^`]*\)` |.*/\1/p' |
      sort)
```

Expected: no output. A left-only ID exists at runtime but not in the manifest; a right-only ID is documented but not loadable.

The command is dynamic and should stay authoritative after intentional additions or removals. Report the new count separately:

```sh
find agents -maxdepth 1 -type f -name '*.toml' | wc -l
```

## 5. Meta discovery safety

```sh
find agents/meta -type f ! -name '*.md' -print
find agents/meta -type f -name '*.toml' -print
git -C /Users/james/.codex check-ignore -v agents/meta/README.md agents/meta/ROLE_MANIFEST.md
```

Expected:

- both `find` commands print nothing;
- `git check-ignore` prints nothing and exits nonzero because the files are versionable.

If a non-Markdown artifact is genuinely needed, place it outside `agents/` or document and validate a runtime-safe location. Do not weaken this invariant casually.

## 6. Live role references

Search current runtime contracts for retired IDs:

```sh
rg -n '`(conductor|concertmaster|principal|publicist|producer|operator|quartermaster|steward|herald|watcher|explorer|testsmith|scribe|worker)`' agents/*.toml
```

Expected: no output.

The manifest rename ledger and dated research intentionally preserve historical IDs. The validation command itself also lists them intentionally; do not apply this search indiscriminately to all documentation.

For any new role, search its inbound and outbound references and inspect every seam:

```sh
rg -n '`<role_id>`|<role_id>\.toml|name = "<role_id>"' agents
```

Replace `<role_id>` before running. Confirm that references are intentional, reciprocal where required, and use the current ID.

## 7. Model, effort, timeout, and sandbox review

```sh
rg -n '^(name|background_terminal_max_timeout|sandbox_mode|model|model_reasoning_effort) = ' agents/*.toml
```

Review the resulting matrix against [AGT-007](DECISIONS.md#agt-007--model-effort-and-sandbox-posture-follow-the-method):

- every model and effort exists in the current catalog;
- Ultra is used only by the accepted command roles unless a new system-wide decision says otherwise;
- read-only and workspace-write behavior match the role's artifact and independence needs;
- timeout changes have a bounded operational rationale.

Do not infer the effective global sandbox from an omitted per-role key; validate through the loaded configuration.

## 8. Embedded JSON examples

The manifest contains protocol examples that must remain parseable:

```sh
node <<'NODE'
const fs = require("fs");
const file = "agents/meta/ROLE_MANIFEST.md";
const text = fs.readFileSync(file, "utf8");
const blocks = [...text.matchAll(/```json\n([\s\S]*?)\n```/g)];
if (blocks.length === 0) throw new Error("no JSON fences found");
for (const [index, match] of blocks.entries()) {
  try {
    JSON.parse(match[1]);
  } catch (error) {
    throw new Error(`JSON block ${index + 1}: ${error.message}`);
  }
}
console.log(`${blocks.length} JSON blocks parsed`);
NODE
```

Expected at the current baseline: `3 JSON blocks parsed`.

If the count intentionally changes, update the baseline and inspect the protocol explanation, not only the parser result.

## 9. Markdown integrity

The following read-only Node check validates local relative files and heading anchors, final newlines, trailing whitespace, balanced backtick fences, duplicate headings, and table widths within every file under `agents/meta/`:

```sh
node <<'NODE'
const fs = require("fs");
const path = require("path");

const root = path.resolve("agents/meta");
const files = [];
function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full);
    else if (entry.isFile() && entry.name.endsWith(".md")) files.push(full);
  }
}
walk(root);

const failures = [];
const cleanText = new Map();
const anchors = new Map();
for (const file of files) {
  const text = fs.readFileSync(file, "utf8");
  const relative = path.relative(process.cwd(), file);
  if (!text.endsWith("\n")) failures.push(`${relative}: missing final newline`);

  const lines = text.split("\n");
  const cleanLines = [];
  const headingCounts = new Map();
  const headingAnchors = new Set();
  let fence = null;
  let tableWidth = null;
  for (let index = 0; index < lines.length; index += 1) {
    const line = lines[index];
    if (/[ \t]+$/.test(line)) failures.push(`${relative}:${index + 1}: trailing whitespace`);

    const fenceMatch = line.match(/^(`{3,})(.*)$/);
    if (fenceMatch) {
      if (fence === null) fence = fenceMatch[1].length;
      else if (fenceMatch[1].length >= fence) fence = null;
      tableWidth = null;
      continue;
    }
    if (fence !== null) continue;
    cleanLines.push(line);

    const heading = line.match(/^#{1,6}\s+(.+?)\s*#*\s*$/);
    if (heading) {
      const base = heading[1]
        .toLowerCase()
        .trim()
        .replace(/<[^>]+>/g, "")
        .replace(/[^\p{L}\p{N}\s-]/gu, "")
        .replace(/ /g, "-");
      const count = headingCounts.get(base) || 0;
      const anchor = count === 0 ? base : `${base}-${count}`;
      if (count > 0) failures.push(`${relative}:${index + 1}: duplicate heading anchor "${base}"`);
      headingCounts.set(base, count + 1);
      headingAnchors.add(anchor);
    }

    if (/^\|.*\|\s*$/.test(line)) {
      const width = (line.match(/(?<!\\)\|/g) || []).length;
      if (tableWidth === null) tableWidth = width;
      else if (width !== tableWidth) {
        failures.push(`${relative}:${index + 1}: table width ${width - 1}, expected ${tableWidth - 1}`);
      }
    } else {
      tableWidth = null;
    }
  }
  if (fence !== null) failures.push(`${relative}: unclosed backtick fence`);
  cleanText.set(file, cleanLines.join("\n"));
  anchors.set(file, headingAnchors);
}

for (const file of files) {
  const relative = path.relative(process.cwd(), file);
  for (const match of cleanText.get(file).matchAll(/!?\[[^\]]*]\(([^)]+)\)/g)) {
    let raw = match[1].trim();
    if (raw.startsWith("<") && raw.endsWith(">")) raw = raw.slice(1, -1);
    if (/^[a-z][a-z0-9+.-]*:/i.test(raw) || raw.startsWith("/")) continue;

    const hashIndex = raw.indexOf("#");
    const targetPart = (hashIndex >= 0 ? raw.slice(0, hashIndex) : raw).split("?", 1)[0];
    const fragment = hashIndex >= 0 ? decodeURIComponent(raw.slice(hashIndex + 1)) : "";
    const resolved = targetPart
      ? path.resolve(path.dirname(file), decodeURIComponent(targetPart))
      : path.resolve(file);

    if (!fs.existsSync(resolved)) {
      failures.push(`${relative}: broken link "${raw}"`);
      continue;
    }
    if (fragment && fs.statSync(resolved).isFile() && resolved.endsWith(".md")) {
      const targetAnchors = anchors.get(resolved);
      if (!targetAnchors || !targetAnchors.has(fragment)) {
        failures.push(`${relative}: broken heading anchor "${raw}"`);
      }
    }
  }
}

if (failures.length) {
  console.error(failures.join("\n"));
  process.exit(1);
}
console.log(`${files.length} Markdown files passed structural checks`);
NODE
```

Expected: one success line and exit zero.

Some restricted shells cannot create the temporary file used by a here-document. In that case, pass the unchanged JavaScript body to an available Node REPL or `node -e` invocation; do not skip the check.

This is a structural check, not a rendering engine. Manually inspect:

- tables with the intended number of columns;
- list nesting and blank lines;
- link labels and anchor destinations;
- status/freshness notices;
- diagrams and code blocks at ordinary rendered width;
- accidental duplication of manifest content.

## 10. Whitespace and patch hygiene

```sh
git -C /Users/james/.codex diff --check -- agents README.md
rg -n '[ \t]+$' agents/meta -g '*.md'
```

Expected: no output.

Because untracked files are not included in ordinary `git diff --check`, the explicit Markdown scan is required. The structural check above also verifies final newlines.

## 11. Real Codex configuration load

Run both modes:

```sh
codex doctor
codex --strict-config doctor
```

Expected invariant: both reports contain `Configuration [ok] config loaded` with no agent-config startup warning.

The overall doctor exit may still be nonzero for unrelated environmental checks. At the 2026-08-05 baseline, the noninteractive `TERM=dumb` check caused a failure and rollout/state parity remained a pre-existing warning. Report those separately; do not convert “configuration loaded” into “every doctor check passed.”

## 12. Final staging and scope audit

```sh
git -C /Users/james/.codex diff --name-status -- agents README.md
git -C /Users/james/.codex diff --cached --name-status -- agents README.md
git -C /Users/james/.codex status --short -- agents README.md
```

Expected:

- the unstaged/untracked list matches the declared patch;
- the cached list is empty unless staging was explicitly requested;
- no unrelated file was absorbed into the handoff.

## Failure interpretation

| Failure | Likely defect | Response |
| --- | --- | --- |
| `taplo check` fails | Invalid TOML syntax | Fix before any semantic review |
| Filename/name mismatch | Runtime identity or rename migration defect | Repair the file and all live references |
| Inventory comparison emits IDs | Runtime/manifest drift | Confirm intended role set and reconcile both surfaces |
| Nested TOML found | Accidental role discovery risk | Move it outside `agents/meta` |
| Retired ID found in live TOML | Incomplete rename or stale handoff | Replace with the current owner and inspect reciprocity |
| JSON block fails | Broken continuity protocol example | Repair the example and re-review surrounding semantics |
| Local link fails | Moved, renamed, or misspelled documentation | Fix target or link; do not leave a stale navigation path |
| Duplicate heading | Unstable or ambiguous anchor | Rename the narrower heading |
| Doctor config load fails | Invalid or incompatible effective configuration | Treat as blocking; inspect exact loader diagnostics |
| Cached diff appears unexpectedly | Unauthorized staging | Stop and preserve ownership before proceeding |
| Only unrelated doctor check fails | Environmental or pre-existing health issue | Report separately with exact evidence; do not misstate config status |

## Validation report template

```text
REVISION: <HEAD and working-tree scope>
TOML: <count checked; result>
IDENTITY: <filename/name/required-field result>
INVENTORY: <runtime count; manifest comparison result>
META_SAFETY: <Markdown-only and ignore result>
REFERENCES: <retired/new role search result>
PROTOCOL: <embedded JSON result when applicable>
MARKDOWN: <links/headings/fences/whitespace result>
LOADER: <ordinary and strict config result; unrelated doctor diagnostics separated>
DIFF: <scope, diff-check, and staging result>
OPEN: <remaining risk or none>
```
