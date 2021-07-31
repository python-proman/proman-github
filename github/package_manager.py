# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: MPL 2.0, see LICENSE for more details.
'''Manage Packages from GitHub.'''

import json
import os
import shutil
from tempfile import TemporaryDirectory
from typing import Any, Dict, List, Optional
from urllib.request import Request, urlopen

from invoke import Collection, Context, task

from . import config
# from . import filesystem
from .archive import Archive

# archives:
#   - url: https://api.github.com/repos/octocat/hello-world/releases
#   - owner: fluxcd
#     repo: flux2
#     tag: v0.7.3
#     archive: flux_0.7.3_linux_amd64.tar.gz
#     executable: flux
#   - owner: kubernetes-sigs
#     repo: kustomize
#     tag: kustomize/v3.9.2
#     archive: kustomize_v3.9.2_linux_amd64.tar.gz
#     executable: kustomize
#   - url: https://dl.k8s.io/release/v1.20.2/bin/linux/amd64/kubectl
#     archive: kubectl
#   - owner: mozilla
#     repo: sops
#     tag: v3.6.1
#     archive: sops-v3.6.1.linux
#     executable: sops


def __get_releases() -> str:
    pass


def __get_asset(
    assets: List[Dict[str, Any]],
    archive: Optional[str] = None,
    platform: str = config.system_type,
    arch: Optional[str] = None,
    suffix: Optional[str] = None,
) -> Optional[str]:
    '''Get archive for platform or architecture.'''
    # print(json.dumps(assets, sort_keys=True, indent=2))
    names = [x['name'] for x in assets]
    for x in assets:
        if archive in names:
            return x
        elif x['content_type'] == 'application/octet-stream':
            if platform != '' and platform in x['name']:
                return x
            if arch and arch in x['name']:
                return x
            if suffix and suffix in x['name']:
                return x
    print('cannot find package')
    return None


def get_release_metadata(url: str) -> Dict[str, Any]:
    '''Get release metadata.'''
    # TODO: need to allow for specific versions
    with urlopen(url) as connection:
        response = connection.read().decode('utf-8')
        return json.loads(response)


def download_package(url: str, dest: str) -> None:
    '''Download package.'''
    # TODO: need to allow for specific versions
    request = Request(
        url, headers={'Accept': 'application/octet-stream'}
    )
    with urlopen(request) as response:
        data = response.read()
        with open(dest, 'wb') as f:
            f.write(data)


def unpack_archive(path: str, dest: str) -> None:
    '''Unpack tarball.'''
    archive = Archive()
    archive.unpack(path, dest)


def move_files() -> None:
    '''Move files to location.'''
    # - name: Move executable
    #   copy:
    #     src: "/tmp/{{ item.executable | d(item.archive) }}"
    #     dest: /usr/local/bin/
    #     mode: '0755'
    #     remote_src: true
    pass


def rename_executable(path: str) -> None:
    '''Rename executable.'''
    #     - archive_type.stat['mimetype'] == 'application/x-executable'
    #     - item.executable is defined
    # - name: Rename executable
    #   copy:
    #     src: "/tmp/{{ item.archive }}"
    #     dest: "/tmp/{{ item.executable }}"
    #     remote_src: true
    pass


@task
def install(
    ctx,  # type: Context
    owner=None,  # type: Optional[str]
    repo=None,  # type: Optional[str]
    version='latest',  # type: str
    url=None,  # type: Optional[str]
    filename=None,  # type: Optional[str]
    new_filename=None,  # type: Optional[str]
    file_pattern=f"*{config.system_type}*"  # type: str
):  # type: (...) -> None
    '''Install GitHub release.'''
    try:
        url = Request(
            f"{config.url_base}/repos/{owner}/{repo}/releases/{version}"
        )
        metadata = get_release_metadata(url)
        # print(json.dumps(metadata, sort_keys=True, indent=2))
        # get_releases
        asset = __get_asset(assets=metadata['assets'])
        print(json.dumps(asset, sort_keys=True, indent=2))
        with TemporaryDirectory() as td:
            contents_dir = os.path.join(td, 'contents')
            os.makedirs(contents_dir)
            filepath = os.path.join(td, asset['name'])
            download_package(asset['url'], filepath)
            unpack_archive(filepath, contents_dir)

            contents = os.listdir(contents_dir)
            if len(contents) == 1:
                filepath = os.path.join(contents_dir, contents[0])
                file_check = ctx.run(f"file --mime {filepath}")
                if file_check.exited == 0:
                    mimetype, charset = file_check.stdout\
                        .split(':')[1]\
                        .split(';')
                    if mimetype.strip() == 'application/x-executable':
                        shutil.move(
                            filepath,
                            os.path.join(
                                os.path.expanduser('~'),
                                '.local',
                                'bin',
                                contents[0],
                            )
                        )
                    else:
                        print('blah')
            else:
                for x in contents:
                    if os.path.isfile(os.path.join(contents, x)):
                        pass
            print('temp contents', os.listdir(td))
        # filesystem.mkdir(ctx, config.bin_path)
        # with ctx.cd(config.bin_path):
        #     if filename:
        #         __filepath = os.path.join(config.bin_path, filename)
        #         if new_filename:
        #             if os.path.exists(__filepath):
        #                 __new_filepath = os.path.join(
        #                     config.bin_path, new_filename
        #                 )
        #                 if not os.path.exists(__new_filepath):
        #                     os.rename(__filepath, __new_filepath)
        #                     __filepath = __new_filepath
        #         if os.name == 'posix':
        #             st = os.stat(__filepath)
        #             os.chmod(__filepath, st.st_mode | 0o111)
    except OSError as err:
        print(f"unable to download github release due to: {err}")


def uninstall(ctx, name):  # type: (Context, str) -> None
    '''Uninstall GitHub release.'''
    pass


def search(
    ctx, owner=None, repo=None
):  # type: (Context, Optional[str], Optional[str]) -> None
    '''Search for packages.'''
    pass


tasks = Collection(install, uninstall)
tasks.configure({
    'conflicted': 'default value',
    'package': {
        'interpreter': 'python3',
        'name': 'example value'
    },
})
