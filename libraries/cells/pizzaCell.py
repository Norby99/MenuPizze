from libraries.cells.subtitlePriceCell import SubtitlePriceCell
import tkinter as tk
import tkinter.font as TkFont

class PizzaCell(SubtitlePriceCell):
    """
    This cell contains:
    - pizza name
    - price
    - ingredients
    - allergens
    """
    def __init__(self, window, name, nameColor, price, priceColor, ingredients, ingredientsColor, allergens, position, width, proportion=5.76):
        self.allergens = allergens
        if self.allergens:
            self.allergensImageSize = self.allergens[0].width()

        super().__init__(window, name, nameColor, price, priceColor, ingredients, ingredientsColor, position, width, proportion)

        # draw red background
        """ self.width = width
        self.height = self.width / proportion
        self.canvas.create_rectangle(self.position[0], self.position[1], self.position[0]+self.width, self.position[1]+self.height, fill="#a86032", outline="#a86032") """

        self.showAllergeni()

    def showAllergeni(self):
        for i, allergen in enumerate(self.allergens):
            allergenSpacing = i*(self.allergensImageSize+self.windowSpecs.resolutionConverter(5))
            self.canvas.create_image(self.textNamePos[0]+self.titleFont.measure(self.title)+self.windowSpecs.resolutionConverter(5)+allergenSpacing, self.textNamePos[1]+self.windowSpecs.resolutionConverter(5), anchor=tk.NW, image=allergen)

    def update(self, language):
        self.canvas.itemconfig(self.textDescription, text=self.description[language])
