# Templates — Requirement Construction II (JIRA)

## .env variables

| Variable | Example | Purpose |
| :--- | :--- | :--- |
| `JIRA_BASE_URL` | `https://yourco.atlassian.net` | JIRA Cloud base URL |
| `JIRA_EMAIL` | `you@company.com` | Account email (basic auth) |
| `JIRA_API_TOKEN` | `ATATT...` | API token from id.atlassian.com → Security → API tokens |
| `JIRA_PROJECT` | `CTT` | Target project key |

All four are required for JIRA output. If any is missing, the skill stays local-only and says which one.

## Story mapping

| Local (Markdown) | JIRA |
| :--- | :--- |
| Story sentence ("As a...") | Summary |
| Scenarios + acceptance criteria | Description (Markdown) |
| Local ID `[PN]US###` | Kept in the description; JIRA key written back into the local file |

## Write-back format

```markdown
## NWUS001 (PROJ-123)
As a ...
```

## Rules

- Issue type: `Story`. Project: only `JIRA_PROJECT`.
- Never modify or delete existing JIRA issues.
- Never print credentials.
