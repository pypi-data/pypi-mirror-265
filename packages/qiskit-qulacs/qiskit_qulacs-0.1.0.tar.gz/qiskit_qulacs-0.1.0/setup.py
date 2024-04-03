# See pyproject.toml for project configuration.
# This file exists for compatibility with legacy tools:
# https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html

import os
from typing import Any, Dict, Optional

from setuptools import setup

version_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "qiskit_qulacs", "version.py")
)

version_dict: Optional[Dict[str, Any]] = {}
with open(version_path) as fp:
    exec(fp.read(), version_dict)
version = version_dict["__version__"]

setup(version=version)
