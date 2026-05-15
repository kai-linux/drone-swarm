#!/bin/bash
set -e

PYTHON="$(pwd)/.venv/bin/python"

echo "== Configure =="
cmake -S . -B build -G Ninja \
  -DPython_EXECUTABLE="$PYTHON" \
  > /dev/null

echo "== Build =="
cmake --build build

echo "== Run C++ simulation =="
./build/swarm_sim

echo "== Plot =="
"$PYTHON" python/plot_trajectory.py