from libraries.gridCell import Cell
import tkinter as tk

class TitleCell(Cell):
    """ This cell contains a big title and a border """

    def __init__(self, window, title, textColor, position, dimensions, winInfo=False):
        super().__init__(window, position, dimensions, winInfoBase=winInfo)
        self.title = title
        self.textColor = textColor
        self.font = "Times " + str(self.windowSpecs.resolutionConverter(36)) + " bold"
        self.createTitle()
        self.setBorders()

    def createTitle(self):
        shadowPosition = 3
        sr = self.windowSpecs.resolutionConverter

        self.canvas.create_text(sr(5)+shadowPosition, self.dimensions[1]-sr(25)+shadowPosition, anchor= tk.SW, fill="#BBBBBB", font=self.font, text=self.title) # shadow text
        self.canvas.create_text(sr(5)+1, self.dimensions[1]-sr(25)+1, anchor= tk.SW, fill="#000000", font=self.font, text=self.title) # outer outline
        self.canvas.create_text(sr(5)-1, self.dimensions[1]-sr(25)-1, anchor= tk.SW, fill="#000000", font=self.font, text=self.title) # inner outline
        self.canvas.create_text(sr(5), self.dimensions[1]-sr(25), anchor= tk.SW, fill=self.textColor, font=self.font, text=self.title) # text body

    def setBorders(self):
        self.canvas.create_line(0, 0, self.dimensions[0]-self.windowSpecs.resolutionConverter(40), 0, fill="#ff8000", width="3")
        self.canvas.create_line(0, self.dimensions[1]-self.windowSpecs.resolutionConverter(15), self.dimensions[0]-self.windowSpecs.resolutionConverter(40), self.dimensions[1]-self.windowSpecs.resolutionConverter(15), fill="#ff8000", width="3")

    def setFont(self, font):
        self.font = font
