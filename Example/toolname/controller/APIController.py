import requests


class ApiController:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ApiController, cls).__new__(cls)
            return cls._instance
        else:
            return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, 'initialized'):
            self.initialized = True

    def make_get_request(self, url: str, params: dict = None, headers: dict = None):
        """
        Make a GET request to the specified URL.

        Args:
            url (str): The URL to make the request to.
            params (dict, optional): Parameters to include in the request. Defaults to None.
            headers (dict, optional): Headers to include in the request. Defaults to None.

        Returns:
            requests.Response: The response object.
        """
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response

    def make_post_request(self, url: str, data: dict = None, headers: dict = None):
        """
        Make a POST request to the specified URL.

        Args:
            url (str): The URL to make the request to.
            data (dict, optional): Data to include in the request body. Defaults to None.
            headers (dict, optional): Headers to include in the request. Defaults to None.

        Returns:
            requests.Response: The response object.
        """
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response
