# Getting Started with ImmunoSys

## What is ImmunoSys?

ImmunoSys is a comprehensive mathematical modeling framework designed specifically for immunological dynamics. The goal is to create an "AlphaFold for the immune system" - a powerful, flexible toolkit that makes it easy to model, simulate, and visualize complex immunological phenomena.

## Who is it for?

- **Immunologists** looking to model immune system dynamics
- **Mathematical biologists** studying biological systems
- **Researchers** working on alopecia areata or other immune-related conditions
- **Students** learning about dynamical systems and immunology
- **Data scientists** analyzing immunological data

## Key Features

### 🧬 Mathematical Modeling
- Abstract base classes for easy model development
- Built-in ODE solvers (odeint, solve_ivp)
- Equilibrium finding and stability analysis
- Parameter sensitivity analysis

### 📊 Publication-Ready Visualizations
- Time series plots
- Phase plane diagrams with vector fields
- 3D trajectory and surface plots
- Heatmaps for spatial patterns
- Network visualizations for cell interactions
- Multiple export formats (PNG, PDF, SVG, EPS)

### 🔧 Utility Functions
- Data normalization
- Numerical derivatives
- Oscillation detection
- Lyapunov exponent estimation
- File I/O for results

## Quick Start

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Reinald0-M/ImmunoSys.git
   cd ImmunoSys
   ```

2. **Create conda environment:**
   ```bash
   conda env create -f environment.yml
   conda activate immunosys-env
   ```

3. **Install package:**
   ```bash
   pip install -e .
   ```

### Your First Model

Let's create a simple immune cell model:

```python
import numpy as np
from immunosys.models import BaseModel
from immunosys.visualization import TimeSeries2D

class SimpleImmuneModel(BaseModel):
    """Simple model of T cell activation."""
    
    def equations(self, state, t):
        naive, activated = state
        
        # Parameters
        activation_rate = self.parameters['alpha']
        decay_rate = self.parameters['beta']
        
        # Equations
        dnaive_dt = -activation_rate * naive
        dactivated_dt = activation_rate * naive - decay_rate * activated
        
        return np.array([dnaive_dt, dactivated_dt])

# Create and simulate model
model = SimpleImmuneModel({'alpha': 0.1, 'beta': 0.05})
time, solution = model.simulate(
    initial_conditions=np.array([100.0, 0.0]),
    time_span=(0, 50)
)

# Visualize results
plotter = TimeSeries2D()
fig, ax = plotter.plot(
    time, solution,
    labels=['Naive T Cells', 'Activated T Cells'],
    xlabel='Time (hours)',
    ylabel='Cell Count'
)
```

### Creating Beautiful Plots

```python
from immunosys.visualization import (
    TimeSeries2D,
    PhasePlane2D,
    Heatmap
)

# Time series with publication styling
plotter = TimeSeries2D(style='nature')
fig, ax = plotter.plot(time, data, labels=['Cell Type 1', 'Cell Type 2'])
plotter.save_figure(fig, 'my_figure', formats=['png', 'pdf'])

# Phase plane
phase_plotter = PhasePlane2D(style='science')
fig, ax = phase_plotter.plot(
    x_data, y_data,
    show_direction=True,
    color_by_time=True
)

# Heatmap
heatmap_plotter = Heatmap()
fig, ax = heatmap_plotter.plot(
    data_matrix,
    cmap='RdYlBu_r',
    cbar_label='Concentration'
)
```

### Using Utility Functions

```python
from immunosys.utils import (
    find_equilibria,
    analyze_stability,
    detect_oscillations,
    parameter_sensitivity
)

# Find equilibria
equilibria = find_equilibria(model.equations, initial_guesses)

# Analyze stability
from immunosys.utils import compute_jacobian
jacobian = compute_jacobian(model.equations, equilibria[0])
stability = analyze_stability(jacobian)
print(f"Stability: {stability['stability']}")

# Detect oscillations
osc_info = detect_oscillations(time, solution[:, 0])
if osc_info['oscillatory']:
    print(f"Period: {osc_info['period']:.2f}")
```

## Examples

The `examples/` directory contains:
- `visualization_examples.ipynb`: Complete gallery of all visualization types
- `simple_model_example.py`: Example of T cell-target cell dynamics

Run the example:
```bash
cd examples
python simple_model_example.py
```

Or explore the Jupyter notebook:
```bash
jupyter notebook visualization_examples.ipynb
```

## Next Steps

1. **Read the [API Reference](API.md)** for detailed documentation
2. **Explore the examples** to see what's possible
3. **Build your own models** starting from `BaseModel`
4. **Customize visualizations** for your specific needs
5. **Contribute** your models and visualizations back to the project

## Common Workflows

### Workflow 1: Model Development
1. Create a class inheriting from `BaseModel`
2. Implement the `equations()` method
3. Simulate with different parameters
4. Visualize results with appropriate plotters
5. Analyze equilibria and stability

### Workflow 2: Parameter Exploration
1. Define your model and base parameters
2. Use `parameter_sensitivity()` to find important parameters
3. Visualize sensitivity with `Heatmap.plot_sensitivity()`
4. Run simulations across parameter ranges
5. Create publication-ready figures

### Workflow 3: Data Analysis
1. Load experimental data
2. Normalize with `normalize_data()`
3. Detect features (oscillations, peaks, etc.)
4. Compare with model predictions
5. Visualize comparisons

## Tips and Tricks

- **Use flexible version specifiers**: All dependencies use `>=` to allow updates
- **Save in multiple formats**: Use `save_figure()` to export PNG, PDF, and SVG
- **Vectorize operations**: Use NumPy arrays for better performance
- **Test your models**: Write tests in the `tests/` directory
- **Document your work**: Add docstrings following NumPy style

## Getting Help

- Check the [API Reference](API.md) for detailed documentation
- Look at examples in `examples/`
- Open an issue on GitHub for bugs or questions
- Read [CONTRIBUTING.md](../CONTRIBUTING.md) to contribute

## What's Next?

The framework is designed to be extensible. Future additions might include:
- Stochastic differential equations
- Spatial models (PDEs)
- Agent-based modeling components
- Machine learning integration
- More specialized immunology models
- Automatic bifurcation analysis
- Parameter estimation from data

Stay tuned for updates!
