from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64

def extract_iv_and_ciphertext(encrypted_data):
    """
    Extract the IV and ciphertext from the encrypted data.
    
    Args:
        encrypted_data (bytes): Base64 encoded encrypted data with prepended IV
        
    Returns:
        tuple: (iv, ciphertext) both as bytes
    """
    # Decode base64 if input is string
    if isinstance(encrypted_data, str):
        encrypted_data = base64.b64decode(encrypted_data)
    
    # First 16 bytes are IV
    iv = encrypted_data[:16]
    # Rest is ciphertext
    ciphertext = encrypted_data[16:]
    
    return iv, ciphertext

def decrypt(encrypted_data, key):
    """
    Decrypt data that was encrypted using Salesforce's encryptManagedIV with AES-128-CBC.
    
    Args:
        encrypted_data (str): Base64 encoded encrypted data with prepended IV
        key (bytes or str): 16-byte (128-bit) key in bytes or hex string
        
    Returns:
        str: Decrypted text
    """
    try:
        # Convert key to bytes if it's a hex string
        if isinstance(key, str):
            key = bytes.fromhex(key)
            
        # Verify key length
        if len(key) != 16:
            raise ValueError("Key must be exactly 16 bytes (128 bits) long")
            
        # Extract IV and ciphertext
        iv, ciphertext = extract_iv_and_ciphertext(encrypted_data)
        
        # Create cipher
        cipher = Cipher(
            algorithms.AES128(key),
            modes.CBC(iv),
            backend=default_backend()
        )
        
        # Create decryptor
        decryptor = cipher.decryptor()
        
        # Decrypt the data
        decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()
        
        # Remove PKCS7 padding
        padding_length = decrypted_padded[-1]
        decrypted = decrypted_padded[:-padding_length]
        
        # Convert to string
        return decrypted.decode('utf-8')
        
    except Exception as e:
        print(f"Decryption failed: {str(e)}")
        raise

# Example usage:
'''
try:
    # Your encrypted data (base64 string)
    encrypted_data = "your-base64-encrypted-data"
    
    # Your 16-byte key (either as hex string or bytes)
    key = "your-32-character-hex-string"  # 16 bytes = 32 hex characters
    # OR
    # key = b'your-16-byte-key'
    
    decrypted_text = decrypt(encrypted_data, key)
    print("Decrypted:", decrypted_text)
    
except Exception as e:
    print("Error:", str(e))
'''