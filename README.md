# Attendance Anomaly System

A Python-based system for processing attendance sheets and detecting anomalies, built for Hacknova 2025 PS-1.

## Features

- **OCR Processing**: Extract text from PDF and image attendance sheets
- **Data Normalization**: Standardize attendance markings across different formats
- **Anomaly Detection**: Identify duplicates, invalid entries, and suspicious patterns
- **Report Generation**: Generate comprehensive Excel reports with attendance analytics
- **Web Dashboard**: Streamlit-based interface for easy interaction

## Installation

1. Install Python 3.8+
2. Install Tesseract OCR on your system
3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line
```python
python main.py --input attendance_sheet.pdf --output reports/
```

### Web Dashboard
```bash
streamlit run dashboard.py
```

## Project Structure

```
attendance_anomaly_system/
├── src/
│   ├── ocr/
│   ├── normalization/
│   ├── validation/
│   ├── anomaly_detection/
│   ├── aggregation/
│   └── reports/
├── tests/
├── sample_data/
├── outputs/
├── main.py
├── dashboard.py
└── requirements.txt
```

## Symbol Mapping Rules

- **Present**: P, ✔, ✓, .
- **Absent**: A, ×, -
- **Unclear**: blank, unknown symbols

## Error Handling

- Graceful handling of OCR failures
- Validation of extracted data
- Comprehensive logging of anomalies
- Fallback mechanisms for processing errors
