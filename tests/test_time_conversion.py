from lbs_sdmx.convert import convert_time


def test_time_conversion():
    rows = [{"TIME_PERIOD_RAW": "2025220252"}]
    cfg = {
        "time": {"quarterly": {"input_length": 10, "output_format": "{year}-Q{quarter}"}}
    }
    convert_time(rows, cfg)
    assert rows[0]["TIME_PERIOD"] == "2025-Q2"