import tkinter as tk
from libraries.utils.utils import capfirst
from libraries.utils.languageHandler import LanguageHandler
from libraries.utils.windowSpecs import WindowSpecs
from libraries.cells.AbstractCell import Cell
from libraries.cells.titleCell import TitleCell
from libraries.cells.pizzaCell import PizzaCell
from libraries.cells.aggiuntaCell import AggiuntaCell
from libraries.cells.insalataCell import InsalataCell
from libraries.cells.allergeniCell import AllergeniCell
from libraries.cells.newColumn import NewColumnCell
from libraries.cells.imageCell import ImageCell
from libraries.cells.socialLogos import SocialLogos
from libraries.cells.simpleTextCell import SimpleTextCell
from libraries.cells.menuSettimanaCell import MenuSettimanaCell
import json
from PIL import ImageTk,Image 
import os
from abc import ABC

class PizzaMenu(ABC):

    DEFAULT_NEWLINE = [{ "objType" : "NewLine" }]
    _font_colors: dict

    def loadJsonData(self, fname):
        with open(fname) as f:
            return json.load(f)

    def connect2db(self, data):
        self.LHandler = LanguageHandler(data['languageSite'] + "/" + data['restaurantName'] + ".php", data['defaultLanguage'], token=data['m_key'])

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

    def simpleTextCreator(self, text_list):
        """
        creates a dictionary with all the simple text
        """

        text = []

        for i in text_list:
            text.append({
                "objType" : "simple_text",
                "text" : i,
                "font_size" : 34
            })

        return text

    def menuSettimanaCreator(self):
        """
        Creates menu della settimana
        """

        # TODO: this is hardcoded and needs to be changed
        menuSettimana = [
            "Lunedi - Cappelletti",
            "Mercoledi - Pollo arrosto",
            "Venerdi - Patatine fritte"
        ]

        return [{
            "objType" : "menu_settimana",
            "title" : "Menu della settimana",
            "body" : menuSettimana
        }]

    def aggiunteCreator(self):
        """
        creates a dictionary with all the aggiunte
        """
        aggiunte = self.pizza.get_aggiunte()
        for i in aggiunte:
            i["objType"] = "aggiunta"
            i["nome_aggiunta"] = capfirst(i["nome_aggiunta"])
            i["nome_inglese"] = capfirst(i["nome_inglese"])
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

        insalate.insert(0, {"objType" : "title", "tipo" : "Insalate  (+spianata)"})  # added title aggiunte

        return insalate

    def allergeniCreator(self):
        allergens = self.loadAllergeni(scale=2)
        allergensList = []
        keys = sorted(allergens.keys())

        for i in range(len(keys) -1):
            allergensList.append({
                "objType" : "allergeni",
                "first" : [capfirst(keys[i]), allergens[keys[i]]],
                "second" : [capfirst(keys[i+1]), allergens[keys[i+1]]]
            })
        allergensList.insert(0, {"objType" : "title", "tipo" : "Legenda allergeni"})  # added title Allergeni

        return allergensList

    def logoCreator(self):
        targetFile = os.path.join(os.path.curdir, 'resources', 'images')
        image = Image.open(os.path.join(targetFile, "Piccola-Italia-logo.png"))
        return [{
            "objType" : "image",
            "image" : image
        }]

    def createCells(self, objList, allergens, cellWidth):
        cellPosition = [0, 0]
        cells = []

        for obj in objList:
            tempCell = False
            if obj["objType"] == "title": # populating the grid with the cells
                tempCell = TitleCell(self.window, obj["tipo"], self._font_colors["p_tipo"], cellPosition, cellWidth)
            elif obj["objType"] == "pizza":
                pizzaAllergens = [allergens[x] for x in obj["allergens"]]    # filters the allergens to show only those that are in the pizza
                tempCell = PizzaCell(self.window, obj["nome"], self._font_colors["titolo"], obj["prezzo"], self._font_colors["price"], {"nome_italiano" : obj["ingredienti"], "nome_inglese" : obj["ingredientiInglese"]}, self._font_colors["generic_text"], pizzaAllergens, cellPosition, cellWidth)
            elif obj["objType"] == "aggiunta":
                tempCell = AggiuntaCell(self.window, {"nome_italiano" : obj["nome_aggiunta"], "nome_inglese" : obj["nome_inglese"]}, self._font_colors["generic_text"], obj["prezzo"], self._font_colors["price"], cellPosition, cellWidth)
            elif obj["objType"] == "insalata":
                insalataAllergens = [allergens[x] for x in obj["allergens"]]    # filters the allergens to show only those that are in the pizza
                tempCell = InsalataCell(self.window, obj["nome"], self._font_colors["titolo"], obj["prezzo"], self._font_colors["price"], {"nome_italiano" : obj["ingredienti"], "nome_inglese" : obj["ingredientiInglese"]}, self._font_colors["generic_text"], insalataAllergens, cellPosition, cellWidth)
            elif obj["objType"] == "allergeni":
                tempCell = AllergeniCell(self.window, obj, self._font_colors["generic_text"], cellPosition, cellWidth)
            elif obj["objType"] == "NewLine":
                tempCell = NewColumnCell(self.window, cellPosition, cellWidth)
            elif obj["objType"] == "image":
                tempCell = ImageCell(self.window, obj["image"], cellPosition, cellWidth)
            elif obj["objType"] == "logosContainer":
                tempCell = SocialLogos(self.window, obj["images"], cellPosition, cellWidth)
            elif obj["objType"] == "simple_text":
                tempCell = SimpleTextCell(self.window, obj["text"], self._font_colors["generic_text"], obj["font_size"], cellPosition, cellWidth)
            elif obj["objType"] == "menu_settimana":
                tempCell = MenuSettimanaCell(self.window, obj["title"], obj["body"], cellPosition, cellWidth)
            else:
                raise ValueError(f'The cell type {obj["objType"]} does not exist.')

            if tempCell:
                cells.append(tempCell)
        return cells

    def loadSocialLogos(self):
        """
        Loads all the social logos and returns a list with them
        """

        targetFile = os.path.join(os.path.curdir, 'resources', 'social_logos')

        logos = []
        for image_name in os.listdir(targetFile):
            logos.append(Image.open(os.path.join(targetFile, image_name)))

        return [{
            "objType" : "logosContainer",
            "images" : logos
        }]

    def loadAllergeni(self, scale=1):
        """
        Loads images of allergens
        @param scale is the scale of the images based on the default resolution
        """
        targetFile = os.path.join(os.path.curdir, 'resources', "allergeni")
        resizeFormat = (self.windowSpecs.resolutionConverter(119/6*scale), self.windowSpecs.resolutionConverter(121/6*scale))

        uova = ImageTk.PhotoImage(Image.open(os.path.join(targetFile, "uova.png")).resize(resizeFormat, Image.ANTIALIAS))
        pesce = ImageTk.PhotoImage(Image.open(os.path.join(targetFile, "pesce.png")).resize(resizeFormat, Image.ANTIALIAS))
        noci = ImageTk.PhotoImage(Image.open(os.path.join(targetFile, "noci.png")).resize(resizeFormat, Image.ANTIALIAS))
        soia = ImageTk.PhotoImage(Image.open(os.path.join(targetFile, "soia.png")).resize(resizeFormat, Image.ANTIALIAS))
        glutine = ImageTk.PhotoImage(Image.open(os.path.join(targetFile, "glutine.png")).resize(resizeFormat, Image.ANTIALIAS))
        latticini = ImageTk.PhotoImage(Image.open(os.path.join(targetFile, "latticini.png")).resize(resizeFormat, Image.ANTIALIAS))
        return { "uova" : uova, "pesce" : pesce, "noci" : noci, "soia" : soia, "glutine" : glutine, "latticini" : latticini }

    def setFontColors(self, colors) -> None:
        """
        Sets the font colors
        """
        self._font_colors = colors


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

    def show(self, menu):
        """
        Shows all menu.
        NOTE : Must be call before update
        """
        self.CACHEDMENU = menu
        if isinstance(menu, list):
            for i in menu:
                i.show()
        else:
            menu.show()

    def update(self):
        if isinstance(self.CACHEDMENU, list):   # if there are more than 1 vertical grids
            for i in self.CACHEDMENU:
                i.updateCells()
        else:
            self.CACHEDMENU.updateCells()
        self.window.after(5000, self.update)
