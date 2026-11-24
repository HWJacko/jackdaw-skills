---
name: opportunity-assessment
description: Compare customer needs and possible product responses against a stated outcome. Produce evidence, assumptions, risks, test plans, and a visual opportunity map. Use after problem framing and before committing delivery scope.
---

# Opportunity Assessment

## Input

- A problem frame or product outcome, with research or other source evidence.
- Candidate options, constraints, and existing IDs, when available.

Derive `[PN]` from the source project. Read [templates.md](templates.md).
An opportunity is a customer need or difficulty. A solution is one possible response to it.

## Method

1. State the outcome and its evidence. Preserve its ID and target status.
2. Extract supported customer needs. Keep a feature request separate from the need it may address.
   Do not create findings from imagined interviews. Label interpretations as assumptions.
3. Compare candidate solutions for the same need. Label newly proposed options `proposed`.
   Record the source, expected benefit, uncertainties, and constraints for each option.
4. Identify risks about user value, usability, technical feasibility, and business fit where relevant.
   Ask engineering or the appropriate owner about unsupported feasibility claims. Do not invent effort estimates.
5. Propose the smallest useful test for each important assumption.
   State the observation needed, decision rule, owner, and result status.
   Use numeric thresholds only when supplied. Otherwise leave them for agreement.
   A test plan is not a test result. Keep unrun tests `not_run`.
6. Recommend what to investigate or compare next. Explain evidence limits and trade-offs.
   Do not rank options through invented scores or claim a delivery decision has been made.
7. Draw outcome → opportunities → options → tests.
   Give every node its source ID and status. An edge shows the proposed structure, not a proven causal effect.
   Keep labels and relationships identical in Mermaid and draw.io.

## Output

- `output/[PN]-opportunity-assessment.md`: assessment tables, recommendation, questions, and Mermaid `flowchart LR`.
- `output/[PN]-opportunity-assessment.drawio`: the same opportunity map as draw.io XML.
- Optional PNG when `drawio` is available: `drawio -x -f png -o <out.png> <in.drawio>`.

Use `[PN]OP###` for opportunities, `[PN]SL###` for proposed solutions, and `[PN]XT###` for tests.
Preserve existing IDs. Continue numbering per project. Missing PNG tooling must not block the other outputs.

## Voice

Use short, clear sentences. Define technical terms. State facts and identify assumptions. Use the template formats and identifiers exactly.

## Examples and method

See [examples/input.md](examples/input.md), [examples/example-output.md](examples/example-output.md),
and [examples/example-output.drawio](examples/example-output.drawio).
The map follows the distinction between outcomes, needs, solutions, and tests described by
[Product Talk](https://www.producttalk.org/opportunity-solution-trees/).
