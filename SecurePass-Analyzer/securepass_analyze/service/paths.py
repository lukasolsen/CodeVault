import os

ProgramData = os.getenv('PROGRAMDATA')

Windows_Paths = {
    "wordlist": ProgramData + "/CodeVault/wordlists/",
    "policy": ProgramData + "/CodeVault/SecurePass/policies/",
    "messages": ProgramData + "/CodeVault/SecurePass/"
}
