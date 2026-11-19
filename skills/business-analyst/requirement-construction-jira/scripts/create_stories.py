#!/usr/bin/env python3
"""Create JIRA stories from a requirement-construction output file.

Usage: create_stories.py <stories-file.md>

Reads JIRA credentials from .env in the current directory:
  JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN, JIRA_PROJECT

Prints one line per story: <local ID> -> <JIRA key>
"""
import os
import re
import sys

import truststore
truststore.inject_into_ssl()

import requests
from requests.auth import HTTPBasicAuth


def load_env(path: str = ".env") -> dict[str, str]:
    env: dict[str, str] = {}
    if not os.path.exists(path):
        return env
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env


def parse_stories(text: str) -> list[dict]:
    """Split the stories file into {local_id, title, body} entries."""
    stories = []
    # Headings: ## NWUS001 or ## NWUS001 (PROJ-123)
    parts = re.split(r"^## ", text, flags=re.M)[1:]
    for part in parts:
        lines = part.splitlines()
        header = lines[0].strip()
        m = re.match(r"([A-Z]+US\d+)", header)
        if not m:
            continue
        local_id = m.group(1)
        body_lines = lines[1:]
        title = next((ln.strip() for ln in body_lines if ln.strip().lower().startswith("as a ")), header)
        body = "\n".join(body_lines).strip()
        stories.append({"local_id": local_id, "title": title, "body": body})
    return stories


def create_story(base: str, auth: HTTPBasicAuth, project: str, title: str, body: str) -> str:
    payload = {
        "fields": {
            "project": {"key": project},
            "summary": title[:255],
            "description": body,
            "issuetype": {"name": "Story"},
        }
    }
    r = requests.post(f"{base}/rest/api/2/issue", json=payload, auth=auth, timeout=30)
    r.raise_for_status()
    return r.json()["key"]


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("Usage: create_stories.py <stories-file.md>")
    with open(sys.argv[1]) as f:
        text = f.read()

    env = load_env()
    missing = [k for k in ("JIRA_BASE_URL", "JIRA_EMAIL", "JIRA_API_TOKEN", "JIRA_PROJECT") if not env.get(k)]
    if missing:
        sys.exit(f"Missing .env variables: {', '.join(missing)}")

    auth = HTTPBasicAuth(env["JIRA_EMAIL"], env["JIRA_API_TOKEN"])
    stories = parse_stories(text)
    if not stories:
        sys.exit("No stories found (headings like '## XXUS001').")

    for s in stories:
        key = create_story(env["JIRA_BASE_URL"], auth, env["JIRA_PROJECT"], s["title"], s["body"])
        print(f"{s['local_id']} -> {key}")


if __name__ == "__main__":
    main()
