# Rescue Application Project

This project provides a simulation and analysis tool for rescue operations. It allows users to:

1. Define rescue stations with coordinates and speeds
2. Run simulations to calculate optimal rescue paths
3. Visualize rescue coverage and response times
4. Calculate rescue probability metrics

## Dependencies

- Python 3.8+
- PyQt6 for the frontend
- NumPy, Matplotlib, NetworkX, and other scientific libraries

## Project Structure

- `run.py`: Main application entry point
- `projectFunctions.py`: Original implementation of core rescue functions
- `rescue_app/`: Main package
  - `app.py`: Application initialization
  - `core/`: Core simulation components
    - `experiment.py`: Experiment class for running simulations
  - `models/`: Data models
    - `station.py`: Station class definitions
  - `ui/`: User interface components
    - `main_window.py`: Main application window
    - `dialogs.py`: Dialog windows for adding and selecting stations
    - `models.py`: UI data models
  - `utils/`: Utility functions
    - `coordinates.py`: Coordinate conversion utilities
    - `project_functions.py`: Modernized version of rescue calculation functions
  - `config/`: Configuration settings
    - `__init__.py`: Default stations and configuration values

## Quick Start

For first-time users, see the [QUICKSTART.md](QUICKSTART.md) guide with simple setup instructions.

## Usage

To run the application:

```bash
python run.py
```

Or use the provided launcher scripts:
```
# Windows
run_program.bat

# Linux/macOS
./run_program.sh
```

Both launcher scripts automatically:
- Create a Python virtual environment
- Install all required dependencies
- Launch the application

## Installation

See the detailed installation instructions in `README-INSTALL.md`.

## Development Notes

The project currently uses both `projectFunctions.py` in the root directory and `rescue_app/utils/project_functions.py` for backward compatibility. The core experiment module imports from the original `projectFunctions.py` file.

When extending the application, follow these patterns:
- Add new rescue station types in the `models` package
- Add new visualization methods to the plotting functions
- Extend experimental parameters in the `Experiment` class
