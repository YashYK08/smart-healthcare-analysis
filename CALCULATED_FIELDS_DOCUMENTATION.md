# Calculated Fields Documentation: Smart Healthcare Risk & Disease Analysis

## 1. Overview & Rationale
During exploratory data audit, the raw column `health_risk_score` in `smart_healthcare_dataset.csv` was identified as having a **constant value of 100.0 across all 5,000 records** (standard deviation $\sigma = 0.0$). 

To ensure analytical validity, reproducible clinical modeling, and actionable business intelligence in Tableau and Python, we developed a standardized suite of calculated fields adhering to recognized clinical benchmarks from the American Heart Association (AHA), American Diabetes Association (ADA), and World Health Organization (WHO).

---

## 2. Calculated Field Inventory

### 2.1 Calibrated Health Risk Score (`[Calibrated Risk Score]`)
- **Tableau Formula:**
```tableau
(([age] - 18.0) / 61.0 * 25.0)
+ MIN(30.0, ([heart_disease] + [diabetes] + [stroke]) * 10.0)
+ (IF [blood_pressure] >= 140 THEN 8.0 ELSEIF [blood_pressure] >= 130 THEN 5.0 ELSEIF [blood_pressure] >= 120 THEN 2.0 ELSE 0.0 END)
+ (IF [cholesterol] >= 240 THEN 7.0 ELSEIF [cholesterol] >= 200 THEN 4.0 ELSE 0.0 END)
+ (IF [glucose] >= 126 THEN 8.0 ELSEIF [glucose] >= 100 THEN 4.0 ELSE 0.0 END)
+ (IF [bmi] >= 35.0 THEN 7.0 ELSEIF [bmi] >= 30.0 THEN 5.0 ELSEIF [bmi] >= 25.0 THEN 3.0 ELSE 0.0 END)
+ (IF [smoking] = 1 THEN 4.0 ELSE 0.0 END)
+ (IF [alcohol] = 1 THEN 2.0 ELSE 0.0 END)
+ (IF [exercise_level] = 0 THEN 4.0 ELSEIF [exercise_level] = 1 THEN 2.0 ELSE 0.0 END)
+ (IF [chest_pain] = 1 THEN 3.0 ELSE 0.0 END)
+ (IF [fatigue] = 1 THEN 1.0 ELSE 0.0 END)
+ (IF [dizziness] = 1 THEN 1.0 ELSE 0.0 END)
```
- **Data Type:** Real / Continuous Measure
- **Range:** `0.0` to `100.0` (Observed cohort mean: `44.55`, std: `20.82`, range: `3.2` to `94.4`)
- **Clinical Rationale:** Synthesizes demographic aging (25 pts), multi-system chronic disease burden (30 pts), vascular biomarkers (30 pts), modifiable behaviors (10 pts), and acute symptom burden (5 pts).

---

### 2.2 Clinical Risk Tier (`[Risk Tier]`)
- **Tableau Formula:**
```tableau
IF [calibrated_risk_score] < 35.0 THEN "Low"
ELSEIF [calibrated_risk_score] < 55.0 THEN "Moderate"
ELSEIF [calibrated_risk_score] < 75.0 THEN "High"
ELSE "Critical"
END
```
- **Data Type:** String / Discrete Dimension
- **Observed Frequencies:**
  - `Low`: 2,176 patients (43.5%)
  - `Moderate`: 1,308 patients (26.2%)
  - `High`: 865 patients (17.3%)
  - `Critical`: 651 patients (13.0%)

---

### 2.3 Blood Pressure Category (`[BP Category]`)
- **Tableau Formula:**
```tableau
IF [blood_pressure] < 120 THEN "Normal"
ELSEIF [blood_pressure] < 130 THEN "Elevated"
ELSEIF [blood_pressure] < 140 THEN "Hypertension Stage 1"
ELSE "Hypertension Stage 2"
END
```
- **Clinical Guideline:** 2017 ACC/AHA High Blood Pressure Clinical Practice Guideline.

---

### 2.4 Fasting Plasma Glucose Category (`[Glucose Category]`)
- **Tableau Formula:**
```tableau
IF [glucose] < 100 THEN "Normal"
ELSEIF [glucose] < 126 THEN "Prediabetic"
ELSE "Diabetic Range"
END
```
- **Clinical Guideline:** American Diabetes Association (ADA) Standards of Medical Care.

---

### 2.5 Body Mass Index Category (`[BMI Category]`)
- **Tableau Formula:**
```tableau
IF [bmi] < 18.5 THEN "Underweight"
ELSEIF [bmi] < 25.0 THEN "Normal"
ELSEIF [bmi] < 30.0 THEN "Overweight"
ELSEIF [bmi] < 35.0 THEN "Obesity Class I"
ELSE "Obesity Class II+"
END
```
- **Clinical Guideline:** World Health Organization (WHO) Adult BMI Classification.

---

### 2.6 Total Cholesterol Category (`[Cholesterol Category]`)
- **Tableau Formula:**
```tableau
IF [cholesterol] < 200 THEN "Desirable"
ELSEIF [cholesterol] < 240 THEN "Borderline High"
ELSE "High"
END
```
- **Clinical Guideline:** National Cholesterol Education Program (NCEP) Adult Treatment Panel III (ATP III).

---

### 2.7 Comorbidity Flag (`[Comorbidity Flag]`)
- **Tableau Formula:**
```tableau
IF ([heart_disease] + [diabetes] + [stroke]) >= 2 THEN 1 ELSE 0 END
```
- **Clinical Rationale:** Identifies multi-morbid patients requiring multidisciplinary coordinated specialty care.
- **Observed Prevalence:** 1,496 patients (29.92%).

---

### 2.8 Metabolic Syndrome Marker (`[Metabolic Syndrome Marker]`)
- **Tableau Formula:**
```tableau
IF [bmi] >= 30.0 AND [glucose] >= 126 AND [blood_pressure] >= 130 THEN "High Metabolic Risk"
ELSE "Standard Profile"
END
```
- **Clinical Rationale:** Detects dangerous syndromic clustering of central obesity, hyperglycemia, and vascular hypertension.
