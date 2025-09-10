from lbs_sdmx.parser import parse_legacy_line


def test_parse_line():
    line = "ARR++Q:S:C:A:CAD:D:5J:A:CA:A:1C:2025220252:708:3244.00:A:N'"
    toks = parse_legacy_line(line)
    assert toks[0] == "Q"
    assert toks[-1] == "N"
    assert len(toks) == 16
