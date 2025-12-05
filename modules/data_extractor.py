import pandas as pd
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def read_data(file_path):
    """
    Controller function to read data from various file formats.
    Checks file extension and calls appropriate reader function.
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
            return None
    except Exception as e:
        logging.error(f"Error reading file: {e}")
        return None

def _read_excel(file_path):
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        df = df.dropna(how='all')
        return df
    except Exception as e:
        logging.error(f"Excel reading error: {e}")
        return None

def _read_csv(file_path):
    encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
    for encoding in encodings:
        try:
            df = pd.read_csv(file_path, encoding=encoding)
            df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
            df = df.dropna(how='all')
            return df
        except UnicodeDecodeError:
            continue
        except Exception as e:
            logging.error(f"CSV reading error: {e}")
            return None
    return None

def _read_text(file_path):
    encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    return None

def get_chart_data(student_data):
    """
    Extracts numeric data for visualization.
    Calculates the average score for each numeric column (Subject).
    """
    if not isinstance(student_data, pd.DataFrame):
        return None

    try:
        # Select only numeric columns
        numeric_df = student_data.select_dtypes(include=['number'])
        
        # Filter out likely non-grade columns (like IDs or phone numbers)
        # Heuristic: Columns with mean > 1000 are probably not grades, or if name contains 'id', 'phone'
        grade_cols = []
        for col in numeric_df.columns:
            if 'id' in col or 'phone' in col or 'zip' in col or 'year' in col:
                continue
            grade_cols.append(col)
        
        if not grade_cols:
            return None

        # Calculate averages
        averages = numeric_df[grade_cols].mean().to_dict()
        
        # Prepare data for Chart.js
        chart_data = {
            'labels': [col.replace('_', ' ').title() for col in averages.keys()],
            'values': [round(val, 2) for val in averages.values()]
        }
        
        return chart_data
    except Exception as e:
        logging.error(f"Error extracting chart data: {e}")
        return None