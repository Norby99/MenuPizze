import tkinter as tk
from libraries.utils import capfirst
from libraries.windowSpecs import WindowSpecs
import json
from abc import ABC

class PizzaMenu(ABC):

    def loadSetupData(self):
        fname = "setup.json"
        with open(fname) as f:
            return json.load(f)

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
                    pizze.append({"objType" : "title", "tipo" : i["nome_tipo"]})
                    tipo_pizza = i["nome_tipo"]

                pizze.append({
                            "objType" : "pizza",
                            "id" : int(i["id"]),
                            "nome": i["nomePizza"],
                            "tipo" : i["nome_tipo"],
                            "prezzo" : '€ {:,.2f}'.format(float(i["prezzo"])),
                            "ingredienti" : capfirst(", ".join(str(x) for x in i["ingredienti"].split(","))),
                            "ingredientiInglese" : capfirst(", ".join(str(x) for x in i["ingredientiInglese"].split(","))),
                            "allergens" : i["allergeni"]
                        })
        return pizze

    def aggiunteCreator(self):
        """
        creates a dictionary with all the aggiunte
        """
        aggiunte = self.pizza.get_aggiunte()
        for i in aggiunte:
            i["objType"] = "aggiunta"
            i["prezzo"] = '€ {:,.2f}'.format(float(i["prezzo"]))

        aggiunte.insert(0, {"objType" : "title", "tipo" : "Aggiunte"})  # added title aggiunte
        return aggiunte

    def insalateCreator(self):
        """
        creates a dictionary with all the "insalate"
        """
        insalate = []
        data = self.pizza.get_insalate(True)

        for i in data:
            insalate.append({
                            "objType" : "insalata",
                            "id" : int(i["id"]),
                            "nome": i["nomeInsalata"],
                            "prezzo" : '€ {:,.2f}'.format(float(i["prezzo"])),
                            "ingredienti" : capfirst(", ".join(str(x) for x in i["ingredienti"].split(","))),
                            "ingredientiInglese" : capfirst(", ".join(str(x) for x in i["ingredientiInglese"].split(","))),
                            "allergens" : i["allergeni"]
                        })

        insalate.insert(0, {"objType" : "title", "tipo" : "Insalate"})  # added title aggiunte

        return insalate

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
        self.windowSpecs = WindowSpecs()
        self.screenDimension = self.windowSpecs.getScreenDimension()
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
