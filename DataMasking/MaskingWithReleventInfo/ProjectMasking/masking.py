import pandas as pd
import string

# Define the characters to use for masking
readable_characters = string.ascii_letters + string.digits + string.punctuation + ' '
character_set_size = len(readable_characters)

# Mapping from character to index
char_to_index = {char: idx for idx, char in enumerate(readable_characters)}

# Function to mask data by shifting characters within the readable characters set
def mask_text(value, shift=3):
    if pd.isna(value):
        return value
    masked_value = []
    for char in value:
        if char in char_to_index:
            masked_value.append(readable_characters[(char_to_index[char] + shift) % character_set_size])
        else:
            masked_value.append(char)
    return ''.join(masked_value)

# Function to unmask data by reversing the shift
def unmask_text(value, shift=3):
    if pd.isna(value):
        return value
    unmasked_value = []
    for char in value:
        if char in char_to_index:
            unmasked_value.append(readable_characters[(char_to_index[char] - shift) % character_set_size])
        else:
            unmasked_value.append(char)
    return ''.join(unmasked_value)

# Example DataFrame
data = {
    'Name': ['Alice Johnson', 'Bob Smith', 'Charlie Brown'],
    'Email': ['alice@example.com', 'bob@example.com', 'charlie@example.com']
}
df = pd.DataFrame(data)

# Mask the Email column
df['Name'] = df['Name'].apply(mask_text)

# Save the masked data to an Excel file
masked_file = 'masked_data_related.xlsx'
df.to_excel(masked_file, index=False)

# To unmask the data, read the masked data and apply the reverse function
# Load the masked data
df_masked = pd.read_excel(masked_file)

# Unmask the Email column
df_masked['Name'] = df_masked['Name'].apply(unmask_text)

print("Masked DataFrame:")
print(df)

print("Unmasked DataFrame:")
print(df_masked)
