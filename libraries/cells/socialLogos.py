from libraries.cells.AbstractCell import Cell
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

            self.social_logos.append(ImageTk.PhotoImage(image.resize((new_image_width, new_image_height), Image.LANCZOS)))

        self.showImage()

    def showImage(self):
        n_logos = len(self.social_logos)
        position = [0, self.dimensions[1]/2]
        for i, logo in enumerate(self.social_logos):
            position[0] = self.dimensions[0]/n_logos*(i+1/2)    # finds the x position of each image
            self.canvas.create_image(position[0], position[1], image=logo, anchor=tk.CENTER)
