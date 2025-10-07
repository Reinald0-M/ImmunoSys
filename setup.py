"""Setup configuration for ImmunoSys package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="immunosys",
    version="0.1.0",
    author="ImmunoSys Research Group",
    description="A Mathematical Modeling Framework for Immunological Dynamics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Reinald0-M/ImmunoSys",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "numpy>=1.24",
        "scipy>=1.10",
        "matplotlib>=3.7",
        "pandas>=2.0",
        "seaborn>=0.12",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4",
            "black>=23.0",
            "flake8>=6.0",
            "mypy>=1.4",
            "jupyter>=1.0",
        ],
        "viz": [
            "plotly>=5.14",
            "mayavi>=4.8",
            "pyvista>=0.40",
        ],
        "all": [
            "pytest>=7.4",
            "black>=23.0",
            "flake8>=6.0",
            "mypy>=1.4",
            "jupyter>=1.0",
            "plotly>=5.14",
            "mayavi>=4.8",
            "pyvista>=0.40",
            "networkx>=3.1",
            "sympy>=1.12",
            "scikit-learn>=1.3",
        ],
    },
)
