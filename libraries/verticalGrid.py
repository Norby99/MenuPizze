import math
from libraries.database import database
import tkinter as tk
from libraries.windowSpecs import WindowSpecs
from libraries.gridTitleCell import TitleCell
from libraries.gridPizzaCell import PizzaCell
from PIL import ImageTk,Image 
import os

class VerticalGrid:
    def __init__(self, window, elenco_pizze, margini, jsonData, color, maxColumns=5):
        self.window = window
        self.elenco_pizze = elenco_pizze
        self.allergens = self.loadAllergeni()
        self.colors = color
        self.windowSpecs = WindowSpecs()
        self.maxColumns = maxColumns
        self.margin = margini
        self.cell_width = (self.margin[2]-self.margin[0])/self.maxColumns
        self.cells = []

        self.db = database("localhost", jsonData["dbUserName"], jsonData["dbPassword"], jsonData["dbData"])

    def show(self, update=False):
        if update:
            self.updateScritte()
        else:
            self.canvas = tk.Canvas(self.window, bg=self.colors["background"], width=self.margin[2], height=self.margin[3])   # creating main canvas
            self.canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

            cellPosition = [self.margin[0], self.margin[1]]
            self.ScritteIngredienti = []
            for pizza in self.elenco_pizze:
                if "nome" in pizza: # populating the grid with the cells
                    pizzaAllergens = [self.allergens[x] for x in pizza["allergens"]]    # filters the allergens to show only those that are in the pizza
                    tempCell = PizzaCell(self.window, pizza["nome"], self.colors["titolo"], pizza["prezzo"], self.colors["price"], {"ingredienti" : pizza["ingredienti"], "ingredientiInglese" : pizza["ingredientiInglese"]}, self.colors["generic_text"], pizzaAllergens, cellPosition, self.cell_width)
                else:
                    tempCell = TitleCell(self.window, pizza["tipo"], self.colors["p_tipo"], cellPosition, self.cell_width)
                self.cells.append(tempCell)

                if tempCell.getBottomCoordinate() > self.margin[3]:
                    cellPosition = [tempCell.getRightCoordinate(), self.margin[1]]

                tempCell.setPostion(cellPosition)
                cellPosition[1] = tempCell.getBottomCoordinate()

                if tempCell.getRightCoordinate() > self.margin[2]:
                    raise IndexError("Given too many Cell's")

    def showAggiunte(self):
        coords = [self.windowSpecs.resolutionConverter(25), self.margin[3]+10, (self.margin[2]*(4/5)+self.windowSpecs.resolutionConverter(500)), self.margin[3]-self.windowSpecs.resolutionConverter(20)]
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
        resizeFormat = (int(119/6), int(121/6))

        uova = ImageTk.PhotoImage(Image.open(os.path.join(targetFile, "uova.png")).resize(resizeFormat, Image.ANTIALIAS))
        pesce = ImageTk.PhotoImage(Image.open(os.path.join(targetFile, "pesce.png")).resize(resizeFormat, Image.ANTIALIAS))
        noci = ImageTk.PhotoImage(Image.open(os.path.join(targetFile, "noci.png")).resize(resizeFormat, Image.ANTIALIAS))
        soia = ImageTk.PhotoImage(Image.open(os.path.join(targetFile, "soia.png")).resize(resizeFormat, Image.ANTIALIAS))
        glutine = ImageTk.PhotoImage(Image.open(os.path.join(targetFile, "glutine.png")).resize(resizeFormat, Image.ANTIALIAS))
        latticini = ImageTk.PhotoImage(Image.open(os.path.join(targetFile, "latticini.png")).resize(resizeFormat, Image.ANTIALIAS))
        return { "uova" : uova, "pesce" : pesce, "noci" : noci, "soia" : soia, "glutine" : glutine, "latticini" : latticini }

    def getLingua(self):
        return self.db.getCurrentLanguage()
