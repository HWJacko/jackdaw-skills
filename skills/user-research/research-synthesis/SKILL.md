---
name: research-synthesis
description: Turn supplied research notes, transcripts, or observations into sourced findings and open questions. Preserve sample limits, repeated participants, and contrary evidence. Produce a visual evidence map for problem framing and product decisions.
---

# Research Synthesis

## Input

- Research notes, transcripts, observation records, or supplied research results.
- The research question, study scope, participant references, and existing project IDs, when available.

Derive `[PN]` from the project name or existing IDs. Ask only when neither is available.
Read [templates.md](templates.md). No participant contact is needed for this analysis.
If raw research is absent, report the gap. Do not invent a study or customer evidence.

## Method

1. Record each source and its location, study, method, sample, and limits.
   Use existing pseudonyms. Omit personal details that are unnecessary for the task.
2. Extract observations separately from interpretations and proposed actions.
   Keep each observation linked to its source and participant when known.
   Quote only words actually supplied. Label a paraphrase as a paraphrase.
3. Group related observations into findings. Cite supporting and contrary evidence.
   Distinguish repeated notes about one participant from independent participant reports.
   Do not merge participant IDs across studies unless their identity link is supplied.
4. State what each finding supports, its limits, and what remains uncertain.
   Counts describe the supplied sample. They do not establish population prevalence or statistical significance.
   Keep missing participant counts unknown. Do not turn an isolated request into an agreed requirement.
5. Link findings to supplied problems or outcomes where the source explicitly establishes that relationship.
   Label a newly suggested relationship `proposed`. Keep existing IDs unchanged.
6. Separate observed behavior, interpreted findings, proposed actions, and recorded stakeholder decisions.
   Return questions that could change the interpretation. Do not claim that a finding is an approved product decision.
7. Draw sources → observations → findings. Include contrary evidence with a labelled edge.
   Keep node IDs, statuses, and relationships identical in Mermaid and draw.io.

## Output

Create `output/research-synthesis/` in the working project before writing files.
Use this folder for all files this skill produces, unless the user gives another path.

- `output/research-synthesis/[PN]-research-synthesis.md`: source register, observations, findings, contrary evidence, limits, questions, trace links, and Mermaid.
- `output/research-synthesis/[PN]-research-synthesis.drawio`: the same evidence map as draw.io XML.
- Optional PNG when `drawio` is available: `drawio -x -f png -o <out.png> <in.drawio>`.

Use `[PN]OB###` for observations and `[PN]RF###` for findings. Continue existing project numbering.
Use existing evidence IDs. If new evidence IDs are needed, use `[PN]EV###` without colliding with supplied records.
Qualify document-local IDs, such as `notes.md#E1`, when they would otherwise be ambiguous.
Markdown and draw.io XML do not depend on PNG tooling.

## Voice

Use short, clear sentences. Define technical terms. State facts and identify assumptions. Use the template formats and identifiers exactly.

## Example and method

See [examples/input.md](examples/input.md), [examples/example-output.md](examples/example-output.md),
and [examples/example-output.drawio](examples/example-output.drawio).
See [GOV.UK research analysis guidance](https://www.gov.uk/service-manual/user-research/analyse-a-research-session)
for the distinction between observations, findings, and actions.
