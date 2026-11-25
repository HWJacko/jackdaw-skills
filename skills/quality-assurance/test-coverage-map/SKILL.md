---
name: test-coverage-map
description: Map supplied stories and acceptance criteria to versioned tests and results. Separate mapped coverage from current passing evidence. Show unrun, stale, conflicting, and missing records in Mermaid and draw.io diagrams.
---

# Test Coverage Map

## Input

- `[PN]-test-register.json` from Acceptance Test Design, or the same register fields from supplied records.
- Source story and criterion versions, current-result selections, and test evidence.

Read [templates.md](templates.md). Preserve all source IDs.
If no register exists, assemble it from explicit supplied records. Do not invent missing tests or results.

## Method

1. State the supplied scope and source versions. Keep missing criteria or records visible as gaps.
2. Resolve this skill folder and run the local helper:

   ```bash
   python3 <absolute-skill-folder>/scripts/summarise_coverage.py output/[PN]-test-register.json
   ```

   The helper reads local JSON. It does not run tests or inspect the target application.
3. Separate criteria with mapped tests from criteria with current passing evidence.
   Every mapped case is required in this register. Do not ignore a failed or unrun case to improve the summary.
4. Preserve the reported result status and its evidence.
   A result for an older test or criterion revision is not current verification.
   An unclear or missing result reference cannot become a pass. Do not choose a different result automatically.
5. Keep proposed, unknown, or conflicting criteria unresolved, even if a related test reports a pass.
   Mark a criterion verified only when it is agreed and all its mapped cases are current and passed.
   This is limited evidence for the listed criteria, not proof of complete coverage or release readiness.
6. Draw story → criterion → test → selected result.
   Label the criterion decision, test design state, reported result, and stale or missing evidence.
   Do not create result nodes for unrun cases. Show missing references as gap placeholders when useful.
7. Keep the tables, helper summary, Mermaid, and draw.io consistent.
   Return review actions for unmapped criteria, blocked designs, stale results, failures, and unresolved rules.
   Do not change source evidence or approve a release.

## Output

- `output/[PN]-test-coverage.md`: scope, criteria, mapped cases, current evidence, gaps, and Mermaid `flowchart LR`.
- `output/[PN]-test-coverage.drawio`: the same coverage graph as draw.io XML.
- Optional PNG when `drawio` is available: `drawio -x -f png -o <out.png> <in.drawio>`.

Always produce Markdown and draw.io XML. Missing PNG tooling does not block the map.
Counts describe only the supplied criteria. Do not present them as a universal test-coverage percentage.

## Voice

Use short, clear sentences. Define technical terms. State facts and identify assumptions. Use the template formats and identifiers exactly.

## Example and method

See [examples/input.md](examples/input.md), [examples/input-test-register.json](examples/input-test-register.json),
[examples/example-summary.json](examples/example-summary.json), [examples/example-output.md](examples/example-output.md),
and [examples/example-output.drawio](examples/example-output.drawio).
See [GOV.UK quality guidance](https://www.gov.uk/service-manual/technology/quality-assurance-testing-your-service-regularly)
for testing technical behavior and user needs.
