# Mermaid 知识图谱

> 轻量关系视图，仅展示章节包含关系和人工维护的强语义关系。主入口请使用 Obsidian Canvas。

```mermaid
graph TD
  wiki_01____1_1____________________["1.1_数字图像处理、计算机视觉、计算机图形学"]
  wiki_01____1_2____________["1.2_数字图像处理系统的结构"]
  wiki_01____1_3_1__________["1.3.1_数字图像的数值描述"]
  wiki_01____1_3_2___________["1.3.2_数字图像的灰度直方图"]
  wiki_01____1_3__________["1.3_数字图像的基本概念"]
  wiki_01____1_4______________["1.4_数字图像处理的主要研究内容"]
  wiki_01____1_5________["1.5_本书的结构安排"]
  wiki_01____1_x___["1.x_习题"]
  wiki_01____README["01_引言"]
  wiki_02______2_1____["2.1_γ校正"]
  wiki_02______2_2________["2.2_对比度线性展宽"]
  wiki_02______2_3_1____["2.3.1_灰级窗"]
  wiki_02______2_3_2______["2.3.2_灰级窗切片"]
  wiki_02______2_3__________["2.3_灰级窗与灰级窗切片"]
  wiki_02______2_4_1_________["2.4.1_线性动态范围调整"]
  wiki_02______2_4_2__________["2.4.2_非线性动态范围调整"]
  wiki_02______2_4_______["2.4_动态范围调整"]
  wiki_02______2_5_______["2.5_直方图均衡化"]
  wiki_02______2_6__________["2.6_自适应直方图均衡化"]
  wiki_02______2_7____["2.7_伪彩色"]
  wiki_02______2_8_Retinex______["2.8_Retinex图像增强方法"]
  wiki_02______2_x___["2.x_习题"]
  wiki_02______README["02_图像增强"]
  wiki_03________3_1_1______["3.1.1_图像的平移"]
  wiki_03________3_1_2______["3.1.2_图像的镜像"]
  wiki_03________3_1_3______["3.1.3_图像的旋转"]
  wiki_03________3_1________["3.1_图像的位置变换"]
  wiki_03________3_2_1______["3.2.1_图像的缩小"]
  wiki_03________3_2_2______["3.2.2_图像的放大"]
  wiki_03________3_2_3______["3.2.3_图像的错切"]
  wiki_03________3_2________["3.2_图像的形状变换"]
  wiki_03________3_3_____________["3.3_齐次坐标与图像的仿射变换"]
  wiki_03________3_4__________["3.4_图像几何畸变的校正"]
  wiki_03________3_x___["3.x_习题"]
  wiki_03________README["03_图像几何变换"]
  wiki_04______4_1_____["4.1_图像噪声"]
  wiki_04______4_2_1________["4.2.1_均值滤波的原理"]
  wiki_04______4_2_2_______["4.2.2_均值滤波方法"]
  wiki_04______4_2_____["4.2_均值滤波"]
  wiki_04______4_3_1________["4.3.1_中值滤波的原理"]
  wiki_04______4_3_2_______["4.3.2_中值滤波方法"]
  wiki_04______4_3_____["4.3_中值滤波"]
  wiki_04______4_4_1_K______["4.4.1_K近邻均值滤波"]
  wiki_04______4_4_2_________["4.4.2_对称近邻均值滤波"]
  wiki_04______4_4__________["4.4_边界保持类平滑滤波"]
  wiki_04______4_5________["4.5_非局部均值滤波"]
  wiki_04______4_x___["4.x_习题"]
  wiki_04______README["04_图像去噪"]
  wiki_05______5_1__________["5.1_图像细节的基本特征"]
  wiki_05______5_2_1_____________["5.2.1_具有方向性的一阶微分算子"]
  wiki_05______5_2_2_Roberts______["5.2.2_Roberts交叉微分算子"]
  wiki_05______5_2_3_Sobel____["5.2.3_Sobel微分算子"]
  wiki_05______5_2_4_Priwitt____["5.2.4_Priwitt微分算子"]
  wiki_05______5_2_______["5.2_一阶微分算子"]
  wiki_05______5_3_1_Laplacian____["5.3.1_Laplacian微分算子"]
  wiki_05______5_3_2_Wallis____["5.3.2_Wallis微分算子"]
  wiki_05______5_3_______["5.3_二阶微分算子"]
  wiki_05______5_4______________["5.4_微分算子在边缘检测中的应用"]
  wiki_05______5_5_Canny__["5.5_Canny算子"]
  wiki_05______5_6_LOG____["5.6_LOG滤波算法"]
  wiki_05______5_x___["5.x_习题"]
  wiki_05______README["05_图像锐化"]
  wiki_06_______6_1_1_p____["6.1.1_p-参数法"]
  wiki_06_______6_1_2______["6.1.2_最大熵方法"]
  wiki_06_______6_1_3____________["6.1.3_最大类间、类内方差比法"]
  wiki_06_______6_1_______["6.1_阈值分割方法"]
  wiki_06_______6_2_________["6.2_区域生长分割方法"]
  wiki_06_______6_x___["6.x_习题"]
  wiki_06_______README["06_图像的分割"]
  wiki_07________7_1_1_______["7.1.1_连接与点特性"]
  wiki_07________7_1_2_____["7.1.2_几何特征"]
  wiki_07________7_1___________["7.1_二值图像中的基本概念"]
  wiki_07________7_2_1___["7.2.1_腐蚀"]
  wiki_07________7_2_2___["7.2.2_膨胀"]
  wiki_07________7_2______["7.2_腐蚀与膨胀"]
  wiki_07________7_3_1____["7.3.1_开运算"]
  wiki_07________7_3_2____["7.3.2_闭运算"]
  wiki_07________7_3________["7.3_开运算与闭运算"]
  wiki_07________7_4_1_______["7.4.1_连通域标签法"]
  wiki_07________7_4_2______["7.4.2_轮廓标签法"]
  wiki_07________7_4____["7.4_贴标签"]
  wiki_07________7_5______["7.5_细线化方法"]
  wiki_07________7_x___["7.x_习题"]
  wiki_07________README["07_二值图像处理"]
  wiki_08________8_1_____________["8.1_彩色的形成原理与基本概念"]
  wiki_08________8_2_1_________["8.2.1_计算颜色模型系统"]
  wiki_08________8_2_2_________["8.2.2_视觉颜色模型系统"]
  wiki_08________8_2_3_________["8.2.3_工业颜色模型系统"]
  wiki_08________8_2____["8.2_表色系"]
  wiki_08________8_3_1_____["8.3.1_白平衡法"]
  wiki_08________8_3_2______["8.3.2_灰色世界法"]
  wiki_08________8_3_____["8.3_色彩平衡"]
  wiki_08________8_4_____["8.4_彩色补偿"]
  wiki_08________8_x___["8.x_习题"]
  wiki_08________README["08_彩色图像处理"]
  wiki_09______9_1_1________["9.1.1_一维傅里叶变换"]
  wiki_09______9_1_2________["9.1.2_二维傅里叶变换"]
  wiki_09______9_1_3_________FFT_["9.1.3_快速傅里叶变换（FFT）"]
  wiki_09______9_1_4__________["9.1.4_图像的频谱分布特性"]
  wiki_09______9_1_______________["9.1_图像的频域变换（傅里叶变换）"]
  wiki_09______9_2_1_______["9.2.1_连续小波变换"]
  wiki_09______9_2_2_______["9.2.2_离散小波变换"]
  wiki_09______9_2_3____________["9.2.3_小波的多尺度分解与重构"]
  wiki_09______9_2_____["9.2_小波变换"]
  wiki_09______9_3_1________["9.3.1_应用于图像压缩"]
  wiki_09______9_3_2________["9.3.2_应用于图像融合"]
  wiki_09______9_3_3________["9.3.3_应用于图像增强"]
  wiki_09______9_3_4________["9.3.4_应用于图像去噪"]
  wiki_09______9_3______________["9.3_小波变换在图像处理中的应用"]
  wiki_09______9_x___["9.x_习题"]
  wiki_09______README["09_图像变换"]
  wiki_10________10_1_1______["10.1.1_冗余的概念"]
  wiki_10________10_1_2_______["10.1.2_图像中的冗余"]
  wiki_10________10_1________["10.1_图像冗余的概念"]
  wiki_10________10_2_1______RLE_["10.2.1_行程编码（RLE）"]
  wiki_10________10_2_2_____Huffman___["10.2.2_哈夫曼（Huffman）编码"]
  wiki_10________10_2_________["10.2_图像无损压缩编码"]
  wiki_10________10_3_1__________["10.3.1_彩色图像的有损编码"]
  wiki_10________10_3_2_______["10.3.2_小波变换编码"]
  wiki_10________10_3_________["10.3_图像有损压缩编码"]
  wiki_10________10_x___["10.x_习题"]
  wiki_10________README["10_图像压缩编码"]
  wiki_11___________11_1_1____["11.1.1_卷积层"]
  wiki_11___________11_1_2____["11.1.2_激活层"]
  wiki_11___________11_1_3_BN____________["11.1.3_BN层（批数据归一化处理层）"]
  wiki_11___________11_1_4____["11.1.4_池化层"]
  wiki_11___________11_1____________["11.1_深度卷积网络的基本结构"]
  wiki_11___________11_2_1_SRCNN__["11.2.1_SRCNN网络"]
  wiki_11___________11_2_2_ESPCN__["11.2.2_ESPCN网络"]
  wiki_11___________11_2_____________["11.2_超分辨率图像重建卷积网络"]
  wiki_11___________11_3_1_LeNet_5__["11.3.1_LeNet-5网络"]
  wiki_11___________11_3_2_AlexNet__["11.3.2_AlexNet网络"]
  wiki_11___________11_3___________["11.3_图像分类深度卷积网络"]
  wiki_11___________11_4_1_Faster_RCNN__["11.4.1_Faster-RCNN网络"]
  wiki_11___________11_4_2_YOLO__["11.4.2_YOLO网络"]
  wiki_11___________11_4_____________["11.4_图像目标检测深度卷积网络"]
  wiki_11___________11_x___["11.x_习题"]
  wiki_11___________README["11_深度学习与图像处理"]
  wiki_98__________["参考文献"]
  concept_ch03_bilinear_interpolation["双线性插值"]
  concept_ch03_nearest_interpolation["最近邻插值"]
  concept_ch03_reverse_mapping["反向映射"]
  concept_ch04_gaussian_noise["高斯噪声"]
  concept_ch04_salt_pepper_noise["椒盐噪声"]
  examples_03_geometric_transform_affine_transform_py["affine_transform.py"]
  examples_03_geometric_transform_geometric_correction_py["geometric_correction.py"]
  examples_03_geometric_transform_image_resize_py["image_resize.py"]
  examples_03_geometric_transform_image_rotation_py["image_rotation.py"]
  examples_03_geometric_transform_image_shear_py["image_shear.py"]
  examples_03_geometric_transform_image_translation_py["image_translation.py"]
  examples_04_image_denoising_k_nearest_mean_filter_py["k_nearest_mean_filter.py"]
  examples_04_image_denoising_mean_filter_py["mean_filter.py"]
  examples_04_image_denoising_median_filter_py["median_filter.py"]
  examples_04_image_denoising_non_local_means_filter_py["non_local_means_filter.py"]
  examples_04_image_denoising_symmetric_nearest_mean_filter_py["symmetric_nearest_mean_filter.py"]
  examples_05_image_sharpening_canny_edge_detection_py["canny_edge_detection.py"]
  examples_05_image_sharpening_laplacian_operator_py["laplacian_operator.py"]
  examples_05_image_sharpening_log_filter_py["log_filter.py"]
  examples_05_image_sharpening_prewitt_operator_py["prewitt_operator.py"]
  examples_05_image_sharpening_roberts_operator_py["roberts_operator.py"]
  examples_05_image_sharpening_sobel_operator_py["sobel_operator.py"]
  examples_06_image_segmentation_max_entropy_threshold_py["max_entropy_threshold.py"]
  examples_06_image_segmentation_otsu_threshold_py["otsu_threshold.py"]
  examples_06_image_segmentation_region_growing_py["region_growing.py"]
  examples_06_image_segmentation_threshold_segmentation_py["threshold_segmentation.py"]
  examples_07_binary_image_processing_connected_component_labeling_py["connected_component_labeling.py"]
  examples_07_binary_image_processing_contour_labeling_py["contour_labeling.py"]
  examples_07_binary_image_processing_erosion_dilation_py["erosion_dilation.py"]
  examples_07_binary_image_processing_opening_closing_py["opening_closing.py"]
  examples_07_binary_image_processing_thinning_py["thinning.py"]
  examples_08_color_image_processing_color_compensation_py["color_compensation.py"]
  examples_08_color_image_processing_color_spaces_py["color_spaces.py"]
  examples_08_color_image_processing_gray_world_py["gray_world.py"]
  examples_08_color_image_processing_white_balance_py["white_balance.py"]
  examples_09_image_transform_one_dimensional_fourier_transform_py["one_dimensional_fourier_transform.py"]
  examples_09_image_transform_spectrum_visualization_py["spectrum_visualization.py"]
  examples_09_image_transform_two_dimensional_fft_py["two_dimensional_fft.py"]
  examples_09_image_transform_wavelet_decomposition_py["wavelet_decomposition.py"]
  examples_09_image_transform_wavelet_denoising_py["wavelet_denoising.py"]
  examples_10_image_compression_huffman_encoding_demo_py["huffman_encoding_demo.py"]
  examples_10_image_compression_jpeg_idea_demo_py["jpeg_idea_demo.py"]
  examples_10_image_compression_rle_encoding_py["rle_encoding.py"]
  examples_10_image_compression_wavelet_compression_demo_py["wavelet_compression_demo.py"]
  examples_11_deep_learning_image_processing_alexnet_structure_demo_py["alexnet_structure_demo.py"]
  examples_11_deep_learning_image_processing_cnn_layers_demo_py["cnn_layers_demo.py"]
  examples_11_deep_learning_image_processing_lenet5_structure_demo_py["lenet5_structure_demo.py"]
  examples_11_deep_learning_image_processing_srcnn_structure_demo_py["srcnn_structure_demo.py"]
  examples_11_deep_learning_image_processing_yolo_concept_demo_py["yolo_concept_demo.py"]
  formula_ch03_affine_matrix["齐次仿射矩阵"]
  formula_ch03_rotation_matrix["旋转矩阵"]
  formula_ch03_translation_matrix["平移矩阵"]
  formula_ch04_additive_noise["加性噪声模型"]
  formula_ch04_mean_filter["均值滤波公式"]
  formula_ch04_median_filter["中值滤波公式"]
  formula_ch04_nlm_weight["非局部均值权重"]
  formula_ch05_Canny____["Canny 双阈值"]
  formula_ch05_Laplacian_____["Laplacian 二阶差分"]
  formula_ch05_LoG___["LoG 公式"]
  formula_ch05_Prewitt_____["Prewitt 差分模板"]
  formula_ch05_Roberts_______["Roberts 交叉差分模板"]
  formula_ch05_Sobel_____["Sobel 差分模板"]
  formula_ch05_______["梯度幅值公式"]
  formula_ch06_Otsu_____["Otsu 类间方差"]
  formula_ch06_______["二值阈值函数"]
  formula_ch06__________["区域生长相似性准则"]
  formula_ch06________["最大熵目标函数"]
  formula_ch06_______["累计概率阈值"]
  formula_ch07_4_8___["4/8 邻域"]
  formula_ch07_______["开闭运算公式"]
  formula_ch07____["标签图"]
  formula_ch07________["细线化拓扑保持"]
  formula_ch07_____["腐蚀公式"]
  formula_ch07_____["膨胀公式"]
  formula_ch08_RGB_____["RGB 加色模型"]
  formula_ch08_______["灰色世界假设"]
  formula_ch08_______["通道增益校正"]
  formula_ch08_______["颜色空间变换"]
  formula_ch09_DFT___["DFT 公式"]
  formula_ch09_FFT____["FFT 复杂度"]
  formula_ch09________["小波多尺度分解"]
  formula_ch09_______["小波阈值去噪"]
  formula_ch09_____["频谱幅值"]
  formula_ch10____["压缩比"]
  formula_ch10_______["小波稀疏系数"]
  formula_ch10_____["平均码长"]
  formula_ch10_____["量化公式"]
  formula_ch11_BN___["BN 公式"]
  formula_ch11_ReLU___["ReLU 函数"]
  formula_ch11_Softmax___["Softmax 分类"]
  formula_ch11______["卷积层公式"]
  formula_ch11______["检测框输出"]
  wiki_05______5_1___________md["图像细节"]
  wiki_05______5_2_2_Roberts_______md["Roberts 算子"]
  wiki_05______5_2_3_Sobel_____md["Sobel 算子"]
  wiki_05______5_2_4_Priwitt_____md["Prewitt 算子"]
  wiki_05______5_2________md["一阶微分算子"]
  wiki_05______5_3_1_Laplacian_____md["Laplacian 算子"]
  wiki_05______5_3________md["二阶微分算子"]
  wiki_05______5_5_Canny___md["Canny 算子"]
  wiki_05______5_6_LOG_____md["LoG 滤波"]
  wiki_06_______6_1_1_p_____md["p-参数法"]
  wiki_06_______6_1_2_______md["最大熵方法"]
  wiki_06_______6_1_3_____________md["Otsu 阈值法"]
  wiki_06_______6_1________md["阈值分割"]
  wiki_06_______6_2__________md["区域生长"]
  wiki_07________7_1_1________md["7.1.1 连接与点特性"]
  wiki_07________7_1_2______md["7.1.2 几何特征"]
  wiki_07________7_1____________md["7.1 二值图像中的基本概念"]
  wiki_07________7_2_1____md["7.2.1 腐蚀"]
  wiki_07________7_2_2____md["7.2.2 膨胀"]
  wiki_07________7_2_______md["7.2 腐蚀与膨胀"]
  wiki_07________7_3_1_____md["7.3.1 开运算"]
  wiki_07________7_3_2_____md["7.3.2 闭运算"]
  wiki_07________7_3_________md["7.3 开运算与闭运算"]
  wiki_07________7_4_1________md["7.4.1 连通域标签法"]
  wiki_07________7_4_2_______md["7.4.2 轮廓标签法"]
  wiki_07________7_4_____md["7.4 贴标签"]
  wiki_07________7_5_______md["7.5 细线化方法"]
  wiki_07________7_x____md["7.x 习题"]
  wiki_08________8_1______________md["8.1 彩色的形成原理与基本概念"]
  wiki_08________8_2_1__________md["8.2.1 计算颜色模型系统"]
  wiki_08________8_2_2__________md["8.2.2 视觉颜色模型系统"]
  wiki_08________8_2_3__________md["8.2.3 工业颜色模型系统"]
  wiki_08________8_2_____md["8.2 表色系"]
  wiki_08________8_3_1______md["8.3.1 白平衡法"]
  wiki_08________8_3_2_______md["8.3.2 灰色世界法"]
  wiki_08________8_3______md["8.3 色彩平衡"]
  wiki_08________8_4______md["8.4 彩色补偿"]
  wiki_08________8_x____md["8.x 习题"]
  wiki_09______9_1_1_________md["9.1.1 一维傅里叶变换"]
  wiki_09______9_1_2_________md["9.1.2 二维傅里叶变换"]
  wiki_09______9_1_3_________FFT__md["9.1.3 快速傅里叶变换（FFT）"]
  wiki_09______9_1_4___________md["9.1.4 图像的频谱分布特性"]
  wiki_09______9_1________________md["9.1 图像的频域变换（傅里叶变换）"]
  wiki_09______9_2_1________md["9.2.1 连续小波变换"]
  wiki_09______9_2_2________md["9.2.2 离散小波变换"]
  wiki_09______9_2_3_____________md["9.2.3 小波的多尺度分解与重构"]
  wiki_09______9_2______md["9.2 小波变换"]
  wiki_09______9_3_1_________md["9.3.1 应用于图像压缩"]
  wiki_09______9_3_2_________md["9.3.2 应用于图像融合"]
  wiki_09______9_3_3_________md["9.3.3 应用于图像增强"]
  wiki_09______9_3_4_________md["9.3.4 应用于图像去噪"]
  wiki_09______9_3_______________md["9.3 小波变换在图像处理中的应用"]
  wiki_09______9_x____md["9.x 习题"]
  wiki_10________10_1_1_______md["10.1.1 冗余的概念"]
  wiki_10________10_1_2________md["10.1.2 图像中的冗余"]
  wiki_10________10_1_________md["10.1 图像冗余的概念"]
  wiki_10________10_2_1______RLE__md["10.2.1 行程编码（RLE）"]
  wiki_10________10_2_2_____Huffman____md["10.2.2 哈夫曼（Huffman）编码"]
  wiki_10________10_2__________md["10.2 图像无损压缩编码"]
  wiki_10________10_3_1___________md["10.3.1 彩色图像的有损编码"]
  wiki_10________10_3_2________md["10.3.2 小波变换编码"]
  wiki_10________10_3__________md["10.3 图像有损压缩编码"]
  wiki_10________10_x____md["10.x 习题"]
  wiki_11___________11_1_1_____md["11.1.1 卷积层"]
  wiki_11___________11_1_2_____md["11.1.2 激活层"]
  wiki_11___________11_1_3_BN_____________md["11.1.3 BN层（批数据归一化处理层）"]
  wiki_11___________11_1_4_____md["11.1.4 池化层"]
  wiki_11___________11_1_____________md["11.1 深度卷积网络的基本结构"]
  wiki_11___________11_2_1_SRCNN___md["11.2.1 SRCNN网络"]
  wiki_11___________11_2_2_ESPCN___md["11.2.2 ESPCN网络"]
  wiki_11___________11_2______________md["11.2 超分辨率图像重建卷积网络"]
  wiki_11___________11_3_1_LeNet_5___md["11.3.1 LeNet-5网络"]
  wiki_11___________11_3_2_AlexNet___md["11.3.2 AlexNet网络"]
  wiki_11___________11_3____________md["11.3 图像分类深度卷积网络"]
  wiki_11___________11_4_1_Faster_RCNN___md["11.4.1 Faster-RCNN网络"]
  wiki_11___________11_4_2_YOLO___md["11.4.2 YOLO网络"]
  wiki_11___________11_4______________md["11.4 图像目标检测深度卷积网络"]
  wiki_11___________11_x____md["11.x 习题"]
  wiki_01____README -->|CONTAINS| wiki_01____1_1____________________
  wiki_01____README -->|CONTAINS| wiki_01____1_2____________
  wiki_01____README -->|CONTAINS| wiki_01____1_3_1__________
  wiki_01____README -->|CONTAINS| wiki_01____1_3_2___________
  wiki_01____README -->|CONTAINS| wiki_01____1_3__________
  wiki_01____README -->|CONTAINS| wiki_01____1_4______________
  wiki_01____README -->|CONTAINS| wiki_01____1_5________
  wiki_01____README -->|CONTAINS| wiki_01____1_x___
  wiki_02______README -->|CONTAINS| wiki_02______2_1____
  wiki_02______README -->|CONTAINS| wiki_02______2_2________
  wiki_02______README -->|CONTAINS| wiki_02______2_3_1____
  wiki_02______README -->|CONTAINS| wiki_02______2_3_2______
  wiki_02______README -->|CONTAINS| wiki_02______2_3__________
  wiki_02______README -->|CONTAINS| wiki_02______2_4_1_________
  wiki_02______README -->|CONTAINS| wiki_02______2_4_2__________
  wiki_02______README -->|CONTAINS| wiki_02______2_4_______
  wiki_02______README -->|CONTAINS| wiki_02______2_5_______
  wiki_02______README -->|CONTAINS| wiki_02______2_6__________
  wiki_02______README -->|CONTAINS| wiki_02______2_7____
  wiki_02______README -->|CONTAINS| wiki_02______2_8_Retinex______
  wiki_02______README -->|CONTAINS| wiki_02______2_x___
  wiki_03________README -->|CONTAINS| wiki_03________3_1_1______
  wiki_03________README -->|CONTAINS| wiki_03________3_1_2______
  wiki_03________README -->|CONTAINS| wiki_03________3_1_3______
  wiki_03________README -->|CONTAINS| wiki_03________3_1________
  wiki_03________README -->|CONTAINS| wiki_03________3_2_1______
  wiki_03________README -->|CONTAINS| wiki_03________3_2_2______
  wiki_03________README -->|CONTAINS| wiki_03________3_2_3______
  wiki_03________README -->|CONTAINS| wiki_03________3_2________
  wiki_03________README -->|CONTAINS| wiki_03________3_3_____________
  wiki_03________README -->|CONTAINS| wiki_03________3_4__________
  wiki_03________README -->|CONTAINS| wiki_03________3_x___
  wiki_04______README -->|CONTAINS| wiki_04______4_1_____
  wiki_04______README -->|CONTAINS| wiki_04______4_2_1________
  wiki_04______README -->|CONTAINS| wiki_04______4_2_2_______
  wiki_04______README -->|CONTAINS| wiki_04______4_2_____
  wiki_04______README -->|CONTAINS| wiki_04______4_3_1________
  wiki_04______README -->|CONTAINS| wiki_04______4_3_2_______
  wiki_04______README -->|CONTAINS| wiki_04______4_3_____
  wiki_04______README -->|CONTAINS| wiki_04______4_4_1_K______
  wiki_04______README -->|CONTAINS| wiki_04______4_4_2_________
  wiki_04______README -->|CONTAINS| wiki_04______4_4__________
  wiki_04______README -->|CONTAINS| wiki_04______4_5________
  wiki_04______README -->|CONTAINS| wiki_04______4_x___
  wiki_05______README -->|CONTAINS| wiki_05______5_1__________
  wiki_05______README -->|CONTAINS| wiki_05______5_2_1_____________
  wiki_05______README -->|CONTAINS| wiki_05______5_2_2_Roberts______
  wiki_05______README -->|CONTAINS| wiki_05______5_2_3_Sobel____
  wiki_05______README -->|CONTAINS| wiki_05______5_2_4_Priwitt____
  wiki_05______README -->|CONTAINS| wiki_05______5_2_______
  wiki_05______README -->|CONTAINS| wiki_05______5_3_1_Laplacian____
  wiki_05______README -->|CONTAINS| wiki_05______5_3_2_Wallis____
  wiki_05______README -->|CONTAINS| wiki_05______5_3_______
  wiki_05______README -->|CONTAINS| wiki_05______5_4______________
  wiki_05______README -->|CONTAINS| wiki_05______5_5_Canny__
  wiki_05______README -->|CONTAINS| wiki_05______5_6_LOG____
  wiki_05______README -->|CONTAINS| wiki_05______5_x___
  wiki_06_______README -->|CONTAINS| wiki_06_______6_1_1_p____
  wiki_06_______README -->|CONTAINS| wiki_06_______6_1_2______
  wiki_06_______README -->|CONTAINS| wiki_06_______6_1_3____________
  wiki_06_______README -->|CONTAINS| wiki_06_______6_1_______
  wiki_06_______README -->|CONTAINS| wiki_06_______6_2_________
  wiki_06_______README -->|CONTAINS| wiki_06_______6_x___
  wiki_07________README -->|CONTAINS| wiki_07________7_1_1_______
  wiki_07________README -->|CONTAINS| wiki_07________7_1_2_____
  wiki_07________README -->|CONTAINS| wiki_07________7_1___________
  wiki_07________README -->|CONTAINS| wiki_07________7_2_1___
  wiki_07________README -->|CONTAINS| wiki_07________7_2_2___
  wiki_07________README -->|CONTAINS| wiki_07________7_2______
  wiki_07________README -->|CONTAINS| wiki_07________7_3_1____
  wiki_07________README -->|CONTAINS| wiki_07________7_3_2____
  wiki_07________README -->|CONTAINS| wiki_07________7_3________
  wiki_07________README -->|CONTAINS| wiki_07________7_4_1_______
  wiki_07________README -->|CONTAINS| wiki_07________7_4_2______
  wiki_07________README -->|CONTAINS| wiki_07________7_4____
  wiki_07________README -->|CONTAINS| wiki_07________7_5______
  wiki_07________README -->|CONTAINS| wiki_07________7_x___
  wiki_08________README -->|CONTAINS| wiki_08________8_1_____________
  wiki_08________README -->|CONTAINS| wiki_08________8_2_1_________
  wiki_08________README -->|CONTAINS| wiki_08________8_2_2_________
  wiki_08________README -->|CONTAINS| wiki_08________8_2_3_________
  wiki_08________README -->|CONTAINS| wiki_08________8_2____
  wiki_08________README -->|CONTAINS| wiki_08________8_3_1_____
  wiki_08________README -->|CONTAINS| wiki_08________8_3_2______
  wiki_08________README -->|CONTAINS| wiki_08________8_3_____
  wiki_08________README -->|CONTAINS| wiki_08________8_4_____
  wiki_08________README -->|CONTAINS| wiki_08________8_x___
  wiki_09______README -->|CONTAINS| wiki_09______9_1_1________
  wiki_09______README -->|CONTAINS| wiki_09______9_1_2________
  wiki_09______README -->|CONTAINS| wiki_09______9_1_3_________FFT_
  wiki_09______README -->|CONTAINS| wiki_09______9_1_4__________
  wiki_09______README -->|CONTAINS| wiki_09______9_1_______________
  wiki_09______README -->|CONTAINS| wiki_09______9_2_1_______
  wiki_09______README -->|CONTAINS| wiki_09______9_2_2_______
  wiki_09______README -->|CONTAINS| wiki_09______9_2_3____________
  wiki_09______README -->|CONTAINS| wiki_09______9_2_____
  wiki_09______README -->|CONTAINS| wiki_09______9_3_1________
  wiki_09______README -->|CONTAINS| wiki_09______9_3_2________
  wiki_09______README -->|CONTAINS| wiki_09______9_3_3________
  wiki_09______README -->|CONTAINS| wiki_09______9_3_4________
  wiki_09______README -->|CONTAINS| wiki_09______9_3______________
  wiki_09______README -->|CONTAINS| wiki_09______9_x___
  wiki_10________README -->|CONTAINS| wiki_10________10_1_1______
  wiki_10________README -->|CONTAINS| wiki_10________10_1_2_______
  wiki_10________README -->|CONTAINS| wiki_10________10_1________
  wiki_10________README -->|CONTAINS| wiki_10________10_2_1______RLE_
  wiki_10________README -->|CONTAINS| wiki_10________10_2_2_____Huffman___
  wiki_10________README -->|CONTAINS| wiki_10________10_2_________
  wiki_10________README -->|CONTAINS| wiki_10________10_3_1__________
  wiki_10________README -->|CONTAINS| wiki_10________10_3_2_______
  wiki_10________README -->|CONTAINS| wiki_10________10_3_________
  wiki_10________README -->|CONTAINS| wiki_10________10_x___
  wiki_11___________README -->|CONTAINS| wiki_11___________11_1_1____
  wiki_11___________README -->|CONTAINS| wiki_11___________11_1_2____
  wiki_11___________README -->|CONTAINS| wiki_11___________11_1_3_BN____________
  wiki_11___________README -->|CONTAINS| wiki_11___________11_1_4____
  wiki_11___________README -->|CONTAINS| wiki_11___________11_1____________
  wiki_11___________README -->|CONTAINS| wiki_11___________11_2_1_SRCNN__
  wiki_11___________README -->|CONTAINS| wiki_11___________11_2_2_ESPCN__
  wiki_11___________README -->|CONTAINS| wiki_11___________11_2_____________
  wiki_11___________README -->|CONTAINS| wiki_11___________11_3_1_LeNet_5__
  wiki_11___________README -->|CONTAINS| wiki_11___________11_3_2_AlexNet__
  wiki_11___________README -->|CONTAINS| wiki_11___________11_3___________
  wiki_11___________README -->|CONTAINS| wiki_11___________11_4_1_Faster_RCNN__
  wiki_11___________README -->|CONTAINS| wiki_11___________11_4_2_YOLO__
  wiki_11___________README -->|CONTAINS| wiki_11___________11_4_____________
  wiki_11___________README -->|CONTAINS| wiki_11___________11_x___
  concept_ch03_nearest_interpolation -->|COMPARES_WITH| concept_ch03_bilinear_interpolation
  concept_ch03_reverse_mapping -->|PREREQUISITE| concept_ch03_bilinear_interpolation
  concept_ch04_gaussian_noise -->|APPLIES_TO| wiki_04______4_2_____
  concept_ch04_salt_pepper_noise -->|APPLIES_TO| wiki_04______4_3_____
  wiki_03________3_1_1______ -->|IMPLEMENTED_BY| examples_03_geometric_transform_image_translation_py
  wiki_03________3_1_1______ -->|USES_FORMULA| formula_ch03_translation_matrix
  wiki_03________3_1_3______ -->|IMPLEMENTED_BY| examples_03_geometric_transform_image_rotation_py
  wiki_03________3_1_3______ -->|USES_FORMULA| formula_ch03_rotation_matrix
  wiki_03________3_2_1______ -->|COMPARES_WITH| wiki_03________3_2_2______
  wiki_03________3_2_2______ -->|IMPLEMENTED_BY| examples_03_geometric_transform_image_resize_py
  wiki_03________3_2_3______ -->|IMPLEMENTED_BY| examples_03_geometric_transform_image_shear_py
  wiki_03________3_3_____________ -->|IMPLEMENTED_BY| examples_03_geometric_transform_affine_transform_py
  wiki_03________3_3_____________ -->|USES_FORMULA| formula_ch03_affine_matrix
  wiki_03________3_3_____________ -->|GENERALIZES| wiki_03________3_1_1______
  wiki_03________3_3_____________ -->|GENERALIZES| wiki_03________3_1_3______
  wiki_03________3_3_____________ -->|GENERALIZES| wiki_03________3_2_3______
  wiki_03________3_4__________ -->|PREREQUISITE| concept_ch03_reverse_mapping
  wiki_03________3_4__________ -->|IMPLEMENTED_BY| examples_03_geometric_transform_geometric_correction_py
  wiki_03________3_4__________ -->|IMPROVES_OR_EXTENDS| wiki_03________3_3_____________
  wiki_04______4_1_____ -->|USES_FORMULA| formula_ch04_additive_noise
  wiki_04______4_1_____ -->|PREREQUISITE| wiki_04______4_2_____
  wiki_04______4_2_____ -->|IMPLEMENTED_BY| examples_04_image_denoising_mean_filter_py
  wiki_04______4_2_____ -->|USES_FORMULA| formula_ch04_mean_filter
  wiki_04______4_2_____ -->|COMPARES_WITH| wiki_04______4_3_____
  wiki_04______4_2_____ -->|PREREQUISITE| wiki_05______5_5_Canny__
  wiki_04______4_3_____ -->|IMPLEMENTED_BY| examples_04_image_denoising_median_filter_py
  wiki_04______4_3_____ -->|USES_FORMULA| formula_ch04_median_filter
  wiki_04______4_4_1_K______ -->|IMPLEMENTED_BY| examples_04_image_denoising_k_nearest_mean_filter_py
  wiki_04______4_4_2_________ -->|IMPLEMENTED_BY| examples_04_image_denoising_symmetric_nearest_mean_filter_py
  wiki_04______4_4__________ -->|IMPROVES_OR_EXTENDS| wiki_04______4_2_____
  wiki_04______4_4__________ -->|GENERALIZES| wiki_04______4_4_1_K______
  wiki_04______4_4__________ -->|GENERALIZES| wiki_04______4_4_2_________
  wiki_04______4_5________ -->|IMPLEMENTED_BY| examples_04_image_denoising_non_local_means_filter_py
  wiki_04______4_5________ -->|USES_FORMULA| formula_ch04_nlm_weight
  wiki_04______4_5________ -->|IMPROVES_OR_EXTENDS| wiki_04______4_4__________
  wiki_05______5_2_2_Roberts_______md -->|IMPLEMENTED_BY| examples_05_image_sharpening_roberts_operator_py
  wiki_05______5_2_2_Roberts_______md -->|USES_FORMULA| formula_ch05_Roberts_______
  wiki_05______5_2_2_Roberts_______md -->|USES_FORMULA| formula_ch05_______
  wiki_05______5_2_2_Roberts_______md -->|GENERALIZES| wiki_05______5_2________md
  wiki_05______5_2_3_Sobel_____md -->|IMPLEMENTED_BY| examples_05_image_sharpening_sobel_operator_py
  wiki_05______5_2_3_Sobel_____md -->|USES_FORMULA| formula_ch05_Sobel_____
  wiki_05______5_2_3_Sobel_____md -->|USES_FORMULA| formula_ch05_______
  wiki_05______5_2_3_Sobel_____md -->|GENERALIZES| wiki_05______5_2________md
  wiki_05______5_2_4_Priwitt_____md -->|IMPLEMENTED_BY| examples_05_image_sharpening_prewitt_operator_py
  wiki_05______5_2_4_Priwitt_____md -->|USES_FORMULA| formula_ch05_Prewitt_____
  wiki_05______5_2_4_Priwitt_____md -->|USES_FORMULA| formula_ch05_______
  wiki_05______5_2_4_Priwitt_____md -->|GENERALIZES| wiki_05______5_2________md
  wiki_05______5_2________md -->|PREREQUISITE| wiki_05______5_1___________md
  wiki_05______5_3_1_Laplacian_____md -->|IMPLEMENTED_BY| examples_05_image_sharpening_laplacian_operator_py
  wiki_05______5_3_1_Laplacian_____md -->|USES_FORMULA| formula_ch05_Laplacian_____
  wiki_05______5_3_1_Laplacian_____md -->|GENERALIZES| wiki_05______5_3________md
  wiki_05______5_3________md -->|PREREQUISITE| wiki_05______5_1___________md
  wiki_05______5_5_Canny___md -->|IMPLEMENTED_BY| examples_05_image_sharpening_canny_edge_detection_py
  wiki_05______5_5_Canny___md -->|USES_FORMULA| formula_ch05_Canny____
  wiki_05______5_5_Canny___md -->|PREREQUISITE| wiki_05______5_2_3_Sobel_____md
  wiki_05______5_5_Canny___md -->|COMPARES_WITH| wiki_05______5_6_LOG_____md
  wiki_05______5_6_LOG_____md -->|IMPLEMENTED_BY| examples_05_image_sharpening_log_filter_py
  wiki_05______5_6_LOG_____md -->|USES_FORMULA| formula_ch05_LoG___
  wiki_05______5_6_LOG_____md -->|IMPROVES_OR_EXTENDS| wiki_05______5_3_1_Laplacian_____md
  wiki_06_______6_1_1_p_____md -->|USES_FORMULA| formula_ch06_______
  wiki_06_______6_1_1_p_____md -->|GENERALIZES| wiki_06_______6_1________md
  wiki_06_______6_1_2_______md -->|IMPLEMENTED_BY| examples_06_image_segmentation_max_entropy_threshold_py
  wiki_06_______6_1_2_______md -->|USES_FORMULA| formula_ch06________
  wiki_06_______6_1_2_______md -->|GENERALIZES| wiki_06_______6_1________md
  wiki_06_______6_1_3_____________md -->|IMPLEMENTED_BY| examples_06_image_segmentation_otsu_threshold_py
  wiki_06_______6_1_3_____________md -->|USES_FORMULA| formula_ch06_Otsu_____
  wiki_06_______6_1_3_____________md -->|GENERALIZES| wiki_06_______6_1________md
  wiki_06_______6_1________md -->|IMPLEMENTED_BY| examples_06_image_segmentation_threshold_segmentation_py
  wiki_06_______6_1________md -->|USES_FORMULA| formula_ch06_______
  wiki_06_______6_2__________md -->|IMPLEMENTED_BY| examples_06_image_segmentation_region_growing_py
  wiki_06_______6_2__________md -->|USES_FORMULA| formula_ch06__________
  wiki_06_______6_2__________md -->|COMPARES_WITH| wiki_06_______6_1________md
  wiki_07________7_1____________md -->|USES_FORMULA| formula_ch07_4_8___
  wiki_07________7_1____________md -->|PREREQUISITE| wiki_06_______6_1________md
  wiki_07________7_2_1____md -->|USES_FORMULA| formula_ch07_____
  wiki_07________7_2_1____md -->|GENERALIZES| wiki_07________7_2_______md
  wiki_07________7_2_2____md -->|USES_FORMULA| formula_ch07_____
  wiki_07________7_2_2____md -->|GENERALIZES| wiki_07________7_2_______md
  wiki_07________7_2_______md -->|IMPLEMENTED_BY| examples_07_binary_image_processing_erosion_dilation_py
  wiki_07________7_2_______md -->|PREREQUISITE| wiki_07________7_1____________md
  wiki_07________7_3_1_____md -->|GENERALIZES| wiki_07________7_3_________md
  wiki_07________7_3_2_____md -->|GENERALIZES| wiki_07________7_3_________md
  wiki_07________7_3_________md -->|IMPLEMENTED_BY| examples_07_binary_image_processing_opening_closing_py
  wiki_07________7_3_________md -->|USES_FORMULA| formula_ch07_______
  wiki_07________7_3_________md -->|IMPROVES_OR_EXTENDS| wiki_07________7_2_______md
  wiki_07________7_4_1________md -->|IMPLEMENTED_BY| examples_07_binary_image_processing_connected_component_labeling_py
  wiki_07________7_4_1________md -->|GENERALIZES| wiki_07________7_4_____md
  wiki_07________7_4_2_______md -->|IMPLEMENTED_BY| examples_07_binary_image_processing_contour_labeling_py
  wiki_07________7_4_2_______md -->|GENERALIZES| wiki_07________7_4_____md
  wiki_07________7_4_____md -->|USES_FORMULA| formula_ch07____
  wiki_07________7_4_____md -->|PREREQUISITE| wiki_07________7_1____________md
  wiki_07________7_5_______md -->|IMPLEMENTED_BY| examples_07_binary_image_processing_thinning_py
  wiki_07________7_5_______md -->|USES_FORMULA| formula_ch07________
  wiki_07________7_5_______md -->|COMPARES_WITH| wiki_07________7_2_______md
  wiki_08________8_1______________md -->|USES_FORMULA| formula_ch08_RGB_____
  wiki_08________8_2_____md -->|IMPLEMENTED_BY| examples_08_color_image_processing_color_spaces_py
  wiki_08________8_2_____md -->|USES_FORMULA| formula_ch08_______
  wiki_08________8_2_____md -->|PREREQUISITE| wiki_08________8_1______________md
  wiki_08________8_3_1______md -->|IMPLEMENTED_BY| examples_08_color_image_processing_white_balance_py
  wiki_08________8_3_1______md -->|GENERALIZES| wiki_08________8_3______md
  wiki_08________8_3_2_______md -->|IMPLEMENTED_BY| examples_08_color_image_processing_gray_world_py
  wiki_08________8_3_2_______md -->|USES_FORMULA| formula_ch08_______
  wiki_08________8_3_2_______md -->|GENERALIZES| wiki_08________8_3______md
  wiki_08________8_3______md -->|USES_FORMULA| formula_ch08_______
  wiki_08________8_3______md -->|PREREQUISITE| wiki_08________8_2_____md
  wiki_08________8_4______md -->|IMPLEMENTED_BY| examples_08_color_image_processing_color_compensation_py
  wiki_08________8_4______md -->|APPLIES_TO| wiki_06_______6_1________md
  wiki_08________8_4______md -->|IMPROVES_OR_EXTENDS| wiki_08________8_3______md
  wiki_09______9_1_1_________md -->|IMPLEMENTED_BY| examples_09_image_transform_one_dimensional_fourier_transform_py
  wiki_09______9_1_2_________md -->|IMPLEMENTED_BY| examples_09_image_transform_two_dimensional_fft_py
  wiki_09______9_1_3_________FFT__md -->|USES_FORMULA| formula_ch09_FFT____
  wiki_09______9_1_3_________FFT__md -->|IMPROVES_OR_EXTENDS| wiki_09______9_1________________md
  wiki_09______9_1_4___________md -->|IMPLEMENTED_BY| examples_09_image_transform_spectrum_visualization_py
  wiki_09______9_1_4___________md -->|USES_FORMULA| formula_ch09_____
  wiki_09______9_1________________md -->|USES_FORMULA| formula_ch09_DFT___
  wiki_09______9_2_3_____________md -->|IMPLEMENTED_BY| examples_09_image_transform_wavelet_decomposition_py
  wiki_09______9_2_3_____________md -->|USES_FORMULA| formula_ch09________
  wiki_09______9_2______md -->|COMPARES_WITH| wiki_09______9_1________________md
  wiki_09______9_3_4_________md -->|IMPLEMENTED_BY| examples_09_image_transform_wavelet_denoising_py
  wiki_09______9_3_4_________md -->|USES_FORMULA| formula_ch09_______
  wiki_09______9_3_______________md -->|PREREQUISITE| wiki_09______9_2______md
  wiki_10________10_1_________md -->|USES_FORMULA| formula_ch10____
  wiki_10________10_2_1______RLE__md -->|IMPLEMENTED_BY| examples_10_image_compression_rle_encoding_py
  wiki_10________10_2_1______RLE__md -->|COMPARES_WITH| wiki_10________10_2_2_____Huffman____md
  wiki_10________10_2_2_____Huffman____md -->|IMPLEMENTED_BY| examples_10_image_compression_huffman_encoding_demo_py
  wiki_10________10_2_2_____Huffman____md -->|USES_FORMULA| formula_ch10_____
  wiki_10________10_2__________md -->|PREREQUISITE| wiki_10________10_1_________md
  wiki_10________10_3_2________md -->|IMPLEMENTED_BY| examples_10_image_compression_wavelet_compression_demo_py
  wiki_10________10_3_2________md -->|USES_FORMULA| formula_ch10_______
  wiki_10________10_3_2________md -->|PREREQUISITE| wiki_09______9_3_1_________md
  wiki_10________10_3__________md -->|IMPLEMENTED_BY| examples_10_image_compression_jpeg_idea_demo_py
  wiki_10________10_3__________md -->|USES_FORMULA| formula_ch10_____
  wiki_10________10_3__________md -->|APPLIES_TO| wiki_08________8_2_____md
  wiki_10________10_3__________md -->|PREREQUISITE| wiki_10________10_1_________md
  wiki_11___________11_1_1_____md -->|USES_FORMULA| formula_ch11______
  wiki_11___________11_1_1_____md -->|GENERALIZES| wiki_11___________11_1_____________md
  wiki_11___________11_1_2_____md -->|USES_FORMULA| formula_ch11_ReLU___
  wiki_11___________11_1_2_____md -->|GENERALIZES| wiki_11___________11_1_____________md
  wiki_11___________11_1_3_BN_____________md -->|USES_FORMULA| formula_ch11_BN___
  wiki_11___________11_1_3_BN_____________md -->|GENERALIZES| wiki_11___________11_1_____________md
  wiki_11___________11_1_4_____md -->|GENERALIZES| wiki_11___________11_1_____________md
  wiki_11___________11_1_____________md -->|IMPLEMENTED_BY| examples_11_deep_learning_image_processing_cnn_layers_demo_py
  wiki_11___________11_1_____________md -->|COMPARES_WITH| wiki_05______5_2________md
  wiki_11___________11_2_1_SRCNN___md -->|IMPLEMENTED_BY| examples_11_deep_learning_image_processing_srcnn_structure_demo_py
  wiki_11___________11_2_1_SRCNN___md -->|GENERALIZES| wiki_11___________11_2______________md
  wiki_11___________11_2_2_ESPCN___md -->|GENERALIZES| wiki_11___________11_2______________md
  wiki_11___________11_3_1_LeNet_5___md -->|IMPLEMENTED_BY| examples_11_deep_learning_image_processing_lenet5_structure_demo_py
  wiki_11___________11_3_1_LeNet_5___md -->|GENERALIZES| wiki_11___________11_3____________md
  wiki_11___________11_3_2_AlexNet___md -->|IMPLEMENTED_BY| examples_11_deep_learning_image_processing_alexnet_structure_demo_py
  wiki_11___________11_3_2_AlexNet___md -->|GENERALIZES| wiki_11___________11_3____________md
  wiki_11___________11_3____________md -->|USES_FORMULA| formula_ch11_Softmax___
  wiki_11___________11_4_1_Faster_RCNN___md -->|GENERALIZES| wiki_11___________11_4______________md
  wiki_11___________11_4_2_YOLO___md -->|IMPLEMENTED_BY| examples_11_deep_learning_image_processing_yolo_concept_demo_py
  wiki_11___________11_4_2_YOLO___md -->|APPLIES_TO| wiki_06_______6_1________md
  wiki_11___________11_4_2_YOLO___md -->|GENERALIZES| wiki_11___________11_4______________md
  wiki_11___________11_4______________md -->|USES_FORMULA| formula_ch11______
  wiki_11___________11_4______________md -->|COMPARES_WITH| wiki_06_______6_2__________md
```
