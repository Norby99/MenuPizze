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
from libraries.cells.subtitlePriceCell import SubtitlePriceCell
from libraries.resourceHandler import Recources
import json
from PIL import ImageTk,Image 
import os
from abc import ABC

class PizzaMenu(ABC):

    _font_colors: dict
    _columnWidth: float

    allergens: dict

    resources: Recources

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
        data = self.resources.get_pizzas(True)
        tipo_pizza = ""

        for i in data:
            if (i["nome_tipo"] in pizzaType) or pizzaType == "*":
                if i["nome_tipo"] != tipo_pizza:
                    tipo_pizza = i["nome_tipo"]
                    pizze.append(TitleCell(self.window, i["nome_tipo"], self._font_colors["p_tipo"], [0, 0], self._columnWidth))

                pizzaAllergens = [self.allergens[x] for x in i["allergeni"]]    # filters the allergens to show only those that are in the pizza
                pizze.append(PizzaCell(self.window, i["nomePizza"], self._font_colors["titolo"], '€ {:,.2f}'.format(float(i["prezzo"])), self._font_colors["price"], {"nome_italiano" : capfirst(", ".join(str(x) for x in i["ingredienti"].split(","))), "nome_inglese" : capfirst(", ".join(str(x) for x in i["ingredientiInglese"].split(",")))}, self._font_colors["generic_text"], pizzaAllergens, [0, 0], self._columnWidth))
        
        return pizze

    def simpleTextCreator(self, text_list):
        """
        creates a dictionary with all the simple text
        """

        text = []

        for i in text_list:
            text.append(SimpleTextCell(self.window, i, self._font_colors["generic_text"], 34, [0, 0], self._columnWidth))

        return text

    def newColumnCreator(self):
        return [NewColumnCell(self.window, [0, 0], self._columnWidth)]

    def menuSettimanaCreator(self):
        """
        Creates menu della settimana
        """
        menu_settimanale = self.resources.get_menu_settimanale()

        if len(menu_settimanale) == 0:
            return []
        
        widget_list = []
        widget_list.append(TitleCell(self.window, "Menu della settimana", self._font_colors["p_tipo"], [0, 0], self._columnWidth))

        for i in menu_settimanale:
            widget_list.append(SubtitlePriceCell(self.window, i["day"], self._font_colors["titolo"], '€ {:,.2f}'.format(float(i["price"])), self._font_colors["price"], i["meal"], self._font_colors["generic_text"], [0, 0], self._columnWidth))

        return widget_list

    def aggiunteCreator(self):
        """
        creates a dictionary with all the aggiunte
        """
        aggiunteCell = []
        aggiunteCell.append(TitleCell(self.window, "Aggiunte", self._font_colors["p_tipo"], [0, 0], self._columnWidth))

        aggiunte = self.resources.get_aggiunte()
        for i in aggiunte:
            aggiunteCell.append(AggiuntaCell(self.window, {"nome_italiano" : capfirst(i["nome_aggiunta"]), "nome_inglese" : capfirst(i["nome_inglese"])}, self._font_colors["generic_text"], '€ {:,.2f}'.format(float(i["prezzo"])), self._font_colors["price"], [0, 0], self._columnWidth))

        return aggiunteCell

    def insalateCreator(self):
        """
        creates a dictionary with all the "insalate"
        """
        insalate = []
        data = self.resources.get_insalate(True)

        insalate.append(TitleCell(self.window, "Insalate  (+spianata)", self._font_colors["p_tipo"], [0, 0], self._columnWidth))

        for i in data:
            insalataAllergens = [self.allergens[x] for x in i["allergeni"]]    # filters the allergens to show only those that are in the pizza
            insalate.append(InsalataCell(self.window, i["nomeInsalata"], self._font_colors["titolo"], '€ {:,.2f}'.format(float(i["prezzo"])), self._font_colors["price"], {"nome_italiano" : capfirst(", ".join(str(x) for x in i["ingredienti"].split(","))), "nome_inglese" : capfirst(", ".join(str(x) for x in i["ingredientiInglese"].split(",")))}, self._font_colors["generic_text"], insalataAllergens, [0, 0], self._columnWidth))

        return insalate

    def allergeniCreator(self):
        allergens = self.loadAllergeni(scale=2)
        allergensList = []

        allergensList.append(TitleCell(self.window, "Legenda allergeni", self._font_colors["p_tipo"], [0, 0], self._columnWidth))

        names, images = zip(*allergens.items())
        i = 0
        while (i < len(allergens)):
            if i+1 < len(allergens):
                allergensList.append(AllergeniCell(self.window, self._font_colors["generic_text"], [0, 0], self._columnWidth, names[i], images[i], names[i+1], images[i+1]))
            else:
                allergensList.append(AllergeniCell(self.window, self._font_colors["generic_text"], [0, 0], self._columnWidth, names[i], images[i]))
            
            i += 2

        return allergensList

    def logoCreator(self):
        targetFile = os.path.join(os.path.curdir, 'resources', 'images')
        image = Image.open(os.path.join(targetFile, "Piccola-Italia-logo.png"))
        return [ImageCell(self.window, image, [0, 0], self._columnWidth)]

    def loadSocialLogos(self):
        """
        Loads all the social logos and returns a list with them
        """
        targetFile = os.path.join(os.path.curdir, 'resources', 'social_logos')

        logos = []
        for image_name in os.listdir(targetFile):
            logos.append(Image.open(os.path.join(targetFile, image_name)))

        return [SocialLogos(self.window, logos, [0, 0], self._columnWidth)]

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
