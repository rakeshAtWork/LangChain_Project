import pandas as pd
from faker import Faker

# Initialize Faker
fake = Faker()

# Function to mask specific columns
def mask_columns(df, columns_to_mask):
    for column in columns_to_mask:
        if column in df.columns:
            if column.lower().find("name") != -1:
                df[column] = df[column].apply(lambda x: fake.name())
            elif column.lower().find("email") != -1:
                df[column] = df[column].apply(lambda x: fake.email())
            elif column.lower().find("ssn") != -1:
                df[column] = df[column].apply(lambda x: fake.ssn())
            # Add more conditions for other types of data if needed
    return df

# Load data from CSV or XLSX
def load_data(file_path):
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        return pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format")

# Save masked data to the same format as input
def save_data(df, file_path):
    if file_path.endswith('.csv'):
        df.to_csv(file_path, index=False)
    elif file_path.endswith('.xlsx'):
        df.to_excel(file_path, index=False)
    else:
        raise ValueError("Unsupported file format")

# Main function
def main(input_file, output_file, columns_to_mask):
    # Load data
    df = load_data(input_file)
    # Mask specific columns
    masked_df = mask_columns(df, columns_to_mask)
    # Save masked data
    save_data(masked_df, output_file)
    print(f"Data masking complete. Masked data saved to '{output_file}'.")

# Example usage
if __name__ == "__main__":
    input_file = 'test.xlsx'  # Input file path
    output_file = 'masked_data.xlsx'  # Output file path
    columns_to_mask = ["Category","Subcategory"]  # Columns to mask
    main(input_file, output_file, columns_to_mask)
