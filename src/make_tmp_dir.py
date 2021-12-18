#! /usr/bin/env python

# IMPORTANT: This module runs under a variaty of Python versions and
# IMPORTANT: must keep supporting Python 2.7+ syntax.

import os
import sys
import tempfile


gha_path = os.path.abspath(sys.argv[1])
tmp_root_dir = os.path.join(gha_path, '.tmp')


os.makedirs(tmp_root_dir)


print('::group::Preparing tox results storage...')


tmp_dir = tempfile.mkdtemp('-results', 'tox-', tmp_root_dir)
print('::set-output name=results-dir::{path!s}'.format(path=tmp_dir))


json_results_file_path = os.path.join(tmp_dir, '.tox-run-results.json')
print(
    '::set-output name=results-file::{path!s}'.
    format(path=json_results_file_path),
)


print('::endgroup::')
