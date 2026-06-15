import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.build_graph_from_wiki import build_wiki_graph, write_mermaid


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


if __name__ == "__main__":
    unittest.main()
