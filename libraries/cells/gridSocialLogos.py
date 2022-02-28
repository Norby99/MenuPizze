from libraries.cells.gridCell import Cell
import tkinter as tk
from PIL import ImageTk,Image 
import math

class SocialLogos(Cell):
    """
    This cell contains the logo of the Pizzeria
    @param logos is an array of PIL images
    """
    def __init__(self, window, logos, position, width, proportion=5):
        super().__init__(window, position, width, proportion)

        self.social_logos = []
        image_size = 4/5    # represents the size of the image compared to the cell size 
        for image in logos:
            new_image_height = math.trunc(width / proportion * image_size)
            new_image_width = math.trunc(image.size[0] * new_image_height / image.size[1])

            self.social_logos.append(ImageTk.PhotoImage(image.resize((new_image_width, new_image_height), Image.ANTIALIAS)))

        self.showImage()

    def showImage(self):
        for logo in self.social_logos:
            center = (self.dimensions[0]/2, self.dimensions[1]/2)
            self.canvas.create_image(center[0], center[1], image=logo, anchor=tk.CENTER)
