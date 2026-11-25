# Support Portal — Acceptance Tests

Scope: supplied criteria at revision 1. Design decision: proposed.

## Source criteria

| Criterion ID | Story ID | Revision | Status | Rule and source |
| --- | --- | --- | --- | --- |
| SPUS001.AC1 | SPUS001 | 1 | agreed | title required; input.md current criteria |
| SPUS002.AC1 | SPUS002 | 1 | conflicting | approval versus immediate publication; input.md current criteria |

## SPTC001 — Reject an empty title

Test revision: 1
Criteria: SPUS001.AC1 revision 1
Design status: ready
Source: input.md SPUS001.AC1
Preconditions: a draft can be submitted to the title validator.
Data: a synthetic draft with an empty title.
Steps: submit the draft to the validator.
Expected: the validator rejects the empty title.
Limits or blockers: this does not check whitespace-only titles, validation messages, or the target application.
Current result: supplied synthetic SPRS001; passed in the named fixture. No new execution is claimed.

## SPTC002 — Publication before approval

Test revision: 1
Criteria: SPUS002.AC1 revision 1
Design status: blocked
Source: input.md conflicting publication rules
Preconditions: a draft without approval; target environment unknown.
Data: a synthetic unapproved draft.
Steps: propose a case that selects Publish before approval.
Expected: unresolved until the owner decides the conflicting rule.
Limits or blockers: no queue state, rejection message, or publication behavior has been invented.
Current result: not_run. No result ID is allocated.

## Open decisions and trace links

Resolve SPUS002.AC1 before accepting an execution oracle for SPTC002.
SPUS001 → SPUS001.AC1 → SPTC001 → SPRS001 is recorded in the supplied sources.
SPUS002 → SPUS002.AC1 → SPTC002 is a test-design link. It has no execution result.
