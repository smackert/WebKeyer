from cryptography.fernet import Fernet
import hashlib
import os
from pathlib import Path
import base64
import logging
import sys


def encrypt(password, input_file, output_path):
    # Generate Salt
    salt = os.urandom(16)

    # Generate Key
    key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)

    # Create Fernet object
    # Fernet key must be 32 url-safe base64-encoded bytes.
    key = base64.b64encode(key)
    f = Fernet(key)

    # Encrypt file
    try:
        with input_file.open("rb") as f_in:
            try:
                enc_d = f.encrypt(f_in.read())
            except Exception as e:
                sys.exit(f"Failed to encrypt data.\n{e}")
    except:
        sys.exit(f"Failed to open input file: {input_file}\n")

    # Write file
    try:
        with output_path.open("wb") as f_out:
            f_out.write(salt)
            f_out.write(enc_d)
    except Exception as e:
        print(f"Failed to write output file: {e}")
