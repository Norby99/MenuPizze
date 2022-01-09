from libraries.cells.gridCell import Cell
import tkinter as tk
import tkinter.font as TkFont

class AllergeniCell(Cell):
    """ This cell contains the legend of Allergens """

    def __init__(self, window, allergen, textColor, position, width, proportion=13):
        super().__init__(window, position, width, proportion=proportion)
        self.backGroundColor = window["background"]

        allergens = allergen["first"] + allergen["second"]

        self.textColor = textColor
        self.font = TkFont.Font(family="Times", size=self.windowSpecs.resolutionConverter(15), weight='bold')

        self.createText(allergens[0])
        self.createText(allergens[2], left=False)
        self.createImages(allergens[1])
        self.createImages(allergens[3], left=False)

    def createText(self, text, left=True):
        """
        Positions a text to left or right center of the canvas
        @text is the text to be shown
        @left if true, positions the text to the center left part of the screen
        """
        center = [self.dimensions[0]*3/4, self.dimensions[1]/2]

        if left:
            center[0] /= 3
        self.textName =  self.canvas.create_text(center[0], center[1], anchor= tk.CENTER, fill=self.textColor, font=self.font, text=text)

    def createImages(self, image, left=True):
        """
        Positions an image to left or right center of the canvas
        @image is the image to be shown
        @left if true, positions the image to the center left part of the screen
        """
        center = self.dimensions[0]/2, self.dimensions[1]/2
        sideOffset = self.windowSpecs.resolutionConverter(10)
        sideAnchor = tk.W
        
        if left:
            sideOffset *= -1
            sideAnchor = tk.E
        self.canvas.create_image(center[0]+sideOffset, center[1], anchor=sideAnchor, image=image)

    def setAllergensFontFont(self, font):
        self.font = font
