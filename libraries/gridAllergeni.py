from libraries.gridCell import Cell
import tkinter as tk
import tkinter.font as TkFont

class AllergeniCell(Cell):
    """ This cell contains the legend of Allergens """

    def __init__(self, window, allergens, textColor, position, width):
        super().__init__(window, position, width, proportion=1)

        del allergens["objType"]
        self.allergens = allergens
        
        self.textColor = textColor
        self.allergensFont = TkFont.Font(family="Times", size=self.windowSpecs.resolutionConverter(15), weight='bold')
        self.canvas.configure(bg='cyan')    #! testing

        self.createAllergens()

    def createAllergens(self):
        self.textNamePos = [self.windowSpecs.resolutionConverter(5), self.windowSpecs.resolutionConverter(5)]
        self.textName = self.canvas.create_text(self.textNamePos[0], self.textNamePos[1], anchor= tk.NW, fill=self.nameColor,font=self.nameFont, text=self.name[next(iter(self.name))])

    def setAllergensFontFont(self, font):
        self.allergensFont = font
