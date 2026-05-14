Build the C++ simulator

Run:
```
cmake -S . -B build -G Ninja
cmake --build build
```

Then run:
```
./build/swarm_sim
```
You should see:

Simulation finished. Wrote trajectory.csv
Now you should have: trajectory.csv in your project root.

```
python python/plot_trajectory.py
```