import copy
import importlib.util
import json
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/data-analyst/text-to-sql-setup"
EXAMPLES = SKILL / "examples"
SPEC = importlib.util.spec_from_file_location("prepare_context", SKILL / "scripts/prepare_context.py")
setup = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(setup)


class TextToSqlSetupTests(unittest.TestCase):
    def setUp(self):
        self.model = json.loads((EXAMPLES / "input-schema-model.json").read_text())

    def relationship(self, status="observed", join_use="approved"):
        target = copy.deepcopy(self.model["tables"][0])
        target.update(id="QETB002", name="order_headers")
        self.model["tables"].append(target)
        relationship = {
            "id": "QERL001", "from_table_id": "QETB001", "from_columns": ["tenant_id", "order_id"],
            "to_table_id": "QETB002", "to_columns": ["tenant_id", "order_id"],
            "status": status, "evidence_ids": ["QEEV001", "QEEV002"], "question_ids": ["QEQ001"],
            "cardinality": "one-to-one", "join_use": join_use,
        }
        self.model["relationships"].append(relationship)
        return relationship

    def test_reviewed_example_produces_context_without_execution_permission(self):
        context = setup.prepare_context(self.model)
        expected = json.loads((EXAMPLES / "example-query-context.json").read_text())
        self.assertEqual(context, expected)
        self.assertEqual(context["runtime_controls"], "not_assessed")
        self.assertFalse(context["execution_authorised"])
        self.assertNotIn("question_ids", json.dumps(context))

    def test_discovery_example_is_rejected(self):
        model = json.loads((ROOT / "skills/data-analyst/schema-map/examples/example-schema-model.json").read_text())
        with self.assertRaisesRegex(ValueError, "SME confirmation"):
            setup.prepare_context(model)

    def test_ready_label_does_not_override_unresolved_blockers(self):
        for status in ("open", "deferred"):
            with self.subTest(status=status):
                self.model["questions"][0]["status"] = status
                with self.assertRaisesRegex(ValueError, "remains unresolved"):
                    setup.prepare_context(self.model)

    def test_missing_sme_evidence_is_rejected(self):
        self.model["evidence"][1]["kind"] = "ddl"
        with self.assertRaisesRegex(ValueError, "SME answer evidence"):
            setup.prepare_context(self.model)

    def test_incomplete_answers_and_invalid_dates_are_rejected(self):
        for field in ("answer", "answered_by", "answered_on"):
            with self.subTest(field=field):
                model = copy.deepcopy(self.model)
                model["questions"][0][field] = None
                with self.assertRaises(ValueError):
                    setup.prepare_context(model)
        self.model["questions"][0]["answered_on"] = "2026-99-99"
        with self.assertRaises(ValueError):
            setup.prepare_context(self.model)

    def test_unconfirmed_row_grain_and_query_cases_are_rejected(self):
        model = copy.deepcopy(self.model)
        model["tables"][0]["grain"]["status"] = "assumed"
        with self.assertRaisesRegex(ValueError, "row grain is not confirmed"):
            setup.prepare_context(model)
        self.model["query_cases"][0]["expected_behavior"]["status"] = "assumed"
        with self.assertRaisesRegex(ValueError, "acceptance case is not confirmed"):
            setup.prepare_context(self.model)

    def test_missing_references_and_duplicate_ids_are_rejected(self):
        model = copy.deepcopy(self.model)
        model["tables"][0]["meaning"]["evidence_ids"] = ["missing"]
        with self.assertRaisesRegex(ValueError, "Unresolved"):
            setup.prepare_context(model)
        self.model["tables"].append(copy.deepcopy(self.model["tables"][0]))
        with self.assertRaisesRegex(ValueError, "Duplicate table"):
            setup.prepare_context(self.model)

    def test_composite_join_pairs_are_preserved(self):
        relationship = self.relationship()
        context = setup.prepare_context(self.model)
        self.assertEqual(context["relationships"][0]["from_columns"], relationship["from_columns"])
        self.assertEqual(context["relationships"][0]["to_columns"], relationship["to_columns"])

    def test_assumed_join_cannot_be_exported_as_approved(self):
        self.relationship(status="assumed")
        with self.assertRaisesRegex(ValueError, "not observed or confirmed"):
            setup.prepare_context(self.model)

    def test_invalid_join_columns_are_rejected(self):
        relationship = self.relationship()
        relationship["to_columns"] = ["tenant_id"]
        with self.assertRaisesRegex(ValueError, "incomplete column pairs"):
            setup.prepare_context(self.model)
        relationship["to_columns"] = ["tenant_id", "absent"]
        with self.assertRaisesRegex(ValueError, "absent column"):
            setup.prepare_context(self.model)

    def test_blocked_joins_and_unconfirmed_definitions_are_withheld(self):
        relationship = self.relationship(status="assumed", join_use="blocked")
        self.model["definitions"].append({"subject": "Unconfirmed revenue", "claim": {
            "text": "Unconfirmed formula", "status": "assumed", "evidence_ids": ["QEEV001"], "question_ids": ["QEQ002"],
        }})
        context = setup.prepare_context(self.model)
        self.assertEqual(context["relationships"], [])
        self.assertEqual(context["blocked_relationship_ids"], [relationship["id"]])
        self.assertEqual(context["unavailable_definitions"], [{"subject": "Unconfirmed revenue", "status": "assumed"}])
        self.assertNotIn("Unconfirmed formula", json.dumps(context))

    def test_failed_cli_check_preserves_existing_context(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "context.json"
            destination.write_text("existing context")
            source = ROOT / "skills/data-analyst/schema-map/examples/example-schema-model.json"
            result = subprocess.run([sys.executable, str(SKILL / "scripts/prepare_context.py"), str(source), str(destination)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Schema handoff rejected", result.stderr)
            self.assertEqual(destination.read_text(), "existing context")

    def test_installed_helper_runs_without_database_dependencies(self):
        with tempfile.TemporaryDirectory() as temporary:
            installed = Path(temporary) / "skill"
            shutil.copytree(SKILL, installed)
            output = Path(temporary) / "output/context.json"
            source = installed / "examples/input-schema-model.json"
            result = subprocess.run([sys.executable, "-I", "-S", str(installed / "scripts/prepare_context.py"), str(source), str(output)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(output.read_text()), setup.prepare_context(self.model))
            result = subprocess.run([sys.executable, str(installed / "scripts/prepare_context.py"), str(source), str(source)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(json.loads(source.read_text()), self.model)

    def test_accepted_fixture_queries_match_sme_counts(self):
        evaluation = json.loads((EXAMPLES / "example-query-evaluation.json").read_text())
        self.assertIsNone(evaluation["runtime"])
        with sqlite3.connect(":memory:") as database:
            database.row_factory = sqlite3.Row
            database.executescript((EXAMPLES / "input-schema.sql").read_text())
            database.executemany("INSERT INTO orders VALUES (?, ?, ?)", [
                (1, 1, "new"), (1, 2, "paid"), (1, 3, "paid"),
                (2, 1, "paid"), (2, 2, "paid"), (2, 3, "paid"),
            ])
            database.execute("PRAGMA query_only = ON")
            for case in evaluation["cases"]:
                self.assertEqual(case["result"], "not_run")
                self.assertIsNone(case["result_evidence"])
                if case["kind"] == "accept":
                    rows = database.execute(case["expected"]["fixture_sql"], case["caller_context"])
                    self.assertEqual([dict(row) for row in rows], case["expected"]["rows"])


if __name__ == "__main__":
    unittest.main()
