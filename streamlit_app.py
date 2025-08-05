#!/usr/bin/env python3
"""
Palisades Fire Dashboard - Streamlit Cloud Entry Point

This is the main entry point for Streamlit Community Cloud deployment.
It imports and runs the main dashboard application.
"""

import sys
from pathlib import Path

# Add the code/src directory to Python path for imports
project_root = Path(__file__).parent
code_src_path = project_root / "code" / "src"
sys.path.insert(0, str(code_src_path))

# Import and run the main dashboard
from dashboards.streamlit.palisades_fire_app import main

if __name__ == "__main__":
    main()