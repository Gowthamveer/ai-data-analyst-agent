#!/bin/bash
# Start the FastAPI server on port 7860 (HF Spaces default)
uvicorn server.app:app --host 0.0.0.0 --port 7860
