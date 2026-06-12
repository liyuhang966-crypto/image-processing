import csv
import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from graph_builder import build_graph


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


class GraphBuilderTest(unittest.TestCase):
    def test_build_graph_from_entity_and_relation_csv(self):
        with TemporaryDirectory() as workspace:
            tmp_path = Path(workspace)
            entities = tmp_path / "entities.csv"
            relations = tmp_path / "relations.csv"
            output = tmp_path / "graph.json"

            write_csv(
                entities,
                [
                    {"id": "python", "label": "Python", "type": "Technology"},
                    {"id": "opencv", "label": "OpenCV", "type": "Library"},
                ],
            )
            write_csv(
                relations,
                [
                    {
                        "source": "opencv",
                        "target": "python",
                        "type": "BUILDS_ON",
                        "description": "OpenCV can be used from Python.",
                    }
                ],
            )

            graph = build_graph(entities, relations, output)

            self.assertEqual(
                graph,
                {
                    "nodes": [
                        {"id": "python", "label": "Python", "type": "Technology"},
                        {"id": "opencv", "label": "OpenCV", "type": "Library"},
                    ],
                    "edges": [
                        {
                            "source": "opencv",
                            "target": "python",
                            "type": "BUILDS_ON",
                            "description": "OpenCV can be used from Python.",
                        }
                    ],
                },
            )
            self.assertEqual(json.loads(output.read_text(encoding="utf-8")), graph)


if __name__ == "__main__":
    unittest.main()
