# Google Earth Engine Interactive Dashboard

A template project for building interactive dashboards with Google Earth Engine Python API.

## 🔥 Overview

This project provides a comprehensive framework for analyzing the **January 2025 Palisades Fire in Los Angeles** using Google Earth Engine (GEE) and Python. The dashboard shows before/after satellite imagery, fire damage assessment, burn severity mapping, and recovery monitoring.

### **Palisades Fire Details:**
- **Location**: Pacific Palisades, Los Angeles (34.0725°N, 118.5425°W)
- **Start Date**: January 7, 2025
- **Size**: ~23,713 acres (~96 km²)
- **Impact**: Significant damage to residential areas and natural habitat

## 🚀 Quick Start

### Prerequisites

- [Anaconda](https://www.anaconda.com/products/distribution) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- [Google Earth Engine account](https://earthengine.google.com/)
- [Google Cloud Project](https://console.cloud.google.com/) with Earth Engine API enabled

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd forwardfuture
   ```

2. **Create conda environment**
   ```bash
   conda env create -f environment.yml
   conda activate gee-dashboard
   ```

3. **Authenticate Google Earth Engine**
   ```bash
   earthengine authenticate
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your project details (especially GEE_PROJECT_ID)
   ```

5. **Quick start dashboard**
   ```bash
   python run_dashboard.py
   ```

6. **Manual test (optional)**
   ```bash
   python -c "import ee; ee.Initialize(project='your-project-id'); print('✅ GEE setup successful!')"
   ```

## 📁 Project Structure

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for detailed directory organization.

```
forwardfuture/
├── 📁 inputs/                   # All input data sources
│   ├── raw/                     # Original, unprocessed data
│   ├── processed/               # Cleaned and preprocessed data
│   └── reference/               # Reference/lookup data
├── 📁 outputs/                  # All generated outputs
│   ├── exports/                 # Data exports from analysis
│   ├── figures/                 # Generated visualizations
│   ├── reports/                 # Generated reports
│   └── tiles/                   # Map tile cache
├── 📁 code/                     # All source code
│   ├── src/                     # Main application source
│   ├── notebooks/               # Jupyter notebooks
│   ├── scripts/                 # Standalone scripts
│   └── tests/                   # Test suite
├── 📁 config/                   # Configuration files
├── 📁 assets/                   # Static assets (icons, styles)
├── 📁 docs/                     # Documentation
├── 📁 deploy/                   # Deployment configurations
├── environment.yml              # Conda environment
├── requirements.txt             # Pip requirements
├── run_dashboard.py             # Quick start script
└── README.md
```

## 🛠️ Development

### Running the Palisades Fire Analysis Dashboard

**Quick Start (Recommended):**
```bash
python run_dashboard.py
```
*This launches the Palisades Fire specific analysis dashboard*

**Manual Streamlit Launch:**
```bash
streamlit run code/src/dashboards/streamlit/palisades_fire_app.py
```
*This dashboard is specifically designed for Palisades Fire analysis*

**Jupyter Notebooks:**
```bash
jupyter lab
# Navigate to code/notebooks/ folder
```

**Voila Dashboard:**
```bash
voila code/notebooks/dashboard.ipynb
```

### Environment Management

**Update environment:**
```bash
conda env update -f environment.yml
```

**Export current environment:**
```bash
conda env export > environment.yml
```

**Activate/Deactivate:**
```bash
conda activate gee-dashboard
conda deactivate
```

## 🔐 Authentication

### Development (User Authentication)
```python
import ee
ee.Authenticate()
ee.Initialize(project='your-project-id')
```

### Production (Service Account)
```python
import ee
import os

credentials = ee.ServiceAccountCredentials(
    email=None,
    key_file=os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
)
ee.Initialize(credentials, project='your-project-id')
```

## 📊 Key Features

- **Interactive Maps**: Built with geemap and folium
- **Time Series Analysis**: Dynamic data exploration tools
- **Chart Visualizations**: Plotly, Altair, and Matplotlib integration
- **Dashboard Framework**: Streamlit and Voila support
- **Data Export**: Seamless GEE to local/cloud export
- **Error Handling**: Robust exception management
- **Performance Optimization**: Caching and memory management
- **Testing**: Unit test framework included

## 🌐 Deployment

### Local Development
```bash
streamlit run src/dashboards/streamlit_app.py --server.port 8501
```

### Streamlit Cloud
1. Push code to GitHub
2. Connect repository to [Streamlit Cloud](https://streamlit.io/cloud)
3. Set environment variables in Streamlit Cloud settings

### Google Cloud Run
```bash
# Build and deploy container
gcloud run deploy gee-dashboard \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Heroku
```bash
# Create Heroku app
heroku create your-app-name
git push heroku main
```

## 📝 Configuration

### Environment Variables (.env)
```bash
# Google Earth Engine
GEE_PROJECT_ID=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json

# Projection Data
PROJ_DATA=/path/to/proj/data
PROJ_LIB=/path/to/proj/data

# App Configuration
DEBUG=True
LOG_LEVEL=INFO
```

### Secrets Management
- **Development**: Use `.env` file (never commit)
- **Production**: Use cloud provider secret management
- **Streamlit Cloud**: Add secrets in app settings
- **Heroku**: Use config vars

## 🧪 Testing

**Run all tests:**
```bash
pytest tests/
```

**Run specific test:**
```bash
pytest tests/test_data_loaders.py
```

**With coverage:**
```bash
pytest --cov=src tests/
```

## 📚 Usage Examples

### Basic Map Creation
```python
import geemap
from src.visualizations.maps import create_base_map

# Create interactive map
m = create_base_map(center=[40, -100], zoom=4)
m.add_basemap('HYBRID')

# Add Earth Engine data
landsat = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2').first()
m.addLayer(landsat, {'bands': ['SR_B4', 'SR_B3', 'SR_B2']}, 'Landsat')
```

### Dashboard Components
```python
import streamlit as st
from src.dashboards.components import create_sidebar, create_map_view

# Streamlit dashboard
st.set_page_config(page_title="GEE Dashboard", layout="wide")

# Create UI components
sidebar_data = create_sidebar()
map_view = create_map_view(sidebar_data)

# Display
col1, col2 = st.columns([3, 1])
with col1:
    st.plotly_chart(map_view)
```

## 🔧 Troubleshooting

### Common Issues

**PROJ Data Error:**
```bash
# Set environment variables
export PROJ_DATA=$CONDA_PREFIX/share/proj
export PROJ_LIB=$CONDA_PREFIX/share/proj
```

**Authentication Failed:**
```bash
# Re-authenticate
earthengine authenticate --force
```

**Memory Issues:**
```python
# Clear Earth Engine cache
ee.Reset()
import gc
gc.collect()
```

**Streamlit Widget Issues:**
- Use `st.cache_resource` for Earth Engine initialization
- Avoid `st.cache_data` with Earth Engine objects

## 📖 Documentation

- [Google Earth Engine Python API](https://developers.google.com/earth-engine/guides/python_install)
- [Geemap Documentation](https://geemap.org/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Folium Documentation](https://python-visualization.github.io/folium/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Google Earth Engine](https://earthengine.google.com/) team
- [Geemap](https://geemap.org/) developers
- [Streamlit](https://streamlit.io/) community
- Open source geospatial community

## 📞 Support

- 📧 Email: [your-email@domain.com]
- 🐛 Issues: [GitHub Issues](https://github.com/your-username/gee-dashboard/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/your-username/gee-dashboard/discussions)

---

**Happy Mapping! 🗺️**