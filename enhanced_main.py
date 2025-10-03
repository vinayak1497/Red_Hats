"""
Enhanced main application for Attendance Anomaly System with signature analysis.
"""

import argparse
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
import pandas as pd

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import modules
from ocr import PDFProcessor, ImageProcessor, TableExtractor
from normalization import SymbolMapper, DataCleaner
from validation import RollValidator, DataValidator, IntegrityChecker
from anomaly_detection import DuplicateDetector, PatternAnalyzer
from aggregation import AttendanceCalculator, StatisticsGenerator, DefaulterIdentifier
from reports import ExcelGenerator, ReportFormatter, SummaryGenerator
from signature_analysis import SignatureMatcher

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


class EnhancedAttendanceSystem:
    """Enhanced attendance system with signature analysis for proxy detection."""
    
    def __init__(self, output_dir: str = "outputs"):
        """
        Initialize the enhanced system.
        
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
        
        # Initialize signature matcher
        self.signature_matcher = SignatureMatcher(similarity_threshold=0.9)
        
        logger.info("Enhanced Attendance Anomaly System initialized")
    
    def process_attendance_sheet(self, file_path: str) -> dict:
        """
        Process attendance sheet with signature analysis.
        
        Args:
            file_path: Path to the attendance sheet (PDF/PNG)
            
        Returns:
            Processing result with signature analysis
        """
        try:
            logger.info(f"Processing attendance sheet: {file_path}")
            
            # Process file based on type
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
            
            # For signature analysis, we need to work with the original image
            # This is a simplified version - in production, you'd extract cell regions
            signature_analysis = self._analyze_signatures_simplified(records)
            
            # Combine OCR results with signature analysis
            enhanced_records = self._combine_ocr_and_signature_analysis(records, signature_analysis)
            
            logger.info(f"Processed {len(enhanced_records)} records with signature analysis")
            
            return {
                'success': True,
                'file': file_path,
                'records': enhanced_records,
                'signature_analysis': signature_analysis,
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
    
    def _analyze_signatures_simplified(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Simplified signature analysis for demonstration.
        In production, this would analyze actual signature images.
        """
        signature_analysis = {
            'total_students': len(records),
            'proxy_detections': 0,
            'signature_consistency': {},
            'anomaly_flags': []
        }
        
        # Simulate signature analysis for each student
        for record in records:
            roll_number = record.get('roll_number', '')
            name = record.get('name', '')
            
            # Simulate signature consistency analysis
            # In real implementation, this would analyze actual signature images
            attendance_records = record.get('attendance_records', [])
            
            if len(attendance_records) > 1:
                # Simulate signature consistency check
                consistency_score = 0.85  # Simulated score
                
                if consistency_score < 0.9:  # 90% threshold
                    signature_analysis['proxy_detections'] += 1
                    signature_analysis['anomaly_flags'].append(
                        f"Proxy detected for {name} (Roll: {roll_number}) - Signature consistency: {consistency_score:.2f}"
                    )
                
                signature_analysis['signature_consistency'][roll_number] = consistency_score
        
        return signature_analysis
    
    def _combine_ocr_and_signature_analysis(self, records: List[Dict[str, Any]], 
                                          signature_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Combine OCR results with signature analysis.
        """
        enhanced_records = []
        
        for record in records:
            roll_number = record.get('roll_number', '')
            name = record.get('name', '')
            
            # Get signature consistency for this student
            consistency = signature_analysis['signature_consistency'].get(roll_number, 1.0)
            
            # Process attendance records with signature analysis
            enhanced_attendance = []
            total_present = 0
            total_lectures = 0
            proxy_flags = []
            
            for i, att_record in enumerate(record.get('attendance_records', [])):
                original_status = att_record.get('status', '')
                original_value = att_record.get('value', '')
                
                # Determine final status based on signature analysis
                if consistency < 0.9:  # Proxy detected
                    final_status = 'A'  # Mark as absent due to proxy
                    proxy_flags.append(f"Lecture {i+1}: Proxy detected")
                elif original_status == 'P' or original_value in ['P', 'p', 'Present']:
                    final_status = 'P'
                    total_present += 1
                elif original_status == 'A' or original_value in ['A', 'a', 'Absent', 'X']:
                    final_status = 'A'
                else:
                    final_status = 'A'  # Default to absent for unclear marks
                
                total_lectures += 1
                
                enhanced_attendance.append({
                    'lecture': i + 1,
                    'original_value': original_value,
                    'original_status': original_status,
                    'final_status': final_status,
                    'is_present': final_status == 'P',
                    'signature_consistency': consistency,
                    'is_proxy': consistency < 0.9
                })
            
            # Calculate attendance percentage
            attendance_percentage = (total_present / total_lectures * 100) if total_lectures > 0 else 0
            
            # Determine status
            if consistency < 0.9:
                status = 'Proxy Detected'
                anomaly_flag = 'PROXY'
            elif attendance_percentage < 75:
                status = 'Defaulter'
                anomaly_flag = 'DEFAULTER'
            else:
                status = 'Regular'
                anomaly_flag = 'NONE'
            
            enhanced_record = {
                'roll_number': roll_number,
                'name': name,
                'subject': record.get('subject', ''),
                'lecture_attendance': enhanced_attendance,
                'total_lectures': total_lectures,
                'present_count': total_present,
                'absent_count': total_lectures - total_present,
                'attendance_percentage': round(attendance_percentage, 2),
                'status': status,
                'anomaly_flag': anomaly_flag,
                'signature_consistency': round(consistency, 3),
                'proxy_flags': proxy_flags
            }
            
            enhanced_records.append(enhanced_record)
        
        return enhanced_records
    
    def generate_enhanced_excel_report(self, records: List[Dict[str, Any]], 
                                     output_path: str) -> str:
        """
        Generate enhanced Excel report with signature analysis.
        """
        try:
            # Create DataFrame for Excel report
            report_data = []
            
            for record in records:
                # Create lecture columns
                lecture_data = {}
                for i, att in enumerate(record['lecture_attendance']):
                    lecture_data[f'Lecture_{i+1}'] = att['final_status']
                
                # Create row data
                row_data = {
                    'Roll_No': record['roll_number'],
                    'Name': record['name'],
                    'Subject': record['subject'],
                    'Total_Lectures': record['total_lectures'],
                    'Present': record['present_count'],
                    'Absent': record['absent_count'],
                    'Attendance_%': f"{record['attendance_percentage']:.2f}%",
                    'Status': record['status'],
                    'Anomaly_Flag': record['anomaly_flag'],
                    'Signature_Consistency': f"{record['signature_consistency']:.3f}",
                    **lecture_data
                }
                
                report_data.append(row_data)
            
            # Create DataFrame
            df = pd.DataFrame(report_data)
            
            # Create Excel file with multiple sheets
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                # Main attendance sheet
                df.to_excel(writer, sheet_name='Attendance_Report', index=False)
                
                # Summary sheet
                summary_data = self._create_summary_sheet(records)
                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
                
                # Proxy detection sheet
                proxy_data = self._create_proxy_detection_sheet(records)
                if proxy_data:
                    proxy_df = pd.DataFrame(proxy_data)
                    proxy_df.to_excel(writer, sheet_name='Proxy_Detection', index=False)
            
            logger.info(f"Enhanced Excel report generated: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Excel report generation failed: {e}")
            raise
    
    def _create_summary_sheet(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create summary data for Excel report."""
        total_students = len(records)
        total_lectures = max(record['total_lectures'] for record in records) if records else 0
        
        # Count by status
        regular_count = len([r for r in records if r['status'] == 'Regular'])
        defaulter_count = len([r for r in records if r['status'] == 'Defaulter'])
        proxy_count = len([r for r in records if r['status'] == 'Proxy Detected'])
        
        # Calculate averages
        avg_attendance = sum(r['attendance_percentage'] for r in records) / total_students if total_students > 0 else 0
        avg_consistency = sum(r['signature_consistency'] for r in records) / total_students if total_students > 0 else 0
        
        return [
            {'Metric': 'Total Students', 'Value': total_students},
            {'Metric': 'Total Lectures', 'Value': total_lectures},
            {'Metric': 'Regular Students', 'Value': regular_count},
            {'Metric': 'Defaulters', 'Value': defaulter_count},
            {'Metric': 'Proxy Detected', 'Value': proxy_count},
            {'Metric': 'Average Attendance %', 'Value': f"{avg_attendance:.2f}%"},
            {'Metric': 'Average Signature Consistency', 'Value': f"{avg_consistency:.3f}"},
            {'Metric': 'Report Generated', 'Value': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        ]
    
    def _create_proxy_detection_sheet(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create proxy detection data for Excel report."""
        proxy_records = [r for r in records if r['status'] == 'Proxy Detected']
        
        proxy_data = []
        for record in proxy_records:
            proxy_data.append({
                'Roll_No': record['roll_number'],
                'Name': record['name'],
                'Subject': record['subject'],
                'Signature_Consistency': f"{record['signature_consistency']:.3f}",
                'Attendance_%': f"{record['attendance_percentage']:.2f}%",
                'Proxy_Flags': '; '.join(record['proxy_flags']),
                'Status': 'PROXY DETECTED'
            })
        
        return proxy_data
    
    def run_enhanced_analysis(self, file_paths: List[str]) -> dict:
        """
        Run enhanced analysis with signature detection.
        """
        logger.info("Starting enhanced attendance analysis...")
        
        all_records = []
        processing_results = []
        
        for file_path in file_paths:
            result = self.process_attendance_sheet(file_path)
            processing_results.append(result)
            
            if result['success']:
                all_records.extend(result['records'])
        
        if not all_records:
            return {
                'success': False,
                'error': 'No records processed successfully'
            }
        
        # Generate enhanced Excel report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        excel_path = self.output_dir / f"enhanced_attendance_report_{timestamp}.xlsx"
        
        try:
            self.generate_enhanced_excel_report(all_records, str(excel_path))
            
            return {
                'success': True,
                'total_records': len(all_records),
                'excel_report': str(excel_path),
                'processing_results': processing_results,
                'records': all_records
            }
            
        except Exception as e:
            logger.error(f"Enhanced analysis failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }


def main():
    """Main function for enhanced attendance system."""
    parser = argparse.ArgumentParser(description='Enhanced Attendance Anomaly System with Signature Analysis')
    parser.add_argument('--input', '-i', nargs='+', required=True, help='Input file paths (PDF/PNG)')
    parser.add_argument('--output', '-o', default='outputs', help='Output directory')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Initialize enhanced system
    system = EnhancedAttendanceSystem(args.output)
    
    # Run enhanced analysis
    results = system.run_enhanced_analysis(args.input)
    
    if results['success']:
        print(f"\n✅ Enhanced analysis completed successfully!")
        print(f"📊 Processed {results['total_records']} records")
        print(f"📁 Enhanced Excel report: {results['excel_report']}")
        
        # Show summary
        records = results['records']
        if records:
            proxy_count = len([r for r in records if r['status'] == 'Proxy Detected'])
            defaulter_count = len([r for r in records if r['status'] == 'Defaulter'])
            regular_count = len([r for r in records if r['status'] == 'Regular'])
            
            print(f"\n📈 Summary:")
            print(f"   Regular Students: {regular_count}")
            print(f"   Defaulters: {defaulter_count}")
            print(f"   Proxy Detected: {proxy_count}")
            
            if proxy_count > 0:
                print(f"\n⚠️  Proxy Detection Results:")
                for record in records:
                    if record['status'] == 'Proxy Detected':
                        print(f"   {record['roll_number']} | {record['name']} | Consistency: {record['signature_consistency']:.3f}")
        
    else:
        print(f"\n❌ Enhanced analysis failed: {results.get('error', 'Unknown error')}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

