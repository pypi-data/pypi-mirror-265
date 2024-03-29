# Author: Mark Blakeney, Feb 2024.
"Uninstall extra packages from an application's virtual environment."
from __future__ import annotations

from argparse import ArgumentParser, Namespace
from typing import Optional

from .. import utils

def init(parser: ArgumentParser) -> None:
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='give more output')
    parser.add_argument('package',
                        help='existing package name')
    parser.add_argument('extras', nargs='+',
                        help='extra package name[s] to uninstall')

def main(args: Namespace) -> Optional[str]:
    pkgname, vdir = utils.get_package_from_arg(args.package, args)
    if not vdir:
        return f'package {pkgname} is not installed.'

    pip_args = utils.make_args((args.verbose, '-v'))
    extras = ' '.join(f'"{a}"' for a in args.extras)
    if not utils.piprun(vdir, f'uninstall{pip_args} {extras}'):
        return f'Error: failed to uninstall {extras} to {pkgname}'

    return utils.add_or_remove_pkg(vdir, pkgname, args.extras, args, add=False)
