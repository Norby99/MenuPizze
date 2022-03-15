import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import json

class LanguageHandler():
    connectionTracker = True    # remouves spam comments

    def __init__(self, website, default_language, token="", no_connection=False):
        """
        This class reads the language (a text shown on a website)
        @param website is the link to the website (eg. 192.168.1.1/request)
        @param default_language is the default language that will be returned in case the website is not reachable
        @param token is optinal and is the autentication token to log in the website
        @param no_connection is optinal and if set to True, it always return the default language
        """
        self.website = website
        self.default_language = default_language
        self.token = token
        self.no_connection = no_connection

    def getCurrentLanguage(self):
        if self.no_connection:
            return self.default_language

        try:
            session = requests.Session()
            retry = Retry(connect=3, backoff_factor=0.5)
            adapter = HTTPAdapter(max_retries=retry)
            session.mount('http://', adapter)
            session.mount('https://', adapter)
            
            if self.token != "":
                req = requests.get(self.website, headers={'X-Master-Key': self.token})
            else:
                req = requests.get(self.website)
            req = req.text
            if (req == ""):
                if self.connectionTracker:
                    print("No response, maybe the token is wrong\n")
                    self.connectionTracker = False
                return self.default_language
            else:
                self.connectionTracker = True
                return req

        except requests.exceptions.RequestException as err:
            if self.connectionTracker:
                print(f"Host is not responding!\n{err}")
                self.connectionTracker = False
            return self.default_language

if __name__ == "__main__":
    with open("DBsetup.json") as f:
        data = json.load(f)
    LHandler = LanguageHandler(data['languageSite'] + "/" + data['restaurantName'] + ".php", data['defaultLanguage'], token=data['m_key'])
    while True:
        print(LHandler.getCurrentLanguage())
