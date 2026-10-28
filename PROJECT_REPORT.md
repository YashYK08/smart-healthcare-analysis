# Smart Healthcare Risk & Disease Analysis: Capstone Project Report

**Academic Capstone Project Report**  
**Domain:** Healthcare Informatics & Data Analytics  
**Technologies:** Python, Pandas, Tableau Desktop / Public, Flask, Chart.js, Pytest, ReportLab  
**Cohort Scope:** 5,000 Patient Records, 31 Features  

---

## Abstract
Chronic non-communicable diseases (NCDs)—predominantly cardiovascular disease, diabetes mellitus, and stroke—represent the leading cause of global disability and mortality. Early detection and calibrated risk stratification are essential to prevent irreversible organ damage and healthcare system strain. 

This project presents an end-to-end clinical informatics platform engineered to audit, validate, analyze, and visualize patient health risk. Utilizing a cohort dataset of 5,000 patient records across 16 biometric and lifestyle attributes, we performed extensive data cleaning and anomaly detection. 

A critical forensic finding revealed that the raw dataset column `health_risk_score` was completely degenerate, holding an identical constant value of 100.0 ($\sigma = 0.0$) across all rows. To address this defect with medical integrity, we engineered a validated **Calibrated Health Risk Score (0 - 100)** adhering to American Heart Association (AHA), American Diabetes Association (ADA), and World Health Organization (WHO) clinical guidelines. 

We developed eight distinct publication-quality visualizations, an eight-worksheet Tableau workbook (`smart_healthcare_analysis.twb`) and packaged archive (`project.twbx`) featuring two interactive dashboards and a four-scene analytical story, and a polished, responsive Flask web application featuring a real-time clinical risk simulator and REST API. Automated unit testing with pytest validated all pipeline components with a 100% pass rate.

---

## 1. Introduction & Background
In modern clinical medicine, the exponential volume of electronic health record (EHR) data offers an unprecedented opportunity for proactive preventative care. However, raw clinical data frequently suffers from formatting inconsistencies, non-representative synthetic artifacts, and multi-collinear comorbidities.

Epidemiological surveillance demonstrates that cardiovascular disease (CVD) and diabetes mellitus rarely occur in isolation; rather, they form part of a compound metabolic syndrome wherein hypertension, hyperlipidemia, abdominal obesity, and behavioral catalysts accelerate end-organ injury.

The objective of this project is to model the progression of chronic disease, quantify risk tiers, and provide intuitive, interactive visual analytics tools for clinical decision-makers.

---

## 2. Problem Statement & Research Objectives
### 2.1 Problem Statement
Healthcare providers require an accessible, transparent, and reproducible analytical pipeline capable of:
1. Ingesting patient biometric data and detecting data corruption or degenerate features.
2. Deriving valid, multi-factor risk scores that accurately differentiate healthy individuals from high-risk and multi-morbid patients.
3. Translating complex statistical findings into actionable business intelligence dashboards and narratives.

### 2.2 Core Project Objectives
- **Data Validation & Cleaning:** Inspect schema, detect anomalies, verify data bounds, and produce a cleaned, feature-engineered dataset.
- **Biomarker Modeling:** Formulate an authentic Calibrated Health Risk Score resolving the constant `health_risk_score` issue.
- **Exploratory Data Analysis (EDA):** Quantify bivariate and multivariate relationships between age, BMI, blood pressure, cholesterol, glucose, lifestyle, and disease outcomes.
- **Tableau Visual Analytics:** Construct a comprehensive Tableau workbook (`.twb`) and packaged archive (`.twbx`) containing eight worksheets, two dashboards, and a four-scene analytical story.
- **Interactive Web Interface:** Deploy a professional Flask web portal supporting live data exploration, interactive chart rendering, and real-time risk assessment calculation.
- **Automated Verification:** Execute a rigorous test suite validating 100% of pipeline stages.

---

## 3. Dataset Characteristics & Forensic Data Audit
The project analyzes `smart_healthcare_dataset.csv`, consisting of 5,000 unique patient observations and 16 initial attributes:

| Feature Name | Type | Range / Domain | Clinical Significance |
|---|---|---|---|
| `age` | Integer | 18 - 79 years | Primary demographic risk driver |
| `gender` | Categorical | 'Male' (49.9%), 'Female' (50.1%) | Demographic stratification |
| `bmi` | Float | 15.0 - 42.6 kg/m² | Nutritional status & obesity indicator |
| `exercise_level`| Integer | 0 (Sedentary), 1 (Moderate), 2 (Active) | Physical activity habit |
| `smoking` | Binary | 0 (Non-smoker), 1 (Active smoker) | Cardiovascular & pulmonary toxicant |
| `alcohol` | Binary | 0 (Non-drinker), 1 (Drinker) | Hepatic and vascular risk factor |
| `blood_pressure`| Integer | 90 - 179 mmHg | Systolic arterial pressure |
| `cholesterol` | Integer | 150 - 299 mg/dL | Serum total cholesterol level |
| `glucose` | Integer | 70 - 199 mg/dL | Fasting plasma glucose |
| `fatigue` | Binary | 0 (Absent), 1 (Present) | Constitutional symptom |
| `chest_pain` | Binary | 0 (Absent), 1 (Present) | Potential acute coronary symptom |
| `dizziness` | Binary | 0 (Absent), 1 (Present) | Cerebrovascular / vestibular symptom |
| `heart_disease` | Binary | 0 (Negative), 1 (Positive) | Documented cardiovascular disease |
| `diabetes` | Binary | 0 (Negative), 1 (Positive) | Documented diabetes mellitus |
| `stroke` | Binary | 0 (Negative), 1 (Positive) | Documented cerebrovascular event |
| `health_risk_score`| Float | **Constant 100.0** | **Degenerate metric ($\sigma = 0$)** |

### 3.1 Forensic Diagnosis of `health_risk_score`
An automated audit confirmed:
- Minimum: `100.0`
- Maximum: `100.0`
- Mean: `100.00`
- Standard Deviation: `0.0000`
- Unique Values: Exactly 1 (`100.0`)

Because variance is zero, this metric fails to distinguish healthy 18-year-olds from 79-year-olds suffering from triple comorbidity. This issue was systematically documented in the data audit module and rectified via calibrated feature engineering.

---

## 4. Methodology & Feature Engineering

### 4.1 Calibrated Risk Score Mathematical Formulation
We defined the continuous Calibrated Health Risk Score $S \in [0, 100]$ as:

$$S = \min\left(100.0, \, S_{\text{age}} + S_{\text{chronic}} + S_{\text{BP}} + S_{\text{Chol}} + S_{\text{Glu}} + S_{\text{BMI}} + S_{\text{Lifestyle}} + S_{\text{Symptoms}}\right)$$

Where:
- **Age Weighting ($S_{\text{age}} \in [0, 25]$):**
  $$S_{\text{age}} = \left(\frac{\text{Age} - 18}{79 - 18}\right) \times 25.0$$
- **Chronic Disease Burden ($S_{\text{chronic}} \in [0, 30]$):**
  $$S_{\text{chronic}} = \min(30.0, \, (\text{heart\_disease} + \text{diabetes} + \text{stroke}) \times 10.0)$$
- **Biomarker Scoring:**
  - Blood Pressure ($S_{\text{BP}} \le 8$): $\ge 140 \implies 8$; $130-139 \implies 5$; $120-129 \implies 2$.
  - Total Cholesterol ($S_{\text{Chol}} \le 7$): $\ge 240 \implies 7$; $200-239 \implies 4$.
  - Fasting Glucose ($S_{\text{Glu}} \le 8$): $\ge 126 \implies 8$; $100-125 \implies 4$.
  - BMI ($S_{\text{BMI}} \le 7$): $\ge 35 \implies 7$; $30-34.9 \implies 5$; $25-29.9 \implies 3$.
- **Lifestyle Factors ($S_{\text{Lifestyle}} \le 10$):**
  - Smoking: $+4$; Alcohol: $+2$; Sedentary: $+4$; Moderate: $+2$.
- **Acute Symptoms ($S_{\text{Symptoms}} \le 5$):**
  - Chest pain: $+3$; Fatigue: $+1$; Dizziness: $+1$.

### 4.2 Cohort Risk Stratification Tiers
1. **Low Risk ($S < 35.0$):** 2,176 patients (43.52%)
2. **Moderate Risk ($35.0 \le S < 55.0$):** 1,308 patients (26.16%)
3. **High Risk ($55.0 \le S < 75.0$):** 865 patients (17.30%)
4. **Critical Risk ($S \ge 75.0$):** 651 patients (13.02%)

---

## 5. Statistical Findings & Exploratory Data Analysis
1. **The Age Inflection Point:** Between ages 18 and 45, chronic disease incidence is 0%. Onset begins in the 46-60 cohort (14.6% diabetes, 7.8% heart disease), and escalates dramatically in the 61-80 cohort (89.4% heart disease, 100% diabetes, 79.1% stroke).
2. **Extreme Triad Comorbidity:** 1,207 patients (24.14%) suffer simultaneously from Heart Disease, Diabetes, and Stroke. Isolated disease accounts for only 5.78% of the cohort, indicating rapid progression once chronic illness initiates.
3. **Cardiovascular & Lipid Burden:** Over 40% of patients exhibit Stage 1 or Stage 2 Hypertension. Patients with co-occurring hypertension ($\ge 140$ mmHg) and hypercholesterolemia ($\ge 240$ mg/dL) demonstrate a 2.4-fold higher risk tier placement.
4. **Modifiable Lifestyle Protection:** Sedentary smokers experience an 18.2% higher cardiovascular event rate than active non-smokers.

---

## 6. Tableau Visual Analytics Architecture
The project delivers a fully structured Tableau Workbook (`smart_healthcare_analysis.twb`) and packaged archive (`project.twbx`):
- **Worksheets (8):** KPI Summary, Disease Prevalence by Age, Risk Tier Distribution, Biomarker Surveillance (BP vs Glucose), Lifestyle Risk Matrix, Comorbidity Burden, Symptom Cluster Analysis, and BMI vs Cholesterol Scatter.
- **Dashboards (2):**
  - *Clinical Risk & Biomarker Dashboard:* Diagnostic overview for hospital clinicians.
  - *Population Health & Lifestyle Matrix:* Public health and behavioral intervention overview.
- **Analytical Story (1):**
  - 4 structured scenes detailing: (1) Cohort & Anomaly Audit, (2) Age Inflection Point, (3) Modifiable Biomarkers, and (4) Clinical Action Roadmap.

---

## 7. Web Application Implementation & Architecture
Built with Flask, Jinja2, Bootstrap 5, and Chart.js:
- **Executive Dashboard (`/`):** Summary metric cards, dynamic Chart.js charts, and clinical takeaways.
- **Exploratory Analysis (`/exploratory-analysis`):** 8 high-resolution figures and a live patient search table.
- **Tableau Analytics (`/tableau`):** Local worksheet simulation and dynamic Tableau Public embed switcher.
- **Analytical Story (`/story`):** Interactive scene stepper.
- **Risk Calculator (`/risk-calculator`):** Real-time patient risk evaluation engine with factor breakdowns.
- **Data Audit (`/data-audit`):** Complete forensic documentation of the constant score resolution.
- **REST APIs (`/api/stats`, `/api/patients`, `/api/predict-risk`):** JSON services supporting asynchronous UI updates.

---

## 8. Verification & Test Suite Execution
Automated unit testing with `pytest` verified all system layers:
```
tests/test_data_cleaning.py::test_raw_dataset_exists_and_shape PASSED
tests/test_data_cleaning.py::test_raw_health_risk_score_is_constant PASSED
tests/test_data_cleaning.py::test_cleaned_dataset_schema_and_integrity PASSED
tests/test_data_cleaning.py::test_calibrated_risk_score_variance_and_bounds PASSED
tests/test_flask_app.py::test_routes_status_200 PASSED
tests/test_flask_app.py::test_api_stats_structure PASSED
tests/test_flask_app.py::test_api_patients_pagination_and_filter PASSED
tests/test_flask_app.py::test_api_predict_risk_endpoint PASSED
tests/test_tableau_workbook.py::test_twb_file_exists_and_valid_xml PASSED
tests/test_tableau_workbook.py::test_twb_datasources_and_calculated_fields PASSED
tests/test_tableau_workbook.py::test_twbx_archive_integrity PASSED

============================= 11 passed in 1.47s =============================
```

---

## 9. Conclusion & Future Roadmap
This project successfully establishes a complete clinical informatics platform for chronic disease surveillance. By identifying and resolving the degenerate `health_risk_score` metric, we ensured clinical accuracy and academic rigor.

**Future Enhancements:**
- Integration with FHIR / HL7 clinical data interoperability standards.
- Machine learning longitudinal survival analysis (Cox Proportional Hazards).
- Mobile push notifications for patient lifestyle interventions.
