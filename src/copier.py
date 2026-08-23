from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

from src.metadata import FileRecord


@dataclass(frozen=True)
class CopyResult:
    source: Path
    destination: Path


def _next_collision_path(path: Path) -> Path:
    stem = path.stem
    suffix = path.suffix
    parent = path.parent
    counter = 1

    while True:
        candidate = parent / f"{stem}__dup{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def copy_selected_files(selected: list[FileRecord], images_dir: Path) -> list[CopyResult]:
    images_dir.mkdir(parents=True, exist_ok=True)
    copied: list[CopyResult] = []

    for record in selected:
        destination = images_dir / record.name
        if destination.exists():
            destination = _next_collision_path(destination)

        shutil.copy2(record.path, destination)
        copied.append(CopyResult(source=record.path, destination=destination))

    return copied
