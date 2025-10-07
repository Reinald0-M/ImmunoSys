"""
Publication-Ready Visualization Module for ImmunoSys

This module provides a comprehensive suite of visualization tools designed
for creating publication-ready figures for immunological modeling research.

Classes
-------
- PublicationPlotter: Base class for all publication-ready plots
- TimeSeries2D: 2D time series plots for dynamics
- PhasePlane2D: 2D phase plane diagrams
- Plot3D: 3D trajectory and surface plots
- Heatmap: Heatmaps for parameter sensitivity and spatial patterns
- NetworkViz: Network diagrams for cell-cell interactions
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap, Normalize
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import seaborn as sns
from typing import Dict, List, Optional, Tuple, Union
import warnings


class PublicationPlotter:
    """
    Base class for publication-ready plots.
    
    Sets up matplotlib with publication-quality defaults including
    proper font sizes, line widths, and figure dimensions.
    """
    
    # Publication-quality style parameters
    STYLE_PARAMS = {
        'figure.figsize': (8, 6),
        'figure.dpi': 300,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
        'savefig.pad_inches': 0.1,
        'font.size': 12,
        'axes.labelsize': 14,
        'axes.titlesize': 16,
        'xtick.labelsize': 12,
        'ytick.labelsize': 12,
        'legend.fontsize': 11,
        'legend.frameon': False,
        'axes.linewidth': 1.5,
        'lines.linewidth': 2.0,
        'lines.markersize': 8,
        'xtick.major.width': 1.5,
        'ytick.major.width': 1.5,
        'xtick.minor.width': 1.0,
        'ytick.minor.width': 1.0,
        'axes.grid': False,
        'grid.alpha': 0.3,
    }
    
    def __init__(self, style: str = 'default'):
        """
        Initialize the plotter with publication-quality settings.
        
        Parameters
        ----------
        style : str, optional
            Style preset ('default', 'nature', 'science', 'minimal')
        """
        self.style = style
        self._apply_style()
    
    def _apply_style(self):
        """Apply the chosen style to matplotlib."""
        plt.style.use('seaborn-v0_8-paper' if 'seaborn-v0_8-paper' in plt.style.available else 'default')
        mpl.rcParams.update(self.STYLE_PARAMS)
        
        if self.style == 'nature':
            mpl.rcParams['font.family'] = 'sans-serif'
            mpl.rcParams['font.sans-serif'] = ['Arial', 'Helvetica']
        elif self.style == 'science':
            mpl.rcParams['font.family'] = 'serif'
            mpl.rcParams['font.serif'] = ['Times New Roman', 'Times']
    
    def save_figure(
        self,
        fig: plt.Figure,
        filename: str,
        formats: List[str] = ['png', 'pdf'],
        **kwargs
    ):
        """
        Save figure in multiple formats for publication.
        
        Parameters
        ----------
        fig : plt.Figure
            Figure to save
        filename : str
            Base filename (without extension)
        formats : List[str], optional
            List of formats to save ('png', 'pdf', 'svg', 'eps')
        **kwargs
            Additional arguments passed to savefig
        """
        for fmt in formats:
            fig.savefig(f"{filename}.{fmt}", format=fmt, **kwargs)
        print(f"Figure saved as: {', '.join([f'{filename}.{fmt}' for fmt in formats])}")


class TimeSeries2D(PublicationPlotter):
    """
    Create publication-ready 2D time series plots for dynamic simulations.
    """
    
    def __init__(self, style: str = 'default'):
        """Initialize TimeSeries2D plotter."""
        super().__init__(style)
    
    def plot(
        self,
        time: np.ndarray,
        data: Union[np.ndarray, Dict[str, np.ndarray]],
        labels: Optional[List[str]] = None,
        xlabel: str = 'Time',
        ylabel: str = 'Population',
        title: Optional[str] = None,
        colors: Optional[List[str]] = None,
        figsize: Tuple[float, float] = (10, 6),
        show_grid: bool = True,
        log_scale: bool = False,
        **kwargs
    ) -> Tuple[plt.Figure, plt.Axes]:
        """
        Create a time series plot.
        
        Parameters
        ----------
        time : np.ndarray
            Time points
        data : Union[np.ndarray, Dict[str, np.ndarray]]
            Data to plot. Can be 2D array (time x variables) or dict of arrays
        labels : Optional[List[str]]
            Labels for each variable
        xlabel, ylabel : str
            Axis labels
        title : Optional[str]
            Plot title
        colors : Optional[List[str]]
            Colors for each line
        figsize : Tuple[float, float]
            Figure size
        show_grid : bool
            Whether to show grid
        log_scale : bool
            Whether to use log scale for y-axis
        **kwargs
            Additional arguments passed to plot
            
        Returns
        -------
        Tuple[plt.Figure, plt.Axes]
            Figure and axes objects
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        # Handle different data formats
        if isinstance(data, dict):
            for i, (key, values) in enumerate(data.items()):
                color = colors[i] if colors and i < len(colors) else None
                ax.plot(time, values, label=key, color=color, **kwargs)
        else:
            if data.ndim == 1:
                data = data.reshape(-1, 1)
            
            for i in range(data.shape[1]):
                label = labels[i] if labels and i < len(labels) else f'Variable {i+1}'
                color = colors[i] if colors and i < len(colors) else None
                ax.plot(time, data[:, i], label=label, color=color, **kwargs)
        
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        if title:
            ax.set_title(title)
        
        if log_scale:
            ax.set_yscale('log')
        
        if show_grid:
            ax.grid(True, alpha=0.3, linestyle='--')
        
        ax.legend(loc='best')
        plt.tight_layout()
        
        return fig, ax


class PhasePlane2D(PublicationPlotter):
    """
    Create 2D phase plane diagrams with trajectories and nullclines.
    """
    
    def __init__(self, style: str = 'default'):
        """Initialize PhasePlane2D plotter."""
        super().__init__(style)
    
    def plot(
        self,
        x_data: np.ndarray,
        y_data: np.ndarray,
        xlabel: str = 'State Variable 1',
        ylabel: str = 'State Variable 2',
        title: Optional[str] = None,
        show_direction: bool = True,
        color_by_time: bool = True,
        equilibria: Optional[List[Tuple[float, float]]] = None,
        figsize: Tuple[float, float] = (8, 8),
        **kwargs
    ) -> Tuple[plt.Figure, plt.Axes]:
        """
        Create a phase plane plot.
        
        Parameters
        ----------
        x_data, y_data : np.ndarray
            Phase plane coordinates
        xlabel, ylabel : str
            Axis labels
        title : Optional[str]
            Plot title
        show_direction : bool
            Whether to show trajectory direction with arrows
        color_by_time : bool
            Whether to color trajectory by time
        equilibria : Optional[List[Tuple[float, float]]]
            List of equilibrium points to mark
        figsize : Tuple[float, float]
            Figure size
        **kwargs
            Additional arguments
            
        Returns
        -------
        Tuple[plt.Figure, plt.Axes]
            Figure and axes objects
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        if color_by_time:
            # Color trajectory by time
            points = np.array([x_data, y_data]).T.reshape(-1, 1, 2)
            segments = np.concatenate([points[:-1], points[1:]], axis=1)
            
            from matplotlib.collections import LineCollection
            lc = LineCollection(segments, cmap='viridis', linewidth=2)
            lc.set_array(np.linspace(0, 1, len(x_data)))
            line = ax.add_collection(lc)
            fig.colorbar(line, ax=ax, label='Normalized Time')
        else:
            ax.plot(x_data, y_data, linewidth=2, **kwargs)
        
        if show_direction:
            # Add arrows to show direction
            arrow_indices = np.linspace(0, len(x_data)-2, 5, dtype=int)
            for idx in arrow_indices:
                ax.annotate(
                    '', xy=(x_data[idx+1], y_data[idx+1]),
                    xytext=(x_data[idx], y_data[idx]),
                    arrowprops=dict(arrowstyle='->', lw=1.5, color='black')
                )
        
        # Mark equilibria
        if equilibria:
            eq_x, eq_y = zip(*equilibria)
            ax.scatter(eq_x, eq_y, s=100, c='red', marker='*', 
                      edgecolors='black', linewidth=1.5, 
                      label='Equilibria', zorder=5)
            ax.legend()
        
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        if title:
            ax.set_title(title)
        ax.set_aspect('auto')
        plt.tight_layout()
        
        return fig, ax
    
    def plot_vector_field(
        self,
        x_range: Tuple[float, float],
        y_range: Tuple[float, float],
        dx_func,
        dy_func,
        density: int = 20,
        figsize: Tuple[float, float] = (10, 8),
        **kwargs
    ) -> Tuple[plt.Figure, plt.Axes]:
        """
        Plot vector field for phase plane analysis.
        
        Parameters
        ----------
        x_range, y_range : Tuple[float, float]
            Ranges for x and y axes
        dx_func, dy_func : callable
            Functions computing dx/dt and dy/dt given (x, y)
        density : int
            Density of vector field grid
        figsize : Tuple[float, float]
            Figure size
        **kwargs
            Additional arguments passed to quiver
            
        Returns
        -------
        Tuple[plt.Figure, plt.Axes]
            Figure and axes objects
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        x = np.linspace(x_range[0], x_range[1], density)
        y = np.linspace(y_range[0], y_range[1], density)
        X, Y = np.meshgrid(x, y)
        
        U = np.zeros_like(X)
        V = np.zeros_like(Y)
        
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                U[i, j] = dx_func(X[i, j], Y[i, j])
                V[i, j] = dy_func(X[i, j], Y[i, j])
        
        # Normalize for better visualization
        M = np.sqrt(U**2 + V**2)
        M[M == 0] = 1  # Avoid division by zero
        U_norm = U / M
        V_norm = V / M
        
        ax.quiver(X, Y, U_norm, V_norm, M, cmap='viridis', alpha=0.6, **kwargs)
        ax.set_xlabel('State Variable 1')
        ax.set_ylabel('State Variable 2')
        ax.set_title('Phase Plane Vector Field')
        plt.tight_layout()
        
        return fig, ax


class Plot3D(PublicationPlotter):
    """
    Create publication-ready 3D plots for trajectories and surfaces.
    """
    
    def __init__(self, style: str = 'default'):
        """Initialize Plot3D plotter."""
        super().__init__(style)
    
    def plot_trajectory(
        self,
        x: np.ndarray,
        y: np.ndarray,
        z: np.ndarray,
        xlabel: str = 'X',
        ylabel: str = 'Y',
        zlabel: str = 'Z',
        title: Optional[str] = None,
        color_by_time: bool = True,
        figsize: Tuple[float, float] = (10, 8),
        **kwargs
    ) -> Tuple[plt.Figure, Axes3D]:
        """
        Plot 3D trajectory.
        
        Parameters
        ----------
        x, y, z : np.ndarray
            3D coordinates
        xlabel, ylabel, zlabel : str
            Axis labels
        title : Optional[str]
            Plot title
        color_by_time : bool
            Whether to color by time
        figsize : Tuple[float, float]
            Figure size
        **kwargs
            Additional arguments
            
        Returns
        -------
        Tuple[plt.Figure, Axes3D]
            Figure and 3D axes objects
        """
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111, projection='3d')
        
        if color_by_time:
            colors = plt.cm.viridis(np.linspace(0, 1, len(x)))
            for i in range(len(x) - 1):
                ax.plot(x[i:i+2], y[i:i+2], z[i:i+2], 
                       color=colors[i], linewidth=2)
        else:
            ax.plot(x, y, z, linewidth=2, **kwargs)
        
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_zlabel(zlabel)
        if title:
            ax.set_title(title)
        
        plt.tight_layout()
        return fig, ax
    
    def plot_surface(
        self,
        X: np.ndarray,
        Y: np.ndarray,
        Z: np.ndarray,
        xlabel: str = 'X',
        ylabel: str = 'Y',
        zlabel: str = 'Z',
        title: Optional[str] = None,
        cmap: str = 'viridis',
        alpha: float = 0.8,
        figsize: Tuple[float, float] = (12, 9),
        **kwargs
    ) -> Tuple[plt.Figure, Axes3D]:
        """
        Plot 3D surface.
        
        Parameters
        ----------
        X, Y, Z : np.ndarray
            2D arrays for surface coordinates
        xlabel, ylabel, zlabel : str
            Axis labels
        title : Optional[str]
            Plot title
        cmap : str
            Colormap name
        alpha : float
            Surface transparency
        figsize : Tuple[float, float]
            Figure size
        **kwargs
            Additional arguments passed to plot_surface
            
        Returns
        -------
        Tuple[plt.Figure, Axes3D]
            Figure and 3D axes objects
        """
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111, projection='3d')
        
        surf = ax.plot_surface(X, Y, Z, cmap=cmap, alpha=alpha, 
                              linewidth=0, antialiased=True, **kwargs)
        fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
        
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_zlabel(zlabel)
        if title:
            ax.set_title(title)
        
        plt.tight_layout()
        return fig, ax


class Heatmap(PublicationPlotter):
    """
    Create publication-ready heatmaps for parameter sensitivity and spatial patterns.
    """
    
    def __init__(self, style: str = 'default'):
        """Initialize Heatmap plotter."""
        super().__init__(style)
    
    def plot(
        self,
        data: np.ndarray,
        xlabel: str = 'X',
        ylabel: str = 'Y',
        title: Optional[str] = None,
        cmap: str = 'RdYlBu_r',
        vmin: Optional[float] = None,
        vmax: Optional[float] = None,
        cbar_label: str = 'Value',
        annotate: bool = False,
        figsize: Tuple[float, float] = (10, 8),
        xticklabels: Optional[List[str]] = None,
        yticklabels: Optional[List[str]] = None,
        **kwargs
    ) -> Tuple[plt.Figure, plt.Axes]:
        """
        Create a heatmap.
        
        Parameters
        ----------
        data : np.ndarray
            2D array to visualize
        xlabel, ylabel : str
            Axis labels
        title : Optional[str]
            Plot title
        cmap : str
            Colormap name
        vmin, vmax : Optional[float]
            Min and max values for colormap
        cbar_label : str
            Colorbar label
        annotate : bool
            Whether to annotate cells with values
        figsize : Tuple[float, float]
            Figure size
        xticklabels, yticklabels : Optional[List[str]]
            Tick labels
        **kwargs
            Additional arguments passed to imshow
            
        Returns
        -------
        Tuple[plt.Figure, plt.Axes]
            Figure and axes objects
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        im = ax.imshow(data, cmap=cmap, vmin=vmin, vmax=vmax, 
                      aspect='auto', **kwargs)
        
        cbar = fig.colorbar(im, ax=ax)
        cbar.set_label(cbar_label, rotation=270, labelpad=20)
        
        if xticklabels:
            ax.set_xticks(np.arange(len(xticklabels)))
            ax.set_xticklabels(xticklabels, rotation=45, ha='right')
        
        if yticklabels:
            ax.set_yticks(np.arange(len(yticklabels)))
            ax.set_yticklabels(yticklabels)
        
        if annotate:
            for i in range(data.shape[0]):
                for j in range(data.shape[1]):
                    text = ax.text(j, i, f'{data[i, j]:.2f}',
                                 ha="center", va="center", color="black")
        
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        if title:
            ax.set_title(title)
        
        plt.tight_layout()
        return fig, ax
    
    def plot_sensitivity(
        self,
        parameters: List[str],
        outputs: List[str],
        sensitivity_matrix: np.ndarray,
        figsize: Tuple[float, float] = (12, 8),
        **kwargs
    ) -> Tuple[plt.Figure, plt.Axes]:
        """
        Create a parameter sensitivity heatmap.
        
        Parameters
        ----------
        parameters : List[str]
            Parameter names
        outputs : List[str]
            Output variable names
        sensitivity_matrix : np.ndarray
            Sensitivity values (outputs x parameters)
        figsize : Tuple[float, float]
            Figure size
        **kwargs
            Additional arguments
            
        Returns
        -------
        Tuple[plt.Figure, plt.Axes]
            Figure and axes objects
        """
        return self.plot(
            sensitivity_matrix,
            xlabel='Parameters',
            ylabel='Output Variables',
            title='Parameter Sensitivity Analysis',
            xticklabels=parameters,
            yticklabels=outputs,
            cbar_label='Sensitivity',
            figsize=figsize,
            **kwargs
        )


class NetworkViz(PublicationPlotter):
    """
    Visualize cell-cell interaction networks and regulatory networks.
    """
    
    def __init__(self, style: str = 'default'):
        """Initialize NetworkViz plotter."""
        super().__init__(style)
    
    def plot_network(
        self,
        adjacency_matrix: np.ndarray,
        node_labels: Optional[List[str]] = None,
        node_colors: Optional[List[str]] = None,
        title: Optional[str] = None,
        layout: str = 'spring',
        figsize: Tuple[float, float] = (12, 10),
        **kwargs
    ) -> Tuple[plt.Figure, plt.Axes]:
        """
        Plot a network from an adjacency matrix.
        
        Parameters
        ----------
        adjacency_matrix : np.ndarray
            Adjacency matrix representing connections
        node_labels : Optional[List[str]]
            Labels for nodes
        node_colors : Optional[List[str]]
            Colors for nodes
        title : Optional[str]
            Plot title
        layout : str
            Network layout algorithm ('spring', 'circular', 'kamada_kawai')
        figsize : Tuple[float, float]
            Figure size
        **kwargs
            Additional arguments
            
        Returns
        -------
        Tuple[plt.Figure, plt.Axes]
            Figure and axes objects
        """
        try:
            import networkx as nx
        except ImportError:
            raise ImportError("NetworkX is required for network visualization. Install with: conda install networkx")
        
        fig, ax = plt.subplots(figsize=figsize)
        
        # Create graph from adjacency matrix
        G = nx.from_numpy_array(adjacency_matrix, create_using=nx.DiGraph)
        
        # Choose layout
        if layout == 'spring':
            pos = nx.spring_layout(G, k=0.5, iterations=50)
        elif layout == 'circular':
            pos = nx.circular_layout(G)
        elif layout == 'kamada_kawai':
            pos = nx.kamada_kawai_layout(G)
        else:
            pos = nx.spring_layout(G)
        
        # Set node labels
        if node_labels:
            labels = {i: label for i, label in enumerate(node_labels)}
        else:
            labels = {i: f'Node {i}' for i in range(len(adjacency_matrix))}
        
        # Draw network
        nx.draw_networkx_nodes(
            G, pos, ax=ax,
            node_color=node_colors if node_colors else 'lightblue',
            node_size=1000,
            alpha=0.9
        )
        nx.draw_networkx_labels(G, pos, labels, ax=ax, font_size=10)
        nx.draw_networkx_edges(
            G, pos, ax=ax,
            edge_color='gray',
            arrows=True,
            arrowsize=20,
            width=2,
            alpha=0.6
        )
        
        if title:
            ax.set_title(title)
        ax.axis('off')
        plt.tight_layout()
        
        return fig, ax


# Convenience function for quick plotting
def quick_plot(
    data: np.ndarray,
    plot_type: str = 'line',
    **kwargs
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Quick plotting function for rapid visualization.
    
    Parameters
    ----------
    data : np.ndarray
        Data to plot
    plot_type : str
        Type of plot ('line', 'scatter', 'heatmap', '3d')
    **kwargs
        Additional arguments passed to specific plotter
        
    Returns
    -------
    Tuple[plt.Figure, plt.Axes]
        Figure and axes objects
    """
    if plot_type == 'line':
        plotter = TimeSeries2D()
        time = np.arange(len(data))
        return plotter.plot(time, data, **kwargs)
    elif plot_type == 'heatmap':
        plotter = Heatmap()
        return plotter.plot(data, **kwargs)
    elif plot_type == '3d' and data.shape[1] >= 3:
        plotter = Plot3D()
        return plotter.plot_trajectory(data[:, 0], data[:, 1], data[:, 2], **kwargs)
    else:
        raise ValueError(f"Unknown plot type: {plot_type}")
