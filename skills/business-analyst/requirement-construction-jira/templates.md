# Templates — Requirement Construction II (JIRA)

## .env variables

| Variable | Example | Purpose |
| :--- | :--- | :--- |
| `JIRA_BASE_URL` | `https://yourco.atlassian.net` | JIRA Cloud base URL |
| `JIRA_EMAIL` | `you@company.com` | Account email (basic auth) |
| `JIRA_API_TOKEN` | `ATATT...` | API token from id.atlassian.com → Security → API tokens |
| `JIRA_PROJECT` | `CTT` | Target project key |

All four are required for JIRA output. If any is missing, the skill stays local-only and says which one.
Environment variables take precedence over `.env` values.

## Story mapping

| Local (Markdown) | JIRA |
| :--- | :--- |
| Story sentence ("As a..." or "As an...") | Summary |
| Local ID and complete story content | Description (Markdown) |
| Local ID `[PN]US###` | Kept in the description; JIRA key written back into the local file |

## Write-back format

```markdown
## NWUS001 (PROJ-123)
Source use case: NWUC001
As a ...
```

The script saves each key before the next request. It skips stories with recorded keys.

Before a request, the heading is `## NWUS001 (JIRA pending)`. This marker blocks another run if the result is unknown. Check JIRA for the local ID. Record the existing issue key, or remove the marker only after confirming that no issue exists.

## Rules

- Issue type: `Story`. Project: only `JIRA_PROJECT`.
- Never modify or delete existing JIRA issues.
- Never print credentials.
