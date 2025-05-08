# -*- coding: utf-8 -*-


"""
Utility script which reads and comparing all version tags defined
throughout the package source, i.e. read versions from

* aiida_cusp/__init__.py
* setup.json
* docs/source/conf.py

"""


import re
import sys
import tomllib
import pathlib

from packaging import version


def parse_version_from_toml(path_to_repo_root):
    """
    Parse version from pyproject.toml file

    :param path_to_repo_root: path to the repository root folder
    :type path_to_repo_root: pathlib.Path
    """
    path_to_toml = pathlib.Path(path_to_repo_root) / "pyproject.toml"
    with open(path_to_toml, 'rb') as toml_file:
        pyproject_args = tomllib.load(toml_file)
    try:
        pkg_version = pyproject_args.get('project').get('version')
        return version.parse(pkg_version)
    except KeyError:
        raise IOError("unable to parse version string from setup.json")


def parse_version_from_init(path_to_source_root):
    """
    Parse version from project's __init__.py file

    :param path_to_source_root: path to the source root folder of the
        package, i.e. `aiida_cusp` located in the repository root folder
    :type path_to_source_root: pathlib.Path
    """
    path_to_init = pathlib.Path(path_to_source_root) / "__init__.py"
    with open(path_to_init, 'r') as init_file:
        content = init_file.read()
    pattern = r"(?<=__version__\s=\s[\'\"])[\s\S]+?(?=[\"\']\n)"
    match = re.search(pattern, content)
    if match is None:
        raise IOError("unable to parse version string from __init__.py")
    return version.parse(match.group(0))


if __name__ == "__main__":
    toml_version = parse_version_from_toml(pathlib.Path('.'))
    init_version = parse_version_from_init(pathlib.Path('./certbot_dns_ddnss'))
    # now check if the parsed versions do match
    assert toml_version == init_version, (
           f"version defined in pyproject.toml does not match with version "
           f"defined in __init__.py ({toml_version} =/= {init_version})")
