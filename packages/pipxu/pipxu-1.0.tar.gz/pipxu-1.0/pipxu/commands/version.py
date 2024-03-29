# Author: Mark Blakeney, Feb 2024.
'List installed package versions.'
from __future__ import annotations

from argparse import ArgumentParser, Namespace
from typing import Optional

from .. import utils

def init(parser: ArgumentParser) -> None:
    "Called to add this command's arguments to parser at init"
    parser.add_argument('package', nargs='?',
                        help='report specific package and dependent '
                        'package versions')

def main(args: Namespace) -> Optional[str]:
    'Called to action this command'
    def display(pkgname, version):
        ver, loc = version
        if loc:
            ver += f' @ {loc}'
        print(f'{pkgname}=={ver}')

    if args.package:
        pkgname, vdir = utils.get_package_from_arg(args.package, args)
        if not vdir:
            return f'Package {pkgname} not found.'

        versions = utils.get_versions(args._packages_dir / pkgname)
        if not versions:
            return f'Package {pkgname} versions not found.'

        # Reorder version dict to put pkgname first
        if pkgname in versions:
            sversions = {pkgname: versions[pkgname]}
            del versions[pkgname]
            sversions.update(versions)
            versions = sversions

        for pkg, ver in versions.items():
            display(pkg, ver)

        return None

    for pdir, data in utils.get_all_pkg_venvs(args):
        package = pdir.name
        versions = utils.get_versions(pdir)
        if versions:
            display(package, versions.get(package, ("unknown", None)))

    return None
