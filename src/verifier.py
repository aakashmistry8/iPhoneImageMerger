from __future__ import annotations

from src.copier import CopyResult
from src.hashing import sha256_file


def verify_copies(copied: list[CopyResult]) -> None:
    for result in copied:
        src_hash = sha256_file(result.source)
        dst_hash = sha256_file(result.destination)
        if src_hash != dst_hash:
            raise ValueError(f"Copy verification failed: {result.source} -> {result.destination}")
