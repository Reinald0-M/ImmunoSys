# Changelog

All notable changes to the ImmunoSys project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-01-XX

### Added
- Initial repository setup for ImmunoSys mathematical modeling framework
- Core package structure with models, visualization, and utils modules
- `BaseModel` abstract class for ODE-based models
- Publication-ready visualization classes:
  - `TimeSeries2D` for temporal dynamics
  - `PhasePlane2D` for phase space analysis with vector fields
  - `Plot3D` for 3D trajectories and surfaces
  - `Heatmap` for spatial patterns and parameter sensitivity
  - `NetworkViz` for cell-cell interaction networks
- Comprehensive utility functions:
  - Equilibrium finding and stability analysis
  - Parameter sensitivity analysis
  - Oscillation detection
  - Data normalization
  - Numerical derivatives
  - Lyapunov exponent estimation
  - File I/O for results
- Conda environment specification with flexible dependencies
- Alternative pip requirements.txt
- Complete test suite with pytest
- Example notebooks and scripts demonstrating framework capabilities
- Comprehensive documentation:
  - README with quick start guide
  - API reference
  - Getting started guide
  - Contributing guidelines
- MIT License
- Configuration file for customization
- Development tools setup (pytest, black, flake8, mypy)

### Infrastructure
- Package installable with `pip install -e .`
- Support for Python 3.9+
- All dependencies use flexible version specifiers (>=)
- Organized directory structure for models, visualization, utils, examples, tests, and docs

## [Unreleased]

### Planned Features
- Specific models for alopecia areata dynamics
- Stochastic differential equation support
- Spatial modeling with PDEs
- Agent-based modeling components
- Parameter estimation from experimental data
- Automatic bifurcation analysis
- Machine learning integration
- Enhanced documentation with Sphinx
- More example models and case studies
- Performance optimizations
- Web interface for model exploration

---

## Version History

- **0.1.0** - Initial release with core framework
