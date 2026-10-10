# Lunar Surface Deescent Propulsion System Sizing

## Problem Statement

Pressure-fed system versus pump-fed system, and produces quantitative outputs that compare both options. Explore the sensitivity with respect to a parameter that you select (e.g. Isp, but since we are giving you this example, please use a different parameter).

Assume the following fixed top-level constraints:
- **Common for both architectures:**
    - Required delta-V: 2,000 m/s
    - Dry mass without including propulsion dry mass: 600 kg.
    - Maximum initial mass: 1,500 kg.
    - Required thrust-to-weight ratio at ignition: >= 1.5
    - Propellant density: 1,000 kg/m3 (assume single fluid for simplicity)
    - Propellant tank mass is proportional to tank's pressure and propellant mass. Justify proportionality factor with a simple model.
- **Pressure-fed system:**
    - Pressurant system mass is proportional to tank's pressure and to propellant mass, with a factor of 0.002 /bar
    - Propellant tank pressure: 25 bar
    - Engine inlet pressure: 20 bar
    - Isp: 310 s
- **Pump-fed system:**
    - Assume that pump mass scales linearly with thrust, with a factor of 0.008 kg/N
    - Propellant tank pressure: 10 bar
    - Engine inlet pressure: 40 bar
    - Isp: 330 s

For each architecture, compute total required propellant mass, and system margin against requirement. Explore the sensitivity with respect to a parameter that you select (e.g. Isp, but since we are giving you this example, please use a different parameter),


## Setting up

### Requirements:
Ensure the following are installed:
- `python 3.10`
- `uv`

### Quick Start

## Directory Structure

```text
ispc-intrvw-prop-sizing
├── docs/
├── src/
│   ├── configs/                # study configurations
│   ├── constants/              # default factors, asset paths, universal constants
│   ├── database/               # database: materials, propellants etc ...
│   ├── propulsion_module/      # propulsion module
│   │   ├── models/             # data calasses
│   │   └── solver/             # data calasses
│   ├── utils/                  # utility modules
│   └── main.py                 
└── tests/
    └── unit/
```
