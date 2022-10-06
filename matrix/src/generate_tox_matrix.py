#! /usr/bin/env python

import enum
import itertools
import json
import re
import subprocess
import sys


class os(enum.Enum):
    macos = 'macOS'
    ubuntu = 'Ubuntu'
    windows = 'Windows'


VM_LATEST_MAP = {
    os.macos: '11',
    os.ubuntu: '20.04',
    os.windows: '2022',
}

VM_VERSIONS = {
    os.macos: (
        VM_LATEST_MAP[os.macos],
        '12',
    ),
    os.ubuntu: (
        VM_LATEST_MAP[os.ubuntu],
        '22.04',
    ),
    os.windows: (
        '2019',
        VM_LATEST_MAP[os.windows],
    ),
}

VM_NAMES = tuple(
    f'{os.value}-{version}'
    for os, versions in VM_VERSIONS.items()
    for version in versions
)

INCOMPATIBLE_PYTHONS = {
    f'{os.ubuntu}-22.04': {'3.5', '2.7'},
}


print('::group::Generating GHA environments based on tox config')
filter_pattern = sys.argv[1]

min_py_ver, max_py_ver = sys.argv[2:4]
if min_py_ver:
    min_py_ver = tuple(map(int, min_py_ver.split('.')))
else:
    min_py_ver = 2, 7
if max_py_ver:
    max_py_ver = tuple(map(int, max_py_ver.split('.')))
else:
    max_py_ver = 3, 10

def inc_minor_py_ver(ver):
    if ver == (2, 7):
        return 3, 5
    return ver[0], ver[1] + 1

def generate_py_vers(min_py, max_py):
    cur_ver = min_py
    while cur_ver <= max_py:
        yield cur_ver
        cur_ver = inc_minor_py_ver(cur_ver)

tox_discovery_cmd = sys.executable, '-m', 'tox', '-a'
toxenvs = set(subprocess.check_output(
    tox_discovery_cmd,
    universal_newlines=True,
).splitlines())
if {'py', 'python'} & toxenvs:
    toxenvs -= {'py', 'python'}
    for py_ver in generate_py_vers(min_py_ver, max_py_ver):
        toxenvs |= {f'py{py_ver[0]}{py_ver[1]}'}

envs = []
for vm, toxenv in itertools.product(VM_NAMES, toxenvs):
    if filter_pattern and not re.search(filter_pattern, toxenv):
        print(
            f'`{toxenv}` does not match `{filter_pattern}`. '
            'Excluding it...',
        )
        continue

    py_ver = (
        (toxenv[2], toxenv[3:]) if toxenv.startswith('py')
        else max_py_ver
    )

    py_ver_str = '.'.join(py_ver)
    print(f'Checking if `{py_ver_str}` is compatible with `{vm}`...')
    print(f'`{vm}` incompatibilities are: {INCOMPATIBLE_PYTHONS.get(vm)!r}')
    if py_ver_str in INCOMPATIBLE_PYTHONS.get(vm, set()):
        print(
            f'`{toxenv}` does not match `{filter_pattern}`. '
            'Excluding it...',
        )
        continue

    print(f'Adding `{toxenv}` via `{py_ver_str}` @ `{vm}` to the list')
    envs.append({
        'python-version': py_ver_str,
        'runs-on': vm,
        'toxenv': toxenv,
    })

matrix_json_string = json.dumps({'include': envs})
print(f'::set-output name=matrix::{matrix_json_string}')
print('::endgroup::')
