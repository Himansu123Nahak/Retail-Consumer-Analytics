"""
============================================================
git_setup.py
============================================================
Run this AFTER Git is installed to initialise the repository
and create the first commit.

Usage:
    py git_setup.py
============================================================
"""

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
GIT_IGNORE   = PROJECT_ROOT / ".gitignore"


def run(cmd, check=True):
    result = subprocess.run(cmd, capture_output=True, text=True,
                             cwd=str(PROJECT_ROOT))
    if result.stdout.strip():
        print(f"  {result.stdout.strip()}")
    if result.returncode != 0 and check:
        print(f"  ERROR: {result.stderr.strip()}")
        return False
    return True


def main():
    print("=" * 55)
    print("  Retail Analytics — Git Repository Setup")
    print("=" * 55)

    # Check git is available
    r = subprocess.run(["git", "--version"], capture_output=True, text=True)
    if r.returncode != 0:
        print("\n  ERROR: Git is not installed or not in PATH.")
        print("  Install via: winget install --id Git.Git -e")
        print("  Then open a NEW PowerShell window and re-run this script.")
        sys.exit(1)
    print(f"\n  Git found: {r.stdout.strip()}")

    # Git init
    print("\n  [1/4] Initialising repository...")
    git_dir = PROJECT_ROOT / ".git"
    if git_dir.exists():
        print("       Already initialised.")
    else:
        run(["git", "init"])

    # Set default branch to main
    run(["git", "checkout", "-b", "main"], check=False)

    # Configure user (basic)
    print("\n  [2/4] Staging all files...")
    run(["git", "add", "."])

    # Status summary
    result = subprocess.run(["git", "status", "--short"],
                              capture_output=True, text=True,
                              cwd=str(PROJECT_ROOT))
    lines = result.stdout.strip().split("\n")
    print(f"       {len(lines)} files staged.")

    # Commit
    print("\n  [3/4] Creating initial commit...")
    run(["git", "commit", "-m",
          "Initial commit: Retail Consumer Intelligence Platform\n\n"
          "- 200K transactions, 50K customers, 5K products, 200 stores\n"
          "- PostgreSQL star schema (4 dims, 3 facts, 5 views)\n"
          "- 24 SQL analytics queries\n"
          "- 17 Python scripts (ETL, EDA, RFM, CLV, stats)\n"
          "- 23 EDA charts\n"
          "- Excel workbook (6 sheets)\n"
          "- Full documentation suite"])

    print("\n  [4/4] Done!")
    print()
    print("  Next — push to GitHub:")
    print("  1. Create a repo on https://github.com/new")
    print("  2. Run:")
    print("     git remote add origin https://github.com/YOUR_USERNAME/Retail-Consumer-Analytics.git")
    print("     git push -u origin main")
    print()
    print("=" * 55)


if __name__ == "__main__":
    main()
