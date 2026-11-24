# Templates — Opportunity Assessment

Preserve outcome IDs from the source. Use `assumed` for an interpretation and `proposed` for a candidate response.
Research findings need source references. A selected solution needs a recorded decision.

## Report

```markdown
# [Project] — Opportunity Assessment

Outcome: [ID and desired change] | Decision status: proposed

## Opportunities and options

| Opportunity | Evidence and limits | Option | Expected benefit | Status | Open risk |
| --- | --- | --- | --- | --- | --- |

## Tests

| Test ID | Option | Assumption | Proposed test | Decision rule | Owner | Result |
| --- | --- | --- | --- | --- | --- | --- |

## Recommendation

[Next investigation or comparison, evidence, and unresolved decisions]

## Opportunity map

[Mermaid flowchart and legend]
```

## Visual contract

- Show outcome, opportunity, option, and test IDs in every label.
- Label the status of each node. Use `not_run` for unrun tests.
- Use labelled edges: `need`, `option`, and `test`.
- Do not encode a score or proven impact through node size or colour.
- Use one draw.io vertex per node and one connector per relationship. Keep unique IDs and valid endpoints.
- Mermaid and draw.io must show the same labels and edges. Escape labels for each format.
