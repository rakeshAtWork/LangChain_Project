import pandas as pd
import os

# Function to shift characters while preserving meaning
def shift_characters(value, shift=3):
    if pd.isna(value):
        return value
    value = str(value)
    def shift_char(c):
        if 'a' <= c <= 'z':
            return chr((ord(c) - ord('a') + shift) % 26 + ord('a'))
        elif 'A' <= c <= 'Z':
            return chr((ord(c) - ord('A') + shift) % 26 + ord('A'))
        elif '0' <= c <= '9':
            return chr((ord(c) - ord('0') + shift) % 10 + ord('0'))
        else:
            return c

    return ''.join(shift_char(c) for c in value)

# Function to unshift characters back to original
def unshift_characters(value, shift=3):
    if pd.isna(value):
        return value
    value = str(value)
    return shift_characters(value, -shift)

# File paths
input_file = 'test.csv'  # Example input file path
output_file = 'masked_output2.csv'  # Example output file path
columns_to_mask = ["Category","Subcategory"]  # Specify the columns to mask

# Determine file format (CSV or XLSX) based on file extension
file_extension = os.path.splitext(input_file)[1]

# Read the data from the input file
try:
    if file_extension == '.xlsx':
        df = pd.read_excel(input_file)
    elif file_extension == '.csv':
        df = pd.read_csv(input_file, encoding='utf-8')
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")
except UnicodeDecodeError:
    df = pd.read_csv(input_file, encoding='latin1')  # Try 'latin1' if 'utf-8' fails

# Convert specified columns to string type and mask them
for column in columns_to_mask:
    df[column] = df[column].astype(str).apply(shift_characters)

# Save the masked data to a new file
if file_extension == '.xlsx':
    df.to_excel(output_file, index=False)
elif file_extension == '.csv':
    df.to_csv(output_file, index=False)
else:
    raise ValueError(f"Unsupported file format: {file_extension}")

# To verify, we can load the masked data and unmask the specified columns
# Load the masked data
if file_extension == '.xlsx':
    df_masked = pd.read_excel(output_file)
elif file_extension == '.csv':
    try:
        df_masked = pd.read_csv(output_file, encoding='utf-8')
    except UnicodeDecodeError:
        df_masked = pd.read_csv(output_file, encoding='latin1')
else:
    raise ValueError(f"Unsupported file format: {file_extension}")

# Convert specified columns to string type and unmask them
for column in columns_to_mask:
    df_masked[column] = df_masked[column].astype(str).apply(unshift_characters)

print("Masked DataFrame:")
print(df)

print("Unmasked DataFrame:")
print(df_masked)
