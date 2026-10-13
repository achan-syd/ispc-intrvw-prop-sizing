# Overview

## Directory Structure
```text
ispc-intrvw-prop-sizing
├── docs/                       # Documentation 
├── src/                        # Source Code          
└── tests/                      # Test Cases
```

## Architecture
```text
src
├── configs/                    # JSON Config files
│   ├── comparative_study/          # Cases sized side by side
│   ├── sensitivity_study/          # Parameter sweeps
│   └── sizing_study/               # Single designs
├── constants/                  # Default factors, asset paths, universal constants
├── database/                   # Material and propellant tables
├── propulsion_module/          # Propulsion Module
│   ├── models/                 # Data classes
│   │   ├── architectures/      
│   │   ├── components/         
│   │   │   └── tanks/          
│   │   ├── materials/          
│   │   └── propellants/        
│   ├── sizing/                 # Single Propulsion module solution logic
│   └── solvers/                # Equaqtion solvers
├── studies/                    # sizing, compariosn and sensitivity loic
├── utils/                      # Unit conversion
└── main.py/                    # Entry Point
```

## Components
```mermaid
flowchart TB
    main["main.py"]
    config["config"]

    subgraph studies["studies"]
        size["size"]
        compare["compare"]
        sensitivity["sensitivity analysis"]
    end

    subgraph module["propulsion module"]
        sizing["sizing"]
        subgraph models["models"]
            architectures["architectures"]
            components["components"]
        end
        solvers["solvers"]
    end

    subgraph database["database"]
        material["material database"]
        propellant["propellant database"]
    end

    main -- calls --> size
    main -- calls --> compare
    main -- calls --> sensitivity
    size -- calls --> module
    compare -- calls --> module
    sensitivity -- calls --> module
    sizing -- resolves --> models
    sizing -- uses --> solvers
    models -- uses --> database
    models -- loads from --> config

    classDef entry fill:#f5f5f5,stroke:#666666,color:#333333
    classDef study fill:#dae8fc,stroke:#6c8ebf,color:#333333
    classDef core fill:#d5e8d4,stroke:#82b366,color:#333333
    classDef data fill:#ffe6cc,stroke:#d79b00,color:#333333
    classDef file fill:#fff2cc,stroke:#d6b656,color:#333333

    class main entry
    class size,compare,sensitivity study
    class sizing,solvers,architectures,components core
    class material,propellant data
    class config file

    style studies fill:#ffffff,stroke:#6c8ebf,color:#333333,stroke-dasharray:5 5
    style module fill:#ffffff,stroke:#82b366,color:#333333,stroke-dasharray:5 5
    style models fill:#ffffff,stroke:#82b366,color:#333333,stroke-dasharray:5 5
    style database fill:#ffffff,stroke:#d79b00,color:#333333,stroke-dasharray:5 5
```

## Models
```mermaid
classDiagram
    class PropulsionSystem {
        +list~PropellantTank~ propellant_tanks
        +list~FeedSystem~ feed_systems
        +list~Engine~ engines
        +float mass
    }
    class PressureFedSystem {
        +list~PressurantSystem~ feed_systems
        +from_config(config)
        +size(prop_mass, thrust)
    }
    class PumpFedSystem {
        +list~PumpSystem~ feed_systems
        +from_config(config)
        +size(prop_mass, thrust)
    }

    class PropellantTank {
        +float max_pressure
        +Material material
        +float fos
        +float ullage
        +Propellant propellant
        +float volume
        +float thickness
        +float mass
    }
    class SphericalTank {
        +float radius
        +from_config(config)
    }
    class CylindricalTank {
        +float radius
        +float length
        +from_config(config)
    }

    class FeedSystem {
        +float mass
    }
    class PressurantSystem {
        +float mass_factor
        +from_config(config)
        +size(pressure, propellant_mass)
    }
    class PumpSystem {
        +float mass_factor
        +from_config(config)
        +size(thrust)
    }

    class Engine {
        +float isp
        +float inlet_pressure
        +float mass
        +from_config(config)
    }
    class Material {
        +str name
        +float density
        +float yield_strength
        +float ultimate_strength
        +from_database(name)
    }
    class Propellant {
        +str name
        +float density
        +from_database(name)
    }

    PropellantTank <|-- SphericalTank
    PropellantTank <|-- CylindricalTank
    FeedSystem <|-- PressurantSystem
    FeedSystem <|-- PumpSystem

    PropulsionSystem <|-- PressureFedSystem
    PropulsionSystem <|-- PumpFedSystem

    PropulsionSystem "1" *-- "1..*" PropellantTank : propellant_tanks
    PropulsionSystem "1" *-- "1..*" FeedSystem : feed_systems
    PropulsionSystem "1" *-- "1..*" Engine : engines

    PropellantTank --> Material : material
    PropellantTank --> Propellant : propellant
```
