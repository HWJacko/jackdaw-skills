# jackdaw-skills

A shareable repository of agent skills for business and product functions. Public on GitHub. Add it to Claude Code or Codex for quick deployment.

## Functions covered

- Business Analyst (Phase 1)
- Data Analyst (Phase 2)
- Product Manager (Phase 3)
- Product Owner (Phase 4)
- User Research (Phase 5)
- Quality Assurance (Phase 6)

## Structure

```text
skills/
└── <function>/
    └── <skill-name>/
        ├── SKILL.md        # Standard skill file: metadata + instructions
        ├── templates.md    # Output formats and identifiers
        └── examples/       # Worked examples
```

The standard is the Claude Code skill format: one folder per skill, instructions in `SKILL.md`.

## Install

**Claude Code — plugin marketplace (recommended):**

```text
/plugin marketplace add hwjacko/jackdaw-skills
/plugin install jackdaw-skills@jackdaw-skills
```

Skills then run as `/jackdaw-skills:use-case-extraction`, `/jackdaw-skills:requirement-construction`, etc.

**Claude Code — manual copy:**

```bash
git clone https://github.com/hwjacko/jackdaw-skills.git
mkdir -p ~/.claude/skills
cp -r jackdaw-skills/skills/business-analyst/* ~/.claude/skills/
cp -r jackdaw-skills/skills/data-analyst/* ~/.claude/skills/
cp -r jackdaw-skills/skills/product-manager/* ~/.claude/skills/
cp -r jackdaw-skills/skills/product-owner/* ~/.claude/skills/
cp -r jackdaw-skills/skills/user-research/* ~/.claude/skills/
cp -r jackdaw-skills/skills/quality-assurance/* ~/.claude/skills/
```

Or use `<project>/.claude/skills/` for one project only (committable, so the team gets it too). Skills run as `/use-case-extraction` etc. **Restart the session after copying** — skills are loaded at startup.

**Codex:** copy skill folders into `~/.agents/skills/` (all projects) or `<repo>/.agents/skills/` (one repo):

```bash
git clone https://github.com/hwjacko/jackdaw-skills.git
mkdir -p ~/.agents/skills
cp -r jackdaw-skills/skills/business-analyst/* ~/.agents/skills/
cp -r jackdaw-skills/skills/data-analyst/* ~/.agents/skills/
cp -r jackdaw-skills/skills/product-manager/* ~/.agents/skills/
cp -r jackdaw-skills/skills/product-owner/* ~/.agents/skills/
cp -r jackdaw-skills/skills/user-research/* ~/.agents/skills/
cp -r jackdaw-skills/skills/quality-assurance/* ~/.agents/skills/
```

Invoke with `$use-case-extraction` or describe the task. The `.claude-plugin/marketplace.json` manifest is Claude Code only; Codex ignores it.

## Output folders

Each skill writes to `output/<skill-name>/` in the working project, unless you give another path.
The skill creates its folder before writing files. Reports, data files, and diagrams stay together.
For example:

```text
output/
├── use-case-extraction/
│   └── APP-use-cases.md
├── requirement-construction/
│   └── APP-user-stories.md
├── user-flow/
│   ├── APP-user-flow-APPEP001.md
│   └── APP-user-flow-APPEP001.drawio
└── requirements-map/
    ├── APP-requirements-map.md
    └── APP-requirements-map.drawio
```

Skills read inputs from the supplied paths or the producing skill's folder.
For example, Test Coverage Map reads `output/acceptance-test-design/[PN]-test-register.json`
and writes its diagrams to `output/test-coverage-map/`.
Jira integration keeps a separate stories copy in `output/requirement-construction-jira/`
so it can retain issue keys and pending markers between runs.

## Database schema discovery

Use `schema-map` to inspect a database through an existing read-only SQL tool, or supply SQL schema files.
No new database connector is required. The skill produces:

- `output/schema-map/[PN]-schema-model.json`: database structure, claims, evidence, questions, and handoff status.
- `output/schema-map/[PN]-schema-map.md`: the assumed schema and its limits.
- `output/schema-map/[PN]-sme-questions.md`: decisions for a subject matter expert (SME).

Example request: "Inspect this schema for paid revenue by customer. Show assumed joins and questions for the SME."

The skill separates observed structure from assumed business meanings. It keeps composite and tenant keys intact.
It records open questions about row grain, measures, dates, access rules, and expected query results.
After SME answers arrive, use the same skill to update the model and its handoff status.

Use `schema-map-visual` with that model for matching Mermaid and draw.io diagrams.
Assumed relationships stay labelled as assumptions. A diagram does not approve a join for query use.

## Text-to-SQL setup

Use `text-to-sql-setup` after SME review. It can prepare an MCP (Model Context Protocol) or text-to-SQL solution.
The skill checks the schema handoff and prepares query context, access rules, evaluation cases, and a setup report.
Its local helper rejects open schema blockers. It exports only confirmed meanings and approved joins.
Each table needs SME-confirmed `row_scope` columns before query setup. A confirmed empty list means global scope.
The helper checks scope pairs and complete keys for approved joins. Existing models need a scope review before export.

Example request: "Use this confirmed schema model to prepare our existing SQL tool for text-to-SQL."

Select the runtime and confirm access rules before implementation. The skill can then create local code and configuration.
If those decisions are absent, it produces a blocked setup report and the files that can be prepared.
Read-only access, tenant scope, and limits must be enforced and tested through the chosen runtime.
The query context records runtime controls as `not_assessed` and grants no query access.

## Product planning and backlog work

| Function | Skill | Output |
| --- | --- | --- |
| Product Manager | `problem-framing` | problem, source evidence, intended outcomes, and measures |
| Product Manager | `opportunity-assessment` | needs, options, assumptions, tests, and a visual opportunity map |
| Product Manager | `outcome-roadmap` | Now/Next/Later roadmap with measures, review conditions, and a visual sequence |
| Product Manager | `outcome-review` | actual results, comparison limits, and a proposed next decision |
| Product Owner | `backlog-prioritisation` | explained backlog order, prerequisites, and unresolved comparisons |
| Product Owner | `backlog-refinement` | review findings and proposed edits to existing stories |
| Product Owner | `release-scope` | candidate release, exclusions, dependencies, conditions, and a visual scope map |

Start with a problem frame. Assess options and plan intended outcomes before constructing use cases and stories.
Review and order the existing backlog, propose release scope, then compare results with the intended outcomes.
The Business Analyst skills remain the route for use case extraction and story construction.

Example request: "Build a visual outcome roadmap from these goals. Keep unconfirmed targets and dates clearly labelled."

Opportunity Assessment, Outcome Roadmap, and Release Scope produce Mermaid in Markdown and matching draw.io XML.
PNG is optional when the drawio CLI is installed. Roadmaps use undated horizons unless source dates are supplied.
The skills retain source IDs, distinguish evidence from assumptions, and leave missing estimates or measures unknown.
They prepare local recommendations. External backlog changes and release actions require a user instruction.

## Evidence, measures, and change review

| Function | Skill | Output |
| --- | --- | --- |
| User Research | `research-synthesis` | sourced observations, interpreted findings, contrary evidence, sample limits, and an evidence map |
| Data Analyst | `metric-definition` | measure rules, source fields, calculation cases, comparability limits, and optional SQL |
| Business Analyst | `change-impact-analysis` | downstream review paths, proposed associations, missing links, and an impact map |

Research synthesis supplies evidence for problem framing. Metric definition specifies how an outcome will be measured.
Change-impact analysis follows documented links when a source, rule, metric, or requirement changes.

Problem, use-case, story, requirements-map, and outcome-review templates retain source IDs and trace-link tables.
Links run from source to dependent. `recorded` means an explicit source link; `proposed` means an association needing review.
These statuses do not approve a business decision or prove a test passed. Missing IDs remain gaps.
The impact helper reads a supplied JSON register. It does not discover unrecorded work or claim complete coverage.

Research and impact maps include Mermaid and matching draw.io XML. PNG is optional when drawio is available.

## Acceptance testing and coverage

Use `acceptance-test-design` to derive versioned cases from supplied stories, criteria, and business rules.
It records normal, error, and boundary cases where the source supports an expected result.
Conflicting rules and missing oracles remain blocked. New unrun cases have no result record.

Use `test-coverage-map` to connect stories and criteria to tests and execution evidence.
The map separates mapped coverage from current passing evidence. Old results do not verify changed criteria or test revisions.
Unknown, proposed, and conflicting criteria remain unresolved. The map includes Mermaid and matching draw.io XML.

The local helper reads a JSON test register. It does not execute cases or approve a release.
All mapped tests are required within that register. Counts describe the supplied criteria, not universal coverage.

See the [full worked example](examples/quality-workflow/workflow.md) for research through outcome review.
It retains missing evidence and conflicting rules. One actual SQL fixture case passes; other checks remain unrun or unresolved.
The example is an author-run exercise. It is not an independent model evaluation or a target-application acceptance run.

## Optional: styled diagrams

The main diagram outputs use Mermaid and draw.io — no dependencies. For presentation-grade, on-brand diagrams (52 types, brand colors/fonts from a URL, SVG/PNG export), install the optional [diagram-design](https://github.com/cathrynlavery/diagram-design) skill:

```text
/plugin marketplace add cathrynlavery/diagram-design
```

When installed, the [VISUAL] skills offer it as an extra render step. It is never required.

## Invoke

After install, describe the task in natural language or use the slash command. The agent matches the task to the skill's `description` in `SKILL.md`. Example: "Extract use cases from these meeting notes."

## Voice

Each skill includes the rules from [voice.md](voice.md). The rules stay available when a skill folder is copied.

## Checks

Run these commands from the repository root:

```bash
python3 -m pip install -r requirements.txt
python3 -m unittest discover -s tests -v
```

The tests check JIRA behavior with simulated responses. They also check plugin paths, skill references, and diagram examples.
Schema examples are checked against a local SQLite database built from the supplied fixture.
Setup tests check schema handoff rejection, confirmed context, and expected tenant-specific counts.
Product examples check diagram consistency, source IDs, release dependencies, and outcome calculations.
Evidence tests check distinct participant counts, contrary observations, metric edge cases, and recorded or proposed impact paths.
QA tests check mappings, current result selection, version changes, and unresolved criteria.
The worked example reruns its named SQLite fixture and checks its source links and coverage summary.

## Roadmap

- **Phase 1A** — Business Analyst: Use Case Extraction, Requirement Construction I (local only)
- **Phase 1B** — Business Analyst: User Flow [VISUAL], Requirements Map [VISUAL] (Mermaid + draw.io XML always; PNG when the drawio CLI is installed; drawio files import into Lucidchart)
- **Phase 1C** — Business Analyst: SWOT analysis
- **Phase 1D** — Business Analyst: Requirement Construction II (JIRA integration; local file fallback)
- **Phase 1E** — Business Analyst: Change-Impact Analysis, with documented trace links and an impact map.
- **Phase 2A** — Data Analyst: Schema Map. Read-only discovery, assumed business meanings, SME questions, and a JSON handoff model.
- **Phase 2B** — Data Analyst: Schema Map [VISUAL]. Diagrams that preserve relationship status and open questions.
- **Phase 2C** — Text-to-SQL Setup: confirmed schema handoff, MCP or SQL-tool setup, access rules, and query evaluation.
- **Phase 2D** — Data Analyst: Metric Definition, with population rules, source fields, and calculation checks.
- **Phase 3** — Product Manager: Problem Framing, Opportunity Assessment, Outcome Roadmap, and Outcome Review.
- **Phase 4** — Product Owner: Backlog Prioritisation, Backlog Refinement, and Release Scope.
- **Phase 5** — User Research: Research Synthesis, with source observations, contrary evidence, and an evidence map.
- **Phase 6** — Quality Assurance: Acceptance Test Design and Test Coverage Map, with versioned execution evidence.
