#! /usr/bin/env python
import pathlib
import sys
import tempfile


gha_path = pathlib.Path(sys.argv[1]).absolute()
tmp_root_dir = gha_path / '.tmp'


tmp_root_dir.mkdir()


print('::group::Preparing tox results storage...')


tmp_dir = pathlib.Path(tempfile.mkdtemp('-results', 'tox-', str(tmp_root_dir)))
print(f'::set-output name=results-dir::{tmp_dir!s}')


json_results_file_path = tmp_dir / '.tox-run-results.json'
print(f'::set-output name=results-file::{json_results_file_path!s}')


print('::endgroup::')
