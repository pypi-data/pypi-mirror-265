
from cff2toml.cff2toml import CFFObject, TOMLObject
from cff2toml.loaders import load_cff_object, load_toml_object
from cff2toml.setters import set_cff_with_toml, set_citation_cff_with_pyproject_toml, set_pyproject_toml_with_citation_cff, set_toml_with_cff, set_version_for_citation_cff_and_pyproject_toml

from tests.temp_copied_file import TempCopiedFile
from tests.common_fixtures import dummy_citation_cff_file_path, dummy_directory_file_path, dummy_pyproject_toml_file_path


def test_set_toml_with_cff(dummy_citation_cff_file_path, dummy_pyproject_toml_file_path):
    with TempCopiedFile(source_file_path=dummy_citation_cff_file_path) as tmp_dummy_citation_cff_file:
        with TempCopiedFile(source_file_path=dummy_pyproject_toml_file_path) as tmp_dummy_pyproject_toml_file:

            toml_object: TOMLObject = load_toml_object(
                toml_file_path=tmp_dummy_pyproject_toml_file.file_path)
            assert toml_object['project']['version'] == '0.0.1'
            assert toml_object['project']['name'] == 'someuncooltool'
            assert toml_object['project']['description'] == 'A module that does something uncool.'
            assert toml_object['project']['license'] == 'Apache-1.0'
            assert toml_object['project']['urls']['Source'] == 'https://github.com/willnilly/somewhereuncool'

            def transformer(toml_object: TOMLObject, cff_object: CFFObject) -> TOMLObject:
                toml_object['project']['version'] = '5.0.1'
                toml_object['project']['name'] = 'cows'
                toml_object['project']['description'] = 'A module that does something else.'
                toml_object['project']['license'] = 'MIT'
                toml_object['project']['urls']['Source'] = 'https://github.com/willynilly/somewhereelse'
                return toml_object

            toml_object = set_toml_with_cff(
                toml_file_path=tmp_dummy_pyproject_toml_file.file_path,
                cff_file_path=tmp_dummy_citation_cff_file.file_path,
                transform_toml_object_func=transformer)

            assert toml_object['project']['version'] == '5.0.1'
            assert toml_object['project']['name'] == 'cows'
            assert toml_object['project']['description'] == 'A module that does something else.'
            assert toml_object['project']['license'] == 'MIT'
            assert toml_object['project']['urls']['Source'] == 'https://github.com/willynilly/somewhereelse'

            toml_object = load_toml_object(
                toml_file_path=tmp_dummy_pyproject_toml_file.file_path)
            assert toml_object['project']['version'] == '5.0.1'
            assert toml_object['project']['name'] == 'cows'
            assert toml_object['project']['description'] == 'A module that does something else.'
            assert toml_object['project']['license'] == 'MIT'
            assert toml_object['project']['urls']['Source'] == 'https://github.com/willynilly/somewhereelse'


def test_set_cff_with_toml(dummy_citation_cff_file_path, dummy_pyproject_toml_file_path):
    with TempCopiedFile(source_file_path=dummy_citation_cff_file_path) as tmp_dummy_citation_cff_file:
        with TempCopiedFile(source_file_path=dummy_pyproject_toml_file_path) as tmp_dummy_pyproject_toml_file:

            cff_object: CFFObject = load_cff_object(
                cff_file_path=tmp_dummy_citation_cff_file.file_path)
            assert cff_object['version'] == '0.0.2'
            assert cff_object['title'] == 'somecooltool'
            assert cff_object['license'] == 'Apache-2.0'
            assert cff_object['abstract'] == 'A module that does something cool.'
            assert cff_object['repository-code'] == 'https://github.com/willynilly/somewherecool'

            def transformer(cff_object: CFFObject, toml_object: TOMLObject) -> CFFObject:
                cff_object['version'] = '4.0.0'
                cff_object['title'] = 'sheep'
                cff_object['license'] = 'MIT'
                cff_object['abstract'] = 'A module that does something else.'
                cff_object['repository-code'] = 'https://github.com/willynilly/somewhereelse'

                return cff_object

            cff_object = set_cff_with_toml(
                cff_file_path=tmp_dummy_citation_cff_file.file_path,
                toml_file_path=tmp_dummy_pyproject_toml_file.file_path,
                transform_cff_object_func=transformer)

            assert cff_object['version'] == '4.0.0'
            assert cff_object['title'] == 'sheep'
            assert cff_object['license'] == 'MIT'
            assert cff_object['abstract'] == 'A module that does something else.'
            assert cff_object['repository-code'] == 'https://github.com/willynilly/somewhereelse'

            cff_object = load_cff_object(
                cff_file_path=tmp_dummy_citation_cff_file.file_path)
            assert cff_object['version'] == '4.0.0'
            assert cff_object['title'] == 'sheep'
            assert cff_object['license'] == 'MIT'
            assert cff_object['abstract'] == 'A module that does something else.'
            assert cff_object['repository-code'] == 'https://github.com/willynilly/somewhereelse'


def test_set_pyproject_toml_with_citation_cff(dummy_citation_cff_file_path, dummy_pyproject_toml_file_path):
    with TempCopiedFile(source_file_path=dummy_citation_cff_file_path) as tmp_dummy_citation_cff_file:
        with TempCopiedFile(source_file_path=dummy_pyproject_toml_file_path) as tmp_dummy_pyproject_toml_file:

            toml_object: TOMLObject = load_toml_object(
                toml_file_path=tmp_dummy_pyproject_toml_file.file_path)
            assert toml_object['project']['version'] == '0.0.1'
            assert toml_object['project']['name'] == 'someuncooltool'
            assert toml_object['project']['description'] == 'A module that does something uncool.'
            assert toml_object['project']['license'] == 'Apache-1.0'
            assert toml_object['project']['urls']['Source'] == 'https://github.com/willnilly/somewhereuncool'

            toml_object = set_pyproject_toml_with_citation_cff(
                pyproject_toml_file_path=tmp_dummy_pyproject_toml_file.file_path,
                citation_cff_file_path=tmp_dummy_citation_cff_file.file_path)

            assert toml_object['project']['version'] == '0.0.2'
            assert toml_object['project']['name'] == 'somecooltool'
            assert toml_object['project']['description'] == 'A module that does something cool.'
            assert toml_object['project']['license'] == 'Apache-2.0'
            assert toml_object['project']['urls']['Source'] == 'https://github.com/willynilly/somewherecool'

            toml_object = load_toml_object(
                toml_file_path=tmp_dummy_pyproject_toml_file.file_path)
            assert toml_object['project']['version'] == '0.0.2'
            assert toml_object['project']['name'] == 'somecooltool'
            assert toml_object['project']['description'] == 'A module that does something cool.'
            assert toml_object['project']['license'] == 'Apache-2.0'
            assert toml_object['project']['urls']['Source'] == 'https://github.com/willynilly/somewherecool'


def test_set_citation_cff_with_pyproject_toml(dummy_citation_cff_file_path, dummy_pyproject_toml_file_path):
    with TempCopiedFile(source_file_path=dummy_citation_cff_file_path) as tmp_dummy_citation_cff_file:
        with TempCopiedFile(source_file_path=dummy_pyproject_toml_file_path) as tmp_dummy_pyproject_toml_file:

            cff_object: CFFObject = load_cff_object(
                cff_file_path=tmp_dummy_citation_cff_file.file_path)
            assert cff_object['version'] == '0.0.2'
            assert cff_object['title'] == 'somecooltool'
            assert cff_object['license'] == 'Apache-2.0'
            assert cff_object['abstract'] == 'A module that does something cool.'
            assert cff_object['repository-code'] == 'https://github.com/willynilly/somewherecool'

            cff_object = set_citation_cff_with_pyproject_toml(
                citation_cff_file_path=tmp_dummy_citation_cff_file.file_path,
                pyproject_toml_file_path=tmp_dummy_pyproject_toml_file.file_path)

            assert cff_object['version'] == '0.0.1'
            assert cff_object['title'] == 'someuncooltool'
            assert cff_object['license'] == 'Apache-1.0'
            assert cff_object['abstract'] == 'A module that does something uncool.'
            assert cff_object['repository-code'] == 'https://github.com/willnilly/somewhereuncool'

            cff_object = load_cff_object(
                cff_file_path=tmp_dummy_citation_cff_file.file_path)
            assert cff_object['version'] == '0.0.1'
            assert cff_object['title'] == 'someuncooltool'
            assert cff_object['license'] == 'Apache-1.0'
            assert cff_object['abstract'] == 'A module that does something uncool.'
            assert cff_object['repository-code'] == 'https://github.com/willnilly/somewhereuncool'


def test_set_version_for_citation_cff_and_pyproject_toml(dummy_citation_cff_file_path, dummy_pyproject_toml_file_path):
    expected_version: str = '10.1.1'
    with TempCopiedFile(source_file_path=dummy_citation_cff_file_path) as tmp_dummy_citation_cff_file:
        with TempCopiedFile(source_file_path=dummy_pyproject_toml_file_path) as tmp_dummy_pyproject_toml_file:

            toml_object: TOMLObject = load_toml_object(
                toml_file_path=tmp_dummy_pyproject_toml_file.file_path)
            assert toml_object['project']['version'] == '0.0.1'
            assert toml_object['project']['name'] == 'someuncooltool'
            assert toml_object['project']['description'] == 'A module that does something uncool.'
            assert toml_object['project']['license'] == 'Apache-1.0'
            assert toml_object['project']['urls']['Source'] == 'https://github.com/willnilly/somewhereuncool'

            cff_object: CFFObject = load_cff_object(
                cff_file_path=tmp_dummy_citation_cff_file.file_path)
            assert cff_object['version'] == '0.0.2'
            assert cff_object['title'] == 'somecooltool'
            assert cff_object['license'] == 'Apache-2.0'
            assert cff_object['abstract'] == 'A module that does something cool.'
            assert cff_object['repository-code'] == 'https://github.com/willynilly/somewherecool'

            cff_object, toml_object = set_version_for_citation_cff_and_pyproject_toml(
                version=expected_version,
                citation_cff_file_path=tmp_dummy_citation_cff_file.file_path,
                pyproject_toml_file_path=tmp_dummy_pyproject_toml_file.file_path)

            assert toml_object['project']['version'] == expected_version
            assert toml_object['project']['name'] == 'someuncooltool'
            assert toml_object['project']['description'] == 'A module that does something uncool.'
            assert toml_object['project']['license'] == 'Apache-1.0'
            assert toml_object['project']['urls']['Source'] == 'https://github.com/willnilly/somewhereuncool'

            assert cff_object['version'] == expected_version
            assert cff_object['title'] == 'somecooltool'
            assert cff_object['license'] == 'Apache-2.0'
            assert cff_object['abstract'] == 'A module that does something cool.'
            assert cff_object['repository-code'] == 'https://github.com/willynilly/somewherecool'

            toml_object = load_toml_object(
                toml_file_path=tmp_dummy_pyproject_toml_file.file_path)
            assert toml_object['project']['version'] == expected_version
            assert toml_object['project']['name'] == 'someuncooltool'
            assert toml_object['project']['description'] == 'A module that does something uncool.'
            assert toml_object['project']['license'] == 'Apache-1.0'
            assert toml_object['project']['urls']['Source'] == 'https://github.com/willnilly/somewhereuncool'

            cff_object = load_cff_object(
                cff_file_path=tmp_dummy_citation_cff_file.file_path)
            assert cff_object['version'] == expected_version
            assert cff_object['title'] == 'somecooltool'
            assert cff_object['license'] == 'Apache-2.0'
            assert cff_object['abstract'] == 'A module that does something cool.'
            assert cff_object['repository-code'] == 'https://github.com/willynilly/somewherecool'
