# ImmunoSys API Reference

## Visualization Module

### PublicationPlotter

Base class for all publication-ready plots. Sets up matplotlib with publication-quality defaults.

```python
from immunosys.visualization import PublicationPlotter

plotter = PublicationPlotter(style='science')
```

**Parameters:**
- `style` (str): Style preset ('default', 'nature', 'science', 'minimal')

**Methods:**
- `save_figure(fig, filename, formats=['png', 'pdf'], **kwargs)`: Save figure in multiple formats

---

### TimeSeries2D

Create publication-ready 2D time series plots for dynamic simulations.

```python
from immunosys.visualization import TimeSeries2D

plotter = TimeSeries2D(style='nature')
fig, ax = plotter.plot(time, data, labels=['T Cells', 'B Cells'])
```

**Methods:**
- `plot(time, data, labels=None, xlabel='Time', ylabel='Population', ...)`: Create time series plot

---

### PhasePlane2D

Create 2D phase plane diagrams with trajectories and nullclines.

```python
from immunosys.visualization import PhasePlane2D

plotter = PhasePlane2D()
fig, ax = plotter.plot(x_data, y_data, show_direction=True)
```

**Methods:**
- `plot(x_data, y_data, ...)`: Create phase plane plot
- `plot_vector_field(x_range, y_range, dx_func, dy_func, ...)`: Plot vector field

---

### Plot3D

Create publication-ready 3D plots for trajectories and surfaces.

```python
from immunosys.visualization import Plot3D

plotter = Plot3D()
fig, ax = plotter.plot_trajectory(x, y, z)
```

**Methods:**
- `plot_trajectory(x, y, z, ...)`: Plot 3D trajectory
- `plot_surface(X, Y, Z, ...)`: Plot 3D surface

---

### Heatmap

Create publication-ready heatmaps for parameter sensitivity and spatial patterns.

```python
from immunosys.visualization import Heatmap

plotter = Heatmap()
fig, ax = plotter.plot(data, cmap='RdYlBu_r')
```

**Methods:**
- `plot(data, ...)`: Create heatmap
- `plot_sensitivity(parameters, outputs, sensitivity_matrix, ...)`: Create parameter sensitivity heatmap

---

### NetworkViz

Visualize cell-cell interaction networks and regulatory networks.

```python
from immunosys.visualization import NetworkViz

plotter = NetworkViz()
fig, ax = plotter.plot_network(adjacency_matrix, node_labels=labels)
```

**Methods:**
- `plot_network(adjacency_matrix, node_labels=None, ...)`: Plot network from adjacency matrix

---

## Models Module

### BaseModel

Abstract base class for immunological mathematical models.

```python
from immunosys.models import BaseModel

class MyModel(BaseModel):
    def equations(self, state, t):
        # Define your ODEs here
        pass

model = MyModel(parameters={'alpha': 0.1})
time, solution = model.simulate(initial_conditions, (0, 100))
```

**Methods:**
- `equations(state, t)`: Define system of differential equations (must be implemented)
- `simulate(initial_conditions, time_span, num_points=1000, method='odeint')`: Simulate the model
- `get_equilibria()`: Find equilibrium points (to be implemented in subclass)
- `stability_analysis(equilibrium)`: Perform linear stability analysis (to be implemented in subclass)

---

## Utils Module

### Data Normalization

```python
from immunosys.utils import normalize_data

normalized, params = normalize_data(data, method='minmax')
```

**Methods:**
- `minmax`: Min-max normalization to [0, 1]
- `zscore`: Z-score normalization
- `robust`: Robust normalization using median and IQR

---

### Derivatives

```python
from immunosys.utils import compute_derivative

derivative = compute_derivative(time, data, method='finite_diff')
```

---

### Equilibrium Analysis

```python
from immunosys.utils import find_equilibria, compute_jacobian, analyze_stability

equilibria = find_equilibria(equations, initial_guesses)
jacobian = compute_jacobian(equations, equilibrium)
stability_info = analyze_stability(jacobian)
```

---

### Oscillation Detection

```python
from immunosys.utils import detect_oscillations

osc_info = detect_oscillations(time, data, prominence=0.1)
```

Returns dictionary with:
- `oscillatory`: bool
- `period`: float (if oscillatory)
- `amplitude`: float (if oscillatory)
- `frequency`: float (if oscillatory)

---

### Parameter Sensitivity

```python
from immunosys.utils import parameter_sensitivity

sensitivity = parameter_sensitivity(
    model_func,
    base_parameters,
    parameter_ranges,
    output_func,
    num_samples=100
)
```

---

### File I/O

```python
from immunosys.utils import save_results, load_results

save_results('output.npz', {'time': time, 'solution': solution})
data = load_results('output.npz')
```

Supports `.npz` and `.csv` formats.
