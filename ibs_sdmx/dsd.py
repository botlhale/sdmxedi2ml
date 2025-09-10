from __future__ import annotations

from typing import Dict, Any, List

from pysdmx.model import (
    DataStructureDefinition,
    Components,
    Component,
    Role,
    ItemReference,
    Facets,
    DataType,
    Codelist,
    Code,
    ConceptScheme,
    Concept,
)


def build_concept_scheme(cfg: Dict[str, Any], agency: str = "AGENCY", version: str = "1.0") -> ConceptScheme:
    concepts = []
    for dim in cfg["dimension_order"]:
        concepts.append(Concept(id=dim, name=dim))
    concepts.append(Concept(id="OBS_VALUE", name="Observation Value"))
    for attr in cfg.get("obs_attributes", []):
        concepts.append(Concept(id=attr, name=attr))
    return ConceptScheme(
        id="CS_LBS",
        version=version,
        agency=agency,
        name="ConceptScheme LBS",
        concepts=concepts,
    )


def build_codelists(cfg: Dict[str, Any], agency: str = "AGENCY", version: str = "1.0") -> List[Codelist]:
    cls = []
    for cid, codes in cfg.get("codelists", {}).items():
        cls.append(
            Codelist(
                id=f"CL_{cid}",
                version=version,
                agency=agency,
                name=f"Codelist {cid}",
                codes=[Code(id=c["id"], name=c.get("name", c["id"])) for c in codes],
            )
        )
    # Confidentiality attribute lists (if you want to treat them as codes)
    conf_map = cfg.get("conf_status_map", {})
    if conf_map:
        cls.append(
            Codelist(
                id="CL_CONF_STATUS",
                version=version,
                agency=agency,
                name="Confidentiality Status",
                codes=[Code(id=k, name=v) for k, v in conf_map.items()],
            )
        )
    break_map = cfg.get("break_status_map", {})
    if break_map:
        cls.append(
            Codelist(
                id="CL_BREAK_STATUS",
                version=version,
                agency=agency,
                name="Break Status",
                codes=[Code(id=k, name=v) for k, v in break_map.items()],
            )
        )
    return cls


def _concept_ref(concept_id: str, agency: str, version: str) -> ItemReference:
    # In tests we saw an ItemReference specifying concept scheme & item.
    return ItemReference(
        sdmx_type="Concept",
        agency=agency,
        id="CS_LBS",  # concept scheme ID
        version=version,
        item_id=concept_id,
    )


def build_dsd(cfg: Dict[str, Any], agency: str = "AGENCY", version: str = "1.0") -> DataStructureDefinition:
    cs = build_concept_scheme(cfg, agency=agency, version=version)
    codelists = build_codelists(cfg, agency=agency, version=version)

    components = []
    # Dimensions
    for dim_id in cfg["dimension_order"]:
        components.append(
            Component(
                id=dim_id,
                required=True,
                role=Role.DIMENSION,
                concept=_concept_ref(dim_id, agency, version),
                local_dtype=DataType.STRING,
                # Example facet: min_length=1
                local_facets=Facets(min_length="1"),
            )
        )
    # Primary measure
    components.append(
        Component(
            id="OBS_VALUE",
            required=True,
            role=Role.MEASURE,  # or Role.PRIMARY_MEASURE if defined
            concept=_concept_ref("OBS_VALUE", agency, version),
            local_dtype=DataType.FLOAT,
        )
    )
    # Observation attributes
    for attr_id in cfg.get("obs_attributes", []):
        components.append(
            Component(
                id=attr_id,
                required=False,
                role=Role.ATTRIBUTE,
                concept=_concept_ref(attr_id, agency, version),
                local_dtype=DataType.STRING,
                attachment_level="Observation",
            )
        )

    return DataStructureDefinition(
        id="LBS_DSD",
        name="Minimal LBS DSD",
        version=version,
        agency=agency,
        components=Components(components),
        annotations=(),
    )