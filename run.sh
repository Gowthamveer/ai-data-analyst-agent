#!/bin/bash
# Start the FastAPI server in the background
uvicorn server.app:app --host 0.0.0.0 --port 7860 &

# Start the Streamlit app in the foreground
streamlit run app.py --server.port=8501 --server.address=0.0.0.0
