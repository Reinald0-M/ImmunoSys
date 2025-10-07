"""
Tests for the utils module.

Run with: pytest tests/
"""

import numpy as np
import pytest
from immunosys.utils import (
    normalize_data,
    compute_derivative,
    compute_jacobian,
    analyze_stability,
    detect_oscillations
)


class TestNormalizeData:
    """Tests for normalize_data function."""
    
    def test_minmax_normalization(self):
        """Test min-max normalization."""
        data = np.array([1, 2, 3, 4, 5])
        normalized, params = normalize_data(data, method='minmax')
        
        assert np.min(normalized) == pytest.approx(0)
        assert np.max(normalized) == pytest.approx(1)
        assert 'min' in params
        assert 'max' in params
    
    def test_zscore_normalization(self):
        """Test z-score normalization."""
        data = np.array([1, 2, 3, 4, 5])
        normalized, params = normalize_data(data, method='zscore')
        
        assert np.mean(normalized) == pytest.approx(0, abs=1e-10)
        assert np.std(normalized) == pytest.approx(1, abs=1e-10)
        assert 'mean' in params
        assert 'std' in params
    
    def test_robust_normalization(self):
        """Test robust normalization."""
        data = np.array([1, 2, 3, 4, 5, 100])  # With outlier
        normalized, params = normalize_data(data, method='robust')
        
        assert 'median' in params
        assert 'iqr' in params
    
    def test_invalid_method(self):
        """Test that invalid method raises error."""
        data = np.array([1, 2, 3])
        
        with pytest.raises(ValueError):
            normalize_data(data, method='invalid')


class TestComputeDerivative:
    """Tests for compute_derivative function."""
    
    def test_finite_diff(self):
        """Test finite difference derivative."""
        time = np.linspace(0, 2*np.pi, 100)
        data = np.sin(time)
        
        derivative = compute_derivative(time, data, method='finite_diff')
        
        # Derivative of sin is cos
        expected = np.cos(time)
        assert derivative.shape == data.shape
        # Check approximate agreement (numerical derivatives aren't exact)
        assert np.allclose(derivative, expected, atol=0.1)
    
    def test_gradient(self):
        """Test gradient method derivative."""
        time = np.linspace(0, 2*np.pi, 100)
        data = np.sin(time)
        
        derivative = compute_derivative(time, data, method='gradient')
        
        assert derivative.shape == data.shape


class TestComputeJacobian:
    """Tests for compute_jacobian function."""
    
    def test_simple_system(self):
        """Test Jacobian computation for simple system."""
        def equations(state, t):
            x, y = state
            return np.array([x, y])
        
        point = np.array([1.0, 1.0])
        jacobian = compute_jacobian(equations, point)
        
        # For this system, Jacobian should be identity
        expected = np.eye(2)
        assert jacobian.shape == (2, 2)
        assert np.allclose(jacobian, expected, atol=0.01)


class TestAnalyzeStability:
    """Tests for analyze_stability function."""
    
    def test_stable_equilibrium(self):
        """Test stability analysis for stable equilibrium."""
        # Jacobian with negative eigenvalues (stable)
        jacobian = np.array([[-1, 0], [0, -2]])
        
        result = analyze_stability(jacobian)
        
        assert result['stability'] == 'stable'
        assert len(result['eigenvalues']) == 2
        assert not result['oscillatory']
    
    def test_unstable_equilibrium(self):
        """Test stability analysis for unstable equilibrium."""
        # Jacobian with positive eigenvalues (unstable)
        jacobian = np.array([[1, 0], [0, 2]])
        
        result = analyze_stability(jacobian)
        
        assert result['stability'] == 'unstable'
    
    def test_saddle_point(self):
        """Test stability analysis for saddle point."""
        # Jacobian with mixed eigenvalues (saddle)
        jacobian = np.array([[1, 0], [0, -1]])
        
        result = analyze_stability(jacobian)
        
        assert result['stability'] == 'saddle'
    
    def test_oscillatory(self):
        """Test detection of oscillatory behavior."""
        # Jacobian with complex eigenvalues
        jacobian = np.array([[0, -1], [1, 0]])
        
        result = analyze_stability(jacobian)
        
        assert result['oscillatory']


class TestDetectOscillations:
    """Tests for detect_oscillations function."""
    
    def test_oscillatory_signal(self):
        """Test oscillation detection in periodic signal."""
        time = np.linspace(0, 10*np.pi, 1000)
        data = np.sin(time)
        
        result = detect_oscillations(time, data, prominence=0.5)
        
        assert result['oscillatory']
        assert result['period'] is not None
        assert result['amplitude'] is not None
        assert result['frequency'] is not None
    
    def test_non_oscillatory_signal(self):
        """Test oscillation detection in non-periodic signal."""
        time = np.linspace(0, 10, 100)
        data = np.exp(-time)  # Exponential decay
        
        result = detect_oscillations(time, data, prominence=0.5)
        
        assert not result['oscillatory']
        assert result['period'] is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
