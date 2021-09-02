'''Test download.'''

import os

from proman_github import get_package_manager

token = os.getenv('GITHUB_TOKEN')

headers = {
    'Authorization': f"token {token}",
    'Accept': 'application/octet-stream'
}

pkgmgr = get_package_manager(token)

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
