import math
from libraries.database import database
import tkinter as tk
from libraries.windowSpecs import WindowSpecs
from libraries.gridTitleCell import TitleCell
from libraries.gridPizzaCell import PizzaCell
from PIL import ImageTk,Image 
import os

#!  self.canvas.create_image(10, coords[1]+self.windowSpecs.resolutionConverter(5)+5, anchor=tk.NW, image=self.alleggeni["glutine"])
#? add next cell Y pos by the previouse one hight and set a default hight

class VerticalGrid:
    def __init__(self, window, elenco_pizze, margini, jsonData, color, maxColumns=5):
        self.window = window
        self.elenco_pizze = elenco_pizze
        self.alleggeni = self.loadAllergeni()
        self.colors = color
        self.windowSpecs = WindowSpecs()
        self.maxColumns = maxColumns
        self.righe_max = math.ceil(len(self.elenco_pizze)/self.maxColumns)   #numero di pizze per colonna
        self.margini = margini
        self.cell_dimension = [(self.margini[2]-self.margini[0])/self.maxColumns, (self.margini[3]-self.margini[1])/self.righe_max]
        self.cells = []

        self.db = database("localhost", jsonData["dbUserName"], jsonData["dbPassword"], jsonData["dbData"])

    def show(self, update=False):
        if update:
            self.updateScritte()
        else:
            self.canvas = tk.Canvas(self.window, bg=self.colors["background"], width=self.margini[2], height=self.margini[3])   # creating main canvas
            self.canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

            x = 0
            y = 0
            self.ScritteIngredienti = []
            for pizza in self.elenco_pizze:
                if y >= self.righe_max:
                    y = 0
                    x += 1

                cellPosition = [self.margini[0]+self.cell_dimension[0]*x, self.margini[1]+self.cell_dimension[1]*y]
                if "nome" in pizza: # populating the grid with the cells
                    tempCell = PizzaCell(self.window, pizza["nome"], self.colors["titolo"], pizza["prezzo"], self.colors["price"], {"ingredienti" : pizza["ingredienti"], "ingredientiInglese" : pizza["ingredientiInglese"]}, self.colors["generic_text"], cellPosition, self.cell_dimension)
                else:
                    tempCell = TitleCell(self.window, pizza["tipo"], self.colors["p_tipo"], cellPosition, self.cell_dimension)
                self.cells.append(tempCell)
                y += 1

    def showAggiunte(self):
        coords = [self.windowSpecs.resolutionConverter(25), self.margini[3]+10, (self.margini[2]*(4/5)+self.windowSpecs.resolutionConverter(500)), self.margini[3]-self.windowSpecs.resolutionConverter(20)]
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

    def updateCells(self):    #this function updates the text boxes
        lingua = self.getLingua()
        if lingua == "nome_italiano":   #modifies the ingredients
            testoLingua = "ingredienti"
        elif lingua == "nome_inglese":
            testoLingua = "ingredientiInglese"

        for i in self.cells:
            if isinstance(i, PizzaCell):
                i.update(testoLingua)

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
