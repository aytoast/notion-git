import json
import os
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path("notion")
API_DIR = Path(__file__).resolve().parent.parent.parent.parent / "api"
UPDATE_PAGE = str(API_DIR / "update-page" / "scripts" / "update-notion-page.py")
UPDATE_BLOCK = str(API_DIR / "update-block" / "scripts" / "update-notion-block.py")
APPEND_BLOCK = str(API_DIR / "append-block-children" / "scripts" / "append-notion-block-children.py")
ARCHIVE_BLOCK = str(API_DIR / "archive-block" / "scripts" / "archive-notion-block.py")
PULL_SCRIPT = str(Path(__file__).resolve().parent.parent.parent / "notion-pull" / "scripts" / "notion-pull.py")


def run_python_script(script_path, *args):
    env = os.environ.copy()
    env["NOTION_VERSION"] = "2026-03-11"
    result = subprocess.run([sys.executable, script_path, *args], capture_output=True, text=True, env=env)
    if result.returncode != 0:
        print(f"Error running {script_path}: {result.stderr or result.stdout}")
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return result.stdout


def page_body(path):
    content = path.read_text(encoding="utf-8")
    if content.startswith("---\n"):
        end = content.find("\n---", 4)
        if end != -1:
            return content[end + 4:].lstrip("\r\n").rstrip()
    return content.rstrip()


def markdown_update(page_id, old_markdown, new_markdown):
    if old_markdown == new_markdown:
        return False
    prefix = 0
    while prefix < min(len(old_markdown), len(new_markdown)) and old_markdown[prefix] == new_markdown[prefix]:
        prefix += 1
    suffix = 0
    while suffix < len(old_markdown) - prefix and suffix < len(new_markdown) - prefix and old_markdown[-1 - suffix] == new_markdown[-1 - suffix]:
        suffix += 1
    old_fragment = old_markdown[prefix:len(old_markdown) - suffix if suffix else len(old_markdown)]
    new_fragment = new_markdown[prefix:len(new_markdown) - suffix if suffix else len(new_markdown)]
    if old_fragment and old_markdown.count(old_fragment) == 1:
        print(f"  [MARKDOWN UPDATE] {len(old_fragment)} -> {len(new_fragment)} characters")
        return run_python_script(UPDATE_PAGE, page_id, "--update", old_fragment, new_fragment) is not None
    print("  [MARKDOWN REPLACE] changed range is ambiguous or insertion-only")
    return run_python_script(UPDATE_PAGE, page_id, "--replace", new_markdown) is not None


def md_to_block(line):
    if line.startswith("# "): return {"type": "heading_1", "heading_1": {"rich_text": [{"text": {"content": line[2:]}}]}}
    if line.startswith("## "): return {"type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": line[3:]}}]}}
    if line.startswith("### "): return {"type": "heading_3", "heading_3": {"rich_text": [{"text": {"content": line[4:]}}]}}
    if line.startswith("- "): return {"type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": line[2:]}}]}}
    return {"type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": line}}]}}


def block_fallback_update(page_id, old_markdown, new_markdown, blocks):
    old_lines, new_lines = old_markdown.split("\n\n"), new_markdown.split("\n\n")
    if len(old_lines) != len(blocks) or len(old_lines) != len(new_lines):
        print("  [BLOCK FALLBACK] structural change requires manual block editing")
        return False
    for old_line, new_line, block in zip(old_lines, new_lines, blocks):
        if old_line != new_line:
            print(f"  [BLOCK UPDATE] {block['id']}")
            if run_python_script(UPDATE_BLOCK, block["id"], json.dumps(md_to_block(new_line))) is None:
                return False
    return True


def page_id_from_yaml(yaml_path):
    for line in yaml_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("id:"):
            return line.split(":", 1)[1].strip().strip('"').strip("'")
    return None


def main():
    if not ROOT_DIR.exists():
        print("No notion directory found. Run notion clone first.")
        return
    index_file = ROOT_DIR / ".notion-index.json"
    if not index_file.exists():
        print("No shadow index found. Run notion pull first.")
        return
    shadow_index = json.loads(index_file.read_text(encoding="utf-8"))
    changed = False
    for root, _, _ in os.walk(ROOT_DIR):
        root_path = Path(root)
        page_md, yaml_path = root_path / "page.md", root_path / "notion.yaml"
        if not page_md.exists() or not yaml_path.exists():
            continue
        page_id = page_id_from_yaml(yaml_path)
        entry = shadow_index.get(page_id)
        if not page_id or not entry:
            continue
        if isinstance(entry, list):
            entry = {"markdown": "\n\n".join(item.get("md_line", "") for item in entry), "block_fallback": True, "blocks": entry}
        old_markdown, new_markdown = entry.get("markdown", ""), page_body(page_md)
        if old_markdown == new_markdown:
            continue
        print(f"\nPushing changes for {page_md}...")
        if entry.get("block_fallback"):
            pushed = block_fallback_update(page_id, old_markdown, new_markdown, entry.get("blocks", []))
        else:
            pushed = markdown_update(page_id, old_markdown, new_markdown)
        changed = changed or pushed
    if changed:
        print("\nPush complete. Refreshing shadow index...")
        run_python_script(PULL_SCRIPT)
    else:
        print("Workspace is clean. Nothing to push.")


if __name__ == "__main__":
    main()
