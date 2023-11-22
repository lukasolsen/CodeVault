import os
import json
from manager.Logger import Logger

from service.paths import Windows_Paths
from pathlib import Path
from rich.progress import Progress
import requests


class Wordlist:
    def __init__(self) -> None:
        if not Path(Windows_Paths.get('wordlist')).exists():
            os.makedirs(Windows_Paths.get('wordlist'), exist_ok=True)

            self.wordlists = ["https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt",
                              "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt"]

            WordlistDownloader().download_wordlists(self.wordlists)

    def get_wordlists(self, path: str) -> dict:
        wordlists = {}

        for root, dirs, files in os.walk(path):
            for file in files:
                if not file.endswith(".txt"):
                    Logger().log("wrong_extension_wordlist", {
                        "wordlist": file, "path": os.path.join(root, file)})
                    continue

                wordlist_path = os.path.join(root, file)
                Logger().log("wordlist_loaded", {
                    "wordlist": file, "path": wordlist_path})

                if wordlist_path:
                    wordlists[file] = {
                        "name": file,
                        "path": wordlist_path,
                    }
                else:
                    Logger().log("error_loading_policy", {"policy": file})

            for dir in dirs:
                self.get_wordlists(dir)

        return wordlists

    def get_wordlist(self, path: str) -> str:
        # Get the wordlist from the path.
        try:
            with open(path, 'r', encoding='utf-8') as file:
                wordlist = file.read()
        except:
            wordlist = ""
        return wordlist

    def word_in_wordlist(self, password: str, wordlist: str) -> bool:
        if password.lower() in wordlist:
            return True


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
