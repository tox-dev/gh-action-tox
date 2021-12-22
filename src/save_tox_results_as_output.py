#! /usr/bin/env python

import json
from pathlib import Path
from sys import argv

print('::group::Saving json results...')

results_file = Path(argv[1])
tox_results = json.loads(results_file.read_text())
compact_tox_results = json.dumps(tox_results, indent=None)

urlencoded_tox_results = (
    compact_tox_results.
    replace('%', '%25').
    replace('\r', '%0D').
    replace('\n', '%0A').
    replace('\\', r'\\')
)

print(f'::set-output name=json-results::{urlencoded_tox_results}')

print('::endgroup::')
