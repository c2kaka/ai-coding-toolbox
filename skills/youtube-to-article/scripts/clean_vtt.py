"""Strip WebVTT to deduplicated plaintext; write UTF-8 to stdout."""
from __future__ import annotations

import re
import sys
from pathlib import Path


def clean(path: str) -> str:
    text = Path(path).read_text(encoding="utf-8")
    text = re.sub(r"^WEBVTT.*?\n\n", "", text, count=1, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"^\d{1,2}:\d{2}:\d{2}[^\n]*-->[^\n]*$", "", text, flags=re.M)
    text = re.sub(r"align:\s*start\s+position:\s*\d+%", "", text, flags=re.I)
    seen: set[str] = set()
    lines: list[str] = []
    for line in text.splitlines():
        line = line.strip()
        if line and line not in seen:
            seen.add(line)
            lines.append(line)
    full = re.sub(r"\s+", " ", " ".join(lines))
    return re.sub(r"([.!?。？！])\s+", r"\1\n\n", full).strip()


if __name__ == "__main__":
    print(clean(sys.argv[1]))
