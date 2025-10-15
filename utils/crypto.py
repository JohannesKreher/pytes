from cryptography.fernet import Fernet

def decrypt_db(db_path, key: str):
    f = Fernet(key)
    with open(db_path, "rb") as file:
        file_data = file.read()
        encrypt_data = f.decrypt(file_data)
        file.write(encrypt_data)

def encrypt_db(db_path, key: str):
    f = Fernet(key)
    with open(db_path, "rb") as file:
        file_data = file.read()
        encrypt_data = f.encrypt(file_data)
        file.write(encrypt_data)
