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


class Chapter10ExampleTest(unittest.TestCase):
    def test_compression_examples_expose_independent_core_functions(self):
        expected = {
            "rle_encoding.py": "run_length_encode",
            "huffman_encoding_demo.py": "huffman_code_lengths",
            "jpeg_idea_demo.py": "jpeg_block_demo",
            "wavelet_compression_demo.py": "wavelet_compress_demo",
        }
        folder = ROOT / "examples" / "10_image_compression"
        for filename, function_name in expected.items():
            with self.subTest(filename=filename):
                module = load_module(folder / filename)
                self.assertTrue(callable(getattr(module, function_name, None)))


class Chapter10CoverageToolTest(unittest.TestCase):
    def test_check_coverage_declares_chapter_10_requirements(self):
        module = load_module(ROOT / "tools" / "check_coverage.py")
        self.assertIn("10.1_图像冗余的概念.md", module.REQUIRED_CHAPTER10_WIKI)
        self.assertIn("ch10_compression_pipeline.png", module.REQUIRED_CHAPTER10_FIGURES)
        self.assertIn("rle_encoding.py", module.REQUIRED_CHAPTER10_CODE)


if __name__ == "__main__":
    unittest.main()
