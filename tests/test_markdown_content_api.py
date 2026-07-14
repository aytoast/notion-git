import contextlib
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(name, relative_path):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class MarkdownContentApiTests(unittest.TestCase):
    def test_targeted_update_uses_markdown_endpoint(self):
        update = load_module("update_page", "api/update-page/scripts/update-notion-page.py")
        requests = []
        update.run_curl = lambda method, path, data=None: requests.append((method, path, json.loads(data))) or b"{}"
        previous_argv = sys.argv
        sys.argv = ["script", "page-id", "--update", "old", "new"]
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                update.main()
        finally:
            sys.argv = previous_argv
        self.assertEqual(requests, [("patch", "/pages/page-id/markdown", {
            "type": "update_content",
            "update_content": {"content_updates": [{"old_str": "old", "new_str": "new"}]},
        })])

    def test_pull_uses_block_fallback_for_unknown_markdown(self):
        pull = load_module("pull", "skills/notion-pull/scripts/notion-pull.py")
        def fake_run(script, *args):
            if script == pull.GET_MARKDOWN:
                return {"markdown": "<unknown/>", "truncated": True, "unknown_block_ids": ["block-id"]}
            if script == pull.GET_BLOCK_CHILDREN:
                return {"results": [{"id": "block-id", "type": "paragraph", "paragraph": {"rich_text": [{"plain_text": "Fallback"}]}}]}
            raise AssertionError(script)
        pull.run_python_script = fake_run
        pull.SHADOW_INDEX = {}
        with tempfile.TemporaryDirectory() as temp_dir:
            page_dir = Path(temp_dir) / "page"; page_dir.mkdir()
            pull.sync_page(page_dir, "page-id", {"properties": {}})
            self.assertIn("Fallback", (page_dir / "page.md").read_text(encoding="utf-8"))
        self.assertTrue(pull.SHADOW_INDEX["page-id"]["block_fallback"])

    def test_push_uses_targeted_markdown_update(self):
        push = load_module("push", "skills/notion-push/scripts/notion-push.py")
        calls = []
        push.run_python_script = lambda *args: calls.append(args) or {}
        self.assertTrue(push.markdown_update("page-id", "before old after", "before new after"))
        self.assertEqual(calls[0], (push.UPDATE_PAGE, "page-id", "--update", "old", "new"))


if __name__ == "__main__":
    unittest.main()
