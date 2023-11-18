import os

from typing import List
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

    def encrypt(self, files: List[str], algorithm, options) -> None:
        """Encrypt file"""
        if not options.get("key"):
            if options.get('verbose'):
                print(colored(messages.get('default_key'), 'yellow'))

        for file_path in files:
            self.encryption.process_file(
                file_path, algorithm or 'aes', options=options, action='encrypt')

    def decrypt(self, files: List[str], algorithm, options) -> None:
        """Decrypt file"""

        if not options.get("key"):
            if options.get('verbose'):
                print(colored(messages.get('key_not_provided'), 'red'))
            return

        for file_path in files:
            self.encryption.process_file(
                file_path, algorithm or 'aes', options=options, action='decrypt')

    def detect(self, file_path) -> None:
        """Detect encryption algorithm"""
        print(self.encryption.detectMethod(file_path))
