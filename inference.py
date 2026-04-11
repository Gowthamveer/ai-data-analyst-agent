from fastapi import FastAPI
import pandas as pd

def create_app():
    app = FastAPI()

    @app.post("/reset")
    def reset():
        return {"status": "ok"}

    return app

# Global state
data = None
step_count = 0

# ---------------- RESET ----------------
@app.post("/reset")
def reset():
    global data, step_count

    data = pd.read_csv("data/small_data.csv")
    step_count = 0

    return {
        "message": "Environment reset successful",
        "rows": len(data)
    }

# ---------------- STEP ----------------
@app.post("/step")
def step(action: dict):
    global data, step_count

    step_count += 1
    action_type = action.get("action", "")

    reward = 0

    if action_type == "clean_missing":
        before = data.isnull().sum().sum()
        data = data.fillna(method="ffill")
        after = data.isnull().sum().sum()
        reward = (before - after) * 0.1

    elif action_type == "remove_duplicates":
        before = data.duplicated().sum()
        data = data.drop_duplicates()
        after = data.duplicated().sum()
        reward = (before - after) * 0.15

    elif action_type == "detect_anomaly":
        numeric_cols = data.select_dtypes(include=["number"])
        z = (numeric_cols - numeric_cols.mean()) / numeric_cols.std()
        anomalies = (abs(z) > 3).sum().sum()
        data["anomaly"] = (abs(z) > 3).any(axis=1)
        reward = min(anomalies * 0.0001, 0.5)

    elif action_type == "generate_insight":
        reward = 0.8

    else:
        reward = -0.1

    done = step_count >= 4

    return {
        "step": step_count,
        "action": action_type,
        "reward": float(reward),
        "done": done
    }

# ---------------- STATUS ----------------
@app.get("/")
def home():
    return {"message": "AI Data Analyst Agent Running"}
