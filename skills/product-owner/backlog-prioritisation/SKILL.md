---
name: backlog-prioritisation
description: Propose an explainable backlog order from a Product Goal, source evidence, constraints, and dependencies. Preserve existing story IDs and identify missing decisions. Use for backlog ordering, not automatic estimates or changes to Jira.
---

# Backlog Prioritisation

## Input

- A Product Goal and backlog items, preferably with existing IDs and source use cases.
- Supplied evidence about value, urgency, constraints, dependencies, and estimates.
- Existing ordering decisions or prioritisation method, when supplied.

Derive `[PN]` from the source project. Read [templates.md](templates.md).
Keep source story IDs and Jira keys unchanged. Do not allocate story IDs to unapproved product ideas.

## Method

1. State the Product Goal, backlog scope, and available decision criteria.
   Keep criteria proposed when the owner has not agreed them.
2. Compare how each item supports the goal. Cite evidence for value and urgency.
   Record unknowns instead of inventing scores, effort, deadlines, or business benefit.
3. Identify prerequisites, duplicate scope, conflicts, and items with insufficient detail.
   Flag missing prerequisite IDs and dependency cycles. Do not hide them through an arbitrary sequence.
4. Propose an order and explain each placement.
   Distinguish business preference from delivery prerequisites. A prerequisite may need earlier delivery without higher direct value.
   If evidence cannot separate items, show the tie and the decision needed.
5. Use a scoring method only when its required values and agreed calculation are supplied.
   Show the calculation and missing inputs. Do not replace unknowns with zero or generated estimates.
6. Explain the effect of changed assumptions and identify decisions for the Product Owner.
   Developers provide delivery estimates. A proposed backlog order is not a Sprint selection or a delivery promise.
7. Produce the recommendation locally. Keep the external backlog unchanged unless its update is explicitly requested.

## Output

Create `output/backlog-prioritisation/` in the working project before writing files.
Use this folder for all files this skill produces, unless the user gives another path.

Write `output/backlog-prioritisation/[PN]-backlog-prioritisation.md`.
Include criteria, source evidence, proposed order, prerequisites, blocked items, ties, and pending decisions.
When dependencies are complex, include a Mermaid dependency view with the same IDs and a source for each arrow.
Do not imply that visual position represents an agreed priority or effort estimate.

## Voice

Use short, clear sentences. Define technical terms. State facts and identify assumptions. Use the template formats and identifiers exactly.

## Example and roles

See [examples/input.md](examples/input.md) and [examples/example-output.md](examples/example-output.md).
See the [Scrum Guide](https://scrumguides.org/scrum-guide.html) for Product Owner accountability and developer sizing responsibility.
