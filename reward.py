def compute_reward(prev_df, curr_df, action, step_count):
    reward = 0

    # Total rows (for normalization)
    total_rows = max(len(curr_df), 1)

    # 1. Cleaning reward
    if action.action_type == "clean_missing":
        prev_missing = prev_df.isnull().sum().sum()
        curr_missing = curr_df.isnull().sum().sum()
        improvement = (prev_missing - curr_missing) / total_rows
        reward += improvement * 5   # scaled

    # 2. Duplicate removal
    elif action.action_type == "remove_duplicates":
        prev_dup = prev_df.duplicated().sum()
        curr_dup = curr_df.duplicated().sum()
        improvement = (prev_dup - curr_dup) / total_rows
        reward += improvement * 5

    # 3. Anomaly detection (normalized)
    elif action.action_type == "detect_anomaly":
        if "anomaly" in curr_df:
            anomaly_ratio = curr_df["anomaly"].sum() / total_rows
            reward += min(anomaly_ratio * 5, 0.5)

    # 4. Insight generation
    elif action.action_type == "generate_insight":
        reward += 1.0

    # ❌ Penalty: no change
    if prev_df.equals(curr_df):
        reward -= 0.2

    # ❌ Penalty: too many steps
    if step_count > 7:
        reward -= 0.3

    return float(reward)
