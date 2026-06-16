"""生成本地 Obsidian Graph View 配置。

Graph View 只作为辅助关系浏览，不承担固定章节布局。固定课程地图请使用
Obsidian Canvas。本脚本会把 .obsidian/graph.json 恢复为干净过滤配置：
只显示 wiki/ 下的 Markdown 学习笔记，排除 Canvas 和维护文件。
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GRAPH_CONFIG = ROOT / ".obsidian" / "graph.json"

CHAPTER_GROUPS = [
    ("path:wiki/01_引言", 0x7DD3FC),
    ("path:wiki/02_图像增强", 0xFB923C),
    ("path:wiki/03_图像几何变换", 0x86EFAC),
    ("path:wiki/04_图像去噪", 0xF0ABFC),
    ("path:wiki/05_图像锐化", 0xC4B5FD),
    ("path:wiki/06_图像的分割", 0xFDE047),
    ("path:wiki/07_二值图像处理", 0x67E8F9),
    ("path:wiki/08_彩色图像处理", 0xFB7185),
    ("path:wiki/09_图像变换", 0xBEF264),
    ("path:wiki/10_图像压缩编码", 0x93C5FD),
    ("path:wiki/11_深度学习与图像处理", 0xFBBF24),
]

# Obsidian Graph View 使用搜索语法过滤节点。这里显式排除 .canvas，
# 避免章节 Canvas 和总览 Canvas 被当作图谱节点。
GRAPH_SEARCH = (
    "path:wiki "
    "-file:.canvas "
    "-file:canvas "
    "-path:.canvas "
    "-file:README "
    "-file:00_导航 "
    "-file:99_术语表 "
    "-path:wiki/98_习题索引 "
    "-path:graph "
    "-path:raw "
    "-path:tools "
    "-path:tests "
    "-path:examples "
    "-path:assets "
    "-path:data "
    "-path:templates "
    "-file:index "
    "-file:coverage_report "
    "-file:AGENTS"
)

GRAPH_SETTINGS = {
    "collapse-filter": False,
    "search": GRAPH_SEARCH,
    "showTags": False,
    "showAttachments": False,
    "hideUnresolved": True,
    "showOrphans": False,
    "collapse-color-groups": False,
    "colorGroups": [{"query": query, "color": {"a": 1, "rgb": rgb}} for query, rgb in CHAPTER_GROUPS],
    "collapse-display": False,
    "showArrow": True,
    "textFadeMultiplier": -1.15,
    "nodeSizeMultiplier": 0.7,
    "lineSizeMultiplier": 0.18,
    "collapse-forces": False,
    "centerStrength": 0.1,
    "repelStrength": 24.0,
    "linkStrength": 0.08,
    "linkDistance": 240,
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
