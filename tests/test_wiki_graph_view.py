import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.build_graph_from_wiki import build_wiki_graph, write_html, write_mermaid


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

    def test_mermaid_view_omits_raw_links(self):
        with TemporaryDirectory() as workspace:
            output = Path(workspace) / "mermaid.md"
            graph = {
                "nodes": [
                    {"id": "chapter", "label": "章节"},
                    {"id": "note-a", "label": "知识点 A"},
                    {"id": "note-b", "label": "知识点 B"},
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

    def test_default_html_uses_radial_cluster_layout(self):
        with TemporaryDirectory() as workspace:
            output = Path(workspace) / "graph.html"
            graph = {
                "nodes": [
                    {"id": "wiki/01_引言/README", "label": "01_引言", "type": "chapter", "chapter": "01_引言"},
                    {"id": "wiki/01_引言/1.1_入口", "label": "1.1_入口", "type": "note", "chapter": "01_引言"},
                ],
                "edges": [
                    {"source": "wiki/01_引言/README", "target": "wiki/01_引言/1.1_入口", "type": "CONTAINS"},
                    {"source": "wiki/01_引言/1.1_入口", "target": "wiki/01_引言/README", "type": "LINKS_TO"},
                ],
            }

            write_html(graph, output)
            text = output.read_text(encoding="utf-8")

            self.assertIn("径向章节簇布局", text)
            self.assertIn('["internalLinks", "章内双链"]', text)
            self.assertIn('["crossLinks", "跨章双链"]', text)

    def test_repository_graph_has_no_overlinked_wiki_hub(self):
        graph = build_wiki_graph(Path(__file__).resolve().parents[1] / "wiki")
        incoming_links = {}
        labels = {node["id"]: node["label"] for node in graph["nodes"]}
        for edge in graph["edges"]:
            if edge["type"] == "LINKS_TO" and edge["target"].startswith("wiki/"):
                incoming_links[edge["target"]] = incoming_links.get(edge["target"], 0) + 1
        worst_id, worst_count = max(incoming_links.items(), key=lambda item: item[1])

        self.assertLessEqual(worst_count, 12, f"{labels.get(worst_id, worst_id)} has too many ordinary wiki links")


if __name__ == "__main__":
    unittest.main()
