from cryptography.fernet import Fernet
from Crypto.Cipher import AES
import hashlib, hmac
from functools import lru_cache

def encrypt_data(data: str) -> bytes:
    key = Fernet.generate_key()
    f = Fernet(key)
    return f.encrypt(data.encode())

@lru_cache(maxsize=32)
def hash_data(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()

if __name__ == "__main__":
    print(encrypt_data("secret"))
    print(hash_data("secret"))
