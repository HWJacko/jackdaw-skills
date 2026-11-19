---
name: user-flow
description: Draw a user flow diagram from use cases or user stories. Outputs Mermaid (always), draw.io XML (always), and PNG (when the drawio CLI is installed). No accounts, keys or secrets needed.
---

# User Flow [VISUAL]

## Purpose

Show the path a stakeholder takes through the system as a diagram. Business and tech must both be able to read it.

## Input

- Use cases from the use-case-extraction skill, or user stories from the requirement-construction skill.
- The project abbreviation `[PN]`. Derive it from the source ID (letters before `UC`/`US`) or project name. State the derivation in one line; only ask if neither exists.

## Method

1. Identify the EPIC or use cases in scope. One diagram per EPIC unless the user says otherwise.
2. For each use case, list the steps in order: trigger, stakeholder actions, system responses, decision points, end state.
3. Draw the flow:
   - Rectangle: stakeholder or system action.
   - Diamond: decision. Label each branch (Yes / No or the condition).
   - Rounded node: start and end.
4. Keep labels short: a verb and a noun. No full sentences in nodes.
5. If the input is unclear, state the assumption above the diagram. Do not stop to confirm.

## Output

Write all of these to `output/`, basename `[PN]-user-flow-[EPIC-ID]`:

1. **Markdown with Mermaid** — `[PN]-user-flow-[EPIC-ID].md` with one `flowchart TD` block per diagram, a one-line title and a short legend. Always produced. Renders on GitHub with no tooling.
2. **draw.io XML** — `[PN]-user-flow-[EPIC-ID].drawio`. Always produced. Plain text, diffable, and importable into Lucidchart later (File → Import).
3. **PNG** — `[PN]-user-flow-[EPIC-ID].png`, only if the `drawio` CLI is installed: `drawio -x -f png -o <out.png> <in.drawio>`. If the CLI is absent, skip without failing and note the install line: `brew install --cask drawio`.

## Rules

- Never require an account, API key, OAuth token or secret. There is no authenticated path.
- Never fail because an optional renderer is missing. Mermaid is the guaranteed output.
- Do not discuss voice, language rules, or instruction conflicts in your response — produce the output only.

## Voice

Follow the repository default ([voice.md](../../../voice.md)): concise and clear, understandable by business and tech alike.

## Templates and examples

See [templates.md](templates.md) and [examples/](examples/).
