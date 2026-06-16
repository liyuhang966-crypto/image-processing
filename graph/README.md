# 知识图谱数据说明

本项目的主知识图谱入口已经切换为 Obsidian Canvas：

- `数字图像处理知识图谱.canvas`
- `数字图像处理跨章关系.canvas`
- `wiki/*/*.canvas`

`graph/` 目录只保留机器可读数据和轻量文档，不再生成 HTML 图谱。

## 保留文件

- `graph/knowledge_graph.json`：从 `wiki/` 双链和 `graph/semantic_edges.json` 合成的机器可读图谱。
- `graph/semantic_edges.json`：人工维护的强语义关系。
- `graph/mermaid_graph.md`：轻量 Mermaid 文档，用于快速查看章节包含关系和强语义关系。

## 已废弃内容

HTML 图谱已废弃，不再作为入口，也不再由脚本生成。`graph/*.html` 已加入 `.gitignore`，避免后续误提交。

如果需要固定章节分区、课程地图式浏览，请打开 Obsidian Canvas；如果只需要轻量关系数据，请使用 JSON 或 Mermaid。

## 重新生成

```powershell
python tools/build_graph_from_wiki.py
```

该命令只生成：

- `graph/knowledge_graph.json`
- `graph/mermaid_graph.md`

不会生成任何 `.html` 文件。
