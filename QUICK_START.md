# 🚀 Quick Start Guide

Welcome to ImmunoSys! This guide will get you up and running in 5 minutes.

## ⚡ Installation (2 minutes)

```bash
# 1. Clone the repository
git clone https://github.com/Reinald0-M/ImmunoSys.git
cd ImmunoSys

# 2. Create environment (takes ~2 minutes)
conda env create -f environment.yml
conda activate immunosys-env

# 3. Install package
pip install -e .
```

## 🎯 Your First Model (3 minutes)

Create a file called `my_first_model.py`:

```python
import numpy as np
from immunosys.models import BaseModel
from immunosys.visualization import TimeSeries2D, PhasePlane2D

# Define a simple immune model
class SimpleImmuneModel(BaseModel):
    """Model of T cells attacking target cells."""
    
    def equations(self, state, t):
        T, C = state  # Target cells, Cytotoxic T cells
        
        r = 0.5    # Target growth rate
        K = 100    # Carrying capacity
        a = 0.01   # Attack rate
        b = 0.005  # T cell proliferation
        d = 0.2    # T cell death
        
        dT_dt = r * T * (1 - T/K) - a * T * C
        dC_dt = b * T * C - d * C
        
        return np.array([dT_dt, dC_dt])

# Create and simulate
model = SimpleImmuneModel({})
time, solution = model.simulate(
    initial_conditions=np.array([80.0, 30.0]),
    time_span=(0, 200)
)

# Visualize time series
plotter = TimeSeries2D(style='science')
fig, ax = plotter.plot(
    time, solution,
    labels=['Target Cells', 'T Cells'],
    xlabel='Time (days)',
    ylabel='Cell Count',
    colors=['#d62728', '#1f77b4']
)

# Save figure
plotter.save_figure(fig, 'my_results', formats=['png', 'pdf'])

# Visualize phase plane
phase = PhasePlane2D()
fig2, ax2 = phase.plot(
    solution[:, 0], solution[:, 1],
    xlabel='Target Cells',
    ylabel='T Cells',
    color_by_time=True
)

import matplotlib.pyplot as plt
plt.show()
```

Run it:
```bash
python my_first_model.py
```

## 📊 Explore Examples

```bash
# Run interactive example
cd examples
python simple_model_example.py

# Or open Jupyter notebook
jupyter notebook visualization_examples.ipynb
```

## 🧪 Run Tests

```bash
pytest tests/ -v
```

## 📚 Learn More

- **[README.md](README.md)** - Complete overview and features
- **[docs/getting_started.md](docs/getting_started.md)** - Detailed tutorial
- **[docs/API.md](docs/API.md)** - Full API reference
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute

## �� Visualization Gallery

The framework provides these publication-ready plots:

1. **Time Series** - Track cell populations over time
2. **Phase Planes** - Visualize system dynamics in 2D
3. **3D Trajectories** - Explore 3D state spaces
4. **Heatmaps** - Show spatial patterns and parameter sensitivity
5. **Networks** - Display cell-cell interactions

All support:
- Multiple styles (default, nature, science)
- Export to PNG, PDF, SVG, EPS
- Customizable colors, labels, and formatting

## 🔬 What You Can Model

- Cell population dynamics
- Immune responses
- Drug treatments
- Disease progression
- Spatial patterns
- Parameter sensitivity
- Bifurcation analysis
- And much more!

## ❓ Need Help?

- Check the [documentation](docs/)
- Look at [examples](examples/)
- Open an [issue](https://github.com/Reinald0-M/ImmunoSys/issues)

## 🎓 Next Steps

1. ✅ Install the framework
2. ✅ Run the examples
3. 📝 Read the getting started guide
4. 🧬 Build your own model
5. 📊 Create beautiful visualizations
6. 🚀 Publish your research!

Happy modeling! 🧬✨
