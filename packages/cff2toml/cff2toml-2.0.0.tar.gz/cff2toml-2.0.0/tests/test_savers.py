from cff2toml.cff2toml import CFFObject, TOMLObject
from cff2toml.loaders import load_cff_object, load_toml_object
from cff2toml.savers import save_cff_object, save_toml_object
from tests.temp_copied_file import TempCopiedFile
from tests.common_fixtures import dummy_citation_cff_file_path, dummy_directory_file_path, dummy_pyproject_toml_file_path


def test_save_cff_object(dummy_citation_cff_file_path):
    with TempCopiedFile(source_file_path=dummy_citation_cff_file_path) as tmp_dummy_citation_cff_file:
        before_cff_object: CFFObject = {
            'version': '5.6',
            'title': 'sometitle'
        }

        save_cff_object(cff_object=before_cff_object,
                        cff_file_path=tmp_dummy_citation_cff_file.file_path)

        after_cff_object: CFFObject = load_cff_object(
            cff_file_path=tmp_dummy_citation_cff_file.file_path)

        assert after_cff_object['version'] == '5.6'
        assert after_cff_object['title'] == 'sometitle'


def test_save_toml_object(dummy_pyproject_toml_file_path):
    with TempCopiedFile(source_file_path=dummy_pyproject_toml_file_path) as tmp_dummy_pyproject_toml_file:

        before_toml_object: TOMLObject = {
            'project': {
                'version': '9.6',
                'name': 'someothertitle'
            }
        }

        save_toml_object(toml_object=before_toml_object,
                         toml_file_path=tmp_dummy_pyproject_toml_file.file_path)

        after_toml_object: CFFObject = load_toml_object(
            toml_file_path=tmp_dummy_pyproject_toml_file.file_path)

        assert after_toml_object['project']['version'] == '9.6'
        assert after_toml_object['project']['name'] == 'someothertitle'
