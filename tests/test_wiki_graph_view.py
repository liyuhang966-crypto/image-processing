import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.build_graph_from_wiki import build_wiki_graph, write_html, write_mermaid
from tools.clustered_graph_layout import build_clustered_layout, write_clustered_graph_suite


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

    def test_default_html_keeps_legacy_radial_controls(self):
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

    def test_clustered_layout_precomputes_fixed_chapter_islands(self):
        graph = build_wiki_graph(Path(__file__).resolve().parents[1] / "wiki")
        layout = build_clustered_layout(graph)

        self.assertEqual(len(layout["chapters"]), 11)
        for number, chapter in enumerate(layout["chapters"], start=1):
            self.assertEqual(chapter["number"], number)
            self.assertTrue(chapter["id"].startswith(f"wiki/{number:02d}_"))
            self.assertTrue(chapter["id"].endswith("/README"))

        for node in layout["nodes"]:
            for field in ("id", "label", "chapter", "level", "type", "path", "x", "y", "radius", "angle", "fixed"):
                self.assertIn(field, node)
            self.assertTrue(node["fixed"])
            self.assertTrue(node["fixedPosition"])
            self.assertFalse(node["physics"])
            self.assertIn("chapterNumber", node)
            self.assertIn("importance", node)

        centers = {chapter["number"]: (chapter["x"], chapter["y"], chapter["radius"]) for chapter in layout["chapters"]}
        min_distance = min(
            ((ax - bx) ** 2 + (ay - by) ** 2) ** 0.5
            for a, (ax, ay, _) in centers.items()
            for b, (bx, by, _) in centers.items()
            if a < b
        )
        self.assertGreater(min_distance, 900)

        boxes = []
        for chapter in layout["chapters"]:
            radius = chapter["radius"]
            boxes.append((chapter["number"], chapter["x"] - radius, chapter["y"] - radius, chapter["x"] + radius, chapter["y"] + radius))
        for left_index, left in enumerate(boxes):
            for right in boxes[left_index + 1 :]:
                overlap = not (left[3] <= right[1] or right[3] <= left[1] or left[4] <= right[2] or right[4] <= left[2])
                self.assertFalse(overlap, f"chapter boxes overlap: {left[0]} and {right[0]}")

        for node in layout["nodes"]:
            chapter_number = node.get("chapterNumber")
            if not chapter_number or node["level"] == "chapter":
                continue
            cx, cy, radius = centers[chapter_number]
            distance = ((node["x"] - cx) ** 2 + (node["y"] - cy) ** 2) ** 0.5
            self.assertLessEqual(distance, radius)
            if node["label"].startswith(("3.", "9.", "10.", "11.")):
                self.assertEqual(chapter_number, int(node["label"].split(".", 1)[0]))

        nav_paths = {node.get("path") for node in layout["nodes"]}
        self.assertNotIn("README.md", nav_paths)
        self.assertNotIn("index.md", nav_paths)
        self.assertNotIn("coverage_report.md", nav_paths)
        self.assertNotIn("graph/README.md", nav_paths)
        self.assertNotIn("wiki/00_导航.md", nav_paths)
        self.assertNotIn("wiki/99_术语表.md", nav_paths)

        for edge in layout["edges"]:
            if edge["type"] == "LINKS_TO" and edge.get("isCrossChapter"):
                self.assertFalse(edge["visibleByDefault"])
            self.assertFalse(edge["layoutInfluence"])

    def test_clustered_graph_suite_writes_all_recommended_views(self):
        graph = build_wiki_graph(Path(__file__).resolve().parents[1] / "wiki")
        with TemporaryDirectory() as workspace:
            output_dir = Path(workspace)
            write_clustered_graph_suite(graph, output_dir)

            expected = {
                "clustered_knowledge_graph.json",
                "clustered_knowledge_graph.html",
                "chapter_overview.html",
                "repo_navigation_graph.html",
                *{f"chapter_{number:02d}_graph.html" for number in range(1, 12)},
            }
            actual = {path.name for path in output_dir.iterdir()}
            self.assertTrue(expected.issubset(actual))

            main_html = (output_dir / "clustered_knowledge_graph.html").read_text(encoding="utf-8")
            self.assertIn("固定章节分区布局", main_html)
            self.assertIn("显示跨章边", main_html)
            self.assertIn("只看跨章主干关系", main_html)
            self.assertIn('<option value="chapters">只显示章节标签</option>', main_html)
            self.assertNotIn("d3.force", main_html)
            self.assertNotIn("vis-network", main_html)


if __name__ == "__main__":
    unittest.main()
