from rich.console import Console
from rich.progress_bar import ProgressBar

from datetime import datetime
import os

from service.paths import Windows_Paths

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

    def log_progress(self, message: str, args: dict, total: int) -> ProgressBar:
        # Log a progress bar.
        if message not in self.messages:
            self.console.print(
                self.prefix + "[red]Error[/red]: Message not found in messages.json.")
            return

        if self.canLog_to_console:
            return self.console.track(
                self.prefix + message.format(**args), total=total)

    def generate_messages(self):
        os.makedirs(Windows_Paths.get("messages"), exist_ok=True)

        # Check if the messages.json file exists.
        if not os.path.exists(Windows_Paths.get("messages") + "messages.json"):
            with open(Windows_Paths.get("messages") + "messages.json", 'w') as f:
                messages = {
                    # General
                    "description": "[cyan]SecurePass Analyzer[/cyan] assesses password strength, providing improvement suggestions.",

                    # Report Generation
                    "generating_report": "[cyan]Generating report[/cyan] for password '[green]{password}'[reset]...",
                    "report_generated": "Report generated for password '[green]{password}'[reset] - [bright_black]{timestamp}[reset].",
                    "error_generating_report": "[red]Error:[/red] Unable to generate report for password '[green]{password}'[reset].",

                    # Password Generation
                    "generating_password": "[cyan]Generating password[/cyan] with options: [yellow]{options}[reset]...",
                    "password_generated": "Password generated: '[green]{password}'[reset].",
                    "error_generating_password": "[red]Error:[/red] Unable to generate password.",

                    # Wordlists
                    "wordlist_loaded": "Wordlist '[yellow]{wordlist}'[reset] loaded from '[bright_black]{path}[reset]'.",
                    "error_loading_wordlist": "[red]Error:[/red] Unable to load wordlist '[yellow]{wordlist}'[reset] from '[bright_black]{path}[reset]'.",
                    "wrong_extension_wordlist": "[red]Error:[/red] Wrong extension of wordlist '[yellow]{wordlist}'[reset]. Only '.txt' is supported. Skipping wordlist.",
                    "downloading_wordlist": "[cyan]Downloading wordlist[/cyan] '[yellow]{wordlist}'[reset] from '[bright_black]{url}[reset]'...",
                    "error_downloading_wordlist": "[red]Error:[/red] Unable to download wordlist '[yellow]{wordlist}'[reset] from '[bright_black]{url}[reset]'.",
                    "wordlist_downloaded": "Wordlist '[yellow]{wordlist}'[reset] downloaded to '[bright_black]{path}[reset]'.",

                    # Policies
                    "policy_loaded": "Policy '[blue]{policy}'[reset] loaded from '[bright_black]{path}[reset]'.",
                    "error_loading_policy": "[red]Error:[/red] Unable to load policy '[blue]{policy}'[reset] from '[bright_black]{path}[reset]'.",
                    "downloading_policy": "[cyan]Downloading policy[/cyan] '[blue]{policy}'[reset] from '[bright_black]{url}[reset]'...",
                    "error_downloading_policy": "[red]Error:[/red] Unable to download policy '[blue]{policy}'[reset] from '[bright_black]{url}[reset]'.",
                    "policy_downloaded": "Policy '[blue]{policy}'[reset] downloaded to '[bright_black]{path}[reset]'."

                }

                json.dump(messages, f, indent=4)
