import pandas as pd
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def read_data(file_path):
    """
    Controller function to read data from various file formats.
    Checks file extension and calls appropriate reader function.

    Args:
        file_path (str): Full path to the input file

    Returns:
        pandas.DataFrame or str: DataFrame for structured data (Excel, CSV),
                                string for unstructured text (.txt),
                                None if file not found or unsupported type
    """
    if not os.path.exists(file_path):
        logging.error(f"File not found: {file_path}")
        return None

    # Get file extension
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()

    try:
        if file_extension in ['.xlsx', '.xls']:
            return _read_excel(file_path)
        elif file_extension == '.csv':
            return _read_csv(file_path)
        elif file_extension == '.txt':
            return _read_text(file_path)
        else:
            logging.error(f"Unsupported file type: {file_extension}")
            print(f"❌ Error: Unsupported file format '{file_extension}'")
            print("   Supported formats: .xlsx, .xls, .csv, .txt")
            return None
    except Exception as e:
        logging.error(f"Error reading file: {e}")
        print(f"❌ Error reading file: {e}")
        return None

def _read_excel(file_path):
    """
    Read data from Excel file with enhanced error handling.
    
    Args:
        file_path (str): Path to Excel file
        
    Returns:
        pandas.DataFrame: Loaded data with cleaned columns
    """
    try:
        # Read Excel file
        df = pd.read_excel(file_path, engine='openpyxl')
        
        # Clean column names (remove extra spaces, make lowercase)
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        
        # Remove completely empty rows
        df = df.dropna(how='all')
        
        # Display basic info
        print(f"   ✓ Loaded {len(df)} rows and {len(df.columns)} columns")
        print(f"   ✓ Columns: {', '.join(df.columns[:5])}" + 
              (f", ... (+{len(df.columns)-5} more)" if len(df.columns) > 5 else ""))
        
        return df
    except ImportError:
        print("❌ Error: 'openpyxl' library not found.")
        print("   Install it using: pip install openpyxl")
        return None
    except Exception as e:
        logging.error(f"Excel reading error: {e}")
        print(f"❌ Error reading Excel file: {e}")
        return None

def _read_csv(file_path):
    """
    Read data from CSV file with enhanced error handling and encoding detection.
    
    Args:
        file_path (str): Path to CSV file
        
    Returns:
        pandas.DataFrame: Loaded data with cleaned columns
    """
    encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
    
    for encoding in encodings:
        try:
            df = pd.read_csv(file_path, encoding=encoding)
            
            # Clean column names
            df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
            
            # Remove completely empty rows
            df = df.dropna(how='all')
            
            # Display basic info
            print(f"   ✓ Loaded {len(df)} rows and {len(df.columns)} columns")
            print(f"   ✓ Columns: {', '.join(df.columns[:5])}" + 
                  (f", ... (+{len(df.columns)-5} more)" if len(df.columns) > 5 else ""))
            
            return df
        except UnicodeDecodeError:
            continue
        except Exception as e:
            logging.error(f"CSV reading error: {e}")
            print(f"❌ Error reading CSV file: {e}")
            return None
    
    print(f"❌ Error: Could not decode CSV file with any supported encoding")
    return None

def _read_text(file_path):
    """
    Read plain text file content.
    
    Args:
        file_path (str): Path to text file
        
    Returns:
        str: Full content of the text file
    """
    encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            
            word_count = len(content.split())
            char_count = len(content)
            
            print(f"   ✓ Loaded text file")
            print(f"   ✓ Characters: {char_count:,} | Words: {word_count:,}")
            
            return content
        except UnicodeDecodeError:
            continue
        except Exception as e:
            logging.error(f"Text reading error: {e}")
            print(f"❌ Error reading text file: {e}")
            return None
    
    print(f"❌ Error: Could not decode text file with any supported encoding")
    return None

def validate_student_data(df):
    """
    Validate that DataFrame contains expected student data structure.
    
    Args:
        df (pandas.DataFrame): DataFrame to validate
        
    Returns:
        bool: True if validation passes, False otherwise
    """
    if df is None or df.empty:
        print("❌ Validation failed: Data is empty")
        return False
    
    # Check for common student data columns
    expected_columns = ['student', 'name', 'grade', 'score', 'marks']
    has_expected = any(col in df.columns for col in expected_columns)
    
    if not has_expected:
        print("⚠️  Warning: No standard student columns detected")
        print(f"   Found columns: {', '.join(df.columns)}")
        print("   Proceeding with analysis anyway...")
    
    return True