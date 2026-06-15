"""Refine chapter 6 image segmentation wiki, graph semantics and docs."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "wiki" / "06_图像的分割"
EX = ROOT / "examples" / "06_image_segmentation"
PDF = "raw/books/数字图像处理基础_朱虹.pdf"
PDF_PAGE_NEEDS_REVIEW = 112


PROFILES = [
    {
        "file": "6.1_阈值分割方法.md",
        "title": "6.1 阈值分割方法",
        "subsection": "6.1 阈值分割方法",
        "figure": "ch06_threshold_histogram.png",
        "code": "threshold_segmentation.py",
        "concept": "阈值分割把灰度图像按一个或多个阈值划分为目标和背景。它隐含的前提是目标与背景在灰度分布上有可分性，例如直方图出现双峰或目标灰度稳定高于背景。",
        "formula": ["二值分割：\\(g(x,y)=1\\) if \\(f(x,y)\\ge T\\)，否则 \\(g(x,y)=0\\)。", "多阈值可写为：\\(g=k\\) if \\(T_k\\le f(x,y)<T_{k+1}\\)。"],
        "steps": ["输入灰度图。", "分析直方图或先验目标比例。", "选择阈值 \\(T\\)。", "逐像素比较并输出二值图。", "可用形态学处理修补小孔和孤立点。"],
        "intuition": "阈值像一道灰度分界线：比分界线亮的归一类，比它暗的归另一类。",
        "scene": "文档二值化、背景单一的目标提取、工业检测中亮暗差明显的缺陷分割。",
        "pros": ["实现简单、速度快。", "结果容易解释。", "适合作为复杂分割方法的基线。"],
        "limits": ["光照不均或灰度重叠时效果差。", "只考虑灰度，不考虑空间连通性。"],
        "compare": ["阈值分割 vs [[06_图像的分割/6.2_区域生长分割方法|区域生长]]：前者按灰度全局分类，后者从种子出发利用连通性。", "阈值分割 vs [[05_图像锐化/5.5_Canny算子|Canny]]：前者输出区域，后者输出边缘。"],
        "links": ["[[06_图像的分割/6.1.2_最大熵方法|最大熵方法]]", "[[06_图像的分割/6.1.3_最大类间、类内方差比法|Otsu 方法]]", "[[07_二值图像处理|二值图像处理]]"],
        "review": ["什么情况下全局阈值分割容易成功？", "为什么光照不均会破坏阈值分割？", "阈值分割和边缘检测的输出有什么不同？"],
    },
    {
        "file": "6.1.1_p-参数法.md",
        "title": "6.1.1 p-参数法",
        "subsection": "6.1.1 p-参数法",
        "figure": "ch06_p_parameter_threshold.png",
        "code": "threshold_segmentation.py",
        "concept": "p-参数法利用目标或背景所占面积比例的先验信息确定阈值。若已知目标大约占图像 p 的比例，就可以在累计直方图上找到对应分位点作为阈值。",
        "formula": ["累计概率：\\(P(t)=\\sum_{i=0}^{t}h(i)\\)。", "若目标占比已知，可取满足 \\(P(T)\\approx p\\) 的灰度作为阈值，方向需按目标亮暗人工判断。"],
        "steps": ["统计归一化直方图。", "计算累计概率。", "根据目标或背景面积比例 p 找到阈值。", "执行二值化。"],
        "intuition": "如果你知道背景大约占 70%，那就可以把灰度从暗到亮累计到 70% 的位置当作分界线。",
        "scene": "目标面积比例比较稳定的工业检测、固定拍摄场景下的批量分割。",
        "pros": ["利用先验面积信息，计算简单。", "比手工试阈值更可复现。"],
        "limits": ["p 估计错误会直接导致分割偏差。", "目标亮暗方向和直方图重叠需要人工判断。"],
        "compare": ["p-参数法 vs Otsu：p-参数法依赖面积先验，Otsu 依赖类间方差最大化。", "p-参数法 vs 最大熵：前者关心比例，后者关心两类信息量。"],
        "links": ["[[06_图像的分割/6.1_阈值分割方法|阈值分割方法]]", "[[06_图像的分割/6.1.3_最大类间、类内方差比法|最大类间、类内方差比法]]"],
        "review": ["p-参数法需要什么先验？", "如果目标面积比例变化很大，会发生什么？", "如何判断阈值应取累计概率的哪一侧？"],
    },
    {
        "file": "6.1.2_最大熵方法.md",
        "title": "6.1.2 最大熵方法",
        "subsection": "6.1.2 最大熵方法",
        "figure": "ch06_max_entropy_threshold.png",
        "code": "max_entropy_threshold.py",
        "concept": "最大熵阈值法把阈值两侧看成两个灰度类别，选择使两类灰度分布信息量之和最大的阈值。它适合从直方图统计角度寻找最能解释目标和背景的分界。",
        "formula": ["背景熵：\\(H_0(t)=-\\sum_{i=0}^{t}p_i/P_0\\log(p_i/P_0)\\)。", "目标熵：\\(H_1(t)=-\\sum_{i=t+1}^{L-1}p_i/P_1\\log(p_i/P_1)\\)。", "选择：\\(T=\\arg\\max_t(H_0(t)+H_1(t))\\)。"],
        "steps": ["统计灰度概率。", "枚举候选阈值。", "分别计算阈值两侧的归一化熵。", "选择总熵最大的阈值。", "用该阈值二值化。"],
        "intuition": "好的阈值会让两边都保留足够的灰度结构信息，而不是把一边压成几乎没有内容的空类。",
        "scene": "直方图双峰不明显但两类灰度分布仍有统计差异的图像。",
        "pros": ["不需要目标面积先验。", "能从信息量角度自动选阈值。"],
        "limits": ["对噪声和直方图估计敏感。", "当两类灰度严重重叠时仍会失败。"],
        "compare": ["最大熵 vs Otsu：最大熵最大化信息量，Otsu 最大化类间差异。", "最大熵 vs p-参数法：最大熵不需要先验面积比例。"],
        "links": ["[[06_图像的分割/6.1_阈值分割方法|阈值分割方法]]", "[[06_图像的分割/6.1.3_最大类间、类内方差比法|Otsu 方法]]"],
        "review": ["最大熵方法为什么要分别计算两类熵？", "概率为零的灰度级在实现中如何处理？", "最大熵和 Otsu 选阈值的目标函数有什么差异？"],
    },
    {
        "file": "6.1.3_最大类间、类内方差比法.md",
        "title": "6.1.3 最大类间、类内方差比法",
        "subsection": "6.1.3 最大类间、类内方差比法",
        "figure": "ch06_otsu_variance.png",
        "code": "otsu_threshold.py",
        "concept": "最大类间方差法通常称为 Otsu 方法。它枚举阈值，寻找让背景和目标均值差异最大、类内波动相对较小的阈值。",
        "formula": ["类间方差：\\(\\sigma_b^2(t)=\\omega_0(t)\\omega_1(t)[\\mu_0(t)-\\mu_1(t)]^2\\)。", "选择：\\(T=\\arg\\max_t\\sigma_b^2(t)\\)。", "类内方差比形式与原书符号需人工复核。"],
        "steps": ["统计直方图概率。", "枚举阈值并计算两类权重和均值。", "计算类间方差或类内/类间方差比。", "选择最优阈值并二值化。"],
        "intuition": "Otsu 想找一个分界，让分出来的两组像素均值离得尽量远，同时每组内部尽量集中。",
        "scene": "背景和目标灰度分布接近双峰、照明较稳定的自动二值化任务。",
        "pros": ["无需手工阈值。", "实现成熟，OpenCV 直接支持。", "对双峰直方图效果好。"],
        "limits": ["不适合严重光照不均。", "目标很小或类比例极端时可能偏向大类。"],
        "compare": ["Otsu vs 最大熵：Otsu 关注均值分离，最大熵关注信息量。", "Otsu vs p-参数法：Otsu 自动统计，p-参数法依赖面积先验。"],
        "links": ["[[06_图像的分割/6.1.2_最大熵方法|最大熵方法]]", "[[07_二值图像处理|二值图像处理]]"],
        "review": ["Otsu 为什么适合双峰直方图？", "目标面积很小时 Otsu 会有什么偏差？", "类间方差最大化和类内方差最小化是什么关系？"],
    },
    {
        "file": "6.2_区域生长分割方法.md",
        "title": "6.2 区域生长分割方法",
        "subsection": "6.2 区域生长分割方法",
        "figure": "ch06_region_growing.png",
        "code": "region_growing.py",
        "concept": "区域生长从一个或多个种子点出发，把邻域中满足相似性准则的像素逐步合并为区域。它不仅看灰度相似，也强调空间连通性。",
        "formula": ["相似性准则示例：\\(|f(x,y)-f(s_x,s_y)|\\le \\tau\\)。", "也可使用区域均值准则：\\(|f(x,y)-\\mu_R|\\le \\tau\\)，具体原书定义需人工复核。"],
        "steps": ["选择种子点。", "设定灰度或纹理相似性阈值。", "检查种子邻域像素。", "符合条件则加入区域并继续扩张。", "直到没有新像素可加入。"],
        "intuition": "像从一个点往外涂色：相邻且颜色足够像的像素加入区域，不像的地方就停止。",
        "scene": "医学图像器官粗分割、交互式目标提取、灰度均匀且连通的区域分割。",
        "pros": ["利用空间连通性，区域结果自然连贯。", "能结合人工种子或先验位置。"],
        "limits": ["种子点和阈值选择敏感。", "区域内部灰度不均时容易漏分，边界弱时容易溢出。"],
        "compare": ["区域生长 vs 阈值分割：区域生长强调连通扩张，阈值分割全局逐像素分类。", "区域生长 vs 边缘检测：前者找区域内部，后者找边界位置。"],
        "links": ["[[06_图像的分割/6.1_阈值分割方法|阈值分割方法]]", "[[05_图像锐化/5.4_微分算子在边缘检测中的应用|边缘检测]]"],
        "review": ["区域生长为什么需要种子点？", "相似性阈值过大或过小分别会怎样？", "区域生长如何利用空间连通性？"],
    },
    {
        "file": "6.x_习题.md",
        "title": "6.x 习题",
        "subsection": "6.x 习题",
        "figure": "ch06_region_growing.png",
        "code": None,
        "concept": "本章习题应围绕阈值选择依据、目标/背景统计差异、空间连通性和参数敏感性展开。重点不是背算法名，而是判断图像条件是否满足算法假设。",
        "formula": ["复习重点：二值阈值函数、累计概率、最大熵目标、Otsu 类间方差、区域生长相似性准则。"],
        "steps": ["先判断图像是灰度可分还是区域连通更重要。", "若灰度可分，选择 p-参数、最大熵或 Otsu。", "若需要连通区域，考虑区域生长。", "说明参数如何影响欠分割或过分割。"],
        "intuition": "分割题先问“我要的是一条边、一块区域，还是目标/背景标签？”答案不同，方法也不同。",
        "scene": "期末复习、实验报告、参数调试记录、后续二值图像处理前置步骤。",
        "pros": ["把阈值、区域和后处理串起来。", "便于为第 7 章二值图像处理打基础。"],
        "limits": ["页码、原书题号和部分符号仍需人工复核。"],
        "compare": ["Otsu、最大熵和 p-参数法适合比较阈值目标函数。", "阈值分割和区域生长适合比较灰度统计与空间连通性。"],
        "links": ["[[06_图像的分割/6.1_阈值分割方法|阈值分割方法]]", "[[06_图像的分割/6.2_区域生长分割方法|区域生长分割方法]]", "[[07_二值图像处理|二值图像处理]]"],
        "review": ["设计一个光照不均图像的分割方案。", "比较最大熵和 Otsu 的阈值选择目标。", "区域生长的种子点选错会怎样？", "为什么分割后常接二值形态学处理？"],
    },
]


def render(profile: dict[str, object]) -> str:
    title = str(profile["title"])
    code = profile["code"]
    code_line = "本节偏复习整合，无单独代码；可结合本章其他示例运行。" if code is None else f"[{code}](../../examples/06_image_segmentation/{code})"
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
- 章节：第 6 章 图像的分割
- 小节：{profile["subsection"]}
- 书中页码：需人工复核
- PDF 页码：需人工复核
- 本地 PDF：{PDF}
- 处理状态：已精修 / 需人工复核

## 核心概念

{profile["concept"]}

## 关键公式

{chr(10).join(f"- {item}" for item in profile["formula"])}

## 算法步骤

{chr(10).join(f"{index}. {item}" for index, item in enumerate(profile["steps"], 1))}

## 直观理解

{profile["intuition"]}

## 使用场景

{profile["scene"]}

## 优点

{chr(10).join(f"- {item}" for item in profile["pros"])}

## 局限性

{chr(10).join(f"- {item}" for item in profile["limits"])}

## 和相关方法的对比

{chr(10).join(f"- {item}" for item in profile["compare"])}

## 教学图示

![{title}](../../assets/extracted_figures/{profile["figure"]})

## 对应代码

{code_line}

## 相关知识

{chr(10).join(f"- {item}" for item in profile["links"])}

## 复习问题

{chr(10).join(f"{index}. {item}" for index, item in enumerate(profile["review"], 1))}
"""


def refine_wiki() -> None:
    WIKI.mkdir(parents=True, exist_ok=True)
    for profile in PROFILES:
        (WIKI / str(profile["file"])).write_text(render(profile), encoding="utf-8")
    (WIKI / "README.md").write_text(
        """# 第 6 章 图像的分割

本章已升级为精品样板章节，重点整理阈值分割、p-参数法、最大熵、Otsu 和区域生长。所有笔记均包含来源状态、公式、步骤、原创教学图示、代码链接、方法对比和复习问题。

## 小节

- [[6.1_阈值分割方法]]
- [[6.1.1_p-参数法]]
- [[6.1.2_最大熵方法]]
- [[6.1.3_最大类间、类内方差比法]]
- [[6.2_区域生长分割方法]]
- [[6.x_习题]]
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

    for node_id, label in [
        ("wiki/06_图像的分割/6.1_阈值分割方法.md", "阈值分割"),
        ("wiki/06_图像的分割/6.1.1_p-参数法.md", "p-参数法"),
        ("wiki/06_图像的分割/6.1.2_最大熵方法.md", "最大熵方法"),
        ("wiki/06_图像的分割/6.1.3_最大类间、类内方差比法.md", "Otsu 阈值法"),
        ("wiki/06_图像的分割/6.2_区域生长分割方法.md", "区域生长"),
    ]:
        node(node_id, label)
    for code in ["threshold_segmentation.py", "max_entropy_threshold.py", "otsu_threshold.py", "region_growing.py"]:
        node(f"examples/06_image_segmentation/{code}", code, "code")
    for formula in ["二值阈值函数", "累计概率阈值", "最大熵目标函数", "Otsu 类间方差", "区域生长相似性准则"]:
        node(f"formula/ch06/{formula}", formula, "formula")

    edge("wiki/06_图像的分割/6.1.1_p-参数法.md", "wiki/06_图像的分割/6.1_阈值分割方法.md", "GENERALIZES")
    edge("wiki/06_图像的分割/6.1.2_最大熵方法.md", "wiki/06_图像的分割/6.1_阈值分割方法.md", "GENERALIZES")
    edge("wiki/06_图像的分割/6.1.3_最大类间、类内方差比法.md", "wiki/06_图像的分割/6.1_阈值分割方法.md", "GENERALIZES")
    edge("wiki/06_图像的分割/6.2_区域生长分割方法.md", "wiki/06_图像的分割/6.1_阈值分割方法.md", "COMPARES_WITH")
    edge("wiki/06_图像的分割/6.1_阈值分割方法.md", "formula/ch06/二值阈值函数", "USES_FORMULA")
    edge("wiki/06_图像的分割/6.1.1_p-参数法.md", "formula/ch06/累计概率阈值", "USES_FORMULA")
    edge("wiki/06_图像的分割/6.1.2_最大熵方法.md", "formula/ch06/最大熵目标函数", "USES_FORMULA")
    edge("wiki/06_图像的分割/6.1.3_最大类间、类内方差比法.md", "formula/ch06/Otsu 类间方差", "USES_FORMULA")
    edge("wiki/06_图像的分割/6.2_区域生长分割方法.md", "formula/ch06/区域生长相似性准则", "USES_FORMULA")
    edge("wiki/06_图像的分割/6.1_阈值分割方法.md", "wiki/07_二值图像处理", "PREREQUISITE")
    edge("wiki/06_图像的分割/6.2_区域生长分割方法.md", "wiki/05_图像锐化/5.4_微分算子在边缘检测中的应用.md", "COMPARES_WITH")
    for wiki, code in [
        ("6.1_阈值分割方法.md", "threshold_segmentation.py"),
        ("6.1.2_最大熵方法.md", "max_entropy_threshold.py"),
        ("6.1.3_最大类间、类内方差比法.md", "otsu_threshold.py"),
        ("6.2_区域生长分割方法.md", "region_growing.py"),
    ]:
        edge(f"wiki/06_图像的分割/{wiki}", f"examples/06_image_segmentation/{code}", "IMPLEMENTED_BY")

    data = {
        "nodes": sorted(nodes.values(), key=lambda item: item["id"]),
        "edges": [{"source": s, "target": t, "type": r} for s, t, r in sorted(edges)],
    }
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_docs() -> None:
    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    text = text.replace(
        "- 第 6 章到第 11 章仍在同一分支继续精修，当前不拆分独立分支，避免后续配置分散。",
        "- 第 6 章“图像的分割”已升级为精品样板，包含原创图示、独立代码示例和语义图谱关系。\n- 第 7 章到第 11 章仍在同一分支继续精修，当前不拆分独立分支，避免后续配置分散。",
    )
    if "第 6 章图像分割示例：" not in text:
        marker = "默认输入为 `assets/sample_images/` 中的合成图片，输出写入 `examples/output/`，该目录已被 `.gitignore` 忽略。"
        block = """第 6 章图像分割示例：

```powershell
python examples/06_image_segmentation/threshold_segmentation.py --threshold 128
python examples/06_image_segmentation/max_entropy_threshold.py
python examples/06_image_segmentation/otsu_threshold.py
python examples/06_image_segmentation/region_growing.py --seed-x 85 --seed-y 120 --tolerance 28
```

"""
        text = text.replace(marker, block + marker)
    text = text.replace("第 3 章、第 4 章和第 5 章语义关系", "第 3 章、第 4 章、第 5 章和第 6 章语义关系")
    readme.write_text(text, encoding="utf-8")

    coverage = ROOT / "coverage_report.md"
    ctext = coverage.read_text(encoding="utf-8")
    ctext = ctext.replace(
        "- 第 6 章到第 11 章：仍在同一分支继续精修，后续按第 2/3/4/5 章样板逐章推进。",
        "- 第 6 章：已精修为第五个精品样板，新增原创分割图示、独立可运行示例和语义图谱关系。\n- 第 7 章到第 11 章：仍在同一分支继续精修，后续按第 2/3/4/5/6 章样板逐章推进。",
    )
    if "## 第 6 章处理记录" not in ctext:
        ctext += """

## 第 6 章处理记录

- 处理的 wiki 文件：`6.1_阈值分割方法.md`、`6.1.1_p-参数法.md`、`6.1.2_最大熵方法.md`、`6.1.3_最大类间、类内方差比法.md`、`6.2_区域生长分割方法.md`、`6.x_习题.md`。
- 新增原创教学图示：`ch06_threshold_histogram.png`、`ch06_p_parameter_threshold.png`、`ch06_max_entropy_threshold.png`、`ch06_otsu_variance.png`、`ch06_region_growing.png`。
- 优化代码：`threshold_segmentation.py`、`max_entropy_threshold.py`、`otsu_threshold.py`、`region_growing.py`，并新增第 6 章 `_utils.py`。
- 新增图谱关系：阈值方法归属的 `GENERALIZES`，公式依赖的 `USES_FORMULA`，分割到二值处理的 `PREREQUISITE`，区域生长与阈值/边缘方法的 `COMPARES_WITH`，以及代码实现关系。
- 仍需人工复核：原书页码、p-参数法方向约定、最大熵公式符号和最大类间/类内方差比写法。
- 未完成内容：未加入原书截图和原始文本；后续可增加自适应阈值、区域合并和分割质量指标。
"""
    coverage.write_text(ctext, encoding="utf-8")

    graph_readme = ROOT / "graph" / "README.md"
    gtext = graph_readme.read_text(encoding="utf-8")
    gtext = gtext.replace("第 3 章、第 4 章和第 5 章的额外语义关系", "第 3 章、第 4 章、第 5 章和第 6 章的额外语义关系")
    graph_readme.write_text(gtext, encoding="utf-8")

    examples_readme = EX / "README.md"
    examples_readme.write_text(
        """# 第 6 章 图像分割代码示例

这些脚本默认使用 `assets/sample_images/sample_segments.png`，输出写入 `examples/output/`。

```powershell
python examples/06_image_segmentation/threshold_segmentation.py --threshold 128
python examples/06_image_segmentation/max_entropy_threshold.py
python examples/06_image_segmentation/otsu_threshold.py
python examples/06_image_segmentation/region_growing.py --seed-x 85 --seed-y 120 --tolerance 28
```

所有输入图片均为可自由提交的合成样例，不使用原书图片。
""",
        encoding="utf-8",
    )

    sample_readme = ROOT / "assets" / "sample_images" / "README.md"
    stext = sample_readme.read_text(encoding="utf-8")
    if "sample_segments.png" not in stext:
        stext = stext.replace(
            "- `sample_noisy.png`：在合成灰度图上加入高斯噪声和椒盐噪声，用于第 4 章去噪示例。",
            "- `sample_noisy.png`：在合成灰度图上加入高斯噪声和椒盐噪声，用于第 4 章去噪示例。\n- `sample_segments.png`：包含多个亮度区域和轻微噪声的合成图，用于第 6 章分割示例。",
        )
        sample_readme.write_text(stext, encoding="utf-8")

    glossary = ROOT / "wiki" / "99_术语表.md"
    glossary_text = glossary.read_text(encoding="utf-8")
    if "## 图像分割" not in glossary_text:
        glossary_text += """

## 图像分割

- 阈值分割：按灰度阈值把像素划分为目标和背景。
- p-参数法：利用目标或背景面积比例先验确定阈值。
- 最大熵阈值：选择让阈值两侧信息量之和最大的分界。
- Otsu 方法：选择最大化类间方差的自动阈值。
- 区域生长：从种子点出发，按相似性和连通性扩张区域。
"""
        glossary.write_text(glossary_text, encoding="utf-8")


def main() -> None:
    refine_wiki()
    add_semantic_edges()
    update_docs()
    print("Refined chapter 6 segmentation content.")


if __name__ == "__main__":
    main()
