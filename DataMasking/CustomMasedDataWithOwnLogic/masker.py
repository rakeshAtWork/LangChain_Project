import pandas as pd
import numpy as np
import random
import string

# Function to mask text by replacing it with random characters
def mask_text(value):
    if pd.isna(value):
        return value
    return ''.join(random.choices(string.ascii_letters + string.digits, k=len(value)))

# Function to partially mask text (e.g., show only last 4 characters)
def partial_mask_text(value, unmasked_chars=4):
    if pd.isna(value):
        return value
    masked_length = max(len(value) - unmasked_chars, 0)
    return '*' * masked_length + value[-unmasked_chars:]

# Load the Excel file
input_file = 'dummy_input_data.xlsx'
df = pd.read_excel(input_file)

# Specify the columns to mask
columns_to_mask = ['Name', 'Email', 'Phone']

# Apply the masking functions to the specified columns
for column in columns_to_mask:
    df[column] = df[column].apply(mask_text)  # You can use partial_mask_text if partial masking is preferred

# Save the masked data to a new Excel file
output_file = 'masked_data.xlsx'
df.to_excel(output_file, index=False)

print(f"Masked data has been saved to {output_file}")
