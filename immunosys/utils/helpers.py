"""
Utility functions for ImmunoSys modeling framework.

This module provides helper functions for common tasks in mathematical
modeling of immunological systems.
"""

import numpy as np
from typing import Dict, List, Tuple, Callable, Optional
from scipy.optimize import fsolve, minimize
from scipy.signal import find_peaks
import warnings


def normalize_data(
    data: np.ndarray,
    method: str = 'minmax'
) -> Tuple[np.ndarray, Dict[str, float]]:
    """
    Normalize data using various methods.
    
    Parameters
    ----------
    data : np.ndarray
        Data to normalize
    method : str
        Normalization method ('minmax', 'zscore', 'robust')
        
    Returns
    -------
    Tuple[np.ndarray, Dict[str, float]]
        Normalized data and normalization parameters
    """
    if method == 'minmax':
        min_val = np.min(data)
        max_val = np.max(data)
        normalized = (data - min_val) / (max_val - min_val + 1e-10)
        params = {'min': min_val, 'max': max_val}
    elif method == 'zscore':
        mean_val = np.mean(data)
        std_val = np.std(data)
        normalized = (data - mean_val) / (std_val + 1e-10)
        params = {'mean': mean_val, 'std': std_val}
    elif method == 'robust':
        median_val = np.median(data)
        iqr = np.percentile(data, 75) - np.percentile(data, 25)
        normalized = (data - median_val) / (iqr + 1e-10)
        params = {'median': median_val, 'iqr': iqr}
    else:
        raise ValueError(f"Unknown normalization method: {method}")
    
    return normalized, params


def compute_derivative(
    time: np.ndarray,
    data: np.ndarray,
    method: str = 'finite_diff'
) -> np.ndarray:
    """
    Compute numerical derivative of data.
    
    Parameters
    ----------
    time : np.ndarray
        Time points
    data : np.ndarray
        Data values
    method : str
        Method for computing derivative ('finite_diff', 'gradient')
        
    Returns
    -------
    np.ndarray
        Derivative values
    """
    if method == 'finite_diff':
        return np.gradient(data, time)
    elif method == 'gradient':
        return np.gradient(data, time, edge_order=2)
    else:
        raise ValueError(f"Unknown derivative method: {method}")


def find_equilibria(
    equations: Callable,
    initial_guesses: List[np.ndarray],
    bounds: Optional[Tuple[np.ndarray, np.ndarray]] = None
) -> List[np.ndarray]:
    """
    Find equilibrium points of a dynamical system.
    
    Parameters
    ----------
    equations : Callable
        Function defining the system (should return derivatives)
    initial_guesses : List[np.ndarray]
        List of initial guesses for equilibria
    bounds : Optional[Tuple[np.ndarray, np.ndarray]]
        Bounds for optimization (lower, upper)
        
    Returns
    -------
    List[np.ndarray]
        List of equilibrium points found
    """
    equilibria = []
    
    for guess in initial_guesses:
        try:
            # Use fsolve to find where derivatives are zero
            eq = fsolve(lambda x: equations(x, 0), guess, full_output=True)
            
            if eq[2] == 1:  # Solution converged
                # Check if this is a new equilibrium
                is_new = True
                for existing_eq in equilibria:
                    if np.allclose(eq[0], existing_eq, rtol=1e-3):
                        is_new = False
                        break
                
                if is_new:
                    # Verify it's actually an equilibrium
                    residual = equations(eq[0], 0)
                    if np.allclose(residual, 0, atol=1e-6):
                        equilibria.append(eq[0])
        except:
            continue
    
    return equilibria


def compute_jacobian(
    equations: Callable,
    point: np.ndarray,
    epsilon: float = 1e-6
) -> np.ndarray:
    """
    Compute Jacobian matrix numerically.
    
    Parameters
    ----------
    equations : Callable
        Function defining the system
    point : np.ndarray
        Point at which to compute Jacobian
    epsilon : float
        Small perturbation for numerical differentiation
        
    Returns
    -------
    np.ndarray
        Jacobian matrix
    """
    n = len(point)
    jacobian = np.zeros((n, n))
    f0 = equations(point, 0)
    
    for i in range(n):
        point_plus = point.copy()
        point_plus[i] += epsilon
        f_plus = equations(point_plus, 0)
        jacobian[:, i] = (f_plus - f0) / epsilon
    
    return jacobian


def analyze_stability(jacobian: np.ndarray) -> Dict[str, any]:
    """
    Analyze stability of an equilibrium point from its Jacobian.
    
    Parameters
    ----------
    jacobian : np.ndarray
        Jacobian matrix at equilibrium
        
    Returns
    -------
    Dict[str, any]
        Dictionary containing eigenvalues and stability classification
    """
    eigenvalues = np.linalg.eigvals(jacobian)
    
    # Classify stability
    real_parts = np.real(eigenvalues)
    
    if np.all(real_parts < 0):
        stability = 'stable'
    elif np.all(real_parts > 0):
        stability = 'unstable'
    elif np.any(np.abs(real_parts) < 1e-10):
        stability = 'center/marginally_stable'
    else:
        stability = 'saddle'
    
    # Check for oscillations (complex eigenvalues)
    has_oscillations = np.any(np.abs(np.imag(eigenvalues)) > 1e-10)
    
    return {
        'eigenvalues': eigenvalues,
        'stability': stability,
        'oscillatory': has_oscillations,
        'dominant_eigenvalue': eigenvalues[np.argmax(np.abs(eigenvalues))]
    }


def detect_oscillations(
    time: np.ndarray,
    data: np.ndarray,
    prominence: float = 0.1
) -> Dict[str, any]:
    """
    Detect oscillations in time series data.
    
    Parameters
    ----------
    time : np.ndarray
        Time points
    data : np.ndarray
        Data values
    prominence : float
        Minimum prominence of peaks
        
    Returns
    -------
    Dict[str, any]
        Dictionary with oscillation properties
    """
    # Find peaks
    peaks, properties = find_peaks(data, prominence=prominence)
    
    if len(peaks) < 2:
        return {
            'oscillatory': False,
            'period': None,
            'amplitude': None,
            'frequency': None
        }
    
    # Estimate period
    peak_times = time[peaks]
    periods = np.diff(peak_times)
    mean_period = np.mean(periods)
    
    # Estimate amplitude
    amplitudes = data[peaks]
    mean_amplitude = np.mean(amplitudes)
    
    # Estimate frequency
    frequency = 1.0 / mean_period if mean_period > 0 else None
    
    return {
        'oscillatory': True,
        'period': mean_period,
        'period_std': np.std(periods),
        'amplitude': mean_amplitude,
        'amplitude_std': np.std(amplitudes),
        'frequency': frequency,
        'num_peaks': len(peaks)
    }


def parameter_sensitivity(
    model_func: Callable,
    base_parameters: Dict[str, float],
    parameter_ranges: Dict[str, Tuple[float, float]],
    output_func: Callable,
    num_samples: int = 100
) -> Dict[str, np.ndarray]:
    """
    Perform parameter sensitivity analysis.
    
    Parameters
    ----------
    model_func : Callable
        Function that runs the model and returns results
    base_parameters : Dict[str, float]
        Base parameter values
    parameter_ranges : Dict[str, Tuple[float, float]]
        Ranges to vary for each parameter (min, max)
    output_func : Callable
        Function to extract output metric from model results
    num_samples : int
        Number of samples for each parameter
        
    Returns
    -------
    Dict[str, np.ndarray]
        Sensitivity results for each parameter
    """
    sensitivity = {}
    base_output = output_func(model_func(base_parameters))
    
    for param_name, (min_val, max_val) in parameter_ranges.items():
        param_values = np.linspace(min_val, max_val, num_samples)
        outputs = np.zeros(num_samples)
        
        for i, val in enumerate(param_values):
            params = base_parameters.copy()
            params[param_name] = val
            outputs[i] = output_func(model_func(params))
        
        # Compute normalized sensitivity
        normalized_sensitivity = (outputs - base_output) / (base_output + 1e-10)
        
        sensitivity[param_name] = {
            'values': param_values,
            'outputs': outputs,
            'normalized_sensitivity': normalized_sensitivity,
            'mean_sensitivity': np.mean(np.abs(normalized_sensitivity))
        }
    
    return sensitivity


def compute_lyapunov_exponent(
    time: np.ndarray,
    trajectory1: np.ndarray,
    trajectory2: np.ndarray
) -> float:
    """
    Estimate largest Lyapunov exponent from two nearby trajectories.
    
    Parameters
    ----------
    time : np.ndarray
        Time points
    trajectory1, trajectory2 : np.ndarray
        Two nearby trajectories
        
    Returns
    -------
    float
        Estimated Lyapunov exponent
    """
    distances = np.linalg.norm(trajectory1 - trajectory2, axis=1)
    
    # Avoid log of zero
    valid_indices = distances > 1e-10
    if np.sum(valid_indices) < 2:
        return np.nan
    
    log_distances = np.log(distances[valid_indices])
    valid_times = time[valid_indices]
    
    # Linear fit to log of distances
    coeffs = np.polyfit(valid_times, log_distances, 1)
    lyapunov = coeffs[0]
    
    return lyapunov


def save_results(
    filename: str,
    data: Dict[str, np.ndarray],
    metadata: Optional[Dict[str, any]] = None
):
    """
    Save simulation results to file.
    
    Parameters
    ----------
    filename : str
        Output filename (supports .npz, .csv)
    data : Dict[str, np.ndarray]
        Dictionary of data arrays to save
    metadata : Optional[Dict[str, any]]
        Additional metadata to save
    """
    if filename.endswith('.npz'):
        if metadata:
            np.savez(filename, **data, metadata=metadata)
        else:
            np.savez(filename, **data)
    elif filename.endswith('.csv'):
        import pandas as pd
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
    else:
        raise ValueError(f"Unsupported file format: {filename}")
    
    print(f"Results saved to {filename}")


def load_results(filename: str) -> Dict[str, np.ndarray]:
    """
    Load simulation results from file.
    
    Parameters
    ----------
    filename : str
        Input filename (supports .npz, .csv)
        
    Returns
    -------
    Dict[str, np.ndarray]
        Dictionary of loaded data arrays
    """
    if filename.endswith('.npz'):
        with np.load(filename, allow_pickle=True) as data:
            return {key: data[key] for key in data.keys()}
    elif filename.endswith('.csv'):
        import pandas as pd
        df = pd.read_csv(filename)
        return {col: df[col].values for col in df.columns}
    else:
        raise ValueError(f"Unsupported file format: {filename}")
