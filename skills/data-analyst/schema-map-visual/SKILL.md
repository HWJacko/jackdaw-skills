---
name: schema-map-visual
description: Draw a database schema model with evidence status, composite join keys, and open SME questions. Use an existing schema-map JSON model to produce Mermaid and draw.io diagrams. Do not infer new relationships or approve query use.
---

# Schema Map [VISUAL]

## Input

- `[PN]-schema-model.json` from Schema Map, or a model with the same fields and statuses.

If no model is available, request it or use Schema Map when source inspection is requested.
Do not infer business meanings from an unlabelled diagram.

## Method

1. Read [templates.md](templates.md) and the supplied model.
2. Show tables and views with model IDs, exact names, columns, and ordered keys.
   Use short diagram node IDs. Keep exact database names in labels.
3. Draw one edge per relationship. Keep every source and target column in order.
   Show the relationship ID, status, cardinality, query-use status, and open question IDs.
   Draw assumed relationships as dashed lines. Draw observed or confirmed relationships as solid lines.
   Status labels remain required. A solid line is not query approval.
4. Keep unknown cardinality labelled `unknown`. List rejected relationships with their reasons below the diagram.
   Do not draw a rejected relationship as a usable join. Do not create absent relationships.
5. Use the same nodes, labels, and edges in Mermaid and draw.io.
   If the model is too large, split the view by the supplied scope. List omitted objects and cross-view edges.
6. Preserve the model's handoff status and unresolved blocking question IDs beside each view.
   If references are invalid, report the broken IDs. Do not repair them by guessing database objects.

## Output

Write to `output/`, with basename `[PN]-schema-map-visual`:

- `.md`: Mermaid `flowchart LR`, a legend, source limits, and the open question IDs.
- `.drawio`: the same graph as draw.io XML.
- `.png`: only when the `drawio` CLI is available. Use `drawio -x -f png -o <out.png> <in.drawio>`.

Mermaid and draw.io XML are always produced. A missing renderer does not block these outputs.
This skill needs no database connection and does not change the source model.

## Voice

Use short, clear sentences. Define technical terms. State facts and identify assumptions. Use the template formats and identifiers exactly.

## Example

See [examples/example-output.md](examples/example-output.md) and [examples/example-output.drawio](examples/example-output.drawio).
