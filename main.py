#!/usr/bin/env python3
"""Seventeen Syllables of Debugging.

A tiny deterministic program: it holds one haiku about debugging,
checks that it keeps the 5-7-5 syllable shape, and writes the three
lines as plain text to entry.txt inside the output directory
($MAKEFUN_OUTPUT_DIR, or /output when that is unset).

No network, no randomness, no input. The same haiku comes out
every run, byte for byte.
"""

import os
import sys

HAIKU = (
    "Three in the morning\n"
    "cursor blinks where the build broke\n"
    "one semicolon"
)

# Syllable counts for every word in the haiku, counted by hand.
SYLLABLES = {
    "three": 1,
    "in": 1,
    "the": 1,
    "morning": 2,
    "cursor": 2,
    "blinks": 1,
    "where": 1,
    "build": 1,
    "broke": 1,
    "one": 1,
    "semicolon": 4,
}

EXPECTED = (5, 7, 5)
MAX_CHARS = 200


def count_syllables(line):
    """Count the syllables of one line from the table above."""
    total = 0
    for word in line.split():
        key = word.strip(".,;:!?\"'").lower()
        if key not in SYLLABLES:
            raise ValueError("no syllable count for word: %r" % word)
        total += SYLLABLES[key]
    return total


def validate(text):
    """Check the haiku is three lines of 5-7-5, under 200 characters."""
    if not text or not text.strip():
        raise ValueError("haiku is empty")
    text.encode("utf-8")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "haiku is %d characters, over the 200 limit" % len(text)
        )
    lines = text.split("\n")
    if len(lines) != 3:
        raise ValueError("haiku must be exactly 3 lines, got %d" % len(lines))
    for line, want in zip(lines, EXPECTED):
        got = count_syllables(line)
        if got != want:
            raise ValueError(
                "line %r has %d syllables, want %d" % (line, got, want)
            )
    return lines


def main():
    validate(HAIKU)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(HAIKU)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except ValueError as error:
        print("error: %s" % error, file=sys.stderr)
        sys.exit(1)
