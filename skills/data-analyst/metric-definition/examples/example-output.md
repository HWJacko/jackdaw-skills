# Support Portal — Metric Definition

Metric ID: SPMT001
Source outcome: SPOC001
Definition status: agreed, within the synthetic example
Target status: 15%, proposed and not agreed
Calculation verification: fixture_checked through the repository's SQLite tests

## Business definition

| Rule | Definition | Status | Source |
| --- | --- | --- | --- |
| Question | What share of eligible attempts needed developer help? | agreed | input.md E2 |
| Unit and grain | percent; one attempt per tenant_id and attempt_id | agreed | input.md E1–E2 |
| Population | authorised tenant; attempt starts inside the supplied period; known help flag | agreed | input.md E2 |
| Numerator | eligible attempts with needs_help = 1 | agreed | input.md E2 |
| Denominator | attempts with needs_help equal to 0 or 1 | agreed | input.md E2 |
| Zero population | zero denominator gives a null rate; keep the separate counts | agreed | input.md E2 |
| Missing data | exclude unknown flags from the rate and report their count | agreed | input.md E2 |
| Time | started_at in canonical UTC; start included and end excluded | agreed | input.md E1–E2 |

Definition owner: Example SME. Decision date: 2026-11-24. This is synthetic decision evidence only.

## Source fields and joins

| Source object and field | Meaning | Key or grain | Rule or join | Evidence |
| --- | --- | --- | --- | --- |
| main.publishing_attempts.tenant_id | tenant boundary | first primary-key column | required scope filter | input.md E1–E2 |
| main.publishing_attempts.attempt_id | attempt within a tenant | second primary-key column | count the base row once | input.md E1 |
| main.publishing_attempts.started_at | start instant | attempt grain | UTC period boundaries | input.md E1–E2 |
| main.publishing_attempts.needs_help | helped, not helped, or unknown | attempt grain | separate numerator, denominator, and unknown count | input.md E1–E2 |
| main.attempt_notes | optional detail records | several rows per attempt | no join is needed for this metric | input.md E1–E2 |

## Verification

| Case | Input population | Expected result | Environment | Result and evidence |
| --- | --- | --- | --- | --- |
| Normal period | tenant 1; supplied start and end | 2 helped; 3 eligible; 1 unknown; 66.67% rounded | local SQLite fixture | fixture_checked; repository metric tests |
| Unknown flag only | tenant 1; 2026-11-05T00:00:00Z to 2026-11-06T00:00:00Z | 0 helped; 0 eligible; 1 unknown; null rate | local SQLite fixture | fixture_checked; repository metric tests |
| Empty population | tenant 999; supplied period | zero counts; null rate | local SQLite fixture | fixture_checked; repository metric tests |

The query excludes the end-boundary row and preserves tenant scope.
Detail notes do not multiply attempts. Fixture results are not a live baseline or evidence of runtime access controls.

## Historical comparability and open decisions

The historical 30% baseline used all recorded attempts. Its null handling is unknown, from input.md E3.
Do not compare it with this definition until the historical population and unknown flags are checked.
Metric agreement does not agree the proposed 15% target. Live source quality and runtime checks remain unrun.

## Trace links

| From ID | To ID | Relationship | Link status | Source |
| --- | --- | --- | --- | --- |
| SPMT001 | SPOC001 | used to assess | recorded | input.md outcome and E2 definition |
