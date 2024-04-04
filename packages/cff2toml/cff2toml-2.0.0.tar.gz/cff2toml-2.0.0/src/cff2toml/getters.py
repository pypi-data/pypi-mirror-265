import functools
from typing import Any

import pydash

from cff2toml.cff2toml import DEFAULT_CITATION_CFF_FILE_PATH, DEFAULT_PYPROJECT_TOML_FILE_PATH, CFFObject, TOMLObject
from cff2toml.loaders import load_cff_object, load_toml_object


def get_object_property(obj: Any, property_path: str) -> Any:
    return pydash.objects.get(
        obj=obj, path=property_path)


def get_property_for_pyproject_toml(property_path: str, pyproject_toml_file_path: str = DEFAULT_PYPROJECT_TOML_FILE_PATH) -> Any:
    pyproject_toml_object: TOMLObject = load_toml_object(
        toml_file_path=pyproject_toml_file_path)

    value: Any = get_object_property(
        obj=pyproject_toml_object, property_path=property_path)

    return value


get_version_for_pyproject_toml = functools.partial(
    get_property_for_pyproject_toml, property_path="project.version")

get_name_for_pyproject_toml = functools.partial(
    get_property_for_pyproject_toml, property_path="project.name")

get_license_for_pyproject_toml = functools.partial(
    get_property_for_pyproject_toml, property_path="project.license")

get_description_for_pyproject_toml = functools.partial(
    get_property_for_pyproject_toml, property_path="project.description")


def get_property_for_citation_cff(property_path: str, citation_cff_file_path: str = DEFAULT_CITATION_CFF_FILE_PATH) -> Any:

    citation_cff_object: CFFObject = load_cff_object(
        cff_file_path=citation_cff_file_path)

    value: Any = get_object_property(
        obj=citation_cff_object, property_path=property_path)

    return value


get_version_for_citation_cff = functools.partial(
    get_property_for_citation_cff, property_path="version")

get_abstract_for_citation_cff = functools.partial(
    get_property_for_citation_cff, property_path="abstract")

get_title_for_citation_cff = functools.partial(
    get_property_for_citation_cff, property_path="title")

get_license_for_citation_cff = functools.partial(
    get_property_for_citation_cff, property_path="license")
