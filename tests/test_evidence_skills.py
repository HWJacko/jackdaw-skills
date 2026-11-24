import copy
import importlib.util
import json
from pathlib import Path
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest

from test_product_skills import graph, table
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "skills/user-research/research-synthesis/examples"
METRIC = ROOT / "skills/data-analyst/metric-definition/examples"
IMPACT = ROOT / "skills/business-analyst/change-impact-analysis"
SPEC = importlib.util.spec_from_file_location("analyse_links", IMPACT / "scripts/analyse_links.py")
impact = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(impact)


class EvidenceExamplesTests(unittest.TestCase):
    def test_findings_count_distinct_participants_and_retain_contrary_observations(self):
        output = (RESEARCH / "example-output.md").read_text()
        observations = {row["Observation ID"]: row for row in table(output, "Observations")}
        participants = {row["Participant"] for row in observations.values()}
        for finding in table(output, "Findings"):
            supported = re.findall(r"SPOB\d+", finding["Supporting observations"])
            distinct = {observations[identifier]["Participant"] for identifier in supported}
            self.assertEqual(finding["Distinct supporting participants"], f"{len(distinct)} of {len(participants)}")
            for identifier in re.findall(r"SPOB\d+", finding["Contrary observations"]):
                self.assertIn(identifier, observations)
        contrary = table(output, "Findings")[0]["Contrary observations"]
        self.assertIn("SPOB005", contrary)
        source = (RESEARCH / "input.md").read_text()
        for observation in observations.values():
            if observation["Form"] == "supplied quote":
                self.assertIn('"' + observation["Observation or supplied quote"] + '"', source)

    def test_research_and_impact_diagrams_match_both_formats(self):
        for folder in (RESEARCH, IMPACT / "examples"):
            with self.subTest(folder=folder):
                _, nodes, edges = graph((folder / "example-output.md").read_text())
                cells = ET.parse(folder / "example-output.drawio").findall(".//mxCell")
                xml_nodes = {cell.get("id"): cell.get("value") for cell in cells if cell.get("vertex") == "1" and cell.get("id") != "legend"}
                self.assertEqual(nodes, xml_nodes)
                self.assertTrue(nodes)
                expected = {(source, target, label, arrow == "-.") for source, arrow, label, _, target in edges}
                actual = {(cell.get("source"), cell.get("target"), cell.get("value"), "dashed=1" in cell.get("style", ""))
                          for cell in cells if cell.get("edge") == "1"}
                self.assertEqual(expected, actual)

    def metric_result(self, tenant=1, start="2026-11-02T00:00:00Z", end="2026-11-09T00:00:00Z"):
        database = sqlite3.connect(":memory:")
        self.addCleanup(database.close)
        database.executescript((METRIC / "input-schema.sql").read_text())
        database.executescript((METRIC / "input-data.sql").read_text())
        database.execute("PRAGMA query_only = ON")
        return database.execute((METRIC / "example-query.sql").read_text(), {
            "tenant_id": tenant, "period_start": start, "period_end": end,
        }).fetchone()

    def test_metric_uses_attempt_grain_and_separates_unknown_flags(self):
        helped, eligible, unknown, rate = self.metric_result()
        self.assertEqual((helped, eligible, unknown), (2, 3, 1))
        self.assertAlmostEqual(rate, 100 * 2 / 3)
        self.assertEqual(round(rate, 2), 66.67)

    def test_metric_scope_and_time_boundaries(self):
        self.assertEqual(self.metric_result(tenant=2), (0, 1, 0, 0.0))
        boundary = self.metric_result(start="2026-11-09T00:00:00Z", end="2026-11-10T00:00:00Z")
        self.assertEqual(boundary, (1, 1, 0, 100.0))

    def test_zero_denominator_is_unavailable_instead_of_zero_percent(self):
        self.assertEqual(self.metric_result(tenant=999), (0, 0, 0, None))
        unknown_only = self.metric_result(start="2026-11-05T00:00:00Z", end="2026-11-06T00:00:00Z")
        self.assertEqual(unknown_only, (0, 0, 1, None))


class ImpactAnalysisTests(unittest.TestCase):
    def setUp(self):
        self.graph = json.loads((IMPACT / "examples/input-trace-links.json").read_text())

    def analyse(self, changed=None):
        return impact.analyse_links(self.graph, changed or ["SPMT001"])

    def test_example_separates_recorded_review_proposals_and_gaps(self):
        expected = json.loads((IMPACT / "examples/example-analysis.json").read_text())
        self.assertEqual(self.analyse(), expected)
        self.assertEqual(set(expected["review_required"]), {"SPOC001", "SPUC001", "SPUS001", "SPTC001", "SPRS001"})
        self.assertEqual(expected["possible_review"], ["SPUS004"])
        self.assertEqual(expected["gaps"][0]["missing_ids"], ["SPUC999"])
        self.assertEqual(expected["coverage"], "partial")
        report = (IMPACT / "examples/example-output.md").read_text()
        self.assertEqual({row["Record ID"] for row in table(report, "Required review from recorded links")}, set(expected["review_required"]))

    def test_proposed_path_remains_possible_through_recorded_descendants(self):
        self.graph["nodes"].append({"id": "SPTC004", "kind": "test", "label": "Colour test", "source": "fixture"})
        self.graph["links"].append({"from": "SPUS004", "to": "SPTC004", "relationship": "checked by", "status": "recorded", "source": "fixture"})
        self.assertEqual(set(self.analyse()["possible_review"]), {"SPUS004", "SPTC004"})

    def test_recorded_path_takes_precedence_over_a_proposed_path(self):
        self.graph["links"].append({"from": "SPMT001", "to": "SPUS004", "relationship": "uses metric", "status": "recorded", "source": "fixture"})
        result = self.analyse()
        self.assertIn("SPUS004", result["review_required"])
        self.assertEqual(result["possible_review"], [])

    def test_cycles_terminate_without_repeating_changed_records(self):
        self.graph["links"].append({"from": "SPRS001", "to": "SPMT001", "relationship": "feedback", "status": "recorded", "source": "fixture"})
        result = self.analyse()
        self.assertNotIn("SPMT001", result["review_required"])
        self.assertEqual(len(result["review_required"]), 5)

    def test_multiple_changed_ids_are_deduplicated_and_excluded_from_review(self):
        result = self.analyse(["SPMT001", "SPUS001", "SPMT001"])
        self.assertEqual(result["changed_ids"], ["SPMT001", "SPUS001"])
        self.assertNotIn("SPUS001", result["review_required"])
        self.assertIn("SPTC001", result["review_required"])

    def test_missing_endpoints_do_not_create_source_nodes_or_mutate_input(self):
        original = copy.deepcopy(self.graph)
        self.analyse()
        self.assertEqual(self.graph, original)
        self.assertNotIn("SPUC999", {node["id"] for node in self.graph["nodes"]})

    def test_qualified_document_ids_are_supported(self):
        self.graph["nodes"].append({"id": "notes.md#E1", "kind": "evidence", "label": "Local evidence", "source": "notes.md E1"})
        self.graph["links"].append({"from": "notes.md#E1", "to": "SPRF001", "relationship": "supports", "status": "recorded", "source": "fixture"})
        self.assertIn("SPRF001", self.analyse(["notes.md#E1"])["review_required"])

    def test_unknown_changed_id_and_empty_change_list_are_rejected(self):
        for changed in (["absent"], []):
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                impact.analyse_links(self.graph, changed)

    def test_duplicate_ids_and_invalid_link_status_are_rejected(self):
        duplicate = copy.deepcopy(self.graph)
        duplicate["nodes"].append(copy.deepcopy(duplicate["nodes"][0]))
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            impact.analyse_links(duplicate, ["SPMT001"])
        self.graph["links"][0]["status"] = "observed"
        with self.assertRaisesRegex(ValueError, "Link status"):
            self.analyse()

    def test_invalid_graph_versions_are_rejected(self):
        for version in (True, "1", 2):
            with self.subTest(version=version):
                self.graph["trace_version"] = version
                with self.assertRaises(ValueError):
                    self.analyse()

    def test_no_gaps_still_does_not_claim_complete_coverage(self):
        self.graph["links"] = [link for link in self.graph["links"] if link["to"] != "SPUC999"]
        self.assertEqual(self.analyse()["coverage"], "supplied_links_only")

    def test_installed_cli_uses_only_standard_library_and_keeps_sources(self):
        with tempfile.TemporaryDirectory() as temporary:
            installed = Path(temporary) / "skill"
            shutil.copytree(IMPACT, installed)
            source = installed / "examples/input-trace-links.json"
            before = source.read_text()
            result = subprocess.run([sys.executable, "-I", "-S", str(installed / "scripts/analyse_links.py"), str(source), "SPMT001"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout), self.analyse())
            self.assertEqual(source.read_text(), before)


if __name__ == "__main__":
    unittest.main()
