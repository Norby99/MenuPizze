import requests
import json
from libraries.utils.logger import Logger
from libraries.utils.jsonValidator import *

class Cloud():

    _log_file: str

    def __init__(self, mKey):
        self.mKey = mKey
        self._logger = Logger()

    def read(self, url):
        """
        Given an @url, it returns the data formated as json
        It returns False if the server is not responding
        """
        headers = {'X-Master-Key': self.mKey}

        try:
            req = requests.get(url, headers=headers)
            data = json.dumps(req.json(), indent = 4)   # sometimes the dumps method is not throwing an exeption if the json is not valid
            if is_json(data):
                self._logger.disp(f"File downloaded successfully! - File: {url}")
                return data

        except requests.exceptions.RequestException as err:
            self._logger.disp(f"Host is not responding! - {err}")
        
        return False

    def update(self, data, url):
        headers = {'Content-Type': 'application/json',
                    'X-Master-Key': self.mKey}

        req = requests.put(url, json=data, headers=headers)
        self._logger.disp(req.text)
        self._logger.disp("File: " + url + "\nSuccesful updated!")

"""if __name__ == "__main__":

    c = Cloud("yourMkey")
    url = 'https://api.jsonbin.io/v3/b/60477e50683e7e079c49e1b3'
    c.read(url)
    
    fileName = "prova.json"
    with open(fileName) as json_file:
        data = json.load(json_file)
    c.update(data, url)"""
