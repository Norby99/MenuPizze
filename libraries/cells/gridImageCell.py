from libraries.cells.gridCell import Cell
import tkinter as tk
from PIL import ImageTk,Image 
import math

class ImageCell(Cell):
    """
    This cell contains the logo of the Pizzeria
    @param image is a PIL image
    """
    def __init__(self, window, image, position, width, proportion=1):
        super().__init__(window, position, width, proportion)
        image_size = 4/5    # represents the size of the image compared to the cell size 
        new_image_width = math.trunc(width * image_size)
        new_image_height = math.trunc(image.size[1] * new_image_width / image.size[0])
        self.image = ImageTk.PhotoImage(image.resize((new_image_width, new_image_height), Image.ANTIALIAS))

        self.showImage()

    def showImage(self):
        center = (self.dimensions[0]/2, self.dimensions[1]/2)
        self.canvas.create_image(center[0], center[1], image=self.image, anchor=tk.CENTER)
