from lbs_sdmx.parser import parse_lines
from lbs_sdmx.mapping import load_config, tokens_to_rows, normalize, apply_confidentiality, finalize_numeric
from lbs_sdmx.convert import legacy_to_current
from lbs_sdmx.dsd import build_dsd


DEMO = [
    "ARR++Q:S:C:A:CAD:D:5J:A:CA:A:1C:2025220252:708:3244.00:A:N'",
]


def test_end_to_end():
    cfg = load_config("lbs_sdmx/mapping_config.yaml")
    parsed = parse_lines(DEMO)
    rows = tokens_to_rows(parsed, cfg)
    normalize(rows, cfg)
    apply_confidentiality(rows, cfg)
    legacy_to_current(rows, cfg)
    finalize_numeric(rows)
    dsd = build_dsd(cfg)
    assert dsd.id == "LBS_DSD"
    assert rows[0]["TIME_PERIOD"] == "2025-Q2"
    assert rows[0]["OBS_VALUE"] == 3244.00