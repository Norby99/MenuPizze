from libraries.gridCell import Cell
import tkinter as tk

class PizzaCell(Cell):
    """
    This cell contains:
    - pizza name
    - price
    - ingredients
    - allergens
    """
    def __init__(self, canvas, name, nameColor, price, priceColor, ingredients, ingredientsColor, position, dimensions):
        super().__init__(canvas, position, dimensions)
        self.name = name    # name setup
        self.nameColor = nameColor
        self.nameFont = "Times " + str(self.windowSpecs.resolutionConverter(20)) + " bold"
        self.price = price  # price setup
        self.priceColor = priceColor
        self.pricFont = "Times " + str(self.windowSpecs.resolutionConverter(18)) + " bold"
        self.ingredients = ingredients  # ingredients setup
        self.ingredientsColor = ingredientsColor
        self.ingredientsFont = "Times " + str(self.windowSpecs.resolutionConverter(15))

    def setnameFont(self, font):
        self.nameFont = font

    def setpricFont(self, font):
        self.pricFont = font

    def setingredientsFont(self, font):
        self.ingredientsFont = font