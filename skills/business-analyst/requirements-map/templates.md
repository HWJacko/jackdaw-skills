# Templates — Requirements Map

Three outputs per map: Mermaid (always), draw.io XML (always), PNG (when the `drawio` CLI is installed).

## Mermaid

Type: `mindmap`. One map per project.

### Hierarchy

```text
[PN] Project name
└── [PN]EP### EPIC short name
    └── [PN]UC### Use case short name
        └── [PN]US### Story short name
```

### Rules

- Every node: ID + short name. Never a node without an ID.
- Use the IDs from the source files. Do not renumber.
- Link stories through `Source use case:`. Link use cases through their EPIC tables.
- List IDs with missing source links under `Unmapped items`. Count them as gaps. Do not guess a parent.
- Retain supplied outcome, test, and result links in a separate trace-link table. Keep the requirements tree unchanged.
- Gaps: append `(no stories)` or `(empty)`.
- After the diagram, give a coverage summary: counts and gaps.

### Skeleton

````markdown
# [PN] — Requirements Map

```mermaid
mindmap
  root(([PN] Project name))
    [PN]EP001 EPIC name
      [PN]UC001 Use case name
        [PN]US001 Story name
      [PN]UC002 Use case name (no stories)
```

## Coverage
- EPICs: n | Use cases: n | Stories: n
- Gaps: [list]

## Trace links

| From ID | To ID | Relationship | Link status | Source |
| --- | --- | --- | --- | --- |
````

Trace links use source → dependent direction. `recorded` means documented; `proposed` means an association needing review.
Missing links remain gaps. Use Change-Impact Analysis for the wider graph rather than adding invented parents to this tree.

## draw.io XML

Same hierarchy and IDs as the Mermaid version. Tree layout: project at left, EPICs in a column, use cases to their right, stories rightmost. One `mxCell` per node (`vertex="1"`), one per connector (`edge="1"`), `parent="1"` throughout.

## PNG

Render only when the CLI exists:

```bash
drawio -x -f png -o [PN]-requirements-map.png [PN]-requirements-map.drawio
```

If `drawio` is not on PATH, skip and note: `brew install --cask drawio`. Never fail.

## Lucidchart path

No integration. The `.drawio` file imports into Lucidchart via File → Import. This is deliberate: no accounts or secrets in this skill.
