from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

from config import Config
from src.copier import copy_selected_files
from src.duplicate_detector import detect_exact_duplicates
from src.metadata import build_file_records
from src.reporter import write_reports
from src.scanner import scan_images
from src.selector import select_representatives
from src.verifier import verify_copies


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Safely consolidate iPhone image imports by copy-only deduplication")
    parser.add_argument("--source-dir", type=Path, default=Path("D:/Data/Pictures/iphone/Code/DemoTest"))
    parser.add_argument("--output-root", type=Path, default=None)
    parser.add_argument("--dry-run", action="store_true", help="Scan and report without copying")
    parser.add_argument("--verify-copy", dest="verify_copy", action="store_true", default=True)
    parser.add_argument("--no-verify-copy", dest="verify_copy", action="store_false")
    return parser.parse_args()


def build_output_dir(source_dir: Path, output_root: Path | None) -> Path:
    if output_root is None:
        output_root = source_dir.parent
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    return output_root / f"iphone_cleaned_{timestamp}"


def validate_paths(source_dir: Path, output_dir: Path) -> None:
    source_dir = source_dir.resolve()
    output_dir = output_dir.resolve()

    if not source_dir.exists() or not source_dir.is_dir():
        raise ValueError(f"Source directory does not exist or is not a directory: {source_dir}")

    if output_dir == source_dir or source_dir in output_dir.parents:
        raise ValueError("Output directory must be outside the source directory")


def run(config: Config, output_dir: Path) -> dict[str, int]:
    output_dir.mkdir(parents=True, exist_ok=False)
    files = scan_images(config.source_dir, config.supported_extensions)
    records = build_file_records(files, config.source_dir)
    duplicate_groups = detect_exact_duplicates(records)
    selected = select_representatives(duplicate_groups)

    copied = []
    if not config.dry_run:
        copied = copy_selected_files(selected, output_dir / "Images")
        if config.verify_copy:
            verify_copies(copied)

    stats = write_reports(
        output_dir=output_dir,
        records=records,
        duplicate_groups=duplicate_groups,
        selected=selected,
        copied_count=len(copied),
        dry_run=config.dry_run,
    )

    return stats


def main() -> int:
    args = parse_args()
    source_dir = args.source_dir.resolve()
    output_dir = build_output_dir(source_dir, args.output_root)
    validate_paths(source_dir, output_dir)

    config = Config(
        source_dir=source_dir,
        output_root=output_dir.parent,
        dry_run=args.dry_run,
        verify_copy=args.verify_copy,
    )
    stats = run(config, output_dir)

    print(f"Scan complete. Output: {output_dir}")
    print(f"Files scanned: {stats['files_scanned']}")
    print(f"Exact duplicate groups: {stats['duplicate_groups']}")
    print(f"Representatives selected: {stats['selected']}")
    print(f"Files copied: {stats['copied']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
