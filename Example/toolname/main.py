from manager.logger import Logger
import argparse
from manager.config import get_version


class ExampleClass:
    def __init__(self) -> None:
        """
        Initialize an instance of the ExampleClass.
        """
        pass

    def create_parser(self) -> argparse.ArgumentParser:
        """
        Create the argument parser.

        Returns:
            argparse.ArgumentParser:
                An instance of the argument parser configured for the tool.
        """
        parser = argparse.ArgumentParser(
            add_help=True,
            usage="toolname [options]",
            epilog="Use 'toolname --help' for usage information.",
            formatter_class=argparse.RawTextHelpFormatter
        )

        parser.add_argument('-v', '--version', action='store_true',
                            help="Show version number and exit")

        return parser

    def run(self) -> None:
        """
        Execute the main functionality of the tool.

        Parses command-line arguments and performs the specified actions.

        Returns:
            None
        """
        parser = self.create_parser()
        args = parser.parse_args()

        if args.version:
            print(get_version())


if __name__ == "__main__":
    Logger().log_progress("progress", "Example", 100)
    ExampleClass().run()
