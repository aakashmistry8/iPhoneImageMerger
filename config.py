from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


SUPPORTED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".heic",
    ".heif",
    ".png",
    ".webp",
    ".tif",
    ".tiff",
    ".bmp",
    ".gif",
    ".mov",
    ".mp4",
    ".m4v",
    ".avi",
    ".mkv",
    ".3gp",
}


@dataclass(frozen=True)
class Config:
    source_dir: Path
    output_root: Path
    dry_run: bool = False
    verify_copy: bool = True
    supported_extensions: set[str] = field(default_factory=lambda: set(SUPPORTED_EXTENSIONS))
