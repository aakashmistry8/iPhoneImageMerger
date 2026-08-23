from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from src.copier import _next_collision_path


class TestCollisionHandling(unittest.TestCase):
    def test_next_collision_path_increments_suffix(self) -> None:
        with TemporaryDirectory() as tmpdir:
            image_dir = Path(tmpdir)
            first = image_dir / "IMG_0001.JPG"
            second = image_dir / "IMG_0001__dup1.JPG"
            first.write_text("a", encoding="utf-8")
            second.write_text("b", encoding="utf-8")

            candidate = _next_collision_path(first)

            self.assertEqual(candidate.name, "IMG_0001__dup2.JPG")


if __name__ == "__main__":
    unittest.main()
