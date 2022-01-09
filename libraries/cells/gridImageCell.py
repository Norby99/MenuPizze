from libraries.cells.gridCell import Cell
import tkinter as tk
import tkinter.font as TkFont

#? Note that i only tested this class with vecotial images. I don't know if it works with scalar images too

class ImageCell(Cell):
    """
    This cell contains the logo of the Pizzeria
    """
    def __init__(self, window, image, position, width, proportion=1):
        super().__init__(window, position, width, proportion)
