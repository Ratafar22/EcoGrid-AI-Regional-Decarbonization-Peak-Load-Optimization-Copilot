# ⚡ EcoGrid AI
### Regional Decarbonization & Peak-Load Optimization Copilot

**Turning regional energy data into insights for reducing emissions and managing peak demand.**

I built EcoGrid AI to explore how data analytics and AI can help turn energy consumption data into practical sustainability decisions. The project combines **Power BI, machine learning and an AI advisor**, using data from **Auvergne-Rhône-Alpes, France**, the region that includes Grenoble.

[Open the Streamlit app](https://ecogrid-ai-regional-decarbonization-peak-load-optimization-cop.streamlit.app/)


## The business problem

Energy and sustainability managers need to decide where to focus their efforts: reducing gas use, managing busy periods or investigating unusual demand. Total consumption alone does not reveal these priorities. The energy source used most may not produce the most emissions, and monthly totals can hide unusual hourly patterns.

EcoGrid AI addresses this through three stages: **understand energy use, identify unusual hours, and explain possible actions**. It supports regional investigations; decisions about individual facilities require local operating information.

## Data source

The project uses **2024–September 2026** electricity and gas consumption data from [ODRÉ — Open Data Réseaux Énergies](https://odre.opendatasoft.com/explore/dataset/consommation-quotidienne-brute-regionale/), provided by **RTE, NaTran and Teréga**, and filtered to **Auvergne-Rhône-Alpes**.

Electricity readings are recorded every 30 minutes and gas readings hourly. **The findings below cover January–September 2026**, matching the selected Power BI report period and the machine-learning analysis.

## Stage 1 — Understand energy use and emissions
**Power Query · Power BI**

📊 **[Executive BI Dashboard Preview](#executive-bi-insights-power-bi)**

I first aligned electricity and gas readings to a common hourly basis. Because the source measures demand in megawatts (MW), simply adding two half-hourly electricity readings would overstate energy use. I averaged those readings within each hour and combined them with the hourly gas values. For a complete one-hour interval, average MW × one hour gives energy in MWh.

I then recalculated combined consumption, compared it with the source total, and added day-of-week fields. The Power BI report uses this prepared data to show consumption trends, estimated emissions and demand by hour and day.

| January–September 2026 | Electricity | Gas | Combined |
| --- | --- | --- | --- |
| Consumption | 46.19 million MWh | 23.12 million MWh | ≈69.30 million MWh |
| Estimated emissions | 2.40 million tonnes CO₂e | 4.74 million tonnes CO₂e | 7.14 million tonnes CO₂e |

**Gas accounts for about one-third of consumption but two-thirds of estimated emissions.** This makes gas-dependent activities a useful starting point for assessing electrification, such as replacing suitable gas heating with heat pumps.

Demand is also higher on weekday mornings than at comparable weekend hours, highlighting periods to examine for shifting flexible energy use. The dashboard’s **66.37% “Electrification Opportunity”** represents gas’s share of estimated emissions, not guaranteed emissions savings.

## Stage 2 — Find unusual hours worth investigating
**Python · pandas · Scikit-learn · Isolation Forest**

I used **Isolation Forest**, a machine-learning model, to identify unusual observations based on consumption, month and time of day. Configured to flag approximately 1% of observations, it identified **66 unusual hours**.

- **6 January at 09:00:** The highest-consumption flagged hour, at approximately **26,368 MWh** of combined gas and electricity use. One possibility is that cold-weather heating coincided with factories starting their morning shifts and commercial buildings warming up.
- **2 April at 07:00:** stood out on a Thursday morning in spring. Was it unusually cold for April, and did buildings still need heating as the working day began?
- **19, 20 and 27 September at 23:00:** were lower-consumption hours late on weekend nights. Comparing them with other weekend nights could show whether demand was higher or lower than usual before investigating equipment schedules or changes in temperature.

These hours give operators a shortlist for investigation. Historical weather records can help test the heating explanations. Facility meter readings and operating schedules can show whether individual sites followed the regional pattern.

[Detection code](EcoGRidAI_hourly_anomaly.py) · [Exported results](detected_anomalies_2026_hourly.csv)

## Stage 3 — GenAI Advisor: Turn findings into practical recommendations
**Streamlit · OpenAI API**

The app displays the headline findings and detected anomalies. Users can ask questions such as:

> How could operators respond to morning demand peaks and reduce emissions associated with gas use?

The AI advisor uses a prepared summary of the analysis to suggest actions: reviewing operating and heating schedules, assessing battery storage for electricity peaks, exploring suitable heat-pump applications, and investigating unusual demand against local conditions.

Anomaly detection runs on the saved dataset; headline metrics and the advisor’s input summary are predefined. An OpenAI API key enables generated responses, while demo mode displays a sample brief.

## Emissions assumptions and savings scenario

Emissions are estimated using fixed reference factors and expressed as **CO₂ equivalent (CO₂e)**.

| Energy source | Factor used | Basis |
| --- | --- | --- |
| Electricity | 0.052 tonnes CO₂e/MWh | Rounded from the ADEME-derived 51.9 gCO₂e/kWh value published in [SNCF’s methodology](https://www.sncf-voyageurs.com/fr/comparateur-carbone/). |
| Gas | 0.205 tonnes CO₂e/MWh PCS | Approximate historical lifecycle factor: [ADEME’s 2015 reference](https://prod-basecarbonesolo.ademe-dri.fr/documentation/UPLOAD_DOC_FR/gaz.htm) of 0.227 kgCO₂e/kWh PCI ÷ [1.11](https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000788395/2026-01-23) ≈ 0.205 kgCO₂e/kWh PCS. |

The gas factor includes upstream emissions and combustion, and uses the same **PCS energy basis** as ODRÉ. Both factors are held constant for this analysis rather than tracking changes each year.

The dashboard’s **1.57 million tonnes CO₂e savings scenario** applies approximately 22% to the period’s estimated emissions. This is inspired by [Schneider Electric’s building-efficiency research](https://www.se.com/ww/en/insights/electricity-4-0/digitalization/can-ai-close-buildings-efficiency-gap/), which reports modelled energy savings of 21.7%–22.4% from AI-enabled HVAC optimization with smart building management.

The estimated 1.57 million tonnes CO₂e represents potential savings if a similar 22% reduction were achieved across the region. Actual savings would depend on the measures implemented and local conditions.

## Future roadmap
The next steps would make EcoGrid AI more responsive to changing conditions and strengthen its recommendations:
- Connect the GenAI advisor directly to analysis results: Automatically supply calculated metrics and detected anomalies so its responses reflect the dataset being analysed.
- Add weather context: Include temperature data to help distinguish expected heating demand from unusual consumption that needs further investigation.
- Automate data updates: Connect to updated energy consumption and grid carbon-intensity data to explore when shifting electricity use could reduce emissions.


**Author: Rukayat Rauf**

