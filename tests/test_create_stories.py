import contextlib
import importlib.util
import io
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/business-analyst/requirement-construction-jira/scripts/create_stories.py"
SPEC = importlib.util.spec_from_file_location("create_stories", SCRIPT)
jira = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(jira)

STORY = """## NWUS001
Source use case: NWUC001
As an editor I want to create a page so that I can publish content

Scenario 1: Create a page
Given I am logged in
When I save a page
Then I see a preview

AC1: A title is required
"""
SECOND_STORY = STORY.replace("NWUS001", "NWUS002")
CONFIG = {
    "JIRA_BASE_URL": "https://example.invalid/",
    "JIRA_EMAIL": "test@example.invalid",
    "JIRA_API_TOKEN": "test-token",
    "JIRA_PROJECT": "TEST",
}


class CreateStoriesTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        previous = Path.cwd()
        os.chdir(self.directory.name)
        self.addCleanup(os.chdir, previous)
        self.environment = patch.dict(os.environ, {}, clear=True)
        self.environment.start()
        self.addCleanup(self.environment.stop)
        self.path = Path("stories.md")
        self.path.write_text(STORY, encoding="utf-8")
        self.output = io.StringIO()
        self.response = Mock()
        self.response.json.return_value = {"key": "TEST-1"}
        self.post = patch.object(jira.requests, "post", return_value=self.response).start()
        self.addCleanup(patch.stopall)

    def run_script(self):
        with patch.object(sys, "argv", [str(SCRIPT), str(self.path)]):
            with contextlib.redirect_stdout(self.output), contextlib.redirect_stderr(self.output):
                jira.main()

    def test_environment_credentials_and_story_mapping(self):
        os.environ.update(CONFIG)
        self.run_script()
        self.post.assert_called_once()
        self.assertEqual(self.post.call_args.args[0], "https://example.invalid/rest/api/2/issue")
        fields = self.post.call_args.kwargs["json"]["fields"]
        self.assertEqual(fields["project"], {"key": "TEST"})
        self.assertEqual(fields["summary"], STORY.splitlines()[2])
        self.assertIn("NWUS001", fields["description"])
        self.assertIn("AC1: A title is required", fields["description"])
        self.assertEqual(self.path.read_text(), STORY.replace("## NWUS001", "## NWUS001 (TEST-1)"))
        self.assertIn("NWUS001 -> TEST-1", self.output.getvalue())

    def test_environment_overrides_dotenv(self):
        Path(".env").write_text("\n".join(f"{key}={value}" for key, value in CONFIG.items()))
        os.environ["JIRA_PROJECT"] = "OTHER"
        self.run_script()
        self.assertEqual(self.post.call_args.kwargs["json"]["fields"]["project"], {"key": "OTHER"})

    def test_missing_credentials_keep_local_file(self):
        self.run_script()
        self.post.assert_not_called()
        self.assertEqual(self.path.read_text(), STORY)
        self.assertIn("JIRA_API_TOKEN", self.output.getvalue())

    def test_linked_story_is_not_created_again(self):
        os.environ.update(CONFIG)
        self.path.write_text(STORY.replace("## NWUS001", "## NWUS001 (TEST-1)") + SECOND_STORY)
        self.response.json.return_value = {"key": "TEST-2"}
        self.run_script()
        self.post.assert_called_once()
        self.assertIn("## NWUS001 (TEST-1)", self.path.read_text())
        self.assertIn("## NWUS002 (TEST-2)", self.path.read_text())

    def test_trace_metadata_does_not_create_extra_stories(self):
        traced = STORY.replace("Source use case: NWUC001", "Source use case: NWUC001\nSource outcome: NWOC001\nVerification refs: NWTC001")
        traced += "\n## Trace links\n\n| From ID | To ID | Relationship | Link status | Source |\n| --- | --- | --- | --- | --- |\n| NWUS001 | NWTC001 | checked by | recorded | fixture |\n"
        self.path.write_text(traced)
        os.environ.update(CONFIG)
        self.run_script()
        self.post.assert_called_once()
        self.assertIn("Source outcome: NWOC001", self.path.read_text())
        self.assertIn("## Trace links", self.path.read_text())

    def test_partial_failure_preserves_success_and_blocks_retry(self):
        os.environ.update(CONFIG)
        self.path.write_text(STORY + SECOND_STORY)
        self.post.side_effect = [self.response, jira.requests.ConnectionError(CONFIG["JIRA_API_TOKEN"])]
        self.run_script()
        saved = self.path.read_text()
        self.assertIn("## NWUS001 (TEST-1)", saved)
        self.assertIn("## NWUS002 (JIRA pending)", saved)
        self.assertNotIn(CONFIG["JIRA_API_TOKEN"], self.output.getvalue())
        self.post.reset_mock()
        self.run_script()
        self.post.assert_not_called()
        self.assertEqual(self.path.read_text(), saved)

    def test_request_is_marked_before_post(self):
        os.environ.update(CONFIG)

        def respond(*args, **kwargs):
            self.assertIn("## NWUS001 (JIRA pending)", self.path.read_text())
            return self.response

        self.post.side_effect = respond
        self.run_script()

    def test_missing_response_key_keeps_pending_marker(self):
        os.environ.update(CONFIG)
        self.response.json.return_value = {}
        self.run_script()
        self.assertIn("## NWUS001 (JIRA pending)", self.path.read_text())

    def test_http_error_keeps_local_output_without_credentials_in_messages(self):
        os.environ.update(CONFIG)
        self.response.raise_for_status.side_effect = jira.requests.HTTPError(CONFIG["JIRA_API_TOKEN"])
        self.run_script()
        self.assertIn("(JIRA pending)", self.path.read_text())
        self.assertNotIn(CONFIG["JIRA_API_TOKEN"], self.output.getvalue())

    def test_failed_key_save_keeps_pending_marker_and_prints_returned_key(self):
        os.environ.update(CONFIG)
        replace = os.replace
        count = 0

        def fail_after_first_save(source, destination):
            nonlocal count
            count += 1
            if count == 2:
                raise OSError("simulated write failure")
            return replace(source, destination)

        with patch.object(jira.os, "replace", side_effect=fail_after_first_save):
            with self.assertRaises(OSError):
                self.run_script()
        self.assertIn("(JIRA pending)", self.path.read_text())
        self.assertIn("NWUS001 -> TEST-1", self.output.getvalue())
        self.post.reset_mock()
        self.run_script()
        self.post.assert_not_called()

    def test_duplicate_local_ids_stop_before_post(self):
        os.environ.update(CONFIG)
        self.path.write_text(STORY + STORY)
        with self.assertRaises(SystemExit):
            self.run_script()
        self.post.assert_not_called()
        self.assertEqual(self.path.read_text(), STORY + STORY)


if __name__ == "__main__":
    unittest.main()
