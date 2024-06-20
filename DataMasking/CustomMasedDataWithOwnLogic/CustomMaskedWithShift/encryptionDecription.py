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

# Example data
data = 'Rakesh Raushan'

# Encrypt the data
encrypted_data = encrypt_data(data)
print(f'Encrypted: {encrypted_data}')

# Decrypt the data
decrypted_data = decrypt_data(encrypted_data)
print(f'Decrypted: {decrypted_data}')
