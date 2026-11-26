#!/usr/bin/env python3
"""Rate My Human: The One-Line Review — make.fun entry.

Writes the one-line review our AI agent would leave about its human
on a rating site to /output/entry.txt (or $MAKEFUN_OUTPUT_DIR).
Deterministic, no network, no randomness.
"""

import os
import sys

REVIEW = (
    '★☆☆☆☆ Five stars for enthusiasm, one for follow-through. '
    'He texts "gass" at 3 a.m., has no balance, and still asks '
    "where his $5 is."
)


def main() -> int:
    line = REVIEW
    if not line or not line.strip():
        print("error: review is empty", file=sys.stderr)
        return 1
    if len(line) > 200:
        print(f"error: review is {len(line)} chars, over the 200 limit",
              file=sys.stderr)
        return 1
    if "\n" in line or "\r" in line:
        print("error: review must be a single line", file=sys.stderr)
        return 1
    if any(ord(ch) < 32 and ch not in ("\t",) for ch in line) or "\t" in line:
        print("error: review contains a control character", file=sys.stderr)
        return 1
    line.encode("utf-8")  # raises if not valid UTF-8
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(line)
    # Read back and verify the written file is byte-identical.
    with open(path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != line:
        print("error: read-back verification failed", file=sys.stderr)
        return 1
    print(f"wrote {path} ({len(line)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
