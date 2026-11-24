---
name: outcome-review
description: Compare supplied product results with the intended outcomes and measures. Assess evidence limits and recommend whether to continue, change, or stop an approach. Use after a product trial or release, not to treat shipped features as proof of success.
---

# Outcome Review

## Input

- Intended outcomes, baseline definitions, targets, and their decision status.
- Actual results, measurement periods, populations, and qualitative feedback.
- Trial or release scope and relevant constraints.

Derive `[PN]` from the project. Read [templates.md](templates.md). Preserve outcome IDs.

## Method

1. Restate the intended outcome and supplied measure. Keep proposed targets distinct from agreed targets.
   Preserve metric definition and result IDs where supplied. Check definition versions before comparing periods.
2. Check whether the baseline and actual results use comparable definitions, units, periods, and populations.
   Show differences. Do not combine incompatible cohorts or treat missing results as zero.
3. Calculate only from supplied values. Show counts, denominators, and the calculation when relevant.
   Distinguish a percentage-point change from a relative percentage change.
4. Compare actual results with the stated target and its status.
   Do not claim an agreed goal was missed when only a proposed target exists.
5. Assess contradictory feedback, measurement gaps, and effects outside the primary measure.
   A before-and-after comparison alone does not establish that the release caused the change.
6. Recommend continuing, changing, stopping, or collecting more evidence.
   Explain the basis and uncertainty. Record the human decision as pending unless supplied.
7. Use a comparison table by default. Add a chart when multiple supplied measurements make a trend or difference clearer.
   Label units, periods, and proposed targets. Keep missing points visibly missing.

## Output

Write `output/[PN]-outcome-review.md`.
Include the results, comparability checks, calculation, interpretation, recommendation, and open decisions.
Do not change the roadmap or backlog without instruction. Identify the affected source IDs for the next review.

## Voice

Use short, clear sentences. Define technical terms. State facts and identify assumptions. Use the template formats and identifiers exactly.

## Example

See [examples/input.md](examples/input.md) and [examples/example-output.md](examples/example-output.md).
