# tests/test_data_cleaning.py
import os
import pandas as pd
import pytest

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_CSV = os.path.join(PROJECT_DIR, 'smart_healthcare_dataset.csv')
CLEANED_CSV = os.path.join(PROJECT_DIR, 'smart_healthcare_dataset_cleaned.csv')

def test_raw_dataset_exists_and_shape():
    assert os.path.exists(RAW_CSV), "Raw dataset file must exist"
    df = pd.read_csv(RAW_CSV)
    assert df.shape[0] == 5000, f"Expected 5,000 rows, got {df.shape[0]}"
    assert df.shape[1] == 16, f"Expected 16 columns, got {df.shape[1]}"

def test_raw_health_risk_score_is_constant():
    """Verify and audit requirement 10: health_risk_score field is constant 100.0."""
    df = pd.read_csv(RAW_CSV)
    unique_vals = df['health_risk_score'].unique().tolist()
    assert len(unique_vals) == 1, f"Expected constant health_risk_score, but found: {unique_vals}"
    assert unique_vals[0] == 100.0, f"Expected constant value 100.0, got: {unique_vals[0]}"

def test_cleaned_dataset_schema_and_integrity():
    assert os.path.exists(CLEANED_CSV), "Cleaned dataset file must exist"
    df = pd.read_csv(CLEANED_CSV)
    assert len(df) == 5000
    assert df.isnull().sum().sum() == 0, "Cleaned dataset should have zero missing values"
    
    # Check engineered columns
    required_cols = [
        'patient_id', 'age_group', 'bmi_category', 'bp_category',
        'glucose_category', 'cholesterol_category', 'exercise_category',
        'symptom_count', 'chronic_disease_count', 'has_comorbidity',
        'calibrated_risk_score', 'risk_tier', 'risk_tier_code'
    ]
    for col in required_cols:
        assert col in df.columns, f"Engineered column {col} missing from cleaned dataset"

def test_calibrated_risk_score_variance_and_bounds():
    df = pd.read_csv(CLEANED_CSV)
    scores = df['calibrated_risk_score']
    assert scores.min() >= 0.0, "Score cannot be below 0"
    assert scores.max() <= 100.0, "Score cannot exceed 100"
    assert scores.std() > 10.0, "Calibrated score must have meaningful statistical dispersion"
    
    tiers = set(df['risk_tier'].unique())
    assert tiers == {'Low', 'Moderate', 'High', 'Critical'}, f"Unexpected tiers: {tiers}"
