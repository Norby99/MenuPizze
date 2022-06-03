from libraries.cells.AbstractCell import Cell
import tkinter as tk
import tkinter.font as TkFont

class SimpleTextCell(Cell):

    __text: str
    __text_color: str

    def __init__(self, window, text, text_color, text_font, position, width, proportion=5.76):
        super().__init__(window, position, width, proportion)

        self.__text = text
        self.__text_color = text_color
        self.font = TkFont.Font(family="Times", size=self.windowSpecs.resolutionConverter(text_font), weight='bold')

        self.create_text()

    def create_text(self):
        sr = self.windowSpecs.resolutionConverter

        self.canvas.create_text(self.dimensions[0]/2, self.dimensions[1]/2, anchor=tk.CENTER, fill=self.__text_color, font=self.font, text=self.__text)
