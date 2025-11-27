from pytes.utils.config import db_path

from cryptography.fernet import Fernet, InvalidToken
from hashlib import pbkdf2_hmac
import base64

salt = "6l6k!khlu_t6e54.?".encode('utf-8')
def do_key(password:bytes)->bytes:
    return base64.urlsafe_b64encode(pbkdf2_hmac("sha256", password, salt, 390_000, dklen=32))

def decrypt_db(password: bytes)->bool:
    key = do_key(password)
    f = Fernet(key)
    with open(db_path, "rb") as file:
        encrypt_data = file.read()
    try:
        decrypt_data = f.decrypt(encrypt_data)
    except InvalidToken:
        return False
    with open(db_path, "wb") as file:
        file.write(decrypt_data)
    return True

def encrypt_db(password: bytes):
    key = do_key(password)
    f = Fernet(key)
    with open(db_path, "rb") as file:
        file_data = file.read()
    encrypt_data = f.encrypt(file_data)
    with open(db_path, "wb") as file:
        file.write(encrypt_data)
