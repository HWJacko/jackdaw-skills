# Requirement Construction II — JIRA

Creates JIRA stories from a local `[PN]-user-stories.md` file.

## Setup

```bash
pip install -r requirements.txt
```

Add to `.env` in **your working project root** (the project you are analysing — never inside this skill folder):

```text
JIRA_BASE_URL=https://<domain>.atlassian.net
JIRA_EMAIL=<email>
JIRA_API_TOKEN=<token from id.atlassian.com>
JIRA_PROJECT=<project key>
```

## Run

```bash
python3 scripts/create_stories.py ../../output/[PN]-user-stories.md
```

Prints `LOCAL-ID -> JIRA-KEY` per story. If `.env` is incomplete, exits with the missing variable names and changes nothing.
