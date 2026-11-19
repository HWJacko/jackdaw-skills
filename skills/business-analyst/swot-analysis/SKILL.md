---
name: swot-analysis
description: Produce a SWOT analysis (Strengths, Weaknesses, Opportunities, Threats) from a project brief, strategy text or discussion notes. Markdown output with a 2x2 grid table.
---

# SWOT Analysis

## Purpose

Structure the internal and external factors affecting a project, product or decision into a SWOT grid that business and tech can both act on.

## Input

Raw text: a project brief, strategy document, meeting notes, or a description of the situation.

## Method

1. Read the full input. State the subject in one line (the project, product or decision being analysed).
2. Classify each factor:
   - **Strengths** — internal, positive. Things the team/org/product does well.
   - **Weaknesses** — internal, negative. Gaps, constraints, known problems.
   - **Opportunities** — external, positive. Market, technology or organisational openings.
   - **Threats** — external, negative. Competition, risks, dependencies outside our control.
3. Each entry: one short sentence, specific, evidence-based. No generic filler ("strong team" is not a strength; "two engineers with prior payments experience" is).
4. Aim for 3–7 entries per quadrant. Fewer is fine if the input is thin — do not pad.
5. If the input supports it, add one line per quadrant on the highest-impact item.
6. If information is missing, state the assumption in one line and continue. Do not stop to confirm derivable values.

## Output

One Markdown file `output/[PN]-swot.md`:

- Header: subject, date.
- 2x2 grid as a Markdown table (Strengths / Weaknesses top row, Opportunities / Threats bottom row).
- Bulleted detail per quadrant under the table.
- Optional "So what" section: 2–3 lines on what the analysis implies for action.

## Voice

Follow the repository default ([voice.md](../../../voice.md)): concise and clear, understandable by business and tech alike.

## Templates and examples

See [templates.md](templates.md) and [examples/](examples/).
