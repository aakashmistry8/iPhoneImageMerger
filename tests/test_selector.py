from __future__ import annotations

from pathlib import Path
import unittest

from src.metadata import FileRecord
from src.selector import select_representatives


class TestSelector(unittest.TestCase):
    def test_select_representatives_prefers_earlier_modified(self) -> None:
        older = FileRecord(Path("/tmp/older.jpg"), Path("older.jpg"), "older.jpg", ".jpg", 1, 1.0, "hash")
        newer = FileRecord(Path("/tmp/newer.jpg"), Path("newer.jpg"), "newer.jpg", ".jpg", 1, 2.0, "hash")

        selected = select_representatives({"hash": [newer, older]})

        self.assertEqual([older], selected)


if __name__ == "__main__":
    unittest.main()
