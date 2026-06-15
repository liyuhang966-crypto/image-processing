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


class Chapter7ExampleTest(unittest.TestCase):
    def test_binary_examples_expose_independent_core_functions(self):
        expected = {
            "erosion_dilation.py": "erode_binary",
            "opening_closing.py": "open_binary",
            "connected_component_labeling.py": "label_connected_components",
            "contour_labeling.py": "label_contours",
            "thinning.py": "thin_binary",
        }
        folder = ROOT / "examples" / "07_binary_image_processing"

        for filename, function_name in expected.items():
            with self.subTest(filename=filename):
                module = load_module(folder / filename)
                self.assertTrue(
                    callable(getattr(module, function_name, None)),
                    f"{filename} should define {function_name}()",
                )


class Chapter7CoverageToolTest(unittest.TestCase):
    def test_check_coverage_declares_chapter_7_requirements(self):
        module = load_module(ROOT / "tools" / "check_coverage.py")

        self.assertIn("7.1_二值图像中的基本概念.md", module.REQUIRED_CHAPTER7_WIKI)
        self.assertIn("ch07_morphology_erosion_dilation.png", module.REQUIRED_CHAPTER7_FIGURES)
        self.assertIn("thinning.py", module.REQUIRED_CHAPTER7_CODE)


if __name__ == "__main__":
    unittest.main()
