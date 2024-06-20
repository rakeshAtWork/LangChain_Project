import pandas as pd

# Simple Caesar cipher shift amount
shift = 3

# Function to encrypt data using a Caesar cipher
def caesar_encrypt(text, shift):
    if pd.isna(text):
        return text
    return ''.join(chr((ord(char) - 32 + shift) % 95 + 32) for char in text)

# Function to decrypt data using a Caesar cipher
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

# Encrypt the Email column
df['Email'] = df['Email'].apply(lambda x: caesar_encrypt(x, shift))

# Save to Excel
caesar_file = 'caesar_encrypted_data.xlsx'
df.to_excel(caesar_file, index=False)

# Decrypt the Email column
df['Email'] = df['Email'].apply(lambda x: caesar_decrypt(x, shift))

print("Caesar encrypted and then decrypted DataFrame:")
print(df)
