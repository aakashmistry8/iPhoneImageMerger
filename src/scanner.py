from __future__ import annotations

from pathlib import Path


def scan_media(source_dir: Path, supported_extensions: set[str]) -> list[Path]:
    extensions = {ext.lower() for ext in supported_extensions}
    files: list[Path] = []

    for path in source_dir.rglob("*"):
        if path.is_file() and path.suffix.lower() in extensions:
            files.append(path)

    return sorted(files)


def scan_images(source_dir: Path, supported_extensions: set[str]) -> list[Path]:
    """Backward-compatible alias for callers using the original API."""

    return scan_media(source_dir, supported_extensions)
