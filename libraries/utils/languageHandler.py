import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import json
from libraries.utils.logger import Logger

class LanguageHandler():

    _logger: Logger
    _connection_tracker = True    # remouves spam comments
    _logger_title = "(LanguageHandler)"

    def __init__(self, website, default_language, token="", no_connection=False):
        """
        This class reads the language (a text shown on a website)
        @param website is the link to the website (eg. 192.168.1.1/request)
        @param default_language is the default language that will be returned in case the website is not reachable
        @param token is optinal and is the autentication token to log in the website
        @param no_connection is optinal and if set to True, it always return the default language
        """
        self._logger = Logger()
        self._website = website
        self._default_language = default_language
        self._token = token
        self.no_connection = no_connection

    def getCurrentLanguage(self):
        if self.no_connection:
            return self._default_language

        try:
            session = requests.Session()
            retry = Retry(connect=3, backoff_factor=0.5)
            adapter = HTTPAdapter(max_retries=retry)
            session.mount('http://', adapter)
            session.mount('https://', adapter)
            
            if self._token != "":
                message = requests.get(self._website, headers={'X-Master-Key': self._token}).text
            else:
                message = requests.get(self._website).text

            if (message == ""):
                if self._connection_tracker:
                    self._logger.disp(f"{self._logger_title}No response, maybe the token is wrong\n")
                    self._connection_tracker = False
                return self._default_language

            if not self._connection_tracker:
                self._logger.disp(f"{self._logger_title}Connection established (language site)")
                self._connection_tracker = True

            return message

        except requests.exceptions.RequestException as err:
            if self._connection_tracker:
                self._logger.disp(f"{self._logger_title}Host (language site) is not responding!\n{err}")
                self._connection_tracker = False
            return self._default_language

if __name__ == "__main__":
    with open("DBsetup.json") as f:
        data = json.load(f)
    LHandler = LanguageHandler(data['languageSite'] + "/" + data['restaurantName'] + ".php", data['defaultLanguage'], token=data['m_key'])
    while True:
        print(LHandler.getCurrentLanguage())
