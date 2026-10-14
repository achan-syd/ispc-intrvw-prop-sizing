# Result Summary

## Problem Statement
Size a lunar descent propulsion system two ways, pressure-fed and pump-fed, and compare propellant mass and margin. Then sweep one parameter (not Isp) to show its sensitivity.

**Specifations**
- Delta-V: 2,000 m/s
- Dry mass, excluding propulsion: 600 kg
- Maximum initial mass: 1,500 kg
- Thrust-to-weight at ignition: >= 1.5
- Propellant density: 1,000 kg/m3, single fluid
- Tank mass: proportional to tank pressure and propellant mass

**Case 1: Pressure-fed**
- Tank pressure: 25 bar
- Engine inlet pressure: 20 bar
- Isp: 310 s
- Pressurant mass: 0.002 /bar x tank pressure x propellant mass

**Case 2: Pump-fed**
- Tank pressure: 10 bar
- Engine inlet pressure: 40 bar
- Isp: 330 s
- Pump mass: 0.008 kg/N x thrust

**Outputs**
- Required propellant mass for each case
- Margin against the requirement for each case
- Sensitivity of both cases to one chosen parameter

## Comparison Results Results

**Inputs:**
| Requirement | Value |
|---|---:|
| Delta-V [m/s] | 2000.0 |
| Thrust-to-weight [-] | 1.50 |
| Dry mass [kg] | 600.0 |
| Maximum mass [kg] | 1500.0 |


**Outputs:**

| | Case 1: Pressure-fed | Case 2: Pump-fed |
|---|---:|---:|
| Propellant mass [kg] | 619.16 | 542.97 |
| Propulsion system mass [kg] | 65.26 | 34.88 |
| Dry mass [kg] | 665.26 | 634.88 |
| Total mass [kg] | 1284.42 | 1177.85 |
| Thrust [N] | 3121.1 | 2862.2 |
| Margin [%] | 14.4 | 21.5 |

## Sensitivity Analysis

**Inputs:**
| Requirement | Value |
|---|---:|
| Delta-V [m/s] | 2000.0 |
| Thrust-to-weight [-] | 1.50 |
| Dry mass [kg] | 600.0 |
| Maximum mass [kg] | 1500.0 |

**Outputs:**

![Sensitivity study results](sensitivity_study_results.png)
