#!/usr/bin/env bash
set -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

VENV="/home/dipes/projects/product-catalog-service/.venv"
if [ -d "$DIR/.venv" ]; then
    VENV="$DIR/.venv"
fi

export PYTHONPATH="$DIR"
exec "$VENV/bin/python" -m uvicorn src.main:app --host 0.0.0.0 --port 8006 --reload
