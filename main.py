"""
Main application file for Attendance Anomaly System.
"""

import argparse
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import modules
from ocr import PDFProcessor, ImageProcessor, TableExtractor
from normalization import SymbolMapper, DataCleaner
from validation import RollValidator, DataValidator, IntegrityChecker
from anomaly_detection import DuplicateDetector, PatternAnalyzer
from aggregation import AttendanceCalculator, StatisticsGenerator, DefaulterIdentifier
from reports import ExcelGenerator, ReportFormatter, SummaryGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('attendance_system.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class AttendanceAnomalySystem:
    """Main class for the Attendance Anomaly System."""
    
    def __init__(self, output_dir: str = "outputs"):
        """
        Initialize the system.
        
        Args:
            output_dir: Directory for output files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize processors
        self.pdf_processor = PDFProcessor()
        self.image_processor = ImageProcessor()
        self.table_extractor = TableExtractor()
        
        # Initialize normalizers
        self.symbol_mapper = SymbolMapper()
        self.data_cleaner = DataCleaner()
        
        # Initialize validators
        self.roll_validator = RollValidator()
        self.data_validator = DataValidator()
        self.integrity_checker = IntegrityChecker()
        
        # Initialize anomaly detectors
        self.duplicate_detector = DuplicateDetector()
        self.pattern_analyzer = PatternAnalyzer()
        
        # Initialize aggregators
        self.attendance_calculator = AttendanceCalculator()
        self.statistics_generator = StatisticsGenerator()
        self.defaulter_identifier = DefaulterIdentifier()
        
        # Initialize report generators
        self.excel_generator = ExcelGenerator()
        self.report_formatter = ReportFormatter()
        self.summary_generator = SummaryGenerator()
        
        logger.info("Attendance Anomaly System initialized")
    
    def process_file(self, file_path: str) -> dict:
        """
        Process a single file.
        
        Args:
            file_path: Path to the file to process
            
        Returns:
            Processing result
        """
        try:
            logger.info(f"Processing file: {file_path}")
            
            # Determine file type and process
            if file_path.lower().endswith('.pdf'):
                result = self.pdf_processor.process_pdf(file_path)
            else:
                result = self.image_processor.process_image(file_path)
            
            if not result['success']:
                return {
                    'success': False,
                    'error': result.get('error', 'Processing failed'),
                    'file': file_path
                }
            
            # Extract tables
            tables = result['tables']
            records = self.table_extractor.process_tables(tables)
            
            logger.info(f"Extracted {len(records)} records from {file_path}")
            
            return {
                'success': True,
                'file': file_path,
                'records': records,
                'tables': tables,
                'text': result.get('text', '')
            }
            
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
            return {
                'success': False,
                'error': str(e),
                'file': file_path
            }
    
    def process_files(self, file_paths: list) -> dict:
        """
        Process multiple files.
        
        Args:
            file_paths: List of file paths to process
            
        Returns:
            Processing results
        """
        all_records = []
        processing_results = []
        
        for file_path in file_paths:
            result = self.process_file(file_path)
            processing_results.append(result)
            
            if result['success']:
                all_records.extend(result['records'])
        
        return {
            'success': True,
            'total_files': len(file_paths),
            'successful_files': sum(1 for r in processing_results if r['success']),
            'total_records': len(all_records),
            'processing_results': processing_results,
            'records': all_records
        }
    
    def normalize_data(self, records: list) -> list:
        """
        Normalize attendance data.
        
        Args:
            records: List of attendance records
            
        Returns:
            Normalized records
        """
        logger.info("Normalizing data...")
        
        # Clean data
        cleaned_records, validation_report = self.data_cleaner.clean_batch(records)
        
        # Normalize symbols
        normalized_records = self.symbol_mapper.normalize_batch(cleaned_records)
        
        logger.info(f"Normalized {len(normalized_records)} records")
        
        return normalized_records
    
    def validate_data(self, records: list) -> dict:
        """
        Validate attendance data.
        
        Args:
            records: List of attendance records
            
        Returns:
            Validation results
        """
        logger.info("Validating data...")
        
        # Roll validation
        roll_validation = self.roll_validator.validate_all(records)
        
        # Data validation
        data_validation = self.data_validator.validate_all(records)
        
        # Integrity check
        integrity_check = self.integrity_checker.check_all_integrity(records)
        
        validation_results = {
            'roll_validation': roll_validation,
            'data_validation': data_validation,
            'integrity_check': integrity_check
        }
        
        logger.info("Data validation completed")
        
        return validation_results
    
    def detect_anomalies(self, records: list) -> dict:
        """
        Detect anomalies in attendance data.
        
        Args:
            records: List of attendance records
            
        Returns:
            Anomaly detection results
        """
        logger.info("Detecting anomalies...")
        
        # Duplicate detection
        duplicate_report = self.duplicate_detector.detect_all_duplicates(records)
        
        # Pattern analysis
        pattern_report = self.pattern_analyzer.analyze_all_patterns(records)
        
        anomaly_results = {
            'duplicate_report': duplicate_report,
            'pattern_report': pattern_report
        }
        
        logger.info("Anomaly detection completed")
        
        return anomaly_results
    
    def generate_reports(self, records: list, anomaly_results: dict = None) -> dict:
        """
        Generate attendance reports.
        
        Args:
            records: List of attendance records
            anomaly_results: Anomaly detection results
            
        Returns:
            Report generation results
        """
        logger.info("Generating reports...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Generate Excel reports
        student_report_path = self.output_dir / f"student_report_{timestamp}.xlsx"
        self.excel_generator.create_student_report(records, str(student_report_path))
        
        subject_report_path = self.output_dir / f"subject_report_{timestamp}.xlsx"
        self.excel_generator.create_subject_report(records, str(subject_report_path))
        
        defaulter_report_path = self.output_dir / f"defaulter_report_{timestamp}.xlsx"
        self.excel_generator.create_defaulter_report(records, str(defaulter_report_path))
        
        # Generate anomaly report if available
        anomaly_report_path = None
        if anomaly_results:
            anomaly_report_path = self.output_dir / f"anomaly_report_{timestamp}.xlsx"
            self.excel_generator.create_anomaly_report(records, anomaly_results, str(anomaly_report_path))
        
        # Generate comprehensive report
        comprehensive_report_path = self.output_dir / f"comprehensive_report_{timestamp}.xlsx"
        self.excel_generator.create_comprehensive_report(records, anomaly_results or {}, str(comprehensive_report_path))
        
        report_paths = {
            'student_report': str(student_report_path),
            'subject_report': str(subject_report_path),
            'defaulter_report': str(defaulter_report_path),
            'comprehensive_report': str(comprehensive_report_path)
        }
        
        if anomaly_report_path:
            report_paths['anomaly_report'] = str(anomaly_report_path)
        
        logger.info("Reports generated successfully")
        
        return report_paths
    
    def run_complete_analysis(self, file_paths: list) -> dict:
        """
        Run complete analysis pipeline.
        
        Args:
            file_paths: List of file paths to process
            
        Returns:
            Complete analysis results
        """
        logger.info("Starting complete analysis...")
        
        # Process files
        processing_results = self.process_files(file_paths)
        
        if not processing_results['success']:
            return processing_results
        
        records = processing_results['records']
        
        if not records:
            return {
                'success': False,
                'error': 'No records found in processed files'
            }
        
        # Normalize data
        normalized_records = self.normalize_data(records)
        
        # Validate data
        validation_results = self.validate_data(normalized_records)
        
        # Detect anomalies
        anomaly_results = self.detect_anomalies(normalized_records)
        
        # Generate reports
        report_paths = self.generate_reports(normalized_records, anomaly_results)
        
        # Generate summary
        summary = self.summary_generator.generate_executive_summary(normalized_records, anomaly_results)
        
        return {
            'success': True,
            'processing_results': processing_results,
            'normalized_records': normalized_records,
            'validation_results': validation_results,
            'anomaly_results': anomaly_results,
            'report_paths': report_paths,
            'summary': summary
        }


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Attendance Anomaly System')
    parser.add_argument('--input', '-i', nargs='+', required=True, help='Input file paths')
    parser.add_argument('--output', '-o', default='outputs', help='Output directory')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Initialize system
    system = AttendanceAnomalySystem(args.output)
    
    # Run complete analysis
    results = system.run_complete_analysis(args.input)
    
    if results['success']:
        print(f"\n✅ Analysis completed successfully!")
        print(f"📊 Processed {results['processing_results']['total_records']} records")
        print(f"📁 Reports generated in: {args.output}")
        
        # Print summary
        summary = results['summary']
        print(f"\n📈 Summary:")
        print(f"   Total Students: {summary['report_metadata']['total_students']}")
        print(f"   Total Subjects: {summary['report_metadata']['total_subjects']}")
        print(f"   Overall Attendance: {summary['attendance_overview']['overall_attendance_percentage']:.2f}%")
        print(f"   Defaulters: {summary['defaulter_analysis']['total_defaulters']}")
        print(f"   Defaulter Rate: {summary['defaulter_analysis']['defaulter_percentage']:.2f}%")
        
        # Print report paths
        print(f"\n📄 Generated Reports:")
        for report_name, report_path in results['report_paths'].items():
            print(f"   {report_name}: {report_path}")
        
    else:
        print(f"\n❌ Analysis failed: {results.get('error', 'Unknown error')}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
