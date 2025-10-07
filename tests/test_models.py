"""
Tests for the models module.

Run with: pytest tests/
"""

import numpy as np
import pytest
from immunosys.models import BaseModel


class SimpleModel(BaseModel):
    """Simple test model implementation."""
    
    def equations(self, state, t):
        """Simple exponential growth/decay."""
        x, y = state
        return np.array([-0.1 * x, -0.2 * y])


class TestBaseModel:
    """Tests for BaseModel class."""
    
    def test_initialization(self):
        """Test model initialization."""
        params = {'alpha': 0.1, 'beta': 0.2}
        model = SimpleModel(params)
        
        assert model.parameters == params
        assert model.time_points is None
        assert model.solution is None
    
    def test_simulate_odeint(self):
        """Test simulation with odeint method."""
        model = SimpleModel({})
        initial = np.array([1.0, 2.0])
        
        time, solution = model.simulate(
            initial_conditions=initial,
            time_span=(0, 10),
            num_points=100,
            method='odeint'
        )
        
        assert len(time) == 100
        assert solution.shape == (100, 2)
        assert np.all(np.isfinite(solution))
        
        # Check that values decay (simple exponential decay)
        assert solution[-1, 0] < initial[0]
        assert solution[-1, 1] < initial[1]
    
    def test_simulate_solve_ivp(self):
        """Test simulation with solve_ivp method."""
        model = SimpleModel({})
        initial = np.array([1.0, 2.0])
        
        time, solution = model.simulate(
            initial_conditions=initial,
            time_span=(0, 10),
            num_points=100,
            method='solve_ivp'
        )
        
        assert len(time) == 100
        assert solution.shape == (100, 2)
        assert np.all(np.isfinite(solution))
    
    def test_invalid_method(self):
        """Test that invalid method raises error."""
        model = SimpleModel({})
        initial = np.array([1.0, 2.0])
        
        with pytest.raises(ValueError):
            model.simulate(
                initial_conditions=initial,
                time_span=(0, 10),
                method='invalid_method'
            )
    
    def test_equilibria_not_implemented(self):
        """Test that base equilibria method raises NotImplementedError."""
        model = SimpleModel({})
        
        with pytest.raises(NotImplementedError):
            model.get_equilibria()
    
    def test_stability_not_implemented(self):
        """Test that base stability method raises NotImplementedError."""
        model = SimpleModel({})
        
        with pytest.raises(NotImplementedError):
            model.stability_analysis(np.array([0, 0]))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
