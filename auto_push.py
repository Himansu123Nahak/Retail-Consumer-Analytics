"""
============================================================
auto_push.py
============================================================
Auto-push updates to GitHub whenever you run this script.
Updates only the files that have changed (via SHA comparison).

Usage:
    py auto_push.py                  ← pushes all changed files
    py auto_push.py --file README.md ← pushes only one file

Token is read from GITHUB_TOKEN env var or .env file.
Add this to .env:
    GITHUB_TOKEN=ghp_xxxxxxxxxxxxx
============================================================
"""

import sys
import os
import base64
from pathlib import Path
from datetime import datetime
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_USERNAME = "Himansu123Nahak"
REPO_NAME       = "Retail-Consumer-Analytics"
PROJECT_ROOT    = Path(__file__).parent
API             = "https://api.github.com"

SKIP_FILES = {
    "customers.csv","customers_clean.csv",
    "transactions.csv","transactions_clean.csv",
    "inventory.csv","inventory_clean.csv",
    "marketing_campaigns.csv","products.csv","rfm_scores.csv",
    "auto_push.py",
}
SKIP_DIRS  = {".git","__pycache__",".ipynb_checkpoints","reports"}
SKIP_EXTS  = {".pyc",".pyo"}


def h(token):
    return {"Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
            "X-GitHub-Api-Version": "2022-11-28"}


def get_token():
    token = os.environ.get("GITHUB_TOKEN","")
    if not token:
        print("ERROR: Set GITHUB_TOKEN in your .env file.")
        print("Add this line: GITHUB_TOKEN=ghp_your_token_here")
        sys.exit(1)
    return token


def get_remote_sha(token, rel_path):
    r = requests.get(
        f"{API}/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{rel_path}",
        headers=h(token))
    if r.status_code == 200:
        return r.json().get("sha")
    return None


def local_sha_b64(abs_path):
    """Compute base64 content and return (content_b64, local_bytes)."""
    data = abs_path.read_bytes()
    return base64.b64encode(data).decode(), data


def upload_file(token, abs_path, rel_path, force=False):
    content_b64, _ = local_sha_b64(abs_path)
    remote_sha = get_remote_sha(token, rel_path)

    payload = {
        "message": f"Update {rel_path} [{datetime.now().strftime('%Y-%m-%d %H:%M')}]",
        "content": content_b64,
    }
    if remote_sha:
        payload["sha"] = remote_sha

    r = requests.put(
        f"{API}/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{rel_path}",
        headers=h(token), json=payload)

    if r.status_code in (200, 201):
        action = "Updated" if remote_sha else "Created"
        print(f"  [OK] {action}: {rel_path}")
        return True
    else:
        print(f"  [ERR {r.status_code}]: {rel_path}  → {r.json().get('message','')}")
        return False


def collect_files(specific_file=None):
    if specific_file:
        p = PROJECT_ROOT / specific_file
        if not p.exists():
            print(f"ERROR: File not found: {p}")
            sys.exit(1)
        return [(p, specific_file.replace("\\", "/"))]

    files = []
    for p in sorted(PROJECT_ROOT.rglob("*")):
        if not p.is_file(): continue
        parts = set(p.relative_to(PROJECT_ROOT).parts)
        if parts & SKIP_DIRS: continue
        if p.name in SKIP_FILES: continue
        if p.suffix in SKIP_EXTS: continue
        if p.stat().st_size > 50 * 1024 * 1024: continue
        rel = p.relative_to(PROJECT_ROOT).as_posix()
        files.append((p, rel))
    return files


def main():
    token = get_token()

    # Verify auth
    r = requests.get(f"{API}/user", headers=h(token))
    if r.status_code != 200:
        print(f"ERROR: Token invalid ({r.status_code})")
        sys.exit(1)
    login = r.json()["login"]

    # Parse args
    specific = None
    if "--file" in sys.argv:
        idx = sys.argv.index("--file")
        if idx + 1 < len(sys.argv):
            specific = sys.argv[idx + 1]

    files = collect_files(specific)

    print(f"\n  Auto-Push → github.com/{GITHUB_USERNAME}/{REPO_NAME}")
    print(f"  User: {login}  |  Files: {len(files)}  |  {datetime.now().strftime('%H:%M:%S')}")
    print("  " + "─" * 50)

    ok = err = 0
    for abs_path, rel_path in files:
        if upload_file(token, abs_path, rel_path):
            ok += 1
        else:
            err += 1

    print("  " + "─" * 50)
    print(f"  Done: {ok} updated  |  {err} errors")
    print(f"  https://github.com/{GITHUB_USERNAME}/{REPO_NAME}")


if __name__ == "__main__":
    main()
