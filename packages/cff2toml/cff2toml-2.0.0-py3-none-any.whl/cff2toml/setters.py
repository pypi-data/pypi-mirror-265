import functools
from typing import Any, Callable, List, Tuple
import pydash

from cff2toml.cff2toml import DEFAULT_CITATION_CFF_FILE_PATH, DEFAULT_PYPROJECT_TOML_FILE_PATH, T, CFFObject, TOMLObject
from cff2toml.getters import get_object_property
from cff2toml.loaders import load_cff_object, load_toml_object
from cff2toml.savers import save_cff_object, save_toml_object

TransformCFFObjectWithTOMLObjectFunction = Callable[[
    CFFObject, TOMLObject], CFFObject]
TransformTOMLObjectWithCFFObjectFunction = Callable[[
    TOMLObject, CFFObject], TOMLObject]


class SetCFFPropertyException(Exception):
    pass


class SetTOMLPropertyException(Exception):
    pass


def set_toml_with_cff(toml_file_path: str, cff_file_path: str, transform_toml_object_func: TransformTOMLObjectWithCFFObjectFunction) -> TOMLObject:

    toml_object: TOMLObject = load_toml_object(toml_file_path=toml_file_path)
    cff_object: CFFObject = load_cff_object(cff_file_path=cff_file_path)

    toml_object: TOMLObject = transform_toml_object_func(
        toml_object, cff_object)

    save_toml_object(toml_object=toml_object,
                     toml_file_path=toml_file_path)

    return toml_object


def set_cff_with_toml(cff_file_path: str, toml_file_path: str, transform_cff_object_func: TransformCFFObjectWithTOMLObjectFunction) -> CFFObject:

    toml_object: TOMLObject = load_toml_object(toml_file_path=toml_file_path)
    cff_object: CFFObject = load_cff_object(cff_file_path=cff_file_path)

    cff_object: CFFObject = transform_cff_object_func(cff_object, toml_object)

    save_cff_object(cff_object=cff_object,
                    cff_file_path=cff_file_path)

    return cff_object


def set_pyproject_toml_with_citation_cff(pyproject_toml_file_path=DEFAULT_PYPROJECT_TOML_FILE_PATH, citation_cff_file_path=DEFAULT_CITATION_CFF_FILE_PATH) -> TOMLObject:
    def transformer(pyproject_toml_object: TOMLObject, citation_cff_object: CFFObject) -> TOMLObject:

        transform_mappings: List[Tuple[str, str]] = [
            ("project.name", "title"),
            ("project.version", "version"),
            ("project.description", "abstract"),
            ("project.license", "license"),
            ("project.urls.Source", "repository-code"),
        ]
        for toml_property_path, cff_property_path in transform_mappings:
            pyproject_toml_object = set_toml_property_with_cff_property(toml_property_path=toml_property_path,
                                                                        toml_object=pyproject_toml_object,
                                                                        cff_property_path=cff_property_path,
                                                                        cff_object=citation_cff_object)
        return pyproject_toml_object
    return set_toml_with_cff(toml_file_path=pyproject_toml_file_path, cff_file_path=citation_cff_file_path, transform_toml_object_func=transformer)


def set_citation_cff_with_pyproject_toml(citation_cff_file_path=DEFAULT_CITATION_CFF_FILE_PATH, pyproject_toml_file_path=DEFAULT_PYPROJECT_TOML_FILE_PATH) -> CFFObject:
    def transformer(citation_cff_object: CFFObject, pyproject_toml_object: TOMLObject) -> CFFObject:

        transform_mappings: List[Tuple[str, str]] = [
            ("title", "project.name"),
            ("version", "project.version"),
            ("abstract", "project.description"),
            ("license", "project.license"),
            ("repository-code", "project.urls.Source"),
        ]
        for cff_property_path, toml_property_path in transform_mappings:
            citation_cff_object = set_cff_property_with_toml_property(cff_property_path=cff_property_path,
                                                                      cff_object=citation_cff_object,
                                                                      toml_property_path=toml_property_path,
                                                                      toml_object=pyproject_toml_object)

        return citation_cff_object
    return set_cff_with_toml(toml_file_path=pyproject_toml_file_path, cff_file_path=citation_cff_file_path, transform_cff_object_func=transformer)


def set_toml_property_with_cff_property(toml_property_path: str, toml_object: TOMLObject, cff_property_path: str, cff_object: CFFObject) -> TOMLObject:
    # uses pydash deep path strings to specify properties
    value = get_object_property(
        obj=cff_object, property_path=cff_property_path)
    if value is None:
        raise SetTOMLPropertyException(
            f"Cannot set TOML property ({toml_property_path}) with CFF property ({cff_property_path}) because CFF property cannot be found.")
    return pydash.objects.set_(
        obj=toml_object, path=toml_property_path, value=value)


def set_cff_property_with_toml_property(cff_property_path: str, cff_object: CFFObject, toml_property_path: str, toml_object: TOMLObject) -> CFFObject:
    # uses pydash deep path strings to specify properties
    value = get_object_property(
        obj=toml_object, property_path=toml_property_path)
    if value is None:
        raise SetCFFPropertyException(
            f"Cannot set CFF property ({cff_property_path}) with TOML property ({toml_property_path}) because TOML property cannot be found.")
    return pydash.objects.set_(
        obj=cff_object, path=cff_property_path, value=value)


def set_toml_property(toml_object: TOMLObject, property_path: str, value: Any) -> TOMLObject:
    return set_object_property(
        obj=toml_object, property_path=property_path, value=value)


def set_cff_property(cff_object: CFFObject, property_path: str, value: Any) -> CFFObject:
    return set_object_property(
        obj=cff_object, property_path=property_path, value=value)


def set_object_property(obj: T, property_path: str, value: Any) -> T:
    return pydash.objects.set_(
        obj=obj, path=property_path, value=value)


def set_properties_for_cff_and_toml(value: Any,
                                    cff_property_path: str,
                                    toml_property_path: str,
                                    cff_file_path: str,
                                    toml_file_path: str) -> Tuple[CFFObject, TOMLObject]:

    cff_object: CFFObject = load_cff_object(
        cff_file_path=cff_file_path)

    cff_object = set_cff_property(
        cff_object=cff_object,
        property_path=cff_property_path,
        value=value)

    toml_object: TOMLObject = load_toml_object(
        toml_file_path=toml_file_path)

    toml_object = set_toml_property(
        toml_object=toml_object,
        property_path=toml_property_path,
        value=value
    )

    save_cff_object(cff_object=cff_object,
                    cff_file_path=cff_file_path)
    save_toml_object(toml_object=toml_object,
                     toml_file_path=toml_file_path)

    return cff_object, toml_object


def set_properties_for_citation_cff_and_pyproject_toml(value: Any,
                                                       citation_cff_property_path: str,
                                                       pyproject_toml_property_path: str,
                                                       citation_cff_file_path: str = DEFAULT_CITATION_CFF_FILE_PATH,
                                                       pyproject_toml_file_path: str = DEFAULT_PYPROJECT_TOML_FILE_PATH) -> Tuple[TOMLObject, CFFObject]:
    return set_properties_for_cff_and_toml(value=value,
                                           cff_property_path=citation_cff_property_path,
                                           toml_property_path=pyproject_toml_property_path,
                                           cff_file_path=citation_cff_file_path,
                                           toml_file_path=pyproject_toml_file_path)


def set_version_for_citation_cff_and_pyproject_toml(version: str,
                                                    citation_cff_file_path: str = DEFAULT_CITATION_CFF_FILE_PATH,
                                                    pyproject_toml_file_path: str = DEFAULT_PYPROJECT_TOML_FILE_PATH) -> Tuple[TOMLObject, CFFObject]:
    return set_properties_for_citation_cff_and_pyproject_toml(value=version,
                                                              citation_cff_property_path="version",
                                                              pyproject_toml_property_path="project.version",
                                                              citation_cff_file_path=citation_cff_file_path,
                                                              pyproject_toml_file_path=pyproject_toml_file_path)
