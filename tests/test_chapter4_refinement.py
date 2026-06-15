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


class Chapter4ExampleTest(unittest.TestCase):
    def test_denoising_examples_expose_independent_core_functions(self):
        expected = {
            "mean_filter.py": "mean_filter_image",
            "median_filter.py": "median_filter_image",
            "k_nearest_mean_filter.py": "k_nearest_mean_filter_image",
            "symmetric_nearest_mean_filter.py": "symmetric_nearest_mean_filter_image",
            "non_local_means_filter.py": "non_local_means_filter_image",
        }
        folder = ROOT / "examples" / "04_image_denoising"

        for filename, function_name in expected.items():
            with self.subTest(filename=filename):
                module = load_module(folder / filename)
                self.assertTrue(
                    callable(getattr(module, function_name, None)),
                    f"{filename} should define {function_name}()",
                )


class Chapter4CoverageToolTest(unittest.TestCase):
    def test_check_coverage_declares_chapter_4_requirements(self):
        module = load_module(ROOT / "tools" / "check_coverage.py")

        self.assertIn("4.1_图像噪声.md", module.REQUIRED_CHAPTER4_WIKI)
        self.assertIn("ch04_noise_models.png", module.REQUIRED_CHAPTER4_FIGURES)
        self.assertIn("mean_filter.py", module.REQUIRED_CHAPTER4_CODE)


if __name__ == "__main__":
    unittest.main()
