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


class Chapter11ExampleTest(unittest.TestCase):
    def test_deep_learning_examples_expose_independent_core_functions(self):
        expected = {
            "cnn_layers_demo.py": "draw_cnn_layers",
            "srcnn_structure_demo.py": "draw_srcnn_structure",
            "lenet5_structure_demo.py": "draw_lenet5_structure",
            "alexnet_structure_demo.py": "draw_alexnet_structure",
            "yolo_concept_demo.py": "draw_yolo_concept",
        }
        folder = ROOT / "examples" / "11_deep_learning_image_processing"
        for filename, function_name in expected.items():
            with self.subTest(filename=filename):
                module = load_module(folder / filename)
                self.assertTrue(callable(getattr(module, function_name, None)))


class Chapter11CoverageToolTest(unittest.TestCase):
    def test_check_coverage_declares_chapter_11_requirements(self):
        module = load_module(ROOT / "tools" / "check_coverage.py")
        self.assertIn("11.1_深度卷积网络的基本结构.md", module.REQUIRED_CHAPTER11_WIKI)
        self.assertIn("ch11_cnn_layers.png", module.REQUIRED_CHAPTER11_FIGURES)
        self.assertIn("yolo_concept_demo.py", module.REQUIRED_CHAPTER11_CODE)


if __name__ == "__main__":
    unittest.main()
