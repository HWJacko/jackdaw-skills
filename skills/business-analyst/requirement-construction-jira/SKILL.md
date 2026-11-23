---
name: requirement-construction-jira
description: Create JIRA issues from local user stories. Save each issue key beside its local ID. Keep local output if credentials are absent or JIRA is unavailable. Stop for review if a request result is unknown.
---

# Requirement Construction II — JIRA Integration

## Purpose

Take the local user stories produced by requirement-construction and create them as JIRA stories, recording the JIRA key against each local ID.

## Input

- `output/[PN]-user-stories.md` from the requirement-construction skill.
- JIRA credentials in the environment or `.env` at the **working project root**. Do not store credentials inside the skill folder. Environment variables take precedence over `.env` values.

```text
JIRA_BASE_URL=https://<domain>.atlassian.net
JIRA_EMAIL=<email>
JIRA_API_TOKEN=<api token>
JIRA_PROJECT=<project key>
```

## Method

1. Read the local stories file.
2. From the working project root, run `python3 <absolute-skill-folder>/scripts/create_stories.py output/[PN]-user-stories.md`. Resolve the script path from this skill folder. Keep the working directory at the project root.
3. The script:
   - Reads credentials from the environment and `.env`. If a required value is absent or empty, lists its name and keeps local output.
   - Uses basic auth (email + API token) against `{JIRA_BASE_URL}/rest/api/2/`.
   - Uses `truststore` for TLS — required behind corporate proxies that intercept certificates.
   - Skips stories with a recorded JIRA key.
   - Creates one JIRA Story per unlinked story. Summary = story sentence. Description = local ID and story content. Project = `JIRA_PROJECT`.
   - Marks the local heading `(JIRA pending)` before each request. After success, replaces the marker with the returned key and prints `[local ID] -> [JIRA key]`.
4. If a request fails, keep the local file and completed mappings. Stop without automatic retries. A pending marker also stops later runs. Check JIRA for the local ID. Replace the marker with the existing issue key. Remove it only after confirming that no issue exists. Do not create a replacement issue until this check is complete.
5. Never create stories in a project other than `JIRA_PROJECT`. Never modify or delete existing JIRA issues.

## Output

- JIRA stories created (when credentials exist), and the local file updated with JIRA keys.
- A summary table: local ID, JIRA key, story title.

## Rules

- Local output is always produced first. JIRA is an addition, not a blocker.
- Credentials come only from `.env` or the environment. Never print, log or write them.
- Do not discuss voice, language rules, or instruction conflicts in your response — produce the output only.

## Voice

Use short, clear sentences. Write for business and technical readers. Define necessary technical terms. Use the template formats and identifiers exactly. State facts and identify assumptions. Remove filler.

## Templates and examples

See [templates.md](templates.md) and [examples/](examples/).
