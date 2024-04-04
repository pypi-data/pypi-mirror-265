from cff2toml.cff2toml import CFFObject, TOMLObject
from cff2toml.loaders import load_cff_object, load_toml_object
from tests.temp_copied_file import TempCopiedFile
from tests.common_fixtures import dummy_citation_cff_file_path, dummy_directory_file_path, dummy_pyproject_toml_file_path


def test_load_cff_object(dummy_citation_cff_file_path):
    with TempCopiedFile(source_file_path=dummy_citation_cff_file_path) as tmp_dummy_citation_cff_file:
        cff_object: CFFObject = load_cff_object(
            cff_file_path=tmp_dummy_citation_cff_file.file_path)
        assert cff_object['version'] == '0.0.2'
        assert cff_object['title'] == 'somecooltool'
        assert cff_object['license'] == 'Apache-2.0'
        assert cff_object['abstract'] == 'A module that does something cool.'
        assert cff_object['repository-code'] == 'https://github.com/willynilly/somewherecool'


def test_load_toml_object(dummy_pyproject_toml_file_path):
    with TempCopiedFile(source_file_path=dummy_pyproject_toml_file_path) as tmp_dummy_pyproject_toml_file:
        toml_object: TOMLObject = load_toml_object(
            toml_file_path=tmp_dummy_pyproject_toml_file.file_path)
        assert toml_object['project']['version'] == '0.0.1'
        assert toml_object['project']['name'] == 'someuncooltool'
        assert toml_object['project']['description'] == 'A module that does something uncool.'
        assert toml_object['project']['license'] == 'Apache-1.0'
        assert toml_object['project']['urls']['Source'] == 'https://github.com/willnilly/somewhereuncool'
