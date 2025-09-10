from __future__ import annotations

from typing import Dict, Any, List, Optional

try:
    from pysdmx.io.pd import PandasDataset  # Optional
    import pandas as pd
except ImportError:  # pragma: no cover
    PandasDataset = None  # type: ignore
    pd = None  # type: ignore


def build_pandas_dataset(rows: List[Dict[str, Any]], dsd):
    """
    Build a PandasDataset if pandas is available; else raise.
    """
    if PandasDataset is None or pd is None:
        raise RuntimeError("pandas not installed. Install extras or implement a custom dataset builder.")
    # Keep only DSD components + measure + attributes
    comp_ids = [c.id for c in dsd.components]
    filtered_rows = []
    for r in rows:
        filtered_rows.append({k: r.get(k) for k in comp_ids})
    df = pd.DataFrame(filtered_rows)
    schema = dsd.to_schema()
    return PandasDataset(data=df, structure=schema)