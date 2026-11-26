---
name: metric-definition
description: Define a product or service measure from its business question and available data. Specify population, grain, numerator, denominator, time rules, source fields, and verification cases. Use before interpreting outcomes or generating metric SQL.
---

# Metric Definition

## Input

- A business question, intended outcome, or proposed measure.
- Source schema, field definitions, data rules, and existing metric decisions where available.
- Supplied baselines, targets, and calculation examples.

Derive `[PN]` from the project. Read [templates.md](templates.md).
Preserve outcome IDs and existing metric IDs. Use `[PN]MT###` only for a new metric.

## Method

1. State the question the measure answers and the outcome it supports.
   Separate the metric definition, target agreement, calculation checks, and evidence of outcome achievement.
2. Specify the unit, row grain, population, and eligibility rules.
   For a rate, define numerator and denominator independently. State what happens when the denominator is zero.
3. Define dates, time zone, period boundaries, status values, null handling, exclusions, and tenant scope where relevant.
   Keep unsupported rules unknown and return questions. Do not silently count missing data as zero.
4. Map every required field to its supplied source object and meaning.
   Preserve composite and tenant keys. Use only reviewed joins and avoid multiplying the base population with detail rows.
   A valid SQL query does not prove that its business definition is correct.
5. Record the decision owner, source, date, and status for agreed rules.
   Without that evidence, keep the definition `proposed` or `incomplete`.
   Do not turn a proposed target into an agreed target when the calculation is accepted.
6. Define verification cases for normal values, missing data, duplicates or detail rows, zero population, time boundaries, and scope.
   Use supplied examples or clearly synthetic test fixtures. Do not present fixture counts as a live baseline.
7. If useful, provide dialect-specific read-only SQL or a calculation specification.
   Do not invent missing columns or create a database connection.
   Execute only within authorised scope. Record the test environment and leave unrun checks `not_run`.
8. Check whether existing baselines and results use the same definition and population.
   If the definition changes, identify affected results for review. Do not relabel historical figures as comparable without evidence.

## Output

Create `output/metric-definition/` in the working project before writing files.
Use this folder for all files this skill produces, unless the user gives another path.

Write `output/metric-definition/[PN]-metric-definition.md`, including source links and verification cases.
When a query can be specified, also write `output/metric-definition/[PN]-metric-query.sql` with named value parameters.
Mark unknown rules and unrun checks. A supplied schema alone cannot establish an agreed metric or runtime access.
Use a field-lineage diagram when several source objects make the calculation difficult to follow.

## Voice

Use short, clear sentences. Define technical terms. State facts and identify assumptions. Use the template formats and identifiers exactly.

## Example and method

See [examples/input.md](examples/input.md), [examples/input-schema.sql](examples/input-schema.sql),
[examples/input-data.sql](examples/input-data.sql), [examples/example-output.md](examples/example-output.md),
and [examples/example-query.sql](examples/example-query.sql).
See [GOV.UK metric guidance](https://www.gov.uk/service-manual/measuring-success/how-to-set-performance-metrics-for-your-service)
for connecting goals, measures, and data sources.
