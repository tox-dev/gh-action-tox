# One (Reusable) Tox Workflow To Rule Them All And A Tox Github Action

This repository holds a centrally maintained test matrix and a GitHub
Action for tox-based projects.

## Howto

The example use is demonstrated below. You can start by provisioning a
file at the path `.github/workflows/ci-cd.yml` in your repository.

```yaml
---

name: 🧪

on:
  pull_request:
  push:
  schedule:
  - cron: 1 0 * * *  # Run daily at 0:01 UTC

concurrency:
  group: >-
    ${{
        github.workflow
    }}-${{
        github.event.pull_request.number || github.sha
    }}
  cancel-in-progress: true

jobs:
  tox-matrix:
    name: >-  # Short name for UI, or use 🧑‍💻, it's even shorter
      [m]
    # REPRODUCIBILITY NOTE: Replace the `main` version with a stable tag
    uses: tox-dev/workflow/.github/workflows/tox.yml@main
    with:  # all of these inputs are absolutely optional
      max-python:  # Python maximum, formated as MAJOR.MINOR
      min-python:  # Python minimum, formated as MAJOR.MINOR
      tox-target:  # Regex to filter the detected tox envs
      tox-version:  # Tox PyPI package w/ version spec for pip
      YOLO: true  # Rely on the unstable version of the underlying GHA

...
```

## Features

The reusable workflow has a job called `✅ check-tox` that waits for the
whole tox matrix. It can be used in the branch protection to avoid
having to list each of the dynamic check names.
