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

from runner import Runner
from utils.messages import messages


class CryptoGuard:
    """CryptoGuard main class"""

    def __init__(self) -> None:
        self.runner = Runner()

    def run(self) -> None:
        """Run CryptoGuard with arguments"""
        parser = self.create_parser()
        args = parser.parse_args()

        options = {
            "replace": args.replace or False,
            "verbose": args.verbose or False
        }

        if args.version:
            self.version()
        elif args.encrypt:
            self.runner.encrypt(args.file, args.key, args.algorithm, options)
        elif args.decrypt:
            self.runner.decrypt(args.file, args.key, args.algorithm, options)
        elif args.detect:
            self.runner.detect(args.file)
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
        parser.add_argument('-r', '--replace', action='store_true',
                            help="Replace original file")
        parser.add_argument("-V", "--verbose", action="store_true",
                            help="Increase output verbosity")

        return parser


if __name__ == '__main__':
    cg = CryptoGuard()
    cg.run()
