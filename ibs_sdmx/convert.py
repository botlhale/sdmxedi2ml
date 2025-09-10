from __future__ import annotations

from typing import Dict, Any, List


def convert_time(rows: List[Dict[str, Any]], cfg: Dict[str, Any]) -> None:
    """
    Convert TIME_PERIOD_RAW -> TIME_PERIOD using heuristics for quarterly codes.
    """
    time_cfg = cfg.get("time", {}).get("quarterly", {})
    expected_len = time_cfg.get("input_length", 10)
    fmt = time_cfg.get("output_format", "{year}-Q{quarter}")
    for r in rows:
        raw = r.get("TIME_PERIOD_RAW")
        if raw and len(raw) == expected_len:
            year = raw[0:4]
            q = raw[4]
            r["TIME_PERIOD"] = fmt.format(year=year, quarter=q)
        else:
            r["TIME_PERIOD"] = raw  # fallback


def legacy_to_current(rows: List[Dict[str, Any]], cfg: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    High-level orchestrator to transform legacy dictionary rows into
    current SDMX-ready rows (dimension IDs, time, attributes).
    """
    convert_time(rows, cfg)
    # Remove raw columns if not wanted in final
    for r in rows:
        r.pop("TIME_PERIOD_RAW", None)
        r.pop("CONF_STATUS_RAW_1", None)
        r.pop("CONF_STATUS_RAW_2", None)
    return rows