# Templates — Acceptance Test Design

## Test design

```markdown
# [Project] — Acceptance Tests

Scope: [supplied stories and source versions]
Design decision: proposed, or supported by the supplied decision

## Source criteria

| Criterion ID | Story ID | Revision | Status | Rule and source |
| --- | --- | --- | --- | --- |

## [PN]TC001 — [Case name]

Test revision: 1
Criteria: [qualified IDs and revisions]
Design status: ready or blocked
Source: [criterion and business rule locations]
Preconditions: [known state and environment]
Data: [supplied or clearly synthetic inputs]
Steps: [actions]
Expected: [observable behavior supported by the source]
Limits or blockers: [uncovered behavior, absent rules, or unknown values]
Current result: not_run unless actual result evidence is supplied or obtained

## Open decisions and trace links

[Questions and source → criterion → test links. Add result links only when result records exist.]
```

## Register contract

Use `coverage_version: 1`, a nonempty `scope` string, and `criteria`, `tests`, and `results` lists.
Use the same IDs, revisions, and statuses as the Markdown design.

| Record | Required fields |
| --- | --- |
| Criterion | `id`, `story_id`, `revision`, `status`, `source` |
| Test | `id`, `revision`, `criterion_refs`, `design_status`, `current_result_id`, `source` |
| Result | `id`, `test_id`, `test_revision`, `status`, `environment`, `observed`, `source` |

All fields are nonempty strings except the lists and nullable `current_result_id`.
Criterion status is `agreed`, `proposed`, `conflicting`, or `unknown`.
Each criterion reference has `id` and `revision`. Use one reference per criterion in a case.
Design status is `ready` or `blocked`. Readiness describes the design, not execution.
Result status is `passed`, `failed`, or `blocked`, based on an actual reported execution or attempted execution.
An unrun test has no new result record. Its current result remains null.
Use source-native result IDs, or `[PN]RS###` only when an execution creates new evidence.

Select the current result explicitly for the tested revision. Do not infer it from array order, filename, or a favourable result.
Keep old results as history. If the current result selection is unclear, leave it null and report the gap.
Retain source decision evidence for criterion status. Writing a precise criterion does not establish business agreement.
The map checks this register's consistency. It cannot prove that a supplied result is true or that criteria are complete.
