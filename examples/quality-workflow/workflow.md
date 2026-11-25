# Evidence Check — Full Worked Example

This is an author-run exercise using the repository skills and synthetic sources in `input.md`.
It is not an independent agent evaluation or a target-application acceptance run.
The programmatic checks verify source links, result consistency, coverage rules, and the named SQL fixture only.

## 1. Research synthesis

| Observation | Participant | Source | Observed note |
| --- | --- | --- | --- |
| ECOB001 | P1 | input.md ECEV001 | Cannot identify the denominator population |
| ECOB002 | P2 | input.md ECEV002 | Cannot explain unknown help flags |

ECRF001: these two participants could not explain the report population. This is an interpreted finding.
Both observations support it. The sample is two people; recruitment and wider prevalence are unknown.
No customer quote, percentage, or research approval has been invented.

## 2. Problem frame

ECPR001: analysts using this report may be unable to judge which attempts its help rate represents.
Source finding: ECRF001. The problem frame is proposed and limited to the supplied evidence.
An unclear denominator rule is an explanation to investigate, not a proven cause of every reporting problem.

## 3. Intended outcome and metric

ECOC001: analysts can understand the population behind the help-rate report. Outcome status: proposed.
Source problem: ECPR001. Baseline, target, and deadline: unknown.
ECMT001: help-rate definition. Status: incomplete because the two null-handling requests conflict.
Known fields are tenant_id, attempt_id, and needs_help. No missing flag rule has been selected.
The exercise does not calculate a help rate or claim an improvement in ECOC001.

## 4. Use case

ECUC001: an authorised analyst reviews the help report for the supplied tenant scope.
Source outcome: ECOC001. Source problem: ECPR001. Use case status: proposed.
The trusted query parameter is a fixture precondition. How the runtime obtains it remains unassessed.

## 5. User story and criteria

ECUS001
Source use case: ECUC001
Source outcome: ECOC001
Verification refs: ECTC001, ECTC002, ECTC003; current result ECRS001
As an analyst I want to inspect the report population for my authorised tenant so that I can interpret the help rate.

| Criterion ID | Revision | Status | Criterion and source |
| --- | --- | --- | --- |
| ECUS001.AC1 | 1 | agreed | with a trusted tenant parameter, the query population contains only that tenant; input.md recorded rules |
| ECUS001.AC2 | 1 | conflicting | treatment of unknown help flags; input.md conflicting requests |
| ECUS001.AC3 | 1 | agreed | empty eligible population means an unavailable rate; input.md recorded rules |
| ECUS001.AC4 | 1 | unknown | report is fast, but no measurable bound is supplied; input.md conflicting requests |

The exact source statuses are retained. Agreement on one criterion does not resolve another.

## 6. Acceptance test design

| Test ID | Revision | Criterion and revision | Design | Preconditions and steps | Expected result | Limit |
| --- | --- | --- | --- | --- | --- | --- |
| ECTC001 | 1 | ECUS001.AC1 revision 1 | ready | run the synthetic population query with trusted tenant 1 | rows (1,10), (1,11), (1,12) only | SQL fixture scope, not authentication or application access |
| ECTC002 | 1 | ECUS001.AC2 revision 1 | blocked | propose an unknown-flag case | no accepted oracle until the rule conflict is resolved | no guessed denominator rule |
| ECTC003 | 1 | ECUS001.AC3 revision 1 | ready | plan a case with no eligible attempts | rate unavailable rather than 0% | planned only; not executed in this exercise |

ECUS001.AC4 has no test because the performance bound is absent. It remains an explicit uncovered gap.
No result ID is created for ECTC002 or ECTC003.

## 7. Actual fixture result and coverage

Run from this directory:

```bash
python3 run_fixture.py > fixture-result.json
```

ECRS001 records the actual ECTC001 revision 1 fixture run.
It returned the three expected tenant 1 rows and no tenant 2 row.
This result is stored in `fixture-result.json` and imported unchanged into `test-register.json`.
ECTC002 and ECTC003 retain null current results and the derived execution state `not_run`.

The coverage helper reports four declared criteria, three mapped criteria, and one verified criterion in the stated fixture scope.
The conflict, planned boundary case, and unmeasurable performance request remain gaps.
See `coverage.md` and its draw.io map. Mapped coverage is not execution evidence.

## 8. Outcome and release review

ECOC001 achievement is unknown. There is no user outcome measurement, baseline, or agreed target.
A passing query-scope case does not prove that analysts understand the report.
ECMT001 remains incomplete, and no historical result is relabelled against a guessed definition.
The release remains blocked by the rule conflict, unrun case, missing performance decision, and unassessed target runtime.
Scope, capacity, dates, and release approval remain unconfirmed. No release action is taken.

## Exercise review

| Check | Observed handling | Limit |
| --- | --- | --- |
| Source IDs | retained through the linked records in trace-links.json | only supplied records are assessed |
| Missing research evidence | recruitment and prevalence remain unknown | no population claim |
| Conflicting rules | AC2 and metric definition remain unresolved | no invented oracle |
| Missing target and deadline | remain unknown | no product success or date promise |
| Unrun tests | null result pointers remain not_run | no fabricated result nodes |
| Real execution | one SQL fixture case produced ECRS001 | no target application or runtime authentication test |
| Review decision | outcome unknown and release blocked | no business acceptance inferred |

This worked example illustrates the skill outputs. It does not measure how an independent model handles unseen prompts.
