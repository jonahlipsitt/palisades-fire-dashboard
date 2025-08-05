# 🔥 Palisades Fire WebGIS Dashboard

## Overview

This project has been specifically tailored to analyze the **January 2025 Palisades Fire** in Los Angeles using Google Earth Engine and interactive web visualization. The dashboard provides before/after analysis, fire damage assessment, and burn severity mapping.

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Clone the repository
git clone <your-repo-url>
cd forwardfuture

# Create conda environment
conda env create -f environment.yml
conda activate gee-dashboard

# Authenticate Google Earth Engine
earthengine authenticate
```

### 2. Launch Dashboard
```bash
# Run the Palisades Fire analysis dashboard
python run_dashboard.py
```

This will launch the specialized dashboard at `http://localhost:8501`

## 🔥 Fire Analysis Features

### **Key Capabilities:**
- **Before/After Satellite Imagery**: Landsat 8/9 and Sentinel-2 comparisons
- **Fire Damage Assessment**: dNBR (difference Normalized Burn Ratio) analysis
- **Burn Severity Mapping**: Classification into 6 severity levels
- **Interactive Visualization**: Pan, zoom, and layer controls
- **Statistical Analysis**: Area calculations and damage summaries
- **Timeline Integration**: Track fire progression over time

### **Satellite Data Sources:**
- **Landsat 8/9**: 30m resolution, excellent for change detection
- **Sentinel-2**: 10m resolution, detailed damage assessment
- **Fire Indices**: NBR, dNBR, NDVI, NDWI, BAI

### **Analysis Methods:**
- **dNBR Classification**: Standard fire damage assessment protocol
- **Multi-temporal Analysis**: Before (Dec 2024) vs After (Jan 2025)
- **Burn Severity Classes**:
  - Unburned/Very Low: dNBR < -0.1
  - Unburned/Low: -0.1 ≤ dNBR < 0.1
  - Low Severity: 0.1 ≤ dNBR < 0.27
  - Moderate-Low: 0.27 ≤ dNBR < 0.44
  - Moderate-High: 0.44 ≤ dNBR < 0.66
  - High Severity: dNBR ≥ 0.66

## 🗺️ Dashboard Components

### **1. Interactive Map**
- **Base Layers**: Satellite imagery, terrain, street maps
- **Fire Layers**: Before/after RGB, dNBR, burn severity
- **Controls**: Layer visibility, opacity, zoom
- **Analysis Tools**: Click for pixel values, area measurements

### **2. Sidebar Controls**
- **Date Selection**: Customize before/after analysis periods
- **Satellite Choice**: Switch between Landsat and Sentinel-2
- **Analysis Options**: Toggle indices and severity mapping
- **Fire Information**: Key facts and timeline

### **3. Statistics Panel**
- **Area Calculations**: Total burned area in hectares/acres
- **Severity Distribution**: Breakdown by damage level
- **Impact Metrics**: Percentage of area affected
- **Interactive Charts**: Pie charts and bar graphs

### **4. Fire Timeline**
- **Key Events**: Fire start, evacuation orders, containment updates
- **Data Integration**: Satellite overpass dates
- **Progress Tracking**: Recovery monitoring capabilities

## 🛠️ Project Structure

```
forwardfuture/
├── code/
│   ├── src/
│   │   ├── dashboards/streamlit/
│   │   │   ├── palisades_fire_app.py    # Main fire dashboard
│   │   │   └── main_app.py              # Generic dashboard
│   │   ├── auth/                        # GEE authentication
│   │   ├── data/                        # Data processing
│   │   ├── utils/                       # Utilities & constants
│   │   └── visualizations/              # Mapping functions
│   └── notebooks/
│       └── palisades_fire_analysis.ipynb  # Jupyter analysis
├── config/
│   ├── gee/datasets.yml                 # GEE dataset configs
│   ├── environments/development.yml     # Environment settings
│   └── dashboard/streamlit_config.toml  # Dashboard config
├── inputs/                              # Input data storage
├── outputs/                             # Analysis outputs
└── run_dashboard.py                     # Quick launch script
```

## 📊 Analysis Workflow

### **1. Data Preparation**
1. Define Area of Interest (Pacific Palisades region)
2. Set analysis time periods (before: Dec 2024, after: Jan 2025)
3. Load Landsat 8/9 and Sentinel-2 imagery
4. Apply cloud masking and quality filters

### **2. Index Calculation**
1. Calculate NBR (Normalized Burn Ratio) before and after fire
2. Compute dNBR (difference NBR) for damage assessment
3. Generate NDVI, NDWI, and other supporting indices
4. Apply standardized fire analysis protocols

### **3. Classification & Analysis**
1. Classify burn severity using dNBR thresholds
2. Calculate area statistics by severity class
3. Generate change detection maps
4. Validate results with high-resolution imagery

### **4. Visualization & Reporting**
1. Create interactive web maps with layer controls
2. Generate statistical summaries and charts
3. Export results for further analysis
4. Provide recovery monitoring capabilities

## 🎯 Key Fire Metrics

### **Palisades Fire Details:**
- **Coordinates**: 34.0725°N, 118.5425°W
- **Start Date**: January 7, 2025
- **Reported Size**: ~23,713 acres (96 km²)
- **Analysis Area**: Pacific Palisades and surrounding areas
- **Primary Impact**: Residential neighborhoods, natural habitat

### **Best Practices Applied:**
- **Multi-sensor approach**: Combines Landsat and Sentinel-2
- **Standardized methods**: Follows established fire analysis protocols
- **Quality control**: Cloud masking and validation procedures
- **Scalable design**: Can be adapted for other fire events

## 🔬 Technical Implementation

### **Google Earth Engine Integration:**
- **Planetary-scale analysis**: Process petabytes of satellite data
- **Cloud computing**: No local storage or processing required
- **Real-time updates**: Access latest satellite imagery
- **API integration**: Seamless Python/JavaScript workflows

### **Dashboard Technology:**
- **Streamlit**: Interactive web application framework
- **geemap**: Python package for GEE visualization
- **Plotly**: Interactive charts and graphs
- **Folium**: Leaflet-based mapping

### **Data Processing:**
- **Efficient algorithms**: Optimized for large-scale analysis
- **Memory management**: Handle high-resolution imagery
- **Error handling**: Robust data quality checks
- **Export capabilities**: Results to various formats

## 🎓 Educational Value

This dashboard serves as an excellent learning resource for:
- **Fire analysis techniques** using satellite data
- **Google Earth Engine** programming and best practices
- **WebGIS development** with Python and Streamlit
- **Remote sensing** applications in disaster response
- **Data visualization** for scientific communication

## 🔄 Future Enhancements

### **Planned Features:**
- **Recovery monitoring**: Track vegetation regrowth over time
- **Smoke analysis**: Integrate air quality and smoke detection
- **Risk assessment**: Predict future fire susceptibility
- **3D visualization**: Terrain and fire behavior modeling
- **Mobile compatibility**: Responsive design for field use

### **Data Integration:**
- **Weather data**: Wind, temperature, humidity conditions
- **Social media**: Crowdsourced fire reports and photos
- **Infrastructure**: Buildings, roads, utilities impact
- **Economic analysis**: Damage assessment and costs

## 📞 Support & Documentation

- **GitHub Issues**: Report bugs and request features
- **Documentation**: Comprehensive user guides and API docs
- **Examples**: Sample analyses and use cases
- **Community**: Discussion forums and user support

---

**Built with**: Google Earth Engine, Python, Streamlit, Landsat, Sentinel-2

**Purpose**: Palisades Fire analysis and disaster response support

**Impact**: Supporting recovery efforts and fire science research