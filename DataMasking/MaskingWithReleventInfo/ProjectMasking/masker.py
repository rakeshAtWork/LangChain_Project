# Importing the pandas libraries.
import pandas as pd
import os

# Function to mask part of the text
def simple_mask(value, keep_ratio=0.75):
    if pd.isna(value):
        return value
    length = len(value)
    keep_length = int(length * keep_ratio)
    masked_part = ''.join(chr((ord(char) + 3) % 128) for char in value[keep_length:])
    return value[:keep_length] + masked_part


# Function to unmask part of the text
def simple_unmask(value, keep_ratio=0.75):
    if pd.isna(value):
        return value
    length = len(value)
    keep_length = int(length * keep_ratio)
    unmasked_part = ''.join(chr((ord(char) - 3) % 128) for char in value[keep_length:])
    return value[:keep_length] + unmasked_part


# File paths
input_file = 'test.csv'  # Example input file path
output_file = 'masked_output.csv'  # Example output file path
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

# Mask the specified columns
for column in columns_to_mask:
    df[column] = df[column].apply(simple_mask) # for each columns, masked is applying.

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

# Unmask the specified columns
for column in columns_to_mask:
    df_masked[column] = df_masked[column].apply(simple_unmask)

print("Masked DataFrame:")
print(df)

print("Unmasked DataFrame:")
print(df_masked)
