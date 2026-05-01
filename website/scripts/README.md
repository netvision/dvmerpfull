# Excel to CSV Converter

This script converts all worksheets in your Excel file to separate CSV files, making it easy to process each class's book list individually.

## 🚀 Quick Start

### Option 1: Use the Batch File (Windows)
1. Double-click `run_converter.bat`
2. The script will automatically install required packages and run the converter

### Option 2: Manual Setup
1. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the converter:
   ```bash
   python xlsx_to_csv_converter.py
   ```

## 📁 File Structure

```
scripts/
├── xlsx_to_csv_converter.py    # Main conversion script
├── requirements.txt            # Python dependencies
├── run_converter.bat          # Windows batch file for easy execution
└── README.md                  # This file
```

## 🔧 How It Works

1. **Input**: Your Excel file (e.g., "Book list For Session 2025-26.xlsx")
2. **Processing**: Each worksheet is converted to a separate CSV file
3. **Output**: Clean CSV files named after each worksheet
   - Example: "Nursery" worksheet → `nursery.csv`
   - Example: "Class I" worksheet → `class_i.csv`

## 📊 Features

- ✅ Converts all worksheets automatically
- ✅ Handles special characters in sheet names
- ✅ Preserves original data structure
- ✅ Creates clean, web-ready CSV files
- ✅ Detailed progress reporting
- ✅ Error handling and validation

## 💡 Usage Tips

1. **Default File**: Place your Excel file as `../public/Book list For Session 2025-26.xlsx`
2. **Custom File**: The script will prompt you to enter a custom path if needed
3. **Output Location**: CSV files are saved to the `../public/` directory by default
4. **File Naming**: Sheet names are automatically cleaned for web use

## 🔄 Integration with Website

After conversion, you can use the CSV files to populate your BookList page:

1. CSV files are saved to the `public/` directory
2. Each file can be processed individually (like we did with nursery.csv)
3. Files are accessible via direct links (e.g., `/nursery.csv`)

## 📋 Example Output

```
📊 Processing Excel file: ../public/Book list For Session 2025-26.xlsx
📁 Output directory: ../public/
--------------------------------------------------
✅ Nursery → nursery.csv
   📄 Rows: 25, Columns: 10
✅ LKG → lkg.csv
   📄 Rows: 25, Columns: 10
✅ UKG → ukg.csv
   📄 Rows: 25, Columns: 10
✅ Class I → class_i.csv
   📄 Rows: 30, Columns: 10
--------------------------------------------------
🎉 Conversion complete! Created 4 CSV files.
```

## 🆘 Troubleshooting

- **Python not found**: Install Python from [python.org](https://python.org)
- **Permission errors**: Run as administrator or check file permissions
- **Excel file not found**: Verify the file path and ensure the file exists
- **Package installation fails**: Try upgrading pip: `python -m pip install --upgrade pip`
