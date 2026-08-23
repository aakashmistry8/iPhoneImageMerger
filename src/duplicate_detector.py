from __future__ import annotations

from collections import defaultdict

from src.metadata import FileRecord


def detect_exact_duplicates(records: list[FileRecord]) -> dict[str, list[FileRecord]]:
    grouped: dict[str, list[FileRecord]] = defaultdict(list)
    for record in records:
        grouped[record.sha256].append(record)

    return {hash_value: group for hash_value, group in grouped.items() if len(group) >= 1}
