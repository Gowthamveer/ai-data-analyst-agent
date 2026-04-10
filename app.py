import streamlit as st
import matplotlib.pyplot as plt
from env.environment import DataEnv, Action

st.set_page_config(page_title="AI Data Analyst", layout="wide")

# -----------------------
# 🎯 HEADER
# -----------------------
st.markdown("""
#  AI Data Analyst Agent
### 🚕 Real-World Data Analysis Dashboard
""")

st.divider()

# -----------------------
# INIT
# -----------------------
if "env" not in st.session_state:
    st.session_state.env = DataEnv()
    st.session_state.obs = st.session_state.env.reset()
    st.session_state.history = []

env = st.session_state.env
obs = st.session_state.obs
df = env.data.sample(n=min(5000, len(env.data)), random_state=42)

fare_col = "fare_amount" if "fare_amount" in df.columns else "fare"

# -----------------------
# 📊 METRICS
# -----------------------
st.markdown("## 📊 Dataset Health")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Missing Values", obs.missing_values)
col2.metric("Duplicates", obs.duplicates)
col3.metric("Anomalies", obs.anomaly_count)

if len(df) > 0:
    col4.metric("Anomaly %", f"{(obs.anomaly_count / len(df))*100:.2f}%")

st.divider()

# -----------------------
# 📄 DATA PREVIEW
# -----------------------
with st.expander("📄 View Dataset Preview"):
    st.dataframe(df.head(20))

# -----------------------
# 📊 CHARTS (SIDE BY SIDE)
# -----------------------
st.markdown("## 📊 Visual Analysis")

colA, colB = st.columns(2)

# 📈 Histogram
with colA:
    st.markdown("### Fare Distribution")
    fig1, ax1 = plt.subplots()
    ax1.hist(df[fare_col].dropna(), bins=50)
    ax1.set_xlabel("Fare")
    ax1.set_ylabel("Frequency")
    st.pyplot(fig1)

# 📉 Distance vs Fare
with colB:
    if "trip_distance" in df.columns:
        st.markdown("### Fare vs Distance")
        fig2, ax2 = plt.subplots()
        ax2.scatter(df["trip_distance"], df[fare_col], s=5)
        ax2.set_xlabel("Distance")
        ax2.set_ylabel("Fare")
        st.pyplot(fig2)

# -----------------------
# 🚨 ANOMALY VISUALIZATION
# -----------------------
if "anomaly" in df.columns:
    st.markdown("## 🚨 Anomaly Detection")

    fig3, ax3 = plt.subplots()

    normal = df[df["anomaly"] == 0]
    anomaly = df[df["anomaly"] == 1]

    ax3.scatter(normal.index, normal[fare_col], s=5, label="Normal")
    ax3.scatter(anomaly.index, anomaly[fare_col], s=5, label="Anomaly")

    ax3.legend()
    ax3.set_xlabel("Index")
    ax3.set_ylabel("Fare")

    st.pyplot(fig3)

# -----------------------
# ⚡ ACTION PANEL
# -----------------------
st.markdown("## ⚡ Agent Actions")

col1, col2, col3, col4 = st.columns(4)

def take_action(action_name):
    action = Action(action_type=action_name, payload={})
    obs, reward, done, _ = env.step(action)

    st.session_state.obs = obs
    st.session_state.history.append((action_name, reward))

    if done:
        st.success("✅ Insight Generated!")

if col1.button("🧹 Clean Missing"):
    take_action("clean_missing")

if col2.button("🧾 Remove Duplicates"):
    take_action("remove_duplicates")

if col3.button("🚨 Detect Anomaly"):
    take_action("detect_anomaly")

if col4.button("📊 Generate Insight"):
    take_action("generate_insight")

# -----------------------
# 📜 HISTORY
# -----------------------
st.markdown("## 📜 Action History")

for act, rew in st.session_state.history:
    st.write(f"**{act}** → Reward: `{round(rew, 3)}`")

# -----------------------
# 💡 INSIGHTS PANEL
# -----------------------
if obs.anomaly_count > 0:
    st.markdown("## 💡 Insights")
    st.info(
        "High fare anomalies detected. These may indicate surge pricing, data errors, or unusual trips."
    )