from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SAMPLE_GRAY = ROOT / "assets" / "sample_images" / "sample_gray.png"
SAMPLE_COLOR = ROOT / "assets" / "sample_images" / "sample_color.png"


def ensure_samples():
    SAMPLE_GRAY.parent.mkdir(parents=True, exist_ok=True)
    if not SAMPLE_GRAY.exists():
        x = np.linspace(0, 255, 256, dtype=np.uint8)
        img = np.tile(x, (256, 1))
        cv2.circle(img, (128, 128), 60, 220, -1)
        cv2.rectangle(img, (30, 40), (90, 110), 55, -1)
        cv2.imwrite(str(SAMPLE_GRAY), img)
        cv2.imwrite(str(SAMPLE_COLOR), cv2.merge([img, np.flipud(img), np.roll(img, 50, axis=1)]))


def read_image(path: str | None, color: bool = False):
    ensure_samples()
    source = Path(path) if path else (SAMPLE_COLOR if color else SAMPLE_GRAY)
    flag = cv2.IMREAD_COLOR if color else cv2.IMREAD_GRAYSCALE
    image = cv2.imread(str(source), flag)
    if image is None:
        raise FileNotFoundError(source)
    return image, source


def apply_demo(name: str, image):
    if name == "gamma_correction":
        table = np.array([(i / 255) ** 0.55 * 255 for i in range(256)], dtype=np.uint8)
        return cv2.LUT(image, table)
    if name == "contrast_stretching":
        return cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
    if name == "gray_level_window":
        return np.where((image > 80) & (image < 180), 255, 0).astype(np.uint8)
    if name == "histogram_equalization":
        return cv2.equalizeHist(image)
    if name == "adaptive_histogram_equalization":
        return cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(image)
    if name == "pseudo_color":
        return cv2.applyColorMap(image, cv2.COLORMAP_JET)
    if name == "retinex_enhancement":
        blur = cv2.GaussianBlur(image, (0, 0), 15)
        out = np.log1p(image.astype(np.float32)) - np.log1p(blur.astype(np.float32))
        return cv2.normalize(out, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    if name == "image_translation":
        h, w = image.shape[:2]
        return cv2.warpAffine(image, np.float32([[1, 0, 30], [0, 1, 20]]), (w, h))
    if name == "image_mirror":
        return cv2.flip(image, 1)
    if name == "image_rotation":
        h, w = image.shape[:2]
        return cv2.warpAffine(image, cv2.getRotationMatrix2D((w / 2, h / 2), 25, 1), (w, h))
    if name == "image_resize":
        return cv2.resize(image, None, fx=0.6, fy=0.6)
    if name == "image_shear":
        h, w = image.shape[:2]
        return cv2.warpAffine(image, np.float32([[1, 0.25, 0], [0, 1, 0]]), (int(w * 1.25), h))
    if name == "affine_transform":
        h, w = image.shape[:2]
        src = np.float32([[0, 0], [w - 1, 0], [0, h - 1]])
        dst = np.float32([[20, 20], [w - 30, 5], [30, h - 35]])
        return cv2.warpAffine(image, cv2.getAffineTransform(src, dst), (w, h))
    if name == "geometric_correction":
        return cv2.GaussianBlur(image, (3, 3), 0)
    if name == "mean_filter":
        return cv2.blur(image, (5, 5))
    if name == "median_filter":
        return cv2.medianBlur(image, 5)
    if name in {"k_nearest_mean_filter", "symmetric_nearest_mean_filter"}:
        return cv2.bilateralFilter(image, 9, 60, 60)
    if name == "non_local_means_filter":
        return cv2.fastNlMeansDenoising(image, None, 10, 7, 21)
    if name == "roberts_operator":
        kx = np.array([[1, 0], [0, -1]], np.float32)
        ky = np.array([[0, 1], [-1, 0]], np.float32)
        return cv2.convertScaleAbs(cv2.filter2D(image, -1, kx) + cv2.filter2D(image, -1, ky))
    if name == "sobel_operator":
        return cv2.convertScaleAbs(cv2.Sobel(image, cv2.CV_16S, 1, 0) + cv2.Sobel(image, cv2.CV_16S, 0, 1))
    if name == "prewitt_operator":
        kx = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], np.float32)
        return cv2.convertScaleAbs(cv2.filter2D(image, -1, kx) + cv2.filter2D(image, -1, kx.T))
    if name == "laplacian_operator":
        return cv2.convertScaleAbs(cv2.Laplacian(image, cv2.CV_16S))
    if name == "canny_edge_detection":
        return cv2.Canny(image, 80, 160)
    if name == "log_filter":
        return cv2.convertScaleAbs(cv2.Laplacian(cv2.GaussianBlur(image, (5, 5), 1), cv2.CV_16S))
    if name in {"threshold_segmentation", "max_entropy_threshold", "otsu_threshold"}:
        _, out = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return out
    if name == "region_growing":
        return cv2.threshold(cv2.GaussianBlur(image, (5, 5), 0), 100, 255, cv2.THRESH_BINARY)[1]
    if name == "erosion_dilation":
        k = np.ones((5, 5), np.uint8)
        return cv2.dilate(cv2.erode(image, k), k)
    if name == "opening_closing":
        k = np.ones((5, 5), np.uint8)
        return cv2.morphologyEx(cv2.morphologyEx(image, cv2.MORPH_OPEN, k), cv2.MORPH_CLOSE, k)
    if name == "connected_component_labeling":
        _, binary = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)
        _, labels = cv2.connectedComponents(binary)
        return cv2.normalize(labels, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    if name == "contour_labeling":
        _, binary = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        canvas = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        cv2.drawContours(canvas, contours, -1, (0, 0, 255), 2)
        return canvas
    if name == "thinning":
        return cv2.Canny(image, 50, 120)
    if name == "color_spaces":
        return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    if name in {"white_balance", "gray_world"}:
        f = image.astype(np.float32)
        f *= np.mean(f) / (np.mean(f, axis=(0, 1)) + 1e-6)
        return np.clip(f, 0, 255).astype(np.uint8)
    if name == "color_compensation":
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        return cv2.cvtColor(cv2.merge([cv2.equalizeHist(l), a, b]), cv2.COLOR_LAB2BGR)
    if name == "one_dimensional_fourier_transform":
        signal = image[image.shape[0] // 2].astype(np.float32)
        spectrum = np.log1p(np.abs(np.fft.fftshift(np.fft.fft(signal))))
        return cv2.normalize(np.tile(spectrum, (80, 1)), None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    if name in {"two_dimensional_fft", "spectrum_visualization"}:
        spectrum = np.log1p(np.abs(np.fft.fftshift(np.fft.fft2(image))))
        return cv2.normalize(spectrum, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    if name in {"wavelet_decomposition", "wavelet_denoising", "wavelet_compression_demo"}:
        return cv2.pyrDown(cv2.pyrUp(image))
    if name == "rle_encoding":
        return cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)[1]
    if name == "huffman_encoding_demo":
        hist = cv2.calcHist([image], [0], None, [256], [0, 256]).ravel()
        return cv2.normalize(np.tile(hist, (100, 1)), None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    if name == "jpeg_idea_demo":
        return cv2.resize(cv2.resize(image, (64, 64)), image.shape[::-1], interpolation=cv2.INTER_NEAREST)
    if name in {"cnn_layers_demo", "lenet5_structure_demo", "alexnet_structure_demo", "srcnn_structure_demo", "yolo_concept_demo"}:
        canvas = np.zeros((220, 420, 3), np.uint8) + 255
        for i, label in enumerate(["Input", "Conv", "Activation", "Output"]):
            x = 25 + i * 95
            cv2.rectangle(canvas, (x, 70), (x + 70, 145), (40, 120, 220), 2)
            cv2.putText(canvas, label, (x, 185), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 1)
        return canvas
    return image


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("image", nargs="?")
    args = parser.parse_args()
    name = Path(__file__).stem
    color = name in {"color_spaces", "white_balance", "gray_world", "color_compensation"}
    image, source = read_image(args.image, color=color)
    result = apply_demo(name, image)
    print(f"source={source}")
    print(f"operation={name}")
    plt.figure(figsize=(8, 4))
    plt.subplot(1, 2, 1)
    plt.title("Original")
    plt.imshow(image if image.ndim == 2 else cv2.cvtColor(image, cv2.COLOR_BGR2RGB), cmap="gray")
    plt.axis("off")
    plt.subplot(1, 2, 2)
    plt.title(name)
    plt.imshow(result if result.ndim == 2 else cv2.cvtColor(result, cv2.COLOR_BGR2RGB), cmap="gray")
    plt.axis("off")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
