"""生成本地 Obsidian Graph View 配置。

.obsidian/ 目录是本地 UI 状态，项目已经通过 .gitignore 忽略。本脚本用于
可重复地恢复干净的学习图谱过滤条件：只看 wiki/ 学习笔记，排除维护文件，
并按章节设置颜色分组。
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

# Obsidian 的搜索语法会在 Graph View 中过滤节点。这里尽量把维护文件和
# 非学习内容排除掉，避免 README、脚本、生成图等混进主学习图谱。
GRAPH_SEARCH = (
    "path:wiki "
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
    "textFadeMultiplier": -1.0,
    "nodeSizeMultiplier": 0.75,
    "lineSizeMultiplier": 0.25,
    "collapse-forces": False,
    "centerStrength": 0.15,
    "repelStrength": 22.0,
    "linkStrength": 0.12,
    "linkDistance": 220,
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
