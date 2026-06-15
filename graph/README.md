# 知识图谱

`wiki/` 的 Obsidian 双链是知识图谱主数据源，`graph/semantic_edges.json` 补充人工维护的语义关系。

运行：

```powershell
python tools/build_graph_from_wiki.py
```

会同步生成：

- `graph/knowledge_graph.json`：完整机器可读图谱，保留精简后的 `LINKS_TO` 和语义关系。
- `graph/mermaid_graph.md`：面向阅读的清爽视图，只展示章节包含关系和语义关系。
- `graph/knowledge_graph.html`：按章节浏览节点的轻量 HTML。

当前图谱关系包括：

- `CONTAINS`
- `LINKS_TO`
- `PREREQUISITE`
- `COMPARES_WITH`
- `GENERALIZES`
- `IMPLEMENTED_BY`
- `USES_FORMULA`
- `IMPROVES_OR_EXTENDS`
- `APPLIES_TO`

## Obsidian 图谱

Obsidian 自带 Graph View 会扫描整个 vault，如果不过滤，会把 `README`、`coverage_report`、`AGENTS`、`graph/`、`tools/` 等维护文件也当成节点。首次打开或图谱变乱时，运行：

```powershell
python tools/configure_obsidian_graph.py
```

该命令会更新本地 `.obsidian/graph.json`，只显示 `wiki/` 中的学习笔记，并隐藏章节 README、导航、术语表、未解析节点和孤立维护节点。`.obsidian/` 是本地配置目录，按项目规则不提交到公开仓库。

`data/raw/entities.csv` 和 `data/raw/relations.csv` 仅保留为 starter 示例，不再作为公开图谱的主数据源。
