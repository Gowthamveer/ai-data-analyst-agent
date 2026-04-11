import os
from openai import OpenAI
from env.environment import DataEnv, Action

# ✅ Required environment variables
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

def main():
    if HF_TOKEN is None:
        raise ValueError("HF_TOKEN environment variable is required")

    # OpenAI client
    client = OpenAI(
        base_url=API_BASE_URL,
        api_key=HF_TOKEN
    )

    # Initialize environment
    env = DataEnv()
    obs = env.reset()

    task_name = "data_analysis"
    benchmark = "openenv"

    print(f"[START] task={task_name} env={benchmark} model={MODEL_NAME}")

    total_rewards = []
    success = False

    actions = [
        "clean_missing",
        "remove_duplicates",
        "detect_anomaly",
        "generate_insight"
    ]

    for step, action_name in enumerate(actions, start=1):
        error = None

        try:
            action = Action(action_type=action_name, payload={})
            obs, reward, done, info = env.step(action)

            total_rewards.append(f"{reward:.2f}")

            print(f"[STEP] step={step} action={action_name} reward={reward:.2f} done={str(done).lower()} error=null")

            if done:
                success = True
                break

        except Exception as e:
            error = str(e)
            print(f"[STEP] step={step} action={action_name} reward=0.00 done=false error={error}")

    print(f"[END] success={str(success).lower()} steps={step} rewards={','.join(total_rewards)}")

if __name__ == "__main__":
    main()