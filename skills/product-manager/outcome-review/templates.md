# Templates — Outcome Review

```markdown
# [Project] — Outcome Review

Outcome: [existing outcome ID]
Metric definition: [existing metric ID and source version, or unknown]
Source results: [existing result IDs, or unknown]
Review decision: pending

## Results

| Measure | Baseline | Actual | Target and status | Change | Sources |
| --- | --- | --- | --- | --- | --- |

## Comparability and limits

[Definition, unit, period, population, missing results, and limits on causal claims]

## Calculation

[Numerator, denominator, formula, and units]

## Interpretation and recommendation

[What is observed, what remains uncertain, and the proposed next decision]

## Follow-up

| Decision or evidence needed | Why it matters | Owner | Affected outcome or backlog IDs |
| --- | --- | --- | --- |

## Trace links

| From ID | To ID | Relationship | Link status | Source |
| --- | --- | --- | --- | --- |
```

For rates, show raw counts when supplied. A move from 30% to 20% is a fall of 10 percentage points.
A chart must use the same values and target status as the table. Do not infer causality from the chart.
Trace links run source → dependent. Use `recorded` for a supplied link and `proposed` for a new association.
Do not create a result ID or a passed test when only a planned measure is supplied.
