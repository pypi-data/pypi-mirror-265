# cff2toml

A module to synchronize metadata between TOML and CFF files, including between pyproject.toml and CITATION.cff files.

[![PyPI - Version](https://img.shields.io/pypi/v/cff2toml.svg)](https://pypi.org/project/cff2toml)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cff2toml.svg)](https://pypi.org/project/cff2toml)

---

**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation

```console
pip install cff2toml
```

## Usage

### Updating pyproject.toml with metadata from CITATION.cff

```python
from cff2toml import update_pyproject_toml_with_citation_cff

# update the pyproject.toml file with metadata
# from CITATION.cff file
# where both files are located in the working directory
update_pyproject_toml_with_citation_cff()
```

```python
from cff2toml import update_pyproject_toml_with_citation_cff

# update the pyproject.toml file with metadata
# from CITATION.cff file
# where both files are located in the working directory
pyproject_toml_file_path: str = os.path.join('somepath', 'pyproject.toml')
citation_cff_file_path: str = os.path.join('somepath', 'CITATION.cff')

update_pyproject_toml_with_citation_cff(pyproject_toml_file_path=pyproject_toml_file_path, citation_cff_file_path=citation_cff_file_path)
```

### Updating CITATION.toml with metadata from pyprojects.toml

```python
from cff2toml import update_citation_cff_with_pyproject_toml

# update the CITATION.cff file with metadata
# from pyprojects.cff file
# where both files are located in the working directory
update_citation_cff_with_pyproject_toml()
```

```python
from cff2toml import update_pyproject_toml_with_citation_cff

# update the CITATION.cff file with metadata
# from pyprojects.cff file
# from specific locations
pyproject_toml_file_path: str = os.path.join('somepath', 'pyproject.toml')
citation_cff_file_path: str = os.path.join('somepath', 'CITATION.cff')

update_citation_cff_with_pyproject_toml(citation_cff_file_path=citation_cff_file_path, pyproject_toml_file_path=pyproject_toml_file_path)
```

### Updating TOML file with metadata from CFF file

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

### Updating CFF file with metadata from TOML file

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

### Load TOML file object

```python
from cff2toml import load_toml_object, TOMLObject
import os

toml_file_path: str = os.path.join('somepath', 'some_toml_file.toml')
toml_object: TOMLObject = load_toml_object(toml_file_path=toml_file_path)
print(toml_object['somekey'])
```

### Save TOML file object

```python
from cff2toml import load_toml_object, TOMLObject
import os

toml_file_path: str = os.path.join('somepath', 'some_toml_file.toml')
toml_object: TOMLObject = load_toml_object(toml_file_path=toml_file_path)
print(toml_object['somekey'])

toml_object['somekey'] = 'somevalue'
save_toml_object(toml_object=toml_object, toml_file_path=toml_file_path)

```

### Load CFF file object

```python
from cff2toml import load_cff_object, CFFObject
import os

cff_file_path: str = os.path.join('somepath', 'some_cff_file.cff')
cff_object: CFFObject = load_cff_object(cff_file_path=cff_file_path)
print(cff_object['somekey'])
```

### Save CFF file object

```python
from cff2toml import load_cff_object, CFFObject
import os

cff_file_path: str = os.path.join('somepath', 'some_cff_file.cff')
cff_object: CFFObject = load_cff_object(cff_file_path)
print(cff_object['somekey'])

cff_object['somekey'] = 'somevalue'
save_cff_object(cff_object=cff_object, cff_file_path=cff_file_path)
```

## License

`cff2toml` is distributed under the terms of the [Apache 2.0](https://spdx.org/licenses/Apache-2.0.html) license
