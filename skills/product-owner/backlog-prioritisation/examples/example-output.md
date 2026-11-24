# Support Portal — Backlog Prioritisation

Product Goal: let editors publish approved content without developer help.
Order status: proposed
Criteria status: proposed, subject to the supplied approval constraint

## Criteria and evidence

| Criterion or constraint | Status | Source | Limit |
| --- | --- | --- | --- |
| Preserve administrator approval | supplied constraint | input.md E2 | not evidence of implementation |
| Support SPOC001 | supplied goal | input.md E1 | expected benefit per item is not measured |
| Address preview uncertainty | observed interview finding | input.md E4 | small sample; impact is unconfirmed |
| Prefer goal-related work over the colour change | proposed criterion | input.md E1, E4 | Product Owner decision pending |

## Proposed order

| Order or tie | Existing ID | Goal contribution | Prerequisites | Readiness | Reason and evidence |
| --- | --- | --- | --- | --- | --- |
| 1 | SPUS003 | preserves the required approval boundary | none | review needed | prerequisite of SPUS002; input.md E2–E3 |
| 2 | SPUS001 | may reduce uncertainty about the result | none | review needed | supports the goal and precedes SPUS002; input.md E3–E4 |
| 3 | SPUS002 | makes approved content public | SPUS001, SPUS003 | blocked pending criterion clarification | AC1 omits the approval condition; input.md E2–E3 |
| deferred | SPUS004 | no supplied link to SPOC001 | none | unknown | goal contribution is unsupported; input.md E4 |

SPUS003 comes first as a required prerequisite. This does not establish higher direct user benefit than preview work.

## Blockers and unresolved comparisons

Clarify SPUS002 AC1 against the approval constraint before selection for delivery.
Estimates, capacity, and dates are unknown. No scoring calculation is justified by the supplied input.
The source supplies no missing prerequisite ID or cycle. Feasibility and team readiness remain unconfirmed.

## Decisions needed

| Decision | Effect on the order | Owner |
| --- | --- | --- |
| Agree the criteria and proposed order | turns a recommendation into a backlog decision | Product Owner; person unknown |
| Clarify SPUS002 acceptance criteria | resolves a delivery blocker | Product Owner and business expert; people unknown |
| Supply estimates when needed for planning | permits capacity discussion | developers; people unknown |
