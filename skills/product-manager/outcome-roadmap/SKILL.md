---
name: outcome-roadmap
description: Build a visual product roadmap around desired user or business outcomes. Show Now, Next, and Later horizons, evidence, dependencies, and review conditions. Use when sequencing product direction without inventing dates or commitments.
---

# Outcome Roadmap

## Input

- Product goals, intended outcomes, problem frames, or opportunity assessments.
- Supplied priorities, dependencies, capacity, decisions, and dates, when available.

Derive `[PN]` from the source project. Read [templates.md](templates.md).
Keep outcome IDs and references to their source evidence.

## Method

1. State the Product Goal, intended audience, planning scope, and roadmap decision status.
2. Describe each item as a desired change. Link supporting features or tests without treating them as achieved outcomes.
   Use supplied baselines and targets. Keep missing measures `unknown` and proposed targets labelled `proposed`.
3. Propose a Now, Next, and Later sequence from the supplied priorities and evidence.
   These horizons describe relative order. They do not imply calendar dates or guaranteed capacity.
4. Separate technical prerequisites from proposed product sequence and review conditions.
   Cite each dependency. Flag cycles, missing prerequisites, and conflicting commitments instead of hiding them.
5. State what must be learned or agreed before an item advances.
   Record the decision owner when supplied. Keep absent owners, capacity, and dates `unknown`.
6. Draw the three horizons with outcome IDs, short labels, and status.
   Use solid arrows for supplied hard dependencies and dashed arrows for proposed sequence.
   Label every arrow. Do not make an uncertain item look committed through styling.
7. Keep the roadmap table, Mermaid, and draw.io consistent.
   If dated planning is requested, use only supplied dates and durations with their commitment status.
   Ask for missing scheduling information. Keep the undated roadmap useful while those decisions remain open.

## Output

Create `output/outcome-roadmap/` in the working project before writing files.
Use this folder for all files this skill produces, unless the user gives another path.

- `output/outcome-roadmap/[PN]-outcome-roadmap.md`: roadmap table, measures, review conditions, open questions, and Mermaid `flowchart LR`.
- `output/outcome-roadmap/[PN]-outcome-roadmap.drawio`: the same roadmap, with Now, Next, and Later lanes.
- Optional PNG when `drawio` is available: `drawio -x -f png -o <out.png> <in.drawio>`.

Always produce Markdown and draw.io XML. Missing PNG tooling does not block them.
Reuse `[PN]OC###` outcome IDs. Assign a new outcome ID only when the source genuinely adds an outcome.
This skill proposes a roadmap. It does not publish commitments or change external backlogs without instruction.

## Voice

Use short, clear sentences. Define technical terms. State facts and identify assumptions. Use the template formats and identifiers exactly.

## Example

See [examples/input.md](examples/input.md), [examples/example-output.md](examples/example-output.md),
and [examples/example-output.drawio](examples/example-output.drawio).
