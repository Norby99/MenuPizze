from libraries.cells.gridCell import Cell
import tkinter as tk
import math

class ImageCell(Cell):
    """
    This cell contains the logo of the Pizzeria
    """
    def __init__(self, window, image, position, width, proportion=1):
        super().__init__(window, position, width, proportion)
        resizeFormat = int(math.ceil(image.width()/width))
        self.image = image._PhotoImage__photo.subsample(resizeFormat)

        self.showImage()

    def showImage(self):
        center = (self.dimensions[0]/2, self.dimensions[1]/2)
        self.canvas.create_image(center[0], center[1], image=self.image, anchor=tk.CENTER)
