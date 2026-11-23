import json
from pathlib import Path
import re
import sqlite3
import unittest
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "skills/data-analyst/schema-map/examples"
VISUAL = ROOT / "skills/data-analyst/schema-map-visual/examples"


class SchemaMapTests(unittest.TestCase):
    def setUp(self):
        self.model = json.loads((EXAMPLES / "example-schema-model.json").read_text())
        self.database = sqlite3.connect(":memory:")
        self.addCleanup(self.database.close)
        self.database.execute("PRAGMA foreign_keys = ON")
        self.database.executescript((EXAMPLES / "input-schema.sql").read_text())
        self.tables = {table["id"]: table for table in self.model["tables"]}

    def test_example_inventory_matches_sqlite_metadata(self):
        names = {row[0] for row in self.database.execute("SELECT name FROM sqlite_schema WHERE type = 'table'")}
        self.assertEqual(names, {table["name"] for table in self.tables.values()})
        for table in self.tables.values():
            with self.subTest(table=table["name"]):
                metadata = self.database.execute("SELECT name, type, [notnull], pk FROM pragma_table_xinfo(?)", (table["name"],)).fetchall()
                self.assertEqual([(column["name"], column["data_type"], column["nullable"]) for column in table["columns"]],
                                 [(name, kind, not bool(not_null)) for name, kind, not_null, _ in metadata])
                primary = [name for name, _, _, order in sorted(metadata, key=lambda row: row[3]) if order]
                self.assertEqual(table["keys"][0]["columns"], primary)

    def test_relationships_distinguish_declared_and_assumed_keys(self):
        for relationship in self.model["relationships"]:
            source = self.tables[relationship["from_table_id"]]
            target = self.tables[relationship["to_table_id"]]
            rows = self.database.execute('SELECT id, seq, "table", "from", "to" FROM pragma_foreign_key_list(?)', (source["name"],)).fetchall()
            constraints = {}
            for identifier, position, table, from_column, to_column in rows:
                constraints.setdefault(identifier, []).append((position, table, from_column, to_column))
            declared = [(items[0][1], [item[2] for item in items], [item[3] for item in items])
                        for items in (sorted(group) for group in constraints.values())]
            edge = (target["name"], relationship["from_columns"], relationship["to_columns"])
            if relationship["status"] == "observed":
                self.assertIn(edge, declared)
            else:
                self.assertEqual(relationship["status"], "assumed")
                self.assertNotIn(edge, declared)
            self.assertEqual(relationship["to_columns"], target["keys"][0]["columns"])
            self.assertEqual(len(relationship["from_columns"]), len(relationship["to_columns"]))
            self.assertIn("tenant_id", relationship["from_columns"])
            self.assertEqual(relationship["join_use"], "blocked")

    def test_model_references_and_review_status_are_consistent(self):
        evidence = {item["id"] for item in self.model["evidence"]}
        questions = {item["id"]: item for item in self.model["questions"]}
        subjects = set(self.tables) | {item["id"] for item in self.model["relationships"]}
        self.assertEqual(len(evidence), len(self.model["evidence"]))
        self.assertEqual(len(questions), len(self.model["questions"]))

        def check_references(value):
            if isinstance(value, dict):
                for field, valid in (("evidence_ids", evidence), ("question_ids", set(questions)), ("subjects", subjects)):
                    self.assertTrue(set(value.get(field, [])).issubset(valid), value)
                if value.get("status") in ("observed", "assumed"):
                    self.assertTrue(value.get("evidence_ids"), value)
                if value.get("status") in ("assumed", "unknown"):
                    self.assertTrue(value.get("question_ids"), value)
                self.assertNotEqual(value.get("status"), "confirmed", "The example supplies no SME answers.")
                for item in value.values():
                    check_references(item)
            elif isinstance(value, list):
                for item in value:
                    check_references(item)

        check_references(self.model)
        blockers = {identifier for identifier, question in questions.items()
                    if question["priority"] == "blocking" and question["status"] != "answered"}
        self.assertEqual(set(self.model["readiness"]["blocking_question_ids"]), blockers)
        self.assertTrue(blockers)
        self.assertEqual(self.model["readiness"]["status"], "needs_confirmation")
        self.assertEqual(self.model["readiness"]["runtime_controls"], "not_assessed")
        review = (EXAMPLES / "example-sme-questions.md").read_text()
        self.assertEqual(set(re.findall(r"^## (SAQ\d+)", review, re.M)), set(questions))
        for question in questions.values():
            self.assertIn(question["question"], review)
            self.assertIsNone(question["answer"])

    def test_month_filter_gap_is_real(self):
        columns = {column["name"] for table in self.tables.values() for column in table["columns"]}
        self.assertFalse(any("date" in name or "time" in name for name in columns))
        rule = next(item["claim"] for item in self.model["definitions"] if item["subject"] == "Month filter")
        self.assertEqual(rule["status"], "unknown")
        self.assertIsNone(rule["text"])
        self.assertTrue(set(rule["question_ids"]).issubset(self.model["readiness"]["blocking_question_ids"]))

    def test_example_join_requires_the_tenant_key(self):
        self.database.executemany("INSERT INTO customers VALUES (?, ?, ?)", [(1, 7, "First"), (2, 7, "Second")])
        self.database.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?)",
                                  [(1, 10, 7, "paid", 100, "USD"), (2, 10, 7, "paid", 300, "USD")])
        incomplete = self.database.execute("SELECT SUM(o.total_minor) FROM orders o JOIN customers c ON o.customer_id = c.customer_id").fetchone()[0]
        complete = self.database.execute("SELECT SUM(o.total_minor) FROM orders o JOIN customers c ON o.tenant_id = c.tenant_id AND o.customer_id = c.customer_id").fetchone()[0]
        self.assertEqual(incomplete, 800)
        self.assertEqual(complete, 400)

    def test_sqlite_inspection_queries_run_with_writes_disabled(self):
        reference = (EXAMPLES.parent / "references/inspection.md").read_text()
        section = reference.split("## SQLite", 1)[1].split("## Other SQL dialects", 1)[0]
        self.database.execute("PRAGMA query_only = ON")
        results = []
        for block in re.findall(r"```sql\n(.*?)```", section, re.S):
            for statement in block.split(";"):
                if statement.strip():
                    results.append(self.database.execute(statement).fetchall())
        self.assertEqual({row[0] for row in results[0]}, {table["name"] for table in self.tables.values()})
        self.assertEqual([row[1] for row in results[1]], ["tenant_id", "order_id", "line_number"])
        self.assertEqual(len(results[2]), 2)
        self.assertEqual(results[4], [(1,)])

    def test_diagrams_preserve_model_edges_labels_and_assumptions(self):
        markdown = (VISUAL / "example-output.md").read_text()
        cells = ET.parse(VISUAL / "example-output.drawio").findall(".//mxCell")
        nodes = {cell.get("id"): cell for cell in cells if cell.get("id") in self.tables}
        self.assertEqual(set(nodes), set(self.tables))
        mermaid_nodes = dict(re.findall(r'^\s*(SATB\d+)\["(.*)"\]$', markdown, re.M))
        self.assertEqual(mermaid_nodes, {identifier: cell.get("value") for identifier, cell in nodes.items()})
        for identifier, table in self.tables.items():
            self.assertIn(f"{table['schema']}.{table['name']}", mermaid_nodes[identifier])
            for column in table["columns"]:
                self.assertIn(f"{column['name']} {column['data_type']}", mermaid_nodes[identifier])
        edges = {cell.get("id"): cell for cell in cells if cell.get("edge") == "1"}
        mermaid_edges = re.findall(r'^\s*(SATB\d+)\s+(--|-\.)\s+"([^"]+)"\s+(-->|\.->)\s+(SATB\d+)$', markdown, re.M)
        self.assertEqual(len(mermaid_edges), len(self.model["relationships"]))
        by_id = {label.split()[0]: (source, arrow, label, target) for source, arrow, label, _, target in mermaid_edges}
        self.assertEqual(set(edges), set(by_id))
        for relationship in self.model["relationships"]:
            identifier = relationship["id"]
            source, arrow, label, target = by_id[identifier]
            self.assertEqual((source, target), (relationship["from_table_id"], relationship["to_table_id"]))
            self.assertEqual((source, target), (edges[identifier].get("source"), edges[identifier].get("target")))
            self.assertEqual(label, edges[identifier].get("value"))
            self.assertEqual(arrow == "-.", relationship["status"] == "assumed")
            self.assertEqual("dashed=1" in edges[identifier].get("style"), relationship["status"] == "assumed")
            self.assertIn("(" + ", ".join(relationship["from_columns"]) + ") to (" + ", ".join(relationship["to_columns"]) + ")", label)
            self.assertIn("query use " + relationship["join_use"], label)


if __name__ == "__main__":
    unittest.main()
