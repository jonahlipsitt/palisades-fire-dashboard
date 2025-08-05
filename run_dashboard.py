#!/usr/bin/env python3
"""
Quick start script for the Google Earth Engine Dashboard

This script sets up the environment and launches the Streamlit dashboard.
"""

import os
import sys
import subprocess
from pathlib import Path

# Add the code/src directory to Python path
project_root = Path(__file__).parent
src_path = project_root / "code" / "src"
sys.path.insert(0, str(src_path))

def check_requirements():
    """Check if required packages are installed."""
    # Check required packages with correct import names
    required_checks = [
        ('streamlit', 'streamlit'),
        ('geemap', 'geemap'), 
        ('earthengine-api', 'ee'),
        ('folium', 'folium'),
        ('plotly', 'plotly'),
        ('pandas', 'pandas')
    ]
    
    missing_packages = []
    for package_name, import_name in required_checks:
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n💡 Install missing packages with:")
        print("   conda env create -f environment.yml")
        print("   conda activate gee-dashboard")
        return False
    
    return True

def check_gee_auth():
    """Check if Google Earth Engine is authenticated."""
    try:
        import ee
        
        # Try to initialize EE without project first
        ee.Authenticate()
        
        # Try different initialization methods
        project_id = os.getenv('GEE_PROJECT_ID')
        if project_id and project_id != 'your-project-id':
            try:
                ee.Initialize(project=project_id)
                print(f"✅ Google Earth Engine authentication successful with project: {project_id}")
            except Exception as e:
                print(f"⚠️  Project {project_id} failed, trying default initialization...")
                ee.Initialize()
                print("✅ Google Earth Engine authentication successful (default)")
        else:
            # Try default initialization
            ee.Initialize()
            print("✅ Google Earth Engine authentication successful (default)")
        
        # Test connection with a simple operation
        ee.Image(1).getInfo()
        return True
        
    except Exception as e:
        print("❌ Google Earth Engine authentication failed")
        print(f"   Error: {e}")
        print("\n💡 Authenticate with:")
        print("   earthengine authenticate")
        return False

def setup_environment():
    """Setup environment variables from .env file if it exists."""
    env_file = project_root / ".env"
    if env_file.exists():
        try:
            from dotenv import load_dotenv
            load_dotenv(env_file)
            print("✅ Loaded environment variables from .env")
        except ImportError:
            print("⚠️  python-dotenv not installed, skipping .env file")
    else:
        print("ℹ️  No .env file found (this is optional)")

def main():
    """Main function to run the dashboard."""
    
    print("🌍 Starting Google Earth Engine Dashboard...")
    print("=" * 50)
    
    # Setup environment
    setup_environment()
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check GEE authentication
    if not check_gee_auth():
        print("\n🔧 To authenticate Google Earth Engine:")
        print("1. Visit: https://developers.google.com/earth-engine/guides/access")
        print("2. Sign up for Earth Engine access")
        print("3. Run: earthengine authenticate")
        print("4. Set GEE_PROJECT_ID in .env file")
        print("\n⚠️  Running dashboard in DEMO mode (no live satellite data)")
        print("✅ You can still explore the interface and functionality")
    
    # Launch Streamlit dashboard - Palisades Fire Analysis
    dashboard_path = src_path / "dashboards" / "streamlit" / "palisades_fire_app.py"
    
    print(f"\n🔥 Launching Palisades Fire Analysis Dashboard...")
    print(f"📁 Dashboard file: {dashboard_path}")
    print(f"🌐 URL: http://localhost:8501")
    print(f"📍 Analyzing the January 2025 Palisades Fire in Los Angeles")
    print("\n" + "=" * 50)
    
    # Set up Streamlit command
    cmd = [
        sys.executable, "-m", "streamlit", "run", 
        str(dashboard_path),
        "--server.port", "8501",
        "--server.address", "localhost"
    ]
    
    try:
        subprocess.run(cmd, cwd=project_root)
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped by user")
    except Exception as e:
        print(f"\n❌ Error running dashboard: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()