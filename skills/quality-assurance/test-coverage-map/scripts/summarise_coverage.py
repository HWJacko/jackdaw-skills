#!/usr/bin/env python3
"""Summarise supplied criteria and execution records. This does not run tests."""
import json
from pathlib import Path
import sys


def require_text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be nonempty text.")


def index_records(value, fields, label):
    if not isinstance(value, list):
        raise ValueError(f"{label} must be a list.")
    indexed = {}
    for item in value:
        if not isinstance(item, dict):
            raise ValueError(f"Each {label} entry must be a record.")
        for field in fields:
            require_text(item[field], f"{label} {field}")
        if item["id"] in indexed:
            raise ValueError(f"Duplicate {label} ID: {item['id']}")
        indexed[item["id"]] = item
    return indexed


def summarise_coverage(register: dict) -> dict:
    if not isinstance(register, dict) or type(register.get("coverage_version")) is not int or register["coverage_version"] != 1:
        raise ValueError("Unsupported coverage register version.")
    require_text(register["scope"], "Scope")
    criteria = index_records(register["criteria"], ("id", "story_id", "revision", "status", "source"), "criterion")
    tests = index_records(register["tests"], ("id", "revision", "design_status", "source"), "test")
    results = index_records(register["results"], ("id", "test_id", "test_revision", "status", "environment", "observed", "source"), "result")
    if len(set(criteria) | set(tests) | set(results)) != len(criteria) + len(tests) + len(results):
        raise ValueError("Qualify IDs that collide across record types.")
    for criterion in criteria.values():
        if criterion["status"] not in ("agreed", "proposed", "conflicting", "unknown"):
            raise ValueError("Invalid criterion status.")
    gaps = [] if criteria else ["No acceptance criteria supplied."]
    for result in results.values():
        if result["status"] not in ("passed", "failed", "blocked"):
            raise ValueError("Invalid execution result status.")
        if result["test_id"] not in tests:
            gaps.append(f"Result {result['id']} refers to a missing test.")

    mappings = {identifier: [] for identifier in criteria}
    test_rows = {}
    for test in tests.values():
        if test["design_status"] not in ("ready", "blocked"):
            raise ValueError("Invalid test design status.")
        test_gaps = [] if test["design_status"] == "ready" else ["test design blocked"]
        refs = test["criterion_refs"]
        if not isinstance(refs, list):
            raise ValueError("Criterion references must be a list.")
        seen = set()
        for ref in refs:
            if not isinstance(ref, dict):
                raise ValueError("Each criterion reference must be a record.")
            require_text(ref["id"], "Criterion reference ID")
            require_text(ref["revision"], "Criterion reference revision")
            if ref["id"] in seen:
                raise ValueError("A test contains duplicate criterion references.")
            seen.add(ref["id"])
            if ref["id"] not in criteria:
                test_gaps.append(f"missing criterion {ref['id']}")
            else:
                mappings[ref["id"]].append(test["id"])
                if ref["revision"] != criteria[ref["id"]]["revision"]:
                    test_gaps.append(f"stale criterion reference {ref['id']}")
        if not refs:
            test_gaps.append("no criterion references")

        result_id = test["current_result_id"]
        status = "not_run"
        if result_id is None:
            test_gaps.append("no current result")
        else:
            require_text(result_id, "Current result ID")
            result = results.get(result_id)
            if result is None or result["test_id"] != test["id"]:
                status = "unknown"
                test_gaps.append(f"missing or mismatched result {result_id}")
            else:
                status = result["status"]
                if result["test_revision"] != test["revision"]:
                    test_gaps.append(f"stale result {result_id}")
        test_rows[test["id"]] = {
            "id": test["id"], "design_status": test["design_status"], "result_id": result_id,
            "recorded_status": status, "current": not test_gaps, "gaps": test_gaps,
        }

    criterion_rows = []
    for criterion in criteria.values():
        linked = mappings[criterion["id"]]
        criterion_gaps = [] if criterion["status"] == "agreed" else [f"criterion is {criterion['status']}"]
        if not linked:
            criterion_gaps.append("no mapped tests")
        for identifier in linked:
            row = test_rows[identifier]
            if not row["current"] or row["recorded_status"] != "passed":
                detail = "; ".join(row["gaps"]) if row["gaps"] else f"reported {row['recorded_status']}"
                criterion_gaps.append(f"{identifier}: {detail}")
        criterion_rows.append({
            "id": criterion["id"], "story_id": criterion["story_id"], "status": criterion["status"],
            "mapped_tests": linked, "verified": not criterion_gaps, "gaps": criterion_gaps,
        })
    return {
        "scope": register["scope"], "coverage": "supplied_criteria_only",
        "criteria": criterion_rows, "tests": list(test_rows.values()), "gaps": gaps,
        "summary": {"criteria": len(criteria), "mapped": sum(bool(row["mapped_tests"]) for row in criterion_rows),
                    "verified": sum(row["verified"] for row in criterion_rows)},
    }


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("Usage: summarise_coverage.py <test-register.json>")
    try:
        register = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        summary = summarise_coverage(register)
    except (OSError, ValueError, KeyError, TypeError) as error:
        sys.exit(f"Coverage register rejected: {error}")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
