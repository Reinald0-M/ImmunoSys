"""
Example: Simple T Cell - Target Cell Interaction Model

This example demonstrates a basic immunological model of T cell-target cell
dynamics, similar to a predator-prey system.
"""

import numpy as np
import sys
sys.path.insert(0, '..')

from immunosys.models import BaseModel
from immunosys.visualization import TimeSeries2D, PhasePlane2D
from immunosys.utils import find_equilibria, compute_jacobian, analyze_stability


class TCellTargetModel(BaseModel):
    """
    A simple model of T cell and target cell dynamics.
    
    Equations:
        dT/dt = r*T*(1 - T/K) - a*T*C
        dC/dt = b*T*C - d*C
    
    Where:
        T = Target cells
        C = T cells (cytotoxic)
        r = Target cell growth rate
        K = Carrying capacity
        a = Attack rate
        b = T cell proliferation rate
        d = T cell death rate
    """
    
    def __init__(self, parameters):
        """Initialize with parameters."""
        super().__init__(parameters)
        self.r = parameters.get('r', 0.5)
        self.K = parameters.get('K', 100)
        self.a = parameters.get('a', 0.01)
        self.b = parameters.get('b', 0.005)
        self.d = parameters.get('d', 0.2)
    
    def equations(self, state, t):
        """Define the system of ODEs."""
        T, C = state
        
        dT_dt = self.r * T * (1 - T/self.K) - self.a * T * C
        dC_dt = self.b * T * C - self.d * C
        
        return np.array([dT_dt, dC_dt])


def main():
    """Run the example simulation."""
    
    # Define parameters
    parameters = {
        'r': 0.5,   # Target growth rate
        'K': 100,   # Carrying capacity
        'a': 0.01,  # Attack rate
        'b': 0.005, # T cell proliferation
        'd': 0.2    # T cell death rate
    }
    
    # Create model
    model = TCellTargetModel(parameters)
    
    # Set initial conditions
    initial_conditions = np.array([80.0, 30.0])  # [Targets, T cells]
    
    # Simulate
    print("Running simulation...")
    time, solution = model.simulate(
        initial_conditions=initial_conditions,
        time_span=(0, 200),
        num_points=2000
    )
    
    # Extract solutions
    targets = solution[:, 0]
    tcells = solution[:, 1]
    
    # Create time series plot
    print("Creating time series plot...")
    plotter = TimeSeries2D(style='science')
    fig1, ax1 = plotter.plot(
        time,
        solution,
        labels=['Target Cells', 'T Cells'],
        xlabel='Time (days)',
        ylabel='Cell Population',
        title='T Cell - Target Cell Dynamics',
        colors=['#d62728', '#1f77b4'],
        show_grid=True
    )
    
    # Save the figure (uncomment to save)
    # plotter.save_figure(fig1, 'tcell_target_timeseries', formats=['png', 'pdf'])
    
    # Create phase plane plot
    print("Creating phase plane plot...")
    plotter2 = PhasePlane2D(style='science')
    fig2, ax2 = plotter2.plot(
        targets,
        tcells,
        xlabel='Target Cells',
        ylabel='T Cells',
        title='Phase Plane: T Cell - Target Dynamics',
        show_direction=True,
        color_by_time=True
    )
    
    # Find equilibria
    print("\nFinding equilibrium points...")
    initial_guesses = [
        np.array([0.0, 0.0]),
        np.array([100.0, 0.0]),
        np.array([50.0, 20.0])
    ]
    
    equilibria = find_equilibria(model.equations, initial_guesses)
    
    print(f"Found {len(equilibria)} equilibrium point(s):")
    for i, eq in enumerate(equilibria):
        print(f"\nEquilibrium {i+1}: T = {eq[0]:.2f}, C = {eq[1]:.2f}")
        
        # Analyze stability
        jacobian = compute_jacobian(model.equations, eq)
        stability = analyze_stability(jacobian)
        
        print(f"  Stability: {stability['stability']}")
        print(f"  Eigenvalues: {stability['eigenvalues']}")
        if stability['oscillatory']:
            print(f"  System shows oscillatory behavior")
    
    print("\nSimulation complete!")
    print("Close the plot windows to exit.")
    
    import matplotlib.pyplot as plt
    plt.show()


if __name__ == "__main__":
    main()
