import openai
import pandas as pd
from sklearn.ensemble import IsolationForest
import streamlit as st

st.set_page_config(
    page_title="EcoGrid AI | Auvergne-Rhône-Alpes", layout="wide"
)
st.title("⚡ EcoGrid AI: Regional Decarbonization & Anomaly Copilot")
st.caption(
    "Auvergne-Rhône-Alpes (Grenoble Hub) | Power BI + Isolation Forest ML +"
    " GenAI Advisory"
)


# 1. Load & Run Contextual ML Anomaly Detection
@st.cache_data
def load_and_detect():
  df = pd.read_excel("clean_grid_data.xlsx")
  df["Date"] = pd.to_datetime(df["Date"])
  df_2026 = df[df["Date"].dt.year == 2026].copy()

  df_2026["Hour_Num"] = pd.to_datetime(df_2026["Heure"].astype(str)).dt.hour
  df_2026["Month_Num"] = df_2026["Date"].dt.month

  features = ["Month_Num", "Hour_Num", "Recalculated Total"]
  model = IsolationForest(contamination=0.01, random_state=42)
  df_2026["anomaly_flag"] = model.fit_predict(df_2026[features])

  anomalies = df_2026[df_2026["anomaly_flag"] == -1].sort_values(
      by="Recalculated Total", ascending=False
  )
  return df_2026, anomalies


df_2026, anomalies = load_and_detect()

# 2. Key Metrics Row (Matching the Power BI findings)
col1, col2, col3, col4 = st.columns(4)
col1.metric("2026 Total Energy", "69.31M MWh")
col2.metric("Total Emissions", "7.14M Tons CO₂")
col3.metric(
    "Gas Carbon Share", "66.4% (4.74M Tons)", delta="Primary Target", delta_color="inverse"
)
col4.metric("ML Contextual Anomalies", f"{len(anomalies)} Hours Flagged")

# 3. Display Contextual Anomalies
st.subheader("🔍 Contextual Grid Anomalies Detected (Isolation Forest)")
st.write(
    "Flags unusual demand spikes across winter peaks (Jan 5–8) and"
    " shoulder/weekend outliers (Apr & Sep)."
)
st.dataframe(
    anomalies[[
        "Date",
        "Heure",
        "Consommation brute Gaz",
        "Consommation brute Electricité",
        "Recalculated Total",
    ]].head(15),
    use_container_width=True,
)

# 4. GenAI Sustainability Advisory Layer
st.subheader("🤖 GenAI Sustainability & Grid Optimization Advisor")
api_key = st.text_input(
    "Enter OpenAI API Key (leave blank to preview sample AI executive brief):",
    type="password",
)
user_question = st.text_input(
    "Ask the Energy Advisor:",
    value=(
        "How should industrial & commercial operators in Grenoble respond to"
        " the Jan 6-7 morning peaks and reduce the 66.4% gas CO2 share?"
    ),
)

if st.button("Generate Executive Recommendations"):
  context = f"""
    Region: Auvergne-Rhône-Alpes (2026 YTD).
    Energy Mix: 46.19M MWh Electricity (66.6%), 23.12M MWh Gas (33.4%).
    CO2 Impact: Gas produces 4.74M Tons CO2 (66.4%), Electricity produces 2.40M Tons CO2 (33.6%).
    Benchmark: Schneider Electric AI for Climate report estimates 21.7%-22.4% energy savings via AI optimization (~1.57M Tons CO2 potential reduction).
    Top ML Anomalies: Jan 6-7, 2026 (07:00-11:00) reaching 26,368 MWh, plus shoulder/weekend anomalies on Apr 2 and Sep 19-27, 2026.
    """

  if api_key:
    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a Schneider Electric Sustainability Advisory"
                    " consultant. Provide concise, actionable recommendations"
                    " referencing EcoStruxure, peak shaving, and"
                    " electrification."
                ),
            },
            {
                "role": "user",
                "content": f"Telemetry Summary:\n{context}\n\nQuestion: {user_question}",
            },
        ],
    )
    st.success(response.choices[0].message.content)
  else:
    st.info("""
        **Sample AI Executive Brief (Demo Mode):**
        1. **Mitigate Winter Morning Peaks (Jan 6–7, 07:00–11:00):** Deploy automated pre-heating schedules (04:00–06:00 off-peak) and behind-the-meter battery discharge to shave up to 15–20% off industrial morning ramp-up loads.
        2. **Target the 66.4% Gas Emissions Share:** Prioritize industrial heat-pump electrification for commercial/tertiary heating in Auvergne-Rhône-Alpes, leveraging France's low-carbon electricity grid (0.052 tCO₂/MWh vs. 0.205 tCO₂/MWh for gas).
        3. **Audit Weekend Shoulder Anomalies (Sep 19–27):** Use EcoStruxure automated fault detection to eliminate idle HVAC/equipment baseload during non-operating weekend hours, capturing Schneider's ~22% AI optimization benchmark (~1.57M tons CO₂ potential savings).
        """)
