# ImmunoSys

Project Repository for the ImmunoSys math modeling research group.

**Goal:** Create an "AlphaFold for the immune system" - a comprehensive framework for modeling immunological dynamics, starting with alopecia areata but extensible to any immunological system.

## Features

- 🧬 **Flexible Mathematical Modeling Framework**: Base classes for differential equation models
- 📊 **Publication-Ready Visualizations**: Comprehensive plotting tools for 2D, 3D, phase planes, heatmaps, and networks
- 🔧 **Utility Functions**: Helper functions for equilibrium analysis, stability analysis, parameter sensitivity, and more
- 📚 **Example Notebooks**: Demonstrations of all visualization capabilities
- 🐍 **Modern Python Stack**: Built with NumPy, SciPy, Matplotlib, and scientific Python ecosystem

## Installation

### Quick Start with Conda

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Reinald0-M/ImmunoSys.git
   cd ImmunoSys
   ```

2. **Create the conda environment:**
   ```bash
   conda env create -f environment.yml
   ```

3. **Activate the environment:**
   ```bash
   conda activate immunosys-env
   ```

4. **Install the package in development mode:**
   ```bash
   pip install -e .
   ```

### Environment Details

The `environment.yml` file includes:
- **Core Scientific Computing**: NumPy, SciPy, SymPy
- **Data Analysis**: Pandas
- **Visualization**: Matplotlib, Seaborn, Plotly, Mayavi, PyVista
- **Modeling Tools**: scikit-learn, NetworkX
- **Development Tools**: Jupyter, pytest, black, flake8, mypy
- **Documentation**: Sphinx

All dependencies use flexible version specifiers (>=) to ensure compatibility and allow for updates.

## Project Structure

```
ImmunoSys/
├── immunosys/              # Main package
│   ├── models/             # Mathematical models
│   │   └── base.py         # Base model class
│   ├── visualization/      # Publication-ready plotting
│   │   └── plots.py        # Plotting classes
│   ├── utils/              # Utility functions
│   │   └── helpers.py      # Helper functions
│   └── data/               # Data storage
├── examples/               # Example notebooks
│   └── visualization_examples.ipynb
├── tests/                  # Unit tests
├── docs/                   # Documentation
├── environment.yml         # Conda environment specification
└── README.md              # This file
```

## Quick Start Guide

### 1. Using Visualization Tools

```python
from immunosys.visualization import TimeSeries2D, PhasePlane2D, Plot3D

# Create publication-ready time series plot
plotter = TimeSeries2D(style='science')
fig, ax = plotter.plot(
    time_data,
    population_data,
    labels=['T Cells', 'B Cells', 'NK Cells'],
    xlabel='Time (days)',
    ylabel='Cell Population'
)

# Save in multiple formats
plotter.save_figure(fig, 'my_results', formats=['png', 'pdf', 'svg'])
```

### 2. Building Mathematical Models

```python
from immunosys.models import BaseModel
import numpy as np

class MyImmuneModel(BaseModel):
    def equations(self, state, t):
        # Define your system of ODEs
        x, y = state
        dxdt = x * (1 - y)
        dydt = -y * (1 - x)
        return np.array([dxdt, dydt])

# Simulate the model
model = MyImmuneModel(parameters={'alpha': 0.1, 'beta': 0.2})
time, solution = model.simulate(
    initial_conditions=np.array([1.0, 0.5]),
    time_span=(0, 100),
    num_points=1000
)
```

### 3. Using Utility Functions

```python
from immunosys.utils import (
    find_equilibria,
    analyze_stability,
    parameter_sensitivity,
    detect_oscillations
)

# Find equilibrium points
equilibria = find_equilibria(model.equations, initial_guesses=[...])

# Analyze stability
jacobian = compute_jacobian(model.equations, equilibria[0])
stability_info = analyze_stability(jacobian)

# Detect oscillations in data
oscillation_info = detect_oscillations(time, solution[:, 0])
```

## Visualization Classes

### Available Plotters

1. **TimeSeries2D**: Time series plots for dynamic simulations
2. **PhasePlane2D**: Phase plane diagrams with trajectories and vector fields
3. **Plot3D**: 3D trajectory and surface plots
4. **Heatmap**: Heatmaps for spatial patterns and parameter sensitivity
5. **NetworkViz**: Network diagrams for cell-cell interactions

All plotters support:
- Multiple publication styles (default, nature, science)
- Automatic formatting for publication quality
- Export to multiple formats (PNG, PDF, SVG, EPS)
- Customizable colors, labels, and styling

### Example Gallery

See `examples/visualization_examples.ipynb` for a complete gallery of visualization examples.

## Development Tools

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black immunosys/
flake8 immunosys/
```

### Type Checking

```bash
mypy immunosys/
```

## Contributing

This is a research project. To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and ensure code quality
5. Submit a pull request

## Roadmap

- [x] Set up project structure
- [x] Create conda environment with flexible dependencies
- [x] Implement publication-ready visualization classes
- [x] Add utility functions for modeling
- [ ] Implement specific models for alopecia areata
- [ ] Add parameter estimation tools
- [ ] Implement bifurcation analysis
- [ ] Add spatial modeling capabilities
- [ ] Create comprehensive documentation
- [ ] Add more example notebooks

## Citation

If you use this framework in your research, please cite:

```bibtex
@software{immunosys2024,
  title={ImmunoSys: A Mathematical Modeling Framework for Immunological Dynamics},
  author={ImmunoSys Research Group},
  year={2024},
  url={https://github.com/Reinald0-M/ImmunoSys}
}
```

## License

[Add your license here]

## Contact

For questions or collaborations, please open an issue on GitHub.

---

**Note**: This framework is under active development. APIs may change as we refine the tools based on research needs.
