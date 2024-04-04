
import toml
import yaml

from cff2toml.cff2toml import CFFObject, TOMLObject


class SaveTOMLFileException(Exception):
    pass


class SaveCFFFileException(Exception):
    pass


def save_toml_object(toml_object: TOMLObject, toml_file_path: str) -> None:
    try:
        with open(toml_file_path, 'w') as toml_file:
            toml.dump(toml_object, toml_file)
    except:
        raise SaveTOMLFileException(
            f"Cannot save this TOML file: {toml_file_path}")


def save_cff_object(cff_object: CFFObject, cff_file_path: str) -> None:
    try:
        with open(cff_file_path, 'w') as cff_file:
            yaml.safe_dump(cff_object, cff_file)
    except:
        raise SaveCFFFileException(
            f"Cannot load this CFF file: {cff_file_path}")
