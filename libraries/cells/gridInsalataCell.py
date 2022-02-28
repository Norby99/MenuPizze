from libraries.cells.gridPizzaCell import PizzaCell
import tkinter as tk
import tkinter.font as TkFont

class InsalataCell(PizzaCell):
    """
    This cell contains:
    - insalata name
    - price
    - ingredients
    - allergens
    """
    def __init__(self, window, name, nameColor, price, priceColor, ingredients, ingredientsColor, allergens, position, width, proportion=5.76):
        super().__init__(window, name, nameColor, price, priceColor, ingredients, ingredientsColor, allergens, position, width, proportion=proportion)
        self.allergens = allergens
        if self.allergens:
            self.allergensImageSize = self.allergens[0].width()

        self.createName()
        self.createPrice()
        self.createIngredients()
        self.showAllergeni()
