# app.py - Smart Healthcare Risk & Disease Analysis Web Application
import os
import json
import pandas as pd
from flask import Flask, render_template, request, jsonify, send_file, url_for

app = Flask(__name__)
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
CLEANED_CSV = os.path.join(PROJECT_DIR, 'smart_healthcare_dataset_cleaned.csv')
SUMMARY_JSON = os.path.join(PROJECT_DIR, 'cleaned_dataset_summary.json')
TWB_FILE = os.path.join(PROJECT_DIR, 'smart_healthcare_analysis.twb')
TWBX_FILE = os.path.join(PROJECT_DIR, 'project.twbx')

# Load dataset and summary
df = pd.read_csv(CLEANED_CSV)
with open(SUMMARY_JSON, 'r') as f:
    summary_data = json.load(f)

def compute_risk(data):
    try:
        age = float(data.get('age', 45))
        bmi = float(data.get('bmi', 24.5))
        bp = float(data.get('blood_pressure', 120))
        chol = float(data.get('cholesterol', 200))
        glucose = float(data.get('glucose', 100))
        smoking = int(data.get('smoking', 0))
        alcohol = int(data.get('alcohol', 0))
        exercise = int(data.get('exercise_level', 1))
        fatigue = int(data.get('fatigue', 0))
        chest_pain = int(data.get('chest_pain', 0))
        dizziness = int(data.get('dizziness', 0))
        heart_disease = int(data.get('heart_disease', 0))
        diabetes = int(data.get('diabetes', 0))
        stroke = int(data.get('stroke', 0))
    except (ValueError, TypeError):
        return None

    score = 0.0
    # 1. Age (0-25)
    age_pts = max(0.0, min(25.0, ((age - 18) / (79 - 18)) * 25.0))
    score += age_pts

    # 2. Chronic condition burden (0-30)
    disease_count = heart_disease + diabetes + stroke
    chronic_pts = min(30.0, disease_count * 10.0)
    score += chronic_pts

    # 3. Blood Pressure (0-8)
    if bp >= 140: bp_pts = 8.0
    elif bp >= 130: bp_pts = 5.0
    elif bp >= 120: bp_pts = 2.0
    else: bp_pts = 0.0
    score += bp_pts

    # 4. Cholesterol (0-7)
    if chol >= 240: chol_pts = 7.0
    elif chol >= 200: chol_pts = 4.0
    else: chol_pts = 0.0
    score += chol_pts

    # 5. Fasting Glucose (0-8)
    if glucose >= 126: glu_pts = 8.0
    elif glucose >= 100: glu_pts = 4.0
    else: glu_pts = 0.0
    score += glu_pts

    # 6. BMI (0-7)
    if bmi >= 35: bmi_pts = 7.0
    elif bmi >= 30: bmi_pts = 5.0
    elif bmi >= 25: bmi_pts = 3.0
    else: bmi_pts = 0.0
    score += bmi_pts

    # 7. Lifestyle (0-10)
    smk_pts = 4.0 if smoking == 1 else 0.0
    alc_pts = 2.0 if alcohol == 1 else 0.0
    if exercise == 0: exe_pts = 4.0
    elif exercise == 1: exe_pts = 2.0
    else: exe_pts = 0.0
    score += (smk_pts + alc_pts + exe_pts)

    # 8. Symptoms (0-5)
    cp_pts = 3.0 if chest_pain == 1 else 0.0
    fat_pts = 1.0 if fatigue == 1 else 0.0
    diz_pts = 1.0 if dizziness == 1 else 0.0
    score += (cp_pts + fat_pts + diz_pts)

    total_score = round(min(100.0, max(0.0, score)), 1)
    if total_score < 35.0:
        tier = 'Low'
        tier_color = 'success'
        recommendation = 'Maintain regular healthy lifestyle, routine annual health checkup, and balanced diet.'
    elif total_score < 55.0:
        tier = 'Moderate'
        tier_color = 'primary'
        recommendation = 'Adopt lifestyle modifications: aerobic exercise 150 min/week, dietary sodium reduction, biannual metabolic monitoring.'
    elif total_score < 75.0:
        tier = 'High'
        tier_color = 'warning'
        recommendation = 'Consult primary care physician for clinical biomarker intervention, medication review, and cardiovascular risk reduction.'
    else:
        tier = 'Critical'
        tier_color = 'danger'
        recommendation = 'Immediate specialist evaluation required (Cardiology / Endocrinology). Intensive multi-factor disease management protocol.'

    return {
        'calibrated_risk_score': total_score,
        'risk_tier': tier,
        'risk_tier_color': tier_color,
        'recommendation': recommendation,
        'breakdown': {
            'age_points': round(age_pts, 1),
            'chronic_points': round(chronic_pts, 1),
            'blood_pressure_points': round(bp_pts, 1),
            'cholesterol_points': round(chol_pts, 1),
            'glucose_points': round(glu_pts, 1),
            'bmi_points': round(bmi_pts, 1),
            'lifestyle_points': round(smk_pts + alc_pts + exe_pts, 1),
            'symptom_points': round(cp_pts + fat_pts + diz_pts, 1)
        }
    }

@app.route('/')
def index():
    return render_template('index.html', summary=summary_data)

@app.route('/exploratory-analysis')
def eda():
    return render_template('eda.html', summary=summary_data)

@app.route('/tableau')
def tableau():
    return render_template('tableau.html', summary=summary_data)

@app.route('/story')
def story():
    return render_template('story.html', summary=summary_data)

@app.route('/risk-calculator')
def calculator():
    return render_template('calculator.html')

@app.route('/data-audit')
def audit():
    return render_template('audit.html', summary=summary_data)

@app.route('/download-cleaned-data')
def download_cleaned_data():
    return send_file(CLEANED_CSV, as_attachment=True, download_name='smart_healthcare_dataset_cleaned.csv')

@app.route('/download-twbx')
def download_twbx():
    return send_file(TWBX_FILE, as_attachment=True, download_name='project.twbx')

@app.route('/download-twb')
def download_twb():
    return send_file(TWB_FILE, as_attachment=True, download_name='smart_healthcare_analysis.twb')

@app.route('/api/stats')
def api_stats():
    # Real computed aggregations for dynamic frontend charts
    age_groups = df.groupby('age_group', observed=False).agg(
        total=('patient_id', 'count'),
        heart_disease_pct=('heart_disease', lambda x: round(float(x.mean() * 100), 1)),
        diabetes_pct=('diabetes', lambda x: round(float(x.mean() * 100), 1)),
        stroke_pct=('stroke', lambda x: round(float(x.mean() * 100), 1)),
        avg_risk=('calibrated_risk_score', lambda x: round(float(x.mean()), 1))
    ).reset_index().to_dict(orient='records')

    risk_tier_counts = df['risk_tier'].value_counts().to_dict()
    bp_cat_counts = df['bp_category'].value_counts().to_dict()
    glucose_cat_counts = df['glucose_category'].value_counts().to_dict()

    return jsonify({
        'summary': summary_data,
        'age_groups': age_groups,
        'risk_tier_counts': risk_tier_counts,
        'bp_cat_counts': bp_cat_counts,
        'glucose_cat_counts': glucose_cat_counts
    })

@app.route('/api/patients')
def api_patients():
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 15))
    except ValueError:
        page, limit = 1, 15

    tier_filter = request.args.get('tier', '').strip()
    gender_filter = request.args.get('gender', '').strip()
    age_filter = request.args.get('age_group', '').strip()

    filtered_df = df
    if tier_filter:
        filtered_df = filtered_df[filtered_df['risk_tier'] == tier_filter]
    if gender_filter:
        filtered_df = filtered_df[filtered_df['gender'] == gender_filter]
    if age_filter:
        filtered_df = filtered_df[filtered_df['age_group'] == age_filter]

    total_matched = len(filtered_df)
    start = (page - 1) * limit
    end = start + limit
    page_data = filtered_df.iloc[start:end].to_dict(orient='records')

    return jsonify({
        'page': page,
        'limit': limit,
        'total': total_matched,
        'patients': page_data
    })

@app.route('/api/predict-risk', methods=['POST'])
def api_predict_risk():
    data = request.get_json(silent=True) or request.form
    result = compute_risk(data)
    if result is None:
        return jsonify({'error': 'Invalid clinical input parameters'}), 400
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
