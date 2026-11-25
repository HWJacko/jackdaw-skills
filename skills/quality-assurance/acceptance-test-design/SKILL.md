---
name: acceptance-test-design
description: Derive acceptance tests from supplied stories, criteria, and business rules. Cover normal, error, and boundary cases where relevant. Preserve source IDs, identify conflicting rules, and keep planned tests separate from execution evidence.
---

# Acceptance Test Design

## Input

- User stories, acceptance criteria, business rules, and their source versions.
- Relevant test data, environments, decisions, and existing tests or results, when supplied.

Derive `[PN]` from the project or existing IDs. Read [templates.md](templates.md).
Keep source story and criterion IDs. Qualify local criteria, such as `SPUS001.AC1`, to avoid collisions.

## Method

1. List the criteria in scope and their source revisions.
   Retain the supplied decision status. If agreement is absent, use `unknown` or `proposed`.
   Flag contradictory rules as `conflicting`. Do not resolve the conflict by choosing a convenient expected result.
2. Derive cases for normal behavior, relevant errors, and boundaries from the supplied rules.
   Specify preconditions, input data, actions, and observable expected results.
   Do not invent limits, messages, permissions, states, or performance targets that the source does not define.
3. Record the criterion and revision that each case checks. Several cases may check one criterion.
   State what the case does not cover. A narrow passing case does not establish that the full feature works.
4. Keep a case `blocked` when a missing rule, expected value, reference asset, or environment prevents execution.
   Produce the useful test design and questions first. Do not stop all design because one rule is incomplete.
5. Use existing test IDs. For new cases, use `[PN]TC###` and continue project numbering.
   Give changed test steps or expected results a new revision. Retain earlier result evidence against its original revision.
6. Create the local test register described in the template.
   New cases have `current_result_id: null`. Do not allocate result IDs for tests that have not run.
   Import supplied results without changing their status. Record source, environment, observed behavior, and tested revision.
7. If execution is requested and the environment is authorised, run the relevant cases and record actual evidence.
   Otherwise keep them unrun. A test plan or source-data example is not evidence that the target application passed.

## Output

- `output/[PN]-acceptance-tests.md`: source criteria, test steps, expected results, blocked cases, and decisions needed.
- `output/[PN]-test-register.json`: criteria, versioned test references, and any supplied or actually observed results.

The register can feed Test Coverage Map. It also retains source links for Change-Impact Analysis.
Do not change source criteria, Jira issues, or release decisions without instruction.

## Voice

Use short, clear sentences. Define technical terms. State facts and identify assumptions. Use the template formats and identifiers exactly.

## Example and method

See [examples/input.md](examples/input.md), [examples/example-output.md](examples/example-output.md),
and [examples/example-test-register.json](examples/example-test-register.json).
See [ISTQB acceptance testing](https://istqb.org/certifications/certified-tester-acceptance-testing/)
for collaboration between business analysis, product ownership, and testing.
