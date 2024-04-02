"""
Simple wrapper about the GitPython library to interact with a git repository.
"""

import subprocess
from git import Repo


def assert_in_git_repo():
    """
    Ensure we are in a git repository.
    """
    try:
        get_repo()
    except Exception as e:
        raise ValueError("You're not in a git repository.") from e


def get_repo_dir() -> str:
    """
    Get the root directory of the git repository.
    """
    return subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        text=True,
        stdout=subprocess.PIPE,
        check=True,
    ).stdout.strip()


def get_repo() -> Repo:
    """
    Get the GitPython Repo object for the current repository.
    @link [GitPython Quick Start Tutorial](https://gitpython.readthedocs.io/en/stable/quickstart.html)
    """
    return Repo.init(get_repo_dir())
