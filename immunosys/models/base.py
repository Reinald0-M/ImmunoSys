"""Base classes for mathematical models of immunological dynamics."""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple
import numpy as np
from scipy.integrate import odeint, solve_ivp


class BaseModel(ABC):
    """
    Abstract base class for immunological mathematical models.
    
    This class provides a template for implementing differential equation
    models of immune system dynamics.
    """
    
    def __init__(self, parameters: Dict[str, float]):
        """
        Initialize the model with given parameters.
        
        Parameters
        ----------
        parameters : Dict[str, float]
            Dictionary of model parameters
        """
        self.parameters = parameters
        self.time_points = None
        self.solution = None
    
    @abstractmethod
    def equations(self, state: np.ndarray, t: float) -> np.ndarray:
        """
        Define the system of differential equations.
        
        Parameters
        ----------
        state : np.ndarray
            Current state vector
        t : float
            Current time point
            
        Returns
        -------
        np.ndarray
            Derivatives of state variables
        """
        pass
    
    def simulate(
        self, 
        initial_conditions: np.ndarray,
        time_span: Tuple[float, float],
        num_points: int = 1000,
        method: str = 'odeint'
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Simulate the model over a given time span.
        
        Parameters
        ----------
        initial_conditions : np.ndarray
            Initial state of the system
        time_span : Tuple[float, float]
            (start_time, end_time) for simulation
        num_points : int, optional
            Number of time points for output
        method : str, optional
            Integration method ('odeint' or 'solve_ivp')
            
        Returns
        -------
        Tuple[np.ndarray, np.ndarray]
            Time points and solution array
        """
        self.time_points = np.linspace(time_span[0], time_span[1], num_points)
        
        if method == 'odeint':
            self.solution = odeint(self.equations, initial_conditions, self.time_points)
        elif method == 'solve_ivp':
            sol = solve_ivp(
                lambda t, y: self.equations(y, t),
                time_span,
                initial_conditions,
                t_eval=self.time_points,
                method='RK45'
            )
            self.solution = sol.y.T
        else:
            raise ValueError(f"Unknown method: {method}")
        
        return self.time_points, self.solution
    
    def get_equilibria(self) -> List[np.ndarray]:
        """
        Find equilibrium points of the system.
        
        Returns
        -------
        List[np.ndarray]
            List of equilibrium points
        """
        # Placeholder - to be implemented in subclasses
        raise NotImplementedError("Equilibrium analysis must be implemented in subclass")
    
    def stability_analysis(self, equilibrium: np.ndarray) -> Dict[str, any]:
        """
        Perform linear stability analysis around an equilibrium point.
        
        Parameters
        ----------
        equilibrium : np.ndarray
            Equilibrium point to analyze
            
        Returns
        -------
        Dict[str, any]
            Dictionary containing eigenvalues and stability information
        """
        # Placeholder - to be implemented in subclasses
        raise NotImplementedError("Stability analysis must be implemented in subclass")
