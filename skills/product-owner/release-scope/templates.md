# Templates — Release Scope

```markdown
# [Project] — Release Scope

Outcome: [existing outcome ID and change]
Scope decision: proposed
Release status: blocked, or supported by the supplied decision evidence
Date and capacity: [supplied evidence, or unknown]

## Candidate scope

| Existing item ID | Included or deferred | Contribution or reason | Prerequisites | Source |
| --- | --- | --- | --- | --- |

## Dependency checks

| Prerequisite | Dependent item | Included or already available | Evidence | Gap |
| --- | --- | --- | --- | --- |

## Release conditions

| Condition | Owner | Evidence | Result |
| --- | --- | --- | --- |

## Scope map

[Mermaid diagram and legend]

## Open decisions and non-goals

[Unresolved scope, feasibility, quality, operational needs, and explicit exclusions]
```

## Visual contract

- Keep source story IDs in node labels. Show `included` or `deferred` on each item.
- Draw source-backed prerequisite → dependent edges labelled `required by`.
- A dashed arrow to the release decision means `check before release`, not a completed test.
- Use a separate decision node with status text. Do not imply readiness through colour.
- Use the same labels and edges in Mermaid and draw.io. Show unresolved prerequisites explicitly.
