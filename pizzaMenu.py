from libraries.PizzaHandler import Pizzas
import tkinter as tk
from libraries.utils import capfirst, waitForConnection
from libraries.windowsSpecs import WindowSpecs
import json
from libraries.elencoGenerator import Elenco
from abc import ABC

class PizzaMenu(ABC):

    def aggiunteCreator(self):
        aggiunte = []
        data = self.p.get_aggiunte()
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
        data = self.p.get_pizzas(True)
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
                            "ingredientiInglese" : capfirst(", ".join(str(x) for x in i["ingredientiInglese"].split(",")))
                        })
        return pizze
        
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
        self.menu.showAggiunte()

    def Update(self):
        self.menu.updateScritte()
        self.window.after(2000, self.Update)
