from cryptography.fernet import Fernet
import hashlib
import os
from pathlib import Path
import base64
import logging

def encrypt(password, input_file, output_path):
    
    # Generate Salt
    salt = os.urandom(16)

    # Generate Key
    key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)

    # Create Fernet object
    # Fernet key must be 32 url-safe base64-encoded bytes.
    key = base64.b64encode(key)
    f = Fernet(key)

    # Encrypt file
    try:
        with open(input_file, 'rb') as f_in:
            enc_d = f.encrypt(f_in.read())
    except:
        print("Failed to open input file.")
    try:
        with open(output_path, 'wb') as f_out:
            f_out.write(salt)
            f_out.write(enc_d)
    except Exception as e:
        print(f"Failed to write output file: {e}")