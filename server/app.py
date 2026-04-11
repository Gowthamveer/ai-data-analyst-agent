from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any, Optional

from env.environment import DataEnv
from env.schemas import Action

app = FastAPI(title="AI Data Analyst Env API")
env = DataEnv()

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/reset")
def reset():
    obs = env.reset()
    return {"obs": obs.dict()}

@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action)
    return {"obs": obs.dict(), "reward": reward, "done": done, "info": info}

@app.get("/state")
def state():
    # Return serializable state
    df_state = env.state()
    return df_state.to_dict(orient="records")
