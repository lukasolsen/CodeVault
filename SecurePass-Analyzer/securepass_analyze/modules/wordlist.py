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


class WordlistManager:
    def __init__(self) -> None:
        self


class WordlistDownloader:
    def __init__(self):
        self.logger = Logger()

    def download_wordlists(self, wordlists):
        for wordlist_url in wordlists:
            wordlist_save_path = Windows_Paths.get(
                'wordlist') + wordlist_url.split("/")[-1]

            self.logger.log("downloading_wordlist", {"wordlist": wordlist_url.split(
                "/")[-1], "url": wordlist_url})

            response = requests.get(wordlist_url, stream=True)

            total_size = int(response.headers.get('content-length', 0))

            with open(wordlist_save_path, 'wb') as file, Progress() as progress:
                task = progress.add_task(
                    "[cyan]Downloading...", total=total_size)
                for chunk in response.iter_lines(chunk_size=128, decode_unicode=False):
                    if chunk:
                        file.write(chunk)
                        progress.update(task, advance=len(chunk))

                if progress.tasks[task].completed != progress.tasks[task].total:
                    progress.update(task, advance=progress.tasks[task].total)

                progress.stop()

            self.logger.log("wordlist_downloaded", {"wordlist": wordlist_url.split(
                "/")[-1], "path": wordlist_save_path})
