import time
import requests
import os

def capfirst(s):
    """Capitalize the first letter of a string without touching the others"""
    return s[:1].upper() + s[1:]

def waitForConnection(url='http://www.google.com/', timeout=5):
    initTime = time.time()
    while True:
        try:
            _ = requests.head(url, timeout=timeout)
            break
        except requests.ConnectionError:
            pass
        nowTime = time.time()
        if (nowTime-initTime)/60 > 3:
            print("No internet connection available.")
            break

def creation_date(path_to_file):
    return os.path.getmtime(path_to_file)