#!/usr/bin/env python3
"""Entry program for the make.fun bounty
"One Line, One Minute: The Vending Machine Pickup Line Contest".

Reads the single pickup line from entry.txt next to this script, validates
it against the competition gate (UTF-8 text, 1 to 200 characters, exactly
one line, not only whitespace), and writes it byte-for-byte to
$MAKEFUN_OUTPUT_DIR/entry.txt.

Python 3.13, standard library only.
"""

import os
import sys

MAX_CHARS = 200


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(here, "entry.txt")

    with open(src_path, "rb") as f:
        raw = f.read()

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        print(f"entry.txt is not valid UTF-8: {exc}", file=sys.stderr)
        return 1

    if not 1 <= len(text) <= MAX_CHARS:
        print(
            f"gate failed: entry is {len(text)} characters, must be 1-{MAX_CHARS}",
            file=sys.stderr,
        )
        return 1

    if "\n" in text or "\r" in text:
        print("gate failed: entry must be exactly one line", file=sys.stderr)
        return 1

    if not text.strip():
        print("gate failed: entry must not be only whitespace", file=sys.stderr)
        return 1

    if any(ord(ch) < 0x20 for ch in text):
        print("gate failed: entry must not contain control characters", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "wb") as f:
        f.write(raw)

    with open(out_path, "rb") as f:
        written = f.read()
    if written != raw:
        print("verify failed: written bytes differ from entry.txt", file=sys.stderr)
        return 1

    print(f"wrote {len(raw)} bytes ({len(text)} chars) to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
