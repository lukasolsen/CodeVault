import os
import json
from datetime import datetime
from manager.locale import _, Locale
from manager.config import ConfigurationManager

try:
    from rich.console import Console
    from rich.progress_bar import ProgressBar
    from rich.progress import Progress
    from rich.table import Table
except ImportError:
    os.system("pip install rich")
    try:
        from rich.console import Console
        from rich.progress_bar import ProgressBar
        from rich.progress import Progress
        from rich.table import Table
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
        return cls._instance

    def __init__(self) -> None:
        """
        Initialize the Logger instance.

        Sets up the console, log file, and other properties for logging.
        """
        self.console = Console()
        self.log_file = os.path.join(
            ConfigurationManager().get_path("logs"), ConfigurationManager().get_name() + "-" +
            datetime.now().strftime("%Y-%m-%d") + ".log"
        )
        self.locale = Locale()
        self.prefix = _("prefix")

    def log(self, message_key: str, *args, options: dict = {"emoji": False}) -> None:
        """
        Log a message to the console.

        Args:
            message_key (str): The key for the localized message.
            args: Additional arguments for formatting the message.
        """
        message = _(message_key)
        self.console.print(self.prefix + message.format(args), **options)

    def log_json(self, data: str, indent=4) -> None:
        """
        Log a JSON object to the console.

        Args:
            data (str): The JSON object to be logged.
        """

        self.console.print_json(json.dumps(data, indent=indent))

    def log_logfile(self, message: str, format="{time} {message}") -> None:
        """
        Log a message to the log file.

        Args:
            message (str): The message to be logged.
        """
        if (not os.path.exists(self.log_file)):
            with open(self.log_file, 'w') as f:
                f.write("")
                f.close()

            self.log_logfile(message, format)
        else:
            with open(self.log_file, 'a') as f:
                f.write(format.format(time=datetime.now().strftime(
                    "%H:%M:%S"), message=message))
                f.write("\n")
            f.close()

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

    def log_table(self, columns: list, rows: list, title: str = None) -> None:
        """
        Log a table to the console.

        Args:
            columns (list): The columns of the table.
            rows (list): The rows of the table.
            title (str, optional): The title of the table. Defaults to None.
        """
        table = Table(title=title or "CodeVault's Table")
        for column in columns:
            table.add_column(column)
        for row in rows:
            table.add_row(*row)
        self.console.print(table)

    def __dir__(self):
        """
        Limit the visible attributes when using dir(Logger).
        """
        return ['log', 'log_to_console', 'log_success', 'log_warning', 'log_json', 'log_progress']
