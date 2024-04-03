# cff2toml

A module to synchronize metadata between TOML and CFF files, including between pyproject.toml and CITATION.cff files.

[![PyPI - Version](https://img.shields.io/pypi/v/cff2toml.svg)](https://pypi.org/project/cff2toml)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cff2toml.svg)](https://pypi.org/project/cff2toml)

---

**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)
- [Limitations](#limitations)
- [Roadmap](#roadmap)
- [License](#license)

## Installation

```console
pip install cff2toml
```

## Usage

### Update pyproject.toml with metadata from CITATION.cff

```python
from cff2toml import update_pyproject_toml_with_citation_cff

# update pyproject.toml with metadata
# from CITATION.cff
# where both files are located in the working directory
update_pyproject_toml_with_citation_cff()
```

```python
from cff2toml import update_pyproject_toml_with_citation_cff
import os

# update pyproject.toml with metadata
# from CITATION.cff where the files
# have custom file paths
pyproject_toml_file_path: str = os.path.join('somepath', 'pyproject.toml')
citation_cff_file_path: str = os.path.join('someotherpath', 'CITATION.cff')

update_pyproject_toml_with_citation_cff(pyproject_toml_file_path=pyproject_toml_file_path, citation_cff_file_path=citation_cff_file_path)
```

### Update CITATION.cff with metadata from pyprojects.toml

```python
from cff2toml import update_citation_cff_with_pyproject_toml

# update CITATION.cff with metadata
# from pyprojects.cff
# where both files are located in the working directory
update_citation_cff_with_pyproject_toml()
```

```python
from cff2toml import update_citation_cff_with_pyproject_toml
import os

# update CITATION.cff with metadata
# from pyprojects.cff where the files
# have custom file paths
pyproject_toml_file_path: str = os.path.join('somepath', 'pyproject.toml')
citation_cff_file_path: str = os.path.join('someotherpath', 'CITATION.cff')

update_citation_cff_with_pyproject_toml(citation_cff_file_path=citation_cff_file_path, pyproject_toml_file_path=pyproject_toml_file_path)
```

### Get the version for pyprojects.toml file

```python
from cff2toml import get_version_for_pyproject_toml

# get the version for pyproject.toml
# where it is located in the working directory
pyprpject_toml_version: str = get_version_for_pyproject_toml()
```

```python
from cff2toml import get_version_for_pyproject_toml
import os

# get version for pyproject.toml
# where it has a custom file path
pyproject_toml_file_path: str = os.path.join('somepath', 'pyproject.toml')

pyproject_toml_version: str = get_version_for_pyproject_toml( pyproject_toml_file_path=pyproject_toml_file_path)
```

### Get the version for CITATION.cff file

```python
from cff2toml import get_version_for_citation_cff

# get the version for CITATION.cff
# where it is located in the working directory
citation_cff_version: str = get_version_for_citation_cff()
```

```python
from cff2toml import get_version_for_citation_cff
import os

# get version for CITATION.cff
# where it has a custom file path
citation_cff_file_path: str = os.path.join('somepath', 'CITATION.cff')

version: str = get_version_for_citation_cff(citation_cff_file_path=citation_cff_file_path)
```

### Set the same version for both pyprojects.toml file and CITATION.cff file

```python
from cff2toml import set_version_for_pyproject_toml_and_citation_cff

# set same version for pyproject.toml
# and CITATION.cff where both files are
# located in the working directory
set_version_for_pyproject_toml_and_citation_cff(version="2.0.0")
```

```python
from cff2toml import set_version_for_pyproject_toml_and_citation_cff
import os

# set same version for pyproject.toml
# and CITATION.cff where the files
# have custom file paths
pyproject_toml_file_path: str = os.path.join('somepath', 'pyproject.toml')
citation_cff_file_path: str = os.path.join('someotherpath', 'CITATION.cff')

set_version_for_pyproject_toml_with_citation_cff(version="2.0.0", pyproject_toml_file_path=pyproject_toml_file_path, citation_cff_file_path=citation_cff_file_path)
```

### Update a TOML file with metadata from a CFF file

```python
from cff2toml import update_toml_with_cff, CFFObject, TOMLObject
import os

toml_file_path: str = os.path.join('somepath', 'some_toml_file.toml')
cff_file_path: str = os.path.join('somepath', 'some_cff_file.cff')

def transformer(toml_object:TOMLObject, cff_object:CFFObject) -> TOMLObject:
    toml_object['somekey'] = cff_object['someotherkey']
    return toml_object

updated_toml_object: TOMLObject = update_toml_with_cff(toml_file_path=toml_file_path, cff_file_path=cff_file_path,  transform_toml_object_func=transformer)
```

### Update a CFF file with metadata from a TOML file

```python
from cff2toml import update_cff_with_toml, CFFObject, TOMLObject
import os

toml_file_path: str = os.path.join('somepath', 'some_toml_file.toml')
cff_file_path: str = os.path.join('somepath', 'some_cff_file.cff')

def transformer(cff_object:CFFObject, toml_object:TOMLObject) -> CFFObject:
    cff_object['somekey'] = toml_object['someotherkey']
    return cff_object

updated_cff_object: CFFObject = update_cff_with_toml(cff_file_path=cff_file_path, toml_file_path=toml_file_path, transform_cff_object_func=transformer)
```

### Load a TOML file object

```python
from cff2toml import load_toml_object, TOMLObject
import os

toml_file_path: str = os.path.join('somepath', 'some_toml_file.toml')
toml_object: TOMLObject = load_toml_object(toml_file_path=toml_file_path)
print(toml_object['somekey'])
```

### Save a TOML file object

```python
from cff2toml import load_toml_object, save_toml_object, TOMLObject
import os

toml_file_path: str = os.path.join('somepath', 'some_toml_file.toml')
toml_object: TOMLObject = load_toml_object(toml_file_path=toml_file_path)
print(toml_object['somekey'])

toml_object['somekey'] = 'somevalue'
save_toml_object(toml_object=toml_object, toml_file_path=toml_file_path)

```

### Load a CFF file object

```python
from cff2toml import load_cff_object, CFFObject
import os

cff_file_path: str = os.path.join('somepath', 'some_cff_file.cff')
cff_object: CFFObject = load_cff_object(cff_file_path=cff_file_path)
print(cff_object['somekey'])
```

### Save a CFF file object

```python
from cff2toml import load_cff_object, save_cff_object, CFFObject
import os

cff_file_path: str = os.path.join('somepath', 'some_cff_file.cff')
cff_object: CFFObject = load_cff_object(cff_file_path)
print(cff_object['somekey'])

cff_object['somekey'] = 'somevalue'
save_cff_object(cff_object=cff_object, cff_file_path=cff_file_path)
```

## Limitations

For update_pyproject_toml_with_citation_cff() and update_citation_cff_with_pyproject_toml(), the only metadata that is currently updated between CITATION.cff and pyproject.toml files is: CFF (title, version, abstract, license, repository-code) <-> TOML (project.name, project.version, project.description, project.license, project.urls.Source).

## Roadmap

1. Update author information for update_pyproject_toml_with_citation_cff() and update_citation_cff_with_pyproject_toml()
2. Create CLI

## License

`cff2toml` is distributed under the terms of the [Apache 2.0](https://spdx.org/licenses/Apache-2.0.html) license
