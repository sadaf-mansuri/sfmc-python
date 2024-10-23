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



from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64

def prepare_key(key):
    """
    Convert key to correct format (16 bytes) regardless of input format.
    
    Args:
        key: Can be string, base64 string, or bytes
        
    Returns:
        bytes: 16-byte key
    """
    if isinstance(key, str):
        # If the key is base64 encoded
        try:
            key_bytes = base64.b64decode(key)
        except:
            # If not base64, encode the raw string to bytes
            key_bytes = key.encode('utf-8')
    else:
        # If already bytes
        key_bytes = key
        
    # If key is longer than 16 bytes, truncate it
    # If shorter than 16 bytes, pad it with zeros
    if len(key_bytes) > 16:
        key_bytes = key_bytes[:16]
    elif len(key_bytes) < 16:
        key_bytes = key_bytes + b'\0' * (16 - len(key_bytes))
        
    return key_bytes

def extract_iv_and_ciphertext(encrypted_data):
    """
    Extract the IV and ciphertext from the encrypted data.
    
    Args:
        encrypted_data (bytes or str): Base64 encoded encrypted data with prepended IV
        
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
        key: The encryption key (can be string, base64 string, or bytes)
        
    Returns:
        str: Decrypted text
    """
    try:
        # Prepare the key
        key_bytes = prepare_key(key)
        
        # Extract IV and ciphertext
        iv, ciphertext = extract_iv_and_ciphertext(encrypted_data)
        
        # Create cipher
        cipher = Cipher(
            algorithms.AES128(key_bytes),
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
# Example with different key formats:

# If your key is a regular string
key1 = "mySecretKey123"  # Will be encoded to bytes and padded/truncated to 16 bytes

# If your key is base64 encoded
key2 = "bXlTZWNyZXRLZXkxMjM="  # Will be decoded from base64 first

# If your key is already bytes
key3 = b"mySecretKey123"  # Will be padded/truncated to 16 bytes

try:
    encrypted_data = "your-base64-encrypted-data"
    decrypted_text = decrypt(encrypted_data, key1)  # or key2 or key3
    print("Decrypted:", decrypted_text)
except Exception as e:
    print("Error:", str(e))
'''


from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

# Convert string to bytes for key and IV
key = "your16or24or32bytekey"  # Key must be 16, 24, or 32 bytes long
iv = "your16byteIVvector"      # IV must be 16 bytes

# Ensure key and IV are bytes
key_bytes = key.encode('utf-8')  # Use utf-8 encoding to convert string to bytes
iv_bytes = iv.encode('utf-8')

# For AES encryption
cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
plain_text = "This is some plain text to encrypt"
cipher_text = cipher.encrypt(pad(plain_text.encode('utf-8'), AES.block_size))

# Encode the cipher text in base64
encoded_cipher_text = base64.b64encode(cipher_text).decode('utf-8')

print("Encrypted (Base64):", encoded_cipher_text)

# For AES decryption
cipher_text_bytes = base64.b64decode(encoded_cipher_text.encode('utf-8'))
decipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
decrypted_text = unpad(decipher.decrypt(cipher_text_bytes), AES.block_size)

print("Decrypted:", decrypted_text.decode('utf-8'))