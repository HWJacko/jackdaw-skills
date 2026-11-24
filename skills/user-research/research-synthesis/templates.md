# Templates — Research Synthesis

Use `observed` for source observations, `interpreted` for findings, and `proposed` for actions.
Source records and participant references must resolve within the supplied study material.

```markdown
# [Project] — Research Synthesis

Research question: [question]
Scope: [studies, participants, period, and gaps]

## Sources

| Evidence ID | Location | Study | Participant reference | Method and limits |
| --- | --- | --- | --- | --- |

## Observations

| Observation ID | Participant | Observation or supplied quote | Form | Evidence ID and location |
| --- | --- | --- | --- | --- |

## Findings

| Finding ID | Interpretation | Supporting observations | Contrary observations | Distinct supporting participants | Limits |
| --- | --- | --- | --- | --- | --- |

## Proposed actions and questions

[Separate suggested action, unresolved question, and recorded decision]

## Trace links

| From ID | To ID | Relationship | Link status | Source |
| --- | --- | --- | --- | --- |

## Evidence map

[Mermaid flowchart and legend]
```

Trace direction is source → dependent. `recorded` means the source explicitly records that link.
It does not confirm a finding or approve an action. Use `proposed` for a new association.
If an ID or relationship is unknown, record the gap rather than create an `unknown` node.
In the map, show the observation form and finding status. Label contrary edges explicitly.
Do not use node size or colour to imply prevalence or confidence.
