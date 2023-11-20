import os
from service.messages import load_messages
from termcolor import colored


def get_wordlists(path: str) -> dict:
    # Use os and go around the path to get the wordlists.
    paths = {}
    messages = load_messages()

    for root, dirs, files in os.walk(path):
        for file in files:
            print(colored(messages.get("loaded_wordlist"), 'green').format(
                wordlist=file, path=os.path.join(root, file)))

            paths[file] = {"name": file, "path": os.path.join(
                root, file), "size": os.path.getsize(os.path.join(root, file))}

        for dir in dirs:
            get_wordlists(dir)

    return paths


def get_wordlist(path: str) -> str:
    # Get the wordlist from the path.
    try:
        with open(path, 'r', encoding='utf-8') as file:
            wordlist = file.read()
    except:
        print("asdasdsd")
        wordlist = ""
    return wordlist


def word_in_wordlist(word: str, wordlist: str) -> bool:
    # Check if the word is in the wordlist.
    if word.lower() in wordlist:
        return True
    else:
        return False
