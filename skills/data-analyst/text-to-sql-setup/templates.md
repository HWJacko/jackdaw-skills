# Templates — Text-to-SQL Setup

## Status

| Status | Required condition |
| --- | --- |
| `blocked_schema` | The schema model fails the handoff check. Report the blockers. Do not prepare runtime context. |
| `blocked_setup` | The schema passes, but runtime decisions, controls, implementation, or tests remain incomplete. |
| `ready_for_trial` | Required controls and query cases pass in the named test runtime for the stated user scope. |

The helper creates context with `runtime_controls: not_assessed` and `execution_authorised: false`.
Keep these values in the context. Track runtime test results separately in the setup report.
The context describes database meaning. It does not grant database access.

## Handoff check

The model must use version `1` and `ready_for_handoff` for its stated scope.
Blocking questions must be answered. An answer needs text, respondent, date, and linked SME evidence.
Use evidence kind `sme_answer` for a dated SME response.
Table meanings, row grain, and query cases must be confirmed with that evidence.
The helper preserves observed structure and exports only confirmed definitions and approved joins.
It lists unconfirmed definitions and blocked relationships as unavailable.
An approved join must have observed or confirmed status, complete column lists, and SME evidence.
All references must resolve. Referenced questions for a confirmed item must be answered.
The helper checks record consistency. It cannot prove that an SME answer is correct or that the database matches the snapshot.

## Access rules

```markdown
# [Project] — Query Access

Status: draft | Owner: [named access owner or unknown]
Scope: [users and business questions]
Runtime: [selected tool or unknown]

| Control | Required rule | Enforcement point | Owner | Test | Result |
| --- | --- | --- | --- | --- | --- |
| Objects and fields | [permitted objects, output columns, join-only columns] | [database and application] | [owner] | [case ID] | not_run |
| Joins | [approved relationship IDs and all key columns] | [query path] | [owner] | [case ID] | not_run |
| Identity and tenant scope | [trusted identity source and required scope] | [database and application] | [owner] | [case ID] | not_run |
| Read-only execution | [database rights and statement restrictions] | [database and application] | [owner] | [case ID] | not_run |
| Query limits | [timeout, rows, output size, cancellation] | [runtime] | [owner] | [case ID] | not_run |
| Secrets and logs | [secret reference and permitted log fields] | [runtime] | [owner] | [case ID] | not_run |
```

Unknown limits remain `unknown`. Do not copy arbitrary values from an example into a live setup.
Distinguish columns needed inside an authorised query from columns that may be returned to the user.

## Evaluation JSON

Use `evaluation_version: 1`, `project`, `runtime`, and `cases`.
`runtime` names the tool and test environment. Use null until selected.
Each case includes:

- `id`: `[PN]QT###`.
- `kind`: `accept`, `refuse`, or `limit`.
- `question`, `caller_context`, and `parameters`.
- `expected`: permitted behavior and any expected rows or comparison rule.
- `evidence_ids`: model evidence that supports the expected business result.
- `result`: `not_run`, `passed`, or `failed`.
- `result_evidence`: command, environment, and observed result, or null when unrun.

An accepted case needs a confirmed query case and an SME-approved answer or result invariant.
A refusal must be enforced through the runtime, not just described in a prompt.
For aggregate results, check input population, row grain, currency, nulls, duplicates, and tenant scope as applicable.
If timing or output limits are unknown, keep their cases `not_run` and the setup blocked.

## Setup report

```markdown
# [Project] — Text-to-SQL Setup

Status: blocked_setup
Date: [date]
Schema model: [path and inspection date]
Target runtime: unknown
Target database: [dialect and test environment, without credentials]
Intended users and scope: [confirmed scope]

## Prepared files and local changes

[Context, access rules, evaluation cases, and actual implementation changes]

## Open decisions

[Question, owner, and the setup step that it blocks]

## Verification

[Check, command, environment, result, and evidence. Mark unrun checks clearly.]

## Trial decision

[Remaining blockers or the test evidence for ready_for_trial]
```
