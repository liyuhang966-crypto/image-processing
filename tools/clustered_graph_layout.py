"""Deterministic chapter-island graph layouts.

The public graph is generated from wiki notes, but the study view should not be
a free force-directed hairball. This module precomputes fixed node coordinates
so each chapter remains a separate visual island.
"""

from __future__ import annotations

import html
import json
import math
import re
from collections import Counter
from pathlib import Path
from typing import Any


ROOT_NODE_ID = "root/digital_image_processing_knowledge_base"
MAIN_CHAPTER_COUNT = 11
CANVAS = {"width": 2800, "height": 2200, "centerX": 1400, "centerY": 1100}

PALETTE = [
    "#7dd3fc",
    "#fb923c",
    "#86efac",
    "#f0abfc",
    "#c4b5fd",
    "#fde047",
    "#67e8f9",
    "#fb7185",
    "#bef264",
    "#93c5fd",
    "#fbbf24",
]

CHAPTER_ANCHORS = {
    1: (-0.70, -0.72),
    2: (0.46, 0.88),
    3: (-1.00, -0.18),
    4: (1.00, -0.10),
    5: (-0.58, 0.82),
    6: (0.28, -1.00),
    7: (-0.28, -1.00),
    8: (0.86, 0.46),
    9: (-0.92, 0.38),
    10: (-0.05, 1.00),
    11: (0.78, -0.62),
}

SEMANTIC_RELATIONS = {
    "PREREQUISITE",
    "COMPARES_WITH",
    "GENERALIZES",
    "IMPLEMENTED_BY",
    "USES_FORMULA",
    "IMPROVES_OR_EXTENDS",
    "APPLIES_TO",
}
STRONG_CROSS_RELATIONS = {"PREREQUISITE", "COMPARES_WITH", "IMPROVES_OR_EXTENDS", "APPLIES_TO"}
CODE_RELATIONS = {"IMPLEMENTED_BY", "USES_FORMULA"}


def chapter_number(value: str | None) -> int | None:
    if not value:
        return None
    match = re.search(r"(?:^|/)(\d{2})_", value) or re.match(r"^(\d+)_", value)
    return int(match.group(1)) if match else None


def label_number(label: str) -> str:
    match = re.match(r"^(\d+(?:\.\d+|\.x)*)_", label)
    return match.group(1) if match else ""


def node_level(node: dict[str, Any]) -> str:
    if node["id"] == ROOT_NODE_ID:
        return "root"
    if node.get("type") == "chapter" or node.get("path", "").endswith("/README.md"):
        return "chapter"
    number = label_number(node.get("label", ""))
    if ".x" in number:
        return "exercise"
    dot_count = number.count(".")
    if dot_count == 1:
        return "section"
    if dot_count >= 2:
        return "subsection"
    node_type = node.get("type", "")
    if node_type in {"concept", "formula", "code"}:
        return node_type
    return "note"


def importance_for_level(level: str) -> int:
    return {
        "root": 5,
        "chapter": 4,
        "section": 3,
        "subsection": 2,
        "exercise": 1,
        "concept": 1,
        "formula": 1,
        "code": 1,
    }.get(level, 1)


def display_label(node: dict[str, Any], level: str) -> str:
    if node["id"] == ROOT_NODE_ID:
        return "数字图像处理知识库"
    label = node.get("label", node["id"])
    if level == "chapter":
        num = chapter_number(node.get("id")) or chapter_number(node.get("chapter"))
        return f"第 {num} 章" if num else label
    number = label_number(label)
    return number or label[:14]


def main_chapter_key(node: dict[str, Any]) -> int | None:
    number = chapter_number(node.get("id")) or chapter_number(node.get("path")) or chapter_number(node.get("chapter"))
    if number and 1 <= number <= MAIN_CHAPTER_COUNT:
        return number
    return None


def sorted_chapter_nodes(nodes: list[dict[str, Any]], number: int) -> list[dict[str, Any]]:
    selected = [node for node in nodes if main_chapter_key(node) == number]

    def key(node: dict[str, Any]) -> tuple[int, str, str]:
        level = node_level(node)
        rank = {"chapter": 0, "section": 1, "subsection": 2, "exercise": 3}.get(level, 4)
        return rank, label_number(node.get("label", "")), node.get("id", "")

    return sorted(selected, key=key)


def infer_non_wiki_chapters(nodes: list[dict[str, Any]], edges: list[dict[str, Any]]) -> dict[str, int | None]:
    node_chapters = {node["id"]: main_chapter_key(node) for node in nodes}
    inferred: dict[str, int | None] = {}
    for node in nodes:
        if node_chapters[node["id"]]:
            inferred[node["id"]] = node_chapters[node["id"]]
            continue
        counts: Counter[int] = Counter()
        for edge in edges:
            other_id = None
            if edge["source"] == node["id"]:
                other_id = edge["target"]
            elif edge["target"] == node["id"]:
                other_id = edge["source"]
            if other_id and node_chapters.get(other_id):
                counts[node_chapters[other_id]] += 1
        inferred[node["id"]] = counts.most_common(1)[0][0] if counts else None
    return inferred


def cluster_center(number: int) -> tuple[float, float]:
    ax, ay = CHAPTER_ANCHORS[number]
    return (
        CANVAS["centerX"] + ax * 1050,
        CANVAS["centerY"] + ay * 820,
    )


def ring_position(center: tuple[float, float], radius: float, index: int, count: int, offset: float) -> tuple[float, float]:
    if count <= 1:
        angle = offset
    else:
        angle = offset + (2 * math.pi * index / count)
    return center[0] + math.cos(angle) * radius, center[1] + math.sin(angle) * radius


def enriched_node(node: dict[str, Any], *, x: float, y: float, chapter_num: int | None, color: str) -> dict[str, Any]:
    level = node_level(node)
    return {
        **node,
        "x": round(x, 2),
        "y": round(y, 2),
        "fixed": True,
        "fixedPosition": True,
        "chapterNumber": chapter_num,
        "chapter": node.get("chapter") or (f"{chapter_num:02d}" if chapter_num else "global"),
        "level": level,
        "importance": importance_for_level(level),
        "displayLabel": display_label(node, level),
        "color": color,
    }


def relation_class(edge: dict[str, Any]) -> str:
    edge_type = edge["type"]
    if edge_type in CODE_RELATIONS:
        base = "code"
    elif edge_type in SEMANTIC_RELATIONS:
        base = "semantic"
    elif edge_type == "CONTAINS" or edge_type == "CHAPTER_CLUSTER":
        base = "contains"
    elif edge_type == "LINKS_TO":
        base = "link"
    else:
        base = "other"
    return f"cross-{base}" if edge.get("isCrossChapter") else base


def build_clustered_layout(graph: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    source_nodes = [dict(node) for node in graph["nodes"]]
    source_edges = [dict(edge) for edge in graph["edges"]]
    inferred = infer_non_wiki_chapters(source_nodes, source_edges)
    node_by_id = {node["id"]: node for node in source_nodes}
    layout_nodes: list[dict[str, Any]] = []
    chapters: list[dict[str, Any]] = []

    root = {
        "id": ROOT_NODE_ID,
        "label": "数字图像处理知识库",
        "type": "root",
        "chapter": "global",
        "path": "",
    }
    layout_nodes.append(
        enriched_node(
            root,
            x=CANVAS["centerX"],
            y=CANVAS["centerY"],
            chapter_num=None,
            color="#f8fafc",
        )
    )

    for number in range(1, MAIN_CHAPTER_COUNT + 1):
        center = cluster_center(number)
        color = PALETTE[number - 1]
        chapter_nodes = sorted_chapter_nodes(source_nodes, number)
        if not chapter_nodes:
            continue
        chapter_center = next((node for node in chapter_nodes if node_level(node) == "chapter"), chapter_nodes[0])
        chapters.append(
            {
                "number": number,
                "id": chapter_center["id"],
                "label": chapter_center.get("label", f"第 {number} 章"),
                "x": round(center[0], 2),
                "y": round(center[1], 2),
                "color": color,
            }
        )
        by_level = {
            "chapter": [node for node in chapter_nodes if node_level(node) == "chapter"],
            "section": [node for node in chapter_nodes if node_level(node) == "section"],
            "subsection": [node for node in chapter_nodes if node_level(node) == "subsection"],
            "exercise": [node for node in chapter_nodes if node_level(node) == "exercise"],
            "note": [node for node in chapter_nodes if node_level(node) not in {"chapter", "section", "subsection", "exercise"}],
        }
        used = set()
        for node in by_level["chapter"]:
            layout_nodes.append(enriched_node(node, x=center[0], y=center[1], chapter_num=number, color=color))
            used.add(node["id"])
        rings = [
            ("section", 126, -math.pi / 2),
            ("subsection", 194, -math.pi / 2 + 0.18),
            ("exercise", 228, math.pi / 2),
            ("note", 252, math.pi / 2 + 0.22),
        ]
        for level, radius, offset in rings:
            nodes = by_level[level]
            for index, node in enumerate(nodes):
                x, y = ring_position(center, radius, index, max(1, len(nodes)), offset)
                layout_nodes.append(enriched_node(node, x=x, y=y, chapter_num=number, color=color))
                used.add(node["id"])

    for index, node in enumerate(source_nodes):
        if node["id"] in {item["id"] for item in layout_nodes}:
            continue
        number = inferred.get(node["id"])
        if number:
            center = cluster_center(number)
            color = PALETTE[number - 1]
            x, y = ring_position(center, 282, index, max(12, len(source_nodes)), -math.pi / 3)
        else:
            color = "#94a3b8"
            x, y = ring_position((CANVAS["centerX"], CANVAS["centerY"]), 92, index, max(12, len(source_nodes)), -math.pi / 2)
        layout_nodes.append(enriched_node(node, x=x, y=y, chapter_num=number, color=color))

    layout_by_id = {node["id"]: node for node in layout_nodes}
    layout_edges: list[dict[str, Any]] = []
    for chapter in chapters:
        layout_edges.append(
            {
                "source": ROOT_NODE_ID,
                "target": chapter["id"],
                "type": "CHAPTER_CLUSTER",
                "sourceChapter": None,
                "targetChapter": chapter["number"],
                "isCrossChapter": True,
                "visibleByDefault": True,
                "class": "backbone",
            }
        )
    for edge in source_edges:
        source = layout_by_id.get(edge["source"])
        target = layout_by_id.get(edge["target"])
        if not source or not target:
            continue
        source_chapter = source.get("chapterNumber")
        target_chapter = target.get("chapterNumber")
        cross = bool(source_chapter and target_chapter and source_chapter != target_chapter)
        enriched = {
            **edge,
            "sourceChapter": source_chapter,
            "targetChapter": target_chapter,
            "isCrossChapter": cross,
            "visibleByDefault": (not cross and edge["type"] != "LINKS_TO") or (cross and edge["type"] in STRONG_CROSS_RELATIONS),
        }
        enriched["class"] = relation_class(enriched)
        layout_edges.append(enriched)

    return {
        "meta": {
            "layout": "deterministic chapter islands",
            "canvas": CANVAS,
            "physics": False,
            "description": "Nodes have fixed x/y coordinates; chapters are separated into visual islands.",
        },
        "chapters": chapters,
        "nodes": layout_nodes,
        "edges": layout_edges,
    }


def json_script(data: dict[str, Any]) -> str:
    return html.escape(json.dumps(data, ensure_ascii=False))


def controls_html() -> str:
    return """
  <div class="controls">
    <label>章节
      <select id="chapterFilter"><option value="all">全部章节</option></select>
    </label>
    <label>关系
      <select id="relationMode">
        <option value="hide_links">隐藏普通 LINKS_TO</option>
        <option value="all">全部关系</option>
        <option value="contains">只看章节包含关系</option>
        <option value="semantic">只看语义关系</option>
        <option value="code">只看代码实现关系</option>
        <option value="backbone">只看主干关系</option>
      </select>
    </label>
    <label>标签
      <select id="labelMode">
        <option value="chapters">只显示章节标签</option>
        <option value="current">显示当前章节标签</option>
        <option value="all">显示全部标签</option>
        <option value="none">隐藏全部小节标签</option>
      </select>
    </label>
    <label><input type="checkbox" id="showCross"> 显示跨章边</label>
    <label><input type="checkbox" id="showLinks"> 显示普通 LINKS_TO</label>
    <button type="button" id="resetView">重置视图</button>
  </div>
"""


def write_clustered_html(layout: dict[str, Any], output_path: Path, *, title: str, controls: bool = True) -> None:
    canvas = layout.get("meta", {}).get("canvas", CANVAS)
    view_box = f"0 0 {canvas.get('width', 2800)} {canvas.get('height', 2200)}"
    template = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>__TITLE__</title>
  <style>
    :root { --bg:#15171b; --panel:#20232a; --ink:#f3f4f6; --muted:#aab2c0; --line:#8c94a3; }
    * { box-sizing:border-box; }
    body { margin:0; background:var(--bg); color:var(--ink); font-family:system-ui, "Microsoft YaHei", sans-serif; }
    main { padding:16px 18px 22px; }
    h1 { margin:0 0 6px; font-size:22px; }
    .summary { margin:0 0 12px; color:var(--muted); font-size:13px; line-height:1.55; }
    .controls { display:flex; flex-wrap:wrap; gap:10px; align-items:center; margin:10px 0 12px; }
    label, button { color:#dde3ee; font-size:12px; }
    select, button { margin-left:6px; border:1px solid #3b404a; border-radius:6px; background:var(--panel); color:#f8fafc; padding:5px 8px; }
    input { vertical-align:middle; }
    .wrap { display:grid; grid-template-columns:minmax(0, 1fr) 300px; gap:12px; }
    .stage { overflow:auto; border:1px solid #30343b; border-radius:8px; background:#101114; min-height:760px; }
    svg { display:block; min-width:1200px; height:min(82vh, 900px); min-height:760px; }
    aside { border:1px solid #30343b; border-radius:8px; background:#1b1e24; padding:12px; min-height:180px; color:#d8dee9; font-size:13px; }
    .legend { display:flex; flex-wrap:wrap; gap:10px; margin:0 0 10px; color:#cbd5e1; font-size:12px; }
    .swatch { width:10px; height:10px; border-radius:50%; display:inline-block; margin-right:5px; }
    .edge { fill:none; stroke:var(--line); stroke-width:1.0; stroke-opacity:.30; }
    .edge.backbone { stroke-width:1.5; stroke-opacity:.48; }
    .edge.contains { stroke-opacity:.30; }
    .edge.link { stroke-opacity:.22; }
    .edge.semantic { stroke-dasharray:5 4; stroke-width:1.35; stroke-opacity:.42; }
    .edge.code { stroke-dasharray:2 4; stroke-width:1.2; stroke-opacity:.42; }
    .edge.cross-link, .edge.cross-semantic { stroke-opacity:.16; stroke-width:.85; }
    .node { stroke:rgba(255,255,255,.72); stroke-width:1; cursor:default; }
    .node.root { fill:#f8fafc; stroke:#f8fafc; }
    .node.chapter { stroke-width:1.8; }
    .node.external, .node.concept, .node.formula, .node.code { stroke-dasharray:2 2; }
    .halo { fill:none; stroke-width:1.4; stroke-opacity:.16; }
    text { font-family:system-ui, "Microsoft YaHei", sans-serif; }
    .label { fill:#e5e7eb; font-size:11px; text-anchor:middle; paint-order:stroke; stroke:#101114; stroke-width:3px; pointer-events:none; }
    .label.chapter { font-size:15px; font-weight:700; opacity:1; }
    .label.root { font-size:14px; font-weight:700; }
    .label.hidden { opacity:0; }
    .dim { opacity:.12; }
    .highlight { opacity:1 !important; stroke-width:2.4; }
    .edge.highlight { stroke-opacity:.88 !important; stroke-width:2; }
    .hidden-node, .hidden-edge { display:none; }
    code { color:#93c5fd; word-break:break-all; }
    @media (max-width:980px) { .wrap { grid-template-columns:1fr; } aside { min-height:120px; } }
  </style>
</head>
<body>
<main>
  <h1>__TITLE__</h1>
  <p class="summary">章节岛屿式布局：第 1 章到第 11 章使用固定坐标分区，章内小节围绕本章中心聚集；普通跨章 LINKS_TO 默认隐藏，只保留少量主干语义线。</p>
  __CONTROLS__
  <div class="legend" id="legend"></div>
  <div class="wrap">
    <div class="stage"><svg id="graph" viewBox="__VIEWBOX__" aria-label="__TITLE__"></svg></div>
    <aside id="details">悬停节点查看完整标题、章节、类型和路径。</aside>
  </div>
</main>
<script type="application/json" id="graph-data">__PAYLOAD__</script>
<script>
const data = JSON.parse(document.getElementById("graph-data").textContent);
const svg = document.getElementById("graph");
const details = document.getElementById("details");
const legend = document.getElementById("legend");
const chapterFilter = document.getElementById("chapterFilter");
const relationMode = document.getElementById("relationMode");
const labelMode = document.getElementById("labelMode");
const showCross = document.getElementById("showCross");
const showLinks = document.getElementById("showLinks");
const resetView = document.getElementById("resetView");
const nodesById = new Map(data.nodes.map((node) => [node.id, node]));
const neighbors = new Map();
const semantic = new Set(["PREREQUISITE", "COMPARES_WITH", "GENERALIZES", "IMPLEMENTED_BY", "USES_FORMULA", "IMPROVES_OR_EXTENDS", "APPLIES_TO"]);
const strong = new Set(["PREREQUISITE", "COMPARES_WITH", "IMPROVES_OR_EXTENDS", "APPLIES_TO"]);
const codeRels = new Set(["IMPLEMENTED_BY", "USES_FORMULA"]);

for (const edge of data.edges) {
  if (!neighbors.has(edge.source)) neighbors.set(edge.source, new Set());
  if (!neighbors.has(edge.target)) neighbors.set(edge.target, new Set());
  neighbors.get(edge.source).add(edge.target);
  neighbors.get(edge.target).add(edge.source);
}

for (const chapter of data.chapters || []) {
  const item = document.createElement("span");
  const swatch = document.createElement("i");
  swatch.className = "swatch";
  swatch.style.background = chapter.color;
  item.append(swatch, document.createTextNode(chapter.label));
  legend.appendChild(item);
  if (chapterFilter) {
    const option = document.createElement("option");
    option.value = String(chapter.number);
    option.textContent = `第 ${chapter.number} 章`;
    chapterFilter.appendChild(option);
  }
}

function el(name, attrs = {}) {
  const node = document.createElementNS("http://www.w3.org/2000/svg", name);
  for (const [key, value] of Object.entries(attrs)) {
    if (value !== undefined && value !== null) node.setAttribute(key, value);
  }
  return node;
}

function nodeRadius(node) {
  if (node.level === "root") return 18;
  if (node.level === "chapter") return 20;
  if (node.level === "section") return 11;
  if (node.level === "subsection") return 8;
  if (node.level === "exercise") return 7;
  return 6;
}

function nodeVisible(node) {
  const selected = chapterFilter ? chapterFilter.value : "all";
  if (selected === "all") return true;
  if (node.level === "root") return true;
  return String(node.chapterNumber) === selected;
}

function edgeVisible(edge) {
  const selected = chapterFilter ? chapterFilter.value : "all";
  const mode = relationMode ? relationMode.value : "hide_links";
  const source = nodesById.get(edge.source);
  const target = nodesById.get(edge.target);
  if (!source || !target || !nodeVisible(source) || !nodeVisible(target)) return false;
  if (mode === "backbone") return edge.type === "CHAPTER_CLUSTER" || (edge.isCrossChapter && strong.has(edge.type));
  if (mode === "contains") return edge.type === "CONTAINS" || edge.type === "CHAPTER_CLUSTER";
  if (mode === "semantic") return semantic.has(edge.type) || edge.type === "CHAPTER_CLUSTER";
  if (mode === "code") return codeRels.has(edge.type);
  if (edge.type === "LINKS_TO") {
    if (!showLinks || !showLinks.checked) return false;
    if (edge.isCrossChapter && (!showCross || !showCross.checked)) return false;
    return true;
  }
  if (edge.isCrossChapter && (!showCross || !showCross.checked) && !strong.has(edge.type)) return false;
  return true;
}

function labelVisible(node) {
  const mode = labelMode ? labelMode.value : "chapters";
  if (node.level === "root" || node.level === "chapter") return mode !== "none";
  if (mode === "all") return true;
  if (mode === "current" && chapterFilter && chapterFilter.value !== "all") return String(node.chapterNumber) === chapterFilter.value;
  return false;
}

function render() {
  svg.replaceChildren();
  const edgeLayer = el("g");
  const haloLayer = el("g");
  const nodeLayer = el("g");
  const labelLayer = el("g");
  svg.append(edgeLayer, haloLayer, nodeLayer, labelLayer);

  for (const chapter of data.chapters || []) {
    const visible = chapterFilter ? (chapterFilter.value === "all" || chapterFilter.value === String(chapter.number)) : true;
    haloLayer.append(el("circle", { class: `halo ${visible ? "" : "hidden-node"}`, cx: chapter.x, cy: chapter.y, r: 265, stroke: chapter.color }));
  }

  for (const edge of data.edges) {
    const source = nodesById.get(edge.source);
    const target = nodesById.get(edge.target);
    if (!source || !target) continue;
    const path = el("path", {
      class: `edge ${edge.class || "edge"} ${edgeVisible(edge) ? "" : "hidden-edge"}`,
      d: `M ${source.x} ${source.y} Q ${(source.x + target.x) / 2} ${(source.y + target.y) / 2 - (edge.isCrossChapter ? 70 : 0)} ${target.x} ${target.y}`,
      stroke: edge.isCrossChapter ? undefined : source.color,
      "data-source": edge.source,
      "data-target": edge.target,
    });
    path.append(el("title"));
    path.firstChild.textContent = `${source.label} -> ${target.label} (${edge.type})`;
    edgeLayer.append(path);
  }

  for (const node of data.nodes) {
    const circle = el("circle", {
      class: `node ${node.level} ${nodeVisible(node) ? "" : "hidden-node"}`,
      cx: node.x,
      cy: node.y,
      r: nodeRadius(node),
      fill: node.color,
      "data-id": node.id,
    });
    circle.addEventListener("mouseenter", () => highlight(node.id));
    circle.addEventListener("mouseleave", clearHighlight);
    nodeLayer.append(circle);

    const label = el("text", {
      class: `label ${node.level} ${labelVisible(node) ? "" : "hidden"} ${nodeVisible(node) ? "" : "hidden-node"}`,
      x: node.x,
      y: node.y + nodeRadius(node) + 16,
      "data-label-for": node.id,
    });
    label.textContent = node.displayLabel || node.label;
    labelLayer.append(label);
  }
}

function highlight(id) {
  const node = nodesById.get(id);
  const near = neighbors.get(id) || new Set();
  for (const circle of svg.querySelectorAll(".node")) {
    const cid = circle.getAttribute("data-id");
    circle.classList.toggle("dim", cid !== id && !near.has(cid));
    circle.classList.toggle("highlight", cid === id);
  }
  for (const edge of svg.querySelectorAll(".edge")) {
    const hit = edge.getAttribute("data-source") === id || edge.getAttribute("data-target") === id;
    edge.classList.toggle("dim", !hit);
    edge.classList.toggle("highlight", hit);
  }
  details.innerHTML = `<strong>${node.label}</strong><p>章节：${node.chapter || "总览"}</p><p>类型：${node.type} / ${node.level}</p><p>路径：<code>${node.path || node.id}</code></p>`;
}

function clearHighlight() {
  for (const item of svg.querySelectorAll(".dim,.highlight")) item.classList.remove("dim", "highlight");
  details.textContent = "悬停节点查看完整标题、章节、类型和路径。";
}

for (const control of [chapterFilter, relationMode, labelMode, showCross, showLinks]) {
  if (control) control.addEventListener("change", render);
}
if (resetView) resetView.addEventListener("click", () => svg.setAttribute("viewBox", "__VIEWBOX__"));
render();
</script>
</body>
</html>
"""
    html_text = (
        template.replace("__TITLE__", html.escape(title))
        .replace("__CONTROLS__", controls_html() if controls else "")
        .replace("__VIEWBOX__", view_box)
        .replace("__PAYLOAD__", json_script(layout))
    )
    output_path.write_text(html_text, encoding="utf-8")


def chapter_relation_edges(layout: dict[str, Any]) -> list[dict[str, Any]]:
    chapter_id_by_number = {chapter["number"]: chapter["id"] for chapter in layout["chapters"]}
    node_by_id = {node["id"]: node for node in layout["nodes"]}
    counts: Counter[tuple[int, int, str]] = Counter()
    for edge in layout["edges"]:
        if not edge.get("isCrossChapter") or edge["type"] not in STRONG_CROSS_RELATIONS:
            continue
        source = node_by_id.get(edge["source"])
        target = node_by_id.get(edge["target"])
        if not source or not target:
            continue
        source_num = source.get("chapterNumber")
        target_num = target.get("chapterNumber")
        if source_num and target_num and source_num != target_num:
            counts[(source_num, target_num, edge["type"])] += 1
    return [
        {
            "source": chapter_id_by_number[source_num],
            "target": chapter_id_by_number[target_num],
            "type": relation,
            "count": count,
            "isCrossChapter": True,
            "class": "cross-semantic",
            "visibleByDefault": True,
        }
        for (source_num, target_num, relation), count in sorted(counts.items())
        if source_num in chapter_id_by_number and target_num in chapter_id_by_number
    ]


def build_chapter_overview(layout: dict[str, Any]) -> dict[str, Any]:
    chapter_ids = {chapter["id"] for chapter in layout["chapters"]}
    nodes = [node for node in layout["nodes"] if node["id"] == ROOT_NODE_ID or node["id"] in chapter_ids]
    edges = [edge for edge in layout["edges"] if edge["type"] == "CHAPTER_CLUSTER"] + chapter_relation_edges(layout)
    return {
        "meta": {"layout": "chapter overview", "canvas": CANVAS, "physics": False},
        "chapters": layout["chapters"],
        "nodes": nodes,
        "edges": edges,
    }


def build_chapter_local_layout(layout: dict[str, Any], number: int) -> dict[str, Any]:
    chapter = next((item for item in layout["chapters"] if item["number"] == number), None)
    if not chapter:
        return {"meta": {"layout": f"chapter {number} local", "canvas": {"width": 1400, "height": 1040}}, "chapters": [], "nodes": [], "edges": []}
    cx, cy = chapter["x"], chapter["y"]
    local_ids = {
        node["id"]
        for node in layout["nodes"]
        if node.get("chapterNumber") == number or node["id"] == ROOT_NODE_ID
    }
    for edge in layout["edges"]:
        if edge.get("isCrossChapter") and edge["type"] in STRONG_CROSS_RELATIONS:
            if edge["source"] in local_ids:
                local_ids.add(edge["target"])
            if edge["target"] in local_ids:
                local_ids.add(edge["source"])

    local_nodes = []
    for node in layout["nodes"]:
        if node["id"] not in local_ids:
            continue
        copy = dict(node)
        copy["x"] = round(700 + (node["x"] - cx), 2)
        copy["y"] = round(520 + (node["y"] - cy), 2)
        local_nodes.append(copy)
    local_ids = {node["id"] for node in local_nodes}
    local_edges = [
        edge
        for edge in layout["edges"]
        if edge["source"] in local_ids and edge["target"] in local_ids and (not edge.get("isCrossChapter") or edge["type"] in STRONG_CROSS_RELATIONS)
    ]
    return {
        "meta": {"layout": f"chapter {number} local", "canvas": {"width": 1400, "height": 1040}, "physics": False},
        "chapters": [dict(chapter, x=700, y=520)],
        "nodes": local_nodes,
        "edges": local_edges,
    }


def write_repo_navigation_graph(output_path: Path) -> None:
    nav_nodes = [
        ("repo/README", "README", "README.md"),
        ("repo/index", "index", "index.md"),
        ("repo/coverage_report", "coverage_report", "coverage_report.md"),
        ("repo/AGENTS", "AGENTS", "AGENTS.md"),
        ("repo/graph_README", "graph README", "graph/README.md"),
        ("repo/wiki_nav", "00_导航", "wiki/00_导航.md"),
        ("repo/glossary", "99_术语表", "wiki/99_术语表.md"),
        ("repo/raw_books", "raw/books README", "raw/books/README.md"),
        ("repo/raw_text", "raw/extracted_text README", "raw/extracted_text/README.md"),
    ]
    width, height = 1100, 760
    cx, cy, radius = width / 2, height / 2, 250
    nodes = []
    for index, (node_id, label, path) in enumerate(nav_nodes):
        angle = -math.pi / 2 + 2 * math.pi * index / len(nav_nodes)
        nodes.append(
            {
                "id": node_id,
                "label": label,
                "path": path,
                "type": "navigation",
                "level": "navigation",
                "chapter": "repo",
                "chapterNumber": None,
                "x": round(cx + math.cos(angle) * radius, 2),
                "y": round(cy + math.sin(angle) * radius, 2),
                "fixed": True,
                "fixedPosition": True,
                "importance": 1,
                "color": "#94a3b8",
                "displayLabel": label,
            }
        )
    edges = [
        {"source": "repo/index", "target": node["id"], "type": "NAVIGATES_TO", "class": "semantic", "isCrossChapter": False}
        for node in nodes
        if node["id"] != "repo/index"
    ]
    write_clustered_html(
        {
            "meta": {"layout": "repo navigation", "canvas": {"width": width, "height": height}, "physics": False},
            "chapters": [],
            "nodes": nodes,
            "edges": edges,
        },
        output_path,
        title="仓库导航图",
        controls=False,
    )


def write_clustered_graph_suite(graph: dict[str, list[dict[str, Any]]], graph_dir: Path) -> None:
    graph_dir.mkdir(parents=True, exist_ok=True)
    layout = build_clustered_layout(graph)
    (graph_dir / "clustered_knowledge_graph.json").write_text(
        json.dumps(layout, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_clustered_html(layout, graph_dir / "clustered_knowledge_graph.html", title="数字图像处理知识图谱：章节岛屿视图")
    overview = build_chapter_overview(layout)
    write_clustered_html(overview, graph_dir / "chapter_overview.html", title="数字图像处理知识图谱：章节总览", controls=True)
    for number in range(1, MAIN_CHAPTER_COUNT + 1):
        local = build_chapter_local_layout(layout, number)
        write_clustered_html(
            local,
            graph_dir / f"chapter_{number:02d}_graph.html",
            title=f"数字图像处理知识图谱：第 {number} 章局部图",
            controls=True,
        )
    write_repo_navigation_graph(graph_dir / "repo_navigation_graph.html")
