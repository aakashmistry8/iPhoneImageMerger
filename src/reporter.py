from __future__ import annotations

import csv
from pathlib import Path

from src.metadata import FileRecord


REPORT_HEADERS = ["path", "name", "extension", "size", "modified_ts", "sha256"]


def _write_scan_report(path: Path, records: list[FileRecord]) -> None:
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(REPORT_HEADERS)
        for record in records:
            writer.writerow(
                [
                    str(record.path),
                    record.name,
                    record.extension,
                    record.size,
                    f"{record.modified_ts:.6f}",
                    record.sha256,
                ]
            )


def _write_duplicate_report(path: Path, duplicate_groups: dict[str, list[FileRecord]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["sha256", "group_size", "selected_candidate", "path"])

        for hash_value, group in sorted(duplicate_groups.items()):
            if len(group) < 2:
                continue
            for record in group:
                writer.writerow([hash_value, len(group), "", str(record.path)])


def _write_review_report(path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["reason", "path_a", "path_b", "notes"])


def _write_summary(
    path: Path,
    files_scanned: int,
    duplicate_groups: int,
    selected: int,
    copied_count: int,
    dry_run: bool,
) -> None:
    with path.open("w", encoding="utf-8") as file:
        file.write("iPhone Image Organizer Summary\n")
        file.write("================================\n")
        file.write(f"Files scanned: {files_scanned}\n")
        file.write(f"Exact duplicate groups: {duplicate_groups}\n")
        file.write(f"Representatives selected: {selected}\n")
        file.write(f"Dry run: {'yes' if dry_run else 'no'}\n")
        file.write(f"Files copied: {copied_count}\n")


def write_reports(
    output_dir: Path,
    records: list[FileRecord],
    duplicate_groups: dict[str, list[FileRecord]],
    selected: list[FileRecord],
    copied_count: int,
    dry_run: bool,
) -> dict[str, int]:
    exact_duplicate_group_count = sum(1 for group in duplicate_groups.values() if len(group) > 1)

    reports_dir = output_dir / "Reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    _write_scan_report(reports_dir / "scan_report.csv", records)
    _write_duplicate_report(reports_dir / "duplicate_report.csv", duplicate_groups)
    _write_review_report(reports_dir / "review_report.csv")
    _write_summary(
        reports_dir / "summary.txt",
        files_scanned=len(records),
        duplicate_groups=exact_duplicate_group_count,
        selected=len(selected),
        copied_count=copied_count,
        dry_run=dry_run,
    )

    return {
        "files_scanned": len(records),
        "duplicate_groups": exact_duplicate_group_count,
        "selected": len(selected),
        "copied": copied_count,
    }
