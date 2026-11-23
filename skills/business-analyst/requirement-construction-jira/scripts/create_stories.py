#!/usr/bin/env python3
"""Create JIRA stories from a requirement-construction output file.

Usage: create_stories.py <stories-file.md>

Reads JIRA credentials from the environment or .env in the current directory:
  JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN, JIRA_PROJECT

Saves each JIRA key in the local heading and prints <local ID> -> <JIRA key>.
"""
import os
from pathlib import Path
import re
import sys
import tempfile

import truststore
truststore.inject_into_ssl()

import requests
from requests.auth import HTTPBasicAuth


VARIABLES = ("JIRA_BASE_URL", "JIRA_EMAIL", "JIRA_API_TOKEN", "JIRA_PROJECT")
PENDING = "JIRA pending"


def load_env(path: str = ".env") -> dict[str, str]:
    env: dict[str, str] = {}
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip()
    return {key: os.environ.get(key, env.get(key, "")) for key in VARIABLES}


def parse_stories(text: str) -> list[dict]:
    """Read story content and any recorded JIRA key or pending marker."""
    stories = []
    seen = set()
    parts = re.split(r"^## ", text, flags=re.M)[1:]
    for part in parts:
        lines = part.splitlines()
        header = lines[0].strip()
        m = re.fullmatch(r"([A-Z]+US\d+)(?: \(([A-Z][A-Z0-9_]*-\d+|JIRA pending)\))?", header)
        if not m:
            if re.match(r"[A-Z]+US\d+", header):
                raise ValueError(f"Invalid story heading: {header}")
            continue
        local_id = m.group(1)
        if local_id in seen:
            raise ValueError(f"Duplicate local ID: {local_id}")
        seen.add(local_id)
        body_lines = lines[1:]
        title = next((ln.strip() for ln in body_lines if re.match(r"as an? ", ln.strip(), re.I)), header)
        body = "\n".join(body_lines).strip()
        stories.append({"local_id": local_id, "title": title, "body": body, "jira_key": m.group(2)})
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
    r = requests.post(f"{base.rstrip('/')}/rest/api/2/issue", json=payload, auth=auth, timeout=30)
    r.raise_for_status()
    return r.json()["key"]


def save_heading(path: Path, text: str, local_id: str, marker: str) -> str:
    """Replace a heading and save the complete file before proceeding."""
    text = re.sub(
        rf"^## {re.escape(local_id)}(?: \([^\n]*\))?[ \t]*$",
        f"## {local_id} ({marker})", text, count=1, flags=re.M,
    )
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, delete=False) as f:
        temporary = Path(f.name)
        try:
            f.write(text)
            f.close()
            os.replace(temporary, path)
        finally:
            temporary.unlink(missing_ok=True)
    return text


def report_pending(local_id: str) -> None:
    print(f"Local output kept. Check JIRA for {local_id} before another run.")
    print("Replace '(JIRA pending)' with the issue key, or remove it only after confirming no issue exists.")


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("Usage: create_stories.py <stories-file.md>")
    path = Path(sys.argv[1])
    text = path.read_text(encoding="utf-8")
    try:
        stories = parse_stories(text)
    except ValueError as error:
        sys.exit(str(error))
    if not stories:
        sys.exit("No stories found (headings like '## XXUS001').")
    for s in stories:
        if s["jira_key"] == PENDING:
            report_pending(s["local_id"])
            return

    env = load_env()
    missing = [k for k in VARIABLES if not env.get(k)]
    if missing:
        print(f"Local output kept. Missing variables: {', '.join(missing)}")
        return

    auth = HTTPBasicAuth(env["JIRA_EMAIL"], env["JIRA_API_TOKEN"])
    for s in stories:
        local_id = s["local_id"]
        if s["jira_key"]:
            print(f"{local_id} -> {s['jira_key']} (already linked)")
            continue
        text = save_heading(path, text, local_id, PENDING)
        try:
            key = create_story(
                env["JIRA_BASE_URL"], auth, env["JIRA_PROJECT"],
                s["title"], f"Local ID: {local_id}\n\n{s['body']}",
            )
        except (requests.RequestException, ValueError, KeyError):
            report_pending(local_id)
            return
        print(f"{local_id} -> {key}", flush=True)
        text = save_heading(path, text, local_id, key)


if __name__ == "__main__":
    main()
