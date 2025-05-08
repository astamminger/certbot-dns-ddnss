# -*- coding: utf-8 -*-


"""
Utility script comparing the current GitHub-Tag (defined via the
GITHUB_REF evironment variable) to the version defined in the
package's setup.json file

Usage: python version.py $GITHUB_REF
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


def parse_tag_version_from_git(github_ref):
    """
    Parse current version from GitHub tag

    :params github_ref: the GITHUB_REF environment variable contents
        provided by github
    :type github_ref: str
    """
    pattern = r"(?<=^refs/tags/v)([\s\S]+$)"
    match = re.search(pattern, github_ref)
    if match is None:
        raise IOError("unable to parse version from GITHUB_REF")
    return version.parse(match.group(0))


if __name__ == "__main__":
    try:
        github_ref = sys.argv[1]
    except IndexError:
        raise IOError("missing $GITHUB_REF as command line argument")
    github_tag = parse_tag_version_from_git(github_ref)
    toml_version = parse_version_from_toml(pathlib.Path('.'))
    assert github_tag == toml_version, (
           f"version defined in pyproject.toml does not match with github "
           f"tag version ({toml_version} =/= {github_tag})")
