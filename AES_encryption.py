import json
import base64
import hmac
import hashlib
import os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from urllib.parse import quote

# Function to generate AES key from Trustpilot's encryption key (if needed)
def generate_aes_key(encryption_key):
    # Hash the encryption key to generate a 256-bit AES key using SHA-256
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

    # Return the IV and encrypted data (Base64 encoded for safe transmission)
    return iv, encrypted_data

# Function to sign the encrypted data using HMAC (with SHA-256)
def sign_data(authentication_key, iv, encrypted_data):
    # Convert the authentication key to bytes and sign the encrypted data with HMAC
    hmac_key = authentication_key.encode()
    
    # Concatenate IV and ciphertext, then hash it with HMAC-SHA256
    hmac_data = iv + encrypted_data
    hmac_signature = hmac.new(hmac_key, hmac_data, hashlib.sha256).digest()

    return hmac_signature

# Function to encrypt and sign the JSON payload
def encrypt_and_sign_json(encryption_key, authentication_key, payload):
    # Convert the payload to JSON string
    payload_json = json.dumps(payload)

    # Encrypt the payload using AES
    iv, encrypted_payload = encrypt_data(encryption_key, payload_json)

    # Sign the encrypted payload using HMAC
    hmac_signature = sign_data(authentication_key, iv, encrypted_payload)

    # Combine IV, encrypted data, and signature
    result = iv + encrypted_payload + hmac_signature

    # Base64 encode the combined result
    base64_encoded_result = base64.b64encode(result).decode('utf-8')

    # URL-encode the Base64 result
    url_encoded_payload = quote(base64_encoded_result)

    return url_encoded_payload

# Example usage
if __name__ == "__main__":
    # Replace with your actual Trustpilot encryption and authentication keys
    encryption_key = "your_encryption_key_here"
    authentication_key = "your_authentication_key_here"

    # Example JSON payload to encrypt and sign
    payload = {
        "email": "user@example.com",
        "name": "John Doe",
        "ref": "abcd1234"
    }

    # Encrypt and sign the JSON payload
    encrypted_signed_payload = encrypt_and_sign_json(encryption_key, authentication_key, payload)

    # Create the final URL with the payload
    final_url = f"https://www.trustpilot.com/evaluate-bgl/yourdomain?p={encrypted_signed_payload}"

    print(f"Final URL: {final_url}")
