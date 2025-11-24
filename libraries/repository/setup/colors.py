import json

class Colors:

    __file = "setup.json"

    def __init__(self):
        with open(self.__file) as f:
            data = json.load(f)
            colors = data['colors']

        self.background = colors["background"]
