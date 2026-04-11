---
title: AI Data Analyst Agent
emoji: 📊
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
---

# AI Data Analyst Agent (OpenEnv RL Challenge)

This is a Meta OpenEnv compliant AI Data Analyst Agent that uses an LLM to automatically clean, process, and analyze datasets (NYC Taxi Dataset).

## Features
- **Data Cleaning**: Automatically detects and handles missing values.
- **Deduplication**: Identifies and removes duplicate records.
- **Anomaly Detection**: Uses statistical methods (Isolation Forest) to detect outliers in fare amounts.
- **Insight Generation**: Produces actionable business insights based on the cleaned data.

## Tasks and Difficulty
The environment defines a workflow task with increasing complexity based on the dataset state:
- **Easy**: Handle missing values and duplicates.
- **Medium**: Detect anomalies in cleaned data.
- **Hard**: Generate comprehensive insights from a fully cleaned and anomaly-free dataset.

## Baseline Performance
Using `gpt-4.1-mini`:
- Task: NYC Taxi Data Analysis Workflow
- Sequence: `clean_missing` -> `remove_duplicates` -> `detect_anomaly` -> `generate_insight`
- Success Rate: 100%
- Average Steps: 4
- Average Reward: 1.0 (0.25 per successful step)

## Setup and Running

1. **Install dependencies**:
   ```bash
   uv venv
   source .venv/bin/activate  # Or .venv\Scripts\activate on Windows
   uv pip install -r requirements.txt
   ```

2. **Set Environment Variables**:
   ```bash
   export API_BASE_URL="https://api.openai.com/v1"
   export MODEL_NAME="gpt-4o-mini" # or whatever model you want
   export HF_TOKEN="your_huggingface_token"
   ```

3. **Run Inference**:
   ```bash
   python inference.py
   ```

4. **Run Server (Locally)**:
   ```bash
   uvicorn server.app:app --host 0.0.0.0 --port 7860
   ```

## OpenEnv Validation
This project is structured to pass Meta's pre-submission validators:
- Proper `openenv.yaml` spec version 1
- `server/app.py` with `main()` entrypoint
- `inference.py` at root using OpenAI Client
- Proper Dockerfile exposing port 7860