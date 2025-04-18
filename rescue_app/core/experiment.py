"""
Experiment module for running simulations and calculations.
"""

import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict, Any, Optional
from PyQt6 import QtWidgets

# Import necessary modules from the project
from ..models import Station
from ..utils.coordinates import DecimalToDegrees
from ..utils.project_functions import (
    makeGraph, expMakeLine, expMakeGraph, ClosestPathWithTraceNew,
    ClosestPathWithTraceDijkstra, PlotMap, PlotMapReachability,
    PlotMapDifStReachability, probsFromTimes
)


class Experiment:
    """
    Class for running rescue simulations and analyzing results.
    """
    
    def __init__(self):
        """Initialize the experiment."""
        self.stationCoords = None
        self.velocities = None
        self.cases_number = 5000
        self.median_lifespan = 10
        self.max_lifespan = 25
        self.mesh_width = 70
        self.check_freq = 40
        self.graph = None
        self.graph_mesh = None
        self.graph_mask = None
        self.show_station_names = True
        self.plot_dpi = 100
    
    def set_parameters(self, 
                       cases_number: int = None,
                       median_lifespan: float = None,
                       max_lifespan: float = None,
                       mesh_width: int = None,
                       check_freq: int = None,
                       show_station_names: bool = None,
                       plot_dpi: int = None):
        """
        Set experiment parameters.
        
        Args:
            cases_number (int): Number of emergency cases to simulate
            median_lifespan (float): Median survival time in minutes
            max_lifespan (float): Maximum survival time in minutes
            mesh_width (int): Width of graph mesh cells
            check_freq (int): Frequency of checks for graph method
            show_station_names (bool): Whether to show station names on plots
            plot_dpi (int): DPI resolution for generated plots
        """
        if cases_number is not None:
            self.cases_number = cases_number
        if median_lifespan is not None:
            self.median_lifespan = median_lifespan
        if max_lifespan is not None:
            self.max_lifespan = max_lifespan
        if mesh_width is not None:
            self.mesh_width = mesh_width
        if check_freq is not None:
            self.check_freq = check_freq
        if show_station_names is not None:
            self.show_station_names = show_station_names
        if plot_dpi is not None:
            self.plot_dpi = plot_dpi
    
    def set_stations(self, stationCoords, velocities):
        """
        Set station coordinates and velocities.
        
        Args:
            stationCoords (np.ndarray): Array of station coordinates
            velocities (np.ndarray): Array of station velocities
        """
        self.stationCoords = stationCoords
        self.velocities = velocities
    
    def generate_graph(self) -> bool:
        """
        Generate a graph for the experiment.
        
        Returns:
            bool: True if a new graph was generated, False if loaded from cache
        """
        if os.path.isfile(f'graphs/saved_graph_{self.mesh_width}_{self.check_freq}.pkl'):
            # Load existing graph
            with open(f'graphs/saved_graph_{self.mesh_width}_{self.check_freq}.pkl', 'rb') as f:
                data = pickle.load(f)
                self.graph = data['G']
                self.graph_mesh = data['Gmesh']
                self.graph_mask = data['Gmask']
            return False
        else:
            # Generate new graph
            G, Gmesh, Gmask = makeGraph(self.mesh_width, self.check_freq)
            self.graph = G
            self.graph_mesh = Gmesh
            self.graph_mask = Gmask
            
            # Save graph for future use
            if not os.path.exists('graphs'):
                os.makedirs('graphs')
                
            with open(f'graphs/saved_graph_{self.mesh_width}_{self.check_freq}.pkl', 'wb') as f:
                pickle.dump({'G': G, 'Gmesh': Gmesh, 'Gmask': Gmask}, f)
            return True
            
    def run_experiment_line(self) -> Tuple[List[float], List[str]]:
        """
        Run an experiment using the line method.
        
        Returns:
            Tuple[List[float], List[str]]: Metrics values and generated image paths
        """
        if not os.path.exists('output'):
            os.makedirs('output')
            
        # Configure matplotlib for plot quality
        plt.rcParams['figure.dpi'] = self.plot_dpi
        plt.rcParams['savefig.dpi'] = self.plot_dpi
            
        ptsFromPix, ptsToPix, ptsToMinTimes, plotData = expMakeLine(
            self.stationCoords, self.velocities, self.cases_number
        )
        
        # Calculate metrics
        values = [
            round(np.mean(ptsToMinTimes) * 60, 3),
            round(np.max(ptsToMinTimes) * 60, 3),
            round(probsFromTimes(np.max(ptsToMinTimes) * 60 + 1.5, self.median_lifespan, self.max_lifespan).mean(), 3),
            round(probsFromTimes(ptsToMinTimes * 60 + 1.5, self.median_lifespan, self.max_lifespan).mean(), 3)
        ]
        
        # Generate the plots
        images = []
        
        # Use actual Station objects if available from the main window
        from ..ui.main_window import MainWindow
        stations = None
        
        # Look for the main window to get actual station objects
        for widget in QtWidgets.QApplication.topLevelWidgets():
            if isinstance(widget, MainWindow):
                stations = widget.stations
                break
        
        # If we couldn't get station objects from the main window, create temporary ones
        if not stations:
            stations = []
            for i, (coords, velocity) in enumerate(zip(self.stationCoords, self.velocities)):
                # Extract coordinates
                lat_deg, lat_min, lat_sec = coords[0]
                lon_deg, lon_min, lon_sec = coords[1]
                
                # Create a temporary station object
                station = Station(f"Станция {i+1}", lat_deg, lon_deg, velocity)
                stations.append(station)
        
        # Plot closest paths with station names if enabled
        PlotMap(ptsFromPix, ptsToPix, plotData, 0.75, True, True, stations=stations if self.show_station_names else None)
        images.append("output/plot_example.png")

        # Generate data for reachability plots
        width = 4113
        height = 3145
        l = 7
        nxt, nyt = (int(width / l), int(height / l))
        x = np.linspace(0, width, nxt)
        y = np.linspace(0, height, nyt)
        xv, yv = np.meshgrid(x, y)
        x = xv.flatten()
        y = yv.flatten()
        yrev = -(y - height)
        ptsToPix = np.append(np.array([x]), np.array([yrev]), axis=0).T

        ptsToPix, ptsToMinTimes, plotData = ClosestPathWithTraceNew(ptsFromPix, ptsToPix, self.velocities)
        
        # Plot reachability with station names if enabled
        PlotMapReachability(ptsFromPix, ptsToPix, plotData, 1, True, True, stations=stations if self.show_station_names else None)
        images.append("output/plot_reachability_example.png")
        
        # Plot responsibility zones with station names if enabled
        PlotMapDifStReachability(ptsFromPix, ptsToPix, plotData, 1, True, True, stations=stations if self.show_station_names else None)
        images.append("output/plot_reachability_difSt_example.png")
        
        return values, images
    
    def run_experiment_graph(self) -> Tuple[List[float], List[str]]:
        """
        Run an experiment using the graph method.
        
        Returns:
            Tuple[List[float], List[str]]: Metrics values and generated image paths
        """
        if not os.path.exists('output'):
            os.makedirs('output')
            
        # Configure matplotlib for plot quality
        plt.rcParams['figure.dpi'] = self.plot_dpi
        plt.rcParams['savefig.dpi'] = self.plot_dpi
            
        # Ensure we have a graph
        if self.graph is None:
            self.generate_graph()
            
        ptsFromPix, ptsToPix, ptsToMinTimes, plotData = expMakeGraph(
            self.stationCoords, self.velocities, self.cases_number, 
            self.graph, self.graph_mesh, self.graph_mask
        )
        
        # Calculate metrics
        values = [
            round(np.mean(ptsToMinTimes) * 60, 2),
            round(np.max(ptsToMinTimes) * 60, 2),
            round(probsFromTimes(np.max(ptsToMinTimes) * 60 + 1.5, self.median_lifespan, self.max_lifespan).mean(), 3),
            round(probsFromTimes(ptsToMinTimes * 60 + 1.5, self.median_lifespan, self.max_lifespan).mean(), 3)
        ]
        
        # Generate the plots
        images = []
        
        # Use actual Station objects if available from the main window
        from ..ui.main_window import MainWindow
        stations = None
        
        # Look for the main window to get actual station objects
        for widget in QtWidgets.QApplication.topLevelWidgets():
            if isinstance(widget, MainWindow):
                stations = widget.stations
                break
        
        # If we couldn't get station objects from the main window, create temporary ones
        if not stations:
            stations = []
            for i, (coords, velocity) in enumerate(zip(self.stationCoords, self.velocities)):
                # Extract coordinates
                lat_deg, lat_min, lat_sec = coords[0]
                lon_deg, lon_min, lon_sec = coords[1]
                
                # Create a temporary station object
                station = Station(f"Станция {i+1}", lat_deg, lon_deg, velocity)
                stations.append(station)
        
        # Plot closest paths with station names if enabled
        PlotMap(ptsFromPix, ptsToPix, plotData, 0.75, True, True, stations=stations if self.show_station_names else None)
        images.append("output/plot_example.png")

        # Generate data for reachability plots
        width = 4113
        height = 3145
        l = 7
        nxt, nyt = (int(width / l), int(height / l))
        x = np.linspace(0, width, nxt)
        y = np.linspace(0, height, nyt)
        xv, yv = np.meshgrid(x, y)
        x = xv.flatten()
        y = yv.flatten()
        yrev = -(y - height)
        ptsToPix = np.append(np.array([x]), np.array([yrev]), axis=0).T

        ptsToPix, ptsToMinTimes, plotData = ClosestPathWithTraceDijkstra(
            ptsFromPix, ptsToPix, self.velocities, 
            self.graph, self.graph_mesh, self.graph_mask
        )
        
        # Plot reachability with station names if enabled
        PlotMapReachability(ptsFromPix, ptsToPix, plotData, 1, True, True, stations=stations if self.show_station_names else None)
        images.append("output/plot_reachability_example.png")
        
        # Plot responsibility zones with station names if enabled
        PlotMapDifStReachability(ptsFromPix, ptsToPix, plotData, 1, True, True, stations=stations if self.show_station_names else None)
        images.append("output/plot_reachability_difSt_example.png")
        
        return values, images 