import time
import requests
import os
import datetime
from libraries.utils.logger import Logger

def capfirst(s):
    """Capitalize the first letter of a string without touching the others"""
    return s[:1].upper() + s[1:]

def waitForConnection(url='http://www.google.com/', timeout=5):
    _logger = Logger()

    initTime = time.time()
    while True:
        try:
            _ = requests.head(url, timeout=timeout)
            break
        except requests.ConnectionError:
            pass
        nowTime = time.time()
        if (nowTime-initTime)/60 > 3:   # do this for 3 minutes
            _logger.disp("No internet connection available.")
            break

def waitForFilesUpdate(fname='aggiunte.json'):
    """
    Checks if the file is too old (for 3 minutes), after that returns:
    - True : if the file is updated
    - False : if it's not
    """
    _logger = Logger()
    initTime = time.time()

    while True:
        nowTime = time.time()
        if not fileIsOld(fname):
            return True
        
        if (nowTime-initTime)/60 > 3:   # do this for 3 minutes
            _logger.disp("Can't update the files.")
            return False
        time.sleep(5)

def fileIsOld(fname):
    """ Given a fname, it returns true, if the file il older than yesterday, or if the file doesn't exists """
    _logger = Logger()
    fileIsOld = False
    if os.path.isfile(fname):
        _logger.disp("Existing file detected!")
        midnight = datetime.datetime.combine(datetime.datetime.today(), datetime.time.min).timestamp() #in realta segna le 11, ma vabbeh
        if midnight-creation_date(fname) < 0:   #the file was modified today
            fileIsOld = False
        else:
            _logger.disp("But is too old.")
            fileIsOld = True
    else:
        fileIsOld = True
    return fileIsOld

def creation_date(path_to_file):
    return os.path.getmtime(path_to_file)