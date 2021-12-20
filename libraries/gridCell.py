from libraries.windowSpecs import WindowSpecs
import tkinter as tk
from abc import ABC

class Cell(ABC):

    def __init__(self, window, position, dimensions):
        """screenDim is an object that is used to avoid creating a tkinter class every time"""
        self.position = position
        self.dimensions = dimensions
        self.window = window
        self.canvas = tk.Canvas(self.window, bg=window["background"], width=dimensions[0], height=dimensions[1], highlightthickness=0, bd=0)
        self.canvas.place(x=position[0], y=position[1], anchor=tk.NW)
        self.windowSpecs = WindowSpecs(self.window.winfo_screenwidth(), self.window.winfo_screenheight())   # to increase performance
