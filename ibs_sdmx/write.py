from __future__ import annotations

from typing import Any
from pysdmx.io import write_sdmx
from pysdmx.io.format import Format


def write_structures(dsd, output_path: str, version: str = "3.1", pretty: bool = True):
    fmt = Format.STRUCTURE_SDMX_ML_3_1 if version == "3.1" else Format.STRUCTURE_SDMX_ML_3_0
    write_sdmx(
        dsd,
        output_path=output_path,
        sdmx_format=fmt,
        prettyprint=pretty,
    )


def write_dataset(dataset, output_path: str, version: str = "3.1", pretty: bool = True):
    fmt = Format.DATA_SDMX_ML_3_1 if version == "3.1" else Format.DATA_SDMX_ML_3_0
    write_sdmx(
        dataset,
        output_path=output_path,
        sdmx_format=fmt,
        prettyprint=pretty,
    )