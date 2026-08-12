#!/usr/bin/env bash
# Launch script for ScummBar AI Streamlit Frontend with persistent SQLite session tracking

# Ensure virtual environment is activated
if [ -d "py-env" ]; then
    source py-env/bin/activate
fi

export PYTHONPATH=.

echo "🍺 Starting ScummBar AI Streamlit Single-Player Web App..."
streamlit run src/scummbar_chat/streamlit/app.py --server.port 8501 --server.headless false
