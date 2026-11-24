# Templates — Outcome Roadmap

Use `proposed` or `agreed` for roadmap decisions. Agreement needs a supplied owner decision and source.
Keep outcome achievement separate from a decision to pursue it.

```markdown
# [Project] — Outcome Roadmap

Product Goal: [goal]
Roadmap status: proposed
Horizons show relative sequence. No dates are implied.

## Roadmap

| Outcome ID | Horizon | Desired change | Evidence | Measure and target status | Hard prerequisites | Review condition | Owner | Decision status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Sequence and dependencies

| From | To | Type | Source or proposed reason |
| --- | --- | --- | --- |

## Visual roadmap

[Mermaid flowchart with Now, Next, and Later subgraphs]

## Open decisions

[Missing measures, dates, capacity, owners, or agreement]
```

## Visual contract

- Put each outcome in one horizon. Show its ID, desired change, and decision status.
- Use Mermaid `subgraph` for each horizon. Use matching lanes in draw.io.
- Solid arrow: supplied hard prerequisite. Dashed arrow: proposed sequence. Label the difference in text.
- Show review conditions in the table. Do not turn a proposed sequence into a technical dependency.
- Use the same displayed node labels and edges in both formats.
- Use plain labels such as `unknown` for absent measures. Never create a date to make a chart render.
