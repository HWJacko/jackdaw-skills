#!/usr/bin/env python3
"""Check a schema handoff and write query context. No database access is made."""
import json
from datetime import date
from pathlib import Path
import sys


def text(value, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be nonempty text.")
    return value


def records(value, label: str) -> list[dict]:
    if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
        raise ValueError(f"{label} must be a list of records.")
    return value


def string_list(value, label: str, required: bool = False) -> list[str]:
    if not isinstance(value, list) or (required and not value):
        raise ValueError(f"{label} must be a list of names or IDs.")
    for item in value:
        text(item, label)
    if len(value) != len(set(value)):
        raise ValueError(f"{label} contains duplicate names or IDs.")
    return value


def index_records(value, label: str) -> dict[str, dict]:
    items = records(value, label)
    for item in items:
        text(item["id"], f"{label} ID")
    indexed = {record["id"]: record for record in items}
    if len(indexed) != len(items):
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
    if not isinstance(model, dict):
        raise ValueError("The schema model must be a record.")
    if type(model["model_version"]) is not int or model["model_version"] != 1:
        raise ValueError("Unsupported schema model version.")
    readiness = model["readiness"]
    if readiness["status"] != "ready_for_handoff":
        raise ValueError("Schema needs SME confirmation before setup.")
    string_list(readiness["scope"], "Handoff scope", required=True)
    if string_list(readiness["blocking_question_ids"], "Blocking question IDs"):
        raise ValueError("Handoff scope is missing or blocking questions remain.")
    if readiness["runtime_controls"] != "not_assessed":
        raise ValueError("Schema runtime controls must remain not_assessed.")
    for field in ("name", "abbreviation"):
        text(model["project"][field], f"Project {field}")
    for field in ("date", "dialect"):
        text(model["inspection"][field], f"Inspection {field}")
    date.fromisoformat(model["inspection"]["date"])
    if model["inspection"]["source_mode"] not in ("live_metadata", "supplied_schema"):
        raise ValueError("Invalid inspection source mode.")
    records(model["query_cases"], "Query cases")
    records(model["definitions"], "Definitions")

    evidence = index_records(model["evidence"], "evidence")
    questions = index_records(model["questions"], "question")
    tables = index_records(model["tables"], "table")
    relationships = index_records(model["relationships"], "relationship")
    subjects = set(tables) | set(relationships)

    def check_refs(value):
        if isinstance(value, dict):
            for field, available in (("evidence_ids", evidence), ("question_ids", questions), ("subjects", subjects)):
                refs = string_list(value.get(field, []), field)
                if not set(refs).issubset(available):
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
        if not isinstance(item, dict) or item.get("status") != "confirmed":
            raise ValueError(f"{label} is not confirmed.")
        text(item["text"], label)
        check_review(item, label)

    check_refs(model)
    for item in evidence.values():
        for field in ("kind", "source", "detail"):
            text(item[field], f"Evidence {field}")
    for question in questions.values():
        if question["priority"] not in ("blocking", "follow_up") or question["status"] not in ("open", "answered", "deferred"):
            raise ValueError(f"Question {question['id']} has invalid priority or status.")
        if question["priority"] == "blocking" and question["status"] != "answered":
            raise ValueError(f"Blocking question {question['id']} remains unresolved.")
        if question["status"] == "answered":
            for field in ("answer", "answered_by", "answered_on"):
                text(question.get(field), f"Question {question['id']} {field}")
            date.fromisoformat(question["answered_on"])
            check_review(question, question["id"])

    if not tables or not model["query_cases"]:
        raise ValueError("The model needs scoped tables and confirmed query cases.")
    for table in tables.values():
        check_claim(table["meaning"], f"{table['id']} meaning")
        check_claim(table["grain"], f"{table['id']} row grain")
        if not table["columns"] or not table["evidence_ids"]:
            raise ValueError(f"Table {table['id']} lacks columns or structural evidence.")
        text(table["name"], "Table name")
        if table["schema"] is not None:
            text(table["schema"], "Schema name")
        if table["kind"] not in ("table", "view"):
            raise ValueError(f"Table {table['id']} has invalid kind.")
        columns = records(table["columns"], "Columns")
        names = string_list([column["name"] for column in columns], "Column names", required=True)
        for column in columns:
            if not isinstance(column["data_type"], str) or (column["nullable"] is not None and type(column["nullable"]) is not bool):
                raise ValueError(f"Column {column['name']} has invalid type or nullability.")
            string_list(column["evidence_ids"], "Column evidence", required=True)
        for key in records(table["keys"], "Keys"):
            key_names = string_list(key["columns"], "Key columns", required=True)
            if key["kind"] not in ("primary", "unique") or not set(key_names).issubset(names):
                raise ValueError(f"Table {table['id']} has an invalid key.")
            string_list(key["evidence_ids"], "Key evidence", required=True)
        row_scope = table.get("row_scope")
        if not isinstance(row_scope, dict) or row_scope.get("status") != "confirmed":
            raise ValueError(f"Table {table['id']} row scope is not confirmed.")
        scope_columns = string_list(row_scope["columns"], "Row scope columns")
        if not set(scope_columns).issubset(names):
            raise ValueError(f"Table {table['id']} row scope refers to an absent column.")
        check_review(row_scope, f"{table['id']} row scope")
    for case in model["query_cases"]:
        text(case["question"], "Query question")
        check_claim(case["expected_behavior"], "Query acceptance case")

    approved = []
    for relationship in relationships.values():
        source = tables[relationship["from_table_id"]]
        target = tables[relationship["to_table_id"]]
        if relationship["join_use"] not in ("approved", "blocked"):
            raise ValueError(f"Join {relationship['id']} has invalid query-use status.")
        if relationship["join_use"] != "approved":
            continue
        if relationship["status"] not in ("observed", "confirmed"):
            raise ValueError(f"Join {relationship['id']} is not observed or confirmed.")
        check_review(relationship, relationship["id"])
        from_columns = string_list(relationship["from_columns"], "Join source columns")
        to_columns = string_list(relationship["to_columns"], "Join target columns")
        if not from_columns or len(from_columns) != len(to_columns):
            raise ValueError(f"Join {relationship['id']} has incomplete column pairs.")
        for names, table in ((from_columns, source), (to_columns, target)):
            if not set(names).issubset(column["name"] for column in table["columns"]):
                raise ValueError(f"Join {relationship['id']} refers to an absent column.")
        if relationship["cardinality"] not in ("many-to-one", "one-to-one", "many-to-many"):
            raise ValueError(f"Join {relationship['id']} has unknown or invalid cardinality.")
        source_scope, target_scope = source["row_scope"]["columns"], target["row_scope"]["columns"]
        if source_scope and target_scope:
            if len(source_scope) != len(target_scope) or not set(zip(source_scope, target_scope)).issubset(zip(from_columns, to_columns)):
                raise ValueError(f"Join {relationship['id']} omits or mismatches row scope.")
        sides = [("target", target, to_columns)] if relationship["cardinality"] == "many-to-one" else []
        if relationship["cardinality"] == "one-to-one":
            sides = [("source", source, from_columns), ("target", target, to_columns)]
        for label, table, names in sides:
            if not any(set(key["columns"]).issubset(names) for key in table["keys"]):
                raise ValueError(f"Join {relationship['id']} must include a complete {label} key.")
        approved.append(relationship)

    for item in model["definitions"]:
        text(item["subject"], "Definition subject")
        if item["claim"]["status"] not in ("observed", "assumed", "confirmed", "rejected", "unknown"):
            raise ValueError("Invalid definition status.")
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
