'''GitHub based package manager.'''
# -*- coding: utf-8 -*-

import logging

from invoke import Program

from .package_manager import tasks as pkgmgr_tasks

logging.getLogger(__name__).addHandler(logging.NullHandler())

# package metadata
__author__ = 'Jesse P. Johnson'
__title__ = 'proman_github'
__version__ = '0.1.0'
__license__ = 'MPL-2.0'
__all__ = []

# workflow CLI endpoint callable by "program.run(['example', 'command'])"
program = Program(
    version=__version__,
    namespace=pkgmgr_tasks,
)
