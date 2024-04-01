import os
import sys
import subprocess
import time
import click
import colorama
from colorama import Fore

# ENCRYPTION MODULES
from MonoCipher.ByteEncryption import byte_encrypt, byte_decrypt # ..checked
from MonoCipher.HmacEncryption import hmac_encrypt, hmac_decrypt # ..checked
from MonoCipher.MacEncryption import mac_encrypt, mac_decrypt # ..checked
from MonoCipher.NonceEncryption import nonce_encrypt, nonce_decrypt # ..checked
from MonoCipher.SaltEncryption import salt_encrypt, salt_decrypt # ..checked
from MonoCipher.SimpleEncryption import shift_encrypt, shift_decrypt # ..checked


# VERSION
VERSION = 'v0.1.4 beta'

# COLORAMA
colorama.init(autoreset=True)
red = Fore.RED
green = Fore.GREEN
blue = Fore.BLUE
yellow = Fore.YELLOW
magenta = Fore.MAGENTA
cyan = Fore.CYAN
reset = Fore.RESET
lit_red = Fore.LIGHTRED_EX


# ERROR MESSAGE
sh_er = 'Shift value must be between 0 and 1000'
com_er = 'Make sure your decryption values are correct → '


# CONSTANTS
cl = f'{blue}MC>>{reset} ' # command line = cl

en = f'{cl}Enter the Massage you want to encrypt ' # encrypt = en
enh = 'Message you want to encrypt' # encrypt help = enh

de = f'{cl}Enter the Message you want to decrypt ' # decrypt = de
deh = 'Message you want to decrypt' # decrypt help = deh

pw = f'{cl}Enter the password ' # password = pw
pwh = 'Password to encrypt/decrypt' # password help = pwh

ivp = f'{cl}Enter the initialization vector ' # iv = ivv
ivh = 'The initialization vector used for encryption/decryption' # iv help = ivh

ch = f'{cl}Enter the ciphertext '
chh = 'Ciphertext to decrypt'

sa = f'{cl}Enter the salt value '
sah = 'Salt value used for encryption/decryption'

hm = f'{cl}Enter the Hmac value'
hmh = 'Hmac value used for encryption/decryption'

no = f'{cl}Enter the nonce value'
noh = 'Nonce value used for encryption/decryption'

ta = f'{cl}Enter the tag value'
tah = 'Tag value used for encryption/decryption'


# TITLE
title = f'\n\t{blue}MonoCipher CLI {green}{VERSION}{reset}\n'


# PROGRESS BAR
def progress_bar(progress, length=50, symbol='█', empty_symbol='-', color_on_completion=green):
    filled_length = int(length * progress)
    bar = symbol * filled_length + empty_symbol * (length - filled_length)
    color = color_on_completion if progress == 1 else ''
    print(f'|{color}{bar}{reset}| {progress:.1%}', end='\r')


# GROUP
@click.group()
def mc_cli():
    print(title)
    pass


# SHIFT ENCRYPTION
@click.command()
@click.option('--message', '-m', prompt= en, help= enh, type=str)
@click.option('--shift', '-s', prompt='Enter the shift value', help='Shift value to encrypt', type=int)
def ShiftEncrypt(message, shift):
    msg = shift_encrypt(message, shift)
    if msg == sh_er:
        print(f'{cl}{red}{sh_er}{reset}')
    else:
        print(f'{cl}{green}The Encrypted Message is : {cyan}{msg}{reset}')


# SHIFT DECRYPTION
@click.command()
@click.option('--encrypted-message', '-m', prompt=de, help=enh, type=str)
@click.option('--shift', '-s', prompt='Enter the shift value', help='Shift value to decrypt', type=int)
def ShiftDecrypt(encrypted_message, shift):
    try:
        msg = shift_decrypt(encrypted_message, shift)
        if msg == sh_er:
            print(f'{cl}{red}{sh_er}{reset}')
        else:
            print(f'{cl}{green}The Decrypted Message is : {cyan}{msg}{reset}')
    except Exception as e:
        print(f'{cl}{red}{com_er}{e}{reset}')


# BYTE ENCRYPTION
@click.command()
@click.option('--message', '-m', prompt=en, help=enh, type=str)
@click.option('--password', '-p', prompt=pw, help=pwh)
def ByteEncrypt(message, password):
    key_length = 16  # AES key length (in bytes)
    if len(password) > key_length:
        password = password[:key_length]  # Truncate if too long
    elif len(password) < key_length:
        password = password.ljust(key_length, '0')  # Pad with zeros if too short

    iv, ciphertext = byte_encrypt(message, password)
    print(f'{cl}The Encrypted Values')
    print(f'{cl}{green}IV : {cyan}{iv}{reset}')
    print(f'{cl}{green}Ciphertext : {cyan}{ciphertext}{reset}')


# BYTE DECRYPTION
@click.command()
@click.option('--iv', '-v', prompt= ivp, help= ivh, type=str)
@click.option('--ciphertext', '-c', prompt=ch, help=chh, type=str)
@click.option('--password', '-p', prompt=pw, help=pwh)
def ByteDecrypt(iv, ciphertext, password):
    key_length = 16  # AES key length (in bytes)
    try:
        if len(password) > key_length:
            password = password[:key_length]  # Truncate if too long
        elif len(password) < key_length:
            password = password.ljust(key_length, '0')  # Pad with zeros if too short

        decrypted_message = byte_decrypt(iv, ciphertext, password)
        print(f'{cl}{green}Decrypted Message: {cyan}{decrypted_message}{reset}')

    except Exception as e:
        print(f'{cl}{red}{com_er}{e}{reset}')


# SALT ENCRYPTION
@click.command()
@click.option('--message', '-m', prompt=en, help=enh, type=str)
@click.option('--password', '-p', prompt=pw, help=pwh)
def SaltEncrypt(message, password):
    salt, iv, ciphertext = salt_encrypt(message, password)
    print(f'{cl}The Encrypted Values')
    print(f'{cl}{green}Salt : {cyan}{salt}{reset}')
    print(f'{cl}{green}IV : {cyan}{iv}{reset}')
    print(f'{cl}{green}Ciphertext : {cyan}{ciphertext}{reset}')


# SALT DECRYPTION
@click.command()
@click.option('--salt', '-s', prompt=sa, help=sah, type=str)
@click.option('--iv', '-v', prompt=ivp, help=ivh, type=str)
@click.option('--ciphertext', '-c', prompt=ch, help=chh, type=str)
@click.option('--password', '-p', prompt=pw, help=pwh)
def SaltDecrypt(salt, iv, ciphertext, password):
    try:
        decrypted_message = salt_decrypt(salt, iv, ciphertext, password)
        print(f'{cl}{green}Decrypted Message: {cyan}{decrypted_message}{reset}')
    except Exception as e:
        print(f'{cl}{red}{com_er}{e}{reset}')


# HMAC ENCRYPTION
@click.command()
@click.option('--message', '-m', prompt=en, help=enh, type=str)
@click.option('--password', '-p', prompt=pw, help=pwh)
def HmacEncrypt(message, password):
    salt, iv, ciphertext, hmac_digest = hmac_encrypt(message, password)
    print(f'{cl}The Encrypted Values')
    print(f'{cl}{green}Salt : {cyan}{salt}{reset}')
    print(f'{cl}{green}IV : {cyan}{iv}{reset}')
    print(f'{cl}{green}Ciphertext : {cyan}{ciphertext}{reset}')
    print(f'{cl}{green}HMAC Digest : {cyan}{hmac_digest}{reset}')


# HMAC DECRYPTION
@click.command()
@click.option('--salt', '-s', prompt=sa, help=sah, type=str)
@click.option('--iv', '-v', prompt=ivp, help=ivh, type=str)
@click.option('--ciphertext', '-c', prompt=ch, help=chh, type=str)
@click.option('--hmac', '-h', prompt=hm, help=hmh, type=str)
@click.option('--password', '-p', prompt=pw, help=pwh)
def HmacDecrypt(salt, iv, ciphertext, hmac, password):
    try:
        decrypted_message = hmac_decrypt(salt, iv, ciphertext, hmac, password)
        print(f'{cl}{green}Decrypted Message: {cyan}{decrypted_message}{reset}')
    except Exception as e:
        print(f'{cl}{red}{com_er}{e}{reset}')


# MAC ENCRYPTION
@click.command()
@click.option('--message', '-m', prompt=en, help=enh, type=str)
@click.option('--password', '-p', prompt=pw, help=pwh)
def MacEncrypt(message, password):
    salt, nonce, ciphertext, tag = mac_encrypt(message, password)
    print(f'{cl}The Encrypted Values')
    print(f'{cl}{green}Salt: {cyan}{salt}{reset}')
    print(f'{cl}{green}Nonce: {cyan}{nonce}{reset}')
    print(f'{cl}{green}Ciphertext: {cyan}{ciphertext}{reset}')
    print(f'{cl}{green}Tag: {cyan}{tag}{reset}')


# MAC DECRYPTION
@click.command()
@click.option('--salt', '-s', prompt=sa, help=sah, type=str)
@click.option('--nonce', '-n', prompt=no, help=noh, type=str)
@click.option('--ciphertext', '-c', prompt=ch, help=chh, type=str)
@click.option('--tag', '-t', prompt=ta, help=tah, type=str)
@click.option('--password', '-p', prompt=pw, help=pwh)  
def MacDecrypt(salt, nonce, ciphertext, tag, password):
    try:
        decrypted_message = mac_decrypt(salt, nonce, ciphertext, tag, password)
        print(f'{cl}{green}Decrypted message: {cyan}{decrypted_message}{reset}' )

    except Exception as e:
        print(f'{cl}{red}{com_er}{e}{reset}')


# NONCE ENCRYPTION
@click.command()
@click.option('--message', '-m', prompt=en, help=enh, type=str)
@click.option('--password', '-p', prompt=pw, help=pwh)
def NonceEncrypt(message, password):
    salt, nonce, ciphertext, tag = nonce_encrypt(message, password)
    print(f'{cl}The Encrypted Values')
    print(f'{cl}{green}Salt: {cyan}{salt}{reset}')
    print(f'{cl}{green}Nonce: {cyan}{nonce}{reset}')
    print(f'{cl}{green}Ciphertext: {cyan}{ciphertext}{reset}')
    print(f'{cl}{green}Tag: {cyan}{tag}{reset}')


# NONCE DECRYPTION
@click.command()
@click.option('--salt', '-s', prompt=sa, help=sah, type=str)
@click.option('--nonce', '-n', prompt=no, help=noh, type=str)
@click.option('--ciphertext', '-c', prompt=ch, help=chh, type=str)
@click.option('--tag', '-t', prompt=ta, help=tah, type=str)
@click.option('--password', '-p', prompt=pw, help=pwh)
def NonceDecrypt(salt, nonce, ciphertext, tag, password):
    try:
        decrypted_message = nonce_decrypt(salt, nonce, ciphertext, tag, password)
        print(f'{cl}{green}Decrypted message: {cyan}{decrypted_message}{reset}')
    except Exception as e:
        print(f'{cl}{red}{com_er}{e}{reset}')


# UPDATE
@click.command()
def update():
    try:
        # Suppress stdout and stderr to hide pip upgrade messages
        with open(os.devnull, "w") as devnull:
            # Execute pip upgrade command and suppress output
            subprocess.check_call(["pip", "install", "--upgrade", "MonoCipher"], stdout=devnull, stderr=subprocess.STDOUT)

        for i in range(101):
            progress = i / 100
            progress_bar(progress)
            time.sleep(0.01)  # Simulate some processing time
          
        print(f'\n\n\t{green}Updated Successfully ✔{reset}\n')
    except Exception as e:
        print(f'{cl}{red}{com_er}{e}{reset}')


# COMMANDS
mc_cli.add_command(ShiftEncrypt)
mc_cli.add_command(ShiftDecrypt)

mc_cli.add_command(ByteEncrypt)
mc_cli.add_command(ByteDecrypt)

mc_cli.add_command(SaltEncrypt)
mc_cli.add_command(SaltDecrypt)

mc_cli.add_command(HmacEncrypt)
mc_cli.add_command(HmacDecrypt)

mc_cli.add_command(MacEncrypt)
mc_cli.add_command(MacDecrypt)

mc_cli.add_command(NonceEncrypt)
mc_cli.add_command(NonceDecrypt)   

mc_cli.add_command(update)
