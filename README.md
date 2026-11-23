# jackdaw-skills

A shareable repository of agent skills for business and product functions. Public on GitHub. Add it to Claude Code or Codex for quick deployment.

## Functions covered

- Business Analyst (Phase 1)
- Data Analyst (Phase 2)
- Product Manager (TBC)
- Product Owner (TBC)

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
```

Or use `<project>/.claude/skills/` for one project only (committable, so the team gets it too). Skills run as `/use-case-extraction` etc. **Restart the session after copying** — skills are loaded at startup.

**Codex:** copy skill folders into `~/.agents/skills/` (all projects) or `<repo>/.agents/skills/` (one repo):

```bash
git clone https://github.com/hwjacko/jackdaw-skills.git
mkdir -p ~/.agents/skills
cp -r jackdaw-skills/skills/business-analyst/* ~/.agents/skills/
cp -r jackdaw-skills/skills/data-analyst/* ~/.agents/skills/
```

Invoke with `$use-case-extraction` or describe the task. The `.claude-plugin/marketplace.json` manifest is Claude Code only; Codex ignores it.

## Database schema discovery

Use `schema-map` to inspect a database through an existing read-only SQL tool, or supply SQL schema files.
No new database connector is required. The skill produces:

- `output/[PN]-schema-model.json`: database structure, claims, evidence, questions, and handoff status.
- `output/[PN]-schema-map.md`: the assumed schema and its limits.
- `output/[PN]-sme-questions.md`: decisions for a subject matter expert (SME).

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

Example request: "Use this confirmed schema model to prepare our existing SQL tool for text-to-SQL."

Select the runtime and confirm access rules before implementation. The skill can then create local code and configuration.
If those decisions are absent, it produces a blocked setup report and the files that can be prepared.
Read-only access, tenant scope, and limits must be enforced and tested through the chosen runtime.
The query context records runtime controls as `not_assessed` and grants no query access.

## Optional: styled diagrams

The [VISUAL] skills (user-flow, requirements-map) produce Mermaid and draw.io by default — no dependencies. For presentation-grade, on-brand diagrams (52 types, brand colors/fonts from a URL, SVG/PNG export), install the optional [diagram-design](https://github.com/cathrynlavery/diagram-design) skill:

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

## Roadmap

- **Phase 1A** — Business Analyst: Use Case Extraction, Requirement Construction I (local only)
- **Phase 1B** — Business Analyst: User Flow [VISUAL], Requirements Map [VISUAL] (Mermaid + draw.io XML always; PNG when the drawio CLI is installed; drawio files import into Lucidchart)
- **Phase 1C** — Business Analyst: SWOT analysis
- **Phase 1D** — Business Analyst: Requirement Construction II (JIRA integration; local file fallback)
- **Phase 2A** — Data Analyst: Schema Map. Read-only discovery, assumed business meanings, SME questions, and a JSON handoff model.
- **Phase 2B** — Data Analyst: Schema Map [VISUAL]. Diagrams that preserve relationship status and open questions.
- **Phase 2C** — Text-to-SQL Setup: confirmed schema handoff, MCP or SQL-tool setup, access rules, and query evaluation.
- **Later scope** — Product Manager / Product Owner TBC.
