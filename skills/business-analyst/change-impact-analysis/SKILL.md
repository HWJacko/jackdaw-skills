---
name: change-impact-analysis
description: Trace a proposed change through supplied evidence, findings, outcomes, metrics, use cases, stories, tests, and results. Identify records needing review, possible impacts, and missing links. Produce a visual impact map without changing the source work.
---

# Change-Impact Analysis

## Input

- The changed source IDs and a description of the proposed change.
- Source documents with explicit links, or a `[PN]-trace-links.json` graph in the template format.
- The review scope and existing source IDs.

Derive `[PN]` from the source project. Read [templates.md](templates.md).
If no change or source material is supplied, ask for it. Do not invent a dependency graph.

## Method

1. State the change, source version, and supplied review scope.
   Preserve all native IDs. Qualify document-local IDs when they would otherwise collide.
2. Build or update the node register from actual supplied records.
   Build source → dependent links from explicit source fields and trace-link tables.
   A similar name does not establish a dependency. Keep suggested associations `proposed`.
   Do not invent a missing endpoint record from its ID alone.
3. Save the source graph as `output/[PN]-trace-links.json`.
   Resolve this skill folder and run the local helper from the working project root:

   ```bash
   python3 <absolute-skill-folder>/scripts/analyse_links.py output/[PN]-trace-links.json <changed-id> [other-changed-ids]
   ```

   The helper reads local JSON only. It follows recorded links for required review.
   It also follows proposed links for possible review. Missing endpoints remain gaps.
   It terminates when links contain cycles. It does not scan files or discover unrecorded dependencies.
4. Explain why each downstream record needs review. Cite the link path and source evidence.
   Check changed business rules, metric definitions, acceptance criteria, plans, and reported results where linked.
   Do not assume that every downstream value has changed. Review is not proof of an actual effect.
5. Keep recorded-link review, possible review, and missing evidence distinct.
   Unreached records are only unreached in this supplied graph. Do not declare them unaffected.
   If links are missing or files are absent, state the incomplete coverage.
6. Propose review actions and owners where supplied. Keep new decisions pending.
   Do not mark a test passed, invalidate an accepted decision, recalculate history, or update a backlog automatically.
7. Draw the changed records and downstream review paths.
   Show proposed links as dashed edges. Show missing endpoints as labelled gap placeholders, not invented source records.
   Keep Markdown, Mermaid, and draw.io consistent.

## Output

- `output/[PN]-trace-links.json`: the supplied node and link register with its scope.
- `output/[PN]-change-impact.md`: review list, reasons, possible review, gaps, actions, and Mermaid `flowchart LR`.
- `output/[PN]-change-impact.drawio`: the same impact map as draw.io XML.
- Optional PNG when `drawio` is available: `drawio -x -f png -o <out.png> <in.drawio>`.

Missing PNG tooling must not block the other outputs. Source records remain unchanged unless their update is requested.

## Voice

Use short, clear sentences. Define technical terms. State facts and identify assumptions. Use the template formats and identifiers exactly.

## Example

See [examples/input.md](examples/input.md), [examples/input-trace-links.json](examples/input-trace-links.json),
[examples/example-analysis.json](examples/example-analysis.json), [examples/example-output.md](examples/example-output.md),
and [examples/example-output.drawio](examples/example-output.drawio).
