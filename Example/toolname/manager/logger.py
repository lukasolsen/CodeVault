import os
import json
from datetime import datetime
from rich.console import Console
from rich.progress_bar import ProgressBar
from rich.progress import Progress
from manager.locale import _, Locale

try:
    from rich.console import Console
    from rich.progress_bar import ProgressBar
except ImportError:
    os.system("pip install rich")
    try:
        from rich.console import Console
        from rich.progress_bar import ProgressBar
    except ImportError:
        print("Unable to install rich. Please install manually.")
        exit(0)


class Logger:
    """
    The main logger class, used for logging messages to the console and log file.

    Features:
        - Console Logging
        - File Logging
        - JSON Logging
        - Progress Bar Logging
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Singleton implementation for the Logger class.

        Ensures that only one instance of Logger exists throughout the program.

        Returns:
            Logger: The Logger instance.
        """
        if not cls._instance:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self) -> None:
        """
        Initialize the Logger instance.

        Sets up the console, log file, and other properties for logging.
        """
        if not self.__initialized:
            self.console = Console()
            self.log_file = f"example-{datetime.now().strftime('%d-%m-%Y')}.log"
            self.log_to_file = False
            self.can_log_to_console = True
            self.__initialized = True
            self.locale = Locale()
            self.prefix = _("prefix")

    def log(self, message_key: str, *args) -> None:
        """
        Log a message to the console.

        Args:
            message_key (str): The key for the localized message.
            args: Additional arguments for formatting the message.
        """
        message = _(message_key)
        self.log_to_console(message, args)

    def log_to_console(self, message: str, *args: dict) -> None:
        """
        Log a message to the console.

        Args:
            message (str): The message to be logged.
            args (dict): Additional arguments for formatting the message.
        """
        if self.can_log_to_console:
            self.console.print(self.prefix + message.format(args))

    def log_success(self, message_key: str, *args) -> None:
        """
        Log a success message to the console.

        Args:
            message_key (str): The key for the localized success message.
            args: Additional arguments for formatting the message.
        """
        if self.can_log_to_console:
            message = _(message_key)
            self.console.print(
                self.prefix + "[green]Success[/green]: " + message.format(args))

    def log_warning(self, message_key: str, *args) -> None:
        """
        Log a warning message to the console.

        Args:
            message_key (str): The key for the localized warning message.
            args: Additional arguments for formatting the message.
        """
        if self.can_log_to_console:
            message = _(message_key)
            self.console.print(
                self.prefix + "[yellow]Warning[/yellow]: " + message.format(args))

    def log_json(self, data: str, indent=4) -> None:
        """
        Log a JSON object to the console.

        Args:
            data (str): The JSON object to be logged.
        """
        if self.can_log_to_console:
            self.console.print_json(json.dumps(data, indent=indent))

    def log_progress(self, message_key: str, args: dict, total: int) -> ProgressBar:
        """
        Log a progress bar to the console.

        Args:
            message_key (str): The key for the localized progress message.
            args (dict): Additional arguments for formatting the message.
            total (int): The total number of steps in the progress.

        Returns:
            ProgressBar: The progress bar object.
        """
        if self.can_log_to_console:
            message = _(message_key)
            progress = Progress(
                self.console,
                self.prefix + message.format(args),
                "[progress.description]{task.description}",
                "{task.completed}/{task.total}",
                "•",
                "progress.remaining",
                transient=True
            )
            return progress.add_task("progress", total=total)

    def __dir__(self):
        """
        Limit the visible attributes when using dir(Logger).
        """
        return ['log', 'log_to_console', 'log_success', 'log_warning', 'log_json', 'log_progress']
