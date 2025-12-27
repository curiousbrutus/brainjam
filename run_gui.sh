#!/bin/bash
# 
# Run BrainJam Streamlit GUI
#
# Usage: ./run_gui.sh [port]
#

PORT=${1:-8501}

echo "🎛️🎶 Starting BrainJam Streamlit GUI..."
echo ""
echo "The app will open in your browser at:"
echo "  http://localhost:$PORT"
echo ""
echo "Press Ctrl+C to stop the app"
echo ""

cd "$(dirname "$0")"
streamlit run streamlit_app/app.py --server.port $PORT
