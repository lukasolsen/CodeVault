import os

try:
    from termcolor import colored
except ImportError:
    os.system("pip install termcolor")
    try:
        from termcolor import colored
    except ImportError:
        print("Error: Failed to install termcolor")
        exit()

from modules.encryption import Encryption
from utils.messages import messages


class Runner:
    """Include all the main functions of CryptoGuard, this is the middleware."""

    def __init__(self) -> None:
        self.encryption = Encryption()

    def encrypt(self, file_path, key, algorithm, options) -> None:
        """Encrypt file"""
        if not os.path.isfile(file_path):
            if options.get('verbose'):
                print(colored(messages.get('file_not_found'), 'red'))
            return

        if not key:
            if options.get('verbose'):
                print(colored(messages.get('default_key'), 'yellow'))

        self.encryption.encrypt(
            file_path, algorithm or 'aes', key or 'secret', replace=options.get('replace'), verbose=options.get('verbose'))

    def decrypt(self, file_path, key: bytes, algorithm, options) -> None:
        """Decrypt file"""
        if not os.path.isfile(file_path):
            if options.get('verbose'):
                print(colored(messages.get('file_not_found'), 'red'))
            return

        if not key:
            if options.get('verbose'):
                print(colored(messages.get('key_not_provided'), 'red'))
            return

        self.encryption.decrypt(
            file_path, algorithm or 'aes', key, verbose=options.get('verbose'))

    def detect(self, file_path) -> None:
        """Detect encryption algorithm"""
        if not os.path.isfile(file_path):
            print(colored(messages.get('file_not_found'), 'red'))
            return

        print(self.encryption.detectMethod(file_path))
