# 🧠 AI Data Analyst Agent (OpenEnv)

## 🚀 Overview
This project implements an AI Data Analyst Agent that performs real-world data analysis tasks using a step-based environment.

The agent can:
- Clean data
- Detect anomalies
- Generate insights

It follows a reward-driven approach to evaluate decision-making.

---

## 🎯 Features
- 📊 Real-world dataset (NYC Taxi data - sampled)
- 🧹 Data cleaning (missing values, duplicates)
- 🚨 Anomaly detection
- 💡 Insight generation
- 🧠 Reward-based agent system
- 🌐 Interactive Streamlit dashboard
- 🐳 Docker-based deployment

---

## ⚙️ Tasks

### 🟢 Task 1: Data Cleaning
- Remove missing values
- Remove duplicates

### 🟡 Task 2: Anomaly Detection
- Identify unusual fare patterns

### 🔴 Task 3: Insight Generation
- Generate meaningful business insights

---

## 🏆 Reward Design
- Positive reward for cleaning data
- Reward for detecting anomalies
- Penalty for redundant actions
- Bonus for completing task

---

## 📊 Dataset
- NYC Taxi dataset (sampled for performance)
- Located in: `data/small_data.csv`

---

## 🖥️ Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
