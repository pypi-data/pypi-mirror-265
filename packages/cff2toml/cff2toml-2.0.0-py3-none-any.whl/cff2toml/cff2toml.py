from typing import Any, Dict, TypeVar
import os

DEFAULT_PYPROJECT_TOML_FILENAME: str = 'pyproject.toml'
DEFAULT_CITATION_CFF_FILENAME: str = 'CITATION.cff'
DEFAULT_DIR: str = '.'

DEFAULT_PYPROJECT_TOML_FILE_PATH: str = os.path.join(
    DEFAULT_DIR, DEFAULT_PYPROJECT_TOML_FILENAME)
DEFAULT_CITATION_CFF_FILE_PATH: str = os.path.join(
    DEFAULT_DIR, DEFAULT_CITATION_CFF_FILENAME)

TOMLObject = Dict[str, Any]
CFFObject = Any
T = TypeVar('T')  # a generic type
