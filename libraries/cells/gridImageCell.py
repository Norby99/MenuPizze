from libraries.cells.gridCell import Cell
import tkinter as tk
from PIL import Image 

class ImageCell(Cell):
    """
    This cell contains the logo of the Pizzeria
    """
    def __init__(self, window, image, position, width, proportion=1):
        super().__init__(window, position, width, proportion)
        resizeFormat = (image.width(), image.height())
        print(resizeFormat)
        self.image = image._PhotoImage__photo.zoom(1)

        self.showImage()

    def showImage(self):
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)
