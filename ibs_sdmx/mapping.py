from __future__ import annotations

import yaml
from typing import Any, Dict, List


def load_config(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def tokens_to_rows(parsed: List[List[str]], cfg: Dict[str, Any]) -> List[Dict[str, Any]]:
    token_map = cfg["legacy_token_map"]
    rows: List[Dict[str, Any]] = []
    for toks in parsed:
        row: Dict[str, Any] = {}
        for pos, comp_id in token_map.items():
            idx = int(pos)
            try:
                row[comp_id] = toks[idx]
            except IndexError:
                raise ValueError(f"Missing token index {idx} in {toks}")
        rows.append(row)
    return rows


def normalize(rows: List[Dict[str, Any]], cfg: Dict[str, Any]) -> None:
    norms = cfg.get("normalizations", {})
    for row in rows:
        for comp, mp in norms.items():
            if comp in row and row[comp] in mp:
                row[comp] = mp[row[comp]]


def apply_confidentiality(rows: List[Dict[str, Any]], cfg: Dict[str, Any]) -> None:
    conf_map = cfg.get("conf_status_map", {})
    break_map = cfg.get("break_status_map", {})
    for r in rows:
        r["CONF_STATUS"] = conf_map.get(r.get("CONF_STATUS_RAW_1"), r.get("CONF_STATUS_RAW_1"))
        r["BREAK_STATUS"] = break_map.get(r.get("CONF_STATUS_RAW_2"), r.get("CONF_STATUS_RAW_2"))


def finalize_numeric(rows: List[Dict[str, Any]]) -> None:
    for r in rows:
        val = r.get("OBS_VALUE")
        if val is not None:
            try:
                r["OBS_VALUE"] = float(val)
            except ValueError:
                r["OBS_VALUE"] = None