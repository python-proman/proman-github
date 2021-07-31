# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: MPL 2.0, see LICENSE for more details.
'''Configuration for package manager.'''

import os
import platform

url_base = 'https://api.github.com'

arch_type = platform.architecture()

# System setup
system_type = platform.system().lower()
if system_type == 'windows':
    __exec_subpath = 'bin'

if system_type == 'darwin':
    __exec_subpath = os.path.join('Library', 'bin')

if system_type == 'linux':
    __exec_subpath = os.path.join('.local', 'bin')

# Paths
home_dir = os.path.expanduser('~')
exec_dir = os.path.join(home_dir, __exec_subpath)
