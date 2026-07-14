import os
import sys
import json
import subprocess
import shutil
from pathlib import Path

# Paths to the Notion API python scripts resolved relatively
API_DIR = Path(__file__).resolve().parent.parent.parent.parent / "api"
GET_PAGE = str(API_DIR / "get-page" / "scripts" / "get-notion-page.py")
GET_BLOCK_CHILDREN = str(API_DIR / "get-block-children" / "scripts" / "get-notion-block-children.py")
QUERY_DATABASE = str(API_DIR / "query-database" / "scripts" / "query-notion-database.py")
GET_MARKDOWN = str(API_DIR / "update-page" / "scripts" / "update-notion-page.py")

ROOT_DIR = Path("notion")
SHADOW_INDEX = {}

def run_python_script(script_path, *args):
    cmd = [sys.executable, script_path, *args]
    env = os.environ.copy()
    env["NOTION_VERSION"] = "2026-03-11"
    res = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if res.returncode != 0:
        print(f"Error running {script_path} with {args}: {res.stderr}")
        return None
    try:
        return json.loads(res.stdout)
    except json.JSONDecodeError:
        return res.stdout

def read_notion_yaml(yaml_path):
    data = {}
    if not yaml_path.exists():
        return data
    lines = yaml_path.read_text("utf-8").splitlines()
    for line in lines:
        if ":" in line:
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip().strip('"').strip("'")
    return data

def write_notion_yaml(yaml_path, type_str, id_str):
    yaml_path.write_text(f'type: "{type_str}"\nid: "{id_str}"\n', encoding="utf-8")

def get_page_title(page_obj):
    props = page_obj.get("properties", {})
    for k, v in props.items():
        if v.get("type") == "title":
            title_arr = v.get("title", [])
            if title_arr:
                return title_arr[0].get("plain_text", "Untitled")
    return "Untitled"

def sync_database(db_dir, db_id):
    print(f"Syncing database {db_id} in {db_dir}")
    remote_data = run_python_script(QUERY_DATABASE, db_id)
    if not remote_data or "results" not in remote_data:
        return
    
    remote_pages = {p["id"]: p for p in remote_data["results"]}
    
    local_pages = {}
    for child in db_dir.iterdir():
        if child.is_dir():
            yaml_path = child / "notion.yaml"
            if yaml_path.exists():
                info = read_notion_yaml(yaml_path)
                if info.get("id"):
                    local_pages[info["id"]] = child

    for local_id, local_dir in local_pages.items():
        if local_id not in remote_pages:
            print(f"Deleting archived local page: {local_dir}")
            shutil.rmtree(local_dir)
            
    for remote_id, page_obj in remote_pages.items():
        title = get_page_title(page_obj)
        safe_title = "".join(c for c in title if c.isalnum() or c in (" ", "-", "_")).strip()
        if not safe_title:
            safe_title = remote_id
        target_dir = local_pages.get(remote_id, db_dir / safe_title)
        if not target_dir.exists():
            target_dir.mkdir(parents=True)
            write_notion_yaml(target_dir / "notion.yaml", "page", remote_id)
        sync_page(target_dir, remote_id, page_obj)

def export_blocks(page_id):
    blocks = run_python_script(GET_BLOCK_CHILDREN, page_id)
    if not blocks or "results" not in blocks:
        return None, []
    lines, shadow = [], []
    for block in blocks.get("results", []):
        b_type = block.get("type")
        b_data = block.get(b_type, {})
        text = "".join(t.get("plain_text", "") for t in b_data.get("rich_text", []))
        if b_type == "paragraph": line = text
        elif b_type.startswith("heading_"): line = f"{'#' * int(b_type.split('_')[1])} {text}"
        elif b_type == "bulleted_list_item": line = f"- {text}"
        elif b_type == "numbered_list_item": line = f"1. {text}"
        elif b_type == "child_database":
            title = b_data.get("title", "Database"); line = f"- [{title}](./{title.lower()}/database.md)"
        elif b_type == "child_page":
            title = b_data.get("title", "Page"); line = f"- [{title}](./{title.lower()}/page.md)"
        else: line = text
        lines.append(line)
        shadow.append({"id": block.get("id"), "type": b_type, "md_line": line})
    return "\n\n".join(lines).strip(), shadow

def sync_page(page_dir, page_id, page_metadata=None):
    print(f"Syncing page {page_id} in {page_dir}")
    if not page_metadata:
        page_metadata = run_python_script(GET_PAGE, page_id)

    markdown_response = run_python_script(GET_MARKDOWN, page_id, "--read-markdown")
    complete_markdown = isinstance(markdown_response, dict) and not markdown_response.get("truncated") and not markdown_response.get("unknown_block_ids")
    if complete_markdown:
        body = markdown_response.get("markdown", "").strip()
        SHADOW_INDEX[page_id] = {"markdown": body, "block_fallback": False}
    else:
        body, blocks = export_blocks(page_id)
        if body is None:
            return
        SHADOW_INDEX[page_id] = {"markdown": body, "block_fallback": True, "blocks": blocks}

    fm_lines = ["---", f"id: {page_id}"]
    if page_metadata:
        fm_lines.append(f"title: {get_page_title(page_metadata)}")
    fm_lines.append("---")
    page_md = page_dir / "page.md"
    new_content = "\n".join(fm_lines) + "\n\n" + body.rstrip() + "\n"
    
    if page_md.exists():
        old_content = page_md.read_text("utf-8")
        if old_content.strip() != new_content.strip():
            print(f"Updating local page.md for {page_id}")
            page_md.write_text(new_content, "utf-8")
    else:
        print(f"Creating local page.md for {page_id}")
        page_md.write_text(new_content, "utf-8")

def main():
    global SHADOW_INDEX
    if not ROOT_DIR.exists():
        print("No notion directory found.")
        return
        
    index_file = ROOT_DIR / ".notion-index.json"
    if index_file.exists():
        try:
            SHADOW_INDEX = json.loads(index_file.read_text("utf-8"))
        except:
            SHADOW_INDEX = {}

    for root, dirs, files in os.walk(ROOT_DIR):
        root_path = Path(root)
        yaml_path = root_path / "notion.yaml"
        if yaml_path.exists():
            info = read_notion_yaml(yaml_path)
            n_type = info.get("type")
            n_id = info.get("id")
            if not n_id:
                continue

            if n_type == "database":
                sync_database(root_path, n_id)
            elif n_type == "page" and root_path == ROOT_DIR:
                sync_page(root_path, n_id)

    index_file.write_text(json.dumps(SHADOW_INDEX, indent=2), "utf-8")

if __name__ == "__main__":
    main()
