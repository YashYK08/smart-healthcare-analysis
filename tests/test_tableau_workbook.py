# tests/test_tableau_workbook.py
import os
import zipfile
import xml.etree.ElementTree as ET
import pytest

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TWB_PATH = os.path.join(PROJECT_DIR, 'smart_healthcare_analysis.twb')
TWBX_PATH = os.path.join(PROJECT_DIR, 'project.twbx')

def test_twb_file_exists_and_valid_xml():
    assert os.path.exists(TWB_PATH), "smart_healthcare_analysis.twb must exist"
    tree = ET.parse(TWB_PATH)
    root = tree.getroot()
    assert root.tag == 'workbook'

def test_twb_datasources_and_calculated_fields():
    tree = ET.parse(TWB_PATH)
    root = tree.getroot()
    
    # Check datasource
    ds = root.find('.//datasource')
    assert ds is not None
    assert 'smart_healthcare' in ds.get('caption', '')
    
    # Check calculated fields
    calc_elements = root.findall('.//calculation')
    assert len(calc_elements) >= 3, "Tableau workbook must contain custom calculated fields"
    
    # Check worksheets
    worksheets = root.findall('.//worksheet')
    assert len(worksheets) >= 8, f"Expected at least 8 worksheets, found {len(worksheets)}"
    
    # Check dashboards
    dashboards = root.findall('.//dashboard')
    assert len(dashboards) >= 2, f"Expected at least 2 dashboards, found {len(dashboards)}"

def test_twbx_archive_integrity():
    assert os.path.exists(TWBX_PATH), "project.twbx packaged workbook must exist"
    with zipfile.ZipFile(TWBX_PATH, 'r') as z:
        names = z.namelist()
        assert 'Book1.twb' in names or any(n.endswith('.twb') for n in names)
        assert any('smart_healthcare_dataset_cleaned.csv' in n for n in names)
