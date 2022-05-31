from libraries.cells.AbstractCell import Cell
import tkinter as tk
import tkinter.font as TkFont

class AggiuntaCell(Cell):
    """ This cell contains the aggiunta name and the price """

    def __init__(self, window, name, nameColor, price, priceColor, position, width, proportion=12):
        super().__init__(window, position, width, proportion)
        self.name = name    # name setup
        self.nameColor = nameColor
        self.nameFont = TkFont.Font(family="Times", size=self.windowSpecs.resolutionConverter(15), weight='bold')
        self.price = price  # price setup
        self.priceColor = priceColor
        self.priceFont = TkFont.Font(family="Times", size=self.windowSpecs.resolutionConverter(18), weight='bold')

        self.createName()
        self.createPrice()

    def createName(self):
        self.textNamePos = [self.windowSpecs.resolutionConverter(5), 0]
        self.textName = self.canvas.create_text(self.textNamePos[0], self.textNamePos[1], anchor= tk.NW, fill=self.nameColor,font=self.nameFont, text=self.name[next(iter(self.name))])

    def createPrice(self):
        self.textPricePos = [self.dimensions[0]-self.windowSpecs.resolutionConverter(10), 0]
        self.textPrice = self.canvas.create_text(self.textPricePos[0], self.textPricePos[1], anchor= tk.NE, fill=self.priceColor,font=self.priceFont, text=self.price)

    def setNameFont(self, font):
        self.nameFont = font

    def setPriceFont(self, font):
        self.priceFont = font

    def update(self, language):
        self.canvas.itemconfig(self.textName, text=self.name[language])
