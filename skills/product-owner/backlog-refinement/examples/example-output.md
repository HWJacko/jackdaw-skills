# Support Portal — Backlog Refinement

Review status: proposed edits
Source items: SPUS001, SPUS002, SPUS003, SPUS004

## Findings

| Item ID | Source location | Finding | Effect | Proposed action | Decision needed |
| --- | --- | --- | --- | --- | --- |
| SPUS002 | input.md E3 AC1 and E2 | immediate-publication wording omits approval | may permit behavior that contradicts the constraint | retain AC1 and add the supplied approval condition | confirm the wording and pre-approval behavior |
| SPUS002, SPUS003 | input.md E3 | both concern approval | responsibilities could overlap | keep approval enforcement in SPUS003 and link SPUS002 | confirm the boundary |
| SPUS001 | input.md E3 AC1 | expected preview states and failure handling are absent | test scope is unclear | ask which states and failures matter | business expert and team input |
| SPUS004 | input.md E1, E4 | no supplied outcome link | value cannot be compared with SPOC001 work | retain the item and ask for its intended outcome | Product Owner decision |

## Proposed edits

### SPUS002 — proposed

Source use case: SPUC002
As a content editor I want to be able to publish an approved page so that visitors can read it.

AC1: The page becomes public only when administrator approval has been recorded.
This wording applies the existing constraint in input.md E2. It has not been applied to the source backlog.

Unconfirmed rules: what should happen when Publish is selected before approval?
Which preview states and approval failures must the related stories cover?
No queue state, rejection message, or new acceptance criterion is assumed.

## Dependencies and duplicate scope

SPUS002 requires SPUS001 and SPUS003, from input.md E3.
Keep both prerequisites. Do not remove SPUS003 merely because SPUS002 refers to approval.
No replacement story ID or source use case ID has been created.

## Team decisions

| Question | Needed evidence or decision | Owner |
| --- | --- | --- |
| Is the proposed SPUS002 wording accepted? | recorded criterion decision | Product Owner and business expert; people unknown |
| What happens before approval and on failure? | agreed behavior and test scope | business expert and developers; people unknown |
| What outcome does SPUS004 serve? | goal and supporting evidence | Product Owner; person unknown |

Estimates and delivery readiness are not confirmed by this wording review.
