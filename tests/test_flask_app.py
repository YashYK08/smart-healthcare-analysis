# tests/test_flask_app.py
import sys
import os
import json
import pytest

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_routes_status_200(client):
    routes = [
        '/',
        '/exploratory-analysis',
        '/tableau',
        '/story',
        '/risk-calculator',
        '/data-audit'
    ]
    for r in routes:
        resp = client.get(r)
        assert resp.status_code == 200, f"Route {r} failed with status {resp.status_code}"

def test_api_stats_structure(client):
    resp = client.get('/api/stats')
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert 'summary' in data
    assert 'age_groups' in data
    assert 'risk_tier_counts' in data
    assert len(data['age_groups']) == 4

def test_api_patients_pagination_and_filter(client):
    resp = client.get('/api/patients?page=1&limit=10')
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert data['page'] == 1
    assert data['limit'] == 10
    assert len(data['patients']) == 10
    assert data['total'] == 5000

    # Test filtering by High tier
    resp_filtered = client.get('/api/patients?page=1&limit=10&tier=High')
    data_filtered = json.loads(resp_filtered.data)
    assert data_filtered['total'] > 0
    for p in data_filtered['patients']:
        assert p['risk_tier'] == 'High'

def test_api_predict_risk_endpoint(client):
    sample_patient = {
        'age': 65,
        'gender': 'Male',
        'bmi': 31.5,
        'blood_pressure': 155,
        'cholesterol': 260,
        'glucose': 145,
        'smoking': 1,
        'alcohol': 1,
        'exercise_level': 0,
        'chest_pain': 1,
        'fatigue': 1,
        'dizziness': 0,
        'heart_disease': 1,
        'diabetes': 1,
        'stroke': 0
    }
    resp = client.post('/api/predict-risk',
                       data=json.dumps(sample_patient),
                       content_type='application/json')
    assert resp.status_code == 200
    res_data = json.loads(resp.data)
    assert 'calibrated_risk_score' in res_data
    assert res_data['risk_tier'] in ['High', 'Critical']
    assert 'breakdown' in res_data
    assert res_data['calibrated_risk_score'] >= 55.0
