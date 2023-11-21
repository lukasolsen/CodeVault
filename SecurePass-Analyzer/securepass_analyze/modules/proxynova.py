import os
import requests


def query_proxynova(query: str) -> dict:
    """Query proxynova.com for leaked passwords, emails and usernames."""
    try:
        response = requests.get(
            f"https://api.proxynova.com/comb?query={query}")

        if response.status_code == 200:
            return response.json()
        else:
            return {}
    except:
        return {}
