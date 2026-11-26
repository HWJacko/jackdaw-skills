---
name: backlog-refinement
description: Review existing backlog items for unclear scope, duplicates, missing acceptance criteria, dependencies, and unanswered decisions. Produce findings and proposed edits while preserving source IDs. Use before team refinement or planning, not as proof of engineering readiness.
---

# Backlog Refinement

## Input

- Existing backlog items or user stories, with source use cases and product outcomes when available.
- Relevant acceptance criteria, business rules, dependencies, and constraints.

Derive `[PN]` from the source project. Read [templates.md](templates.md).
The Business Analyst requirement-construction skill remains the story-writing route.
This skill reviews existing items and provides proposed edits without requiring another installed skill.

## Method

1. Preserve story IDs, source use case links, Jira keys, and original text references.
   If source links are absent, record the gap. Do not invent a parent use case or outcome.
2. Check that each item states a user need and a useful result.
   Check scope, testable behavior, and acceptance criteria. Separate uncertain business rules from writing defects.
3. Review dependencies and consistency across items.
   Flag duplicate scope, contradictory criteria, missing exception paths, and unsupported assumptions when they affect the task.
4. Propose the smallest edits that resolve clear writing defects.
   Label all changed wording `proposed`. Keep unconfirmed business rules as questions, not new acceptance criteria.
   If a split is needed, describe candidate parts. Let the existing story-writing process assign any new permanent IDs.
5. Identify decisions for the Product Owner, subject matter expert, and developers as appropriate.
   Do not invent estimates, feasibility approval, capacity, or completion evidence.
6. Summarise what remains for team refinement.
   Clear wording does not prove delivery readiness or satisfaction of the team's Definition of Done.
   Produce the local review and proposed edits before asking remaining questions.

## Output

Create `output/backlog-refinement/` in the working project before writing files.
Use this folder for all files this skill produces, unless the user gives another path.

Write `output/backlog-refinement/[PN]-backlog-refinement.md`.
Include findings, source references, proposed edits, dependencies, and unanswered decisions.
Do not overwrite the source stories or external backlog unless that update is requested.

## Voice

Use short, clear sentences. Define technical terms. State facts and identify assumptions. Use the template formats and identifiers exactly.

## Example and method

See [examples/input.md](examples/input.md) and [examples/example-output.md](examples/example-output.md).
The [Scrum Guide](https://scrumguides.org/scrum-guide.html) describes refinement as continuing clarification of backlog work.
