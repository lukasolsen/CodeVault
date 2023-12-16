import os
import yaml
import subprocess
import shutil


class InitializeManager:
    def __init__(self) -> None:
        self.main_path = os.path.join(
            os.getenv("PROGRAMDATA"), "Example")

    def initialize(self) -> None:
        os.makedirs(self.main_path, exist_ok=True)

        # Config
        config_path = os.path.join(self.main_path, 'config.yml')
        if not os.path.exists(config_path):
            self.config(config_path)

        # Locales
        locales_path = os.path.join(self.main_path, 'locales')
        if not os.path.exists(locales_path):
            self.create_locales()

    def config(self, path: str) -> None:
        """Create a config file."""
        default_config = {
            "name": "Example",
            "version": "1.0.0",
            "author": "Example Author",
            "paths": {
                "windows": {
                    "messages": "%PROGRAMDATA%/Example/locales/",
                },
                "linux": {
                    "messages": "/usr/share/locales/",
                },
                "mac": {
                    "messages": "/usr/local/share/locales/",
                }
            },
            "locale": "en_US",
            "internationalization_method": "default",
        }

        with open(path, 'w') as f:
            yaml.dump(default_config, f, default_flow_style=False)

    def create_locales(self) -> None:
        """Create the locales directory."""
        os.makedirs(os.path.join(self.main_path, 'locales'), exist_ok=True)

        prefix = "[gray][[blue]Example Code[/blue]][/gray][reset] "

        # Create the default locale
        self.write_locale('en_US', {
            "prefix": prefix,

            "description": "[cyan]Example Code[/cyan] assesses the quality of your code.",
            "example_command": "[cyan]Example Code[/cyan] [blue]example[/blue] [green]--help[/green]",
        })

    def write_locale(self, locale: str, data: str) -> None:
        """Write a locale file."""
        with open(os.path.join(self.main_path, 'locales', locale + '.yml'), 'w') as f:
            yaml.dump(data, f, default_flow_style=False)


class ConfigurationManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigurationManager, cls).__new__(cls)
            return cls._instance
        else:
            return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, 'initialized'):
            self.initialized = True
            InitializeManager().initialize()

            self.data = None
            self.path = os.path.join(
                os.getenv("PROGRAMDATA"), "Example")

            self.load()

    def load(self) -> None:
        os.makedirs(self.path, exist_ok=True)
        if os.path.exists(os.path.join(self.path, 'config.yml')):
            with open(os.path.join(self.path, 'config.yml'), 'r') as f:
                self.data = yaml.load(f, Loader=yaml.FullLoader)

                def replace_env_vars(paths):
                    for key, value in paths.items():
                        if isinstance(value, str):
                            paths[key] = os.path.expandvars(value)
                        elif isinstance(value, dict):
                            replace_env_vars(value)

                replace_env_vars(self.data['paths'])
            f.close()
        else:
            print("Something went wrong, see the logs for more information.")

    def get_name(self) -> str:
        return self.data['name']

    def get_version(self) -> str:
        return self.data['version']

    def get_author(self) -> str:
        return self.data['author']

    def get_paths(self) -> dict:
        return self.data['paths']

    def get_windows_paths(self) -> dict:
        return self.data['paths']["windows"]

    def get_linux_paths(self) -> dict:
        return self.data['paths']["linux"]

    def get_mac_paths(self) -> dict:
        return self.data['paths']["mac"]

    def get_path(self, path: str) -> str:
        """Get a path from the dictionary."""
        if os.name == "posix":
            return self.get_linux_paths().get(path)
        elif os.name == "darwin":
            return self.get_mac_paths().get(path)
        elif os.name == "nt":
            return self.get_windows_paths().get(path)

    def get_locale(self) -> str:
        return self.data['locale']

    def get_internationalization_method(self) -> str:
        return self.data['internationalization_method']
