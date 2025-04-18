"""
Default configurations for the rescue application.
"""

import numpy as np
from ..utils.coordinates import DegreesToDecimalVec

# Default rescue stations with their coordinates and speeds
DEFAULT_STATIONS = [
    ('ЦСПС', round(DegreesToDecimalVec((59, 58, 56)), 4), round(DegreesToDecimalVec((30, 13, 19)), 4), 40.0),
    ('СПС-1', round(DegreesToDecimalVec((60, 11, 17)), 4), round(DegreesToDecimalVec((29, 41, 39)), 4), 40.0),
    ('СПС-13', round(DegreesToDecimalVec((60, 9, 46)), 4), round(DegreesToDecimalVec((29, 51, 29)), 4), 40.0),
    ('СПС-23', round(DegreesToDecimalVec((60, 8, 44)), 4), round(DegreesToDecimalVec((29, 55, 30)), 4), 40.0),
    ('СПС-3', round(DegreesToDecimalVec((60, 5, 31)), 4), round(DegreesToDecimalVec((29, 55, 51)), 4), 40.0),
    ('СПС-19', round(DegreesToDecimalVec((60, 0, 41.868)), 4), round(DegreesToDecimalVec((29, 57, 52.085)), 4), 40.0),
    ('СПС-22', round(DegreesToDecimalVec((59, 51, 42)), 4), round(DegreesToDecimalVec((30, 8, 4)), 4), 40.0),
    ('СПС-10', round(DegreesToDecimalVec((59, 51, 45)), 4), round(DegreesToDecimalVec((30, 2, 44)), 4), 40.0),
    ('СПС-30', round(DegreesToDecimalVec((59, 54, 33)), 4), round(DegreesToDecimalVec((29, 48, 38)), 4), 40.0),
    ('СПС-21', round(DegreesToDecimalVec((60, 0, 18.211)), 4), round(DegreesToDecimalVec((29, 43, 0.272)), 4), 40.0),
]

# Default station coordinates in degrees, minutes, seconds format
DEFAULT_STATION_COORDS = np.array([
    ((59, 58, 56), (30, 13, 19)),
    ((60, 11, 17), (29, 41, 39)),
    ((60, 9, 46), (29, 51, 29)),
    ((60, 8, 44), (29, 55, 30)),
    ((60, 5, 31), (29, 55, 51)),
    ((60, 0, 41.868), (29, 57, 52.085)),
    ((59, 51, 42), (30, 8, 4)),
    ((59, 51, 45), (30, 2, 44)),
    ((59, 54, 33), (29, 48, 38)),
    ((60, 0, 18.211), (29, 43, 0.272)),  # kron
])

# Default station velocities in km/h
DEFAULT_VELOCITIES = np.array([40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0])

# Default experiment parameters
DEFAULT_EXPERIMENT_PARAMS = {
    'cases_number': 5000,        # Number of emergency cases to simulate
    'median_lifespan': 10,       # Median survival time in minutes
    'max_lifespan': 25,          # Maximum survival time in minutes
    'mesh_width': 70,            # Width of graph mesh cells
    'check_freq': 40             # Frequency of checks for graph method
} 