import os

try:
    from cryptography.fernet import Fernet
except ImportError:
    print("Installing Fernet dependencies")
    os.system("pip3 install cryptography")
    from cryptography.fernet import Fernet


class FernetMethod:
    def __init__(self):
        pass

    def encrypt(self, data: bytes, key):
        key = Fernet.generate_key()
        fernet = Fernet(key)
        if not os.path.exists("key.key"):
            open("key.key", 'w').close()
        with open("key.key", 'ab') as f:
            # Since we might have multiple keys already, we need to write it like this: Key (number of line): <key>
            f.write("Key ".encode() + str(len(open("key.key").readlines()) +
                    1).encode() + ": ".encode() + key + "\n".encode())
        print("Outputted key to the path: " + os.path.abspath("key.key"))
        return fernet.encrypt(data)

    def decrypt(self, data: bytes, key):
        try:
            fernet = Fernet(key)
            return fernet.decrypt(data)
        except:
            print("Error: Key is invalid")
            exit()
