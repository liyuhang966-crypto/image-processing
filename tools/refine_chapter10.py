"""Refine chapter 10 image compression wiki, graph semantics and docs."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "wiki" / "10_图像压缩编码"
EX = ROOT / "examples" / "10_image_compression"
PDF = "raw/books/数字图像处理基础_朱虹.pdf"
PDF_PAGE_NEEDS_REVIEW = 195


FILES = [
    ("10.1_图像冗余的概念.md", "10.1 图像冗余的概念", "ch10_compression_pipeline.png", None, "图像压缩利用图像数据中的冗余：相邻像素相似、符号概率不均、视觉系统对某些误差不敏感。压缩编码的本质是用更少比特表达足够有用的信息。", "\\(CR=n_1/n_2\\)，压缩比定义需按原书复核。", "冗余分析 vs 编码算法：前者解释为什么能压缩，后者实现如何压缩。"),
    ("10.1.1_冗余的概念.md", "10.1.1 冗余的概念", "ch10_compression_pipeline.png", None, "冗余指数据中可预测、重复或对最终任务不重要的部分。消除冗余可以无损，也可以在允许失真的情况下有损。", "\\(R=1-1/CR\\) 可表示相对冗余，符号需人工复核。", "无损冗余 vs 有损冗余：无损删除可恢复冗余，有损删除感知不敏感信息。"),
    ("10.1.2_图像中的冗余.md", "10.1.2 图像中的冗余", "ch10_compression_pipeline.png", None, "图像常见冗余包括空间冗余、编码冗余、心理视觉冗余和频域/变换域冗余。不同冗余对应不同压缩策略。", "空间相关性可抽象为：\\(f(x,y)\\approx f(x+1,y)\\)。", "空间冗余 vs 编码冗余：前者来自像素相关性，后者来自码字长度不匹配概率。"),
    ("10.2_图像无损压缩编码.md", "10.2 图像无损压缩编码", "ch10_rle_runs.png", "rle_encoding.py", "无损压缩要求解码后与原图完全一致，常用于文档、医学、标签图和中间数据。RLE 和 Huffman 是经典基础方法。", "\\(D(E(f))=f\\)。", "无损 vs 有损：无损保真但压缩率有限，有损压缩率高但引入失真。"),
    ("10.2.1_行程编码（RLE）.md", "10.2.1 行程编码（RLE）", "ch10_rle_runs.png", "rle_encoding.py", "RLE 将连续相同值编码为“值 + 长度”。它适合大块平坦区域或二值图，遇到纹理/噪声多的图像时压缩效果差。", "序列 \\([a,a,a,b,b]\\) 可编码为 \\((a,3),(b,2)\\)。", "RLE vs Huffman：RLE 利用连续重复，Huffman 利用符号概率不均。"),
    ("10.2.2_哈夫曼（Huffman）编码.md", "10.2.2 哈夫曼（Huffman）编码", "ch10_huffman_tree.png", "huffman_encoding_demo.py", "Huffman 编码给高概率符号分配短码、低概率符号分配长码，减少平均码长。它是前缀码，可无歧义解码。", "\\(L=\\sum_i p_i l_i\\)，目标是降低平均码长。", "Huffman vs 固定长度编码：固定长度不考虑概率，Huffman 按概率分配码长。"),
    ("10.3_图像有损压缩编码.md", "10.3 图像有损压缩编码", "ch10_lossy_quantization.png", "jpeg_idea_demo.py", "有损压缩允许一定失真，用量化、下采样或系数截断换取更高压缩率。关键是让失真尽量落在人眼不敏感的部分。", "\\(\\hat{c}=round(c/Q)Q\\)。", "有损 vs 增强：有损压缩为省比特允许误差，增强为改善视觉效果调整图像。"),
    ("10.3.1_彩色图像的有损编码.md", "10.3.1 彩色图像的有损编码", "ch10_lossy_quantization.png", "jpeg_idea_demo.py", "彩色有损编码常利用人眼对亮度更敏感、对色度相对不敏感的特点，将亮度和色度分开处理，并对色度更强压缩。", "可抽象为：\\(RGB\\rightarrow YCbCr\\rightarrow\\) 色度下采样/量化。", "彩色有损编码 vs 白平衡：前者压缩表示，后者校正色偏。"),
    ("10.3.2_小波变换编码.md", "10.3.2 小波变换编码", "ch10_wavelet_compression.png", "wavelet_compression_demo.py", "小波变换编码把图像分解为多尺度子带，保留重要系数并量化/编码其余系数，适合渐进式和多分辨率压缩思想。", "保留 \\(|c|>T\\) 的小波系数可形成稀疏表示。", "小波编码 vs JPEG 思路：二者都变换后量化，小波更强调多尺度表示。"),
    ("10.x_习题.md", "10.x 习题", "ch10_wavelet_compression.png", None, "本章习题应围绕冗余来源、无损/有损取舍、RLE/Huffman/JPEG/小波编码适用条件展开。", "复习重点：压缩比、冗余、平均码长、量化误差、小波系数稀疏性。", "方法选择应看是否允许失真、图像是否重复、符号概率是否不均。"),
]


def render(item: tuple[str, str, str, str | None, str, str, str]) -> str:
    file, title, figure, code, concept, formula, compare = item
    code_line = "本节偏复习整合，无单独代码；可结合本章其他示例运行。" if code is None else f"[{code}](../../examples/10_image_compression/{code})"
    return f"""# {title}

> [!note] 书中对应页
> PDF 页码：{PDF_PAGE_NEEDS_REVIEW}
> 打开原页（Obsidian）：[[{PDF}#page={PDF_PAGE_NEEDS_REVIEW}]]
>
> GitHub 公开仓库不随附原书 PDF；下载仓库后，将有权使用的同名 PDF 放入 `raw/books/`，下面的 Obsidian 本地内嵌预览才会显示。
> ![[{PDF}#page={PDF_PAGE_NEEDS_REVIEW}]]

## 来源与状态

- 书名：数字图像处理基础
- 作者：朱虹
- 章节：第 10 章 图像压缩编码
- 小节：{title}
- 书中页码：需人工复核
- PDF 页码：需人工复核
- 本地 PDF：{PDF}
- 处理状态：已精修 / 需人工复核

## 核心概念

{concept}

## 关键公式

- {formula}
- 公式符号、比特计数和码字约定需对照原书人工复核。

## 算法步骤

1. 分析图像中的冗余或可容忍失真。
2. 选择无损编码或有损编码策略。
3. 对像素、符号或变换系数进行预测、变换、量化或熵编码。
4. 记录压缩率、失真和可逆性。
5. 解码或重构图像并检查质量。

## 直观理解

压缩是在问“哪些信息必须精确保存，哪些信息可以更短地写，哪些误差可以接受”。

## 使用场景

文档和标签图无损存储、照片有损压缩、传输带宽受限的图像编码、渐进式图像浏览。

## 优点

- 能显著降低存储和传输成本。
- 可按任务选择无损或有损方案。

## 局限性

- 有损压缩会引入不可逆失真。
- 无损压缩率受图像冗余程度限制。

## 和相关方法的对比

- {compare}

## 教学图示

![{title}](../../assets/extracted_figures/{figure})

## 对应代码

{code_line}

## 相关知识

- [[09_图像变换/9.3.1_应用于图像压缩|小波压缩]]
- [[08_彩色图像处理/8.2_表色系|表色系]]
- [[07_二值图像处理/7.4_贴标签|贴标签]]

## 复习问题

1. 本节方法利用了哪一种冗余？
2. 它是无损还是有损？为什么？
3. 什么图像条件下该方法压缩效果会变差？
"""


def refine_wiki() -> None:
    WIKI.mkdir(parents=True, exist_ok=True)
    for item in FILES:
        (WIKI / item[0]).write_text(render(item), encoding="utf-8")
    (WIKI / "README.md").write_text("# 第 10 章 图像压缩编码\n\n本章已升级为精品样板章节，覆盖冗余、RLE、Huffman、有损编码和彩色/小波压缩思想。\n", encoding="utf-8")


def add_semantic_edges() -> None:
    path = ROOT / "graph" / "semantic_edges.json"
    data = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"nodes": [], "edges": []}
    nodes = {node["id"]: node for node in data.get("nodes", [])}
    edges = {(edge["source"], edge["target"], edge["type"]) for edge in data.get("edges", [])}
    def node(i: str, label: str, kind: str = "concept") -> None:
        nodes[i] = {"id": i, "label": label, "kind": kind}
    def edge(s: str, t: str, r: str) -> None:
        edges.add((s, t, r))
    for file, title, *_ in FILES:
        node(f"wiki/10_图像压缩编码/{file}", title)
    for code in ["rle_encoding.py", "huffman_encoding_demo.py", "jpeg_idea_demo.py", "wavelet_compression_demo.py"]:
        node(f"examples/10_image_compression/{code}", code, "code")
    for formula in ["压缩比", "平均码长", "量化公式", "小波稀疏系数"]:
        node(f"formula/ch10/{formula}", formula, "formula")
    edge("wiki/10_图像压缩编码/10.2_图像无损压缩编码.md", "wiki/10_图像压缩编码/10.1_图像冗余的概念.md", "PREREQUISITE")
    edge("wiki/10_图像压缩编码/10.3_图像有损压缩编码.md", "wiki/10_图像压缩编码/10.1_图像冗余的概念.md", "PREREQUISITE")
    edge("wiki/10_图像压缩编码/10.2.1_行程编码（RLE）.md", "wiki/10_图像压缩编码/10.2.2_哈夫曼（Huffman）编码.md", "COMPARES_WITH")
    edge("wiki/10_图像压缩编码/10.3.2_小波变换编码.md", "wiki/09_图像变换/9.3.1_应用于图像压缩.md", "PREREQUISITE")
    for wiki, formula in [("10.1_图像冗余的概念.md", "压缩比"), ("10.2.2_哈夫曼（Huffman）编码.md", "平均码长"), ("10.3_图像有损压缩编码.md", "量化公式"), ("10.3.2_小波变换编码.md", "小波稀疏系数")]:
        edge(f"wiki/10_图像压缩编码/{wiki}", f"formula/ch10/{formula}", "USES_FORMULA")
    for wiki, code in [("10.2.1_行程编码（RLE）.md", "rle_encoding.py"), ("10.2.2_哈夫曼（Huffman）编码.md", "huffman_encoding_demo.py"), ("10.3_图像有损压缩编码.md", "jpeg_idea_demo.py"), ("10.3.2_小波变换编码.md", "wavelet_compression_demo.py")]:
        edge(f"wiki/10_图像压缩编码/{wiki}", f"examples/10_image_compression/{code}", "IMPLEMENTED_BY")
    edge("wiki/10_图像压缩编码/10.3_图像有损压缩编码.md", "wiki/08_彩色图像处理/8.2_表色系.md", "APPLIES_TO")
    data = {"nodes": sorted(nodes.values(), key=lambda x: x["id"]), "edges": [{"source": s, "target": t, "type": r} for s, t, r in sorted(edges)]}
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_docs() -> None:
    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    text = text.replace("- 第 10 章到第 11 章仍在同一分支继续精修，当前不拆分独立分支，避免后续配置分散。", "- 第 10 章“图像压缩编码”已升级为精品样板，包含原创图示、独立代码示例和语义图谱关系。\n- 第 11 章仍在同一分支继续精修，当前不拆分独立分支，避免后续配置分散。")
    if "第 10 章图像压缩编码示例：" not in text:
        marker = "默认输入为 `assets/sample_images/` 中的合成图片，输出写入 `examples/output/`，该目录已被 `.gitignore` 忽略。"
        block = """第 10 章图像压缩编码示例：

```powershell
python examples/10_image_compression/rle_encoding.py --threshold 128
python examples/10_image_compression/huffman_encoding_demo.py
python examples/10_image_compression/jpeg_idea_demo.py --quality 24
python examples/10_image_compression/wavelet_compression_demo.py --keep-ratio 0.15
```

"""
        text = text.replace(marker, block + marker)
    readme.write_text(text, encoding="utf-8")
    coverage = ROOT / "coverage_report.md"
    ctext = coverage.read_text(encoding="utf-8")
    ctext = ctext.replace("- 第 10 章到第 11 章：仍在同一分支继续精修，后续按第 2/3/4/5/6/7/8/9 章样板逐章推进。", "- 第 10 章：已精修为第九个精品样板，新增原创压缩图示、独立可运行示例和语义图谱关系。\n- 第 11 章：仍在同一分支继续精修，后续按第 2/3/4/5/6/7/8/9/10 章样板推进。")
    if "## 第 10 章处理记录" not in ctext:
        ctext += "\n\n## 第 10 章处理记录\n\n- 处理的 wiki 文件：第 10 章全部 10 个小节。\n- 新增原创教学图示：`ch10_compression_pipeline.png`、`ch10_rle_runs.png`、`ch10_huffman_tree.png`、`ch10_lossy_quantization.png`、`ch10_wavelet_compression.png`。\n- 优化代码：`rle_encoding.py`、`huffman_encoding_demo.py`、`jpeg_idea_demo.py`、`wavelet_compression_demo.py`，并新增第 10 章 `_utils.py`。\n- 新增图谱关系：无损/有损压缩的 `PREREQUISITE`，RLE/Huffman 的 `COMPARES_WITH`，小波编码依赖图像变换的关系，公式依赖和代码实现关系。\n- 仍需人工复核：原书页码、压缩比定义、码字约定、JPEG 量化表和小波编码细节。\n- 未完成内容：未加入原书截图和原始文本；后续可加入真实比特流和 PSNR/SSIM 指标。\n"
    coverage.write_text(ctext, encoding="utf-8")
    (EX / "README.md").write_text("# 第 10 章 图像压缩编码代码示例\n\n这些脚本默认使用 `assets/sample_images/sample_gray.png`，输出写入 `examples/output/`。\n", encoding="utf-8")


def main() -> None:
    refine_wiki()
    add_semantic_edges()
    update_docs()
    print("Refined chapter 10 image compression content.")


if __name__ == "__main__":
    main()
