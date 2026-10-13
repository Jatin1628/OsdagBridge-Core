# OsdagBridge Core (`osdagbridge-core`)

[![Python Version](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![License: LGPL v3](https://img.shields.io/badge/License-LGPL_v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)
[![Code style](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)

**OsdagBridge Core** is the headless computational, structural analysis, and design engine for steel bridges developed under the [Osdag](https://osdag.fossee.in/) initiative at IIT Bombay.

It serves as the backend computation layer for **OsdagBridge Desktop** (GUI), CLI utilities, and future web/cloud applications, providing standard-compliant bridge modeling, finite element grillage analysis, structural capacity evaluations, report generation, and BIM export.

---

## Key Features

- **Standard-Compliant Structural Design:**
  - **IRC:5-2015:** General features of design (carriageway widths, footpath, clearances, and layouts).
  - **IRC:6-2017:** Loads and load combinations (IRC Class 70R, Class A, Class B, 70R Bogie, Special Vehicles, wind, seismic, and fatigue loading).
  - **IRC:22-2015 / IS 800:2007:** Steel bridge superstructure and plate girder design (bending, shear, lateral torsional buckling, web buckling, stiffeners, and splices).
  - **IRC:112-2019 / IRC:22:** Reinforced concrete deck slab design (transverse bending, punching shear, and reinforcement layout).

- **Grillage & Finite Element Analysis:**
  - Automated 2D/3D grillage model generation powered by [OpenSeesPy](https://opensees.berkeley.edu/) and [ospgrillage](https://ospgrillage.readthedocs.io/).
  - Longitudinal and transverse load distribution.
  - Moving load analysis with influence lines and critical load placement envelopes.
  - Live load and dead load demand envelope generation (ULS and SLS combinations).

- **Comprehensive Component Sizing & Checks:**
  - **Plate Girders:** Initial sizing, cross-section classification, moment/shear resistance, serviceability deflection, and camber.
  - **Stiffeners:** Intermediate transverse stiffeners, bearing/support stiffeners, longitudinal stiffeners.
  - **Cross Bracings & Diaphragms:** Intermediate cross bracings, end diaphragms, forces and member design.
  - **Shear Connectors:** Headed stud shear connectors, pitch, and spacing calculation.
  - **Bearings & Sub-components:** Crash barriers, median barriers, railings, and footpaths.

- **Automated Design Reports & Quantities:**
  - **Report Generation:** Production-ready LaTeX and PDF design reports covering Executive Summary, Input Schedules, Load Calculations, Analysis Results, Design Checks, and Code Verification.
  - **Bill of Quantities (BOQ):** Automated material take-off for structural steel, concrete, reinforcement, shear studs, and wearing coat.

- **BIM / IFC Interoperability:**
  - IFC export of 3D bridge geometry according to openBIM standards for downstream CAD/BIM workflows.

- **Decoupled Headless Architecture:**
  - Pure Python computation engine free of GUI dependencies.
  - Easily integrated into desktop applications (`osdagbridge_desktop`), CLI scripts, or REST API microservices.

---

## Directory Structure

```text
OsdagBridge-Core/
├── conda-recipe/             # Conda packaging recipe and build scripts
├── examples/                 # Verification and example YAML input decks
├── src/
│   └── osdagbridge_core/     # Main package namespace
│       ├── cli/              # CLI entry point and subcommands
│       └── core/             # Core engineering & computation engine
│           ├── boq/          # Bill of Quantities generator
│           ├── bridge_components/ # Superstructure builders (deck, girder, bracing, etc.)
│           ├── bridge_types/ # Bridge domain modules (plate_girder, truss, etc.)
│           ├── data/         # Material databases and GIS location shapefiles
│           ├── ifc_export_bridge/ # IFC / BIM export utilities
│           ├── loads/        # IRC vehicle models and load placement engines
│           ├── reports/      # LaTeX report generation chapters and utilities
│           ├── solvers/      # OpenSeesPy and grillage solver adapters
│           └── utils/        # Code standards (IRC/IS), units, and common helpers
├── tests/
│   ├── integration/          # End-to-end integration tests
│   └── unit/                 # Unit tests for core calculation routines
├── environment.yaml          # Conda development environment specification
└── pyproject.toml            # Build system metadata and dependencies (PEP 517/518/621)
```

---

## Installation

### Prerequisites
- Python **3.11** or **3.12**
- [Conda](https://docs.conda.io/en/latest/) (recommended) or `pip`

### Option 1: Using Conda (Recommended)

Create and activate the environment using the provided specification:

```bash
# Clone the repository
git clone https://github.com/osdagbridge/OsdagBridge-Core.git
cd OsdagBridge-Core

# Create the conda environment
conda env create -f environment.yaml

# Activate the environment
conda activate osdagbridge-core
```

### Option 2: Using `pip`

In an existing virtual environment:

```bash
# Install package in editable development mode
pip install -e .

# With optional testing dependencies
pip install -e ".[test]"
```

---

## Usage

### Command Line Interface (CLI)

The package provides the `osdagbridge-cli` command:

```bash
osdagbridge-cli --help
```

### Python API

Import modules from `osdagbridge_core.core` directly in your scripts or applications:

```python
from osdagbridge_core.core.bridge_types.plate_girder.defaults import BASIC_INPUT_DICT
from osdagbridge_core.core.utils.codes.irc6_2017 import IRC6_2017
from osdagbridge_core.core.utils.codes.irc5_2015 import IRC5_2015

# Query IRC:6 vehicle parameters
class_70r = IRC6_2017.cl_204_track_vehicle()
print("IRC Class 70R Tracked Vehicle:", class_70r)

# Access design defaults
print("Carriageway width:", BASIC_INPUT_DICT.get("Carriageway Width"))
```

---

## Running Tests

Execute the test suite using `pytest`:

```bash
pytest
```

---

## License

This project is licensed under the **GNU Lesser General Public License v3.0 (LGPLv3)**.  
See the [LICENSE](LICENSE) file for the complete license terms.

---

## Acknowledgments

- **[Osdag Project](https://osdag.fossee.in/):** Open Source Design of Steel Structures initiative developed at IIT Bombay, funded by the National Mission on Education through ICT (NMEICT), Ministry of Education, Government of India.
- **[OpenSees / OpenSeesPy](https://opensees.berkeley.edu/):** Open System for Earthquake Engineering Simulation.
- **[ospgrillage](https://ospgrillage.readthedocs.io/):** OpenSees-based bridge deck grillage analysis framework.