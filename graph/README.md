# 知识图谱

`wiki/` 的 Obsidian 链接是当前知识图谱主数据源。运行：

```powershell
python tools/build_graph_from_wiki.py
```

会同步生成：

- `graph/knowledge_graph.json`
- `graph/mermaid_graph.md`
- `graph/knowledge_graph.html`

`data/raw/entities.csv` 和 `data/raw/relations.csv` 仅保留为 starter 示例，不再作为公开图谱的主来源。
