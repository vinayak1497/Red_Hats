"""
Streamlit dashboard for Attendance Anomaly System.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
import os
import sys
from datetime import datetime
import logging

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import modules
from ocr import PDFProcessor, ImageProcessor, TableExtractor
from normalization import SymbolMapper, DataCleaner
from validation import RollValidator, DataValidator, IntegrityChecker
from anomaly_detection import DuplicateDetector, PatternAnalyzer, SignatureAnalyzer
from aggregation import AttendanceCalculator, StatisticsGenerator, DefaulterIdentifier
from reports import ExcelGenerator, ReportFormatter, SummaryGenerator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Attendance Anomaly System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .anomaly-card {
        background-color: #fff2cc;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ff6b6b;
    }
    .success-card {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main dashboard function."""
    
    # Header
    st.markdown('<h1 class="main-header">📊 Attendance Anomaly System</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.title("Navigation")
        page = st.selectbox(
            "Choose a page",
            ["Home", "Upload & Process", "View Results", "Generate Reports", "Settings"]
        )
    
    # Page routing
    if page == "Home":
        show_home_page()
    elif page == "Upload & Process":
        show_upload_page()
    elif page == "View Results":
        show_results_page()
    elif page == "Generate Reports":
        show_reports_page()
    elif page == "Settings":
        show_settings_page()

def show_home_page():
    """Display home page."""
    st.header("Welcome to Attendance Anomaly System")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>📈 Features</h3>
            <ul>
                <li>OCR Processing</li>
                <li>Anomaly Detection</li>
                <li>Report Generation</li>
                <li>Data Validation</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>🔍 Capabilities</h3>
            <ul>
                <li>Duplicate Detection</li>
                <li>Pattern Analysis</li>
                <li>Defaulter Identification</li>
                <li>Excel Reports</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>📊 Analytics</h3>
            <ul>
                <li>Attendance Statistics</li>
                <li>Subject Analysis</li>
                <li>Trend Analysis</li>
                <li>Anomaly Reports</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick start guide
    st.header("Quick Start Guide")
    
    st.markdown("""
    1. **Upload Files**: Go to "Upload & Process" page and upload your attendance sheets (PDF/Image)
    2. **Process Data**: The system will automatically extract and process the data
    3. **View Results**: Check the "View Results" page for processed data and analytics
    4. **Generate Reports**: Use "Generate Reports" to create Excel reports
    5. **Settings**: Configure system settings in the "Settings" page
    """)
    
    # System status
    st.header("System Status")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("OCR Engine", "Ready", "✅")
    
    with col2:
        st.metric("Anomaly Detection", "Active", "✅")
    
    with col3:
        st.metric("Report Generator", "Ready", "✅")
    
    with col4:
        st.metric("Data Validator", "Active", "✅")

def show_upload_page():
    """Display upload and processing page."""
    st.header("Upload & Process Attendance Sheets")
    
    # File upload
    uploaded_files = st.file_uploader(
        "Choose attendance files",
        type=['pdf', 'png', 'jpg', 'jpeg'],
        accept_multiple_files=True,
        help="Upload PDF or image files containing attendance sheets"
    )
    
    if uploaded_files:
        st.success(f"Uploaded {len(uploaded_files)} file(s)")
        
        # Processing options
        st.subheader("Processing Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            use_ocr = st.checkbox("Use OCR Processing", value=True)
            detect_anomalies = st.checkbox("Detect Anomalies", value=True)
        
        with col2:
            generate_reports = st.checkbox("Generate Reports", value=True)
            validate_data = st.checkbox("Validate Data", value=True)
        
        # Process button
        if st.button("Process Files", type="primary"):
            with st.spinner("Processing files..."):
                process_files(uploaded_files, {
                    'use_ocr': use_ocr,
                    'detect_anomalies': detect_anomalies,
                    'generate_reports': generate_reports,
                    'validate_data': validate_data
                })
    
    else:
        st.info("Please upload files to begin processing")

def process_files(uploaded_files, options):
    """Process uploaded files."""
    try:
        # Initialize processors
        pdf_processor = PDFProcessor()
        image_processor = ImageProcessor()
        table_extractor = TableExtractor()
        
        all_records = []
        processing_results = []
        
        for uploaded_file in uploaded_files:
            st.write(f"Processing {uploaded_file.name}...")
            
            # Save uploaded file temporarily
            with open(f"temp_{uploaded_file.name}", "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Process based on file type
            if uploaded_file.name.lower().endswith('.pdf'):
                result = pdf_processor.process_pdf(f"temp_{uploaded_file.name}")
            else:
                result = image_processor.process_image(f"temp_{uploaded_file.name}")
            
            if result['success']:
                # Extract tables
                tables = result['tables']
                records = table_extractor.process_tables(tables)
                all_records.extend(records)
                
                processing_results.append({
                    'file': uploaded_file.name,
                    'status': 'Success',
                    'records': len(records)
                })
            else:
                processing_results.append({
                    'file': uploaded_file.name,
                    'status': 'Failed',
                    'error': result.get('error', 'Unknown error')
                })
            
            # Clean up temp file
            os.remove(f"temp_{uploaded_file.name}")
        
        # Store results in session state
        st.session_state['processed_records'] = all_records
        st.session_state['processing_results'] = processing_results
        
        # Display results
        st.success(f"Processing completed! Found {len(all_records)} records")
        
        # Show processing summary
        df_results = pd.DataFrame(processing_results)
        st.dataframe(df_results)
        
        # Process data if options are enabled
        if options['validate_data'] and all_records:
            with st.spinner("Validating data..."):
                validate_attendance_data(all_records)
        
        if options['detect_anomalies'] and all_records:
            with st.spinner("Detecting anomalies..."):
                detect_attendance_anomalies(all_records)
        
        if options['generate_reports'] and all_records:
            with st.spinner("Generating reports..."):
                generate_attendance_reports(all_records)
        
    except Exception as e:
        st.error(f"Processing failed: {str(e)}")
        logger.error(f"Processing error: {e}")

def validate_attendance_data(records):
    """Validate attendance data."""
    try:
        # Initialize validators
        roll_validator = RollValidator()
        data_validator = DataValidator()
        integrity_checker = IntegrityChecker()
        
        # Perform validation
        roll_validation = roll_validator.validate_all(records)
        data_validation = data_validator.validate_all(records)
        integrity_check = integrity_checker.check_all_integrity(records)
        
        # Store validation results
        st.session_state['validation_results'] = {
            'roll_validation': roll_validation,
            'data_validation': data_validation,
            'integrity_check': integrity_check
        }
        
        st.success("Data validation completed")
        
    except Exception as e:
        st.error(f"Validation failed: {str(e)}")
        logger.error(f"Validation error: {e}")

def detect_attendance_anomalies(records):
    """Detect attendance anomalies."""
    try:
        # Initialize detectors
        duplicate_detector = DuplicateDetector()
        pattern_analyzer = PatternAnalyzer()
        
        # Perform anomaly detection
        duplicate_report = duplicate_detector.detect_all_duplicates(records)
        pattern_report = pattern_analyzer.analyze_all_patterns(records)
        
        # Store anomaly results
        st.session_state['anomaly_results'] = {
            'duplicate_report': duplicate_report,
            'pattern_report': pattern_report
        }
        
        st.success("Anomaly detection completed")
        
    except Exception as e:
        st.error(f"Anomaly detection failed: {str(e)}")
        logger.error(f"Anomaly detection error: {e}")

def generate_attendance_reports(records):
    """Generate attendance reports."""
    try:
        # Initialize generators
        excel_generator = ExcelGenerator()
        summary_generator = SummaryGenerator()
        
        # Generate reports
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Student report
        student_report_path = f"outputs/student_report_{timestamp}.xlsx"
        excel_generator.create_student_report(records, student_report_path)
        
        # Subject report
        subject_report_path = f"outputs/subject_report_{timestamp}.xlsx"
        excel_generator.create_subject_report(records, subject_report_path)
        
        # Defaulter report
        defaulter_report_path = f"outputs/defaulter_report_{timestamp}.xlsx"
        excel_generator.create_defaulter_report(records, defaulter_report_path)
        
        # Store report paths
        st.session_state['report_paths'] = {
            'student_report': student_report_path,
            'subject_report': subject_report_path,
            'defaulter_report': defaulter_report_path
        }
        
        st.success("Reports generated successfully")
        
    except Exception as e:
        st.error(f"Report generation failed: {str(e)}")
        logger.error(f"Report generation error: {e}")

def show_results_page():
    """Display results page."""
    st.header("View Results")
    
    if 'processed_records' not in st.session_state:
        st.warning("No processed data available. Please upload and process files first.")
        return
    
    records = st.session_state['processed_records']
    
    # Display summary metrics
    st.subheader("Summary Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Records", len(records))
    
    with col2:
        subjects = set(record.get('subject', 'Unknown') for record in records)
        st.metric("Subjects", len(subjects))
    
    with col3:
        # Calculate defaulters
        defaulter_count = 0
        for record in records:
            attendance_records = record.get('attendance_records', [])
            present_count = sum(1 for att in attendance_records if att.get('status') == 'P')
            absent_count = sum(1 for att in attendance_records if att.get('status') == 'A')
            total_clear = present_count + absent_count
            
            if total_clear > 0:
                attendance_percentage = (present_count / total_clear) * 100
                if attendance_percentage < 75:
                    defaulter_count += 1
        
        st.metric("Defaulters", defaulter_count)
    
    with col4:
        st.metric("Defaulter %", f"{(defaulter_count/len(records)*100):.1f}%" if records else "0%")
    
    # Display data tables
    st.subheader("Processed Data")
    
    # Create DataFrame
    df_data = []
    for record in records:
        attendance_records = record.get('attendance_records', [])
        
        present_count = sum(1 for att in attendance_records if att.get('status') == 'P')
        absent_count = sum(1 for att in attendance_records if att.get('status') == 'A')
        unclear_count = sum(1 for att in attendance_records if att.get('status') == '?')
        
        total_clear = present_count + absent_count
        attendance_percentage = (present_count / total_clear * 100) if total_clear > 0 else 0
        
        df_data.append({
            'Roll Number': record.get('roll_number', ''),
            'Name': record.get('name', ''),
            'Subject': record.get('subject', ''),
            'Present': present_count,
            'Absent': absent_count,
            'Unclear': unclear_count,
            'Attendance %': f"{attendance_percentage:.2f}%",
            'Status': 'Defaulter' if attendance_percentage < 75 else 'Regular'
        })
    
    df = pd.DataFrame(df_data)
    st.dataframe(df)
    
    # Display charts
    st.subheader("Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Attendance distribution
        attendance_ranges = {
            'Excellent (≥90%)': 0,
            'Good (75-89%)': 0,
            'Poor (50-74%)': 0,
            'Critical (<50%)': 0
        }
        
        for record in records:
            attendance_records = record.get('attendance_records', [])
            present_count = sum(1 for att in attendance_records if att.get('status') == 'P')
            absent_count = sum(1 for att in attendance_records if att.get('status') == 'A')
            total_clear = present_count + absent_count
            
            if total_clear > 0:
                attendance_percentage = (present_count / total_clear) * 100
                
                if attendance_percentage >= 90:
                    attendance_ranges['Excellent (≥90%)'] += 1
                elif attendance_percentage >= 75:
                    attendance_ranges['Good (75-89%)'] += 1
                elif attendance_percentage >= 50:
                    attendance_ranges['Poor (50-74%)'] += 1
                else:
                    attendance_ranges['Critical (<50%)'] += 1
        
        fig = px.pie(
            values=list(attendance_ranges.values()),
            names=list(attendance_ranges.keys()),
            title="Attendance Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Subject-wise analysis
        subject_stats = {}
        for record in records:
            subject = record.get('subject', 'Unknown')
            if subject not in subject_stats:
                subject_stats[subject] = {'total': 0, 'defaulters': 0}
            
            subject_stats[subject]['total'] += 1
            
            attendance_records = record.get('attendance_records', [])
            present_count = sum(1 for att in attendance_records if att.get('status') == 'P')
            absent_count = sum(1 for att in attendance_records if att.get('status') == 'A')
            total_clear = present_count + absent_count
            
            if total_clear > 0:
                attendance_percentage = (present_count / total_clear) * 100
                if attendance_percentage < 75:
                    subject_stats[subject]['defaulters'] += 1
        
        subjects = list(subject_stats.keys())
        defaulter_rates = [subject_stats[s]['defaulters']/subject_stats[s]['total']*100 for s in subjects]
        
        fig = px.bar(
            x=subjects,
            y=defaulter_rates,
            title="Defaulter Rate by Subject",
            labels={'x': 'Subject', 'y': 'Defaulter Rate (%)'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Display validation results if available
    if 'validation_results' in st.session_state:
        st.subheader("Validation Results")
        
        validation_results = st.session_state['validation_results']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            roll_summary = validation_results['roll_validation']['summary']
            st.metric("Valid Rolls", roll_summary['valid_rolls'])
            st.metric("Invalid Rolls", roll_summary['invalid_rolls'])
        
        with col2:
            data_summary = validation_results['data_validation']['summary']
            st.metric("Valid Records", data_summary['valid_records'])
            st.metric("Invalid Records", data_summary['invalid_records'])
        
        with col3:
            integrity_summary = validation_results['integrity_check']['summary']
            st.metric("Duplicate Count", integrity_summary['duplicate_count'])
            st.metric("Anomalous Records", integrity_summary['anomalous_record_count'])
    
    # Display anomaly results if available
    if 'anomaly_results' in st.session_state:
        st.subheader("Anomaly Detection Results")
        
        anomaly_results = st.session_state['anomaly_results']
        
        col1, col2 = st.columns(2)
        
        with col1:
            duplicate_summary = anomaly_results['duplicate_report']['summary']
            st.metric("Duplicate Rolls", duplicate_summary['duplicate_roll_count'])
            st.metric("Duplicate Names", duplicate_summary['duplicate_name_count'])
            st.metric("Duplicate Patterns", duplicate_summary['duplicate_pattern_count'])
        
        with col2:
            pattern_summary = anomaly_results['pattern_report']['summary']
            st.metric("Suspicious Records", pattern_summary['suspicious_record_count'])
            st.metric("Anomalous Records", pattern_summary['anomalous_record_count'])

def show_reports_page():
    """Display reports page."""
    st.header("Generate Reports")
    
    if 'processed_records' not in st.session_state:
        st.warning("No processed data available. Please upload and process files first.")
        return
    
    records = st.session_state['processed_records']
    
    # Report generation options
    st.subheader("Report Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        generate_student_report = st.checkbox("Student-wise Report", value=True)
        generate_subject_report = st.checkbox("Subject-wise Report", value=True)
        generate_defaulter_report = st.checkbox("Defaulter Report", value=True)
    
    with col2:
        generate_anomaly_report = st.checkbox("Anomaly Report", value=True)
        generate_comprehensive_report = st.checkbox("Comprehensive Report", value=True)
        include_charts = st.checkbox("Include Charts", value=True)
    
    # Generate reports button
    if st.button("Generate Reports", type="primary"):
        with st.spinner("Generating reports..."):
            try:
                # Initialize generators
                excel_generator = ExcelGenerator()
                summary_generator = SummaryGenerator()
                
                # Generate timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                generated_reports = []
                
                # Student report
                if generate_student_report:
                    student_path = f"outputs/student_report_{timestamp}.xlsx"
                    excel_generator.create_student_report(records, student_path)
                    generated_reports.append(("Student Report", student_path))
                
                # Subject report
                if generate_subject_report:
                    subject_path = f"outputs/subject_report_{timestamp}.xlsx"
                    excel_generator.create_subject_report(records, subject_path)
                    generated_reports.append(("Subject Report", subject_path))
                
                # Defaulter report
                if generate_defaulter_report:
                    defaulter_path = f"outputs/defaulter_report_{timestamp}.xlsx"
                    excel_generator.create_defaulter_report(records, defaulter_path)
                    generated_reports.append(("Defaulter Report", defaulter_path))
                
                # Anomaly report
                if generate_anomaly_report and 'anomaly_results' in st.session_state:
                    anomaly_path = f"outputs/anomaly_report_{timestamp}.xlsx"
                    excel_generator.create_anomaly_report(
                        records, 
                        st.session_state['anomaly_results'], 
                        anomaly_path
                    )
                    generated_reports.append(("Anomaly Report", anomaly_path))
                
                # Comprehensive report
                if generate_comprehensive_report:
                    comprehensive_path = f"outputs/comprehensive_report_{timestamp}.xlsx"
                    excel_generator.create_comprehensive_report(
                        records,
                        st.session_state.get('anomaly_results', {}),
                        comprehensive_path
                    )
                    generated_reports.append(("Comprehensive Report", comprehensive_path))
                
                # Display generated reports
                st.success(f"Generated {len(generated_reports)} report(s)")
                
                for report_name, report_path in generated_reports:
                    if os.path.exists(report_path):
                        with open(report_path, "rb") as f:
                            st.download_button(
                                label=f"Download {report_name}",
                                data=f.read(),
                                file_name=os.path.basename(report_path),
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                
            except Exception as e:
                st.error(f"Report generation failed: {str(e)}")
                logger.error(f"Report generation error: {e}")
    
    # Display existing reports if available
    if 'report_paths' in st.session_state:
        st.subheader("Previously Generated Reports")
        
        report_paths = st.session_state['report_paths']
        
        for report_name, report_path in report_paths.items():
            if os.path.exists(report_path):
                with open(report_path, "rb") as f:
                    st.download_button(
                        label=f"Download {report_name.replace('_', ' ').title()}",
                        data=f.read(),
                        file_name=os.path.basename(report_path),
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

def show_settings_page():
    """Display settings page."""
    st.header("Settings")
    
    # OCR Settings
    st.subheader("OCR Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        tesseract_path = st.text_input(
            "Tesseract Path",
            value="",
            help="Path to tesseract executable (if not in PATH)"
        )
        
        ocr_language = st.selectbox(
            "OCR Language",
            ["eng", "hin", "eng+hin"],
            index=0
        )
    
    with col2:
        ocr_psm = st.selectbox(
            "Page Segmentation Mode",
            [1, 3, 6, 8, 13],
            index=2,
            help="Tesseract PSM mode"
        )
        
        ocr_confidence = st.slider(
            "OCR Confidence Threshold",
            min_value=0,
            max_value=100,
            value=60
        )
    
    # Attendance Settings
    st.subheader("Attendance Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        defaulter_threshold = st.slider(
            "Defaulter Threshold (%)",
            min_value=0,
            max_value=100,
            value=75
        )
        
        severe_threshold = st.slider(
            "Severe Defaulter Threshold (%)",
            min_value=0,
            max_value=100,
            value=50
        )
    
    with col2:
        critical_threshold = st.slider(
            "Critical Defaulter Threshold (%)",
            min_value=0,
            max_value=100,
            value=25
        )
        
        warning_threshold = st.slider(
            "Warning Threshold (%)",
            min_value=0,
            max_value=100,
            value=80
        )
    
    # Anomaly Detection Settings
    st.subheader("Anomaly Detection Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        duplicate_threshold = st.slider(
            "Duplicate Detection Threshold",
            min_value=0.0,
            max_value=1.0,
            value=0.8,
            step=0.1
        )
        
        suspicious_threshold = st.slider(
            "Suspicious Pattern Threshold",
            min_value=0.0,
            max_value=1.0,
            value=0.9,
            step=0.1
        )
    
    with col2:
        enable_signature_analysis = st.checkbox(
            "Enable Signature Analysis",
            value=False,
            help="Analyze signatures for duplicates (experimental)"
        )
        
        enable_pattern_analysis = st.checkbox(
            "Enable Pattern Analysis",
            value=True,
            help="Analyze attendance patterns for anomalies"
        )
    
    # Save settings
    if st.button("Save Settings", type="primary"):
        settings = {
            'tesseract_path': tesseract_path,
            'ocr_language': ocr_language,
            'ocr_psm': ocr_psm,
            'ocr_confidence': ocr_confidence,
            'defaulter_threshold': defaulter_threshold,
            'severe_threshold': severe_threshold,
            'critical_threshold': critical_threshold,
            'warning_threshold': warning_threshold,
            'duplicate_threshold': duplicate_threshold,
            'suspicious_threshold': suspicious_threshold,
            'enable_signature_analysis': enable_signature_analysis,
            'enable_pattern_analysis': enable_pattern_analysis
        }
        
        st.session_state['settings'] = settings
        st.success("Settings saved successfully!")
    
    # Display current settings
    if 'settings' in st.session_state:
        st.subheader("Current Settings")
        settings = st.session_state['settings']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.json({
                'OCR Settings': {
                    'Tesseract Path': settings.get('tesseract_path', ''),
                    'Language': settings.get('ocr_language', 'eng'),
                    'PSM': settings.get('ocr_psm', 6),
                    'Confidence': settings.get('ocr_confidence', 60)
                }
            })
        
        with col2:
            st.json({
                'Attendance Settings': {
                    'Defaulter Threshold': settings.get('defaulter_threshold', 75),
                    'Severe Threshold': settings.get('severe_threshold', 50),
                    'Critical Threshold': settings.get('critical_threshold', 25),
                    'Warning Threshold': settings.get('warning_threshold', 80)
                }
            })

if __name__ == "__main__":
    main()
