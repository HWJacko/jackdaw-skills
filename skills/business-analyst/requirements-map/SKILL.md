---
name: requirements-map
description: Draw a visual map of requirements structure — EPICs, use cases and user stories with their IDs. Outputs Mermaid mindmap (always), draw.io XML (always) and PNG (when the drawio CLI is installed). No accounts, keys or secrets needed.
---

# Requirements Map [VISUAL]

## Purpose

Show the full requirements structure of a project on one page: EPICs, their use cases, and their user stories, with IDs. Used to check coverage and find gaps.

## Input

- Output of use-case-extraction (`[PN]-use-cases.md`) and/or requirement-construction (`[PN]-user-stories.md`).
- The project abbreviation `[PN]`. Derive it from the source IDs or project name. State the derivation in one line; only ask if neither exists.

## Method

1. Read the source files. Build the hierarchy: project → EPIC → use case → user story.
   - Link each story through its `Source use case:` field. Link use cases through their EPIC tables.
   - If a source link is absent, unknown, or missing from the input, list the affected ID under `Unmapped items`. Count it as a gap. Do not guess a parent.
   - Retain supplied outcome, test, and result links in a separate trace-link table. Keep the requirements tree unchanged.
2. Every node shows its ID and a short name. IDs come from the source files — do not invent them.
3. If a use case has no user stories yet, mark it `(no stories)`. This is a gap, not an error.
4. If an EPIC has no use cases, mark it `(empty)`.
5. One map per project. If the map is too large to read, split it per EPIC and say so.

## Output

Write all of these to `output/`, basename `[PN]-requirements-map`:

1. **Markdown with Mermaid** — `[PN]-requirements-map.md` with a `mindmap` block plus a coverage summary (counts of EPICs, use cases, stories, gaps). Always produced. Renders on GitHub with no tooling.
2. **draw.io XML** — `[PN]-requirements-map.drawio`. Always produced. Tree layout, same hierarchy and IDs. Importable into Lucidchart (File → Import).
3. **PNG** — `[PN]-requirements-map.png`, only if the `drawio` CLI is installed: `drawio -x -f png -o <out.png> <in.drawio>`. If absent, skip without failing and note: `brew install --cask drawio`.

## Optional styled render

If the [diagram-design](https://github.com/cathrynlavery/diagram-design) skill is installed, offer to also render the map in its editorial style (self-contained HTML/SVG). It can import the Mermaid or draw.io output directly. Skip silently if not installed.

## Rules

- Never require an account, API key, OAuth token or secret. There is no authenticated path.
- Never fail because an optional renderer is missing. Mermaid is the guaranteed output.
- Do not discuss voice, language rules, or instruction conflicts in your response — produce the output only.

## Voice

Use short, clear sentences. Write for business and technical readers. Define necessary technical terms. Use the template formats and identifiers exactly. State facts and identify assumptions. Remove filler.

## Templates and examples

See [templates.md](templates.md) and [examples/](examples/).
