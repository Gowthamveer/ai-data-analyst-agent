import numpy as np

def detect_anomalies(df):
    # Choose correct column
    col = "fare_amount" if "fare_amount" in df.columns else "fare"

    df = df.copy()

    # Handle missing values
    df[col] = df[col].fillna(df[col].mean())

    mean = df[col].mean()
    std = df[col].std()

    if std == 0 or np.isnan(std):
        return [0] * len(df)

    z_scores = (df[col] - mean) / std

    # Mark anomalies
    return (np.abs(z_scores) > 4).astype(int)
