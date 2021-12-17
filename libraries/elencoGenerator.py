import math
from libraries.database import database
import tkinter as tk
from libraries.windowsSpecs import WindowSpecs
from PIL import ImageTk,Image 
import os

class Elenco:
    def __init__(self, window, elenco_pizze, margini, jsonData, color, screenDimension):
        self.window = window
        self.elenco_pizze = elenco_pizze
        self.alleggeni = self.loadAllergeni()
        self.colors = color
        self.screenDimension = screenDimension
        self.windowSpecs = WindowSpecs(self.screenDimension)
        self.colonne_max = 5
        self.righe_max = math.ceil(len(self.elenco_pizze)/self.colonne_max)   #numero di pizze per colonna
        self.margini = margini
        self.screenDimension = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        self.cell_dimension = [(self.margini[2]-self.margini[0])/self.colonne_max, (self.margini[3]-self.margini[1])/self.righe_max]
        
        self.db = database("localhost", jsonData["dbUserName"], jsonData["dbPassword"], jsonData["dbData"])

    
    def show(self, update=False):
        if update:
            self.updateScritte()
        else:
            self.canvas = tk.Canvas(self.window, width =self.screenDimension[0], height = self.screenDimension[1])
            self.canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            self.canvas.configure(background = self.colors["background"])
            self.canvas.pack()

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
        coords = [self.windowSpecs.resolutionConverter(25), self.margini[3]+10, (self.margini[2]*(4/5)+self.windowSpecs.resolutionConverter(500)), self.screenDimension[1]-self.windowSpecs.resolutionConverter(20)]
        self.canvas.pack()

        font_titolo = "Times " + str(self.windowSpecs.resolutionConverter(22)) + " bold"
        font_aggiunte = "Times " + str(self.windowSpecs.resolutionConverter(16))

        self.ScritteAggiunte = {}
        ### TITOLO ###
        canvas = self.canvas.create_text(coords[0], coords[1], anchor= tk.NW, fill=self.colors["generic_text"],font=font_titolo, text= "Aggiunte")
        self.ScritteAggiunte.update({'titolo': canvas})

        ### AGGIUNTE ###
        canvas = self.canvas.create_text(coords[0], coords[3]-self.windowSpecs.resolutionConverter(5), anchor= tk.SW, fill=self.colors["generic_text"],font=font_aggiunte, text= self.testo_aggiunte, width = (coords[2]-coords[0]))
        self.ScritteAggiunte.update({'aggiunte': canvas})

    def showAllergeni():
        pass

    def scritte(self, coords, pizza):

        font_nome = "Times " + str(self.windowSpecs.resolutionConverter(20)) + " bold"
        font_prezzo = "Times " + str(self.windowSpecs.resolutionConverter(18)) + " bold"
        font_ingredienti = "Times " + str(self.windowSpecs.resolutionConverter(15))
        font_tipo = "Times " + str(self.windowSpecs.resolutionConverter(36)) + " bold"

        if "nome" in pizza:

            if pizza["nome"] == "Estiva":
                pizza["ingredienti"] += " tutto fuori cottura"
            
            ### NOME ###
            self.canvas.create_text(coords[0]+self.windowSpecs.resolutionConverter(5), coords[1]+self.windowSpecs.resolutionConverter(5), anchor= tk.NW, fill=self.colors["titolo"],font=font_nome, text= pizza["nome"])
            self.canvas.create_image(10, coords[1]+self.windowSpecs.resolutionConverter(5)+5, anchor=tk.NW, image=self.alleggeni["glutine"])

            ### PREZZO ###
            self.canvas.create_text(coords[2]-self.windowSpecs.resolutionConverter(10), coords[1]+self.windowSpecs.resolutionConverter(10), anchor= tk.NE, fill=self.colors["price"],font=font_prezzo, text= pizza["prezzo"])

            ### INGREDIENTI ###
            self.ScritteIngredienti.append(self.canvas.create_text(coords[0]+self.windowSpecs.resolutionConverter(5), (coords[3]+coords[1])/2-self.windowSpecs.resolutionConverter(10), anchor= tk.NW, fill=self.colors["generic_text"],font=font_ingredienti, text= pizza["ingredienti"], width=(self.cell_dimension[0]-self.windowSpecs.resolutionConverter(10))))
        else:
            ### TIPO ###
            a = 3
            self.canvas.create_line(coords[0], coords[1], coords[2]-self.windowSpecs.resolutionConverter(40), coords[1], fill="#ff8000", width="3")
            self.canvas.create_line(coords[0], coords[3]-self.windowSpecs.resolutionConverter(15), coords[2]-self.windowSpecs.resolutionConverter(40), coords[3]-self.windowSpecs.resolutionConverter(15), fill="#ff8000", width="3")

            self.canvas.create_text(coords[0]+self.windowSpecs.resolutionConverter(5)+a, coords[3]-self.windowSpecs.resolutionConverter(25)+a, anchor= tk.SW, fill="#BBBBBB", font=font_tipo, text= pizza["tipo"])
            self.canvas.create_text(coords[0]+self.windowSpecs.resolutionConverter(5)+1, coords[3]-self.windowSpecs.resolutionConverter(25)+1, anchor= tk.SW, fill="#000000", font=font_tipo, text= pizza["tipo"])
            self.canvas.create_text(coords[0]+self.windowSpecs.resolutionConverter(5)-1, coords[3]-self.windowSpecs.resolutionConverter(25)-1, anchor= tk.SW, fill="#000000", font=font_tipo, text= pizza["tipo"])

            self.canvas.create_text(coords[0]+self.windowSpecs.resolutionConverter(5), coords[3]-self.windowSpecs.resolutionConverter(25), anchor= tk.SW, fill=self.colors["p_tipo"], font=font_tipo, text= pizza["tipo"])

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

    def loadAllergeni(self):
        targetFile = os.path.join(os.path.curdir, 'resources', "allergeni")
        resizeFormat = (int(119/4), int(121/4))

        uova = ImageTk.PhotoImage(Image.open(os.path.join(targetFile, "uova.png")).resize(resizeFormat, Image.ANTIALIAS))
        pesce = ImageTk.PhotoImage(Image.open(os.path.join(targetFile, "pesce.png")))
        noci = ImageTk.PhotoImage(Image.open(os.path.join(targetFile, "noci.png")))
        soia = ImageTk.PhotoImage(Image.open(os.path.join(targetFile, "soia.png")))
        glutine = ImageTk.PhotoImage(Image.open(os.path.join(targetFile, "glutine.png")).resize(resizeFormat, Image.ANTIALIAS))
        latticini = ImageTk.PhotoImage(Image.open(os.path.join(targetFile, "latticini.png")))
        return { "uova" : uova, "pesce" : pesce, "noci" : noci, "soia" : soia, "glutine" : glutine, "latticini" : latticini }

    def getLingua(self):
        return self.db.getCurrentLanguage()
