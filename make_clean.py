# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import os
import argparse
import shutil


VERSION = (1, 0, 0)
__version__ = '{0:d}.{1:d}.{2:d}'.format(*VERSION)


def make_clean(target_dir, ignore_fname=None, ignores=None):
    '''clean target_dir except ignores relatively

    cleanup target directory except:

    - file: is in ignores
    - directory: is in ignores

    Files and directories are referenced relatively.

    :param str target_dir: target directory to cleanup
    :param list ignores: not rm files or directories
    '''
    target_dir = os.path.abspath(target_dir)
    ignore_dirs, ignore_files = parse_ignores(ignore_fname, ignores)
    rm_files(target_dir, ignore_dirs, ignore_files)
    rm_dirs(target_dir, ignore_dirs)


def parse_ignores(ignore_fname, ignore_patterns):
    ignores = []
    if ignore_fname:
        if os.path.isfile(ignore_fname):
            with open(ignore_fname) as fp:
                for line in fp:
                    line = line.strip()
                    if not line.startswith('#'):
                        ignores.append(
                            os.path.abspath(line.replace('/', os.sep)))

    if ignore_patterns:
        ignores.extend([os.path.abspath(x) for x in ignore_patterns if x])
    ignore_dirs = tuple(x for x in ignores if x and os.path.isdir(x))
    ignore_files = {x for x in ignores if x and os.path.isfile(x)}
    return ignore_dirs, ignore_files


def rm_files(target_dir, ignore_dirs, ignore_files):
    '''Remove files.'''
    for root, _, files in os.walk(target_dir):
        for f in files:
            fullpath = os.path.join(root, f)
            if (fullpath.startswith(ignore_dirs) or
                    fullpath in ignore_files):
                continue
            os.remove(fullpath)


def rm_dirs(target_dir, ignore_dirs):
    '''Remove empty directories.'''
    ignore_dir_set = set(ignore_dirs)

    for root, _, _ in os.walk(target_dir):
        if (not is_empty_dir(root) or
                root in ignore_dir_set or
                root == target_dir):
            continue
        shutil.rmtree(root)


def is_empty_dir(target_dir):
    '''return is empty directory or not

    :param str target_dir: target dir
    '''
    for root, _, files in os.walk(target_dir):
        for f in files:
            if os.path.isfile(os.path.join(root, f)):
                return False
    return True


def main():
    parser = argparse.ArgumentParser(
        description=u'clean target dir without ignores')
    parser.add_argument(
        'target_dir',
        metavar='TARGET_DIR',
        help=u'dir to remove recursively ')
    parser.add_argument(
        '--clean-ignore',
        metavar='CLEAN_IGNORE',
        help=u'dir/file file to ignore from remove',
        default='.cleanignore',
        )
    parser.add_argument(
        '-i', '--ignores',
        metavar='IGNORE',
        help=u'dir/file to ignore from remove',
        nargs='*',
        default=[],
        )
    parser.set_defaults(
        func=lambda args:
            make_clean(
                args.target_dir,
                args.clean_ignore,
                args.ignore))

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
