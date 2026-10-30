import base64
from cryptography.fernet import Fernet


class TokenEncryptor:
    def __init__(self, key: str):
        material = (key.encode('utf-8') + b'0' * 32)[:32]
        self.fernet = Fernet(base64.urlsafe_b64encode(material))

    def encrypt(self, value: str) -> str:
        return self.fernet.encrypt(value.encode('utf-8')).decode('utf-8')

    def decrypt(self, value: str) -> str:
        return self.fernet.decrypt(value.encode('utf-8')).decode('utf-8')
