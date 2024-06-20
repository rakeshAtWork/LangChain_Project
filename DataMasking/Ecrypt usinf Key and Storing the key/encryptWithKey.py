from cryptography.fernet import Fernet
import pandas as pd

# Generate a key for encryption and decryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Function to encrypt data
def encrypt_data(value):
    if pd.isna(value):
        return value
    return cipher_suite.encrypt(value.encode()).decode()

# Function to decrypt data
def decrypt_data(value):
    if pd.isna(value):
        return value
    return cipher_suite.decrypt(value.encode()).decode()

# Example DataFrame
data = {
    'Name': ['Alice Johnson', 'Bob Smith', 'Charlie Brown'],
    'Email': ['alice@example.com', 'bob@example.com', 'charlie@example.com']
}
df = pd.DataFrame(data)

# Encrypt the Email column
df['Email'] = df['Email'].apply(encrypt_data)

# Create a DataFrame to store the key
key_df = pd.DataFrame({'Key': [key.decode()]})

# Save the encrypted data and the key to separate sheets in an Excel file
with pd.ExcelWriter('encrypted_with_key.xlsx') as writer:
    df.to_excel(writer, sheet_name='EncryptedData', index=False)
    key_df.to_excel(writer, sheet_name='Key', index=False)

print("Encrypted data and key have been saved to 'encrypted_with_key.xlsx'")

# To read and decrypt the data:

# Load the Excel file
excel_file = pd.ExcelFile('encrypted_with_key.xlsx')

# Read the key
key_df = pd.read_excel(excel_file, sheet_name='Key')
stored_key = key_df.loc[0, 'Key'].encode()
cipher_suite = Fernet(stored_key)

# Read the encrypted data
encrypted_df = pd.read_excel(excel_file, sheet_name='EncryptedData')

# Decrypt the Email column
encrypted_df['Email'] = encrypted_df['Email'].apply(decrypt_data)

print("Decrypted DataFrame:")
print(encrypted_df)
