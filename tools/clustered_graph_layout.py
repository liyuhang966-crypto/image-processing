"""Fixed chapter-island graph layouts.

The main graph is intentionally not a force-directed graph. Every visible node
gets a deterministic position from its own path/id, and edges never influence
layout. This keeps each chapter as an independent visual island.
"""

from __future__ import annotations

import html
import json
import math
import re
from collections import Counter
from pathlib import Path
from typing import Any


MAIN_CHAPTER_COUNT = 11
CANVAS = {"width": 5000, "height": 3600}
CLUSTER_RADIUS = 370

CHAPTER_CENTERS = {
    1: (700, 700),
    2: (1800, 450),
    3: (3000, 500),
    4: (4300, 850),
    5: (4300, 2000),
    6: (3300, 3050),
    7: (2200, 3150),
    8: (1000, 2700),
    9: (500, 1700),
    10: (1900, 1850),
    11: (3200, 1850),
}

PALETTE = {
    1: "#7dd3fc",
    2: "#fb923c",
    3: "#86efac",
    4: "#f0abfc",
    5: "#c4b5fd",
    6: "#fde047",
    7: "#67e8f9",
    8: "#fb7185",
    9: "#bef264",
    10: "#93c5fd",
    11: "#fbbf24",
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
STRONG_CROSS_RELATIONS = {"PREREQUISITE", "COMPARES_WITH", "GENERALIZES", "IMPROVES_OR_EXTENDS", "APPLIES_TO"}
CODE_RELATIONS = {"IMPLEMENTED_BY", "USES_FORMULA"}
NAVIGATION_PATHS = {
    "README.md",
    "index.md",
    "coverage_report.md",
    "graph/README.md",
    "wiki/00_导航.md",
    "wiki/99_术语表.md",
    "raw/books/README.md",
    "raw/extracted_text/README.md",
}


def chapter_from_text(value: str | None) -> int | None:
    if not value:
        return None
    patterns = [
        r"(?:^|/)wiki/(\d{2})_",
        r"(?:^|/)examples/(\d{2})_",
        r"(?:^|/)formula/ch(\d{2})",
        r"(?:^|/)concept/ch(\d{2})",
        r"(?:^|/)code/ch(\d{2})",
        r"^(\d{2})_",
    ]
    for pattern in patterns:
        match = re.search(pattern, value)
        if match:
            number = int(match.group(1))
            if 1 <= number <= MAIN_CHAPTER_COUNT:
                return number
    return None


def chapter_from_label(label: str | None) -> int | None:
    if not label:
        return None
    match = re.match(r"^(\d+)(?:\.|_)", label)
    if not match:
        return None
    number = int(match.group(1))
    return number if 1 <= number <= MAIN_CHAPTER_COUNT else None


def chapter_for_node(node: dict[str, Any]) -> int | None:
    for field in (node.get("path"), node.get("id"), node.get("chapter")):
        number = chapter_from_text(str(field) if field else "")
        if number:
            return number
    return chapter_from_label(node.get("label"))


def is_navigation_node(node: dict[str, Any]) -> bool:
    path = node.get("path", "")
    node_id = node.get("id", "")
    label = node.get("label", "")
    if path in NAVIGATION_PATHS or node_id in {"README", "index", "coverage_report"}:
        return True
    if path.startswith("raw/books/") or path.startswith("raw/extracted_text/") or path.startswith("raw/temp/"):
        return True
    if node_id.startswith("raw/books") or node_id.startswith("raw/extracted_text") or node_id.startswith("raw/temp"):
        return True
    return label in {"README", "index", "coverage_report", "00_导航", "99_术语表"}


def label_number(label: str) -> str:
    match = re.match(r"^(\d+(?:\.\d+|\.x)*)_", label)
    return match.group(1) if match else ""


def node_level(node: dict[str, Any]) -> str:
    if node.get("type") == "chapter" or re.match(r"^wiki/\d{2}_[^/]+/README$", str(node.get("id", ""))):
        return "chapter"
    node_kind = node.get("type") or node.get("kind")
    if node_kind == "code" or str(node.get("id", "")).startswith("examples/"):
        return "code"
    if node_kind == "formula" or str(node.get("id", "")).startswith("formula/"):
        return "formula"
    if node_kind == "concept" or str(node.get("id", "")).startswith("concept/"):
        return "concept"
    number = label_number(node.get("label", ""))
    if ".x" in number:
        return "exercise"
    dot_count = number.count(".")
    if dot_count == 1:
        return "section"
    if dot_count >= 2:
        return "subsection"
    return "note"


def importance_for_level(level: str) -> int:
    return {"chapter": 5, "section": 4, "subsection": 3, "exercise": 2, "concept": 2, "formula": 2, "code": 1}.get(level, 1)


def display_label(node: dict[str, Any], level: str, chapter_number: int) -> str:
    if level == "chapter":
        label = node.get("label", f"{chapter_number:02d}")
        return f"第 {chapter_number} 章 {label.split('_', 1)[-1]}"
    number = label_number(node.get("label", ""))
    return number or node.get("label", node["id"])[:18]


def sort_key(node: dict[str, Any]) -> tuple[int, str, str]:
    level = node_level(node)
    rank = {"chapter": 0, "section": 1, "subsection": 2, "exercise": 3, "concept": 4, "formula": 5, "code": 6}.get(level, 7)
    return rank, label_number(node.get("label", "")), node.get("id", "")


def ring_position(center: tuple[float, float], radius: float, index: int, count: int, offset: float) -> tuple[float, float, float]:
    angle = offset if count <= 1 else offset + 2 * math.pi * index / count
    return center[0] + radius * math.cos(angle), center[1] + radius * math.sin(angle), angle


def validate_chapter_assignment(node: dict[str, Any], chapter_number: int) -> None:
    path_chapter = chapter_from_text(node.get("path"))
    label_chapter = chapter_from_label(node.get("label"))
    id_chapter = chapter_from_text(node.get("id"))
    for source, expected in (("path", path_chapter), ("label", label_chapter), ("id", id_chapter)):
        if expected and expected != chapter_number:
            raise ValueError(
                f"Chapter mismatch for {node.get('id')}: {source} implies chapter {expected}, "
                f"but layout assigned chapter {chapter_number}."
            )
    if label_chapter in {3, 9, 10, 11} and chapter_number != label_chapter:
        raise ValueError(f"Strict chapter check failed for {node.get('id')}: label belongs to chapter {label_chapter}.")


def enrich_node(node: dict[str, Any], *, chapter_number: int, radius: float, angle: float, x: float, y: float) -> dict[str, Any]:
    validate_chapter_assignment(node, chapter_number)
    level = node_level(node)
    color = PALETTE[chapter_number]
    return {
        **node,
        "chapterNumber": chapter_number,
        "chapter": node.get("chapter") or f"{chapter_number:02d}",
        "level": level,
        "type": node.get("type") or node.get("kind") or "note",
        "path": node.get("path") or node["id"],
        "importance": importance_for_level(level),
        "displayLabel": display_label(node, level, chapter_number),
        "color": color,
        "x": round(x, 2),
        "y": round(y, 2),
        "radius": round(radius, 2),
        "angle": round(angle, 6),
        "fixed": True,
        "fixedPosition": True,
        "physics": False,
    }


def relation_class(edge: dict[str, Any]) -> str:
    edge_type = edge["type"]
    if edge_type in CODE_RELATIONS:
        base = "code"
    elif edge_type in SEMANTIC_RELATIONS:
        base = "semantic"
    elif edge_type == "CONTAINS":
        base = "contains"
    elif edge_type == "LINKS_TO":
        base = "link"
    else:
        base = "other"
    return f"cross-{base}" if edge.get("isCrossChapter") else base


def chapter_bounds(chapter: dict[str, Any]) -> tuple[float, float, float, float]:
    x, y = chapter["x"], chapter["y"]
    return x - CLUSTER_RADIUS, y - CLUSTER_RADIUS, x + CLUSTER_RADIUS, y + CLUSTER_RADIUS


def boxes_overlap(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> bool:
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])


def validate_cluster_boundaries(chapters: list[dict[str, Any]], nodes: list[dict[str, Any]]) -> None:
    for left_index, left in enumerate(chapters):
        for right in chapters[left_index + 1 :]:
            if boxes_overlap(chapter_bounds(left), chapter_bounds(right)):
                raise ValueError(f"Chapter cluster boxes overlap: {left['number']} and {right['number']}.")
    centers = {chapter["number"]: (chapter["x"], chapter["y"]) for chapter in chapters}
    for node in nodes:
        chapter_number = node["chapterNumber"]
        center = centers[chapter_number]
        distance = math.hypot(node["x"] - center[0], node["y"] - center[1])
        if distance > CLUSTER_RADIUS:
            raise ValueError(f"Node {node['id']} escaped chapter {chapter_number} cluster: radius {distance:.1f}.")


def build_clustered_layout(graph: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    source_nodes = [dict(node) for node in graph["nodes"] if not is_navigation_node(node)]
    source_edges = [dict(edge) for edge in graph["edges"]]
    nodes_by_chapter: dict[int, list[dict[str, Any]]] = {number: [] for number in range(1, MAIN_CHAPTER_COUNT + 1)}
    skipped_nodes: list[str] = []

    for node in source_nodes:
        chapter_number = chapter_for_node(node)
        if not chapter_number:
            skipped_nodes.append(node["id"])
            continue
        nodes_by_chapter[chapter_number].append(node)

    layout_nodes: list[dict[str, Any]] = []
    chapters: list[dict[str, Any]] = []
    for number in range(1, MAIN_CHAPTER_COUNT + 1):
        center = CHAPTER_CENTERS[number]
        chapter_nodes = sorted(nodes_by_chapter[number], key=sort_key)
        if not chapter_nodes:
            raise ValueError(f"Chapter {number} has no nodes; cannot build island layout.")
        chapter_center = next((node for node in chapter_nodes if node_level(node) == "chapter"), chapter_nodes[0])
        chapters.append(
            {
                "number": number,
                "id": chapter_center["id"],
                "label": chapter_center.get("label", f"第 {number} 章"),
                "x": center[0],
                "y": center[1],
                "radius": CLUSTER_RADIUS,
                "color": PALETTE[number],
            }
        )

        by_level = {
            "chapter": [node for node in chapter_nodes if node_level(node) == "chapter"],
            "section": [node for node in chapter_nodes if node_level(node) == "section"],
            "subsection": [node for node in chapter_nodes if node_level(node) == "subsection"],
            "exercise": [node for node in chapter_nodes if node_level(node) == "exercise"],
            "concept": [node for node in chapter_nodes if node_level(node) == "concept"],
            "formula": [node for node in chapter_nodes if node_level(node) == "formula"],
            "code": [node for node in chapter_nodes if node_level(node) == "code"],
            "note": [node for node in chapter_nodes if node_level(node) == "note"],
        }

        used_ids: set[str] = set()
        for node in by_level["chapter"]:
            layout_nodes.append(enrich_node(node, chapter_number=number, radius=0, angle=0, x=center[0], y=center[1]))
            used_ids.add(node["id"])

        rings = [
            ("section", 135, -math.pi / 2),
            ("subsection", 245, -math.pi / 2 + 0.08),
            ("exercise", 300, math.pi / 2),
            ("concept", 285, -math.pi / 6),
            ("formula", 315, math.pi / 7),
            ("code", 345, math.pi),
            ("note", 205, math.pi / 2),
        ]
        for level, radius, offset in rings:
            ring_nodes = by_level[level]
            for index, node in enumerate(ring_nodes):
                x, y, angle = ring_position(center, radius, index, max(1, len(ring_nodes)), offset)
                layout_nodes.append(enrich_node(node, chapter_number=number, radius=radius, angle=angle, x=x, y=y))
                used_ids.add(node["id"])

    layout_by_id = {node["id"]: node for node in layout_nodes}
    edge_keys: set[tuple[str, str, str]] = set()
    layout_edges: list[dict[str, Any]] = []
    for edge in source_edges:
        source = layout_by_id.get(edge["source"])
        target = layout_by_id.get(edge["target"])
        if not source or not target:
            continue
        edge_key = (edge["source"], edge["target"], edge["type"])
        if edge_key in edge_keys:
            continue
        edge_keys.add(edge_key)
        source_chapter = source["chapterNumber"]
        target_chapter = target["chapterNumber"]
        cross = source_chapter != target_chapter
        enriched = {
            **edge,
            "sourceChapter": source_chapter,
            "targetChapter": target_chapter,
            "isCrossChapter": cross,
            "layoutInfluence": False,
            "visibleByDefault": (not cross and edge["type"] in {"CONTAINS", *SEMANTIC_RELATIONS}),
        }
        enriched["class"] = relation_class(enriched)
        layout_edges.append(enriched)

    validate_cluster_boundaries(chapters, layout_nodes)
    return {
        "meta": {
            "layout": "fixed chapter partitions",
            "canvas": CANVAS,
            "physics": False,
            "clusterRadius": CLUSTER_RADIUS,
            "skippedUnassignedNodes": skipped_nodes,
            "description": "Static SVG layout with fixed chapter centers; edges never affect node coordinates.",
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
        <option value="default">默认：章内结构与语义</option>
        <option value="all">全部关系</option>
        <option value="contains">只看章节包含关系</option>
        <option value="semantic">只看语义关系</option>
        <option value="code">只看代码实现关系</option>
        <option value="backbone">只看跨章主干关系</option>
      </select>
    </label>
    <label>标签
      <select id="labelMode">
        <option value="chapters">只显示章节标签</option>
        <option value="current">显示当前章节标签</option>
        <option value="all">显示全部标签</option>
        <option value="none">隐藏全部标签</option>
      </select>
    </label>
    <label><input type="checkbox" id="showCross"> 显示跨章边</label>
    <label><input type="checkbox" id="showLinks"> 显示普通 LINKS_TO</label>
    <button type="button" id="resetView">重置视图</button>
  </div>
"""


def write_clustered_html(layout: dict[str, Any], output_path: Path, *, title: str, controls: bool = True) -> None:
    canvas = layout.get("meta", {}).get("canvas", CANVAS)
    view_box = f"0 0 {canvas.get('width', 5000)} {canvas.get('height', 3600)}"
    template = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>__TITLE__</title>
  <style>
    :root { --bg:#111317; --panel:#1d222b; --ink:#f3f4f6; --muted:#aab2c0; --line:#8c94a3; }
    * { box-sizing:border-box; }
    body { margin:0; background:var(--bg); color:var(--ink); font-family:system-ui, "Microsoft YaHei", sans-serif; }
    main { padding:16px 18px 22px; }
    h1 { margin:0 0 6px; font-size:22px; }
    .summary { margin:0 0 12px; color:var(--muted); font-size:13px; line-height:1.55; }
    .controls { display:flex; flex-wrap:wrap; gap:10px; align-items:center; margin:10px 0 12px; }
    label, button { color:#dde3ee; font-size:12px; }
    select, button { margin-left:6px; border:1px solid #3b404a; border-radius:6px; background:var(--panel); color:#f8fafc; padding:5px 8px; }
    input { vertical-align:middle; }
    .wrap { display:grid; grid-template-columns:minmax(0, 1fr) 310px; gap:12px; }
    .stage { overflow:auto; border:1px solid #30343b; border-radius:8px; background:#0b0d10; min-height:780px; }
    svg { display:block; min-width:1300px; height:min(82vh, 920px); min-height:780px; }
    aside { border:1px solid #30343b; border-radius:8px; background:#1b1e24; padding:12px; min-height:180px; color:#d8dee9; font-size:13px; }
    .legend { display:flex; flex-wrap:wrap; gap:10px; margin:0 0 10px; color:#cbd5e1; font-size:12px; }
    .swatch { width:10px; height:10px; border-radius:50%; display:inline-block; margin-right:5px; }
    .edge { fill:none; stroke:var(--line); stroke-width:.9; stroke-opacity:.26; }
    .edge.contains { stroke-opacity:.34; }
    .edge.link { stroke-opacity:.18; }
    .edge.semantic { stroke-dasharray:5 4; stroke-width:1.1; stroke-opacity:.34; }
    .edge.code { stroke-dasharray:2 4; stroke-width:1.0; stroke-opacity:.30; }
    .edge.cross-link, .edge.cross-semantic, .edge.cross-code { stroke:#cbd5e1; stroke-opacity:.10; stroke-width:.7; }
    .node { stroke:rgba(255,255,255,.72); stroke-width:1; cursor:default; }
    .node.chapter { stroke-width:2.2; }
    .node.section { stroke-width:1.4; }
    .node.code, .node.formula, .node.concept { stroke-dasharray:2 2; }
    .halo { fill:rgba(255,255,255,.018); stroke-width:1.1; stroke-opacity:.24; }
    .label { fill:#e5e7eb; font-size:11px; text-anchor:middle; paint-order:stroke; stroke:#0b0d10; stroke-width:3px; pointer-events:none; }
    .label.chapter { font-size:16px; font-weight:700; opacity:1; }
    .label.hidden { opacity:0; }
    .dim { opacity:.10; }
    .highlight { opacity:1 !important; stroke-width:2.6; }
    .edge.highlight { stroke-opacity:.88 !important; stroke-width:2; }
    .hidden-node, .hidden-edge { display:none; }
    code { color:#93c5fd; word-break:break-all; }
    @media (max-width:980px) { .wrap { grid-template-columns:1fr; } aside { min-height:120px; } }
  </style>
</head>
<body>
<main>
  <h1>__TITLE__</h1>
  <p class="summary">固定章节分区布局：每章一个独立圆形星团，节点坐标只由本章中心和目录顺序决定；跨章边只作为可开关的淡色线条，不参与布局。</p>
  __CONTROLS__
  <div class="legend" id="legend"></div>
  <div class="wrap">
    <div class="stage"><svg id="graph" viewBox="__VIEWBOX__" aria-label="__TITLE__"></svg></div>
    <aside id="details">悬停节点查看完整标题、章节、类型和路径；点击章节节点可只显示该章标签。</aside>
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
const strong = new Set(["PREREQUISITE", "COMPARES_WITH", "GENERALIZES", "IMPROVES_OR_EXTENDS", "APPLIES_TO"]);
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
  item.append(swatch, document.createTextNode(`第 ${chapter.number} 章`));
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
  if (node.level === "chapter") return 23;
  if (node.level === "section") return 12;
  if (node.level === "subsection") return 8;
  if (node.level === "exercise") return 7;
  if (node.level === "code") return 5;
  return 6;
}

function nodeVisible(node) {
  const selected = chapterFilter ? chapterFilter.value : "all";
  return selected === "all" || String(node.chapterNumber) === selected;
}

function edgeVisible(edge) {
  const mode = relationMode ? relationMode.value : "default";
  const source = nodesById.get(edge.source);
  const target = nodesById.get(edge.target);
  if (!source || !target || !nodeVisible(source) || !nodeVisible(target)) return false;
  if (edge.isCrossChapter && (!showCross || !showCross.checked)) return false;
  if (edge.type === "LINKS_TO" && (!showLinks || !showLinks.checked)) return false;
  if (mode === "all") return true;
  if (mode === "contains") return edge.type === "CONTAINS";
  if (mode === "semantic") return semantic.has(edge.type);
  if (mode === "code") return codeRels.has(edge.type);
  if (mode === "backbone") return edge.isCrossChapter && strong.has(edge.type);
  return !edge.isCrossChapter && (edge.type === "CONTAINS" || semantic.has(edge.type));
}

function labelVisible(node) {
  const mode = labelMode ? labelMode.value : "chapters";
  if (mode === "none") return false;
  if (node.level === "chapter") return mode !== "none";
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
    haloLayer.append(el("circle", { class: `halo ${visible ? "" : "hidden-node"}`, cx: chapter.x, cy: chapter.y, r: chapter.radius, stroke: chapter.color }));
  }

  for (const edge of data.edges) {
    const source = nodesById.get(edge.source);
    const target = nodesById.get(edge.target);
    if (!source || !target) continue;
    const bend = edge.isCrossChapter ? 120 : 0;
    const path = el("path", {
      class: `edge ${edge.class || "edge"} ${edgeVisible(edge) ? "" : "hidden-edge"}`,
      d: `M ${source.x} ${source.y} Q ${(source.x + target.x) / 2} ${(source.y + target.y) / 2 - bend} ${target.x} ${target.y}`,
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
    circle.append(el("title"));
    circle.firstChild.textContent = `${node.label}\\n${node.path || node.id}`;
    circle.addEventListener("mouseenter", () => highlight(node.id));
    circle.addEventListener("mouseleave", clearHighlight);
    circle.addEventListener("click", () => focusChapter(node.chapterNumber));
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

function focusChapter(chapterNumber) {
  if (!chapterFilter || !labelMode) return;
  chapterFilter.value = String(chapterNumber);
  labelMode.value = "current";
  render();
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
  details.innerHTML = `<strong>${node.label}</strong><p>章节：第 ${node.chapterNumber} 章</p><p>类型：${node.type} / ${node.level}</p><p>路径：<code>${node.path || node.id}</code></p>`;
}

function clearHighlight() {
  for (const item of svg.querySelectorAll(".dim,.highlight")) item.classList.remove("dim", "highlight");
  details.textContent = "悬停节点查看完整标题、章节、类型和路径；点击章节节点可只显示该章标签。";
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
    counts: Counter[tuple[int, int, str]] = Counter()
    for edge in layout["edges"]:
        if not edge.get("isCrossChapter") or edge["type"] not in STRONG_CROSS_RELATIONS:
            continue
        source_num = edge.get("sourceChapter")
        target_num = edge.get("targetChapter")
        if source_num and target_num and source_num != target_num:
            counts[(source_num, target_num, edge["type"])] += 1
    edges = []
    for (source_num, target_num, relation), count in sorted(counts.items()):
        edges.append(
            {
                "source": chapter_id_by_number[source_num],
                "target": chapter_id_by_number[target_num],
                "type": relation,
                "count": count,
                "sourceChapter": source_num,
                "targetChapter": target_num,
                "isCrossChapter": True,
                "layoutInfluence": False,
                "visibleByDefault": False,
                "class": "cross-semantic",
            }
        )
    return edges


def build_chapter_overview(layout: dict[str, Any]) -> dict[str, Any]:
    chapter_ids = {chapter["id"] for chapter in layout["chapters"]}
    nodes = [node for node in layout["nodes"] if node["id"] in chapter_ids]
    return {
        "meta": {"layout": "chapter overview", "canvas": CANVAS, "physics": False},
        "chapters": layout["chapters"],
        "nodes": nodes,
        "edges": chapter_relation_edges(layout),
    }


def build_chapter_local_layout(layout: dict[str, Any], number: int) -> dict[str, Any]:
    chapter = next((item for item in layout["chapters"] if item["number"] == number), None)
    if not chapter:
        return {"meta": {"layout": f"chapter {number} local", "canvas": {"width": 1000, "height": 900}}, "chapters": [], "nodes": [], "edges": []}
    cx, cy = chapter["x"], chapter["y"]
    local_nodes = []
    local_ids = set()
    for node in layout["nodes"]:
        if node.get("chapterNumber") != number:
            continue
        copy = dict(node)
        copy["x"] = round(500 + (node["x"] - cx), 2)
        copy["y"] = round(450 + (node["y"] - cy), 2)
        local_nodes.append(copy)
        local_ids.add(node["id"])
    local_edges = [
        edge
        for edge in layout["edges"]
        if edge["source"] in local_ids and edge["target"] in local_ids and not edge.get("isCrossChapter")
    ]
    return {
        "meta": {"layout": f"chapter {number} local", "canvas": {"width": 1000, "height": 900}, "physics": False},
        "chapters": [dict(chapter, x=500, y=450)],
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
                "radius": radius,
                "angle": round(angle, 6),
                "fixed": True,
                "fixedPosition": True,
                "physics": False,
                "importance": 1,
                "color": "#94a3b8",
                "displayLabel": label,
            }
        )
    edges = [
        {"source": "repo/index", "target": node["id"], "type": "NAVIGATES_TO", "class": "semantic", "isCrossChapter": False, "layoutInfluence": False}
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
    write_clustered_html(overview, graph_dir / "chapter_overview.html", title="数字图像处理知识图谱：章节总览")
    for number in range(1, MAIN_CHAPTER_COUNT + 1):
        local = build_chapter_local_layout(layout, number)
        write_clustered_html(
            local,
            graph_dir / f"chapter_{number:02d}_graph.html",
            title=f"数字图像处理知识图谱：第 {number} 章局部图",
        )
    write_repo_navigation_graph(graph_dir / "repo_navigation_graph.html")
