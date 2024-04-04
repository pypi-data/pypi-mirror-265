# cff2toml

A module to synchronize metadata between TOML and CFF files, including between pyproject.toml and CITATION.cff files.

[![PyPI - Version](https://img.shields.io/pypi/v/cff2toml.svg)](https://pypi.org/project/cff2toml)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cff2toml.svg)](https://pypi.org/project/cff2toml)

---

**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)
  - [Setting Metadata](#setting-metadata)
  - [Getting Metadata](#getting-metadata)
  - [Loading Metadata](#loading-metadata)
  - [Saving Metadata](#saving-metadata)
- [Limitations](#limitations)
- [Roadmap](#roadmap)
- [License](#license)

## Installation

```console
pip install cff2toml
```

## Usage

This library allows you to load, save, set, and get metadata from CFF and TOML files.

One common use case is to synchronize metadata between pyproject.toml and CITATION.cff files in a Python project.

In some of the examples below, you will see the idea of property paths. Property paths are a way to get and set nested data. In this library, property paths use the [deep path strings as defined by pydash](https://pydash.readthedocs.io/en/latest/deeppath.html).

### Setting Metadata

#### Set pyproject.toml with metadata from CITATION.cff

```python
from cff2toml import set_pyproject_toml_with_citation_cff

# set pyproject.toml with metadata
# from CITATION.cff
# where both files are located in the working directory
set_pyproject_toml_with_citation_cff()
```

```python
from cff2toml import set_pyproject_toml_with_citation_cff
import os

# set pyproject.toml with metadata
# from CITATION.cff where the files
# have custom file paths
pyproject_toml_file_path: str = os.path.join('somepath', 'pyproject.toml')
citation_cff_file_path: str = os.path.join('someotherpath', 'CITATION.cff')

set_pyproject_toml_with_citation_cff(pyproject_toml_file_path=pyproject_toml_file_path, citation_cff_file_path=citation_cff_file_path)
```

#### Set CITATION.cff with metadata from pyprojects.toml

```python
from cff2toml import set_citation_cff_with_pyproject_toml

# set CITATION.cff with metadata
# from pyprojects.cff
# where both files are located in the working directory
set_citation_cff_with_pyproject_toml()
```

```python
from cff2toml import set_citation_cff_with_pyproject_toml
import os

# set CITATION.cff with metadata
# from pyprojects.cff where the files
# have custom file paths
pyproject_toml_file_path: str = os.path.join('somepath', 'pyproject.toml')
citation_cff_file_path: str = os.path.join('someotherpath', 'CITATION.cff')

set_citation_cff_with_pyproject_toml(citation_cff_file_path=citation_cff_file_path, pyproject_toml_file_path=pyproject_toml_file_path)
```

#### Set pyproject.toml and CITATION.cff to have a specific version

```python
from cff2toml import set_version_for_citation_cff_and_pyproject_toml

# set CITATION.cff
# and pyproject.toml to have same version
# where both files are
# located in the working directory
set_version_for_citation_cff_and_pyproject_toml(version="2.0.0")
```

```python
from cff2toml import set_version_for_citation_cff_and_pyproject_toml
import os

# set CITATION.cff
# and pyproject.toml to have the same version
# where the files
# have custom file paths
citation_cff_file_path: str = os.path.join('someotherpath', 'CITATION.cff')
pyproject_toml_file_path: str = os.path.join('somepath', 'pyproject.toml')

set_version_for_citation_cff_and_pyproject_toml(version="2.0.0",  citation_cff_file_path=citation_cff_file_path, pyproject_toml_file_path=pyproject_toml_file_path)
```

#### Set a TOML file with metadata from a CFF file

```python
from cff2toml import set_toml_with_cff, CFFObject, TOMLObject, set_toml_property_with_cff_property
import os

toml_file_path: str = os.path.join('somepath', 'some_toml_file.toml')
cff_file_path: str = os.path.join('someotherpath', 'some_cff_file.cff')

def transform_toml_object(toml_object:TOMLObject, cff_object:CFFObject) -> TOMLObject:
    toml_object = set_toml_property_with_cff_property(toml_property_path='project.name', toml_object=toml_object, cff_property_path='title', cff_object=cff_object)
    return toml_object

toml_object: TOMLObject = set_toml_with_cff(toml_file_path=toml_file_path, cff_file_path=cff_file_path,  transform_toml_object_func=transform_toml_object)
```

#### Set a CFF file with metadata from a TOML file

```python
from cff2toml import set_cff_with_toml, CFFObject, TOMLObject, set_cff_property_with_toml_property
import os

cff_file_path: str = os.path.join('somepath', 'some_cff_file.cff')
toml_file_path: str = os.path.join('somepath', 'some_toml_file.toml')

def transform_cff_object(cff_object:CFFObject, toml_object:TOMLObject) -> CFFObject:
    cff_object = set_cff_property_with_toml_property(cff_property_path='title', cff_object=cff_object, toml_property_path='project.name', toml_object=toml_object)
    return cff_object

cff_object: CFFObject = set_cff_with_toml(cff_file_path=cff_file_path, toml_file_path=toml_file_path, transform_cff_object_func=cff_object_transformer)
```

### Getting Metadata

#### Get the version for pyprojects.toml file

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

#### Get the version for CITATION.cff file

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

### Loading Metadata

#### Load a TOML object from a TOML file

```python
from cff2toml import load_toml_object, TOMLObject
import os

toml_file_path: str = os.path.join('somepath', 'some_toml_file.toml')
toml_object: TOMLObject = load_toml_object(toml_file_path=toml_file_path)
print(toml_object)
```

#### Load a CFF object from a CFF file

```python
from cff2toml import load_cff_object, CFFObject
import os

cff_file_path: str = os.path.join('somepath', 'some_cff_file.cff')
cff_object: CFFObject = load_cff_object(cff_file_path=cff_file_path)
print(cff_object)
```

### Saving Metadata

#### Save a CFF object to a CFF file

```python
from cff2toml import load_cff_object, save_cff_object, CFFObject, set_cff_property
import os

cff_file_path: str = os.path.join('somepath', 'some_cff_file.cff')
cff_object: CFFObject = load_cff_object(cff_file_path)
print(cff_object)

cff_object = set_cff_property(cff_object=cff_boject, property_path='somekey.someotherkey', value='somevalue')

save_cff_object(cff_object=cff_object, cff_file_path=cff_file_path)
```

#### Save a TOML object to a TOML file

```python
from cff2toml import load_toml_object, save_toml_object, TOMLObject, set_toml_property
import os

toml_file_path: str = os.path.join('somepath', 'some_toml_file.toml')
toml_object: TOMLObject = load_toml_object(toml_file_path=toml_file_path)
print(toml_object)

toml_object = set_toml_property(toml_object=cff_boject, property_path='somekey.someotherkey', value='somevalue')

save_toml_object(toml_object=toml_object, toml_file_path=toml_file_path)

```

## Limitations

For set_pyproject_toml_with_citation_cff() and set_citation_cff_with_pyproject_toml(), the only metadata that is currently changed between CITATION.cff and pyproject.toml files is: CFF (title, version, abstract, license, repository-code) <-> TOML (project.name, project.version, project.description, project.license, project.urls.Source).

## Roadmap

1. Update author information for set_pyproject_toml_with_citation_cff() and set_citation_cff_with_pyproject_toml()
2. Add documentation for module methods
3. Create CLI

## License

`cff2toml` is distributed under the terms of the [Apache 2.0](https://spdx.org/licenses/Apache-2.0.html) license
