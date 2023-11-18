import os

try:
    from cryptography.fernet import Fernet
except ImportError:
    print("Installing Fernet dependencies")
    os.system("pip3 install cryptography")
    try:
        from cryptography.fernet import Fernet
    except ImportError:
        print("Error: Failed to install cryptography")
        exit()


class FernetMethod:
    def __init__(self):
        self.key = Fernet.generate_key()

    def encrypt(self, data: bytes, key):
        fernet = Fernet(self.key)
        return fernet.encrypt(data)

    def decrypt(self, data: bytes, key):
        fernet = Fernet(self.key)
        return fernet.decrypt(data)
