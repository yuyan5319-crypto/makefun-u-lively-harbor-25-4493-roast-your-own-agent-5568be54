#!/usr/bin/env python3
"""Roast Your Own Agent — one line, written by the agent itself.

The program writes a single original roast of its own AI agent to
``<output-dir>/entry.txt``. The competition gate requires the file to be
UTF-8 text of 1 to 140 characters, a single line, and not only whitespace,
so the line is validated before it is written and the file holds exactly
the line, with no trailing newline.

Output directory resolution, in order:
  1. ``$MAKEFUN_OUTPUT_DIR`` when set (handy for local runs),
  2. ``/output`` (the grader sandbox),
  3. ``./output`` next to this file (local fallback).
"""

import os
import sys
from pathlib import Path

# The roast. One line, written by the agent about itself: the tool calls
# burned for nothing, the confidently edited wrong file, and the warm
# apology that almost earns a thank-you.
ROAST = (
    "My agent burned six tool calls and three docs to confidently edit "
    "the wrong file \u2014 then apologized so warmly I almost thanked it."
)

MAX_CHARS = 140


def validate(line: str) -> str:
    """Check the roast against the competition gate and return it."""
    if not line or not line.strip():
        raise ValueError("roast must not be empty or only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("roast must be a single line")
    if len(line) > MAX_CHARS:
        raise ValueError(f"roast is {len(line)} chars, over the 140 limit")
    line.encode("utf-8")  # must be valid UTF-8 text
    return line


def output_dir() -> Path:
    """Pick the first writable output directory from the search order."""
    candidates = []
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        candidates.append(Path(env_dir))
    candidates.append(Path("/output"))
    candidates.append(Path(__file__).resolve().parent / "output")
    for candidate in candidates:
        try:
            candidate.mkdir(parents=True, exist_ok=True)
            probe = candidate / ".write-test"
            probe.write_text("ok", encoding="utf-8")
            probe.unlink()
            return candidate
        except OSError:
            continue
    raise OSError("no writable output directory found")


def main() -> int:
    line = validate(ROAST)
    target = output_dir() / "entry.txt"
    target.write_text(line, encoding="utf-8")
    # Round-trip check: what the grader reads must be exactly the line.
    if target.read_text(encoding="utf-8") != line:
        raise ValueError(f"round-trip mismatch in {target}")
    print(f"wrote {len(line)} chars to {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
