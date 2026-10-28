# Technical Architecture: Smart Healthcare Risk & Disease Analysis

## 1. Executive System Overview
The **Smart Healthcare Risk & Disease Analysis** platform is an end-to-end clinical informatics and data analytics ecosystem designed to ingest, audit, feature-engineer, visualize, and stratify chronic disease risk across diverse patient cohorts.

The platform provides a dual-layer analytics architecture:
1. **Interactive Clinical Web Platform (Flask + Bootstrap 5 + Chart.js)**: Delivers client-facing dashboards, real-time patient risk calculators, forensic data audit reports, and live embedded analytics.
2. **Business Intelligence & Visual Analytics Engine (Tableau Desktop / Tableau Public)**: Delivers publication-grade multi-scene analytical stories, calculated field definitions, and population health surveillance dashboards.

---

## 2. High-Level System Architecture Diagram

```
+-----------------------------------------------------------------------------------+
|                              DATA INGESTION LAYER                                 |
|  smart_healthcare_dataset.csv (5,000 Patient Records, 16 Features)                 |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|                         DATA AUDIT & VALIDATION ENGINE                            |
|  - Null value detection (0 missing values detected)                               |
|  - Forensic check on health_risk_score (Detected Constant 100.0, zero variance)   |
|  - Automated schema validation and boundary enforcement                           |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|                      CLINICAL FEATURE ENGINEERING PIPELINE                        |
|  - Patient Identifiers: P0001 - P5000                                             |
|  - Clinical Categorizations: Age Groups, BMI Categories, Blood Pressure (AHA),     |
|    Glucose (ADA), Cholesterol (NCEP ATP III), Physical Activity Categories        |
|  - Comorbidity Indices: Symptom Count (0-3), Chronic Disease Count (0-3), Flag    |
|  - Calibrated Multi-Factor Health Risk Score (0 - 100 Continuous Scale)           |
|  - 4-Tier Risk Categorization: Low (<35), Moderate (35-54), High (55-74), Critical|
|  Output: smart_healthcare_dataset_cleaned.csv (31 Columns)                        |
+-----------------------------------------------------------------------------------+
                  │                                                  │
                  ▼                                                  ▼
+------------------------------------+             +----------------------------------+
|    TABLEAU ANALYTICS ENGINE        |             |       FLASK WEB APPLICATION      |
|                                    |             |                                  |
| • smart_healthcare_analysis.twb    |             | • app.py (REST API & Web Server) |
| • project.twbx (Packaged Archive)  |             | • Jinja2 Modular Templates:      |
| • 8 Custom Calculated Fields       |             |   - Executive Dashboard (/)      |
| • 8 Analytical Worksheets          |             |   - Exploratory Analysis (/eda)  |
| • 2 Interactive Dashboards         |             |   - Tableau Analytics (/tableau) |
| • 1 Multi-Scene Analytical Story   |             |   - Narrative Story (/story)     |
| • Tableau Public Publishing Hub    |             |   - Risk Calculator (/calc)      |
+------------------------------------+             |   - Forensic Data Audit (/audit) |
                  │                                | • Chart.js Real-time Visuals     |
                  │                                +----------------------------------+
                  │                                                  ▲
                  └─────────────────── EMBED / IFRAME ───────────────┘
```

---

## 3. Component Breakdown

### 3.1 Data Cleaning & Feature Engineering Engine (`data_cleaning_and_eda.py`)
- **Language / Runtime:** Python 3.14+
- **Core Libraries:** `pandas`, `numpy`, `matplotlib`, `seaborn`
- **Responsibilities:**
  - Ingestion of raw comma-separated records.
  - Zero-variance anomaly detection on `health_risk_score`.
  - Computation of deterministic clinical formulas.
  - High-resolution figure rendering (`static/img/visualizations/fig1` to `fig8`).
  - Cache export of aggregate statistics into `cleaned_dataset_summary.json`.

### 3.2 Clinical Web Server & API Gateway (`app.py`)
- **Framework:** Flask 3.1+ WSGI Application
- **Static Assets:** Vanilla JavaScript (`static/js/main.js`), Modular CSS (`static/css/style.css`), FontAwesome 6, Bootstrap 5.3, Chart.js 4.4.
- **REST Endpoints:**
  - `GET /api/stats`: Yields pre-aggregated demographic and biomarker metrics for chart consumption.
  - `GET /api/patients`: Paginated, filterable endpoint supporting real-time cohort inspection by risk tier, gender, and age group.
  - `POST /api/predict-risk`: Clinical calculator endpoint returning real-time score, risk tier, breakdown weights, and clinical guidance.
  - `GET /download-cleaned-data`: Direct binary stream of `smart_healthcare_dataset_cleaned.csv`.
  - `GET /download-twbx`: Direct binary stream of `project.twbx`.

### 3.3 Tableau Visual Analytics Architecture (`smart_healthcare_analysis.twb` & `project.twbx`)
- **Format:** Tableau Workbook XML 18.1 (v2026.2 compatible) & Packaged Zip Archive.
- **Datasource:** Textscan connection bound to UTF-8 CSV.
- **Worksheets:**
  1. `KPI_Cohort_Summary`: Patient count, mean calibrated risk, and disease prevalence metrics.
  2. `Disease_Prevalence_by_Age`: Stacked and clustered multi-bar distribution across four age tiers.
  3. `Risk_Tier_Distribution`: Cohort frequency histogram.
  4. `Biomarker_Surveillance_BP_vs_Glucose`: Dual-axis biomarker scatter with risk tier color encoding.
  5. `Lifestyle_Risk_Matrix`: Smoking vs physical activity cross-tabulation.
  6. `Comorbidity_Burden`: Trivariate distribution of multi-morbidity progression (0 to 3 conditions).
  7. `Symptom_Cluster_Analysis`: Comparative rates of chest pain, chronic fatigue, and dizziness.
  8. `BMI_vs_Cholesterol_Scatter`: Continuous colormap overlaying body mass against lipid profiles.
- **Dashboards:**
  - `Clinical_Risk_and_Biomarker_Dashboard`: High-density diagnostic layout.
  - `Population_Health_and_Lifestyle_Matrix`: Epidemiological policy and lifestyle prevention layout.
- **Story Points:**
  - 4 sequential storyboard scenes guiding clinical stakeholders from anomaly diagnosis to intervention.

---

## 4. Security, Performance & Scalability Considerations
1. **Stateless Service Architecture:** The Flask web server operates in a stateless mode, enabling horizontal containerized scaling across Docker / Kubernetes pods.
2. **Deterministic Reproducibility:** All data transformations and risk formulas are purely deterministic. No stochastic seeds or non-reproducible states exist.
3. **Optimized Client Caching:** Aggregated summary statistics are cached in `cleaned_dataset_summary.json`, eliminating redundant on-the-fly DataFrame recalculations during high-concurrency requests.
4. **Input Sanitization:** The `/api/predict-risk` endpoint validates type boundaries, handling float casting errors and clamping input metrics to physiologic limits.
