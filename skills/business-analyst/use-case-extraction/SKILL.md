---
name: use-case-extraction
description: Extract stakeholders, systems, goals, EPICs and atomic use cases from unstructured text (meeting notes, briefs, transcripts). Use when the user provides raw input and wants structured business analysis output.
---

# Use Case Extraction

## Purpose

Convert unstructured text into structured use cases, ready for story writing by the requirement-construction skill.

## Input

Raw text: meeting notes, a project brief, a transcript, or a description.

## Method

1. Read the full input. Identify the project name and derive a two-or-more-letter abbreviation `[PN]` (example: New Website → NW).
2. Extract:
   - **Stakeholders** — impacted and involved users.
   - **Systems** — infrastructure elements (hardware and software) that impact the flow.
   - **Goals** — high-level expected outcomes.
3. Write one EPIC per distinct end-to-end journey.
   - Format (preferred, not mandatory): "To achieve [Goals summarised] in/on [Systems] through [Behaviours summarised]".
   - ID: `[PN]EP001`, `[PN]EP002`, ...
4. Write use cases under each EPIC.
   - Format: "To achieve [Goal] [Stakeholder] can [Behaviour] by [Trigger] in/on [Systems], with [Dependencies]".
   - ID: `[PN]UC001`, sequential across the project.
   - Preserve supplied problem and outcome IDs in the trace-link table. Do not infer them from similar names.
5. Granularity rule: each use case must be small enough to break down into atomic user stories by the requirement-construction skill. If the input needs more than one EPIC with its own use cases, produce them all.
6. If information is missing, state the assumption in one line and continue. Do not stop to confirm derivable values (project abbreviation, paths, formats). Only ask the user when required information is genuinely absent.
7. Do not discuss voice, language rules, or instruction conflicts in your response — produce the output only.

## Output

One Markdown document:

- Header: project name, `[PN]`, date.
- Lists: Stakeholders, Systems, Goals.
- EPIC table: ID, statement.
- Use case table per EPIC: ID, use case, dependencies.
- Source problem and outcome references, plus documented trace links. Leave absent references `unknown`.

Write the output to `output/[PN]-use-cases.md` unless the user says otherwise.

## Voice

Use short, clear sentences. Write for business and technical readers. Define necessary technical terms. Use the template formats and identifiers exactly. State facts and identify assumptions. Remove filler.

## Templates and examples

See [templates.md](templates.md) and [examples/](examples/).
