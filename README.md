---
title: AI Data Analyst Agent
emoji: 🧠
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
---

# 🧠 AI Data Analyst Agent (OpenEnv)

## 🚀 Overview
This project simulates a real-world AI data analyst workflow using an interactive environment.

The agent performs:
- Data cleaning
- Anomaly detection
- Insight generation

---

## 🎯 Features
- Real dataset (NYC Taxi)
- Step-based environment (OpenEnv style)
- Reward-driven agent system
- Streamlit dashboard with visualizations
- Anomaly detection using statistical methods

---

## ⚙️ Tasks

### 🟢 Task 1: Data Cleaning
Remove missing values and duplicates

### 🟡 Task 2: Anomaly Detection
Identify outliers in fare data

### 🔴 Task 3: Insight Generation
Generate meaningful business insights

---

## 🏆 Reward Design
- Rewards for data cleaning improvements
- Rewards for anomaly detection
- Penalties for redundant actions
- Final reward for completing task

---

## 📊 Dataset
NYC Taxi dataset (subset used for efficiency)

---

## 🖥️ Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```