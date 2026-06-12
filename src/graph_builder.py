import argparse
import csv
import json
from pathlib import Path


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
    parser = argparse.ArgumentParser(
        description="Build a knowledge graph JSON file from entity and relation CSV files."
    )
    parser.add_argument("--entities", default="data/raw/entities.csv")
    parser.add_argument("--relations", default="data/raw/relations.csv")
    parser.add_argument("--output", default="data/processed/knowledge_graph.json")
    args = parser.parse_args()

    build_graph(args.entities, args.relations, args.output)


if __name__ == "__main__":
    main()
