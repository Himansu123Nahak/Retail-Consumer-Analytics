"""
============================================================
push_to_github.py
============================================================
Pushes the entire project to GitHub using the GitHub REST API.
No git installation required — uses only Python + requests.

Usage:
    1. Generate a GitHub Personal Access Token (PAT):
       - Go to: https://github.com/settings/tokens/new
       - Select scopes: repo (full control)
       - Click "Generate token" — copy it immediately
    
    2. Run this script:
       py push_to_github.py

    3. Enter your token when prompted.

What it does:
    - Creates repo "Retail-Consumer-Analytics" on GitHub
    - Uploads all project files (respecting .gitignore)
    - Sets a proper description and topics
============================================================
"""

import os
import sys
import base64
import json
from pathlib import Path

try:
    import requests
except ImportError:
    print("Installing requests...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "requests", "-q"])
    import requests

# ── Config ────────────────────────────────────────────────────
GITHUB_USERNAME = "Himansu123Nahak"
REPO_NAME       = "Retail-Consumer-Analytics"
REPO_DESC       = (
    "End-to-end Retail Consumer Intelligence Platform | "
    "200K transactions | Python | SQL | PostgreSQL | Excel | Power BI"
)
REPO_TOPICS     = ["data-analytics","python","sql","postgresql","power-bi",
                    "excel","retail-analytics","pandas","matplotlib","seaborn"]

PROJECT_ROOT    = Path(__file__).parent

# Files/dirs to EXCLUDE from upload (large data files, generated pngs, etc.)
EXCLUDE_DIRS  = {".git","__pycache__",".ipynb_checkpoints"}
EXCLUDE_EXTS  = {".pyc",".pyo",".pyd"}
# Keep CSVs small — skip raw/large ones but keep processed summaries
EXCLUDE_FILES = {
    "customers.csv","customers_clean.csv",
    "transactions.csv","transactions_clean.csv",
    "inventory.csv","inventory_clean.csv",
    "marketing_campaigns.csv",
    "products.csv",
    "rfm_scores.csv",
}


def get_token():
    token = os.environ.get("GITHUB_TOKEN", "")
    if not token:
        print("\n" + "="*55)
        print("  GitHub Personal Access Token Required")
        print("="*55)
        print("  1. Open: https://github.com/settings/tokens/new")
        print("  2. Note: 'Retail Analytics Upload'")
        print("  3. Expiry: 7 days")
        print("  4. Scope: check 'repo'")
        print("  5. Click 'Generate token' and COPY it")
        print("="*55)
        token = input("\n  Paste your token here: ").strip()
    return token


def api(method, url, token, **kwargs):
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    return requests.request(method, f"https://api.github.com{url}",
                             headers=headers, **kwargs)


def create_repo(token):
    print(f"\n  Creating repository: {REPO_NAME}...")
    r = api("POST", "/user/repos", token, json={
        "name":        REPO_NAME,
        "description": REPO_DESC,
        "private":     False,
        "auto_init":   False,
    })
    if r.status_code == 201:
        print(f"  [OK] Repository created: {r.json()['html_url']}")
        return True
    elif r.status_code == 422:
        print(f"  [OK] Repository already exists — will update files.")
        return True
    else:
        print(f"  [ERROR] {r.status_code}: {r.text}")
        return False


def file_to_b64(path: Path) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def get_existing_sha(token, rel_path):
    r = api("GET", f"/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{rel_path}", token)
    if r.status_code == 200:
        return r.json().get("sha")
    return None


def upload_file(token, path: Path, rel_path: str, idx: int, total: int):
    b64 = file_to_b64(path)
    sha = get_existing_sha(token, rel_path)
    payload = {
        "message": f"Add {rel_path}",
        "content": b64,
    }
    if sha:
        payload["sha"] = sha

    r = api("PUT", f"/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{rel_path}",
             token, json=payload)
    status = "[OK]  " if r.status_code in (200, 201) else f"[{r.status_code}]"
    bar    = "#" * int((idx / total) * 30)
    print(f"  [{bar:<30}] {idx}/{total}  {status} {rel_path[:55]}", end="\r")
    return r.status_code in (200, 201)


def collect_files():
    files = []
    for p in sorted(PROJECT_ROOT.rglob("*")):
        if not p.is_file():
            continue
        # Skip excluded dirs
        if any(exc in p.parts for exc in EXCLUDE_DIRS):
            continue
        # Skip excluded extensions
        if p.suffix.lower() in EXCLUDE_EXTS:
            continue
        # Skip large data files
        if p.name in EXCLUDE_FILES:
            continue
        # Skip files >10 MB
        if p.stat().st_size > 10 * 1024 * 1024:
            continue
        # Skip this script itself from repo — optional
        rel = p.relative_to(PROJECT_ROOT).as_posix()
        files.append((p, rel))
    return files


def set_topics(token):
    r = api("PUT", f"/repos/{GITHUB_USERNAME}/{REPO_NAME}/topics",
             token, json={"names": REPO_TOPICS})
    if r.status_code == 200:
        print(f"\n  [OK] Topics set: {', '.join(REPO_TOPICS)}")


def main():
    print("="*55)
    print("  Retail Analytics → GitHub Upload")
    print(f"  Target: github.com/{GITHUB_USERNAME}/{REPO_NAME}")
    print("="*55)

    token = get_token()
    if not token:
        print("  No token provided. Exiting.")
        sys.exit(1)

    # Verify token
    r = api("GET", "/user", token)
    if r.status_code != 200:
        print(f"  [ERROR] Invalid token: {r.status_code}")
        sys.exit(1)
    user = r.json()
    print(f"\n  Authenticated as: {user['login']} ({user.get('name','')})")

    # Create repo
    if not create_repo(token):
        sys.exit(1)

    # Collect files
    files = collect_files()
    print(f"\n  Files to upload: {len(files)}")

    # Upload
    ok = err = 0
    for i, (path, rel) in enumerate(files, 1):
        if upload_file(token, path, rel, i, len(files)):
            ok += 1
        else:
            err += 1

    print()  # newline after progress bar

    # Set topics
    set_topics(token)

    # Summary
    print()
    print("="*55)
    print(f"  Upload complete!")
    print(f"  Uploaded:  {ok} files")
    if err:
        print(f"  Errors:    {err} files")
    print(f"  URL: https://github.com/{GITHUB_USERNAME}/{REPO_NAME}")
    print("="*55)


if __name__ == "__main__":
    main()
