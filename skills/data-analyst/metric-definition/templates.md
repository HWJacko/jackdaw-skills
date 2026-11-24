# Templates — Metric Definition

```markdown
# [Project] — Metric Definition

Metric ID: [PN]MT001
Source outcome: [existing ID, or unknown]
Definition status: proposed, agreed, or incomplete
Target status: [separate supplied decision, or unknown]
Calculation verification: not_run, fixture_checked, or checked_in_named_environment

## Business definition

| Rule | Definition | Status | Source |
| --- | --- | --- | --- |
| Question | [business question] | [status] | [source] |
| Unit and grain | [unit and what one base row represents] | [status] | [source] |
| Population | [eligible users, rows, tenant, and exclusions] | [status] | [source] |
| Numerator | [exact count or value] | [status] | [source] |
| Denominator | [exact population for a rate] | [status] | [source] |
| Zero population | [null, unavailable, or supplied rule] | [status] | [source] |
| Missing data | [handling and separately reported counts] | [status] | [source] |
| Time | [field, zone, start/end boundaries] | [status] | [source] |

## Source fields and joins

| Source object and field | Meaning | Key or grain | Rule or join | Evidence |
| --- | --- | --- | --- | --- |

## Verification

| Case | Input population | Expected result | Environment | Result and evidence |
| --- | --- | --- | --- | --- |

## Historical comparability and open decisions

[Baseline compatibility, definition changes, missing decisions, and affected result IDs]

## Trace links

| From ID | To ID | Relationship | Link status | Source |
| --- | --- | --- | --- | --- |
```

Trace direction is source → dependent. A metric definition points to the outcome or result that uses it.
Use `recorded` for an explicitly documented link and `proposed` for a new association.
Neither link status proves business agreement. Keep the definition source and decision separate.
Never create a result ID to imply an actual measurement has occurred.
