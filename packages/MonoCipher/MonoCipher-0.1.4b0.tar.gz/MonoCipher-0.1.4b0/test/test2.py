# cli_test.py → Test Passed ✔
# loction → c:/Users/Akash kanna/OneDrive/Desktop/MonoCipher/MonoCipher/Test/test2.py

import sys
import os
import colorama
from colorama import Fore

colorama.init(autoreset=True)
red = Fore.RED
green = Fore.GREEN
reset = Fore.RESET

# Add the parent directory of MonoCipher to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you can perform relative imports
try:
    from MonoCipher.HmacEncryption import hmac_encrypt, hmac_decrypt
    from MonoCipher.NonceEncryption import nonce_encrypt, nonce_decrypt
    from MonoCipher.MacEncryption import mac_encrypt, mac_decrypt

except Exception:
    from HmacEncryption import hmac_encrypt, hmac_decrypt
    from NonceEncryption import nonce_encrypt, nonce_decrypt
    from MacEncryption import mac_encrypt, mac_decrypt

def test_hmac_cipher():
    message = "Hello, World!"
    password = "MySecretPassword"

    # Test HMAC encryption and decryption
    salt, iv, ciphertext, hmac_digest = hmac_encrypt(message, password)
    decrypted_message = hmac_decrypt(salt, iv, ciphertext, hmac_digest, password)
    assert decrypted_message == message, "HMAC encryption/decryption failed"
    print(green+"HMAC cipher test passed ✔"+reset)

def test_nonce_cipher():
    message = "Hello, World!"
    password = "MySecretPassword"

    # Test nonce encryption and decryption
    salt, nonce, ciphertext, tag = nonce_encrypt(message, password)
    decrypted_message = nonce_decrypt(salt, nonce, ciphertext, tag, password)
    assert decrypted_message == message, "Nonce encryption/decryption failed"
    print(green+"Nonce cipher test passed ✔"+reset)

def test_mac_cipher():
    # Define test message and password
    message = "Hello, World!"
    password = "MySecretPassword"

    # Encrypt the message
    salt, nonce, ciphertext, tag = mac_encrypt(message, password)

    # Decrypt the ciphertext
    decrypted_message = mac_decrypt(salt, nonce, ciphertext, tag, password)

    # Check if decryption was successful
    assert decrypted_message == message, "Mac encryption/decryption failed"

    print(green+"Mac cipher test passed ✔"+reset)


