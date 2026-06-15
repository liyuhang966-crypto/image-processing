"""Refine chapter 8 color image processing wiki, graph semantics and docs."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "wiki" / "08_彩色图像处理"
EX = ROOT / "examples" / "08_color_image_processing"
PDF = "raw/books/数字图像处理基础_朱虹.pdf"
PDF_PAGE_NEEDS_REVIEW = 150


PROFILES = [
    ("8.1_彩色的形成原理与基本概念.md", "8.1 彩色的形成原理与基本概念", "ch08_color_formation.png", None, "彩色图像通常由多个颜色通道共同描述。RGB 强调显示设备的加色混合，亮度、色调和饱和度则更贴近视觉感受。理解通道、颜色空间和色偏是后续白平衡与补偿的基础。", ["RGB 加色模型可写为：\\(C=rR+gG+bB\\)。", "色彩可从亮度、色调、饱和度三个角度描述，具体符号需人工复核。"], "彩色处理 vs 灰度处理：彩色处理必须考虑通道耦合和人眼感知。", "为什么同一颜色可以用不同颜色空间表示？"),
    ("8.2_表色系.md", "8.2 表色系", "ch08_color_spaces.png", "color_spaces.py", "表色系是颜色的坐标系统。不同表色系强调不同任务：RGB 适合显示和采集，HSV 适合按色调选择，Lab 更强调感知均匀性，工业模型服务标准化测量。", ["颜色变换可抽象为：\\(q=T(c)\\)，其中 \\(c\\) 是原颜色向量，\\(q\\) 是目标颜色空间坐标。"], "RGB vs HSV：RGB 是设备通道，HSV 更接近“颜色种类、纯度、明暗”的描述。", "选择颜色空间时应考虑哪些任务需求？"),
    ("8.2.1_计算颜色模型系统.md", "8.2.1 计算颜色模型系统", "ch08_color_spaces.png", "color_spaces.py", "计算颜色模型侧重机器存储、显示和算法处理，如 RGB、CMY/CMYK、YCrCb 等。它们便于矩阵变换、通道运算和压缩编码。", ["线性颜色变换常写为：\\(q=Mc+b\\)，矩阵和偏置按具体模型确定。"], "计算模型 vs 视觉模型：计算模型便于工程实现，视觉模型更强调人眼感知。", "为什么视频编码常把亮度和色度分开？"),
    ("8.2.2_视觉颜色模型系统.md", "8.2.2 视觉颜色模型系统", "ch08_color_spaces.png", "color_spaces.py", "视觉颜色模型强调人眼对色调、明度和饱和度的感知，例如 HSV/HSL 和 Lab。它们常用于颜色选择、感知差异和颜色增强。", ["HSV 中可理解为：\\(H\\) 表示色调，\\(S\\) 表示饱和度，\\(V\\) 表示明度。"], "HSV vs Lab：HSV 便于直观调色，Lab 更适合感知差异和颜色校正。", "为什么色调变化不等同于亮度变化？"),
    ("8.2.3_工业颜色模型系统.md", "8.2.3 工业颜色模型系统", "ch08_color_spaces.png", "color_compensation.py", "工业颜色模型系统关注颜色标准、设备一致性和可测量性，常用于印刷、显示校准、检测和生产质控。", ["设备校正可抽象为：\\(c_{out}=A c_{in}+b\\)，具体标定矩阵需实验获得。"], "工业模型 vs 教学 RGB：工业模型更重视标准光源、设备标定和可重复测量。", "为什么工业检测不能只依赖未经校准的 RGB 值？"),
    ("8.3_色彩平衡.md", "8.3 色彩平衡", "ch08_white_balance.png", "white_balance.py", "色彩平衡的目标是消除光源或设备造成的整体色偏，让中性物体恢复接近灰色或白色。它通常通过调整各通道增益实现。", ["通道增益校正：\\(I'_k=\\alpha_k I_k\\)。", "理想中性目标满足：\\(R'\\approx G'\\approx B'\\)。"], "色彩平衡 vs 彩色补偿：色彩平衡多针对全局色偏，补偿可针对特定通道或场景误差。", "如何判断一张图存在全局色偏？"),
    ("8.3.1_白平衡法.md", "8.3.1 白平衡法", "ch08_white_balance.png", "white_balance.py", "白平衡利用白色或中性参考估计光源色偏，再调整 RGB 通道，使参考区域接近等通道响应。", ["若参考白区域通道均值为 \\(m_k\\)，可取 \\(\\alpha_k=\\bar{m}/(m_k+\\epsilon)\\)。"], "白平衡 vs 灰度世界：白平衡依赖白/灰参考，灰度世界依赖整幅图平均中性假设。", "如果参考白区域选错，会产生什么问题？"),
    ("8.3.2_灰色世界法.md", "8.3.2 灰色世界法", "ch08_gray_world.png", "gray_world.py", "灰色世界法假设自然图像整体平均颜色应接近中性灰，因此用全图通道均值估计并校正色偏。", ["\\(\\alpha_k=\\bar{m}/(m_k+\\epsilon)\\)，其中 \\(m_k\\) 是第 \\(k\\) 个通道均值。"], "灰度世界 vs 白平衡：灰度世界无需手工参考点，但当画面本身大面积偏色时假设会失效。", "什么图像会违反灰色世界假设？"),
    ("8.4_彩色补偿.md", "8.4 彩色补偿", "ch08_color_compensation.png", "color_compensation.py", "彩色补偿根据成像、传感器或环境偏差对颜色通道进行修正。它可以是简单通道增益，也可以是更复杂的颜色矩阵校正。", ["简单补偿：\\([B',G',R']^T=diag(\\alpha_B,\\alpha_G,\\alpha_R)[B,G,R]^T\\)。"], "彩色补偿 vs 白平衡：白平衡常以中性恢复为目标，彩色补偿可面向设备误差或任务目标。", "通道增益过大可能造成什么伪影？"),
    ("8.x_习题.md", "8.x 习题", "ch08_color_compensation.png", None, "本章习题应围绕颜色空间选择、色偏来源、白平衡假设和颜色补偿参数展开，重点是说明为什么要换空间、为什么要调通道。", ["复习重点：RGB 加色、颜色空间变换、通道增益、灰色世界假设。"], "颜色空间变换 vs 颜色校正：前者改变表达坐标，后者改变颜色数值以修正偏差。", "如何为一张偏蓝图像设计颜色校正流程？"),
]


def render(profile: tuple[str, str, str, str | None, str, list[str], str, str]) -> str:
    file, title, figure, code, concept, formulas, compare, review = profile
    code_line = "本节偏概念复习，无单独代码；可结合本章其他示例运行。" if code is None else f"[{code}](../../examples/08_color_image_processing/{code})"
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
- 章节：第 8 章 彩色图像处理
- 小节：{title}
- 书中页码：需人工复核
- PDF 页码：需人工复核
- 本地 PDF：{PDF}
- 处理状态：已精修 / 需人工复核

## 核心概念

{concept}

## 关键公式

{chr(10).join(f"- {item}" for item in formulas)}

## 算法步骤

1. 输入彩色图像。
2. 选择颜色空间或通道校正目标。
3. 估计变换矩阵、通道增益或颜色统计量。
4. 对各通道执行变换并裁剪到合法范围。
5. 观察色偏、亮度和饱和度是否符合任务需求。

## 直观理解

彩色处理不是只调亮暗，而是在多个通道之间重新分配颜色信息；换颜色空间像换一套坐标轴，白平衡和补偿像重新校准各通道的刻度。

## 使用场景

相机白平衡、工业颜色检测、医学彩色图像校正、低质照片修复、颜色分割前处理。

## 优点

- 能保留或恢复颜色语义。
- 便于分离亮度、色调和设备通道误差。

## 局限性

- 色彩校正依赖光源、设备和场景假设。
- 过度补偿可能造成偏色、饱和或肤色失真。

## 和相关方法的对比

- {compare}

## 教学图示

![{title}](../../assets/extracted_figures/{figure})

## 对应代码

{code_line}

## 相关知识

- [[02_图像增强/2.7_伪彩色|伪彩色]]
- [[06_图像的分割/6.1_阈值分割方法|阈值分割方法]]
- [[08_彩色图像处理/8.3_色彩平衡|色彩平衡]]

## 复习问题

1. {review}
2. 本节方法依赖什么颜色或场景假设？
3. 如果输入图像已经饱和，颜色校正会遇到什么限制？
"""


def refine_wiki() -> None:
    WIKI.mkdir(parents=True, exist_ok=True)
    for profile in PROFILES:
        (WIKI / profile[0]).write_text(render(profile), encoding="utf-8")
    (WIKI / "README.md").write_text("# 第 8 章 彩色图像处理\n\n本章已升级为精品样板章节，覆盖颜色形成、表色系、白平衡、灰色世界和彩色补偿。\n", encoding="utf-8")


def add_semantic_edges() -> None:
    path = ROOT / "graph" / "semantic_edges.json"
    data = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"nodes": [], "edges": []}
    nodes = {node["id"]: node for node in data.get("nodes", [])}
    edges = {(edge["source"], edge["target"], edge["type"]) for edge in data.get("edges", [])}
    def node(i: str, label: str, kind: str = "concept") -> None:
        nodes[i] = {"id": i, "label": label, "kind": kind}
    def edge(s: str, t: str, r: str) -> None:
        edges.add((s, t, r))
    for file, title, *_ in PROFILES:
        node(f"wiki/08_彩色图像处理/{file}", title)
    for code in ["color_spaces.py", "white_balance.py", "gray_world.py", "color_compensation.py"]:
        node(f"examples/08_color_image_processing/{code}", code, "code")
    for formula in ["RGB 加色模型", "颜色空间变换", "通道增益校正", "灰色世界假设"]:
        node(f"formula/ch08/{formula}", formula, "formula")
    edge("wiki/08_彩色图像处理/8.2_表色系.md", "wiki/08_彩色图像处理/8.1_彩色的形成原理与基本概念.md", "PREREQUISITE")
    edge("wiki/08_彩色图像处理/8.3_色彩平衡.md", "wiki/08_彩色图像处理/8.2_表色系.md", "PREREQUISITE")
    edge("wiki/08_彩色图像处理/8.3.1_白平衡法.md", "wiki/08_彩色图像处理/8.3_色彩平衡.md", "GENERALIZES")
    edge("wiki/08_彩色图像处理/8.3.2_灰色世界法.md", "wiki/08_彩色图像处理/8.3_色彩平衡.md", "GENERALIZES")
    edge("wiki/08_彩色图像处理/8.4_彩色补偿.md", "wiki/08_彩色图像处理/8.3_色彩平衡.md", "IMPROVES_OR_EXTENDS")
    edge("wiki/08_彩色图像处理/8.1_彩色的形成原理与基本概念.md", "formula/ch08/RGB 加色模型", "USES_FORMULA")
    edge("wiki/08_彩色图像处理/8.2_表色系.md", "formula/ch08/颜色空间变换", "USES_FORMULA")
    edge("wiki/08_彩色图像处理/8.3_色彩平衡.md", "formula/ch08/通道增益校正", "USES_FORMULA")
    edge("wiki/08_彩色图像处理/8.3.2_灰色世界法.md", "formula/ch08/灰色世界假设", "USES_FORMULA")
    for wiki, code in [("8.2_表色系.md", "color_spaces.py"), ("8.3.1_白平衡法.md", "white_balance.py"), ("8.3.2_灰色世界法.md", "gray_world.py"), ("8.4_彩色补偿.md", "color_compensation.py")]:
        edge(f"wiki/08_彩色图像处理/{wiki}", f"examples/08_color_image_processing/{code}", "IMPLEMENTED_BY")
    edge("wiki/08_彩色图像处理/8.4_彩色补偿.md", "wiki/06_图像的分割/6.1_阈值分割方法.md", "APPLIES_TO")
    data = {"nodes": sorted(nodes.values(), key=lambda x: x["id"]), "edges": [{"source": s, "target": t, "type": r} for s, t, r in sorted(edges)]}
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_docs() -> None:
    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    text = text.replace("- 第 8 章到第 11 章仍在同一分支继续精修，当前不拆分独立分支，避免后续配置分散。", "- 第 8 章“彩色图像处理”已升级为精品样板，包含原创图示、独立代码示例和语义图谱关系。\n- 第 9 章到第 11 章仍在同一分支继续精修，当前不拆分独立分支，避免后续配置分散。")
    if "第 8 章彩色图像处理示例：" not in text:
        marker = "默认输入为 `assets/sample_images/` 中的合成图片，输出写入 `examples/output/`，该目录已被 `.gitignore` 忽略。"
        block = """第 8 章彩色图像处理示例：

```powershell
python examples/08_color_image_processing/color_spaces.py --space hsv
python examples/08_color_image_processing/white_balance.py --percentile 95
python examples/08_color_image_processing/gray_world.py
python examples/08_color_image_processing/color_compensation.py --red-gain 1.05 --blue-gain 0.95
```

"""
        text = text.replace(marker, block + marker)
    readme.write_text(text, encoding="utf-8")
    coverage = ROOT / "coverage_report.md"
    ctext = coverage.read_text(encoding="utf-8")
    ctext = ctext.replace("- 第 8 章到第 11 章：仍在同一分支继续精修，后续按第 2/3/4/5/6/7 章样板逐章推进。", "- 第 8 章：已精修为第七个精品样板，新增原创彩色处理图示、独立可运行示例和语义图谱关系。\n- 第 9 章到第 11 章：仍在同一分支继续精修，后续按第 2/3/4/5/6/7/8 章样板逐章推进。")
    if "## 第 8 章处理记录" not in ctext:
        ctext += "\n\n## 第 8 章处理记录\n\n- 处理的 wiki 文件：第 8 章全部 10 个小节。\n- 新增原创教学图示：`ch08_color_formation.png`、`ch08_color_spaces.png`、`ch08_white_balance.png`、`ch08_gray_world.png`、`ch08_color_compensation.png`。\n- 优化代码：`color_spaces.py`、`white_balance.py`、`gray_world.py`、`color_compensation.py`，并新增第 8 章 `_utils.py`。\n- 新增图谱关系：颜色形成到表色系的 `PREREQUISITE`，色彩平衡子方法的 `GENERALIZES`，彩色补偿的 `IMPROVES_OR_EXTENDS`，公式依赖和代码实现关系。\n- 仍需人工复核：原书页码、各颜色模型符号、工业颜色模型细节和补偿矩阵定义。\n- 未完成内容：未加入原书截图和原始文本；后续可增加更多颜色空间定量比较。\n"
    coverage.write_text(ctext, encoding="utf-8")
    (EX / "README.md").write_text("# 第 8 章 彩色图像处理代码示例\n\n这些脚本默认使用 `assets/sample_images/sample_color.png`，输出写入 `examples/output/`。\n", encoding="utf-8")


def main() -> None:
    refine_wiki()
    add_semantic_edges()
    update_docs()
    print("Refined chapter 8 color image processing content.")


if __name__ == "__main__":
    main()
