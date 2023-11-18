from utils.messages import messages
from termcolor import colored
import os


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


def get_files_from_args(args):
    files = []
    for file in args.files:
        if os.path.isdir(file):
            files.extend(get_files_from_folder(
                file, args.depth or 1, args.verbose))
        elif os.path.exists(file):
            files.append(file)
        else:
            if args.verbose:
                print(colored(messages.get(
                    'file_not_found').format(file=file), 'red'))
    return files


def get_files_from_folder(folder, depth, verbose):
    files = []
    current_depth = 0
    for root, dirs, filenames in os.walk(folder):
        current_depth += 1
        if current_depth > depth:
            if verbose:
                print(colored(messages.get('depth_reached').format(
                    depth=depth), 'yellow'))
            break
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files
