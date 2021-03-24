from database import database
from PizzaHandler import Pizzas
import tkinter as tk
from PIL import Image, ImageTk
import time
import os
import math
import distutils.dir_util
import json

class Elenco:
    def __init__(self, window, elenco_pizze, aggiunte, margini, fname):
        self.window = window
        self.elenco_pizze = elenco_pizze
        self.elenco_aggiunte = aggiunte
        self.colonne_max = 5
        self.righe_max = math.ceil(len(self.elenco_pizze)/self.colonne_max)   #numero di pizze per colonna
        self.margini = margini
        self.screenDimension = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        self.cell_dimension = [(self.margini[2]-self.margini[0])/self.colonne_max, (self.margini[3]-self.margini[1])/self.righe_max]
        
        self.testo_aggiunte = ""
        for i in self.elenco_aggiunte:
            self.testo_aggiunte += "| " + i["nome"] + " : " + i["prezzo"] + " "

        with open(fname) as f:
            data = json.load(f)
        self.db = database("localhost", data["dbUserName"], data["dbPassword"], data["dbData"])
    
    def show(self, update=False):
        if update:
            self.updateScritte()
        else:
            self.canvas = tk.Canvas(self.window, width =self.screenDimension[0], height = self.screenDimension[1])
            self.canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            self.canvas.pack()

            #self.canvas.create_rectangle(self.margini[0], self.margini[1], self.margini[2], self.margini[3], fill='red')   #canvas che copre il margine delle pizze

            x = 0
            y = 0
            self.ScritteIngredienti = []
            for i in self.elenco_pizze:
                if y >= self.righe_max:
                    y = 0
                    x += 1
                self.cell_coordinates = [self.margini[0]+self.cell_dimension[0]*x, self.margini[1]+self.cell_dimension[1]*y, self.margini[0]+self.cell_dimension[0]*(x+1), self.margini[1]+self.cell_dimension[1]*(y+1)]
                self.scritte(self.cell_coordinates, i)
                y += 1

    def showAggiunte(self):
        coords = [resolutionConverter(25), self.margini[3], (self.margini[2]*(4/5)+resolutionConverter(500)), self.screenDimension[1]-resolutionConverter(20)]
        self.canvas.pack()

        font_titolo = "Times " + str(resolutionConverter(22)) + " bold"
        font_aggiunte = "Times " + str(resolutionConverter(16))

        ### TITOLO ###
        self.canvas.create_text(coords[0], coords[1], anchor= tk.NW, fill="black",font=font_titolo, text= "Aggiunte")

        ### AGGIUNTE ###
        self.canvas.create_text(coords[0], coords[3]-resolutionConverter(5), anchor= tk.SW, fill="black",font=font_aggiunte, text= self.testo_aggiunte, width = (coords[2]-coords[0]))

    def scritte(self, coords, pizza):

        font_nome = "Times " + str(resolutionConverter(20)) + " bold"
        font_prezzo = "Times " + str(resolutionConverter(20)) + " bold"
        font_ingredienti = "Times " + str(resolutionConverter(15))
        font_tipo = "Times " + str(resolutionConverter(36)) + " bold"

        colori = {"Pizze classiche" : "green", "Pizze bianche" : "blue", "Pizze conditissime" : "red"}

        if "nome" in pizza:

            if pizza["nome"] == "Estiva":
                pizza["ingredienti"] += " tutto fuori cottura"
            
            ### NOME ###
            self.canvas.create_text(coords[0]+resolutionConverter(5), coords[1]+resolutionConverter(5), anchor= tk.NW, fill="black",font=font_nome, text= pizza["nome"])

            ### PREZZO ###
            self.canvas.create_text(coords[2]-resolutionConverter(10), coords[1]+resolutionConverter(10), anchor= tk.NE, fill="red",font=font_prezzo, text= pizza["prezzo"])

            ### INGREDIENTI ###
            self.ScritteIngredienti.append(self.canvas.create_text(coords[0]+resolutionConverter(5), (coords[3]+coords[1])/2-resolutionConverter(10), anchor= tk.NW, fill="black",font=font_ingredienti, text= pizza["ingredienti"], width=(self.cell_dimension[0]-resolutionConverter(10))))
        else:
            ### TIPO ###
            self.canvas.create_text(coords[0]+resolutionConverter(5), coords[3]-resolutionConverter(25), anchor= tk.SW, fill=colori[pizza["tipo"]], font=font_tipo, text= pizza["tipo"])

    def updateScritte(self):    #this function updates the text boxes
        lingua = self.getLingua()
        if lingua == "nome_italiano":   #modifies the ingredients
            testoLingua = "ingredienti"
        elif lingua == "nome_inglese":
            testoLingua = "ingredientiInglese"
        j = 0
        for i in self.elenco_pizze:
            if "id" in i:
                self.canvas.itemconfig(self.ScritteIngredienti[j], text=i[testoLingua])
                j += 1

    def getLingua(self):
        return self.db.getCurrentLanguage()

class Fullscreen:
    def __init__(self):
        fname = "jsonBins.json"
        self.p = Pizzas(fname)
        self.p.downloadAllFromCloud()
        
        self.window = tk.Tk()
        self.window.attributes('-fullscreen', True)  
        self.fullScreenState = False
        self.window.bind("<F12>", self.close)
        self.window.bind("<F11>", self.toggleFullScreen)
        self.window.bind("<Escape>", self.quitFullScreen)
        self.screenDimension = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        global ris
        ris = self.screenDimension[0]
        self.window.config(cursor="none")
        self.pizze = self.pizzeCreator()
        self.aggiunte = self.aggiunteCreator()
        self.menu = Elenco(self.window, self.pizze, self.aggiunte, [resolutionConverter(25), resolutionConverter(25), self.screenDimension[0]-resolutionConverter(50), self.screenDimension[1]-resolutionConverter(100)], fname)

        self.ShowAll()
        self.Update()
        self.window.mainloop()

    def aggiunteCreator(self):
        aggiunte = []
        data = self.p.get_aggiunte()
        for i in data:
            aggiunte.append({
                "nome" : (", ".join(str(x) for x in i["nome_aggiunta"].split(","))).capitalize(),
                "prezzo" : '€ {:,.2f}'.format(i["prezzo_aggiunta"])
            })
        return aggiunte

    def pizzeCreator(self):     ### crea un dizionario con tutte le pizze e i suoi atributi
        pizze = []
        data = self.p.get_pizzas(True)
        tipo_pizza = ""

        for i in data:
            if i["nome_tipo"] != tipo_pizza:
                pizze.append({"tipo" : i["nome_tipo"]})
                tipo_pizza = i["nome_tipo"]
            pizze.append({
                        "id" : i["id"],
                        "nome": i["nomePizza"],
                        "tipo" : i["nome_tipo"],
                        "prezzo" : '€ {:,.2f}'.format(i["prezzo"]),
                        "ingredienti" : (", ".join(str(x) for x in i["ingredienti"].split(","))).capitalize(),
                        "ingredientiInglese" : (", ".join(str(x) for x in i["ingredientiInglese"].split(","))).capitalize()
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

def resolutionConverter(n):
    #converts the ratio from 2560x1440 to ris
    return int(n/(2560/ris))

if __name__ == '__main__':
    app = Fullscreen()
