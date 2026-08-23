from __future__ import annotations

import hashlib
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from src.hashing import sha256_file


class TestHashing(unittest.TestCase):
    def test_sha256_file_matches_hashlib(self) -> None:
        with TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "sample.jpg"
            data = b"image-bytes" * 100
            path.write_bytes(data)

            self.assertEqual(sha256_file(path), hashlib.sha256(data).hexdigest())


if __name__ == "__main__":
    unittest.main()
