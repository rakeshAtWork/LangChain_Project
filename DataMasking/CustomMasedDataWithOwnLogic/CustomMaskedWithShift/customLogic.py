import pandas as pd

# Shift amount for the Caesar cipher
shift = 4

# Function to mask data using a Caesar cipher
def caesar_encrypt(text, shift):
    if pd.isna(text):
        return text
    return ''.join(chr((ord(char) - 32 + shift) % 95 + 32) for char in text)

# Function to unmask data using a Caesar cipher
def caesar_decrypt(text, shift):
    if pd.isna(text):
        return text
    return ''.join(chr((ord(char) - 32 - shift) % 95 + 32) for char in text)

# Example DataFrame
data = {
    'Name': ['Alice Johnson', 'Bob Smith', 'Charlie Brown'],
    'Email': ['alice@example.com', 'bob@example.com', 'charlie@example.com']
}
df = pd.DataFrame(data)

# Mask the Email column
df['Email'] = df['Email'].apply(lambda x: caesar_encrypt(x, shift))

# Save the masked data to an Excel file
masked_file = 'masked_data_caesar.xlsx'
df.to_excel(masked_file, index=False)

# To unmask the data, read the masked data and apply the reverse function
# Load the masked data
df_masked = pd.read_excel(masked_file)

# Unmask the Email column
df_masked['Email'] = df_masked['Email'].apply(lambda x: caesar_decrypt(x, shift))

print("Masked DataFrame:")
print(df)

print("Unmasked DataFrame:")
print(df_masked)
