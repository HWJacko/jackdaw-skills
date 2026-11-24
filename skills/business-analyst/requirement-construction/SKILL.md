---
name: requirement-construction
description: Write atomic, testable user stories with Gherkin scenarios and acceptance criteria from a use case. Local Markdown output. JIRA integration is a separate, later skill.
---

# Requirement Construction I — Local

## Purpose

Turn one use case into atomic, testable user stories stored in a local file.

## Input

- One use case, typically produced by the use-case-extraction skill.
- Its project abbreviation `[PN]`. Derive it from the use case ID if present (the letters before `UC`). If no ID exists, derive it from the project name in the input. State which you used in one line at the top of the output. Only ask the user if neither is available.

## Method

1. Split the use case into atomic, testable elements. One story per element.
2. Story format: "As a [stakeholder] I want to be able to [action] so that [outcome]".
3. Each story has one or more scenarios in Gherkin: GIVEN, WHEN, THEN, with AND / BUT / OR as needed.
4. Each story ends with numbered acceptance criteria: AC1, AC2, ...
5. IDs: `[PN]US001`, sequential per project. When appending, read the existing IDs and continue after the highest number. This is a local ID. It is not the JIRA key; JIRA keys are added only when a JIRA connection is available (Requirement Construction II).
6. Each story must be testable on its own. If a story needs another story to make sense, split again.
7. Record `Source use case: [PN]UC###` under each story heading. Use the source ID. If it is absent, write `Source use case: unknown`. Do not invent an ID.
8. Carry supplied outcome IDs and test or result references into the source fields. Keep absent references `unknown`.
   Record explicit source → dependent links in the trace-link table. Do not create test or result IDs without source records.

## Output

Append to (or create) `output/[PN]-user-stories.md`:

- Story ID and story sentence.
- Source use case ID, or `unknown` if the source has no ID.
- One Gherkin block per scenario.
- Acceptance criteria list.

## Behaviour

- Do not stop to confirm derivable values (project abbreviation, file paths, formats). Derive them, state the derivation in one line, and proceed.
- Only ask the user when required information is genuinely absent from the input.

## Voice

Use short, clear sentences. Write for business and technical readers. Define necessary technical terms. Use the template formats and identifiers exactly. State facts and identify assumptions. Remove filler. Write story content in this voice. Do not discuss voice, language rules, or instruction conflicts in your response — produce the output only.

## Templates and examples

See [templates.md](templates.md) and [examples/](examples/).
