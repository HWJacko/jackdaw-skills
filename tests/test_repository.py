import json
from pathlib import Path
import re
import shutil
import tempfile
import unittest
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills/business-analyst"
SKILL_FILES = sorted((ROOT / "skills").glob("*/*/SKILL.md"))


class RepositoryTests(unittest.TestCase):
    def test_marketplace_exposes_every_skill(self):
        marketplace = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
        exposed = set()
        for plugin in marketplace["plugins"]:
            plugin_root = ROOT / plugin["source"]
            for directory in plugin.get("skills", ["./skills"]):
                folder = plugin_root / directory
                self.assertTrue(folder.is_dir())
                exposed.update(path.resolve() for path in folder.glob("*/SKILL.md"))
        self.assertEqual(exposed, {path.resolve() for path in SKILL_FILES})
        self.assertTrue(exposed)

    def test_copied_skills_have_valid_metadata_and_local_references(self):
        with tempfile.TemporaryDirectory() as temporary:
            installed = Path(temporary).resolve() / "skills"
            for source in SKILL_FILES:
                shutil.copytree(source.parent, installed / source.parent.name)
            for skill in installed.iterdir():
                with self.subTest(skill=skill.name):
                    text = (skill / "SKILL.md").read_text()
                    metadata = text.split("---", 2)[1]
                    self.assertIn(f"name: {skill.name}\n", metadata)
                    self.assertRegex(metadata, r"(?m)^description: \S.+$")
                    for document in skill.rglob("*.md"):
                        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", document.read_text()):
                            if "://" in target or target.startswith("#"):
                                continue
                            resolved = (document.parent / target.split("#", 1)[0]).resolve()
                            self.assertTrue(resolved.is_relative_to(installed), (document, target))
                            self.assertTrue(resolved.exists(), (document, target))

    def test_drawio_files_have_valid_connectors(self):
        for path in (ROOT / "skills").glob("*/*/examples/*.drawio"):
            with self.subTest(path=path):
                cells = ET.parse(path).findall(".//mxCell")
                identifiers = [cell.get("id") for cell in cells]
                self.assertEqual(len(identifiers), len(set(identifiers)))
                nodes = {cell.get("id") for cell in cells if cell.get("vertex") == "1"}
                for cell in cells:
                    if cell.get("edge") == "1":
                        self.assertIn(cell.get("source"), nodes)
                        self.assertIn(cell.get("target"), nodes)

    def test_user_flow_formats_show_the_same_steps_and_branches(self):
        folder = SKILLS / "user-flow/examples"
        markdown = (folder / "example-output.md").read_text()
        mermaid = markdown.split("```mermaid\n", 1)[1].split("```", 1)[0]
        cells = ET.parse(folder / "example-output.drawio").findall(".//mxCell")
        node_pattern = r"(\w+)(?:\(\[([^\]]+)\]\)|\[([^\]]+)\]|\{([^}]+)\})"
        labels = {match[0]: next(value for value in match[1:] if value)
                  for match in re.findall(node_pattern, mermaid)}
        xml_labels = {cell.get("id"): cell.get("value") for cell in cells if cell.get("vertex") == "1"}
        self.assertEqual(labels, xml_labels)
        edge_pattern = r"(\w+)(?:\(\[[^\]]+\]\)|\[[^\]]+\]|\{[^}]+\})?\s*(?:--\s+(.+?)\s+)?-->\s*(\w+)"
        edges = {(source, target, label) for source, label, target in re.findall(edge_pattern, mermaid)}
        xml_edges = {(cell.get("source"), cell.get("target"), cell.get("value", ""))
                     for cell in cells if cell.get("edge") == "1"}
        self.assertTrue(edges)
        self.assertEqual(edges, xml_edges)

    def test_requirements_map_matches_source_relationships(self):
        use_cases = (SKILLS / "use-case-extraction/examples/example-output.md").read_text()
        stories = (SKILLS / "requirement-construction/examples/example-output.md").read_text()
        story_id = re.search(r"^## (\w+US\d+)$", stories, re.M).group(1)
        parent_id = re.search(r"^Source use case: (\w+UC\d+)$", stories, re.M).group(1)
        epic_id = re.search(r"^## Use Cases — (\w+EP\d+)$", use_cases, re.M).group(1)
        use_case_ids = set(re.findall(r"^\| (\w+UC\d+) \|", use_cases, re.M))
        self.assertIn(parent_id, use_case_ids)
        expected = {("NW", epic_id), (parent_id, story_id)} | {(epic_id, identifier) for identifier in use_case_ids}
        cells = ET.parse(SKILLS / "requirements-map/examples/example-output.drawio").findall(".//mxCell")
        labels = {cell.get("id"): cell.get("value").split()[0]
                  for cell in cells if cell.get("vertex") == "1"}
        xml_edges = {(labels[cell.get("source")], labels[cell.get("target")])
                     for cell in cells if cell.get("edge") == "1"}
        self.assertEqual(expected, xml_edges)
        markdown = (SKILLS / "requirements-map/examples/example-output.md").read_text()
        mermaid = markdown.split("```mermaid\n", 1)[1].split("```", 1)[0]
        parents = []
        mermaid_edges = set()
        for line in mermaid.splitlines()[1:]:
            indent = len(line) - len(line.lstrip())
            identifier = re.search(r"\bNW(?:EP\d+|UC\d+|US\d+)?\b", line).group(0)
            while parents and parents[-1][0] >= indent:
                parents.pop()
            if parents:
                mermaid_edges.add((parents[-1][1], identifier))
            parents.append((indent, identifier))
        self.assertEqual(expected, mermaid_edges)


if __name__ == "__main__":
    unittest.main()
