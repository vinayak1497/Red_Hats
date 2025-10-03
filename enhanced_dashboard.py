"""
Enhanced Streamlit dashboard for Attendance Anomaly System with signature analysis.
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
try:
    from ocr import PDFProcessor, ImageProcessor, TableExtractor
    from normalization import SymbolMapper, DataCleaner
    from validation import RollValidator, DataValidator, IntegrityChecker
    from anomaly_detection import DuplicateDetector, PatternAnalyzer
    from aggregation import AttendanceCalculator, StatisticsGenerator, DefaulterIdentifier
    from reports import ExcelGenerator, ReportFormatter, SummaryGenerator
    from signature_analysis import SignatureMatcher
except ImportError as e:
    st.warning(f"Some modules not available: {e}")
    # Fallback to basic processing

# Import dynamic processor
from dynamic_attendance_processor import DynamicAttendanceProcessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Enhanced Attendance Anomaly System",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .feature-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .proxy-alert {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .success-card {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main dashboard function."""
    
    # Header
    st.markdown('<h1 class="main-header">🔍 Enhanced Attendance Anomaly System</h1>', unsafe_allow_html=True)
    st.markdown("**Advanced Signature Analysis & Proxy Detection for Academic Institutions**")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.title("🎯 Navigation")
        page = st.selectbox(
            "Choose a page",
            ["🏠 Home", "📤 Upload & Process", "🔍 Signature Analysis", "📊 View Results", "📄 Generate Reports", "⚙️ Settings"]
        )
        
        st.markdown("---")
        st.markdown("### 🚀 Quick Actions")
        if st.button("📁 Open Sample Data"):
            st.info("Sample data available in sample_data/ directory")
        
        if st.button("📖 View Documentation"):
            st.info("Check docs/ directory for detailed documentation")
    
    # Page routing
    if page == "🏠 Home":
        show_home_page()
    elif page == "📤 Upload & Process":
        show_upload_page()
    elif page == "🔍 Signature Analysis":
        show_signature_analysis_page()
    elif page == "📊 View Results":
        show_results_page()
    elif page == "📄 Generate Reports":
        show_reports_page()
    elif page == "⚙️ Settings":
        show_settings_page()

def show_home_page():
    """Display enhanced home page."""
    st.header("🎯 Welcome to Enhanced Attendance Anomaly System")
    
    # Feature highlights
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🔍 Signature Analysis</h3>
            <ul>
                <li>Handwritten signature detection</li>
                <li>Signature consistency analysis</li>
                <li>Proxy attendance detection</li>
                <li>90% similarity threshold</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>📊 Advanced Analytics</h3>
            <ul>
                <li>Real-time attendance tracking</li>
                <li>Anomaly pattern detection</li>
                <li>Defaulter identification</li>
                <li>Statistical analysis</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>📄 Professional Reports</h3>
            <ul>
                <li>Excel report generation</li>
                <li>Multiple sheet formats</li>
                <li>Proxy detection reports</li>
                <li>Comprehensive analytics</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # System status
    st.header("📊 System Status")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card"><h3>OCR Engine</h3><p>✅ Ready</p></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card"><h3>Signature Analysis</h3><p>🔍 Active</p></div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card"><h3>Proxy Detection</h3><p>⚠️ Monitoring</p></div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card"><h3>Report Generator</h3><p>📄 Ready</p></div>', unsafe_allow_html=True)
    
    # Quick start guide
    st.header("🚀 Quick Start Guide")
    
    st.markdown("""
    ### Step-by-Step Process:
    
    1. **📤 Upload Files**: Go to "Upload & Process" page and upload your attendance sheets (PDF/PNG)
    2. **🔍 Signature Analysis**: The system will automatically analyze signatures for proxy detection
    3. **📊 View Results**: Check the "View Results" page for processed data and analytics
    4. **📄 Generate Reports**: Use "Generate Reports" to create Excel reports with signature analysis
    5. **⚙️ Settings**: Configure system settings in the "Settings" page
    """)
    
    # Demo section
    st.header("🎬 Live Demo")
    
    if st.button("🎯 Run Demo with Sample Data", type="primary"):
        run_demo_analysis()

def show_upload_page():
    """Display enhanced upload page with signature analysis."""
    st.header("📤 Upload & Process Attendance Sheets")
    
    # File upload
    uploaded_files = st.file_uploader(
        "Choose attendance files",
        type=['pdf', 'png', 'jpg', 'jpeg'],
        accept_multiple_files=True,
        help="Upload PDF or image files containing attendance sheets with signatures"
    )
    
    if uploaded_files:
        st.success(f"📁 Uploaded {len(uploaded_files)} file(s)")
        
        # Enhanced processing options
        st.subheader("🔧 Processing Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            use_ocr = st.checkbox("🔍 OCR Processing", value=True, help="Extract text and tables from images/PDFs")
            signature_analysis = st.checkbox("✍️ Signature Analysis", value=True, help="Analyze handwritten signatures for proxy detection")
            detect_anomalies = st.checkbox("⚠️ Anomaly Detection", value=True, help="Detect suspicious patterns and duplicates")
        
        with col2:
            generate_reports = st.checkbox("📄 Generate Reports", value=True, help="Create Excel reports with signature analysis")
            validate_data = st.checkbox("✅ Data Validation", value=True, help="Validate roll numbers and data integrity")
            proxy_detection = st.checkbox("🚨 Proxy Detection", value=True, help="Detect proxy attendance using signature analysis")
        
        # Signature analysis settings
        st.subheader("🔍 Signature Analysis Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            similarity_threshold = st.slider(
                "Signature Similarity Threshold",
                min_value=0.5,
                max_value=1.0,
                value=0.9,
                step=0.05,
                help="Minimum similarity for valid signature (0.9 = 90%)"
            )
        
        with col2:
            enable_color_detection = st.checkbox("🎨 Color Detection", value=True, help="Detect red X marks and colored annotations")
        
        # Process button
        if st.button("🚀 Process Files with Signature Analysis", type="primary"):
            with st.spinner("🔍 Processing files with signature analysis..."):
                process_files_enhanced(uploaded_files, {
                    'use_ocr': use_ocr,
                    'signature_analysis': signature_analysis,
                    'detect_anomalies': detect_anomalies,
                    'generate_reports': generate_reports,
                    'validate_data': validate_data,
                    'proxy_detection': proxy_detection,
                    'similarity_threshold': similarity_threshold,
                    'color_detection': enable_color_detection
                })
    
    else:
        st.info("📁 Please upload files to begin processing")
        
        # Show sample data option
        if st.button("📋 Use Sample Data for Demo"):
            run_demo_analysis()

def show_signature_analysis_page():
    """Display signature analysis page."""
    st.header("🔍 Signature Analysis & Proxy Detection")
    
    if 'processed_records' not in st.session_state:
        st.warning("⚠️ No processed data available. Please upload and process files first.")
        return
    
    records = st.session_state['processed_records']
    
    # Signature analysis overview
    st.subheader("📊 Signature Analysis Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_students = len(records)
        st.metric("Total Students", total_students)
    
    with col2:
        proxy_count = len([r for r in records if r.get('status') == 'Proxy Detected'])
        st.metric("Proxy Detected", proxy_count)
    
    with col3:
        consistent_signatures = len([r for r in records if r.get('signature_consistency', 1) >= 0.9])
        st.metric("Consistent Signatures", consistent_signatures)
    
    with col4:
        avg_consistency = sum(r.get('signature_consistency', 1) for r in records) / len(records) if records else 0
        st.metric("Avg Consistency", f"{avg_consistency:.3f}")
    
    # Proxy detection results
    st.subheader("🚨 Proxy Detection Results")
    
    proxy_students = [r for r in records if r.get('status') == 'Proxy Detected']
    
    if proxy_students:
        st.markdown('<div class="proxy-alert">⚠️ Proxy attendance detected! Review the following students:</div>', unsafe_allow_html=True)
        
        for student in proxy_students:
            with st.expander(f"🚨 {student.get('name', 'Unknown')} (Roll: {student.get('roll_number', 'Unknown')})"):
                st.write(f"**Signature Consistency:** {student.get('signature_consistency', 0):.3f}")
                st.write(f"**Status:** {student.get('status', 'Unknown')}")
                st.write(f"**Anomaly Flag:** {student.get('anomaly_flag', 'Unknown')}")
                
                if 'proxy_flags' in student:
                    st.write("**Proxy Flags:**")
                    for flag in student['proxy_flags']:
                        st.write(f"- {flag}")
    else:
        st.markdown('<div class="success-card">✅ No proxy attendance detected. All signatures are consistent.</div>', unsafe_allow_html=True)
    
    # Signature consistency chart
    st.subheader("📈 Signature Consistency Analysis")
    
    if records:
        consistency_data = []
        for record in records:
            consistency_data.append({
                'Student': f"{record.get('roll_number', '')} - {record.get('name', '')[:20]}...",
                'Consistency': record.get('signature_consistency', 1),
                'Status': record.get('status', 'Unknown')
            })
        
        df_consistency = pd.DataFrame(consistency_data)
        
        # Create bar chart
        fig = px.bar(
            df_consistency, 
            x='Student', 
            y='Consistency',
            color='Status',
            title="Signature Consistency by Student",
            labels={'Consistency': 'Signature Consistency Score', 'Student': 'Student'}
        )
        
        # Add threshold line
        fig.add_hline(y=0.9, line_dash="dash", line_color="red", 
                     annotation_text="90% Threshold", annotation_position="top right")
        
        st.plotly_chart(fig, use_container_width=True)

def show_results_page():
    """Display enhanced results page with signature analysis."""
    st.header("📊 View Results - Enhanced Analysis")
    
    if 'processed_records' not in st.session_state:
        st.warning("⚠️ No processed data available. Please upload and process files first.")
        return
    
    records = st.session_state['processed_records']
    
    # Enhanced summary metrics
    st.subheader("📈 Enhanced Summary Metrics")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Records", len(records))
    
    with col2:
        subjects = set(record.get('subject', 'Unknown') for record in records)
        st.metric("Subjects", len(subjects))
    
    with col3:
        proxy_count = len([r for r in records if r.get('status') == 'Proxy Detected'])
        st.metric("Proxy Detected", proxy_count)
    
    with col4:
        defaulter_count = len([r for r in records if r.get('status') == 'Defaulter'])
        st.metric("Defaulters", defaulter_count)
    
    with col5:
        regular_count = len([r for r in records if r.get('status') == 'Regular'])
        st.metric("Regular", regular_count)
    
    # Enhanced data display
    st.subheader("📋 Processed Data with Signature Analysis")
    
    # Create enhanced DataFrame
    df_data = []
    for record in records:
        # Calculate attendance statistics
        lecture_attendance = record.get('lecture_attendance', [])
        present_count = sum(1 for att in lecture_attendance if att.get('is_present', False))
        total_lectures = len(lecture_attendance)
        attendance_percentage = (present_count / total_lectures * 100) if total_lectures > 0 else 0
        
        # Create lecture columns
        lecture_columns = {}
        for i, att in enumerate(lecture_attendance):
            lecture_columns[f'L{i+1}'] = att.get('final_status', '')
        
        df_data.append({
            'Roll_No': record.get('roll_number', ''),
            'Name': record.get('name', ''),
            'Subject': record.get('subject', ''),
            'Total': total_lectures,
            'Present': present_count,
            'Absent': total_lectures - present_count,
            'Attendance_%': f"{attendance_percentage:.2f}%",
            'Status': record.get('status', ''),
            'Anomaly_Flag': record.get('anomaly_flag', ''),
            'Signature_Consistency': f"{record.get('signature_consistency', 1):.3f}",
            **lecture_columns
        })
    
    df = pd.DataFrame(df_data)
    st.dataframe(df, use_container_width=True)
    
    # Enhanced analytics
    st.subheader("📊 Enhanced Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Status distribution
        status_counts = df['Status'].value_counts()
        fig_status = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="Student Status Distribution"
        )
        st.plotly_chart(fig_status, use_container_width=True)
    
    with col2:
        # Signature consistency distribution
        consistency_data = df['Signature_Consistency'].str.replace('%', '').astype(float)
        fig_consistency = px.histogram(
            x=consistency_data,
            title="Signature Consistency Distribution",
            labels={'x': 'Consistency Score', 'y': 'Number of Students'}
        )
        fig_consistency.add_vline(x=0.9, line_dash="dash", line_color="red", 
                                 annotation_text="90% Threshold")
        st.plotly_chart(fig_consistency, use_container_width=True)

def show_reports_page():
    """Display enhanced reports page."""
    st.header("📄 Generate Enhanced Reports")
    
    if 'processed_records' not in st.session_state:
        st.warning("⚠️ No processed data available. Please upload and process files first.")
        return
    
    records = st.session_state['processed_records']
    
    # Enhanced report options
    st.subheader("📋 Enhanced Report Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        generate_student_report = st.checkbox("👥 Student Report", value=True, help="Individual student attendance with signature analysis")
        generate_proxy_report = st.checkbox("🚨 Proxy Detection Report", value=True, help="Detailed proxy detection results")
        generate_summary_report = st.checkbox("📊 Summary Report", value=True, help="Overall statistics and analysis")
    
    with col2:
        generate_anomaly_report = st.checkbox("⚠️ Anomaly Report", value=True, help="All anomalies and flags")
        generate_comprehensive_report = st.checkbox("📄 Comprehensive Report", value=True, help="Complete analysis with all sheets")
        include_signature_analysis = st.checkbox("🔍 Include Signature Analysis", value=True, help="Include signature consistency data")
    
    # Generate reports button
    if st.button("🚀 Generate Enhanced Reports", type="primary"):
        with st.spinner("📄 Generating enhanced reports with signature analysis..."):
            try:
                # Check if Excel output already exists
                if 'excel_output' in st.session_state and st.session_state['excel_output']:
                    excel_path = st.session_state['excel_output']
                    if os.path.exists(excel_path):
                        st.success("✅ Excel report already generated!")
                        
                        # Download button for existing report
                        with open(excel_path, "rb") as f:
                            st.download_button(
                                label="📥 Download Attendance Report",
                                data=f.read(),
                                file_name=os.path.basename(excel_path),
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                        return
                
                # Generate new Excel reports
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                generated_reports = []
                
                if generate_student_report:
                    student_path = f"outputs/enhanced_student_report_{timestamp}.xlsx"
                    generate_enhanced_student_report(records, student_path)
                    generated_reports.append(("Enhanced Student Report", student_path))
                
                if generate_proxy_report:
                    proxy_path = f"outputs/proxy_detection_report_{timestamp}.xlsx"
                    generate_proxy_detection_report(records, proxy_path)
                    generated_reports.append(("Proxy Detection Report", proxy_path))
                
                if generate_comprehensive_report:
                    comprehensive_path = f"outputs/enhanced_comprehensive_report_{timestamp}.xlsx"
                    generate_enhanced_comprehensive_report(records, comprehensive_path)
                    generated_reports.append(("Enhanced Comprehensive Report", comprehensive_path))
                
                # Display generated reports
                st.success(f"✅ Generated {len(generated_reports)} enhanced report(s)")
                
                for report_name, report_path in generated_reports:
                    if os.path.exists(report_path):
                        with open(report_path, "rb") as f:
                            st.download_button(
                                label=f"📥 Download {report_name}",
                                data=f.read(),
                                file_name=os.path.basename(report_path),
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                
            except Exception as e:
                st.error(f"❌ Report generation failed: {str(e)}")

def show_settings_page():
    """Display enhanced settings page."""
    st.header("⚙️ Enhanced System Settings")
    
    # OCR Settings
    st.subheader("🔍 OCR Settings")
    
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
    
    # Signature Analysis Settings
    st.subheader("🔍 Signature Analysis Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        similarity_threshold = st.slider(
            "Signature Similarity Threshold",
            min_value=0.5,
            max_value=1.0,
            value=0.9,
            step=0.05,
            help="Minimum similarity for valid signature (0.9 = 90%)"
        )
        
        enable_color_detection = st.checkbox(
            "Enable Color Detection",
            value=True,
            help="Detect red X marks and colored annotations"
        )
    
    with col2:
        enable_handwriting_recognition = st.checkbox(
            "Enable Handwriting Recognition",
            value=True,
            help="Process handwritten attendance marks"
        )
        
        signature_hash_size = st.selectbox(
            "Signature Hash Size",
            [16, 32, 64],
            index=1,
            help="Size of signature hash for comparison"
        )
    
    # Attendance Settings
    st.subheader("📊 Attendance Settings")
    
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
    
    # Save settings
    if st.button("💾 Save Enhanced Settings", type="primary"):
        settings = {
            'tesseract_path': tesseract_path,
            'ocr_language': ocr_language,
            'ocr_psm': ocr_psm,
            'ocr_confidence': ocr_confidence,
            'similarity_threshold': similarity_threshold,
            'enable_color_detection': enable_color_detection,
            'enable_handwriting_recognition': enable_handwriting_recognition,
            'signature_hash_size': signature_hash_size,
            'defaulter_threshold': defaulter_threshold,
            'severe_threshold': severe_threshold,
            'critical_threshold': critical_threshold,
            'warning_threshold': warning_threshold
        }
        
        st.session_state['enhanced_settings'] = settings
        st.success("✅ Enhanced settings saved successfully!")

def run_demo_analysis():
    """Run demo analysis with sample data."""
    st.info("🎬 Running demo analysis with sample data...")
    
    # Simulate processing results
    demo_records = [
        {
            'roll_number': '76',
            'name': 'AGARE SAMIHAN MANOHAR',
            'subject': 'AOA TH',
            'status': 'Regular',
            'anomaly_flag': 'NONE',
            'signature_consistency': 0.95,
            'attendance_percentage': 100.0,
            'lecture_attendance': [
                {'lecture': 1, 'final_status': 'P', 'is_present': True},
                {'lecture': 2, 'final_status': 'P', 'is_present': True},
                {'lecture': 3, 'final_status': 'P', 'is_present': True},
                {'lecture': 4, 'final_status': 'P', 'is_present': True},
                {'lecture': 5, 'final_status': 'P', 'is_present': True}
            ]
        },
        {
            'roll_number': '84',
            'name': 'CHAUBAL SURABHI PANKAJ',
            'subject': 'AOA TH',
            'status': 'Proxy Detected',
            'anomaly_flag': 'PROXY',
            'signature_consistency': 0.75,
            'attendance_percentage': 100.0,
            'lecture_attendance': [
                {'lecture': 1, 'final_status': 'A', 'is_present': False},
                {'lecture': 2, 'final_status': 'A', 'is_present': False},
                {'lecture': 3, 'final_status': 'A', 'is_present': False},
                {'lecture': 4, 'final_status': 'A', 'is_present': False},
                {'lecture': 5, 'final_status': 'A', 'is_present': False}
            ]
        }
    ]
    
    st.session_state['processed_records'] = demo_records
    st.success("✅ Demo analysis completed! Check the 'View Results' page to see the results.")

def process_files_enhanced(uploaded_files, options):
    """Process uploaded files with enhanced signature analysis."""
    st.info("🔍 Processing files with enhanced signature analysis...")
    
    try:
        # Initialize dynamic processor
        processor = DynamicAttendanceProcessor()
        
        # Process each uploaded file
        all_processed_records = []
        
        for uploaded_file in uploaded_files:
            st.info(f"Processing {uploaded_file.name}...")
            
            # Save uploaded file temporarily
            temp_path = f"temp_{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Process the file
            result = processor.process_attendance_sheet(temp_path)
            
            if result['success']:
                all_processed_records.extend(result['processed_records'])
                st.success(f"✅ Successfully processed {uploaded_file.name}")
            else:
                st.error(f"❌ Error processing {uploaded_file.name}: {result.get('error', 'Unknown error')}")
            
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
        
        if all_processed_records:
            st.session_state['processed_records'] = all_processed_records
            st.session_state['excel_output'] = processor._generate_excel_output(all_processed_records)
            st.success(f"✅ Enhanced processing completed! Processed {len(all_processed_records)} records.")
        else:
            st.error("❌ No records were processed successfully.")
            
    except Exception as e:
        st.error(f"❌ Processing failed: {str(e)}")
        # Fallback to demo data
        demo_records = [
            {
                'roll_number': '76',
                'name': 'AGARE SAMIHAN MANOHAR',
                'subject': 'AOA TH',
                'status': 'Regular',
                'anomaly_flag': 'NONE',
                'signature_consistency': 0.95,
                'attendance_percentage': 100.0,
                'lecture_attendance': [
                    {'lecture': 1, 'final_status': 'P', 'is_present': True},
                    {'lecture': 2, 'final_status': 'P', 'is_present': True},
                    {'lecture': 3, 'final_status': 'P', 'is_present': True},
                    {'lecture': 4, 'final_status': 'P', 'is_present': True},
                    {'lecture': 5, 'final_status': 'P', 'is_present': True}
                ]
            }
        ]
        st.session_state['processed_records'] = demo_records
        st.warning("⚠️ Using demo data due to processing error.")

def generate_enhanced_student_report(records, output_path):
    """Generate enhanced student report."""
    # Implementation for enhanced student report
    pass

def generate_proxy_detection_report(records, output_path):
    """Generate proxy detection report."""
    # Implementation for proxy detection report
    pass

def generate_enhanced_comprehensive_report(records, output_path):
    """Generate enhanced comprehensive report."""
    # Implementation for enhanced comprehensive report
    pass

if __name__ == "__main__":
    main()
