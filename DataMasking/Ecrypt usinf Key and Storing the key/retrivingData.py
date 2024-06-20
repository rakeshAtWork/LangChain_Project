from cryptography.fernet import Fernet
import pandas as pd

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