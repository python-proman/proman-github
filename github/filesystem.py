# -*- coding: utf-8 -*-
# type: ignore
# copyright: (c) 2020 by Jesse Johnson.
# license: MPL 2.0, see LICENSE for more details.
'''Filesystem Task-Runner.'''

import os
import shutil

from invoke import task


@task
def mkdir(ctx, path):
    '''Make directory path.'''
    try:
        os.makedirs(path, exist_ok=True)
    except OSError as err:
        print(f"unable to download github release due to: {err}")


@task
def rmdir(ctx, path):
    '''Remove directory path.'''
    try:
        shutil.rmtree(path)
    except OSError as err:
        print(f"unable to delete direcotry path due to: {err}")
