import pytest
import shutil
import os
from pathlib import Path
from hashlib import sha256
from encrypt import encrypt
from cryptography.fernet import Fernet
import hashlib
import base64
import random
from random import randint
import string


@pytest.fixture
def password():
    pass_len = randint(0, 20)
    chars = string.printable
    return "".join((random.choice(chars) for x in range(pass_len)))


def decrypt(password, encrypted_data):
    salt_len = 16
    salt = encrypted_data[:salt_len]
    key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
    key = base64.b64encode(key)
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_data[16:])


def read_file(file_path):
    with file_path.open("rb") as f:
        return f.read()


def test_successful_encrypt(password):
    input_file = Path("./tests/test-data/tmp/test-input.bin")
    output_path = Path("./tests/test-data/tmp/test-input.bin.wbkr")

    # Create the parent directory `tmp` if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Create input file
    with input_file.open("wb") as f:
        input_data = os.urandom(randint(90000, 150000))
        f.write(input_data)

    # Act
    # Call the tested function
    encrypt(password, input_file, output_path)

    # Get contents of encrypted file
    encrypted_data = read_file(output_path)

    # Get contents of decrypted file
    decrypted_data = decrypt(password, encrypted_data)

    # Assert
    # Assert file was created and not empty
    assert output_path.exists()
    assert output_path.stat().st_size > 0

    # Assert output file is not same as input file
    assert input_data != encrypted_data

    # Assert decrypted output is same as input
    assert decrypted_data == input_data


@pytest.fixture(autouse=True)
def cleanup_files(request):
    """
    Cleanup test files after running the tests.
    """

    def fin():
        # Delete the tmp directory
        shutil.rmtree("./tests/test-data/tmp")

    request.addfinalizer(fin)
