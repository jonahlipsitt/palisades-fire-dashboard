"""
Authentication module for Google Earth Engine Dashboard

Handles authentication for Google Earth Engine and other services.
"""

from .gee_auth import initialize_ee

__all__ = [
    'initialize_ee'
]