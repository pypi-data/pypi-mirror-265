from typing import Any, Callable, Dict, Tuple
import toml
import yaml

DEFAULT_PYPROJECT_TOML_FILENAME: str = 'pyproject.toml'
DEFAULT_CITATION_CFF_FILENAME: str = 'CITATION.cff'
DEFAULT_DIR: str = '.'

DEFAULT_PYPROJECT_TOML_FILE_PATH: str = DEFAULT_DIR + \
    DEFAULT_PYPROJECT_TOML_FILENAME
DEFAULT_CITATION_CFF_FILE_PATH: str = DEFAULT_DIR + DEFAULT_CITATION_CFF_FILENAME

TOMLObject = Dict[str, Any]
CFFObject = Any

TransformCFFObjectWithTOMLObjectFunction = Callable[[
    CFFObject, TOMLObject], CFFObject]
TransformTOMLObjectWithCFFObjectFunction = Callable[[
    TOMLObject, CFFObject], TOMLObject]


class LoadTOMLFileException(Exception):
    pass


class SaveTOMLFileException(Exception):
    pass


class LoadCFFFileException(Exception):
    pass


class SaveCFFFileException(Exception):
    pass


def load_toml_object(toml_file_path: str) -> TOMLObject:
    try:
        with open(toml_file_path, 'r') as toml_file:
            toml_object: TOMLObject = toml.load(toml_file)
    except:
        raise LoadTOMLFileException(
            f"Cannot load this TOML file: {toml_file_path}")
    return toml_object


def save_toml_object(toml_object: TOMLObject, toml_file_path: str) -> None:
    try:
        with open(toml_file_path, 'w') as toml_file:
            toml.dump(toml_object, toml_file)
    except:
        raise SaveTOMLFileException(
            f"Cannot save this TOML file: {toml_file_path}")


def load_cff_object(cff_file_path: str) -> CFFObject:
    try:
        with open(cff_file_path, 'r') as cff_file:
            cff_object: CFFObject = yaml.safe_load(cff_file)
    except:
        raise LoadCFFFileException(
            f"Cannot load this CFF file: {cff_file_path}")
    return cff_object


def save_cff_object(cff_object: CFFObject, cff_file_path: str) -> None:
    try:
        with open(cff_file_path, 'w') as cff_file:
            yaml.safe_dump(cff_object, cff_file)
    except:
        raise SaveCFFFileException(
            f"Cannot load this CFF file: {cff_file_path}")


def update_toml_with_cff(toml_file_path: str, cff_file_path: str, transform_toml_object_func: TransformTOMLObjectWithCFFObjectFunction) -> TOMLObject:

    toml_object: TOMLObject = load_toml_object(toml_file_path=toml_file_path)
    cff_object: CFFObject = load_cff_object(cff_file_path=cff_file_path)

    toml_object: TOMLObject = transform_toml_object_func(
        toml_object, cff_object)

    save_toml_object(toml_object=toml_object,
                     toml_file_path=toml_file_path)

    return toml_object


def update_cff_with_toml(cff_file_path: str, toml_file_path: str, transform_cff_object_func: TransformCFFObjectWithTOMLObjectFunction) -> CFFObject:

    toml_object: TOMLObject = load_toml_object(toml_file_path=toml_file_path)
    cff_object: CFFObject = load_cff_object(cff_file_path=cff_file_path)

    cff_object: CFFObject = transform_cff_object_func(cff_object, toml_object)

    save_cff_object(cff_object=cff_object,
                    cff_file_path=cff_file_path)

    return cff_object


def update_pyproject_toml_with_citation_cff(pyproject_toml_file_path=DEFAULT_PYPROJECT_TOML_FILE_PATH, citation_cff_file_path=DEFAULT_CITATION_CFF_FILE_PATH) -> TOMLObject:
    def transformer(pyproject_toml_object: TOMLObject, citation_cff_object: CFFObject) -> TOMLObject:
        pyproject_toml_object['project']['name'] = citation_cff_object['title']
        pyproject_toml_object['project']['version'] = citation_cff_object['version']
        pyproject_toml_object['project']['description'] = citation_cff_object['abstract']
        pyproject_toml_object['project']['license'] = citation_cff_object['license']
        pyproject_toml_object['project']['urls']['Source'] = citation_cff_object['repository-code']

        return pyproject_toml_object
    return update_toml_with_cff(toml_file_path=pyproject_toml_file_path, cff_file_path=citation_cff_file_path, transform_toml_object_func=transformer)


def update_citation_cff_with_pyproject_toml(citation_cff_file_path=DEFAULT_CITATION_CFF_FILE_PATH, pyproject_toml_file_path=DEFAULT_PYPROJECT_TOML_FILE_PATH) -> CFFObject:
    def transformer(citation_cff_object: CFFObject, pyproject_toml_object: TOMLObject) -> CFFObject:
        citation_cff_object['title'] = pyproject_toml_object['project']['name']
        citation_cff_object['version'] = pyproject_toml_object['project']['version']
        citation_cff_object['abstract'] = pyproject_toml_object['project']['description']
        citation_cff_object['license'] = pyproject_toml_object['project']['license']
        citation_cff_object['repository-code'] = pyproject_toml_object['project']['urls']['Source']

        return citation_cff_object
    return update_cff_with_toml(toml_file_path=pyproject_toml_file_path, cff_file_path=citation_cff_file_path, transform_cff_object_func=transformer)


def set_version_for_pyproject_toml_and_citation_cff(version: str, pyproject_toml_file_path: str, citation_cff_file_path: str) -> Tuple[TOMLObject, CFFObject]:
    pyproject_toml_object: TOMLObject = load_toml_object(
        toml_file_path=pyproject_toml_file_path)
    citation_cff_object: CFFObject = load_cff_object(
        cff_file_path=citation_cff_file_path)

    citation_cff_object['version'] = version
    pyproject_toml_object['project']['version'] = version

    save_cff_object(citation_cff_object, cff_file_path=citation_cff_file_path)
    save_toml_object(toml_object=pyproject_toml_object,
                     toml_file_path=pyproject_toml_file_path)

    return pyproject_toml_object, citation_cff_object


def get_version_for_pyproject_toml(pyproject_toml_file_path: str) -> str:
    pyproject_toml_object: TOMLObject = load_toml_object(
        toml_file_path=pyproject_toml_file_path)

    pyproject_toml_version: str = pyproject_toml_object['project']['version']

    return pyproject_toml_version


def get_version_for_citation_cff(citation_cff_file_path: str) -> str:

    citation_cff_object: CFFObject = load_cff_object(
        cff_file_path=citation_cff_file_path)

    citation_cff_version: str = citation_cff_object['version']

    return citation_cff_version
