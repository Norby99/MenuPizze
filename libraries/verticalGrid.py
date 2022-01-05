import math
from libraries.database import database
import tkinter as tk
from libraries.windowSpecs import WindowSpecs
from libraries.gridTitleCell import TitleCell
from libraries.gridPizzaCell import PizzaCell
from libraries.gridAggiuntaCell import AggiuntaCell
from PIL import ImageTk,Image 
import os

class VerticalGrid:
    def __init__(self, window, objectsList, margini, jsonData, color, maxColumns=5, ):
        self.window = window
        self.objectsList = objectsList
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
            self.canvas = tk.Canvas(self.window, bg=self.colors["background"], width=self.margin[2], height=self.margin[3], highlightthickness=0, bd=0)   # creating main canvas
            self.canvas.place(x=self.margin[0], y=self.margin[1], anchor=tk.NW)

            cellPosition = [self.margin[0], self.margin[1]]
            self.ScritteIngredienti = []
            for object in self.objectsList:
                newCellExists = False
                if object["objType"] == "title": # populating the grid with the cells
                    tempCell = TitleCell(self.window, object["tipo"], self.colors["p_tipo"], cellPosition, self.cell_width)
                    newCellExists = True
                elif object["objType"] == "pizza":
                    pizzaAllergens = [self.allergens[x] for x in object["allergens"]]    # filters the allergens to show only those that are in the pizza
                    tempCell = PizzaCell(self.window, object["nome"], self.colors["titolo"], object["prezzo"], self.colors["price"], {"nome_italiano" : object["ingredienti"], "nome_inglese" : object["ingredientiInglese"]}, self.colors["generic_text"], pizzaAllergens, cellPosition, self.cell_width)
                    newCellExists = True
                elif object["objType"] == "aggiunta":
                    tempCell = AggiuntaCell(self.window, {"nome_italiano" : object["nome_aggiunta"], "nome_inglese" : object["nome_inglese"]}, self.colors["generic_text"], object["prezzo"], self.colors["price"], cellPosition, self.cell_width)
                    newCellExists = True
                elif object["objType"] == "insalata":
                    pass
                    #newCellExists = True

                if newCellExists:
                    self.cells.append(tempCell)
                    if tempCell.getBottomCoordinate() > self.margin[3]: # getting next element position
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
        testoLingua = self.getLingua()

        for i in self.cells:
            if hasattr(i, 'update'):
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
