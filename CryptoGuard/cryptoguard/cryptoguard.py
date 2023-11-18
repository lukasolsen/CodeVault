import os
import argparse

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


class CryptoGuard:
    """CryptoGuard main class"""

    def __init__(self) -> None:
        self.encryption = Encryption()

    def run(self) -> None:
        """Run CryptoGuard with arguments"""
        parser = self.create_parser()
        args = parser.parse_args()

        if args.version:
            self.version()
        elif args.encrypt:
            self.encrypt(args.file, args.key, args.algorithm,
                         args.output, args.replace)
        elif args.decrypt:
            self.decrypt(args.file, args.key, args.algorithm)
        elif args.detect:
            self.detect(args.file)
        else:
            parser.print_help()

    def create_parser(self) -> argparse.ArgumentParser:
        """Create parser for CryptoGuard"""
        parser = argparse.ArgumentParser(
            description=messages.get('description'), add_help=True, usage="cryptoguard [options] <file>", epilog="Use 'cryptoguard --help' for usage information.", formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument('-v', '--version', action='store_true',
                            help="Show version number and exit")
        parser.add_argument('-e', '--encrypt',
                            action='store_true', help="Encrypt file")
        parser.add_argument('-d', '--decrypt',
                            action='store_true', help="Decrypt file")
        parser.add_argument(
            '-k', '--key', help="The key to use for encryption/decryption")
        parser.add_argument(
            '-det', '--detect', action='store_true', help="Detect encryption algorithm")
        parser.add_argument('-algo', '--algorithm',
                            help="Choose encryption algorithm")
        parser.add_argument('file', help="File to be encrypted/decrypted")
        parser.add_argument('-o', '--output',
                            help="Return output")
        parser.add_argument('-r', '--replace', action='store_true',
                            help="Replace original file")

        return parser

    def encrypt(self, file_path, key, algorithm, output, replace) -> None:
        """Encrypt file"""
        if not os.path.isfile(file_path):
            print(colored(messages.get('file_not_found'), 'red'))
            return

        self.encryption.encrypt(
            file_path, algorithm or 'aes', key or 'secret', output=output, replace=replace)

    def decrypt(self, file_path, key: bytes, algorithm) -> None:
        """Decrypt file"""
        if not os.path.isfile(file_path):
            print(colored(messages.get('file_not_found'), 'red'))
            return

        if not key:
            print(colored(messages.get('key_not_provided'), 'red'))
            return

        self.encryption.decrypt(
            file_path, algorithm or 'aes', key)

    def detect(self, file_path) -> None:
        """Detect encryption algorithm"""
        if not os.path.isfile(file_path):
            print(colored(messages.get('file_not_found'), 'red'))
            return

        print(self.encryption.detectMethod(file_path))


if __name__ == '__main__':
    cg = CryptoGuard()
    cg.run()
