from __future__ import annotations

import argparse
from pathlib import Path

from .parser import parse_lines
from .mapping import load_config, tokens_to_rows, normalize, apply_confidentiality, finalize_numeric
from .convert import legacy_to_current
from .dsd import build_dsd
from .dataset import build_pandas_dataset
from .write import write_structures, write_dataset


DEFAULT_DEMO = [
    "ARR++Q:S:C:A:CAD:D:5J:A:CA:A:1C:2025220252:708:3244.00:A:N'",
    "ARR++Q:S:C:A:CAD:D:5J:A:CA:A:5J:2025220252:708:6244.00:A:F'",
]


def main():
    ap = argparse.ArgumentParser(description="Legacy BIS LBS -> SDMX 3.x (pysdmx) generator")
    ap.add_argument("--config", default="lbs_sdmx/mapping_config.yaml")
    ap.add_argument("--legacy-file", help="Path to legacy lines file (if omitted, demo lines used)")
    ap.add_argument("--structure-out", default="structure.xml")
    ap.add_argument("--data-out", default="data.xml")
    ap.add_argument("--sdmx-version", default="3.1", choices=["3.0", "3.1"])
    ap.add_argument("--agency", default="AGENCY")
    ap.add_argument("--version", default="1.0")
    ap.add_argument("--no-data", action="store_true", help="Only write structures, skip dataset")
    args = ap.parse_args()

    cfg = load_config(args.config)

    if args.legacy_file:
        lines = Path(args.legacy_file).read_text(encoding="utf-8").splitlines()
    else:
        lines = DEFAULT_DEMO

    parsed = parse_lines(lines)
    rows = tokens_to_rows(parsed, cfg)
    normalize(rows, cfg)
    apply_confidentiality(rows, cfg)
    legacy_to_current(rows, cfg)
    finalize_numeric(rows)

    # Build structures
    dsd = build_dsd(cfg, agency=args.agency, version=args.version)
    write_structures(dsd, args.structure_out, version=args.sdmx_version)

    if not args.no_data:
        try:
            dataset = build_pandas_dataset(rows, dsd)
            write_dataset(dataset, args.data_out, version=args.sdmx_version)
        except RuntimeError as e:
            print(f"Skipping dataset writing (pandas not installed): {e}")

    print("DONE.")


if __name__ == "__main__":
    main()