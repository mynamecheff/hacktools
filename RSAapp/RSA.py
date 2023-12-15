import os
import re
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from hashlib import md5

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

from base64 import b64encode, b64decode

class Options:
    data = ""
    password = ""
    filename = "encrypt.txt"

opts = Options()

def parse_args():
    global opts
    # parse_args from go-flags is not implemented as in original go program.
    # This function is for demonstration purposes only and may need to be adjusted based on the actual use case.
    opts.data = input("Enter data for encrypt: ")
    opts.password = input("Enter password: ")

def main():
    parse_args()

    if opts.data:
        reg_str = re.compile(r'([0-9a-zA-Z]){8,}')

        if reg_str.match(opts.password):
            print("Pass ok")
            encrypt_file(opts.filename, opts.data.encode(), opts.password)
            print("Encrypt ok")
        else:
            print("Bad password\nUse a good password")
    elif opts.password:
        print(f"Decrypt:\n{decrypt_file(opts.filename, opts.password).decode()}")

def create_hash(key):
    hasher = md5()
    hasher.update(key.encode())
    return hasher.hexdigest()

def encrypt(data, passphrase):
    key = create_hash(passphrase)
    cipher = Cipher(algorithms.AES(key.encode()), modes.GCM())
    encryptor = cipher.encryptor()

    nonce = encryptor.nonce
    ciphertext = encryptor.update(data) + encryptor.finalize()

    return nonce + ciphertext

def decrypt(data, passphrase):
    key = create_hash(passphrase)
    cipher = Cipher(algorithms.AES(key.encode()), modes.GCM(iv=data[:16]))
    decryptor = cipher.decryptor()

    plaintext = decryptor.update(data[16:]) + decryptor.finalize()

    return plaintext

def encrypt_file(filename, data, passphrase):
    with open(filename, 'wb') as f:
        f.write(encrypt(data, passphrase))

def decrypt_file(filename, passphrase):
    with open(filename, 'rb') as f:
        data = f.read()
    return decrypt(data, passphrase)

if __name__ == "__main__":
    main()
