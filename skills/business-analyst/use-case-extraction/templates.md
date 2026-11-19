# Templates — Use Case Extraction

## Identifiers

| Item | Format | Example |
| :--- | :--- | :--- |
| Project abbreviation | `[PN]` | New Website → `NW` |
| EPIC | `[PN]EP###` | `NWEP001` |
| Use case | `[PN]UC###` | `NWUC001` |

Use case IDs are sequential across the whole project, not per EPIC.

## EPIC format

Preferred, not mandatory:

> To achieve [Goals summarised] in/on [Systems] through [Behaviours summarised]

## Use case format

> To achieve [Goal] [Stakeholder] can [Behaviour] by [Trigger] in/on [Systems], with [Dependencies]

## Output skeleton

```markdown
# [Project name] — Use Case Extraction
Date: [date] | Project ID: [PN]

## Stakeholders
- ...

## Systems
- ...

## Goals
- ...

## EPICs
| ID | Statement |
| --- | --- |
| [PN]EP001 | ... |

## Use Cases — [PN]EP001
| ID | Use case | Dependencies |
| --- | --- | --- |
| [PN]UC001 | ... | ... |
```
