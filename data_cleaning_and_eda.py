# data_cleaning_and_eda.py
import os
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_CSV = os.path.join(PROJECT_DIR, 'smart_healthcare_dataset.csv')
OUTPUT_CSV = os.path.join(PROJECT_DIR, 'smart_healthcare_dataset_cleaned.csv')
OUTPUT_JSON = os.path.join(PROJECT_DIR, 'cleaned_dataset_summary.json')
IMG_DIR = os.path.join(PROJECT_DIR, 'static', 'img', 'visualizations')

os.makedirs(IMG_DIR, exist_ok=True)

def clean_and_feature_engineer():
    print(f'[+] Loading raw healthcare dataset from: {INPUT_CSV}')
    df = pd.read_csv(INPUT_CSV)
    raw_rows, raw_cols = df.shape
    print(f'    Raw Shape: {raw_rows} rows, {raw_cols} columns')

    # 1. Verification of Schema and Nulls
    null_counts = df.isnull().sum().to_dict()
    duplicates = int(df.duplicated().sum())

    # 2. Critical Audit: health_risk_score constant verification
    hrs_unique = df['health_risk_score'].unique().tolist()
    hrs_min = float(df['health_risk_score'].min())
    hrs_max = float(df['health_risk_score'].max())
    hrs_is_constant = (len(hrs_unique) == 1)
    print(f'    [!] Critical Audit: health_risk_score constant: {hrs_is_constant} (values: {hrs_unique})')

    # 3. Patient ID Generation
    df['patient_id'] = [f'P{i+1:04d}' for i in range(len(df))]

    # 4. Clinical Categorizations
    # Age Groups
    age_bins = [17, 30, 45, 60, 80]
    age_labels = ['18-30', '31-45', '46-60', '61-80']
    df['age_group'] = pd.cut(df['age'], bins=age_bins, labels=age_labels)

    # BMI Categories (WHO standard)
    def categorize_bmi(b):
        if b < 18.5: return 'Underweight'
        elif b < 25.0: return 'Normal'
        elif b < 30.0: return 'Overweight'
        elif b < 35.0: return 'Obesity Class I'
        else: return 'Obesity Class II+'
    df['bmi_category'] = df['bmi'].apply(categorize_bmi)

    # Blood Pressure Categories (AHA/ACC)
    def categorize_bp(bp):
        if bp < 120: return 'Normal'
        elif bp < 130: return 'Elevated'
        elif bp < 140: return 'Hypertension Stage 1'
        else: return 'Hypertension Stage 2'
    df['bp_category'] = df['blood_pressure'].apply(categorize_bp)

    # Fasting Glucose Categories (ADA guidelines)
    def categorize_glucose(g):
        if g < 100: return 'Normal'
        elif g < 126: return 'Prediabetic'
        else: return 'Diabetic Range'
    df['glucose_category'] = df['glucose'].apply(categorize_glucose)

    # Total Cholesterol Categories (NCEP ATP III)
    def categorize_chol(c):
        if c < 200: return 'Desirable'
        elif c < 240: return 'Borderline High'
        else: return 'High'
    df['cholesterol_category'] = df['cholesterol'].apply(categorize_chol)

    # Exercise Levels
    exercise_map = {0: 'Sedentary', 1: 'Moderate', 2: 'Active'}
    df['exercise_category'] = df['exercise_level'].map(exercise_map)

    # Lifestyle Strings
    df['smoking_status'] = df['smoking'].map({0: 'Non-Smoker', 1: 'Smoker'})
    df['alcohol_status'] = df['alcohol'].map({0: 'Non-Drinker', 1: 'Drinker'})

    # 5. Symptom Burden and Chronic Disease Burden
    df['symptom_count'] = df['fatigue'] + df['chest_pain'] + df['dizziness']
    df['chronic_disease_count'] = df['heart_disease'] + df['diabetes'] + df['stroke']
    df['has_comorbidity'] = (df['chronic_disease_count'] >= 2).astype(int)

    # 6. Calibrated Health Risk Score (0-100)
    # Formulated to resolve the constant raw health_risk_score:
    def calculate_calibrated_risk(row):
        score = 0.0
        # Age contribution: normalized (max 25 pts)
        score += ((row['age'] - 18) / (79 - 18)) * 25.0
        # Chronic condition burden: up to 30 pts
        score += min(30.0, row['chronic_disease_count'] * 10.0)
        # Blood pressure
        bp = row['blood_pressure']
        if bp >= 140: score += 8.0
        elif bp >= 130: score += 5.0
        elif bp >= 120: score += 2.0
        # Cholesterol
        c = row['cholesterol']
        if c >= 240: score += 7.0
        elif c >= 200: score += 4.0
        # Glucose
        g = row['glucose']
        if g >= 126: score += 8.0
        elif g >= 100: score += 4.0
        # BMI
        b = row['bmi']
        if b >= 35: score += 7.0
        elif b >= 30: score += 5.0
        elif b >= 25: score += 3.0
        # Lifestyle factors
        if row['smoking'] == 1: score += 4.0
        if row['alcohol'] == 1: score += 2.0
        if row['exercise_level'] == 0: score += 4.0
        elif row['exercise_level'] == 1: score += 2.0
        # Symptoms
        if row['chest_pain'] == 1: score += 3.0
        if row['fatigue'] == 1: score += 1.0
        if row['dizziness'] == 1: score += 1.0
        return round(min(100.0, max(0.0, score)), 1)

    df['calibrated_risk_score'] = df.apply(calculate_calibrated_risk, axis=1)

    # Risk Tiers
    def get_risk_tier(s):
        if s < 35.0: return 'Low'
        elif s < 55.0: return 'Moderate'
        elif s < 75.0: return 'High'
        else: return 'Critical'
    df['risk_tier'] = df['calibrated_risk_score'].apply(get_risk_tier)
    df['risk_tier_code'] = df['risk_tier'].map({'Low': 1, 'Moderate': 2, 'High': 3, 'Critical': 4})

    # Order columns logically
    ordered_cols = [
        'patient_id', 'age', 'age_group', 'gender', 'bmi', 'bmi_category',
        'exercise_level', 'exercise_category', 'smoking', 'smoking_status',
        'alcohol', 'alcohol_status', 'blood_pressure', 'bp_category',
        'cholesterol', 'cholesterol_category', 'glucose', 'glucose_category',
        'fatigue', 'chest_pain', 'dizziness', 'symptom_count',
        'heart_disease', 'diabetes', 'stroke', 'chronic_disease_count', 'has_comorbidity',
        'health_risk_score', 'calibrated_risk_score', 'risk_tier', 'risk_tier_code'
    ]
    df = df[ordered_cols]

    # Save cleaned dataset
    df.to_csv(OUTPUT_CSV, index=False)
    print(f'[+] Cleaned dataset saved to: {OUTPUT_CSV} ({df.shape[0]} rows, {df.shape[1]} cols)')

    # Summary Statistics
    summary = {
        'total_patients': int(len(df)),
        'total_features': int(df.shape[1]),
        'raw_health_risk_score_constant': bool(hrs_is_constant),
        'raw_health_risk_score_value': float(hrs_min),
        'gender_distribution': {k: int(v) for k, v in df['gender'].value_counts().items()},
        'age_metrics': {
            'min': int(df['age'].min()),
            'max': int(df['age'].max()),
            'mean': round(float(df['age'].mean()), 2),
            'median': int(df['age'].median())
        },
        'disease_prevalence': {
            'heart_disease_cases': int(df['heart_disease'].sum()),
            'heart_disease_pct': round(float(df['heart_disease'].mean() * 100), 2),
            'diabetes_cases': int(df['diabetes'].sum()),
            'diabetes_pct': round(float(df['diabetes'].mean() * 100), 2),
            'stroke_cases': int(df['stroke'].sum()),
            'stroke_pct': round(float(df['stroke'].mean() * 100), 2),
            'comorbidity_cases': int(df['has_comorbidity'].sum()),
            'comorbidity_pct': round(float(df['has_comorbidity'].mean() * 100), 2)
        },
        'risk_tier_distribution': {k: int(v) for k, v in df['risk_tier'].value_counts().items()},
        'calibrated_risk_score_metrics': {
            'min': float(df['calibrated_risk_score'].min()),
            'max': float(df['calibrated_risk_score'].max()),
            'mean': round(float(df['calibrated_risk_score'].mean()), 2),
            'median': round(float(df['calibrated_risk_score'].median()), 2),
            'std': round(float(df['calibrated_risk_score'].std()), 2)
        },
        'age_group_prevalence': df.groupby('age_group', observed=False)[['heart_disease', 'diabetes', 'stroke']].mean().round(4).to_dict()
    }

    with open(OUTPUT_JSON, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f'[+] Summary stats exported to: {OUTPUT_JSON}')

    return df

def generate_visualizations(df):
    print(f'[+] Generating 8 distinct healthcare visualizations in {IMG_DIR}...')
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    palette = {'Low': '#2ca02c', 'Moderate': '#1f77b4', 'High': '#ff7f0e', 'Critical': '#d62728'}

    # 1. Disease Prevalence by Age Group
    plt.figure(figsize=(9, 5.5))
    age_prev = df.groupby('age_group', observed=False)[['heart_disease', 'diabetes', 'stroke']].mean() * 100
    ax = age_prev.plot(kind='bar', figsize=(9, 5.5), colormap='coolwarm', width=0.8)
    plt.title('Chronic Disease Prevalence Across Age Groups (%)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Age Group', fontsize=11, fontweight='bold')
    plt.ylabel('Prevalence (%)', fontsize=11, fontweight='bold')
    plt.xticks(rotation=0)
    plt.ylim(0, 110)
    plt.legend(['Heart Disease', 'Diabetes', 'Stroke'], frameon=True)
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'fig1_disease_prevalence_by_age.png'), dpi=200)
    plt.close('all')

    # 2. Calibrated Risk Score Distribution
    plt.figure(figsize=(9, 5.5))
    sns.histplot(df['calibrated_risk_score'], bins=30, kde=True, color='#1f77b4', edgecolor='white', alpha=0.7)
    plt.axvline(35, color='#2ca02c', linestyle='--', linewidth=1.8, label='Low/Moderate Threshold (35)')
    plt.axvline(55, color='#ff7f0e', linestyle='--', linewidth=1.8, label='Moderate/High Threshold (55)')
    plt.axvline(75, color='#d62728', linestyle='--', linewidth=1.8, label='High/Critical Threshold (75)')
    plt.title('Calibrated Multi-Factor Health Risk Score Distribution (N=5,000)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Calibrated Risk Score (0 - 100)', fontsize=11, fontweight='bold')
    plt.ylabel('Patient Count', fontsize=11, fontweight='bold')
    plt.legend(frameon=True)
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'fig2_calibrated_risk_distribution.png'), dpi=200)
    plt.close('all')

    # 3. Biomarker Correlation Matrix
    plt.figure(figsize=(10, 8))
    corr_cols = ['age', 'bmi', 'exercise_level', 'smoking', 'alcohol', 'blood_pressure', 
                 'cholesterol', 'glucose', 'fatigue', 'chest_pain', 'dizziness', 
                 'heart_disease', 'diabetes', 'stroke', 'calibrated_risk_score']
    corr = df[corr_cols].corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, cmap='RdBu_r', center=0, annot=True, fmt='.2f', 
                cbar_kws={'shrink': 0.8}, square=True, linewidths=.5)
    plt.title('Biomarker, Lifestyle & Disease Risk Correlation Matrix', fontsize=14, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'fig3_biomarker_correlation_matrix.png'), dpi=200)
    plt.close('all')

    # 4. Lifestyle Impact on Heart Disease
    plt.figure(figsize=(9, 5.5))
    life_hd = df.groupby(['smoking_status', 'exercise_category'], observed=False)['heart_disease'].mean().unstack() * 100
    life_hd.plot(kind='bar', figsize=(9, 5.5), colormap='viridis', width=0.75)
    plt.title('Heart Disease Prevalence by Smoking & Physical Activity (%)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Smoking Status', fontsize=11, fontweight='bold')
    plt.ylabel('Heart Disease Rate (%)', fontsize=11, fontweight='bold')
    plt.xticks(rotation=0)
    plt.legend(title='Physical Activity', frameon=True)
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'fig4_lifestyle_impact_heart_disease.png'), dpi=200)
    plt.close('all')

    # 5. Comorbidity Burden Overlap (Disease Count Breakdown)
    plt.figure(figsize=(9, 5.5))
    counts = df['chronic_disease_count'].value_counts().sort_index()
    labels = ['0 Conditions (Healthy)', '1 Condition (Isolated)', '2 Conditions (Dual Morbidity)', '3 Conditions (Triad)']
    colors = ['#2ca02c', '#17becf', '#ff7f0e', '#d62728']
    plt.bar(labels, counts.values, color=colors, edgecolor='black', alpha=0.85)
    for i, v in enumerate(counts.values):
        pct = (v / len(df)) * 100
        plt.text(i, v + 40, f'{v:,} ({pct:.1f}%)', ha='center', fontweight='bold', fontsize=10)
    plt.title('Multi-Morbidity Burden Distribution in Cohort', fontsize=14, fontweight='bold', pad=15)
    plt.ylabel('Patient Count', fontsize=11, fontweight='bold')
    plt.ylim(0, max(counts.values) + 300)
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'fig5_comorbidity_trivariate_overlap.png'), dpi=200)
    plt.close('all')

    # 6. Blood Pressure vs Glucose Stratified by Risk Tier
    plt.figure(figsize=(9.5, 6))
    for tier, col in palette.items():
        sub = df[df['risk_tier'] == tier]
        plt.scatter(sub['blood_pressure'], sub['glucose'], label=tier, alpha=0.45, color=col, s=25)
    plt.axvline(140, color='gray', linestyle=':', label='Hypertension Threshold (140 mmHg)')
    plt.axhline(126, color='gray', linestyle='--', label='Diabetic Fasting Glucose (126 mg/dL)')
    plt.title('Blood Pressure vs Glucose Trajectories by Risk Tier', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Blood Pressure (mmHg)', fontsize=11, fontweight='bold')
    plt.ylabel('Fasting Glucose (mg/dL)', fontsize=11, fontweight='bold')
    plt.legend(frameon=True, loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'fig6_blood_pressure_vs_glucose_by_tier.png'), dpi=200)
    plt.close('all')

    # 7. Symptom Frequency Across Chronic Disease Status
    plt.figure(figsize=(9, 5.5))
    symp_df = df.groupby('chronic_disease_count', observed=False)[['fatigue', 'chest_pain', 'dizziness']].mean() * 100
    symp_df.plot(kind='bar', figsize=(9, 5.5), colormap='plasma', width=0.7)
    plt.title('Symptom Frequency vs Chronic Disease Burden (%)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Chronic Disease Count (0 to 3)', fontsize=11, fontweight='bold')
    plt.ylabel('Symptom Reported (%)', fontsize=11, fontweight='bold')
    plt.xticks(rotation=0)
    plt.legend(['Fatigue', 'Chest Pain', 'Dizziness'], frameon=True)
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'fig7_symptom_frequency_by_chronic_disease.png'), dpi=200)
    plt.close('all')

    # 8. BMI vs Cholesterol Risk Scatter
    plt.figure(figsize=(9.5, 6))
    scatter = plt.scatter(df['bmi'], df['cholesterol'], c=df['calibrated_risk_score'], cmap='Spectral_r', alpha=0.6, s=30)
    cbar = plt.colorbar(scatter)
    cbar.set_label('Calibrated Risk Score (0-100)', fontsize=10, fontweight='bold')
    plt.axvline(25, color='gray', linestyle=':', label='Overweight BMI (25)')
    plt.axvline(30, color='brown', linestyle='--', label='Obesity BMI (30)')
    plt.axhline(200, color='gray', linestyle=':', label='Borderline High Chol (200)')
    plt.axhline(240, color='red', linestyle='--', label='High Chol (240)')
    plt.title('BMI vs Total Cholesterol Mapped to Calibrated Risk Score', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Body Mass Index (BMI)', fontsize=11, fontweight='bold')
    plt.ylabel('Total Cholesterol (mg/dL)', fontsize=11, fontweight='bold')
    plt.legend(loc='lower right', frameon=True)
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'fig8_bmi_vs_cholesterol_risk_scatter.png'), dpi=200)
    plt.close('all')

    print('[+] All 8 visualizations successfully saved to static/img/visualizations/')

if __name__ == '__main__':
    df = clean_and_feature_engineer()
    generate_visualizations(df)
    print('[+] Data cleaning and exploratory analysis pipeline finished successfully!')
