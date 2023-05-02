from cryptography.fernet import Fernet
from pathlib import Path
import hashlib
import base64
import logging
import sys


def decrypt(password, input_file, output_path):
    salt_length = 16
    # Grab salt from header - Fixed length (16)
    try:
        with input_file.open("rb") as f_in:
            salt = f_in.read()[:salt_length]
            logging.debug(f"Read salt: {salt}")
    except:
        sys.exit(f"Could not read salt.")

    # Generate key
    key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)

    # New Fernet obj
    # Fernet key must be 32 url-safe base64-encoded bytes.
    key = base64.b64encode(key)
    f = Fernet(key)

    # Now try to decrypt
    try:
        with input_file.open("rb") as f_in:
            try:
                # Begin reading after len(salt) = 16
                decrypted_data = f.decrypt(f_in.read()[salt_length:])
            except Exception as e:
                sys.exit(f"Failed to decrypt the input file.\n{e}")
    except Exception as e:
        sys.exit(f"Failed to read the input file.\n{e}")

    try:
        logging.debug(f"Attempting to write output file {output_path}")
        with output_path.open("wb") as f_out:
            f_out.write(decrypted_data)
    except Exception as e:
        print(f"Failed to write decrypted data: {e}")
