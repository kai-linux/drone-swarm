#!/bin/bash
set -e

echo "Configuring..."
cmake -S . -B build -G Ninja

echo "Building..."
cmake --build build

echo "Running simulation..."
./build/swarm_sim

echo "Plotting..."
python python/plot_trajectory.py