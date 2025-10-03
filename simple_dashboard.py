"""
Simplified Streamlit dashboard for Attendance Anomaly System
Focuses on dynamic processing without complex dependencies.
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime
import logging

# Import dynamic processor
from dynamic_attendance_processor import DynamicAttendanceProcessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Attendance Anomaly System",
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
    st.markdown('<h1 class="main-header">🔍 Attendance Anomaly System</h1>', unsafe_allow_html=True)
    st.markdown("**Dynamic Processing & Excel Generation for Academic Institutions**")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.title("🎯 Navigation")
        page = st.selectbox(
            "Choose a page",
            ["🏠 Home", "📤 Upload & Process", "📊 View Results", "📄 Generate Reports"]
        )
        
        st.markdown("---")
        st.markdown("### 🚀 Quick Actions")
        if st.button("📋 Run Demo"):
            run_demo_analysis()
    
    # Page routing
    if page == "🏠 Home":
        show_home_page()
    elif page == "📤 Upload & Process":
        show_upload_page()
    elif page == "📊 View Results":
        show_results_page()
    elif page == "📄 Generate Reports":
        show_reports_page()

def show_home_page():
    """Display home page."""
    st.header("🎯 Welcome to Attendance Anomaly System")
    
    # Feature highlights
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🔍 Dynamic Processing</h3>
            <ul>
                <li>PDF and image processing</li>
                <li>OCR text extraction</li>
                <li>Table structure detection</li>
                <li>Automatic data parsing</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>📊 Excel Generation</h3>
            <ul>
                <li>Exact format output</li>
                <li>Multiple sheets</li>
                <li>Professional formatting</li>
                <li>Comprehensive reports</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>🔍 Anomaly Detection</h3>
            <ul>
                <li>Proxy detection</li>
                <li>Pattern analysis</li>
                <li>Defaulter identification</li>
                <li>Signature consistency</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # System status
    st.header("📊 System Status")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card"><h3>Dynamic Processor</h3><p>✅ Ready</p></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card"><h3>Excel Generator</h3><p>📄 Active</p></div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card"><h3>Anomaly Detection</h3><p>⚠️ Monitoring</p></div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card"><h3>Report Generator</h3><p>📊 Ready</p></div>', unsafe_allow_html=True)
    
    # Quick start guide
    st.header("🚀 Quick Start Guide")
    
    st.markdown("""
    ### Step-by-Step Process:
    
    1. **📤 Upload Files**: Go to "Upload & Process" page and upload your attendance sheets (PDF/PNG)
    2. **🔍 Dynamic Processing**: The system will automatically extract and process all data
    3. **📊 View Results**: Check the "View Results" page for processed data and analytics
    4. **📄 Generate Reports**: Use "Generate Reports" to create Excel reports with exact format
    """)
    
    # Demo section
    st.header("🎬 Live Demo")
    
    if st.button("🎯 Run Demo with Sample Data", type="primary"):
        run_demo_analysis()

def show_upload_page():
    """Display upload page."""
    st.header("📤 Upload & Process Attendance Sheets")
    
    # File upload
    uploaded_files = st.file_uploader(
        "Choose attendance files",
        type=['pdf', 'png', 'jpg', 'jpeg'],
        accept_multiple_files=True,
        help="Upload PDF or image files containing attendance sheets"
    )
    
    if uploaded_files:
        st.success(f"📁 Uploaded {len(uploaded_files)} file(s)")
        
        # Processing options
        st.subheader("🔧 Processing Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            use_ocr = st.checkbox("🔍 OCR Processing", value=True, help="Extract text and tables from images/PDFs")
            detect_anomalies = st.checkbox("⚠️ Anomaly Detection", value=True, help="Detect suspicious patterns and duplicates")
        
        with col2:
            generate_reports = st.checkbox("📄 Generate Reports", value=True, help="Create Excel reports")
            validate_data = st.checkbox("✅ Data Validation", value=True, help="Validate roll numbers and data integrity")
        
        # Process button
        if st.button("🚀 Process Files", type="primary"):
            with st.spinner("🔍 Processing files..."):
                process_files(uploaded_files, {
                    'use_ocr': use_ocr,
                    'detect_anomalies': detect_anomalies,
                    'generate_reports': generate_reports,
                    'validate_data': validate_data
                })
    
    else:
        st.info("📁 Please upload files to begin processing")
        
        # Show sample data option
        if st.button("📋 Use Sample Data for Demo"):
            run_demo_analysis()

def show_results_page():
    """Display results page."""
    st.header("📊 View Results - Processed Data")
    
    if 'processed_records' not in st.session_state:
        st.warning("⚠️ No processed data available. Please upload and process files first.")
        return
    
    records = st.session_state['processed_records']
    
    # Summary metrics
    st.subheader("📈 Summary Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Records", len(records))
    
    with col2:
        subjects = set(record.get('subject', 'Unknown') for record in records)
        st.metric("Subjects", len(subjects))
    
    with col3:
        defaulter_count = len([r for r in records if r.get('status') == 'DEFAULTER'])
        st.metric("Defaulters", defaulter_count)
    
    with col4:
        regular_count = len([r for r in records if r.get('status') == 'REGULAR'])
        st.metric("Regular", regular_count)
    
    # Data display
    st.subheader("📋 Processed Data")
    
    # Create DataFrame
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
            'Roll No': record.get('roll_number', ''),
            'Name': record.get('name', ''),
            'Student ID': record.get('student_id', ''),
            **lecture_columns,
            'Total': present_count,
            '%': f"{attendance_percentage:.1f}%",
            'Status': record.get('status', ''),
            'Anomaly Flag': record.get('anomaly_flag', '')
        })
    
    df = pd.DataFrame(df_data)
    st.dataframe(df, use_container_width=True)
    
    # Analytics
    st.subheader("📊 Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Status distribution
        status_counts = df['Status'].value_counts()
        st.bar_chart(status_counts)
    
    with col2:
        # Attendance distribution
        attendance_data = df['Total'].value_counts().sort_index()
        st.bar_chart(attendance_data)

def show_reports_page():
    """Display reports page."""
    st.header("📄 Generate Reports")
    
    if 'processed_records' not in st.session_state:
        st.warning("⚠️ No processed data available. Please upload and process files first.")
        return
    
    records = st.session_state['processed_records']
    
    # Report options
    st.subheader("📋 Report Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        generate_student_report = st.checkbox("👥 Student Report", value=True, help="Individual student attendance")
        generate_summary_report = st.checkbox("📊 Summary Report", value=True, help="Overall statistics and analysis")
    
    with col2:
        generate_anomaly_report = st.checkbox("⚠️ Anomaly Report", value=True, help="All anomalies and flags")
        generate_comprehensive_report = st.checkbox("📄 Comprehensive Report", value=True, help="Complete analysis with all sheets")
    
    # Generate reports button
    if st.button("🚀 Generate Reports", type="primary"):
        with st.spinner("📄 Generating reports..."):
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
                processor = DynamicAttendanceProcessor()
                excel_path = processor._generate_excel_output(records)
                
                if excel_path and os.path.exists(excel_path):
                    st.session_state['excel_output'] = excel_path
                    st.success("✅ Excel report generated successfully!")
                    
                    # Download button
                    with open(excel_path, "rb") as f:
                        st.download_button(
                            label="📥 Download Attendance Report",
                            data=f.read(),
                            file_name=os.path.basename(excel_path),
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                else:
                    st.error("❌ Failed to generate Excel report")
                
            except Exception as e:
                st.error(f"❌ Report generation failed: {str(e)}")

def process_files(uploaded_files, options):
    """Process uploaded files."""
    st.info("🔍 Processing files...")
    
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
            st.success(f"✅ Processing completed! Processed {len(all_processed_records)} records.")
        else:
            st.error("❌ No records were processed successfully.")
            
    except Exception as e:
        st.error(f"❌ Processing failed: {str(e)}")
        # Fallback to demo data
        run_demo_analysis()

def run_demo_analysis():
    """Run demo analysis with sample data."""
    st.info("🎬 Running demo analysis with sample data...")
    
    # Create sample data
    demo_records = [
        {
            'roll_number': '76',
            'name': 'AGARE SAMIHAN MANOHAR',
            'student_id': '23102094',
            'subject': 'AOA TH',
            'status': 'REGULAR',
            'anomaly_flag': 'NONE',
            'attendance_percentage': 100.0,
            'lecture_attendance': [
                {'lecture': 1, 'final_status': 'P', 'is_present': True},
                {'lecture': 2, 'final_status': 'P', 'is_present': True},
                {'lecture': 3, 'final_status': 'P', 'is_present': True},
                {'lecture': 4, 'final_status': 'P', 'is_present': True},
                {'lecture': 5, 'final_status': 'P', 'is_present': True},
                {'lecture': 6, 'final_status': 'P', 'is_present': True},
                {'lecture': 7, 'final_status': 'P', 'is_present': True},
                {'lecture': 8, 'final_status': 'P', 'is_present': True},
                {'lecture': 9, 'final_status': 'P', 'is_present': True}
            ]
        },
        {
            'roll_number': '77',
            'name': 'AHIR ANSH MOHAN',
            'student_id': '23102165',
            'subject': 'AOA TH',
            'status': 'DEFAULTER',
            'anomaly_flag': 'DEFAULTER',
            'attendance_percentage': 0.0,
            'lecture_attendance': [
                {'lecture': 1, 'final_status': 'A', 'is_present': False},
                {'lecture': 2, 'final_status': 'A', 'is_present': False},
                {'lecture': 3, 'final_status': 'AB', 'is_present': False},
                {'lecture': 4, 'final_status': 'A', 'is_present': False},
                {'lecture': 5, 'final_status': 'A', 'is_present': False},
                {'lecture': 6, 'final_status': 'A', 'is_present': False},
                {'lecture': 7, 'final_status': 'A', 'is_present': False},
                {'lecture': 8, 'final_status': 'A', 'is_present': False},
                {'lecture': 9, 'final_status': 'A', 'is_present': False}
            ]
        },
        {
            'roll_number': '78',
            'name': 'ANNANDATE VANSH MANISH',
            'student_id': '23102166',
            'subject': 'AOA TH',
            'status': 'REGULAR',
            'anomaly_flag': 'NONE',
            'attendance_percentage': 100.0,
            'lecture_attendance': [
                {'lecture': 1, 'final_status': 'P', 'is_present': True},
                {'lecture': 2, 'final_status': 'P', 'is_present': True},
                {'lecture': 3, 'final_status': 'P', 'is_present': True},
                {'lecture': 4, 'final_status': 'P', 'is_present': True},
                {'lecture': 5, 'final_status': 'P', 'is_present': True},
                {'lecture': 6, 'final_status': 'P', 'is_present': True},
                {'lecture': 7, 'final_status': 'P', 'is_present': True},
                {'lecture': 8, 'final_status': 'P', 'is_present': True},
                {'lecture': 9, 'final_status': 'P', 'is_present': True}
            ]
        }
    ]
    
    st.session_state['processed_records'] = demo_records
    st.success("✅ Demo analysis completed! Check the 'View Results' page to see the results.")

if __name__ == "__main__":
    main()
