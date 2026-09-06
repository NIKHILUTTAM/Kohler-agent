"""Local LLM runtime management: starting Ollama and pulling models on demand.

Isolated from graph.py so the "is the local model server alive, and does it
have the right models" concern can be tested/reused independently of the
LangGraph reasoning pipeline.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import time
from typing import Any

from . import config


def ollama_request(method: str, path: str, **kwargs: Any) -> Any:
    import requests

    response = requests.request(method, f"{config.OLLAMA_BASE_URL}{path}", **kwargs)
    response.raise_for_status()
    return response


def ollama_is_ready() -> bool:
    try:
        return ollama_request("GET", "/api/tags", timeout=3).ok
    except Exception:
        return False


def start_ollama_if_needed() -> None:
    if ollama_is_ready():
        return
    executable = shutil.which("ollama")
    if not executable:
        raise RuntimeError(
            "Ollama is not installed or is not on PATH. Install it once, then rerun:\n"
            "  Linux: curl -fsSL https://ollama.com/install.sh | sh\n"
            "  macOS: https://ollama.com/download/mac\n"
            "  Windows: https://ollama.com/download/windows"
        )
    options: dict[str, Any] = {"stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL}
    if os.name != "nt":
        options["start_new_session"] = True
    subprocess.Popen([executable, "serve"], **options)
    deadline = time.time() + 30
    while time.time() < deadline:
        if ollama_is_ready():
            return
        time.sleep(0.5)
    raise RuntimeError("Ollama did not become ready. Start it manually with: ollama serve")


def model_name_matches(installed_name: str, requested_name: str) -> bool:
    return installed_name == requested_name or (
        ":" not in requested_name and installed_name == f"{requested_name}:latest"
    )


def ensure_ollama_model(model_name: str) -> None:
    installed = ollama_request("GET", "/api/tags", timeout=10).json().get("models", [])
    names = {str(model.get("name", "")) for model in installed}
    if any(model_name_matches(name, model_name) for name in names):
        return
    print(f"Downloading local model {model_name}; this may take a while...")
    import requests

    with requests.post(
        f"{config.OLLAMA_BASE_URL}/api/pull",
        json={"name": model_name, "stream": True},
        stream=True,
        timeout=(10, 3600),
    ) as response:
        response.raise_for_status()
        last_status = ""
        for line in response.iter_lines(decode_unicode=True):
            if not line:
                continue
            try:
                event = json.loads(line)
                status = event.get("status", "")
                if status and status != last_status:
                    print(f"  {status}")
                    last_status = status
                if event.get("error"):
                    raise RuntimeError(event["error"])
            except json.JSONDecodeError:
                continue
