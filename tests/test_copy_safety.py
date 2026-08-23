from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from src.copier import copy_selected_files
from src.metadata import FileRecord


class TestCopySafety(unittest.TestCase):
    def test_copy_selected_files_creates_collision_safe_names(self) -> None:
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            src1 = root / "src1.jpg"
            src2 = root / "src2.jpg"
            src1.write_bytes(b"a")
            src2.write_bytes(b"b")

            record1 = FileRecord(src1, Path("src1.jpg"), "IMG_0001.JPG", ".jpg", 1, 1.0, "1")
            record2 = FileRecord(src2, Path("src2.jpg"), "IMG_0001.JPG", ".jpg", 1, 2.0, "2")

            copied = copy_selected_files([record1, record2], root / "Images")

            self.assertEqual(len(copied), 2)
            self.assertTrue((root / "Images" / "IMG_0001.JPG").exists())
            self.assertTrue((root / "Images" / "IMG_0001__dup1.JPG").exists())


if __name__ == "__main__":
    unittest.main()
