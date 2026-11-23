#!/usr/bin/env python3
"""Check a schema handoff and write query context. No database access is made."""
import json
from datetime import date
from pathlib import Path
import sys


def index_records(records: list[dict], label: str) -> dict[str, dict]:
    indexed = {record["id"]: record for record in records}
    if len(indexed) != len(records):
        raise ValueError(f"Duplicate {label} IDs.")
    return indexed


def remove_question_refs(value):
    """Keep review questions in the source model, outside runtime context."""
    if isinstance(value, dict):
        return {key: remove_question_refs(item) for key, item in value.items() if key != "question_ids"}
    if isinstance(value, list):
        return [remove_question_refs(item) for item in value]
    return value


def prepare_context(model: dict) -> dict:
    if model["model_version"] != 1:
        raise ValueError("Unsupported schema model version.")
    readiness = model["readiness"]
    if readiness["status"] != "ready_for_handoff":
        raise ValueError("Schema needs SME confirmation before setup.")
    if not readiness["scope"] or readiness["blocking_question_ids"]:
        raise ValueError("Handoff scope is missing or blocking questions remain.")

    evidence = index_records(model["evidence"], "evidence")
    questions = index_records(model["questions"], "question")
    tables = index_records(model["tables"], "table")
    relationships = index_records(model["relationships"], "relationship")
    subjects = set(tables) | set(relationships)

    def check_refs(value):
        if isinstance(value, dict):
            for field, available in (("evidence_ids", evidence), ("question_ids", questions), ("subjects", subjects)):
                if not set(value.get(field, [])).issubset(available):
                    raise ValueError(f"Unresolved {field} reference.")
            for item in value.values():
                check_refs(item)
        elif isinstance(value, list):
            for item in value:
                check_refs(item)

    def check_review(item, label):
        refs = item["evidence_ids"]
        if not any(evidence[identifier]["kind"] == "sme_answer" for identifier in refs):
            raise ValueError(f"{label} lacks SME answer evidence.")
        if any(questions[identifier]["status"] != "answered" for identifier in item.get("question_ids", [])):
            raise ValueError(f"{label} has an unresolved review question.")

    def check_claim(item, label):
        if item["status"] != "confirmed" or not item["text"]:
            raise ValueError(f"{label} is not confirmed.")
        check_review(item, label)

    check_refs(model)
    for item in evidence.values():
        if not item["source"] or not item["detail"]:
            raise ValueError("An evidence record lacks its source or detail.")
    for question in questions.values():
        if question["priority"] == "blocking" and question["status"] != "answered":
            raise ValueError(f"Blocking question {question['id']} remains unresolved.")
        if question["status"] == "answered":
            if not all(question.get(field) for field in ("answer", "answered_by", "answered_on")):
                raise ValueError(f"Question {question['id']} has an incomplete answer.")
            date.fromisoformat(question["answered_on"])
            check_review(question, question["id"])

    if not tables or not model["query_cases"]:
        raise ValueError("The model needs scoped tables and confirmed query cases.")
    for table in tables.values():
        check_claim(table["meaning"], f"{table['id']} meaning")
        check_claim(table["grain"], f"{table['id']} row grain")
        if not table["columns"] or not table["evidence_ids"]:
            raise ValueError(f"Table {table['id']} lacks columns or structural evidence.")
    for case in model["query_cases"]:
        check_claim(case["expected_behavior"], "Query acceptance case")

    approved = []
    for relationship in relationships.values():
        source = tables[relationship["from_table_id"]]
        target = tables[relationship["to_table_id"]]
        if relationship["join_use"] != "approved":
            continue
        if relationship["status"] not in ("observed", "confirmed"):
            raise ValueError(f"Join {relationship['id']} is not observed or confirmed.")
        check_review(relationship, relationship["id"])
        from_columns, to_columns = relationship["from_columns"], relationship["to_columns"]
        if not from_columns or len(from_columns) != len(to_columns):
            raise ValueError(f"Join {relationship['id']} has incomplete column pairs.")
        for names, table in ((from_columns, source), (to_columns, target)):
            if not set(names).issubset(column["name"] for column in table["columns"]):
                raise ValueError(f"Join {relationship['id']} refers to an absent column.")
        if relationship["cardinality"] not in ("many-to-one", "one-to-one", "many-to-many"):
            raise ValueError(f"Join {relationship['id']} has unknown or invalid cardinality.")
        approved.append(relationship)

    definitions = [item for item in model["definitions"] if item["claim"]["status"] == "confirmed"]
    for item in definitions:
        check_claim(item["claim"], item["subject"])
    return remove_question_refs({
        "context_version": 1,
        "project": model["project"],
        "inspection": model["inspection"],
        "scope": readiness["scope"],
        "tables": list(tables.values()),
        "relationships": approved,
        "definitions": definitions,
        "unavailable_definitions": [{"subject": item["subject"], "status": item["claim"]["status"]}
                                    for item in model["definitions"] if item not in definitions],
        "blocked_relationship_ids": [item["id"] for item in relationships.values() if item["join_use"] != "approved"],
        "query_cases": model["query_cases"],
        "evidence": list(evidence.values()),
        "runtime_controls": "not_assessed",
        "execution_authorised": False,
    })


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit("Usage: prepare_context.py <schema-model.json> <query-context.json>")
    source, destination = (Path(argument) for argument in sys.argv[1:])
    if source.resolve() == destination.resolve():
        sys.exit("The output path must differ from the schema model path.")
    try:
        context = prepare_context(json.loads(source.read_text(encoding="utf-8")))
    except (ValueError, KeyError, TypeError) as error:
        sys.exit(f"Schema handoff rejected: {error}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(context, indent=2) + "\n", encoding="utf-8")
    print(f"Prepared {destination}. Runtime controls remain unassessed.")


if __name__ == "__main__":
    main()
