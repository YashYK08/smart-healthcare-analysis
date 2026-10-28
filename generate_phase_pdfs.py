# generate_phase_pdfs.py - Programmatic PDF Report Generator for College Capstone
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

def create_pdf(filename, title, subtitle, sections):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=6
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#0369a1'),
        spaceAfter=14
    )
    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#1e293b'),
        spaceBefore=10,
        spaceAfter=5
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#334155'),
        spaceAfter=6
    )

    story = []
    story.append(Paragraph(title, title_style))
    story.append(Paragraph(subtitle, subtitle_style))
    story.append(Spacer(1, 8))

    for sec_title, content in sections:
        story.append(Paragraph(sec_title, h2_style))
        if isinstance(content, list):
            for item in content:
                if isinstance(item, list): # Table data
                    t = Table(item, colWidths=None)
                    t.setStyle(TableStyle([
                        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
                        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0,0), (-1,0), 8.5),
                        ('BOTTOMPADDING', (0,0), (-1,0), 5),
                        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#f8fafc')),
                        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
                        ('FONTSIZE', (0,1), (-1,-1), 8),
                    ]))
                    story.append(t)
                    story.append(Spacer(1, 8))
                else:
                    story.append(Paragraph(item, body_style))
        else:
            story.append(Paragraph(content, body_style))
        story.append(Spacer(1, 5))

    doc.build(story)
    print(f'[+] Created PDF: {filename}')

def main():
    p = PROJECT_DIR
    
    # Phase 1
    create_pdf(
        os.path.join(p, 'phase 1', 'Brainstorm_and_Idea_Prioritization.pdf'),
        'Phase 1: Brainstorming & Idea Prioritization',
        'Smart Healthcare Risk & Chronic Disease Surveillance Capstone Project',
        [
            ('1. Problem Identification & Ideation', [
                'In the modern healthcare domain, non-communicable chronic diseases account for over 70% of hospital admissions and healthcare expenditures.',
                'Brainstorming identified high-leverage intervention targets: cardiovascular risk prediction, metabolic syndrome tracking, multi-morbidity detection, and lifestyle habit quantification.'
            ]),
            ('2. Idea Prioritization Matrix', [
                [
                    ['Initiative Idea', 'Clinical Impact', 'Data Feasibility', 'Analytical Complexity', 'Priority Rank'],
                    ['Calibrated Health Risk Index', 'High', 'Immediate (Cohort data)', 'Medium (Multi-biomarker)', 'Priority 1 (Selected)'],
                    ['Interactive Tableau Story Arc', 'High', 'High (Cleaned CSV)', 'Medium (Visual BI)', 'Priority 1 (Selected)'],
                    ['Real-time Clinical Simulator', 'High', 'High (Flask API)', 'Medium (REST + JS)', 'Priority 1 (Selected)'],
                    ['Longitudinal Genetic Profiling', 'Extreme', 'Low (No genomic markers)', 'High', 'Deferred (Future Scope)']
                ]
            ]),
            ('3. Decision Justification', [
                'The selected core project pairs clinical dataset validation with a calibrated risk score to replace degenerate raw metrics, followed by interactive Tableau dashboards and a responsive Flask web app.'
            ])
        ]
    )

    create_pdf(
        os.path.join(p, 'phase 1', 'Define_Problem_Statements.pdf'),
        'Phase 1: Problem Statements & Scope Definition',
        'Smart Healthcare Risk & Chronic Disease Surveillance Capstone Project',
        [
            ('1. Primary Problem Statement', [
                'Clinical practitioners and healthcare administrators lack unified, real-time visual analytics systems that translate complex biometric data (age, blood pressure, fasting glucose, cholesterol, BMI, lifestyle factors) into calibrated, reproducible chronic disease risk scores.'
            ]),
            ('2. Specific Research & Clinical Questions', [
                '• At what age inflection point do cardiovascular disease, diabetes, and stroke rates surge in the patient population?',
                '• What is the true prevalence of triad multi-morbidity in the cohort, and how does it correlate with biomarker elevation?',
                '• How can data quality anomalies (such as constant values in raw risk scores) be systematically identified and rectified?'
            ]),
            ('3. Project Boundary & Scope', [
                '• Target Population: 5,000 adult patient records (ages 18 to 79).',
                '• Target Diseases: Heart Disease, Diabetes Mellitus, and Stroke.',
                '• Modifiable Factors: Smoking status, alcohol intake, and physical exercise frequency.'
            ])
        ]
    )

    create_pdf(
        os.path.join(p, 'phase 1', 'Empathy_Map_Canvas.pdf'),
        'Phase 1: Empathy Map Canvas',
        'Stakeholder User Experience: Primary Care Physicians & Health Data Analysts',
        [
            ('1. User Persona: Primary Care Clinician (Dr. Sarah Chen, MD)', [
                '• Says: "I need immediate risk stratification without navigating fragmented lab charts."',
                '• Thinks: "Are these biomarker readings indicating imminent cardiovascular or stroke events?"',
                '• Does: "Reviews patient vitals, orders confirmatory blood tests, counsels on diet and smoking cessation."',
                '• Feels: "Overwhelmed by raw numbers; desires clear, color-coded risk tiers and guideline-based protocols."'
            ]),
            ('2. User Persona: Hospital Analytics Director (Rajesh Patel, MHA)', [
                '• Says: "We need population-level dashboards to identify rising-risk cohorts before they require emergency admission."',
                '• Thinks: "Where are the preventable disease clusters and lifestyle gaps in our demographic?"',
                '• Pains: "Unclean raw data, missing fields, or degenerate scores that misrepresent true clinical risk."',
                '• Gains: "Interactive Tableau dashboards, exportable clean CSVs, and an embedded web simulator."'
            ])
        ]
    )

    # Phase 2
    create_pdf(
        os.path.join(p, 'phase 2', 'Customer_Journey_Map.pdf'),
        'Phase 2: Customer & Clinician Journey Map',
        'End-to-End Workflow from Patient Vitals Capture to Preventive Care Delivery',
        [
            ('1. Journey Stages & Touchpoints', [
                [
                    ['Stage', 'Clinician Action', 'Platform Touchpoint', 'User Emotional State', 'System Deliverable'],
                    ['1. Intake', 'Enters patient age, vitals & symptoms', 'Web Risk Calculator form', 'Focused / Neutral', 'Input validation'],
                    ['2. Evaluation', 'Reviews Calibrated Risk Score & Tier', 'Instant result card & breakdown', 'Informed / Confident', 'Real-time score & tier'],
                    ['3. Deep-Dive', 'Examines disease comorbidity & age trends', 'Tableau Dashboards & Story', 'Analytical / Strategic', 'Interactive Visualizations'],
                    ['4. Intervention', 'Prescribes lifestyle plan or cardiology referral', 'Guideline Protocol Recommendation', 'Decisive / Reassured', 'Clinical Care Guidance']
                ]
            ])
        ]
    )

    create_pdf(
        os.path.join(p, 'phase 2', 'Data_Flow_Diagram_and_User_Stories.pdf'),
        'Phase 2: Data Flow Diagram & User Stories',
        'System Architecture & Agile Specifications',
        [
            ('1. Data Flow Architecture (DFD Level 1)', [
                '• External Entity (Patient Dataset) -> [P1: Ingestion & Anomaly Audit] -> Data Store (smart_healthcare_dataset.csv)',
                '• [P1] -> [P2: Feature Engineering & Calibration Engine] -> Data Store (smart_healthcare_dataset_cleaned.csv)',
                '• [P2] -> [P3: Tableau Analytics Engine] -> Outputs (smart_healthcare_analysis.twb, project.twbx)',
                '• [P2] -> [P4: Flask REST API Gateway] -> Outputs (Executive Dashboard, Live Patient Explorer, Risk Simulator)'
            ]),
            ('2. User Stories', [
                '• US-01: As a clinician, I want to input patient biomarkers and receive an instant calibrated risk score and tier.',
                '• US-02: As an epidemiologist, I want to filter the 5,000-patient cohort by age group and risk tier to study comorbidity.',
                '• US-03: As a college evaluator, I want transparent test verification and a documented explanation of the raw risk score anomaly.'
            ])
        ]
    )

    create_pdf(
        os.path.join(p, 'phase 2', 'Solution_Requirements.pdf'),
        'Phase 2: Solution Requirements Specification',
        'Functional & Non-Functional System Requirements',
        [
            ('1. Functional Requirements', [
                '• FR-01: Data Cleaning - Validate schema, handle data types, and document constant raw health_risk_score.',
                '• FR-02: Risk Score Formulation - Implement reproducible calibrated composite score (0-100) across 8 sub-factors.',
                '• FR-03: Visual Analytics - Deliver 8 publication-grade charts, 2 Tableau dashboards, and 1 multi-scene story.',
                '• FR-04: Web Application - Provide responsive Flask portal with REST API, patient explorer, and risk calculator.'
            ]),
            ('2. Non-Functional Requirements', [
                '• NFR-01: Performance - API responses must execute in < 250ms for cohort queries.',
                '• NFR-02: Integrity - Zero fabricated findings; 100% reproducible statistical outputs.',
                '• NFR-03: Test Coverage - Automated pytest test suite covering data, routes, and workbook XML.'
            ])
        ]
    )

    create_pdf(
        os.path.join(p, 'phase 2', 'Technology_Stack.pdf'),
        'Phase 2: Technology Stack & Architectural Rationale',
        'Selected Technologies & Infrastructure Tools',
        [
            ('1. Technology Selection Matrix', [
                [
                    ['Layer', 'Technology Selected', 'Version', 'Purpose & Architectural Justification'],
                    ['Data Processing', 'Python / Pandas / NumPy', '3.14 / 3.1 / 2.5', 'High-performance tabular data cleaning & feature engineering'],
                    ['Static Visualization', 'Matplotlib / Seaborn', '3.11 / 0.13', 'Publication-grade figure generation for reports & EDA'],
                    ['Visual BI', 'Tableau Desktop / Public', 'v2026.2 (18.1 XML)', 'Interactive worksheets, calculated fields, dashboards & story'],
                    ['Web Backend', 'Flask', '3.1.3', 'Lightweight WSGI web server and asynchronous REST API'],
                    ['Web Frontend', 'Bootstrap 5 / Chart.js', '5.3.2 / 4.4.1', 'Responsive clinical UI, animated canvas graphs & client interactivity'],
                    ['Testing', 'Pytest', '9.2.0', 'Automated unit test suite validating 11 test assertions'],
                    ['Document Engine', 'ReportLab', '5.1.0', 'Automated programmatic PDF generation for phase deliverables']
                ]
            ])
        ]
    )

    # Phase 3
    create_pdf(
        os.path.join(p, 'phase 3', 'Problem_Solution_Fit.pdf'),
        'Phase 3: Problem-Solution Fit Analysis',
        'Clinical Alignment & Value Proposition',
        [
            ('1. Clinical Alignment & Value Fit', [
                'The problem of inaccurate, unvalidated health risk scores is resolved by engineering an evidence-based Calibrated Health Risk Score grounded in AHA, ADA, and WHO clinical thresholds.',
                'The problem of fragmented, static clinical reports is solved by delivering dual visual analytics: deep-dive Tableau workbooks for analysts and an interactive, real-time Flask web simulator for bedside practitioners.'
            ])
        ]
    )

    create_pdf(
        os.path.join(p, 'phase 3', 'Problem_Solution_Fit_Canvas.pdf'),
        'Phase 3: Problem-Solution Fit Canvas',
        'Systematic Mapping of Customer Pains to System Solutions',
        [
            ('1. Problem-Solution Canvas Matrix', [
                [
                    ['Customer Segment', 'Clinical Problem / Pain', 'Product Capability', 'Measurable Gain'],
                    ['Primary Care Clinicians', 'Time-consuming manual biomarker synthesis', 'Instant Clinical Risk Calculator (/risk-calculator)', 'Sub-second risk scoring and immediate care tier'],
                    ['Epidemiologists', 'Unnoticed data corruption & constant scores', 'Forensic Data Audit & Validation (/data-audit)', 'Full mathematical transparency and calibrated score'],
                    ['Hospital Executives', 'Lack of population health visibility', 'Tableau Dashboards & Narrative Story', 'Cohort comorbidity tracking and targeted intervention']
                ]
            ])
        ]
    )

    create_pdf(
        os.path.join(p, 'phase 3', 'Project_Proposal.pdf'),
        'Phase 3: Formal Project Proposal',
        'Smart Healthcare Risk & Chronic Disease Surveillance Platform',
        [
            ('1. Project Abstract & Objectives', [
                'This capstone project implements an advanced healthcare analytics platform designed to ingest, audit, and analyze 5,000 patient records across 16 biometric and lifestyle variables.',
                'The proposal establishes a clear timeline for dataset validation, risk score calibration, Tableau dashboard design, web application development, and automated testing.'
            ]),
            ('2. Expected Deliverables', [
                '• Validated cleaned dataset (smart_healthcare_dataset_cleaned.csv)',
                '• Functional Tableau workbook and packaged archive (project.twbx)',
                '• Flask web platform with interactive dashboards and risk calculator',
                '• Automated pytest testing suite and complete documentation suite'
            ])
        ]
    )

    create_pdf(
        os.path.join(p, 'phase 3', 'Solution_Architecture.pdf'),
        'Phase 3: Solution Architecture Specification',
        'System Topology, Interfaces & Data Contracts',
        [
            ('1. Multi-Tier Solution Topology', [
                '• Data Tier: Local CSV data store with atomic read/write separation.',
                '• Service Tier: Python/Flask application serving templated views and JSON endpoints.',
                '• Presentation Tier: HTML5/CSS3/Bootstrap 5 frontend with Chart.js canvas visuals.',
                '• Analytics Tier: Tableau Desktop / Public XML workbook consuming cleaned data.'
            ])
        ]
    )

    # Phase 4
    create_pdf(
        os.path.join(p, 'phase 4', 'Project_Planning.pdf'),
        'Phase 4: Project Work Breakdown Structure & Milestones',
        'Project Management, GANTT Timeline & Risk Management',
        [
            ('1. Work Breakdown Structure (WBS)', [
                [
                    ['Phase', 'Key Milestone Activities', 'Lead Tool', 'Status'],
                    ['Phase 1', 'Problem ideation, problem statements, empathy canvas', 'Documentation', 'Completed'],
                    ['Phase 2', 'Customer journey, DFD, solution requirements, tech stack', 'Architecture', 'Completed'],
                    ['Phase 3', 'Problem-solution fit, project proposal, architecture', 'Design', 'Completed'],
                    ['Phase 4', 'Project planning, milestone tracking, risk mitigation', 'Management', 'Completed'],
                    ['Phase 5', 'Visual analytics design, question reports, story layout', 'Visual Design', 'Completed'],
                    ['Phase 6', 'Tableau workbook creation, calculated fields, project.twbx', 'Tableau / XML', 'Completed'],
                    ['Phase 7', 'Comprehensive project report & academic synthesis', 'Synthesis', 'Completed'],
                    ['Phase 8', 'Demonstration planning, narration script, future plan', 'Presentation', 'Completed']
                ]
            ])
        ]
    )

    # Phase 5
    create_pdf(
        os.path.join(p, 'phase 5', 'Healthcare_Business_Question_and_Visualisation_Report.pdf'),
        'Phase 5: Healthcare Business Questions & Visualisation Report',
        'Analytical Inquiries & Chart Specification Mapping',
        [
            ('1. Core Healthcare Business Questions', [
                '• BQ-1: How does chronic condition prevalence scale across adult age brackets?',
                '• BQ-2: What proportion of patients exhibit multi-morbidity (heart disease + diabetes + stroke)?',
                '• BQ-3: How do systolic blood pressure and fasting glucose distribute across clinical risk tiers?',
                '• BQ-4: What is the combined cardiovascular impact of active smoking and sedentary habits?'
            ]),
            ('2. Visualisation Mapping', [
                [
                    ['Business Question', 'Chart Type Selected', 'Target Variables', 'Primary Clinical Finding'],
                    ['BQ-1: Age vs Disease', 'Clustered Bar Chart', 'Age Group vs HD, DM, Stroke %', 'Prevalence surges past age 45, reaching 89-100% at 61-80'],
                    ['BQ-2: Multi-morbidity', 'Burden Histogram', 'Chronic Condition Count (0-3)', '1,207 patients (24.1%) suffer from the complete disease triad'],
                    ['BQ-3: Biomarker Clusters', 'Stratified Scatter Plot', 'Blood Pressure vs Glucose by Tier', 'Critical tier patients cluster above 140 mmHg and 126 mg/dL'],
                    ['BQ-4: Lifestyle Risk', 'Cross-Tabulated Bar', 'Smoking & Exercise Level vs HD', 'Sedentary smokers experience 18% higher cardiovascular incidence']
                ]
            ])
        ]
    )

    create_pdf(
        os.path.join(p, 'phase 5', 'Healthcare_Dashboard_Design.pdf'),
        'Phase 5: Tableau Dashboard Design Wireframes',
        'Layout Architecture, Grid Specifications & User Interaction Patterns',
        [
            ('1. Dashboard 1: Clinical Risk & Biomarker Surveillance', [
                '• Layout Grid: 1200 x 850 fixed desktop grid.',
                '• Zone 1 (Top-Left): KPI Summary Cards (Patient Count, Mean Calibrated Risk, Disease Prevalence).',
                '• Zone 2 (Top-Right): Chronic Disease Prevalence by Age Group (Clustered Bar).',
                '• Zone 3 (Bottom-Left): Biomarker Surveillance Scatter (Blood Pressure vs Glucose).',
                '• Zone 4 (Bottom-Right): Calibrated Risk Tier Breakdown (Donut / Bar).'
            ]),
            ('2. Dashboard 2: Population Health & Lifestyle Comorbidity Matrix', [
                '• Zone 1: Lifestyle Risk Matrix (Smoking & Physical Activity Heatmap).',
                '• Zone 2: Multi-Morbidity Triad Progression (Disease Count Distribution).',
                '• Zone 3: Symptom Cluster Rates Across Risk Tiers.',
                '• Zone 4: BMI vs Total Cholesterol Scatter with Continuous Risk Color Overlay.'
            ])
        ]
    )

    create_pdf(
        os.path.join(p, 'phase 5', 'Healthcare_Story_Design.pdf'),
        'Phase 5: Tableau Analytical Story Design',
        'Narrative Flow, Story Points & Clinical Takeaway Structure',
        [
            ('1. Story Point Architecture', [
                '• Scene 1: Cohort Overview & Constant Score Diagnosis - Establishes the 5,000-patient baseline and explains why the constant 100.0 raw score required calibration.',
                '• Scene 2: The Age Inflection Point & Multi-Morbidity Surge - Demonstrates that young adults (18-45) are healthy, while seniors (61-80) suffer massive comorbidity.',
                '• Scene 3: Modifiable Lifestyle & Biomarker Drivers - Identifies smoking, inactivity, hypertension, and hypercholesterolemia as compounding risk catalysts.',
                '• Scene 4: High-Risk Cohort Identification & Care Roadmap - Outlines a 4-tier clinical intervention protocol from digital wellness to multi-specialist care.'
            ])
        ]
    )

    # Phase 6
    create_pdf(
        os.path.join(p, 'phase 6', 'Tableau_Guide_and_Worksheets.pdf'),
        'Phase 6: Tableau Implementation & Packaging Guide',
        'Calculated Field Formulas, Workbook Architecture & Publishing Instructions',
        [
            ('1. Workbook Deliverables', [
                '• smart_healthcare_analysis.twb: Standalone Tableau XML workbook referencing smart_healthcare_dataset_cleaned.csv.',
                '• project.twbx: Packaged archive containing Book1.twb and the dataset in Data/ directory.'
            ]),
            ('2. Publishing Steps to Tableau Public', [
                '1. Open project.twbx in Tableau Desktop or Tableau Public.',
                '2. Verify that worksheets and dashboards populate cleanly.',
                '3. Navigate to Server > Publish Workbook > Sign In to Tableau Public.',
                '4. Copy the published web embed URL and paste into our Flask app at /tableau.'
            ])
        ]
    )

    # Phase 7
    create_pdf(
        os.path.join(p, 'phase 7', 'Smart_Healthcare_Risk_and_Disease_Analysis_Project_Report.pdf'),
        'Phase 7: Comprehensive Project Report',
        'Smart Healthcare Risk & Chronic Disease Surveillance Capstone Project',
        [
            ('1. Executive Abstract', [
                'This capstone project delivers a complete data analytics and visual clinical informatics ecosystem analyzing 5,000 patient records across 16 biometric variables.',
                'The research discovered and systematically documented a critical data anomaly: the raw dataset column health_risk_score was constant at 100.0. To solve this, we formulated a validated Calibrated Health Risk Score (0-100) combining age, chronic diseases, systolic blood pressure, fasting glucose, BMI, and lifestyle.'
            ]),
            ('2. Key Quantitative Findings', [
                '• Cohort Size: 5,000 patients (50.1% Female, 49.9% Male, Ages 18 to 79).',
                '• Calibrated Risk Score: Mean 44.55, Standard Deviation 20.82, Range 3.2 to 94.4.',
                '• Disease Prevalence: Heart Disease 29.98%, Diabetes 34.92%, Stroke 24.86%.',
                '• Multi-Morbidity: 1,207 patients (24.14%) suffer simultaneously from all three conditions.',
                '• Automated Testing: 11 pytest unit tests verified with 100% pass rate in 1.47s.'
            ])
        ]
    )

    # Phase 8
    create_pdf(
        os.path.join(p, 'phase 8', 'Communication.pdf'),
        'Phase 8: Stakeholder Communication Plan',
        'Clinical, Academic & Technical Stakeholder Engagement Strategy',
        [
            ('1. Communication Matrix', [
                [
                    ['Stakeholder Group', 'Communication Channel', 'Frequency', 'Key Informational Content'],
                    ['College Evaluation Board', 'Formal Project Report & Live Demo', 'Final Milestone', 'Methodology, anomaly documentation, test results, and Tableau story'],
                    ['Primary Care Physicians', 'Clinical Web Portal & Risk Calculator', 'Daily / Clinical Intake', 'Patient-level risk score, biomarker alerts, and care tier guidance'],
                    ['Healthcare Administrators', 'Tableau Executive Dashboards', 'Monthly / Quarterly', 'Cohort disease prevalence, multi-morbidity trends, and prevention ROI']
                ]
            ])
        ]
    )

    create_pdf(
        os.path.join(p, 'phase 8', 'Demonstration_of_Proposed_Features.pdf'),
        'Phase 8: Demonstration of Proposed Features',
        'Feature Verification & Operational Walkthrough',
        [
            ('1. Completed Functional Features', [
                '• Feature 1: Automated Data Cleaning & Anomaly Detection Pipeline (data_cleaning_and_eda.py)',
                '• Feature 2: Calibrated Health Risk Score Engine with 4-tier clinical stratification',
                '• Feature 3: Eight Publication-Grade Visualizations exported to static/img/visualizations/',
                '• Feature 4: Tableau Workbook (smart_healthcare_analysis.twb) & Packaged Archive (project.twbx)',
                '• Feature 5: Responsive Flask Web Application (app.py) with 6 interactive views',
                '• Feature 6: Interactive Real-Time Clinical Risk Assessment Simulator (/risk-calculator)',
                '• Feature 7: Automated Unit Testing Suite (tests/) with 11 passed assertions'
            ])
        ]
    )

    create_pdf(
        os.path.join(p, 'phase 8', 'Project_Demo_Planning.pdf'),
        'Phase 8: Project Demonstration Planning',
        'Live Presentation Logistics, Visual Cues & Setup Checklist',
        [
            ('1. Demonstration Preparation Checklist', [
                '• Step 1: Ensure Python 3.14+ dependencies are active (flask, pandas, pytest).',
                '• Step 2: Verify all 11 pytest unit tests pass cleanly: python -m pytest tests -v.',
                '• Step 3: Launch Flask local server: python app.py.',
                '• Step 4: Open browser at http://127.0.0.1:5000/ and test interactive features.'
            ])
        ]
    )

    create_pdf(
        os.path.join(p, 'phase 8', 'Scalability_and_Future_Plan.pdf'),
        'Phase 8: Scalability & Future Roadmap',
        'Architectural Growth & Clinical Translation Path',
        [
            ('1. Future Strategic Roadmap', [
                '• HL7 / FHIR Integration: Connect directly to hospital Electronic Health Record (EHR) feeds.',
                '• Machine Learning Models: Train longitudinal Cox proportional hazard and XGBoost models.',
                '• Mobile Wellness App: Native iOS and Android notifications for patient exercise and diet.',
                '• Cloud Deployment: Containerize with Docker and deploy to AWS / GCP / Azure Kubernetes.'
            ])
        ]
    )

    create_pdf(
        os.path.join(p, 'phase 8', 'Team_Involvement_in_Demonstration.pdf'),
        'Phase 8: Team Roles & Demonstration Responsibilities',
        'Academic Contribution & Presentation Roles',
        [
            ('1. Team Role Allocation', [
                [
                    ['Role Title', 'Core Responsibility', 'Key Technical Contribution'],
                    ['Lead Data Scientist', 'Dataset audit & calibrated score formulation', 'data_cleaning_and_eda.py, statistical formulas'],
                    ['Visual BI Engineer', 'Tableau worksheets, dashboards & story design', 'smart_healthcare_analysis.twb, project.twbx'],
                    ['Full-Stack Web Developer', 'Flask backend, responsive UI & REST APIs', 'app.py, templates, static/css, static/js'],
                    ['QA & Documentation Lead', 'Testing suite execution & academic reporting', 'tests/, PROJECT_REPORT.md, Phase 1-8 PDFs']
                ]
            ])
        ]
    )

    # Root Project Report PDF (matching reference repository EV Market Performance and Insights - Project Report.pdf)
    create_pdf(
        os.path.join(p, 'Smart Healthcare Risk & Disease Analysis - Project Report.pdf'),
        'Smart Healthcare Risk & Disease Analysis',
        'Comprehensive College Capstone Project Report | Data Analytics with Tableau & Python',
        [
            ('1. Abstract & Executive Summary', [
                'This comprehensive project presents an end-to-end data analytics and visual clinical informatics ecosystem analyzing 5,000 patient records across 16 biometric and lifestyle attributes.',
                'A critical forensic audit revealed that the raw dataset field health_risk_score was degenerate (constant 100.0 across all rows). We resolved this by engineering a validated Calibrated Health Risk Score (0-100) adhering to American Heart Association and American Diabetes Association clinical guidelines.',
                'The project delivers 8 publication-grade charts, an 8-worksheet Tableau workbook (project.twbx) with 2 dashboards and a 4-scene story, a responsive Flask web portal with real-time risk simulator, and 11 passed unit tests.'
            ]),
            ('2. Cohort Demographics & Biomarker Statistics', [
                [
                    ['Metric Name', 'Observed Value', 'Clinical Interpretation / Benchmark'],
                    ['Total Cohort Size', '5,000 Patients', 'Sufficient sample size for robust statistical inference'],
                    ['Gender Distribution', '50.12% F / 49.88% M', 'Perfect balance across male and female populations'],
                    ['Age Range', '18 to 79 Years (Mean 48.8)', 'Covers young adults, working age, and senior populations'],
                    ['Mean Systolic Blood Pressure', '134.4 mmHg (Std 26.2)', 'Over 40% of cohort exhibits Stage 1 or Stage 2 Hypertension'],
                    ['Mean Fasting Glucose', '134.5 mg/dL (Std 37.4)', 'Significant prediabetic and diabetic cohort representation'],
                    ['Mean Total Cholesterol', '224.6 mg/dL (Std 43.1)', 'Mean lies above desirable threshold (< 200 mg/dL)'],
                    ['Heart Disease Prevalence', '1,499 Cases (29.98%)', 'Primary cardiovascular outcome endpoint'],
                    ['Diabetes Mellitus Prevalence', '1,746 Cases (34.92%)', 'Primary metabolic outcome endpoint'],
                    ['Stroke Event Prevalence', '1,243 Cases (24.86%)', 'Primary cerebrovascular outcome endpoint'],
                    ['Triad Multi-Morbidity Rate', '1,207 Patients (24.14%)', 'Patients concurrently diagnosed with HD + Diabetes + Stroke']
                ]
            ]),
            ('3. Forensic Audit of health_risk_score Anomaly', [
                'Automated statistical testing confirmed that raw health_risk_score has a standard deviation of exactly 0.0000, min 100.0, max 100.0, and 1 unique value.',
                'Our engineered Calibrated Health Risk Score restores continuous variance (range: 3.2 to 94.4, mean: 44.55, std: 20.82) and allows legitimate clinical stratification into Low (43.5%), Moderate (26.2%), High (17.3%), and Critical (13.0%) risk tiers.'
            ]),
            ('4. Tableau Business Intelligence Architecture', [
                'We created smart_healthcare_analysis.twb and packaged project.twbx featuring:',
                '• 8 Worksheets: KPI Summary, Disease by Age, Risk Tiers, BP vs Glucose, Lifestyle Matrix, Comorbidity Burden, Symptoms, and BMI vs Cholesterol.',
                '• 2 Dashboards: Clinical Risk & Biomarker Dashboard, Population Health & Lifestyle Matrix.',
                '• 1 Analytical Story: 4-scene narrative arc from anomaly audit to targeted care intervention.'
            ]),
            ('5. Software Architecture & Web Implementation', [
                'A modern Flask web application (app.py) serves executive metrics, exploratory analysis galleries, local Tableau mirrors, and an interactive real-time Clinical Risk Assessment Calculator.',
                'The frontend is fully responsive across desktop, tablet, and mobile devices using Bootstrap 5, FontAwesome, and Chart.js.'
            ]),
            ('6. Quality Assurance & Testing Suite', [
                'An automated pytest suite (tests/) validates raw and cleaned data schemas, constant score detection, Flask REST routes, API endpoints, and Tableau workbook XML structure with 11/11 tests passing.'
            ])
        ]
    )

if __name__ == '__main__':
    main()
