# A Packaged React App

A simple demo client for demonsrating build & package into a Python package.

## Getting Started

### Installation

```shell
npm install
npm run build
```

### Packaging

```shell
touch setup.py
```

with the following content:

```python
from setuptools import setup
from pathlib import Path


cwd = Path(__file__).parent
long_description = (cwd / "README.md").read_text()

setup(
    name="react-app",
    version="0.0.1",
    package_dir={"react_app": "build"},
    package_data={"react_app": ["**/*.*"]},
    long_description=long_description,
    long_description_content_type="text/markdown",
)

```
