"""
Project constants and configuration values
"""

import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
INPUTS_DIR = PROJECT_ROOT / "inputs"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
CONFIG_DIR = PROJECT_ROOT / "config"
ASSETS_DIR = PROJECT_ROOT / "assets"

# Data directories
RAW_DATA_DIR = INPUTS_DIR / "raw"
PROCESSED_DATA_DIR = INPUTS_DIR / "processed"
REFERENCE_DATA_DIR = INPUTS_DIR / "reference"

# Output directories
EXPORTS_DIR = OUTPUTS_DIR / "exports"
FIGURES_DIR = OUTPUTS_DIR / "figures"
REPORTS_DIR = OUTPUTS_DIR / "reports"
TILES_DIR = OUTPUTS_DIR / "tiles"

# Google Earth Engine settings
GEE_PROJECT_ID = os.getenv('GEE_PROJECT_ID', 'your-project-id')
GEE_MAX_PIXELS = int(os.getenv('GEE_MAX_PIXELS', '1000000000'))
GEE_DEFAULT_SCALE = int(os.getenv('GEE_DEFAULT_SCALE', '30'))
GEE_DEFAULT_CRS = os.getenv('GEE_DEFAULT_CRS', 'EPSG:4326')

# Dashboard settings - Configured for Palisades Fire Analysis
DASHBOARD_TITLE = os.getenv('DASHBOARD_TITLE', 'Palisades Fire Analysis Dashboard')
DASHBOARD_PORT = int(os.getenv('DASHBOARD_PORT', '8501'))
DASHBOARD_HOST = os.getenv('DASHBOARD_HOST', 'localhost')

# Map settings - Centered on Palisades Fire area
DEFAULT_MAP_CENTER = [
    float(os.getenv('DEFAULT_MAP_CENTER_LAT', '34.0725')),  # Palisades Fire latitude
    float(os.getenv('DEFAULT_MAP_CENTER_LON', '-118.5425'))  # Palisades Fire longitude
]
DEFAULT_MAP_ZOOM = int(os.getenv('DEFAULT_MAP_ZOOM', '12'))  # Zoomed in for fire analysis

# Palisades Fire specific constants
PALISADES_FIRE_CENTER = [34.0725, -118.5425]
PALISADES_FIRE_BBOX = [-118.65, 34.0, -118.45, 34.15]  # [west, south, east, north]
PALISADES_FIRE_START_DATE = "2025-01-07"
PALISADES_FIRE_SIZE_ACRES = 23713
PALISADES_FIRE_SIZE_HECTARES = 9593  # Approximately

# Visualization palettes
PALETTES = {
    'elevation': ['006633', 'E5FFCC', '662A00', 'D8D8D8', 'F5F5F5'],
    'ndvi': ['FFFFFF', 'CE7E45', 'DF923D', 'F1B555', 'FCD163', '99B718', 
             '74A901', '66A000', '529400', '3E8601', '207401', '056201', 
             '004C00', '023B01', '012E01', '011D01', '011301'],
    'temperature': ['blue', 'cyan', 'yellow', 'orange', 'red'],
    'precipitation': ['white', 'lightblue', 'blue', 'darkblue', 'purple'],
    'landcover': ['419BDF', '397D49', '88B053', '7A87C6', 'E49635', 
                  'DFC35A', 'C4281B', 'A59B8F', 'B39FE1']
}

# Sentinel-2 band combinations (used in fire analysis)
BAND_COMBINATIONS = {
    'sentinel2_rgb': ['B4', 'B3', 'B2'],
    'sentinel2_nir': ['B8', 'B4', 'B3'],
    'sentinel2_agriculture': ['B11', 'B8', 'B2'],
    'sentinel2_fire_analysis': ['B12', 'B8', 'B4']  # SWIR, NIR, Red for fire detection
}

# Fire analysis visualization parameters
FIRE_VIS_PARAMS = {
    'sentinel_rgb': {
        'bands': ['B4', 'B3', 'B2'],
        'min': 0.0,
        'max': 3000,
        'gamma': 1.4
    },
    'nbr': {
        'min': -1,
        'max': 1,
        'palette': ['red', 'yellow', 'green']
    },
    'dnbr': {
        'min': -0.5,
        'max': 1.0,
        'palette': ['green', 'yellow', 'orange', 'red', 'purple']
    },
    'burn_severity': {
        'min': 0,
        'max': 5,
        'palette': ['white', 'green', 'yellow', 'orange', 'red', 'purple']
    }
}

# File formats
SUPPORTED_VECTOR_FORMATS = ['.shp', '.geojson', '.kml', '.gpx']
SUPPORTED_RASTER_FORMATS = ['.tif', '.tiff', '.nc', '.hdf', '.he5']
SUPPORTED_TABLE_FORMATS = ['.csv', '.xlsx', '.json', '.parquet']

# Performance settings
MEMORY_LIMIT = os.getenv('MEMORY_LIMIT', '2GB')
MAX_WORKERS = int(os.getenv('MAX_WORKERS', '4'))
CACHE_TIMEOUT = int(os.getenv('CACHE_TIMEOUT', '3600'))

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# API endpoints
GEE_API_URL = 'https://earthengine.googleapis.com'
GEE_HIGH_VOLUME_URL = 'https://earthengine-highvolume.googleapis.com'

# Error messages
ERROR_MESSAGES = {
    'auth_failed': 'Google Earth Engine authentication failed',
    'project_not_found': 'GEE project not found or access denied',
    'data_not_found': 'Requested data not found',
    'export_failed': 'Data export failed',
    'processing_error': 'Data processing error',
    'visualization_error': 'Visualization creation failed'
}