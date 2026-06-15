"""Configure the local Obsidian graph view for the study vault.

The .obsidian directory is intentionally ignored by Git, so this script keeps
the useful local graph filters reproducible without committing personal UI
state.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GRAPH_CONFIG = ROOT / ".obsidian" / "graph.json"

GRAPH_SETTINGS = {
    "collapse-filter": False,
    "search": (
        "path:wiki "
        "-file:README "
        "-file:00_导航 "
        "-file:99_术语表 "
        "-path:graph "
        "-path:raw "
        "-path:tools "
        "-path:tests "
        "-path:examples "
        "-path:assets "
        "-path:data"
    ),
    "showTags": False,
    "showAttachments": False,
    "hideUnresolved": True,
    "showOrphans": False,
    "collapse-color-groups": False,
    "colorGroups": [
        {"query": "path:wiki/01_引言", "color": {"a": 1, "rgb": 14701138}},
        {"query": "path:wiki/02_图像增强", "color": {"a": 1, "rgb": 14270531}},
        {"query": "path:wiki/03_图像几何变换", "color": {"a": 1, "rgb": 6196165}},
        {"query": "path:wiki/04_图像去噪", "color": {"a": 1, "rgb": 5616524}},
        {"query": "path:wiki/05_图像锐化", "color": {"a": 1, "rgb": 12870403}},
        {"query": "path:wiki/06_图像的分割", "color": {"a": 1, "rgb": 4087532}},
        {"query": "path:wiki/07_二值图像处理", "color": {"a": 1, "rgb": 9662683}},
        {"query": "path:wiki/08_彩色图像处理", "color": {"a": 1, "rgb": 15836725}},
        {"query": "path:wiki/09_图像变换", "color": {"a": 1, "rgb": 10642260}},
        {"query": "path:wiki/10_图像压缩编码", "color": {"a": 1, "rgb": 13458524}},
        {"query": "path:wiki/11_深度学习与图像处理", "color": {"a": 1, "rgb": 3606271}},
    ],
    "collapse-display": False,
    "showArrow": True,
    "textFadeMultiplier": -0.7,
    "nodeSizeMultiplier": 0.75,
    "lineSizeMultiplier": 0.45,
    "collapse-forces": False,
    "centerStrength": 0.38,
    "repelStrength": 18.0,
    "linkStrength": 0.35,
    "linkDistance": 180,
    "scale": 0.55,
    "close": False,
}


def main() -> None:
    GRAPH_CONFIG.parent.mkdir(parents=True, exist_ok=True)
    GRAPH_CONFIG.write_text(
        json.dumps(GRAPH_SETTINGS, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {GRAPH_CONFIG}")


if __name__ == "__main__":
    main()
