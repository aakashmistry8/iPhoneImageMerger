from __future__ import annotations

from pathlib import Path
import unittest

from src.duplicate_detector import detect_exact_duplicates
from src.metadata import FileRecord


class TestDuplicates(unittest.TestCase):
    def test_detect_exact_duplicates_groups_by_hash(self) -> None:
        record_a = FileRecord(Path("/tmp/a.jpg"), Path("a.jpg"), "a.jpg", ".jpg", 10, 1.0, "abc")
        record_b = FileRecord(Path("/tmp/b.jpg"), Path("b.jpg"), "b.jpg", ".jpg", 12, 2.0, "abc")
        record_c = FileRecord(Path("/tmp/c.jpg"), Path("c.jpg"), "c.jpg", ".jpg", 9, 3.0, "def")

        grouped = detect_exact_duplicates([record_a, record_b, record_c])

        self.assertIn("abc", grouped)
        self.assertIn("def", grouped)
        self.assertEqual(len(grouped["abc"]), 2)
        self.assertEqual(len(grouped["def"]), 1)


if __name__ == "__main__":
    unittest.main()
