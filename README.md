# MAP Assessment Longitudinal Growth & Prediction Analysis

## Project Overview
This project analyzes 6 years of high school MAP assessment data (2021–2027). The objective is to transition from a cross-sectional linear regression analysis of math sub-domains to a **longitudinal predictive growth model** that tracks historical cohort performance and forecasts Spring outcomes for current students.

## Key Findings
* **Historical Growth:** Across the previous 5 academic cohorts, students exhibited a consistent average Fall-to-Spring growth of **+6.33 RIT points**.
* **Spring 2027 Prediction:** Applying this historical baseline to the current Fall 2026 cohort (starting average: 242.59) yields a predicted Spring average of **248.92**.

## Repository Structure
* `src/map_regression_growth.py`: The main Python script handling data ingestion, cleaning, historical calculations, and visualization.
* `data/`: Contains the yearly Excel sheets used for the analysis.
* `docs/images/`: Stores generated visualizations, including the longitudinal prediction bar chart (`longitudinal_growth_prediction.png`).

## Technical Highlights & Solutions
* **Dynamic Header Cleaning:** Handled messy real-world data with unpredictable spacing in Excel headers using a custom pandas list comprehension:
  `df.columns = [c.replace('  ', ' ').strip() for c in df.columns]`
* **Missing Data Management:** Configured the script to isolate historical cohorts with complete Fall-to-Spring data while gracefully handling missing (`NaN`) Spring values for the active 2026-2027 cohort.

## Technologies Used
* Python (pandas, matplotlib)
* Windows 11 / VS Code / Git & GitHub