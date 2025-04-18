"""
Configuration settings for the rescue application.
"""

import numpy as np
from ..utils.coordinates import DegreesToDecimalVec

# Define default stations data
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
    ((60, 0, 18.211), (29, 43, 0.272)),
])

DEFAULT_VELOCITIES = np.array([40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0])

# Default experiment parameters
DEFAULT_CASES_NUMBER = 5000
DEFAULT_MEDIAN_LIFESPAN = 10
DEFAULT_MAX_LIFESPAN = 25
DEFAULT_MESH_WIDTH = 70
DEFAULT_CHECK_FREQ = 40

# Output directory
OUTPUT_DIR = "output"
GRAPHS_DIR = "graphs"

# Ensure directories exist
import os
for directory in [OUTPUT_DIR, GRAPHS_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)

__all__ = [
    'DEFAULT_STATIONS', 'DEFAULT_STATION_COORDS',
    'DEFAULT_VELOCITIES', 'DEFAULT_CASES_NUMBER',
    'DEFAULT_MEDIAN_LIFESPAN', 'DEFAULT_MAX_LIFESPAN',
    'DEFAULT_MESH_WIDTH', 'DEFAULT_CHECK_FREQ',
    'OUTPUT_DIR', 'GRAPHS_DIR'
] 