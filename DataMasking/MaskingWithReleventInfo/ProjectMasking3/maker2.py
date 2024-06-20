import pandas as pd
import os
import random
import string

def generate_unique_word(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def mask_values_in_columns(file_path, column_names, output_file_path):
    # Determine file type
    file_extension = os.path.splitext(file_path)[1]

    # Read the file
    try:
        if file_extension == '.xlsx':
            df = pd.read_excel(file_path)
        elif file_extension == '.csv':
            df = pd.read_csv(file_path, encoding='utf-8')
        else:
            raise ValueError("Unsupported file format. Please provide a .xlsx or .csv file.")
    except UnicodeDecodeError:
        if file_extension == '.csv':
            df = pd.read_csv(file_path, encoding='ISO-8859-1')  # Try an alternative encoding
        else:
            raise

    # Ensure the specified columns are treated as strings
    for column in column_names:
        df[column] = df[column].astype(str)

    # Initialize a dictionary to store mappings of original words to transformed words
    word_mapping = {}

    # Mask values in the specified columns using unique generated words
    for column in column_names:
        for index, row in df.iterrows():
            word = row[column]
            if word not in word_mapping:
                unique_word = generate_unique_word(len(word))
                word_mapping[word] = unique_word
            df.at[index, column] = word_mapping[word]

    # Save the masked data back to a file
    if file_extension == '.xlsx':
        df.to_excel(output_file_path, index=False)
    elif file_extension == '.csv':
        df.to_csv(output_file_path, index=False)

# Parameters
input_file_path = 'test.csv'  # Change this to your actual input file path
column_names = ["Category", "Subcategory"]  # Change this to your actual column names
output_file_path = 'masked_output2.csv'  # Change this to your desired output file path

# Execute the masking function
mask_values_in_columns(input_file_path, column_names, output_file_path)
