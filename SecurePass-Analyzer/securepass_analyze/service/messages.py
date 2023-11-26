from service.paths import Windows_Paths
import json


def load_messages() -> dict:
    with open(Windows_Paths.get("messages") + "messages.json", "r") as f:
        messages = json.load(f)
    return messages


def get_message(message: str, **kwargs) -> str:
    # Get the message from the messages.json file.
    messages = load_messages()
    return messages.get(message).format(**kwargs)
