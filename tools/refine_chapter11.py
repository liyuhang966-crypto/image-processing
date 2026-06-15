"""Refine chapter 11 deep learning wiki, graph semantics and docs."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "wiki" / "11_深度学习与图像处理"
EX = ROOT / "examples" / "11_deep_learning_image_processing"
PDF = "raw/books/数字图像处理基础_朱虹.pdf"
PDF_PAGE_NEEDS_REVIEW = 220


FILES = [
    ("11.1_深度卷积网络的基本结构.md", "11.1 深度卷积网络的基本结构", "ch11_cnn_layers.png", "cnn_layers_demo.py", "深度卷积网络由卷积、激活、归一化、池化和任务头等模块组成。它通过层级特征从局部边缘逐步抽象到目标结构。", "\\(y=F_L(\\cdots F_2(F_1(x)))\\)", "CNN vs 传统滤波：CNN 的卷积核由数据学习，传统滤波核由人工设计。"),
    ("11.1.1_卷积层.md", "11.1.1 卷积层", "ch11_cnn_layers.png", "cnn_layers_demo.py", "卷积层用多个可学习卷积核在局部感受野上提取特征，并通过权值共享降低参数量。", "\\(Y_k=\\sum_c X_c * W_{k,c}+b_k\\)", "卷积层 vs Sobel：Sobel 是固定边缘核，卷积层核可由训练学习。"),
    ("11.1.2_激活层.md", "11.1.2 激活层", "ch11_cnn_layers.png", "cnn_layers_demo.py", "激活层引入非线性，使网络能表达复杂映射。ReLU 是常见激活函数，能保留正响应并抑制负响应。", "\\(ReLU(x)=\\max(0,x)\\)", "激活层 vs 线性卷积：没有激活，多层线性变换仍等价于线性变换。"),
    ("11.1.3_BN层（批数据归一化处理层）.md", "11.1.3 BN层（批数据归一化处理层）", "ch11_cnn_layers.png", "cnn_layers_demo.py", "BN 层对批数据特征进行标准化并学习缩放和平移参数，常用于稳定训练和加快收敛。", "\\(\\hat{x}=(x-\\mu_B)/\\sqrt{\\sigma_B^2+\\epsilon}\\)，\\(y=\\gamma\\hat{x}+\\beta\\)", "BN vs 普通归一化：BN 位于网络内部并带可学习参数。"),
    ("11.1.4_池化层.md", "11.1.4 池化层", "ch11_cnn_layers.png", "cnn_layers_demo.py", "池化层在局部窗口内汇聚响应，降低空间尺寸并增强一定平移鲁棒性。常见有最大池化和平均池化。", "\\(y=\\max_{(i,j)\\in\\Omega}x_{i,j}\\)", "池化 vs 步幅卷积：两者都能降采样，步幅卷积参数可学习。"),
    ("11.2_超分辨率图像重建卷积网络.md", "11.2 超分辨率图像重建卷积网络", "ch11_super_resolution.png", "srcnn_structure_demo.py", "超分辨率网络学习从低分辨率图像到高分辨率图像的映射，目标是在放大时恢复纹理和边缘细节。", "\\(I_{SR}=f_\\theta(I_{LR})\\)", "超分辨率 vs 插值放大：插值规则固定，网络从数据学习细节恢复。"),
    ("11.2.1_SRCNN网络.md", "11.2.1 SRCNN网络", "ch11_super_resolution.png", "srcnn_structure_demo.py", "SRCNN 是早期端到端超分辨率网络，通常包含特征提取、非线性映射和重建三个阶段。", "\\(F(Y)=W_3*\\sigma(W_2*\\sigma(W_1*Y+b_1)+b_2)+b_3\\)", "SRCNN vs 传统锐化：SRCNN 学习低清到高清映射，锐化只增强局部高频。"),
    ("11.2.2_ESPCN网络.md", "11.2.2 ESPCN网络", "ch11_super_resolution.png", "srcnn_structure_demo.py", "ESPCN 将主要计算放在低分辨率空间，最后用亚像素重排放大图像，计算效率较高。", "PixelShuffle 将通道维重排为空间维，具体公式需人工复核。", "ESPCN vs SRCNN：ESPCN 低分辨率计算更多，SRCNN 常先插值再卷积。"),
    ("11.3_图像分类深度卷积网络.md", "11.3 图像分类深度卷积网络", "ch11_classification_networks.png", "lenet5_structure_demo.py", "图像分类网络把图像映射为类别概率，通常由特征提取骨干和分类头组成。", "\\(p=softmax(z)\\)", "分类网络 vs 检测网络：分类给整图类别，检测还要定位目标。"),
    ("11.3.1_LeNet-5网络.md", "11.3.1 LeNet-5网络", "ch11_classification_networks.png", "lenet5_structure_demo.py", "LeNet-5 是经典早期 CNN，使用卷积、池化和全连接层进行手写数字识别。", "LeNet 结构可抽象为 Conv-Pool-Conv-Pool-FC。", "LeNet vs AlexNet：LeNet 更浅更小，AlexNet 更深并使用 ReLU 等现代技巧。"),
    ("11.3.2_AlexNet网络.md", "11.3.2 AlexNet网络", "ch11_classification_networks.png", "alexnet_structure_demo.py", "AlexNet 通过更深的卷积结构、ReLU、Dropout 和数据增强显著提升大规模图像分类表现。", "分类损失常用交叉熵：\\(L=-\\sum y_i\\log p_i\\)。", "AlexNet vs LeNet：AlexNet 面向大规模自然图像，层数和参数更多。"),
    ("11.4_图像目标检测深度卷积网络.md", "11.4 图像目标检测深度卷积网络", "ch11_detection_networks.png", "yolo_concept_demo.py", "目标检测需要同时预测类别和位置，输出边界框、置信度和类别概率。", "\\(output=(x,y,w,h,score,class)\\)", "检测 vs 分类：检测要回答在哪里，分类只回答是什么。"),
    ("11.4.1_Faster-RCNN网络.md", "11.4.1 Faster-RCNN网络", "ch11_detection_networks.png", "yolo_concept_demo.py", "Faster R-CNN 是两阶段检测方法，先由 RPN 生成候选框，再对候选区域分类和回归边界框。", "\\(L=L_{cls}+\\lambda L_{box}\\)", "Faster R-CNN vs YOLO：前者两阶段精细，后者单阶段速度快。"),
    ("11.4.2_YOLO网络.md", "11.4.2 YOLO网络", "ch11_yolo_grid.png", "yolo_concept_demo.py", "YOLO 将图像划分网格，并在一次前向传播中预测边界框和类别，强调实时检测。", "网格单元预测边界框、置信度和类别概率，具体损失需人工复核。", "YOLO vs Faster R-CNN：YOLO 一阶段直接预测，速度通常更快。"),
    ("11.x_习题.md", "11.x 习题", "ch11_yolo_grid.png", None, "本章习题应围绕 CNN 层功能、超分网络结构、分类与检测任务差异和网络输出解释展开。", "复习重点：卷积、激活、BN、池化、SRCNN/ESPCN、LeNet/AlexNet、Faster R-CNN/YOLO。", "深度学习方法 vs 传统图像处理：前者从数据学习参数，后者依赖人工设计规则。"),
]


def render(item: tuple[str, str, str, str | None, str, str, str]) -> str:
    file, title, figure, code, concept, formula, compare = item
    code_line = "本节偏复习整合，无单独代码；可结合本章其他示例运行。" if code is None else f"[{code}](../../examples/11_deep_learning_image_processing/{code})"
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
- 章节：第 11 章 深度学习与图像处理
- 小节：{title}
- 书中页码：需人工复核
- PDF 页码：需人工复核
- 本地 PDF：{PDF}
- 处理状态：已精修 / 需人工复核

## 核心概念

{concept}

## 关键公式

- {formula}
- 网络结构、损失函数和符号需对照原书人工复核。

## 算法步骤

1. 明确任务：分类、超分辨率或目标检测。
2. 选择网络模块和输入输出格式。
3. 前向传播提取层级特征。
4. 用损失函数衡量预测和标注差异。
5. 训练或推理后解释输出结果。

## 直观理解

深度网络像一组可学习的图像处理流水线：浅层看边缘和纹理，深层组合成目标、类别或重建细节。

## 使用场景

图像分类、超分辨率重建、目标检测、视觉质检、医学影像辅助分析。

## 优点

- 能从数据中学习复杂特征。
- 可端到端优化任务目标。

## 局限性

- 依赖数据、算力和训练配置。
- 可解释性弱，部署时需关注模型大小和推理速度。

## 和相关方法的对比

- {compare}

## 教学图示

![{title}](../../assets/extracted_figures/{figure})

## 对应代码

{code_line}

## 相关知识

- [[05_图像锐化/5.2_一阶微分算子|一阶微分算子]]
- [[06_图像的分割/6.1_阈值分割方法|图像分割]]
- [[09_图像变换/9.2_小波变换|小波变换]]

## 复习问题

1. 本节网络或层解决什么任务？
2. 输入、输出和关键参数分别是什么？
3. 它与对应传统图像处理方法有什么区别？
"""


def refine_wiki() -> None:
    WIKI.mkdir(parents=True, exist_ok=True)
    for item in FILES:
        (WIKI / item[0]).write_text(render(item), encoding="utf-8")
    (WIKI / "README.md").write_text("# 第 11 章 深度学习与图像处理\n\n本章已升级为精品样板章节，覆盖 CNN 基本层、超分辨率、分类网络和目标检测网络。\n", encoding="utf-8")


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
        node(f"wiki/11_深度学习与图像处理/{file}", title)
    for code in ["cnn_layers_demo.py", "srcnn_structure_demo.py", "lenet5_structure_demo.py", "alexnet_structure_demo.py", "yolo_concept_demo.py"]:
        node(f"examples/11_deep_learning_image_processing/{code}", code, "code")
    for formula in ["卷积层公式", "ReLU 函数", "BN 公式", "Softmax 分类", "检测框输出"]:
        node(f"formula/ch11/{formula}", formula, "formula")
    edge("wiki/11_深度学习与图像处理/11.1_深度卷积网络的基本结构.md", "wiki/05_图像锐化/5.2_一阶微分算子.md", "COMPARES_WITH")
    edge("wiki/11_深度学习与图像处理/11.2_超分辨率图像重建卷积网络.md", "wiki/03_图像几何变换/3.2.2_图像的放大.md", "IMPROVES_OR_EXTENDS")
    edge("wiki/11_深度学习与图像处理/11.4_图像目标检测深度卷积网络.md", "wiki/06_图像的分割/6.2_区域生长分割方法.md", "COMPARES_WITH")
    for child in ["11.1.1_卷积层.md", "11.1.2_激活层.md", "11.1.3_BN层（批数据归一化处理层）.md", "11.1.4_池化层.md"]:
        edge(f"wiki/11_深度学习与图像处理/{child}", "wiki/11_深度学习与图像处理/11.1_深度卷积网络的基本结构.md", "GENERALIZES")
    for child in ["11.2.1_SRCNN网络.md", "11.2.2_ESPCN网络.md"]:
        edge(f"wiki/11_深度学习与图像处理/{child}", "wiki/11_深度学习与图像处理/11.2_超分辨率图像重建卷积网络.md", "GENERALIZES")
    for child in ["11.3.1_LeNet-5网络.md", "11.3.2_AlexNet网络.md"]:
        edge(f"wiki/11_深度学习与图像处理/{child}", "wiki/11_深度学习与图像处理/11.3_图像分类深度卷积网络.md", "GENERALIZES")
    for child in ["11.4.1_Faster-RCNN网络.md", "11.4.2_YOLO网络.md"]:
        edge(f"wiki/11_深度学习与图像处理/{child}", "wiki/11_深度学习与图像处理/11.4_图像目标检测深度卷积网络.md", "GENERALIZES")
    for wiki, formula in [("11.1.1_卷积层.md", "卷积层公式"), ("11.1.2_激活层.md", "ReLU 函数"), ("11.1.3_BN层（批数据归一化处理层）.md", "BN 公式"), ("11.3_图像分类深度卷积网络.md", "Softmax 分类"), ("11.4_图像目标检测深度卷积网络.md", "检测框输出")]:
        edge(f"wiki/11_深度学习与图像处理/{wiki}", f"formula/ch11/{formula}", "USES_FORMULA")
    for wiki, code in [("11.1_深度卷积网络的基本结构.md", "cnn_layers_demo.py"), ("11.2.1_SRCNN网络.md", "srcnn_structure_demo.py"), ("11.3.1_LeNet-5网络.md", "lenet5_structure_demo.py"), ("11.3.2_AlexNet网络.md", "alexnet_structure_demo.py"), ("11.4.2_YOLO网络.md", "yolo_concept_demo.py")]:
        edge(f"wiki/11_深度学习与图像处理/{wiki}", f"examples/11_deep_learning_image_processing/{code}", "IMPLEMENTED_BY")
    edge("wiki/11_深度学习与图像处理/11.4.2_YOLO网络.md", "wiki/06_图像的分割/6.1_阈值分割方法.md", "APPLIES_TO")
    data = {"nodes": sorted(nodes.values(), key=lambda x: x["id"]), "edges": [{"source": s, "target": t, "type": r} for s, t, r in sorted(edges)]}
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_docs() -> None:
    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    text = text.replace("- 第 11 章仍在同一分支继续精修，当前不拆分独立分支，避免后续配置分散。", "- 第 11 章“深度学习与图像处理”已升级为精品样板，包含原创图示、独立代码示例和语义图谱关系。")
    if "第 11 章深度学习与图像处理示例：" not in text:
        marker = "默认输入为 `assets/sample_images/` 中的合成图片，输出写入 `examples/output/`，该目录已被 `.gitignore` 忽略。"
        block = """第 11 章深度学习与图像处理示例：

```powershell
python examples/11_deep_learning_image_processing/cnn_layers_demo.py
python examples/11_deep_learning_image_processing/srcnn_structure_demo.py
python examples/11_deep_learning_image_processing/lenet5_structure_demo.py
python examples/11_deep_learning_image_processing/alexnet_structure_demo.py
python examples/11_deep_learning_image_processing/yolo_concept_demo.py
```

"""
        text = text.replace(marker, block + marker)
    readme.write_text(text, encoding="utf-8")
    coverage = ROOT / "coverage_report.md"
    ctext = coverage.read_text(encoding="utf-8")
    ctext = ctext.replace("- 第 11 章：仍在同一分支继续精修，后续按第 2/3/4/5/6/7/8/9/10 章样板推进。", "- 第 11 章：已精修为第十个精品样板，新增原创深度学习图示、独立可运行示例和语义图谱关系。")
    if "## 第 11 章处理记录" not in ctext:
        ctext += "\n\n## 第 11 章处理记录\n\n- 处理的 wiki 文件：第 11 章全部 15 个小节。\n- 新增原创教学图示：`ch11_cnn_layers.png`、`ch11_super_resolution.png`、`ch11_classification_networks.png`、`ch11_detection_networks.png`、`ch11_yolo_grid.png`。\n- 优化代码：`cnn_layers_demo.py`、`srcnn_structure_demo.py`、`lenet5_structure_demo.py`、`alexnet_structure_demo.py`、`yolo_concept_demo.py`，并新增第 11 章 `_utils.py`。\n- 新增图谱关系：CNN 层归属的 `GENERALIZES`，超分对插值放大的 `IMPROVES_OR_EXTENDS`，检测与分割的 `COMPARES_WITH`，公式依赖和代码实现关系。\n- 仍需人工复核：原书页码、网络结构细节、损失函数符号和模型历史描述。\n- 未完成内容：未下载或提交任何模型/数据集；示例仅为原创结构示意，后续可在本地自备模型时扩展推理实验。\n"
    coverage.write_text(ctext, encoding="utf-8")
    (EX / "README.md").write_text("# 第 11 章 深度学习与图像处理代码示例\n\n这些脚本只生成原创结构示意图，不下载模型或数据集，输出写入 `examples/output/`。\n", encoding="utf-8")


def main() -> None:
    refine_wiki()
    add_semantic_edges()
    update_docs()
    print("Refined chapter 11 deep learning content.")


if __name__ == "__main__":
    main()
