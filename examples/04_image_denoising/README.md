# 04_image_denoising

本目录保存第 4 章“图像去噪”的独立教学示例。默认输入为 `assets/sample_images/sample_noisy.png`，该图片由合成灰度图加入高斯噪声和椒盐噪声生成，不使用原书图片。

## 运行示例

```powershell
python examples/04_image_denoising/mean_filter.py --kernel-size 5
python examples/04_image_denoising/median_filter.py --kernel-size 5
python examples/04_image_denoising/k_nearest_mean_filter.py --kernel-size 5 --k 8
python examples/04_image_denoising/symmetric_nearest_mean_filter.py --kernel-size 5
python examples/04_image_denoising/non_local_means_filter.py --h 10
```

输出默认写入 `examples/output/`，该目录已被 `.gitignore` 忽略。
