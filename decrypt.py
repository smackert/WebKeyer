from cryptography.fernet import Fernet
from pathlib import Path
import hashlib
import base64

def decrypt(password, input_file, output_path):

    # Grab salt from header - Fixed length (16)
    with open(input_file, 'rb') as f_in:
        salt = f_in.read()[:16]

    # Generate key 
    key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    
    # New Fernet obj
    # Fernet key must be 32 url-safe base64-encoded bytes.
    key = base64.b64encode(key)
    f = Fernet(key)

    
    # Now try to decrypt
    try:
        with open(input_file, 'rb') as f_in:
            # Begin reading after len(salt) = 16
            f_in.seek(1 + 16) 
            decrypted_data = f.decrypt(f_in.read())
    except:
        print("Failed to read the input file.")
        
    try:
        with open(output_path, 'wb') as f_out:
            f_out.write(decrypted_data)
    except Exception as e:
        print(f'Failed to write decrypted data: {e}')