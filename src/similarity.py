from __future__ import annotations

from src.metadata import FileRecord


def detect_near_duplicates(_records: list[FileRecord]) -> list[tuple[FileRecord, FileRecord]]:
    """Placeholder for perceptual similarity checks.

    The default behavior is conservative and returns no automatic near-duplicate matches.
    """

    return []
