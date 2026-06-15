import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(path: Path):
    previous_utils = sys.modules.pop("_utils", None)
    previous_path = list(sys.path)
    sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    try:
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path[:] = previous_path
        sys.modules.pop("_utils", None)
        if previous_utils is not None:
            sys.modules["_utils"] = previous_utils


class Chapter9ExampleTest(unittest.TestCase):
    def test_transform_examples_expose_independent_core_functions(self):
        expected = {
            "one_dimensional_fourier_transform.py": "one_dimensional_spectrum",
            "two_dimensional_fft.py": "two_dimensional_spectrum",
            "spectrum_visualization.py": "visualize_spectrum",
            "wavelet_decomposition.py": "wavelet_decompose_image",
            "wavelet_denoising.py": "wavelet_denoise_image",
        }
        folder = ROOT / "examples" / "09_image_transform"

        for filename, function_name in expected.items():
            with self.subTest(filename=filename):
                module = load_module(folder / filename)
                self.assertTrue(callable(getattr(module, function_name, None)))


class Chapter9CoverageToolTest(unittest.TestCase):
    def test_check_coverage_declares_chapter_9_requirements(self):
        module = load_module(ROOT / "tools" / "check_coverage.py")
        self.assertIn("9.1_图像的频域变换（傅里叶变换）.md", module.REQUIRED_CHAPTER9_WIKI)
        self.assertIn("ch09_fft_spectrum.png", module.REQUIRED_CHAPTER9_FIGURES)
        self.assertIn("wavelet_denoising.py", module.REQUIRED_CHAPTER9_CODE)


if __name__ == "__main__":
    unittest.main()
