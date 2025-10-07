# Contributing to ImmunoSys

Thank you for your interest in contributing to ImmunoSys! This document provides guidelines for contributing to the project.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/ImmunoSys.git
   cd ImmunoSys
   ```
3. **Set up the development environment**:
   ```bash
   conda env create -f environment.yml
   conda activate immunosys-env
   pip install -e .
   ```

## Development Workflow

1. **Create a new branch** for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the coding guidelines below

3. **Run tests** to ensure nothing is broken:
   ```bash
   pytest tests/
   ```

4. **Format your code** with Black:
   ```bash
   black immunosys/
   ```

5. **Check code quality** with flake8:
   ```bash
   flake8 immunosys/
   ```

6. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add feature: description of your changes"
   ```

7. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Create a Pull Request** on GitHub

## Coding Guidelines

### Python Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use [Black](https://black.readthedocs.io/) for code formatting (line length: 88)
- Use type hints where appropriate
- Write docstrings for all public functions and classes

### Docstring Format

We use NumPy-style docstrings:

```python
def function_name(param1: type, param2: type) -> return_type:
    """
    Brief description of the function.
    
    Longer description if needed, explaining what the function does,
    any important details, algorithms used, etc.
    
    Parameters
    ----------
    param1 : type
        Description of param1
    param2 : type
        Description of param2
        
    Returns
    -------
    return_type
        Description of return value
        
    Examples
    --------
    >>> function_name(value1, value2)
    expected_output
    """
    pass
```

### Testing

- Write tests for all new functionality
- Aim for high test coverage
- Tests should be in the `tests/` directory
- Use pytest for testing
- Test file names should match the module they test: `test_module.py`

### Commit Messages

- Use clear, descriptive commit messages
- Start with a verb in present tense (e.g., "Add", "Fix", "Update")
- Keep the first line under 50 characters
- Add detailed description after a blank line if needed

Example:
```
Add parameter sensitivity analysis function

Implements a function to compute parameter sensitivities
using finite differences. Includes tests and documentation.
```

## Types of Contributions

### Bug Reports

When filing a bug report, please include:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Python version and relevant package versions
- Code snippet demonstrating the issue (if applicable)

### Feature Requests

When proposing a new feature, please:
- Explain the motivation for the feature
- Provide examples of how it would be used
- Consider how it fits with existing functionality
- Be willing to help implement it

### Code Contributions

We welcome contributions including:
- New models or modeling techniques
- Enhanced visualization capabilities
- Utility functions for common tasks
- Documentation improvements
- Bug fixes
- Performance improvements

## Documentation

- Update documentation for any changed functionality
- Add docstrings to new functions and classes
- Update the README if needed
- Add examples to demonstrate new features

## Project Structure

```
ImmunoSys/
├── immunosys/              # Main package
│   ├── models/             # Mathematical models
│   ├── visualization/      # Plotting tools
│   ├── utils/              # Utility functions
│   └── data/               # Data storage
├── examples/               # Example notebooks and scripts
├── tests/                  # Test suite
├── docs/                   # Documentation
└── README.md              # Project overview
```

## Questions?

If you have questions about contributing, please:
- Open an issue on GitHub
- Tag it with the "question" label
- Provide context for your question

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on what is best for the community
- Show empathy towards other community members

Thank you for contributing to ImmunoSys!
