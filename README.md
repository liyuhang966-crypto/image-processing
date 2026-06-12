# Image Processing Knowledge Graph

This repository contains a small Python starter for building a knowledge graph
from CSV files.

## Structure

- `data/raw/entities.csv`: graph nodes with `id`, `label`, and `type`.
- `data/raw/relations.csv`: graph edges with `source`, `target`, `type`, and `description`.
- `src/graph_builder.py`: converts the CSV files into JSON.
- `tests/`: regression tests for the graph builder.

## Run

```powershell
python src/graph_builder.py
```

The generated graph is written to:

```text
data/processed/knowledge_graph.json
```

## Test

```powershell
python -m unittest discover -s tests
```
