import os
import subprocess
import hashlib
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def encrypt(data, key):
    cipher = Cipher(algorithms.AES(key), modes.GCM())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(data) + encryptor.finalize()
    return encryptor.nonce + ciphertext + encryptor.tag

def encrypt_file(filename, data, key):
    with open(filename, 'wb') as f:
        f.write(encrypt(data, key))

def is_dir(name):
    return os.path.isdir(name)

def decrypt(data, key):
    nonce = data[:12]
    ciphertext = data[12:-16]
    tag = data[-16:]
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize_with_tag(tag)

def decrypt_file(filename, key):
    with open(filename, 'rb') as f:
        encrypted_data = f.read()
    decrypted_data = decrypt(encrypted_data, key)
    with open(filename[:-4], 'wb') as f:
        f.write(decrypted_data)

def crypto_dir(directory, key):
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            print(f'Encrypting {filename}')
            with open(file_path, 'rb') as f:
                file_data = f.read()
            encrypt_file(file_path + ".crp", file_data, key)
            os.remove(file_path)

def decrypt_file_save(key, directory):
    save_file = f'''\
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def decrypt(data, key):
    nonce = data[:12]
    ciphertext = data[12:-16]
    tag = data[-16:]
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize_with_tag(tag)

def decrypt_file(filename, key):
    with open(filename, 'rb') as f:
        encrypted_data = f.read()
    decrypted_data = decrypt(encrypted_data, key)
    with open(filename[:-4], 'wb') as f:
        f.write(decrypted_data)

key = {key}
directory = {directory}

for dirpath, dirnames, filenames in os.walk(directory):
    for filename in filenames:
        file_path = os.path.join(dirpath, filename)
        print(f'Decrypting {decrypt}')
        decrypt_file(file_path, key)
        os.remove(file_path)
'''

    with open('./decrypt.py', 'w') as f:
        f.write(save_file)

def build_decrypt_file():
    subprocess.run(['python', '-m', 'py_compile', 'decrypt.py'])
    os.remove('decrypt.py')

if __name__ == '__main__':
    directory = input('Write the folder for encryption: ')
    if not is_dir(directory):
        print("It's not a directory")
        exit(1)
    else:
        print('Directory ok')

    key = input('Write the password: ')
    if len(key) < 8:
        print('Bad password\nUse a password with at least 8 characters')
        exit(1)

    # get the hash
    hasher = hashlib.md5()
    hasher.update(key.encode())
    key_hash = hasher.digest()

    decrypt_file_save(key_hash, directory)

    print("-----------------------------------------------------------")

    crypto_dir(directory, key_hash)

    import time
    time.sleep(2)

    build_decrypt_file()
