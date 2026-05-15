#!/bin/bash
set -e

PYTHON="$(pwd)/.venv/bin/python"

echo "== Train PPO =="
"$PYTHON" python/train_ppo.py

echo "== Evaluate PPO =="
"$PYTHON" python/evaluate_ppo.py

echo "== Visualize Policy =="
"$PYTHON" python/visualize_policy.py