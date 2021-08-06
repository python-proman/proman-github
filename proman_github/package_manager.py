'''Test download.'''
import os
import platform
import shutil
from tempfile import TemporaryDirectory
from typing import Any, Dict, List, Optional, TYPE_CHECKING
from urllib.request import Request, urlopen

import magic
from github import Github
from proman_common.bases import PackageManagerBase
from proman_common.filepaths import GlobalDirs

# from proman_github import config
# from proman_github import filesystem
from proman_github.archive import Archive

if TYPE_CHECKING:
    from github.GithubReleaseAsset import GithubReleaseAsset
    from github.PaginatedList import PaginatedList
    from .config import Manifest


class PackageManager(PackageManagerBase):
    '''Proide package manager for GitHub releases.'''

    def __init__(
        self,
        manifest: Optional['Manifest'] = None,
        force: bool = False,
        update: bool = False,
        **kwargs: Any,
    ) -> None:
        '''Initialize GitHub package manager.'''
        self.__manifest = manifest
        self.__arch: str = kwargs.get('arch', platform.machine().lower())
        self.__platform: str = kwargs.get('platorm', platform.system().lower())
        self.__dirs = kwargs.get('dirs', GlobalDirs())
        self.__github = kwargs.get('github', Github())
        self.__archive = kwargs.get('archive', Archive())

    def __get_asset(
        self,
        assets: 'PaginatedList',
        archive: Optional[str] = None,
        arch: Optional[str] = None,
        suffix: Optional[str] = None,
    ) -> Optional['GithubReleaseAsset']:
        '''Get archive for platform or architecture.'''
        match = None
        weight = 0
        asset_names = [x.name for x in assets]
        for asset in assets:
            asset_weight = 0
            if archive and archive in asset_names:
                return asset
            elif (
                asset.content_type == 'application/octet-stream'
                or asset.content_type == 'application/gzip'
                or asset.content_type == 'application/zip'
            ):
                if self.__platform != '' and self.__platform in asset.name:
                    asset_weight += 2
                if self.__arch and self.__arch in asset.name:
                    asset_weight += 1
                if suffix and asset.name.endswith(suffix):
                    asset_weight += 1
                if asset_weight > weight:
                    match = asset
                    weight = asset_weight
        return match

    def _unpack_archive(self, path: str, dest: str) -> List[str]:
        '''Unpack tarball.'''
        os.makedirs(dest)
        self.__archive.unpack(path, dest)
        return os.listdir(dest)

    def __install_executable(self, executable: str, source_path: str) -> None:
        '''Install executable.'''
        executable_path = os.path.join(self.__dirs.executable_dir, executable)
        if not os.path.exists(executable_path):
            os.makedirs(self.__dirs.executable_dir, exist_ok=True)
            shutil.move(source_path, executable_path)
            if os.name == 'posix':
                st = os.stat(executable_path)
                os.chmod(executable_path, st.st_mode | 0o111)
        else:
            print('already installed:', executable)

    def _install_asset(self, source_path: str, filename: str) -> None:
        '''Install package.'''
        # handle download
        mimetype = magic.from_file(source_path, mime=True)
        if mimetype == 'application/x-executable':
            self.__install_executable(filename, source_path)
        else:
            contents_dir = os.path.join(
                os.path.dirname(source_path), 'contents'
            )
            contents = self._unpack_archive(source_path, contents_dir)
            for path in contents:
                contents_file = os.path.join(contents_dir, path)
                if os.path.isfile(contents_file):
                    mimetype = magic.from_file(contents_file, mime=True)
                    if mimetype == 'application/x-executable':
                        self.__install_executable(filename, contents_file)

    def install(
        self,
        name: Optional[str],
        dev: bool = False,
        **kwargs: Any,
    ) -> None:
        '''Install GitHub release.'''
        owner = kwargs.get('owner', None)
        project = kwargs.get('project', None)
        version = kwargs.get('version', 'latest')
        if name:
            repository = name
        elif owner and project:
            repository = f"{owner}/{project}"
        filename = kwargs.get('filename', project)
        if not filename:
            filename = repository.split('/')[1]
        # file_pattern: str = f"*{config.system_type}*",

        assets = self.search(repository, version=version)
        asset = self.__get_asset(assets)

        if asset:
            with TemporaryDirectory() as temp_dir:
                filepath = os.path.join(temp_dir, asset.name)
                self.download(asset.url, filepath)
                self._install_asset(source_path=filepath, filename=filename)
            if self.__manifest:
                self.__manifest.add_dependency(
                    name=repository,
                    version='meh',
                    dev=dev,
                )
        else:
            raise Exception('no release found')

    def __remove_paths(self, path: str) -> None:
        '''Remove package directory from path.'''
        try:
            shutil.rmtree(path)
        except OSError as err:
            print(f"unable to delete direcotry path due to: {err}")

    def uninstall(self, name: str, force: bool = False) -> None:
        '''Perform package uninstall.'''
        pass

    def update(self, name: str, force: bool = False) -> None:
        '''Update the package.'''
        pass

    def search(self, name: str, **kwargs: Any) -> 'PaginatedList':
        '''Perform package search.'''
        version = kwargs.get('version', 'latest')
        if version == 'latest':
            assets = gh.get_repo(name).get_latest_release().get_assets()
        else:
            # assets = gh.get_repo(name).get_latest(id='test').get_assets()
            assets = gh.get_repo(name).get_latest_release().get_assets()
        return assets

    def info(self, name: str, output: str) -> Dict[str, Any]:
        '''Retrieve package information.'''
        return {}

    def download(self, url: str, dest: str) -> None:
        '''Download package.'''
        try:
            request = Request(
                url, headers={'Accept': 'application/octet-stream'}
            )
            with urlopen(request) as response:
                data = response.read()
                with open(dest, 'wb') as f:
                    f.write(data)
        except OSError as err:
            print(f"unable to download github release due to: {err}")

    def __get_releases(self) -> str:
        pass


token = os.getenv('GITHUB_TOKEN')
gh = Github(token)
global_dirs = GlobalDirs()

# download = gh.get_repo("PyGithub").get_download(242550)

headers = {
    'Authorization': f"token {token}",
    'Accept': 'application/octet-stream'
}

pkgmgr = PackageManager(github=gh, dirs=global_dirs)

assets = pkgmgr.search('mozilla/sops')
pkgmgr.install('mozilla/sops')
pkgmgr.install('fluxcd/flux2')
pkgmgr.install('kubernetes-sigs/kustomize')

# archives:
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
#   - owner: mozilla
#     repo: sops
#     tag: v3.6.1
#     archive: sops-v3.6.1.linux
#     executable: sops
#   - url: https://api.github.com/repos/octocat/hello-world/releases
#   - url: https://dl.k8s.io/release/v1.20.2/bin/linux/amd64/kubectl
#     archive: kubectl
