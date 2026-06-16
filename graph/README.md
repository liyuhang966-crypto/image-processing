# 知识图谱视图说明

`wiki/` 中的 Obsidian 双链是知识图谱主数据源，`graph/semantic_edges.json` 补充人工维护的语义关系。运行：

```powershell
python tools/build_graph_from_wiki.py
```

会同步生成机器数据、Mermaid 视图和 HTML 可视化。

## 推荐打开

优先打开：

- `graph/clustered_knowledge_graph.html`：主推荐图。使用固定章节分区布局，每一章是一个独立圆形星团；节点坐标由本章中心、节点层级和目录顺序决定，不使用自由力导向。
- `graph/chapter_overview.html`：只看 11 个章节节点和少量跨章强语义关系。
- `graph/chapter_01_graph.html` 到 `graph/chapter_11_graph.html`：每章一个局部图，只显示本章节点和章内关系。
- `graph/repo_navigation_graph.html`：单独展示 `README`、`index`、`coverage_report`、导航、术语表等仓库维护节点，避免干扰主知识图。

`graph/knowledge_graph.html` 保留为旧版全量浏览图，不再推荐作为主要学习入口。它更接近普通网络图，节点多时容易出现章节混杂和标签重叠。

## 固定岛屿布局

`graph/clustered_knowledge_graph.json` 中每个节点都包含：

- `chapterNumber`
- `level`
- `type`
- `path`
- `x`
- `y`
- `radius`
- `angle`
- `fixed: true`
- `physics: false`

第 1 章到第 11 章各有固定中心点和独立边界。跨章边只作为可开关的视觉线条绘制，不参与坐标计算。

## 生成文件

- `graph/knowledge_graph.json`：完整机器可读图谱，保留精简后的 `LINKS_TO` 和语义关系。
- `graph/clustered_knowledge_graph.json`：章节固定分区布局数据。
- `graph/mermaid_graph.md`：面向阅读的清爽视图，只展示章节包含关系和语义关系。
- `graph/clustered_knowledge_graph.html`：主推荐 HTML 图谱。
- `graph/chapter_overview.html`：章节总览图。
- `graph/chapter_01_graph.html` 到 `graph/chapter_11_graph.html`：章节局部图。
- `graph/repo_navigation_graph.html`：仓库导航图。

## 关系类型

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

主图默认显示章内 `CONTAINS` 和章内语义关系，默认隐藏普通跨章 `LINKS_TO`。需要查看跨章知识迁移时，可以打开“显示跨章边”，并切换关系过滤。

## 交互建议

- 先用 `clustered_knowledge_graph.html` 看全局章节岛屿分布。
- 默认只显示章节标签，避免小节文字遮挡。
- 点击某个章节节点后，会切换到该章并显示该章内部标签。
- 复习单章时也可以直接打开对应的 `chapter_XX_graph.html`。
- 需要调试维护文件时，再打开 `repo_navigation_graph.html`。

## Obsidian 图谱

Obsidian 自带 Graph View 会扫描整个 vault；如果不过滤，会把 `README`、`coverage_report`、`AGENTS`、`graph/`、`tools/` 等维护文件也当成节点。首次打开或图谱变乱时，运行：

```powershell
python tools/configure_obsidian_graph.py
```

该命令会更新本地 `.obsidian/graph.json`，只显示 `wiki/` 中的学习笔记，并隐藏章节 README、导航、术语表、未解析节点和本站维护节点。`.obsidian/` 是本地配置目录，按项目规则不提交到公开仓库。

`data/raw/entities.csv` 和 `data/raw/relations.csv` 仅保留为 starter 示例，不再作为公开图谱的主数据源。
