import csv
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from build_graph_from_wiki import main as build_wiki_graph_files


def read_csv_rows(path):
    with Path(path).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def build_graph(entities_path, relations_path, output_path):
    nodes = read_csv_rows(entities_path)
    edges = read_csv_rows(relations_path)
    graph = {"nodes": nodes, "edges": edges}

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(graph, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return graph


def main():
    build_wiki_graph_files()


if __name__ == "__main__":
    main()
