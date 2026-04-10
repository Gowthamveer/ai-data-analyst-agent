import pandas as pd
from env.schemas import Observation, Action
from models.anomaly import detect_anomalies
from env.reward import compute_reward


class DataEnv:
    def __init__(self):
        self.raw_path = "data/small_data.csv"
        self.reset()

    def reset(self):
        self.data = pd.read_csv(self.raw_path)
        self.step_count = 0
        self.done = False
        return self._get_obs()

    def state(self):
        return self.data.copy()

    def step(self, action: Action):
        self.step_count += 1
        prev_state = self.data.copy()

        col = "fare_amount" if "fare_amount" in self.data.columns else "fare"

        if action.action_type == "clean_missing":
            self.data = self.data.dropna()

        elif action.action_type == "remove_duplicates":
            self.data = self.data.drop_duplicates()

        elif action.action_type == "detect_anomaly":
            self.data["anomaly"] = detect_anomalies(self.data)

        elif action.action_type == "generate_insight":
            self.done = True

        else:
            return self._get_obs(), -0.5, False, {"error": "Invalid action"}

        obs = self._get_obs()
        reward = compute_reward(prev_state, self.data, action, self.step_count)

        return obs, reward, self.done, {}

    def _get_obs(self):
        return Observation(
            summary=str(self.data.describe(include="all")),
            missing_values=int(self.data.isnull().sum().sum()),
            duplicates=int(self.data.duplicated().sum()),
            anomaly_count=int(self.data["anomaly"].sum()) if "anomaly" in self.data else 0,
            step_count=self.step_count
        )
