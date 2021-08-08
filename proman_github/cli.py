# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: MPL-2.0, see LICENSE for more details.
'''Arguments for inspection based CLI parser.'''

# import atexit
import json
import logging
import sys
from typing import Optional

from . import get_package_manager

logger = logging.getLogger(__name__)

package_manager = get_package_manager()


def config() -> None:
    '''Manage distributions and global configuration.'''
    pass


def info(name: str, output: str = 'plain') -> None:
    '''Get package info.'''
    info = package_manager.info(name, output)
    print(json.dumps(info, indent=2))


def download(name: str, dest: str = '.') -> None:
    '''Download packages.'''
    package_manager.download(name, dest)


def install(
    name: Optional[str],
    dev: bool = False,
    platform: Optional[str] = None,
    optional: bool = False,
    prerelease: bool = False,
) -> None:
    '''Install package and dependencies.

    Parameters
    ----------
    name: str
        name of package to be installed
    dev: bool
        add package as a development dependency
    prerelease: bool
        allow prerelease version of package
    optional: bool
        optional package that is not required
    platform: str
        restrict package to specific platform

    '''
    if name and name.startswith('-'):
        print('error: not a valid install argument', file=sys.stderr)
    else:
        package_manager.install(
            name,
            dev,
            platform=platform,
            optional=optional,
            prerelease=prerelease
        )


def uninstall(name: Optional[str]) -> None:
    '''Uninstall packages.'''
    if name and name.startswith('-'):
        print('error: not a valid install argument', file=sys.stderr)
    else:
        package_manager.uninstall(name)


def update(
    name: Optional[str],
    force: bool = False,
) -> None:
    '''Install package and dependencies.

    Parameters
    ----------
    name: str
        name of package to be installed
    force: bool
        force changes

    '''
    if name and name.startswith('-'):
        print('error: not a valid install argument', file=sys.stderr)
    else:
        package_manager.update(name, force)


# def list(versions: bool = True) -> None:
#     '''List installed packages.'''
#     if versions:
#         for k in local_package.packages:
#             print(k.name.ljust(25), k.version.ljust(15), file=sys.stdout)
#     else:
#         print('\n'.join(local_package.package_names), file=sys.stdout)


def search(
    query: str,
    sort: str = 'stars',
    order: str = 'desc',
) -> None:
    '''Search PyPI for packages.'''
    packages = package_manager.search(
        query=query,
        sort=sort,
        order=order,
    )
    for package in packages:
        print(
            package,
            file=sys.stdout
        )
