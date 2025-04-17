from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import base64
import hashlib
import os

# Function to generate AES key from the Trustpilot encryption key (if needed)
def generate_aes_key(encryption_key):
    # If Trustpilot provides the encryption key in string form, we can hash it to generate a 256-bit key
    # Convert the string to bytes before hashing
    return hashlib.sha256(encryption_key.encode()).digest()

# Function to encrypt data using AES (CBC mode)
def encrypt_data(encryption_key, data):
    # Generate AES key from the provided Trustpilot encryption key
    aes_key = generate_aes_key(encryption_key)

    # Generate a random 16-byte IV for AES (this should be unique for every encryption)
    iv = os.urandom(16)

    # Pad the data to ensure it's a multiple of the block size (16 bytes)
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data.encode()) + padder.finalize()

    # Create the AES cipher object
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Perform encryption
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    # Return the encrypted data along with the IV (Base64 encoded for safe transmission)
    return base64.b64encode(iv + encrypted_data).decode('utf-8')

# Example usage
if __name__ == "__main__":
    # Replace with the encryption key provided by Trustpilot
    trustpilot_encryption_key = "e204d/g4xJIS8...."  # Example encryption key

    # The data to encrypt
    data = "This is a secret message for Trustpilot."

    # Encrypt the data
    encrypted_data = encrypt_data(trustpilot_encryption_key, data)

    print(f"Encrypted Data: {encrypted_data}")
