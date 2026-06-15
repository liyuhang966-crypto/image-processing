# 知识图谱

`wiki/` 的 Obsidian 链接是当前知识图谱主数据源。第 3 章到第 11 章的额外语义关系维护在 `graph/semantic_edges.json`。

运行：

```powershell
python tools/build_graph_from_wiki.py
```

会同步生成：

- `graph/knowledge_graph.json`
- `graph/mermaid_graph.md`
- `graph/knowledge_graph.html`

当前图谱包含基础关系：

- `CONTAINS`
- `LINKS_TO`

以及精品章节扩展语义关系：

- `PREREQUISITE`
- `COMPARES_WITH`
- `GENERALIZES`
- `IMPLEMENTED_BY`
- `USES_FORMULA`
- `IMPROVES_OR_EXTENDS`
- `APPLIES_TO`

`data/raw/entities.csv` 和 `data/raw/relations.csv` 仅保留为 starter 示例，不再作为公开图谱的主来源。
