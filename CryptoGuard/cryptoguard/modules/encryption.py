import os
from utils.messages import messages
from termcolor import colored

from loaders.CustomLoader import Loader


class Encryption:
    def __init__(self):
        self.loader = Loader()

    def process_file(self, file: str, algorithm: str, options: dict, action: str) -> None:
        if action == 'encrypt':
            self.encrypt(file, algorithm, options.get('key'), options.get(
                'replace'), options.get('verbose'))

        elif action == 'decrypt':
            self.decrypt(file, algorithm, options.get(
                'key'), options.get('verbose'))

    def encrypt(self, file: str, algorithm: str, key: str, replace: bool = False, verbose: bool = True) -> None:
        method = self.loader.get_method(algorithm)

        if method is None:
            if verbose:
                print(colored(messages.get(
                    'encryption_method_not_found').format(algorithm=algorithm), 'red'))
            return

        with open(file, 'rb') as f:
            data = f.read()

        encrypted_data = method.encrypt(data, key)

        if replace:
            os.remove(file)
            with open(file, 'wb') as f:
                f.write(encrypted_data)
        else:
            with open(file + ".enc", 'wb') as f:
                f.write(encrypted_data)

        if verbose:
            print(colored(messages.get('file_encrypted'), 'green'))

    def decrypt(self, file: str, algorithm: str, key: str, verbose: bool = True) -> None:
        method = self.loader.get_method(algorithm)

        if method is None:
            if verbose:
                print(colored(messages.get(
                    'decryption_method_not_found').format(algorithm=algorithm), 'red'))
            return

        with open(file, 'rb') as f:
            encrypted_data = f.read()

        decrypted_data = method.decrypt(encrypted_data, key)

        with open(file, 'wb') as f:
            f.write(decrypted_data)

        if verbose:
            print(colored(messages.get('file_decrypted'), 'green'))

    def detect_method(self, file: str) -> dict:
        results = {
            "method": None,
            "key": None,
        }

        with open(file, 'rb') as f:
            encrypted_data = f.read()
        for method_name, method in self.loader.get_methods().items():
            try:
                decrypted_data = method.decrypt(encrypted_data, 'dummy_key')
                results["method"] = method_name
                results["key"] = 'dummy_key'
                break
            except Exception as e:
                pass

        return results
