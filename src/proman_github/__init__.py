# copyright: (c) 2020 by Jesse Johnson.
# license: LGPL-3.0, see LICENSE.md for more details.
"""GitHub based package manager."""

import logging
import os
# import site
from typing import List, Optional
# from urllib.parse import urljoin

from github import Github
from proman_common.config import Config
from proman_common.filepaths import GlobalDirs
from proman_common.manifest import LockFile, SourceTreeFile, Manifest
# from proman_common.system import System

from .config import ProjectPaths
# from .distributions import LocalDistributionPath, UserDistributionPath
from .package_manager import PackageManager

# package metadata
__author__ = 'Jesse P. Johnson'
__title__ = 'proman-github'
__version__ = '0.1.1-dev2'
__license__ = 'LGPL-3.0'

logging.getLogger(__name__).addHandler(logging.NullHandler())


def get_package_manager(
    token: Optional[str] = os.getenv('GITHUB_TOKEN')
) -> PackageManager:
    """Get package manager instance."""
    # Load configuration files
    project_paths = ProjectPaths()
    specfile = None
    lockfile = None

    if os.path.exists(project_paths.pyproject_path):
        spec_cfg = Config(
            filepath=project_paths.pyproject_path, writable=True
        )
        specfile = SourceTreeFile(
            spec_cfg, basepath='.tool.proman.github'
        )

        if os.path.exists(project_paths.lock_path):
            lock_cfg = Config(filepath=project_paths.lock_path, writable=True)
            lockfile = LockFile(lock_cfg, basepath='.github')
        else:
            print('log no lockfile')
    else:
        print('log no source tree')

    manifest: Optional[Manifest] = None
    if specfile and lockfile:
        manifest = Manifest(
            specfile=specfile,
            lockfile=lockfile,
            dependency_class={
                'module': 'proman_github.dependency',
                'class': 'Dependency',
            }
        )

    # Setup package manager
    return PackageManager(
        github=Github(token),
        dirs=GlobalDirs(),
        manifest=manifest,
        force=False,
        update=False,
        options={}
    )


__all__: List[str] = ['get_package_manager']
