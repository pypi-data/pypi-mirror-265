from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
import base64

def derive_master_key(password, salt):
    return scrypt(password.encode(), salt, key_len=32, N=2**20, r=8, p=1)

def generate_nonce():
    return get_random_bytes(12)

def mac_encrypt(message, password):
    salt = get_random_bytes(16)
    nonce = generate_nonce()
    master_key = derive_master_key(password, salt)
    cipher = AES.new(master_key, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode())
    return base64.b64encode(salt).decode('utf-8'), base64.b64encode(nonce).decode('utf-8'), \
           base64.b64encode(ciphertext).decode('utf-8'), base64.b64encode(tag).decode('utf-8')

def mac_decrypt(salt, nonce, ciphertext, tag, password):
    salt = base64.b64decode(salt)
    nonce = base64.b64decode(nonce)
    ciphertext = base64.b64decode(ciphertext)
    tag = base64.b64decode(tag)
    master_key = derive_master_key(password, salt)
    cipher = AES.new(master_key, AES.MODE_GCM, nonce=nonce)
    try:
        decrypted_message = cipher.decrypt_and_verify(ciphertext, tag).decode()
        return decrypted_message
    except ValueError:
        return "Decryption failed: MAC check failed"

'''

# Example usage:
password = "MySecretPassword"
message = "Hello, World!"

# Encryption
salt, nonce, ciphertext, tag = mac_encrypt(message, password)
print("Salt:", salt)
print("Nonce:", nonce)
print("Ciphertext:", ciphertext)
print("Tag:", tag)

# Decryption
decrypted_message = mac_decrypt(salt, nonce, ciphertext, tag, password)
print("Decrypted message:", decrypted_message)
'''