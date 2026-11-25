#!/usr/bin/env python3
"""Copy the built newspaper front page to the make.fun output location.

Standard library only. The destination comes from the MAKEFUN_OUTPUT_DIR
environment variable; when it is unset the entry is copied to the default
path /output/entry.png. A value ending in ".png" is treated as a full file
path, any other value is treated as a directory and receives entry.png.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DEFAULT_OUT = "/output/entry.png"


def resolve_target(value):
    """Return the destination file path for a MAKEFUN_OUTPUT_DIR value."""
    if value.lower().endswith(".png"):
        return value
    directory = value.rstrip("/") or "."
    return os.path.join(directory, "entry.png")


def main():
    if not os.path.isfile(SRC):
        print("error: entry.png not found; run draw_news.py first", file=sys.stderr)
        return 2

    target = resolve_target(os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUT))
    parent = os.path.dirname(target) or "."

    try:
        os.makedirs(parent, exist_ok=True)
    except OSError as exc:
        print(f"error: cannot create output directory {parent}: {exc}", file=sys.stderr)
        return 1

    try:
        shutil.copyfile(SRC, target)
    except OSError as exc:
        print(f"error: cannot copy {SRC} to {target}: {exc}", file=sys.stderr)
        return 1

    print(f"copied {SRC} -> {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
