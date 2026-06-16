"""生成 Obsidian Canvas 固定章节分区图。

本脚本只读取 wiki/ 下的 Markdown 笔记，生成 Obsidian 原生 .canvas
文件。布局使用固定坐标和目录顺序，不使用力导向算法，因此不会生成
普通网络图那种毛线球效果。
"""

from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
WIKI_DIR = ROOT / "wiki"
MAIN_CANVAS = ROOT / "数字图像处理知识图谱.canvas"

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

# 总览 Canvas 使用 4 列固定分区。每个分区足够大，保证章节之间有留白。
OVERVIEW_POSITIONS = {
    1: (0, 0),
    2: (760, 0),
    3: (1520, 0),
    4: (2280, 0),
    5: (0, 820),
    6: (760, 820),
    7: (1520, 820),
    8: (2280, 820),
    9: (0, 1640),
    10: (760, 1640),
    11: (1520, 1640),
}


@dataclass(frozen=True)
class Note:
    """一个 wiki 笔记及其章节、层级信息。"""

    path: Path
    rel_path: str
    label: str
    chapter_number: int
    level: str
    order_key: tuple[int, str, str]


def chapter_number_from_path(path: Path) -> int | None:
    """从 wiki/NN_章节名/xxx.md 路径严格识别章节。"""

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
    """扫描 wiki/，只纳入第 1 章到第 11 章的学习笔记。"""

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
    return text[:80]


def file_node(note: Note, *, x: int, y: int, width: int = 260, height: int = 72, color: str | None = None) -> dict:
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


def edge(edge_id: str, source: str, target: str, *, source_side: str = "bottom", target_side: str = "top", color: str | None = None) -> dict:
    item = {"id": edge_id, "fromNode": source, "fromSide": source_side, "toNode": target, "toSide": target_side}
    if color:
        item["color"] = color
    return item


def overview_positions(notes: list[Note], base_x: int, base_y: int) -> dict[str, tuple[int, int]]:
    """总览图中，章节点在上，一级节居中，二级小节在下。"""

    positions: dict[str, tuple[int, int]] = {}
    levels = {
        "chapter": [note for note in notes if note.level == "chapter"],
        "section": [note for note in notes if note.level == "section"],
        "subsection": [note for note in notes if note.level == "subsection"],
        "exercise": [note for note in notes if note.level == "exercise"],
        "note": [note for note in notes if note.level == "note"],
    }
    for note in levels["chapter"]:
        positions[note.rel_path] = (base_x + 210, base_y + 70)
    for index, note in enumerate(levels["section"]):
        positions[note.rel_path] = (base_x + 70 + (index % 2) * 300, base_y + 190 + (index // 2) * 92)
    for index, note in enumerate(levels["subsection"] + levels["note"]):
        positions[note.rel_path] = (base_x + 55 + (index % 2) * 310, base_y + 455 + (index // 2) * 82)
    for note in levels["exercise"]:
        positions[note.rel_path] = (base_x + 435, base_y + 670)
    return positions


def parent_for(note: Note, notes: Iterable[Note]) -> Note | None:
    """按编号找父级节，找不到时回到章节 README。"""

    if note.level == "chapter":
        return None
    if note.level == "section" or note.level == "exercise":
        return next((item for item in notes if item.level == "chapter"), None)
    number = label_number(note.label)
    parent_number = number.rsplit(".", 1)[0] if "." in number else ""
    return next((item for item in notes if label_number(item.label) == parent_number), None) or next(
        (item for item in notes if item.level == "chapter"),
        None,
    )


def build_overview_canvas(notes_by_chapter: dict[int, list[Note]]) -> dict:
    """生成全局固定章节分区 Canvas。"""

    nodes: list[dict] = []
    edges: list[dict] = []
    for number, notes in notes_by_chapter.items():
        base_x, base_y = OVERVIEW_POSITIONS[number]
        group_id = node_id("overview-group", number)
        nodes.append(
            group_node(
                group_id,
                CHAPTER_TITLES[number],
                x=base_x,
                y=base_y,
                width=680,
                height=760,
                color=CHAPTER_COLORS[number],
            )
        )
        positions = overview_positions(notes, base_x, base_y)
        node_ids_by_path: dict[str, str] = {}
        for note in notes:
            x, y = positions[note.rel_path]
            item = file_node(note, x=x, y=y, width=260, height=70, color=CHAPTER_COLORS[number] if note.level == "chapter" else None)
            nodes.append(item)
            node_ids_by_path[note.rel_path] = item["id"]
        for note in notes:
            parent = parent_for(note, notes)
            if not parent:
                continue
            edges.append(
                edge(
                    node_id("overview-edge", number, parent.path.stem, note.path.stem),
                    node_ids_by_path[parent.rel_path],
                    node_ids_by_path[note.rel_path],
                    color=CHAPTER_COLORS[number],
                )
            )
    return {"nodes": nodes, "edges": edges}


def chapter_canvas_positions(notes: list[Note]) -> dict[str, tuple[int, int]]:
    """每章局部图使用分层布局：README、一级节、二级小节、习题分区。"""

    positions: dict[str, tuple[int, int]] = {}
    chapter_notes = [note for note in notes if note.level == "chapter"]
    sections = [note for note in notes if note.level == "section"]
    subsections = [note for note in notes if note.level == "subsection"]
    exercises = [note for note in notes if note.level == "exercise"]
    other_notes = [note for note in notes if note.level == "note"]
    for note in chapter_notes:
        positions[note.rel_path] = (320, 180)
    for index, note in enumerate(sections):
        positions[note.rel_path] = (80 + (index % 3) * 310, 360 + (index // 3) * 95)
    for index, note in enumerate(subsections + other_notes):
        positions[note.rel_path] = (80 + (index % 3) * 310, 700 + (index // 3) * 90)
    for index, note in enumerate(exercises):
        positions[note.rel_path] = (700 + index * 25, 1180)
    return positions


def learning_goal(number: int, title: str) -> str:
    return f"{title}\n\n学习目标：先把本章核心概念、典型方法和公式关系串起来，再进入具体小节复习。Canvas 只做固定结构导航；详细内容请打开对应 wiki 笔记。"


def build_chapter_canvas(number: int, notes: list[Note]) -> dict:
    """生成单章 Canvas，包含学习目标、分区 group 和本章文件节点。"""

    nodes: list[dict] = []
    edges: list[dict] = []
    title = CHAPTER_TITLES[number]
    color = CHAPTER_COLORS[number]
    nodes.append(text_node(node_id("goal", number), learning_goal(number, title), x=40, y=30, width=880, height=120, color=color))
    nodes.extend(
        [
            group_node(node_id("group-basic", number), "基础概念", x=40, y=165, width=940, height=160, color=color),
            group_node(node_id("group-method", number), "方法 / 算法", x=40, y=330, width=940, height=330, color=color),
            group_node(node_id("group-formula", number), "公式与关键关系", x=40, y=670, width=940, height=410, color=color),
            group_node(node_id("group-exercise", number), "习题", x=650, y=1110, width=330, height=180, color=color),
        ]
    )
    positions = chapter_canvas_positions(notes)
    node_ids_by_path: dict[str, str] = {}
    for note in notes:
        x, y = positions[note.rel_path]
        item = file_node(note, x=x, y=y, width=260, height=72, color=color if note.level == "chapter" else None)
        nodes.append(item)
        node_ids_by_path[note.rel_path] = item["id"]
    for note in notes:
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


def write_canvas(path: Path, canvas: dict) -> None:
    path.write_text(json.dumps(canvas, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    notes_by_chapter = scan_notes()
    write_canvas(MAIN_CANVAS, build_overview_canvas(notes_by_chapter))
    print(f"Wrote {MAIN_CANVAS.relative_to(ROOT)}")
    for number, notes in notes_by_chapter.items():
        chapter_dir = WIKI_DIR / next(path.name for path in WIKI_DIR.iterdir() if path.is_dir() and path.name.startswith(f"{number:02d}_"))
        output = chapter_dir / f"{chapter_dir.name}.canvas"
        write_canvas(output, build_chapter_canvas(number, notes))
        print(f"Wrote {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
