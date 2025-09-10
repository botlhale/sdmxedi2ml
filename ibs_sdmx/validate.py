from __future__ import annotations

from typing import List, Dict


def check_required(rows: List[Dict[str, str]], required: List[str]) -> List[str]:
    errors = []
    for i, r in enumerate(rows):
        for comp in required:
            if comp not in r or r[comp] in (None, "", "NA"):
                errors.append(f"Row {i}: missing {comp}")
    return errors