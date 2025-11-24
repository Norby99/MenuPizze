import json

class FontColors:

    __file = "setup.json"

    def __init__(self):
        with open(self.__file) as f:
            data = json.load(f)
            colors = data['colors']

        self.background = colors["background"]
        self.p_tipo = colors["p_tipo"]
        self.titolo = colors["titolo"]
        self.generic_text = colors["generic_text"]
        self.price = colors["price"]
        self.menu_settimanale = colors["menu_settimanale"]
