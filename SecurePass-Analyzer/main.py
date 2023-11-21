import argparse
import os
from pathlib import Path
import requests
import json

from service.generator import generate_password
from analyzer import PasswordAnalyzer
from service.paths import Windows_Paths
from datetime import datetime

from manager.logger import Logger


def checker(os_type):
    wordlists = ["https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt",
                 "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt"]

    if os_type == 'nt':
        if not Path(Windows_Paths.get('wordlist')).exists():
            os.makedirs(Windows_Paths.get('wordlist'), exist_ok=True)

            for wordlist_url in wordlists:
                wordlist_save_path = Windows_Paths.get(
                    'wordlist') + wordlist_url.split("/")[-1]

                # print(colored(messages.get("downloading_wordlist").format(
                #     wordlist=wordlist_url.split("/")[-1], url=wordlist_url
                # ), 'yellow'))
                Logger().log("downloading_wordlist", {"wordlist": wordlist_url.split(
                    "/")[-1], "url": wordlist_url})

                response = requests.get(wordlist_url)

                with open(wordlist_save_path, 'wb') as file:
                    try:
                        file.write(response.content)
                        Logger().log("wordlist_downloaded", {"wordlist": wordlist_url.split(
                            "/")[-1], "path": wordlist_save_path})
                    except:
                        Logger().log("error_downloading_wordlist", {"wordlist": wordlist_url.split(
                            "/")[-1], "url": wordlist_url})


class SecurePass:
    def __init__(self) -> None:
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

            if args.output:
                Logger().log("generating_report", {"password": args.password})

                with open(args.output, "w+") as f:
                    f.write(json.dumps(results, indent=2))
                Logger().log("report_generated", {
                    "password": args.password, "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S")})
            else:
                Logger().log("generating_report", {"password": args.password})
                Logger().log("report_generated", {"password": args.password, "timestamp": datetime.now().strftime(
                    "%d/%m/%Y %H:%M:%S")})
                Logger().log_json(results)

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
