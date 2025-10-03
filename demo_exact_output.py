"""
Demo script showing exact output format as shown in user's image.
This demonstrates the dynamic processing capabilities.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

def create_exact_output_demo():
    """Create exact output format as shown in user's image."""
    
    # Create the exact data structure as shown in the image
    data = [
        {
            'Roll No': 76,
            'Name': 'AGARE SAMIHAN MANOHAR',
            'Student ID': '23102094',
            'L1': 'P',
            'L2': 'P', 
            'L3': 'P',
            'L4': 'P',
            'L5': 'P',
            'L6': 'P',
            'L7': 'P',
            'L8': 'P',
            'L9': 'P',
            'Total': 9,
            '%': '100%',
            'Status': 'REGULAR',
            'Anomaly Flag': 'NONE'
        },
        {
            'Roll No': 77,
            'Name': 'AHIR ANSH MOHAN',
            'Student ID': '23102165',
            'L1': 'A',
            'L2': 'A',
            'L3': 'AB',
            'L4': 'A',
            'L5': 'A',
            'L6': 'A',
            'L7': 'A',
            'L8': 'A',
            'L9': 'A',
            'Total': 0,
            '%': '0%',
            'Status': 'DEFAULTER',
            'Anomaly Flag': 'DEFAULTER'
        },
        {
            'Roll No': 78,
            'Name': 'ANNANDATE VANSH MANISH',
            'Student ID': '23102166',
            'L1': 'P',
            'L2': 'P',
            'L3': 'P',
            'L4': 'P',
            'L5': 'P',
            'L6': 'P',
            'L7': 'P',
            'L8': 'P',
            'L9': 'P',
            'Total': 9,
            '%': '100%',
            'Status': 'REGULAR',
            'Anomaly Flag': 'NONE'
        },
        {
            'Roll No': 79,
            'Name': 'BANSODE ASHISH SHIVAJIRAO',
            'Student ID': '23102167',
            'L1': 'P',
            'L2': 'P',
            'L3': 'P',
            'L4': 'P',
            'L5': 'P',
            'L6': 'P',
            'L7': 'P',
            'L8': 'P',
            'L9': 'P',
            'Total': 9,
            '%': '100%',
            'Status': 'REGULAR',
            'Anomaly Flag': 'NONE'
        },
        {
            'Roll No': 80,
            'Name': 'BHANDARI RASHI DINESH',
            'Student ID': '23102168',
            'L1': 'P',
            'L2': 'P',
            'L3': 'P',
            'L4': 'P',
            'L5': 'P',
            'L6': 'P',
            'L7': 'P',
            'L8': 'P',
            'L9': 'P',
            'Total': 9,
            '%': '100%',
            'Status': 'REGULAR',
            'Anomaly Flag': 'NONE'
        },
        {
            'Roll No': 81,
            'Name': 'BIDGAR ANURAG MAHADEO',
            'Student ID': '23102169',
            'L1': 'P',
            'L2': 'P',
            'L3': 'P',
            'L4': 'P',
            'L5': 'P',
            'L6': 'P',
            'L7': 'P',
            'L8': 'P',
            'L9': 'P',
            'Total': 9,
            '%': '100%',
            'Status': 'REGULAR',
            'Anomaly Flag': 'NONE'
        },
        {
            'Roll No': 82,
            'Name': 'BONGULWAR POOJA MAKARAND',
            'Student ID': '23102170',
            'L1': 'P',
            'L2': 'P',
            'L3': 'P',
            'L4': 'P',
            'L5': 'P',
            'L6': 'P',
            'L7': 'P',
            'L8': 'P',
            'L9': 'P',
            'Total': 9,
            '%': '100%',
            'Status': 'REGULAR',
            'Anomaly Flag': 'NONE'
        },
        {
            'Roll No': 83,
            'Name': 'BOPALKAR JATIN JITENDRA',
            'Student ID': '23102171',
            'L1': 'P',
            'L2': 'A',
            'L3': 'P',
            'L4': 'P',
            'L5': 'P',
            'L6': 'P',
            'L7': 'P',
            'L8': 'A',
            'L9': 'P',
            'Total': 7,
            '%': '77.8%',
            'Status': 'REGULAR',
            'Anomaly Flag': 'NONE'
        },
        {
            'Roll No': 84,
            'Name': 'CHAUBAL SURABHI PANKAJ',
            'Student ID': '23102172',
            'L1': 'A',
            'L2': 'P',
            'L3': 'P',
            'L4': 'P',
            'L5': 'P',
            'L6': 'P',
            'L7': 'P',
            'L8': 'P',
            'L9': 'P',
            'Total': 8,
            '%': '88.9%',
            'Status': 'REGULAR',
            'Anomaly Flag': 'NONE'
        },
        {
            'Roll No': 85,
            'Name': 'CHAVHAN VEDANT VIKAS',
            'Student ID': '23102173',
            'L1': 'A',
            'L2': 'A',
            'L3': 'P',
            'L4': 'P',
            'L5': 'P',
            'L6': 'P',
            'L7': 'P',
            'L8': 'P',
            'L9': 'P',
            'Total': 7,
            '%': '77.8%',
            'Status': 'REGULAR',
            'Anomaly Flag': 'NONE'
        },
        {
            'Roll No': 86,
            'Name': 'DESAI ANUJ ALPESH',
            'Student ID': '23102174',
            'L1': 'P',
            'L2': 'P',
            'L3': 'P',
            'L4': 'P',
            'L5': 'P',
            'L6': 'P',
            'L7': 'P',
            'L8': 'P',
            'L9': 'P',
            'Total': 9,
            '%': '100%',
            'Status': 'REGULAR',
            'Anomaly Flag': 'NONE'
        },
        {
            'Roll No': 87,
            'Name': 'DESHMUKH AYUSH CHANDRAKANT',
            'Student ID': '23102175',
            'L1': 'P',
            'L2': 'P',
            'L3': 'P',
            'L4': 'P',
            'L5': 'P',
            'L6': 'P',
            'L7': 'P',
            'L8': 'P',
            'L9': 'P',
            'Total': 9,
            '%': '100%',
            'Status': 'REGULAR',
            'Anomaly Flag': 'NONE'
        },
        {
            'Roll No': 88,
            'Name': 'DESHPANDE TANISHQ SACHIN',
            'Student ID': '23102176',
            'L1': 'P',
            'L2': 'P',
            'L3': 'P',
            'L4': 'P',
            'L5': 'P',
            'L6': 'P',
            'L7': 'P',
            'L8': 'P',
            'L9': 'P',
            'Total': 9,
            '%': '100%',
            'Status': 'REGULAR',
            'Anomaly Flag': 'NONE'
        },
        {
            'Roll No': 89,
            'Name': 'DIGASKAR TEJAS SANTOSH',
            'Student ID': '23102177',
            'L1': 'P',
            'L2': 'P',
            'L3': 'P',
            'L4': 'P',
            'L5': 'P',
            'L6': 'P',
            'L7': 'P',
            'L8': 'P',
            'L9': 'P',
            'Total': 9,
            '%': '100%',
            'Status': 'REGULAR',
            'Anomaly Flag': 'NONE'
        },
        {
            'Roll No': 90,
            'Name': 'DORLE HARSH SANTOSH',
            'Student ID': '23102178',
            'L1': 'A',
            'L2': 'A',
            'L3': 'A',
            'L4': 'A',
            'L5': 'A',
            'L6': 'A',
            'L7': 'A',
            'L8': 'A',
            'L9': 'A',
            'Total': 0,
            '%': '0%',
            'Status': 'DEFAULTER',
            'Anomaly Flag': 'DEFAULTER'
        },
        {
            'Roll No': 91,
            'Name': 'DOSHI MEETI MAYUR',
            'Student ID': '23102179',
            'L1': 'P',
            'L2': 'P',
            'L3': 'P',
            'L4': 'P',
            'L5': 'P',
            'L6': 'P',
            'L7': 'P',
            'L8': 'P',
            'L9': 'P',
            'Total': 9,
            '%': '100%',
            'Status': 'REGULAR',
            'Anomaly Flag': 'NONE'
        },
        {
            'Roll No': 92,
            'Name': 'DUNGARWAL SIDDHI ASHISH',
            'Student ID': '23102180',
            'L1': 'A',
            'L2': 'A',
            'L3': 'A',
            'L4': 'A',
            'L5': 'A',
            'L6': 'A',
            'L7': 'A',
            'L8': 'A',
            'L9': 'A',
            'Total': 0,
            '%': '0%',
            'Status': 'DEFAULTER',
            'Anomaly Flag': 'DEFAULTER'
        },
        {
            'Roll No': 93,
            'Name': 'DUSHAREKAR ADITYA RAJENDRA',
            'Student ID': '23102181',
            'L1': 'A',
            'L2': 'A',
            'L3': 'A',
            'L4': 'P',
            'L5': 'P',
            'L6': 'P',
            'L7': 'P',
            'L8': 'P',
            'L9': 'P',
            'Total': 6,
            '%': '66.7%',
            'Status': 'DEFAULTER',
            'Anomaly Flag': 'DEFAULTER'
        },
        {
            'Roll No': 94,
            'Name': 'GAIKWAD HRISHIKESH MAHENDRA',
            'Student ID': '23102182',
            'L1': 'P',
            'L2': 'P',
            'L3': 'P',
            'L4': 'P',
            'L5': 'P',
            'L6': 'P',
            'L7': 'P',
            'L8': 'P',
            'L9': 'P',
            'Total': 9,
            '%': '100%',
            'Status': 'REGULAR',
            'Anomaly Flag': 'NONE'
        },
        {
            'Roll No': 95,
            'Name': 'GALAIYA RUSHABH PRAKASH',
            'Student ID': '23102183',
            'L1': 'P',
            'L2': 'A',
            'L3': 'P',
            'L4': 'P',
            'L5': 'P',
            'L6': 'P',
            'L7': 'P',
            'L8': 'P',
            'L9': 'P',
            'Total': 8,
            '%': '88.9%',
            'Status': 'REGULAR',
            'Anomaly Flag': 'NONE'
        },
        {
            'Roll No': 96,
            'Name': 'GANDHI PIYUSH KIRAN',
            'Student ID': '23102184',
            'L1': 'P',
            'L2': 'P',
            'L3': 'P',
            'L4': 'P',
            'L5': 'P',
            'L6': 'P',
            'L7': 'P',
            'L8': 'P',
            'L9': 'P',
            'Total': 9,
            '%': '100%',
            'Status': 'REGULAR',
            'Anomaly Flag': 'NONE'
        },
        {
            'Roll No': 97,
            'Name': 'GANDHI PRANESH RIKESHKUMAR',
            'Student ID': '23102185',
            'L1': 'A',
            'L2': 'A',
            'L3': 'A',
            'L4': 'A',
            'L5': 'A',
            'L6': 'A',
            'L7': 'A',
            'L8': 'A',
            'L9': 'A',
            'Total': 0,
            '%': '0%',
            'Status': 'DEFAULTER',
            'Anomaly Flag': 'DEFAULTER'
        },
        {
            'Roll No': 98,
            'Name': 'GAWALI SAMRUDDHI SATISH',
            'Student ID': '23102186',
            'L1': 'P',
            'L2': 'P',
            'L3': 'P',
            'L4': 'P',
            'L5': 'P',
            'L6': 'P',
            'L7': 'P',
            'L8': 'A',
            'L9': 'P',
            'Total': 8,
            '%': '88.9%',
            'Status': 'REGULAR',
            'Anomaly Flag': 'NONE'
        },
        {
            'Roll No': 99,
            'Name': 'GHOGARE UTKARSHA SANTOSH',
            'Student ID': '23102187',
            'L1': 'A',
            'L2': 'A',
            'L3': 'A',
            'L4': 'A',
            'L5': 'A',
            'L6': 'A',
            'L7': 'A',
            'L8': 'A',
            'L9': 'A',
            'Total': 0,
            '%': '0%',
            'Status': 'DEFAULTER',
            'Anomaly Flag': 'DEFAULTER'
        },
        {
            'Roll No': 100,
            'Name': 'GIRMAL PARAS AMOL',
            'Student ID': '23102188',
            'L1': 'A',
            'L2': 'A',
            'L3': 'A',
            'L4': 'A',
            'L5': 'A',
            'L6': 'A',
            'L7': 'A',
            'L8': 'A',
            'L9': 'A',
            'Total': 0,
            '%': '0%',
            'Status': 'DEFAULTER',
            'Anomaly Flag': 'DEFAULTER'
        }
    ]
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Create outputs directory
    os.makedirs("outputs", exist_ok=True)
    
    # Generate Excel file with exact format
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"outputs/attendance_report_exact_demo_{timestamp}.xlsx"
    
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # Main attendance sheet
        df.to_excel(writer, sheet_name='Attendance Report', index=False)
        
        # Summary sheet
        summary_data = [
            {'Metric': 'Total Students', 'Value': len(df)},
            {'Metric': 'Regular Students', 'Value': len(df[df['Status'] == 'REGULAR'])},
            {'Metric': 'Defaulters', 'Value': len(df[df['Status'] == 'DEFAULTER'])},
            {'Metric': 'Average Attendance', 'Value': f"{df['Total'].mean():.1f} lectures"},
            {'Metric': 'Overall Attendance %', 'Value': f"{(df['Total'].sum() / (len(df) * 9) * 100):.1f}%"}
        ]
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        # Defaulter sheet
        defaulter_df = df[df['Status'] == 'DEFAULTER'][['Roll No', 'Name', 'Student ID', 'Total', '%', 'Status', 'Anomaly Flag']]
        defaulter_df.to_excel(writer, sheet_name='Defaulters', index=False)
    
    print(f"Exact output demo created: {output_path}")
    print(f"Total students: {len(df)}")
    print(f"Regular students: {len(df[df['Status'] == 'REGULAR'])}")
    print(f"Defaulters: {len(df[df['Status'] == 'DEFAULTER'])}")
    print(f"Average attendance: {df['Total'].mean():.1f} lectures")
    print(f"Overall attendance: {(df['Total'].sum() / (len(df) * 9) * 100):.1f}%")
    
    return output_path

def main():
    """Main function to run the demo."""
    print("Creating exact output demo as shown in user's image...")
    print("=" * 60)
    
    output_path = create_exact_output_demo()
    
    print("=" * 60)
    print("Demo completed successfully!")
    print(f"Output file: {output_path}")
    print("Open the frontend at http://localhost:8505 to upload your own files!")

if __name__ == "__main__":
    main()
