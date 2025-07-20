#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

echo "$PWD"

export PYTHONPATH="src/b2broker/"

source venv/bin/activate

python3 -m gunicorn --bind 0.0.0.0:8000 config.wsgi --reload --capture-output
