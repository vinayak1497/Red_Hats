# API Reference

## Overview

The Attendance Anomaly System provides a comprehensive API for processing attendance sheets, detecting anomalies, and generating reports.

## Core Modules

### OCR Module

#### PDFProcessor
```python
from src.ocr import PDFProcessor

processor = PDFProcessor()
result = processor.process_pdf("attendance.pdf")
```

**Methods:**
- `process_pdf(pdf_path: str) -> Dict[str, Any]`: Process PDF file and extract data
- `extract_tables_structured(pdf_path: str) -> List[pd.DataFrame]`: Extract tables using camelot
- `extract_tables_pdfplumber(pdf_path: str) -> List[pd.DataFrame]`: Extract tables using pdfplumber
- `extract_text(pdf_path: str) -> str`: Extract raw text from PDF

#### ImageProcessor
```python
from src.ocr import ImageProcessor

processor = ImageProcessor()
result = processor.process_image("attendance.jpg")
```

**Methods:**
- `process_image(image_path: str) -> Dict[str, Any]`: Process image file and extract data
- `extract_text_from_image(image: np.ndarray, config: str = '--psm 6') -> str`: Extract text from image
- `detect_tables(image: np.ndarray) -> List[Tuple[int, int, int, int]]`: Detect table regions
- `preprocess_image(image: np.ndarray) -> np.ndarray`: Preprocess image for OCR

#### TableExtractor
```python
from src.ocr import TableExtractor

extractor = TableExtractor()
records = extractor.process_tables(tables)
```

**Methods:**
- `process_tables(tables: List[List[List[str]]]) -> List[Dict[str, Any]]`: Process extracted tables
- `extract_attendance_data(tables: List[List[List[str]]]) -> List[Dict[str, Any]]`: Extract attendance data
- `consolidate_records(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]`: Consolidate records by roll number

### Normalization Module

#### SymbolMapper
```python
from src.normalization import SymbolMapper

mapper = SymbolMapper()
normalized = mapper.normalize_batch(records)
```

**Methods:**
- `normalize_symbol(symbol: str) -> str`: Normalize a single attendance symbol
- `normalize_attendance_record(record: Dict[str, Any]) -> Dict[str, Any]`: Normalize attendance record
- `calculate_attendance_percentage(record: Dict[str, Any]) -> float`: Calculate attendance percentage
- `is_defaulter(record: Dict[str, Any], threshold: float = 75.0) -> bool`: Check if student is defaulter

#### DataCleaner
```python
from src.normalization import DataCleaner

cleaner = DataCleaner()
cleaned_records, validation_report = cleaner.clean_batch(records)
```

**Methods:**
- `clean_roll_number(roll_number: str) -> Tuple[str, bool]`: Clean and validate roll number
- `clean_name(name: str) -> Tuple[str, bool]`: Clean and validate student name
- `clean_attendance_mark(mark: str) -> Tuple[str, str]`: Clean attendance mark
- `remove_duplicates(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]`: Remove duplicate records

### Validation Module

#### RollValidator
```python
from src.validation import RollValidator

validator = RollValidator()
results = validator.validate_all(records)
```

**Methods:**
- `validate_roll_number(roll_number: str) -> Dict[str, Any]`: Validate single roll number
- `find_duplicate_rolls(records: List[Dict[str, Any]]) -> Dict[str, List[int]]`: Find duplicate roll numbers
- `validate_roll_sequence(records: List[Dict[str, Any]]) -> Dict[str, Any]`: Validate roll number sequence
- `cross_validate_with_names(records: List[Dict[str, Any]]) -> Dict[str, Any]`: Cross-validate with names

#### DataValidator
```python
from src.validation import DataValidator

validator = DataValidator()
results = validator.validate_all(records)
```

**Methods:**
- `validate_attendance_mark(mark: str) -> Dict[str, Any]`: Validate attendance mark
- `validate_name(name: str) -> Dict[str, Any]`: Validate student name
- `validate_attendance_record(record: Dict[str, Any]) -> Dict[str, Any]`: Validate attendance record
- `check_attendance_consistency(records: List[Dict[str, Any]]) -> Dict[str, Any]`: Check consistency

#### IntegrityChecker
```python
from src.validation import IntegrityChecker

checker = IntegrityChecker()
results = checker.check_all_integrity(records)
```

**Methods:**
- `check_duplicate_entries(records: List[Dict[str, Any]]) -> Dict[str, Any]`: Check for duplicates
- `check_attendance_anomalies(records: List[Dict[str, Any]]) -> Dict[str, Any]`: Check for anomalies
- `check_data_consistency(records: List[Dict[str, Any]]) -> Dict[str, Any]`: Check data consistency
- `check_missing_data(records: List[Dict[str, Any]]) -> Dict[str, Any]`: Check for missing data

### Anomaly Detection Module

#### DuplicateDetector
```python
from src.anomaly_detection import DuplicateDetector

detector = DuplicateDetector()
results = detector.detect_all_duplicates(records)
```

**Methods:**
- `detect_duplicate_rolls(records: List[Dict[str, Any]]) -> Dict[str, Any]`: Detect duplicate roll numbers
- `detect_duplicate_names(records: List[Dict[str, Any]]) -> Dict[str, Any]`: Detect duplicate names
- `detect_duplicate_attendance_patterns(records: List[Dict[str, Any]]) -> Dict[str, Any]`: Detect duplicate patterns
- `detect_suspicious_patterns(records: List[Dict[str, Any]]) -> Dict[str, Any]`: Detect suspicious patterns

#### PatternAnalyzer
```python
from src.anomaly_detection import PatternAnalyzer

analyzer = PatternAnalyzer()
results = analyzer.analyze_all_patterns(records)
```

**Methods:**
- `analyze_attendance_distribution(records: List[Dict[str, Any]]) -> Dict[str, Any]`: Analyze distribution
- `analyze_individual_patterns(records: List[Dict[str, Any]]) -> Dict[str, Any]`: Analyze individual patterns
- `analyze_temporal_patterns(records: List[Dict[str, Any]]) -> Dict[str, Any]`: Analyze temporal patterns
- `analyze_correlation_patterns(records: List[Dict[str, Any]]) -> Dict[str, Any]`: Analyze correlations

### Aggregation Module

#### AttendanceCalculator
```python
from src.aggregation import AttendanceCalculator

calculator = AttendanceCalculator()
stats = calculator.calculate_all_statistics(records)
```

**Methods:**
- `calculate_student_attendance(record: Dict[str, Any]) -> Dict[str, Any]`: Calculate student statistics
- `calculate_subject_attendance(records: List[Dict[str, Any]], subject: str = None) -> Dict[str, Any]`: Calculate subject statistics
- `calculate_department_attendance(records: List[Dict[str, Any]]) -> Dict[str, Any]`: Calculate department statistics
- `identify_defaulters(records: List[Dict[str, Any]], threshold: float = None) -> List[Dict[str, Any]]`: Identify defaulters

#### StatisticsGenerator
```python
from src.aggregation import StatisticsGenerator

generator = StatisticsGenerator()
df = generator.generate_student_summary(records)
```

**Methods:**
- `generate_student_summary(records: List[Dict[str, Any]]) -> pd.DataFrame`: Generate student summary
- `generate_subject_summary(records: List[Dict[str, Any]]) -> pd.DataFrame`: Generate subject summary
- `generate_attendance_distribution(records: List[Dict[str, Any]]) -> Dict[str, Any]`: Generate distribution
- `generate_anomaly_summary(records: List[Dict[str, Any]], anomaly_reports: Dict[str, Any]) -> Dict[str, Any]`: Generate anomaly summary

#### DefaulterIdentifier
```python
from src.aggregation import DefaulterIdentifier

identifier = DefaulterIdentifier()
defaulters = identifier.identify_defaulters(records)
```

**Methods:**
- `identify_defaulters(records: List[Dict[str, Any]], threshold: float = None) -> List[Dict[str, Any]]`: Identify defaulters
- `categorize_defaulters(defaulters: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]`: Categorize defaulters
- `analyze_defaulter_patterns(defaulters: List[Dict[str, Any]]) -> Dict[str, Any]`: Analyze patterns
- `identify_at_risk_students(records: List[Dict[str, Any]], warning_threshold: float = 80.0) -> List[Dict[str, Any]]`: Identify at-risk students

### Reports Module

#### ExcelGenerator
```python
from src.reports import ExcelGenerator

generator = ExcelGenerator()
path = generator.create_student_report(records, "output.xlsx")
```

**Methods:**
- `create_student_report(records: List[Dict[str, Any]], output_path: str) -> str`: Create student report
- `create_subject_report(records: List[Dict[str, Any]], output_path: str) -> str`: Create subject report
- `create_defaulter_report(records: List[Dict[str, Any]], output_path: str) -> str`: Create defaulter report
- `create_anomaly_report(records: List[Dict[str, Any]], anomaly_reports: Dict[str, Any], output_path: str) -> str`: Create anomaly report
- `create_comprehensive_report(records: List[Dict[str, Any]], anomaly_reports: Dict[str, Any], output_path: str) -> str`: Create comprehensive report

#### ReportFormatter
```python
from src.reports import ReportFormatter

formatter = ReportFormatter()
df = formatter.format_student_summary(records)
```

**Methods:**
- `format_student_summary(records: List[Dict[str, Any]]) -> pd.DataFrame`: Format student summary
- `format_subject_summary(records: List[Dict[str, Any]]) -> pd.DataFrame`: Format subject summary
- `format_defaulter_list(records: List[Dict[str, Any]], threshold: float = 75.0) -> pd.DataFrame`: Format defaulter list
- `format_anomaly_report(anomaly_reports: Dict[str, Any]) -> Dict[str, pd.DataFrame]`: Format anomaly report

#### SummaryGenerator
```python
from src.reports import SummaryGenerator

generator = SummaryGenerator()
summary = generator.generate_executive_summary(records)
```

**Methods:**
- `generate_executive_summary(records: List[Dict[str, Any]], anomaly_reports: Dict[str, Any] = None) -> Dict[str, Any]`: Generate executive summary
- `generate_detailed_report(records: List[Dict[str, Any]], anomaly_reports: Dict[str, Any] = None) -> Dict[str, Any]`: Generate detailed report
- `generate_subject_report(records: List[Dict[str, Any]], subject: str) -> Dict[str, Any]`: Generate subject report
- `generate_defaulter_report(records: List[Dict[str, Any]], threshold: float = 75.0) -> Dict[str, Any]`: Generate defaulter report

## Main Application

### AttendanceAnomalySystem
```python
from main import AttendanceAnomalySystem

system = AttendanceAnomalySystem(output_dir="outputs")
results = system.run_complete_analysis(file_paths)
```

**Methods:**
- `process_file(file_path: str) -> dict`: Process single file
- `process_files(file_paths: list) -> dict`: Process multiple files
- `normalize_data(records: list) -> list`: Normalize attendance data
- `validate_data(records: list) -> dict`: Validate attendance data
- `detect_anomalies(records: list) -> dict`: Detect anomalies
- `generate_reports(records: list, anomaly_results: dict = None) -> dict`: Generate reports
- `run_complete_analysis(file_paths: list) -> dict`: Run complete analysis pipeline

## Data Structures

### Attendance Record
```python
{
    'roll_number': str,
    'name': str,
    'subject': str,
    'attendance_records': [
        {
            'status': str,  # 'P', 'A', or '?'
            'value': str,   # Original value
            'column': int   # Column index
        }
    ]
}
```

### Processing Result
```python
{
    'success': bool,
    'file': str,
    'records': List[Dict[str, Any]],
    'tables': List[List[List[str]]],
    'text': str,
    'error': str  # If success is False
}
```

### Validation Result
```python
{
    'roll_validation': Dict[str, Any],
    'data_validation': Dict[str, Any],
    'integrity_check': Dict[str, Any]
}
```

### Anomaly Result
```python
{
    'duplicate_report': Dict[str, Any],
    'pattern_report': Dict[str, Any]
}
```

## Error Handling

All methods return structured results with success indicators and error messages:

```python
{
    'success': bool,
    'data': Any,  # Result data if success is True
    'error': str   # Error message if success is False
}
```

## Configuration

### Symbol Mapping
```python
symbol_mappings = {
    'present': ['P', 'p', '✔', '✓', '.', '1', 'present'],
    'absent': ['A', 'a', '×', 'x', '-', '0', 'absent'],
    'unclear': ['', '?', 'unclear', 'unreadable']
}
```

### Validation Rules
- Roll numbers must be numeric
- Names must contain only letters, spaces, dots, and hyphens
- Attendance marks must be valid symbols
- Data must be consistent across records

### Thresholds
- Default defaulter threshold: 75%
- Severe defaulter threshold: 50%
- Critical defaulter threshold: 25%
- Warning threshold: 80%
