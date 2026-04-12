"""
FastAPI application entry point for the AI Data Analyst environment.

Provides the standard OpenEnv server endpoints: reset(), step(), state(), health.
"""

import os
import sys
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any, Optional

# Ensure project root is in sys.path for imports
SERVER_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SERVER_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from env.environment import DataEnv
from env.schemas import Action, Observation

app = FastAPI(title="AI Data Analyst Env API")
env = DataEnv()


# ── Health / Root ────────────────────────────────────────────────
@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/health")
def health():
    return {"status": "healthy", "service": "ai-data-analyst-env"}


# ── OpenEnv Endpoints ───────────────────────────────────────────
@app.get("/reset")
@app.post("/reset")
def reset():
    obs = env.reset()
    return {"observation": obs.dict()}


@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action)
    return {"observation": obs.dict(), "reward": reward, "done": done, "info": info}


@app.get("/state")
def state():
    df_state = env.state()
    return df_state.to_dict(orient="records")


# ── Entry Point (required by OpenEnv spec) ──────────────────────
def main(host: str = "0.0.0.0", port: int | None = None):
    """Run the AI Data Analyst environment server with uvicorn."""
    import uvicorn

    if port is None:
        port = int(os.getenv("API_PORT", "7860"))

    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
