#!/usr/bin/env python3
"""Trace review paths in supplied links. No source files or database are changed."""
import json
from pathlib import Path
import sys


def require_text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be nonempty text.")


def analyse_links(graph: dict, changed_ids: list[str]) -> dict:
    if not isinstance(graph, dict) or type(graph.get("trace_version")) is not int or graph["trace_version"] != 1:
        raise ValueError("Unsupported trace graph version.")
    require_text(graph["scope"], "Scope")
    if not isinstance(graph["nodes"], list) or not isinstance(graph["links"], list):
        raise ValueError("Nodes and links must be lists.")
    nodes = {}
    for node in graph["nodes"]:
        if not isinstance(node, dict):
            raise ValueError("Each node must be a record.")
        for field in ("id", "kind", "label", "source"):
            require_text(node[field], f"Node {field}")
        if node["id"] in nodes:
            raise ValueError(f"Duplicate node ID: {node['id']}")
        nodes[node["id"]] = node
    if not changed_ids:
        raise ValueError("Supply at least one changed ID.")
    for identifier in changed_ids:
        require_text(identifier, "Changed ID")
        if identifier not in nodes:
            raise ValueError(f"Changed ID has no source record: {identifier}")

    recorded = {identifier: set() for identifier in nodes}
    combined = {identifier: set() for identifier in nodes}
    gaps = []
    for link in graph["links"]:
        if not isinstance(link, dict):
            raise ValueError("Each link must be a record.")
        for field in ("from", "to", "relationship", "status", "source"):
            require_text(link[field], f"Link {field}")
        if link["status"] not in ("recorded", "proposed"):
            raise ValueError("Link status must be recorded or proposed.")
        missing = sorted({link["from"], link["to"]} - nodes.keys())
        if missing:
            gaps.append({**link, "missing_ids": missing})
            continue
        combined[link["from"]].add(link["to"])
        if link["status"] == "recorded":
            recorded[link["from"]].add(link["to"])

    def reachable(adjacency):
        seen = set(changed_ids)
        pending = list(seen)
        while pending:
            identifier = pending.pop()
            for target in adjacency[identifier] - seen:
                seen.add(target)
                pending.append(target)
        return seen

    direct = reachable(recorded)
    possible = reachable(combined)
    return {
        "scope": graph["scope"],
        "changed_ids": sorted(set(changed_ids)),
        "review_required": sorted(direct - set(changed_ids)),
        "possible_review": sorted(possible - direct),
        "gaps": gaps,
        "coverage": "partial" if gaps else "supplied_links_only",
    }


def main() -> None:
    if len(sys.argv) < 3:
        sys.exit("Usage: analyse_links.py <trace-links.json> <changed-id> [other-changed-ids]")
    try:
        graph = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        result = analyse_links(graph, sys.argv[2:])
    except (OSError, ValueError, KeyError, TypeError) as error:
        sys.exit(f"Trace analysis rejected: {error}")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
