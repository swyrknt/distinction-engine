#!/usr/bin/env python3
"""
Pre-Push Status Check

Runs all quality checks before pushing code. Used locally by developers
and by GitHub Actions for pull request validation.

Usage:
    python tools/status_check.py

Exit codes:
    0: All checks passed
    1: One or more checks failed
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd: list, description: str) -> bool:
    """
    Execute command and report results.

    Returns True if command succeeds, False otherwise.
    """
    print(f"\n{'=' * 70}")
    print(f"Running: {description}")
    print(f"{'=' * 70}")

    try:
        result = subprocess.run(
            cmd,
            cwd=Path(__file__).parent.parent,
            capture_output=False,
            text=True
        )

        if result.returncode == 0:
            print(f"✅ {description} passed")
            return True
        else:
            print(f"❌ {description} failed")
            return False

    except Exception as e:
        print(f"❌ {description} failed with exception: {e}")
        return False


def main():
    """Run all status checks."""
    print("\nDistinction Engine - Status Check")
    print("=" * 70)

    checks = []

    checks.append(run_command(
        [sys.executable, "-m", "pytest", "tests/", "-v"],
        "Test Suite"
    ))

    print(f"\n{'=' * 70}")
    print("Summary")
    print(f"{'=' * 70}")

    passed = sum(checks)
    total = len(checks)

    print(f"Checks passed: {passed}/{total}")

    if all(checks):
        print("\n✅ All checks passed. Ready to push.")
        return 0
    else:
        print("\n❌ Some checks failed. Please fix before pushing.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
