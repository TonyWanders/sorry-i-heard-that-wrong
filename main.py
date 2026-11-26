#!/usr/bin/env python3
"""Write one funny smart-speaker apology to /output/entry.txt.

Deterministic: no network, no clock, no randomness. The apology is a fixed
string. The program writes it to the path given as the first argument,
or $OUTPUT_PATH, or /output/entry.txt by default, and enforces the
competition gate: 1 to 140 characters, not only white space.
"""

import os
import sys
from pathlib import Path

ENTRY = "Sorry, I heard 'dim the lights' as 'delete the flights', so your honeymoon is cancelled but the room looks lovely."

MIN_CHARS = 1
MAX_CHARS = 140
DEFAULT_PATH = "/output/entry.txt"


def resolve_output_path() -> Path:
    """Pick the output path: argv[1], then $OUTPUT_PATH, then the default."""
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    env_path = os.environ.get("OUTPUT_PATH")
    if env_path:
        return Path(env_path)
    return Path(DEFAULT_PATH)


def validate(text: str) -> int:
    """Enforce the competition gate: 1 to 140 chars, not only white space.

    Returns the character count. Raises ValueError when the gate fails.
    """
    chars = len(text)
    if not (MIN_CHARS <= chars <= MAX_CHARS):
        raise ValueError(f"entry is {chars} characters, outside 1-140")
    if not text.strip():
        raise ValueError("entry is only white space")
    return chars


def write_entry(text: str, path: Path) -> int:
    """Write the entry to the output target, creating parent dirs as needed.

    Returns the number of characters written.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return len(text)


def main() -> int:
    try:
        chars = validate(ENTRY)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1

    path = resolve_output_path()
    written = write_entry(ENTRY, path)
    print(f"wrote {written} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
