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
    def __init__(self, window, name, nameColor, price, priceColor, ingredients, ingredientsColor, position, dimensions):
        super().__init__(window, position, dimensions)
        self.name = name    # name setup
        self.nameColor = nameColor
        self.nameFont = "Times " + str(self.windowSpecs.resolutionConverter(20)) + " bold"
        self.price = price  # price setup
        self.priceColor = priceColor
        self.priceFont = "Times " + str(self.windowSpecs.resolutionConverter(18)) + " bold"
        self.ingredients = ingredients  # ingredients setup
        self.ingredientsColor = ingredientsColor
        self.ingredientsFont = "Times " + str(self.windowSpecs.resolutionConverter(14))

        self.createName()
        self.createPrice()
        self.createIngredients()

    def createName(self):
        self.textName = self.canvas.create_text(self.windowSpecs.resolutionConverter(5), 0, anchor= tk.NW, fill=self.nameColor,font=self.nameFont, text=self.name)

    def createPrice(self):
        self.textPrice = self.canvas.create_text(self.dimensions[0]-self.windowSpecs.resolutionConverter(10), self.windowSpecs.resolutionConverter(5), anchor= tk.NE, fill=self.priceColor,font=self.priceFont, text=self.price)

    def createIngredients(self):
        self.textIngredients = self.canvas.create_text(self.windowSpecs.resolutionConverter(5), self.dimensions[1]/2-self.windowSpecs.resolutionConverter(13), anchor= tk.NW, fill=self.ingredientsColor,font=self.ingredientsFont, text=next(iter(self.ingredients)), width=(self.dimensions[0]-self.windowSpecs.resolutionConverter(5)))

    def setNameFont(self, font):
        self.nameFont = font

    def setPriceFont(self, font):
        self.priceFont = font

    def setIngredientsFont(self, font):
        self.ingredientsFont = font

    def update(self, language):
        self.canvas.itemconfig(self.textIngredients, text=self.ingredients[language])
