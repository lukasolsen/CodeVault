import os
from manager.Logger import Logger
from service.paths import Windows_Paths
from rich.progress import Progress
import requests


def get_wordlists(path: str) -> dict:
    # Use os and go around the path to get the wordlists.
    paths = {}

    for root, dirs, files in os.walk(path):
        for file in files:
            # Check if correct extension
            if not file.endswith(".txt"):
                Logger().log(
                    "wrong_extension_wordlist", {"wordlist": file})
                continue

            Logger().log("wordlist_loaded", {
                "wordlist": file, "path": os.path.join(root, file)})

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
        wordlist = ""
    return wordlist


def word_in_wordlist(word: str, wordlist: str) -> bool:
    # Check if the word is in the wordlist.
    if word.lower() in wordlist:
        return True
    else:
        return False

