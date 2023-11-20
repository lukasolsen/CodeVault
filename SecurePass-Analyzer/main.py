import argparse
import os
from pathlib import Path
import requests
import json
from service.messages import load_messages

from service.generator import generate_password
from analyzer import PasswordAnalyzer
from service.paths import Windows_Paths
from datetime import datetime

try:
    from termcolor import colored
except ImportError:
    os.system("pip install termcolor")
    try:
        from termcolor import colored
    except ImportError:
        print("Error: Failed to install termcolor")
        exit()


def check_messages(path):
    os.makedirs(path, exist_ok=True)

    with open(path + "messages.json", "w+") as f:
        jsonData = {
            "description": "SecurePass-Analyzer is a password analyzer that analyzes the strength of a password and gives suggestions for improvement.",

            "loaded_wordlist": "[SecurePass-Analyzer] Loaded wordlist: '{wordlist}' from '{path}'",
            "error_loading_wordlist": "[SecurePass-Analyzer] Error: Could not load wordlist: '{wordlist}' from '{path}'",
            "downloading_wordlist": "[SecurePass-Analyzer] Downloading wordlist: '{wordlist}' from '{url}'",
            "error_downloading_wordlist": "[SecurePass-Analyzer] Error: Could not download wordlist: '{wordlist}' from '{url}'",
            "wordlist_downloaded": "[SecurePass-Analyzer] Wordlist: '{wordlist}' downloaded to '{path}'",

            "generating_report": "[SecurePass-Analyzer] Generating report for password: '{password}'",
            "report_generated": "[SecurePass-Analyzer] Report generated for password: '{password}' - {timestamp}",
            "error_generating_report": "[SecurePass-Analyzer] Error: Could not generate report for password: '{password}'",

            "generating_password": "[SecurePass-Analyzer] Generating password with the following options: {options}",
            "password_generated": "[SecurePass-Analyzer] Password generated: '{password}'",
            "error_generating_password": "[SecurePass-Analyzer] Error: Could not generate password",
        }

        f.write(json.dumps(jsonData, indent=2))


def checker(os_type):
    # Check if windows first..
    wordlists = ["https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt",
                 "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt"]

    if os_type == 'nt':
        if not Path(Windows_Paths.get("messages")).exists():

            check_messages(Windows_Paths.get("messages"))

        if not Path(Windows_Paths.get('wordlist')).exists():
            messages = load_messages()

            os.makedirs(Windows_Paths.get('wordlist'), exist_ok=True)

            for wordlist_url in wordlists:
                wordlist_save_path = Windows_Paths.get(
                    'wordlist') + wordlist_url.split("/")[-1]

                print(colored(messages.get("downloading_wordlist").format(
                    wordlist=wordlist_url.split("/")[-1], url=wordlist_url
                ), 'yellow'))
                response = requests.get(wordlist_url)

                with open(wordlist_save_path, 'wb') as file:
                    try:
                        file.write(response.content)
                        print(colored(messages.get("wordlist_downloaded").format(
                            wordlist=wordlist_url.split(
                                "/")[-1], path=wordlist_save_path
                        ), 'green'))
                    except:
                        print(colored(messages.get("error_downloading_wordlist").format(
                            wordlist=wordlist_url.split(
                                "/")[-1], url=wordlist_url
                        ), 'red'))


class SecurePass:
    def __init__(self) -> None:
        # Load required things. Check if we have the required things to run.
        checker(os.name)

    def create_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            add_help=True, usage="securepassanalyzer [options]", epilog="Use 'cryptoguard --help' for usage information.", formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument('-v', '--version', action='store_true',
                            help="Show version number and exit")

        parser.add_argument('-o', '--output',
                            help="Output the results to a file")

        parser.add_argument('-a', '--analyze', action='store_true',
                            help="Analyze the password")

        parser.add_argument('-p', '--password',
                            help="The password to analyze")
        parser.add_argument('-zxcvbn', '--zxcvbn', action='store_true',
                            help="Use zxcvbn to analyze the password")

        parser.add_argument('-g', '--generate', action='store_true',
                            help="Generate a strong password based on the password provided")
        parser.add_argument('-l', '--length', type=int,
                            help="The length of the password to generate")
        parser.add_argument('-u', '--uppercase', action='store_true',
                            help="Include uppercase letters in the generated password")
        parser.add_argument('-w', '--lowercase', action='store_true',
                            help="Include lowercase letters in the generated password")
        parser.add_argument('-d', '--digits', action='store_true',
                            help="Include digits in the generated password")
        parser.add_argument('-s', '--special', action='store_true',
                            help="Include special characters in the generated password")

        return parser

    def run(self) -> None:
        parser = self.create_parser()
        args = parser.parse_args()

        if args.version:
            print(self.version())
        elif args.analyze:
            if not args.password:
                print("Error: No password provided")
                exit()
            analyzer = PasswordAnalyzer()
            results = analyzer.analyze(args.password or "", {
                "zxcvbn": args.zxcvbn or False
            })

            # Check if output is provided
            if args.output:
                # Write the results to the file
                print(colored(load_messages().get('generating_report'), 'yellow').format(
                    password=args.password
                ))
                with open(args.output, "w+") as f:
                    f.write(json.dumps(results, indent=2))

                print(colored(load_messages().get('report_generated'), 'green').format(
                    password=args.password, timestamp=datetime.now().strftime("%d/%m/%Y %H:%M:%S")

                ))
            else:
                print(colored(load_messages().get('generating_report'), 'yellow').format(
                    password=args.password
                ))

                print(colored(load_messages().get('report_generated'), 'green').format(
                    password=args.password, timestamp=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                ))
                # Print the results
                print(json.dumps(results, indent=4))

        elif args.generate:
            options = {
                "length": args.length or 14,
                "include_uppercase": args.uppercase or True,
                "include_lowercase": args.lowercase or True,
                "include_digits": args.digits or True,
                "include_special_chars": args.special or False
            }

            password = generate_password(options)

            print(f"Generated password: {password}")

    def version(self) -> str:
        return "1.0.0"


if __name__ == '__main__':
    sp = SecurePass()
    sp.run()
