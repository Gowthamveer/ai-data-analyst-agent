import os
import json
from openai import OpenAI
from env.environment import DataEnv, Action

# ✅ Required environment variables
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

VALID_ACTIONS = ["clean_missing", "remove_duplicates", "detect_anomaly", "generate_insight"]

SYSTEM_PROMPT = """You are an AI Data Analyst agent working on a NYC Taxi dataset.
You must analyze the dataset observation and decide the best next action to take.

Available actions (choose exactly one):
- clean_missing: Remove rows with missing/null values
- remove_duplicates: Remove duplicate rows
- detect_anomaly: Detect anomalies/outliers in fare data using statistical methods
- generate_insight: Generate final business insights (use this as the LAST action when data is clean)

You will receive dataset health metrics:
- missing_values: count of null values in the dataset
- duplicates: count of duplicate rows
- anomaly_count: count of detected anomalies
- step_count: how many actions have been taken so far

Strategy:
1. If missing_values > 0, use clean_missing first
2. If duplicates > 0, use remove_duplicates
3. If anomaly_count == 0 and data is clean, use detect_anomaly
4. Once data is clean and anomalies are detected, use generate_insight to finish

Respond with ONLY a JSON object: {"action": "<action_name>"}
Do not include any other text."""


def get_llm_action(client, obs_dict):
    """Ask the LLM to choose the next action based on the current observation."""
    user_message = f"""Current dataset observation:
- Missing values: {obs_dict['missing_values']}
- Duplicates: {obs_dict['duplicates']}
- Anomaly count: {obs_dict['anomaly_count']}
- Steps taken: {obs_dict['step_count']}

What action should I take next? Respond with ONLY a JSON object: {{"action": "<action_name>"}}"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        temperature=0.0,
        max_tokens=50
    )

    content = response.choices[0].message.content.strip()

    # Parse the LLM response
    try:
        parsed = json.loads(content)
        action_name = parsed.get("action", "").strip()
    except json.JSONDecodeError:
        # Fallback: try to extract action name from text
        for act in VALID_ACTIONS:
            if act in content:
                action_name = act
                break
        else:
            action_name = "generate_insight"  # safe fallback

    # Validate action
    if action_name not in VALID_ACTIONS:
        action_name = "generate_insight"

    return action_name


def main():
    if HF_TOKEN is None:
        raise ValueError("HF_TOKEN environment variable is required")

    # Initialize OpenAI client
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
    step = 0
    max_steps = 10  # Safety limit

    try:
        while not success and step < max_steps:
            step += 1

            # Build observation dict for LLM
            obs_dict = {
                "missing_values": obs.missing_values,
                "duplicates": obs.duplicates,
                "anomaly_count": obs.anomaly_count,
                "step_count": obs.step_count
            }

            # Ask LLM for next action
            try:
                action_name = get_llm_action(client, obs_dict)
            except Exception as e:
                # If LLM call fails, use fallback logic
                if obs.missing_values > 0:
                    action_name = "clean_missing"
                elif obs.duplicates > 0:
                    action_name = "remove_duplicates"
                elif obs.anomaly_count == 0:
                    action_name = "detect_anomaly"
                else:
                    action_name = "generate_insight"

            try:
                action = Action(action_type=action_name, payload={})
                obs, reward, done, info = env.step(action)

                total_rewards.append(f"{reward:.2f}")
                error_str = "null"

                print(f"[STEP] step={step} action={action_name} reward={reward:.2f} done={str(done).lower()} error={error_str}")

                if done:
                    success = True

            except Exception as e:
                error_str = str(e)
                total_rewards.append("0.00")
                print(f"[STEP] step={step} action={action_name} reward=0.00 done=false error={error_str}")

    except Exception as e:
        # Ensure [END] is always emitted even on unexpected errors
        if step == 0:
            step = 1
            total_rewards.append("0.00")
            print(f"[STEP] step=1 action=none reward=0.00 done=false error={str(e)}")

    print(f"[END] success={str(success).lower()} steps={step} rewards={','.join(total_rewards)}")


if __name__ == "__main__":
    main()