"""Refine chapter 7 binary image processing wiki, graph semantics and docs."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "wiki" / "07_二值图像处理"
EX = ROOT / "examples" / "07_binary_image_processing"
PDF = "raw/books/数字图像处理基础_朱虹.pdf"
PDF_PAGE_NEEDS_REVIEW = 130


BASE = {
    "concept": "二值图像处理把像素简化为前景和背景后，重点研究连通性、形状、边界和骨架。它通常接在图像分割之后，用来清理区域、提取结构和统计目标特征。",
    "formula": ["二值图像可写为：\\(B(x,y)\\in\\{0,1\\}\\)。", "集合形式常把前景看成点集 \\(A\\)，结构元素看成点集 \\(S\\)。"],
    "steps": ["输入二值图像。", "确定前景、背景和邻接规则。", "按结构元素或连通性规则处理前景点集。", "输出清理后的二值图、标签图或骨架图。"],
    "intuition": "二值处理像在黑白剪影上做几何操作：有时收缩、有时扩张、有时编号、有时抽出中心线。",
    "scene": "文档处理、目标计数、缺陷检测、OCR 前处理、医学区域测量。",
    "pros": ["计算快，结果清晰。", "适合做形状统计和后处理。"],
    "limits": ["强依赖分割质量。", "结构元素和连通规则选错会改变拓扑。"],
}


PROFILES = [
    ("7.1_二值图像中的基本概念.md", "7.1 二值图像中的基本概念", "ch07_connectivity.png", None, "二值图像的核心是前景/背景、邻域、连通性和目标几何属性。4 邻域更严格，8 邻域更容易把斜向接触的点连成同一区域。", ["4 邻域：\\(N_4(p)=\\{上,下,左,右\\}\\)。", "8 邻域：\\(N_8(p)=N_4(p)\\cup\\{四个对角点\\}\\)。"], "二值概念 vs 阈值分割：阈值分割产生二值图，二值处理进一步分析其结构。", "为什么 4 邻域和 8 邻域会影响连通域数量？"),
    ("7.1.1_连接与点特性.md", "7.1.1 连接与点特性", "ch07_connectivity.png", None, "连接性决定哪些前景点属于同一目标。点特性关注端点、连接点、孤立点和边界点，是细线化和目标分析的基础。", ["若两点之间存在由邻接前景点组成的路径，则两点连通。"], "连接与点特性 vs 连通域标记：前者定义规则，后者按规则给区域编号。", "端点和分叉点在骨架分析中有什么意义？"),
    ("7.1.2_几何特征.md", "7.1.2 几何特征", "ch07_component_labeling.png", "connected_component_labeling.py", "几何特征把二值目标转化为面积、周长、外接矩形、质心等可计算指标，便于分类、筛选和测量。", ["面积：\\(A=\\sum B(x,y)\\)。", "质心：\\((\\bar{x},\\bar{y})=(\\sum xB/A,\\sum yB/A)\\)。"], "几何特征 vs 灰度特征：几何特征描述形状，灰度特征描述强度分布。", "面积、质心和外接矩形分别适合回答什么问题？"),
    ("7.2_腐蚀与膨胀.md", "7.2 腐蚀与膨胀", "ch07_morphology_erosion_dilation.png", "erosion_dilation.py", "腐蚀和膨胀是二值形态学的基本操作。腐蚀让前景收缩、断开细连接；膨胀让前景扩张、填补小间隙。", ["腐蚀：\\(A\\ominus S=\\{z|(S)_z\\subseteq A\\}\\)。", "膨胀：\\(A\\oplus S=\\{z|(\\hat{S})_z\\cap A\\ne\\varnothing\\}\\)。"], "腐蚀 vs 膨胀：一个收缩前景，一个扩张前景。", "结构元素大小如何影响腐蚀和膨胀结果？"),
    ("7.2.1_腐蚀.md", "7.2.1 腐蚀", "ch07_morphology_erosion_dilation.png", "erosion_dilation.py", "腐蚀要求结构元素完全落在前景内部，只有满足条件的位置保留前景，因此可去除小突起、细线和孤立噪点。", ["\\(A\\ominus S\\) 表示所有能完整容纳结构元素的位置集合。"], "腐蚀 vs 开运算：腐蚀单独会缩小目标，开运算再膨胀以尽量恢复主体大小。", "腐蚀为什么会断开细桥？"),
    ("7.2.2_膨胀.md", "7.2.2 膨胀", "ch07_morphology_erosion_dilation.png", "erosion_dilation.py", "膨胀只要结构元素与前景相交就把对应位置纳入前景，因此可填补小裂缝、连接近邻目标并扩大边界。", ["\\(A\\oplus S\\) 表示前景与结构元素平移后相交的位置集合。"], "膨胀 vs 闭运算：膨胀单独会扩大目标，闭运算再腐蚀以尽量恢复主体大小。", "膨胀为什么可能把相邻目标粘连？"),
    ("7.3_开运算与闭运算.md", "7.3 开运算与闭运算", "ch07_opening_closing.png", "opening_closing.py", "开运算和闭运算是腐蚀/膨胀的组合。开运算先腐蚀后膨胀，偏向去除小前景噪声；闭运算先膨胀后腐蚀，偏向填补小孔和裂缝。", ["开运算：\\(A\\circ S=(A\\ominus S)\\oplus S\\)。", "闭运算：\\(A\\bullet S=(A\\oplus S)\\ominus S\\)。"], "开运算 vs 闭运算：开去小白点，闭补小黑洞。", "为什么开闭运算比单独腐蚀/膨胀更常用于后处理？"),
    ("7.3.1_开运算.md", "7.3.1 开运算", "ch07_opening_closing.png", "opening_closing.py", "开运算先删除放不下结构元素的小前景，再恢复主体尺寸，适合去除小噪声和断开窄连接。", ["\\(A\\circ S=(A\\ominus S)\\oplus S\\)。"], "开运算 vs 腐蚀：开运算会部分恢复主体，腐蚀不会。", "开运算为什么能去除小前景噪点？"),
    ("7.3.2_闭运算.md", "7.3.2 闭运算", "ch07_opening_closing.png", "opening_closing.py", "闭运算先扩张目标再收缩回来，适合填充小孔、连接窄裂缝并平滑边界内凹。", ["\\(A\\bullet S=(A\\oplus S)\\ominus S\\)。"], "闭运算 vs 膨胀：闭运算会尽量保持主体外形，膨胀会持续扩大。", "闭运算适合修复什么类型的缺陷？"),
    ("7.4_贴标签.md", "7.4 贴标签", "ch07_component_labeling.png", "connected_component_labeling.py", "贴标签把每个连通目标赋予唯一编号，是目标计数、面积统计和后续筛选的前提。", ["标签图：\\(L(x,y)=k\\) 表示像素属于第 \\(k\\) 个连通区域。"], "连通域标签 vs 轮廓标签：前者标内部区域，后者标外部边界。", "贴标签为什么通常在形态学清理之后进行？"),
    ("7.4.1_连通域标签法.md", "7.4.1 连通域标签法", "ch07_component_labeling.png", "connected_component_labeling.py", "连通域标签法按扫描和等价关系合并前景点，最终为每个连通区域分配编号。连通规则不同会改变标签数量。", ["若 \\(p\\) 与 \\(q\\) 连通，则 \\(L(p)=L(q)\\)。"], "4 连通 vs 8 连通：8 连通会把对角接触的区域合并。", "为什么连通域标记需要处理等价标签？"),
    ("7.4.2_轮廓标签法.md", "7.4.2 轮廓标签法", "ch07_component_labeling.png", "contour_labeling.py", "轮廓标签法关注目标边界而非全部内部像素，适合提取形状边界、计算周长和绘制外接框。", ["轮廓可理解为前景与背景相邻的边界点集合。"], "轮廓标签 vs 连通域标签：轮廓更轻量地描述边界，连通域保留区域内部。", "什么时候轮廓比完整连通域更有用？"),
    ("7.5_细线化方法.md", "7.5 细线化方法", "ch07_thinning.png", "thinning.py", "细线化把粗二值目标逐步削成一像素宽骨架，同时尽量保持连通性和拓扑结构。它常用于字符、道路、血管等线状目标分析。", ["细线化没有唯一公式，常用迭代删除满足拓扑保持条件的边界点。"], "细线化 vs 腐蚀：腐蚀可能破坏目标，细线化强调保持骨架连通。", "细线化为什么要避免删除端点和关键连接点？"),
    ("7.x_习题.md", "7.x 习题", "ch07_thinning.png", None, "本章习题应围绕邻接规则、结构元素、形态学组合、标签统计和骨架保持展开，重点是解释操作为何改变二值结构。", ["复习重点：4/8 邻域、腐蚀、膨胀、开闭运算、标签图、细线化。"], "形态学后处理 vs 分割：分割产生二值结果，形态学修正其结构。", "给定带小孔和小噪点的二值图，应如何组合开闭运算？"),
]


def render(item: tuple[str, str, str, str | None, str, list[str], str, str]) -> str:
    filename, title, figure, code, concept, formulas, compare, review = item
    code_line = "本节偏概念复习，无单独代码；可结合本章其他示例运行。" if code is None else f"[{code}](../../examples/07_binary_image_processing/{code})"
    steps = BASE["steps"]
    if code == "erosion_dilation.py":
        steps = ["输入二值图像。", "选择结构元素大小和形状。", "执行腐蚀或膨胀。", "观察目标收缩、扩张、断开或连接情况。"]
    elif code == "opening_closing.py":
        steps = ["输入二值图像。", "选择结构元素。", "按开运算或闭运算顺序组合腐蚀和膨胀。", "输出清理后的二值图。"]
    elif code == "connected_component_labeling.py":
        steps = ["输入二值图像。", "选择 4 连通或 8 连通。", "扫描前景并合并等价标签。", "输出标签图和区域统计。"]
    elif code == "contour_labeling.py":
        steps = ["输入二值图像。", "寻找前景外轮廓。", "过滤太小的轮廓。", "绘制轮廓编号和边界框。"]
    elif code == "thinning.py":
        steps = ["输入二值图像。", "反复检查边界点。", "删除不破坏连通性的可删点。", "直到骨架稳定。"]
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
- 章节：第 7 章 二值图像处理
- 小节：{title}
- 书中页码：需人工复核
- PDF 页码：需人工复核
- 本地 PDF：{PDF}
- 处理状态：已精修 / 需人工复核

## 核心概念

{concept}

## 关键公式

{chr(10).join(f"- {formula}" for formula in formulas)}

## 算法步骤

{chr(10).join(f"{index}. {step}" for index, step in enumerate(steps, 1))}

## 直观理解

{BASE["intuition"]}

## 使用场景

{BASE["scene"]}

## 优点

{chr(10).join(f"- {item}" for item in BASE["pros"])}

## 局限性

{chr(10).join(f"- {item}" for item in BASE["limits"])}

## 和相关方法的对比

- {compare}

## 教学图示

![{title}](../../assets/extracted_figures/{figure})

## 对应代码

{code_line}

## 相关知识

- [[06_图像的分割/6.1_阈值分割方法|阈值分割方法]]
- [[07_二值图像处理/7.2_腐蚀与膨胀|腐蚀与膨胀]]
- [[07_二值图像处理/7.4_贴标签|贴标签]]

## 复习问题

1. {review}
2. 本节操作会如何改变前景区域的面积或连通性？
3. 结构元素或邻接规则选错会带来什么后果？
"""


def refine_wiki() -> None:
    WIKI.mkdir(parents=True, exist_ok=True)
    for profile in PROFILES:
        (WIKI / profile[0]).write_text(render(profile), encoding="utf-8")
    (WIKI / "README.md").write_text(
        """# 第 7 章 二值图像处理

本章已升级为精品样板章节，重点整理二值图像基本概念、腐蚀、膨胀、开闭运算、贴标签和细线化。
""",
        encoding="utf-8",
    )


def add_semantic_edges() -> None:
    path = ROOT / "graph" / "semantic_edges.json"
    data = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"nodes": [], "edges": []}
    nodes = {node["id"]: node for node in data.get("nodes", [])}
    edges = {(edge["source"], edge["target"], edge["type"]) for edge in data.get("edges", [])}

    def node(node_id: str, label: str, kind: str = "concept") -> None:
        nodes[node_id] = {"id": node_id, "label": label, "kind": kind}

    def edge(source: str, target: str, relation: str) -> None:
        edges.add((source, target, relation))

    for file, title, *_ in PROFILES:
        node(f"wiki/07_二值图像处理/{file}", title)
    for code in ["erosion_dilation.py", "opening_closing.py", "connected_component_labeling.py", "contour_labeling.py", "thinning.py"]:
        node(f"examples/07_binary_image_processing/{code}", code, "code")
    for formula in ["4/8 邻域", "腐蚀公式", "膨胀公式", "开闭运算公式", "标签图", "细线化拓扑保持"]:
        node(f"formula/ch07/{formula}", formula, "formula")

    edge("wiki/07_二值图像处理/7.1_二值图像中的基本概念.md", "wiki/06_图像的分割/6.1_阈值分割方法.md", "PREREQUISITE")
    edge("wiki/07_二值图像处理/7.2_腐蚀与膨胀.md", "wiki/07_二值图像处理/7.1_二值图像中的基本概念.md", "PREREQUISITE")
    edge("wiki/07_二值图像处理/7.3_开运算与闭运算.md", "wiki/07_二值图像处理/7.2_腐蚀与膨胀.md", "IMPROVES_OR_EXTENDS")
    edge("wiki/07_二值图像处理/7.4_贴标签.md", "wiki/07_二值图像处理/7.1_二值图像中的基本概念.md", "PREREQUISITE")
    edge("wiki/07_二值图像处理/7.5_细线化方法.md", "wiki/07_二值图像处理/7.2_腐蚀与膨胀.md", "COMPARES_WITH")
    for child in ["7.2.1_腐蚀.md", "7.2.2_膨胀.md"]:
        edge(f"wiki/07_二值图像处理/{child}", "wiki/07_二值图像处理/7.2_腐蚀与膨胀.md", "GENERALIZES")
    for child in ["7.3.1_开运算.md", "7.3.2_闭运算.md"]:
        edge(f"wiki/07_二值图像处理/{child}", "wiki/07_二值图像处理/7.3_开运算与闭运算.md", "GENERALIZES")
    for child in ["7.4.1_连通域标签法.md", "7.4.2_轮廓标签法.md"]:
        edge(f"wiki/07_二值图像处理/{child}", "wiki/07_二值图像处理/7.4_贴标签.md", "GENERALIZES")
    for wiki, formula in [
        ("7.1_二值图像中的基本概念.md", "4/8 邻域"),
        ("7.2.1_腐蚀.md", "腐蚀公式"),
        ("7.2.2_膨胀.md", "膨胀公式"),
        ("7.3_开运算与闭运算.md", "开闭运算公式"),
        ("7.4_贴标签.md", "标签图"),
        ("7.5_细线化方法.md", "细线化拓扑保持"),
    ]:
        edge(f"wiki/07_二值图像处理/{wiki}", f"formula/ch07/{formula}", "USES_FORMULA")
    for wiki, code in [
        ("7.2_腐蚀与膨胀.md", "erosion_dilation.py"),
        ("7.3_开运算与闭运算.md", "opening_closing.py"),
        ("7.4.1_连通域标签法.md", "connected_component_labeling.py"),
        ("7.4.2_轮廓标签法.md", "contour_labeling.py"),
        ("7.5_细线化方法.md", "thinning.py"),
    ]:
        edge(f"wiki/07_二值图像处理/{wiki}", f"examples/07_binary_image_processing/{code}", "IMPLEMENTED_BY")
    edge("wiki/07_二值图像处理/7.4_贴标签.md", "wiki/08_彩色图像处理", "APPLIES_TO")

    data = {"nodes": sorted(nodes.values(), key=lambda x: x["id"]), "edges": [{"source": s, "target": t, "type": r} for s, t, r in sorted(edges)]}
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_docs() -> None:
    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    text = text.replace(
        "- 第 7 章到第 11 章仍在同一分支继续精修，当前不拆分独立分支，避免后续配置分散。",
        "- 第 7 章“二值图像处理”已升级为精品样板，包含原创图示、独立代码示例和语义图谱关系。\n- 第 8 章到第 11 章仍在同一分支继续精修，当前不拆分独立分支，避免后续配置分散。",
    )
    if "第 7 章二值图像处理示例：" not in text:
        marker = "默认输入为 `assets/sample_images/` 中的合成图片，输出写入 `examples/output/`，该目录已被 `.gitignore` 忽略。"
        block = """第 7 章二值图像处理示例：

```powershell
python examples/07_binary_image_processing/erosion_dilation.py --operation both --kernel-size 5
python examples/07_binary_image_processing/opening_closing.py --operation both --kernel-size 5
python examples/07_binary_image_processing/connected_component_labeling.py --connectivity 8
python examples/07_binary_image_processing/contour_labeling.py --min-area 30
python examples/07_binary_image_processing/thinning.py --max-iterations 80
```

"""
        text = text.replace(marker, block + marker)
    readme.write_text(text, encoding="utf-8")

    coverage = ROOT / "coverage_report.md"
    ctext = coverage.read_text(encoding="utf-8")
    ctext = ctext.replace(
        "- 第 7 章到第 11 章：仍在同一分支继续精修，后续按第 2/3/4/5/6 章样板逐章推进。",
        "- 第 7 章：已精修为第六个精品样板，新增原创二值处理图示、独立可运行示例和语义图谱关系。\n- 第 8 章到第 11 章：仍在同一分支继续精修，后续按第 2/3/4/5/6/7 章样板逐章推进。",
    )
    if "## 第 7 章处理记录" not in ctext:
        ctext += """

## 第 7 章处理记录

- 处理的 wiki 文件：第 7 章全部 14 个小节。
- 新增原创教学图示：`ch07_connectivity.png`、`ch07_morphology_erosion_dilation.png`、`ch07_opening_closing.png`、`ch07_component_labeling.png`、`ch07_thinning.png`。
- 优化代码：`erosion_dilation.py`、`opening_closing.py`、`connected_component_labeling.py`、`contour_labeling.py`、`thinning.py`，并新增第 7 章 `_utils.py`。
- 新增图谱关系：分割到二值处理的 `PREREQUISITE`，开闭运算对腐蚀膨胀的 `IMPROVES_OR_EXTENDS`，子方法归属的 `GENERALIZES`，公式依赖和代码实现关系。
- 仍需人工复核：原书页码、结构元素符号、贴标签扫描规则和细线化判据。
- 未完成内容：未加入原书截图和原始文本；后续可增加更多骨架评价和拓扑保持案例。
"""
    coverage.write_text(ctext, encoding="utf-8")

    examples_readme = EX / "README.md"
    examples_readme.write_text(
        """# 第 7 章 二值图像处理代码示例

这些脚本默认使用 `assets/sample_images/sample_binary.png`，输出写入 `examples/output/`。
""",
        encoding="utf-8",
    )

    sample_readme = ROOT / "assets" / "sample_images" / "README.md"
    stext = sample_readme.read_text(encoding="utf-8")
    if "sample_binary.png" not in stext:
        stext = stext.replace(
            "- `sample_segments.png`：包含多个亮度区域和轻微噪声的合成图，用于第 6 章分割示例。",
            "- `sample_segments.png`：包含多个亮度区域和轻微噪声的合成图，用于第 6 章分割示例。\n- `sample_binary.png`：包含多个二值目标、小孔和小噪点，用于第 7 章二值处理示例。",
        )
        sample_readme.write_text(stext, encoding="utf-8")


def main() -> None:
    refine_wiki()
    add_semantic_edges()
    update_docs()
    print("Refined chapter 7 binary image processing content.")


if __name__ == "__main__":
    main()
