from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from config import SUPPORTED_EXTENSIONS
from src.scanner import scan_media


class TestScanner(unittest.TestCase):
    def test_scan_media_includes_images_and_videos(self) -> None:
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            image = root / "photo.JPG"
            video = root / "clip.MOV"
            ignored = root / "notes.txt"
            image.write_bytes(b"image")
            video.write_bytes(b"video")
            ignored.write_bytes(b"ignored")

            self.assertEqual(scan_media(root, SUPPORTED_EXTENSIONS), [image, video])


if __name__ == "__main__":
    unittest.main()