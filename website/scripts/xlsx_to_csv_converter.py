#!/usr/bin/env python3
"""
Excel to CSV Converter Script
============================

This script converts all worksheets in an Excel (.xlsx) file to separate CSV files.
Perfect for processing school book lists where each worksheet represents a different class.

Usage:
    python xlsx_to_csv_converter.py

Requirements:
    pip install pandas openpyxl

Author: GitHub Copilot
Created for: Dalmia Vidya Mandir Book List Processing
"""

import pandas as pd
import os
import sys
from pathlib import Path

def xlsx_to_csv_converter(excel_file_path, output_directory=None):
    """
    Convert all worksheets in an Excel file to separate CSV files.
    
    Args:
        excel_file_path (str): Path to the Excel file
        output_directory (str): Directory to save CSV files (optional)
    
    Returns:
        list: List of created CSV file paths
    """
    
    # Validate input file
    if not os.path.exists(excel_file_path):
        raise FileNotFoundError(f"Excel file not found: {excel_file_path}")
    
    # Set output directory
    if output_directory is None:
        output_directory = os.path.dirname(excel_file_path)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)
    
    # Get the base filename without extension
    base_filename = Path(excel_file_path).stem
    
    print(f"📊 Processing Excel file: {excel_file_path}")
    print(f"📁 Output directory: {output_directory}")
    print("-" * 50)
    
    # Read all worksheets from the Excel file
    try:
        excel_data = pd.read_excel(excel_file_path, sheet_name=None, header=None)
    except Exception as e:
        print(f"❌ Error reading Excel file: {e}")
        return []
    
    created_files = []
    
    # Process each worksheet
    for sheet_name, dataframe in excel_data.items():
        # Clean sheet name for filename (remove invalid characters)
        clean_sheet_name = "".join(c for c in sheet_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        clean_sheet_name = clean_sheet_name.replace(' ', '_').lower()
        
        # Create CSV filename
        csv_filename = f"{clean_sheet_name}.csv"
        csv_path = os.path.join(output_directory, csv_filename)
        
        try:
            # Save to CSV
            dataframe.to_csv(csv_path, index=False, header=False)
            created_files.append(csv_path)
            
            # Print summary
            rows, cols = dataframe.shape
            print(f"✅ {sheet_name} → {csv_filename}")
            print(f"   📄 Rows: {rows}, Columns: {cols}")
            
        except Exception as e:
            print(f"❌ Error saving {sheet_name}: {e}")
    
    print("-" * 50)
    print(f"🎉 Conversion complete! Created {len(created_files)} CSV files.")
    
    return created_files

def main():
    """
    Main function to run the converter with user input or default file.
    """
    
    print("=" * 60)
    print("📚 EXCEL TO CSV CONVERTER")
    print("   For Dalmia Vidya Mandir Book Lists")
    print("=" * 60)
    
    # Default file path (adjust as needed)
    default_excel_file = "../public/Book list For Session 2025-26.xlsx"
    default_output_dir = "../public/"
    
    # Check if default file exists
    if os.path.exists(default_excel_file):
        print(f"🔍 Found default file: {default_excel_file}")
        choice = input("Use this file? (y/n): ").lower().strip()
        
        if choice == 'y' or choice == 'yes' or choice == '':
            excel_file = default_excel_file
            output_dir = default_output_dir
        else:
            excel_file = input("Enter path to Excel file: ").strip()
            output_dir = input("Enter output directory (press Enter for same directory): ").strip()
            if not output_dir:
                output_dir = None
    else:
        print("📁 Default file not found.")
        excel_file = input("Enter path to Excel file: ").strip()
        output_dir = input("Enter output directory (press Enter for same directory): ").strip()
        if not output_dir:
            output_dir = None
    
    # Convert the file
    try:
        created_files = xlsx_to_csv_converter(excel_file, output_dir)
        
        if created_files:
            print("\n📋 Created CSV files:")
            for file_path in created_files:
                print(f"   • {os.path.basename(file_path)}")
            
            print(f"\n💡 Tip: You can now use these CSV files to populate your website!")
            print("   Example: nursery.csv, lkg.csv, ukg.csv, class_i.csv, etc.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
