from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from src.hashing import sha256_file


@dataclass(frozen=True)
class FileRecord:
    path: Path
    relative_path: Path
    name: str
    extension: str
    size: int
    modified_ts: float
    sha256: str


def build_file_records(paths: list[Path], source_root: Path) -> list[FileRecord]:
    if not paths:
        return []

    records: list[FileRecord] = []
    root = source_root.resolve()
    for path in paths:
        resolved = path.resolve()
        stat = resolved.stat()
        try:
            relative = resolved.relative_to(root)
        except ValueError:
            relative = Path(resolved.name)
        records.append(
            FileRecord(
                path=resolved,
                relative_path=relative,
                name=resolved.name,
                extension=resolved.suffix.lower(),
                size=stat.st_size,
                modified_ts=stat.st_mtime,
                sha256=sha256_file(resolved),
            )
        )

    return records
