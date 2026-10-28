# Demo Video Narration Script: Smart Healthcare Risk & Disease Analysis

**Project Title:** Smart Healthcare Risk & Chronic Disease Surveillance Platform  
**Target Video Duration:** 5 Minutes (300 Seconds)  
**Presenter:** Project Lead / Capstone Analyst  
**Reference Alignment:** Formatted to match college demonstration standards (`demonstration.mp4`)

---

## Video Timeline & Storyboard

### [00:00 - 00:45] Phase 1: Introduction & Problem Context
- **Visual Cue:** Screen displays the Flask Web Application homepage at `http://127.0.0.1:5000/`. Camera zooms smoothly to the Executive Dashboard title and top KPI metric cards.
- **Narration Audio:**
  > *"Hello evaluators, professors, and esteemed guests. Welcome to the demonstration of our college capstone project: Smart Healthcare Risk and Disease Analysis.
  >
  > Chronic diseases such as cardiovascular disorders, diabetes, and stroke represent over 70% of non-communicable global mortality. The challenge in modern clinical informatics lies in aggregating disparate patient biomarkers, auditing data anomalies, and establishing reproducible, calibrated risk stratification models.
  >
  > In this project, we analyze a real cohort of 5,000 patient records across 16 biometric and clinical features. We have engineered an end-to-end architecture pairing an interactive Flask web application with a comprehensive Tableau visual analytics engine."*

---

### [00:45 - 01:30] Phase 2: Data Audit, Validation & The 100.0 Score Anomaly
- **Visual Cue:** Click on the **Data Audit & Validation** tab in the navigation bar (`/data-audit`). Highlight the anomaly table and schema validation checklist.
- **Narration Audio:**
  > *"Before jumping into visualization, academic and medical rigor requires a forensic data quality audit. During our exploratory inspection using Python and pandas, we identified zero missing values across all 5,000 rows.
  >
  > However, we uncovered a critical data anomaly: the raw dataset field `health_risk_score` was completely degenerate—holding a constant value of 100.0 across every single patient. A metric with zero variance has zero predictive capacity.
  >
  > Rather than ignoring this defect, we formally documented the anomaly and engineered a clinically grounded, multi-factor Calibrated Health Risk Score scaled from 0 to 100. Incorporating age, chronic illness counts, systolic blood pressure, fasting glucose, BMI, and lifestyle factors, our calibrated score restores true clinical variance, yielding a balanced cohort mean of 44.55."*

---

### [01:30 - 02:45] Phase 3: Tableau Worksheets, Dashboards & Story Arc
- **Visual Cue:** Transition to the **Tableau Analytics** tab (`/tableau`) and **Analytical Story** (`/story`). Show the packaged `project.twbx` workbook structure, the interactive dashboard mirror, and step through the 4 story scenes.
- **Narration Audio:**
  > *"Turning to our visual analytics layer, we developed `smart_healthcare_analysis.twb` and packaged `project.twbx`. We formulated eight custom calculated fields in Tableau—including our risk tier thresholds, comorbidity flags, and metabolic syndrome markers.
  >
  > Let's step through our Tableau Analytical Story:
  > - In **Scene 1**, we establish our cohort baseline and present the risk score distribution.
  > - In **Scene 2**, we expose the critical age inflection point: patients under 45 exhibit virtually zero chronic conditions, whereas patients aged 61 to 80 suffer an astonishing 89.4% heart disease rate and a 24.1% triad comorbidity rate.
  > - In **Scene 3**, we dissect modifiable drivers: smokers with sedentary activity patterns experience the steepest vascular degradation.
  > - Finally, in **Scene 4**, we deliver an actionable 4-tier clinical care roadmap—allocating resources from digital wellness for low-risk cohorts to intensive multi-specialist care for critical-risk patients."*

---

### [02:45 - 03:45] Phase 4: Exploratory Analysis & Interactive Cohort Explorer
- **Visual Cue:** Navigate to **Exploratory Analysis** (`/exploratory-analysis`). Scroll through the 8 publication-grade visualization cards. Filter the live patient table by 'High' risk tier and '61-80' age group.
- **Narration Audio:**
  > *"On our Exploratory Analysis interface, we have rendered eight publication-quality statistical visualizations generated via matplotlib and seaborn. These capture biomarker correlation heatmaps, trivariate comorbidity breakdowns, and blood pressure versus glucose trajectories.
  >
  > Below the charts, our live patient explorer connects to our Flask REST API. Doctors and researchers can instantaneously filter the cohort by risk tier, gender, and age bracket with sub-second response times, inspecting individual patient biomarker profiles with complete transparency."*

---

### [03:45 - 04:30] Phase 5: Real-Time Clinical Risk Assessment Calculator
- **Visual Cue:** Navigate to the **Risk Calculator** tab (`/risk-calculator`). Enter sample clinical parameters for a 62-year-old patient with BP 155, glucose 145, smoking, and prior diabetes. Click 'Compute Calibrated Risk Score'.
- **Narration Audio:**
  > *"To demonstrate the translational clinical utility of our model, we built an interactive Patient Risk Calculator.
  >
  > Let's simulate a 62-year-old patient presenting with elevated systolic blood pressure of 155 mmHg, fasting glucose of 145 mg/dL, positive smoking history, and sedentary habits.
  >
  > Clicking 'Compute' calls our POST API. Instantly, the engine returns a Calibrated Risk Score of 76.5, assigning the patient to the Critical Risk Tier. The interface displays real-time point contributions across all clinical categories and delivers immediate guideline-based medical guidance."*

---

### [04:30 - 05:00] Phase 6: Automated Testing & Conclusion
- **Visual Cue:** Switch terminal window showing all 11 pytest unit tests passing in 1.4 seconds (`11 passed in 1.47s`). Return to browser footer.
- **Narration Audio:**
  > *"Every component of our system is backed by comprehensive automated unit testing—from data validation and schema integrity to Flask REST routes and Tableau XML structure, with 100% test pass rates.
  >
  > In conclusion, our Smart Healthcare Risk & Disease Analysis platform bridges data science with clinical medicine—turning raw biometric data into life-saving preventive intelligence.
  >
  > Thank you for your time and consideration. We welcome your questions."*
