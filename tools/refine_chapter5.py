"""Refine chapter 5 image sharpening wiki, graph semantics and docs."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "wiki" / "05_图像锐化"
FIG = ROOT / "assets" / "extracted_figures"
EX = ROOT / "examples" / "05_image_sharpening"
PDF = "raw/books/数字图像处理基础_朱虹.pdf"
PDF_PAGE_NEEDS_REVIEW = 96


PROFILES = [
    {
        "file": "5.1_图像细节的基本特征.md",
        "title": "5.1 图像细节的基本特征",
        "section": "第 5 章 图像锐化",
        "subsection": "5.1 图像细节的基本特征",
        "figure": "ch05_detail_profiles.png",
        "code": None,
        "concept": "图像锐化关注的是灰度在空间位置上的快速变化。点、细线、边缘和纹理都可以看成局部灰度突变；平坦区域或缓慢变化区域则不应被过度放大。理解这一点后，锐化就不只是让图像看起来更清楚，而是有选择地增强高频细节。",
        "formula": ["一阶差分可近似局部变化率：\\(g_x=f(x+1,y)-f(x,y)\\)，\\(g_y=f(x,y+1)-f(x,y)\\)。", "梯度幅值常写成：\\(|\\nabla f|=\\sqrt{g_x^2+g_y^2}\\)，实际实现也常用 \\(|g_x|+|g_y|\\) 近似。"],
        "steps": ["输入灰度图像。", "观察局部窗口内像素是否有快速变化。", "用一阶或二阶差分估计变化强度。", "将变化强的位置作为边缘、细线或纹理候选输出。"],
        "intuition": "平滑区域像缓坡，锐化方法不该大幅响应；边缘像台阶，差分后会出现峰值；孤立点和细线比边缘更局部，二阶算子通常更敏感。",
        "scene": "显微图像细胞边界、文档扫描文字边缘、工业零件轮廓、医学图像结构轮廓增强。",
        "pros": ["把锐化目标从主观清晰转化为局部变化检测。", "为一阶、二阶、Canny、LoG 等方法建立共同语言。"],
        "limits": ["噪声也是快速变化，未经平滑直接锐化会放大噪声。", "强纹理和真实边缘都属于高频，单靠差分不一定能区分。"],
        "compare": ["图像锐化 vs [[04_图像去噪/4.2_均值滤波|图像去噪]]：前者放大变化，后者抑制变化。", "一阶变化强调边缘方向，二阶变化强调灰度曲率和细节转折。"],
        "links": ["[[05_图像锐化/5.2_一阶微分算子|一阶微分算子]]", "[[05_图像锐化/5.3_二阶微分算子|二阶微分算子]]", "[[04_图像去噪/4.1_图像噪声|图像噪声]]"],
        "review": ["为什么噪声会被锐化算子放大？", "点、线、边缘在灰度剖面上有什么差异？", "为什么锐化前常常需要先平滑？"],
    },
    {
        "file": "5.2_一阶微分算子.md",
        "title": "5.2 一阶微分算子",
        "section": "第 5 章 图像锐化",
        "subsection": "5.2 一阶微分算子",
        "figure": "ch05_first_derivative_kernels.png",
        "code": "sobel_operator.py",
        "concept": "一阶微分算子用相邻像素差分近似梯度，主要检测灰度阶跃和边缘方向。它把水平、垂直或对角方向的灰度变化变成响应强度，响应越大表示该方向的边缘越明显。",
        "formula": ["梯度向量：\\(\\nabla f=[\\partial f/\\partial x,\\partial f/\\partial y]^T\\)。", "幅值：\\(M=\\sqrt{G_x^2+G_y^2}\\)，方向：\\(\\theta=\\arctan(G_y/G_x)\\)。"],
        "steps": ["输入灰度图。", "选择一阶差分模板，如 Roberts、Prewitt 或 Sobel。", "分别卷积得到 \\(G_x\\) 和 \\(G_y\\)。", "计算梯度幅值和方向。", "按阈值或后续流程得到边缘图。"],
        "intuition": "把模板放到图像上滑动，一边看左边和右边差多少，一边看上边和下边差多少；差得越大，就越像边缘。",
        "scene": "边缘检测、轮廓提取、锐化预处理、目标分割前的边界提示。",
        "pros": ["实现简单，计算量低。", "可以给出边缘方向。", "与阈值、非极大值抑制等步骤容易组合。"],
        "limits": ["对噪声敏感。", "只用局部窗口，容易产生断裂边缘。", "阈值选择会明显影响结果。"],
        "compare": ["Roberts 窗口小、定位敏感；Prewitt 平滑较弱；Sobel 对中心行列加权，抗噪略好。", "一阶微分 vs 二阶微分：一阶响应边缘峰值，二阶常在边缘两侧出现符号变化。"],
        "links": ["[[05_图像锐化/5.2.2_Roberts交叉微分算子|Roberts交叉微分算子]]", "[[05_图像锐化/5.2.3_Sobel微分算子|Sobel微分算子]]", "[[05_图像锐化/5.5_Canny算子|Canny算子]]"],
        "review": ["为什么一阶微分能检测阶跃边缘？", "梯度方向和边缘方向是什么关系？", "为什么 Sobel 通常比简单差分更稳？"],
    },
    {
        "file": "5.2.1_具有方向性的一阶微分算子.md",
        "title": "5.2.1 具有方向性的一阶微分算子",
        "section": "第 5 章 图像锐化",
        "subsection": "5.2.1 具有方向性的一阶微分算子",
        "figure": "ch05_first_derivative_kernels.png",
        "code": "sobel_operator.py",
        "concept": "方向性一阶算子通过不同方向的模板估计灰度变化，例如水平差分关注垂直边缘，垂直差分关注水平边缘。实际边缘检测通常组合多个方向响应，避免只看一个方向造成漏检。",
        "formula": ["水平方向响应：\\(G_x=f*K_x\\)。", "垂直方向响应：\\(G_y=f*K_y\\)。", "综合响应可写成：\\(M=|G_x|+|G_y|\\) 或 \\(M=\\sqrt{G_x^2+G_y^2}\\)。"],
        "steps": ["准备多个方向模板。", "对图像分别卷积。", "比较或合成不同方向响应。", "保留响应强的位置作为候选边缘。"],
        "intuition": "模板像一个有方向的探针：横向探针更容易发现左右灰度差，纵向探针更容易发现上下灰度差。",
        "scene": "检测道路边线、文字笔画方向、工业零件轮廓中某一类方向边缘。",
        "pros": ["方向信息明确。", "适合针对性检测特定方向结构。"],
        "limits": ["单方向算子容易漏掉其他方向边缘。", "响应强度受噪声和纹理干扰。"],
        "compare": ["方向性一阶算子 vs Canny：前者只给局部梯度，Canny 还包含平滑、细化和连接。", "单方向响应 vs 综合梯度幅值：前者可解释性强，后者边缘覆盖更完整。"],
        "links": ["[[05_图像锐化/5.2_一阶微分算子|一阶微分算子]]", "[[05_图像锐化/5.4_微分算子在边缘检测中的应用|微分算子在边缘检测中的应用]]"],
        "review": ["为什么水平差分常检测垂直边缘？", "只用一个方向模板会有什么风险？", "方向响应如何合成成一张边缘强度图？"],
    },
    {
        "file": "5.2.2_Roberts交叉微分算子.md",
        "title": "5.2.2 Roberts交叉微分算子",
        "section": "第 5 章 图像锐化",
        "subsection": "5.2.2 Roberts交叉微分算子",
        "figure": "ch05_roberts_sobel_prewitt.png",
        "code": "roberts_operator.py",
        "concept": "Roberts 算子使用 2x2 交叉差分模板，估计两个对角方向的灰度变化。窗口很小，所以定位精细，但几乎没有平滑能力，对噪声非常敏感。",
        "formula": ["常用模板：\\(K_1=\\begin{bmatrix}1&0\\\\0&-1\\end{bmatrix}\\)，\\(K_2=\\begin{bmatrix}0&1\\\\-1&0\\end{bmatrix}\\)。", "响应：\\(M=\\sqrt{(f*K_1)^2+(f*K_2)^2}\\)。"],
        "steps": ["输入灰度图。", "使用两个 2x2 Roberts 交叉模板卷积。", "计算两个方向响应的幅值。", "归一化并按阈值输出边缘。"],
        "intuition": "Roberts 直接比较小方块的两条对角线，如果对角方向亮暗变化很大，就认为那里有边缘。",
        "scene": "噪声较低、边缘较清晰的小图像快速边缘检测。",
        "pros": ["模板小，计算快。", "边缘定位较敏感。"],
        "limits": ["抗噪能力弱。", "对水平/垂直方向边缘的表达不如 Sobel 直观。"],
        "compare": ["Roberts vs Sobel：Roberts 更局部，Sobel 用 3x3 加权平滑更稳。", "Roberts vs Prewitt：Roberts 是 2x2 交叉差分，Prewitt 是 3x3 方向差分。"],
        "links": ["[[05_图像锐化/5.2_一阶微分算子|一阶微分算子]]", "[[05_图像锐化/5.2.3_Sobel微分算子|Sobel微分算子]]"],
        "review": ["Roberts 的两个模板为什么叫交叉差分？", "为什么 Roberts 对噪声敏感？", "什么场景下 Roberts 仍然有价值？"],
    },
    {
        "file": "5.2.3_Sobel微分算子.md",
        "title": "5.2.3 Sobel微分算子",
        "section": "第 5 章 图像锐化",
        "subsection": "5.2.3 Sobel微分算子",
        "figure": "ch05_roberts_sobel_prewitt.png",
        "code": "sobel_operator.py",
        "concept": "Sobel 算子在差分的同时引入垂直于差分方向的加权平滑。中间行或中间列权重为 2，使它比简单差分更稳定，是经典边缘检测和梯度计算的常用算子。",
        "formula": ["\\(K_x=\\begin{bmatrix}-1&0&1\\\\-2&0&2\\\\-1&0&1\\end{bmatrix}\\)，\\(K_y=K_x^T\\)。", "边缘强度：\\(M=\\sqrt{(f*K_x)^2+(f*K_y)^2}\\)。"],
        "steps": ["输入灰度图。", "用 Sobel x/y 模板计算两个方向梯度。", "计算幅值，可选计算方向。", "根据应用做归一化、阈值化或作为 Canny 的前置梯度。"],
        "intuition": "Sobel 不是只看左右两个像素，而是把邻域里多行/多列一起看，中间线权重更高，所以对孤立噪声没那么冲动。",
        "scene": "通用边缘检测、纹理梯度、目标轮廓增强、Canny 前的梯度估计。",
        "pros": ["方向明确，抗噪性比 Roberts 更好。", "OpenCV 等库支持完善。", "可直接输出 x/y 梯度。"],
        "limits": ["仍然是局部线性算子，对强噪声需要预平滑。", "边缘可能较粗，需要后续细化。"],
        "compare": ["Sobel vs Prewitt：Sobel 中心权重更大，平滑和差分结合更强。", "Sobel vs Canny：Sobel 给梯度图，Canny 在此基础上做细化和连接。"],
        "links": ["[[05_图像锐化/5.5_Canny算子|Canny算子]]", "[[05_图像锐化/5.2.4_Priwitt微分算子|Priwitt微分算子]]"],
        "review": ["Sobel 模板中权重 2 的作用是什么？", "Sobel 输出的边缘为什么可能较粗？", "Sobel 和 Canny 的关系是什么？"],
    },
    {
        "file": "5.2.4_Priwitt微分算子.md",
        "title": "5.2.4 Priwitt微分算子",
        "section": "第 5 章 图像锐化",
        "subsection": "5.2.4 Priwitt微分算子",
        "figure": "ch05_roberts_sobel_prewitt.png",
        "code": "prewitt_operator.py",
        "concept": "Priwitt 算子通常也写作 Prewitt 算子，使用 3x3 均匀方向差分模板。它比 Roberts 有更大的邻域，但不像 Sobel 那样强调中心行列。",
        "formula": ["\\(K_x=\\begin{bmatrix}-1&0&1\\\\-1&0&1\\\\-1&0&1\\end{bmatrix}\\)，\\(K_y=K_x^T\\)。", "响应：\\(M=\\sqrt{(f*K_x)^2+(f*K_y)^2}\\)。"],
        "steps": ["输入灰度图。", "用 Prewitt x/y 模板卷积。", "计算综合梯度幅值。", "按阈值获得边缘候选。"],
        "intuition": "Prewitt 相当于先在一个方向上做简单平均，再在另一个方向上看亮暗差；它更朴素，权重也更均匀。",
        "scene": "教学演示、简单边缘检测、对模板权重差异进行实验比较。",
        "pros": ["形式简单，易于手算和解释。", "比 2x2 差分更稳定。"],
        "limits": ["抗噪性通常弱于 Sobel。", "边缘定位和方向精度受模板粗糙程度限制。"],
        "compare": ["Prewitt vs Sobel：Prewitt 权重均匀，Sobel 强调中心行列。", "Prewitt vs Roberts：Prewitt 使用 3x3 邻域，对噪声稍稳但边缘定位更宽。"],
        "links": ["[[05_图像锐化/5.2.2_Roberts交叉微分算子|Roberts交叉微分算子]]", "[[05_图像锐化/5.2.3_Sobel微分算子|Sobel微分算子]]"],
        "review": ["Prewitt 为什么比 Roberts 更平滑？", "Prewitt 和 Sobel 的模板差别在哪里？", "为什么教材和代码中可能同时出现 Priwitt/Prewitt 两种写法？"],
    },
    {
        "file": "5.3_二阶微分算子.md",
        "title": "5.3 二阶微分算子",
        "section": "第 5 章 图像锐化",
        "subsection": "5.3 二阶微分算子",
        "figure": "ch05_laplacian_sharpening.png",
        "code": "laplacian_operator.py",
        "concept": "二阶微分关注灰度变化率本身的变化，也就是曲率或转折。它对细节和孤立点很敏感，常用于增强边缘、检测零交叉或构造锐化图像。",
        "formula": ["连续形式：\\(\\nabla^2 f=\\partial^2 f/\\partial x^2+\\partial^2 f/\\partial y^2\\)。", "离散 4 邻域模板可写为：\\(\\begin{bmatrix}0&1&0\\\\1&-4&1\\\\0&1&0\\end{bmatrix}\\)，符号约定需人工复核。"],
        "steps": ["输入灰度图，必要时先平滑。", "用二阶差分模板卷积。", "根据符号约定将二阶响应加回或从原图中减去。", "裁剪到有效灰度范围得到锐化结果。"],
        "intuition": "一阶算子看坡度，二阶算子看坡度怎么变；在边缘附近，坡度变化最剧烈，所以二阶响应明显。",
        "scene": "图像细节增强、边缘细化、LoG 零交叉检测、医学和工业图像轮廓增强。",
        "pros": ["对细小结构敏感。", "方向无关的 Laplacian 形式简单。"],
        "limits": ["极易放大噪声。", "符号约定不同会影响“加还是减”的实现。", "可能产生过冲和光晕。"],
        "compare": ["二阶微分 vs 一阶微分：二阶更敏感但更怕噪声。", "Laplacian vs LoG：LoG 先平滑再二阶微分，抗噪更好。"],
        "links": ["[[05_图像锐化/5.3.1_Laplacian微分算子|Laplacian微分算子]]", "[[05_图像锐化/5.6_LOG滤波算法|LOG滤波算法]]", "[[04_图像去噪/4.2_均值滤波|均值滤波]]"],
        "review": ["为什么二阶微分比一阶微分更容易放大噪声？", "Laplacian 为什么可以看成方向无关算子？", "锐化时为什么要注意模板符号？"],
    },
    {
        "file": "5.3.1_Laplacian微分算子.md",
        "title": "5.3.1 Laplacian微分算子",
        "section": "第 5 章 图像锐化",
        "subsection": "5.3.1 Laplacian微分算子",
        "figure": "ch05_laplacian_sharpening.png",
        "code": "laplacian_operator.py",
        "concept": "Laplacian 是最常见的二阶微分算子，把 x 和 y 两个方向的二阶差分相加。它不直接给边缘方向，重点是突出灰度变化的转折位置。",
        "formula": ["\\(\\nabla^2 f=f(x+1,y)+f(x-1,y)+f(x,y+1)+f(x,y-1)-4f(x,y)\\)。", "锐化形式常写为：\\(g=f-c\\nabla^2 f\\) 或 \\(g=f+c\\nabla^2 f\\)，取决于模板符号，需人工复核。"],
        "steps": ["输入灰度图。", "计算 Laplacian 响应。", "按模板符号将响应与原图组合。", "归一化或裁剪输出锐化图。"],
        "intuition": "如果一个像素和四周差异很大，Laplacian 响应就大；把这个响应反馈到原图，就能让局部细节更突出。",
        "scene": "文字增强、纹理强化、边缘预突出、教学中观察二阶差分效果。",
        "pros": ["模板简单，方向无关。", "对点、线和细边缘响应强。"],
        "limits": ["对噪声和压缩块效应敏感。", "不提供边缘方向。", "锐化强度过大会产生过冲。"],
        "compare": ["Laplacian vs Sobel：Laplacian 是二阶无方向响应，Sobel 是一阶方向响应。", "Laplacian vs LoG：LoG 在 Laplacian 前加入高斯平滑。"],
        "links": ["[[05_图像锐化/5.2.3_Sobel微分算子|Sobel微分算子]]", "[[05_图像锐化/5.6_LOG滤波算法|LOG滤波算法]]"],
        "review": ["Laplacian 为什么没有显式方向？", "锐化时响应应加还是减由什么决定？", "如何缓解 Laplacian 放大噪声的问题？"],
    },
    {
        "file": "5.3.2_Wallis微分算子.md",
        "title": "5.3.2 Wallis微分算子",
        "section": "第 5 章 图像锐化",
        "subsection": "5.3.2 Wallis微分算子",
        "figure": "ch05_laplacian_sharpening.png",
        "code": "laplacian_operator.py",
        "concept": "Wallis 微分算子可理解为一类用于增强局部细节的二阶或高通锐化思想。不同资料对模板形式和符号写法可能不完全一致，本知识库先按“局部高频增强”整理，具体原书模板需人工复核。",
        "formula": ["局部高通增强的一般形式：\\(g=f+\\lambda H(f)\\)，其中 \\(H(f)\\) 表示高频或二阶响应。", "若使用 Wallis 原书模板，模板系数和符号需对照 PDF 人工复核。"],
        "steps": ["输入灰度图。", "按 Wallis 或高通模板计算局部细节响应。", "用系数控制响应叠加强度。", "裁剪灰度范围输出。"],
        "intuition": "它的核心不是改变整体亮度，而是把局部起伏从原图里提出来再加回去，让细节更明显。",
        "scene": "局部对比度不足但边缘结构存在的图像、扫描件细节增强、纹理可视化。",
        "pros": ["可作为 Laplacian 锐化的扩展理解。", "便于讨论增强强度和高频响应的关系。"],
        "limits": ["原书符号和模板需复核。", "参数不当会增强噪声和伪影。"],
        "compare": ["Wallis vs Laplacian：都强调局部高频，但 Wallis 的具体模板和增强策略需按原书定义。", "Wallis vs 灰度增强：前者偏空间细节，后者偏灰度映射。"],
        "links": ["[[05_图像锐化/5.3.1_Laplacian微分算子|Laplacian微分算子]]", "[[02_图像增强/2.2_对比度线性展宽|对比度线性展宽]]"],
        "review": ["为什么 Wallis 算子需要人工复核模板？", "局部高频增强和全局对比度增强有什么区别？", "增强系数过大会出现什么现象？"],
    },
    {
        "file": "5.4_微分算子在边缘检测中的应用.md",
        "title": "5.4 微分算子在边缘检测中的应用",
        "section": "第 5 章 图像锐化",
        "subsection": "5.4 微分算子在边缘检测中的应用",
        "figure": "ch05_canny_pipeline.png",
        "code": "canny_edge_detection.py",
        "concept": "微分算子通常只是边缘检测的一步。完整边缘检测还要考虑噪声抑制、响应阈值、边缘细化和连通性，否则输出容易出现粗边缘、断裂边缘或噪声点。",
        "formula": ["边缘候选可由阈值给出：\\(E(x,y)=1\\) if \\(M(x,y)>T\\)，否则为 0。", "双阈值连接可抽象为强边缘 \\(M>T_h\\) 和弱边缘 \\(T_l<M\\le T_h\\) 的连通筛选。"],
        "steps": ["先平滑抑制噪声。", "用一阶或二阶算子计算边缘响应。", "进行阈值化或非极大值抑制。", "连接可信边缘，去除孤立噪声响应。"],
        "intuition": "直接微分像把所有变化都喊出来；边缘检测还要判断哪些变化是真边界，哪些只是噪声或纹理。",
        "scene": "目标轮廓提取、车道线检测、文字边缘、分割算法的前置边界提示。",
        "pros": ["把锐化响应转化为结构化边缘图。", "能服务后续分割、识别和测量。"],
        "limits": ["阈值和预平滑参数会影响结果。", "纹理密集区域容易产生过多边缘。"],
        "compare": ["简单阈值边缘 vs Canny：Canny 通过非极大值抑制和双阈值连接提升边缘质量。", "边缘检测 vs 图像锐化：前者输出结构位置，后者常输出增强图像。"],
        "links": ["[[05_图像锐化/5.5_Canny算子|Canny算子]]", "[[06_图像的分割|图像分割]]"],
        "review": ["为什么微分响应不能直接等同于最终边缘？", "强边缘和弱边缘的连接有什么意义？", "边缘检测如何服务图像分割？"],
    },
    {
        "file": "5.5_Canny算子.md",
        "title": "5.5 Canny算子",
        "section": "第 5 章 图像锐化",
        "subsection": "5.5 Canny算子",
        "figure": "ch05_canny_pipeline.png",
        "code": "canny_edge_detection.py",
        "concept": "Canny 是多阶段边缘检测方法：先用高斯平滑降噪，再计算梯度，然后用非极大值抑制细化边缘，最后用双阈值和滞后连接保留可信边缘。",
        "formula": ["高斯平滑：\\(I_s=G_\\sigma * I\\)。", "梯度幅值：\\(M=\\sqrt{G_x^2+G_y^2}\\)。", "双阈值：强边缘 \\(M\\ge T_h\\)，弱边缘 \\(T_l\\le M<T_h\\)。"],
        "steps": ["输入灰度图。", "高斯滤波平滑。", "用 Sobel 等算子计算梯度幅值和方向。", "沿梯度方向做非极大值抑制。", "使用高低阈值连接边缘。"],
        "intuition": "Canny 不急着把每个响应都当边缘，而是先降噪、再找局部最大、再把可靠边缘周围的弱边缘接上。",
        "scene": "通用轮廓检测、自动标注辅助、几何测量、后续霍夫变换或轮廓分析前处理。",
        "pros": ["边缘较细，噪声响应较少。", "双阈值连接能减少断裂。", "工程中成熟稳定。"],
        "limits": ["参数较多，低/高阈值和高斯尺度需调。", "弱纹理和真实弱边缘可能混淆。"],
        "compare": ["Canny vs Sobel：Sobel 是 Canny 的梯度基础之一，Canny 是完整边缘检测流程。", "Canny vs LoG：Canny 强调方向细化和连接，LoG 强调平滑后二阶响应。"],
        "links": ["[[05_图像锐化/5.2.3_Sobel微分算子|Sobel微分算子]]", "[[05_图像锐化/5.6_LOG滤波算法|LOG滤波算法]]"],
        "review": ["Canny 为什么需要非极大值抑制？", "双阈值中的弱边缘为什么不能全部丢弃？", "高斯平滑尺度对 Canny 有什么影响？"],
    },
    {
        "file": "5.6_LOG滤波算法.md",
        "title": "5.6 LOG滤波算法",
        "section": "第 5 章 图像锐化",
        "subsection": "5.6 LOG滤波算法",
        "figure": "ch05_log_filter.png",
        "code": "log_filter.py",
        "concept": "LOG 即 Laplacian of Gaussian，先用高斯滤波抑制噪声，再用 Laplacian 检测二阶变化。它把平滑和二阶边缘响应合成一个思想，常用于零交叉边缘检测。",
        "formula": ["\\(LoG(x,y)=\\nabla^2 G_\\sigma(x,y)\\)。", "等价计算思路：\\(R=\\nabla^2(G_\\sigma * I)\\)。", "零交叉处可作为边缘候选，阈值规则需人工复核。"],
        "steps": ["输入灰度图。", "选择高斯尺度 \\(\\sigma\\)。", "先平滑，再计算 Laplacian，或直接用 LoG 模板卷积。", "寻找响应符号变化且幅值足够的位置。", "输出边缘或细节响应图。"],
        "intuition": "Laplacian 很怕噪声，所以 LoG 先把小噪声压下去，再寻找真正的灰度转折。",
        "scene": "噪声存在时的二阶边缘检测、尺度空间边缘分析、Blob 或轮廓预检测教学实验。",
        "pros": ["比裸 Laplacian 更抗噪。", "尺度参数能控制检测粗细。"],
        "limits": ["尺度过小仍受噪声影响，尺度过大可能抹掉细节。", "零交叉判定实现比简单阈值复杂。"],
        "compare": ["LoG vs Laplacian：LoG 先平滑再二阶微分。", "LoG vs Canny：LoG 用二阶零交叉思想，Canny 用一阶梯度、非极大值抑制和双阈值连接。"],
        "links": ["[[05_图像锐化/5.3.1_Laplacian微分算子|Laplacian微分算子]]", "[[05_图像锐化/5.5_Canny算子|Canny算子]]", "[[04_图像去噪/4.2_均值滤波|均值滤波]]"],
        "review": ["LoG 为什么要先做高斯平滑？", "尺度 \\(\\sigma\\) 变大后边缘结果会怎样？", "LoG 和 Canny 的核心差异是什么？"],
    },
    {
        "file": "5.x_习题.md",
        "title": "5.x 习题",
        "section": "第 5 章 图像锐化",
        "subsection": "5.x 习题",
        "figure": "ch05_canny_pipeline.png",
        "code": None,
        "concept": "本章习题应围绕“微分为什么能锐化、噪声为什么会被放大、不同算子如何取舍、边缘检测如何从响应走向结构化结果”展开，而不是只记模板。",
        "formula": ["复习重点：一阶梯度、Laplacian 二阶差分、Sobel/Prewitt/Roberts 模板、Canny 双阈值、LoG 平滑后二阶响应。"],
        "steps": ["先画出灰度剖面。", "判断适合用一阶还是二阶方法。", "写出对应模板或公式。", "解释参数对噪声、边缘宽度和断裂的影响。", "用示例代码验证直觉。"],
        "intuition": "做题时别只背名字，先问图像里要增强的是什么：边缘、细线、点、纹理，还是完整可连接的轮廓。",
        "scene": "期末复习、实验报告、代码参数解释、方法选型对比。",
        "pros": ["帮助把公式、图示和代码连起来。", "便于检查自己是否理解方法取舍。"],
        "limits": ["页码、原书题号和部分 Wallis 细节仍需人工复核。"],
        "compare": ["Roberts、Prewitt、Sobel 适合比较模板大小和抗噪性。", "Laplacian、LoG、Canny 适合比较二阶响应、预平滑和完整流程。"],
        "links": ["[[05_图像锐化/5.2_一阶微分算子|一阶微分算子]]", "[[05_图像锐化/5.3_二阶微分算子|二阶微分算子]]", "[[05_图像锐化/5.5_Canny算子|Canny算子]]"],
        "review": ["给定噪声较大的图像，应先锐化还是先平滑？为什么？", "比较 Roberts、Prewitt、Sobel 的模板和抗噪能力。", "说明 Canny 的五个主要步骤。", "LoG 中高斯尺度如何影响边缘检测结果？"],
    },
]


def status_block(profile: dict[str, object]) -> str:
    return f"""## 来源与状态

- 书名：数字图像处理基础
- 作者：朱虹
- 章节：{profile["section"]}
- 小节：{profile["subsection"]}
- 书中页码：需人工复核
- PDF 页码：需人工复核
- 本地 PDF：{PDF}
- 处理状态：已精修 / 需人工复核
"""


def render(profile: dict[str, object]) -> str:
    title = str(profile["title"])
    figure = str(profile["figure"])
    code = profile["code"]
    code_line = "本节偏概念复习，无单独代码；可结合本章其他示例运行。" if code is None else f"[{code}](../../examples/05_image_sharpening/{code})"
    formulas = "\n".join(f"- {item}" for item in profile["formula"])
    steps = "\n".join(f"{index}. {item}" for index, item in enumerate(profile["steps"], 1))
    pros = "\n".join(f"- {item}" for item in profile["pros"])
    limits = "\n".join(f"- {item}" for item in profile["limits"])
    compares = "\n".join(f"- {item}" for item in profile["compare"])
    links = "\n".join(f"- {item}" for item in profile["links"])
    review = "\n".join(f"{index}. {item}" for index, item in enumerate(profile["review"], 1))
    return f"""# {title}

> [!note] 书中对应页
> PDF 页码：{PDF_PAGE_NEEDS_REVIEW}
> 打开原页（Obsidian）：[[{PDF}#page={PDF_PAGE_NEEDS_REVIEW}]]
>
> GitHub 公开仓库不随附原书 PDF；下载仓库后，将有权使用的同名 PDF 放入 `raw/books/`，下面的 Obsidian 本地内嵌预览才会显示。
> ![[{PDF}#page={PDF_PAGE_NEEDS_REVIEW}]]

{status_block(profile)}

## 核心概念

{profile["concept"]}

## 关键公式

{formulas}

## 算法步骤

{steps}

## 直观理解

{profile["intuition"]}

## 使用场景

{profile["scene"]}

## 优点

{pros}

## 局限性

{limits}

## 和相关方法的对比

{compares}

## 教学图示

![{title}](../../assets/extracted_figures/{figure})

## 对应代码

{code_line}

## 相关知识

{links}

## 复习问题

{review}
"""


def refine_wiki() -> None:
    WIKI.mkdir(parents=True, exist_ok=True)
    for profile in PROFILES:
        (WIKI / str(profile["file"])).write_text(render(profile), encoding="utf-8")
    readme = """# 第 5 章 图像锐化

本章已升级为精品样板章节，重点整理图像细节、一阶微分算子、二阶微分算子、Canny 和 LoG。所有笔记均保留来源状态、公式、步骤、原创教学图示、代码链接、方法对比和复习问题。

## 小节

- [[5.1_图像细节的基本特征]]
- [[5.2_一阶微分算子]]
- [[5.2.1_具有方向性的一阶微分算子]]
- [[5.2.2_Roberts交叉微分算子]]
- [[5.2.3_Sobel微分算子]]
- [[5.2.4_Priwitt微分算子]]
- [[5.3_二阶微分算子]]
- [[5.3.1_Laplacian微分算子]]
- [[5.3.2_Wallis微分算子]]
- [[5.4_微分算子在边缘检测中的应用]]
- [[5.5_Canny算子]]
- [[5.6_LOG滤波算法]]
- [[5.x_习题]]
"""
    (WIKI / "README.md").write_text(readme, encoding="utf-8")


def add_semantic_edges() -> None:
    path = ROOT / "graph" / "semantic_edges.json"
    data = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"nodes": [], "edges": []}
    nodes = {node["id"]: node for node in data.get("nodes", [])}
    edges = {(edge["source"], edge["target"], edge["type"]) for edge in data.get("edges", [])}

    def node(node_id: str, label: str, kind: str = "concept") -> None:
        nodes[node_id] = {"id": node_id, "label": label, "kind": kind}

    def edge(source: str, target: str, relation: str) -> None:
        edges.add((source, target, relation))

    concepts = [
        ("wiki/05_图像锐化/5.1_图像细节的基本特征.md", "图像细节"),
        ("wiki/05_图像锐化/5.2_一阶微分算子.md", "一阶微分算子"),
        ("wiki/05_图像锐化/5.2.2_Roberts交叉微分算子.md", "Roberts 算子"),
        ("wiki/05_图像锐化/5.2.3_Sobel微分算子.md", "Sobel 算子"),
        ("wiki/05_图像锐化/5.2.4_Priwitt微分算子.md", "Prewitt 算子"),
        ("wiki/05_图像锐化/5.3_二阶微分算子.md", "二阶微分算子"),
        ("wiki/05_图像锐化/5.3.1_Laplacian微分算子.md", "Laplacian 算子"),
        ("wiki/05_图像锐化/5.5_Canny算子.md", "Canny 算子"),
        ("wiki/05_图像锐化/5.6_LOG滤波算法.md", "LoG 滤波"),
    ]
    for node_id, label in concepts:
        node(node_id, label)
    for code in ["roberts_operator.py", "sobel_operator.py", "prewitt_operator.py", "laplacian_operator.py", "canny_edge_detection.py", "log_filter.py"]:
        node(f"examples/05_image_sharpening/{code}", code, "code")
    for formula in ["梯度幅值公式", "Roberts 交叉差分模板", "Sobel 差分模板", "Prewitt 差分模板", "Laplacian 二阶差分", "Canny 双阈值", "LoG 公式"]:
        node(f"formula/ch05/{formula}", formula, "formula")

    edge("wiki/05_图像锐化/5.2_一阶微分算子.md", "wiki/05_图像锐化/5.1_图像细节的基本特征.md", "PREREQUISITE")
    edge("wiki/05_图像锐化/5.3_二阶微分算子.md", "wiki/05_图像锐化/5.1_图像细节的基本特征.md", "PREREQUISITE")
    for child in [
        "wiki/05_图像锐化/5.2.2_Roberts交叉微分算子.md",
        "wiki/05_图像锐化/5.2.3_Sobel微分算子.md",
        "wiki/05_图像锐化/5.2.4_Priwitt微分算子.md",
    ]:
        edge(child, "wiki/05_图像锐化/5.2_一阶微分算子.md", "GENERALIZES")
        edge(child, "formula/ch05/梯度幅值公式", "USES_FORMULA")
    edge("wiki/05_图像锐化/5.2.2_Roberts交叉微分算子.md", "formula/ch05/Roberts 交叉差分模板", "USES_FORMULA")
    edge("wiki/05_图像锐化/5.2.3_Sobel微分算子.md", "formula/ch05/Sobel 差分模板", "USES_FORMULA")
    edge("wiki/05_图像锐化/5.2.4_Priwitt微分算子.md", "formula/ch05/Prewitt 差分模板", "USES_FORMULA")
    edge("wiki/05_图像锐化/5.3.1_Laplacian微分算子.md", "wiki/05_图像锐化/5.3_二阶微分算子.md", "GENERALIZES")
    edge("wiki/05_图像锐化/5.3.1_Laplacian微分算子.md", "formula/ch05/Laplacian 二阶差分", "USES_FORMULA")
    edge("wiki/05_图像锐化/5.6_LOG滤波算法.md", "wiki/05_图像锐化/5.3.1_Laplacian微分算子.md", "IMPROVES_OR_EXTENDS")
    edge("wiki/05_图像锐化/5.6_LOG滤波算法.md", "formula/ch05/LoG 公式", "USES_FORMULA")
    edge("wiki/05_图像锐化/5.5_Canny算子.md", "wiki/05_图像锐化/5.2.3_Sobel微分算子.md", "PREREQUISITE")
    edge("wiki/05_图像锐化/5.5_Canny算子.md", "formula/ch05/Canny 双阈值", "USES_FORMULA")
    edge("wiki/05_图像锐化/5.5_Canny算子.md", "wiki/05_图像锐化/5.6_LOG滤波算法.md", "COMPARES_WITH")
    edge("wiki/05_图像锐化/5.2_一阶微分算子.md", "wiki/04_图像去噪/4.1_图像噪声.md", "APPLIES_TO")
    edge("wiki/05_图像锐化/5.3_二阶微分算子.md", "wiki/04_图像去噪/4.1_图像噪声.md", "APPLIES_TO")
    for wiki, code in [
        ("5.2.2_Roberts交叉微分算子.md", "roberts_operator.py"),
        ("5.2.3_Sobel微分算子.md", "sobel_operator.py"),
        ("5.2.4_Priwitt微分算子.md", "prewitt_operator.py"),
        ("5.3.1_Laplacian微分算子.md", "laplacian_operator.py"),
        ("5.5_Canny算子.md", "canny_edge_detection.py"),
        ("5.6_LOG滤波算法.md", "log_filter.py"),
    ]:
        edge(f"wiki/05_图像锐化/{wiki}", f"examples/05_image_sharpening/{code}", "IMPLEMENTED_BY")

    data = {
        "nodes": sorted(nodes.values(), key=lambda item: item["id"]),
        "edges": [{"source": s, "target": t, "type": r} for s, t, r in sorted(edges)],
    }
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_docs() -> None:
    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    text = text.replace(
        "- 第 5 章到第 11 章仍在同一分支继续精修，当前不拆分独立分支，避免后续配置分散。",
        "- 第 5 章“图像锐化”已升级为精品样板，包含原创图示、独立代码示例和语义图谱关系。\n- 第 6 章到第 11 章仍在同一分支继续精修，当前不拆分独立分支，避免后续配置分散。",
    )
    if "第 5 章图像锐化示例：" not in text:
        marker = "默认输入为 `assets/sample_images/` 中的合成图片，输出写入 `examples/output/`，该目录已被 `.gitignore` 忽略。"
        block = """第 5 章图像锐化示例：

```powershell
python examples/05_image_sharpening/sobel_operator.py --kernel-size 3 --direction both
python examples/05_image_sharpening/laplacian_operator.py --amount 0.7
python examples/05_image_sharpening/canny_edge_detection.py --low 60 --high 160
python examples/05_image_sharpening/log_filter.py --sigma 1.2
```

"""
        text = text.replace(marker, block + marker)
    text = text.replace("补充第 3 章和第 4 章语义关系", "补充第 3 章、第 4 章和第 5 章语义关系")
    readme.write_text(text, encoding="utf-8")

    coverage = ROOT / "coverage_report.md"
    ctext = coverage.read_text(encoding="utf-8")
    ctext = ctext.replace(
        "- 第 5 章到第 11 章：仍在同一分支继续精修，后续按第 2/3/4 章样板逐章推进。",
        "- 第 5 章：已精修为第四个精品样板，新增原创锐化图示、独立可运行示例和语义图谱关系。\n- 第 6 章到第 11 章：仍在同一分支继续精修，后续按第 2/3/4/5 章样板逐章推进。",
    )
    if "## 第 5 章处理记录" not in ctext:
        ctext += """

## 第 5 章处理记录

- 处理的 wiki 文件：`5.1_图像细节的基本特征.md`、`5.2_一阶微分算子.md`、`5.2.1_具有方向性的一阶微分算子.md`、`5.2.2_Roberts交叉微分算子.md`、`5.2.3_Sobel微分算子.md`、`5.2.4_Priwitt微分算子.md`、`5.3_二阶微分算子.md`、`5.3.1_Laplacian微分算子.md`、`5.3.2_Wallis微分算子.md`、`5.4_微分算子在边缘检测中的应用.md`、`5.5_Canny算子.md`、`5.6_LOG滤波算法.md`、`5.x_习题.md`。
- 新增原创教学图示：`ch05_detail_profiles.png`、`ch05_first_derivative_kernels.png`、`ch05_roberts_sobel_prewitt.png`、`ch05_laplacian_sharpening.png`、`ch05_canny_pipeline.png`、`ch05_log_filter.png`。
- 优化代码：`roberts_operator.py`、`sobel_operator.py`、`prewitt_operator.py`、`laplacian_operator.py`、`canny_edge_detection.py`、`log_filter.py`，并新增第 5 章 `_utils.py`。
- 新增图谱关系：一阶/二阶微分的 `PREREQUISITE`，算子归属的 `GENERALIZES`，公式依赖的 `USES_FORMULA`，代码实现的 `IMPLEMENTED_BY`，Canny/LoG 对比的 `COMPARES_WITH`，以及锐化与噪声敏感性的 `APPLIES_TO`。
- 仍需人工复核：原书页码、Wallis 算子模板、Laplacian 符号约定和零交叉判定细节。
- 未完成内容：未加入原书截图和原始文本；后续可继续增加真实实验指标，如边缘连通性、噪声敏感性和阈值曲线。
"""
    coverage.write_text(ctext, encoding="utf-8")

    graph_readme = ROOT / "graph" / "README.md"
    gtext = graph_readme.read_text(encoding="utf-8")
    gtext = gtext.replace("第 3 章和第 4 章的额外语义关系", "第 3 章、第 4 章和第 5 章的额外语义关系")
    graph_readme.write_text(gtext, encoding="utf-8")

    examples_readme = EX / "README.md"
    examples_readme.write_text(
        """# 第 5 章 图像锐化代码示例

这些脚本默认使用 `assets/sample_images/sample_gray.png`，输出写入 `examples/output/`。

```powershell
python examples/05_image_sharpening/roberts_operator.py --scale 1.0
python examples/05_image_sharpening/sobel_operator.py --kernel-size 3 --direction both
python examples/05_image_sharpening/prewitt_operator.py --direction both
python examples/05_image_sharpening/laplacian_operator.py --amount 0.7 --kernel-size 3
python examples/05_image_sharpening/canny_edge_detection.py --low 60 --high 160
python examples/05_image_sharpening/log_filter.py --sigma 1.2 --kernel-size 5
```

所有输入图片均为可自由提交的合成样例，不使用原书图片。
""",
        encoding="utf-8",
    )

    glossary = ROOT / "wiki" / "99_术语表.md"
    glossary_text = glossary.read_text(encoding="utf-8")
    if "## 图像锐化" not in glossary_text:
        glossary_text += """

## 图像锐化

- 一阶微分算子：用局部差分估计梯度，常用于边缘检测。
- Roberts 算子：2x2 交叉差分算子，定位敏感但抗噪弱。
- Sobel 算子：3x3 加权差分算子，兼顾方向梯度和局部平滑。
- Laplacian 算子：二阶微分算子，强调灰度变化的转折。
- Canny 算子：包含平滑、梯度、非极大值抑制和双阈值连接的边缘检测流程。
- LoG：高斯平滑后进行 Laplacian 二阶检测的边缘方法。
"""
        glossary.write_text(glossary_text, encoding="utf-8")


def main() -> None:
    refine_wiki()
    add_semantic_edges()
    update_docs()
    print("Refined chapter 5 sharpening content.")


if __name__ == "__main__":
    main()
