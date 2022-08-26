from libraries.utils.windowSpecs import WindowSpecs
import tkinter as tk
from abc import ABC

class Cell(ABC):

    def __init__(self, window, position, width, proportion):
        """
        window is the tkinter root object
        given a width it calculates it's hight by the given proportion
        """
        self.position = position
        self.proportion = proportion
        self.dimensions = [width, width/self.proportion]
        self.window = window
        self.canvas = tk.Canvas(self.window, bg=window["background"], width=self.dimensions[0], height=self.dimensions[1], highlightthickness=0, bd=0)
        self.canvas.place(x=position[0], y=position[1], anchor=tk.NW)
        self.windowSpecs = WindowSpecs([self.window.winfo_screenwidth(), self.window.winfo_screenheight()])   # to increase performance

    def getBottomCoordinate(self):
        return self.position[1]+self.dimensions[1]

    def getRightCoordinate(self):
        return self.position[0]+self.dimensions[0]

    def getWidth(self):
        return self.dimensions[0]

    def getHeight(self):
        return self.dimensions[1]

    def setPostion(self, coord):
        self.position = coord
        self.canvas.place(x=self.position[0], y=self.position[1], anchor=tk.NW)
