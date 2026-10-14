# Tutorial

Three options are provided:
- sizing: size one design
- comparison: size several designs side by side
- sensitivity study: sweep one parameter for every design

Run every command from the repo root. Use `python3` with the project environment active (Python 3.10 or newer), or `uv`.

The shared requirements sit in `src/configs/specification.json`:
```json
{
    "requirements": {
        "delta_v": 2000,        # m/s
        "twr": 1.5,             # thrust-to-weight at ignition [-]
        "dry_mass": 600,        # kg, allocated mass without propulsion
        "maximum_mass": 1500    # kg, the margin is measured against this
    }
}
```

# Sizing
Store one file per design in `src/configs/sizing_study/<design>.json`.
```json
{
    "propulsion_module": {
        "name": "Design 1: Pressure Fed",    # only printed
        "id": "001",                         # only printed
        "architecture": "pressure_fed",      # pressure_fed or pump_fed
        "tank": {
            "propellant": "Hydrazine",       # name in database/propellant.csv
            "material": "Aluminium",         # name in database/material.csv
            "pressure": [25, "bar"]          # [value, unit], a bare number is SI
        },                                   # add "radius" or "length" for a cylinder, else a sphere
        "engine": {
            "isp": 310,                      # s
            "inlet_pressure": [20, "bar"],
            "mass_factor": [0.2, "kg/bar"]   # engine mass per inlet pressure
        },
        "pressurant": {                      # pump_fed uses "pump" with [0.008, "kg/N"]
            "mass_factor": [0.002, "1/bar"]
        }
    }
}
```

Config File: [pressure_fed.json](../src/configs/sizing_study/pressure_fed.json)
```bash
# python3 -m src.main size <design>
python3 -m src.main size pressure_fed
# uv run main size <design>
uv run main size pressure_fed
```
`<design>` is the file name without `.json`.

# Comparison
Store one file per study in `src/configs/comparative_study/<study>.json`. Each case is a design as above. Add as many cases as you like.
```json
{
    "cases": [
        {
            "case": 1,                       # case number
            "propulsion_module": { ... }     # same as the sizing design
        },
        {
            "case": 2,
            "propulsion_module": { ... }
        }
    ]
}
```

Config File: [pressure_vs_pump.json](../src/configs/comparative_study/pressure_vs_pump.json)
```bash
# python3 -m src.main compare <study>
python3 -m src.main compare pressure_vs_pump
# uv run main compare <study>
uv run main compare pressure_vs_pump
```
`<study>` is the file name without `.json`.

# Sensitivity Study
Store one file per study in `src/configs/sensitivity_study/<study>.json`. It holds the requirements, the cases, and the swept range.
```json
{
    "PARAM": [1000, 100, 3000],    # swept range as [start, interval, stop]
    "requirements": {
        "delta_v": "PARAM",        # swept, replaced by each value of PARAM
        "twr": 1.5,                # fixed
        "dry_mass": 600,
        "maximum_mass": 1500
    },
    "cases": [ ... ]               # same as the comparison
}
```

Config File: [sweep_config.json](../src/configs/sensitivity_study/sweep_config.json)
```bash
# python3 -m src.main sweep <study>
python3 -m src.main sweep sweep_config
# uv run main sweep <study>
uv run main sweep sweep_config
```
`<study>` is the file name without `.json`.

Using `PARAM`:
- Write `"PARAM"` where the swept value goes, in the requirements or in any case, for example `"isp": "PARAM"`.
- To sweep a value that has a unit write `["PARAM", "bar"]`. The range is then in that unit.
- Put it in every place that should move together. It is not checked.
- The plot is labelled with the name of the key that holds it.
