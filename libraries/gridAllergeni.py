from libraries.gridCell import Cell
import tkinter as tk
import tkinter.font as TkFont

class AllergeniCell(Cell):
    """ This cell contains the legend of Allergens """

    def __init__(self, window, allergen, textColor, position, width, proportion=15):
        super().__init__(window, position, width, proportion=proportion)
        self.backGroundColor = window["background"]
        self.width = width

        self.allergens = allergen["first"] + allergen["second"]

        self.textColor = textColor
        self.font = TkFont.Font(family="Times", size=self.windowSpecs.resolutionConverter(15), weight='bold')

        self.createAllergens()

    def createAllergens(self):
        self.textName =  self.canvas.create_text(0, 0, anchor= tk.NW, fill=self.textColor, font=self.font, text=self.allergens[0])
        self.textName =  self.canvas.create_text(self.width, 0, anchor= tk.NE, fill=self.textColor, font=self.font, text=self.allergens[2])

    def setAllergensFontFont(self, font):
        self.font = font
