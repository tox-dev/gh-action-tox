#! /usr/bin/env python

import json
import sys

with open(sys.argv[1], 'r') as fd:
    tox_results = json.load(fd)
toxenv_data = tox_results['testenvs'][sys.argv[2]]
test_commands = toxenv_data['test']

for test_cmd in test_commands:
    from pprint import pprint
    pprint(test_cmd)

    rc = test_cmd['retcode']
    if rc:
        print(
            '::error file=({rc}) $ {cmd}::{out}'.
            format(
                rc=rc,
                cmd=' '.join(test_cmd['command']),
                out=test_cmd['output'].replace('\n', '%0A'),
            )
        )
        continue

    print(
        '::debug:({rc}) $ {cmd}'.
        format(rc=rc, cmd=' '.join(test_cmd['command']))
    )
    print('::debug:{out}'.format(out=test_cmd['output'].replace('\n', '%0A')))
