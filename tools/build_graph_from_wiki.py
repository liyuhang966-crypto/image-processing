"""从 Obsidian wiki 笔记生成轻量知识图谱数据。

本项目的主知识图谱入口已经切换到 Obsidian Canvas。本脚本只保留
机器可读 JSON 和 Mermaid 轻量文档，不再生成任何 HTML 图谱。
"""

from __future__ import annotations

import argparse
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


def mermaid_node_id(raw_id: str) -> str:
    safe = re.sub(r"[^0-9A-Za-z_]", "_", raw_id)
    if safe and safe[0].isdigit():
        safe = f"n_{safe}"
    return safe or "node"


def write_mermaid(graph: dict[str, list[dict[str, str]]], output_path: Path) -> None:
    labels = {node["id"]: node["label"] for node in graph["nodes"]}
    lines = [
        "# Mermaid 知识图谱",
        "",
        "> 轻量关系视图，仅展示章节包含关系和人工维护的强语义关系。主入口请使用 Obsidian Canvas。",
        "",
        "```mermaid",
        "graph TD",
    ]
    for node in graph["nodes"]:
        node_id = mermaid_node_id(node["id"])
        label = node["label"].replace('"', "'")
        lines.append(f'  {node_id}["{label}"]')
    for edge in graph["edges"]:
        edge_type = edge.get("type", "")
        if edge_type not in MERMAID_RELATION_TYPES:
            continue
        source = mermaid_node_id(edge["source"])
        target = mermaid_node_id(edge["target"])
        lines.append(f"  {source} -->|{edge_type}| {target}")
    lines.append("```")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build JSON and Mermaid graph files from wiki Markdown links.")
    parser.add_argument("--wiki", default="wiki")
    parser.add_argument("--json", default="graph/knowledge_graph.json")
    parser.add_argument("--mermaid", default="graph/mermaid_graph.md")
    args = parser.parse_args()

    graph = build_wiki_graph(args.wiki)
    json_path = Path(args.json)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_mermaid(graph, Path(args.mermaid))
    print(f"Built graph JSON and Mermaid with {len(graph['nodes'])} nodes and {len(graph['edges'])} edges.")


if __name__ == "__main__":
    main()
