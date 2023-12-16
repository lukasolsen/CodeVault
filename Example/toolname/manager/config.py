import yaml
import os

data = None

with open(os.path.join(os.getcwd(), 'config.yml')) as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

    def replace_env_vars(paths):
        for key, value in paths.items():
            if isinstance(value, str):
                paths[key] = os.path.expandvars(value)
            elif isinstance(value, dict):
                replace_env_vars(value)

    replace_env_vars(data['paths'])


def get_name() -> str:
    return data['name']


def get_version() -> str:
    return data['version']


def get_author() -> str:
    return data['author']


def get_paths() -> dict:
    return data['paths']


def get_windows_paths() -> dict:
    return data['paths']["windows"]


def get_linux_paths() -> dict:
    return data['paths']["linux"]


def get_mac_paths() -> dict:
    return data['paths']["mac"]


def get_path(path: str) -> str:
    """Get a path from the dictionary."""
    # Get a path from the dictionary.
    if os.name == "posix":
        return get_linux_paths().get(path)
    elif os.name == "darwin":
        return get_mac_paths().get(path)
    elif os.name == "nt":
        return get_windows_paths().get(path)
