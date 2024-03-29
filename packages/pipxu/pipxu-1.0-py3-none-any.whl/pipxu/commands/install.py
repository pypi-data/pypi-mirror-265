# Author: Mark Blakeney, Feb 2024.
'Install a Python application using an isolated virtual environment.'
from __future__ import annotations

import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Optional

from filelock import FileLock
from platformdirs import user_runtime_path

from .. import utils
from ..run import run

MAX_VDIRS = 1_000_000

def get_python(args: Namespace) -> str:
    'Return the python executable based on command line args'
    if args.pyenv:
        pyenv_root = run('pyenv root', capture=True)
        if not pyenv_root:
            sys.exit('Error: Can not find pyenv. Is it installed?')

        pyenv_version = run(f'pyenv latest {args.pyenv}', capture=True)
        if not pyenv_version:
            sys.exit(f'Error: no pyenv version {args.pyenv} installed.')

        pyexe = Path(pyenv_root, 'versions', pyenv_version, 'bin', 'python')
        if not pyexe.exists():
            sys.exit(f'Can not determine pyenv version for {args.pyenv}')
    elif args.python:
        pyexe = Path(args.python)
        if not pyexe.exists():
            sys.exit(f'{pyexe} does not exist.')
    else:
        pyexe = args._pyexe

    return str(pyexe)

def get_next_vdir(vdirbase: Path, maxn) -> Optional[Path]:
    'Return the first available venv directory'
    vdirs = set(int(f.name) for f in vdirbase.iterdir())
    for n in range(1, maxn + 1):
        if n not in vdirs:
            return vdirbase / str(n)

    return None

def init(parser: ArgumentParser) -> None:
    "Called to add this command's arguments to parser at init"
    xgroup = parser.add_mutually_exclusive_group()
    xgroup.add_argument('-p', '--python',
                        help='specify explicit python executable path')
    xgroup.add_argument('-P', '--pyenv',
                        help='pyenv python version to use, '
                        'i.e. from `pyenv versions`, e.g. "3.9".')
    parser.add_argument('-f', '--force', action='store_true',
                        help='recreate any existing venv')
    parser.add_argument('-e', '--editable', action='store_true',
                        help='install package[s] in editable mode')
    parser.add_argument('-d', '--include-deps', action='store_true',
                        help='include executables from dependencies')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='give more output')
    parser.add_argument('package', nargs='+',
                        help='package[s] to install')

def main(args: Namespace) -> Optional[str]:
    'Called to action this command'
    pyexe = get_python(args)
    venv_args = utils.make_args((args.verbose, '-v'), (not args.verbose, '-q'),
                                (bool(pyexe), f'--python={pyexe}'))
    pip_args = utils.make_args((args.verbose, '-v'), (args.editable, '-e'))

    lockfile = user_runtime_path() / f'{args._prog}.lock'
    vdirbase = args._venvs_dir
    for pkg in args.package:
        # Use a lock file in case we are running multiple installs in parallel
        with FileLock(lockfile):
            vdir = get_next_vdir(vdirbase, MAX_VDIRS)
            if not vdir:
                return f'Error: Too many vdirs (>{MAX_VDIRS}) in {vdirbase}'

            # Create the vdir
            if not run(f'uv venv {venv_args} {vdir}'):
                utils.rm_vdir(vdir, args)
                return f'Error: failed to create {vdir} for {pkg}.'

        python_exe = (vdir / 'bin' / 'python').resolve()
        python_ver = run(f'{python_exe} -V', capture=True)
        python_ver = python_ver.strip().split()[1] if python_ver else '?ver?'
        print(f'Created {vdir} using {python_exe} ({python_ver})')

        # Install the package
        if not utils.piprun(vdir, f'install --no-deps{pip_args} "{pkg}"'):
            utils.rm_vdir(vdir, args)
            return f'Error: failed to preinstall "{pkg}".'

        versions = utils.get_versions(vdir)
        if not versions:
            utils.rm_vdir(vdir, args)
            return f'Error: failed to get versions for {pkg}.'

        if len(versions) != 1:
            return f'Error: multiple packages qualified: {list(versions)}'

        pkgname, (vers, editpath) = versions.popitem()
        pdir = Path(args._packages_dir, pkgname)

        if pdir.exists():
            if not args.force:
                utils.rm_vdir(vdir, args)
                return f'Error: venv for {pkgname} exists. Use -f to force.'
            print(f'Removing pre-existing {pkgname} venv dir.')
            utils.rm_vdir(pdir, args)
            pdir.unlink()

        if not utils.piprun(vdir, f'install{pip_args} "{pkg}"'):
            utils.rm_vdir(vdir, args)
            return f'Error: failed to install "{pkg}".'

        pdir.symlink_to(vdir)

        data: dict = {'name': pkgname}
        if editpath:
            data['editpath'] = editpath

        if args.include_deps:
            data['deps'] = True

        err = utils.make_links(vdir, pkgname, args, data)
        if err:
            pdir.unlink()
            utils.rm_vdir(vdir, args)
            return err

    return None
