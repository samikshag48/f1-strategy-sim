# F1 Race Strategy Simulator (Silverstone)

A Monte Carlo–based simulation and optimization framework for evaluating Formula 1 pit stop strategies under tire degradation, fuel burn-off, and stochastic race uncertainty.

This project explores risk-adjusted decision making and compares Python research workflows with a high-performance C++ simulation core, inspired by how quantitative trading systems evaluate strategies under uncertainty.

---

## Overview

This project models a full Formula 1 race lap-by-lap and evaluates pit strategies using repeated stochastic simulations.

Instead of optimizing only for fastest expected race time, strategies are selected using a risk-adjusted objective that balances performance against outcome variability.

> The workflow mirrors a typical quant research → production optimization pipeline.

---

## Core Features

### Monte Carlo Race Simulation
- Lap times incorporate:
  - Compound-specific tire degradation (nonlinear)
  - Fuel burn-off effects
  - Stochastic lap-to-lap noise
- Thousands of full-race simulations per strategy estimate:
  - Expected race time (mean)
  - Outcome variability (standard deviation)

---

### Strategy Optimization
- Evaluates 1-stop pit strategies across:
  - Multiple compound orderings (S→M, S→H, M→H, etc.)
  - A configurable range of pit lap choices
- Searches for optimal strategies using repeated Monte Carlo evaluation

---

### Risk Budget (λ)
Strategies are evaluated using a risk-adjusted objective;

score = mean_race_time + λ · standard_deviation


- λ (lambda) represents a risk budget
- Higher λ penalizes volatility and favors more stable outcomes
- Varying λ demonstrates how optimal strategies shift under different risk tolerances

This formulation is analogous to risk-adjusted portfolio optimization** in quantitative finance.

---

### High-Performance C++ Simulation Core
- Performance-critical simulation loop reimplemented in C++
- Enables hundreds of thousands of simulations in under one second**
- Models stochastic pit stop execution risk
- Allows direct comparison between:
  - Python (modeling, experimentation)
  - C++ (throughput, latency)

---

## Project Structure

```text
f1-strategy-sim/
├── py/
│   ├── sim.py                 # Race simulation engine
│   ├── strategies.py          # Strategy definitions
│   ├── run_experiments.py     # Baseline evaluations
│   ├── optimize.py            # Pit lap optimization
│   └── optimize_compounds.py  # Risk-adjusted compound + pit optimization
├── cpp/
│   ├── sim_core.hpp           # C++ simulation interface
│   ├── sim_core.cpp           # High-performance simulation core
│   └── main.cpp               # Risk-adjusted optimizer (C++)
└── README.md

---

## Running the Project

### Python (Research & Optimization)
From the project root:

```bash
python -m py.run_experiments
python -m py.optimize_compounds

C++ (Performance Core)
cd cpp
g++ -O3 -std=c++17 sim_core.cpp main.cpp -o sim
./sim

Example Output (C++)
C++ ran 200000 sims in 0.51 seconds
BEST (λ=1.0): 1-stop M->H @L22
mean=4710.8s  std=2.51s

Key Takeaways
    - Monte Carlo simulation enables probabilistic strategy evaluation

    - Risk-adjusted objectives expose tradeoffs between speed and stability

    - Strategy optimization depends on risk tolerance, not just expected value

    - C++ dramatically improves throughput for large-scale simulations

    - The workflow closely resembles quantitative research pipelines


Possible Extensions
    - Two-stop strategies

    - Safety car modeling

    - Tire cliff probability

    - Python ↔ C++ bindings

    - Visualization of efficient frontiers

Author
Samiksha Gupta

