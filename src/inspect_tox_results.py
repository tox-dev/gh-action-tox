#! /usr/bin/env python

import json
import os
import sys
from pprint import pprint
try:
    from shlex import join as _shlex_join  # Python 3.8+
except ImportError:
    # Vendored from
    # https://github.com/python/cpython/blob/e500cc0/Lib/shlex.py#L316-L318
    def _shlex_join(split_command):
        """Return a shell-escaped string from *split_command*."""
        return ' '.join(quote(arg) for arg in split_command)


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
    summary_file.write(
        '# {status_emoji} Tox run results'.
        format(
            status_emoji='❌' if any(cmd['retcode'] for cmd in test_commands)
            else '✓',
        ),
    )
    summary_file.write('\n')
    summary_file.write('\n')
    for command_number, test_cmd in enumerate(test_commands):
        pprint(test_cmd)

        rc = test_cmd['retcode']
        status_emoji='❌' if rc else '✓'

        summary_file.write(
            '## {status_emoji} Tox command #{command_number} result'.
            format(status_emoji=status_emoji, command_number=command_number),
        )
        summary_file.write('\n')
        summary_file.write(repr(test_cmd))

        summary_file.write('\n')
        summary_file.write('\n')

        test_cmd_out = test_cmd['output']
        escaped_test_cmd_out = test_cmd_out.replace('\n', '%0A')

        lexed_command = _shlex_join(test_cmd['command'])
        raw_command = ' '.join(test_cmd['command'])

        summary_file.write('<details>')
        summary_file.write('\n')
        summary_file.write('\n')
        summary_file.write('<summary>')
        summary_file.write(
            '{status_emoji} <code>({rc}) $ <kbd>{cmd}</kbd></code>'.
            format(status_emoji=status_emoji, rc=rc, cmd=lexed_command),
        )
        summary_file.write('</summary>')
        summary_file.write('\n')
        summary_file.write('\n')
        summary_file.write('```console')
        summary_file.write('\n')
        summary_file.write(test_cmd_out)
        summary_file.write('\n')
        summary_file.write('```')
        summary_file.write('\n')
        summary_file.write('\n')
        summary_file.write('</details>')
        summary_file.write('\n')
        summary_file.write('\n')

        if rc:
            print(
                '::error file=({rc}) $ {cmd}::{out}'.
                format(
                    rc=rc,
                    cmd=raw_command,
                    out=escaped_test_cmd_out,
                )
            )
            continue

        print(
            '::debug:({rc}) $ {cmd}'.
            format(rc=rc, cmd=raw_command)
        )
        print('::debug:{out}'.format(out=escaped_test_cmd_out))
