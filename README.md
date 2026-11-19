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
cp -r jackdaw-skills/skills/business-analyst/* ~/.claude/skills/
```

Or use `<project>/.claude/skills/` for one project only (committable, so the team gets it too). Skills run as `/use-case-extraction` etc. **Restart the session after copying** — skills are loaded at startup.

**Codex:** copy skill folders into `~/.agents/skills/` (all projects) or `<repo>/.agents/skills/` (one repo):

```bash
git clone https://github.com/hwjacko/jackdaw-skills.git
cp -r jackdaw-skills/skills/business-analyst/* ~/.agents/skills/
```

Invoke with `$use-case-extraction` or describe the task. The `.claude-plugin/marketplace.json` manifest is Claude Code only; Codex ignores it.

## Invoke

After install, describe the task in natural language or use the slash command. The agent matches the task to the skill's `description` in `SKILL.md`. Example: "Extract use cases from these meeting notes."

## Voice

All skills follow [voice.md](voice.md): concise and clear, understandable by business and tech alike. A skill can override it.

## Roadmap

- **Phase 1A** — Business Analyst: Use Case Extraction, Requirement Construction I (local only)
- **Phase 1B** — Business Analyst: User Flow [VISUAL], Requirements Map [VISUAL] (Mermaid + draw.io XML always; PNG when the drawio CLI is installed; drawio files import into Lucidchart)
- **Phase 1C** — Business Analyst: SWOT analysis
- **Phase 1D** — Business Analyst: Requirement Construction II (JIRA integration; local file fallback)
- **Phase 2** — Data Analyst: Schema Map, Schema Map [VISUAL]. Product Manager / Product Owner TBC.
