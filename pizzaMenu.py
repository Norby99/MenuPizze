import tkinter as tk
from libraries.utils import capfirst
import json
from abc import ABC

class PizzaMenu(ABC):

    def loadSetupData(self):
        fname = "setup.json"
        with open(fname) as f:
            return json.load(f)

    def aggiunteCreator(self):
        aggiunte = []
        data = self.pizza.get_aggiunte()
        for i in data:
            aggiunte.append({
                "nome" : (", ".join(str(x) for x in i["nome_aggiunta"].split(","))).capitalize(),
                "nomeInglese" : (", ".join(str(x) for x in i["nome_inglese"].split(","))).capitalize(),
                "prezzo" : '€ {:,.2f}'.format(float(i["prezzo_aggiunta"]))
            })
        return aggiunte

    
    def pizzeCreator(self, pizzaType="*"):     ### crea un dizionario con tutte le pizze e i suoi atributi
        """
        creates a dictionary with all the pizzas that have the @pizzaType
        @pizzaType it's a list, or it can be "*" (default) for all elements
        """
        pizze = []
        data = self.pizza.get_pizzas(True)
        tipo_pizza = ""

        for i in data:
            if (i["nome_tipo"] in pizzaType) or pizzaType == "*":
                if i["nome_tipo"] != tipo_pizza:
                    pizze.append({"tipo" : i["nome_tipo"]})
                    tipo_pizza = i["nome_tipo"]

                pizze.append({
                            "id" : int(i["id"]),
                            "nome": i["nomePizza"],
                            "tipo" : i["nome_tipo"],
                            "prezzo" : '€ {:,.2f}'.format(float(i["prezzo"])),
                            "ingredienti" : capfirst(", ".join(str(x) for x in i["ingredienti"].split(","))),
                            "ingredientiInglese" : capfirst(", ".join(str(x) for x in i["ingredientiInglese"].split(","))),
                            "allergens" : i["allergeni"]
                        })
        return pizze

    def tkWindowSetup(self):
        """
        - Creates a window(Tk) and a @screenDimension[width, height] that contains the current screen dimension
        - Sets the screen to full screen and creates an attribute @fullScreebState that tracks the full screen state
        - It binds:   F12 to quitFullScreen(); F11 to FullScreen(); Escape to close()
        - Hides cursor
        """

        self.window = tk.Tk()
        self.window.attributes('-fullscreen', True)  
        self.fullScreenState = False
        self.window.bind("<F12>", self.quitFullScreen)
        self.window.bind("<F11>", self.toggleFullScreen)
        self.window.bind("<Escape>", self.close)
        self.screenDimension = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        self.window.config(cursor="none")
        
    def close(self, event):
        self.window.destroy()
        exit()

    def toggleFullScreen(self, event):
        self.fullScreenState = not self.fullScreenState
        self.window.attributes("-fullscreen", self.fullScreenState)

    def quitFullScreen(self, event):
        self.fullScreenState = False
        self.window.attributes("-fullscreen", self.fullScreenState)

    def ShowAll(self):
        self.menu.show()

    def Update(self):
        self.menu.updateCells()
        self.window.after(2000, self.Update)
