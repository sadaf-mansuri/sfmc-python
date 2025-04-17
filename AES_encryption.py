from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import base64
import hashlib
import os

# Function to generate AES key from API key (using SHA-256 hash)
def generate_aes_key(api_key):
    # Hash the API key to generate a 32-byte AES key (for AES-256)
    return hashlib.sha256(api_key.encode()).digest()

# Function to encrypt data using AES (CBC mode)
def encrypt_data(api_key, data):
    # Generate a 256-bit AES key from the API key
    aes_key = generate_aes_key(api_key)

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
    api_key = "your_api_key_here"  # Replace with your actual API key
    data = "This is a secret message."

    # Encrypt the data
    encrypted_data = encrypt_data(api_key, data)

    print(f"Encrypted Data: {encrypted_data}")
