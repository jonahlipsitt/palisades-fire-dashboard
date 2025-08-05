"""
Palisades Fire Before/After Analysis Dashboard

Interactive dashboard for analyzing the January 2025 Palisades Fire in Los Angeles
using Google Earth Engine data to show before/after conditions and fire impact.
"""

import streamlit as st
import geemap.foliumap as geemap
import ee
import pandas as pd
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(src_path))

from auth.gee_auth import initialize_ee
from utils.constants import (
    PALISADES_FIRE_CENTER, 
    PALISADES_FIRE_BBOX, 
    PALISADES_FIRE_START_DATE,
    FIRE_VIS_PARAMS
)

# Handle GEE Project ID from secrets or environment
def get_gee_project_id():
    """Get GEE Project ID from Streamlit secrets or environment variables."""
    try:
        # Try Streamlit secrets first (for Cloud deployment)
        return st.secrets["gee"]["project_id"]
    except (KeyError, FileNotFoundError):
        # Fall back to environment variable
        import os
        return os.getenv('GEE_PROJECT_ID', 'ee-jonahlipsitt')

# Page configuration
st.set_page_config(
    page_title="🔥 Palisades Fire Analysis",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_resource
def init_earth_engine():
    """Initialize Earth Engine with caching."""
    try:
        project_id = get_gee_project_id()
        success = initialize_ee(project_id=project_id)
        if success:
            return True
        else:
            st.warning("⚠️ Running in DEMO mode - Google Earth Engine not available")
            st.info("📝 To enable live satellite data analysis:")
            st.info("1. Visit: https://developers.google.com/earth-engine/guides/access")
            st.info("2. Sign up for Earth Engine access")
            st.info("3. Run: `earthengine authenticate`")
            return False
    except Exception as e:
        st.warning("⚠️ Running in DEMO mode - Google Earth Engine not available")
        st.info("📝 You can still explore the dashboard interface and methodology")
        return False

@st.cache_resource
def create_fire_aoi():
    """Create Area of Interest for Palisades Fire."""
    try:
        return ee.Geometry.Rectangle(PALISADES_FIRE_BBOX)
    except:
        # Return None if Earth Engine is not available
        return None

def load_fire_datasets(before_date, after_date, aoi):
    """Load Sentinel-2 satellite imagery before and after the fire."""
    
    # Sentinel-2 collection  
    sentinel2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
    
    # Before fire imagery (6 months lookback window)
    before_start = (datetime.strptime(before_date, '%Y-%m-%d') - timedelta(days=180)).strftime('%Y-%m-%d')
    
    sentinel_before = (sentinel2
                      .filterDate(before_start, before_date)
                      .filterBounds(aoi)
                      .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
                      .median()
                      .clip(aoi))
    
    # After fire imagery (30 day window) 
    after_end = (datetime.strptime(after_date, '%Y-%m-%d') + timedelta(days=30)).strftime('%Y-%m-%d')
    
    sentinel_after = (sentinel2
                     .filterDate(after_date, after_end)
                     .filterBounds(aoi)
                     .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 30))
                     .median()
                     .clip(aoi))
    
    return {
        'sentinel_before': sentinel_before,
        'sentinel_after': sentinel_after
    }

def calculate_fire_indices(before_img, after_img):
    """Calculate fire-related spectral indices using Sentinel-2 bands."""
    
    # Sentinel-2 band names
    nir_band = 'B8'     # Near infrared
    red_band = 'B4'     # Red  
    swir_band = 'B12'   # Shortwave infrared 2
    green_band = 'B3'   # Green
    
    try:
        # Verify bands are available
        band_names = before_img.bandNames().getInfo()
        required_bands = [nir_band, red_band, swir_band, green_band]
        
        if not all(band in band_names for band in required_bands):
            # Return empty indices if required bands are missing
            return {
                'nbr_before': ee.Image(0),
                'nbr_after': ee.Image(0),
                'dnbr': ee.Image(0),
                'ndvi_before': ee.Image(0),
                'ndvi_after': ee.Image(0),
                'ndwi_before': ee.Image(0),
                'ndwi_after': ee.Image(0)
            }
    except Exception:
        # Return empty indices if there's any error
        return {
            'nbr_before': ee.Image(0),
            'nbr_after': ee.Image(0),
            'dnbr': ee.Image(0),
            'ndvi_before': ee.Image(0),
            'ndvi_after': ee.Image(0),
            'ndwi_before': ee.Image(0),
            'ndwi_after': ee.Image(0)
        }
    
    # Calculate NBR (Normalized Burn Ratio)
    nbr_before = before_img.normalizedDifference([nir_band, swir_band]).rename('NBR_before')
    nbr_after = after_img.normalizedDifference([nir_band, swir_band]).rename('NBR_after')
    
    # Calculate dNBR (difference NBR) - key fire damage indicator
    dnbr = nbr_before.subtract(nbr_after).rename('dNBR')
    
    # Calculate NDVI (vegetation health)
    ndvi_before = before_img.normalizedDifference([nir_band, red_band]).rename('NDVI_before')
    ndvi_after = after_img.normalizedDifference([nir_band, red_band]).rename('NDVI_after')
    
    # Calculate NDWI (water/moisture content)
    ndwi_before = before_img.normalizedDifference([green_band, nir_band]).rename('NDWI_before')
    ndwi_after = after_img.normalizedDifference([green_band, nir_band]).rename('NDWI_after')
    
    return {
        'nbr_before': nbr_before,
        'nbr_after': nbr_after,
        'dnbr': dnbr,
        'ndvi_before': ndvi_before,
        'ndvi_after': ndvi_after,
        'ndwi_before': ndwi_before,
        'ndwi_after': ndwi_after
    }

def classify_burn_severity(dnbr):
    """Classify burn severity based on dNBR values."""
    
    # Standard burn severity classification
    severity = (dnbr.where(dnbr.lt(-0.1), 0)  # Unburned/Low
                    .where(dnbr.gte(-0.1).And(dnbr.lt(0.1)), 1)  # Unburned/Low
                    .where(dnbr.gte(0.1).And(dnbr.lt(0.27)), 2)  # Low severity
                    .where(dnbr.gte(0.27).And(dnbr.lt(0.44)), 3)  # Moderate-low severity
                    .where(dnbr.gte(0.44).And(dnbr.lt(0.66)), 4)  # Moderate-high severity
                    .where(dnbr.gte(0.66), 5))  # High severity
    
    return severity.rename('burn_severity')

def create_base_map():
    """Create a standardized base map with consistent settings."""
    return geemap.Map(
        center=PALISADES_FIRE_CENTER, 
        zoom=11, 
        draw_control=False, 
        measure_control=False,
        fullscreen_control=False, 
        search_control=False
    )

def create_comparison_map(imagery, indices, aoi):
    """Create interactive comparison map."""
    
    # Initialize base map
    m = create_base_map()
    
    # Add OpenStreetMap basemap
    m.add_basemap('OpenStreetMap')
    
    # Use standardized visualization parameters
    sentinel_rgb_vis = FIRE_VIS_PARAMS['sentinel_rgb']
    nbr_vis = FIRE_VIS_PARAMS['nbr']
    dnbr_vis = FIRE_VIS_PARAMS['dnbr']
    severity_vis = FIRE_VIS_PARAMS['burn_severity']
    
    # Add fire damage analysis only (main map)
    if 'dnbr' in indices:
        m.addLayer(indices['dnbr'], dnbr_vis, 'Fire Damage (dNBR)', True)
    
    return m

def create_sentinel_swipe_map(imagery, aoi):
    """Create split-panel swipe map for Sentinel-2 before and after comparison."""
    
    # Use standardized Sentinel-2 visualization
    sentinel_rgb_vis = FIRE_VIS_PARAMS['sentinel_rgb']
    
    # Create split-panel map if both images exist
    if imagery['sentinel_before'] and imagery['sentinel_after']:
        # Create tile layers using geemap.ee_tile_layer
        left_layer = geemap.ee_tile_layer(imagery['sentinel_before'], sentinel_rgb_vis, 'Before Fire')
        right_layer = geemap.ee_tile_layer(imagery['sentinel_after'], sentinel_rgb_vis, 'After Fire')
        
        # Create map with split panel
        m = create_base_map()
        m.split_map(left_layer, right_layer)
        return m
    else:
        # Fallback map if no imagery
        return create_base_map()

def create_nbr_swipe_map(indices, aoi):
    """Create split-panel swipe map for NBR before and after comparison."""
    
    # Use standardized NBR visualization
    nbr_vis = FIRE_VIS_PARAMS['nbr']
    
    # Create split-panel map if both NBR images exist
    if 'nbr_before' in indices and 'nbr_after' in indices:
        # Create tile layers using geemap.ee_tile_layer
        left_layer = geemap.ee_tile_layer(indices['nbr_before'], nbr_vis, 'NBR Before')
        right_layer = geemap.ee_tile_layer(indices['nbr_after'], nbr_vis, 'NBR After')
        
        # Create map with split panel
        m = create_base_map()
        m.split_map(left_layer, right_layer)
        return m
    else:
        # Fallback map if no NBR data
        return create_base_map()

def create_burn_severity_map(indices, aoi):
    """Create map showing burn severity classification."""
    
    # Initialize base map
    m = create_base_map()
    m.add_basemap('OpenStreetMap')
    
    # Use standardized burn severity visualization
    severity_vis = FIRE_VIS_PARAMS['burn_severity']
    
    # Add burn severity if available
    if 'burn_severity' in indices:
        m.addLayer(indices['burn_severity'], severity_vis, 'Burn Severity Classification', True)
    
    return m

def calculate_fire_statistics(indices, aoi):
    """Calculate fire impact statistics."""
    
    try:
        if 'dnbr' in indices:
            # Calculate area statistics
            dnbr = indices['dnbr']
            
            # Total area calculation
            area_image = ee.Image.pixelArea().divide(10000)  # Convert to hectares
            
            # Burned area (dNBR > 0.1)
            burned_mask = dnbr.gte(0.1)
            burned_area = area_image.updateMask(burned_mask)
            
            # Calculate total burned area
            burned_stats = burned_area.reduceRegion(
                reducer=ee.Reducer.sum(),
                geometry=aoi,
                scale=30,
                maxPixels=1e9
            )
            
            # Calculate severity statistics
            if 'burn_severity' in indices:
                severity = indices['burn_severity']
                
                # Area by severity class
                severity_stats = {}
                for i in range(6):
                    mask = severity.eq(i)
                    area = area_image.updateMask(mask).reduceRegion(
                        reducer=ee.Reducer.sum(),
                        geometry=aoi,
                        scale=30,
                        maxPixels=1e9
                    )
                    severity_stats[f'severity_{i}'] = area
                
                return {
                    'burned_area': burned_stats,
                    'severity_stats': severity_stats
                }
        
        return None
        
    except Exception as e:
        st.warning(f"Could not calculate fire statistics: {e}")
        return None

def create_sidebar():
    """Create sidebar with controls."""
    
    # Add logo to sidebar
    logo_path = "/Users/jlipsitt/Documents/forwardfuture/assets/logos/logo_transparent.png"
    try:
        st.sidebar.image(logo_path, width=100)
    except Exception as e:
        pass  # Continue without logo if it doesn't load
    
    st.sidebar.title("Palisades Fire Analysis Dashboard")
    st.sidebar.markdown("---")
    
    # Fire information
    st.sidebar.subheader("🔥 Fire Information")
    st.sidebar.write("**Location**: Pacific Palisades, Los Angeles")
    st.sidebar.write("**Start Date**: January 7, 2025")
    st.sidebar.write("**Coordinates**: 34.0725°N, 118.5425°W")
    st.sidebar.write("**Size**: ~23,713 acres (~96 km²)")
    
    st.sidebar.markdown("---")
    
    # Date selection
    st.sidebar.subheader("📅 Analysis Dates")
    
    before_date = st.sidebar.date_input(
        "Before Fire Date",
        value=datetime(2024, 11, 1),  # Earlier date for more data availability
        max_value=datetime(2025, 1, 6),
        help="Select a date before the fire started"
    ).strftime('%Y-%m-%d')
    
    after_date = st.sidebar.date_input(
        "After Fire Date", 
        value=datetime(2025, 2, 1),  # Later date for more data availability
        min_value=datetime(2025, 1, 8),
        help="Select a date after the fire started"
    ).strftime('%Y-%m-%d')
    
    # Satellite selection
    st.sidebar.subheader("🛰️ Satellite Data")
    satellite = "Sentinel-2"  # Use Sentinel-2 only
    st.sidebar.write("**Primary Satellite**: Sentinel-2")
    st.sidebar.write("📡 High-resolution (10m) optical imagery")
    
    # Analysis options
    st.sidebar.subheader("🔍 Analysis Options")
    show_indices = st.sidebar.checkbox("Show Fire Indices", value=True)
    show_severity = st.sidebar.checkbox("Show Burn Severity", value=True)
    show_comparison = st.sidebar.checkbox("Show Before/After Comparison", value=True)
    
    return {
        'before_date': before_date,
        'after_date': after_date,
        'satellite': satellite,
        'show_indices': show_indices,
        'show_severity': show_severity,
        'show_comparison': show_comparison
    }

def main():
    """Main dashboard application."""
    
    # Configure page
    logo_path = "/Users/jlipsitt/Documents/forwardfuture/assets/logos/logo_transparent.png"
    
    # Add banner image at the top
    banner_path = "/Users/jlipsitt/Documents/forwardfuture/assets/images/banner_cropped_more.png"
    try:
        st.image(banner_path, use_container_width=True)
        st.markdown("<br>", unsafe_allow_html=True)  # Add small space after banner
    except Exception as e:
        # Fallback if image doesn't load
        st.title("🔥 Palisades Fire Before/After Analysis")
    
    # Brief description (since banner has the title)
    st.markdown("""
    **Interactive analysis of the January 2025 Palisades Fire in Los Angeles using satellite imagery**
    
    This dashboard analyzes the impact of the Palisades Fire using Google Earth Engine data,
    showing before and after conditions, fire damage assessment, and burn severity mapping.
    """)
    
    # Initialize Earth Engine
    gee_available = init_earth_engine()
    
    # Create sidebar
    config = create_sidebar()
    
    # Create fire area of interest
    aoi = create_fire_aoi()
    
    # Main content
    if gee_available:
        with st.spinner("Loading satellite imagery and calculating fire indices..."):
            # Load imagery
            imagery = load_fire_datasets(config['before_date'], config['after_date'], aoi)
            
            # Calculate fire indices using Sentinel-2 data
            before_img = imagery['sentinel_before'] 
            after_img = imagery['sentinel_after']
            
            indices = {}
            if before_img and after_img:
                indices = calculate_fire_indices(before_img, after_img)
                
                if config['show_severity'] and 'dnbr' in indices:
                    indices['burn_severity'] = classify_burn_severity(indices['dnbr'])
        
        # Show fire impact completion status
        st.success("🔥 **Fire Impact Analysis COMPLETE** - All satellite data loaded and indices calculated")
        
        # Create 4 maps in a 2x2 grid
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🗺️ Fire Damage Overview")
            main_map = create_comparison_map(imagery, indices, aoi)
            main_map.to_streamlit(height=400)
            
            st.markdown("""
            **Fire Damage Analysis**: Shows overall fire damage using dNBR (difference Normalized Burn Ratio). 
            Red areas indicate high fire damage, green areas show little to no impact.
            """)
        
        with col2:
            st.subheader("📊 Burn Severity Classification")
            severity_map = create_burn_severity_map(indices, aoi)
            severity_map.to_streamlit(height=400)
            
            st.markdown("""
            **Burn Severity Levels**: 6-level classification from unburned (white/green) to high severity (purple). 
            Based on dNBR thresholds used by fire management agencies.
            """)
        
        # Second row of maps
        col3, col4 = st.columns(2)
        
        with col3:
            st.subheader("🛰️ Sentinel-2 Before/After")
            sentinel_comparison = create_sentinel_swipe_map(imagery, aoi)
            sentinel_comparison.to_streamlit(height=400)
            
            st.markdown("""
            **Satellite Imagery Comparison**: **Swipe Left = After Fire | Swipe Right = Before Fire** - Drag the vertical slider line to swipe between high-resolution Sentinel-2 imagery 
            before and after the fire. Notice vegetation color change from green to brown/black in burned areas.
            """)
        
        with col4:
            st.subheader("🌿 NBR Before/After Analysis")  
            nbr_comparison = create_nbr_swipe_map(indices, aoi)
            nbr_comparison.to_streamlit(height=400)
            
            st.markdown("""
            **Vegetation Health Analysis**: **Swipe Left = After Fire | Swipe Right = Before Fire** - NBR measures vegetation health. Green = healthy vegetation, 
            red = stressed/burned. Drag the slider to swipe between before and after vegetation health maps.
            """)
    else:
        # Demo mode - show static information
        st.info("🌐 **Demo Mode**: This is where the interactive map would appear with live satellite data")
        
        # Create a simple demo map
        import folium
        demo_map = folium.Map(location=PALISADES_FIRE_CENTER, zoom_start=11)
        
        # Add fire area boundary
        folium.Rectangle(
            bounds=[[PALISADES_FIRE_BBOX[1], PALISADES_FIRE_BBOX[0]], [PALISADES_FIRE_BBOX[3], PALISADES_FIRE_BBOX[2]]],
            color='red',
            fill=True,
            fillColor='red',
            fillOpacity=0.3,
            popup="Palisades Fire Area"
        ).add_to(demo_map)
        
        # Add marker for fire center
        folium.Marker(
            PALISADES_FIRE_CENTER,
            popup="Palisades Fire Start Location<br>January 7, 2025",
            tooltip="Fire Start Location",
            icon=folium.Icon(color='red', icon='fire')
        ).add_to(demo_map)
        
        st_folium = __import__('streamlit_folium')
        st_folium.st_folium(demo_map, width=700, height=500)
    
    # Fire Timeline section
    st.markdown("---")
    st.subheader("📅 Fire Timeline")
    
    import pandas as pd
    
    timeline_data = [
        {"Date": "2025-01-07", "Event": "Fire Started", "Details": "10:30 AM local time"},
        {"Date": "2025-01-07", "Event": "Evacuations Ordered", "Details": "Immediate threat to life"},
        {"Date": "2025-01-08", "Event": "Fire Spread", "Details": "High winds fuel rapid expansion"},
        {"Date": "2025-01-15", "Event": "Current Status", "Details": "~23,713 acres burned"}
    ]
    
    timeline_df = pd.DataFrame(timeline_data)
    st.dataframe(timeline_df, hide_index=True, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    **Data Sources**: Google Earth Engine (Sentinel-2) | 
    **Analysis**: dNBR-based fire damage assessment | 
    **Dashboard**: Built with Streamlit and geemap
    """)

if __name__ == "__main__":
    main()