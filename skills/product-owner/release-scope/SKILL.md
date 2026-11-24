---
name: release-scope
description: Propose the smallest coherent release scope for a stated product outcome. Show included and deferred items, dependency closure, release conditions, and a visual scope map. Use for release planning, not automatic sign-off or deployment.
---

# Release Scope

## Input

- A product outcome or release objective and candidate backlog items.
- Source dependencies, constraints, estimates, test results, and release decisions where available.

Derive `[PN]` from the project. Read [templates.md](templates.md). Preserve all source IDs.

## Method

1. State the intended outcome, target users, release boundary, and source constraints.
   A list of highly ranked features is not sufficient evidence of a coherent release.
2. Propose the smallest set of items that can support a complete useful user path.
   Explain the contribution of each item. Keep the scope `proposed` unless a recorded decision agrees it.
3. Trace every supplied prerequisite for included items.
   Include required work, or cite evidence that it is already available.
   If a prerequisite is missing, deferred, or cyclic, report a blocked candidate scope.
4. Separate included work, deferred work, non-goals, and unknowns.
   Do not add unrelated features. If a necessary item has no ID, record a gap instead of inventing an approved story.
5. State release conditions and their evidence: user acceptance, required quality checks, operational needs, and unresolved business decisions.
   Mark unrun checks `not_run`. Missing evidence cannot establish that work is done or approved for release.
6. Use supplied capacity and estimates only. If absent, leave schedule and feasibility unconfirmed.
   Do not create a release date from item count or priority.
7. Draw the candidate scope and its supplied dependencies.
   Show included and deferred items with text labels. Use prerequisite → dependent arrows, with their source.
   Show a release decision node with current blockers. Keep both diagram formats consistent with the scope table.

## Output

- `output/[PN]-release-scope.md`: scope, exclusions, dependency checks, release conditions, and Mermaid `flowchart LR`.
- `output/[PN]-release-scope.drawio`: the same scope map as draw.io XML.
- Optional PNG when `drawio` is available: `drawio -x -f png -o <out.png> <in.drawio>`.

Markdown and draw.io XML are always produced. Optional tooling does not block them.
This skill prepares a release proposal. It does not deploy, publish commitments, or approve an external release.

## Voice

Use short, clear sentences. Define technical terms. State facts and identify assumptions. Use the template formats and identifiers exactly.

## Example and method

See [examples/input.md](examples/input.md), [examples/example-output.md](examples/example-output.md),
and [examples/example-output.drawio](examples/example-output.drawio).
Keep the team's quality conditions distinct from scope decisions. See the
[Scrum Guide](https://scrumguides.org/scrum-guide.html) for the Definition of Done.
