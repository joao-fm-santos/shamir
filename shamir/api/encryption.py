import base64
import hashlib

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def create_hash(value):
    sha = hashlib.sha256()
    sha.update(value.encode("utf-8"))
    sha = sha.hexdigest()
    return sha


def cipher(content, salt, mode="encrypt"):
    id = content['id'].encode("utf-8")
    secret = content['secret'].encode("utf-8")

    key_derivation_function = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=10000
    )
    key = base64.urlsafe_b64encode(key_derivation_function.derive(id))
    fernet = Fernet(key)

    if mode == 'encrypt':
        encrypted = fernet.encrypt(secret)
        return encrypted.decode('utf-8')

    elif mode == 'decrypt':
        decrypted = fernet.decrypt(secret)
        return decrypted.decode('utf-8')

