#!/bin/bash

# Palisades Fire Dashboard Launcher
# This script automatically activates the correct conda environment and launches the dashboard

echo "🔥 Palisades Fire Analysis Dashboard 🔥"
echo "========================================"

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Navigate to project directory
cd "$SCRIPT_DIR"

# Check if we're in the right conda environment
if [[ "$CONDA_DEFAULT_ENV" != "gee-dashboard" ]]; then
    echo "📦 Activating gee-dashboard environment..."
    
    # Initialize conda for this shell
    eval "$(conda shell.bash hook)"
    
    # Activate the correct environment
    conda activate gee-dashboard
    
    if [[ "$?" -ne 0 ]]; then
        echo "❌ Failed to activate gee-dashboard environment"
        echo "Please run: conda activate gee-dashboard"
        exit 1
    fi
fi

# Set environment variables
export PYTHONPATH="$PYTHONPATH:$SCRIPT_DIR/code/src"
export GEE_PROJECT_ID="ee-jonahlipsitt"

echo "✅ Environment: $CONDA_DEFAULT_ENV"
echo "✅ Project ID: $GEE_PROJECT_ID"
echo "🚀 Launching dashboard..."
echo ""
echo "Dashboard will be available at: http://localhost:8501"
echo "Press Ctrl+C to stop the dashboard"
echo ""

# Launch the dashboard
streamlit run code/src/dashboards/streamlit/palisades_fire_app.py --server.port 8501 --server.address localhost