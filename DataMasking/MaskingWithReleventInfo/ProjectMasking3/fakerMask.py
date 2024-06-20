import pandas as pd
import faker
import os

# Initialize Faker for generating fake data
fake = faker.Faker()

def update_columns(file_path, output_file_path, columns_to_update):
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

    # Ensure the specified columns are treated as strings (if necessary)
    for column in columns_to_update:
        if df[column].dtype != 'object':  # Check if column is not already string type
            df[column] = df[column].astype(str)

    # Initialize a dictionary to store mappings of original values to updated values
    column_mappings = {col: {} for col in columns_to_update}

    # Update specified columns with fake data using Faker
    for column in columns_to_update:
        for index, value in df[column].items():
            if value not in column_mappings[column]:
                column_mappings[column][value] = fake.word()
            df.at[index, column] = column_mappings[column][value]

    # Save the updated data back to a file
    if file_extension == '.xlsx':
        df.to_excel(output_file_path, index=False)
    elif file_extension == '.csv':
        df.to_csv(output_file_path, index=False, encoding='utf-8')

# Example usage:
input_file_path = 'test.csv'  # Replace with your actual input file path
output_file_path = 'updated_data_Faker.csv'  # Replace with your desired output file path
columns_to_update = ["Category", "Subcategory"]  # Specify columns to update

update_columns(input_file_path, output_file_path, columns_to_update)
