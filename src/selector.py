from __future__ import annotations

from src.metadata import FileRecord


def select_representatives(duplicate_groups: dict[str, list[FileRecord]]) -> list[FileRecord]:
    selected: list[FileRecord] = []

    for group in duplicate_groups.values():
        # Date priority first, then larger size, then stable path order.
        representative = sorted(
            group,
            key=lambda record: (record.modified_ts, -record.size, str(record.path)),
        )[0]
        selected.append(representative)

    return sorted(selected, key=lambda record: str(record.path))
