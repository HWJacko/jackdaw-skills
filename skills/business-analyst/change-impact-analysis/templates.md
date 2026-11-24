# Templates — Change-Impact Analysis

## Source graph

Use UTF-8 JSON with `trace_version: 1`, `scope`, `nodes`, and `links`.
`scope` describes the supplied documents or snapshot. It is not a claim that every dependency is present.

Each node has `id`, `kind`, `label`, and `source`, all nonempty strings.
Kinds describe the source record, such as evidence, finding, problem, outcome, metric, use_case, story, test, or result.
IDs must be unique. Keep source-native IDs. Qualify local IDs such as `notes.md#E1` when necessary.

Each link has `from`, `to`, `relationship`, `status`, and `source`, all nonempty strings.
Direction is source → dependent. Use `recorded` when a supplied document explicitly records the link.
Use `proposed` for an association that needs review. These statuses do not confirm a business claim or test result.
Missing endpoint IDs remain in the link register as gaps. Do not insert a fictional node to satisfy validation.

```json
{
  "trace_version": 1,
  "scope": "Supplied product and backlog records only",
  "nodes": [
    {"id": "SPMT001", "kind": "metric", "label": "Help-rate definition", "source": "metric.md#SPMT001"},
    {"id": "SPOC001", "kind": "outcome", "label": "Fewer attempts need help", "source": "problem.md#SPOC001"}
  ],
  "links": [
    {"from": "SPMT001", "to": "SPOC001", "relationship": "used to assess", "status": "recorded", "source": "problem.md#Measures"}
  ]
}
```

## Helper result

- `changed_ids`: supplied starting records.
- `review_required`: downstream records reached through recorded links only, excluding changed records.
- `possible_review`: additional records reached through at least one proposed link.
- `gaps`: links with missing endpoint records, including the missing IDs and source.
- `coverage`: `partial` when endpoints are missing; otherwise `supplied_links_only`. Neither value means complete coverage.

The helper identifies review paths. It does not decide whether a change is correct or an outcome has actually changed.

## Report

```markdown
# [Project] — Change Impact

Changed records: [existing IDs]
Proposed change: [description]
Scope and coverage: [supplied material and limits]

## Required review from recorded links

| Record ID | Kind | Link path and source | Review action | Owner |
| --- | --- | --- | --- | --- |

## Possible review

[Proposed links and the evidence needed to confirm them]

## Gaps and limits

[Missing endpoints, missing files, and unrecorded dependencies]

## Impact map

[Mermaid diagram and legend]

## Decisions and next actions

[Pending decisions and targeted review work]
```

Use stable Mermaid-safe aliases for node names when native IDs contain punctuation.
Show the native ID in the label. A gap placeholder is a diagram aid, not a source record.
