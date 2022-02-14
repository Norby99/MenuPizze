import requests
import json

class Cloud():

    def __init__(self, mKey):
        self.mKey = mKey

    def read(self, url):
        """
        Given an @url, it returns the data formated as json
        It returns False if the server is not responding
        """
        headers = {'X-Master-Key': self.mKey}

        try:
            print("url: ", url)
            print("h: ", headers)
            req = requests.get(url, headers=headers)
            data = json.dumps(req.json(), indent = 4)
            return data
        except requests.exceptions.RequestException as err:
            print(f"Host is not responding!\n{err}")
            return False

    def update(self, data, url):
        headers = {'Content-Type': 'application/json',
                    'X-Master-Key': self.mKey}

        req = requests.put(url, json=data, headers=headers)
        print(req.text)
        print("File: " + url + "\nSuccesful updated!")

"""if __name__ == "__main__":

    c = Cloud("yourMkey")
    url = 'https://api.jsonbin.io/v3/b/60477e50683e7e079c49e1b3'
    c.read(url)
    
    fileName = "prova.json"
    with open(fileName) as json_file:
        data = json.load(json_file)
    c.update(data, url)"""
