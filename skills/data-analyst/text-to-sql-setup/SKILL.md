---
name: text-to-sql-setup
description: Prepare or implement an MCP or text-to-SQL solution from a confirmed schema model. Check the SME handoff, define query access and limits, and build evaluation cases. Use after schema discovery and SME review, not to infer missing business rules.
---

# Text-to-SQL Setup

## Purpose

Use confirmed database meanings to prepare a query solution.
MCP means Model Context Protocol. Text-to-SQL means generating SQL from a question in normal language.
An approved schema handoff permits setup work. It does not prove that a runtime is ready for use.

## Input

- A scoped `[PN]-schema-model.json` from Schema Map, with dated SME answers and confirmed query cases.
- The target database dialect, intended users, and approved business questions.
- The chosen SQL tool or MCP runtime, when known.
- The access owner's decisions on tables, columns, tenant scope, and query limits.

Use the existing SQL tool when it meets the requirements. Do not add a connector or choose a framework without need.
If runtime details are absent, prepare the setup files and list the missing decisions.
Ask for details only when they block the next implementation step. Do not invent access rights or limit values.

## Method

1. Read [templates.md](templates.md). Check that the model covers the intended query scope.
   Resolve this skill's absolute folder path. From the working project root, run:

   ```bash
   python3 <absolute-skill-folder>/scripts/prepare_context.py output/schema-map/[PN]-schema-model.json output/text-to-sql-setup/[PN]-query-context.json
   ```

   The helper checks local files only. It makes no database connection.
   If it rejects the model, report the specific blockers. Keep the setup status `blocked_schema`.
   Return the model for SME review. Do not change its status or remove questions to force acceptance.
   For narrower scope, obtain a revised scoped model with its own SME decision.
2. Inspect the existing tool or chosen runtime. Read [references/runtime-controls.md](references/runtime-controls.md).
   Use official documentation for the installed version before changing configuration or implementation.
   Record which controls the database enforces and which the application enforces.
3. Define the permitted tables, columns, joins, calculations, and filters for each intended query.
   Use only confirmed meanings and approved relationships from the query context.
   Do not infer extra joins from similar column names. Ask for clarification when a question needs an unavailable definition.
   Confirm each table's explicit row scope. Keep every required scope pair and complete key in approved joins.
4. Define user identity, tenant scope, read-only database rights, secret storage, and query limits.
   Bind access scope from the authenticated caller. A model-generated tenant value cannot grant access.
   Record an owner and test for each control. A written policy is not proof of enforcement.
5. Build query evaluation cases from the confirmed SME examples.
   Include expected results or invariants, input identity, permitted parameters, and comparison rules.
   Include refusals for unavailable meanings, forbidden fields, tenant changes, writes, and unapproved joins.
   Include timeout and result-limit cases. Keep unrun tests marked `not_run`.
6. When the runtime is selected and implementation is requested, create or update its local code and configuration.
   Follow the target repository's conventions. Keep credentials out of tracked files.
   Enforce the access rules outside the language model. Use parameters for values and dialect-aware SQL validation.
   A read-only transaction, SQL prefix check, or prompt alone is insufficient.
7. Run the selected runtime's checks against an authorised test database or synthetic fixture.
   Verify tenant isolation, field access, query limits, approved results, and refusal cases through the actual query path.
   Record versions, commands, results, and remaining gaps. Do not report a fixture test as a live database check.
8. Set `ready_for_trial` only when required controls and query cases pass in the target test runtime.
   Use `blocked_setup` when decisions, implementation, or checks remain absent.
   State the intended users and scope. Do not label the solution production-ready from this workflow alone.

## Output

Create `output/text-to-sql-setup/` in the working project before writing files.
Use this folder for all files this skill produces, unless the user gives another path.

Write these files to `output/text-to-sql-setup/` in the working project:

- `[PN]-query-context.json`: generated physical structure, confirmed meanings, approved joins, and confirmed query cases.
- `[PN]-query-access.md`: the access rules, their owners, and evidence of enforcement.
- `[PN]-query-evaluation.json`: accepted and refused cases, expected behavior, and recorded results.
- `[PN]-text-to-sql-setup.md`: selected runtime, local changes, open decisions, checks, and trial status.

If the schema check fails, produce only the setup report with `blocked_schema` and its blockers.
An existing context file may be stale. Do not use it after a failed check. Do not delete it without instruction.
Treat prepared access rules and evaluation files as drafts until the access owner and target checks confirm them.

## Voice

Use short, clear sentences. Define technical terms. State facts and identify assumptions. Use the template formats and identifiers exactly.

## Examples

The examples are synthetic. They grant no access to a real database.
See [examples/input-schema-model.json](examples/input-schema-model.json),
[examples/input-sme-answers.md](examples/input-sme-answers.md), [examples/example-query-context.json](examples/example-query-context.json),
[examples/example-query-access.md](examples/example-query-access.md), [examples/example-query-evaluation.json](examples/example-query-evaluation.json),
and [examples/example-output.md](examples/example-output.md).
