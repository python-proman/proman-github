# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: MPL 2.0, see LICENSE for more details.
'''Control Package Archives.'''

import gzip
import mimetypes
# import os
import tarfile
# from tempfile import TemporaryDirectory
# from zipfile import ZipFile


class Archive:
    def __init__(self):
        '''Initialize archive.'''
        pass

    def _unpack_gzip(self, path):
        with open(path, 'rb') as p:
            gzip.decompress(p.read())

    def _unpack_zipfile(self, path):
        pass

    def pack(self, path):
        '''Pack archive.'''
        pass

    def unpack(self, path, dest='.'):
        '''Unpack archive.'''
        mt = mimetypes.guess_type(path)
        if mt[0] == 'application/gzip':
            mode = 'r:gz'
        if mt[0] == 'application/x-tar':
            self._unpack_gzip(path)
            mode = 'r:gz'
        if mt[0] == 'application/x-bzip2':
            mode = 'r:bz2'
        if mt[0] == 'application/x-lzma':
            mode = 'r:xz'
        # if mt[0] == 'application/zip':
        #     mode = 'zip'

        with tarfile.open(path, mode) as archive:
            archive.extractall(dest, members=None, numeric_owner=False)
