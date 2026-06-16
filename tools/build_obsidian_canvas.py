"""生成 Obsidian Canvas 固定课程知识地图。

Canvas 是本知识库的主知识图谱入口。脚本只扫描 wiki/ 下的 Markdown
学习笔记，使用固定坐标生成：

- 总览 Canvas：11 个章节大卡片，清爽展示课程结构；
- 跨章关系 Canvas：只展示章节节点和少量强语义关系；
- 每章 Canvas：展示本章知识点、学习目标和清晰层级。

脚本不使用 force layout，不读取 raw/books，也不依赖外部 API。
"""

from __future__ import annotations

import json
import math
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
WIKI_DIR = ROOT / "wiki"
MAIN_CANVAS = ROOT / "数字图像处理知识图谱.canvas"
CROSS_CHAPTER_CANVAS = ROOT / "数字图像处理跨章关系.canvas"

CHAPTER_TITLES = {
    1: "第 1 章 引言",
    2: "第 2 章 图像增强",
    3: "第 3 章 图像几何变换",
    4: "第 4 章 图像去噪",
    5: "第 5 章 图像锐化",
    6: "第 6 章 图像的分割",
    7: "第 7 章 二值图像处理",
    8: "第 8 章 彩色图像处理",
    9: "第 9 章 图像变换",
    10: "第 10 章 图像压缩编码",
    11: "第 11 章 深度学习与图像处理",
}

# Obsidian Canvas 原生颜色编号。章节颜色保持一致但尽量柔和。
CHAPTER_COLORS = {
    1: "1",
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "1",
    8: "2",
    9: "3",
    10: "4",
    11: "5",
}

STRONG_CROSS_RELATIONS = {
    "PREREQUISITE",
    "COMPARES_WITH",
    "GENERALIZES",
    "IMPROVES_OR_EXTENDS",
    "APPLIES_TO",
}

# 4 列 x 3 行，总览卡片之间保留明显留白。
OVERVIEW_CELL_WIDTH = 1320
OVERVIEW_CELL_HEIGHT = 1420
OVERVIEW_CARD_WIDTH = 1140
OVERVIEW_CARD_HEIGHT = 1240
OVERVIEW_POSITIONS = {
    number: ((number - 1) % 4 * OVERVIEW_CELL_WIDTH, (number - 1) // 4 * OVERVIEW_CELL_HEIGHT)
    for number in CHAPTER_TITLES
}


@dataclass(frozen=True)
class Note:
    """一个 wiki 笔记及其章节、层级和目录顺序。"""

    path: Path
    rel_path: str
    label: str
    chapter_number: int
    level: str
    order_key: tuple[int, str, str]


def chapter_number_from_path(path: Path) -> int | None:
    """从 wiki/NN_章节名/xxx.md 严格识别章节。"""

    try:
        rel = path.relative_to(WIKI_DIR)
    except ValueError:
        return None
    if len(rel.parts) < 2:
        return None
    match = re.match(r"^(\d{2})_", rel.parts[0])
    if not match:
        return None
    number = int(match.group(1))
    return number if number in CHAPTER_TITLES else None


def chapter_number_from_text(value: str | None) -> int | None:
    """从路径、id 或 chapter 字段中识别章节编号。"""

    if not value:
        return None
    patterns = [
        r"(?:^|/)wiki/(\d{2})_",
        r"^(\d{2})_",
        r"(?:^|/)examples/(\d{2})_",
        r"(?:^|/)formula/ch(\d{2})",
        r"(?:^|/)concept/ch(\d{2})",
    ]
    for pattern in patterns:
        match = re.search(pattern, value)
        if match:
            number = int(match.group(1))
            if number in CHAPTER_TITLES:
                return number
    return None


def label_number(label: str) -> str:
    match = re.match(r"^(\d+(?:\.\d+|\.x)*)_", label)
    return match.group(1) if match else ""


def note_level(path: Path) -> str:
    """根据文件名判断 README、一级节、二级小节和习题。"""

    if path.name == "README.md":
        return "chapter"
    number = label_number(path.stem)
    if ".x" in number:
        return "exercise"
    dots = number.count(".")
    if dots == 1:
        return "section"
    if dots >= 2:
        return "subsection"
    return "note"


def scan_notes() -> dict[int, list[Note]]:
    """扫描第 1 章到第 11 章学习笔记，排除导航、术语表和维护文件。"""

    notes_by_chapter: dict[int, list[Note]] = {number: [] for number in CHAPTER_TITLES}
    for path in sorted(WIKI_DIR.rglob("*.md")):
        chapter_number = chapter_number_from_path(path)
        if not chapter_number:
            continue
        rel_path = path.relative_to(ROOT).as_posix()
        level = note_level(path)
        rank = {"chapter": 0, "section": 1, "subsection": 2, "exercise": 3, "note": 4}[level]
        note = Note(
            path=path,
            rel_path=rel_path,
            label=path.parent.name if path.name == "README.md" else path.stem,
            chapter_number=chapter_number,
            level=level,
            order_key=(rank, label_number(path.stem), path.stem),
        )
        notes_by_chapter[chapter_number].append(note)
    for number in notes_by_chapter:
        notes_by_chapter[number].sort(key=lambda note: note.order_key)
    return notes_by_chapter


def node_id(*parts: object) -> str:
    """生成稳定 Canvas 节点 id。"""

    text = "-".join(str(part) for part in parts)
    text = re.sub(r"[^A-Za-z0-9_-]+", "-", text).strip("-")
    return text[:96]


def file_node(
    note: Note,
    *,
    x: int,
    y: int,
    width: int = 420,
    height: int = 82,
    color: str | None = None,
) -> dict:
    node = {
        "id": node_id("note", note.chapter_number, note.path.stem),
        "type": "file",
        "file": note.rel_path,
        "x": x,
        "y": y,
        "width": width,
        "height": height,
    }
    if color:
        node["color"] = color
    return node


def group_node(group_id: str, label: str, *, x: int, y: int, width: int, height: int, color: str | None = None) -> dict:
    node = {"id": group_id, "type": "group", "label": label, "x": x, "y": y, "width": width, "height": height}
    if color:
        node["color"] = color
    return node


def text_node(text_id: str, text: str, *, x: int, y: int, width: int, height: int, color: str | None = None) -> dict:
    node = {"id": text_id, "type": "text", "text": text, "x": x, "y": y, "width": width, "height": height}
    if color:
        node["color"] = color
    return node


def edge(
    edge_id: str,
    source: str,
    target: str,
    *,
    source_side: str = "bottom",
    target_side: str = "top",
    color: str | None = None,
) -> dict:
    item = {"id": edge_id, "fromNode": source, "fromSide": source_side, "toNode": target, "toSide": target_side}
    if color:
        item["color"] = color
    return item


def parent_for(note: Note, notes: Iterable[Note]) -> Note | None:
    """按编号找父级节，找不到时回到章节 README。"""

    if note.level == "chapter":
        return None
    if note.level in {"section", "exercise"}:
        return next((item for item in notes if item.level == "chapter"), None)
    number = label_number(note.label)
    parent_number = number.rsplit(".", 1)[0] if "." in number else ""
    return next((item for item in notes if label_number(item.label) == parent_number), None) or next(
        (item for item in notes if item.level == "chapter"),
        None,
    )


def overview_positions(notes: list[Note], base_x: int, base_y: int) -> dict[str, tuple[int, int]]:
    """总览图：标题醒目，README 在上，节和小节按目录顺序纵向排列。"""

    positions: dict[str, tuple[int, int]] = {}
    sections = [note for note in notes if note.level == "section"]
    subsections = [note for note in notes if note.level in {"subsection", "note"}]
    exercises = [note for note in notes if note.level == "exercise"]
    for note in [note for note in notes if note.level == "chapter"]:
        positions[note.rel_path] = (base_x + 350, base_y + 145)
    for index, note in enumerate(sections):
        positions[note.rel_path] = (base_x + 70, base_y + 285 + index * 88)
    for index, note in enumerate(subsections):
        positions[note.rel_path] = (base_x + 575, base_y + 285 + index * 82)
    for note in exercises:
        positions[note.rel_path] = (base_x + 70, base_y + 1110)
    return positions


def build_overview_canvas(notes_by_chapter: dict[int, list[Note]]) -> dict:
    """生成主入口总览 Canvas：11 个大卡片，只保留章到一级节主干线。"""

    nodes: list[dict] = []
    edges: list[dict] = []
    for number, notes in notes_by_chapter.items():
        base_x, base_y = OVERVIEW_POSITIONS[number]
        color = CHAPTER_COLORS[number]
        group_id = node_id("overview-group", number)
        nodes.append(
            group_node(
                group_id,
                CHAPTER_TITLES[number],
                x=base_x,
                y=base_y,
                width=OVERVIEW_CARD_WIDTH,
                height=OVERVIEW_CARD_HEIGHT,
                color=color,
            )
        )
        nodes.append(
            text_node(
                node_id("overview-title", number),
                f"# {CHAPTER_TITLES[number]}\n固定课程分区",
                x=base_x + 45,
                y=base_y + 35,
                width=1040,
                height=86,
                color=color,
            )
        )
        positions = overview_positions(notes, base_x, base_y)
        node_ids_by_path: dict[str, str] = {}
        for note in notes:
            x, y = positions[note.rel_path]
            width = 440 if note.level in {"section", "subsection", "note"} else 380
            height = 82 if note.level != "chapter" else 90
            item = file_node(note, x=x, y=y, width=width, height=height, color=color if note.level == "chapter" else None)
            nodes.append(item)
            node_ids_by_path[note.rel_path] = item["id"]
        chapter_note = next((note for note in notes if note.level == "chapter"), None)
        if chapter_note:
            for note in [item for item in notes if item.level == "section"]:
                edges.append(
                    edge(
                        node_id("overview-main-edge", number, note.path.stem),
                        node_ids_by_path[chapter_note.rel_path],
                        node_ids_by_path[note.rel_path],
                        color=color,
                    )
                )
    return {"nodes": nodes, "edges": edges}


def chapter_canvas_positions(notes: list[Note]) -> dict[str, tuple[int, int]]:
    """每章局部图：宽松分层，右侧预留代码/补充区，底部放习题。"""

    positions: dict[str, tuple[int, int]] = {}
    sections = [note for note in notes if note.level == "section"]
    subsections = [note for note in notes if note.level in {"subsection", "note"}]
    exercises = [note for note in notes if note.level == "exercise"]
    for note in [note for note in notes if note.level == "chapter"]:
        positions[note.rel_path] = (430, 210)
    for index, note in enumerate(sections):
        positions[note.rel_path] = (80, 430 + index * 112)
    for index, note in enumerate(subsections):
        positions[note.rel_path] = (585, 430 + index * 96)
    exercise_y = max(1320, 430 + len(subsections) * 96 + 120)
    for index, note in enumerate(exercises):
        positions[note.rel_path] = (80 + index * 30, exercise_y)
    return positions


def learning_goal(number: int, title: str) -> str:
    return (
        f"# {title}\n\n"
        "学习目标：先把本章核心概念、典型方法、公式关系和代码入口串起来，"
        "再进入具体小节复习。Canvas 只做固定结构导航；详细内容请打开对应 wiki 笔记。"
    )


def build_chapter_canvas(number: int, notes: list[Note]) -> dict:
    """生成单章 Canvas，线条只保留主要父子层级。"""

    nodes: list[dict] = []
    edges: list[dict] = []
    title = CHAPTER_TITLES[number]
    color = CHAPTER_COLORS[number]
    positions = chapter_canvas_positions(notes)
    exercise_y_values = [y for note in notes if note.level == "exercise" for _, y in [positions[note.rel_path]]]
    exercise_group_y = (min(exercise_y_values) - 50) if exercise_y_values else 1270
    detail_height = max(840, exercise_group_y - 410 - 30)
    nodes.append(text_node(node_id("goal", number), learning_goal(number, title), x=40, y=30, width=1180, height=145, color=color))
    nodes.extend(
        [
            group_node(node_id("group-basic", number), "基础概念", x=40, y=185, width=1220, height=210, color=color),
            group_node(node_id("group-method", number), "方法 / 算法", x=40, y=410, width=500, height=840, color=color),
            group_node(node_id("group-detail", number), "公式 / 小节 / 补充", x=555, y=410, width=705, height=detail_height, color=color),
            group_node(node_id("group-exercise", number), "习题", x=40, y=exercise_group_y, width=500, height=190, color=color),
        ]
    )
    node_ids_by_path: dict[str, str] = {}
    for note in notes:
        x, y = positions[note.rel_path]
        width = 430 if note.level != "chapter" else 420
        height = 86 if note.level != "chapter" else 95
        item = file_node(note, x=x, y=y, width=width, height=height, color=color if note.level == "chapter" else None)
        nodes.append(item)
        node_ids_by_path[note.rel_path] = item["id"]
    for note in notes:
        if note.level not in {"section", "subsection", "exercise"}:
            continue
        parent = parent_for(note, notes)
        if not parent:
            continue
        edges.append(
            edge(
                node_id("chapter-edge", number, parent.path.stem, note.path.stem),
                node_ids_by_path[parent.rel_path],
                node_ids_by_path[note.rel_path],
                color=color,
            )
        )
    return {"nodes": nodes, "edges": edges}


def build_cross_chapter_canvas(notes_by_chapter: dict[int, list[Note]]) -> dict:
    """生成跨章关系 Canvas：只展示章节节点和聚合后的强语义关系。"""

    nodes: list[dict] = []
    edges: list[dict] = []
    radius = 900
    center_x, center_y = 1250, 1050
    chapter_node_ids: dict[int, str] = {}
    for index, number in enumerate(CHAPTER_TITLES):
        angle = -math.pi / 2 + 2 * math.pi * index / len(CHAPTER_TITLES)
        x = round(center_x + math.cos(angle) * radius)
        y = round(center_y + math.sin(angle) * radius)
        chapter_note = next((note for note in notes_by_chapter[number] if note.level == "chapter"), None)
        if not chapter_note:
            continue
        item = file_node(chapter_note, x=x, y=y, width=430, height=96, color=CHAPTER_COLORS[number])
        nodes.append(item)
        nodes.append(
            text_node(
                node_id("cross-title", number),
                CHAPTER_TITLES[number],
                x=x,
                y=y - 96,
                width=430,
                height=70,
                color=CHAPTER_COLORS[number],
            )
        )
        chapter_node_ids[number] = item["id"]

    graph_path = ROOT / "graph" / "knowledge_graph.json"
    relation_counts: Counter[tuple[int, int, str]] = Counter()
    if graph_path.exists():
        graph = json.loads(graph_path.read_text(encoding="utf-8"))
        node_chapters = {
            node["id"]: chapter_number_from_text(node.get("path")) or chapter_number_from_text(node.get("chapter")) or chapter_number_from_text(node.get("id"))
            for node in graph.get("nodes", [])
        }
        for relation in graph.get("edges", []):
            relation_type = relation.get("type")
            if relation_type not in STRONG_CROSS_RELATIONS:
                continue
            source_chapter = node_chapters.get(relation.get("source"))
            target_chapter = node_chapters.get(relation.get("target"))
            if source_chapter and target_chapter and source_chapter != target_chapter:
                relation_counts[(source_chapter, target_chapter, relation_type)] += 1

    for index, ((source, target, relation_type), count) in enumerate(sorted(relation_counts.items())):
        if source not in chapter_node_ids or target not in chapter_node_ids:
            continue
        edges.append(
            edge(
                node_id("cross-edge", index, source, target, relation_type),
                chapter_node_ids[source],
                chapter_node_ids[target],
                color="6",
            )
        )
        if index >= 28:
            break
    nodes.append(
        text_node(
            "cross-note",
            "# 跨章关系说明\n\n这里只聚合展示强语义关系。具体小节关系请回到总览 Canvas、章节 Canvas 或 Graph View 查看。",
            x=center_x - 380,
            y=center_y - 120,
            width=760,
            height=220,
            color="6",
        )
    )
    return {"nodes": nodes, "edges": edges}


def write_canvas(path: Path, canvas: dict) -> None:
    path.write_text(json.dumps(canvas, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    notes_by_chapter = scan_notes()
    write_canvas(MAIN_CANVAS, build_overview_canvas(notes_by_chapter))
    print(f"Wrote {MAIN_CANVAS.relative_to(ROOT)}")
    write_canvas(CROSS_CHAPTER_CANVAS, build_cross_chapter_canvas(notes_by_chapter))
    print(f"Wrote {CROSS_CHAPTER_CANVAS.relative_to(ROOT)}")
    for number, notes in notes_by_chapter.items():
        chapter_dir = WIKI_DIR / next(path.name for path in WIKI_DIR.iterdir() if path.is_dir() and path.name.startswith(f"{number:02d}_"))
        output = chapter_dir / f"{chapter_dir.name}.canvas"
        write_canvas(output, build_chapter_canvas(number, notes))
        print(f"Wrote {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
