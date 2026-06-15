"""Repository health checks for the public image-processing knowledge base."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str]) -> int:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    return result.returncode


def check_graph() -> list[str]:
    path = ROOT / "graph" / "knowledge_graph.json"
    errors: list[str] = []
    if not path.exists():
        return [f"missing {path.relative_to(ROOT)}"]
    graph = json.loads(path.read_text(encoding="utf-8"))
    node_ids = {node["id"] for node in graph.get("nodes", [])}
    for edge in graph.get("edges", []):
        if edge.get("source") not in node_ids:
            errors.append(f"graph edge has missing source: {edge}")
        if edge.get("target") not in node_ids:
            errors.append(f"graph edge has missing target: {edge}")
    return errors


def check_public_boundaries() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    tracked = result.stdout.splitlines()
    errors = []
    for path in tracked:
        normalized = path.replace("\\", "/")
        if normalized.endswith(".pdf"):
            errors.append(f"tracked PDF should not be public: {path}")
        if normalized.startswith("raw/books/") and normalized != "raw/books/README.md":
            errors.append(f"tracked raw book file should not be public: {path}")
        if normalized.startswith("raw/extracted_text/") and normalized != "raw/extracted_text/README.md":
            errors.append(f"tracked extracted text should not be public: {path}")
        if normalized.startswith("raw/temp/") and normalized != "raw/temp/README.md":
            errors.append(f"tracked temp file should not be public: {path}")
    return errors


def check_figures() -> list[str]:
    required = [
        "ch02_gamma_curves.png",
        "ch02_contrast_stretching.png",
        "ch02_gray_window_slicing.png",
        "ch02_histogram_equalization.png",
        "ch02_adaptive_histogram_equalization.png",
        "ch02_pseudo_color_lut.png",
        "ch02_retinex_decomposition.png",
        "README.md",
    ]
    folder = ROOT / "assets" / "extracted_figures"
    return [f"missing assets/extracted_figures/{name}" for name in required if not (folder / name).exists()]


def main() -> int:
    errors: list[str] = []
    for command in [
        [sys.executable, "tools/check_reading_blocks.py"],
        [sys.executable, "tools/check_links.py"],
        [sys.executable, "tools/check_coverage.py"],
    ]:
        if run(command) != 0:
            errors.append(f"command failed: {' '.join(command)}")
    errors.extend(check_graph())
    errors.extend(check_public_boundaries())
    errors.extend(check_figures())

    if errors:
        print("Health check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Health check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
