from decimal import Decimal
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
MANAGER = ROOT / "skills/product-manager"
OWNER = ROOT / "skills/product-owner"


def table(markdown, section):
    body = markdown.split(f"## {section}\n", 1)[1].split("\n## ", 1)[0]
    lines = [line for line in body.splitlines() if line.startswith("|")]
    cells = [[cell.strip() for cell in line.strip("|").split("|")] for line in lines]
    return [dict(zip(cells[0], row, strict=True)) for row in cells[2:]]


def graph(markdown):
    block = re.search(r"```mermaid\n(.*?)```", markdown, re.S).group(1)
    nodes = dict(re.findall(r'^\s*(\w+)\["([^"]+)"\]$', block, re.M))
    edges = re.findall(r'^\s*(\w+)\s+(--|-\.)\s+"([^"]+)"\s+(-->|\.->)\s+(\w+)$', block, re.M)
    return block, nodes, edges


class ProductSkillTests(unittest.TestCase):
    def test_visual_examples_have_matching_nodes_edges_and_statuses(self):
        folders = [MANAGER / "opportunity-assessment", MANAGER / "outcome-roadmap", OWNER / "release-scope"]
        for folder in folders:
            with self.subTest(skill=folder.name):
                markdown = (folder / "examples/example-output.md").read_text()
                block, nodes, edges = graph(markdown)
                cells = ET.parse(folder / "examples/example-output.drawio").findall(".//mxCell")
                lanes = set(re.findall(r'^\s*subgraph (\w+)\[', block, re.M))
                xml_nodes = {cell.get("id"): cell.get("value") for cell in cells
                             if cell.get("vertex") == "1" and cell.get("id") not in lanes | {"legend"}}
                self.assertTrue(nodes)
                self.assertEqual(nodes, xml_nodes)
                mermaid_edges = set()
                for source, arrow, label, tail, target in edges:
                    self.assertEqual(arrow == "-.", tail == ".->")
                    self.assertIn(source, nodes)
                    self.assertIn(target, nodes)
                    mermaid_edges.add((source, target, label, arrow == "-."))
                xml_edges = {(cell.get("source"), cell.get("target"), cell.get("value"), "dashed=1" in cell.get("style", ""))
                             for cell in cells if cell.get("edge") == "1"}
                self.assertTrue(mermaid_edges)
                self.assertEqual(mermaid_edges, xml_edges)

    def test_roadmap_horizons_and_sequence_match_the_source(self):
        folder = MANAGER / "outcome-roadmap/examples"
        source = (folder / "input.md").read_text()
        output = (folder / "example-output.md").read_text()
        roadmap = table(output, "Roadmap")
        self.assertEqual({row["Outcome ID"] for row in roadmap}, set(re.findall(r"SPOC\d+", source)))
        block, nodes, edges = graph(output)
        horizon = None
        locations = {}
        for line in block.splitlines():
            group = re.match(r'\s*subgraph \w+\["([^"]+)"\]', line)
            node = re.match(r'\s*(SPOC\d+)\[', line)
            if group:
                horizon = group.group(1)
            elif line.strip() == "end":
                horizon = None
            elif node:
                locations[node.group(1)] = horizon
        self.assertEqual(locations, {row["Outcome ID"]: row["Horizon"] for row in roadmap})
        self.assertEqual(set(locations.values()), {"Now", "Next", "Later"})
        sequence = table(output, "Sequence and dependencies")
        self.assertEqual({(source, target, label.replace("<br/>", " ")) for source, _, label, _, target in edges},
                         {(row["From"], row["To"], row["Type"]) for row in sequence})
        self.assertTrue(all(arrow == "-." for _, arrow, _, _, _ in edges))
        self.assertFalse(re.search(r"\b\d{4}-\d{2}-\d{2}\b", block))
        self.assertTrue(all("proposed" in label for label in nodes.values()))

    def test_release_scope_preserves_items_and_closes_supplied_dependencies(self):
        folder = OWNER / "release-scope/examples"
        source = table((folder / "input.md").read_text(), "E3 — Existing backlog")
        output = (folder / "example-output.md").read_text()
        scope = table(output, "Candidate scope")
        self.assertEqual({row["Existing item ID"] for row in scope}, {row["Item ID"] for row in source})
        included = {row["Existing item ID"] for row in scope if row["Included or deferred"] == "included"}
        deferred = {row["Existing item ID"] for row in scope if row["Included or deferred"] == "deferred"}
        prerequisites = {(identifier.strip(), row["Item ID"]) for row in source if row["Item ID"] in included
                         for identifier in row["Prerequisites"].split(",") if identifier.strip() != "none"}
        self.assertTrue(all(prerequisite in included for prerequisite, _ in prerequisites))
        _, nodes, edges = graph(output)
        self.assertEqual({(source, target) for source, arrow, label, _, target in edges if label == "required by" and arrow == "--"}, prerequisites)
        self.assertEqual({source for source, arrow, _, _, target in edges if target == "release" and arrow == "-."}, included)
        self.assertFalse(any(source in deferred and target == "release" for source, _, _, _, target in edges))
        self.assertIn("blocked", nodes["release"])
        self.assertTrue(all("included" in nodes[identifier] for identifier in included))
        self.assertTrue(all("deferred" in nodes[identifier] for identifier in deferred))

    def test_outcome_review_calculations_match_supplied_attempt_counts(self):
        folder = MANAGER / "outcome-review/examples"
        source = (folder / "input.md").read_text()
        periods = table(source, "E1 — Measurement extract")
        rates = {row["Period"]: Decimal(row["Helped attempts"]) / Decimal(row["All attempts"]) * 100 for row in periods}
        result = table((folder / "example-output.md").read_text(), "Results")[0]
        for field, period in (("Baseline", "Baseline"), ("Actual", "Follow-up")):
            numerator, denominator, percent = re.fullmatch(r"(\d+)/(\d+) = (\d+)%", result[field]).groups()
            self.assertEqual(Decimal(numerator) / Decimal(denominator) * 100, rates[period])
            self.assertEqual(Decimal(percent), rates[period])
        difference = rates["Follow-up"] - rates["Baseline"]
        change, unit = result["Change"].split(" ", 1)
        self.assertEqual(Decimal(change), difference)
        self.assertEqual(unit, "percentage points")
        target = re.search(r"proposed a (\d+)% target", source).group(1)
        self.assertEqual(result["Target and status"], f"{target}%; proposed, not agreed")

    def test_backlog_examples_preserve_source_ids_and_use_case_links(self):
        for skill, section, identifier in (("backlog-prioritisation", "Proposed order", "Existing ID"),
                                          ("release-scope", "Candidate scope", "Existing item ID")):
            with self.subTest(skill=skill):
                folder = OWNER / skill / "examples"
                source = table((folder / "input.md").read_text(), "E3 — Existing backlog")
                output = table((folder / "example-output.md").read_text(), section)
                self.assertEqual({row[identifier] for row in output}, {row["Item ID"] for row in source})
        folder = OWNER / "backlog-refinement/examples"
        source = {row["Item ID"]: row["Source use case"] for row in table((folder / "input.md").read_text(), "E3 — Existing backlog")}
        output = (folder / "example-output.md").read_text()
        edits = re.findall(r"^### (SPUS\d+) — proposed\n\nSource use case: (SPUC\d+)$", output, re.M)
        self.assertTrue(edits)
        for story, use_case in edits:
            self.assertEqual(source[story], use_case)


if __name__ == "__main__":
    unittest.main()
