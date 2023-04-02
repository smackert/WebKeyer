from cryptography.fernet import Fernet
import hashlib
import os
import getpass
import web
import logging

password = ''



def encrypt(password, input_file, output_path):
    
    # Generate Salt
    salt = os.urandom(16)
    # Generate Key
    key = hashlib.pbkdf2_hmac('sha256', password, salt, 100000)

    # Create Fernet object
    f = Fernet(key)

    # Encrypt file
    try:
        with open(input_file, 'rb') as f_in:
            enc_d = f.encrypt(f_in.read())
    except:
        print("Failed to open input file.")
    try:
        with open(output_path, 'rb') as f_out:
            f_out.write(len(salt))
            f_out.write(salt)
            f_out.write(enc_d)
    except:
        print("Failed to write output file.")