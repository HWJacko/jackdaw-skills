# Templates — Test Coverage Map

## Input register

Use `coverage_version: 1`, `scope`, and `criteria`, `tests`, and `results` lists.

| Record | Fields |
| --- | --- |
| Criterion | `id`, `story_id`, `revision`, `status`, `source` |
| Test | `id`, `revision`, `criterion_refs`, `design_status`, `current_result_id`, `source` |
| Result | `id`, `test_id`, `test_revision`, `status`, `environment`, `observed`, `source` |

Strings are nonempty. `current_result_id` is a string or null.
Criterion status: `agreed`, `proposed`, `conflicting`, or `unknown`.
Each criterion reference has `id` and `revision`. Design status: `ready` or `blocked`.
Reported result status: `passed`, `failed`, or `blocked`.
No execution means no new result record. Use a null current result for an unrun case.
Keep historical results, but select the current one explicitly from source evidence.

## Helper interpretation

`recorded_status` retains the selected source result, or `not_run` for null selection and `unknown` for a missing or mismatched reference.
`current` is false when the design is blocked, a criterion reference is missing or stale, or current result evidence is absent or stale.
An unresolved criterion can have current test evidence, but cannot become verified through that evidence alone.

A criterion is `verified` only when it is agreed, has mapped tests, and every mapped case is current and passed.
All mapped cases are required. List incomplete test design separately; this count cannot prove the cases cover every relevant behavior.
Missing references are gaps. Duplicate IDs or invalid status values are input errors.
The helper checks record consistency. It does not validate the truth of execution records or the completeness of the test design.

```markdown
# [Project] — Test Coverage

Scope: [supplied criteria and versions]
Coverage basis: supplied_criteria_only

## Criteria

| Criterion ID | Story | Decision status | Mapped tests | Current verification | Gaps |
| --- | --- | --- | --- | --- | --- |

## Test evidence

| Test ID | Design state | Selected result | Reported status | Current | Evidence or gap |
| --- | --- | --- | --- | --- | --- |

## Summary and limits

[Declared criteria, mapped criteria, verified criteria, and unassessed scope]

## Coverage map

[Mermaid flowchart and legend]

## Review actions

[Unknown criteria, incomplete cases, missing records, stale evidence, failures, and required decisions]
```

Use safe diagram aliases when criterion IDs contain punctuation. Display native IDs and statuses in labels.
Keep the same nodes, labels, and edges in Mermaid and draw.io. An unrun test has no invented result node.
