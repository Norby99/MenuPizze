from libraries.gridCell import Cell
import tkinter as tk

class TitleCell(Cell):
    """ This cell contains a big title and a border """

    def __init__(self, canvas, title, textColor, position, dimensions, winInfo=False):
        super().__init__(canvas, position, dimensions, winInfoBase=winInfo)
        self.title = title
        self.textColor = textColor
        self.font = "Times " + str(self.windowSpecs.resolutionConverter(36)) + " bold"
        self.createTitle()
        self.setBorders()

    def createTitle(self):
        shadowPosition = 3

        self.canvas.create_text(self.relativeXPostion(5)+shadowPosition, self.relativeYPostion(-self.windowSpecs.resolutionConverter(25))+shadowPosition, anchor= tk.SW, fill="#BBBBBB", font=self.font, text=self.title) # shadow text
        self.canvas.create_text(self.relativeXPostion(5)+1, self.relativeYPostion(-self.windowSpecs.resolutionConverter(25))+1, anchor= tk.SW, fill="#000000", font=self.font, text=self.title) # outer outline
        self.canvas.create_text(self.relativeXPostion(5)-1, self.relativeYPostion(-self.windowSpecs.resolutionConverter(25))-1, anchor= tk.SW, fill="#000000", font=self.font, text=self.title) # inner outline
        self.canvas.create_text(self.relativeXPostion(5), self.relativeYPostion(-self.windowSpecs.resolutionConverter(25)), anchor= tk.SW, fill=self.textColor, font=self.font, text=self.title) # text body

    def setBorders(self):
        self.canvas.create_line(self.relativeXPostion(0), self.relativeYPostion(0), self.relativeXPostion(-1)-self.windowSpecs.resolutionConverter(40), self.relativeYPostion(0), fill="#ff8000", width="3")
        self.canvas.create_line(self.relativeXPostion(0), self.relativeYPostion(-1)-self.windowSpecs.resolutionConverter(15), self.relativeXPostion(-1)-self.windowSpecs.resolutionConverter(40), self.relativeYPostion(-1)-self.windowSpecs.resolutionConverter(15), fill="#ff8000", width="3")

    def setFont(self, font):
        self.font = font
