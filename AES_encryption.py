import json
import base64
import hmac
import hashlib
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

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

    # Return the encrypted data along with the IV (Base64 encoded for safe transmission)
    return base64.b64encode(iv + encrypted_data).decode('utf-8')

# Function to sign the encrypted data using HMAC (with SHA-256)
def sign_data(authentication_key, encrypted_data):
    # Convert the authentication key to bytes and sign the encrypted data with HMAC
    hmac_key = authentication_key.encode()
    return hmac.new(hmac_key, encrypted_data.encode(), hashlib.sha256).hexdigest()

# Function to encrypt and sign the JSON payload
def encrypt_and_sign_json(encryption_key, authentication_key, payload):
    # Convert the payload to JSON string
    payload_json = json.dumps(payload)

    # Encrypt the payload using AES
    encrypted_payload = encrypt_data(encryption_key, payload_json)

    # Sign the encrypted payload using HMAC
    signature = sign_data(authentication_key, encrypted_payload)

    # Combine encrypted payload and signature into one string
    result = {
        "data": encrypted_payload,
        "signature": signature
    }

    # Base64 encode the final result
    final_result = base64.b64encode(json.dumps(result).encode()).decode('utf-8')

    return final_result

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

    print(f"Encrypted and Signed Payload (Base64): {encrypted_signed_payload}")
