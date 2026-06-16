import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.build_graph_from_wiki import build_wiki_graph, write_mermaid
from tools.configure_obsidian_graph import GRAPH_SETTINGS


class WikiGraphViewTest(unittest.TestCase):
    def test_public_graph_skips_utility_notes_and_readme_link_noise(self):
        with TemporaryDirectory() as workspace:
            root = Path(workspace)
            wiki = root / "wiki"
            chapter = wiki / "02_图像增强"
            chapter.mkdir(parents=True)
            (wiki / "00_导航.md").write_text("[[2.1_γ校正]]\n", encoding="utf-8")
            (wiki / "99_术语表.md").write_text("[[2.1_γ校正]]\n", encoding="utf-8")
            (chapter / "README.md").write_text("[[2.1_γ校正]]\n[[2.2_对比度线性展宽]]\n", encoding="utf-8")
            (chapter / "2.1_γ校正.md").write_text("[[2.2_对比度线性展宽]]\n", encoding="utf-8")
            (chapter / "2.2_对比度线性展宽.md").write_text("无链接\n", encoding="utf-8")

            graph = build_wiki_graph(wiki)
            node_ids = {node["id"] for node in graph["nodes"]}
            edges = {(edge["source"], edge["target"], edge["type"]) for edge in graph["edges"]}

            self.assertNotIn("wiki/00_导航", node_ids)
            self.assertNotIn("wiki/99_术语表", node_ids)
            self.assertNotIn(("wiki/02_图像增强/README", "wiki/02_图像增强/2.1_γ校正", "LINKS_TO"), edges)
            self.assertIn(("wiki/02_图像增强/2.1_γ校正", "wiki/02_图像增强/2.2_对比度线性展宽", "LINKS_TO"), edges)
            self.assertIn(("wiki/02_图像增强/README", "wiki/02_图像增强/2.1_γ校正", "CONTAINS"), edges)

    def test_mermaid_view_omits_raw_and_ordinary_links(self):
        with TemporaryDirectory() as workspace:
            output = Path(workspace) / "mermaid.md"
            graph = {
                "nodes": [
                    {"id": "chapter", "label": "章节"},
                    {"id": "note-a", "label": "知识点A"},
                    {"id": "note-b", "label": "知识点B"},
                ],
                "edges": [
                    {"source": "chapter", "target": "note-a", "type": "CONTAINS"},
                    {"source": "note-a", "target": "note-b", "type": "LINKS_TO"},
                    {"source": "note-a", "target": "note-b", "type": "COMPARES_WITH"},
                ],
            }

            write_mermaid(json.loads(json.dumps(graph)), output)
            text = output.read_text(encoding="utf-8")

            self.assertIn("CONTAINS", text)
            self.assertIn("COMPARES_WITH", text)
            self.assertNotIn("-->|LINKS_TO|", text)
            self.assertIn("主入口请使用 Obsidian Canvas", text)

    def test_repository_graph_has_no_overlinked_wiki_hub(self):
        graph = build_wiki_graph(Path(__file__).resolve().parents[1] / "wiki")
        incoming_links = {}
        labels = {node["id"]: node["label"] for node in graph["nodes"]}
        for edge in graph["edges"]:
            if edge["type"] == "LINKS_TO" and edge["target"].startswith("wiki/"):
                incoming_links[edge["target"]] = incoming_links.get(edge["target"], 0) + 1
        worst_id, worst_count = max(incoming_links.items(), key=lambda item: item[1])

        self.assertLessEqual(worst_count, 12, f"{labels.get(worst_id, worst_id)} has too many ordinary wiki links")

    def test_canvas_files_are_the_primary_graph_entry(self):
        root = Path(__file__).resolve().parents[1]
        overview = root / "数字图像处理知识图谱.canvas"
        cross = root / "数字图像处理跨章关系.canvas"
        self.assertTrue(overview.exists())
        self.assertTrue(cross.exists())

        overview_data = json.loads(overview.read_text(encoding="utf-8"))
        chapter_groups = [node for node in overview_data["nodes"] if node["type"] == "group"]
        file_nodes = [node for node in overview_data["nodes"] if node["type"] == "file"]
        self.assertEqual(len(chapter_groups), 11)
        self.assertGreater(len(file_nodes), 100)
        self.assertLess(len(overview_data.get("edges", [])), len(file_nodes))

        for number in range(1, 12):
            chapter_dir = next(path for path in (root / "wiki").iterdir() if path.is_dir() and path.name.startswith(f"{number:02d}_"))
            canvas = chapter_dir / f"{chapter_dir.name}.canvas"
            self.assertTrue(canvas.exists(), canvas)
            data = json.loads(canvas.read_text(encoding="utf-8"))
            self.assertTrue(any(node["type"] == "text" for node in data["nodes"]))
            self.assertTrue(any(node["type"] == "file" for node in data["nodes"]))

    def test_obsidian_graph_filters_canvas_and_maintenance_files(self):
        search = GRAPH_SETTINGS["search"]
        for token in [
            "-file:.canvas",
            "-file:canvas",
            "-path:.canvas",
            "-file:README",
            "-file:00_导航",
            "-file:99_术语表",
            "-path:tools",
            "-path:graph",
            "-path:examples",
            "-path:raw",
            "-path:templates",
        ]:
            self.assertIn(token, search)
        self.assertFalse(GRAPH_SETTINGS["showAttachments"])
        self.assertFalse(GRAPH_SETTINGS["showOrphans"])
        self.assertTrue(GRAPH_SETTINGS["hideUnresolved"])

    def test_html_graph_outputs_are_removed(self):
        root = Path(__file__).resolve().parents[1]
        self.assertFalse((root / "tools" / "clustered_graph_layout.py").exists())
        self.assertEqual([], list((root / "graph").glob("*.html")))
        self.assertFalse((root / "graph" / "clustered_knowledge_graph.json").exists())


if __name__ == "__main__":
    unittest.main()
