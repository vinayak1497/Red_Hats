# 🚀 Quick Start Guide - Attendance Anomaly System

## Prerequisites Installation

### 1. Install Python 3.8+
- Download from [python.org](https://www.python.org/downloads/)
- **IMPORTANT**: Check "Add Python to PATH" during installation
- Verify: Open Command Prompt and type `python --version`

### 2. Install Tesseract OCR
- Download from [GitHub Tesseract for Windows](https://github.com/UB-Mannheim/tesseract/wiki)
- Install the executable
- Add to PATH: `C:\Program Files\Tesseract-OCR`

### 3. Install Dependencies
```bash
# In your project directory
pip install -r requirements.txt
```

## 🧪 Test Your Setup

```bash
# Run the test script
python test_setup.py
```

## 🎯 How to Run

### Option 1: Web Dashboard (Recommended)
```bash
streamlit run dashboard.py
```
Then open: http://localhost:8501

### Option 2: Command Line
```bash
# Process sample data
python main.py --input sample_data/sample_attendance.csv --output outputs/

# Process your own files
python main.py --input your_attendance.pdf --output outputs/
```

## 📊 Expected Outputs

After running, you'll find these Excel reports in the `outputs/` directory:
- `student_report_YYYYMMDD_HHMMSS.xlsx` - Student-wise attendance
- `subject_report_YYYYMMDD_HHMMSS.xlsx` - Subject-wise analysis  
- `defaulter_report_YYYYMMDD_HHMMSS.xlsx` - Defaulter list
- `comprehensive_report_YYYYMMDD_HHMMSS.xlsx` - Complete analysis

## 🔧 Troubleshooting

### If Python is not found:
- Reinstall Python with "Add to PATH" checked
- Restart Command Prompt
- Try `python3` instead of `python`

### If pip is not found:
- Try `python -m pip install -r requirements.txt`
- Or `python3 -m pip install -r requirements.txt`

### If Tesseract is not found:
- Add Tesseract to your system PATH
- Or specify path in dashboard settings

## 📁 Project Structure
```
Attendance/
├── main.py              # Main application
├── dashboard.py         # Web interface
├── test_setup.py        # Setup test script
├── requirements.txt     # Dependencies
├── sample_data/         # Test data
├── outputs/            # Generated reports
└── src/                # Source code modules
```

## 🎉 You're Ready!

Once setup is complete, you can:
1. Upload PDF/image attendance sheets
2. Process and analyze data
3. Detect anomalies and duplicates
4. Generate comprehensive Excel reports
5. View analytics and statistics

Happy coding! 🚀
