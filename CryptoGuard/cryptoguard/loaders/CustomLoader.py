import os
import importlib.machinery
from termcolor import colored
from utils.messages import messages

from methods.AES import AESMethod
from methods.Fernet import FernetMethod
from methods.RSA import RSAMethod


class Loader:
    def __init__(self) -> None:
        self.methods = {}

        self.load_premade_methods()
        self.load_custom_methods()

    def load_custom_methods(self):
        custom_methods_directory = "custom_methods"
        if os.path.exists(custom_methods_directory) and os.path.isdir(custom_methods_directory):
            for file_name in os.listdir(custom_methods_directory):
                if file_name.endswith(".py"):
                    module_name = os.path.splitext(file_name)[0]
                    # Get the abs path of the module
                    module_path = os.path.join(
                        os.path.abspath(custom_methods_directory), file_name)

                    try:
                        loader = importlib.machinery.SourceFileLoader(
                            module_name, module_path)
                        custom_method_module = loader.load_module()

                        custom_methods = [getattr(custom_method_module, x) for x in dir(
                            custom_method_module) if x.endswith("Method")]

                        for custom_method in custom_methods:
                            custom_method_name = custom_method.__name__
                            if custom_method:
                                self.methods[custom_method_name] = custom_method()
                                print(colored(messages.get(
                                    'custom_method_loaded').format(method=custom_method_name), 'green'))
                            else:
                                print(colored(messages.get(
                                    'invalid_custom_method').format(method=custom_method_name), 'red'))
                    except Exception as e:
                        print(colored(messages.get(
                            'error_loading_custom_method').format(method=module_name, error=str(e)), 'red'))

    def load_premade_methods(self):
        self.methods = {
            "aes": AESMethod(),
            "fernet": FernetMethod(),
            "rsa": RSAMethod()
        }

    def get_method(self, method_name: str):
        return self.methods.get(method_name)

    def get_methods(self):
        return self.methods
