#!/usr/bin/env bash

set -e
set -x

python -m venv venv
source venv/bin/activate
python -m pip install --progress-bar=off dist/*.tar.gz
pip install pytest
pytest tests/
deactivate
rm -r venv