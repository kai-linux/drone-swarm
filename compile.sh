#!/bin/bash

# This script compiles the C++ code.

set -e

PYTHON="$(pwd)/.venv/bin/python"

echo "== Configure =="
cmake -S . -B build -G Ninja \
  -DPython_EXECUTABLE="$PYTHON" \
  > /dev/null

echo "== Build =="
cmake --build build