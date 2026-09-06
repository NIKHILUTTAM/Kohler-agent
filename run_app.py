"""Convenience entry point so the app can be launched as:

    streamlit run run_app.py

from the project root, without needing `pip install -e .` first (it adds
`src/` to sys.path itself).
"""

from __future__ import annotations

import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from kohler_agent.app import run_streamlit  # noqa: E402

if __name__ == "__main__":
    run_streamlit()
