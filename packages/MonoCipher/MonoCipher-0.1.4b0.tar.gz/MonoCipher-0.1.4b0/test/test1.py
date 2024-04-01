# test1.py → Test Passed ✔
# loction → c:/Users/Akash kanna/OneDrive/Desktop/MonoCipher/MonoCipher/Test/test1.py

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
    from MonoCipher.SimpleEncryption import shift_encrypt, shift_decrypt
    from MonoCipher.ByteEncryption import byte_encrypt, byte_decrypt
    from MonoCipher.SaltEncryption import salt_encrypt, salt_decrypt

except Exception:
    from SimpleEncryption import shift_encrypt, shift_decrypt
    from ByteEncryption import byte_encrypt, byte_decrypt
    from SaltEncryption import salt_encrypt, salt_decrypt


def test_shift_cipher():
    message = "Hello, World!"
    shift = 3

    # Test shift encryption and decryption
    encrypted_message = shift_encrypt(message, shift)
    decrypted_message = shift_decrypt(encrypted_message, shift)
    assert decrypted_message == message, "Shift encryption/decryption failed"
    print(green+"Shift cipher test passed ✔"+reset)

def test_byte_cipher():
    message = "Hello, World!"
    password = "MySecretPassword"

    # Test byte encryption and decryption
    iv, ciphertext = byte_encrypt(message, password)
    decrypted_message = byte_decrypt(iv, ciphertext, password)
    assert decrypted_message == message, "Byte encryption/decryption failed"
    print(green+"Byte cipher test passed ✔"+reset)

def test_salt_cipher():
    message = "Hello, World!"
    password = "MySecretPassword"

    # Test salt encryption and decryption
    salt, iv, ciphertext = salt_encrypt(message, password)
    decrypted_message = salt_decrypt(salt, iv, ciphertext, password)
    assert decrypted_message == message, "Salt encryption/decryption failed"
    print(green+"Salt cipher test passed ✔"+reset)


