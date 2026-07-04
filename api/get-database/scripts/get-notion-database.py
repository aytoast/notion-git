import os
import shutil
import subprocess
import sys
from pathlib import Path

api_base = "https://api.notion.com"
default_version = "2026-03-11"
token_env_names = ("NOTION_PAT",)

def load_env() -> None:
    for path in (Path.cwd(), Path(__file__).parent.parent.parent.parent):
        env_file = path / ".env"
        if env_file.is_file():
            try:
                for line in env_file.read_text(encoding="utf-8").splitlines():
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" in line:
                        k, v = line.split("=", 1)
                        os.environ.setdefault(k.strip(), v.strip())
                break
            except Exception:
                pass

def get_token() -> str:
    load_env()
    for name in token_env_names:
        value = os.environ.get(name)
        if value:
            return value
    raise SystemExit("missing notion token. set one of: " + ", ".join(token_env_names))

def get_curl_path() -> str:
    for name in ("curl.exe", "curl"):
        path = shutil.which(name)
        if path:
            return path
    raise SystemExit("curl was not found on path")

def run_curl(method: str, path: str, data: str | None = None) -> bytes:
    token = get_token()
    version = os.environ.get("NOTION_VERSION", default_version)
    url = api_base + path if path.startswith("http") else api_base + "/v1" + path
    args = [
        get_curl_path(), "--silent", "--show-error", "--ssl-no-revoke", "--insecure",
        "--fail-with-body", "--location", "--request", method.upper(), url,
        "--header", f"Authorization: Bearer {token}",
        "--header", f"Notion-Version: {version}",
        "--header", "Accept: application/json",
    ]
    if data is not None:
        args.extend(["--header", "Content-Type: application/json", "--data-raw", data])
    result = subprocess.run(args, capture_output=True, check=False)
    if result.returncode != 0:
        sys.stderr.buffer.write(result.stderr)
        if result.stdout:
            sys.stderr.buffer.write(result.stdout)
        raise SystemExit(result.returncode)
    return result.stdout

def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("usage: get-notion-database.py <database_id>")
    database_id = sys.argv[1]
    raw = run_curl("get", f"/databases/{database_id}")
    sys.stdout.write(raw.decode("utf-8", errors="replace"))

if __name__ == "__main__":
    main()
