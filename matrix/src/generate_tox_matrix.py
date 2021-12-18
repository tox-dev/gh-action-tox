#! /usr/bin/env python

import itertools
import json
import re
import subprocess
import sys


VM_LIST = 'macOS', 'Ubuntu', 'Windows'


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
for vm, toxenv in itertools.product(VM_LIST, toxenvs):
    if filter_pattern and not re.search(filter_pattern, toxenv):
        print(
            f'`{toxenv}` does not march `{filter_pattern}`. '
            'Excluding it...',
        )
        continue

    print(f'Adding `{toxenv}` to the list')
    py_ver = (
        (toxenv[2], toxenv[3:]) if toxenv.startswith('py')
        else max_py_ver
    )
    envs.append({
        'python-version': '.'.join(py_ver),
        'runs-on': f'{vm}-latest',
        'toxenv': toxenv,
    })

matrix_json_string = json.dumps({'include': envs})
print(f'::set-output name=matrix::{matrix_json_string}')
print('::endgroup::')
