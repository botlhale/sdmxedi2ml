from __future__ import annotations

from typing import List

ARR_PREFIX = "ARR++"


def parse_legacy_line(line: str) -> list[str]:
    """
    Parse a single legacy line like:
    ARR++Q:S:C:A:CAD:D:5J:A:CA:A:1C:2025220252:708:3244.00:A:N'
    Returns tokens (excluding ARR++ and trailing apostrophe).
    """
    original = line
    line = line.strip()
    if not line:
        raise ValueError("Empty line")
    if line.endswith("'"):
        line = line[:-1]
    if not line.startswith(ARR_PREFIX):
        raise ValueError(f"Line does not start with {ARR_PREFIX}: {original}")
    payload = line[len(ARR_PREFIX):]
    return payload.split(":")


def parse_lines(lines: List[str]) -> list[list[str]]:
    out = []
    for l in lines:
        l = l.strip()
        if not l:
            continue
        out.append(parse_legacy_line(l))
    return out