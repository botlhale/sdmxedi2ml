# pysdmx LBS Conversion

Convert legacy BIS LBS (Locational Banking Statistics) colon-separated lines (old SDMX-like layout) into proper SDMX 3.0/3.1 structures & datasets using only the `pysdmx` library (your opinionated Python SDMX implementation).

## Features

- Parse legacy lines such as:

  ```
  ARR++Q:S:C:A:CAD:D:5J:A:CA:A:1C:2025220252:708:3244.00:A:N'
  ```

- Map tokens to dimension IDs defined in a configurable YAML file.
- Convert legacy internal time tokens (e.g. `2025220252`) to `YYYY-Qn` (e.g. `2025-Q2`).
- Extract confidentiality pair `A:N` → `CONF_STATUS=Restricted`, `BREAK_STATUS=NoBreak`.
- Build minimal `DataStructureDefinition`, supporting:
  - Dimensions
  - Primary Measure
  - Observation Attributes
  - Concept Scheme & Codelists (stubbed; replace with real BIS metadata if available).
- Serialize:
  - SDMX-ML 3.1 (or 3.0) Structures (`Format.STRUCTURE_SDMX_ML_3_1`)
  - SDMX-ML 3.1 Data (`Format.DATA_SDMX_ML_3_1`)

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
# If you want dataset -> PandasDataset convenience:
pip install pandas
```

## Configuration

Edit `lbs_sdmx/mapping_config.yaml` to:
- Reorder dimensions
- Add or normalize codes
- Adjust confidentiality mapping
- Extend codelists or replace stubs with authoritative BIS lists

## Usage

Example (uses demo embedded lines if no input provided):

```bash
python -m lbs_sdmx.cli \
  --legacy-file legacy_lines.txt \
  --structure-out structure.xml \
  --data-out data.xml \
  --sdmx-version 3.1
```

Outputs:
- `structure.xml`: SDMX-ML 3.1 structures (DSD etc.)
- `data.xml`: SDMX-ML 3.1 dataset

## Legacy Line Format (Token Mapping)

| Index | Example | Meaning (Config ID) |
|-------|---------|---------------------|
| 0 | Q | FREQ |
| 1 | S | MEASURE |
| 2 | C | POSITION |
| 3 | A | INSTR |
| 4 | CAD | CURR_DENOM |
| 5 | D | CURR_TYPE |
| 6 | 5J | PARENT_CNTRY |
| 7 | A | REPORTING_INST_TYPE |
| 8 | CA | REPORTER |
| 9 | A | CP_SECTOR |
| 10 | 1C | CP_COUNTRY |
| 11 | 2025220252 | TIME_PERIOD_RAW (→ TIME_PERIOD) |
| 12 | 708 | SERIES_ID (optional / internal) |
| 13 | 3244.00 | OBS_VALUE |
| 14 | A | CONF_STATUS_RAW_1 |
| 15 | N | CONF_STATUS_RAW_2 |

Adjust to real BIS DSD naming if required.

## Time Conversion

Default heuristic (`convert.parse_quarter_time`) expects a 10-char pattern where:
- First 4 chars = year
- 5th char = quarter number
- Remainder duplicates and is ignored

`2025220252` → `2025-Q2`.

## Replacing Stub Structures with Real BIS Metadata

1. Retrieve official BIS DSD via SDMX-REST 2.0 endpoint (supported by `pysdmx`).
2. Override mapping dimension IDs to match official concept IDs.
3. Skip code list creation in `dsd.py` if you rely on the loaded structure’s existing codelists.

## Tests

```bash
pytest -q
```

## Extending

- Add additional observation attributes (e.g. DECIMALS, UNIT_MULT).
- Introduce content constraints for validation.
- Support SDMX-JSON 2.0 output (adapt `write_sdmx` call with JSON formats if available).

## License

MIT
