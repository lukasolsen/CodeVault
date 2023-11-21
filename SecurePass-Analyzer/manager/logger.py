from rich.console import Console
from rich.markdown import Markdown
from rich.text import Text
from datetime import datetime
import os

from service.paths import Windows_Paths

from enum import Enum
import json

# Message: "[gray]Error[/gray]: {error}"


class Logger:
    _instance = None  # Singleton instance

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self) -> None:
        if not self.__initialized:
            self.generate_messages()

            self.log_to_file = False
            self.canLog_to_console = True

            self.console = Console()
            self.log_file = "securepass-" + datetime.now().strftime("%d-%m-%Y") + ".log"

            self.messages = []
            with open(Windows_Paths.get("messages") + "messages.json", 'r') as f:
                self.messages = json.load(f)

            self.prefix = "[gray][[blue]SecurePass-Analyzer[/blue]][/gray][reset] "
            self.__initialized = True

    def log(self, message: str, args: dict) -> None:
        # Log to both console and file.
        if message not in self.messages:
            self.console.print(
                self.prefix + "[red]Error[/red]: Message not found in messages.json.")
            return

        # self.log_to_file(message)
        self.log_to_console(self.messages.get(message), args)

    def log_to_console(self, message: str, args: dict) -> None:
        # Log to console.
        if self.canLog_to_console:
            self.console.print(self.prefix + message.format(**args))

    def log_success(self, message: str, *args) -> None:
        # Log a success message.
        if message not in self.messages:
            self.console.print(
                self.prefix + "[red]Error[/red]: Message not found in messages.json.")
            return

        if self.canLog_to_console:
            self.console.print(
                self.prefix + "[green]Success[/green]: " + message.format(*args))

    def log_warning(self, message: str, *args) -> None:
        # Log a warning message.
        if message not in self.messages:
            self.console.print(
                self.prefix + "[red]Error[/red]: Message not found in messages.json.")
            return

        if self.canLog_to_console:
            self.console.print(
                self.prefix + "[yellow]Warning[/yellow]: " + message.format(*args))

    def log_json(self, data: str) -> None:
        # Log a json object.
        if self.canLog_to_console:
            self.console.print_json(json.dumps(data, indent=4))

    def generate_messages(self):
        os.makedirs(Windows_Paths.get("messages"), exist_ok=True)

        # Check if the messages.json file exists.
        if not os.path.exists(Windows_Paths.get("messages") + "messages.json"):
            with open(Windows_Paths.get("messages") + "messages.json", 'w') as f:
                messages = {
                    "description": "SecurePass-Analyzer is a password analyzer that analyzes the strength of a password and gives suggestions for improvement.",

                    "loaded_wordlist": "Loaded wordlist: '{wordlist}' from '{path}'",
                    "error_loading_wordlist": "Error: Could not load wordlist: '{wordlist}' from '{path}'",
                    "downloading_wordlist": "Downloading wordlist: '{wordlist}' from '{url}'",
                    "error_downloading_wordlist": "Error: Could not download wordlist: '{wordlist}' from '{url}'",
                    "wordlist_downloaded": "Wordlist: '{wordlist}' downloaded to '{path}'",

                    "generating_report": "Generating report for password: '{password}'",
                    "report_generated": "Report generated for password: '{password}' - {timestamp}",
                    "error_generating_report": "Error: Could not generate report for password: '{password}'",

                    "generating_password": "Generating password with the following options: {options}",
                    "password_generated": "Password generated: '{password}'",
                    "error_generating_password": "Error: Could not generate password",
                }

                json.dump(messages, f, indent=4)
