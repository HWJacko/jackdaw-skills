---
name: requirement-construction-jira
description: Push user stories from requirement-construction output into JIRA, writing the JIRA key back next to each local ID. Falls back to local-only output if JIRA credentials are absent. Never fails when JIRA is unavailable.
---

# Requirement Construction II — JIRA Integration

## Purpose

Take the local user stories produced by requirement-construction and create them as JIRA stories, recording the JIRA key against each local ID.

## Input

- `output/[PN]-user-stories.md` from the requirement-construction skill.
- JIRA credentials in `.env` at the **working project root** (the project you are analysing — never inside the skill folder; skills are shared and get replaced on update):

```text
JIRA_BASE_URL=https://<domain>.atlassian.net
JIRA_EMAIL=<email>
JIRA_API_TOKEN=<api token>
JIRA_PROJECT=<project key>
```

## Method

1. Read the stories file. Parse each story: local ID, story sentence, scenarios, acceptance criteria.
2. Check `.env`. If any of the four variables is missing or empty, **stop at local output**: tell the user which variable is missing, keep the local file as the deliverable. Do not fail.
3. If credentials are present, run `scripts/create_stories.py <stories-file>`. The script:
   - Uses basic auth (email + API token) against `{JIRA_BASE_URL}/rest/api/2/`.
   - Uses `truststore` for TLS — required behind corporate proxies that intercept certificates.
   - Creates one JIRA Story per local story: summary = story sentence, description = scenarios + ACs in Markdown, project = `JIRA_PROJECT`.
   - Prints one line per story: `[local ID] -> [JIRA key]`.
4. Update `output/[PN]-user-stories.md`: append the JIRA key to each story heading, e.g. `## NWUS001 (PROJ-123)`.
5. Never create stories in a project other than `JIRA_PROJECT`. Never modify or delete existing JIRA issues.

## Output

- JIRA stories created (when credentials exist), and the local file updated with JIRA keys.
- A summary table: local ID, JIRA key, story title.

## Rules

- Local output is always produced first. JIRA is an addition, not a blocker.
- Credentials come only from `.env` or the environment. Never print, log or write them.
- Do not discuss voice, language rules, or instruction conflicts in your response — produce the output only.

## Voice

Follow the repository default ([voice.md](../../../voice.md)): concise and clear, understandable by business and tech alike.

## Templates and examples

See [templates.md](templates.md) and [examples/](examples/).
