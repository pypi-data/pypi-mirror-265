import os
from typing import Dict, List, Optional, Set

from graphlib import CycleError, TopologicalSorter

from goshawk.domain.model import SQLModel

from ..settings import Settings

app_settings = Settings()


def get_database_paths() -> List[str]:
    return [os.path.relpath(f.path) for f in os.scandir(app_settings.MODELS_PATH) if f.is_dir()]


def get_schema_paths(database_path: str) -> List[str]:
    return [f.path for f in os.scandir(database_path) if f.is_dir()]


def get_files(schema_path: str) -> List[str]:
    return [f.path for f in os.scandir(schema_path) if f.path.endswith(".sql")]


def schema_in_mask(schema_path: str, mask: str) -> bool:
    schema_db = schema_path.split("/")[-2].upper()
    schema_name = schema_path.split("/")[-1].upper()
    mask_db = mask.split(".")[0].upper()
    mask_schema = mask.split(".")[1].upper()
    if mask_db != schema_db:
        print(f"mask db{mask_db} not equal schema db {schema_db}")
        return False
    if mask_schema == "*":
        return True
    return mask_schema == schema_name


def schema_matches_mask(schema_path: str, masks: Optional[List[str]]) -> bool:
    if not masks:
        return True
    return any(schema_in_mask(schema_path, mask) for mask in masks)


def read_files(masks: Optional[List[str]] = None) -> List[SQLModel]:
    models = []
    for database_folder in get_database_paths():
        for schema_folder in get_schema_paths(database_folder):
            if schema_matches_mask(schema_folder, masks):
                for sqlfile in get_files(schema_folder):
                    model = SQLModel(database_folder, schema_folder, sqlfile, sqlfile)
                    models.append(model)
    return models


def build_dag_old(models: List[SQLModel]) -> TopologicalSorter:
    ts: TopologicalSorter = TopologicalSorter()
    for m in models:
        for s in m.schemas:
            ts.add(m._schema, s)
    return ts


def build_dag(models: List[SQLModel]) -> Dict[str, Set[str]]:
    child_models: Dict[str, Set[str]] = {}
    for m in models:
        child_models[m.fqn] = set()
        for parent_model in m.parent_tables:
            child_models[m.fqn].add(parent_model)
    return child_models


def build_schema_dag_old(models: List[SQLModel]) -> Dict[str, Set[str]]:
    schemas: Dict[str, Set[str]] = {}
    for m in models:
        if m._schema not in schemas:
            schemas[m._schema] = set()

        for t in m.parent_tables:
            tschema = f"{t.split('.')[0]}.{t.split('.')[1]}"
            if tschema != m._schema:
                schemas[m._schema].add(tschema)

    return schemas


def build_schema_dag(models: List[SQLModel]) -> Dict[str, Set[str]]:
    schemas: Dict[str, Set[str]] = {}
    for m in models:
        if m._schema not in schemas:
            schemas[m._schema] = set()

        for parent_schema in m.schemas:
            if parent_schema != m._schema:
                schemas[m._schema].add(parent_schema)

    return schemas


def validate_schema_dag(schema_dag: Dict[str, Set[str]]) -> bool:
    ts: TopologicalSorter = TopologicalSorter(schema_dag)
    try:
        ts.prepare()
    except CycleError:
        return False
    return True
