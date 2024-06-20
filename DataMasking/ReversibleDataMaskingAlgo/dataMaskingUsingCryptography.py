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

# Save to Excel
encrypted_file = 'encrypted_data.xlsx'
df.to_excel(encrypted_file, index=False)

# Decrypt the Email column
df['Email'] = df['Email'].apply(decrypt_data)

print("Encrypted and then decrypted DataFrame:")
print(df)
