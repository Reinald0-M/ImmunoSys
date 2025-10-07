"""
Tests for the visualization module.

Run with: pytest tests/
"""

import numpy as np
import pytest
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for testing
import matplotlib.pyplot as plt

from immunosys.visualization import (
    TimeSeries2D,
    PhasePlane2D,
    Plot3D,
    Heatmap,
    quick_plot
)


class TestTimeSeries2D:
    """Tests for TimeSeries2D plotter."""
    
    def test_basic_plot(self):
        """Test basic time series plotting."""
        time = np.linspace(0, 10, 100)
        data = np.sin(time)
        
        plotter = TimeSeries2D()
        fig, ax = plotter.plot(time, data)
        
        assert isinstance(fig, plt.Figure)
        assert isinstance(ax, plt.Axes)
        plt.close(fig)
    
    def test_multiple_series(self):
        """Test plotting multiple time series."""
        time = np.linspace(0, 10, 100)
        data = np.column_stack([np.sin(time), np.cos(time)])
        
        plotter = TimeSeries2D()
        fig, ax = plotter.plot(
            time, data,
            labels=['sin', 'cos']
        )
        
        assert len(ax.lines) == 2
        plt.close(fig)
    
    def test_dict_input(self):
        """Test plotting with dictionary input."""
        time = np.linspace(0, 10, 100)
        data = {
            'sine': np.sin(time),
            'cosine': np.cos(time)
        }
        
        plotter = TimeSeries2D()
        fig, ax = plotter.plot(time, data)
        
        assert len(ax.lines) == 2
        plt.close(fig)


class TestPhasePlane2D:
    """Tests for PhasePlane2D plotter."""
    
    def test_basic_phase_plot(self):
        """Test basic phase plane plotting."""
        theta = np.linspace(0, 2*np.pi, 100)
        x = np.cos(theta)
        y = np.sin(theta)
        
        plotter = PhasePlane2D()
        fig, ax = plotter.plot(
            x, y,
            show_direction=False,
            color_by_time=False
        )
        
        assert isinstance(fig, plt.Figure)
        plt.close(fig)
    
    def test_vector_field(self):
        """Test vector field plotting."""
        def dx_dt(x, y):
            return -y
        
        def dy_dt(x, y):
            return x
        
        plotter = PhasePlane2D()
        fig, ax = plotter.plot_vector_field(
            x_range=(-2, 2),
            y_range=(-2, 2),
            dx_func=dx_dt,
            dy_func=dy_dt,
            density=10
        )
        
        assert isinstance(fig, plt.Figure)
        plt.close(fig)


class TestPlot3D:
    """Tests for Plot3D plotter."""
    
    def test_trajectory_plot(self):
        """Test 3D trajectory plotting."""
        t = np.linspace(0, 10, 100)
        x = np.sin(t)
        y = np.cos(t)
        z = t
        
        plotter = Plot3D()
        fig, ax = plotter.plot_trajectory(
            x, y, z,
            color_by_time=False
        )
        
        assert isinstance(fig, plt.Figure)
        plt.close(fig)
    
    def test_surface_plot(self):
        """Test 3D surface plotting."""
        x = np.linspace(-5, 5, 30)
        y = np.linspace(-5, 5, 30)
        X, Y = np.meshgrid(x, y)
        Z = np.sin(np.sqrt(X**2 + Y**2))
        
        plotter = Plot3D()
        fig, ax = plotter.plot_surface(X, Y, Z)
        
        assert isinstance(fig, plt.Figure)
        plt.close(fig)


class TestHeatmap:
    """Tests for Heatmap plotter."""
    
    def test_basic_heatmap(self):
        """Test basic heatmap plotting."""
        data = np.random.randn(10, 10)
        
        plotter = Heatmap()
        fig, ax = plotter.plot(data)
        
        assert isinstance(fig, plt.Figure)
        plt.close(fig)
    
    def test_sensitivity_heatmap(self):
        """Test parameter sensitivity heatmap."""
        parameters = ['p1', 'p2', 'p3']
        outputs = ['o1', 'o2']
        matrix = np.random.randn(2, 3)
        
        plotter = Heatmap()
        fig, ax = plotter.plot_sensitivity(
            parameters, outputs, matrix
        )
        
        assert isinstance(fig, plt.Figure)
        plt.close(fig)


class TestQuickPlot:
    """Tests for quick_plot convenience function."""
    
    def test_line_plot(self):
        """Test quick line plot."""
        data = np.random.randn(100)
        fig, ax = quick_plot(data, plot_type='line')
        
        assert isinstance(fig, plt.Figure)
        plt.close(fig)
    
    def test_heatmap(self):
        """Test quick heatmap."""
        data = np.random.randn(10, 10)
        fig, ax = quick_plot(data, plot_type='heatmap')
        
        assert isinstance(fig, plt.Figure)
        plt.close(fig)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
