"""
Bump module contained version (i.e. __init__.py).
Changes the file, commits and tags. You verufy and push.
"""

# TODO:
# - support date version format
# - defensive algorithm
# - provide helpful messages on exceptions

__version__ = '1.1.0'
__author__ = 'Bartek Rychlicki'
__author_email__ = 'bartek.r@webinterpret.com'
import argparse
from copy import copy
import re
import subprocess

RE_VERSION = re.compile(
    "(?P<start>(__version__|version) ?= ?)"
    "'(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)'"
)
repl = "\g<start>'{major}.{minor}.{patch}'"


def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        '--part',
        choices=['major', 'minor', 'patch'],
        default='patch'
    )
    parser.add_argument(
        '-n',
        '--dry-run',
        action='store_true'
    )
    parser.add_argument(
        '-f',
        '--filename',
        default='setup.py'
    )
    return parser.parse_args()


def _get_version(file_content, str_):
    search = RE_VERSION.search(file_content)
    version = search.groupdict()
    print('[INFO] {desc:>8} version : {major}.{minor}.{patch}'.format(
        desc=str_, **version))
    return version


def get_file_contents(filename):
    with open(filename) as fo:
        return fo.read()


def bump(current_version):
    new_version = copy(current_version)
    # dirty
    if args.part == 'minor':
        new_version['patch'] = 0
    if args.part == 'major':
        new_version['minor'] = 0
        new_version['patch'] = 0
    bumped = int(current_version[args.part]) + 1
    new_version[args.part] = str(bumped)
    return new_version


def change_the_file():
    if args.dry_run:
        return
    file_content = get_file_contents(args.filename)
    current_version = _get_version(file_content, 'detected')
    new_version = bump(current_version)
    with open(args.filename, 'w') as fo:
        changed_file_content = RE_VERSION.sub(
            repl.format(**new_version), file_content)
        fo.write(changed_file_content)


def _call_shell(cmd, exception_msg):
    child = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    print('[CALLED] %s' % cmd)
    child.communicate()
    if child.returncode:
        raise Exception(exception_msg)


def commit(new_version):
    cmd = (
        'git commit {filename} '
        '-m "Bump version to {major}.{minor}.{patch}"'
    ).format(
        filename=args.filename, **new_version
    )
    if not args.dry_run:
        _call_shell(cmd, 'commit failed')


def tag(new_version):
    cmd = 'git tag v{major}.{minor}.{patch}'.format(**new_version)
    if not args.dry_run:
        _call_shell(cmd, 'tagging failed')


def main():
    global args
    args = parse_args()
    change_the_file()
    new_version = _get_version(get_file_contents(args.filename), 'new')
    commit(new_version)
    tag(new_version)
    print(
        '[INFO] Verify that all is well and paste'
        '\n git push\n git push --tags'
        '\n[INFO] Both may be needed depending on your git.config.push.default'
    )

if __name__ == '__main__':
    main()
