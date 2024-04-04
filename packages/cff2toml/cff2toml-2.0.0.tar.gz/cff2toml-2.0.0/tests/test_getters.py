from unittest.mock import patch

from cff2toml.getters import get_version_for_citation_cff, get_version_for_pyproject_toml
from cff2toml.getters import get_title_for_citation_cff, get_name_for_pyproject_toml
from tests.temp_copied_file import TempCopiedFile
from tests.common_fixtures import dummy_citation_cff_file_path, dummy_directory_file_path, dummy_pyproject_toml_file_path


def test_get_version_for_citation_cff(dummy_citation_cff_file_path):
    with TempCopiedFile(source_file_path=dummy_citation_cff_file_path) as tmp_dummy_citation_cff_file:
        version: str = get_version_for_citation_cff(
            citation_cff_file_path=tmp_dummy_citation_cff_file.file_path)
        assert version == '0.0.2'


def test_get_version_for_pyproject_toml(dummy_pyproject_toml_file_path):
    with TempCopiedFile(source_file_path=dummy_pyproject_toml_file_path) as tmp_dummy_pyproject_toml_file:
        version: str = get_version_for_pyproject_toml(
            pyproject_toml_file_path=tmp_dummy_pyproject_toml_file.file_path)
        assert version == '0.0.1'


def test_get_version_for_citation_cff_with_default_file_path(dummy_citation_cff_file_path):
    with TempCopiedFile(source_file_path=dummy_citation_cff_file_path) as tmp_dummy_citation_cff_file:
        # patch the default parameters in the partial object
        # the func object is original function that is partialed
        # the __defaults__ variable contains
        # the tuple of paramter defaults that can be mocked
        with patch('cff2toml.getters.get_version_for_citation_cff.func.__defaults__', (tmp_dummy_citation_cff_file.file_path,)):
            version: str = get_version_for_citation_cff()
            assert version == '0.0.2'


def test_get_title_for_citation_cff_with_default_file_path(dummy_citation_cff_file_path):
    with TempCopiedFile(source_file_path=dummy_citation_cff_file_path) as tmp_dummy_citation_cff_file:
        # patch the default parameters in the partial object
        # the func object is original function that is partialed
        # the __defaults__ variable contains
        # the tuple of paramter defaults that can be mocked
        with patch('cff2toml.getters.get_title_for_citation_cff.func.__defaults__', (tmp_dummy_citation_cff_file.file_path,)):
            title: str = get_title_for_citation_cff()
            assert title == 'somecooltool'


def test_get_version_for_pyproject_toml_with_default_file_path(dummy_pyproject_toml_file_path):
    with TempCopiedFile(source_file_path=dummy_pyproject_toml_file_path) as tmp_dummy_pyproject_toml_file:
        # patch the default parameters in the partial object
        # the func object is original function that is partialed
        # the __defaults__ variable contains
        # the tuple of paramter defaults that can be mocked
        with patch('cff2toml.getters.get_version_for_pyproject_toml.func.__defaults__', (tmp_dummy_pyproject_toml_file.file_path,)):
            version: str = get_version_for_pyproject_toml()
            assert version == '0.0.1'


def test_get_name_for_pyproject_toml_with_default_file_path(dummy_pyproject_toml_file_path):
    with TempCopiedFile(source_file_path=dummy_pyproject_toml_file_path) as tmp_dummy_pyproject_toml_file:
        # patch the default parameters in the partial object
        # the func object is original function that is partialed
        # the __defaults__ variable contains
        # the tuple of paramter defaults that can be mocked
        with patch('cff2toml.getters.get_name_for_pyproject_toml.func.__defaults__', (tmp_dummy_pyproject_toml_file.file_path,)):
            name: str = get_name_for_pyproject_toml()
            assert name == 'someuncooltool'
