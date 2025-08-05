"""
Google Earth Engine Authentication Module

Handles authentication and initialization for Google Earth Engine.
"""

import os
import ee
import pyproj
from pathlib import Path
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


def set_proj_data():
    """
    Set PROJ_DATA environment variable to avoid projection errors.
    
    This addresses common PROJ data directory issues in GEE Python environments.
    """
    try:
        # Try to set PROJ_DATA automatically
        pyproj.datadir.set_data_dir()
        
        # Also set environment variables for conda environments
        conda_prefix = os.environ.get('CONDA_PREFIX')
        if conda_prefix:
            proj_data_path = os.path.join(conda_prefix, 'share', 'proj')
            if os.path.exists(proj_data_path):
                os.environ['PROJ_DATA'] = proj_data_path
                os.environ['PROJ_LIB'] = proj_data_path
                logger.info(f"Set PROJ_DATA to: {proj_data_path}")
    except Exception as e:
        logger.warning(f"Could not set PROJ_DATA automatically: {e}")


def initialize_ee(
    project_id: Optional[str] = None,
    use_service_account: bool = False,
    credentials_path: Optional[str] = None,
    use_high_volume: bool = False
) -> bool:
    """
    Initialize Earth Engine with proper authentication.
    
    Args:
        project_id: Google Cloud Project ID for Earth Engine
        use_service_account: Whether to use service account authentication
        credentials_path: Path to service account credentials file
        use_high_volume: Whether to use high-volume endpoint
        
    Returns:
        bool: True if initialization successful, False otherwise
        
    Raises:
        ValueError: If required parameters are missing
        ee.EEException: If Earth Engine initialization fails
    """
    try:
        # Set PROJ data to avoid projection errors
        set_proj_data()
        
        # Get project ID from environment if not provided
        if not project_id:
            project_id = os.getenv('GEE_PROJECT_ID')
            if not project_id:
                raise ValueError("Project ID must be provided or set in GEE_PROJECT_ID environment variable")
        
        if use_service_account:
            # Production: service account authentication
            if not credentials_path:
                credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
            
            if not credentials_path or not os.path.exists(credentials_path):
                raise ValueError(
                    "Service account credentials file not found. "
                    "Set GOOGLE_APPLICATION_CREDENTIALS environment variable or provide credentials_path."
                )
            
            credentials = ee.ServiceAccountCredentials(
                email=None,  # Will be read from credentials file
                key_file=credentials_path
            )
            
            # Set high-volume endpoint if requested
            if use_high_volume:
                ee.Initialize(
                    credentials,
                    project=project_id,
                    url='https://earthengine-highvolume.googleapis.com'
                )
            else:
                ee.Initialize(credentials, project=project_id)
                
            logger.info(f"Initialized Earth Engine with service account for project: {project_id}")
            
        else:
            # Development: user authentication
            try:
                # Try to initialize with existing credentials
                ee.Initialize(project=project_id)
                logger.info(f"Initialized Earth Engine with existing credentials for project: {project_id}")
            except ee.EEException:
                # If that fails, authenticate first
                logger.info("Existing credentials not found, starting authentication...")
                ee.Authenticate()
                ee.Initialize(project=project_id)
                logger.info(f"Authenticated and initialized Earth Engine for project: {project_id}")
        
        # Test the connection
        test_connection()
        return True
        
    except Exception as e:
        logger.error(f"Failed to initialize Earth Engine: {e}")
        return False


def test_connection() -> bool:
    """
    Test the Earth Engine connection by making a simple request.
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        # Simple test to verify connection
        image = ee.Image(1)
        info = image.getInfo()
        logger.info("Earth Engine connection test successful")
        return True
    except Exception as e:
        logger.error(f"Earth Engine connection test failed: {e}")
        return False


# Configuration constants for Earth Engine operations
DEFAULT_CONFIG = {
    'max_pixels': 1e9,
    'scale': 30,
    'crs': 'EPSG:4326',
    'timeout': 300
}