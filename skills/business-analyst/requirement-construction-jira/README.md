# Requirement Construction II — JIRA

Creates JIRA stories from a local `[PN]-user-stories.md` file.

## Setup

Run from the working project root. Set `JIRA_SKILL_DIR` to the absolute path of this installed skill folder.

```bash
JIRA_SKILL_DIR="/absolute/path/to/requirement-construction-jira"
python3 -m pip install -r "$JIRA_SKILL_DIR/requirements.txt"
```

Add to `.env` in **your working project root** (the project you are analysing — never inside this skill folder):

```text
JIRA_BASE_URL=https://<domain>.atlassian.net
JIRA_EMAIL=<email>
JIRA_API_TOKEN=<token from id.atlassian.com>
JIRA_PROJECT=<project key>
```

You can also set these environment variables. They take precedence over `.env` values.

## Run

```bash
python3 "$JIRA_SKILL_DIR/scripts/create_stories.py" "output/[PN]-user-stories.md"
```

The script saves each returned key in the local heading and prints `LOCAL-ID -> JIRA-KEY`. It skips stories with recorded keys.

If credentials are incomplete, the script lists the missing variable names. The local file stays unchanged.

Before each request, the script saves a `(JIRA pending)` marker. If JIRA fails, the script stops and keeps completed mappings. It does not print credentials or request errors.

A pending marker blocks later runs. Check JIRA for the local ID first. Replace the marker with the existing issue key. Remove it only after confirming that no issue exists. Then run the script again.
