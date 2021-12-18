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
        self.priceFont = "Times " + str(self.windowSpecs.resolutionConverter(18)) + " bold"
        self.ingredients = ingredients  # ingredients setup
        self.ingredientsColor = ingredientsColor
        self.ingredientsFont = "Times " + str(self.windowSpecs.resolutionConverter(15))

        self.createName()
        self.createPrice()
        self.createIngredients()

    def createName(self):
        self.canvas.create_text(self.relativeXPostion(self.windowSpecs.resolutionConverter(5)), self.relativeYPostion(self.windowSpecs.resolutionConverter(5)), anchor= tk.NW, fill=self.nameColor,font=self.nameFont, text=self.name)

    def createPrice(self):
        self.canvas.create_text(self.relativeXPostion(-self.windowSpecs.resolutionConverter(10)), self.relativeYPostion(self.windowSpecs.resolutionConverter(10)), anchor= tk.NE, fill=self.priceColor,font=self.priceFont, text=self.price)

    def createIngredients(self):
        self.canvas.create_text(self.relativeXPostion(self.windowSpecs.resolutionConverter(5)), (self.relativeYPostion(-1)+self.relativeYPostion(0))/2-self.windowSpecs.resolutionConverter(10), anchor= tk.NW, fill=self.ingredientsColor,font=self.ingredientsFont, text=self.ingredients, width=(self.dimensions[0]-self.windowSpecs.resolutionConverter(10)))

    def setNameFont(self, font):
        self.nameFont = font

    def setPriceFont(self, font):
        self.priceFont = font

    def setIngredientsFont(self, font):
        self.ingredientsFont = font