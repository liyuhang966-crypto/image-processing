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


def write_html(graph: dict[str, list[dict[str, str]]], output_path: Path) -> None:
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
