import http.client
import os
import re
import sys


def get_pypi_http_version(repo_name: str) -> str:
    """Returns actual version number from PyPi as a string
    """
    url = f"pypi.org"
    conn = http.client.HTTPSConnection(url)
    get_url = f"/project/{repo_name}/"
    conn.request("GET", get_url)
    resp = conn.getresponse()
    cont = resp.read().decode('utf-8')

    opening_tag = f'''class="package-header__name">'''
    closing_tag = "<"
    pattern = f"{opening_tag}(.*?){closing_tag}"

    tag_match = re.search(pattern, cont, re.DOTALL)
    if tag_match:
        return tag_match.group(1).split()[1]


def get_pypi_git_version(file_path: str) -> str:
    """Returns version number as a string from setup.py of PyPi package in repository
    """
    opening_tag = f'''version="'''
    closing_tag = '",'
    pattern = f"{opening_tag}(.*?){closing_tag}"
    with open(file_path, 'r') as f:
        s = f.read()
        tag_match = re.search(pattern, s, re.DOTALL)
        if tag_match:
            return tag_match.group(1)


def get__version(file_path: str) -> str:
    """Returns version number as a string from __version__.py in main arg directory
    """
    opening_tag = f'''__version__ = "'''
    closing_tag = '"'
    pattern = f"{opening_tag}(.*?){closing_tag}"
    with open(file_path, 'r') as f:
        s = f.read()
        tag_match = re.search(pattern, s, re.DOTALL)
        if tag_match:
            return tag_match.group(1)


def version_comparison(pypi_ver: str, git_ver: str) -> str:
    """Returns a string with comparison between pypi_ver(http) and git_version(setup.py)
    """
    pypi_is_RC = False
    git_is_RC = False
    if pypi_ver == git_ver:
        res = 'SAME'
    else:
        pypi_is_RC = '-RC' in pypi_ver
        git_is_RC = '-RC' in git_ver
        pypi_RC_ver = pypi_ver.split('-RC')[1] if pypi_is_RC else None
        git_RC_ver = git_ver.split('-RC')[1] if git_is_RC else None
        pypi_ver = pypi_ver.split('-RC')[0] if pypi_is_RC else pypi_ver
        git_ver = git_ver.split('-RC')[0] if git_is_RC else git_ver
        zipped_ver = zip(map(int, pypi_ver.split(".")), map(int, git_ver.split(".")))
        for ver_part in zipped_ver:
            if ver_part[0] > ver_part[1]:
                return 'PYPI'
            elif ver_part[0] < ver_part[1]:
                return 'REPO'
        if (pypi_is_RC and not pypi_RC_ver) or (git_is_RC and not git_RC_ver):
            res = 'A release candidate must have a RC version'
        elif pypi_RC_ver >= git_RC_ver:
            res = 'PYPI'
        elif pypi_RC_ver < git_RC_ver:
            res = 'REPO'
    return res


if __name__ == "__main__":
    """ Returns a string with comparison between pypi_ver(http) and git_version(setup.py)
        If passed argument is 'pyARG' checks if version in __version__.py and setup.py are the same
    """
    args = sys.argv
    repo = args[1]
    setup_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(args[0]))),
                              f".gitlab/deployment/pypi/{repo}/setup.py")
    version_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(args[0])))),
                                "arg/arg/__version__.py")
    actual_pypi_version = get_pypi_http_version(repo_name=repo)
    actual_git_version = get_pypi_git_version(file_path=setup_file)
    actual__version = get__version(file_path=version_file)
    comp = version_comparison(pypi_ver=actual_pypi_version, git_ver=actual_git_version)
    if actual_git_version != actual__version and repo == 'pyARG':
        print("__version__.py and setup.py needs to be the same!")
    else:
        print(comp)
