#!/usr/bin/env python3
"""Verify the handoff's original files, without accessing a device or network."""
import hashlib
from pathlib import Path, PurePosixPath
import sys


def main():
    root = Path(__file__).resolve().parent
    failures = []
    checked = 0
    for line in (root / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
        digest, name = line.split("  ", 1)
        relative = PurePosixPath(name)
        if relative.is_absolute() or ".." in relative.parts or "\\" in name:
            failures.append(f"Invalid manifest path: {name}")
            continue
        path = root.joinpath(*relative.parts)
        try:
            value = hashlib.sha256()
            with path.open("rb") as source:
                for chunk in iter(lambda: source.read(1024 * 1024), b""):
                    value.update(chunk)
            if value.hexdigest() != digest:
                failures.append(f"Changed: {name}")
            checked += 1
        except OSError as error:
            failures.append(f"Cannot read {name}: {error}")
    for failure in failures:
        print(failure)
    print(f"Checked {checked} files; {len(failures)} errors.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
