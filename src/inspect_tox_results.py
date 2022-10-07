#! /usr/bin/env python

import json
import os
import sys
from pprint import pprint


FILE_APPEND_MODE = 'a'


print('::group::Printing json results...')

results_json_string = sys.argv[1].strip().replace('\n', '%0A')
toxenv_name = sys.argv[2].strip()
tox_results_file = sys.argv[3]

github_summary_file_path = os.environ['GITHUB_STEP_SUMMARY']

tox_results = json.loads(results_json_string)
with open(tox_results_file, 'r') as tox_results_fd:
    tox_results = json.load(tox_results_fd)
toxenv_data = tox_results['testenvs'][toxenv_name]
test_commands = toxenv_data['test']

with open(github_summary_file_path, mode=FILE_APPEND_MODE) as summary_file:
    for test_cmd in test_commands:
        pprint(test_cmd)
        summary_file.write('# Tox run command result')
        summary_file.write('\n')
        summary_file.write(test_cmd)

        summary_file.write('\n')
        summary_file.write('\n')

        test_cmd_out = test_cmd['output']
        escaped_test_cmd_out = test_cmd_out.replace('\n', '%0A')

        rc = test_cmd['retcode']
        if rc:
            print(
                '::error file=({rc}) $ {cmd}::{out}'.
                format(
                    rc=rc,
                    cmd=' '.join(test_cmd['command']),
                    out=escaped_test_cmd_out,
                )
            )

            summary_file.write('```console')
            summary_file.write('\n')
            summary_file.write(
                '({rc}) $ {cmd}\n{out}'.
                format(
                    rc=rc,
                    cmd=' '.join(test_cmd['command']),
                    out=test_cmd_out,
                )
            )
            summary_file.write('\n')
            summary_file.write('```')
            summary_file.write('\n')
            summary_file.write('\n')

            continue

        print(
            '::debug:({rc}) $ {cmd}'.
            format(rc=rc, cmd=' '.join(test_cmd['command']))
        )
        print(f'::debug:{test_cmd_out}')
        print('::debug:{out}'.format(out=escaped_test_cmd_out))

        summary_file.write('```console')
        summary_file.write('\n')
        summary_file.write(
            '({rc}) $ {cmd}\n{out}'.
            format(
                rc=rc,
                cmd=' '.join(test_cmd['command']),
                out=test_cmd_out,
            )
        )
        summary_file.write('\n')
        summary_file.write('```')
        summary_file.write('\n')
        summary_file.write('\n')
