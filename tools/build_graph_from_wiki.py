"""Build the public knowledge graph from Obsidian-style wiki notes.

The wiki is the source of truth. CSV graph data is kept only for the
starter example, while this script reads Markdown files under wiki/ and
derives graph nodes and edges from folders plus [[Obsidian links]].
"""

from __future__ import annotations

import argparse
import html
import json
import re
from dataclasses import dataclass
from pathlib import Path


WIKI_LINK_RE = re.compile(r"\[\[([^\]#|]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
ROOT_UTILITY_NOTES = {"00_导航.md", "99_术语表.md"}
MERMAID_RELATION_TYPES = {
    "CONTAINS",
    "PREREQUISITE",
    "COMPARES_WITH",
    "GENERALIZES",
    "IMPLEMENTED_BY",
    "USES_FORMULA",
    "IMPROVES_OR_EXTENDS",
    "APPLIES_TO",
}


@dataclass(frozen=True)
class WikiNote:
    path: Path
    rel_path: str
    note_id: str
    label: str
    chapter: str


def normalize_path(path: Path) -> str:
    return path.as_posix()


def note_label(path: Path) -> str:
    return path.stem if path.stem != "README" else path.parent.name


def is_root_utility_note(path: Path, wiki_dir: Path) -> bool:
    return path.parent == wiki_dir and path.name in ROOT_UTILITY_NOTES


def should_read_wiki_links(note: WikiNote, wiki_dir: Path) -> bool:
    if note.path.name == "README.md":
        return False
    return not is_root_utility_note(note.path, wiki_dir)


def load_notes(wiki_dir: Path) -> list[WikiNote]:
    notes: list[WikiNote] = []
    for path in sorted(wiki_dir.rglob("*.md")):
        if is_root_utility_note(path, wiki_dir):
            continue
        rel = normalize_path(path.relative_to(wiki_dir.parent))
        chapter = path.parent.name if path.parent != wiki_dir else "wiki"
        notes.append(
            WikiNote(
                path=path,
                rel_path=rel,
                note_id=rel.removesuffix(".md"),
                label=note_label(path),
                chapter=chapter,
            )
        )
    return notes


def build_lookup(notes: list[WikiNote]) -> dict[str, str]:
    lookup: dict[str, str] = {}
    for note in notes:
        lookup[note.note_id] = note.note_id
        lookup[note.label] = note.note_id
        lookup[Path(note.note_id).name] = note.note_id
        lookup[note.rel_path] = note.note_id
        lookup[note.rel_path.removesuffix(".md")] = note.note_id
    return lookup


def resolve_link(raw_target: str, lookup: dict[str, str]) -> str | None:
    target = raw_target.strip().replace("\\", "/")
    if not target or target.startswith("raw/books/"):
        return None
    candidates = [
        target,
        target.removesuffix(".md"),
        Path(target).name,
        Path(target).stem,
    ]
    for candidate in candidates:
        if candidate in lookup:
            return lookup[candidate]
    return None


def build_wiki_graph(wiki_dir: str | Path = "wiki") -> dict[str, list[dict[str, str]]]:
    root = Path(wiki_dir)
    notes = load_notes(root)
    lookup = build_lookup(notes)
    nodes = [
        {
            "id": note.note_id,
            "label": note.label,
            "type": "chapter" if note.path.name == "README.md" else "note",
            "chapter": note.chapter,
            "path": note.rel_path,
        }
        for note in notes
    ]

    edge_keys: set[tuple[str, str, str]] = set()
    edges: list[dict[str, str]] = []
    for note in notes:
        if note.path.name != "README.md":
            chapter_readme = note.path.parent / "README.md"
            if chapter_readme.exists():
                target = normalize_path(chapter_readme.relative_to(root.parent)).removesuffix(".md")
                key = (target, note.note_id, "CONTAINS")
                if key not in edge_keys:
                    edge_keys.add(key)
                    edges.append(
                        {
                            "source": target,
                            "target": note.note_id,
                            "type": "CONTAINS",
                            "description": "Chapter note contains this section note.",
                        }
                    )

        if should_read_wiki_links(note, root):
            text = note.path.read_text(encoding="utf-8")
            for raw_target in WIKI_LINK_RE.findall(text):
                target_id = resolve_link(raw_target, lookup)
                if target_id and target_id != note.note_id:
                    key = (note.note_id, target_id, "LINKS_TO")
                    if key not in edge_keys:
                        edge_keys.add(key)
                        edges.append(
                            {
                                "source": note.note_id,
                                "target": target_id,
                                "type": "LINKS_TO",
                                "description": "Obsidian wiki link.",
                            }
                        )

    graph = {"nodes": nodes, "edges": edges}
    merge_semantic_overlay(graph, Path(wiki_dir).parent / "graph" / "semantic_edges.json")
    return graph


def merge_semantic_overlay(graph: dict[str, list[dict[str, str]]], overlay_path: Path) -> None:
    if not overlay_path.exists():
        return
    overlay = json.loads(overlay_path.read_text(encoding="utf-8"))
    node_ids = {node["id"] for node in graph["nodes"]}
    for node in overlay.get("nodes", []):
        if node["id"] not in node_ids:
            graph["nodes"].append(node)
            node_ids.add(node["id"])

    edge_keys = {(edge["source"], edge["target"], edge["type"]) for edge in graph["edges"]}
    for edge in overlay.get("edges", []):
        if edge["source"] not in node_ids or edge["target"] not in node_ids:
            continue
        key = (edge["source"], edge["target"], edge["type"])
        if key not in edge_keys:
            graph["edges"].append(edge)
            edge_keys.add(key)


def write_mermaid(graph: dict[str, list[dict[str, str]]], output_path: Path) -> None:
    labels = {node["id"]: node["label"] for node in graph["nodes"]}
    lines = [
        "# Mermaid 知识图谱",
        "",
        "`tools/build_graph_from_wiki.py` 从 `wiki/` 生成。为保证图可读，此视图只展示章节包含关系和人工维护的语义关系；细粒度 `LINKS_TO` 仍保留在 `knowledge_graph.json` 中。",
        "",
        "```mermaid",
        "graph TD",
    ]
    for edge in graph["edges"]:
        if edge["type"] not in MERMAID_RELATION_TYPES:
            continue
        source = edge["source"]
        target = edge["target"]
        relation = edge["type"]
        lines.append(
            f'  {safe_mermaid_id(source)}["{escape_mermaid(labels.get(source, source))}"] '
            f'-->|{relation}| {safe_mermaid_id(target)}["{escape_mermaid(labels.get(target, target))}"]'
        )
    lines.extend(["```", ""])
    output_path.write_text("\n".join(lines), encoding="utf-8")


def safe_mermaid_id(value: str) -> str:
    return "N" + re.sub(r"[^0-9A-Za-z_]", "_", value)


def escape_mermaid(value: str) -> str:
    return value.replace('"', "'")


def write_html_legacy(graph: dict[str, list[dict[str, str]]], output_path: Path) -> None:
    payload = html.escape(json.dumps(graph, ensure_ascii=False))
    text = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <title>数字图像处理知识图谱</title>
  <style>
    body {{ font-family: system-ui, sans-serif; margin: 24px; background: #f7f7f4; color: #1f2933; }}
    main {{ max-width: 1180px; margin: auto; }}
    h1 {{ font-size: 28px; }}
    .summary {{ margin-bottom: 16px; color: #52616b; }}
    .graph {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 12px; }}
    article {{ border: 1px solid #d6d3ca; border-radius: 8px; padding: 12px; background: #ffffff; }}
    h2 {{ font-size: 16px; margin: 0 0 8px; }}
    ul {{ margin: 0; padding-left: 18px; }}
    li {{ margin: 4px 0; }}
    code {{ color: #075985; }}
  </style>
</head>
<body>
<main>
  <h1>数字图像处理知识图谱</h1>
  <p class="summary">数据来源：wiki/ Markdown 与 Obsidian 双链。原书 PDF 不包含在公开仓库中。</p>
  <div id="graph" class="graph"></div>
</main>
<script type="application/json" id="graph-data">{payload}</script>
<script>
const graph = JSON.parse(document.getElementById("graph-data").textContent);
const byChapter = new Map();
for (const node of graph.nodes) {{
  const chapter = node.chapter || "wiki";
  if (!byChapter.has(chapter)) byChapter.set(chapter, []);
  byChapter.get(chapter).push(node);
}}
const root = document.getElementById("graph");
for (const [chapter, nodes] of byChapter.entries()) {{
  const article = document.createElement("article");
  const h2 = document.createElement("h2");
  h2.textContent = chapter;
  const ul = document.createElement("ul");
  for (const node of nodes) {{
    const li = document.createElement("li");
    li.innerHTML = `<code>${{node.label}}</code>`;
    ul.appendChild(li);
  }}
  article.append(h2, ul);
  root.appendChild(article);
}}
</script>
</body>
</html>
"""
    output_path.write_text(text, encoding="utf-8")


def write_html(graph: dict[str, list[dict[str, str]]], output_path: Path) -> None:
    payload = html.escape(json.dumps(graph, ensure_ascii=False))
    template = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <title>数字图像处理知识图谱</title>
  <style>
    :root {
      --bg: #f7f7f4;
      --ink: #1f2933;
      --muted: #667085;
      --line: #c9ced6;
      --chapter: #2563eb;
      --note: #334155;
      --concept: #0f766e;
      --formula: #b45309;
      --code: #7c3aed;
    }
    body { font-family: system-ui, sans-serif; margin: 0; background: var(--bg); color: var(--ink); }
    main { padding: 20px 24px 28px; }
    h1 { font-size: 24px; margin: 0 0 6px; }
    .summary { margin: 0 0 14px; color: var(--muted); line-height: 1.6; }
    .toolbar { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; margin: 12px 0 16px; }
    .toolbar label { display: inline-flex; align-items: center; gap: 6px; font-size: 13px; color: #344054; }
    .stage { overflow: auto; border: 1px solid #d6d3ca; background: #fff; }
    svg { display: block; min-width: 1480px; min-height: 1120px; }
    .cluster { fill: #f8fafc; stroke: #e2e8f0; stroke-width: 1; }
    .edge { fill: none; stroke: var(--line); stroke-opacity: .56; stroke-width: 1.15; }
    .edge.semantic { stroke-opacity: .74; stroke-width: 1.55; }
    .node.chapter { fill: var(--chapter); }
    .node.note { fill: var(--note); }
    .node.concept { fill: var(--concept); }
    .node.formula { fill: var(--formula); }
    .node.code { fill: var(--code); }
    .label { font-size: 10px; fill: #344054; pointer-events: none; }
    .chapter-label { font-size: 13px; font-weight: 700; fill: #111827; pointer-events: none; }
    .legend { display: flex; flex-wrap: wrap; gap: 14px; font-size: 13px; color: #344054; margin-bottom: 10px; }
    .swatch { width: 10px; height: 10px; border-radius: 50%; display: inline-block; margin-right: 5px; }
  </style>
</head>
<body>
<main>
  <h1>数字图像处理知识图谱</h1>
  <p class="summary">默认使用固定章节分组布局，节点大小按类型固定，不按连接数放大。普通双链可按需打开；默认视图只保留章节结构和语义关系，避免复习图被热点节点拉散。</p>
  <div class="toolbar" id="toolbar"></div>
  <div class="legend">
    <span><i class="swatch" style="background:var(--chapter)"></i>章节</span>
    <span><i class="swatch" style="background:var(--note)"></i>小节</span>
    <span><i class="swatch" style="background:var(--concept)"></i>概念</span>
    <span><i class="swatch" style="background:var(--formula)"></i>公式</span>
    <span><i class="swatch" style="background:var(--code)"></i>代码</span>
  </div>
  <div class="stage"><svg id="graph" viewBox="0 0 1480 1120" aria-label="知识图谱"></svg></div>
</main>
<script type="application/json" id="graph-data">__GRAPH_DATA__</script>
<script>
const graph = JSON.parse(document.getElementById("graph-data").textContent);
const svg = document.getElementById("graph");
const toolbar = document.getElementById("toolbar");
const width = 1480;
const height = 1120;
const semanticTypes = ["PREREQUISITE", "COMPARES_WITH", "GENERALIZES", "IMPLEMENTED_BY", "USES_FORMULA", "IMPROVES_OR_EXTENDS", "APPLIES_TO"];
const relationState = new Map([["CONTAINS", true], ["LINKS_TO", false], ...semanticTypes.map((name) => [name, true])]);

for (const [name, enabled] of relationState.entries()) {
  const label = document.createElement("label");
  const input = document.createElement("input");
  input.type = "checkbox";
  input.checked = enabled;
  input.dataset.relation = name;
  input.addEventListener("change", () => {
    relationState.set(name, input.checked);
    render();
  });
  label.append(input, document.createTextNode(name));
  toolbar.appendChild(label);
}

function chapterIndex(label) {
  const match = String(label || "").match(/^(\\d+)/);
  return match ? Number(match[1]) : 99;
}

function nodeClass(node) {
  if (node.type === "chapter") return "chapter";
  if (node.type === "code") return "code";
  if (node.type === "formula") return "formula";
  if (node.type === "concept") return "concept";
  return "note";
}

function nodeRadius(node) {
  const klass = nodeClass(node);
  if (klass === "chapter") return 14;
  if (klass === "note") return 5.5;
  return 4.2;
}

function buildLayout() {
  const nodes = graph.nodes;
  const byId = new Map(nodes.map((node) => [node.id, node]));
  const chapterNodes = nodes
    .filter((node) => node.type === "chapter" && String(node.id).startsWith("wiki/"))
    .sort((a, b) => chapterIndex(a.label) - chapterIndex(b.label) || a.label.localeCompare(b.label, "zh-CN"));
  const positions = new Map();
  const cols = 4;
  const rows = Math.ceil(chapterNodes.length / cols);
  const cellW = width / cols;
  const cellH = height / rows;
  const centers = new Map();

  chapterNodes.forEach((chapter, index) => {
    const col = index % cols;
    const row = Math.floor(index / cols);
    const cx = col * cellW + cellW / 2;
    const cy = row * cellH + cellH / 2;
    centers.set(chapter.chapter, { x: cx, y: cy, w: cellW, h: cellH });
    positions.set(chapter.id, { x: cx, y: cy });

    const children = nodes
      .filter((node) => node.type !== "chapter" && node.chapter === chapter.chapter && String(node.id).startsWith("wiki/"))
      .sort((a, b) => a.label.localeCompare(b.label, "zh-CN"));
    const radius = Math.min(cellW, cellH) * 0.34;
    children.forEach((node, childIndex) => {
      const angle = -Math.PI / 2 + (2 * Math.PI * childIndex) / Math.max(children.length, 1);
      const ring = radius * (children.length > 12 && childIndex % 2 ? 0.72 : 1);
      positions.set(node.id, { x: cx + Math.cos(angle) * ring, y: cy + Math.sin(angle) * ring });
    });
  });

  const chapterVotes = new Map();
  for (const edge of graph.edges) {
    for (const id of [edge.source, edge.target]) {
      const node = byId.get(id);
      if (node && node.chapter && centers.has(node.chapter)) {
        const other = id === edge.source ? edge.target : edge.source;
        if (!chapterVotes.has(other)) chapterVotes.set(other, new Map());
        const votes = chapterVotes.get(other);
        votes.set(node.chapter, (votes.get(node.chapter) || 0) + 1);
      }
    }
  }

  const externalNodesByChapter = new Map();
  for (const node of nodes) {
    if (positions.has(node.id)) continue;
    const votes = chapterVotes.get(node.id);
    if (!votes) continue;
    const chapter = [...votes.entries()].sort((a, b) => b[1] - a[1])[0][0];
    if (!externalNodesByChapter.has(chapter)) externalNodesByChapter.set(chapter, []);
    externalNodesByChapter.get(chapter).push(node);
  }

  for (const [chapter, externalNodes] of externalNodesByChapter.entries()) {
    const center = centers.get(chapter);
    if (!center) continue;
    externalNodes.slice(0, 18).forEach((node, index) => {
      const x = center.x - 115 + (index % 6) * 46;
      const y = center.y + center.h * 0.31 + Math.floor(index / 6) * 22;
      positions.set(node.id, { x, y });
    });
  }

  return { byId, chapterNodes, centers, positions };
}

function svgEl(name, attrs = {}) {
  const el = document.createElementNS("http://www.w3.org/2000/svg", name);
  for (const [key, value] of Object.entries(attrs)) el.setAttribute(key, value);
  return el;
}

function render() {
  svg.replaceChildren();
  const { byId, chapterNodes, centers, positions } = buildLayout();
  const edgeLayer = svgEl("g");
  const nodeLayer = svgEl("g");
  svg.append(edgeLayer, nodeLayer);

  for (const chapter of chapterNodes) {
    const center = centers.get(chapter.chapter);
    nodeLayer.append(svgEl("rect", {
      class: "cluster",
      x: center.x - center.w / 2 + 14,
      y: center.y - center.h / 2 + 14,
      width: center.w - 28,
      height: center.h - 28,
      rx: 8,
    }));
  }

  for (const edge of graph.edges) {
    if (!relationState.get(edge.type)) continue;
    const source = positions.get(edge.source);
    const target = positions.get(edge.target);
    if (!source || !target) continue;
    const path = svgEl("path", {
      class: `edge ${edge.type === "CONTAINS" || edge.type === "LINKS_TO" ? "" : "semantic"}`,
      d: `M ${source.x} ${source.y} L ${target.x} ${target.y}`,
    });
    path.append(svgEl("title"));
    path.firstChild.textContent = `${byId.get(edge.source)?.label || edge.source} -> ${byId.get(edge.target)?.label || edge.target} (${edge.type})`;
    edgeLayer.append(path);
  }

  for (const [id, pos] of positions.entries()) {
    const node = byId.get(id);
    if (!node) continue;
    const klass = nodeClass(node);
    const circle = svgEl("circle", {
      class: `node ${klass}`,
      cx: pos.x,
      cy: pos.y,
      r: nodeRadius(node),
    });
    circle.append(svgEl("title"));
    circle.firstChild.textContent = `${node.label}\\n${node.id}`;
    nodeLayer.append(circle);
    const label = svgEl("text", {
      class: klass === "chapter" ? "chapter-label" : "label",
      x: pos.x + nodeRadius(node) + 4,
      y: pos.y + 3,
    });
    label.textContent = node.label;
    nodeLayer.append(label);
  }
}

render();
</script>
</body>
</html>
"""
    output_path.write_text(template.replace("__GRAPH_DATA__", payload), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build graph files from wiki Markdown links.")
    parser.add_argument("--wiki", default="wiki")
    parser.add_argument("--json", default="graph/knowledge_graph.json")
    parser.add_argument("--mermaid", default="graph/mermaid_graph.md")
    parser.add_argument("--html", default="graph/knowledge_graph.html")
    args = parser.parse_args()

    graph = build_wiki_graph(args.wiki)
    json_path = Path(args.json)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_mermaid(graph, Path(args.mermaid))
    write_html(graph, Path(args.html))
    print(f"Built graph with {len(graph['nodes'])} nodes and {len(graph['edges'])} edges.")


if __name__ == "__main__":
    main()
