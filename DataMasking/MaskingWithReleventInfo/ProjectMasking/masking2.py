import pandas as pd

# Function to mask part of the text
def simple_mask(value, keep_ratio=0.75):
    if pd.isna(value):
        return value
    length = len(value)
    keep_length = int(length * keep_ratio)
    mask_length = length - keep_length
    masked_part = ''.join(chr((ord(char) + 3) % 128) for char in value[keep_length:])
    return value[:keep_length] + masked_part

# Function to unmask part of the text
def simple_unmask(value, keep_ratio=0.75):
    if pd.isna(value):
        return value
    length = len(value)
    keep_length = int(length * keep_ratio)
    mask_length = length - keep_length
    unmasked_part = ''.join(chr((ord(char) - 3) % 128) for char in value[keep_length:])
    return value[:keep_length] + unmasked_part

# Example DataFrame
data = {
    'Name': ['Alice Johnson', 'Bob Smith', 'Charlie Brown'],
    'Email': ['alice@example.com', 'bob@example.com', 'charlie@example.com']
}
df = pd.DataFrame(data)

# Mask the Email column
df['Name'] = df['Name'].apply(simple_mask)

# Save the masked data to an Excel file
masked_file = 'masked_data_simple.xlsx'
df.to_excel(masked_file, index=False)

# To unmask the data, read the masked data and apply the reverse function
# Load the masked data
df_masked = pd.read_excel(masked_file)

# Unmask the Email column
df_masked['Name'] = df_masked['Name'].apply(simple_unmask)

print("Masked DataFrame:")
print(df)

print("Unmasked DataFrame:")
print(df_masked)
