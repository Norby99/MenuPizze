from libraries.cells.pizzaCell import PizzaCell
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
