import requests
import json

class LanguageHandler():
    connectionTracker = True #remouves spam comments

    def __init__(self, website, token=""):
        """
        This class reads the language (a text shown on a website)
        @param website is the link to the website (eg. 192.168.1.1/request)
        @param token is optinal and is the autentication token to log in the website
        """
        self.website = website
        self.token = token

    def getCurrentLanguage(self):
        try:
            if self.token != "":
                req = requests.get(self.website, headers={'X-Master-Key': self.token})
            else:
                req = requests.get(self.website)
            return req

        except requests.exceptions.RequestException as err:
            print(f"Host is not responding!\n{err}")
            return False

    def temp(self):
        try:
            if self.restaurant_name != "":
                self.con = self.connect()
                cursor = self.con.cursor(buffered=True)
                query = f"""
                    SELECT language_name
                    FROM `restaurants`
                    INNER JOIN languages ON restaurants.id_language = languages.id
                    WHERE restaurants.restaurant_name = '{self.restaurant_name}';
                    """
                cursor.execute(query)
                self.con.close()
                return cursor.fetchone()[0]
            else:
                return "nome_italiano"
        except:
            return "nome_italiano"

if __name__ == "__main__":
    with open("DBsetup.json") as f:
        data = json.load(f)
    LHandler = LanguageHandler(data['languageSite'] + "/" + data['restaurantName'] + ".php", token=data['m_key'])
    while True:
        print(LHandler.getCurrentLanguage())
