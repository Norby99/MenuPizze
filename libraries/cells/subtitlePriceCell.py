from libraries.cells.AbstractCell import Cell
import tkinter as tk
import tkinter.font as TkFont

class SubtitlePriceCell(Cell):
    """
    This cell contains:
    - pizza name
    - price
    - ingredients
    - allergens
    """
    def __init__(self, window, title, titleColor, price, priceColor, description, descriptionColor, position, width, proportion=5.76):
        super().__init__(window, position, width, proportion)
        self.title = title    # title setup
        self.titleColor = titleColor
        self.titleFont = TkFont.Font(family="Times", size=self.windowSpecs.resolutionConverter(20), weight='bold')
        self.price = price  # price setup
        self.priceColor = priceColor
        self.priceFont = TkFont.Font(family="Times", size=self.windowSpecs.resolutionConverter(18), weight='bold')
        self.description = description  # ingredients setup
        self.descriptionColor = descriptionColor
        self.descriptionFont = TkFont.Font(family="Times", size=self.windowSpecs.resolutionConverter(16))

        self.createTitle()
        self.createPrice()
        self.createDescription()

    def createTitle(self):
        self.textNamePos = [self.windowSpecs.resolutionConverter(5), 0]
        self.textName = self.canvas.create_text(self.textNamePos[0], self.textNamePos[1], anchor= tk.NW, fill=self.titleColor,font=self.titleFont, text=self.title)

    def createPrice(self):
        self.textPricePos = [self.dimensions[0]-self.windowSpecs.resolutionConverter(10), 0]
        self.textPrice = self.canvas.create_text(self.textPricePos[0], self.textPricePos[1], anchor= tk.NE, fill=self.priceColor,font=self.priceFont, text=self.price)

    def createDescription(self):
        self.textDescriptionPos = [self.windowSpecs.resolutionConverter(5), self.dimensions[1]/2-self.windowSpecs.resolutionConverter(13)]
        if isinstance(self.description, str):
            self.textDescription = self.canvas.create_text(self.textDescriptionPos[0], self.textDescriptionPos[1], anchor= tk.NW, fill=self.descriptionColor,font=self.descriptionFont, text=self.description, width=(self.dimensions[0]-self.windowSpecs.resolutionConverter(5)))
        if isinstance(self.description, dict):
            self.textDescription = self.canvas.create_text(self.textDescriptionPos[0], self.textDescriptionPos[1], anchor= tk.NW, fill=self.descriptionColor,font=self.descriptionFont, text=self.description[next(iter(self.description))], width=(self.dimensions[0]-self.windowSpecs.resolutionConverter(5)))

    def setTitleFont(self, font):
        self.titleFont = font

    def setPriceFont(self, font):
        self.priceFont = font

    def setDescriptionFont(self, font):
        self.descriptionFont = font
