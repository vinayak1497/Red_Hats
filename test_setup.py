"""
Test script to verify the Attendance Anomaly System setup.
"""

import sys
import os

def test_imports():
    """Test if all modules can be imported."""
    try:
        # Add src to path
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
        
        # Test core imports
        from ocr import PDFProcessor, ImageProcessor, TableExtractor
        from normalization import SymbolMapper, DataCleaner
        from validation import RollValidator, DataValidator, IntegrityChecker
        from anomaly_detection import DuplicateDetector, PatternAnalyzer
        from aggregation import AttendanceCalculator, StatisticsGenerator, DefaulterIdentifier
        from reports import ExcelGenerator, ReportFormatter, SummaryGenerator
        
        print("✅ All modules imported successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_sample_data():
    """Test with sample data."""
    try:
        import pandas as pd
        
        # Load sample data
        sample_file = "sample_data/sample_attendance.csv"
        if os.path.exists(sample_file):
            df = pd.read_csv(sample_file)
            print(f"✅ Sample data loaded: {len(df)} records")
            print(f"   Columns: {list(df.columns)}")
            return True
        else:
            print("❌ Sample data file not found")
            return False
            
    except Exception as e:
        print(f"❌ Error loading sample data: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality."""
    try:
        # Add src to path
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
        
        from normalization import SymbolMapper
        
        # Test symbol mapping
        mapper = SymbolMapper()
        assert mapper.normalize_symbol('P') == 'P'
        assert mapper.normalize_symbol('✔') == 'P'
        assert mapper.normalize_symbol('A') == 'A'
        assert mapper.normalize_symbol('×') == 'A'
        
        print("✅ Basic functionality test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing Attendance Anomaly System Setup...")
    print("=" * 50)
    
    tests = [
        ("Module Imports", test_imports),
        ("Sample Data", test_sample_data),
        ("Basic Functionality", test_basic_functionality)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
        print("\n🚀 Next steps:")
        print("1. Run: streamlit run dashboard.py")
        print("2. Or run: python main.py --input sample_data/sample_attendance.csv")
    else:
        print("⚠️  Some tests failed. Please check the setup.")
    
    return passed == total

if __name__ == "__main__":
    main()
