import os
import yaml
import subprocess
import shutil


class InitializeManager:
    def __init__(self) -> None:
        self.main_path = os.path.join(
            os.getenv("PROGRAMDATA"), "Example")
        self.github_repo = "https://github.com/lukasolsen/CodeVault.git"
        self.locales_repo_path = os.path.join(
            self.main_path, 'Example/data/locales')

    def initialize(self) -> None:
        os.makedirs(self.main_path, exist_ok=True)

        # Config
        config_path = os.path.join(self.main_path, 'config.yml')
        if not os.path.exists(config_path):
            self.config(config_path)

        # Locales
        locales_path = os.path.join(self.main_path, 'locales')
        if not os.path.exists(locales_path):
            self.clone_locales_repo()
            self.copy_locales(locales_path)

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

    def clone_locales_repo(self) -> None:
        """Clone the locales repository."""
        try:
            subprocess.run(['git', 'clone', self.github_repo,
                           self.locales_repo_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error cloning locales repository: {e}")

    def copy_locales(self, path: str) -> None:
        """Copy locales folder from the cloned repository."""
        locales_repo_path = os.path.join(self.locales_repo_path, 'locales')

        try:
            shutil.copytree(locales_repo_path, path)
        except shutil.Error as e:
            print(f"Error copying locales: {e}")


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
