import pandas as pd
from anonympy import anonymize
import os

def anonymize_file(input_file, output_file, columns_to_anonymize):
    _, file_extension = os.path.splitext(input_file)
    
    # Load the file into a pandas DataFrame based on file extension
    if file_extension == '.csv':
        df = pd.read_csv(input_file)
    elif file_extension in ['.xls', '.xlsx']:
        df = pd.read_excel(input_file)
    else:
        raise ValueError("Unsupported file format. Only CSV, XLS, or XLSX files are supported.")
    
    # Anonymize the specified columns
    for col in columns_to_anonymize:
        df[col] = df[col].apply(anonymize)
    
    # Save the anonymized DataFrame to a new file based on file extension
    if file_extension == '.csv':
        df.to_csv(output_file, index=False)
    elif file_extension in ['.xls', '.xlsx']:
        df.to_excel(output_file, index=False)
    
    print(f"Anonymized data saved to {output_file}")

# Example usage:
input_file = 'test.csv'  # Replace with your input file path
output_file = 'output.csv'  # Replace with your output file path
columns_to_anonymize = ["Category", "Subcategory"]  # Replace with columns to anonymize

anonymize_file(input_file, output_file, columns_to_anonymize)
