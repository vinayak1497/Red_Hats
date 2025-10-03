# User Guide

## Getting Started

### Installation

1. **Install Python 3.8+**
   ```bash
   python --version
   ```

2. **Install Tesseract OCR**
   - **Windows**: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
   - **macOS**: `brew install tesseract`
   - **Linux**: `sudo apt-get install tesseract-ocr`

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Quick Start

1. **Command Line Usage**
   ```bash
   python main.py --input attendance_sheet.pdf --output reports/
   ```

2. **Web Dashboard**
   ```bash
   streamlit run dashboard.py
   ```

## File Formats

### Supported Input Formats

- **PDF**: Structured and scanned PDFs
- **Images**: PNG, JPG, JPEG
- **CSV**: Direct data import (for testing)

### Expected Attendance Sheet Format

The system expects attendance sheets with:
- Roll numbers in the first column
- Student names in the second column
- Subject information
- Date information
- Lecture-wise attendance marks

### Attendance Mark Symbols

| Symbol | Meaning | Normalized |
|--------|---------|------------|
| P, p | Present | P |
| A, a | Absent | A |
| ✔, ✓ | Present | P |
| ×, x | Absent | A |
| ., 1 | Present | P |
| -, 0 | Absent | A |
| ? | Unclear | ? |

## Using the System

### 1. Command Line Interface

#### Basic Usage
```bash
# Process single file
python main.py --input attendance.pdf

# Process multiple files
python main.py --input file1.pdf file2.jpg file3.png

# Specify output directory
python main.py --input attendance.pdf --output reports/

# Verbose output
python main.py --input attendance.pdf --verbose
```

#### Output Files
The system generates several Excel reports:
- `student_report_YYYYMMDD_HHMMSS.xlsx` - Student-wise attendance
- `subject_report_YYYYMMDD_HHMMSS.xlsx` - Subject-wise analysis
- `defaulter_report_YYYYMMDD_HHMMSS.xlsx` - Defaulter list
- `anomaly_report_YYYYMMDD_HHMMSS.xlsx` - Anomaly detection results
- `comprehensive_report_YYYYMMDD_HHMMSS.xlsx` - Complete analysis

### 2. Web Dashboard

#### Starting the Dashboard
```bash
streamlit run dashboard.py
```

#### Dashboard Features

1. **Home Page**
   - System overview
   - Quick start guide
   - System status

2. **Upload & Process**
   - File upload interface
   - Processing options
   - Real-time progress

3. **View Results**
   - Processed data display
   - Analytics charts
   - Validation results
   - Anomaly detection results

4. **Generate Reports**
   - Report generation options
   - Download links
   - Report previews

5. **Settings**
   - OCR configuration
   - Attendance thresholds
   - Anomaly detection settings

#### Using the Dashboard

1. **Upload Files**
   - Go to "Upload & Process" page
   - Select PDF or image files
   - Choose processing options
   - Click "Process Files"

2. **View Results**
   - Check "View Results" page for processed data
   - Review analytics and charts
   - Examine validation results

3. **Generate Reports**
   - Go to "Generate Reports" page
   - Select report types
   - Download generated reports

4. **Configure Settings**
   - Visit "Settings" page
   - Adjust thresholds and options
   - Save configuration

### 3. Programmatic Usage

#### Basic Processing
```python
from main import AttendanceAnomalySystem

# Initialize system
system = AttendanceAnomalySystem(output_dir="outputs")

# Process files
results = system.run_complete_analysis(["attendance.pdf"])

# Check results
if results['success']:
    print(f"Processed {results['processing_results']['total_records']} records")
    print(f"Reports generated in: {results['report_paths']}")
else:
    print(f"Processing failed: {results['error']}")
```

#### Individual Module Usage
```python
from src.ocr import PDFProcessor
from src.normalization import SymbolMapper
from src.validation import RollValidator

# Process PDF
processor = PDFProcessor()
result = processor.process_pdf("attendance.pdf")

# Normalize data
mapper = SymbolMapper()
normalized = mapper.normalize_batch(records)

# Validate data
validator = RollValidator()
validation = validator.validate_all(normalized)
```

## Understanding Results

### 1. Attendance Statistics

#### Student-wise Analysis
- **Total Lectures**: Number of lectures attended
- **Present**: Number of present marks
- **Absent**: Number of absent marks
- **Unclear**: Number of unclear marks
- **Attendance %**: Percentage of attendance
- **Status**: Regular or Defaulter

#### Subject-wise Analysis
- **Total Students**: Number of students in subject
- **Average Attendance**: Overall attendance percentage
- **Defaulter Count**: Number of defaulters
- **Defaulter Rate**: Percentage of defaulters

### 2. Anomaly Detection

#### Duplicate Detection
- **Duplicate Rolls**: Multiple records with same roll number
- **Duplicate Names**: Same name with different roll numbers
- **Duplicate Patterns**: Identical attendance patterns

#### Suspicious Patterns
- **Perfect Attendance**: All present marks (might be suspicious)
- **No Attendance**: All absent marks
- **All Unclear**: All unclear marks
- **Identical Marks**: All marks are the same

#### Attendance Anomalies
- **High Unclear Ratio**: More than 50% unclear marks
- **Sudden Changes**: Sudden changes in attendance pattern
- **Correlation**: High correlation between students

### 3. Validation Results

#### Data Validation

#### Roll Number Validation
- **Valid Rolls**: Roll numbers that pass validation
- **Invalid Rolls**: Roll numbers that fail validation
- **Duplicate Rolls**: Multiple records with same roll number
- **Missing Rolls**: Records without roll numbers

#### Data Integrity
- **Consistent Records**: Records with consistent data
- **Inconsistent Records**: Records with data inconsistencies
- **Missing Data**: Records with missing required fields

## Troubleshooting

### Common Issues

#### 1. OCR Errors
**Problem**: Poor text extraction from images/PDFs
**Solutions**:
- Ensure high-quality input images
- Check Tesseract installation
- Adjust OCR settings in dashboard
- Try different image preprocessing

#### 2. Validation Errors
**Problem**: Many validation errors
**Solutions**:
- Check data format and quality
- Review symbol mappings
- Clean input data
- Adjust validation thresholds

#### 3. Anomaly Detection
**Problem**: Too many anomalies detected
**Solutions**:
- Review detection thresholds
- Check data quality
- Adjust anomaly detection settings
- Manually review flagged records

#### 4. Report Generation
**Problem**: Reports not generated
**Solutions**:
- Check output directory permissions
- Ensure sufficient disk space
- Verify Excel dependencies
- Check file paths

### Performance Optimization

#### 1. Large Files
- Process files in batches
- Use appropriate OCR settings
- Consider file size limits
- Monitor memory usage

#### 2. Multiple Files
- Process files sequentially
- Use parallel processing for large datasets
- Optimize OCR settings
- Cache intermediate results

#### 3. System Resources
- Monitor CPU and memory usage
- Adjust processing parameters
- Use appropriate hardware
- Optimize system settings

## Best Practices

### 1. Data Preparation
- Use high-quality images/PDFs
- Ensure consistent formatting
- Clean data before processing
- Validate input data

### 2. Processing
- Start with small test files
- Verify results before full processing
- Use appropriate settings
- Monitor processing progress

### 3. Results Analysis
- Review validation results
- Check anomaly reports
- Verify attendance calculations
- Validate report accuracy

### 4. System Maintenance
- Regular updates
- Monitor system performance
- Backup configuration
- Update dependencies

## Support

### Getting Help
- Check documentation
- Review error messages
- Test with sample data
- Contact support team

### Reporting Issues
- Include error messages
- Provide sample data
- Describe steps to reproduce
- Include system information

### Feature Requests
- Describe desired functionality
- Provide use cases
- Suggest implementation
- Consider alternatives

## Examples

### Example 1: Basic Processing
```bash
# Process single PDF file
python main.py --input attendance.pdf --output reports/

# Check generated reports
ls reports/
# student_report_20241204_143022.xlsx
# subject_report_20241204_143022.xlsx
# defaulter_report_20241204_143022.xlsx
# comprehensive_report_20241204_143022.xlsx
```

### Example 2: Multiple Files
```bash
# Process multiple files
python main.py --input file1.pdf file2.jpg file3.png --output reports/
```

### Example 3: Web Dashboard
```bash
# Start dashboard
streamlit run dashboard.py

# Open browser to http://localhost:8501
# Upload files and process
# Download generated reports
```

### Example 4: Programmatic Usage
```python
from main import AttendanceAnomalySystem

# Initialize system
system = AttendanceAnomalySystem()

# Process files
results = system.run_complete_analysis(["attendance.pdf"])

# Access results
records = results['normalized_records']
validation = results['validation_results']
anomalies = results['anomaly_results']
reports = results['report_paths']

# Generate additional reports
system.generate_reports(records, anomalies)
```
