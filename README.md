# ⚡ EcoGrid AI: Regional Decarbonization & Peak-Load Optimization Copilot

**An end-to-end Energy Intelligence, Contextual Machine Learning, and GenAI Advisory solution designed to bridge the gap between grid visibility and actionable decarbonization in Auvergne-Rhône-Alpes, France.**

🔗 **[Live Interactive App (Streamlit)](#)** *(https://ecogrid-ai-regional-decarbonization-peak-load-optimization-cop.streamlit.app/)*  
📊 **[Executive BI Dashboard Preview](#executive-bi-insights-power-bi)**

---

## 1. Executive Summary & Problem Statement

### The Business & Climate Challenge
Industrial and commercial hubs across regions like **Auvergne-Rhône-Alpes (Grenoble)** face two critical energy transition bottlenecks:
1. **The Fossil-Fuel Carbon Trap:** While France benefits from a low-carbon electricity grid (~0.052 tCO₂/MWh), heavy reliance on natural gas (~0.205 tCO₂/MWh) for heating and industrial processes creates disproportionate carbon footprints.
2. **The "Visibility vs. Optimization" Gap:** As highlighted in Schneider Electric’s *AI for Climate* research (October 2026), raw telemetry dashboards alone do not automatically reduce emissions. Sustainability managers and facility operators struggle to translate millions of raw grid data points into timely **peak-shaving** and **electrification** decisions.

### The Solution: EcoGrid AI
**EcoGrid AI** transforms raw regional grid telemetry (ODRÉ) into an automated, three-stage decision-support pipeline:
* **Stage 1 (Data Engineering & BI Visibility):** Reconciles multi-frequency gas and electricity telemetry to quantify true cross-fuel CO₂ disparities, identify weekday peak-strain windows, and model the **~22% AI optimization savings benchmark**.
* **Stage 2 (Contextual Machine Learning):** Deploys a lightweight **Isolation Forest** model enriched with temporal context (`Month` + `Hour`) to detect both extreme winter demand surges and subtle weekend/shoulder-season anomalies.
* **Stage 3 (GenAI Sustainability Advisory):** Synthesizes statistical findings and ML anomaly logs into executive-ready recommendations for industrial load-shifting, battery storage dispatch, and heat-pump electrification.

---

## 2. Architecture & End-to-End Methodology

```text
[ODRÉ Open Grid Telemetry] ──▶ [Power Query ETL & Resampling] ──▶ [Power BI Executive Dashboard]
                                          │
                                          ▼
                            [Contextual Isolation Forest ML] ──▶ [GenAI Sustainability Advisor (Streamlit)]
```

---

## 3. Data Quality Engineering & Problem-Solving Log

Real-world energy data is rarely ready for modeling out of the box. During exploratory auditing of the official **ODRÉ (*Open Data Réseaux Énergies*)** regional dataset (`Auvergne-Rhône-Alpes`, INSEE 84), a critical data integrity trap was identified and resolved:

| Challenge Identified | Root Cause Analysis | Engineering Solution Implemented |
| :--- | :--- | :--- |
| **1. Sampling Frequency Mismatch** | Electricity demand (`RTE`) is logged at **30-minute intervals** (`:00`, `:30`), whereas natural gas demand (`GRTgaz/Teréga`) is logged at **1-hour intervals** (`:00` only), creating 50% `null` values on half-hour rows. | Built an `Hour Floor` timestamp key in Power Query to group sub-hourly records onto a unified hourly grain. |
| **2. The 2x Double-Counting Trap** | Summing half-hourly **Megawatt (MW)** power readings artificially doubles total energy volume (`92.36M` vs. true `46.19M MWh`), making electricity appear larger than combined gas + electricity (`69.37M`). | Applied **Mean (`Average`) aggregation** to half-hourly MW electricity readings to convert instantaneous power rates into true hourly energy volume (`MWh`). |
| **3. Cross-Fuel Total Reconciliation** | The source's raw combined column (`Consommation brute totale`) only captured top-of-the-hour (`:00`) snapshots, ignoring `:30` intra-hour fluctuations. | Engineered a `Recalculated Total` (`Avg Hourly Electricity + Hourly Gas`), reconciling within **0.1%** of official totals (`69.30M` vs. `69.37M MWh`) while preserving full intra-hour accuracy. |

---

## 4. Key Analytical Findings & Business Insights

### 📊 Stage 1: Executive BI Insights (Power BI)
*(Upload a screenshot of your Power BI dashboard as `powerbi_dashboard.png` in your repo to display it below)*  
![Power BI Energy & Carbon Dashboard](powerbi_dashboard.png)

* **The Electrification Business Case (Volume vs. Carbon Flip):**
  * **Energy Consumption Mix:** Electricity accounts for **66.6% (`46.19M MWh`)** of regional demand, while natural gas represents **33.4% (`23.12M MWh`)**.
  * **Carbon Emissions Reality:** Because natural gas emits nearly **4x more CO₂ per MWh** than the French power grid, gas generates **66.4% (`4.74M Tons CO₂`)** of total emissions compared to **33.6% (`2.40M Tons CO₂`)** for electricity. **Electrifying that remaining 33.4% gas share is the single highest-leverage decarbonization action.**
* **Predictable Weekday Peak Strain (`07:00 – 10:00` & `18:00 – 20:00`):**
  * Temporal heatmap analysis reveals sharp demand surges on **Tuesday and Wednesday mornings (`07:00–09:00`)** driven by simultaneous industrial shift startups and commercial HVAC heating, followed by a **20%–25% load drop** on weekends.
* **AI Optimization Savings Potential (`1.57M Tons CO₂`):**
  * Applying Schneider Electric’s empirical *AI for Climate* benchmark (**21.7% – 22.4% energy reduction** via AI-enabled building and process controls) projects an annual regional reduction of **~1.57 Million Tons of CO₂**.

---

### 🤖 Stage 2: Contextual Machine Learning Anomaly Detection
* **The Modeling Challenge:** A baseline `Isolation Forest` trained solely on total energy volume flagged 100% of anomalies inside a single winter cold snap (January 1–12, 2026), missing subtle operational anomalies during warmer months.
* **The Contextual Upgrade:** By engineering temporal features (`Month_Num` and `Hour_Num`) alongside `Recalculated Total`, the model learned seasonal and diurnal baselines—flagging **66 contextual anomalies** across multiple seasons:
  1. **Severe Winter Ramp-Up Peaks (`Jan 6–7, 2026`, `07:00–11:00`):** Demand spiked to **26,368 MWh** (more than double the ~12,000 MWh average), requiring urgent peak-shaving and battery dispatch.
  2. **Shoulder-Season & Weekend Outliers (`Apr 2` and `Sep 19–27, 2026`):** Flagged abnormal weekend baseload spikes (Sat/Sun) where commercial/industrial HVAC or equipment remained active during non-operating hours.

---

### 💬 Stage 3: GenAI Sustainability & Grid Optimization Advisor
To close the gap between technical detection and executive execution, the Streamlit application integrates a **GenAI Advisory Layer** that ingests live telemetry metrics and ML anomaly timestamps to generate targeted recommendations:
* **Peak Shaving:** Automated pre-heating schedules (`04:00–06:00` off-peak) and behind-the-meter battery discharge prior to `07:00` industrial ramp-ups.
* **Industrial Electrification:** Prioritizing commercial heat-pump retrofits to displace high-carbon gas heating (`4.74M Tons CO₂`).
* **Automated Fault Detection:** Auditing weekend baseload anomalies (`Sep 19–27`) to eliminate idle equipment energy waste.

---

## 5. Tech Stack & How to Run Locally

* **Data Engineering & BI:** Power Query (M), DAX, Microsoft Power BI
* **Machine Learning & Analytics:** Python, `pandas`, `scikit-learn` (`IsolationForest`), `openpyxl`
* **Application & GenAI Layer:** `Streamlit`, `OpenAI API` (with built-in executive Demo Mode)

### Quickstart Installation
```bash
# 1. Clone the repository
git clone https://github.com
cd EcoGrid-AI-Decarbonization-Copilot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the Streamlit application
streamlit run app.py
```

---

## 6. Future Roadmap
* **Dynamic Weather Normalization:** Integrate Météo-France Heating Degree Days (HDD) to separate temperature-driven heating spikes from true equipment inefficiency.
* **Live Grid Carbon Intensity API:** Connect real-time RTE *éCO2mix* API feeds to trigger automated load-shifting alerts when marginal grid carbon intensity rises.
