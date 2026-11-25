import copy
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

from test_product_skills import graph


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/quality-assurance/test-coverage-map"
EXAMPLES = SKILL / "examples"
WORKFLOW = ROOT / "examples/quality-workflow"
SPEC = importlib.util.spec_from_file_location("summarise_coverage", SKILL / "scripts/summarise_coverage.py")
coverage = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(coverage)


class CoverageTests(unittest.TestCase):
    def setUp(self):
        self.register = json.loads((EXAMPLES / "input-test-register.json").read_text())

    def summary(self):
        return coverage.summarise_coverage(self.register)

    def test_example_keeps_mapped_coverage_separate_from_verified_criteria(self):
        expected = json.loads((EXAMPLES / "example-summary.json").read_text())
        self.assertEqual(self.summary(), expected)
        self.assertEqual(expected["summary"], {"criteria": 2, "mapped": 2, "verified": 1})
        self.assertFalse(expected["criteria"][1]["verified"])
        self.assertEqual(expected["tests"][1]["recorded_status"], "not_run")

    def test_current_result_is_not_inferred_from_historical_passes(self):
        self.register["tests"][0]["current_result_id"] = None
        result = self.summary()
        self.assertEqual(result["tests"][0]["recorded_status"], "not_run")
        self.assertEqual(result["summary"]["verified"], 0)
        self.assertEqual(self.register["results"][0]["status"], "passed")

    def test_a_passing_test_does_not_resolve_a_conflicting_criterion(self):
        self.register["criteria"][0]["status"] = "conflicting"
        result = self.summary()
        self.assertTrue(result["tests"][0]["current"])
        self.assertEqual(result["tests"][0]["recorded_status"], "passed")
        self.assertFalse(result["criteria"][0]["verified"])

    def test_a_blocked_design_cannot_verify_a_criterion(self):
        self.register["tests"][0]["design_status"] = "blocked"
        result = self.summary()
        self.assertFalse(result["tests"][0]["current"])
        self.assertEqual(result["tests"][0]["recorded_status"], "passed")
        self.assertFalse(result["criteria"][0]["verified"])

    def test_failed_and_blocked_execution_records_remain_visible(self):
        for status in ("failed", "blocked"):
            with self.subTest(status=status):
                self.register["results"][0]["status"] = status
                result = self.summary()
                self.assertEqual(result["tests"][0]["recorded_status"], status)
                self.assertTrue(result["tests"][0]["current"])
                self.assertFalse(result["criteria"][0]["verified"])

    def test_old_test_results_do_not_verify_a_changed_test_revision(self):
        self.register["tests"][0]["revision"] = "2"
        result = self.summary()
        self.assertEqual(result["tests"][0]["recorded_status"], "passed")
        self.assertFalse(result["tests"][0]["current"])
        self.assertFalse(result["criteria"][0]["verified"])

    def test_old_test_references_do_not_verify_a_changed_criterion(self):
        self.register["criteria"][0]["revision"] = "2"
        result = self.summary()
        self.assertFalse(result["tests"][0]["current"])
        self.assertFalse(result["criteria"][0]["verified"])

    def test_all_mapped_cases_are_required(self):
        case = copy.deepcopy(self.register["tests"][0])
        case.update(id="SPTC003", current_result_id=None)
        self.register["tests"].append(case)
        result = self.summary()
        self.assertEqual(set(result["criteria"][0]["mapped_tests"]), {"SPTC001", "SPTC003"})
        self.assertFalse(result["criteria"][0]["verified"])

    def test_missing_result_reference_does_not_become_a_pass(self):
        self.register["tests"][0]["current_result_id"] = "absent"
        result = self.summary()
        self.assertEqual(result["tests"][0]["recorded_status"], "unknown")
        self.assertFalse(result["criteria"][0]["verified"])

    def test_a_result_for_another_test_cannot_verify_the_selected_case(self):
        self.register["results"][0]["test_id"] = "SPTC002"
        result = self.summary()
        self.assertEqual(result["tests"][0]["recorded_status"], "unknown")
        self.assertFalse(result["criteria"][0]["verified"])

    def test_missing_criteria_and_orphan_results_are_reported(self):
        self.register["tests"][0]["criterion_refs"].append({"id": "absent", "revision": "1"})
        self.register["results"].append({**self.register["results"][0], "id": "SPRS002", "test_id": "absent-test"})
        result = self.summary()
        self.assertFalse(result["criteria"][0]["verified"])
        self.assertTrue(any("missing criterion" in gap for gap in result["tests"][0]["gaps"]))
        self.assertTrue(result["gaps"])

    def test_empty_scope_has_no_verified_criteria(self):
        self.register.update(criteria=[], tests=[], results=[])
        result = self.summary()
        self.assertEqual(result["summary"], {"criteria": 0, "mapped": 0, "verified": 0})
        self.assertTrue(result["gaps"])
        self.assertEqual(result["coverage"], "supplied_criteria_only")

    def test_invalid_versions_statuses_and_duplicate_ids_are_rejected(self):
        mutations = [
            lambda data: data.update(coverage_version=True),
            lambda data: data["criteria"][0].update(status="accepted"),
            lambda data: data["tests"][0].update(design_status="passed"),
            lambda data: data["results"][0].update(status="not_run"),
            lambda data: data["results"][0].update(observed=""),
            lambda data: data["criteria"].append(copy.deepcopy(data["criteria"][0])),
            lambda data: data["tests"][0]["criterion_refs"].append(copy.deepcopy(data["tests"][0]["criterion_refs"][0])),
        ]
        for position, mutate in enumerate(mutations):
            with self.subTest(position=position):
                data = copy.deepcopy(self.register)
                mutate(data)
                with self.assertRaises(ValueError):
                    coverage.summarise_coverage(data)

    def test_installed_helper_uses_only_standard_library_and_preserves_input(self):
        with tempfile.TemporaryDirectory() as temporary:
            installed = Path(temporary) / "skill"
            shutil.copytree(SKILL, installed)
            source = installed / "examples/input-test-register.json"
            before = source.read_text()
            result = subprocess.run([sys.executable, "-I", "-S", str(installed / "scripts/summarise_coverage.py"), str(source)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout), self.summary())
            self.assertEqual(source.read_text(), before)


class WorkedWorkflowTests(unittest.TestCase):
    def test_fixture_result_is_reproducible_and_matches_the_register(self):
        result = subprocess.run([sys.executable, "-I", "-S", str(WORKFLOW / "run_fixture.py")], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        actual = json.loads(result.stdout)
        stored = json.loads((WORKFLOW / "fixture-result.json").read_text())
        register = json.loads((WORKFLOW / "test-register.json").read_text())
        self.assertEqual(actual, stored)
        self.assertEqual(register["results"], [stored])
        self.assertEqual(stored["rows"], [[1, 10], [1, 11], [1, 12]])

    def test_conflict_unrun_case_and_missing_performance_bound_remain_gaps(self):
        register = json.loads((WORKFLOW / "test-register.json").read_text())
        result = coverage.summarise_coverage(register)
        self.assertEqual(result, json.loads((WORKFLOW / "coverage-summary.json").read_text()))
        self.assertEqual(result["summary"], {"criteria": 4, "mapped": 3, "verified": 1})
        self.assertEqual([case["recorded_status"] for case in result["tests"]], ["passed", "not_run", "not_run"])
        self.assertFalse(any(criterion["verified"] for criterion in result["criteria"][1:]))

    def test_trace_connects_research_to_review_without_inventing_unrun_results(self):
        trace = json.loads((WORKFLOW / "trace-links.json").read_text())
        spec = importlib.util.spec_from_file_location("workflow_impact", ROOT / "skills/business-analyst/change-impact-analysis/scripts/analyse_links.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        result = module.analyse_links(trace, ["ECEV001"])
        for identifier in ("ECOB001", "ECRF001", "ECPR001", "ECOC001", "ECUC001", "ECUS001", "ECTC001", "ECRS001", "workflow.md#8-outcome-and-release-review"):
            self.assertIn(identifier, result["review_required"])
        self.assertEqual(result["gaps"], [])
        result_ids = {node["id"] for node in trace["nodes"] if node["kind"] == "result"}
        for identifier in ("ECTC002", "ECTC003"):
            self.assertTrue(result_ids.isdisjoint(module.analyse_links(trace, [identifier])["review_required"]))

    def test_maps_preserve_labels_and_have_no_results_for_unrun_cases(self):
        for folder, markdown, register_name in ((EXAMPLES, "example-output.md", "input-test-register.json"),
                                                  (WORKFLOW, "coverage.md", "test-register.json")):
            with self.subTest(folder=folder):
                register = json.loads((folder / register_name).read_text())
                _, nodes, edges = graph((folder / markdown).read_text())
                cells = ET.parse((folder / markdown).with_suffix(".drawio")).findall(".//mxCell")
                xml_nodes = {cell.get("id"): cell.get("value") for cell in cells if cell.get("vertex") == "1" and cell.get("id") != "legend"}
                self.assertEqual(nodes, xml_nodes)
                self.assertEqual({(source, target, label) for source, _, label, _, target in edges},
                                 {(cell.get("source"), cell.get("target"), cell.get("value")) for cell in cells if cell.get("edge") == "1"})
                selected = {case["current_result_id"] for case in register["tests"] if case["current_result_id"]}
                self.assertEqual({identifier for identifier in nodes if identifier in {result["id"] for result in register["results"]}}, selected)
                for case in register["tests"]:
                    if case["current_result_id"] is None:
                        self.assertIn("not_run", nodes[case["id"]])
                        self.assertFalse(any(source == case["id"] for source, _, _, _, _ in edges))


if __name__ == "__main__":
    unittest.main()
