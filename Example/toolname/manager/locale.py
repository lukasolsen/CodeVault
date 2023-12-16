import yaml
import os
import locale
from manager.config import ConfigurationManager


class Locale:
    """
    Singleton class for managing localization.

    Handles loading and retrieving localized messages from YAML files based on the current locale.
    """
    _instance = None  # Singleton instance

    def __new__(cls, *args, **kwargs):
        """
        Singleton implementation for the Locale class.

        Ensures that only one instance of Locale exists throughout the program.

        Returns:
            Locale: The Locale instance.
        """
        if not cls._instance:
            cls._instance = super(Locale, cls).__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self) -> None:
        """
        Initialize the Locale instance.

        Sets the default locale, loads the corresponding YAML file, and initializes locale data.
        """
        if not self.__initialized:
            self.locale_ = ConfigurationManager().get_locale() or "en_US"
            self.locale_data = None
            locale.setlocale(locale.LC_ALL, self.locale_)

            # Load en_US.yml file from manager/locales/en_US.yml
            if os.path.exists(f"{ConfigurationManager().get_path('messages')}{self.locale_}.yml"):
                with open(f"{ConfigurationManager().get_path('messages')}{self.locale_}.yml", "r") as f:
                    self.locale_data = yaml.safe_load(f)

            self.__initialized = True

    def set_locale(self, locale_="en_US"):
        """
        Set the current locale.

        Loads the corresponding YAML file for the given locale.

        Args:
            locale_ (str): The locale to set.
        """
        self.locale_ = locale_

        if os.path.exists(f"{ConfigurationManager().get_path('messages')}{locale_}.yml"):
            with open(f"{ConfigurationManager().get_path('messages')}{locale_}.yml", "r") as f:
                self.locale_data = yaml.safe_load(f)

        locale.setlocale(locale.LC_ALL, locale_)

    def get_locale(self):
        """
        Get the current locale.

        Returns:
            str: The current locale.
        """
        return self.locale_

    def get_locale_data(self, key):
        """
        Get the localized message for the given key.

        Args:
            key (str): The key for the localized message.

        Returns:
            str: The localized message or the key itself if not found.
        """
        try:
            return self.locale_data[key]
        except KeyError:
            return key


def _(key: str) -> str:
    """
    Get a localized message for the given key.

    Args:
        key (str): The key for the localized message.

    Returns:
        str: The localized message or the key itself if not found.
    """
    locale_instance = Locale()
    if locale_instance.locale_data is None:
        return key
    else:
        return locale_instance.get_locale_data(key)
