import pandas as pd
from sklearn.ensemble import IsolationForest

# 1. Load the clean hourly table exported from Power BI
df = pd.read_excel("clean_grid_data.xlsx")

# Filter for 2026 to match dashboard
df["Date"] = pd.to_datetime(df["Date"])
df_2026 = df[df["Date"].dt.year == 2026].copy()

# 2. Train a lightweight Isolation Forest model on Total Hourly Consumption
# contamination=0.01 flags the top 1% most unusual demand spikes/drops
df_2026["Hour_Num"] = pd.to_datetime(
    df_2026["Heure"].astype(str)
).dt.hour
df_2026["Month_Num"] = df_2026["Date"].dt.month

features = ["Month_Num", "Hour_Num", "Recalculated Total"]
model = IsolationForest(contamination=0.01, random_state=42)
df_2026["anomaly_flag"] = model.fit_predict(
    df_2026[features]
)

# 3. Extract only the anomalies and sort by highest consumption
anomalies_hourly = df_2026[df_2026["anomaly_flag"] == -1].sort_values(
    by="Recalculated Total", ascending=False
)

print(
    f"Total 2026 hours analyzed: {len(df_2026)} | Anomalies detected:"
    f" {len(anomalies_hourly)}"
)
print("\nMonths represented in detected anomalies:")
print(anomalies_hourly["Month_Num"].value_counts().sort_index())

print("\nTop 10 Contextual Grid Anomalies:")
print(
    anomalies_hourly[[
        "Date",
        "Heure",
        "Consommation brute Gaz",
        "Consommation brute Electricité",
        "Recalculated Total",
    ]].head(10)
)

# Save anomalies to CSV so we can feed them into Stage 3 (GenAI Advisor)
anomalies_hourly.to_csv("detected_anomalies_2026_hourly.csv", index=False)
