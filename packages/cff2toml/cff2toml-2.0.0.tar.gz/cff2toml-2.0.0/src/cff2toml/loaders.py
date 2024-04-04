import toml
import yaml

from cff2toml.cff2toml import CFFObject, TOMLObject


class LoadTOMLFileException(Exception):
    pass


class LoadCFFFileException(Exception):
    pass


def load_toml_object(toml_file_path: str) -> TOMLObject:
    try:
        with open(toml_file_path, 'r') as toml_file:
            toml_object: TOMLObject = toml.load(toml_file)
    except:
        raise LoadTOMLFileException(
            f"Cannot load this TOML file: {toml_file_path}")
    return toml_object


def load_cff_object(cff_file_path: str) -> CFFObject:
    try:
        with open(cff_file_path, 'r') as cff_file:
            cff_object: CFFObject = yaml.safe_load(cff_file)
    except:
        raise LoadCFFFileException(
            f"Cannot load this CFF file: {cff_file_path}")
    return cff_object
