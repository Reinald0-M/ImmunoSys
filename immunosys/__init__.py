"""
ImmunoSys - A Mathematical Modeling Framework for Immunological Dynamics

This package provides tools and utilities for modeling immunological systems,
with a focus on alopecia areata dynamics and other immune system phenomena.
The goal is to create an 'AlphaFold for the immune system'.
"""

__version__ = "0.1.0"
__author__ = "ImmunoSys Research Group"

from .visualization import plots
from .models import base
from .utils import helpers

__all__ = ["plots", "base", "helpers"]
