from libraries.PizzaHandler import Pizzas
import tkinter as tk
import time
from libraries.windowsSpecs import WindowSpecs
import json
import requests
from libraries.elencoGenerator import Elenco

class PizzaMenu1:

    def __init__(self):
        fname = "setup.json"
        with open(fname) as f:
            data = json.load(f)
        self.p = Pizzas(data)
        self.pizzaTypesRequered = ["Pizze classiche", "Pizze bianche", "Pizze conditissime"] # the pizza types that have to be visualized
        self.p.downloadAllFromCloud()
        
        self.window = tk.Tk()
        self.window.attributes('-fullscreen', True)  
        self.fullScreenState = False
        self.window.bind("<F12>", self.close)
        self.window.bind("<F11>", self.toggleFullScreen)
        self.window.bind("<Escape>", self.quitFullScreen)
        self.screenDimension = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        self.windowSpecs = WindowSpecs(self.screenDimension)

        ### These are all the pretty combinations I've found
        #colors = {"background" : "#003049", "generic_text" : "#EAE2B7", "titolo" : "#FCBF49","price" : "#D62828", "p_tipo" : "#F77F00","p_classica" : "#FF0000", "p_bianca" : "#0000FF", "p_speciale" : "#FF0000"}
        #colors = {"background" : "#000000", "p_tipo" : "#FCA311", "titolo" : "#14213D", "generic_text" : "#E5E5E5", "price" : "#FFFFFF"}
        #colors = {"background" : "#1D3557", "p_tipo" : "#E63946", "titolo" : "#F1FAEE", "generic_text" : "#A8DADC", "price" : "#457B9D"}
        #colors = {"background" : "#F4F1DE", "p_tipo" : "#E07A5F", "titolo" : "#3D405B", "generic_text" : "#81B29A", "price" : "#F2CC8F"}
        #colors = {"background" : "#3D405B", "p_tipo" : "#E07A5F", "titolo" : "#81B29A", "generic_text" : "#F4F1DE", "price" : "#F2CC8F"}
        #colors = {"background" : "#2b2e4a", "p_tipo" : "#E07A5F", "titolo" : "#81B29A", "generic_text" : "#F4F1DE", "price" : "#F2CC8F"}
        #colors = {"background" : "#2b2e4a", "p_tipo" : "#e84545", "titolo" : "#903749", "generic_text" : "#53354a", "price" : "#903749"}
        #colors = {"background" : "#540B0E", "p_tipo" : "#e84545", "titolo" : "#E09F3E", "generic_text" : "#FFF3B0", "price" : "#335C67"}
        #colors = {"background" : "#2B2D42", "p_tipo" : "#EF233C", "titolo" : "#8D99AE", "generic_text" : "#EDF2F4", "price" : "#EF233C"}598392
        #colors = {"background" : "#0B0014", "p_tipo" : "#FFFFFF", "titolo" : "#ef233c", "generic_text" : "#F5E9E2", "price" : "#fdc500"}
        colors = data["colors"] # colors are taken from the setup file

        self.window.config(cursor="none")
        self.pizze = self.pizzeCreator(self.pizzaTypesRequered)
        self.aggiunte = self.aggiunteCreator()
        self.menu = Elenco(self.window, self.pizze, self.aggiunte, [self.windowSpecs.resolutionConverter(25), self.windowSpecs.resolutionConverter(25), self.screenDimension[0]-self.windowSpecs.resolutionConverter(50), self.screenDimension[1]-self.windowSpecs.resolutionConverter(100)], data, colors, self.screenDimension)

        self.ShowAll()
        self.Update()
        self.window.mainloop()

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

def capfirst(s):
    """Capitalize the first letter of a string without touching the others"""
    return s[:1].upper() + s[1:]

def waitForConnection(url='http://www.google.com/', timeout=5):
    initTime = time.time()
    while True:
        try:
            _ = requests.head(url, timeout=timeout)
            break
        except requests.ConnectionError:
            pass
        nowTime = time.time()
        if (nowTime-initTime)/60 > 3:
            print("No internet connection available.")
            break

if __name__ == '__main__':
    waitForConnection()
    app = PizzaMenu1()
