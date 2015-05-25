"""
Bump module contained version (i.e. __init__.py).
Changes the file, commits and tags. You verify and push.
"""

# TODO:
# - support date version format
# - defensive algorithm
# - provide helpful messages on exceptions

import argparse
from copy import copy
import re

from git import Repo


RE_VERSION = re.compile(
    "(?P<start>(__version__|version) ?= ?)"
    "'(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)'"
)
repl = "\g<start>'{major}.{minor}.{patch}'"

repo = Repo()


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
    if not search:
        raise Exception('regex mismatch, is version specified correctly?')
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
        print('[INFO] %s changed ' % args.filename)


def commit(new_version):
    msg = 'Bump version to {major}.{minor}.{patch}'.format(**new_version)
    if not args.dry_run:
        print('[CALLED] git add %s ' % args.filename)
        repo.index.add([args.filename])
        print('[CALLED] git commit %s -m "%s"' % (args.filename, msg))
        repo.index.commit(msg)


def tag(new_version):
    if not args.dry_run:
        msg = 'v{major}.{minor}.{patch}'.format(**new_version)
        print('[CALLED] git tag %s ' % msg)
        repo.create_tag(path=msg)


def validate_repository_state():
    assert not repo.is_dirty(), 'Dirty status, aborting.'
    assert repo.active_branch.name == 'master', \
        'You need to be on master to bump.'


def main():
    global args
    args = parse_args()
    validate_repository_state()
    change_the_file()
    new_version = _get_version(get_file_contents(args.filename), 'new')
    commit(new_version)
    tag(new_version)
    print(
        '[INFO] Verify that all is well and paste'
        '\n git push\n git push --tags'
        '\n[INFO] Both may be needed depending on your git.config.push.default'
        '\n[INFO] Now build dists and upload to cheeseshops:'
        '\n python setup.py bdist_wheel'
        '\n rm -rf dist build  # clean'
        '\n twine upload -r wi dist/*.whl'
        '\n twine upload -r ubuntuwheels dist/*.whl  # optional'
        '\n rm -rf dist build  # clean'
    )

if __name__ == '__main__':
    main()
