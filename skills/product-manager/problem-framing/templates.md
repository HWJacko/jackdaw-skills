# Templates — Problem Framing

Use `observed`, `assumed`, `proposed`, `agreed`, or `unknown` for each finding or decision.
`Agreed` needs a supplied decision with its owner and source. It does not mean the outcome has been achieved.
Evidence IDs such as `E1` are local to the source document. Cite the document when carrying them into another output.

```markdown
# [Project] — Product Problem

Project: [PN] | Frame status: proposed
Source findings: [existing research finding IDs, or unknown]

## Problem

[PN]PR001: [Affected user, situation, observed difficulty, and effect]
Assumed cause: [Separate assumption, or unknown]

## Evidence

| Source | Finding | Status | Population and period | Limits |
| --- | --- | --- | --- | --- |

## Intended outcomes

| ID | Related problem | Desired change | Status | Source |
| --- | --- | --- | --- | --- |

## Measures

| Outcome | Measure and unit | Population and period | Baseline | Target and status | Source |
| --- | --- | --- | --- | --- | --- |

## Constraints and non-goals

[Supplied limits and explicit exclusions]

## Open questions

| Decision needed | Why it matters | Evidence needed | Owner |
| --- | --- | --- | --- |

## Handoff

[What can be assessed next and what remains unconfirmed]

## Trace links

| From ID | To ID | Relationship | Link status | Source |
| --- | --- | --- | --- | --- |
```

Use source → dependent direction. `recorded` means an explicit source link, not agreement with the finding.
Use `proposed` for a new association. Do not infer links from matching project names or fill missing IDs.
