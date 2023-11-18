import argparse
from runner import Runner
from utils.messages import messages
from utils.utils import get_files_from_args


class CryptoGuard:
    def __init__(self) -> None:
        self.runner = Runner()

    def run(self) -> None:
        parser = self.create_parser()
        args = parser.parse_args()

        options = {
            "replace": args.replace or False,
            "verbose": args.verbose or False,
            "key": args.key or "secret"
        }

        if args.version:
            self.version()
        elif args.detect:
            self.runner.detect(args.file)
        else:
            files = get_files_from_args(args)
            if files:
                if args.encrypt:
                    self.runner.encrypt(files, args.algorithm, options)
                elif args.decrypt:
                    self.runner.decrypt(files, args.algorithm, options)

    def create_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            description=messages.get('description'), add_help=True, usage="cryptoguard [options] <file>", epilog="Use 'cryptoguard --help' for usage information.", formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument('-v', '--version', action='store_true',
                            help="Show version number and exit")
        parser.add_argument('-e', '--encrypt',
                            action='store_true', help="Encrypt file")
        parser.add_argument('-d', '--decrypt',
                            action='store_true', help="Decrypt file")
        parser.add_argument(
            '-det', '--detect', action='store_true', help="Detect encryption algorithm")
        parser.add_argument(
            '-k', '--key', help="The key to use for encryption/decryption")
        parser.add_argument('-algo', '--algorithm',
                            help="Choose encryption algorithm")
        parser.add_argument('-r', '--replace', action='store_true',
                            help="Replace original file")
        parser.add_argument("-V", "--verbose", action="store_true",
                            help="Increase output verbosity")
        parser.add_argument("-depth", "--depth", type=int,
                            help="Custom depth for folder encryption/decryption")
        parser.add_argument(
            'files', nargs='*', help="Files to be encrypted/decrypted")
        return parser


if __name__ == '__main__':
    cg = CryptoGuard()
    cg.run()
