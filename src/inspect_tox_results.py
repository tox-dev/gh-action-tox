#! /usr/bin/env python

import json
import sys
from pprint import pprint

print('::group::Printing json results...')

results_json_string = sys.argv[1].strip().replace('\n', '%0A')
toxenv_name = sys.argv[2].strip()

tox_results = json.loads(results_json_string)
toxenv_data = tox_results['testenvs'][toxenv_name]
test_commands = toxenv_data['test']

for test_cmd in test_commands:
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

    test_cmd_out = test_cmd['output'].replace('\n', '%0A')
    print(
        '::debug:({rc}) $ {cmd}'.
        format(rc=rc, cmd=' '.join(test_cmd['command']))
    )
    print(f'::debug:{test_cmd_out}')
    print('::debug:{out}'.format(out=test_cmd['output'].replace('\n', '%0A')))
