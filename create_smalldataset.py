import pandas as pd

df = pd.read_csv("data/raw_data.csv", nrows=5000)
df.to_csv("data/small_data.csv", index=False)

print("Small dataset created ✅")