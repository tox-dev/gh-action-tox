#! /usr/bin/env python

from shutil import rmtree
from sys import argv
from pathlib import Path

results_dir = Path(argv[1])
group_name = f'Cleaning up the `{results_dir!s}` results directory...'

print(f'::group::{group_name}')
try:
    rmtree(results_dir)
except:
    print('❌ Failure :(')
else:
    print('🔥 Success!')
finally:
    print('::endgroup::')
