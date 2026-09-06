"""Run the dependency-light self-test from the project root:

    python run_self_test.py
"""

from __future__ import annotations

import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from kohler_agent.run_self_test import run_self_test  # noqa: E402

if __name__ == "__main__":
    run_self_test()
