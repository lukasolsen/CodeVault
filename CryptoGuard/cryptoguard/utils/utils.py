from cryptoguard.utils.messages import messages
from termcolor import colored


def help() -> None:
    print(colored(messages.get('help'), 'cyan', attrs=["bold"]))
    print(colored(messages.get('version'), 'cyan'))
    print(colored(messages.get('usage'), 'cyan'))
    print(colored(messages.get('options'), 'cyan'))
    print(colored(messages.get('version_option'), 'cyan'))
    print(colored(messages.get('encrypt_option'), 'cyan'))
    print(colored(messages.get('decrypt_option'), 'cyan'))
    print(colored(messages.get('key_option'), 'cyan'))
    print(colored(messages.get('detect_option'), 'cyan'))
    print(colored(messages.get('algorithm_option'), 'cyan'))
    print(colored(messages.get('output_option'), 'cyan'))
    print(colored(messages.get('replace_option'), 'cyan'))


def version() -> None:
    print(colored(messages.get("version"), 'cyan'))
