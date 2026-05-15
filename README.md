## System dependencies

macOS:
```bash
xcode-select --install
brew install cmake ninja python@3.12
```

Python:
```bash
python3.12 -m venv .venv 
source .venv/bin/activate
python -m pip install -r requirements.txt
python python/train_ppo.py 
python python/evaluate_ppo.py 
```

To run the C++ main interface

```bash
./run_main.sh   
```

To run the python ML training interface

```bash
./compile.sh  
python python/train_ppo.py 
python python/evaluate_ppo.py 
```

###

Alternatively:
Build the C++ simulator

Run:
```bash
cmake -S . -B build -G Ninja
cmake --build build
```

Then run:
```bash
./build/swarm_sim
```
You should see:

Simulation finished. Wrote trajectory.csv
Now you should have: trajectory.csv in your project root.

```bash
python python/plot_trajectory.py
```