# Templates — Schema Map

## IDs

| Item | Format | Example |
| --- | --- | --- |
| Table or view | `[PN]TB###` | `SATB001` |
| Relationship | `[PN]RL###` | `SARL001` |
| Evidence | `[PN]EV###` | `SAEV001` |
| SME question | `[PN]Q###` | `SAQ001` |

IDs remain stable during review. Database names remain unchanged in the model.

## Claim status

| Status | Meaning |
| --- | --- |
| `observed` | Directly shown by the cited metadata, file, or authorised data check. Limited to that source and scope. |
| `assumed` | A proposed meaning or relationship. Cite its basis and the question that can confirm it. |
| `confirmed` | Explicitly confirmed for the stated scope. Cite the SME response and any required technical check. |
| `rejected` | A prior proposal was rejected. Keep the reason and evidence. |
| `unknown` | Evidence is insufficient. Use null for the claim text and link a question. |

Observed structure and confirmed business meaning are separate facts. Do not replace one with the other.

## JSON model contract

Use UTF-8 JSON. Set `model_version` to `1`. Include these fields:

| Field | Content |
| --- | --- |
| `project` | `name`, `abbreviation` |
| `inspection` | `date`, `dialect`, `source_mode` (`live_metadata` or `supplied_schema`), `scope`, `limitations` |
| `evidence` | List of `id`, `kind`, `source`, `detail`. Use file lines, catalogue query references, or dated SME answers. No credentials. |
| `tables` | List of `id`, `schema`, `name`, `kind`, `evidence_ids`, `columns`, `keys`, `meaning`, `grain` |
| `relationships` | List of `id`, `from_table_id`, `from_columns`, `to_table_id`, `to_columns`, `status`, `evidence_ids`, `question_ids`, `cardinality`, `join_use` |
| `definitions` | Business terms or field rules: `subject`, `claim`. Use exact object names in `subject`. |
| `questions` | SME question records defined below |
| `query_cases` | List of `question` and `expected_behavior` claim. Include joins, filters, calculation, and result grain. |
| `readiness` | `status`, `scope`, `blocking_question_ids`, `runtime_controls` |

Use an empty list when no items are known. Do not fill absent metadata with invented defaults.
`schema` may be null when the source does not supply one. `kind` is `table` or `view`.
Each column has `name`, `data_type`, `nullable`, and `evidence_ids`. `nullable` may be null if unknown.
Add source-backed defaults or generated-column details when relevant.
Each key has `kind` (`primary` or `unique`), ordered `columns`, and `evidence_ids`.
Keep expression indexes separate from ordinary column keys when encountered.

`meaning`, `grain`, each definition's `claim`, and each query case's `expected_behavior` use:

```json
{
  "text": "One row may represent one customer within one tenant.",
  "status": "assumed",
  "evidence_ids": ["SAEV001"],
  "question_ids": ["SAQ002"]
}
```

Relationship column lists have matching positions and lengths. Pair columns by position.
`cardinality` is `many-to-one`, `one-to-one`, `many-to-many`, or `unknown` from the source table to the target.
For an observed relationship, this describes the declared structure, not a completed data-quality check.
For an assumed relationship, cardinality is also assumed. Use `unknown` if there is no basis for it.
`join_use` is `blocked` or `approved`. Preserve rejected relationships with `join_use: blocked`.

Each question has:

- `id`, `priority` (`blocking` or `follow_up`), and `subjects` (table or relationship IDs).
- `question`, `why_it_matters`, `needed_evidence`, and `evidence_ids`.
- `status` (`open`, `answered`, or `deferred`), `answer`, `answered_by`, and `answered_on`.

Use null for unanswered answer fields. An answered question needs a response, respondent, date, and evidence.
Use `YYYY-MM-DD` for `answered_on`.
New answers also become evidence records with `kind: sme_answer`.
An answer that requires a further check does not confirm the affected claim yet.
`readiness.status` is `needs_confirmation` or `ready_for_handoff`.
`blocking_question_ids` contains all blocking questions that remain unresolved, including deferred questions.
`readiness.runtime_controls` is `not_assessed`. The future runtime skill must establish them.

## Schema report

```markdown
# [Project] — Assumed Schema Map

Date: [date] | Project: [PN] | Handoff: needs_confirmation

## Source and limits

[Dialect, files or tool, scope, visibility, and checks not performed]

## Tables and row grain

| ID | Database object | Observed structure | Proposed meaning and grain | Status | Evidence | Questions |
| --- | --- | --- | --- | --- | --- | --- |

## Relationships

| ID | Ordered source columns | Ordered target columns | Cardinality | Status | Query use | Evidence | Questions |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Business meanings and query cases

[Measures, dates, status rules, access boundaries, and expected answers to confirm]

## Handoff decision

[Open blocking question IDs, limitations, and the decisions required]
Runtime controls: not_assessed
```

## SME questions

```markdown
# [Project] — SME Questions

Handoff: needs_confirmation

## [PN]Q001 — [Decision]

Priority: blocking | Subjects: [IDs] | Status: open
Evidence: [IDs]
Question: [Specific decision the SME must make]
Why it matters: [Effect on a join, calculation, filter, access rule, or expected result]
Needed evidence: [Definition, source rule, or worked query example]
Answer: pending
Answered by: pending
Answered on: pending
```

This file is a review copy of the JSON questions. Keep both outputs consistent after answers arrive.
